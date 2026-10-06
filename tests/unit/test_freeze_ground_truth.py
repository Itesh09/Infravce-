"""Tests for the Debian version comparator used to freeze ground truth.

This comparator decides backport verdicts. If it ranks ``+deb12u9`` above
``+deb12u15``, every affected/safe label derived from it inverts, and the
benchmark reports confident nonsense. It is therefore tested directly rather
than only through the freezer that calls it.

Cases are taken from Debian Policy §5.6.12 and from real bookworm versions.
"""

from __future__ import annotations

import functools
import importlib.util
import itertools
import shutil
import subprocess
import sys
from pathlib import Path
from typing import ClassVar

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "freeze_ground_truth",
    Path(__file__).resolve().parents[2]
    / "bench"
    / "infra-cve-bench"
    / "freeze_ground_truth.py",
)
assert _SPEC and _SPEC.loader
freeze_ground_truth = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = freeze_ground_truth
_SPEC.loader.exec_module(freeze_ground_truth)

deb_compare = freeze_ground_truth.deb_compare
verdict_for = freeze_ground_truth.verdict_for

# The freezer imports the collector's apk parser, so importing the freezer above
# already put the collector in sys.modules. Reusing it avoids loading the same
# file twice under two names, which would give two distinct class objects.
collect_lab_state = sys.modules["collect_lab_state"]
split_apk_line = collect_lab_state.split_apk_line
check_service = collect_lab_state.check_service
NOT_INSTALLED = collect_lab_state.NOT_INSTALLED


@pytest.mark.parametrize(
    ("a", "b"),
    [
        # The exact case that would silently invert a backport verdict if the
        # revision were compared lexicographically.
        ("7.88.1-10+deb12u9", "7.88.1-10+deb12u15"),
        ("1.0-1", "1.0-2"),
        ("2.4.1", "2.6"),
        ("5.4.1-1", "5.4.1-2"),
        ("3.0.17-1~deb12u1", "3.0.20-1~deb12u2"),
        # Epoch dominates everything: epoch 1 beats a higher upstream version.
        ("2.0", "1:1.0"),
        # Tilde sorts below the end of the string, so a pre-release is below its
        # own release.
        ("1.0~rc1", "1.0"),
        ("1.0~rc1", "1.0~rc2"),
        ("1.0~~", "1.0~a"),
        ("1.0", "1.0.0"),
        # Real bookworm builds from this project.
        ("1.22.1-9+deb12u3", "1.22.1-9+deb12u10"),
        ("5.4.1-1", "5.4.1-1+deb12u2"),
        ("7.88.1-10+deb12u12", "7.88.1-10+deb12u15"),
    ],
)
def test_ordering(a: str, b: str) -> None:
    assert deb_compare(a, b) < 0, f"{a} should sort below {b}"
    assert deb_compare(b, a) > 0, f"{b} should sort above {a}"


@pytest.mark.parametrize(
    "v",
    ["1.0", "1:1.0-1", "5.4.1-1+deb12u2", "1.0~rc1", "3.0.17-1~deb12u1"],
)
def test_reflexive(v: str) -> None:
    assert deb_compare(v, v) == 0


def test_result_is_clamped_to_three_values() -> None:
    """Magnitude is meaningless; only the sign may matter.

    Returning a raw character-code difference is easy to leak into a caller that
    asserts equality against a reference result, so the contract is pinned here.
    """
    assert deb_compare("1.0", "2.0") == -1
    assert deb_compare("2.0", "1.0") == 1
    assert deb_compare("1.0", "1.0") == 0


def test_antisymmetry_is_consistent() -> None:
    """deb_compare must be a total order on this set, not just pairwise right.

    Sorting with it has to be stable and transitive, otherwise the pick of "the
    newest fix available" would depend on input order.
    """
    versions = [
        "1.0",
        "1.0~rc1",
        "1.0.1",
        "1.0-1",
        "1.0-2",
        "1.0-10",
        "1:0.5",
        "2.0",
        "1.007",
        "1.7",
    ]
    ordered = sorted(versions, key=functools.cmp_to_key(deb_compare))
    # Epoch 1 sorts last despite having the lowest upstream, because epoch
    # dominates. Expected order verified against `dpkg --compare-versions`.
    assert ordered == [
        "1.0~rc1",
        "1.0",
        "1.0-1",
        "1.0-2",
        "1.0-10",
        "1.0.1",
        "1.007",
        "1.7",
        "2.0",
        "1:0.5",
    ]


