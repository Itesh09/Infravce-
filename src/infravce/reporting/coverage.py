"""Coverage and freshness reporting."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from infravce.models import ScanCoverage


def write_coverage(coverages: list[ScanCoverage], out: Path) -> None:
    data = [c.model_dump(mode="json") for c in coverages]
    out.write_text(json.dumps(data, indent=2) + "\n")


def write_coverage_summary(coverages: list[ScanCoverage], out: Path) -> None:
    lines = ["# Scan Coverage Summary", ""]
    for c in coverages:
        lines.append(f"- {c.summary()}")
    out.write_text("\n".join(lines) + "\n")
