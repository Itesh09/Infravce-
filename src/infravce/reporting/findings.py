"""Emit findings with evidence bundles and confidence tiers."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from infravce.models import (
    Applicability,
    ConfidenceTier,
    Finding,
    Observation,
)


def _tier_from_votes(votes: list[Applicability], has_verification: bool = False, has_corroboration: bool = False) -> ConfidenceTier:
    if not votes:
        return ConfidenceTier.UNRESOLVED
    verdicts = {v.verdict for v in votes}
    if has_verification:
        return ConfidenceTier.VERIFIED
    if has_corroboration and len(verdicts) > 1:
        return ConfidenceTier.STRONGLY_INFERRED
    if has_corroboration or len(votes) >= 1:
        return ConfidenceTier.INFERRED
    return ConfidenceTier.WEAK


def build_findings(
    observations: list[Observation],
    votes: list[Applicability],
    *,
    corroborated: dict[str, bool] | None = None,
    verified: dict[str, bool] | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    # map obs -> votes
    by_obs: dict[str, list[Applicability]] = {}
    for v in votes:
        by_obs.setdefault(v.observation_id, []).append(v)

    # build lookup for observations
    obs_by_id = {o.observation_id: o for o in observations}

    # group votes by (asset_id, cve_id) derived from observation + vote
    groups: dict[tuple[str, str], list[tuple[Observation, Applicability]]] = {}
    for obs_id, ovlist in by_obs.items():
        o = obs_by_id.get(obs_id)
        if o is None:
            continue
        for v in ovlist:
            key = (o.asset_id, v.advisory_id)
            groups.setdefault(key, []).append((o, v))

    for (asset_id, cve_id), items in groups.items():
        # collect unique observations and votes
        obs_list = []
        seen_o = set()
        for o, v in items:
            if o.observation_id not in seen_o:
                obs_list.append(o)
                seen_o.add(o.observation_id)
        vote_list = [v for _, v in items]
        obs_id_ref = obs_list[0].observation_id if obs_list else items[0][1].observation_id
        has_corr = corroborated.get(obs_id_ref, False) if corroborated else False
        has_ver = verified.get(obs_id_ref, False) if verified else False
        f = Finding(
            asset_id=asset_id,
            cve_id=cve_id,
            confidence_tier=_tier_from_votes(vote_list, has_verification=has_ver, has_corroboration=has_corr),
            supporting_observations=tuple(obs_list),
            applicability_votes=tuple(vote_list),
            evidence_bundle={
                "observation_id": obs_id_ref,
                "raw": {"product": obs_list[0].raw_product, "version": obs_list[0].raw_version} if obs_list else {},
                "winning_vote": vote_list[0].model_dump(mode="json") if vote_list else None,
            },
        )
        findings.append(f)
    return findings


def write_findings(findings: list[Finding], out: Path) -> None:
    data = [f.model_dump(mode="json") for f in findings]
    out.write_text(json.dumps(data, indent=2) + "\n")
