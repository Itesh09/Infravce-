"""Schemas for INFRA-CVE-Bench ground truth and tool predictions.

Two rules from ``docs/03-evaluation-plan.md`` are encoded structurally here,
rather than left to the scorer to remember:

1. Every ground-truth label must carry provenance. A label without a source is
   rejected at load time, so an unprovenanced label cannot reach the scorer.
2. FP and FN must never be combined into one headline number. There is no
   ``f1`` property anywhere in this module, deliberately, so that no summary
   reporter can invent one later.
"""

from __future__ import annotations

import json
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Final

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

__all__ = [
    "CaseClass",
    "GroundTruthCase",
    "GroundTruthSet",
    "Prediction",
    "PredictionSet",
    "TruthVerdict",
]


class TruthVerdict(StrEnum):
    """The correct answer for one ``(asset, CVE)`` pair.

    ``UNKNOWN`` is a first-class value. The published CVE data is categorically
    incomplete for distro packages, so "the truth is genuinely undetermined" is
    sometimes the honest label and must be scorable rather than guessed at.
    """

    AFFECTED = "affected"
    NOT_AFFECTED = "not_affected"
    UNDER_INVESTIGATION = "under_investigation"
    UNRESOLVED = "unresolved"


class CaseClass(StrEnum):
    """Why a case is in the benchmark.

    Per-class scores are the actionable output. A single aggregate over these
    classes is meaningless, because they exist to test different failure modes.
    """

    #: Upstream CVE already fixed downstream. Version comparison alone fails.
    BACKPORT = "backport"
    #: Vulnerable code was never shipped in this package.
    NEVER_PRESENT = "never_present"
    #: Genuinely vulnerable and genuinely unpatched. Must not be downgraded.
    DEFERRED_PATCH = "deferred_patch"
    #: Vendor namespace collides with another product. Identity is the question.
    AMBIGUOUS_IDENTITY = "ambiguous_identity"
    #: SHA-pinned, ``(devel)``, truncated. Correct output is ``unresolved``.
    UNPARSEABLE_VERSION = "unparseable_version"
    #: Banner advertises a vulnerable version the service does not run.
    DECOY = "decoy"
    #: Ordinary vulnerable package. The control group.
    PLAIN_AFFECTED = "plain_affected"
    #: Present and not vulnerable. Measures FP rate on a realistic mix.
    KNOWN_SAFE = "known_safe"
    #: Ground truth itself is contested. Disagreement is the label.
    CONTESTED = "contested"


