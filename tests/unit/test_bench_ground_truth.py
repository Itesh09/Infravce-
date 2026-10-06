"""Ground-truth integrity tests.

The frozen ground truth and its two reference prediction sets are fixtures for
the whole study. If they drift, every recorded result becomes incomparable, so
they are validated in CI rather than trusted on disk.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from infravce.bench.schema import (
    CaseClass,
    GroundTruthSet,
    PredictionSet,
    TruthVerdict,
    load_ground_truth,
    load_predictions,
)
from infravce.bench.scoring import score

BENCH = Path(__file__).parents[2] / "bench" / "infra-cve-bench"
GT_DIR = BENCH / "ground-truth"
GT_PATH = GT_DIR / "cases.json"
PRED_DIR = GT_DIR / "predictions"

#: Every frozen version, newest last. Each stays in the repository: a set is
#: never edited in place, so results recorded against one remain reproducible
#: after a later freeze supersedes it.
GT_VERSIONS = (
    GT_DIR / "cases.2026.10.01-rc1.json",
    GT_DIR / "cases.json",
)


@pytest.fixture(scope="module")
def truth() -> GroundTruthSet:
    return load_ground_truth(GT_PATH)


@pytest.mark.parametrize("path", GT_VERSIONS, ids=lambda p: p.name)
class TestEveryFrozenVersionIsStillValid:
    """Old versions must keep validating.

    If a superseded version stops loading, results recorded against it can no
    longer be reproduced or compared, which quietly destroys the audit trail the
    version field exists to provide.
    """

    def test_loads(self, path: Path) -> None:
        gt = load_ground_truth(path)
        assert gt.cases
        assert gt.version

    def test_every_case_has_provenance(self, path: Path) -> None:
        for case in load_ground_truth(path).cases:
            assert case.provenance.reference_id or case.provenance.quote, case.case_id
            assert case.provenance.snapshot_date is not None, case.case_id


def test_ground_truth_versions_are_distinct() -> None:
    """A new freeze must not reuse a previous version string.

    Two different label sets sharing a version string makes recorded results
    ambiguous: nothing says which labels a run was scored against.
    """
    versions = [load_ground_truth(p).version for p in GT_VERSIONS]
    assert len(versions) == len(set(versions)), versions


def test_active_version_is_newest_in_the_directory() -> None:
    """`cases.json` must be the newest freeze, not a stale leftover.

    Scoring silently uses `cases.json`, so a newer file sitting beside it would
    mean results are attributed to the wrong labels.
    """
    active = load_ground_truth(GT_PATH)
    for other in GT_VERSIONS:
        if other == GT_PATH:
            continue
        historical = load_ground_truth(other)
        assert active.snapshot_date >= historical.snapshot_date, (
            f"{GT_PATH.name} ({active.snapshot_date}) is older than "
            f"{other.name} ({historical.snapshot_date})"
        )


#: Classes whose labels come from a version comparison against a distribution
#: advisory, and therefore must show that comparison in their provenance quote.
#:
#: The other classes are decided by the shape of the evidence instead, so no
#: comparison exists to quote: NEVER_PRESENT rests on the package being absent,
#: UNPARSEABLE_VERSION and AMBIGUOUS_IDENTITY on the version or identity string
#: not resolving, CONTESTED on two records disagreeing, DECOY on a mismatch
#: between the advertised and installed version. Demanding comparison language
#: from those would mean inventing a quote that did not happen.
_ADVISORY_DERIVED_CLASSES = frozenset(
    {
        CaseClass.BACKPORT,
        CaseClass.DEFERRED_PATCH,
        CaseClass.KNOWN_SAFE,
        CaseClass.PLAIN_AFFECTED,
    }
)


def test_derived_labels_declare_how_they_were_made() -> None:
    """A derived set must say it was derived.

    Hand-written and machine-derived labels deserve different trust, and the
    difference should be visible in the artefact rather than only in the commit
    history.

    For the classes decided by comparing versions against a distribution advisory,
    each quote must show that comparison. The two advisory feeds word it
    differently (Debian reports a tracker status plus a comparison; Alpine reports
    a secfix boundary plus a comparison), so the assertion checks for the
    comparison itself rather than either vocabulary.
    """
    gt = load_ground_truth(GT_PATH)
    if gt.generated_by:
        assert gt.generated_at, "a derived set should record when it was generated"
        for case in gt.cases:
            if case.case_class not in _ADVISORY_DERIVED_CLASSES:
                continue
            quote = case.provenance.quote
            shows_reasoning = (
                "deb_compare(" in quote
                or "apk_version_lt(" in quote
                or "status=" in quote
                or "secfixes" in quote
            )
            assert shows_reasoning, f"{case.case_id} records no derivation: {quote}"


def test_topology_cases_record_what_was_actually_observed() -> None:
    """A label read off the lab must cite the observation it came from.

    The counter to the test above: cases decided by evidence shape still have to
    say *what* was seen, otherwise a later reader cannot tell an observed absence
    from an assumed one.
    """
    gt = load_ground_truth(GT_PATH)
    for case in gt.cases:
        if case.case_class in _ADVISORY_DERIVED_CLASSES:
            continue
        assert case.provenance.source.strip(), case.case_id
        assert len(case.provenance.quote.strip()) > 20, f"{case.case_id} quote is too thin"


def test_every_case_names_the_authority_it_came_from() -> None:
    """A derived label must name a source, not just carry a quote.

    Provenance is what separates a label someone checked from a label a tool
    emitted; without the source named, the two are indistinguishable.
    """
    for case in load_ground_truth(GT_PATH).cases:
        assert case.provenance.source.strip(), case.case_id


def test_derived_cases_never_compare_against_a_missing_version() -> None:
    """A version comparison must always have two real versions.

    An early version of the generator printed `deb_compare(7.88.1, None) = 1` for
    CVEs with no fixed version. That reads as the reasoning behind the label while
    being meaningless, which is worse than saying nothing. Only the literal
    absence of a boundary is checked; the honest phrase "verdict from status
    alone" is allowed.
    """
    gt = load_ground_truth(GT_PATH)
    if not gt.generated_by:
        pytest.skip("active ground truth is not machine-derived")
    for case in gt.cases:
        quote = case.provenance.quote
        assert not re.search(r"compare\(\s*[^,)]+,\s*None\s*\)", quote), case.case_id


class TestGroundTruthShape:
    def test_every_case_carries_provenance(self, truth: GroundTruthSet) -> None:
        """Ground-truth rule 1. No provenance means the label is not evidence."""
        for c in truth.cases:
            assert c.provenance.reference_id or c.provenance.quote, c.case_id

    def test_every_case_records_a_snapshot(self, truth: GroundTruthSet) -> None:
        """Threat 11. Advisory data decays; an undated label is not reproducible."""
        for c in truth.cases:
            assert c.provenance.snapshot_date is not None, c.case_id

    def test_every_case_names_a_lab_service(self, truth: GroundTruthSet) -> None:
        """A label not tied to something in the lab cannot be checked against it."""
        assert all(c.lab_service for c in truth.cases)

    def test_case_ids_are_unique(self, truth: GroundTruthSet) -> None:
        ids = [c.case_id for c in truth.cases]
        assert len(ids) == len(set(ids))

    def test_all_critical_case_classes_are_present(self, truth: GroundTruthSet) -> None:
        """The classes docs/03 §3.1 calls mandatory.

        A missing class would let the benchmark silently stop testing the thing
        it exists to test, with no failure to signal it.
        """
        present = {c.case_class for c in truth.cases}
        required = {
            CaseClass.BACKPORT,
            CaseClass.NEVER_PRESENT,
            CaseClass.DEFERRED_PATCH,
            CaseClass.AMBIGUOUS_IDENTITY,
            CaseClass.UNPARSEABLE_VERSION,
            CaseClass.DECOY,
            CaseClass.PLAIN_AFFECTED,
            CaseClass.KNOWN_SAFE,
            CaseClass.CONTESTED,
        }
        assert required <= present, f"missing: {sorted(c.value for c in required - present)}"

    def test_backport_class_is_substantial(self, truth: GroundTruthSet) -> None:
        """The headline claim needs more than one case to be worth reporting."""
        n = sum(1 for c in truth.cases if c.case_class is CaseClass.BACKPORT)
        assert n >= 3

    def test_there_is_at_least_one_affected_truth(self, truth: GroundTruthSet) -> None:
        """Without affected truth, false-negative rate is undefined and a tool
        that reports nothing would look perfect."""
        assert any(c.is_affected_truth for c in truth.cases)

    def test_known_safe_present_for_a_realistic_mix(self, truth: GroundTruthSet) -> None:
        """Without known-safe cases the FP rate is not comparable to the 92%
        baseline, which was measured on a mix rather than on positives only."""
        assert sum(1 for c in truth.cases if c.case_class is CaseClass.KNOWN_SAFE) >= 2

    def test_contested_case_has_two_sources(self, truth: GroundTruthSet) -> None:
        """Ground-truth rule 2: a contested label records the disagreement."""
        contested = [c for c in truth.cases if c.case_class is CaseClass.CONTESTED]
        assert contested
        assert all(c.secondary_provenance is not None for c in contested)

    def test_documented_notes_are_present(self, truth: GroundTruthSet) -> None:
        """Every case explains itself, so a reviewer can check the reasoning
        without reverse-engineering the label."""
        assert all(c.notes for c in truth.cases)


class TestGroundTruthFileIsStable:
    def test_version_and_snapshot_are_recorded(self, truth: GroundTruthSet) -> None:
        assert truth.version
        assert truth.snapshot_date is not None

    def test_shipped_file_matches_parsed_model(self, truth: GroundTruthSet) -> None:
        raw = json.loads(GT_PATH.read_text())
        assert len(raw["cases"]) == len(truth.cases)

    def test_validation_cli_would_accept_the_shipped_file(self, truth: GroundTruthSet) -> None:
        assert truth.cases, "ground truth must not be empty"


class TestNaiveBaselineFixture:
    """The null hypothesis must behave like the null hypothesis.

    If this fixture ever scores well, the harness is not measuring what the
    study claims to measure.
    """

    @pytest.fixture(scope="class")
    @classmethod
    def card(cls, truth: GroundTruthSet):
        return score(truth, load_predictions(PRED_DIR / "naive-nvd-range.json"))

    def test_its_false_positive_rate_grows_with_the_case_set(self, card) -> None:
        """Most of what the null hypothesis reports is wrong.

        Asserted as "the overwhelming majority" rather than a fixed 0.8. The exact
        rate moves whenever cases are added or the class mix shifts, so pinning the
        number would make an unrelated refreeze look like a scoring regression.
        What must hold is the property the hypothesis depends on: flagging
        everything is mostly incorrect.
        """
        assert card.false_positive_rate > 0.6, (
            "flagging every case should be mostly wrong; a lower rate means the "
            "fixture stopped modelling the null hypothesis"
        )
        assert card.false_positives > card.correct

    def test_it_never_reports_an_unknown_correctly(self, card) -> None:
        """It cannot, by construction: it has no way to express one.

        Worth asserting explicitly, because "unknown handling" is the metric that
        separates it from the prototype and this is the source of the difference.
        """
        assert card.correct_unknowns == 0

    def test_it_fails_every_backport_case(self, card) -> None:
        assert card.class_score(CaseClass.BACKPORT).false_positives >= 3

    def test_it_fails_the_unparseable_class(self, card) -> None:
        assert card.class_score(CaseClass.UNPARSEABLE_VERSION).false_positives >= 1

    def test_it_wrongly_claims_the_decoy(self, card) -> None:
        assert card.class_score(CaseClass.DECOY).false_positives == 1

    def test_its_extra_asset_is_a_discovery_error_not_a_fp(self, card) -> None:
        assert card.unmatched_assets == 1

    def test_it_carries_no_evidence(self, card) -> None:
        """Provenance completeness is the variable the study is testing."""
        assert card.provenance_completeness == 0.0


class TestPrototypeFixture:
    """The planned system's expected behaviour, pinned before it exists.

    This is a specification, not a result. Written by hand from
    docs/02-architecture.md so the benchmark cannot be tuned to whatever the
    system happens to do.
    """

    @pytest.fixture(scope="class")
    @classmethod
    def card(cls, truth: GroundTruthSet):
        return score(truth, load_predictions(PRED_DIR / "infravce-prototype.json"))

    def test_it_has_no_false_positives(self, card) -> None:
        """The headline hypothesis. Backport and never-present are where
        version-range matching fails, and the whole design exists to fix them."""
        assert card.false_positives == 0

    def test_it_never_claims_affected_on_a_not_affected_case(self, card) -> None:
        for e in card.errors:
            if e.error_type.value == "false_positive":
                assert e.case_class not in {CaseClass.BACKPORT, CaseClass.NEVER_PRESENT}

    def test_it_finds_the_control_case(self, card) -> None:
        """It must not win by refusing to report.

        The plain_affected control exists specifically to catch a tool that scores
        well on false positives simply by staying silent. Asserted as "every case
        in the class" so the check still works as the control grows.
        """
        control = card.class_score(CaseClass.PLAIN_AFFECTED)
        assert control.total >= 1
        assert control.correct == control.total, (
            f"control cases found {control.correct} of {control.total}; a tool that "
            "misses them may be winning by refusing to report"
        )

    def test_it_handles_unknowns_explicitly(self, card) -> None:
        """Silence is not correct handling (threat 5)."""
        assert card.correct_unknowns >= 6
        assert card.silent_on_unresolved == 0

    def test_every_claim_carries_evidence(self, card) -> None:
        assert card.provenance_completeness == 1.0

    def test_it_beats_the_null_hypothesis(self, truth: GroundTruthSet) -> None:
        """The comparison the study exists to make.

        Note what is *not* asserted: raw accuracy does not separate these two
        tools. The null hypothesis flags everything, so it gets every genuinely
        affected case right by construction, and the prototype's `correct` count
        can match it exactly. Accuracy on a set the tool has not seen would
        separate them, but here it cannot.

        The separation is in false positives and in unknowns, which is exactly why
        the benchmark reports those separately and refuses a combined headline
        number (see `docs/03-evaluation-plan.md` §4.1).
        """
        proto = score(truth, load_predictions(PRED_DIR / "infravce-prototype.json"))
        naive = score(truth, load_predictions(PRED_DIR / "naive-nvd-range.json"))
        assert proto.false_positive_rate < naive.false_positive_rate
        assert proto.correct_unknowns > naive.correct_unknowns
        assert proto.false_positives == 0


class TestPredictionFixturesLoad:
    @pytest.mark.parametrize("name", ["naive-nvd-range.json", "infravce-prototype.json"])
    def test_fixture_parses(self, name: str) -> None:
        ps: PredictionSet = load_predictions(PRED_DIR / name)
        assert ps.predictions

    @pytest.mark.parametrize("name", ["naive-nvd-range.json", "infravce-prototype.json"])
    def test_fixture_targets_the_current_ground_truth(self, name: str) -> None:
        """A fixture pinned to a stale truth version would silently compare
        against labels it was not written for."""
        truth = load_ground_truth(GT_PATH)
        assert load_predictions(PRED_DIR / name).ground_truth_version == truth.version

    @pytest.mark.parametrize("name", ["naive-nvd-range.json", "infravce-prototype.json"])
    def test_fixture_uses_known_asset_ids(self, name: str, truth: GroundTruthSet) -> None:
        """Assets are declared up front, so a finding elsewhere is a discovery
        error rather than an unknown label to score."""
        ps = load_predictions(PRED_DIR / name)
        known = {c.asset_id for c in truth.cases}
        for p in ps.predictions:
            assert p.asset_id in known or p.matched_asset is False, p.asset_id


class TestGroundTruthMatchesLabCompose:
    """Cross-check the labels against the lab definition.

    docs/03 threat 12: an asset the lab does not actually run caps measured
    recall below 100% for reasons that have nothing to do with the tools.
    """

    @pytest.fixture(scope="class")
    @classmethod
    def compose(cls) -> str:
        return (BENCH / "lab" / "docker-compose.yml").read_text()

    def test_every_lab_service_exists_in_compose(self, truth: GroundTruthSet, compose: str) -> None:
        for service in {c.lab_service for c in truth.cases if c.lab_service}:
            assert f"{service}:" in compose, f"{service} is labelled but not in compose"

    def test_compose_services_are_labelled_or_explicitly_fixtures(
        self, truth: GroundTruthSet, compose: str
    ) -> None:
        """A service in the lab with no ground truth would quietly cap recall.

        Two are deliberately unlabelled, and the exceptions are stated here
        rather than left implicit: the hidden backend that outside-in scanning
        is supposed to miss, and the proxy that fronts it.
        """
        services = {
            line.strip().rstrip(":")
            for line in compose.splitlines()
            if line.startswith("  ")
            and line.strip().endswith(":")
            and not line.strip().startswith("#")
        }
        candidates = {s for s in services if "-" in s and not s.startswith("x-")}
        labelled = {c.lab_service for c in truth.cases if c.lab_service}
        intentional_gaps = {
            # The origin is not published and has no CVE case. Its role is to
            # exist undetected, which is the discovery blind spot itself.
            "waffront-origin",
            # The proxy fronts the origin. It runs a current nginx with no known
            # finding, so it contributes only to the known-safe mix.
            "waf-proxy",
        }
        unlabelled = candidates - labelled
        assert unlabelled <= intentional_gaps, (
            f"unlabelled lab services with no documented reason: "
            f"{sorted(unlabelled - intentional_gaps)}"
        )

    def test_unknown_truth_is_used_for_unresolvable_labels(self, truth: GroundTruthSet) -> None:
        for c in truth.cases:
            if c.case_class is CaseClass.UNPARSEABLE_VERSION:
                assert c.truth is TruthVerdict.UNRESOLVED, c.case_id


class TestReportSerialisation:
    """Saved scorecards must carry their computed metrics.

    Regression: `asdict()` walks dataclass fields only, so every `@property` was
    dropped on write. `report` then read the absent `false_positive_rate` as
    `0.0`, which printed a 0% false-positive rate for a tool with eight false
    positives. The report now refuses cards missing required keys.
    """

    def test_written_card_includes_computed_rates(
        self, tmp_path: Path, truth: GroundTruthSet
    ) -> None:
        from infravce.bench.cli import _card_to_json

        card = score(truth, load_predictions(PRED_DIR / "naive-nvd-range.json"))
        data = json.loads(_card_to_json(card))
        for key in (
            "false_positive_rate",
            "false_negative_rate",
            "unknown_handling_accuracy",
            "calibration_monotonic",
        ):
            assert key in data, key
        assert data["false_positive_rate"] == card.false_positive_rate
        assert data["false_positive_rate"] > 0.6

    def test_report_rejects_a_card_missing_a_rate(self, tmp_path: Path) -> None:
        from infravce.bench.cli import main

        truncated = tmp_path / "trunc.json"
        truncated.write_text(
            json.dumps(
                {
                    "tool": "x",
                    "mode": "y",
                    "false_positives": 0,
                    "false_negatives": 0,
                    "wrong_verdicts": 0,
                    "classes": [],
                    "calibration": [],
                }
            )
        )
        assert main(["report", str(truncated)]) == 1

    def test_report_accepts_a_complete_card(self, tmp_path: Path, truth: GroundTruthSet) -> None:
        from infravce.bench.cli import _card_to_json, main

        card = score(truth, load_predictions(PRED_DIR / "naive-nvd-range.json"))
        good = tmp_path / "good.json"
        good.write_text(_card_to_json(card))
        assert main(["report", str(good)]) == 0

    def test_scores_and_reports_the_expected_gap(self, truth: GroundTruthSet, capsys) -> None:
        """The study's headline comparison, as a regression test.

        If this stops holding, either the harness changed or the fixtures drifted.
        Both need a human decision, so it is a failure either way.

        The gap is asserted as a relationship between the two tools rather than as
        absolute rates, because the rates move with the case mix while the finding
        does not: distribution-aware matching cuts false positives, and expressing
        unknowns cuts wrong verdicts.
        """
        naive = score(truth, load_predictions(PRED_DIR / "naive-nvd-range.json"))
        proto = score(truth, load_predictions(PRED_DIR / "infravce-prototype.json"))
        assert naive.false_positives > 0
        assert proto.false_positive_rate == 0.0
        assert proto.false_positive_rate < naive.false_positive_rate
        assert proto.unknown_handling_accuracy > naive.unknown_handling_accuracy