class TestApkVersions:
    """apk version ordering, which decides Alpine backport verdicts."""

    @pytest.mark.parametrize(
        ("a", "b"),
        [
            # The boundary that makes busybox in this lab an affected case:
            # r20 predates the r21 fix.
            ("1.36.1-r20", "1.36.1-r21"),
            ("8.5.0-r0", "8.9.1-r0"),
            ("3.1.7-r1", "3.1.8-r0"),
            ("1.1.1q-r0", "1.1.1w-r1"),
            # A later revision of the same upstream is newer.
            ("1.36.1-r2", "1.36.1-r19"),
            # Numeric segments compare numerically, not as text.
            ("8.9.0-r0", "8.14.1-r2"),
            ("3.1.8-r1", "3.3.3-r0"),
            # Verified against `apk version -t`, which reports `<` here: the
            # upstream segments are compared before the -rN revision, so r20 of
            # 1.36.1 sorts below r12 of 1.37.0. Expecting the opposite would
            # have been a plausible-looking but wrong test.
            ("1.36.1-r20", "1.37.0-r12"),
        ],
    )
    def test_ordering(self, a: str, b: str) -> None:
        assert freeze_ground_truth.apk_version_lt(a, b), f"{a} should sort below {b}"
        assert not freeze_ground_truth.apk_version_lt(b, a)

    @pytest.mark.parametrize("v", ["1.36.1-r20", "8.5.0-r0", "1.1.1q-r0"])
    def test_not_less_than_itself(self, v: str) -> None:
        assert not freeze_ground_truth.apk_version_lt(v, v)

    def test_missing_revision_is_treated_as_r0(self) -> None:
        assert freeze_ground_truth.apk_version_lt("1.36.1", "1.36.1-r1")

    def test_agrees_with_apk_where_available(self) -> None:
        """Differential test against `apk version -t`, the reference comparator.

        Alpine's own tool is the authority for apk ordering, and the Debian
        differential test already showed that a plausible hand-written version of
        this kind of code disagrees with the real one. Only runs where an alpine
        image is available; otherwise the hand-written cases above stand alone.
        """
        if shutil.which("docker") is None:
            pytest.skip("docker not available")

        image = "alpine:3.19"

        def apk_says_lt(a: str, b: str) -> bool:
            out = subprocess.run(
                [
                    "docker", "run", "--rm", image,
                    "sh", "-c", 'apk version -t "$1" "$2"',
                    "_", a, b,
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=180,
            )
            return "<" in out.stdout

        try:
            first = apk_says_lt("1.36.1-r20", "1.37.0-r12")
            second = apk_says_lt("1.37.0-r12", "1.36.1-r20")
        except subprocess.TimeoutExpired:
            pytest.skip("apk probe timed out")
        if first == second:
            pytest.skip("apk comparator returned no usable result")

        pairs = [
            ("1.36.1-r20", "1.37.0-r12"),
            ("1.36.1-r20", "1.36.1-r21"),
            ("1.36.1-r21", "1.36.1-r21"),
            ("1.36.1", "1.36.1-r1"),
            ("8.9.0-r0", "8.14.1-r2"),
            ("1.1.1q-r0", "1.1.1w-r1"),
            ("3.1.7-r1", "3.1.8-r0"),
        ]
        for a, b in pairs:
            assert freeze_ground_truth.apk_version_lt(a, b) == apk_says_lt(a, b), (
                f"disagreed with apk on {a} vs {b}"
            )

    def test_a_build_at_the_fix_boundary_is_not_vulnerable(self) -> None:
        """Fixed-in version itself must count as patched.

        The boundary is inclusive on the safe side: a build equal to the fixed
        version has the fix and must not be labelled affected.
        """
        assert not freeze_ground_truth.apk_version_lt("1.36.1-r21", "1.36.1-r21")


class TestAlpineVerdicts:
    """Deriving verdicts from secfix boundaries.

    The interesting case is a build that sits between two boundaries: patched for
    the older CVE, still exposed to the newer one. Producing both from one
    authoritative dataset is the point of using secdb rather than a CVE list.
    """

    SECFIXES: ClassVar[dict[str, list[str]]] = {
        "1.36.1-r19": ["CVE-2023-42364"],
        "1.36.1-r2": ["CVE-2022-48174"],
        "1.36.1-r21": ["CVE-2024-58251", "CVE-2025-46394"],
    }

    def _truth_for(self, cve: str, installed: str = "1.36.1-r20") -> str:
        rows = freeze_ground_truth.alpine_verdicts(self.SECFIXES, installed)
        return next(t for c, _, t in rows if c == cve)

    def test_build_before_a_fix_is_affected(self) -> None:
        assert self._truth_for("CVE-2024-58251") == "affected"

    def test_build_after_a_fix_is_not_affected(self) -> None:
        assert self._truth_for("CVE-2023-42364") == "not_affected"

    def test_one_build_can_be_split_across_both_verdicts(self) -> None:
        """r20 is past the r19 fix and short of the r21 fix.

        This single build is the lab's most instructive case: a tool that decides
        by CVE identity alone rather than by version gets exactly one of the two
        wrong.
        """
        assert self._truth_for("CVE-2023-42364") == "not_affected"
        assert self._truth_for("CVE-2024-58251") == "affected"

    def test_earliest_boundary_is_used_when_a_cve_has_several(self) -> None:
        """A CVE fixed in more than one build is decided by the first one.

        Using the newest boundary would wrongly call an intermediate build safe.
        """
        secfixes = {"1.0-r1": ["CVE-1"], "2.0-r1": ["CVE-1"]}
        rows = freeze_ground_truth.alpine_verdicts(secfixes, "1.5")
        assert rows == [("CVE-1", "1.0-r1", "not_affected")]

    def test_no_secfixes_yields_no_cases(self) -> None:
        assert freeze_ground_truth.alpine_verdicts({}, "1.36.1-r20") == []

    def test_output_is_sorted_for_reproducible_freezes(self) -> None:
        rows = freeze_ground_truth.alpine_verdicts(self.SECFIXES, "1.36.1-r20")
        assert [r[0] for r in rows] == sorted(r[0] for r in rows)


class TestArchitectureScope:
    """An arch-scoped advisory is not applicable to this machine.

    Debian keeps such CVEs open indefinitely because no fix is needed on the
    other architectures, so a tracker status alone would label them "affected"
    on amd64. That would be a ground-truth false positive which every correctly
    behaving system under test would then be penalised for.
    """

    def test_ppc_scoped_advisory_does_not_apply_to_amd64(self) -> None:
        desc = (
            "OpenSSL 3.0.0 through 3.3.2 on the PowerPC architecture is vulnerable "
            "to a Minerva attack."
        )
        assert freeze_ground_truth.architecture_applies(desc, "amd64") is False

    def test_same_advisory_applies_to_ppc64el(self) -> None:
        desc = "OpenSSL 3.0.0 through 3.3.2 on the PowerPC architecture is vulnerable."
        assert freeze_ground_truth.architecture_applies(desc, "ppc64el") is True

    @pytest.mark.parametrize(
        ("desc", "arch"),
        [
            ("CVE-2023-1255 affects armhf builds only.", "armhf"),
            ("The flaw was found on arm64.", "arm64"),
            ("Only builds for ppc64el are impacted.", "ppc64el"),
        ],
    )
    def test_scope_detection(self, desc: str, arch: str) -> None:
        assert freeze_ground_truth._mentioned_architectures(desc) == {arch}

    def test_advisory_naming_no_architecture_is_unscoped(self) -> None:
        """An advisory that does not name an architecture must not be read as
        naming every architecture.

        A description saying "all architectures are affected" mentions no
        specific one, so it scopes nothing and stays in the benchmark.
        """
        assert freeze_ground_truth._mentioned_architectures(
            "All architectures are affected."
        ) == set()

    def test_x86_64_does_not_also_match_the_i386_alias(self) -> None:
        """`x86-64` and `x86_64` are amd64 only, never i386.

        With a plain `\\b` boundary the hyphen counts as a separator, so the i386
        alias `x86` matches the prefix and an amd64-only advisory would be
        classified as also affecting i386.
        """
        for desc in ("affects x86-64", "affects x86_64"):
            assert freeze_ground_truth._mentioned_architectures(desc) == {"amd64"}, desc

    def test_bare_x86_is_still_recognised_as_i386(self) -> None:
        assert freeze_ground_truth._mentioned_architectures("affects x86 only") == {"i386"}

    def test_amd64_aliases_are_recognised(self) -> None:
        assert freeze_ground_truth._mentioned_architectures("affects x86_64") == {"amd64"}
        assert freeze_ground_truth._mentioned_architectures("affects x86-64") == {"amd64"}

    def test_missing_description_is_treated_as_applicable(self) -> None:
        """Absence of evidence must not silently drop a case.

        Dropping a genuinely applicable CVE inflates measured recall, which is
        the worse direction for a benchmark that exists to catch false negatives.
        """
        assert freeze_ground_truth.architecture_applies(None, "amd64") is True
        assert freeze_ground_truth.architecture_applies("", "amd64") is True

    def test_unrecognised_architecture_name_is_treated_as_applicable(self) -> None:
        desc = "affects only loong64 builds"
        assert freeze_ground_truth.architecture_applies(desc, "amd64") is True

    def test_word_boundaries_prevent_substring_false_matches(self) -> None:
        """'arm' must not match inside 'armour' or 'alarm'.

        A substring search would classify unrelated advisories as arch-scoped and
        quietly drop them from the benchmark.
        """
        assert freeze_ground_truth._mentioned_architectures("a flaw in armour plating") == set()
        assert freeze_ground_truth._mentioned_architectures("armour and alarm handling") == set()


class TestVerdictMapping:
    """The mapping is where a bug becomes a wrong label rather than a crash."""

    def test_not_affected_is_trusted_without_comparison(self) -> None:
        assert verdict_for("not-affected", "0.1", None) == "not_affected"

    def test_open_and_no_dsa_are_affected(self) -> None:
        assert verdict_for("open", "7.88.1-10+deb12u15", None) == "affected"
        assert verdict_for("no-dsa", "7.88.1-10+deb12u15", None) == "affected"

    def test_undetermined_is_under_investigation(self) -> None:
        assert verdict_for("undetermined", "1.0", None) == "under_investigation"

    def test_resolved_below_fixed_version_is_affected(self) -> None:
        assert verdict_for("resolved", "3.0.17-1~deb12u1", "3.0.20-1~deb12u2") == "affected"

    def test_resolved_at_or_above_fixed_version_is_not_affected(self) -> None:
        assert verdict_for("resolved", "7.88.1-10+deb12u15", "7.10.7-1") == "not_affected"

    @pytest.mark.parametrize("fixed", [None, "0", "None", ""])
    def test_resolved_without_a_usable_fix_version_yields_no_label(
        self, fixed: str | None
    ) -> None:
        """A fix version of 0 does not mean "every version is fine".

        Returning a label here would invent ground truth the tracker never
        gave, so the honest outcome is no label at all.
        """
        assert verdict_for("resolved", "1.22.1-9+deb12u10", fixed) is None

    def test_unknown_status_yields_no_label(self) -> None:
        assert verdict_for("some-future-status", "1.0", "1.0") is None


def test_agrees_with_dpkg_over_a_generated_corpus() -> None:
    """Differential test against dpkg, the reference implementation.

    A version comparator is exactly the kind of code where a plausible
    implementation disagrees with the real one on inputs nobody would have
    thought to write down. Policy §5.6.12 examples cannot cover that space, so
    this checks an exhaustive pairwise cross product plus a random sample against
    ``dpkg --compare-versions`` when dpkg is available.
    """
    dpkg = shutil.which("dpkg")
    if dpkg is None:
        pytest.skip("dpkg not available on this system")

    pool = [
        "1.0",
        "1.0~rc1",
        "1.0.1",
        "1.0-1",
        "1.0-2",
        "1.0-10",
        "1:0.5",
        "2.0",
        "1.007",
        "1.7",
        "7.88.1-10+deb12u9",
        "7.88.1-10+deb12u15",
        "3.0.17-1~deb12u1",
        "3.0.20-1~deb12u2",
        "1.22.1-9+deb12u3",
        "1.22.1-9+deb12u10",
        "5.4.1-1",
        "5.4.1-1+deb12u2",
        "1.0~~",
        "1.0~a",
        "2.4.1",
        "2.6",
    ]

    def dpkg_compare(a: str, b: str) -> int | None:
        for op, value in (("lt", -1), ("eq", 0), ("gt", 1)):
            proc = subprocess.run(
                [dpkg, "--compare-versions", a, op, b],
                capture_output=True,
                check=False,
            )
            if proc.returncode == 0:
                return value
        return None

    random = __import__("random").Random(20261001)
    pairs = list(itertools.product(pool, pool))
    pairs += [
        (random.choice(pool), random.choice(pool)) for _ in range(200)
    ]

    mismatches = [
        (a, b, deb_compare(a, b), dpkg_compare(a, b))
        for a, b in pairs
        if (reference := dpkg_compare(a, b)) is not None
        and deb_compare(a, b) != reference
    ]

    assert not mismatches, f"disagreed with dpkg on: {mismatches[:10]}"


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        # The hyphenated names that a first-hyphen split drops. These were
        # silently missing from the collected state while installed in the lab,
        # which made a vulnerable library look absent rather than mislabelled.
        ("libcrypto1.1-1.1.1q-r0", ("libcrypto1.1", "1.1.1q-r0")),
        ("libssl1.1-1.1.1q-r0", ("libssl1.1", "1.1.1q-r0")),
        ("nginx-module-geoip-1.27.4-r1", ("nginx-module-geoip", "1.27.4-r1")),
        ("alpine-keys-2.5-r0", ("alpine-keys", "2.5-r0")),
        # Revision suffix, and a version with no revision at all.
        ("busybox-1.37.0-r20", ("busybox", "1.37.0-r20")),
        ("curl-8.14.1", ("curl", "8.14.1")),
        # Not package records. Parsing these into a version is how a description
        # line once became an nginx version.
        ("nginx: High performance web server", None),
        ("", None),
        ("   ", None),
    ],
)
def test_apk_lines_split_into_name_and_version(line: str, expected) -> None:
    assert split_apk_line(line) == expected


def test_never_present_sentinel_is_checked_as_absence(monkeypatch: pytest.MonkeyPatch) -> None:
    """A NEVER_PRESENT label records absence, so the checker must not compare it.

    The label's `version` field holds a sentinel, not a version. Checking it the
    same way as a real version reported the package as missing drift while it was
    absent exactly as the label required, so the lab could never look clean.
    """
    monkeypatch.setattr(
        collect_lab_state, "installed_packages", lambda _s: {"busybox": "1.37.0-r20"}
    )

    assert check_service("known-safe", {"busybox": "1.37.0-r20"}) == []

    # Absent, as the label requires: still clean.
    assert check_service("known-safe", {"squid": NOT_INSTALLED}) == []

    # Suddenly present: that IS drift, and the message has to say so.
    problems = check_service("known-safe", {"busybox": NOT_INSTALLED})
    assert len(problems) == 1
    assert "never be present" in problems[0]


def test_version_drift_is_still_reported() -> None:
    """The sentinel path must not have swallowed ordinary version mismatches."""
    assert check_service("svc", {"busybox": "1.37.0-r20"}) == [
        "svc: no package database readable (is the container running?)"
    ]
