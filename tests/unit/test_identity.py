"""Identity resolution: PURL primary, CPE fallback, ambiguity never guessed."""

from __future__ import annotations

import pytest

from infravce.identity import ALIASES, cpe23, lookup_alias, purl, resolve_identity
from infravce.identity.resolver import IdentityScheme
from infravce.models import Ecosystem

# --------------------------------------------------------------------------- #
# PURL construction
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("ecosystem", "name", "version", "expected"),
    [
        (Ecosystem.PYPI, "requests", "2.31.0", "pkg:pypi/requests@2.31.0"),
        # PyPI treats underscores and hyphens as the same character.
        (Ecosystem.PYPI, "zope_interface", "5.0", "pkg:pypi/zope-interface@5.0"),
        (Ecosystem.NPM, "left-pad", "1.3.0", "pkg:npm/left-pad@1.3.0"),
        (Ecosystem.MAVEN, "org.apache.commons", "1.0", "pkg:maven/org.apache.commons@1.0"),
        (Ecosystem.NUGET, "Newtonsoft.Json", "13.0.1", "pkg:nuget/Newtonsoft.Json@13.0.1"),
    ],
)
def test_purl_uses_the_canonical_form(
    ecosystem: Ecosystem, name: str, version: str, expected: str
) -> None:
    assert purl(ecosystem, name, version=version) == expected


def test_purl_does_not_duplicate_the_version_as_a_qualifier() -> None:
    """`?version=` alongside `@version` made some consumers drop the version."""
    result = purl(Ecosystem.PYPI, "requests", version="2.31.0")
    assert result == "pkg:pypi/requests@2.31.0"
    assert "?" not in result


def test_purl_omits_the_version_when_absent() -> None:
    assert purl(Ecosystem.PYPI, "requests") == "pkg:pypi/requests"


@pytest.mark.parametrize(
    "ecosystem",
    [Ecosystem.DEBIAN, Ecosystem.APK, Ecosystem.RPM, Ecosystem.UNKNOWN],
)
def test_os_ecosystems_have_no_purl_type(ecosystem: Ecosystem) -> None:
    """No purl type exists for dpkg or apk.

    Inventing one would imply a standardisation the format does not have.
    """
    assert purl(ecosystem, "openssl", version="3.0.22") is None


# --------------------------------------------------------------------------- #
# CPE 2.3
# --------------------------------------------------------------------------- #


def test_cpe_has_twelve_components() -> None:
    """A short CPE looks valid and matches nothing, which reads as "no advisory"."""
    cpe = cpe23("nginx", vendor="nginx", version="1.22.1")
    parts = cpe.split(":")
    assert len(parts) == 13, f"expected cpe:2.3:a: + 11 components, got {len(parts) - 1}"
    assert parts[:3] == ["cpe", "2.3", "a"]


def test_cpe_escapes_special_characters() -> None:
    """Unescaped characters produce a malformed CPE that no consumer matches."""
    assert "\\ " in cpe23("my product")
    assert "\\:" in cpe23("weird:name")


def test_cpe_does_not_escape_the_wildcard_or_the_escape_character() -> None:
    """`*` is the CPE wildcard and `\\` is the escape, so neither is escaped.

    Escaping the asterisk would make a product that genuinely contains one
    unmatched, and doubling the backslash is required for escaping to be
    reversible at all.
    """
    assert "\\*" not in cpe23("star*name")
    assert "\\\\" in cpe23("back\\slash")


def test_cpe_vendor_defaults_to_the_product() -> None:
    """An empty vendor component never matches anything."""
    assert ":nginx:nginx:" in cpe23("nginx", version="1.0")


# --------------------------------------------------------------------------- #
# The poco collision, from grype#1737
# --------------------------------------------------------------------------- #


def test_poco_is_ambiguous_and_not_resolved() -> None:
    """The case the whole ambiguous_identity class exists to measure.

    Silently picking either namespace would attribute one software's advisories
    to another. The resolution must report ambiguity and refuse to choose.
    """
    resolution = resolve_identity("poco", version="1.0.0")
    assert resolution.ambiguous
    assert not resolution.is_resolved
    assert resolution.scheme is IdentityScheme.UNRESOLVED
    assert len(resolution.candidates) == 2
    assert any("pocoproject" in c for c in resolution.candidates)


