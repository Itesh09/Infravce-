"""Scoring tests.

The scorer is the part of the benchmark that must not be wrong in a convenient
direction, so the tests below are mostly about what the scorer *refuses* to do:
combine FP with recall, treat silence as correctness, or merge discovery errors
into verdict errors.
"""

from __future__ import annotations

import pytest

from infravce.bench.schema import (
    CaseClass,
    GroundTruthCase,
    GroundTruthSet,
    Prediction,
    PredictionSet,
    Provenance,
    TruthVerdict,
)
from infravce.bench.scoring import ErrorType, format_table, score

GT_VERSION = "2026-10-01"


def prov(reference_id: str = "DSA-0000-1", source: str = "Debian Security Tracker") -> Provenance:
    return Provenance(source=source, reference_id=reference_id, quote="status line")


def case(
    case_id: str,
    *,
    truth: TruthVerdict,
    case_class: CaseClass,
    cve: str = "CVE-2024-0001",
    asset: str = "web-01",
    product: str = "nginx",
    ecosystem: str = "rpm",
    version: str = "1.18.0",
) -> GroundTruthCase:
    return GroundTruthCase(
        case_id=case_id,
        asset_id=asset,
        product=product,
        ecosystem=ecosystem,
        version=version,
        cve_id=cve,
        truth=truth,
        case_class=case_class,
        provenance=prov(),
        lab_service="web",
    )


def pred(
    *,
    verdict: str,
    cve: str = "CVE-2024-0001",
    asset: str = "web-01",
    tier: str | None = "inferred",
    evidence: str | None = "matched range",
    matched_asset: bool = True,
) -> Prediction:
    return Prediction(
        asset_id=asset,
        cve_id=cve,
        verdict=verdict,
        confidence_tier=tier,
        evidence=evidence,
        matched_asset=matched_asset,
    )


def preds(tool: str, *ps: Prediction, gt_version: str = GT_VERSION) -> PredictionSet:
    return PredictionSet(
        tool=tool,
        ground_truth_version=gt_version,
        predictions=tuple(ps),
    )


# --------------------------------------------------------------------------- #
# Schema guards
# --------------------------------------------------------------------------- #


class TestProvenanceIsMandatory:
    def test_label_without_reference_or_quote_is_rejected(self) -> None:
        """Ground-truth rule 1. A source name alone is not checkable."""
        with pytest.raises(ValueError, match="reference_id or a quote"):
            Provenance(source="Debian Security Tracker")

    def test_reference_id_alone_is_enough(self) -> None:
        assert Provenance(source="tracker", reference_id="DSA-1").reference_id == "DSA-1"

    def test_quote_alone_is_enough(self) -> None:
        assert Provenance(source="tracker", quote="status: resolved").quote


class TestCaseClassMustAgreeWithTruth:
    def test_backport_cannot_be_labelled_affected(self) -> None:
        """The backport class exists to hold not_affected cases.

        A mislabelled one would make the headline backport metric meaningless
        and hide the FP rate that class exists to expose.
        """
        with pytest.raises(ValueError, match="case_class"):
            case(
                "bad",
                truth=TruthVerdict.AFFECTED,
                case_class=CaseClass.BACKPORT,
            )

    def test_deferred_patch_cannot_be_labelled_safe(self) -> None:
        with pytest.raises(ValueError, match="case_class"):
            case(
                "bad2",
                truth=TruthVerdict.NOT_AFFECTED,
                case_class=CaseClass.DEFERRED_PATCH,
            )

    def test_unparseable_version_must_be_unresolved(self) -> None:
        with pytest.raises(ValueError, match="case_class"):
            case(
                "bad3",
                truth=TruthVerdict.AFFECTED,
                case_class=CaseClass.UNPARSEABLE_VERSION,
            )

    def test_matching_class_and_truth_is_accepted(self) -> None:
        assert case("ok", truth=TruthVerdict.NOT_AFFECTED, case_class=CaseClass.BACKPORT)


