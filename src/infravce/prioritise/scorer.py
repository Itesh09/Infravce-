"""Multi-signal scoring with a visible breakdown.

Every term is reported separately so a reviewer can disagree with the ranking
without having to reverse-engineer it. Two consequences of that requirement:

* **A missing signal is 0.0 and visible**, never silently omitted. There is no
  EPSS/KEV ingester in this MVP, so those terms are present and zero rather than
  pretending they were considered.
* **Severity is not applicability.** A critical CVSS contributes to *ordering*
  only; it can never turn a ``not_affected`` verdict into a finding. That
  separation happens in :mod:`infravce.reporting.findings`.
"""

from __future__ import annotations

from dataclasses import dataclass

from infravce.models import ConfidenceTier, Finding

__all__ = ["SignalScores", "score_finding"]

_CONFIDENCE = {
    ConfidenceTier.VERIFIED: 1.0,
    ConfidenceTier.STRONGLY_INFERRED: 0.8,
    ConfidenceTier.INFERRED: 0.55,
    ConfidenceTier.WEAK: 0.25,
    ConfidenceTier.UNRESOLVED: 0.0,
}

_SEVERITY = {
    "critical": 1.0,
    "high": 0.8,
    "important": 0.8,
    "moderate": 0.55,
    "medium": 0.55,
    "low": 0.25,
    "negligible": 0.1,
}

#: Weights sum to 1.0. The two signals that are actually wired in this MVP carry
#: 0.85 of the score; the rest are placeholders whose zero contribution is
#: printed rather than hidden.
_WEIGHTS = {
    "severity": 0.55,
    "confidence": 0.30,
    "kev": 0.05,
    "epss": 0.05,
    "exposure": 0.05,
}


@dataclass(frozen=True, slots=True)
class SignalScores:
    kev: float = 0.0
    epss: float = 0.0
    exposure: float = 0.0
    criticality: float = 0.0
    blast_radius: float = 0.0
    cvss: float = 0.0

    def as_dict(self) -> dict[str, float]:
        return {
            "kev": self.kev,
            "epss": self.epss,
            "exposure": self.exposure,
            "criticality": self.criticality,
            "blast_radius": self.blast_radius,
            "cvss": self.cvss,
        }


def _severity_norm(finding: Finding) -> float:
    if finding.cvss is not None:
        return max(0.0, min(1.0, finding.cvss / 10.0))
    if finding.severity:
        return _SEVERITY.get(finding.severity.strip().lower(), 0.0)
    return 0.0


def score_finding(finding: Finding) -> tuple[float, dict[str, float]]:
    """Return a 0-100 priority score and the contribution of each term."""
    severity = _severity_norm(finding)
    confidence = _CONFIDENCE.get(finding.confidence_tier, 0.0)
    signals = SignalScores(
        kev=0.0,
        epss=0.0,
        exposure=float(finding.evidence_bundle.get("exposure_score", 0.0) or 0.0),
        criticality=0.0,
        blast_radius=0.0,
        cvss=severity,
    )

    contributions = {
        "severity": 100.0 * _WEIGHTS["severity"] * severity,
        "confidence": 100.0 * _WEIGHTS["confidence"] * confidence,
        "kev": 100.0 * _WEIGHTS["kev"] * signals.kev,
        "epss": 100.0 * _WEIGHTS["epss"] * signals.epss,
        "exposure": 100.0 * _WEIGHTS["exposure"] * signals.exposure,
    }
    # Declared-but-unwired signals are reported at their true value (zero) so the
    # breakdown stays a complete account of the score.
    contributions["criticality"] = 0.0
    contributions["blast_radius"] = 0.0
    score = round(sum(contributions.values()), 2)
    return score, {k: round(v, 2) for k, v in contributions.items()}