class Provenance(BaseModel):
    """Where a label came from. Mandatory, per ground-truth rule 1."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    source: str = Field(
        min_length=1,
        description="Authority that published the label, e.g. 'Debian Security Tracker'",
    )
    reference_id: str | None = Field(
        default=None, description="DSA id, CVE id, tracker URL, or commit hash"
    )
    snapshot_date: date | None = Field(
        default=None,
        description="Date the advisory data was read. CVE data decays, so a label "
        "without a snapshot date is not reproducible later.",
    )
    quote: str | None = Field(
        default=None, description="The specific text relied on, so a reviewer can check it"
    )

    @model_validator(mode="after")
    def _needs_a_reference_or_quote(self) -> Provenance:
        """A bare source name is not checkable.

        "Debian Security Tracker" alone does not identify a position; the DSA id
        does. Requiring one of the two prevents provenance that looks rigorous in
        a table but cannot be verified.
        """
        if not self.reference_id and not self.quote:
            raise ValueError(
                "provenance needs a reference_id or a quote to be verifiable (ground-truth rule 1)"
            )
        return self


class GroundTruthCase(BaseModel):
    """One ``(asset, CVE, expected verdict)`` triple, with its case class."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    case_id: str = Field(min_length=1)
    asset_id: str = Field(min_length=1)
    product: str = Field(min_length=1)
    ecosystem: str = Field(min_length=1)
    version: str = Field(
        description="Exactly as the lab reports it. Not normalised here: "
        "normalising the truth with the system's own code would let the system "
        "grade its own homework (threat 2)."
    )
    cve_id: str = Field(pattern=r"^CVE-\d{4}-\d{4,7}$|^GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}$")
    truth: TruthVerdict
    case_class: CaseClass
    provenance: Provenance
    secondary_provenance: Provenance | None = Field(
        default=None,
        description="A second independent source. Disagreement between the two is "
        "recorded rather than resolved silently (ground-truth rule 2).",
    )
    lab_service: str | None = Field(
        default=None, description="Compose service that materialises this asset"
    )
    lab_architecture: str | None = Field(
        default=None,
        description="Machine architecture of the asset. Recorded because a "
        "distribution can track an advisory as unfixed while the advisory's own "
        "description restricts it to another architecture; without this, a "
        "correctly reported not-affected finding looks like a miss.",
    )
    notes: str | None = None

    @model_validator(mode="after")
    def _class_must_agree_with_verdict(self) -> GroundTruthCase:
        """Catch a mislabelled case before it silently corrupts a class score.

        Each case class exists to test one failure mode, so a ``KNOWN_SAFE`` case
        carrying an ``AFFECTED`` truth would quietly inflate the safe-class score
        and understate the FP rate that class exists to measure.
        """
        expected: dict[CaseClass, set[TruthVerdict]] = {
            CaseClass.BACKPORT: {TruthVerdict.NOT_AFFECTED},
            CaseClass.NEVER_PRESENT: {TruthVerdict.NOT_AFFECTED},
            CaseClass.DEFERRED_PATCH: {TruthVerdict.AFFECTED},
            CaseClass.UNPARSEABLE_VERSION: {TruthVerdict.UNRESOLVED},
            CaseClass.AMBIGUOUS_IDENTITY: {TruthVerdict.AFFECTED, TruthVerdict.UNRESOLVED},
            CaseClass.DECOY: {TruthVerdict.NOT_AFFECTED},
            CaseClass.KNOWN_SAFE: {TruthVerdict.NOT_AFFECTED},
            CaseClass.PLAIN_AFFECTED: {TruthVerdict.AFFECTED},
            CaseClass.CONTESTED: set(TruthVerdict),
        }
        allowed = expected.get(self.case_class)
        if allowed is None:
            return self
        if self.truth not in allowed:
            raise ValueError(
                f"case_class {self.case_class.value!r} expects truth in "
                f"{sorted(v.value for v in allowed)}, got {self.truth.value!r}. "
                "The case class and the verdict must agree or the class score is meaningless."
            )
        return self

    @property
    def is_affected_truth(self) -> bool:
        return self.truth is TruthVerdict.AFFECTED

    @property
    def key(self) -> tuple[str, str, str, str]:
        """Identity of one labelled package instance.

        Includes product and version, so two builds of the same package on one
        asset stay distinct. That distinction is what makes the backport case
        measurable at all.
        """
        return (self.asset_id, self.product, self.version, self.cve_id)

    @property
    def pair(self) -> tuple[str, str]:
        """The ``(asset, CVE)`` pair a tool reports against.

        Coarser than :attr:`key`, because tools report one finding per asset and
        CVE without naming a specific build.
        """
        return (self.asset_id, self.cve_id)


