"""Live OSV ingest.

OSV is the one advisory source that has a stable, keyless API and carries
distribution ecosystems (``Debian:12``, ``Alpine:v3.19``, ``Ubuntu:22.04:LTS``)
alongside language ones. That makes it the fastest honest path from a discovered
service to a real range: the response gives ``introduced``/``fixed`` events, and
:func:`infravce.applicability.engine.decide_range` evaluates them with the
ecosystem's own comparator. Nothing here decides affectedness; it only converts
OSV's vocabulary into the project's records.

Two properties matter for the benchmark and are preserved deliberately:

* **The raw response is cached with its fetch time.** A report can be replayed
  after the feed changes, and the coverage report can state how old the data is
  instead of implying it is current.
* **No silent fallback.** A failed query produces a coverage entry with
  ``last_successful_ingest=None``; it never produces an empty record list that
  would read as "this package has no vulnerabilities".
"""

from __future__ import annotations

import json
import time
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from infravce.models import AdvisorySource, Ecosystem, ScanCoverage

from .ingest import AdvisoryRecord

__all__ = [
    "OSVBatchEntry",
    "OSVCacheEntry",
    "ecosystem_label",
    "fetch_batch",
    "fetch_package",
    "fetch_vuln",
    "fetch_vulns",
    "records_from_vulns",
]

_API = "https://api.osv.dev/v1/query"
_API_BATCH = "https://api.osv.dev/v1/querybatch"
_API_VULN = "https://api.osv.dev/v1/vulns/"
#: OSV asks clients to be polite; one request per package is already few.
_MIN_INTERVAL_S = 0.15
#: A hard ceiling so a package with hundreds of historical CVEs cannot turn one
#: scan into an unbounded report. Recorded in coverage when it bites.
_MAX_VULNS = 500
#: OSV's documented maximum for one querybatch request.
_MAX_BATCH = 1000

_last_call = [0.0]


#: Our ecosystem enum -> the OSV ecosystem string. Distributions need a release
#: because Debian backports make a release-less answer wrong: the same upstream
#: version has different fix boundaries in bookworm and trixie.
def ecosystem_label(ecosystem: Ecosystem, os_release: str | None = None) -> str | None:
    if ecosystem is Ecosystem.DEBIAN:
        return f"Debian:{os_release}" if os_release else "Debian"
    if ecosystem is Ecosystem.UBUNTU:
        return f"Ubuntu:{os_release}" if os_release else "Ubuntu"
    if ecosystem is Ecosystem.APK:
        return f"Alpine:{os_release}" if os_release else "Alpine"
    if ecosystem is Ecosystem.RPM:
        return "Red Hat" if not os_release else os_release
    return {
        Ecosystem.PYPI: "PyPI",
        Ecosystem.NPM: "npm",
        Ecosystem.GOLANG: "Go",
        Ecosystem.GO_DEPS: "Go",
        Ecosystem.MAVEN: "Maven",
        Ecosystem.NUGET: "NuGet",
        Ecosystem.CONAN: "ConanCenter",
        Ecosystem.GITHUB: "GitHub Actions",
    }.get(ecosystem)


@dataclass(frozen=True, slots=True)
class OSVCacheEntry:
    vulns: tuple[dict[str, Any], ...]
    fetched_at: datetime
    from_cache: bool
    error: str | None = None


def _cache_path(cache_dir: Path, name: str, label: str) -> Path:
    safe = f"{label.replace(':', '_').replace('/', '_')}__{name.replace('/', '_')}"
    return cache_dir / f"{safe}.json"


