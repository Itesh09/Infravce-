"""Canonical identity resolution: PURL first, CPE 2.3 as fallback."""

from __future__ import annotations

from infravce.identity.aliases import ALIASES, Alias, lookup_alias
from infravce.identity.resolver import (
    IdentityScheme,
    Resolution,
    cpe23,
    purl,
    resolve_identity,
)

__all__ = [
    "ALIASES",
    "Alias",
    "IdentityScheme",
    "Resolution",
    "cpe23",
    "lookup_alias",
    "purl",
    "resolve_identity",
]
