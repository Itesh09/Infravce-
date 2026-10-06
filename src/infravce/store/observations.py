"""SQLite observation store, per ``docs/02-architecture.md`` §3.1.

Design commitments, each of which exists because of a measured failure mode:

**Provenance on every row.** An observation without its acquisition method and
raw evidence is not auditable, and the Dependency-Track↔Trivy divergence could not
have been diagnosed without both. ``raw_product``/``raw_version`` are stored
verbatim alongside the resolved values precisely so a wrong resolution is
locatable to a specific row rather than inferred from a symptom.

**Raw and resolved versions are stored separately, never collapsed.** The
grype#2606 SHA-pinned action is representable only because the SHA survives in
``raw_version`` while the parsed version stays unresolved. Overwriting one with the
other would lose the evidence that the input was unusable.

**The store never decides.** It records what was seen and what was concluded,
separately. Nothing here infers applicability; that is the engine's job, and a
store that answered applicability questions could not be reused for the ablation.

**The database is a cache, not the artefact of record.** The frozen ground truth is
JSON and is diffable in git. This store exists so a scan's intermediate state is
queryable, and it is disposable.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Final

from infravce.models import (
    AcquisitionMethod,
    AdvisorySource,
    Applicability,
    Asset,
    Ecosystem,
    NormalisedVersion,
    Observation,
    ScanCoverage,
)

__all__ = ["SCHEMA_VERSION", "ObservationStore"]

SCHEMA_VERSION: Final = 1

_SCHEMA: Final = """
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assets (
    asset_id                 TEXT PRIMARY KEY,
    address                  TEXT,
    hostname                  TEXT,
    discovered_via            TEXT NOT NULL,
    discovered_at            TEXT NOT NULL,
    is_declared              INTEGER NOT NULL,
    is_authorised_for_active_scan INTEGER NOT NULL,
    attribution_hypothesis   TEXT,
    attribution_confidence   REAL NOT NULL,
    criticality              TEXT NOT NULL,
    internet_exposed         INTEGER,
    service_tags             TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS observations (
    observation_id        TEXT PRIMARY KEY,
    asset_id              TEXT NOT NULL REFERENCES assets(asset_id),
    observed_at           TEXT NOT NULL,
    acquisition_method    TEXT NOT NULL,
    evidence              TEXT NOT NULL,
    raw_product           TEXT NOT NULL,
    raw_version           TEXT NOT NULL,
    resolved_product      TEXT,
    -- The parsed version, flattened to columns rather than serialised, so that
    -- "find every observation we can actually compare" is a SQL predicate instead
    -- of a Python filter over JSON.
    epoch                 INTEGER,
    upstream              TEXT,
    release               TEXT,
    distro_revision       TEXT,
    pre_release           TEXT,
    build_metadata        TEXT,
    local_revision        TEXT,
    resolution_confidence REAL NOT NULL,
    parse_notes           TEXT NOT NULL,
    ecosystem             TEXT NOT NULL,
    identity_purl         TEXT,
    identity_cpe          TEXT,
    identity_ambiguous    INTEGER NOT NULL,
    -- The database refuses the row that would cause the false positive: a version
    -- field filled in while the parse never resolved. The model enforces the same
    -- rule; the constraint exists so a hand-written INSERT, or a future code path
    -- that forgets the check, cannot bypass it.
    CHECK (resolution_confidence > 0.0 OR release IS NULL)
);

CREATE INDEX IF NOT EXISTS idx_observations_asset ON observations(asset_id);
CREATE INDEX IF NOT EXISTS idx_observations_product ON observations(resolved_product);
CREATE INDEX IF NOT EXISTS idx_observations_comparable
    ON observations(resolution_confidence) WHERE resolution_confidence > 0.0;

CREATE TABLE IF NOT EXISTS applicability (
    observation_id        TEXT NOT NULL REFERENCES observations(observation_id),
    advisory_source       TEXT NOT NULL,
    advisory_id           TEXT NOT NULL,
    range_representation  TEXT NOT NULL,
    verdict               TEXT NOT NULL,
    justification         TEXT,
    impact_statement      TEXT,
    evidence              TEXT NOT NULL,
    advisory_published_at TEXT,
    evaluated_at          TEXT NOT NULL,
    PRIMARY KEY (observation_id, advisory_source, advisory_id)
);

CREATE INDEX IF NOT EXISTS idx_applicability_verdict ON applicability(verdict);

CREATE TABLE IF NOT EXISTS scan_coverage (
    source                 TEXT NOT NULL,
    ecosystem              TEXT NOT NULL,
    last_successful_ingest TEXT,
    record_count           INTEGER NOT NULL,
    is_stale               INTEGER NOT NULL,
    known_gaps             TEXT NOT NULL,
    detail_url             TEXT,
    PRIMARY KEY (source, ecosystem)
);
"""


class ObservationStore:
    """A thin, explicit wrapper over the SQLite schema.

    Deliberately not an ORM. The queries here are few, and an ORM would hide
    exactly the thing this project needs visible: which column ended up holding
    which fact.
    """

    def __init__(self, path: Path | str = ":memory:") -> None:
        self._path = str(path)
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(_SCHEMA)
        self._conn.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', ?)",
            (str(SCHEMA_VERSION),),
        )
        self._conn.commit()

    @classmethod
    def open(cls, path: Path) -> ObservationStore:
        path.parent.mkdir(parents=True, exist_ok=True)
        return cls(path)

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """Commit on success, roll back on any error.

        A partially ingested advisory batch is worse than a failed one: the
        coverage table would then claim a freshness it does not have.
        """
        try:
            yield self._conn
        except Exception:
            self._conn.rollback()
            raise
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    # ---------------------------------------------------------------- assets #

    def put_asset(self, asset: Asset) -> None:
        self._conn.execute(
            """
            INSERT OR REPLACE INTO assets (
              asset_id, address, hostname, discovered_via, discovered_at,
              is_declared, is_authorised_for_active_scan,
              attribution_hypothesis, attribution_confidence,
              criticality, internet_exposed, service_tags
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                asset.asset_id,
                asset.address,
                asset.hostname,
                asset.discovered_via.value,
                asset.discovered_at.isoformat(),
                int(asset.is_declared),
                int(asset.is_authorised_for_active_scan),
                asset.attribution_hypothesis,
                asset.attribution_confidence,
                asset.criticality,
                None
                if asset.internet_exposed is None
                else int(asset.internet_exposed),
                json.dumps(asset.service_tags),
            ),
        )
        self._conn.commit()

    def get_asset(self, asset_id: str) -> Asset | None:
        row = self._conn.execute(
            "SELECT * FROM assets WHERE asset_id = ?", (asset_id,)
        ).fetchone()
        return _row_to_asset(row) if row else None

    # ---------------------------------------------------------- observations #

    def put_observation(
        self, observation: Observation, *, ecosystem: Ecosystem | None = None
    ) -> None:
        """Store an observation and, when given, the identity resolved for it.

        An observation whose version did not resolve is stored with the version
        columns NULL and ``resolution_confidence`` 0.0. Writing the raw string
        into ``release`` as a convenience would defeat the entire guard: the
        comparison would run, and grype#2606 would happen here instead.
        """
        parsed = observation.resolved_version
        resolved = parsed if (parsed and parsed.is_resolved) else None
        self._conn.execute(
            """
            INSERT OR REPLACE INTO observations (
              observation_id, asset_id, observed_at, acquisition_method, evidence,
              raw_product, raw_version, resolved_product,
              epoch, upstream, release, distro_revision,
              pre_release, build_metadata, local_revision,
              resolution_confidence, parse_notes, ecosystem,
              identity_purl, identity_cpe, identity_ambiguous
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL,NULL,0)
            """,
            (
                observation.observation_id,
                observation.asset_id,
                observation.observed_at.isoformat(),
                observation.acquisition_method.value,
                observation.evidence,
                observation.raw_product,
                observation.raw_version,
                observation.resolved_product,
                None if resolved is None else resolved.epoch,
                None if resolved is None else resolved.upstream,
                None if resolved is None else resolved.release,
                None if resolved is None else resolved.distro_revision,
                None if resolved is None else resolved.pre_release,
                None if resolved is None else resolved.build_metadata,
                None if resolved is None else resolved.local_revision,
                observation.resolution_confidence,
                json.dumps(list(observation.parse_notes)),
                (ecosystem or Ecosystem.UNKNOWN).value,
            ),
        )
        self._conn.commit()

    def attach_identity(
        self, observation_id: str, *, purl: str | None, cpe: str | None, ambiguous: bool
    ) -> None:
        self._conn.execute(
            """
            UPDATE observations
            SET identity_purl = ?, identity_cpe = ?, identity_ambiguous = ?
            WHERE observation_id = ?
            """,
            (purl, cpe, int(ambiguous), observation_id),
        )
        self._conn.commit()

    def get_observation(self, observation_id: str) -> Observation | None:
        row = self._conn.execute(
            "SELECT * FROM observations WHERE observation_id = ?", (observation_id,)
        ).fetchone()
        return _row_to_observation(row) if row else None

    def observations_for(self, asset_id: str) -> list[Observation]:
        rows = self._conn.execute(
            "SELECT * FROM observations WHERE asset_id = ? ORDER BY observed_at",
            (asset_id,),
        ).fetchall()
        return [_row_to_observation(r) for r in rows]

    def observations_with_identity(self, observation_id: str) -> dict[str, Any]:
        row = self._conn.execute(
            "SELECT identity_purl, identity_cpe, identity_ambiguous "
            "FROM observations WHERE observation_id = ?",
            (observation_id,),
        ).fetchone()
        if row is None:
            return {"purl": None, "cpe": None, "ambiguous": False}
        return {
            "purl": row["identity_purl"],
            "cpe": row["identity_cpe"],
            "ambiguous": bool(row["identity_ambiguous"]),
        }

    def unresolved_observations(self) -> list[str]:
        """Observation ids whose version could not be ordered.

        The operational view of the docs/02 §4.2 guard: the list of things the
        system refused to judge. A non-empty result is a finding about coverage
        rather than about safety.
        """
        rows = self._conn.execute(
            """
            SELECT observation_id FROM observations
            WHERE resolution_confidence = 0.0 AND raw_version IS NOT NULL
            ORDER BY observation_id
            """
        ).fetchall()
        return [r["observation_id"] for r in rows]

    def comparable_observations(self) -> list[str]:
        """Observations with a version that may legally be compared."""
        rows = self._conn.execute(
            """
            SELECT observation_id FROM observations
            WHERE resolution_confidence > 0.0 AND resolved_product IS NOT NULL
            ORDER BY observation_id
            """
        ).fetchall()
        return [r["observation_id"] for r in rows]

    # --------------------------------------------------------- applicability #

    def put_applicability(self, record: Applicability) -> None:
        """Store one source's verdict on one observation."""
        self._conn.execute(
            "INSERT OR REPLACE INTO applicability VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                record.observation_id,
                record.advisory_source.value,
                record.advisory_id,
                record.range_representation.value,
                record.verdict.value,
                None if record.justification is None else record.justification.value,
                record.impact_statement,
                record.evidence,
                None
                if record.advisory_published_at is None
                else record.advisory_published_at.isoformat(),
                record.evaluated_at.isoformat(),
            ),
        )
        self._conn.commit()

    def votes_for(self, observation_id: str) -> list[dict[str, Any]]:
        """Every source's verdict on one observation, including dissent.

        Ordered by precedence rank so the deciding source is first, which is what
        keeps the dissent visible instead of averaged away at write time.
        """
        order = {s.value: s.precedence_rank for s in AdvisorySource}
        rows = self._conn.execute(
            "SELECT * FROM applicability WHERE observation_id = ?", (observation_id,)
        ).fetchall()
        records = [dict(r) for r in rows]
        records.sort(key=lambda r: order[r["advisory_source"]])
        return records

    def dissent_count(self) -> int:
        """Observations where sources disagree.

        Non-zero is not automatically a defect — it is the signal that a human
        should look, which is why it stays queryable.
        """
        row = self._conn.execute(
            """
            SELECT COUNT(*) AS n FROM (
                SELECT observation_id FROM applicability
                GROUP BY observation_id
                HAVING COUNT(DISTINCT verdict) > 1
            )
            """
        ).fetchone()
        return int(row["n"]) if row else 0

    # -------------------------------------------------------------- coverage #

    def put_coverage(self, coverage: ScanCoverage) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO scan_coverage VALUES (?,?,?,?,?,?,?)",
            (
                coverage.source.value,
                coverage.ecosystem.value,
                None
                if coverage.last_successful_ingest is None
                else coverage.last_successful_ingest.isoformat(),
                coverage.record_count,
                int(coverage.is_stale),
                json.dumps(list(coverage.known_gaps)),
                coverage.detail_url,
            ),
        )
        self._conn.commit()

    def coverage(self) -> list[dict[str, Any]]:
        return [dict(r) for r in self._conn.execute("SELECT * FROM scan_coverage")]

    # -------------------------------------------------------------- queries #

    def counts(self) -> dict[str, int]:
        # Written out per table rather than looped over an f-string: table names
        # can never be caller-supplied this way, so there is nothing to inject and
        # nothing for a scanner to reason about.
        return {
            "assets": self._one("SELECT COUNT(*) AS n FROM assets"),
            "observations": self._one("SELECT COUNT(*) AS n FROM observations"),
            "applicability": self._one("SELECT COUNT(*) AS n FROM applicability"),
            "scan_coverage": self._one("SELECT COUNT(*) AS n FROM scan_coverage"),
        }

    def _one(self, sql: str) -> int:
        row = self._conn.execute(sql).fetchone()
        return int(row["n"]) if row else 0


