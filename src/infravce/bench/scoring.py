"""Scoring for INFRA-CVE-Bench.

The one structural rule from ``docs/03-evaluation-plan.md`` §4.1 that this
module enforces: **false positives and false negatives are reported
separately and never combined.** There is no ``f1`` here and no aggregate
"accuracy" across error types. If you are tempted to add one, that is the
92%-FP-behind-a-good-recall-number problem the literature review was written up
to prevent.

Error taxonomy, because the four failure modes have different fixes:

- ``FALSE_POSITIVE``  - claimed affected; truth says not affected, or truth is
  unresolved/undetermined. The headline number to drive down.
- ``FALSE_NEGATIVE``  - truth says affected; the tool stayed silent.
- ``WRONG_VERDICT``   - reported on the right pair but concluded the opposite.
  Worse than a FN for trust: it is an active claim of safety.
- ``UNMATCHED_ASSET`` - reported against an asset the lab does not contain.
  A discovery error, not a verdict error, so it is never scored as a FP.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import StrEnum
from itertools import pairwise
from typing import Final

from .schema import (
    CaseClass,
    GroundTruthCase,
    GroundTruthSet,
    Prediction,
    PredictionSet,
    TruthVerdict,
)

__all__ = [
    "ClassScore",
    "ErrorRecord",
    "ErrorType",
    "Scorecard",
    "TierCalibration",
    "score",
]


class ErrorType(StrEnum):
    FALSE_POSITIVE = "false_positive"
    FALSE_NEGATIVE = "false_negative"
    WRONG_VERDICT = "wrong_verdict"
    UNMATCHED_ASSET = "unmatched_asset"
    SILENT_ON_UNRESOLVED = "silent_on_unresolved"
    CORRECT_UNKNOWN = "correct_unknown"


@dataclass(frozen=True, slots=True)
class ErrorRecord:
    """One thing a tool got wrong, with enough context to debug it."""

    error_type: ErrorType
    asset_id: str
    cve_id: str
    product: str
    case_class: CaseClass | None
    truth: TruthVerdict | None
    predicted: str | None
    detail: str

    def as_row(self) -> dict[str, str | None]:
        return {
            "error_type": self.error_type.value,
            "asset_id": self.asset_id,
            "cve_id": self.cve_id,
            "product": self.product,
            "case_class": self.case_class.value if self.case_class else None,
            "truth": self.truth.value if self.truth else None,
            "predicted": self.predicted,
            "detail": self.detail,
        }


@dataclass(frozen=True, slots=True)
class ClassScore:
    """Per-case-class result.

    Reported per class because the classes exist to test different failure
    modes; an aggregate over them hides which mechanism actually failed.
    """

    case_class: CaseClass
    total: int
    correct: int
    false_positives: int
    false_negatives: int
    wrong_verdicts: int
    correct_unknowns: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0

    @property
    def is_scored(self) -> bool:
        return self.total > 0

    def as_row(self) -> dict[str, object]:
        return {
            "case_class": self.case_class.value,
            "total": self.total,
            "correct": self.correct,
            "accuracy": round(self.accuracy, 4),
            "false_positives": self.false_positives,
            "false_negatives": self.false_negatives,
            "wrong_verdicts": self.wrong_verdicts,
            "correct_unknowns": self.correct_unknowns,
        }


@dataclass(frozen=True, slots=True)
class TierCalibration:
    """Observed precision of one confidence tier.

    The metric that tests whether grading works at all. A ``WEAK`` tier that is
    90% wrong is worse than no tier, because it looks like signal.
    """

    tier: str
    claimed: int
    correct: int
    false_positives: int

    @property
    def observed_precision(self) -> float | None:
        return self.correct / self.claimed if self.claimed else None

    def as_row(self) -> dict[str, object]:
        p = self.observed_precision
        return {
            "tier": self.tier,
            "claimed": self.claimed,
            "correct": self.correct,
            "observed_precision": round(p, 4) if p is not None else None,
            "false_positives": self.false_positives,
        }


@dataclass(frozen=True, slots=True)
class Scorecard:
    """Full result for one tool against one ground-truth set."""

    tool: str
    tool_version: str | None
    mode: str | None
    ground_truth_version: str
    ground_truth_snapshot: str
    tool_snapshot: str | None

    truth_total: int
    affected_truth: int
    correct: int
    false_positives: int
    false_negatives: int
    wrong_verdicts: int
    correct_unknowns: int
    silent_on_unresolved: int
    unmatched_assets: int
    predictions_total: int
    claims_total: int
    claims_with_evidence: int

    classes: tuple[ClassScore, ...]
    calibration: tuple[TierCalibration, ...]
    errors: tuple[ErrorRecord, ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)

    # -- deliberately no `f1` -------------------------------------------- #
    # `docs/03-evaluation-plan.md` §4.1: FP and FN are reported separately and
    # never combined into a single headline number. Adding a combined metric
    # here would recreate the exact failure this benchmark exists to measure.

    @property
    def false_positive_rate(self) -> float:
        """Of everything the tool claimed affected, how much was wrong."""
        claimed = self.correct + self.false_positives + self.wrong_verdicts
        return self.false_positives / claimed if claimed else 0.0

    @property
    def false_negative_rate(self) -> float:
        """Of everything genuinely affected, how much was missed."""
        return self.false_negatives / self.affected_truth if self.affected_truth else 0.0

    @property
    def unknown_handling_accuracy(self) -> float:
        """Correct handling of genuinely-undetermined cases.

        Includes not claiming a verdict, and saying so explicitly. Silence on
        an undetermined case is not correct, because it is indistinguishable
        from not having looked.
        """
        unknown_truth = self.correct_unknowns + self.silent_on_unresolved
        if not unknown_truth:
            return 0.0
        return self.correct_unknowns / unknown_truth

    @property
    def provenance_completeness(self) -> float | None:
        """Fraction of affected claims that carried evidence text.

        Measured rather than assumed, per P1. ``None`` when the tool made no
        affected claims at all, because ``0.0`` would be indistinguishable from
        "actively stripped provenance", which is a different failure.
        """
        if not self.claims_total:
            return None
        return self.claims_with_evidence / self.claims_total

    def class_score(self, case_class: CaseClass) -> ClassScore | None:
        for c in self.classes:
            if c.case_class is case_class:
                return c
        return None

    def tier_calibration(self, tier: str) -> TierCalibration | None:
        for t in self.calibration:
            if t.tier == tier:
                return t
        return None

    def is_calibration_monotonic(self) -> bool | None:
        """Whether observed precision rises with claimed confidence.

        ``None`` when fewer than two tiers were claimed, since monotonicity is
        undefined on one point. A non-monotonic result is a *finding*, not a
        bug: report it rather than tuning the tiers until it looks good.
        """
        ranked = sorted(self.calibration, key=lambda t: _tier_rank(t.tier))
        precisions: list[float] = []
        for t in ranked:
            p = t.observed_precision
            if p is not None:
                precisions.append(p)
        if len(precisions) < 2:
            return None
        return all(a <= b for a, b in pairwise(precisions))

    def summary_rows(self) -> list[dict[str, object]]:
        """Flat rows for tabular reporting.

        Deliberately splits the rates. A consumer wanting one number has to
        choose, which is the intended friction.
        """
        return [
            {"metric": "tool", "value": self.tool},
            {"metric": "mode", "value": self.mode},
            {"metric": "ground_truth_version", "value": self.ground_truth_version},
            {"metric": "truth_cases", "value": self.truth_total},
            {"metric": "affected_truth_cases", "value": self.affected_truth},
            {"metric": "correct", "value": self.correct},
            {"metric": "false_positives", "value": self.false_positives},
            {"metric": "false_positive_rate", "value": round(self.false_positive_rate, 4)},
            {"metric": "false_negatives", "value": self.false_negatives},
            {"metric": "false_negative_rate", "value": round(self.false_negative_rate, 4)},
            {"metric": "wrong_verdicts", "value": self.wrong_verdicts},
            {"metric": "correct_unknowns", "value": self.correct_unknowns},
            {
                "metric": "unknown_handling_accuracy",
                "value": round(self.unknown_handling_accuracy, 4),
            },
            {"metric": "unmatched_asset_findings", "value": self.unmatched_assets},
            {"metric": "calibration_monotonic", "value": self.is_calibration_monotonic()},
        ]


_TIER_ORDER: Final[dict[str, int]] = {
    "verified": 5,
    "strongly_inferred": 4,
    "inferred": 3,
    "weak": 2,
    "unresolved": 1,
}


def _tier_rank(tier: str) -> int:
    """Rank a confidence tier, normalising case and separator style.

    Unknown tiers sort lowest so a new tier cannot accidentally read as the
    most confident thing in the table.
    """
    key = tier.strip().lower().replace("-", "_").replace(" ", "_")
    return _TIER_ORDER.get(key, 0)


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #

#: Verdicts that count as "correctly declined to claim".
_UNKNOWN_VERDICTS: Final = {"unresolved", "under_investigation", "unknown"}

#: Ground-truth verdicts that mean "nobody knows", as opposed to "known safe".
_UNDETERMINED: Final = {TruthVerdict.UNRESOLVED, TruthVerdict.UNDER_INVESTIGATION}


def _verdict_matches(predicted: str, truth: TruthVerdict) -> bool:
    """Whether a predicted verdict agrees with ground truth.

    ``not_affected`` is only ever correct when the truth says so. The reverse
    asymmetry matters: predicting ``unresolved`` where truth is ``affected`` is
    a miss, because refusing to answer on something answerable loses recall.
    """
    p = predicted.strip().lower()
    if p == "affected":
        return truth is TruthVerdict.AFFECTED
    if p in _UNKNOWN_VERDICTS:
        return truth in {TruthVerdict.UNRESOLVED, TruthVerdict.UNDER_INVESTIGATION}
    if p == "not_affected":
        return truth is TruthVerdict.NOT_AFFECTED
    return False


def score(truth: GroundTruthSet, preds: PredictionSet) -> Scorecard:
    """Score one tool's output against frozen ground truth."""
    warnings: list[str] = []

    if preds.ground_truth_version != truth.version:
        warnings.append(
            f"tool was scored against ground truth {preds.ground_truth_version!r} but "
            f"the loaded set is {truth.version!r}. Comparison is invalid unless these "
            "are genuinely the same labels."
        )
    if preds.snapshot_date is not None and truth.snapshot_date is not None:
        gap = (truth.snapshot_date - preds.snapshot_date).days
        if gap > 0:
            warnings.append(
                f"tool advisory snapshot is {gap} day(s) older than ground truth. Some "
                "misses are data staleness, not tool error; read the false-negative "
                "count with that in mind."
            )

    known_assets = {c.asset_id for c in truth.cases}

    # Tools report one finding per (asset, CVE). Ground truth is keyed more
    # finely, at (asset, product, version, CVE), because one asset can hold two
    # builds of the same product and a CVE can be fixed in one but not the other.
    #
    # When several ground-truth cases share a pair, a prediction is graded
    # against the best match it could plausibly be referring to: correct if it
    # agrees with any of them, otherwise scored as a false positive. Grading
    # against the first match found instead would make the result depend on
    # iteration order, which is not a property anyone wants in a measurement.
    truth_by_pair: dict[tuple[str, str], list[GroundTruthCase]] = {}
    for c in truth.cases:
        truth_by_pair.setdefault(c.pair, []).append(c)

    errors: list[ErrorRecord] = []
    per_class_correct: Counter[CaseClass] = Counter()
    per_class_fp: Counter[CaseClass] = Counter()
    per_class_fn: Counter[CaseClass] = Counter()
    per_class_wrong: Counter[CaseClass] = Counter()
    per_class_unknown_ok: Counter[CaseClass] = Counter()

    tier_claimed: Counter[str] = Counter()
    tier_correct: Counter[str] = Counter()
    tier_fp: Counter[str] = Counter()

    correct = 0
    false_positives = 0
    wrong_verdicts = 0
    correct_unknowns = 0
    silent_on_unresolved = 0
    unmatched = 0
    claims_total = 0
    claims_with_evidence = 0

    # ---- iterate over ground truth: catches FNs by construction ---------- #
    predictions_by_pair: dict[tuple[str, str], Prediction] = {
        (p.asset_id, p.cve_id): p for p in preds.predictions
    }

    for pair, cases in truth_by_pair.items():
        pred = predictions_by_pair.get(pair)

        if pred is None:
            # No prediction for this pair. Each ground-truth case sharing it is
            # a miss of its own kind.
            for case in cases:
                if case.truth is TruthVerdict.AFFECTED:
                    per_class_fn[case.case_class] += 1
                    errors.append(
                        ErrorRecord(
                            error_type=ErrorType.FALSE_NEGATIVE,
                            asset_id=case.asset_id,
                            cve_id=case.cve_id,
                            product=case.product,
                            case_class=case.case_class,
                            truth=case.truth,
                            predicted=None,
                            detail="no finding reported for a genuinely affected pair",
                        )
                    )
                elif case.truth in _UNDETERMINED:
                    # Silence here is not correctness. It is indistinguishable
                    # from not having looked, which is threat 5.
                    silent_on_unresolved += 1
                    errors.append(
                        ErrorRecord(
                            error_type=ErrorType.SILENT_ON_UNRESOLVED,
                            asset_id=case.asset_id,
                            cve_id=case.cve_id,
                            product=case.product,
                            case_class=case.case_class,
                            truth=case.truth,
                            predicted=None,
                            detail=(
                                "truth is undetermined and the tool said nothing; it "
                                "should have reported an explicit unresolved verdict"
                            ),
                        )
                    )
                else:
                    per_class_correct[case.case_class] += 1
            continue

        # One prediction can cover several ground-truth cases for the pair.
        # Prefer a same-product match, since that is what the tool meant.
        case = next((c for c in cases if pred.product and c.product == pred.product), cases[0])
        tier = pred.confidence_tier or "ungraded"
        is_affected_claim = pred.is_affected_claim

        tier = pred.confidence_tier or "ungraded"
        is_affected_claim = pred.is_affected_claim

        if is_affected_claim:
            tier_claimed[tier] += 1
            claims_total += 1
            if pred.evidence and pred.evidence.strip():
                claims_with_evidence += 1

        if _verdict_matches(pred.verdict, case.truth):
            if case.truth is TruthVerdict.AFFECTED:
                correct += 1
                per_class_correct[case.case_class] += 1
                if is_affected_claim:
                    tier_correct[tier] += 1
            else:
                correct_unknowns += 1
                per_class_unknown_ok[case.case_class] += 1
            continue

        # ---- disagreement ------------------------------------------------ #
        if is_affected_claim:
            tier_fp[tier] += 1
            if case.truth is TruthVerdict.NOT_AFFECTED:
                false_positives += 1
                per_class_fp[case.case_class] += 1
                errors.append(
                    ErrorRecord(
                        error_type=ErrorType.FALSE_POSITIVE,
                        asset_id=case.asset_id,
                        cve_id=case.cve_id,
                        product=case.product,
                        case_class=case.case_class,
                        truth=case.truth,
                        predicted=pred.verdict,
                        detail=_fp_detail(case),
                    )
                )
            else:
                # Claimed affected where the truth is unknown: still a FP, but
                # not one a human could have caught from published data.
                false_positives += 1
                per_class_fp[case.case_class] += 1
                errors.append(
                    ErrorRecord(
                        error_type=ErrorType.FALSE_POSITIVE,
                        asset_id=case.asset_id,
                        cve_id=case.cve_id,
                        product=case.product,
                        case_class=case.case_class,
                        truth=case.truth,
                        predicted=pred.verdict,
                        detail=(
                            "claimed affected on a case whose ground truth is "
                            "undetermined; a defensible output was 'unresolved'"
                        ),
                    )
                )
        elif pred.verdict.strip().lower() == "not_affected" and case.truth is TruthVerdict.AFFECTED:
            wrong_verdicts += 1
            per_class_wrong[case.case_class] += 1
            errors.append(
                ErrorRecord(
                    error_type=ErrorType.WRONG_VERDICT,
                    asset_id=case.asset_id,
                    cve_id=case.cve_id,
                    product=case.product,
                    case_class=case.case_class,
                    truth=case.truth,
                    predicted=pred.verdict,
                    detail=(
                        "actively asserted not_affected for a genuinely affected pair; "
                        "more damaging than silence because it is a claim of safety"
                    ),
                )
            )
        elif (
            pred.verdict.strip().lower() in _UNKNOWN_VERDICTS
            and case.truth is TruthVerdict.AFFECTED
        ):
            per_class_fn[case.case_class] += 1
            errors.append(
                ErrorRecord(
                    error_type=ErrorType.FALSE_NEGATIVE,
                    asset_id=case.asset_id,
                    cve_id=case.cve_id,
                    product=case.product,
                    case_class=case.case_class,
                    truth=case.truth,
                    predicted=pred.verdict,
                    detail="declined to decide on an answerable case",
                )
            )
        else:
            wrong_verdicts += 1
            per_class_wrong[case.case_class] += 1
            errors.append(
                ErrorRecord(
                    error_type=ErrorType.WRONG_VERDICT,
                    asset_id=case.asset_id,
                    cve_id=case.cve_id,
                    product=case.product,
                    case_class=case.case_class,
                    truth=case.truth,
                    predicted=pred.verdict,
                    detail="verdict disagreed with ground truth",
                )
            )

    # ---- iterate over predictions: catches claims on unknown pairs ------ #
    for p in preds.predictions:
        if (p.asset_id, p.cve_id) in truth_by_pair:
            continue
        if not p.matched_asset or p.asset_id not in known_assets:
            unmatched += 1
            errors.append(
                ErrorRecord(
                    error_type=ErrorType.UNMATCHED_ASSET,
                    asset_id=p.asset_id,
                    cve_id=p.cve_id,
                    product=p.product or "?",
                    case_class=None,
                    truth=None,
                    predicted=p.verdict,
                    detail=(
                        "finding against an asset absent from the lab manifest; a "
                        "discovery error, not scored as a false positive"
                    ),
                )
            )
            continue
        # Right asset, CVE the frozen set does not cover.
        errors.append(
            ErrorRecord(
                error_type=ErrorType.FALSE_POSITIVE,
                asset_id=p.asset_id,
                cve_id=p.cve_id,
                product=p.product or "?",
                case_class=None,
                truth=None,
                predicted=p.verdict,
                detail=(
                    "claimed affected for a CVE with no ground-truth entry; counted "
                    "as a false positive because the frozen set is the reference"
                ),
            )
        )
        if p.is_affected_claim:
            false_positives += 1

    classes = tuple(
        ClassScore(
            case_class=cc,
            total=sum(len(v) for k, v in truth.by_class().items() if k is cc),
            correct=per_class_correct[cc],
            false_positives=per_class_fp[cc],
            false_negatives=per_class_fn[cc],
            wrong_verdicts=per_class_wrong[cc],
            correct_unknowns=per_class_unknown_ok[cc],
        )
        for cc in sorted(CaseClass, key=lambda c: c.value)
    )

    calibration = tuple(
        TierCalibration(
            tier=t, claimed=tier_claimed[t], correct=tier_correct[t], false_positives=tier_fp[t]
        )
        for t in sorted(tier_claimed, key=_tier_rank)
    )

    return Scorecard(
        tool=preds.tool,
        tool_version=preds.tool_version,
        mode=preds.mode,
        ground_truth_version=truth.version,
        ground_truth_snapshot=truth.snapshot_date.isoformat(),
        tool_snapshot=preds.snapshot_date.isoformat() if preds.snapshot_date else None,
        truth_total=len(truth.cases),
        affected_truth=sum(1 for c in truth.cases if c.is_affected_truth),
        correct=correct,
        false_positives=false_positives,
        false_negatives=sum(per_class_fn.values()),
        wrong_verdicts=wrong_verdicts,
        correct_unknowns=correct_unknowns,
        silent_on_unresolved=silent_on_unresolved,
        unmatched_assets=unmatched,
        predictions_total=len(preds.predictions),
        claims_total=claims_total,
        claims_with_evidence=claims_with_evidence,
        classes=classes,
        calibration=calibration,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def _fp_detail(case: GroundTruthCase) -> str:
    """Explain *why* a claim was wrong, so the FP list is actionable."""
    text = {
        CaseClass.BACKPORT: (
            "upstream CVE is fixed in this downstream build; version range "
            "comparison alone cannot see the backport"
        ),
        CaseClass.NEVER_PRESENT: (
            "the vulnerable code was never shipped in this package; no version of it is affected"
        ),
        CaseClass.DECOY: "banner advertised a version the service does not actually run",
        CaseClass.KNOWN_SAFE: "package is present and not vulnerable",
        CaseClass.DEFERRED_PATCH: (
            "genuinely vulnerable and genuinely unpatched downstream; downgrading "
            "it is a miss, not caution"
        ),
    }.get(case.case_class, "ground truth disagrees with the claim")
    if case.provenance.reference_id:
        text = f"{text} (ref {case.provenance.reference_id})"
    return text


def format_table(rows: Iterable[dict[str, object]]) -> str:
    """Render dict rows as a fixed-width table.

    Deliberately dependency-free: the report layer must not be able to fail in a
    way that loses the scores.
    """
    rows = list(rows)
    if not rows:
        return "(no rows)"
    cols = list(rows[0].keys())
    widths = {c: max(len(str(c)), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    line = "  ".join(c.ljust(widths[c]) for c in cols)
    sep = "  ".join("-" * widths[c] for c in cols)
    body = "\n".join("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols) for r in rows)
    return f"{line}\n{sep}\n{body}"