class TestSetIntegrity:
    def test_duplicate_case_ids_rejected(self) -> None:
        c = case("dup", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED)
        with pytest.raises(ValueError, match="duplicate case_id"):
            GroundTruthSet(
                version=GT_VERSION,
                snapshot_date="2026-10-01",
                cases=(c, c.model_copy()),
            )

    def test_two_definite_contradictory_truths_rejected(self) -> None:
        """A pair cannot be both affected and not affected."""
        a = case("a", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED)
        b = case("b", truth=TruthVerdict.NOT_AFFECTED, case_class=CaseClass.BACKPORT)
        with pytest.raises(ValueError, match="contradictory"):
            GroundTruthSet(
                version=GT_VERSION,
                snapshot_date="2026-10-01",
                cases=(a, b),
            )

    def test_contested_truth_is_allowed(self) -> None:
        """Ground-truth rule 2: record the disagreement, do not resolve it."""
        a = case("a", truth=TruthVerdict.UNDER_INVESTIGATION, case_class=CaseClass.CONTESTED)
        b = case("b", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED)
        s = GroundTruthSet(version=GT_VERSION, snapshot_date="2026-10-01", cases=(a, b))
        assert len(s.cases) == 2


class TestPredictionSetIntegrity:
    def test_double_reporting_a_pair_is_rejected(self) -> None:
        """A tool reporting the same asset twice is a real defect."""
        p = pred(verdict="affected")
        with pytest.raises(ValueError, match="twice"):
            PredictionSet(tool="t", ground_truth_version=GT_VERSION, predictions=(p, p))

    def test_mismatched_cve_format_rejected(self) -> None:
        with pytest.raises(ValueError):
            Prediction(
                asset_id="web-01",
                cve_id="CVE-24-1",
                verdict="affected",
                confidence_tier=None,
            )


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #


class TestScoringSeparatesErrorTypes:
    def _gt(self, *cases: GroundTruthCase) -> GroundTruthSet:
        return GroundTruthSet(version=GT_VERSION, snapshot_date="2026-10-01", cases=tuple(cases))

    def test_correct_affected(self) -> None:
        gt = self._gt(case("a", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED))
        s = score(gt, preds("t", pred(verdict="affected")))
        assert (s.correct, s.false_positives, s.false_negatives) == (1, 0, 0)

    def test_backport_claimed_affected_is_a_false_positive(self) -> None:
        gt = self._gt(case("b", truth=TruthVerdict.NOT_AFFECTED, case_class=CaseClass.BACKPORT))
        s = score(gt, preds("t", pred(verdict="affected")))
        assert s.false_positives == 1
        assert s.class_score(CaseClass.BACKPORT).false_positives == 1

    def test_silence_on_affected_is_a_false_negative(self) -> None:
        gt = self._gt(case("c", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED))
        s = score(gt, preds("t"))
        assert s.false_negatives == 1

    def test_asserting_not_affected_on_affected_is_wrong_verdict(self) -> None:
        """An active claim of safety is worse than silence, and scored apart."""
        gt = self._gt(case("d", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED))
        s = score(gt, preds("t", pred(verdict="not_affected")))
        assert s.wrong_verdicts == 1
        assert s.false_negatives == 0

    def test_declining_on_an_answerable_case_is_a_false_negative(self) -> None:
        gt = self._gt(case("e", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED))
        s = score(gt, preds("t", pred(verdict="unresolved")))
        assert s.false_negatives == 1

    def test_unresolvable_case_answered_correctly(self) -> None:
        gt = self._gt(
            case(
                "f",
                truth=TruthVerdict.UNRESOLVED,
                case_class=CaseClass.UNPARSEABLE_VERSION,
                cve="CVE-2024-0002",
            )
        )
        s = score(gt, preds("t", pred(verdict="unresolved", cve="CVE-2024-0002")))
        assert s.correct_unknowns == 1
        assert s.false_positives == 0

    def test_silence_on_unresolvable_is_not_correct(self) -> None:
        """Silence is indistinguishable from not having looked (threat 5)."""
        gt = self._gt(
            case(
                "g",
                truth=TruthVerdict.UNRESOLVED,
                case_class=CaseClass.UNPARSEABLE_VERSION,
                cve="CVE-2024-0003",
            )
        )
        s = score(gt, preds("t"))
        assert s.correct_unknowns == 0
        assert s.silent_on_unresolved == 1

    def test_claiming_affected_on_unknown_truth_is_a_false_positive(self) -> None:
        gt = self._gt(
            case(
                "h",
                truth=TruthVerdict.UNRESOLVED,
                case_class=CaseClass.UNPARSEABLE_VERSION,
                cve="CVE-2024-0004",
            )
        )
        s = score(gt, preds("t", pred(verdict="affected", cve="CVE-2024-0004")))
        assert s.false_positives == 1

    def test_unknown_asset_is_a_discovery_error_not_a_false_positive(self) -> None:
        """Threat 12. Discovery errors must not inflate the FP rate."""
        gt = self._gt(case("i", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED))
        s = score(
            gt,
            preds(
                "t",
                pred(
                    verdict="affected", cve="CVE-2024-0009", asset="ghost-99", matched_asset=False
                ),
            ),
        )
        assert s.false_positives == 0
        assert s.unmatched_assets == 1
        assert any(e.error_type is ErrorType.UNMATCHED_ASSET for e in s.errors)

    def test_claim_on_uncategorised_cve_counts_as_false_positive(self) -> None:
        gt = self._gt(case("j", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED))
        s = score(gt, preds("t", pred(verdict="affected", cve="CVE-2024-0099")))
        assert s.false_positives == 1


