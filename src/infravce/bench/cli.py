"""CLI for the benchmark: ``infravce-bench``.

Subcommands
-----------
``score``   score a tool's output against the frozen ground truth
``baseline`` report which baseline tools are installed
``report``  render a markdown comparison from saved scorecards

Kept separate from ``infravce`` because scoring is the *measurement* side of the
project. A benchmark that shares a code path with the system under test invites
the ground truth to be tuned until it agrees with the system, which is threat 2.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .baselines import main as baselines_main
from .schema import load_ground_truth, load_predictions
from .scoring import Scorecard, format_table, score

DEFAULT_GT = Path("bench/infra-cve-bench/ground-truth/cases.json")


def _cmd_score(args: argparse.Namespace) -> int:
    truth = load_ground_truth(args.ground_truth)
    preds = load_predictions(args.predictions)
    card = score(truth, preds)

    for w in card.warnings:
        print(f"warning: {w}", file=sys.stderr)

    print(format_table(card.summary_rows()))
    print()
    print(format_table([dict(c.as_row()) for c in card.classes if c.is_scored]))
    if card.calibration:
        print()
        print(format_table([dict(t.as_row()) for t in card.calibration]))

    if card.errors:
        print()
        print(f"errors ({len(card.errors)}):")
        print(format_table([dict(e.as_row()) for e in card.errors]))

    if args.json_out:
        Path(args.json_out).write_text(_card_to_json(card) + "\n")
        print(f"\nwrote {args.json_out}", file=sys.stderr)

    return 0


def _card_to_json(card: Scorecard) -> str:
    """Serialise a scorecard, computed properties included.

    ``asdict`` only walks dataclass *fields*, so every ``@property`` - including
    ``false_positive_rate``, the study's headline number - is silently dropped.
    Reading a missing key back as 0.0 would render a tool with eight false
    positives as having a 0% false-positive rate, so the derived values are
    added explicitly and the report refuses to read a card missing them.
    """
    data: dict[str, Any] = asdict(card)
    data.update(
        false_positive_rate=card.false_positive_rate,
        false_negative_rate=card.false_negative_rate,
        unknown_handling_accuracy=card.unknown_handling_accuracy,
        provenance_completeness=card.provenance_completeness,
        calibration_monotonic=card.is_calibration_monotonic(),
    )
    return json.dumps(data, indent=2, default=str)


#: Keys a saved scorecard must carry for ``report`` to read it. Computed fields
#: are included because a card written before a metric existed is not comparable.
_REQUIRED_CARD_KEYS = (
    "tool",
    "mode",
    "false_positives",
    "false_negative_rate",
    "false_positive_rate",
    "wrong_verdicts",
    "unknown_handling_accuracy",
    "unmatched_assets",
    "classes",
)


def _load_cards(paths: list[Path]) -> list[dict[str, Any]]:
    """Load saved scorecards, refusing any that lack a required metric.

    A missing key is not the same as a zero, and this report exists to compare
    error rates. Reading an absent metric as ``0.0`` would let a truncated or
    older card look like a perfect result, so it is an error here instead.
    """
    cards: list[dict[str, Any]] = []
    for p in sorted(paths):
        card: dict[str, Any] = json.loads(p.read_text())
        missing = [k for k in _REQUIRED_CARD_KEYS if k not in card]
        if missing:
            raise ValueError(
                f"{p}: scorecard is missing {missing}. Re-run `score` with "
                "--json-out rather than editing the file by hand."
            )
        cards.append(card)
    return cards


def _cmd_report(args: argparse.Namespace) -> int:
    try:
        cards = _load_cards(args.scorecards)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not cards:
        print("no scorecards to compare", file=sys.stderr)
        return 1

    rows = []
    for c in cards:
        rows.append(
            {
                "tool": c["tool"],
                "mode": c["mode"],
                "FP rate": round(float(c["false_positive_rate"]), 4),
                "FP": c["false_positives"],
                "FN rate": round(float(c["false_negative_rate"]), 4),
                "FN": c["false_negatives"],
                "wrong verdict": c["wrong_verdicts"],
                "unknown handling": round(float(c["unknown_handling_accuracy"]), 4),
                "unmatched assets": c["unmatched_assets"],
            }
        )

    print("# INFRA-CVE-Bench results\n")
    print(
        "False-positive and false-negative rates are reported separately. "
        "No combined score is given: a single number would let a recall gain "
        "conceal a high FP rate.\n"
    )
    print(format_table(rows))

    print("\n## Per case class\n")
    class_rows: list[dict[str, Any]] = []
    for c in cards:
        for cls in c.get("classes") or []:
            if not cls.get("total"):
                continue
            class_rows.append(
                {
                    "tool": c["tool"],
                    "case_class": cls["case_class"],
                    "total": cls["total"],
                    "correct": cls["correct"],
                    "FP": cls["false_positives"],
                    "FN": cls["false_negatives"],
                    "wrong verdict": cls["wrong_verdicts"],
                }
            )
    print(format_table(class_rows))

    print("\n## Confidence tier calibration\n")
    cal_rows: list[dict[str, Any]] = []
    for c in cards:
        for t in c.get("calibration") or []:
            cal_rows.append(
                {
                    "tool": c.get("tool"),
                    "tier": t.get("tier"),
                    "claimed": t.get("claimed"),
                    "observed precision": t.get("observed_precision"),
                }
            )
    print(format_table(cal_rows) if cal_rows else "(no tiers claimed)")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    """Load and validate ground truth without scoring anything.

    Useful as a pre-commit gate: if the frozen labels no longer satisfy their
    own invariants, that must fail loudly before a run is recorded against them.
    """
    truth = load_ground_truth(args.ground_truth)
    classes: dict[str, int] = {}
    for c in truth.cases:
        classes[c.case_class.value] = classes.get(c.case_class.value, 0) + 1
    print(f"ground truth {truth.version} @ {truth.snapshot_date}: {len(truth.cases)} cases")
    for k in sorted(classes):
        print(f"  {k:<24} {classes[k]}")
    affected = sum(1 for c in truth.cases if c.is_affected_truth)
    print(f"\naffected truth cases: {affected}")
    if args.expect_affected is not None and affected != args.expect_affected:
        print(
            f"\nwarning: expected {args.expect_affected} affected cases, found {affected}",
            file=sys.stderr,
        )
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="infravce-bench", description="INFRA-CVE-Bench scoring")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("score", help="score one tool's output")
    s.add_argument("predictions", type=Path)
    s.add_argument("--ground-truth", type=Path, default=DEFAULT_GT)
    s.add_argument("--json-out", help="write the scorecard as JSON")
    s.set_defaults(func=_cmd_score)

    b = sub.add_parser("baseline", help="report baseline tool availability")
    b.add_argument("--json", action="store_true")
    b.set_defaults(func=_cmd_baseline)

    v = sub.add_parser("validate", help="validate ground truth invariants")
    v.add_argument("--ground-truth", type=Path, default=DEFAULT_GT)
    v.add_argument("--expect-affected", type=int, default=None)
    v.set_defaults(func=_cmd_validate)

    r = sub.add_parser("report", help="render a comparison from saved scorecards")
    r.add_argument("scorecards", nargs="+", type=Path)
    r.set_defaults(func=_cmd_report)

    return p


def _cmd_baseline(args: argparse.Namespace) -> int:
    argv = ["--json"] if args.json else []
    return baselines_main(argv)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
