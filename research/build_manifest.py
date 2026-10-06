#!/usr/bin/env python3
"""Build research/sources.json.

Part A: parse the verification ledger out of the academic literature review.
Part B: append the sources cited in the tool-landscape and practitioner reports
        (those two reports are prose, so their URLs are listed explicitly here).
Deduplicates by URL and assigns stable sequential IDs per category.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIT = ROOT / "raw" / "02-academic-literature-review.md"
OUT = ROOT / "sources.json"

CATEGORIES = {"papers", "standards", "tools", "practitioner", "blogs"}

# --- Part B: sources from the tool-landscape report -------------------------
TOOLS: list[tuple[str, str, str]] = [
    ("tool-anchore-false-positives", "Anchore: Say goodbye to false positives (CPE->PURL/GHSA/OSV shift)", "https://anchore.com/blog/say-goodbye-to-false-positives/"),
    ("tool-anchore-nvd-opaque", "Anchore: NVD opaque changes and answered questions", "https://anchore.com/blog/national-vulnerability-database-opaque-changes-and-answered-questions/"),
    ("tool-grype-2606", "grype#2606: GitHub Actions pinned by SHA yields false positives", "https://github.com/anchore/grype/issues/2606"),
    ("tool-grype-1737", "grype#1737: PURL/CPE vendor namespace mismatch (poco vs pocoproject)", "https://github.com/anchore/grype/issues/1737"),
    ("tool-grype-1245", "grype#1245: SPDX cannot express Go mainModule -> match against all versions", "https://github.com/anchore/grype/issues/1245"),
    ("tool-grype-1764", "grype#1764: missing fix-version data (CVE-2023-45853 zlib/Minizip)", "https://github.com/anchore/grype/issues/1764"),
    ("tool-grype-3456", "grype#3456: wrong version range for CVE-2025-3277 (SQLite 3.24.0 flagged)", "https://github.com/anchore/grype/issues/3456"),
    ("tool-syft-2319", "syft#2319: SPDX Go mainModule regression", "https://github.com/anchore/syft/issues/2319"),
    ("tool-syft-4025", "syft#4025: invalid PURL for Go replace directives, rejected by Trivy", "https://github.com/anchore/syft/issues/4025"),
    ("tool-syft-3776", "syft#3776: PR parsing trailing version comment on SHA-pinned actions", "https://github.com/anchore/syft/pull/3776"),
    ("tool-trivy-7850", "trivy discussion #7850: SBOM round-trip loses SrcName -> 0 vulns on vulnerable image", "https://github.com/aquasecurity/trivy/discussions/7850"),
    ("tool-trivy-8351", "trivy discussion #8351: .trivyignore is client-side only", "https://github.com/aquasecurity/trivy/discussions/8351"),
    ("tool-trivy-scanner", "Trivy docs: vulnerability scanner design, distro-first advisory policy", "https://trivy.dev/docs/latest/guide/scanner/vulnerability/"),
    ("tool-osv-scanner-v2", "OSV-Scanner v2 built on OSV-Scalibr", "http://osv.dev/blog/posts/osv-scanner-v2-beta1-is-ready/"),
    ("tool-osv-5295", "google/osv.dev#5295: 10-day GHSA ingestion outage + unreviewed advisories 404", "https://github.com/google/osv.dev/issues/5295"),
    ("tool-ghsa-7587", "github/advisory-database#7587: GHSA ingestion outage April 2026", "https://github.com/github/advisory-database#7587"),
    ("tool-ghsa-2451", "github/advisory-database#2451: incomplete CVE ingestion for unsupported ecosystems", "https://github.com/github/advisory-database/issues/2451"),
    ("tool-ghsa-readme", "GitHub Advisory Database README: database_specific last_known_affected_version_range", "https://github.com/github/advisory-database/blob/main/README.md"),
    ("tool-ghsa-docs", "GitHub docs: GHSA sources, reviewed vs unreviewed tiers, Dependabot behaviour", "https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/github-advisory-database"),
    ("tool-snyk-db", "Snyk Vulnerability Database: Application Feed and OS Feed", "https://docs.snyk.io/scan-fix-and-prevent/scan-with-snyk/snyk-open-source/manage-vulnerabilities/snyk-vulnerability-database"),
    ("tool-snyk-nvd-delays", "Snyk: Snyk users don't have to worry about NVD delays (2024-03-13)", "https://snyk.io/blog/snyk-users-dont-have-to-worry-about-nvd-delays/"),
    ("tool-snyk-fp-claims", "Snyk: Minimizing false positives (vendor claim, 0.08% FP rate)", "https://snyk.io/blog/minimizing-false-positives-enhancing-security-efficiency/"),
    ("tool-doyensec-sca-benchmark", "Doyensec SCA benchmark: Snyk and Dependabot below 15% accuracy", "https://www.doyensec.com/resources/Doyensec_Software_Composition_Analysis_Benchmark.pdf"),
    ("tool-claircore-matching", "Claircore concepts: vulnerability matching and distro-specific matchers", "https://quay.github.io/claircore/concepts/vulnerability_matching.html"),
    ("tool-claircore-indexing", "Clair core concepts: indexing (layer diffing, content-addressable store)", "https://github.com/quay/clair/blob/main/Documentation/concepts/indexing.md"),
    ("tool-docker-scout", "Docker Scout: analysis model, CVE list stored in image metadata, 10GB limit", "https://docs.docker.com/scout/explore/analysis/"),
    ("tool-dt-3178", "Dependency-Track#3178: NVD version ranges always use ANY -> SUBSET/SUPERSET matching", "https://github.com/DependencyTrack/dependency-track/issues/3178"),
    ("tool-dt-3146", "Dependency-Track#3146: CPE SUBSET/SUPERSET relationships during matching", "https://github.com/DependencyTrack/dependency-track/issues/3146"),
    ("tool-dt-3268", "Dependency-Track#3268: CPE version '-' (NA) matches every version -> recurring FPs", "https://github.com/DependencyTrack/dependency-track/issues/3268"),
    ("tool-dt-3774", "Dependency-Track#3774: RPM epoch/release field mismatch -> 77 vs 27 findings (50 FPs)", "https://github.com/DependencyTrack/dependency-track/issues/3774"),
    ("tool-dt-4568", "Dependency-Track#4568: third-party analyzer (OSS Index) produced a false positive", "https://github.com/DependencyTrack/dependency-track/issues/4568"),
    ("tool-dt-4862", "Dependency-Track#4862: VEX and .trivyignore ignored on ingestion", "https://github.com/DependencyTrack/dependency-track/issues/4862"),
    ("tool-dt-5370", "Dependency-Track#5370: false negative when severity is UNASSIGNED", "https://github.com/DependencyTrack/dependency-track/issues/5370"),
    ("tool-dt-5992", "Dependency-Track#5992: suppression is project-scoped, no global CVE<->component suppression", "https://github.com/DependencyTrack/dependency-track/issues/5992"),
    ("tool-dt-changelog", "Dependency-Track changelog (NVD 2.0 feeds, ANY/NA false negative fix)", "https://docs.dependencytrack.org/changelog/"),
    ("tool-openspg-536", "OpenSPG#536: silent rule failures, no client-visible error", "https://github.com/OpenSPG/openspg/issues/536"),
    ("tool-vuls-purl", "Vuls docs: CPE and PURL assignment, upstream version precedence", "https://help.vuls.biz/en/manual/scan/cpe/assign_cpe_purl/"),
    ("tool-nmap-vulns-nse", "Nmap vulns NSE library: VULNERABLE vs LIKELY_VULN state model", "https://nmap.org/nsedoc/lib/vulns.html"),
    ("tool-shodan-vuln-assessment", "Shodan docs: verified vs unverified vulns, backport limitation", "https://help.shodan.io/mastery/vulnerability-assessment"),
    ("tool-nessus-45590", "Tenable Nessus plugin 45590: best-effort computed CPE derivation", "https://www.tenable.com/plugins/nessus/45590"),
    ("tool-nessus-inventory", "Tenable docs: determining software inventory and authorization support", "https://docs.tenable.com/cyber-exposure-studies/software-inventory/Content/DeterminingSoftwareAuthorizationSupport.htm"),
    ("tool-greenbone-18656", "Greenbone forum: CVE-2015-8960 false positive, backport origin, CPE constraints", "https://forum.greenbone.net/t/false-positive-of-cve-2015-8960/18656"),
    ("tool-greenbone-21389", "Greenbone forum: CVE-2025-24016 feed coverage latency", "https://forum.greenbone.net/t/question-on-cve-2025-24016-coverage/21389"),
    ("tool-cve-bin-tool-triage", "cve-bin-tool: manual TRIAGE.json, package-name collision FPs (arrow)", "https://cve-bin-tool.readthedocs.io/en/stable/triaging_process.html"),
    ("tool-nvd-home", "NIST NVD programme home (backlog status, NVD 2.0 feeds)", "https://www.nist.gov/itl/nvd"),
    ("tool-nvd-cpe-range-notice", "NVD CPE Range Notification: ranges depend on dictionary coverage", "https://nvd.nist.gov/General/News/CPE-Range-Notification"),
    ("tool-enisa-euvd", "ENISA European Vulnerability Database announcement (2025)", "https://www.enisa.europa.eu/news/consult-the-european-vulnerability-database-to-enhance-your-digital-security"),
    ("tool-ossindex-lookup", "OSS Index component lookup used as a Dependency-Track analyzer", "https://ossindex.sonatype.org/component/pkg:nuget/System.Text.Json"),
]

# --- Part B: practitioner / incident sources --------------------------------
PRACTITIONER: list[tuple[str, str, str]] = [
    ("prac-debian-tracker", "Debian Security Tracker: how downstream analysis and status states work", "https://security-team.debian.org/security_tracker.html"),
    ("prac-debian-curl-2025-9086", "Debian tracker commit: CVE-2025-9086 (curl) vulnerable code introduced later", "https://www.mail-archive.com/debian-security-tracker-commits@alioth-lists.debian.net/msg72206.html"),
    ("prac-debian-python311-backport", "Debian bookworm python3.11 backport batch (+deb12u7)", "https://linux.debian.devel.release.narkive.com/Aytbrshn/processed-bookworm-pu-package-python3-11-3-11-2-6-deb12u7"),
    ("prac-cisa-vex-min-req", "CISA: Minimum Requirements for a VEX (statuses and justifications)", "https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf"),
    ("prac-cisa-when-to-issue-vex", "CISA: When to Issue a VEX (inheritance rules, automation limits)", "https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf"),
    ("prac-openshift-triage", "OpenShift engineering: node-cve triage guidance, evidence-based Uncertain/Unaffected", "https://github.com/openshift-eng/ai-helpers/blob/main/plugins/node-cve/commands/triage.md"),
    ("prac-cyclonedx-vex-609", "CycloneDX spec discussion #609: lossy mapping between VEX profiles", "https://github.com/CycloneDX/specification/discussions/609"),
    ("prac-cyclonedx-vex-crosswalk", "Community CycloneDX->OpenVEX crosswalk: contested and lossy cells", "https://github.com/getreeldev/cyclonedx-to-openvex"),
    ("prac-mandiant-moveit", "Mandiant: zero-day MOVEit data theft, exploitation 4 days pre-disclosure", "https://cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft"),
    ("prac-quo-wirefire", "Quo Intelligence: unreported WIREFIRE web shell variant evading public YARA", "https://quointelligence.eu/2024/01/unc5221-unreported-and-undetected-wirefire-web-shell-variant/"),
    ("prac-bishopfox-fortijump", "Bishop Fox: FortiJump CVE-2024-47575, exploitation preceded the advisory", "https://bishopfox.com/blog/a-look-at-fortijump-cve-2024-47575"),
    ("prac-darktrace-citrix", "Darktrace: stemming the Citrix Bleed (CVE-2023-4966) exploitation", "https://www.darktrace.com/blog/stemming-the-citrix-bleed-vulnerability-with-darktraces-activeai-platform"),
    ("prac-rapid7-asset-discovery", "Rapid7: approaches to asset discovery and the blind spot of each", "https://www.rapid7.com/blog/post/2024/10/17/understanding-your-attack-surface-different-approaches-to-asset-discovery/"),
    ("prac-intruder-shadow-it", "Intruder: shadow IT risks discovered via Certificate Transparency logs", "https://www.intruder.io/research/shadow-it-risks"),
    ("prac-precursor-easm", "Precursor: EASM vs vulnerability scanning, the seed-list single point of failure", "https://www.precursorintelligence.com/blog/easm-vs-vulnerability-scanning"),
    ("prac-cycognito-waf", "Cycognito: state of WAF protection, WAF sprawl, unknown unknowns", "https://www.cycognito.com/blog/state-of-waf-protection/"),
    ("prac-runzero-kevology", "runZero KEVology (Beardsley, ex-CISA KEV section chief): analysis of KEV", "https://www.runzero.com/uploads/documents/reports/KEVology-An-analysis-of-exploits-scores-and-timelines-on-the-CISA-KEV.pdf"),
    ("prac-runzero-kev-blog", "runZero: making CISA KEV actionable (KEVology summary)", "https://www.runzero.com/blog/making-cisa-kev-actionable/"),
    ("prac-kev-collider-data", "runZero kev-collider-data: per-CVE KEV enrichment dataset", "https://github.com/runZeroInc/kev-collider-data"),
    ("prac-docker-dhi-vex", "Docker Hardened Images VEX policy: not_affected + inline_mitigations_already_exist", "https://docs.docker.com/dhi/explore/security-concepts/vex/"),
    ("prac-jku-vex-thesis", "JKU thesis: distribution of VEX statements, cites 88.8% FP figure", "https://epub.jku.at/obvulihs/download/pdf/12450868"),
    ("prac-cso-nvd-overload", "CSO: NIST cuts down CVE analysis amid vulnerability overload", "https://www.csoonline.com/article/4159882/nist-cuts-down-cve-analysis-amid-vulnerability-overload.html"),
    ("prac-sitehost-backports", "sitehost.nz: vulnerability scans and backported patches", "https://sitehost.nz/blog/vulnerability-scans-backported-patches"),
    ("prac-thingsrecon-shadow", "ThingsRecon: why CISOs struggle with shadow assets", "https://www.thingsrecon.com/blog/why-cisos-struggle-with-shadow-assets"),
    ("prac-zerofox-shadow-cloud", "ZeroFox: shadow in the cloud, unmanaged cloud/CDN assets (vendor)", "https://www.zerofox.com/blog/shadow-in-the-cloud-why-easm-must-uncover-your-unknown-cloud-cdn-assets/"),
]

# --- Part B: conference talks / blogs ---------------------------------------
BLOGS: list[tuple[str, str, str]] = [
    ("blog-gamblin-2024-cve-review", "Gamblin: 2024 CVE data review (40,009 CVEs, +38.83%)", "https://jgamblin.com/2025/01/05/2024-cve-data-review/"),
    ("blog-gamblin-bsides-munich-2025", "Gamblin, BSides Munich 2025: navigating the volatile vulnerability landscape", "https://rogolabs.net/Talks/Navigating%20the%20Volatile%20Vulnerability%20Landscape%20-%20BSides%20Munich.pdf"),
    ("blog-perkal-bsideslv23", "Perkal, BSidesLV 2023: review of vulnerability triage (abstract)", "https://pretalx.com/bsideslv23/talk/review/VCYNCXSUHPFBAGJLGMKHTJB7CHF99FHV"),
    ("blog-censys-v2-benchmark", "Censys vs Shodan v2 (vendor honeypot benchmark, methodology disclosed)", "https://anchor-u.com/wp-content/uploads/Censys-vs.-Shodan-v2-2024.pdf"),
    ("blog-ponce-2024-br", "Ponce et al. 2024: Shodan vs Censys on Brazilian internet space", "https://exa.ai/library/publication/bcdclpd7w5y"),
    ("blog-rapid7-project-sonar", "Rapid7 Project Sonar: internet-wide IPv4 scanning", "https://www.rapid7.com/research/project-sonar/"),
    ("blog-github-advisory-docs", "GitHub docs: vulnerability reporting and management, GHSA", "https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/github-advisory-database"),
    ("blog-github-ecosystem-sec", "GitHub: how we investigate CVEs and coordinate with the ecosystem", "https://github.blog/engineering/platform-security/how-we-investigate-cves-and-coordinate-with-the-ecosystem/"),
]

# arXiv / eprint sources for 2025-2026 LLM-agentic vuln work (from the first search pass)
PAPERS_EXTRA: list[tuple[str, str, str]] = [
    ("arx-2604-17860-titanca", "TitanCA: multi-agent LLM pipeline for zero-day discovery (SMU/GovTech)", "https://arxiv.org/pdf/2604.17860"),
    ("arx-2609-05335-bugstone", "BUGSTONE-E2E: CVE patch history as executable detection rules", "https://arxiv.org/pdf/2609.05335"),
    ("arx-2607-12316-antiproof", "Antiproof: vulnerability detector synthesis + proofs of exploitability", "https://arxiv.org/html/2607.12316"),
    ("arx-2606-19149-openant", "OpenAnt: LLM vuln discovery with adversarial verification and dynamic testing", "https://arxiv.org/html/2606.19149v2"),
    ("arx-2607-26656-graph-verifier", "Graph Is the Verifier: agentic RL for interprocedural vulnerability detection", "https://arxiv.org/abs/2607.26656"),
    ("arx-2509-03876-affected-versions", "Affected-version identification: 12 tools, 1,128 real C/C++ vulns, best accuracy 44.9%", "https://arxiv.org/html/2509.03876"),
    ("arx-2506-12995-crossdb", "Cross-database vulnerability report reconciliation (GHSA + Snyk, 10 languages)", "https://arxiv.org/pdf/2506.12995"),
    ("arx-2006-15074-cleaning-nvd", "Cleaning the NVD: vendor/product name inconsistency at scale", "https://arxiv.org/pdf/2006.15074v1.pdf"),
    ("arx-1302-4133-nvd-unreliable", "(Un)Reliability of NVD Vulnerable Versions (Chrome version-range errors)", "https://arxiv.org/pdf/1302.4133"),
    ("arx-1705-05347-cpe-cve", "Software vulnerability analysis using CPE and CVE (Benthin et al.)", "https://arxiv.org/pdf/1705.05347"),
    ("arx-2506-17798-savant", "Savant: reachability analysis trade-off between FP and FN", "https://arxiv.org/html/2506.17798v2"),
    ("arx-2608-19430-harp", "HARP: domain-adaptive vulnerability prioritization for enterprise IT/security", "https://arxiv.org/abs/2608.19430"),
    ("arx-2601-22952-sifting-noise", "Sifting the Noise: agentic suppression of false-positive code alerts", "https://arxiv.org/abs/2601.22952"),
    ("arx-2512-17710-svs-test", "SVS-TEST: testing software vulnerability scanner behaviour incl. silent failures", "https://arxiv.org/abs/2512.17710"),
    ("arx-2603-06422-siabench", "Before You Hand Over the Wheel: SIABENCH for AI security agents", "https://arxiv.org/abs/2603.06422"),
    ("arx-2510-20739-triagejs", "Learning to Triage Vulnerability Reports from Community Data", "https://arxiv.org/abs/2510.20739"),
    ("arx-2609-08040-vexbench", "VEX-Bench: benchmarking LLMs on VEX affected/not_affected and justifications", "https://arxiv.org/html/2609.08040v1"),
    ("std-ovana-quality-vdb", "OVANA: quality of vulnerability databases (ARES 2021)", "https://peasec.de/paper/2021/2021_KuehnBayerWendelbornReuter_OVANAQualityVulnerabilityDatabases_ARES.pdf"),
    ("std-msr4ps-2025-sbom-compliance", "MSR4PS 2025: SBOM generator vs format effect on NTIA compliance (2,225 images)", "https://www.cs.montana.edu/izurieta/pubs/MSR4PS_2025.pdf"),
    ("std-guac-docs", "GUAC documentation: ontology", "https://docs.guac.sh/guac/guac-ontology/"),
    ("std-guac-github", "guacsec/guac repository", "https://github.com/guacsec/guac"),
    ("std-openssf-guac-1", "OpenSSF: GUAC joins OpenSSF as incubating project", "https://openssf.org/blog/2024/03/07/guac-joins-openssf-as-incubating-project/"),
]


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def main() -> None:
    entries: list[dict] = []
    seen: set[str] = set()

    # Part A - academic literature review verification ledger
    text = LIT.read_text(encoding="utf-8")
    ledger = text.split("## Verification ledger", 1)[-1]
    for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*(https?://[^|]+?)\s*\|\s*([^|]*?)\s*\|\s*(VERIFIED|UNVERIFIED)\s*\|$",
                         ledger, flags=re.M):
        num, url, cited_in, status = m.groups()
        url = url.strip().rstrip(".")
        if url in seen:
            continue
        seen.add(url)
        entries.append({
            "id": f"lit-{int(num):03d}",
            "category": "papers",
            "title": "",
            "cited_in": cited_in.strip(),
            "url": url,
            "verified": status == "VERIFIED",
        })

    for group, cat in ((TOOLS_EXTRA := TOOLS, "tools"), (PRACTITIONER, "practitioner"),
                       (BLOGS, "blogs"), (PAPERS_EXTRA, "papers")):
        for sid, title, url in group:
            if url in seen:
                continue
            seen.add(url)
            entries.append({
                "id": sid,
                "category": cat,
                "title": title,
                "cited_in": "",
                "url": url,
                "verified": None,
            })

    bad = {e["category"] for e in entries} - CATEGORIES
    if bad:
        raise SystemExit(f"unknown categories: {bad}")

    OUT.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    counts: dict[str, int] = {}
    for e in entries:
        counts[e["category"]] = counts.get(e["category"], 0) + 1
    print(f"wrote {OUT} with {len(entries)} unique sources")
    for k, v in sorted(counts.items()):
        print(f"  {k:<13} {v}")


if __name__ == "__main__":
    main()
