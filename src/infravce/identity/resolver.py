"""Canonical identity resolution: PURL first, CPE 2.3 as fallback.

Identity resolution is a lookup problem with a measurable answer, not a reasoning
problem (``docs/02-architecture.md`` §4.2 Stage B). That is why there is no model
call, no fuzzy-matching dependency, and no special-case code here: aliases live in
:mod:`infravce.identity.aliases` as data.

**Why PURL is primary and CPE is a fallback.** PURL is what OSV and GHSA use
natively, so matching on it avoids a lossy round-trip. CPE remains necessary
because NVD's ranges are keyed on it, and for OS packages there is often no PURL
at all. The residual quality of that fallback is open question 1 in
``docs/02-architecture.md`` §7, so :class:`Resolution` records which scheme was
used and how confident the result is rather than hiding the choice.

**Why an ambiguous result is a first-class outcome.** ``poco`` names both a C++
library (``pocoproject/poco``) and an unrelated Python package. Returning one of
them silently would attach advisories for the wrong software to a real asset. The
benchmark's ``ambiguous_identity`` class exists to measure exactly this, so an
ambiguous resolution must be representable and must not be guessed through.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from urllib.parse import quote

from infravce.identity.aliases import Alias, lookup_alias
from infravce.models import Ecosystem

__all__ = [
    "IdentityScheme",
    "Resolution",
    "cpe23",
    "purl",
    "resolve_identity",
]


class IdentityScheme(StrEnum):
    PURL = "purl"
    CPE23 = "cpe23"
    UNRESOLVED = "unresolved"


#: Confidence bands, matching ``docs/02-architecture.md`` §3.1's
#: ``resolution_confidence`` vocabulary so the two do not drift apart.
_EXACT = 1.0
_ALIAS_MATCHED = 0.9
_INFERRED = 0.5
_UNRESOLVED = 0.0

#: Ecosystems with a PURL type. OS distributions deliberately have none: there is no
#: purl type for dpkg or apk, and inventing one would give a false impression of
#: standardisation the format does not have.
_PURL_TYPE: dict[Ecosystem, str] = {
    Ecosystem.PYPI: "pypi",
    Ecosystem.GOLANG: "golang",
    Ecosystem.NPM: "npm",
    Ecosystem.MAVEN: "maven",
    Ecosystem.CONAN: "conan",
    Ecosystem.NUGET: "nuget",
    Ecosystem.GO_DEPS: "golang",
}


#: Characters that must be backslash-escaped inside a CPE 2.3 formatted-string
#: component (NIST IR 7695 §6.2). The backslash and the asterisk are deliberately
#: absent: a backslash must be doubled so escaping is reversible, and `*` is the
#: wildcard, which a real product name may legitimately contain and must not have
#: silently turned into.
_CPE_SPECIAL = "!?\"'#$&()+,/:;<=>@[]^`{|}~ \t\n"


def _cpe_escape(value: str) -> str:
    r"""Escape a CPE 2.3 formatted-string component.

    Unescaped spaces and colons produce a malformed CPE that no consumer matches,
    which looks like a missing advisory rather than a broken identifier.
    """
    escaped = value.replace("\\", "\\\\")
    for char in _CPE_SPECIAL:
        escaped = escaped.replace(char, f"\\{char}")
    return escaped


def purl(ecosystem: Ecosystem, name: str, *, version: str | None = None) -> str | None:
    """Build a package URL, or None when the ecosystem has no purl type."""
    ptype = _PURL_TYPE.get(ecosystem)
    if ptype is None or not name:
        return None

    if ecosystem is Ecosystem.GOLANG:
        # Go module paths already carry their host and, for versioned modules, a
        # `/vN` major-version suffix. Both are part of the module's identity and are
        # stripped here only when they are not, because a golang purl must not
        # contain the semantic-version part as a path segment.
        path = name
        if path.startswith("github.com/") and path.count("/") >= 2:
            path = path.rsplit("/", 1)[0]
    elif ecosystem is Ecosystem.PYPI:
        # PyPI normalises underscores and hyphens together, so they are one name.
        path = name.replace("_", "-").lower()
    else:
        path = name

    if not version:
        return f"pkg:{ptype}/{quote(path, safe='/')}"
    # Both forms are valid purl. The version goes after `@` with no qualifier: that
    # is the canonical form, and duplicating it as a `?version=` qualifier as well
    # produced `pkg:pypi/requests@2.31.0?version=2.31.0`, which some consumers
    # parse as a qualifier-only purl and drop the version entirely.
    return f"pkg:{ptype}/{quote(path, safe='/')}@{quote(version, safe='')}"


def cpe23(product: str, *, vendor: str | None = None, version: str | None = None) -> str:
    """Build a CPE 2.3 application string.

    ``vendor`` defaults to the product name, which is what the vendor string means
    in the overwhelming majority of NVD CPEs and is a better default than an empty
    string. An empty vendor never matches, so a guess here is strictly better than
    nothing and is recorded as inferred by the caller.
    """
    v = _cpe_escape(vendor or product)
    p = _cpe_escape(product)
    ver = _cpe_escape(version) if version else "*"
    return f"cpe:2.3:a:{v}:{p}:{ver}:*:*:*:*:*:*:*"


@dataclass(frozen=True, slots=True)
class Resolution:
    """The outcome of an identity resolution.

    ``ambiguous`` is separate from ``unresolved`` on purpose. Unresolved means "I
    could not identify this"; ambiguous means "I found more than one candidate and
    will not choose for you". Collapsing them would let the second case report the
    first case's conclusion, which is the poco failure this project exists to
    avoid.
    """

    raw_product: str
    scheme: IdentityScheme
    canonical_name: str | None = None
    canonical_vendor: str | None = None
    purl: str | None = None
    cpe: str | None = None
    confidence: float = _UNRESOLVED
    ambiguous: bool = False
    candidates: tuple[str, ...] = field(default=())
    notes: tuple[str, ...] = field(default=())

    @property
    def is_resolved(self) -> bool:
        """True only for a single confident identity.

        An ambiguous result is deliberately *not* resolved: the caller must
        disambiguate with more evidence before anything is compared or reported.
        """
        return self.scheme is not IdentityScheme.UNRESOLVED and not self.ambiguous

    def summary(self) -> str:
        if self.ambiguous:
            return (
                f"{self.raw_product!r}: AMBIGUOUS between "
                f"{', '.join(self.candidates)}; not resolved"
            )
        if not self.is_resolved:
            reason = self.notes[0] if self.notes else "no alias or scheme matched"
            return f"{self.raw_product!r}: unresolved ({reason})"
        return f"{self.raw_product!r} -> {self.canonical_name} [{self.scheme.value}]"


def _infer_ecosystem(product: str) -> Ecosystem:
    """Best-effort ecosystem from a product name alone.

    Deliberately conservative: without a version to infer from, this only reports
    an ecosystem when the name is unambiguous for one. Guessing wrongly here would
    build a PURL of the wrong type, which is worse than reporting none and
    falling back to CPE.
    """
    lowered = product.strip().lower()
    if lowered in {"nodejs", "npm", "node"}:
        return Ecosystem.NPM
    if lowered.startswith("golang.org/") or lowered.startswith("github.com/"):
        return Ecosystem.GOLANG
    if ":" in product and "/" in product and not product.startswith("pkg:"):
        return Ecosystem.MAVEN
    return Ecosystem.UNKNOWN


#: Product names made up entirely of punctuation and whitespace. These carry no
#: product identity at all, so resolving them to a CPE would produce a wildcard-
#: matching identifier that appears in every advisory database at once.
_NO_PRODUCT = re.compile(r"^[\W_]+$")


def resolve_identity(
    raw_product: str,
    *,
    ecosystem: Ecosystem | None = None,
    version: str | None = None,
    aliases: tuple[Alias, ...] | None = None,
) -> Resolution:
    """Resolve ``(raw_product, version)`` to a canonical identity.

    The order is fixed and each step is recorded:

    1. An exact or aliased table lookup, which is authoritative and therefore
       confidence 1.0 (exact) or 0.9 (alias).
    2. PURL construction for ecosystems that have a purl type.
    3. CPE 2.3, the universal fallback, at inferred confidence.
    4. Unresolved, when the product is empty or ambiguous.

    Aliases are consulted before scheme construction because a wrong-but-confident
    PURL is worse than an acknowledged alias: it attaches the wrong advisories
    without any signal that anything was guessed.
    """
    product = raw_product.strip()
    if not product or _NO_PRODUCT.match(product):
        return Resolution(
            raw_product=raw_product,
            scheme=IdentityScheme.UNRESOLVED,
            notes=(
                (
                    "empty product name"
                    if not product
                    else f"{product!r} is punctuation only and names no product"
                ),
            ),
        )

    # Step 1: the alias table, which may be ambiguous on purpose.
    alias = lookup_alias(product, aliases=aliases)
    if alias is not None:
        if alias.ambiguous:
            return Resolution(
                raw_product=product,
                scheme=IdentityScheme.UNRESOLVED,
                ambiguous=True,
                candidates=alias.candidates,
                notes=(
                    f"{product!r} matches more than one vendor namespace "
                    f"({', '.join(alias.candidates)}); the advisory databases "
                    "disagree and choosing one would attribute vulnerabilities to "
                    "the wrong software",
                ),
            )
        eco = alias.ecosystem or ecosystem or _infer_ecosystem(product)
        alias_purl = purl(eco, alias.canonical_name, version=version)
        return Resolution(
            raw_product=product,
            scheme=IdentityScheme.PURL if alias_purl else IdentityScheme.CPE23,
            canonical_name=alias.canonical_name,
            canonical_vendor=alias.canonical_vendor,
            purl=alias_purl,
            cpe=cpe23(alias.canonical_name, vendor=alias.canonical_vendor, version=version),
            confidence=_ALIAS_MATCHED,
            notes=(f"matched alias table entry {alias.source!r}",),
        )

    eco = ecosystem if ecosystem is not None else _infer_ecosystem(product)
    built_purl = purl(eco, product, version=version)

    # Step 2: a purl type exists and we know which ecosystem we are in.
    if built_purl is not None and ecosystem is not None:
        return Resolution(
            raw_product=product,
            scheme=IdentityScheme.PURL,
            canonical_name=product,
            purl=built_purl,
            cpe=cpe23(product, version=version),
            confidence=_EXACT,
            notes=(f"purl constructed directly for {eco.value}",),
        )

    # Step 3: CPE, the fallback NVD ranges can actually match.
    return Resolution(
        raw_product=product,
        scheme=IdentityScheme.CPE23,
        canonical_name=product,
        cpe=cpe23(product, version=version),
        confidence=_INFERRED,
        notes=(
            "no purl type for this ecosystem; falling back to CPE, whose residual "
            "match quality is an open question in this project",
        ),
    )