class TestRatesAreSeparate:
    def _gt(self, *cases: GroundTruthCase) -> GroundTruthSet:
        return GroundTruthSet(version=GT_VERSION, snapshot_date="2026-10-01", cases=tuple(cases))

    def test_no_combined_f1_attribute_exists(self) -> None:
        """docs/03 §4.1. A single combined metric is the failure this avoids."""
        s = score(self._gt(), preds("t"))
        assert not hasattr(s, "f1")
        assert "f1" not in {r["metric"] for r in s.summary_rows()}

    def test_false_positive_rate_is_over_claims(self) -> None:
        gt = self._gt(
            case("a", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED),
            case(
                "b",
                truth=TruthVerdict.NOT_AFFECTED,
                case_class=CaseClass.BACKPORT,
                cve="CVE-2024-0002",
            ),
        )
        s = score(
            gt, preds("t", pred(verdict="affected"), pred(verdict="affected", cve="CVE-2024-0002"))
        )
        assert s.false_positive_rate == 0.5

    def test_false_negative_rate_is_over_affected_truth(self) -> None:
        gt = self._gt(
            case("a", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED),
            case(
                "b",
                truth=TruthVerdict.AFFECTED,
                case_class=CaseClass.PLAIN_AFFECTED,
                cve="CVE-2024-0002",
            ),
        )
        s = score(gt, preds("t", pred(verdict="affected")))
        assert s.false_negative_rate == 0.5

    def test_zero_affected_truth_gives_zero_fn_rate_not_a_crash(self) -> None:
        gt = self._gt(case("a", truth=TruthVerdict.NOT_AFFECTED, case_class=CaseClass.KNOWN_SAFE))
        s = score(gt, preds("t"))
        assert s.false_negative_rate == 0.0


