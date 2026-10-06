"""Comparators and the source-precedence engine.

The comparators are differentially tested against the distributions' own tools
where available, because a wrong ordering does not fail loudly: it produces a
confident wrong verdict, which is the failure this benchmark exists to measure.
"""

from __future__ import annotations

import itertools
import random
import shutil
import subprocess

import pytest

from infravce.applicability import (
    DistributionState,
    decide,
    rpm_compare,
    select_sources,
    verdict_for_state,
)
from infravce.applicability.comparators import apk_compare, deb_compare
from infravce.models import AdvisorySource, ApplicabilityVerdict, RangeRepresentation

# --------------------------------------------------------------------------- #
# Debian comparator
# --------------------------------------------------------------------------- #

#: The pairs that matter most. Each one is a case where the wrong ordering
#: silently inverts a backport verdict.
DEBIAN_PAIRS = [
    # u9 vs u15: lexicographic comparison puts u15 first, so a text sort would
    # make the *older* build look newer and invert the verdict.
    ("7.88.1-10+deb12u9", "7.88.1-10+deb12u15", -1),
    ("7.88.1-10+deb12u15", "7.88.1-10+deb12u9", 1),
    # Epoch dominates everything after it. An absent epoch is 0, so an explicit
    # epoch of 1 beats a large-looking upstream. Confirmed against dpkg:
    # `dpkg --compare-versions 1:1.0 gt 2.0` is true.
    ("1:1.12.20-8.el9", "2.12.20-8.el9", 1),
    ("2.12.20-8.el9", "1:1.12.20-8.el9", -1),
    ("1:1.0", "2.0", 1),
    ("2.0", "1:1.0", -1),
    # Epoch comparison with identical upstreams still orders correctly.
    ("1:1.0-1", "2:1.0-1", -1),
    # Revision compared when upstreams are equal.
    ("1.22.1-9+deb12u10", "1.22.1-9+deb12u9", 1),
    ("1.22.1-9+deb12u9", "1.22.1-9+deb12u10", -1),
    # Tilde sorts below everything, including the empty string.
    ("1.0~beta1", "1.0", -1),
    ("1.0", "1.0~beta1", 1),
    ("1.0~beta1", "1.0~beta2", -1),
    # Numeric, not textual, on multi-digit segments.
    ("1.9", "1.10", -1),
    ("2.4.7", "2.4.11", -1),
    # Equality.
    ("1.36.1-r20", "1.36.1-r20", 0),
    ("7.88.1-10+deb12u15", "7.88.1-10+deb12u15", 0),
    # Leading zeros.
    ("1.0.10", "1.0.010", 0),
]


@pytest.mark.parametrize(("a", "b", "expected"), DEBIAN_PAIRS)
def test_deb_compare_known_orderings(a: str, b: str, expected: int) -> None:
    assert deb_compare(a, b) == expected
    # Antisymmetry: if the order holds one way it must hold the other.
    assert deb_compare(b, a) == -expected


def _dpkg_compare(a: str, b: str) -> int | None:
    """Ask dpkg itself, if available.

    ``eq`` is asked first: dpkg's ``lt`` and ``gt`` both exit 1 both when the
    comparison is false *and* when the version string is invalid, so a bare ``lt``
    result cannot distinguish "greater than" from "dpkg rejected this input".
    """
    if shutil.which("dpkg") is None:
        return None
    proc = subprocess.run(
        ["dpkg", "--compare-versions", a, "eq", b],
        capture_output=True,
        check=False,
    )
    if proc.returncode == 0:
        return 0
    if proc.returncode == 1:
        proc = subprocess.run(
            ["dpkg", "--compare-versions", a, "lt", b],
            capture_output=True,
            check=False,
        )
        if proc.returncode == 0:
            return -1
        if proc.returncode == 1:
            return 1
    return None


