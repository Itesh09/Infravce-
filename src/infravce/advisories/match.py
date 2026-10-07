"""Match observations to advisories using applicability engine with precedence."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from infravce.applicability.engine import decide
from infravce.models import (
    AdvisorySource,
    Applicability,
    ApplicabilityVerdict,
    Ecosystem,
    Justification,
    Observation,
    RangeRepresentation,
)

from .ingest import AdvisoryRecord


@dataclass(frozen=True, slots=True)
class ApplicabilityVote(Applicability):
    pass


def match_observations(
    observations: list[Observation],
    advisories: list[AdvisoryRecord],
) -> list[Applicability]:
    from infravce.applicability.comparators import compare_versions
    from infravce.applicability.engine import decide

    votes: list[Applicability] = []
    for o in observations:
        if not o.is_usable_for_matching:
            continue
        prod = (o.resolved_product or o.raw_product).lower()
        o_ver = o.resolved_version
        o_ver_raw = o_ver.raw if o_ver else o.raw_version
        o_ecos = o_ver.ecosystem.value if o_ver else "unknown"
        for a in advisories:
            if (a.product or "").lower() != prod:
                continue
            # also try to match by version in advisory if specified
            a_vers = [str(x) for x in a.versions]
            ver_match = True
            if a_vers:
                ver_match = any(str(x) == o_ver_raw or str(x) == (o.raw_version or "") for x in a_vers)
            if a_vers and not ver_match:
                continue  # exact version in case doesn't match observation version? let us be precise to observation
            installed = o_ver_raw
            fixed = a.fixed_version
            try:
                outcome = decide(
                    installed=installed,
                    fixed_version=fixed,
                    distro_state=a.distro_state,
                    ecosystem=o_ver.ecosystem.value if o_ver else "unknown",
                )
                rep = RangeRepresentation.UNKNOWN
                v = Applicability(
                    observation_id=o.observation_id,
                    advisory_source=a.source,
                    advisory_id=a.advisory_id,
                    range_representation=rep,
                    verdict=outcome.verdict,
                    evidence=outcome.reason or f"{a.advisory_id} matches {prod}",
                    evaluated_at=datetime.now(UTC),
                )
                votes.append(v)
                continue
            except Exception:
                pass
            try:
                if fixed and installed:
                    c = compare_versions(installed, fixed)
                    if c < 0:
                        verdict = ApplicabilityVerdict.AFFECTED
                        ev = f"{installed} < fixed {fixed}"
                    elif c >= 0:
                        verdict = ApplicabilityVerdict.FIXED
                        ev = f"{installed} >= fixed {fixed}"
                    else:
                        verdict = ApplicabilityVerdict.UNDER_INVESTIGATION
                        ev = "comparison indeterminate"
                    v = Applicability(
                        observation_id=o.observation_id,
                        advisory_source=a.source,
                        advisory_id=a.advisory_id,
                        range_representation=RangeRepresentation.UNKNOWN,
                        verdict=verdict,
                        evidence=ev,
                        evaluated_at=datetime.now(UTC),
                    )
                    votes.append(v)
                    continue
            except Exception:
                pass
            v = Applicability(
                observation_id=o.observation_id,
                advisory_source=a.source,
                advisory_id=a.advisory_id,
                range_representation=RangeRepresentation.UNKNOWN,
                verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
                evidence=f"advisory {a.advisory_id} matches product {prod}",
                evaluated_at=datetime.now(UTC),
            )
            votes.append(v)
    return votes