class TestCalibration:
    def _gt(self, *cases: GroundTruthCase) -> GroundTruthSet:
        return GroundTruthSet(version=GT_VERSION, snapshot_date="2026-10-01", cases=tuple(cases))

    def test_tier_precision_is_measured_per_tier(self) -> None:
        """E3. A WEAK tier that is 90% wrong looks like signal."""
        gt = self._gt(
            case("a", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED),
            case(
                "b",
                truth=TruthVerdict.NOT_AFFECTED,
                case_class=CaseClass.BACKPORT,
                cve="CVE-2024-0002",
            ),
        )
        s = score(
            gt,
            preds(
                "t",
                pred(verdict="affected", tier="verified"),
                pred(verdict="affected", tier="weak", cve="CVE-2024-0002"),
            ),
        )
        assert s.tier_calibration("verified").observed_precision == 1.0
        assert s.tier_calibration("weak").observed_precision == 0.0
        assert s.is_calibration_monotonic() is True

    def test_non_monotonic_calibration_is_reported_not_hidden(self) -> None:
        """E3 says a non-monotonic result is a finding, not something to tune away."""
        gt = self._gt(
            case("a", truth=TruthVerdict.NOT_AFFECTED, case_class=CaseClass.KNOWN_SAFE),
            case(
                "b",
                truth=TruthVerdict.AFFECTED,
                case_class=CaseClass.PLAIN_AFFECTED,
                cve="CVE-2024-0002",
            ),
        )
        s = score(
            gt,
            preds(
                "t",
                pred(verdict="affected", tier="verified"),
                pred(verdict="affected", tier="weak", cve="CVE-2024-0002"),
            ),
        )
        assert s.is_calibration_monotonic() is False

    def test_single_tier_leaves_monotonicity_undefined(self) -> None:
        gt = self._gt(case("a", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED))
        assert (
            score(
                gt, preds("t", pred(verdict="affected", tier="inferred"))
            ).is_calibration_monotonic()
            is None
        )


class TestProvenanceCompleteness:
    def test_measured_from_the_predictions(self) -> None:
        gt = GroundTruthSet(
            version=GT_VERSION,
            snapshot_date="2026-10-01",
            cases=(
                case("a", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED),
                case(
                    "b",
                    truth=TruthVerdict.AFFECTED,
                    case_class=CaseClass.PLAIN_AFFECTED,
                    cve="CVE-2024-0002",
                ),
            ),
        )
        s = score(
            gt,
            preds(
                "t",
                pred(verdict="affected", evidence="dpkg status: vulnerable"),
                pred(verdict="affected", cve="CVE-2024-0002", evidence=None),
            ),
        )
        assert s.provenance_completeness == 0.5

    def test_no_claims_reports_none_not_zero(self) -> None:
        gt = GroundTruthSet(
            version=GT_VERSION,
            snapshot_date="2026-10-01",
            cases=(case("a", truth=TruthVerdict.AFFECTED, case_class=CaseClass.PLAIN_AFFECTED),),
        )
        assert score(gt, preds("t")).provenance_completeness is None


class TestWarnings:
    def test_version_mismatch_warns(self) -> None:
        gt = GroundTruthSet(version=GT_VERSION, snapshot_date="2026-10-01", cases=())
        s = score(gt, preds("t", gt_version="2020-01-01"))
        assert any("2020-01-01" in w for w in s.warnings)

    def test_stale_tool_snapshot_warns(self) -> None:
        """E5. Data staleness is not tool error and must be called out."""
        gt = GroundTruthSet(version=GT_VERSION, snapshot_date="2026-10-01", cases=())
        p = PredictionSet(
            tool="t",
            ground_truth_version=GT_VERSION,
            snapshot_date="2026-09-01",
            predictions=(),
        )
        s = score(gt, p)
        assert any("30 day" in w for w in s.warnings)

    def test_matching_snapshots_are_silent(self) -> None:
        gt = GroundTruthSet(version=GT_VERSION, snapshot_date="2026-10-01", cases=())
        p = PredictionSet(
            tool="t",
            ground_truth_version=GT_VERSION,
            snapshot_date="2026-10-01",
            predictions=(),
        )
        assert score(gt, p).warnings == ()


def test_format_table_renders_rows() -> None:
    out = format_table([{"a": 1, "b": "x"}, {"a": 22, "b": "yy"}])
    assert "a" in out and "22" in out and "-" in out
