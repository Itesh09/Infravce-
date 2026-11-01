"""Minimal manifest parsing for declared inventory.

Parses:
- requirements.txt (lines, ignores comments, -r/-e, extras)
- package.json (dependencies, devDependencies)
- go.mod (requires)

Preserves raw strings; normalisation happens downstream.
"""
from __future__ import annotations

import json
import re
from collections.abc import Iterator
from pathlib import Path

from infravce.models import AcquisitionMethod, Ecosystem, Observation
from infravce.normalise.versions import normalise
from infravce.identity.resolver import resolve_identity


_PKG_NAME_VER = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]+)\s*([=><!~]+)\s*([^,\s#]+)")


def _mk_obs(
    asset_id: str,
    product: str,
    version: str,
    evidence: str,
    *,
    ecosystem: Ecosystem | None = None,
) -> Observation:
    ps = (product or "").strip()
    vs = (version or "").strip()
    nv = normalise(vs, ecosystem=ecosystem, product=ps)
    res = resolve_identity(ps, ecosystem=nv.ecosystem, version=vs if nv.is_resolved else None)
    return Observation(
        asset_id=asset_id,
        acquisition_method=AcquisitionMethod.MANIFEST,
        evidence=evidence,
        raw_product=ps,
        raw_version=vs,
        resolved_product=res.canonical_name if res.canonical_name else (ps or None),
        resolved_version=nv if nv.is_resolved else None,
        resolution_confidence=nv.confidence if nv.is_resolved else 0.0,
        parse_notes=nv.notes,
    )


def parse_requirements_txt(path: Path) -> list[Observation]:
    obs: list[Observation] = []
    for i, line in enumerate(path.read_text().splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("-r") or s.startswith("-e") or s.startswith("http"):
            continue
        # strip extras like package[extra]>=1.0
        if "[" in s and "]" in s:
            s = s.split("[", 1)[0] + s.split("]", 1)[1]
        m = _PKG_NAME_VER.match(s)
        if not m:
            # try simple name==ver
            m2 = re.match(r"^([A-Za-z0-9][\w.-]+)==([^#\s]+)", s)
            if m2:
                name, ver = m2.groups()
            else:
                # skip unparseable
                continue
        else:
            name, _, ver = m.groups()
        aid = f"req:{path.name}:{i}:{name}"
        obs.append(
            _mk_obs(
                aid, name, ver, f"manifest:{path.name}:line{i}:{aid}", ecosystem=Ecosystem.PYPI
            )
        )
    return obs


def parse_package_json(path: Path) -> list[Observation]:
    obs: list[Observation] = []
    try:
        data = json.loads(path.read_text())
    except Exception:
        return obs
    for section in ("dependencies", "devDependencies"):
        deps = data.get(section)
        if isinstance(deps, dict):
            for name, ver in deps.items():
                vs = str(ver)
                if vs.startswith("^") or vs.startswith("~"):
                    vs = vs[1:]
                if vs.startswith("file:") or vs.startswith("link:") or vs.startswith("github:"):
                    continue  # skip non-version refs
                aid = f"npm:{path.name}:{section}:{name}"
                obs.append(
                    _mk_obs(
                        aid,
                        name,
                        vs,
                        f"manifest:{path.name}:{section}:{name}",
                        ecosystem=Ecosystem.NPM,
                    )
                )
    return obs


def parse_go_mod(path: Path) -> list[Observation]:
    obs: list[Observation] = []
    text = path.read_text()
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("require "):
            # single line or block start? handle single line: require foo v1.2.3
            parts = s.split()
            if len(parts) >= 3:
                name = parts[1]
                ver = parts[2].lstrip("v") if parts[2].startswith("v") else parts[2]
                aid = f"go:{path.name}:{i}:{name}"
                obs.append(
                    _mk_obs(
                        aid, name, ver, f"manifest:{path.name}:require:{name}", ecosystem=Ecosystem.GOLANG
                    )
                )
        elif s and not s.startswith("//") and not s.startswith("module") and not s.startswith("go ") and not s.startswith(")"):
            # inside require block: foo v1.2.3
            parts = s.split()
            if len(parts) >= 2 and not parts[0].startswith("//"):
                name = parts[0]
                ver = parts[1].lstrip("v") if parts[1].startswith("v") else parts[1]
                aid = f"go:{path.name}:{i}:{name}"
                obs.append(
                    _mk_obs(
                        aid, name, ver, f"manifest:{path.name}:require:{name}", ecosystem=Ecosystem.GOLANG
                    )
                )
    return obs


def parse_manifest(path: Path) -> list[Observation]:
    name = path.name.lower()
    if name == "requirements.txt":
        return parse_requirements_txt(path)
    if name == "package.json":
        return parse_package_json(path)
    if name == "go.mod":
        return parse_go_mod(path)
    return []
