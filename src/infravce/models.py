"""Core data model.

The shape of these types is the project's main architectural claim: a fact and
its provenance are inseparable, and uncertainty is a value rather than an error.

Design rules enforced here (see docs/02-architecture.md):

* Every :class:`Observation` records ``acquisition_method`` and the raw
  unnormalised strings alongside the resolved ones. A wrong answer must be
  localisable to the layer that produced it.
* ``resolved_version`` is ``None`` when parsing fails, and
  ``resolution_confidence`` is then ``0.0``. Nothing downstream may attempt a
  range comparison against an unresolved version.
* :class:`Applicability` keeps the advisory source and the *range
  representation* it used, because "affected according to an NVD range" and
  "affected according to a Debian package status" are different claims.
* :class:`Finding` carries every supporting observation and every
  applicability vote, including dissent, so a confidence tier is auditable
  rather than asserted.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

# --------------------------------------------------------------------------- #
# Enumerations
# --------------------------------------------------------------------------- #


class AcquisitionMethod(StrEnum):
    """How an observation was obtained. Drives trust: passive < active."""

    CT_LOG = "ct_log"
    DNS = "dns"
    WHOIS = "whois"
    CLOUD_API = "cloud_api"
    DECLARED_CMDB = "declared_cmdb"
    DECLARED_IAC = "declared_iac"
    SBOM = "sbom"
    MANIFEST = "manifest"
    LOCKFILE = "lockfile"
    PACKAGE_DB = "package_db"
    AGENT_REPORT = "agent_report"
    TCP_PROBE = "tcp_probe"
    TLS_CERT = "tls_cert"
    HTTP_HEADER = "http_header"
    BANNER = "banner"

    @property
    def is_active(self) -> bool:
        """Active methods send packets to the target and need authorisation."""
        return self in _ACTIVE_METHODS

    @property
    def is_passive(self) -> bool:
        return self in _PASSIVE_METHODS


_ACTIVE_METHODS = frozenset(
    {
        AcquisitionMethod.TCP_PROBE,
        AcquisitionMethod.TLS_CERT,
        AcquisitionMethod.HTTP_HEADER,
        AcquisitionMethod.BANNER,
    }
)

_PASSIVE_METHODS = frozenset(set(AcquisitionMethod) - _ACTIVE_METHODS)


class Ecosystem(StrEnum):
    """Ecosystem determines which version comparator is correct.

    A generic semver comparison is wrong for most of these, which is the point:
    see docs/02-architecture.md section 4.2.
    """

    UNKNOWN = "unknown"
    DEBIAN = "debian"
    UBUNTU = "ubuntu"
    RPM = "rpm"
    APK = "apk"
    SEMVER = "semver"
    PYPI = "pypi"
    GOLANG = "golang"
    MAVEN = "maven"
    CONAN = "conan"
    NPM = "npm"
    NUGET = "nuget"
    GO_DEPS = "go_deps"
    GITHUB = "github"


class AdvisorySource(StrEnum):
    """Precedence matters. See docs/02-architecture.md principle P3."""

    DISTRO_TRACKER = "distro_tracker"
    VENDOR_ADVISORY = "vendor_advisory"
    OSV = "osv"
    GHSA = "ghsa"
    NVD = "nvd"
    UNKNOWN = "unknown"

    @property
    def precedence_rank(self) -> int:
        """Lower wins. Distribution and vendor truth outrank upstream NVD.

        Backported distributions make upstream version ranges categorically
        wrong, not merely imprecise: Debian marks curl CVE-2025-9086
        <not-affected> because the vulnerable code was never introduced.
        """
        return _PRECEDENCE[self]


_PRECEDENCE: dict[AdvisorySource, int] = {
    AdvisorySource.DISTRO_TRACKER: 0,
    AdvisorySource.VENDOR_ADVISORY: 1,
    AdvisorySource.OSV: 2,
    AdvisorySource.GHSA: 3,
    AdvisorySource.NVD: 4,
    AdvisorySource.UNKNOWN: 5,
}


class RangeRepresentation(StrEnum):
    """How an advisory expresses affectedness.

    A distribution tracker answers with a *status*; NVD answers with a
    *range* that always has version ANY. Collapsing these loses the distinction
    that makes distro-first matching work.
    """

    DPKG_STATUS = "dpkg_status"
    APK_STATUS = "apk_status"
    RPM_EVR = "rpm_evr"
    OSV_EVENTS = "osv_events"
    GITHUB = "github"
    GITHUB_ACTIONS = "github_actions"
    GITHUB_LKAVR = "github_lkavr"
    NVD_RANGE = "nvd_range"
    VENDOR_RANGE = "vendor_range"
    UNKNOWN = "unknown"


class ApplicabilityVerdict(StrEnum):
    """CISA's four statuses. See CISA Minimum Requirements for VEX."""

    AFFECTED = "affected"
    NOT_AFFECTED = "not_affected"
    FIXED = "fixed"
    UNDER_INVESTIGATION = "under_investigation"