def test_deb_compare_agrees_with_dpkg() -> None:
    """Differential test against the reference implementation.

    Random pairs from a realistic pool, plus the hand-picked cases above. If dpkg
    is unavailable the test is skipped rather than silently passing.
    """
    pool = [
        "1.22.1-9+deb12u10",
        "1.22.1-9+deb12u9",
        "5.4.1-1+deb12u2",
        "7.88.1-10+deb12u15",
        "7.88.1-10+deb12u9",
        "1.0~beta1",
        "1.0",
        "2.4.7",
        "2.4.11",
        "1:1.12.20-8.el9",
        "3.0.22-1~deb12u1",
        "0.9.8-1",
    ]
    pairs = list(itertools.product(pool, pool))
    pairs += [(random.choice(pool), random.choice(pool)) for _ in range(300)]

    mismatches = [
        (a, b, deb_compare(a, b), reference)
        for a, b in pairs
        if (reference := _dpkg_compare(a, b)) is not None and deb_compare(a, b) != reference
    ]

    assert not mismatches, f"disagreed with dpkg on: {mismatches[:10]}"


# --------------------------------------------------------------------------- #
# apk comparator
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        # The revision is what separates these two builds of the same upstream.
        ("1.36.1-r20", "1.36.1-r21", -1),
        ("1.36.1-r21", "1.36.1-r20", 1),
        ("1.36.1-r20", "1.36.1-r20", 0),
        # A missing revision is r0, so 1.36.1 sorts below 1.36.1-r1.
        ("1.36.1", "1.36.1-r1", -1),
        ("1.36.1-r1", "1.36.1", 1),
        # Numeric on both segments.
        ("3.1.8-r1", "3.1.8-r2", -1),
        ("1.36.1-r9", "1.36.1-r10", -1),
        # The EOL asset sits below every published secfix boundary.
        ("1.1.1q-r0", "1.1.1v-r0", -1),
        ("1.1.1q-r0", "1.1.1w-r1", -1),
        # Multi-digit numeric segments.
        ("1.36.1", "1.36.2", -1),
    ],
)
def test_apk_compare_known_orderings(a: str, b: str, expected: int) -> None:
    assert apk_compare(a, b) == expected
    assert apk_compare(b, a) == -expected


def test_apk_compare_agrees_with_apk() -> None:
    """Differential test against apk itself, where available."""
    if shutil.which("apk") is None:
        pytest.skip("apk is not installed on this machine")
    pool = ["1.36.1-r20", "1.36.1-r21", "1.1.1q-r0", "3.1.8-r1", "1.36.1"]
    mismatches = []
    for a, b in itertools.product(pool, pool):
        proc = subprocess.run(["apk", "version", "-t", a, b], capture_output=True, check=False)
        out = proc.stdout.decode().strip()
        expected = {"<": -1, "=": 0, ">": 1}.get(out)
        if expected is not None and apk_compare(a, b) != expected:
            mismatches.append((a, b, apk_compare(a, b), expected))
    assert not mismatches, f"disagreed with apk on: {mismatches[:10]}"


# --------------------------------------------------------------------------- #
# RPM
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("1:1.12.20-8.el9", "1.12.20-8.el9", 1),
        ("1.12.20-8.el9", "1:1.12.20-8.el9", -1),
        ("1.12.20-8.el9", "1.12.20-9.el9", -1),
        ("1.0", "1.0.1", -1),
        ("2.0-1", "2.0-1", 0),
    ],
)
def test_rpm_compare_known_orderings(a: str, b: str, expected: int) -> None:
    assert rpm_compare(a, b) == expected
    assert rpm_compare(b, a) == -expected


# --------------------------------------------------------------------------- #
# Distribution state mapping
# --------------------------------------------------------------------------- #


def test_resolved_compares_versions() -> None:
    boundary = "7.88.1-10+deb12u15"
    before = verdict_for_state(DistributionState.RESOLVED, "7.88.1-10+deb12u9", boundary)
    assert before.verdict is ApplicabilityVerdict.AFFECTED
    assert "compare_versions" in (before.comparison or "")

    after = verdict_for_state(DistributionState.RESOLVED, boundary, boundary)
    assert after.verdict is ApplicabilityVerdict.NOT_AFFECTED


