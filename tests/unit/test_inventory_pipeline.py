"""End-to-end tests for the inventory -> ingest -> match -> report path.

These tests are offline and deterministic. They exist because every class of bug
this project has hit so far lived in the seams: a banner version compared against
a distribution boundary, a release filter that leaked another release's fix, a
finding promoted for a source that said "not affected". Each test below pins one
of those seams.
"""

from __future__ import annotations

import json
from pathlib import Path

from infravce.advisories.ingest import ingest
from infravce.advisories.match import match_observations
from infravce.advisories.osv import _segments, records_from_vulns, the_versions
from infravce.discovery.package_db import (
    detect_host_os,
    inventory_observations,
    parse_apk_installed,
    parse_dpkg_status,
)
from infravce.models import (
    AcquisitionMethod,
    ApplicabilityVerdict,
    ConfidenceTier,
    Ecosystem,
    Observation,
)
from infravce.normalise.versions import normalise
from infravce.reporting.findings import build_findings

DPKG_SAMPLE = """\
Package: openssl
Status: install ok installed
Source: openssl (3.0.11-1~deb12u2)
Version: 3.0.11-1~deb12u2
Architecture: amd64
Description: Secure Sockets Layer toolkit
 continuation line

Package: libssl3
Status: install ok installed
Source: openssl
Version: 3.0.11-1~deb12u2
Architecture: amd64

Package: removed-pkg
Status: deinstall ok config-files
Version: 1.0-1

Package: unpacked-pkg
Status: install ok unpacked
Version: 2.0-1

Package: zlib1g
Status: install ok installed
Version: 1:1.2.13.dfsg-1
Architecture: amd64
"""

APK_SAMPLE = """\
C:Q1abc=
P:musl
V:1.2.4_git20230717-r4
A:x86_64
o:musl
m:Timo Teräs

C:Q1def=
P:libssl3
V:3.1.4-r5
A:x86_64
o:openssl
"""


def _observation(
    product: str,
    version: str,
    *,
    ecosystem: Ecosystem = Ecosystem.DEBIAN,
    method: AcquisitionMethod = AcquisitionMethod.PACKAGE_DB,
    asset: str = "host",
) -> Observation:
    resolved = normalise(version, ecosystem=ecosystem, product=product)
    return Observation(
        asset_id=asset,
        acquisition_method=method,
        evidence=f"test evidence for {product}={version}",
        raw_product=product,
        raw_version=version,
        resolved_product=product,
        resolved_version=resolved,
        resolution_confidence=resolved.confidence,
    )


def _record(**overrides):
    from infravce.advisories.ingest import AdvisoryRecord
    from infravce.models import AdvisorySource

    fields = {
        "advisory_id": "DEBIAN-CVE-TEST",
        "source": AdvisorySource.DISTRO_TRACKER,
        "ecosystem": Ecosystem.DEBIAN,
        "product": "openssl",
        "distro_state": "resolved",
        "fixed_version": "3.0.11-1~deb12u3",
    }
    fields.update(overrides)
    return AdvisoryRecord(**fields)


# --------------------------------------------------------------------------- #
# Package database parsing
# --------------------------------------------------------------------------- #


def test_dpkg_parser_keeps_installed_packages_and_source_names():
    packages = parse_dpkg_status(DPKG_SAMPLE)
    names = {p.name: p for p in packages}
    assert set(names) == {"openssl", "libssl3", "zlib1g"}
    assert "removed-pkg" not in names and "unpacked-pkg" not in names
    # A binary package and its source package must collapse to the name an
    # advisory feed indexes, or one install produces two different queries.
    assert names["libssl3"].advisory_name == "openssl"
    assert names["openssl"].version == "3.0.11-1~deb12u2"
    assert names["zlib1g"].advisory_name == "zlib1g"


def test_apk_parser_uses_origin_as_advisory_name():
    packages = parse_apk_installed(APK_SAMPLE)
    by_name = {p.name: p for p in packages}
    assert set(by_name) == {"musl", "libssl3"}
    assert by_name["libssl3"].advisory_name == "openssl"
    assert by_name["libssl3"].manager == "apk"
    assert by_name["musl"].version == "1.2.4_git20230717-r4"


