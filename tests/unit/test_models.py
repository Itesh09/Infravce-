"""Core data model invariant tests.

These encode the design rules from docs/02-architecture.md as executable
constraints. Each test names the failure it prevents, because an invariant
without a documented reason gets removed by the next person who does not know
why it was there.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from infravce.models import (
    AcquisitionMethod,
    AdvisorySource,
    Applicability,
    ApplicabilityVerdict,
    Asset,
    ConfidenceTier,
    Ecosystem,
    Finding,
    Justification,
    NormalisedVersion,
    Observation,
    RangeRepresentation,
    ScanCoverage,
)


def _obs(**kw) -> Observation:
    base = {
        "asset_id": "web-01",
        "acquisition_method": AcquisitionMethod.BANNER,
        "evidence": "b'nginx/1.18.0'",
        "raw_product": "nginx",
        "raw_version": "1.18.0",
        "resolved_product": "nginx",
        "resolved_version": NormalisedVersion(
            ecosystem=Ecosystem.SEMVER, raw="1.18.0", upstream="1.18.0", confidence=0.95
        ),
        "resolution_confidence": 0.95,
    }
    return Observation(**{**base, **kw})


class TestObservationInvariant:
    def test_unresolved_version_forbids_nonzero_confidence(self) -> None:
        """The central guard.

        grype#2606: a GitHub Action pinned by commit SHA was recorded with the
        SHA as its version, and every range comparison against it produced a
        false positive. Confidence must be 0.0 whenever there is no version to
        compare.
        """
        with pytest.raises(ValidationError, match=r"resolution_confidence must be 0\.0"):
            Observation(
                asset_id="ci-01",
                acquisition_method=AcquisitionMethod.SBOM,
                evidence="uses: tj-actions/changed-files@ed68ef8",
                raw_product="tj-actions/changed-files",
                raw_version="ed68ef8",
                resolved_product="tj-actions/changed-files",
                resolved_version=None,
                resolution_confidence=0.9,
            )

    def test_observation_is_unusable_for_matching_when_unresolved(self) -> None:
        o = _obs(resolved_version=None, resolution_confidence=0.0)
        assert o.is_usable_for_matching is False

    def test_observation_is_usable_when_fully_resolved(self) -> None:
        assert _obs().is_usable_for_matching is True

    def test_non_resolved_version_string_forces_confidence_to_zero(self) -> None:
        """A NormalisedVersion whose upstream is None must not smuggle confidence."""
        o = _obs(
            resolved_version=NormalisedVersion(
                ecosystem=Ecosystem.UNKNOWN, raw="latest", upstream=None, confidence=0.9
            ),
            resolution_confidence=0.9,
        )
        assert o.resolution_confidence == 0.0
        assert o.is_usable_for_matching is False

    def test_raw_strings_are_preserved_alongside_resolved(self) -> None:
        """Provenance is not optional: the raw string is the evidence."""
        o = _obs(raw_version="1:1.12.20-8.el9", raw_product="OpenSSL")
        assert o.raw_version == "1:1.12.20-8.el9"
        assert o.raw_product == "OpenSSL"


class TestAcquisitionMethodTrust:
    def test_probe_methods_are_active(self) -> None:
        for m in (
            AcquisitionMethod.TCP_PROBE,
            AcquisitionMethod.TLS_CERT,
            AcquisitionMethod.HTTP_HEADER,
            AcquisitionMethod.BANNER,
        ):
            assert m.is_active and not m.is_passive

    def test_declared_and_passive_methods_are_not_active(self) -> None:
        """Only these may be used against a host without packet-level authorisation."""
        for m in (
            AcquisitionMethod.SBOM,
            AcquisitionMethod.LOCKFILE,
            AcquisitionMethod.PACKAGE_DB,
            AcquisitionMethod.CT_LOG,
            AcquisitionMethod.CLOUD_API,
            AcquisitionMethod.DECLARED_CMDB,
        ):
            assert m.is_passive and not m.is_active

    def test_every_method_is_exactly_one_of_passive_or_active(self) -> None:
        for m in AcquisitionMethod:
            assert m.is_active ^ m.is_passive


class TestAdvisoryPrecedence:
    def test_distribution_truth_outranks_nvd(self) -> None:
        """The backport principle.

        Debian marks curl CVE-2025-9086 <not-affected> because the vulnerable
        code was never introduced, so an upstream NVD range is not merely less
        precise here, it is wrong.
        """
        assert AdvisorySource.DISTRO_TRACKER.precedence_rank < AdvisorySource.NVD.precedence_rank

    def test_vendor_outranks_upstream_aggregators(self) -> None:
        assert AdvisorySource.VENDOR_ADVISORY.precedence_rank < AdvisorySource.OSV.precedence_rank
        assert AdvisorySource.OSV.precedence_rank < AdvisorySource.NVD.precedence_rank

    def test_precedence_is_unique_per_source(self) -> None:
        ranks = [s.precedence_rank for s in AdvisorySource]
        assert len(ranks) == len(set(ranks))


class TestApplicabilityValidation:
    def test_not_affected_requires_a_justification(self) -> None:
        """CISA Minimum Requirements for VEX: justification or impact_statement."""
        with pytest.raises(ValidationError, match="not_affected requires a justification"):
            Applicability(
                observation_id="o1",
                advisory_source=AdvisorySource.DISTRO_TRACKER,
                advisory_id="DSA-5588-1",
                verdict=ApplicabilityVerdict.NOT_AFFECTED,
                evidence="dpkg status: fixed",
            )

    def test_not_affected_accepts_an_impact_statement_instead(self) -> None:
        a = Applicability(
            observation_id="o1",
            advisory_source=AdvisorySource.DISTRO_TRACKER,
            advisory_id="DSA-5588-1",
            verdict=ApplicabilityVerdict.NOT_AFFECTED,
            evidence="dpkg status: not-affected",
            impact_statement="feature is compiled out of this build",
        )
        assert a.verdict is ApplicabilityVerdict.NOT_AFFECTED

    def test_not_affected_with_justification_is_valid(self) -> None:
        a = Applicability(
            observation_id="o1",
            advisory_source=AdvisorySource.DISTRO_TRACKER,
            advisory_id="DSA-5588-1",
            range_representation=RangeRepresentation.DPKG_STATUS,
            verdict=ApplicabilityVerdict.NOT_AFFECTED,
            justification=Justification.COMPONENT_NOT_PRESENT,
            evidence="dpkg status: vulnerable code absent from the package",
        )
        assert a.justification is Justification.COMPONENT_NOT_PRESENT

    def test_justification_is_rejected_on_affected(self) -> None:
        with pytest.raises(ValidationError, match="justification applies only to not_affected"):
            Applicability(
                observation_id="o1",
                advisory_source=AdvisorySource.NVD,
                advisory_id="CVE-2021-44228",
                verdict=ApplicabilityVerdict.AFFECTED,
                justification=Justification.COMPONENT_NOT_PRESENT,
                evidence="version in range",
            )

    def test_under_investigation_needs_no_justification(self) -> None:
        """Debian's <undetermined> must be representable without a claim.

        It means "someone needs to come back to this", which is not the same as
        safe, so it must not require justification to express.
        """
        a = Applicability(
            observation_id="o1",
            advisory_source=AdvisorySource.DISTRO_TRACKER,
            advisory_id="DSA-0000-1",
            verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
            evidence="dpkg status: undetermined",
        )
        assert a.verdict is ApplicabilityVerdict.UNDER_INVESTIGATION


class TestFindingAggregation:
    def _finding(self, votes: list[Applicability]) -> Finding:
        return Finding(
            asset_id="web-01",
            cve_id="CVE-2024-9143",
            confidence_tier=ConfidenceTier.INFERRED,
            supporting_observations=(_obs(),),
            applicability_votes=tuple(votes),
        )

    def test_lowest_precedence_source_wins(self) -> None:
        f = self._finding(
            [
                Applicability(
                    observation_id="o1",
                    advisory_source=AdvisorySource.NVD,
                    advisory_id="CVE-2024-9143",
                    verdict=ApplicabilityVerdict.AFFECTED,
                    evidence="versionStartIncluding match",
                ),
                Applicability(
                    observation_id="o1",
                    advisory_source=AdvisorySource.DISTRO_TRACKER,
                    advisory_id="DSA-5922-1",
                    range_representation=RangeRepresentation.DPKG_STATUS,
                    verdict=ApplicabilityVerdict.NOT_AFFECTED,
                    justification=Justification.COMPONENT_NOT_PRESENT,
                    evidence="dpkg status: not-affected",
                ),
            ]
        )
        assert f.winning_vote is not None
        assert f.winning_vote.advisory_source is AdvisorySource.DISTRO_TRACKER

    def test_dissent_is_surfaced_not_discarded(self) -> None:
        """A source disagreement rate is itself a reported metric."""
        f = self._finding(
            [
                Applicability(
                    observation_id="o1",
                    advisory_source=AdvisorySource.NVD,
                    advisory_id="CVE-2024-9143",
                    verdict=ApplicabilityVerdict.AFFECTED,
                    evidence="range match",
                ),
                Applicability(
                    observation_id="o1",
                    advisory_source=AdvisorySource.DISTRO_TRACKER,
                    advisory_id="DSA-5922-1",
                    verdict=ApplicabilityVerdict.NOT_AFFECTED,
                    justification=Justification.VULNERABLE_CODE_NOT_PRESENT,
                    evidence="dpkg status",
                ),
            ]
        )
        assert f.has_dissent is True
        assert len(f.applicability_votes) == 2

    def test_unanimous_votes_are_not_dissent(self) -> None:
        v = Applicability(
            observation_id="o1",
            advisory_source=AdvisorySource.OSV,
            advisory_id="GHSA-xxxx",
            verdict=ApplicabilityVerdict.AFFECTED,
            evidence="events",
        )
        assert self._finding([v, v]).has_dissent is False

    def test_finding_without_votes_has_no_winner(self) -> None:
        assert self._finding([]).winning_vote is None

    def test_suppression_is_visible_on_the_finding(self) -> None:
        f = self._finding([])
        assert f.is_suppressed is False
        f.suppression_state = "known_bad_mapping"
        assert f.is_suppressed is True


class TestAssetAttribution:
    def test_attribution_is_never_asserted_by_default(self) -> None:
        """Angelova et al. (WEIS 2026): WHOIS attribution is 58% recall, 62% FP.

        An asset discovered outside-in starts unattributed and unattributed
        assets route to their own queue rather than into or out of scope silently.
        """
        a = Asset(asset_id="10.1.2.3:443", discovered_via=AcquisitionMethod.CT_LOG)
        assert a.is_attributed is False
        assert a.attribution_confidence == 0.0

    def test_declared_assets_are_flagged_as_declared(self) -> None:
        a = Asset(
            asset_id="web-01",
            discovered_via=AcquisitionMethod.DECLARED_CMDB,
            is_declared=True,
            is_authorised_for_active_scan=True,
        )
        assert a.is_declared and a.is_authorised_for_active_scan

    def test_criticality_defaults_to_unknown_not_low(self) -> None:
        """Absent input must not read as low importance."""
        a = Asset(asset_id="x", discovered_via=AcquisitionMethod.SBOM)
        assert a.criticality == "unknown"

    def test_exposure_is_tri_state(self) -> None:
        """Unmeasured exposure is not the same as not exposed."""
        a = Asset(asset_id="x", discovered_via=AcquisitionMethod.SBOM)
        assert a.internet_exposed is None


class TestScanCoverage:
    def test_never_ingested_is_reported_loudly(self) -> None:
        """A scanner that would match correctly still reports nothing if the
        advisory is absent, and nothing in its output revealed it (OSV's ten-day
        GHSA ingestion outage; Greenbone's documented coverage lag)."""
        c = ScanCoverage(source=AdvisorySource.OSV, ecosystem=Ecosystem.NPM)
        assert c.last_successful_ingest is None
        assert "NEVER INGESTED" in c.summary()

    def test_stale_feed_is_flagged_in_the_summary(self) -> None:
        c = ScanCoverage(
            source=AdvisorySource.OSV,
            ecosystem=Ecosystem.PYPI,
            last_successful_ingest=datetime.now(UTC),
            record_count=100,
            is_stale=True,
        )
        assert "STALE" in c.summary()

    def test_fresh_feed_summarises_without_a_stale_flag(self) -> None:
        c = ScanCoverage(
            source=AdvisorySource.DISTRO_TRACKER,
            last_successful_ingest=datetime.now(UTC),
            record_count=5,
        )
        assert "STALE" not in c.summary()


class TestCompareKeySemantics:
    """compare_key is for equality and dedup, not ordering.

    These tests pin that distinction so nobody "fixes" it into a sort key and
    silently reverses which package build looks newer.
    """

    def _v(self, **kw) -> NormalisedVersion:
        kw.setdefault("ecosystem", Ecosystem.RPM)
        kw.setdefault("raw", "x")
        kw.setdefault("upstream", "1.0")
        kw.setdefault("confidence", 0.95)
        return NormalisedVersion(**kw)

    def test_unresolved_version_refuses_to_build_a_key(self) -> None:
        with pytest.raises(ValueError, match="unresolved"):
            _ = self._v(
                ecosystem=Ecosystem.UNKNOWN, raw="latest", upstream=None, confidence=0.0
            ).compare_key

    def test_same_version_normalises_to_the_same_key(self) -> None:
        a = self._v(upstream="1.2.3", release="8.el9", epoch=1, raw="1:1.2.3-8.el9")
        b = self._v(upstream="1.2.3", release="8.el9", epoch=1, raw="1:1.2.3-8.el9")
        assert a.compare_key == b.compare_key

    def test_distro_release_is_part_of_the_key(self) -> None:
        """Two builds of the same upstream version are different versions.

        Collapsing them would make a fixed and an unfixed package compare equal,
        which is the false-negative direction and is worse than a false positive.
        """
        a = self._v(upstream="1.2.3", release="8.el9", raw="1.2.3-8.el9")
        b = self._v(upstream="1.2.3", release="9.el9", raw="1.2.3-9.el9")
        assert a.compare_key != b.compare_key

    def test_epoch_is_part_of_the_key(self) -> None:
        a = self._v(upstream="1.2.3", epoch=1, raw="1:1.2.3")
        b = self._v(upstream="1.2.3", epoch=2, raw="2:1.2.3")
        assert a.compare_key != b.compare_key