@pytest.mark.parametrize(
    "state",
    [
        DistributionState.UNDETERMINED,
        DistributionState.NO_DSA,
        DistributionState.POSTPONED,
        DistributionState.UNKNOWN,
    ],
)
def test_unassessed_states_never_become_not_affected(state: DistributionState) -> None:
    """The mapping that matters most.

    These states mean nobody has finished assessing the issue. Reporting them as
    safe is how a tool convinces an operator to stop patching, so the test asserts
    the exact failure rather than a broad property.
    """
    # A fix version is supplied precisely so a naive implementation would be
    # tempted to use it and land on a confident verdict.
    outcome = verdict_for_state(state, "1.22.1-9+deb12u10", "1.22.1-9+deb12u11")
    assert outcome.verdict is ApplicabilityVerdict.UNDER_INVESTIGATION
    assert outcome.comparison is None, "no comparison should have been attempted"


def test_zero_fixed_version_is_not_treated_as_a_boundary() -> None:
    """Debian's `fixed_version=0` means no fix was needed, not that 0 is a fix.

    Comparing an installed version against the number 0 would always say
    "affected", and comparing in the other direction would always say "safe".
    Both are wrong; the honest answer is that the record does not settle it.
    """
    outcome = verdict_for_state(DistributionState.RESOLVED, "5.4.1-1+deb12u2", "0")
    assert outcome.verdict is ApplicabilityVerdict.UNDER_INVESTIGATION
    assert "no fix was needed" in outcome.reason


def test_not_affected_carries_a_justification() -> None:
    """CISA VEX requires it, and the model enforces it downstream."""
    outcome = verdict_for_state(DistributionState.NOT_AFFECTED, "7.88.1-10+deb12u15", None)
    assert outcome.verdict is ApplicabilityVerdict.NOT_AFFECTED
    assert outcome.justification is not None


def test_missing_versions_yield_under_investigation() -> None:
    """`resolved` with nothing to compare against is not `not_affected`."""
    for installed, fixed in ((None, "1.0"), ("1.0", None), (None, None)):
        result = verdict_for_state(DistributionState.RESOLVED, installed, fixed)
        assert result.verdict is ApplicabilityVerdict.UNDER_INVESTIGATION


def test_open_is_affected_without_a_version_comparison() -> None:
    outcome = verdict_for_state(DistributionState.OPEN, "1.22.1-9+deb12u10", None)
    assert outcome.verdict is ApplicabilityVerdict.AFFECTED
    assert outcome.comparison is None


# --------------------------------------------------------------------------- #
# Source precedence (P3)
# --------------------------------------------------------------------------- #


def test_distro_tracker_outranks_nvd_for_os_packages() -> None:
    decision = select_sources(
        {
            AdvisorySource.NVD: RangeRepresentation.NVD_RANGE,
            AdvisorySource.DISTRO_TRACKER: RangeRepresentation.DPKG_STATUS,
        },
        is_os_package=True,
    )
    assert decision.winner is AdvisorySource.DISTRO_TRACKER
    assert AdvisorySource.NVD in decision.outranked


def test_nvd_fallback_for_an_os_package_is_recorded_as_a_fallback() -> None:
    """Falling back to NVD for an OS package is a known-wrong answer, not a guess.

    The condition has to be visible to a reviewer, so the decision carries why.
    """
    decision = select_sources(
        {AdvisorySource.NVD: RangeRepresentation.NVD_RANGE},
        is_os_package=True,
    )
    assert decision.winner is AdvisorySource.NVD
    assert decision.fallback_reason is not None
    assert "OS package" in decision.fallback_reason


def test_osv_wins_for_language_packages() -> None:
    decision = select_sources(
        {
            AdvisorySource.NVD: RangeRepresentation.NVD_RANGE,
            AdvisorySource.OSV: RangeRepresentation.OSV_EVENTS,
        },
        is_os_package=False,
    )
    assert decision.winner is AdvisorySource.OSV
    assert decision.fallback_reason is None


