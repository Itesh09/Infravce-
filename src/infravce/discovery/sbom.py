"""SBOM parsing (minimal, read-only).

Supports CycloneDX JSON (``bomFormat`` == ``CycloneDX``) and SPDX JSON
(``spdxVersion`` or ``SPDXID``). The parser preserves raw strings verbatim for
provenance: ``raw_product`` and ``raw_version`` are never massaged here. All
normalisation and identity resolution happen downstream.

This is intentionally small (the bench doesn't need full spec compliance). The
goal is to turn declared inventory into :class:`Observation` records with correct
``acquisition_method`` and provenance.
"""
from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from infravce.models import (
    AcquisitionMethod,
    Asset,
    Ecosystem,
    NormalisedVersion,
    Observation,
)
from infravce.normalise.versions import normalise
from infravce.identity.resolver import resolve_identity


def _mk_obs(
    *,
    asset_id: str,
    product: str,
    version: str,
    evidence: str,
    method: AcquisitionMethod,
) -> Observation:
    product_s = (product or "").strip()
    version_s = (version or "").strip() if version is not None else ""

    nv = normalise(version_s, product=product_s)
    res = resolve_identity(product_s, ecosystem=nv.ecosystem, version=version_s if nv.is_resolved else None)

    return Observation(
        asset_id=asset_id,
        acquisition_method=method,
        evidence=evidence,
        raw_product=product_s,
        raw_version=version_s,
        resolved_product=res.canonical_name if res.canonical_name else (product_s or None),
        resolved_version=nv if nv.is_resolved else None,
        resolution_confidence=nv.confidence if nv.is_resolved else 0.0,
        parse_notes=nv.notes,
    )


def _asset_id_for(component: dict[str, Any]) -> str:
    """Derive a stable-ish asset id from component identity."""
    # Prefer purl if present
    purl = component.get("purl")
    if isinstance(purl, str) and purl:
        return purl
    name = component.get("name") or ""
    ver = component.get("version") or ""
    bom_ref = component.get("bom-ref") or component.get("bomRef") or ""
    if bom_ref:
        return str(bom_ref)
    return f"{name}:{ver}" or "asset"


def _iter_cyclonedx_components(data: dict[str, Any]) -> Iterator[tuple[dict[str, Any], str]]:
    """Yield (component, evidence_path) for CycloneDX."""
    # components at top level
    comps = data.get("components")
    if isinstance(comps, list):
        for c in comps:
            if isinstance(c, dict):
                yield c, "components[]"
    # also check metadata.component
    md = data.get("metadata")
    if isinstance(md, dict):
        mc = md.get("component")
        if isinstance(mc, dict):
            yield mc, "metadata.component"


def _iter_spdx_packages(data: dict[str, Any]) -> Iterator[tuple[dict[str, Any], str]]:
    pkgs = data.get("packages")
    if isinstance(pkgs, list):
        for p in pkgs:
            if isinstance(p, dict):
                yield p, "packages[]"
    # sometimes files? not needed for deps


def parse_cyclonedx_json(path: Path) -> list[Observation]:
    data = json.loads(path.read_text())
    obs: list[Observation] = []
    for comp, evp in _iter_cyclonedx_components(data):
        name = comp.get("name") or comp.get("purl") or ""
        ver = comp.get("version") or ""
        # extract name from purl if missing
        if not name and isinstance(comp.get("purl"), str):
            p = comp["purl"]
            if "/" in p:
                name = p.rsplit("/", 1)[1]
                if "@" in name:
                    name = name.split("@", 1)[0]
        if not name:
            continue
        aid = _asset_id_for(comp)
        evidence = f"sbom:{path.name}:{evp}:{aid}"
        obs.append(
            _mk_obs(
                asset_id=aid,
                product=name,
                version=ver,
                evidence=evidence,
                method=AcquisitionMethod.SBOM,
            )
        )
    return obs


def parse_spdx_json(path: Path) -> list[Observation]:
    data = json.loads(path.read_text())
    obs: list[Observation] = []
    for pkg, evp in _iter_spdx_packages(data):
        name = pkg.get("name") or pkg.get("packageName") or ""
        ver = pkg.get("versionInfo") or pkg.get("version") or ""
        if not name:
            continue
        # derive id
        spdxid = pkg.get("SPDXID") or pkg.get("spdxid") or ""
        aid = spdxid or f"{name}:{ver}"
        evidence = f"sbom:{path.name}:{evp}:{aid}"
        obs.append(
            _mk_obs(
                asset_id=aid,
                product=name,
                version=ver,
                evidence=evidence,
                method=AcquisitionMethod.SBOM,
            )
        )
    return obs


def parse_sbom(path: Path) -> list[Observation]:
    """Parse SBOM file (CycloneDX JSON or SPDX JSON)."""
    try:
        data = json.loads(path.read_text())
    except Exception:
        return []

    # detect
    bomfmt = data.get("bomFormat") or data.get("bomformat")
    spdxver = data.get("spdxVersion") or data.get("SPDXVersion")
    spdxid = data.get("SPDXID")
    if bomfmt == "CycloneDX" or "components" in data or "metadata" in data and data["metadata"].get("component"):
        # Heuristic: prefer CycloneDX if components present
        pass

    # simple detection
    if bomfmt and "cyclone" in str(bomfmt).lower():
        return parse_cyclonedx_json(path)
    if spdxver or spdxid or "packages" in data:
        # treat as SPDX if packages present
        return parse_spdx_json(path)
    # fallback: try CycloneDX first if components exist
    if "components" in data:
        return parse_cyclonedx_json(path)
    if "packages" in data:
        return parse_spdx_json(path)
    return []
