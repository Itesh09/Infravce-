"""Applicability: source precedence, distribution states, version comparison."""

from __future__ import annotations

from infravce.applicability.comparators import (
    apk_compare,
    apk_version_lt,
    compare_versions,
    deb_compare,
    rpm_compare,
    sort_versions,
)
from infravce.applicability.engine import (
    DistributionState,
    SourceDecision,
    VerdictOutcome,
    decide,
    select_sources,
    verdict_for_state,
)

__all__ = [
    "DistributionState",
    "SourceDecision",
    "VerdictOutcome",
    "apk_compare",
    "apk_version_lt",
    "compare_versions",
    "deb_compare",
    "decide",
    "rpm_compare",
    "select_sources",
    "sort_versions",
    "verdict_for_state",
]