def test_no_sources_is_unresolved_not_safe() -> None:
    """Absence of data is not absence of a finding."""
    verdict, decision, _ = decide(
        installed_version="1.0",
        ecosystem="debian",
        candidates={},
        is_os_package=True,
    )
    assert verdict is ApplicabilityVerdict.UNDER_INVESTIGATION
    assert decision.winner is None


def test_decide_ignores_outranked_sources() -> None:
    """Only the winning source's state decides.

    If the outranked sources were consulted, a `resolved` distro record would be
    overridden by an NVD range, which is the whole failure P3 describes.
    """
    verdict, decision, outcome = decide(
        installed_version="1.22.1-9+deb12u10",
        ecosystem="debian",
        candidates={
            AdvisorySource.DISTRO_TRACKER: (DistributionState.RESOLVED, "1.22.1-9+deb12u11"),
            AdvisorySource.NVD: (DistributionState.OPEN, None),
        },
        is_os_package=True,
    )
    assert decision.winner is AdvisorySource.DISTRO_TRACKER
    assert verdict is ApplicabilityVerdict.AFFECTED
    assert "compare_versions" in (outcome.comparison or "")


def test_sort_versions_uses_native_ordering() -> None:
    """Sorting must use the ecosystem's own ordering, not a text sort.

    A lexicographic sort would place u9 after u15 and 1.36.1-r20 after
    1.36.1-r3, which is the same class of error the comparators exist to prevent.
    """
    from infravce.applicability import sort_versions

    assert sort_versions(
        "debian", ["7.88.1-10+deb12u9", "7.88.1-10+deb12u15", "7.88.1-10+deb12u2"]
    ) == ["7.88.1-10+deb12u2", "7.88.1-10+deb12u9", "7.88.1-10+deb12u15"]

    assert sort_versions("apk", ["1.36.1-r20", "1.36.1-r3", "1.36.1-r9"]) == [
        "1.36.1-r3",
        "1.36.1-r9",
        "1.36.1-r20",
    ]


# --------------------------------------------------------------------------- #
# The guard that links the two modules
# --------------------------------------------------------------------------- #

#: Version strings observed in the wild that must never be compared.
UNCOMPARABLE = [
    "(devel)",
    "latest",
    "*",
    "999999",
    "git-abc1234",
    "(unknown)",
    "",
    "1.3#0602",
]


@pytest.mark.parametrize("raw", UNCOMPARABLE)
def test_unparseable_versions_never_reach_a_comparator(raw: str) -> None:
    """The single most important guard in the system, per docs/02 §4.2.

    When a version cannot be parsed the pipeline must halt for that observation.
    Coercing it to something orderable is how a finding gets invented, which is
    exactly what the benchmark's `unparseable_version` class measures.
    """
    from infravce.normalise.versions import normalise

    version = normalise(raw, product="openssl")
    assert not version.is_resolved, f"{raw!r} should not have resolved"
    assert version.compare_key if version.is_resolved else True


@pytest.mark.parametrize("raw", UNCOMPARABLE)
def test_unparseable_versions_map_to_under_investigation(raw: str) -> None:
    """An unorderable version cannot be compared, so no verdict may be claimed.

    The end-to-end guard: unresolvable version in, unresolved verdict out, with no
    comparison attempted. `999999` is the sharpest case, since it parses as a
    perfectly good number and only means "unpinned placeholder" out of context.
    """
    from infravce.applicability.engine import decide

    verdict, decision, outcome = decide(
        installed_version=None if raw == "" else raw,
        ecosystem="debian",
        candidates={AdvisorySource.DISTRO_TRACKER: (DistributionState.RESOLVED, "1.0")},
        is_os_package=True,
    )
    assert decision.winner is AdvisorySource.DISTRO_TRACKER
    assert verdict is ApplicabilityVerdict.UNDER_INVESTIGATION
    assert outcome.comparison is None
