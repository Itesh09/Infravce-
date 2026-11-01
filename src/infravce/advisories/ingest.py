"""Advisory ingest.

Two entry points, both returning the same shape:

* :func:`ingest` reads a local advisory file. Used by the benchmark fixtures and
  by offline replay, and kept because a report must be reproducible without a
  network.
* :func:`ingest_observed` queries a live source (currently OSV) for exactly the
  packages that were discovered, and reports per-source coverage.

The coverage rule is the point of this module. A source that failed is recorded
with ``last_successful_ingest=None``; a source that was never asked is recorded
as a gap. Neither is allowed to look like "checked, nothing found", because that
is the failure mode the whole project is about (docs/02-architecture.md P6).
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from infravce.models import AdvisorySource, Ecosystem, Observation, ScanCoverage


@dataclass(frozen=True, slots=True)
class AdvisoryRecord:
    advisory_id: str
    source: AdvisorySource
    ecosystem: Ecosystem
    product: str
    versions: tuple[str, ...] = ()
    ranges: tuple[dict[str, Any], ...] = ()
    distro_state: str | None = None
    fixed_version: str | None = None
    published_at: datetime | None = None
    url: str | None = None
    raw: dict[str, Any] | None = None

    #: OSV-style half-open intervals ``(introduced, fixed)``. ``None`` for
    #: ``fixed`` means the range is still open. Kept separate from ``versions``
    #: because "enumerated affected versions" and "a range" are different
    #: claims, and collapsing them loses the boundary that decides the verdict.
    affected_ranges: tuple[tuple[str | None, str | None], ...] = ()
    aliases: tuple[str, ...] = ()
    severity: str | None = None
    cvss: float | None = None
    summary: str | None = None
    #: The ecosystem string the source was actually queried with, e.g.
    #: ``Debian:12``. Recorded so a wrong-release query is visible after the fact.
    queried_as: str | None = None


@dataclass(frozen=True, slots=True)
class IngestResult:
    records: tuple[AdvisoryRecord, ...]
    coverages: tuple[ScanCoverage, ...] = field(default=())


def _parse_dt(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def _to_ecosystem(e: str | None) -> Ecosystem:
    try:
        if e:
            return Ecosystem(e)
    except ValueError:
        pass
    return Ecosystem.UNKNOWN


_SOURCE_NAMES = {
    "debian security tracker": AdvisorySource.DISTRO_TRACKER,
    "debian": AdvisorySource.DISTRO_TRACKER,
    "alpine secdb": AdvisorySource.DISTRO_TRACKER,
    "ubuntu security": AdvisorySource.DISTRO_TRACKER,
    "rhsa": AdvisorySource.DISTRO_TRACKER,
    "vendor": AdvisorySource.VENDOR_ADVISORY,
    "nvd": AdvisorySource.NVD,
    "ghsa": AdvisorySource.GHSA,
    "osv": AdvisorySource.OSV,
}


def _source(name: str | None) -> AdvisorySource:
    if not name:
        return AdvisorySource.OSV
    lowered = name.strip().lower()
    if lowered in _SOURCE_NAMES:
        return _SOURCE_NAMES[lowered]
    try:
        return AdvisorySource(lowered)
    except ValueError:
        return AdvisorySource.OSV


def _record_from_mapping(item: dict[str, Any]) -> AdvisoryRecord:
    adv_id = str(item.get("advisory_id") or item.get("cve_id") or item.get("id") or "ADV")
    fixed = item.get("fixed_version") or item.get("fixed")
    affected_ranges: list[tuple[str | None, str | None]] = []
    for entry in item.get("affected_ranges") or []:
        if isinstance(entry, dict):
            affected_ranges.append(
                (
                    str(entry["introduced"]) if entry.get("introduced") is not None else None,
                    str(entry["fixed"]) if entry.get("fixed") is not None else None,
                )
            )
        elif isinstance(entry, (list, tuple)) and len(entry) == 2:
            affected_ranges.append(
                (
                    str(entry[0]) if entry[0] is not None else None,
                    str(entry[1]) if entry[1] is not None else None,
                )
            )
    return AdvisoryRecord(
        advisory_id=adv_id,
        source=_source(item.get("source")),
        ecosystem=_to_ecosystem(item.get("ecosystem")),
        product=str(item.get("product") or ""),
        versions=tuple(str(v) for v in item.get("versions", []) if isinstance(v, (str, int, float))),
        distro_state=item.get("distro_state") or item.get("status"),
        fixed_version=str(fixed) if fixed is not None else None,
        published_at=_parse_dt(item.get("published_at")),
        url=item.get("url"),
        raw=item,
        affected_ranges=tuple(affected_ranges),
        aliases=tuple(str(a) for a in item.get("aliases") or []),
        severity=item.get("severity"),
        cvss=float(item["cvss"]) if isinstance(item.get("cvss"), (int, float)) else None,
        summary=item.get("summary"),
        queried_as=item.get("queried_as") or item.get("ecosystem"),
    )


def _record_from_case(case: dict[str, Any]) -> AdvisoryRecord:
    cve = str(case.get("cve_id") or case.get("case_id") or "")
    provenance = case.get("provenance") or {}
    state = case.get("distro_state") or case.get("status")
    if not state:
        truth = str(case.get("truth", "")).lower()
        state = {
            "not_affected": "not-affected",
            "fixed": "resolved",
            "affected": "open",
            "under_investigation": "undetermined",
        }.get(truth)
    return AdvisoryRecord(
        advisory_id=cve or f"case-{case.get('case_id')}",
        source=_source(provenance.get("source")),
        ecosystem=_to_ecosystem(case.get("ecosystem")),
        product=str(case.get("product") or ""),
        versions=(str(case["version"]),) if case.get("version") is not None else (),
        distro_state=state,
        fixed_version=case.get("fixed_version"),
        published_at=_parse_dt(provenance.get("snapshot_date")),
        url=None,
        raw=case,
    )


def _load_file(path: Path) -> tuple[list[AdvisoryRecord], list[str]]:
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        return [], [f"{path.name}: unreadable ({type(exc).__name__})"]
    if isinstance(data, list):
        return [_record_from_mapping(i) for i in data if isinstance(i, dict)], []
    if isinstance(data, dict) and isinstance(data.get("cases"), list):
        return [_record_from_case(c) for c in data["cases"] if isinstance(c, dict)], []
    return [], [f"{path.name}: unrecognised advisory file shape"]


def _coverage_from_records(records: list[AdvisoryRecord], when: datetime) -> list[ScanCoverage]:
    """One row per source that actually contributed a record.

    The previous version emitted a single ``OSV`` row regardless of where the
    records came from, which made the coverage report claim a feed had been
    ingested when it had not been contacted at all.
    """
    by_source: dict[AdvisorySource, list[AdvisoryRecord]] = {}
    for record in records:
        by_source.setdefault(record.source, []).append(record)
    rows = [
        ScanCoverage(
            source=source,
            ecosystem=Ecosystem.UNKNOWN,
            last_successful_ingest=when,
            record_count=len(group),
            is_stale=False,
            known_gaps=("loaded from a local file; not a freshness signal",),
        )
        for source, group in sorted(by_source.items(), key=lambda kv: kv[0].precedence_rank)
    ]
    return rows


def ingest(cache_path: Path | str | None = None) -> IngestResult:
    """Load a local advisory file (list shape or ground-truth ``cases`` shape)."""
    if cache_path is None:
        return IngestResult((), (_never_ingested("no advisory source configured"),))

    path = Path(cache_path)
    if not path.exists():
        return IngestResult((), (_never_ingested(f"advisory file not found: {path}"),))

    records, gaps = _load_file(path)
    now = datetime.now(UTC)
    coverages = _coverage_from_records(records, now)
    if gaps:
        coverages.append(
            ScanCoverage(
                source=AdvisorySource.UNKNOWN,
                last_successful_ingest=None,
                record_count=0,
                is_stale=True,
                known_gaps=tuple(gaps),
            )
        )
    return IngestResult(records=tuple(records), coverages=tuple(coverages))


def _never_ingested(reason: str) -> ScanCoverage:
    return ScanCoverage(
        source=AdvisorySource.UNKNOWN,
        last_successful_ingest=None,
        record_count=0,
        is_stale=True,
        known_gaps=(reason,),
    )


def _package_key(observation: Observation) -> tuple[str, Ecosystem] | None:
    product = (observation.resolved_product or observation.raw_product or "").strip().lower()
    if not product:
        return None
    version = observation.resolved_version
    ecosystem = version.ecosystem if version else Ecosystem.UNKNOWN
    return product, ecosystem


def ingest_observed(
    observations: Iterable[Observation],
    *,
    os_release: str | None = None,
    cache_dir: Path | str = ".infravce-cache/osv",
    allow_network: bool = True,
    local_advisories: Path | str | None = None,
) -> IngestResult:
    """Query OSV for every distinct package that was actually observed.

    Only observed packages are queried. Fetching a whole feed and filtering
    afterwards would make scan time independent of the target, which is the
    wrong shape for an infrastructure scanner and makes the freshness claim
    cover data that was never used.
    """
    from . import osv as osv_feed  # local import: osv imports AdvisoryRecord from here
    records: list[AdvisoryRecord] = []
    coverages: list[ScanCoverage] = []

    if local_advisories:
        local = ingest(local_advisories)
        records.extend(local.records)
        coverages.extend(local.coverages)

    wanted: dict[tuple[str, Ecosystem], str] = {}
    skipped: list[str] = []
    for observation in observations:
        key = _package_key(observation)
        if key is None or not observation.is_usable_for_matching:
            continue
        product, ecosystem = key
        label = osv_feed.ecosystem_label(ecosystem, os_release)
        if label is None:
            skipped.append(f"{product}: no OSV ecosystem for {ecosystem.value}")
            continue
        wanted[key] = label

    by_label: dict[str, list[tuple[str, osv_feed.OSVCacheEntry]]] = {}
    for (product, ecosystem), label in sorted(wanted.items()):
        entry = osv_feed.fetch_package(
            product,
            ecosystem,
            os_release=os_release,
            cache_dir=cache_dir,
            allow_network=allow_network,
        )
        by_label.setdefault(label, []).append((product, entry))
        if entry.error:
            continue
        records.extend(
            osv_feed.records_from_vulns(
                entry.vulns,
                product=product,
                ecosystem=ecosystem,
                queried_as=label,
            )
        )

    for label, entries in sorted(by_label.items()):
        coverages.append(
            osv_feed.coverage_for(
                entries,
                ecosystem=_ecosystem_of_label(label),
                label=label,
            )
        )

    if skipped:
        coverages.append(
            ScanCoverage(
                source=AdvisorySource.UNKNOWN,
                last_successful_ingest=None,
                record_count=0,
                is_stale=True,
                known_gaps=tuple(dict.fromkeys(skipped)),
            )
        )
    if not by_label:
        coverages.append(_never_ingested("no observed package had a queryable ecosystem"))
    return IngestResult(records=tuple(records), coverages=tuple(coverages))


def ingest_inventory(
    observations: Iterable[Observation],
    *,
    os_release: str | None = None,
    cache_dir: Path | str = ".infravce-cache/osv",
    allow_network: bool = True,
    local_advisories: Path | str | None = None,
    max_vulns: int = 800,
) -> IngestResult:
    """Query OSV for an exact package inventory using ``querybatch``.

    Only observations that carry a resolved version are eligible: a versionless
    package cannot be range-matched, and asking OSV about it would return the
    entire history for the name. Queries are deduplicated by
    ``(package, ecosystem, version)`` because a package database lists every
    binary built from one source package and they share an advisory record.

    ``querybatch`` is used as a **candidate index** only. It answers "which
    advisories mention this exact version"; the full records are then fetched
    and :func:`infravce.advisories.match.match_observations` re-evaluates every
    range with the project's own comparator. If the two disagree, the local
    engine wins and the disagreement is visible in the vote's evidence.
    """
    from . import osv as osv_feed

    records: list[AdvisoryRecord] = []
    coverages: list[ScanCoverage] = []

    if local_advisories:
        local = ingest(local_advisories)
        records.extend(local.records)
        coverages.extend(local.coverages)

    wanted: dict[tuple[str, str, str], tuple[Ecosystem, str]] = {}
    skipped: list[str] = []
    for observation in observations:
        if not observation.is_usable_for_matching or not observation.raw_version:
            continue
        product = (observation.resolved_product or observation.raw_product or "").strip().lower()
        version = observation.resolved_version
        if not product or version is None:
            continue
        label = osv_feed.ecosystem_label(version.ecosystem, os_release)
        if label is None:
            skipped.append(f"{product}: no OSV ecosystem for {version.ecosystem.value}")
            continue
        wanted[(product, label, observation.raw_version)] = (version.ecosystem, label)

    if not wanted:
        coverages.append(_never_ingested("no exact-version inventory to query"))
        return IngestResult((), tuple(coverages))

    keys = sorted(wanted)
    queries = [
        {"package": {"name": product, "ecosystem": label}, "version": raw_version}
        for product, label, raw_version in keys
    ]
    batch = osv_feed.fetch_batch(queries, cache_dir=cache_dir, allow_network=allow_network)

    # One fetch per unique vulnerability, not per package/vulnerability pair:
    # a source package's binaries produce identical ids.
    ids: list[str] = []
    seen_ids: set[str] = set()
    for entry in batch:
        for vuln_id in entry.vuln_ids:
            if vuln_id not in seen_ids:
                seen_ids.add(vuln_id)
                ids.append(vuln_id)
    truncated = ids[max_vulns:]
    selected = ids[:max_vulns]

    fetched: dict[str, dict[str, Any]] = {}
    fetch_errors: list[str] = []
    oldest: datetime | None = None
    fetched_entries: dict[str, Any] = osv_feed.fetch_vulns(
        selected, cache_dir=cache_dir, allow_network=allow_network
    )
    for vuln_id, entry in fetched_entries.items():
        if entry.error:
            fetch_errors.append(f"{vuln_id}: {entry.error}")
            continue
        fetched[vuln_id] = entry.vulns[0]
        if oldest is None or entry.fetched_at < oldest:
            oldest = entry.fetched_at

    by_label: dict[str, list[dict[str, Any]]] = {}
    batch_errors: dict[str, list[str]] = {}
    for (product, label, _version), entry in zip(keys, batch, strict=False):
        if entry.error:
            batch_errors.setdefault(label, []).append(f"{product}: {entry.error}")
            continue
        vulns = [fetched[vuln_id] for vuln_id in entry.vuln_ids if vuln_id in fetched]
        if not vulns:
            continue
        by_label.setdefault(label, []).extend(vulns)
        records.extend(
            osv_feed.records_from_vulns(
                vulns,
                product=product,
                ecosystem=wanted[(product, label, _version)][0],
                queried_as=label,
            )
        )

    now = datetime.now(UTC)
    for label in sorted(set(label for _, label, _ in keys)):
        label_records = [
            record for record in records if record.queried_as == label
        ]
        gaps = list(batch_errors.get(label, []))
        if ":" not in label and label.split(":", 1)[0].lower() in {
            "debian",
            "ubuntu",
            "alpine",
            "red hat",
        }:
            gaps.append(
                "distribution release not specified; records from every release "
                "were merged, so fix boundaries may belong to another release"
            )
        if fetch_errors:
            gaps.append(f"{len(fetch_errors)} vulnerability record(s) could not be fetched")
        if truncated and label_records:
            gaps.append(f"{len(truncated)} candidate vulnerability record(s) not fetched (cap {max_vulns})")
        coverages.append(
            ScanCoverage(
                source=AdvisorySource.OSV,
                ecosystem=_ecosystem_of_label(label),
                last_successful_ingest=oldest or now,
                record_count=len(label_records),
                is_stale=oldest is None,
                known_gaps=tuple(dict.fromkeys(gaps)),
                detail_url="https://osv.dev",
            )
        )

    if skipped:
        coverages.append(
            ScanCoverage(
                source=AdvisorySource.UNKNOWN,
                last_successful_ingest=None,
                record_count=0,
                is_stale=True,
                known_gaps=tuple(dict.fromkeys(skipped)),
            )
        )
    return IngestResult(records=tuple(records), coverages=tuple(coverages))


def _ecosystem_of_label(label: str) -> Ecosystem:
    base = label.split(":", 1)[0].strip().lower()
    return {
        "debian": Ecosystem.DEBIAN,
        "ubuntu": Ecosystem.UBUNTU,
        "alpine": Ecosystem.APK,
        "red hat": Ecosystem.RPM,
        "pypi": Ecosystem.PYPI,
        "npm": Ecosystem.NPM,
        "go": Ecosystem.GOLANG,
        "maven": Ecosystem.MAVEN,
        "nuget": Ecosystem.NUGET,
        "conancenter": Ecosystem.CONAN,
        "github actions": Ecosystem.GITHUB,
    }.get(base, Ecosystem.UNKNOWN)


__all__ = ["AdvisoryRecord", "IngestResult", "ingest", "ingest_inventory", "ingest_observed"]
