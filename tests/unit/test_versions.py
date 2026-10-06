"""Version normalisation tests.

Every case is a real version string from a documented production failure, so a
regression here means a known false-positive class has come back.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from infravce.models import Ecosystem
from infravce.normalise.versions import UnresolvableVersion, detect_ecosystem, normalise

FIXTURES = Path(__file__).parent.parent / "fixtures" / "version_cases.json"
_DATA: dict[str, Any] = json.loads(FIXTURES.read_text())


def _ids(section: str) -> list[str]:
    return [c["id"] for c in _DATA[section]]


RESOLVABLE = _DATA["resolvable"]
UNRESOLVABLE = _DATA["unresolvable"]


class TestResolvable:
    @pytest.mark.parametrize("case", RESOLVABLE, ids=_ids("resolvable"))
    def test_decomposes_into_expected_fields(self, case: dict[str, Any]) -> None:
        v = normalise(
            case["raw"],
            ecosystem=Ecosystem(case["ecosystem"]),
            product=case["product"],
        )
        assert isinstance(v, UnresolvableVersion) is False, (
            f"{case['id']} should have resolved but did not"
        )
        assert v.is_resolved
        assert v.confidence >= case["min_confidence"]
        for field in ("epoch", "upstream", "release", "distro_revision", "local_revision"):
            if field in case:
                assert getattr(v, field) == case[field], f"{case['id']}.{field}"

    @pytest.mark.parametrize("case", RESOLVABLE, ids=_ids("resolvable"))
    def test_never_raises(self, case: dict[str, Any]) -> None:
        """A parse failure must be recorded, not propagated."""
        normalise(case["raw"], ecosystem=Ecosystem(case["ecosystem"]), product=case["product"])


class TestUnresolvable:
    @pytest.mark.parametrize("case", UNRESOLVABLE, ids=_ids("unresolvable"))
    def test_refuses_range_comparison(self, case: dict[str, Any]) -> None:
        """The central guard: an unparseable version must be excluded from matching.

        grype#2606 is the failure this prevents: a GitHub Action pinned by SHA
        was recorded with the SHA as its version, and every range comparison
        against it produced a false positive.
        """
        v = normalise(case["raw"], product=case["product"])
        assert v.is_resolved is False
        assert v.upstream is None
        assert v.confidence == 0.0
        with pytest.raises(ValueError, match="unresolved version"):
            _ = v.compare_key

    @pytest.mark.parametrize("case", UNRESOLVABLE, ids=_ids("unresolvable"))
    def test_records_a_note(self, case: dict[str, Any]) -> None:
        """A refusal must be diagnosable from the database alone."""
        v = normalise(case["raw"], product=case["product"])
        assert v.notes, f"{case['id']} was refused without recording why"


class TestRPMRegression:
    """dependency-track#3774: 50 verified false positives from field folding."""

    def test_epoch_and_release_stay_separate(self) -> None:
        v = normalise("1:1.12.20-8.el9", ecosystem=Ecosystem.RPM, product="openssl")
        assert v.epoch == 1
        assert v.upstream == "1.12.20"
        assert v.release == "8.el9"
        assert v.distro_revision is None

    def test_compare_key_does_not_conflate_two_different_builds(self) -> None:
        a = normalise("1:1.12.20-8.el9", ecosystem=Ecosystem.RPM, product="openssl")
        b = normalise("1:1.12.20-9.el9", ecosystem=Ecosystem.RPM, product="openssl")
        assert a.compare_key != b.compare_key

    def test_epoch_changes_the_key(self) -> None:
        a = normalise("1.2.3-1.el9", ecosystem=Ecosystem.RPM, product="openssl")
        b = normalise("2:1.2.3-1.el9", ecosystem=Ecosystem.RPM, product="openssl")
        assert a.compare_key != b.compare_key


class TestEcosystemDetection:
    @pytest.mark.parametrize(
        ("product", "version", "expected"),
        [
            ("openssl", "1:1.12.20-8.el9", Ecosystem.RPM),
            ("libcrypto3", "3.3.2-r0", Ecosystem.APK),
            ("openssl", "3.1.4-r5", Ecosystem.APK),
            ("curl", "7.88.1-10+deb12u12", Ecosystem.DEBIAN),
            ("github.com/foo/bar", "v0.0.0-20230323144144-5bcd846fa16e", Ecosystem.GOLANG),
            ("openssl", "1.3#06023034579559bb64357db3a53f88a4", Ecosystem.CONAN),
            ("requests", "2.31.0", Ecosystem.PYPI),
            ("lodash", "4.17.21", Ecosystem.NPM),
        ],
    )
    def test_detects(self, product: str, version: str, expected: Ecosystem) -> None:
        assert detect_ecosystem(product, version) == expected

    @pytest.mark.parametrize(
        "version",
        ["ed68ef82c095e0d48ec87eccea555d944a631a4c", "(devel)", "latest", "sha256:" + "a" * 64],
    )
    def test_immutable_and_floating_refs_never_infer_an_ecosystem(self, version: str) -> None:
        """A wrong ecosystem picks the wrong comparator, which is the bug class."""
        assert detect_ecosystem("some/package", version) is Ecosystem.UNKNOWN


