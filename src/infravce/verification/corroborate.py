"""Corroboration: independent advisory sources agreeing on the same verdict.

Corroboration is counted per **source**, not per record. Ten Debian records are
one source's opinion, not ten confirmations; counting records would let a single
feed manufacture a high confidence tier simply by publishing many entries for the
same CVE. That is the same aggregation error the cross-tool literature
(``docs/04``) identifies when tool agreement is measured without accounting for
shared upstream databases.

A dissenting higher-precedence source blocks corroboration even when several
lower-precedence sources agree: per principle P3, a distribution saying
``not-affected`` outranks any number of upstream ranges saying otherwise.
"""

from __future__ import annotations

from collections import defaultdict

from infravce.models import Applicability, ApplicabilityVerdict, Observation

__all__ = ["corroborate", "source_agreement"]


def source_agreement(votes: list[Applicability]) -> dict[str, dict[str, int]]:
    """Per observation, how many distinct sources said what."""
    tally: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    seen: set[tuple[str, object, str]] = set()
    for vote in votes:
        key = (vote.observation_id, vote.advisory_source, vote.advisory_id)
        if key in seen:
            continue
        seen.add(key)
        tally[vote.observation_id][vote.verdict.value] += 1
    return {obs: dict(counts) for obs, counts in tally.items()}


def corroborate(
    observations: list[Observation],
    votes: list[Applicability],
) -> dict[str, bool]:
    """Mark an observation corroborated when sources independently agree.

    ``affected`` corroboration requires two distinct sources asserting
    ``affected``. A single source, however many records it contributed, is not
    corroboration.
    """
    by_observation: dict[str, list[Applicability]] = defaultdict(list)
    for vote in votes:
        by_observation[vote.observation_id].append(vote)

    result: dict[str, bool] = {}
    for observation in observations:
        observation_votes = by_observation.get(observation.observation_id, [])
        if not observation_votes:
            result[observation.observation_id] = False
            continue

        affected_sources = {
            v.advisory_source
            for v in observation_votes
            if v.verdict is ApplicabilityVerdict.AFFECTED
        }
        dissenting = [
            v
            for v in observation_votes
            if v.verdict is ApplicabilityVerdict.NOT_AFFECTED
            and v.advisory_source in affected_sources
        ]
        result[observation.observation_id] = len(affected_sources) >= 2 and not dissenting
    return result