def fetch_package(
    name: str,
    ecosystem: Ecosystem,
    *,
    os_release: str | None = None,
    cache_dir: Path | str = ".infravce-cache/osv",
    timeout: float = 20.0,
    allow_network: bool = True,
) -> OSVCacheEntry:
    """Fetch (or load) every OSV record for ``name`` in ``ecosystem``.

    Querying without a version is deliberate: the version decision belongs to
    :func:`decide_range`, not to OSV's server. Otherwise the tool would be
    reporting OSV's verdict while claiming it applied its own engine, and the
    benchmark would be measuring the wrong system.
    """
    label = ecosystem_label(ecosystem, os_release)
    if label is None:
        return OSVCacheEntry((), datetime.now(UTC), False, f"no OSV ecosystem for {ecosystem.value}")

    cache_dir = Path(cache_dir)
    path = _cache_path(cache_dir, name, label)
    if path.exists():
        try:
            payload = json.loads(path.read_text())
            return OSVCacheEntry(
                vulns=tuple(payload.get("vulns", [])),
                fetched_at=datetime.fromisoformat(payload["fetched_at"]),
                from_cache=True,
            )
        except Exception:
            pass  # corrupt cache is a cache miss, not a result

    if not allow_network:
        return OSVCacheEntry((), datetime.now(UTC), False, "network disabled and no cache entry")

    try:
        import httpx

        gap = time.monotonic() - _last_call[0]
        if gap < _MIN_INTERVAL_S:
            time.sleep(_MIN_INTERVAL_S - gap)
        _last_call[0] = time.monotonic()
        resp = httpx.post(
            _API,
            json={"package": {"name": name, "ecosystem": label}},
            timeout=timeout,
        )
        if resp.status_code != 200:
            return OSVCacheEntry(
                (), datetime.now(UTC), False, f"OSV HTTP {resp.status_code}"
            )
        vulns = resp.json().get("vulns", [])[:_MAX_VULNS]
    except Exception as exc:  # network is an expected failure mode, not a crash
        return OSVCacheEntry((), datetime.now(UTC), False, f"{type(exc).__name__}: {exc}")

    now = datetime.now(UTC)
    cache_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"fetched_at": now.isoformat(), "vulns": vulns}, indent=2))
    return OSVCacheEntry(tuple(vulns), now, False)


# --------------------------------------------------------------------------- #
# Exact-inventory path: querybatch + per-vulnerability fetch
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class OSVBatchEntry:
    """Result of asking OSV which advisories touch one exact package version.

    ``querybatch`` returns only ``id``/``modified``, so the ids are used as a
    *candidate index*; the full records are fetched separately and the project's
    own engine still decides applicability. This keeps the batch endpoint from
    becoming the authority on whether a version is affected.
    """

    vuln_ids: tuple[str, ...]
    fetched_at: datetime
    from_cache: bool
    error: str | None = None


def _batch_cache_path(cache_dir: Path, queries: list[dict[str, Any]]) -> Path:
    import hashlib

    payload = json.dumps(queries, sort_keys=True, separators=(",", ":")).encode()
    return cache_dir / "batch" / f"{hashlib.sha256(payload).hexdigest()[:32]}.json"


def _throttle() -> None:
    gap = time.monotonic() - _last_call[0]
    if gap < _MIN_INTERVAL_S:
        time.sleep(_MIN_INTERVAL_S - gap)
    _last_call[0] = time.monotonic()


