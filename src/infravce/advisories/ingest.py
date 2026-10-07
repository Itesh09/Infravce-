"""Advisory ingest with optional local cache support.

Reads a local advisory cache (JSON). Accepts either a list of advisory records or
the ground-truth cases.json shape (maps cases to advisory-like entries).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from infravce.models import AdvisorySource, Ecosystem, ScanCoverage


@dataclass(frozen=True, slots=True)
class AdvisoryRecord:
    advisory_id: str
    source: AdvisorySource
    ecosystem: Ecosystem
    product: str
    versions: tuple[str, ...] = ()
    ranges: tuple[dict, ...] = ()
    distro_state: str | None = None
    fixed_version: str | None = None
    published_at: datetime | None = None
    url: str | None = None
    raw: dict | None = None


@dataclass(frozen=True, slots=True)
class IngestResult:
    records: tuple[AdvisoryRecord, ...]
    coverages: tuple[ScanCoverage, ...]


def _parse_dt(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        # handle Z
        if s.endswith("Z"):
            s2 = s[:-1] + "+00:00"
        else:
            s2 = s
        dt = datetime.fromisoformat(s2)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC)
    except Exception:
        return None


def _to_ecosystem(e: str | None) -> Ecosystem:
    try:
        if e:
            return Ecosystem(e)
    except Exception:
        pass
    return Ecosystem.UNKNOWN


def ingest(cache_path: Path | str | None = None) -> IngestResult:
    records: list[AdvisoryRecord] = []
    coverages: list[ScanCoverage] = []

    if cache_path:
        p = Path(cache_path)
        if p.exists():
            try:
                data = json.loads(p.read_text())
            except Exception:
                data = None
            if isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict):
                        continue
                        adv_id = str(item.get("advisory_id") or item.get("cve_id") or item.get("id") or "ADV")
                    prod = str(item.get("product") or "")
                    src = str(item.get("source") or "osv")
                    try:
                        src_e = AdvisorySource(str(src).lower())
                    except Exception:
                        src_e = AdvisorySource.OSV
                    ecos = _to_ecosystem(item.get("ecosystem"))
                    versions = tuple(str(v) for v in item.get("versions", []) if isinstance(v, (str, int, float)))
                    fixed = item.get("fixed_version") or item.get("fixed")
                    rec = AdvisoryRecord(
                        advisory_id=adv_id,
                        source=src_e,
                        ecosystem=ecos,
                        product=prod,
                        versions=versions,
                        distro_state=item.get("distro_state"),
                        fixed_version=str(fixed) if fixed is not None else None,
                        published_at=_parse_dt(item.get("published_at")),
                        url=item.get("url"),
                        raw=item,
                    )
                    records.append(rec)
            elif isinstance(data, dict) and "cases" in data and isinstance(data["cases"], list):
                for c in data["cases"]:
                    if not isinstance(c, dict):
                        continue
                    cve = str(c.get("cve_id") or c.get("case_id") or "")
                    prod = str(c.get("product") or "")
                    ver = c.get("version")
                    ecos = _to_ecosystem(c.get("ecosystem"))
                    prov = c.get("provenance") or {}
                    src_str = prov.get("source") or "osv"
                    try:
                        src_e = AdvisorySource(str(src_str).lower())
                    except Exception:
                        src_e = AdvisorySource.OSV
                    rec = AdvisoryRecord(
                        advisory_id=cve or f"case-{c.get('case_id')}",
                        source=src_e,
                        ecosystem=ecos,
                        product=prod,
                        versions=(str(ver),) if ver is not None else (),
                        distro_state=c.get("distro_state"),
                        fixed_version=c.get("fixed_version"),
                        published_at=_parse_dt(prov.get("snapshot_date")),
                        url=None,
                        raw=c,
                    )
                    records.append(rec)
            coverages.append(
                ScanCoverage(
                    source=AdvisorySource.OSV,
                    ecosystem=Ecosystem.UNKNOWN,
                    last_successful_ingest=datetime.now(UTC),
                    record_count=len(records),
                    is_stale=False,
                    known_gaps=(),
                )
            )
            return IngestResult(records=tuple(records), coverages=tuple(coverages))

    coverages.append(
        ScanCoverage(
            source=AdvisorySource.OSV,
            ecosystem=Ecosystem.UNKNOWN,
            last_successful_ingest=None,
            record_count=0,
            is_stale=True,
            known_gaps=("no local cache provided",),
        )
    )
    return IngestResult(records=(), coverages=tuple(coverages))


__all__ = ["AdvisoryRecord", "IngestResult", "ingest"]
