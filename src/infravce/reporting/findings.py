"""Turn votes into graded findings.

Three rules, each of which the previous implementation got wrong:

1. **A finding is an ``affected`` claim, not any vote.** Emitting a finding for
   ``not_affected`` inflated the report with rows that say nothing is wrong.
   Non-affected verdicts stay in the votes for the dissent metric, not in the
   findings list.
2. **The winning vote follows source precedence.** A distribution saying
   ``not-affected`` outranks an upstream range saying ``affected``; if the
   winning verdict is not ``affected`` there is no finding, whatever the
   minority said.
3. **A tier is earned, not assumed.** ``VERIFIED`` requires both an independently
   confirmed version and corroboration by a second advisory source. A single
   banner plus a single feed is ``INFERRED`` at best, and a bare NVD range is
   ``WEAK``.
"""

from __future__ import annotations

import json
from pathlib import Path

from infravce.models import (
    AdvisorySource,
    Applicability,
    ApplicabilityVerdict,
    ConfidenceTier,
    Finding,
    Observation,
)
from infravce.prioritise.scorer import score_finding

__all__ = ["build_findings", "write_findings", "tier_for"]

#: Sources whose version statements are authoritative for OS packages.
_STRONG_SOURCES = {AdvisorySource.DISTRO_TRACKER, AdvisorySource.VENDOR_ADVISORY}
#: Sources whose version statements are known to be unreliable for backports.
_WEAK_SOURCES = {AdvisorySource.NVD, AdvisorySource.UNKNOWN}


def tier_for(
    votes: list[Applicability],
    *,
    has_verification: bool,
    has_corroboration: bool,
) -> ConfidenceTier:
    """Grade the strongest ``affected`` claim in ``votes``."""
    affected = [v for v in votes if v.verdict is ApplicabilityVerdict.AFFECTED]
    if not affected:
        return ConfidenceTier.UNRESOLVED

    best = min(affected, key=lambda v: (v.precedence_rank, -v.evaluated_at.timestamp()))
    strong_source = best.advisory_source in _STRONG_SOURCES

    # A comparison that had to drop the distribution revision is an
    # approximation regardless of how authoritative the source is. It can be
    # ordered, but it must not be presented as verified.
    if all(v.evidence_quality == "approximate" for v in affected):
        return ConfidenceTier.INFERRED if has_verification else ConfidenceTier.WEAK

    if has_verification and has_corroboration:
        return ConfidenceTier.VERIFIED
    if has_corroboration and strong_source:
        return ConfidenceTier.STRONGLY_INFERRED
    if has_verification and strong_source:
        return ConfidenceTier.STRONGLY_INFERRED
    if has_verification or best.advisory_source not in _WEAK_SOURCES:
        return ConfidenceTier.INFERRED
    return ConfidenceTier.WEAK


#: Backwards-compatible private name.
_tier_from_votes = tier_for


def _winning(votes: list[Applicability]) -> Applicability:
    return min(votes, key=lambda v: (v.precedence_rank, -v.evaluated_at.timestamp()))


def build_findings(
    observations: list[Observation],
    votes: list[Applicability],
    *,
    corroborated: dict[str, bool] | None = None,
    verified: dict[str, bool] | None = None,
) -> list[Finding]:
    by_observation: dict[str, list[Applicability]] = {}
    for vote in votes:
        by_observation.setdefault(vote.observation_id, []).append(vote)

    observations_by_id = {o.observation_id: o for o in observations}

    groups: dict[tuple[str, str], list[tuple[Observation, Applicability]]] = {}
    for observation_id, observation_votes in by_observation.items():
        observation = observations_by_id.get(observation_id)
        if observation is None:
            continue
        for vote in observation_votes:
            groups.setdefault((observation.asset_id, vote.advisory_id), []).append(
                (observation, vote)
            )

    findings: list[Finding] = []
    for (asset_id, cve_id), items in groups.items():
        vote_list = [v for _, v in items]
        winner = _winning(vote_list)
        if winner.verdict is not ApplicabilityVerdict.AFFECTED:
            # The highest-precedence source does not claim this asset is
            # affected. A minority dissent is recorded in the votes but is not
            # promoted to a finding.
            continue

        observation_list = list({o.observation_id: o for o, _ in items}.values())
        has_ver = any(bool(verified and verified.get(o.observation_id)) for o in observation_list)
        has_corr = any(
            bool(corroborated and corroborated.get(o.observation_id)) for o in observation_list
        )
        tier = tier_for(vote_list, has_verification=has_ver, has_corroboration=has_corr)

        sources = sorted({v.advisory_source.value for v in vote_list})
        notes = [
            note
            for note in dict.fromkeys(
                [
                    f"{len(vote_list)} vote(s) from {len(sources)} source(s)",
                    "dissent present" if len({v.verdict.value for v in vote_list}) > 1 else "",
                    "" if has_ver else "version not independently confirmed",
                    "" if has_corr else "single advisory source",
                ]
            )
            if note
        ]
        finding = Finding(
            asset_id=asset_id,
            cve_id=cve_id,
            confidence_tier=tier,
            severity=winner.severity,
            cvss=winner.cvss,
            summary=winner.summary,
            aliases=winner.aliases,
            fix_available=winner.fix_available,
            supporting_observations=tuple(observation_list),
            applicability_votes=tuple(vote_list),
            evidence_bundle={
                "winning_source": winner.advisory_source.value,
                "winning_evidence": winner.evidence,
                "sources": sources,
                "vote_count": len(vote_list),
                "has_dissent": len({v.verdict.value for v in vote_list}) > 1,
                "version_verified": has_ver,
                "source_corroborated": has_corr,
                "observations": [
                    {
                        "observation_id": o.observation_id,
                        "method": o.acquisition_method.value,
                        "asset_id": o.asset_id,
                        "raw_product": o.raw_product,
                        "raw_version": o.raw_version,
                        "resolution_confidence": o.resolution_confidence,
                        "evidence": o.evidence,
                    }
                    for o in observation_list
                ],
            },
            notes=tuple(notes),
        )
        score, breakdown = score_finding(finding)
        finding.priority_score = score
        finding.priority_breakdown = breakdown
        findings.append(finding)

    findings.sort(
        key=lambda f: (
            -(f.priority_score or 0.0),
            f.confidence_tier.value,
            f.asset_id,
            f.cve_id,
        )
    )
    return findings


def write_findings(findings: list[Finding], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    data = [f.model_dump(mode="json") for f in findings]
    out.write_text(json.dumps(data, indent=2) + "\n")