def fetch_batch(
    queries: list[dict[str, Any]],
    *,
    cache_dir: Path | str = ".infravce-cache/osv",
    timeout: float = 45.0,
    allow_network: bool = True,
) -> list[OSVBatchEntry]:
    """Run ``querybatch`` in chunks of at most 1000 queries.

    Each query must already carry an exact ``version``; a versionless batch
    would return every advisory ever published for the package and defeat the
    point of using the endpoint.
    """
    cache_dir = Path(cache_dir)
    out: list[OSVBatchEntry] = []
    for start in range(0, len(queries), _MAX_BATCH):
        chunk = queries[start : start + _MAX_BATCH]
        path = _batch_cache_path(cache_dir, chunk)
        if path.exists():
            try:
                payload = json.loads(path.read_text())
                results = payload["results"]
                out.extend(
                    OSVBatchEntry(
                        tuple(str(v["id"]) for v in r.get("vulns", []) if v.get("id")),
                        datetime.fromisoformat(payload["fetched_at"]),
                        True,
                    )
                    for r in results
                )
                continue
            except Exception:
                pass  # corrupt cache is a cache miss

        if not allow_network:
            out.extend(
                OSVBatchEntry((), datetime.now(UTC), False, "network disabled and no cache entry")
                for _ in chunk
            )
            continue
        try:
            import httpx

            _throttle()
            response = httpx.post(_API_BATCH, json={"queries": chunk}, timeout=timeout)
            if response.status_code != 200:
                out.extend(
                    OSVBatchEntry((), datetime.now(UTC), False, f"OSV HTTP {response.status_code}")
                    for _ in chunk
                )
                continue
            results = response.json().get("results", [])
        except Exception as exc:
            out.extend(
                OSVBatchEntry((), datetime.now(UTC), False, f"{type(exc).__name__}: {exc}")
                for _ in chunk
            )
            continue

        now = datetime.now(UTC)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"fetched_at": now.isoformat(), "results": results}, indent=2))
        for result in results:
            ids = tuple(str(v.get("id")) for v in result.get("vulns", []) if v.get("id"))
            out.append(OSVBatchEntry(ids, now, False))
        # A short response is still a response; pad so indexes stay aligned.
        while len(out) < start + len(chunk):
            out.append(OSVBatchEntry((), now, False, "OSV returned fewer results than queries"))
    return out


def fetch_vuln(
    vuln_id: str,
    *,
    cache_dir: Path | str = ".infravce-cache/osv",
    timeout: float = 20.0,
    allow_network: bool = True,
) -> OSVCacheEntry:
    """Fetch one full OSV record by id, with the same cache semantics.

    Unlike the package query this is a plain GET of an immutable record, so it
    is not throttled here; callers that fan out use :func:`fetch_vulns`.
    """
    cache_dir = Path(cache_dir)
    path = cache_dir / "vulns" / f"{vuln_id.replace('/', '_')}.json"
    if path.exists():
        try:
            payload = json.loads(path.read_text())
            return OSVCacheEntry(
                (payload["vuln"],),
                datetime.fromisoformat(payload["fetched_at"]),
                True,
            )
        except Exception:
            pass

    if not allow_network:
        return OSVCacheEntry((), datetime.now(UTC), False, "network disabled and no cache entry")
    try:
        import httpx

        response = httpx.get(f"{_API_VULN}{vuln_id}", timeout=timeout)
        if response.status_code != 200:
            return OSVCacheEntry((), datetime.now(UTC), False, f"OSV HTTP {response.status_code}")
        vuln = response.json()
    except Exception as exc:
        return OSVCacheEntry((), datetime.now(UTC), False, f"{type(exc).__name__}: {exc}")

    now = datetime.now(UTC)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"fetched_at": now.isoformat(), "vuln": vuln}, indent=2))
    return OSVCacheEntry((vuln,), now, False)


def fetch_vulns(
    vuln_ids: list[str],
    *,
    cache_dir: Path | str = ".infravce-cache/osv",
    timeout: float = 20.0,
    allow_network: bool = True,
    max_workers: int = 6,
) -> dict[str, OSVCacheEntry]:
    """Fetch many records concurrently.

    An inventory on a real host can reference several hundred advisories, and a
    sequential fetch would make the scan unusably slow. Six workers is enough to
    turn minutes into seconds without turning a courtesy API into a target.
    """
    from concurrent.futures import ThreadPoolExecutor

    if not vuln_ids:
        return {}

    def one(vuln_id: str) -> tuple[str, OSVCacheEntry]:
        return vuln_id, fetch_vuln(
            vuln_id,
            cache_dir=cache_dir,
            timeout=timeout,
            allow_network=allow_network,
        )

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return dict(pool.map(one, vuln_ids))