class Justification(StrEnum):
    """CISA's five ``not_affected`` justifications.

    The system never asserts these without evidence. It may *suggest* a
    justification for human review; it may not emit one as a finding.
    """

    COMPONENT_NOT_PRESENT = "component_not_present"
    VULNERABLE_CODE_NOT_PRESENT = "vulnerable_code_not_present"
    VULNERABLE_CODE_NOT_IN_EXECUTE_PATH = "vulnerable_code_not_in_execute_path"
    VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY = (
        "vulnerable_code_cannot_be_controlled_by_adversary"
    )
    INLINE_MITIGATIONS_ALREADY_EXIST = "inline_mitigations_already_exist"


class ConfidenceTier(StrEnum):
    """Graded output. Precedent: Nmap VULNERABLE vs LIKELY_VULN."""

    VERIFIED = "verified"
    STRONGLY_INFERRED = "strongly_inferred"
    INFERRED = "inferred"
    WEAK = "weak"
    UNRESOLVED = "unresolved"


class NormalisedVersion(BaseModel):
    """Ecosystem-aware version, decomposed for correct comparison.

    ``epoch`` and ``distro_revision`` are separate fields because folding them
    into a single string is precisely what produced 50 false positives when
    Dependency-Track sent ``1:1.12.20-8.el9`` where Trivy CLI sent
    ``1.12.20`` plus release ``8.el9`` (dependency-track#3774).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    ecosystem: Ecosystem
    raw: str
    epoch: int | None = None
    upstream: str | None = None
    release: str | None = None
    distro_revision: str | None = None
    pre_release: str | None = None
    build_metadata: str | None = None
    local_revision: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    notes: tuple[str, ...] = ()

    @property
    def is_resolved(self) -> bool:
        return self.upstream is not None and self.confidence > 0.0

    @property
    def compare_key(self) -> str:
        """Canonical string for equality, grouping, and deduplication.

        This is **not** an ordering key. Comparing distro release suffixes
        lexicographically is wrong in the common case: ``-10.el9`` sorts before
        ``-8.el9``, so ``curl-7.88.1-10.el9`` would appear older than
        ``curl-7.88.1-8.el9`` and the newer build would look like a downgrade.
        Ordering must go through the ecosystem-specific comparators in
        :mod:`infravce.applicability`.

        Only valid when :attr:`is_resolved`; callers must check first.
        """
        if not self.is_resolved:
            raise ValueError("cannot build a compare key for an unresolved version")
        parts = [self.upstream or ""]
        if self.pre_release:
            parts.append(f"~{self.pre_release}")
        if self.release:
            parts.append(f"-{self.release}")
        if self.epoch:
            parts.insert(0, f"{self.epoch}:")
        return "~".join(parts)


# --------------------------------------------------------------------------- #
# Core records
# --------------------------------------------------------------------------- #


class Observation(BaseModel):
    """Something observed about an asset, with the method that observed it."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str
    observation_id: str = Field(
        default_factory=lambda: uuid4().hex,
        description=(
            "Stable id for this observation. Applicability records reference it, "
            "so the same evidence seen twice is two votes from one asset rather "
            "than one vote counted twice."
        ),
    )
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    acquisition_method: AcquisitionMethod

    evidence: str = Field(description="Raw bytes or a hash of what was actually seen")
    raw_product: str = Field(description="Vendor string as reported, unnormalised")
    raw_version: str = Field(description="Version string as reported, unnormalised")

    resolved_product: str | None = None
    resolved_version: NormalisedVersion | None = None
    resolution_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    parse_notes: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _enforce_resolution_invariant(self) -> Observation:
        """An unresolved version must not carry a range-comparable value.

        This is the single most important guard in the system. grype#2606 shows
        what happens without it: a GitHub Action pinned by commit SHA was
        recorded with the SHA as its version, and every range comparison against
        it produced a false positive.
        """
        if self.resolved_version is None and self.resolution_confidence > 0.0:
            raise ValueError("resolution_confidence must be 0.0 when resolved_version is None")
        if self.resolved_version is not None and not self.resolved_version.is_resolved:
            self.resolution_confidence = 0.0
        return self

    @property
    def is_usable_for_matching(self) -> bool:
        """Whether applicability evaluation may proceed for this observation."""
        return (
            self.resolved_product is not None
            and self.resolved_version is not None
            and self.resolved_version.is_resolved
        )


