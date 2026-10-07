"""Authorised-only, non-destructive probes (stubs + guard).

This module enforces the safety boundary from docs/06-ethics-and-scope.md and
docs/02-architecture.md (P7). Active methods require explicit authorisation and
an allowlist; they are read-only and do not alter service state.
"""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass

from infravce.models import AcquisitionMethod


@dataclass(frozen=True, slots=True)
class ProbeTarget:
    host: str
    port: int | None = None


@dataclass(frozen=True, slots=True)
class ActiveProbeConfig:
    authorised: bool = False
    allowlist: tuple[str, ...] = ()
    max_concurrent: int = 1
    timeout_s: float = 2.0


def _is_allowed(host: str, cfg: ActiveProbeConfig) -> bool:
    if not cfg.authorised:
        return False
    if not cfg.allowlist:
        return False
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        # treat hostname as string match against allowlist entries
        return any(host == a or host.endswith(f".{a}") if a.startswith(".") else False for a in cfg.allowlist)
    # IP in allowlist? check network containment
    for a in cfg.allowlist:
        try:
            if "/" in a:
                if ip in ipaddress.ip_network(a, strict=False):
                    return True
            else:
                if ip == ipaddress.ip_address(a):
                    return True
        except Exception:
            continue
    return False


def banner_probe(target: ProbeTarget, cfg: ActiveProbeConfig) -> list[object]:
    """Non-destructive banner grab stub (not implemented by default)."""
    if not _is_allowed(target.host, cfg):
        return []
    # Intentionally not implemented; real impl would do a single read-only fetch
    return []


__all__ = ["ActiveProbeConfig", "ProbeTarget", "banner_probe", "_is_allowed"]
