"""Human-readable scan report.

The JSON artifacts are the machine interface; this is what a reviewer reads
first. It is deliberately explicit about three things a CVE report usually
leaves implicit:

* which assets were *not* identified (so "no findings" cannot be mistaken for
  "nothing there"),
* which advisory sources were actually contacted and how old the data is,
* why each finding has the confidence tier it has.

That last point is the project's thesis, so the report prints the winning
source, the comparison that was performed, and whether the version was
independently confirmed.
"""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from infravce.models import Finding, Observation, ScanCoverage

__all__ = ["render_markdown", "write_markdown"]


def _counts(findings: list[Finding]) -> Counter[str]:
    return Counter(f.confidence_tier.value for f in findings)


def render_markdown(
    findings: list[Finding],
    observations: list[Observation],
    coverages: list[ScanCoverage],
    *,
    target: str | None = None,
    os_family: str | None = None,
    mode: str = "live",
) -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    counts = _counts(findings)
    identified = {o.asset_id for o in observations}
    usable_count = sum(1 for o in observations if o.resolved_version is not None)

    lines = [
        "# INFRA-CVE scan report",
        "",
        f"- **Target:** `{target or 'declared inventory'}`",
        f"- **Generated:** {now}",
        f"- **Advisory mode:** {mode}",
        f"- **Distance hint:** {os_family or 'none'}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Assets observed | {len(identified)} |",
        f"| Observations recorded | {len(observations)} |",
        f"| Observations with a usable version | {usable_count} |",
        f"| Findings (affected claims) | {len(findings)} |",
        f"| … with a published fix | {sum(1 for f in findings if f.fix_available)} |",
        f"| … with no published fix | {sum(1 for f in findings if f.fix_available is False)} |",
        f"| VERIFIED | {counts.get('verified', 0)} |",
        f"| STRONGLY_INFERRED | {counts.get('strongly_inferred', 0)} |",
        f"| INFERRED | {counts.get('inferred', 0)} |",
        f"| WEAK | {counts.get('weak', 0)} |",
        "",
        "## Findings",
        "",
    ]

    if not findings:
        lines += [
            "_No affected claims were produced._ An empty result here means the "
            "advisory sources were queried and returned no range containing the "
            "observed versions — check the coverage table below before reading it "
            "as 'safe'.",
            "",
        ]
    else:
        lines += [
            "| Asset | Advisory | Severity | Fix | Tier | Score | Basis |",
            "|---|---|---|---|---|---|---|",
        ]
        for finding in findings:
            severity = (
                finding.severity
                or (f"CVSS {finding.cvss}" if finding.cvss else "unknown")
            )
            fix = (
                "published"
                if finding.fix_available
                else ("none" if finding.fix_available is False else "unknown")
            )
            basis = finding.evidence_bundle.get("winning_evidence", "")
            lines.append(
                f"| `{finding.asset_id}` | {finding.cve_id} | {severity} | {fix} | "
                f"**{finding.confidence_tier.value}** | {finding.priority_score or 0:.1f} | "
                f"{_escape(str(basis))[:160]} |"
            )
        lines.append("")

        lines += ["## Finding detail", ""]
        for finding in findings:
            bundle = finding.evidence_bundle
            fix_text = (
                "yes"
                if finding.fix_available
                else ("no" if finding.fix_available is False else "unknown")
            )
            lines += [
                f"### {finding.cve_id} on `{finding.asset_id}`",
                "",
                f"- **Tier:** {finding.confidence_tier.value}",
                f"- **Priority:** {finding.priority_score or 0:.1f} / 100",
                f"- **Fix published:** {fix_text}",
                f"- **Winning source:** {bundle.get('winning_source', 'unknown')}",
                f"- **Sources consulted:** {', '.join(bundle.get('sources', [])) or 'none'}",
                f"- **Version independently confirmed:** "
                f"{'yes' if bundle.get('version_verified') else 'no'}",
                f"- **Second source agrees:** "
                f"{'yes' if bundle.get('source_corroborated') else 'no'}",
                f"- **Evidence:** {bundle.get('winning_evidence', '')}",
            ]
            if finding.summary:
                lines.append(f"- **Advisory summary:** {_escape(finding.summary)}")
            if finding.notes:
                lines.append(f"- **Notes:** {'; '.join(finding.notes)}")
            raw_observations = bundle.get("observations") or []
            for obs in raw_observations:
                lines.append(
                    f"- **Observed as:** `{obs.get('raw_product')}` "
                    f"`{obs.get('raw_version') or '(no version)'}` via "
                    f"{obs.get('method')} (confidence {obs.get('resolution_confidence')})"
                )
            lines.append("")

    lines += ["## Advisory coverage and freshness", ""]
    if not coverages:
        lines.append("_No advisory source was contacted._")
    else:
        lines += [
            "| Source | Ecosystem | Records | Last successful ingest | Gaps |",
            "|---|---|---|---|---|",
        ]
        for coverage in coverages:
            when = (
                coverage.last_successful_ingest.astimezone(UTC).strftime("%Y-%m-%d %H:%M")
                if coverage.last_successful_ingest
                else "**NEVER INGESTED**"
            )
            gaps = "; ".join(coverage.known_gaps) or "—"
            lines.append(
                f"| {coverage.source.value} | {coverage.ecosystem.value} | "
                f"{coverage.record_count} | {when} | {_escape(gaps)[:120]} |"
            )
    lines += [
        "",
        "## What was not checked",
        "",
        "- Services whose banner published no version cannot be range-matched; "
        "they are listed in the observations JSON with an empty `raw_version`.",
        "- CVSS severity is a *priority* input. It never decides applicability.",
        "- A banner-derived version is a hypothesis. Findings resting only on a "
        "banner are capped below `VERIFIED` by construction.",
        "",
    ]
    return "\n".join(lines)


def _escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_markdown(
    findings: list[Finding],
    observations: list[Observation],
    coverages: list[ScanCoverage],
    out: Path,
    *,
    target: str | None = None,
    os_family: str | None = None,
    mode: str = "live",
) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        render_markdown(
            findings,
            observations,
            coverages,
            target=target,
            os_family=os_family,
            mode=mode,
        )
        + "\n"
    )