class Applicability(BaseModel):
    """One advisory source's verdict on one observation."""

    model_config = ConfigDict(extra="forbid")

    observation_id: str
    advisory_source: AdvisorySource
    advisory_id: str
    range_representation: RangeRepresentation = RangeRepresentation.UNKNOWN
    verdict: ApplicabilityVerdict
    justification: Justification | None = None
    impact_statement: str | None = None
    evidence: str = Field(description="The specific fact this verdict rests on")
    advisory_published_at: datetime | None = None
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def _require_justification(self) -> Applicability:
        """CISA requires a justification or impact statement for not_affected."""
        if (
            self.verdict is ApplicabilityVerdict.NOT_AFFECTED
            and self.justification is None
            and not self.impact_statement
        ):
            raise ValueError(
                "not_affected requires a justification or an impact_statement "
                "(CISA Minimum Requirements for VEX)"
            )
        if self.verdict is ApplicabilityVerdict.AFFECTED and self.justification:
            raise ValueError("justification applies only to not_affected")
        return self

    @property
    def precedence_rank(self) -> int:
        return self.advisory_source.precedence_rank


class Finding(BaseModel):
    """A graded, evidence-backed claim that an asset is affected by a CVE."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str
    cve_id: str
    confidence_tier: ConfidenceTier

    supporting_observations: tuple[Observation, ...] = ()
    applicability_votes: tuple[Applicability, ...] = ()

    priority_score: float | None = None
    priority_breakdown: dict[str, float] = Field(default_factory=dict)

    evidence_bundle: dict[str, Any] = Field(default_factory=dict)
    suppression_state: str | None = None
    notes: tuple[str, ...] = ()

    @property
    def winning_vote(self) -> Applicability | None:
        """Highest-precedence verdict, with ties broken by recency.

        Dissent is preserved in ``applicability_votes`` rather than discarded;
        a source disagreement rate is itself a reported metric.
        """
        if not self.applicability_votes:
            return None
        return min(
            self.applicability_votes,
            key=lambda v: (v.precedence_rank, -v.evaluated_at.timestamp()),
        )

    @property
    def has_dissent(self) -> bool:
        return len({v.verdict for v in self.applicability_votes}) > 1

    @property
    def is_suppressed(self) -> bool:
        return self.suppression_state is not None


class Asset(BaseModel):
    """A discovered or declared asset, with attribution kept as a hypothesis.

    Angelova et al. (WEIS 2026) measured WHOIS attribution at 58% recall, 62%
    false positives and 94% overestimation of vulnerable hosts. The system
    therefore never asserts ownership; it records attribution with a confidence
    and routes unattributed assets to their own queue.
    """

    model_config = ConfigDict(extra="forbid")

    asset_id: str
    address: str | None = None
    hostname: str | None = None
    discovered_via: AcquisitionMethod
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    is_declared: bool = False
    is_authorised_for_active_scan: bool = False

    attribution_hypothesis: str | None = None
    attribution_confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    criticality: Literal["unknown", "low", "medium", "high", "critical"] = "unknown"
    internet_exposed: bool | None = None
    service_tags: tuple[str, ...] = ()

    @property
    def is_attributed(self) -> bool:
        return self.attribution_hypothesis is not None


class ScanCoverage(BaseModel):
    """Per-source ingest freshness. A first-class output, not an internal detail.

    Motivated by the OSV ten-day GHSA ingestion outage in April 2026 and by
    Greenbone's documented feed-coverage lag: in both cases a scanner would have
    matched correctly but the advisory was absent, and nothing in the scanner's
    own output revealed it.
    """

    model_config = ConfigDict(extra="forbid")

    source: AdvisorySource
    ecosystem: Ecosystem = Ecosystem.UNKNOWN
    last_successful_ingest: datetime | None = None
    record_count: int = 0
    is_stale: bool = False
    known_gaps: tuple[str, ...] = ()
    detail_url: str | None = None

    def summary(self) -> str:
        if self.last_successful_ingest is None:
            return f"{self.source}/{self.ecosystem}: NEVER INGESTED"
        age_h = (datetime.now(UTC) - self.last_successful_ingest).total_seconds() / 3600
        flag = " STALE" if self.is_stale else ""
        eco = self.ecosystem.value if self.ecosystem is not None else "all"
        return f"{self.source.value}/{eco}: {self.record_count} records, {age_h:.1f}h old{flag}"
