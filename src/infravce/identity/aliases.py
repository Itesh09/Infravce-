"""Vendor-alias table.

Aliases are **data, not code** (``docs/02-architecture.md`` §4.2 Stage B). That is
a deliberate architectural constraint, not a style preference: the 50.18%
vendor-name inconsistency measured in NVD and the poco/pocoproject collision are
both table entries, and neither is a reasoning problem. Encoding them as ``if``
branches would make every future namespace collision a code change, and would hide
which entries the system actually relies on — which is the thing open question 1
needs measured.

Each entry carries its evidence. An alias with no ``source`` is a guess, and this
module will not accept one.

Ambiguity is represented, not resolved. Where a name genuinely refers to two
different pieces of software, the entry lists both candidates and the resolver
declines to choose. The lab's ``ambiguous-poco`` fixture is exactly this case.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from infravce.models import Ecosystem

__all__ = ["ALIASES", "Alias", "lookup_alias"]


@dataclass(frozen=True, slots=True)
class Alias:
    """One row of the vendor-alias table."""

    #: Names that refer to the same software as :attr:`canonical_name`.
    raw_names: tuple[str, ...]
    canonical_name: str
    canonical_vendor: str
    ecosystem: Ecosystem | None = None
    #: Where this equivalence comes from. No source means no entry.
    source: str = ""
    #: When set, the name refers to more than one piece of software and must not
    #: be resolved to either. Candidates are the distinct identities involved.
    ambiguous: bool = False
    candidates: tuple[str, ...] = ()


#: The table. Kept small and sourced: every entry here was observed in a real
#: advisory database or a real tool output, and the ``source`` says which.
#:
#: Deliberately *not* included: guesses about vendor names that were never seen to
#: disagree. Adding speculative entries would make the table look more capable
#: while making its errors harder to see, and this project's contribution is a
#: measurement, so an unmeasured entry helps nothing.
ALIASES: tuple[Alias, ...] = (
    Alias(
        raw_names=("poco",),
        canonical_name="poco",
        canonical_vendor="pocoproject",
        ecosystem=Ecosystem.UNKNOWN,
        source="grype#1737: Syft emitted cpe:2.3:a:poco:poco:1.12.2 while the "
        "advisory database carried cpe:2.3:a:pocoproject:poco:*",
        ambiguous=True,
        candidates=("pocoproject/poco (C++ library)", "poco (unrelated Python package)"),
    ),
    Alias(
        raw_names=("openssl", "openssl3", "libssl1.1", "libcrypto1.1", "openssl-libs"),
        canonical_name="openssl",
        canonical_vendor="openssl",
        ecosystem=Ecosystem.UNKNOWN,
        source="Alpine secdb keys advisories on the source package `openssl` while "
        "assets report the subpackages libcrypto1.1 / libssl1.1 / openssl3",
    ),
    Alias(
        raw_names=("curl", "libcurl4", "libcurl4-openssl-dev"),
        canonical_name="curl",
        canonical_vendor="curl",
        ecosystem=Ecosystem.UNKNOWN,
        source="Debian tracker records advisories against source package `curl`; "
        "installed assets report libcurl4",
    ),
    Alias(
        raw_names=("xz", "xz-utils", "liblzma5", "liblzma-dev"),
        canonical_name="xz",
        canonical_vendor="tukaani",
        ecosystem=Ecosystem.UNKNOWN,
        source="Debian source package `xz` builds xz-utils and liblzma5; the "
        "tracker keys on `xz-utils` while assets report either",
    ),
    Alias(
        raw_names=("nginx", "nginx-core"),
        canonical_name="nginx",
        canonical_vendor="nginx",
        ecosystem=Ecosystem.UNKNOWN,
        source="Debian source package `nginx`; assets report nginx-core in some "
        "manifest formats",
    ),
    Alias(
        raw_names=("busybox",),
        canonical_name="busybox",
        canonical_vendor="busybox",
        ecosystem=Ecosystem.UNKNOWN,
        source="Alpine secdb `busybox`; no rename, recorded so the table's "
        "coverage is auditable rather than implicit",
    ),
    Alias(
        raw_names=("redis", "redis-server"),
        canonical_name="redis",
        canonical_vendor="redis",
        ecosystem=Ecosystem.UNKNOWN,
        source="Debian source package `redis`, installed as redis-server",
    ),
    Alias(
        raw_names=("postgresql", "postgresql-15", "postgresql-client-15"),
        canonical_name="postgresql",
        canonical_vendor="postgresql",
        ecosystem=Ecosystem.UNKNOWN,
        source="Debian tracker keys on postgresql-15; assets report postgresql "
        "or a client package of a specific major version",
    ),
    Alias(
        raw_names=("nodejs", "node", "node.js"),
        canonical_name="nodejs",
        canonical_vendor="nodejs",
        ecosystem=Ecosystem.NPM,
        source="Distribution packages use nodejs/node.js while the npm registry "
        "identity is `node`",
    ),
)

#: Case-insensitive lookup, built once at import. Keys are lowercased so
#: `OpenSSL`, `openssl`, and `OPENSSL` all resolve, which is the normalisation that
#: vendor databases most often omit.
_INDEX: dict[str, Alias] = {name.lower(): alias for alias in ALIASES for name in alias.raw_names}

#: Names that look like a package reference but carry no product at all.
_JUNK = re.compile(r"^[\s\-_./*]+$")


def lookup_alias(raw_name: str, *, aliases: tuple[Alias, ...] | None = None) -> Alias | None:
    """Find the alias entry for a raw product name, if there is one.

    Returns ``None`` when the name is not in the table. That is the normal case for
    a project with no namespace conflict, so the caller falls through to PURL/CPE
    construction rather than treating a miss as a failure.
    """
    name = raw_name.strip()
    if not name or _JUNK.match(name):
        return None

    if aliases is not None:
        lowered = name.lower()
        for alias in aliases:
            if any(raw.lower() == lowered for raw in alias.raw_names):
                return alias
        return None

    return _INDEX.get(name.lower())
