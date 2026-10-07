"""Safe, read-only verification checks (non-destructive)."""
from __future__ import annotations

from infravce.models import Observation


def safe_verify(observations: list[Observation]) -> dict[str, bool]:
    res = {}
    for o in observations:
        res[o.observation_id] = o.is_usable_for_matching
    return res
