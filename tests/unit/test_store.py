"""Observation store: provenance survives the round trip, guards survive the DB."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from infravce.models import (
    AcquisitionMethod,
    AdvisorySource,
    Applicability,
    ApplicabilityVerdict,
    Asset,
    Ecosystem,
    Justification,
    NormalisedVersion,
    Observation,
    RangeRepresentation,
    ScanCoverage,
)
from infravce.store import ObservationStore


@pytest.fixture
def store() -> ObservationStore:
    store = ObservationStore()
    store.put_asset(
        Asset(
            asset_id="lab:debian12-backport-curl",
            address="127.0.0.1",
            discovered_via=AcquisitionMethod.PACKAGE_DB,
            is_declared=True,
            criticality="medium",
            service_tags=("curl",),
        )
    )
    return store


def _observation(asset_id: str = "lab:debian12-backport-curl", **kw) -> Observation:
    base = {
        "asset_id": asset_id,
        "acquisition_method": AcquisitionMethod.PACKAGE_DB,
        "evidence": "curl 7.88.1-10+deb12u15 amd64",
        "raw_product": "libcurl4",
        "raw_version": "7.88.1-10+deb12u15",
        "resolved_product": "curl",
        "resolved_version": NormalisedVersion(
            ecosystem=Ecosystem.DEBIAN,
            raw="7.88.1-10+deb12u15",
            upstream="7.88.1",
            release="7.88.1-10+deb12u15",
            distro_revision="deb12u15",
            confidence=1.0,
        ),
        "resolution_confidence": 1.0,
    }
    return Observation(**{**base, **kw})


class TestRoundTrip:
    def test_observation_survives_a_round_trip(self, store: ObservationStore) -> None:
        original = _observation()
        store.put_observation(original, ecosystem=Ecosystem.DEBIAN)
        loaded = store.get_observation(original.observation_id)
        assert loaded is not None
        assert loaded.raw_product == original.raw_product
        assert loaded.raw_version == original.raw_version
        assert loaded.resolved_product == "curl"
        assert loaded.resolution_confidence == 1.0
        assert loaded.acquisition_method is AcquisitionMethod.PACKAGE_DB

    def test_the_raw_string_is_preserved_alongside_the_parse(self, store: ObservationStore) -> None:
        """The vendor string is the only link back to what dpkg actually said."""
        observation = _observation()
        store.put_observation(observation, ecosystem=Ecosystem.DEBIAN)
        row = store._conn.execute(
            "SELECT raw_version, upstream, distro_revision FROM observations"
        ).fetchone()
        assert row["raw_version"] == "7.88.1-10+deb12u15"
        assert row["upstream"] == "7.88.1"
        assert row["distro_revision"] == "deb12u15"

    def test_asset_survives_a_round_trip(self, store: ObservationStore) -> None:
        loaded = store.get_asset("lab:debian12-backport-curl")
        assert loaded is not None
        assert loaded.is_declared
        assert loaded.criticality == "medium"
        assert loaded.service_tags == ("curl",)

    def test_a_second_asset_does_not_disturb_the_first(self, store: ObservationStore) -> None:
        store.put_asset(
            Asset(
                asset_id="lab:alpine319-libcrypto",
                discovered_via=AcquisitionMethod.PACKAGE_DB,
                is_declared=True,
            )
        )
        assert store.get_asset("lab:debian12-backport-curl") is not None
        assert store.get_asset("lab:alpine319-libcrypto") is not None

    def test_identity_is_stored_alongside_the_observation(self, store: ObservationStore) -> None:
        observation = _observation()
        store.put_observation(observation, ecosystem=Ecosystem.DEBIAN)
        store.attach_identity(
            observation.observation_id,
            purl=None,
            cpe="cpe:2.3:a:curl:curl:*:*:*:*:*:*:*:*",
            ambiguous=False,
        )
        assert store.observations_with_identity(observation.observation_id) == {
            "purl": None,
            "cpe": "cpe:2.3:a:curl:curl:*:*:*:*:*:*:*:*",
            "ambiguous": False,
        }


class TestUnresolvedVersionGuard:
    def test_an_unresolved_version_is_stored_without_comparable_columns(
        self, store: ObservationStore
    ) -> None:
        """The grype#2606 guard, enforced by the database.

        A SHA-pinned action, an empty version and a sentinel are all stored — the
        evidence is never discarded — but none of them gets a `release` a
        comparison could order.
        """
        observation = _observation(
            raw_product="tj-actions/changed-files",
            raw_version="ed68ef8",
            resolved_product=None,
            resolved_version=None,
            resolution_confidence=0.0,
            evidence="uses: tj-actions/changed-files@ed68ef8",
        )
        store.put_observation(observation, ecosystem=Ecosystem.GITHUB)
        row = store._conn.execute(
            "SELECT raw_version, release, upstream, resolution_confidence FROM observations"
        ).fetchone()
        assert row["raw_version"] == "ed68ef8"
        assert row["release"] is None
        assert row["upstream"] is None
        assert row["resolution_confidence"] == 0.0

    def test_an_unresolved_observation_is_not_comparable(
        self, store: ObservationStore
    ) -> None:
        observation = _observation(
            resolved_product=None,
            resolved_version=None,
            resolution_confidence=0.0,
        )
        store.put_observation(observation, ecosystem=Ecosystem.DEBIAN)
        assert store.comparable_observations() == []
        assert store.unresolved_observations() == [observation.observation_id]

    def test_the_database_refuses_a_parsed_version_without_confidence(
        self, store: ObservationStore
    ) -> None:
        """Belt to the model's braces: a hand-written INSERT cannot smuggle in a
        release with zero confidence and nothing to trace it to."""
        with pytest.raises(sqlite3.IntegrityError):
            store._conn.execute(
                """
                INSERT INTO observations (
                  observation_id, asset_id, observed_at, acquisition_method, evidence,
                  raw_product, raw_version, resolved_product,
                  epoch, upstream, release, distro_revision,
                  pre_release, build_metadata, local_revision,
                  resolution_confidence, parse_notes, ecosystem,
                  identity_purl, identity_cpe, identity_ambiguous
                ) VALUES (
                  'o1','lab:debian12-backport-curl','2026-10-01T00:00:00+00:00',
                  'package_db','evidence','openssl','3.0.22','openssl',
                  NULL,'made-up','3.0.22-1',NULL,NULL,NULL,NULL,
                  0.0,'[]','debian',NULL,NULL,0
                )
                """
            )
            store._conn.commit()

    def test_a_resolution_is_not_silently_upgraded_by_the_store(
        self, store: ObservationStore
    ) -> None:
        """Storing must never make an unusable version usable."""
        observation = _observation(resolution_confidence=0.0, resolved_version=None)
        store.put_observation(observation, ecosystem=Ecosystem.DEBIAN)
        loaded = store.get_observation(observation.observation_id)
        assert loaded is not None
        assert not loaded.is_usable_for_matching


class TestApplicability:
    def _vote(self, observation_id: str, source: AdvisorySource, verdict: ApplicabilityVerdict):
        return Applicability(
            observation_id=observation_id,
            advisory_source=source,
            advisory_id="CVE-2003-1605",
            range_representation=(
                RangeRepresentation.DPKG_STATUS
                if source is AdvisorySource.DISTRO_TRACKER
                else RangeRepresentation.NVD_RANGE
            ),
            verdict=verdict,
            justification=(
                Justification.COMPONENT_NOT_PRESENT
                if verdict is ApplicabilityVerdict.NOT_AFFECTED
                else None
            ),
            evidence="dpkg status: fixed",
        )

    def test_votes_are_ordered_by_precedence(self, store: ObservationStore) -> None:
        observation = _observation()
        store.put_observation(observation, ecosystem=Ecosystem.DEBIAN)
        store.put_applicability(
            self._vote(observation.observation_id, AdvisorySource.NVD, ApplicabilityVerdict.AFFECTED)
        )
        store.put_applicability(
            self._vote(
                observation.observation_id,
                AdvisorySource.DISTRO_TRACKER,
                ApplicabilityVerdict.NOT_AFFECTED,
            )
        )
        votes = store.votes_for(observation.observation_id)
        assert votes[0]["advisory_source"] == AdvisorySource.DISTRO_TRACKER.value
        assert votes[1]["advisory_source"] == AdvisorySource.NVD.value

    def test_dissent_is_preserved_not_averaged(self, store: ObservationStore) -> None:
        """The Dependency-Track↔Trivy divergence has to stay visible."""
        observation = _observation()
        store.put_observation(observation, ecosystem=Ecosystem.DEBIAN)
        store.put_applicability(
            self._vote(observation.observation_id, AdvisorySource.NVD, ApplicabilityVerdict.AFFECTED)
        )
        store.put_applicability(
            self._vote(
                observation.observation_id,
                AdvisorySource.DISTRO_TRACKER,
                ApplicabilityVerdict.NOT_AFFECTED,
            )
        )
        votes = store.votes_for(observation.observation_id)
        assert len(votes) == 2
        assert store.dissent_count() == 1

    def test_agreement_is_not_dissent(self, store: ObservationStore) -> None:
        observation = _observation()
        store.put_observation(observation, ecosystem=Ecosystem.DEBIAN)
        for source in (AdvisorySource.NVD, AdvisorySource.DISTRO_TRACKER):
            store.put_applicability(
                self._vote(observation.observation_id, source, ApplicabilityVerdict.AFFECTED)
            )
        assert store.dissent_count() == 0

    def test_a_vote_cannot_reference_an_absent_observation(
        self, store: ObservationStore
    ) -> None:
        with pytest.raises(sqlite3.IntegrityError):
            store.put_applicability(
                self._vote("does-not-exist", AdvisorySource.NVD, ApplicabilityVerdict.AFFECTED)
            )

    def test_the_same_vote_is_not_counted_twice(self, store: ObservationStore) -> None:
        observation = _observation()
        store.put_observation(observation, ecosystem=Ecosystem.DEBIAN)
        vote = self._vote(observation.observation_id, AdvisorySource.NVD, ApplicabilityVerdict.AFFECTED)
        store.put_applicability(vote)
        store.put_applicability(vote)
        assert store.counts()["applicability"] == 1


class TestCoverage:
    def test_a_known_gap_is_recorded_rather_than_hidden(self, store: ObservationStore) -> None:
        store.put_coverage(
            ScanCoverage(
                source=AdvisorySource.DISTRO_TRACKER,
                ecosystem=Ecosystem.DEBIAN,
                last_successful_ingest=datetime(2026, 10, 1, tzinfo=UTC),
                record_count=4,
                known_gaps=("bookworm: not yet published for DSA-5588-1",),
                detail_url="https://security-tracker.debian.org/tracker/CVE-2024-9143",
            )
        )
        entry = store.coverage()[0]
        assert "DSA-5588-1" in entry["known_gaps"]
        assert entry["record_count"] == 4

    def test_a_stale_source_is_marked_stale(self, store: ObservationStore) -> None:
        store.put_coverage(
            ScanCoverage(
                source=AdvisorySource.DISTRO_TRACKER,
                ecosystem=Ecosystem.APK,
                is_stale=True,
                known_gaps=("alpine 3.16 repository retired",),
            )
        )
        assert store.coverage()[0]["is_stale"] == 1


class TestTransactions:
    def test_a_failure_rolls_the_whole_batch_back(self, store: ObservationStore) -> None:
        """A half-ingested batch would let the coverage table claim a freshness it
        does not have."""
        observation = _observation()
        with pytest.raises(sqlite3.IntegrityError):
            with store.transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO observations (
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
                        "package_db",
                        "evidence",
                        "openssl",
                        "3.0.22",
                        "openssl",
                        None,
                        "made-up",
                        "3.0.22-1",
                        None,
                        None,
                        None,
                        None,
                        0.0,
                        "[]",
                        "debian",
                    ),
                )
        assert store.counts()["observations"] == 0


class TestSchema:
    def test_the_store_starts_empty(self, store: ObservationStore) -> None:
        assert store.counts() == {
            "assets": 1,
            "observations": 0,
            "applicability": 0,
            "scan_coverage": 0,
        }

    def test_reopening_a_file_backed_store_keeps_the_data(self, tmp_path) -> None:
        path = tmp_path / "scan.db"
        first = ObservationStore.open(path)
        first.put_asset(
            Asset(asset_id="a1", discovered_via=AcquisitionMethod.BANNER, is_declared=True)
        )
        first.close()
        assert ObservationStore.open(path).counts()["assets"] == 1

    def test_foreign_keys_are_enforced_on_an_asset_with_observations(
        self, store: ObservationStore
    ) -> None:
        """An observation for an asset nobody discovered is a scan bug, and it must
        be caught at the boundary rather than in a report."""
        with pytest.raises(sqlite3.IntegrityError):
            store.put_observation(
                _observation(asset_id="not-discovered"), ecosystem=Ecosystem.DEBIAN
            )

    def test_the_model_still_forbids_a_confident_unresolved_version(self) -> None:
        """The store is a cache; the model remains the authority."""
        with pytest.raises(ValidationError, match=r"resolution_confidence must be 0\.0"):
            Observation(
                asset_id="a1",
                acquisition_method=AcquisitionMethod.SBOM,
                evidence="uses: org/repo@ed68ef8",
                raw_product="org/repo",
                raw_version="ed68ef8",
                resolution_confidence=0.9,
            )
