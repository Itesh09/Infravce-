"""Discovery plane: declared/passive/active sources (read-only)."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from infravce.models import Observation

from .manifests import parse_manifest
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
    if "sbom" in lname or "spdx" in lname or "cyclonedx" in lname or lname.endswith((".sbom.json",)):
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


__all__ = ["discover", "parse_sbom", "parse_manifest"]
