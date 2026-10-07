"""Multi-signal scoring with visible breakdown."""
from __future__ import annotations

from dataclasses import dataclass

from infravce.models import Finding


@dataclass(frozen=True, slots=True)
class SignalScores:
    kev: float = 0.0
    epss: float = 0.0
    exposure: float = 0.0
    criticality: float = 0.0
    blast_radius: float = 0.0
    cvss: float = 0.0


def score_finding(f: Finding) -> tuple[float, dict[str, float]]:
    breakdown = {
        "kev": 0.0,
        "epss": 0.0,
        "exposure": 0.0,
        "criticality": 0.0,
        "blast_radius": 0.0,
        "cvss": 0.0,
    }
    score = 0.0
    if f.confidence_tier.value == "verified":
        score += 0.5
    elif f.confidence_tier.value == "inferred":
        score += 0.3
    elif f.confidence_tier.value == "strongly_inferred":
        score += 0.4
    elif f.confidence_tier.value == "weak":
        score += 0.1
    breakdown["confidence"] = score
    return score, breakdown