class GroundTruthSet(BaseModel):
    """A frozen, versioned collection of ground-truth cases."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    version: str = Field(min_length=1, description="Bump when any label changes")
    snapshot_date: date = Field(
        description="Advisory snapshot this set was frozen against (threat 11)"
    )
    generated_by: str | None = Field(
        default=None,
        description="Tool that produced the file. Set when labels are derived "
        "from advisory data rather than written by hand, so a reader can tell "
        "derived labels from asserted ones.",
    )
    generated_at: str | None = Field(
        default=None, description="Timestamp the set was generated, when derived"
    )
    notes: str | None = None
    cases: tuple[GroundTruthCase, ...]

    @field_validator("cases")
    @classmethod
    def _unique_case_ids(cls, v: tuple[GroundTruthCase, ...]) -> tuple[GroundTruthCase, ...]:
        ids = [c.case_id for c in v]
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            raise ValueError(f"duplicate case_id(s): {sorted(dupes)}")
        return v

    @model_validator(mode="after")
    def _no_contradictions(self) -> GroundTruthSet:
        """Two cases for the same package instance and CVE is a bug.

        Keyed on ``(asset, product, version, cve)`` rather than
        ``(asset, cve)`` on purpose: one asset legitimately holds two builds of
        the same product, and a CVE can be fixed in one and unfixed in the other.
        That pair is the backport case working as intended, so collapsing it
        would delete the most important distinction in the benchmark.

        Allowed through when at least one label is genuinely undetermined, which
        is how a real contested label is expressed.
        """
        by_key: dict[tuple[str, str, str, str], list[GroundTruthCase]] = {}
        for c in self.cases:
            by_key.setdefault((c.asset_id, c.product, c.version, c.cve_id), []).append(c)

        for (asset_id, product, version, cve_id), group in by_key.items():
            truths = {c.truth for c in group}
            if len(group) > 1 and len(truths) > 1:
                unresolved_present = bool(
                    truths & {TruthVerdict.UNRESOLVED, TruthVerdict.UNDER_INVESTIGATION}
                )
                if not unresolved_present:
                    raise ValueError(
                        f"contradictory ground truth for {asset_id} "
                        f"{product} {version} / {cve_id}: "
                        f"{sorted(t.value for t in truths)}. Two definite answers "
                        "means one of them is wrong."
                    )
        return self

    def by_class(self) -> dict[CaseClass, tuple[GroundTruthCase, ...]]:
        out: dict[CaseClass, list[GroundTruthCase]] = {}
        for c in self.cases:
            out.setdefault(c.case_class, []).append(c)
        return {k: tuple(v) for k, v in out.items()}


class Prediction(BaseModel):
    """One finding reported by a tool under test."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(min_length=1)
    cve_id: str = Field(pattern=r"^CVE-\d{4}-\d{4,7}$|^GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}$")
    verdict: str = Field(
        description="'affected', 'not_affected', 'under_investigation' or 'unresolved'"
    )
    product: str | None = None
    version: str | None = None
    confidence_tier: str | None = Field(
        default=None, description="Tool's own grading, if it has one"
    )
    confidence_value: float | None = Field(default=None, ge=0.0, le=1.0)
    advisory_source: str | None = None
    evidence: str | None = Field(
        default=None, description="Free text. Provenance completeness is measured, not assumed."
    )
    matched_asset: bool = Field(
        default=True,
        description="False when the tool reported a finding against an asset that is "
        "not in the lab at all. That is a discovery error, counted separately from "
        "a wrong verdict on a real asset.",
    )

    @property
    def is_affected_claim(self) -> bool:
        return self.verdict.strip().lower() == "affected"


class PredictionSet(BaseModel):
    """One tool's complete output for one run, plus run metadata."""

    model_config = ConfigDict(extra="forbid")

    tool: str = Field(min_length=1)
    tool_version: str | None = None
    mode: str | None = Field(default=None, description="How it was run, e.g. 'sbom' or 'image'")
    ground_truth_version: str = Field(
        min_length=1, description="Which frozen truth this run was scored against"
    )
    snapshot_date: date | None = Field(
        default=None,
        description="Advisory data the tool actually used. A tool whose "
        "snapshot is older than the truth's is being asked a harder question, so "
        "the gap is reported rather than hidden.",
    )
    notes: str | None = None
    predictions: tuple[Prediction, ...]

    @model_validator(mode="after")
    def _one_verdict_per_pair(self) -> PredictionSet:
        seen: dict[tuple[str, str], str] = {}
        for p in self.predictions:
            key = (p.asset_id, p.cve_id)
            if key in seen:
                raise ValueError(
                    f"{self.tool} reported {p.cve_id} on {p.asset_id} twice "
                    f"(verdicts {seen[key]!r} and {p.verdict!r}). Deduplicate upstream: "
                    "a tool double-reporting an asset is a real defect, and silently "
                    "collapsing it here would hide it."
                )
            seen[key] = p.verdict
        return self

    def pairs(self) -> set[tuple[str, str]]:
        return {(p.asset_id, p.cve_id) for p in self.predictions}


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #

_GT_REQUIRED: Final = {
    "version",
    "snapshot_date",
    "cases",
}
_PRED_REQUIRED: Final = {
    "tool",
    "ground_truth_version",
    "predictions",
}


def load_ground_truth(path: str | Path) -> GroundTruthSet:
    """Load and validate a frozen ground-truth file."""
    data = json.loads(Path(path).read_text())
    missing = _GT_REQUIRED - data.keys()
    if missing:
        raise ValueError(f"{path}: ground truth missing required key(s) {sorted(missing)}")
    return GroundTruthSet(**data)


def load_predictions(path: str | Path) -> PredictionSet:
    """Load one tool's output."""
    data = json.loads(Path(path).read_text())
    missing = _PRED_REQUIRED - data.keys()
    if missing:
        raise ValueError(f"{path}: predictions missing required key(s) {sorted(missing)}")
    return PredictionSet(**data)


def dump(obj: BaseModel, path: str | Path) -> None:
    """Write a validated model as JSON, so fixtures cannot drift from schema."""
    Path(path).write_text(obj.model_dump_json(indent=2) + "\n")
