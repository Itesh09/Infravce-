"""Human-review queue ordered by expected information gain (not severity)."""
from __future__ import annotations

import json
from pathlib import Path

from infravce.models import Finding


def build_queue(findings: list[Finding]) -> list[Finding]:
    def gain(f: Finding) -> tuple[int, float, float]:
        tier_order = {
            "unresolved": 0,
            "weak": 1,
            "inferred": 2,
            "strongly_inferred": 3,
            "verified": 4,
        }
        t = tier_order.get(f.confidence_tier.value, 5)
        ps = -(f.priority_score or 0.0)
        # deterministic tie-breaker by cve+asset
        return (t, ps, hash((f.cve_id, f.asset_id)))
    return sorted(findings, key=gain)


def write_queue(findings: list[Finding], out: Path) -> None:
    q = build_queue(findings)
    data = [f.model_dump(mode="json") for f in q]
    out.write_text(json.dumps(data, indent=2) + "\n")