class TestRobustness:
    @pytest.mark.parametrize(
        "raw",
        [None, "", "   ", "\x00", "v", "1.", "..", "-" * 3, "999999999999999999999.0.0", "🎉"],
    )
    def test_never_raises_on_hostile_input(self, raw: str | None) -> None:
        v = normalise(raw, product="anything")
        assert v.confidence >= 0.0

    def test_whitespace_is_trimmed(self) -> None:
        assert normalise("  1.2.3  ", ecosystem=Ecosystem.SEMVER).upstream == "1.2.3"

    def test_confidence_is_always_in_range(self) -> None:
        for raw in ("1.2.3", "1:1.2-3.el9", "3.3.2-r0", "bogus", "latest", ""):
            v = normalise(raw)
            assert 0.0 <= v.confidence <= 1.0


class TestNotesAreTraceable:
    def test_apk_revision_note(self) -> None:
        v = normalise("3.3.2-r0", ecosystem=Ecosystem.APK, product="openssl")
        assert any("revision" in n for n in v.notes)

    def test_conan_revision_note(self) -> None:
        v = normalise("1.3#06023034579559bb64357db3a53f88a4", ecosystem=Ecosystem.CONAN)
        assert any("conan" in n.lower() for n in v.notes)

    def test_loose_semver_padding_is_disclosed(self) -> None:
        """grype#2606 saw a bare 'v46'; padding it silently would hide a guess."""
        v = normalise("v46", ecosystem=Ecosystem.SEMVER)
        assert v.upstream == "46.0.0"
        assert v.confidence < 0.7
        assert any("padded" in n for n in v.notes)


# --------------------------------------------------------------------------- #
# Strings that must never resolve, per docs/02 §4.2's non-negotiable guard
# --------------------------------------------------------------------------- #

#: Each of these reached the normaliser as an "installed version" and would, with a
#: looser parse, produce a confident verdict about a build that does not exist.
#: `999999` is the important one: it is a well-formed dotted number, so shape-based
#: checks accept it, and it stands for "rolling/dev placeholder" in the lab's CI
#: fixture.
UNRESOLVABLE_STRINGS = [
    "(devel)",
    "latest",
    "*",
    "999999",
    "000000",
    "0.0.0",
    "git-abc1234",
    "(unknown)",
    "",
    "   ",
    "1.3#0602",
]


@pytest.mark.parametrize("raw", UNRESOLVABLE_STRINGS)
def test_placeholder_and_non_version_strings_do_not_resolve(raw: str) -> None:
    for ecosystem in (None, Ecosystem.DEBIAN, Ecosystem.APK, Ecosystem.RPM):
        version = normalise(raw, ecosystem=ecosystem, product="openssl")
        assert not version.is_resolved, (
            f"{raw!r} resolved as {version.upstream!r} under {ecosystem}; "
            "an unorderable string must halt the pipeline, not become comparable"
        )
        assert version.confidence == 0.0


@pytest.mark.parametrize("raw", UNRESOLVABLE_STRINGS)
def test_resolve_key_raises_on_unresolvable_versions(raw: str) -> None:
    """The second line of defence.

    `compare_key` raising rather than returning a string means a caller that
    forgets to check `is_resolved` gets an exception instead of a wrong ordering.
    """
    version = normalise(raw, product="openssl")
    if not version.is_resolved:
        with pytest.raises(ValueError, match="unresolved"):
            _ = version.compare_key


def test_real_distribution_versions_still_resolve() -> None:
    """The guard must not become so strict that real versions are rejected."""
    for raw, eco in [
        ("7.88.1-10+deb12u15", Ecosystem.DEBIAN),
        ("1:1.12.20-8.el9", Ecosystem.RPM),
        ("1.36.1-r20", Ecosystem.APK),
        ("3.1.8-r1", Ecosystem.APK),
        ("5.4.1-1+deb12u2", Ecosystem.DEBIAN),
    ]:
        version = normalise(raw, ecosystem=eco)
        assert version.is_resolved, f"{raw!r} should resolve under {eco}"
        assert version.compare_key