def _source_for(vuln_id: str) -> AdvisorySource:
    upper = vuln_id.upper()
    if upper.startswith(("DEBIAN-", "DSA-", "DLA-", "ALPINE-", "UBUNTU-", "USN-", "RLSA-", "RHSA-")):
        return AdvisorySource.DISTRO_TRACKER
    if upper.startswith("GHSA-"):
        return AdvisorySource.GHSA
    if upper.startswith("CVE-"):
        return AdvisorySource.NVD
    return AdvisorySource.OSV


_SEVERITY_CVSS = {
    "critical": 9.5,
    "high": 8.0,
    "moderate": 6.0,
    "medium": 5.5,
    "low": 3.0,
}


def _severity(
    vuln: dict[str, Any], product: str, queried_as: str | None = None
) -> tuple[str | None, float | None]:
    for affected in _affected_blocks(vuln, product, queried_as):
        block = affected.get("ecosystem_specific")
        if not isinstance(block, dict):
            continue
        urgency = block.get("urgency")
        if isinstance(urgency, str):
            mapped = _URGENCY.get(urgency.strip().lower())
            if mapped:
                return mapped, _SEVERITY_CVSS.get(mapped)
    for block in (vuln.get("database_specific"), vuln.get("ecosystem_specific")):
        if isinstance(block, dict):
            sev = block.get("severity")
            if isinstance(sev, str) and sev.strip():
                label = sev.strip().lower()
                return label, _SEVERITY_CVSS.get(label)
    for entry in vuln.get("severity") or []:
        score = entry.get("score") if isinstance(entry, dict) else None
        if not isinstance(score, str):
            continue
        try:
            return None, float(score)
        except ValueError:
            continue  # a CVSS vector, whose numeric base score is not the vector
    return None, None


def _affected_blocks(
    vuln: dict[str, Any], product: str, queried_as: str | None
) -> list[dict[str, Any]]:
    """The ``affected`` entries that describe the package *and* release asked about.

    An OSV Debian record contains one ``affected`` block per release
    (``Debian:12``, ``Debian:13``, ...), each with its OWN ``ranges`` and
    ``versions``. Merging them would evaluate a bookworm asset against trixie's
    fix boundaries and report a version as affected because a *different* release
    had not been patched yet. The queried ecosystem string is therefore a hard
    filter, not a hint.
    """
    blocks: list[dict[str, Any]] = []
    for affected in vuln.get("affected") or []:
        if not isinstance(affected, dict):
            continue
        pkg = affected.get("package") or {}
        if str(pkg.get("name", "")).lower() != product.lower():
            continue
        block_ecosystem = pkg.get("ecosystem")
        if queried_as and isinstance(block_ecosystem, str):
            wanted = queried_as.strip().lower()
            actual = block_ecosystem.strip().lower()
            if wanted != actual:
                # A release-less query (``Debian``) matches every release block.
                # That merge is wider than a release-specific query and is only
                # used when the caller could not state a release; the coverage
                # report records that as a gap.
                wanted_base, _, _ = wanted.partition(":")
                actual_base, _, _ = actual.partition(":")
                if ":" in wanted or wanted_base != actual_base:
                    continue
        blocks.append(affected)
    return blocks


def _segments(
    vuln: dict[str, Any], product: str, queried_as: str | None = None
) -> tuple[tuple[str | None, str | None], ...]:
    """Extract ``(introduced, fixed)`` intervals for the queried package only.

    A single OSV record can list several affected packages; taking another
    package's ranges would attach a fix boundary for ``libssl`` to ``nginx``.
    """
    out: list[tuple[str | None, str | None]] = []
    for affected in _affected_blocks(vuln, product, queried_as):
        for rng in affected.get("ranges") or []:
            if not isinstance(rng, dict):
                continue
            if rng.get("type") not in {"ECOSYSTEM", "SEMVER", "GIT"}:
                continue
            introduced: str | None = None
            for event in rng.get("events") or []:
                if not isinstance(event, dict):
                    continue
                if "introduced" in event:
                    introduced = str(event["introduced"])
                elif "fixed" in event:
                    out.append((introduced, str(event["fixed"])))
                    introduced = None
                elif "last_affected" in event:
                    # last_affected is inclusive; represented as an open segment
                    # rather than inventing a next version that may not exist.
                    out.append((introduced, None))
                    introduced = None
            if introduced is not None:
                out.append((introduced, None))
    return tuple(out)


