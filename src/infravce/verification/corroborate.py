"""Corroboration: multi-source identity agreement (minimal)."""
from __future__ import annotations

from infravce.models import Applicability, Observation


def corroborate(
    observations: list[Observation],
    votes: list[Applicability],
) -> dict[str, bool]:
    by_obs = {v.observation_id for v in votes}
    return {o.observation_id: o.is_usable_for_matching and o.observation_id in by_obs for o in observations}
