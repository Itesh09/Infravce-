"""CLI entry point.

Thin orchestration: wire existing modules. Logic belongs in modules.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from infravce import __version__
from infravce.advisories.ingest import AdvisoryRecord, IngestResult, ingest, ingest_inventory, ingest_observed
from infravce.advisories.match import match_observations
from infravce.discovery import discover, parse_target, read_host_inventory, scan_target
from infravce.discovery.network import OS_FAMILIES
from infravce.models import AcquisitionMethod, Observation, ScanCoverage
from infravce.normalise.versions import detect_ecosystem, normalise_many
from infravce.reporting import (
    build_findings,
    build_queue,
    write_coverage,
    write_coverage_summary,
    write_findings,
    write_markdown,
    write_queue,
)
from infravce.verification import corroborate, safe_verify

_ARTIFACTS = (
    "observations.json",
    "votes.json",
    "findings.json",
    "coverage.json",
    "coverage-summary.md",
    "review-queue.json",
    "report.md",
)


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


def _parse_ports(value: str | None) -> tuple[int, ...] | None:
    if not value:
        return None
    return tuple(int(p.strip()) for p in value.split(",") if p.strip())


def _collect(args: argparse.Namespace) -> tuple[list[Observation], str | None, str | None]:
    """Gather observations from a network target, host inventory and/or files.

    Returns ``(observations, os_release, target_description)``. An unauthorised
    target is a hard error rather than an empty scan, so a demo cannot silently
    report "no findings" because the guard refused.
    """
    observations = []
    os_release: str | None = None
    target_description: str | None = None

    if getattr(args, "target", None):
        target = parse_target(args.target, _parse_ports(getattr(args, "ports", None)))
        authorised = bool(getattr(args, "authorised", False))
        allowlist = tuple(getattr(args, "allow", None) or ())
        if not authorised:
            print(
                "refusing to probe: pass --authorised to confirm you own or are "
                "permitted to test this target (docs/06-ethics-and-scope.md)",
                file=sys.stderr,
            )
            raise SystemExit(2)
        observations_net, _ecosystem, os_release, _target = scan_target(
            args.target,
            authorised=authorised,
            allowlist=allowlist,
            ports=target.ports,
            os_family=getattr(args, "os", None) or "debian:12",
        )
        observations.extend(observations_net)
        target_description = args.target

    inventory = list(getattr(args, "inventory", None) or ())
    if inventory:
        auto = [value for value in inventory if value.lower() in {"auto", "host", "detect"}]
        paths = [value for value in inventory if value.lower() not in {"auto", "host", "detect"}]
        observations_inv, _ecosystem, release, host, gaps = read_host_inventory(
            paths or None
        )
        observations.extend(observations_inv)
        # An explicit --os is the caller stating the release; detection only
        # fills the gap when they did not. Reading a saved Debian status file on
        # a Kali analysis box must not turn into "Debian:2026.3".
        hint = OS_FAMILIES.get((getattr(args, "os", None) or "").lower())
        os_release = (hint[1] if hint and hint[1] else None) or os_release or release
        target_description = target_description or f"host inventory ({host})"
        for gap in gaps:
            print(f"inventory gap: {gap}", file=sys.stderr)
        if auto and not paths:
            print(
                f"host inventory: {len(observations_inv)} package(s) from {host}",
                file=sys.stderr,
            )

    if getattr(args, "source", None):
        observations.extend(discover(args.source))
        target_description = target_description or ", ".join(args.source)

    return observations, os_release, target_description


def _ingest_scan(
    observations: list[Observation],
    args: argparse.Namespace,
    os_release: str | None,
) -> IngestResult:
    """Route exact inventory through the batch endpoint and the rest through
    per-package queries, then merge the records.

    A host scan produces both kinds of observation at once (a package database
    and a service banner). Runnning them through one path would either waste a
    full package query per installed package or lose the exact version that
    makes the inventory worth reading.
    """
    exact = [
        o
        for o in observations
        if o.acquisition_method is AcquisitionMethod.PACKAGE_DB and o.raw_version
    ]
    exact_ids = {o.observation_id for o in exact}
    rest = [o for o in observations if o.observation_id not in exact_ids]

    results: list[IngestResult] = []
    if rest:
        results.append(
            ingest_observed(
                rest,
                os_release=os_release,
                cache_dir=args.cache_dir,
                allow_network=not args.offline,
                local_advisories=args.advisories,
            )
        )
    if exact:
        results.append(
            ingest_inventory(
                exact,
                os_release=os_release,
                cache_dir=args.cache_dir,
                allow_network=not args.offline,
                local_advisories=args.advisories,
            )
        )
    if not results:
        return ingest_observed(
            [],
            os_release=os_release,
            cache_dir=args.cache_dir,
            allow_network=not args.offline,
            local_advisories=args.advisories,
        )

    records: dict[tuple[str, str, str], AdvisoryRecord] = {}
    coverages: list[ScanCoverage] = []
    for result in results:
        for record in result.records:
            key = (record.advisory_id, record.product, record.ecosystem.value)
            existing = records.get(key)
            if existing is None or len(record.affected_ranges) > len(existing.affected_ranges):
                records[key] = record
        coverages.extend(result.coverages)
    return IngestResult(tuple(records.values()), tuple(coverages))


def _cmd_discover(args: argparse.Namespace) -> int:
    observations, _release, _target = _collect(args)
    data = [o.model_dump(mode="json") for o in observations]
    payload = json.dumps(data, indent=2)
    if args.out:
        Path(args.out).write_text(payload + "\n")
        print(f"wrote {len(observations)} observation(s) to {args.out}", file=sys.stderr)
    else:
        print(payload)
    return 0


def _cmd_coverage(args: argparse.Namespace) -> int:
    res = ingest(args.advisories)
    out = Path(args.out) if args.out else Path("coverage.json")
    write_coverage(list(res.coverages), out)
    write_coverage_summary(list(res.coverages), Path("coverage-summary.md"))
    print(f"wrote {out} and coverage-summary.md", file=sys.stderr)
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    observations, os_release, target_description = _collect(args)
    if not observations:
        print("no observations: nothing to match against advisories", file=sys.stderr)

    res = _ingest_scan(observations, args, os_release)
    votes = match_observations(observations, list(res.records))
    corroborated = corroborate(observations, votes)
    verified = safe_verify(observations)
    findings = build_findings(
        observations, votes, corroborated=corroborated, verified=verified
    )
    if getattr(args, "fixed_only", False):
        findings = [finding for finding in findings if finding.fix_available]

    outdir = Path(args.outdir or "out")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "observations.json").write_text(
        json.dumps([o.model_dump(mode="json") for o in observations], indent=2) + "\n"
    )
    (outdir / "votes.json").write_text(
        json.dumps([v.model_dump(mode="json") for v in votes], indent=2) + "\n"
    )
    write_findings(findings, outdir / "findings.json")
    write_coverage(list(res.coverages), outdir / "coverage.json")
    write_coverage_summary(list(res.coverages), outdir / "coverage-summary.md")
    write_queue(findings, outdir / "review-queue.json")
    write_markdown(
        findings,
        observations,
        list(res.coverages),
        outdir / "report.md",
        target=target_description,
        os_family=args.os or (f"host {os_release}" if os_release else None),
        mode="offline (cache only)" if args.offline else "live OSV",
    )

    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.confidence_tier.value] = counts.get(finding.confidence_tier.value, 0) + 1
    tier_text = ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none"
    print(
        f"{len(observations)} observation(s), {len(res.records)} advisory record(s), "
        f"{len(votes)} vote(s), {len(findings)} finding(s) [{tier_text}]",
        file=sys.stderr,
    )
    print(f"wrote {', '.join(_ARTIFACTS)} in {outdir}", file=sys.stderr)
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    outdir = Path(args.outdir or "out")
    findings_path = outdir / "findings.json"
    if not findings_path.exists():
        print(f"no findings at {findings_path}", file=sys.stderr)
        return 1
    from infravce.models import Finding

    findings = [Finding.model_validate(item) for item in json.loads(findings_path.read_text())]
    write_queue(findings, outdir / "review-queue.json")
    print("wrote review-queue.json", file=sys.stderr)
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    observations, _release, _target = _collect(args)
    verified = safe_verify(observations)
    confirmed = sum(1 for value in verified.values() if value)
    print(
        f"{confirmed}/{len(observations)} observation(s) have an independently "
        "confirmed version",
        file=sys.stderr,
    )
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

    disc = sub.add_parser("discover", help="discover observations from targets or declared sources")
    disc.add_argument("source", nargs="*", help="files/dirs to scan")
    disc.add_argument("--target", help="host or host:port[,port] to probe (requires --authorised)")
    disc.add_argument("--ports", help="comma-separated ports to probe")
    disc.add_argument("--os", default=None, choices=sorted(OS_FAMILIES), help="target distribution hint (default: debian:12)")
    disc.add_argument("--inventory", action="append", help="read the local package database, or 'auto' to detect; repeatable")
    disc.add_argument("--authorised", action="store_true", help="confirm authorisation to probe the target")
    disc.add_argument("--allow", action="append", help="additional allowlisted host/CIDR")
    disc.add_argument("--out", help="write JSON here instead of stdout")
    disc.set_defaults(func=_cmd_discover)

    cov = sub.add_parser("coverage", help="show source coverage/freshness")
    cov.add_argument("--advisories", "--cache", dest="advisories", help="path to advisory/cache JSON")
    cov.add_argument("--out", help="coverage.json path")
    cov.set_defaults(func=_cmd_coverage)

    scan = sub.add_parser("scan", help="discover and check a target or declared inventory")
    scan.add_argument("source", nargs="*", help="files/dirs to scan")
    scan.add_argument("--target", help="host or host:port[,port] to probe (requires --authorised)")
    scan.add_argument("--ports", help="comma-separated ports to probe")
    scan.add_argument("--os", default=None, choices=sorted(OS_FAMILIES), help="distribution hint (default: debian:12; inferred when --inventory detects the host)")
    scan.add_argument("--inventory", action="append", help="read the local package database, or 'auto' to detect; repeatable")
    scan.add_argument("--authorised", action="store_true", help="confirm authorisation to probe the target")
    scan.add_argument("--allow", action="append", help="additional allowlisted host/CIDR")
    scan.add_argument("--outdir", default="out", help="output directory")
    scan.add_argument("--advisories", "--cache", dest="advisories", help="path to advisory cache JSON")
    scan.add_argument("--cache-dir", default=".infravce-cache/osv", help="OSV response cache directory")
    scan.add_argument("--offline", action="store_true", help="use only cached advisories; no network")
    scan.add_argument("--fixed-only", action="store_true", help="only report findings with a published fix")
    scan.set_defaults(func=_cmd_scan)

    rep = sub.add_parser("report", help="regenerate report artifacts from findings")
    rep.add_argument("--outdir", default="out")
    rep.set_defaults(func=_cmd_report)

    ver = sub.add_parser("verify", help="report which observations have confirmed versions")
    ver.add_argument("source", nargs="*", help="files/dirs to scan")
    ver.add_argument("--target", help="host or host:port[,port] to probe (requires --authorised)")
    ver.add_argument("--ports", help="comma-separated ports to probe")
    ver.add_argument("--os", default=None, choices=sorted(OS_FAMILIES))
    ver.add_argument("--inventory", action="append", help="read the local package database, or 'auto' to detect")
    ver.add_argument("--authorised", action="store_true")
    ver.add_argument("--allow", action="append")
    ver.set_defaults(func=_cmd_verify)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