def _row_to_asset(row: sqlite3.Row) -> Asset:
    return Asset(
        asset_id=row["asset_id"],
        address=row["address"],
        hostname=row["hostname"],
        discovered_via=AcquisitionMethod(row["discovered_via"]),
        discovered_at=datetime.fromisoformat(row["discovered_at"]),
        is_declared=bool(row["is_declared"]),
        is_authorised_for_active_scan=bool(row["is_authorised_for_active_scan"]),
        attribution_hypothesis=row["attribution_hypothesis"],
        attribution_confidence=row["attribution_confidence"],
        criticality=row["criticality"],
        internet_exposed=None
        if row["internet_exposed"] is None
        else bool(row["internet_exposed"]),
        service_tags=tuple(json.loads(row["service_tags"])),
    )


def _row_to_observation(row: sqlite3.Row) -> Observation:
    confidence = float(row["resolution_confidence"])
    parsed: NormalisedVersion | None = None
    if confidence > 0.0 and row["upstream"] is not None:
        parsed = NormalisedVersion(
            ecosystem=Ecosystem(row["ecosystem"]),
            raw=row["raw_version"],
            epoch=row["epoch"],
            upstream=row["upstream"],
            release=row["release"],
            distro_revision=row["distro_revision"],
            pre_release=row["pre_release"],
            build_metadata=row["build_metadata"],
            local_revision=row["local_revision"],
            confidence=confidence,
            notes=tuple(json.loads(row["parse_notes"])),
        )
    elif row["upstream"] is not None:
        # Confidence 0 with a parse present means the parse failed after all: keep
        # the text so the round trip stays honest about what was attempted.
        parsed = NormalisedVersion(
            ecosystem=Ecosystem(row["ecosystem"]),
            raw=row["raw_version"],
            upstream=row["upstream"],
            confidence=0.0,
            notes=tuple(json.loads(row["parse_notes"])),
        )
    return Observation(
        observation_id=row["observation_id"],
        asset_id=row["asset_id"],
        observed_at=datetime.fromisoformat(row["observed_at"]),
        acquisition_method=AcquisitionMethod(row["acquisition_method"]),
        evidence=row["evidence"],
        raw_product=row["raw_product"],
        raw_version=row["raw_version"],
        resolved_product=row["resolved_product"],
        resolved_version=parsed,
        resolution_confidence=confidence,
        parse_notes=tuple(json.loads(row["parse_notes"])),
    )


def utc_now() -> datetime:
    return datetime.now(UTC)
