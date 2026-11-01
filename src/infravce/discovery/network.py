"""Network target parsing and orchestrating an authorised scan.

Accepts the forms a person actually types in a demo::

    127.0.0.1
    127.0.0.1:22,80,443
    http://192.168.1.10:8080
    lab.internal

The parser records what it inferred (scheme implies a port) so the report can be
read without guessing which ports were tried. Nothing here bypasses the
authorisation guard in :mod:`infravce.discovery.active`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlsplit

from infravce.discovery.active import (
    DEFAULT_PORTS,
    ActiveProbeConfig,
    probe_ports,
)
from infravce.models import Ecosystem, Observation

__all__ = ["Target", "parse_target", "scan_target"]

#: How a caller names the target's distribution. The banner does not carry it,
#: and guessing it would pick the wrong comparator, so the caller states it.
OS_FAMILIES: dict[str, tuple[Ecosystem, str | None]] = {
    "debian": (Ecosystem.DEBIAN, None),
    "debian:12": (Ecosystem.DEBIAN, "12"),
    "debian:11": (Ecosystem.DEBIAN, "11"),
    "debian:13": (Ecosystem.DEBIAN, "13"),
    "ubuntu": (Ecosystem.UBUNTU, None),
    "ubuntu:22.04": (Ecosystem.UBUNTU, "22.04:LTS"),
    "ubuntu:24.04": (Ecosystem.UBUNTU, "24.04:LTS"),
    "alpine": (Ecosystem.APK, None),
    "alpine:3.19": (Ecosystem.APK, "v3.19"),
    "alpine:3.20": (Ecosystem.APK, "v3.20"),
    "rhel": (Ecosystem.RPM, None),
    "none": (Ecosystem.UNKNOWN, None),
}


@dataclass(frozen=True, slots=True)
class Target:
    host: str
    ports: tuple[int, ...] = field(default_factory=lambda: DEFAULT_PORTS)
    scheme: str = "tcp"
    inferred_port: bool = False


def parse_target(spec: str, ports: tuple[int, ...] | None = None) -> Target:
    """Parse ``host[:port[,port]]`` or a URL."""
    text = spec.strip()
    if not text:
        raise ValueError("empty target")

    if "://" in text:
        parts = urlsplit(text)
        if not parts.hostname:
            raise ValueError(f"no host in target {spec!r}")
        scheme = parts.scheme.lower()
        default = 443 if scheme == "https" else 80
        selected = (parts.port or default,) if parts.port or ports is None else ports
        return Target(parts.hostname, tuple(selected), scheme, inferred_port=parts.port is None)

    host, _, port_text = text.partition(":")
    if not host:
        raise ValueError(f"no host in target {spec!r}")
    if port_text:
        try:
            selected = tuple(int(p) for p in port_text.split(",") if p.strip())
        except ValueError as exc:
            raise ValueError(f"invalid port list in {spec!r}") from exc
    else:
        selected = tuple(ports) if ports else DEFAULT_PORTS
    return Target(host, selected, "tcp", inferred_port=not port_text)


def scan_target(
    spec: str,
    *,
    authorised: bool,
    allowlist: tuple[str, ...] = (),
    ports: tuple[int, ...] | None = None,
    os_family: str | None = "debian:12",
    timeout_s: float = 2.0,
) -> tuple[list[Observation], Ecosystem, str | None, Target]:
    """Probe one target and return ``(observations, ecosystem, os_release, target)``.

    The allowlist defaults to the target's own host only when the caller passed
    an explicit allowlist through ``--allow``. Without either, the guard refuses,
    which is the intended default: an unauthorised scan must fail loudly rather
    than produce an empty report that looks like a clean result.
    """
    target = parse_target(spec, ports)
    ecosystem, os_release = OS_FAMILIES.get((os_family or "none").lower(), (Ecosystem.UNKNOWN, None))
    config = ActiveProbeConfig(
        authorised=authorised,
        allowlist=tuple(allowlist) or ((target.host,) if authorised else ()),
        timeout_s=timeout_s,
    )
    observations = probe_ports(target.host, target.ports, config, ecosystem=ecosystem)
    return observations, ecosystem, os_release, target
