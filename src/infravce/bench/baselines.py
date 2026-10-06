"""Run a baseline tool against the lab and emit a PredictionSet.

Adapters are deliberately dumb. Each one shells out to the tool, parses what it
emitted, and records what was found. No filtering, no deduping, no dropping of
results a human would consider wrong, because a baseline that is tidied up
before scoring stops being a measurement of that tool.

Shared guard: every adapter records ``matched_asset=False`` for findings against
assets outside the lab manifest, so the scorer can charge them as discovery
errors rather than false positives (threat 12).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Final

from .schema import Prediction, PredictionSet

#: Loopback ports published by bench/infra-cve-bench/lab/docker-compose.yml,
#: mapped to the asset ids used in ground truth. Kept here rather than discovered
#: so a tool cannot be credited for finding an asset it was simply handed.
LAB_ASSETS: Final[dict[str, str]] = {
    "18080": "lab:debian12-backport-curl",
    "18081": "lab:debian12-deferred-patch",
    "18082": "lab:decoy-banner",
    "18083": "lab:waf-proxy",
    "18084": "lab:known-safe",
}

#: Assets with no listening port, reachable only through a volume or the network.
LAB_VOLUME_ASSETS: Final[dict[str, str]] = {
    "alpine319-backport-openssl": "lab:alpine319-backport-openssl",
    "alpine-outdated-openssl": "lab:alpine-outdated-openssl",
    "ci-unparseable": "lab:ci-unparseable",
    "ambiguous-poco": "lab:ambiguous-poco",
    "waffront-origin": "lab:waffront-origin",
}


def _run(cmd: list[str], *, timeout: int = 900) -> subprocess.CompletedProcess[str]:
    """Run a tool and return the result, never raising on a non-zero exit.

    A baseline that exits non-zero on findings is normal, and treating that as a
    crash would silently drop the exact cases being measured.
    """
    return subprocess.run(  # noqa: S603
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _tools_installed() -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    for tool in ("trivy", "grype", "osv-scanner"):
        path = shutil.which(tool)
        if not path:
            out[tool] = None
            continue
        proc = _run([tool, "--version"], timeout=60)
        first = (proc.stdout or proc.stderr).strip().splitlines()
        out[tool] = first[0].strip() if first else None
    return out


def run_trivy(image: str, asset_id: str, gt_version: str, snapshot: date) -> PredictionSet:
    """Trivy in image mode.

    Trivy needs network access for its vulnerability database. In this
    repository that is a deliberate, one-off action at benchmark setup time,
    never something the scanning pipeline itself does at runtime.
    """
    proc = _run(
        [
            "trivy",
            "image",
            "--format",
            "json",
            "--scanners",
            "vuln",
            "--quiet",
            image,
        ]
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(f"trivy failed on {image}: {proc.stderr.strip()[:400]}")

    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"trivy emitted non-JSON for {image}") from exc

    predictions: list[Prediction] = []
    for result in data.get("Results") or []:
        for vuln in result.get("Vulnerabilities") or []:
            cve = vuln.get("VulnerabilityID") or ""
            if not cve.startswith(("CVE-", "GHSA-")):
                # Trivy reports distro vendor IDs like DLA-1234-1 too. They are
                # recorded as evidence, not as findings, because ground truth is
                # keyed on CVE and GHSA ids only.
                continue
            status = (vuln.get("Status") or "").lower()
            predictions.append(
                Prediction(
                    asset_id=asset_id,
                    cve_id=cve,
                    verdict="affected" if status in {"fixed", "affected"} else "not_affected",
                    product=(vuln.get("PkgName") or "").strip() or None,
                    version=(vuln.get("InstalledVersion") or "").strip() or None,
                    advisory_source="trivy",
                    evidence=json.dumps(
                        {
                            "status": vuln.get("Status"),
                            "fixed_version": vuln.get("FixedVersion"),
                            "title": vuln.get("Title"),
                            "primary_url": vuln.get("PrimaryURL"),
                            "data_source": vuln.get("DataSource"),
                        }
                    )[:500],
                    matched_asset=True,
                )
            )

    return PredictionSet(
        tool="trivy",
        tool_version=_tools_installed().get("trivy"),
        mode="image",
        ground_truth_version=gt_version,
        snapshot_date=snapshot,
        predictions=tuple(predictions),
        notes=f"image {image}",
    )


def run_grype_sbom(
    sbom_path: Path, asset_id: str, gt_version: str, snapshot: date
) -> PredictionSet:
    """Grype against a CycloneDX SBOM.

    Uses the SBOM path specifically because grype's SBOM and image paths can
    disagree (trivy#7850). That divergence is itself a benchmark result, so the
    SBOM path is used here and the image path is a separate run.
    """
    proc = _run(
        ["grype", f"sbom:{sbom_path}", "--output", "json", "--quiet"],
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(f"grype failed on {sbom_path}: {proc.stderr.strip()[:400]}")

    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"grype emitted non-JSON for {sbom_path}") from exc

    predictions: list[Prediction] = []
    for match in data.get("matches") or []:
        vuln = match.get("vulnerability") or {}
        cve = vuln.get("id") or ""
        if not cve.startswith(("CVE-", "GHSA-")):
            continue
        art = match.get("artifact") or {}
        predictions.append(
            Prediction(
                asset_id=asset_id,
                cve_id=cve,
                verdict="affected",
                product=(art.get("name") or "").strip() or None,
                version=(art.get("version") or "").strip() or None,
                advisory_source="grype",
                evidence=json.dumps(
                    {
                        "namespace": vuln.get("namespace"),
                        "severity": vuln.get("severity"),
                        "fix_state": (match.get("fix") or {}).get("state"),
                        "fix_versions": (match.get("fix") or {}).get("versions"),
                    }
                )[:500],
                matched_asset=True,
            )
        )

    return PredictionSet(
        tool="grype",
        tool_version=_tools_installed().get("grype"),
        mode="sbom",
        ground_truth_version=gt_version,
        snapshot_date=snapshot,
        predictions=tuple(predictions),
        notes=f"sbom {sbom_path.name}",
    )


def run_osv_scanner(
    lockfile_or_dir: Path, asset_id: str, gt_version: str, snapshot: date
) -> PredictionSet:
    """OSV-Scanner against a lockfile or directory tree."""
    proc = _run(["osv-scanner", "--format", "json", str(lockfile_or_dir)])
    # OSV-Scanner exits non-zero when it finds vulnerabilities; stdout is still
    # valid JSON, so a non-zero exit is not treated as failure.
    if not proc.stdout.strip():
        raise RuntimeError(f"osv-scanner produced no output for {lockfile_or_dir}")

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"osv-scanner emitted non-JSON for {lockfile_or_dir}") from exc

    predictions: list[Prediction] = []
    for result in data.get("results") or []:
        for pkg in result.get("packages") or []:
            package = pkg.get("package") or {}
            for vuln in pkg.get("vulnerabilities") or []:
                aliases = [a for a in (vuln.get("aliases") or []) if a.startswith("CVE-")]
                ids = [vuln.get("id") or "", *aliases]
                cve = next((i for i in ids if i.startswith("CVE-")), None)
                if cve is None:
                    cve = next((i for i in ids if i.startswith("GHSA-")), None)
                if cve is None:
                    continue
                predictions.append(
                    Prediction(
                        asset_id=asset_id,
                        cve_id=cve,
                        verdict="affected",
                        product=(package.get("name") or "").strip() or None,
                        version=(package.get("version") or "").strip() or None,
                        advisory_source="osv-scanner",
                        evidence=json.dumps(
                            {"id": vuln.get("id"), "modified": vuln.get("modified")}
                        )[:500],
                        matched_asset=True,
                    )
                )

    return PredictionSet(
        tool="osv-scanner",
        tool_version=_tools_installed().get("osv-scanner"),
        mode="lockfile",
        ground_truth_version=gt_version,
        snapshot_date=snapshot,
        predictions=tuple(predictions),
        notes=f"input {lockfile_or_dir}",
    )


def available() -> dict[str, str | None]:
    return _tools_installed()


def main(argv: list[str] | None = None) -> int:
    """Report which baselines are installed.

    Deliberately does not run a scan. Each adapter needs different inputs (an
    image reference, an SBOM, a lockfile) and the right choice depends on what
    the operator has available, so this only tells them what is missing.
    """
    args = sys.argv[1:] if argv is None else argv
    versions = _tools_installed()

    if "--json" in args:
        print(json.dumps(versions, indent=2))
        return 0

    print("baseline availability:")
    for tool, version in versions.items():
        state = version or "NOT INSTALLED"
        print(f"  {tool:<14} {state}")

    missing = [t for t, v in versions.items() if v is None]
    if missing:
        print(f"\n{len(missing)} baseline(s) unavailable: {', '.join(missing)}")
        print("Results from a partial baseline set are valid, but the comparison is")
        print("not. Record which tools ran in the run manifest.")
        return 1
    return 0


__all__ = [
    "LAB_ASSETS",
    "LAB_VOLUME_ASSETS",
    "available",
    "main",
    "run_grype_sbom",
    "run_osv_scanner",
    "run_trivy",
]