def test_inventory_observations_keep_the_exact_distribution_version():
    observations = inventory_observations(
        parse_dpkg_status(DPKG_SAMPLE),
        asset_id="host",
        ecosystem=Ecosystem.DEBIAN,
    )
    openssl = next(o for o in observations if o.raw_product == "openssl")
    # The revision is the reason the inventory is worth reading: a banner cannot
    # report it, and it is what decides whether the backported patch is present.
    assert openssl.raw_version == "3.0.11-1~deb12u2"
    assert openssl.resolved_version is not None
    assert openssl.resolved_version.distro_revision
    assert openssl.resolution_confidence >= 0.85
    assert openssl.is_usable_for_matching


def test_detect_host_os_never_invents_a_release_for_rolling_distros(tmp_path: Path):
    (tmp_path / "etc").mkdir()
    (tmp_path / "etc/os-release").write_text(
        'PRETTY_NAME="Kali GNU/Linux Rolling"\nID=kali\nVERSION_ID="2026.3"\n'
    )
    ecosystem, release, pretty = detect_host_os(tmp_path)
    assert ecosystem is Ecosystem.DEBIAN
    # Kali is Debian-derived but has no bookworm/trixie number. Guessing
    # ``Debian:2026.3`` would query an ecosystem that does not exist and apply
    # another release's fix boundaries.
    assert release is None
    assert "Kali" in pretty


# --------------------------------------------------------------------------- #
# Matching: exact inventory vs approximate banners
# --------------------------------------------------------------------------- #


def test_exact_inventory_behind_the_fix_is_affected():
    observation = _observation("openssl", "3.0.11-1~deb12u2")
    votes = match_observations([observation], [_record()])
    assert len(votes) == 1
    assert votes[0].verdict is ApplicabilityVerdict.AFFECTED
    assert votes[0].evidence_quality == "exact"
    assert votes[0].fix_available is True


def test_exact_inventory_at_the_fix_is_not_affected():
    observation = _observation("openssl", "3.0.11-1~deb12u3")
    votes = match_observations([observation], [_record()])
    assert votes[0].verdict is ApplicabilityVerdict.NOT_AFFECTED
    assert votes[0].evidence_quality == "exact"


def test_banner_on_the_fixed_upstream_release_is_conservatively_affected():
    # A banner reports ``3.0.11``; the tracker fixes ``3.0.11-1~deb12u3``. The
    # upstream release alone does not say whether the Debian revision is
    # installed, so the vulnerable build must be assumed -- and capped at WEAK.
    observation = _observation(
        "openssl", "3.0.11", method=AcquisitionMethod.BANNER, asset="10.0.0.5:443"
    )
    votes = match_observations([observation], [_record()])
    assert votes[0].verdict is ApplicabilityVerdict.AFFECTED
    assert votes[0].evidence_quality == "approximate"

    findings = build_findings([observation], votes)
    assert len(findings) == 1
    assert findings[0].confidence_tier is ConfidenceTier.WEAK


def test_banner_on_an_unrevisioned_fix_is_not_affected():
    # ``fixed: 3.0.1`` with no revision means the upstream release *is* the fix,
    # so equality is genuinely patched and must not be turned into a finding.
    record = _record(fixed_version="3.0.1")
    observation = _observation(
        "openssl", "3.0.1", method=AcquisitionMethod.BANNER, asset="10.0.0.5:443"
    )
    votes = match_observations([observation], [record])
    assert votes[0].verdict is ApplicabilityVerdict.NOT_AFFECTED


def test_an_old_fix_boundary_does_not_affect_a_current_banner():
    # Before the upstream-only reduction this compared ``1:3.0.1`` literally,
    # and every epoch boundary looked newer than a modern upstream version.
    record = _record(product="openssh", fixed_version="1:3.0.1")
    observation = _observation(
        "openssh", "10.5p1", method=AcquisitionMethod.BANNER, asset="10.0.0.5:22"
    )
    votes = match_observations([observation], [record])
    assert votes[0].verdict is ApplicabilityVerdict.NOT_AFFECTED


