"""CLI entry point.

Thin orchestration: wire existing modules. Logic belongs in modules.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from infravce import __version__
from infravce.advisories.ingest import ingest
from infravce.advisories.match import match_observations
from infravce.discovery import discover
from infravce.normalise.versions import detect_ecosystem, normalise_many
from infravce.reporting import (
    build_findings,
    build_queue,
    write_coverage,
    write_coverage_summary,
    write_findings,
    write_queue,
)
from infravce.verification import corroborate, safe_verify


def _cmd_version(_: argparse.Namespace) -> int:
    print(f"infravce {__version__}")
    return 0


def _cmd_normalise(args: argparse.Namespace) -> int:
    versions: list[str] = list(args.version)
    if args.file:
        versions.extend(
            line.strip() for line in Path(args.file).read_text().splitlines() if line.strip()
        )

    pairs = [(args.product, v) for v in versions]
    records = [v.model_dump(mode="json") for v in normalise_many(pairs)]

    payload = json.dumps(records, indent=2)
    if args.out:
        Path(args.out).write_text(payload + "\n")
        print(f"wrote {len(records)} record(s) to {args.out}", file=sys.stderr)
    else:
        print(payload)
    return 0


def _cmd_detect(args: argparse.Namespace) -> int:
    print(detect_ecosystem(args.product, args.version).value)
    return 0


def _cmd_discover(args: argparse.Namespace) -> int:
    srcs = []
    if args.source:
        srcs.extend(args.source)
    obs = discover(srcs)
    data = [o.model_dump(mode="json") for o in obs]
    payload = json.dumps(data, indent=2)
    if args.out:
        Path(args.out).write_text(payload + "\n")
        print(f"wrote {len(obs)} observation(s) to {args.out}", file=sys.stderr)
    else:
        print(payload)
    return 0


def _cmd_coverage(args: argparse.Namespace) -> int:
    res = ingest()
    out = Path(args.out) if args.out else Path("coverage.json")
    write_coverage(list(res.coverages), out)
    write_coverage_summary(list(res.coverages), Path("coverage-summary.md"))
    print(f"wrote {out} and coverage-summary.md", file=sys.stderr)
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    srcs = []
    if args.source:
        srcs.extend(args.source)
    obs = discover(srcs)
    res = ingest(getattr(args, "advisories", None))
    votes = match_observations(obs, list(res.records))
    corr = corroborate(obs, votes)
    ver = safe_verify(obs)
    findings = build_findings(obs, votes, corroborated=corr, verified=ver)
    outd = Path(args.outdir or ".")
    outd.mkdir(parents=True, exist_ok=True)
    write_findings(findings, outd / "findings.json")
    write_coverage(list(res.coverages), outd / "coverage.json")
    write_coverage_summary(list(res.coverages), outd / "coverage-summary.md")
    write_queue(findings, outd / "review-queue.json")
    print(f"wrote findings.json, coverage.json, coverage-summary.md, review-queue.json in {outd}", file=sys.stderr)
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    # minimal: if findings exist, regenerate queue/summary from them
    outd = Path(args.outdir or ".")
    findings_path = outd / "findings.json"
    if findings_path.exists():
        findings = [__import__("infravce.models", fromlist=[""]).Finding.model_validate(x) for x in json.loads(findings_path.read_text())]  # type: ignore
        write_queue(findings, outd / "review-queue.json")
        print("wrote review-queue.json", file=sys.stderr)
        return 0
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    srcs = []
    if args.source:
        srcs.extend(args.source)
    obs = discover(srcs)
    res = ingest()
    votes = match_observations(obs, list(res.records))
    _ = corroborate(obs, votes)
    _ = safe_verify(obs)
    print("verification done (minimal)", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="infravce", description="Infrastructure CVE checker.")
    p.add_argument("--version", action="version", version=f"infravce {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="print version").set_defaults(func=_cmd_version)

    n = sub.add_parser("normalise", help="decompose version strings")
    n.add_argument("version", nargs="*", help="version strings to normalise")
    n.add_argument("--file", help="read version strings from a file, one per line")
    n.add_argument("--product", default="", help="product name, used for ecosystem detection")
    n.add_argument("--out", help="write JSON here instead of stdout")
    n.set_defaults(func=_cmd_normalise)

    d = sub.add_parser("detect", help="detect the ecosystem of a product/version pair")
    d.add_argument("product")
    d.add_argument("version")
    d.set_defaults(func=_cmd_detect)

    disc = sub.add_parser("discover", help="discover observations from declared sources")
    disc.add_argument("source", nargs="*", help="files/dirs to scan")
    disc.add_argument("--out", help="write JSON here instead of stdout")
    disc.set_defaults(func=_cmd_discover)

    cov = sub.add_parser("coverage", help="show source coverage/freshness")
    cov.add_argument("--out", help="coverage.json path")
    cov.set_defaults(func=_cmd_coverage)

    scan = sub.add_parser("scan", help="run full minimal pipeline")
    scan.add_argument("source", nargs="*", help="files/dirs to scan")
    scan.add_argument("--outdir", help="output directory")
    scan.add_argument("--advisories", "--cache", dest="advisories", help="path to advisory/cache JSON")
    scan.set_defaults(func=_cmd_scan)

    rep = sub.add_parser("report", help="regenerate report artifacts from findings")
    rep.add_argument("--outdir", help="output directory")
    rep.set_defaults(func=_cmd_report)

    ver = sub.add_parser("verify", help="run minimal verification")
    ver.add_argument("source", nargs="*", help="files/dirs to scan")
    ver.set_defaults(func=_cmd_verify)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
