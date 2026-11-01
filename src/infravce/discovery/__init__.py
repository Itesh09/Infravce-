"""Discovery plane: declared/passive/active sources (read-only)."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from infravce.models import Observation

from .active import ActiveProbeConfig, ProbeTarget, probe_ports, scan_ports
from .manifests import parse_manifest
from .network import OS_FAMILIES, Target, parse_target, scan_target
from .package_db import (
    PackageRecord,
    detect_host_os,
    inventory_observations,
    parse_apk_installed,
    parse_dpkg_status,
    read_host_inventory,
)
from .sbom import parse_sbom


def _collect_from_path(p: Path) -> list[Observation]:
    if not p.exists():
        return []
    if p.is_dir():
        obs: list[Observation] = []
        for fname in ("requirements.txt", "package.json", "go.mod"):
            mf = p / fname
            if mf.exists():
                obs.extend(parse_manifest(mf))
        for pattern in ("*sbom*.json", "*spdx*.json", "*cyclonedx*.json", "*.sbom.json"):
            for f in p.glob(pattern):
                obs.extend(parse_sbom(f))
        for f in p.glob("*.json"):
            name = f.name.lower()
            if "sbom" in name or "spdx" in name or "cyclonedx" in name:
                obs.extend(parse_sbom(f))
        return obs
    lname = p.name.lower()
    sbomish = "sbom" in lname or "spdx" in lname or "cyclonedx" in lname
    if sbomish or lname.endswith(".sbom.json"):
        res = parse_sbom(p)
        if res:
            return res
    if lname.endswith(".json"):
        res = parse_sbom(p)
        if res:
            return res
    return parse_manifest(p)


def discover(sources: Iterable[Path | str] | None = None) -> list[Observation]:
    obs: list[Observation] = []
    if sources is None:
        obs.extend(_collect_from_path(Path.cwd()))
    else:
        for s in sources:
            obs.extend(_collect_from_path(Path(s)))
    seen: set[tuple[str, str, str, str]] = set()
    out: list[Observation] = []
    for o in obs:
        key = (o.asset_id, o.raw_product, o.raw_version, o.acquisition_method.value)
        if key not in seen:
            seen.add(key)
            out.append(o)
    return out


__all__ = [
    "OS_FAMILIES",
    "ActiveProbeConfig",
    "PackageRecord",
    "ProbeTarget",
    "Target",
    "detect_host_os",
    "discover",
    "inventory_observations",
    "parse_apk_installed",
    "parse_dpkg_status",
    "parse_manifest",
    "parse_sbom",
    "parse_target",
    "probe_ports",
    "read_host_inventory",
    "scan_ports",
    "scan_target",
]