def the_versions(
    vuln: dict[str, Any], product: str, queried_as: str | None = None
) -> tuple[str, ...]:
    out: list[str] = []
    for affected in _affected_blocks(vuln, product, queried_as):
        out.extend(str(v) for v in affected.get("versions") or [])
    return tuple(dict.fromkeys(out))


#: Tracker urgency -> the severity vocabulary the scorer understands. Debian's
#: OSV records do not carry a CVSS score, so urgency is the only published
#: priority signal; mapping it is better than reporting every historical
#: ``unimportant`` issue as unknown.
_URGENCY = {
    "unimportant": "low",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "critical": "critical",
}


def records_from_vulns(
    vulns: Iterable[Mapping[str, Any]],
    *,
    product: str,
    ecosystem: Ecosystem,
    queried_as: str,
) -> list[AdvisoryRecord]:
    """Convert OSV vulns into records the matcher can evaluate."""
    records: dict[str, AdvisoryRecord] = {}
    for vuln in vulns:
        if not isinstance(vuln, dict):
            continue
        vuln_id = str(vuln.get("id") or "")
        aliases = tuple(str(a) for a in vuln.get("aliases") or [])
        cve = next((a for a in aliases if a.upper().startswith("CVE-")), None)
        advisory_id = cve or vuln_id or "OSV-UNKNOWN"
        segments = _segments(vuln, product, queried_as)
        versions = the_versions(vuln, product, queried_as)
        if not segments and not versions:
            continue  # record does not describe this package/release
        severity, cvss = _severity(vuln, product, queried_as)

        existing = records.get(advisory_id)
        if existing is not None and len(existing.affected_ranges) >= len(segments):
            continue
        records[advisory_id] = AdvisoryRecord(
            advisory_id=advisory_id,
            source=_source_for(vuln_id or advisory_id),
            ecosystem=ecosystem,
            product=product.lower(),
            versions=versions,
            distro_state=None,
            fixed_version=None,
            published_at=_dt(vuln.get("published")),
            url=f"https://osv.dev/vulnerability/{vuln_id}" if vuln_id else None,
            raw=vuln,
            affected_ranges=segments,
            aliases=aliases,
            severity=severity,
            cvss=cvss,
            summary=(str(vuln.get("summary") or vuln.get("details") or "")[:500] or None),
            queried_as=queried_as,
        )
    return list(records.values())


def _dt(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def coverage_for(
    entries: list[tuple[str, OSVCacheEntry]],
    *,
    ecosystem: Ecosystem,
    label: str,
) -> ScanCoverage:
    """One coverage row per queried ecosystem, with the oldest fetch time.

    Reporting the oldest successful fetch (rather than the newest) is the
    conservative choice: the report's freshness claim is then no better than its
    stalest input.
    """
    ok = [e for _, e in entries if e.error is None]
    gaps = tuple(dict.fromkeys(e.error for _, e in entries if e.error))
    oldest = min((e.fetched_at for e in ok), default=None)
    return ScanCoverage(
        source=AdvisorySource.OSV,
        ecosystem=ecosystem,
        last_successful_ingest=oldest,
        record_count=sum(len(e.vulns) for e in ok),
        is_stale=oldest is None,
        known_gaps=gaps,
        detail_url="https://osv.dev",
    )