def test_ambiguous_identity_never_yields_a_usable_identifier() -> None:
    """Ambiguity must not leak a purl or cpe that a caller might compare against."""
    resolution = resolve_identity("poco", version="1.0.0")
    assert resolution.canonical_name is None
    assert resolution.purl is None


def test_ambiguous_summary_names_both_candidates() -> None:
    summary = resolve_identity("poco").summary()
    assert "AMBIGUOUS" in summary
    assert "pocoproject/poco" in summary


# --------------------------------------------------------------------------- #
# Alias table
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("raw", "canonical", "vendor"),
    [
        # The Alpine source-package vs installed-subpackage indirection that
        # hid libcrypto1.1 from the lab's own collector.
        ("libcrypto1.1", "openssl", "openssl"),
        ("libssl1.1", "openssl", "openssl"),
        ("openssl3", "openssl", "openssl"),
        # Debian source package vs installed package name.
        ("libcurl4", "curl", "curl"),
        ("xz-utils", "xz", "tukaani"),
        ("xz", "xz", "tukaani"),
        ("redis-server", "redis", "redis"),
    ],
)
def test_alias_table_resolves_subpackages_to_source(raw: str, canonical: str, vendor: str) -> None:
    alias = lookup_alias(raw)
    assert alias is not None, f"{raw!r} missing from the alias table"
    assert alias.canonical_name == canonical
    assert alias.canonical_vendor == vendor


def test_alias_lookup_is_case_insensitive() -> None:
    """Vendor databases disagree on case; the table must not."""
    assert lookup_alias("OpenSSL") is not None
    assert lookup_alias("OPENSSL") is not None
    assert lookup_alias("LIBMYSQL") is None


def test_every_alias_entry_cites_its_source() -> None:
    """An unsourced alias is a guess, and guesses are not measurements."""
    for alias in ALIASES:
        assert alias.source.strip(), f"{alias.raw_names} has no source"
        if alias.ambiguous:
            assert alias.candidates, f"{alias.raw_names} is ambiguous with no candidates listed"


def test_alias_table_has_no_duplicate_raw_names() -> None:
    """A duplicate would make resolution depend on table order."""
    seen: set[str] = set()
    for alias in ALIASES:
        for name in alias.raw_names:
            key = name.lower()
            assert key not in seen, f"{name!r} appears in more than one entry"
            seen.add(key)


@pytest.mark.parametrize("junk", ["", "   ", "-", "___", "/", "*"])
def test_junk_product_names_do_not_resolve(junk: str) -> None:
    resolution = resolve_identity(junk)
    assert not resolution.is_resolved


# --------------------------------------------------------------------------- #
# Resolution outcomes
# --------------------------------------------------------------------------- #


def test_known_ecosystem_uses_purl() -> None:
    resolution = resolve_identity("requests", ecosystem=Ecosystem.PYPI, version="2.31.0")
    assert resolution.scheme is IdentityScheme.PURL
    assert resolution.is_resolved
    assert resolution.purl == "pkg:pypi/requests@2.31.0"
    assert resolution.confidence == 1.0


def test_unknown_ecosystem_falls_back_to_cpe_at_lower_confidence() -> None:
    """The CPE residual is open question 1 in docs/02 §7, so it is recorded."""
    resolution = resolve_identity("somebinary")
    assert resolution.scheme is IdentityScheme.CPE23
    assert resolution.confidence == 0.5
    assert resolution.cpe is not None


def test_alias_match_sits_between_exact_and_inferred() -> None:
    resolution = resolve_identity("libcrypto1.1", version="1.1.1q-r0")
    assert resolution.canonical_name == "openssl"
    assert 0.5 < resolution.confidence < 1.0


def test_alias_resolves_before_purl_construction() -> None:
    """A confidently wrong purl is worse than an acknowledged alias.

    Building a purl for `libcrypto1.1` would produce an identifier nothing matches,
    and it would look resolved rather than guessed.
    """
    resolution = resolve_identity("libcurl4", ecosystem=Ecosystem.PYPI, version="8.0")
    assert resolution.canonical_name == "curl"
    assert resolution.canonical_vendor == "curl"


def test_resolution_summary_is_readable() -> None:
    assert "requests" in resolve_identity("requests", ecosystem=Ecosystem.PYPI).summary()
    assert "unresolved" in resolve_identity("").summary()