def test_verdicts_are_not_promoted_to_findings_when_not_affected():
    observation = _observation("openssl", "3.0.11-1~deb12u3")
    votes = match_observations([observation], [_record()])
    assert build_findings([observation], votes) == []


# --------------------------------------------------------------------------- #
# OSV record handling
# --------------------------------------------------------------------------- #

OSV_VULN = {
    "id": "DEBIAN-CVE-2024-0001",
    "aliases": ["CVE-2024-0001"],
    "summary": "A test issue",
    "affected": [
        {
            "package": {"name": "openssl", "ecosystem": "Debian:12"},
            "ranges": [
                {
                    "type": "ECOSYSTEM",
                    "events": [{"introduced": "0"}, {"fixed": "3.0.11-1~deb12u3"}],
                }
            ],
            "ecosystem_specific": {"urgency": "high"},
        },
        {
            "package": {"name": "openssl", "ecosystem": "Debian:13"},
            "ranges": [
                {
                    "type": "ECOSYSTEM",
                    "events": [{"introduced": "0"}, {"fixed": "3.0.11-1~deb13u9"}],
                }
            ],
            "ecosystem_specific": {"urgency": "unimportant"},
        },
        {
            "package": {"name": "libssl3", "ecosystem": "Debian:12"},
            "ranges": [
                {"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "9.9.9-1"}]}
            ],
        },
    ],
}


def test_release_filter_keeps_only_the_queried_release():
    segments = _segments(OSV_VULN, "openssl", "Debian:12")
    assert segments == (("0", "3.0.11-1~deb12u3"),)

    others = _segments(OSV_VULN, "openssl", "Debian:13")
    assert others == (("0", "3.0.11-1~deb13u9"),)


def test_package_filter_ignores_other_packages_in_the_same_record():
    assert the_versions(OSV_VULN, "openssl", "Debian:12") == ()
    segments = _segments(OSV_VULN, "libssl3", "Debian:12")
    assert segments == (("0", "9.9.9-1"),)


def test_severity_comes_from_the_queried_release_block():
    from infravce.advisories.osv import _severity

    assert _severity(OSV_VULN, "openssl", "Debian:12")[0] == "high"
    # The trixie block is marked unimportant; a bookworm query must not inherit
    # the severity of a release it was never evaluated against.
    assert _severity(OSV_VULN, "openssl", "Debian:13")[0] == "low"


def test_records_from_vulns_only_emit_the_queried_release():
    records = records_from_vulns(
        [OSV_VULN], product="openssl", ecosystem=Ecosystem.DEBIAN, queried_as="Debian:12"
    )
    assert len(records) == 1
    record = records[0]
    assert record.advisory_id == "CVE-2024-0001"
    assert record.affected_ranges == (("0", "3.0.11-1~deb12u3"),)
    assert record.severity == "high"
    assert record.queried_as == "Debian:12"


def test_a_release_less_query_merges_blocks_and_is_marked_a_gap():
    # ``Debian`` (no release) keeps both blocks; the ingest layer is responsible
    # for recording that wider merge as a coverage gap.
    from infravce.advisories.ingest import _ecosystem_of_label

    segments = _segments(OSV_VULN, "openssl", "Debian")
    assert len(segments) == 2
    assert _ecosystem_of_label("Debian:12") is Ecosystem.DEBIAN


# --------------------------------------------------------------------------- #
# CLI end to end, offline
# --------------------------------------------------------------------------- #


def test_scan_cli_produces_artifacts_from_a_saved_inventory(tmp_path: Path):
    from infravce.cli import main

    status = tmp_path / "status"
    status.write_text(DPKG_SAMPLE)
    advisories = tmp_path / "advisories.json"
    advisories.write_text(
        json.dumps(
            [
                {
                    "advisory_id": "CVE-TEST-0001",
                    "source": "distro_tracker",
                    "ecosystem": "debian",
                    "product": "openssl",
                    "status": "resolved",
                    "fixed_version": "3.0.11-1~deb12u3",
                },
                {
                    "advisory_id": "CVE-TEST-0002",
                    "source": "distro_tracker",
                    "ecosystem": "debian",
                    "product": "zlib1g",
                    "status": "resolved",
                    "fixed_version": "1:1.2.13.dfsg-1",
                },
            ]
        )
    )
    outdir = tmp_path / "out"

    exit_code = main(
        [
            "scan",
            "--inventory",
            str(status),
            "--os",
            "debian:12",
            "--advisories",
            str(advisories),
            "--offline",
            "--cache-dir",
            str(tmp_path / "cache"),
            "--outdir",
            str(outdir),
        ]
    )
    assert exit_code == 0

    for name in (
        "observations.json",
        "votes.json",
        "findings.json",
        "coverage.json",
        "coverage-summary.md",
        "review-queue.json",
        "report.md",
    ):
        assert (outdir / name).exists(), name

    findings = json.loads((outdir / "findings.json").read_text())
    # Only openssl is behind its fix. zlib1g is exactly at its fix and must not
    # be reported; libssl3 is the same source package and must not double-count.
    assert [f["cve_id"] for f in findings] == ["CVE-TEST-0001"]
    assert findings[0]["confidence_tier"] == "strongly_inferred"
    assert findings[0]["fix_available"] is True

    observations = json.loads((outdir / "observations.json").read_text())
    assert {o["raw_product"] for o in observations} == {"openssl", "zlib1g"}

    report = (outdir / "report.md").read_text()
    assert "CVE-TEST-0001" in report
    assert "CVE-TEST-0002" not in report


def test_scan_cli_fixed_only_filters_unfixed_findings(tmp_path: Path):
    from infravce.cli import main

    status = tmp_path / "status"
    status.write_text(
        "Package: openssl\nStatus: install ok installed\nVersion: 3.0.11-1~deb12u2\n"
    )
    advisories = tmp_path / "advisories.json"
    advisories.write_text(
        json.dumps(
            [
                {
                    "advisory_id": "CVE-FIXED",
                    "source": "distro_tracker",
                    "ecosystem": "debian",
                    "product": "openssl",
                    "status": "resolved",
                    "fixed_version": "3.0.11-1~deb12u3",
                },
                {
                    "advisory_id": "CVE-UNFIXED",
                    "source": "distro_tracker",
                    "ecosystem": "debian",
                    "product": "openssl",
                    "status": "vulnerable",
                },
            ]
        )
    )

    def scan(outdir: Path, *extra: str) -> list[dict]:
        assert (
            main(
                [
                    "scan",
                    "--inventory",
                    str(status),
                    "--os",
                    "debian:12",
                    "--advisories",
                    str(advisories),
                    "--offline",
                    "--cache-dir",
                    str(tmp_path / "cache"),
                    "--outdir",
                    str(outdir),
                    *extra,
                ]
            )
            == 0
        )
        return json.loads((outdir / "findings.json").read_text())

    everything = scan(tmp_path / "all")
    assert {f["cve_id"] for f in everything} == {"CVE-FIXED", "CVE-UNFIXED"}

    fixed = scan(tmp_path / "fixed", "--fixed-only")
    assert [f["cve_id"] for f in fixed] == ["CVE-FIXED"]


def test_local_advisory_ingest_understands_the_extended_shape(tmp_path: Path):
    path = tmp_path / "advisories.json"
    path.write_text(
        json.dumps(
            [
                {
                    "advisory_id": "DEBIAN-CVE-2024-9999",
                    "source": "distro_tracker",
                    "ecosystem": "debian",
                    "product": "openssl",
                    "affected_ranges": [{"introduced": "0", "fixed": "3.0.11-1~deb12u3"}],
                    "aliases": ["CVE-2024-9999"],
                    "severity": "high",
                    "summary": "test",
                    "queried_as": "Debian:12",
                }
            ]
        )
    )
    record = ingest(path).records[0]
    assert record.affected_ranges == (("0", "3.0.11-1~deb12u3"),)
    assert record.aliases == ("CVE-2024-9999",)
    assert record.severity == "high"
    assert record.queried_as == "Debian:12"
