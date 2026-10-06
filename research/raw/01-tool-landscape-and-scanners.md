# Tool Landscape and Data-Layer Survey — Automatic CVE Matching for Infrastructure

**Date of research:** 2026-10-01
**Method:** direct retrieval of vendor documentation, GitHub issues, release APIs, and primary studies. Every limitation below is cited to a primary source that was actually opened. Where a source could not be retrieved, this is stated rather than filled in.

**Provenance note:** this report was produced by a research subagent whose terminal output was truncated after §6.3. Sections 1–6.3 are the subagent's original text. §6.4–6.5 are marked as reconstructed. Anything after the truncation point that could not be recovered is listed explicitly in §7 so it is not mistaken for completed research.

---

## 0. Executive summary

The bottleneck is no longer vulnerability *discovery* — it is **binding a CVE record to a specific installed artifact**. Every tool here is functionally a matcher between a database record (CPE, PURL, OSV range) and an observed string, and the observed string is usually a version number scraped from a manifest, a lockfile, a dpkg database, or a network banner. The failure modes are therefore concentrated and highly repeatable.

| Failure mode | Root cause | Documented impact |
|---|---|---|
| Wrong version bound | Scraper / database range error | Grype flagged SQLite 3.24.0 for CVE-2025-3277 when NVD's actual range was 3.44.0–3.49.1 |
| Missing source-package mapping | Alpine CVEs keyed to `openssl`, not `libcrypto3` | Trivy SBOM scan returned 0 vulns where a direct image scan found them |
| Lost metadata across SBOM formats | SPDX 2.3 cannot express Go `mainModule` | Grype matched a package against *all* versions, producing pure noise |
| Epoch/release field splitting | RPM `1:1.12.20-8.el9` vs `{epoch, release}` | Dependency-Track: 77 findings vs Trivy CLI's 27 — **50 false positives** |
| Backport-invisible patching | Distro keeps upstream version, changes build | Shodan explicitly documents that patched enterprise Linux is never detected as fixed |
| CPE `ANY` / `NA` wildcards | NVD ranges always use `ANY` for version | Strict spec compliance in Dependency-Track discarded valid matches (23 vs 366 findings) |
| Cross-tool semantic mismatch | Same name, different vendor namespace | `cpe:2.3:a:poco:poco` vs DB's `cpe:2.3:a:pocoproject:poco` |
| Distribution lag | NVD backlog, GHSA sync outage | 500+ CVEs in Snyk's DB unanalyzed by NVD; OSV missed Maven/npm advisories for ~10 days |

Two independent quantitative anchors dominate everything below:

- An empirical study of **2,414 repositories** found a **97.5% false-positive rate** from downstream SBOM-based scanners *even when the SBOM itself was generated accurately from lockfiles*. Function-call analysis pruned 63.3% of those. (The companion academic review records a **92.0%** FP rate on a manually-validated subset of the same study — 9 true positives of 113 findings — which is the more defensible figure, since 97.5% was measured against a looser criterion. Treat 92% as the citable number.)
- A USENIX Security 2025 study of internet-wide scanners found **over 95% of Shodan's banner-based CVE detections to be false positives**, and for 18 of 21 tested CVEs, independent Nuclei verification contradicted more than 95% of them.

---

## 1. Scanners

### 1.1 Anchore Grype + Syft

**Releases observed:** Grype v0.119.0 and Syft v1.52.0, both 2026-09-17.

**Architecture.** Syft catalogs packages and emits an SBOM (its own JSON, CycloneDX, or SPDX); Grype matches that inventory against Anchore's normalized vulnerability DB. Anchore's stated strategy is to move away from CPE-only matching toward PURL/GHSA/OSV identifiers, because CPE strings are the single largest source of false positives ([Anchore, 2023](https://anchore.com/blog/say-goodbye-to-false-positives/)).

**Documented limitations:**

1. **Immutable-reference version loss.** GitHub Actions pinned by commit SHA (`uses: tj-actions/changed-files@ed68ef82…  # v46.0.5`) were recorded with the SHA as the "version," producing false positives against unrelated GHSA records. Fixed by teaching Syft to parse the trailing version comment ([grype#2606](https://github.com/anchore/grype/issues/2606), via [syft#3776](https://github.com/anchore/syft/pull/3776)). The general lesson stands: **when an artifact is pinned by digest, the version string is absent and every range comparison is meaningless.**

2. **Vendor-namespace mismatch.** Syft generated `cpe:2.3:a:poco:poco:1.12.2` while the advisory DB carried `cpe:2.3:a:pocoproject:poco:*` → silent non-match ([grype#1737](https://github.com/anchore/grype/issues/1737)). The same thread shows Conan revision suffixes (`1.3#06023034579559bb64357db3a53f88a4`) embedded in the version field, breaking both CPE and PURL construction.

3. **SBOM format fidelity loss (structural FP source).** For Go main modules, Grype suppresses findings by consulting Syft's `metadata.mainModule`. **SPDX 2.x has no way to express that field.** Scanning the same image's SPDX SBOM matched the package against *all* versions and reported vulnerabilities fixed years earlier ([grype#1245](https://github.com/anchore/grype/issues/1245)). Closed as *"really a format limitation of SPDX 2, not a bug in syft/grype."* Reproduced as [syft#2319](https://github.com/anchore/syft/issues/2319). Syft's SPDX PURL for Go `replace` directives (`pkg:golang/../../@(devel)`) is now rejected outright by Trivy ([syft#4025](https://github.com/anchore/syft/issues/4025)).

4. **Missing fix-version data.** For CVE-2023-45853 and CVE-2022-37434 (zlib), neither NVD nor GHSA carried fix-version data, so Grype could not populate `FIXED-IN`. Anchore's own assessment: *"We explored the idea of using CPE matching to infer fix version information in some cases, but it turned out to be an unreliable method"* ([grype#1764](https://github.com/anchore/grype/issues/1764)). Note the underlying data problem — CVE-2023-45853 is actually in Minizip, bundled inside zlib, so the CVE's product attribution is itself wrong.

5. **Range-bound bug in the DB itself (2025).** Grype's DB reported CVE-2025-3277 as `cpe:2.3:a:sqlite:sqlite < 3.49.1` while the NVD API showed `versionStartIncluding: 3.44.0`, `versionEndExcluding: 3.49.1`. SQLite **3.24.0** was flagged as vulnerable. Root cause was an Anchore *enriched* record shadowing the NVD record, compounded by DB caching ([grype#3456](https://github.com/anchore/grype/issues/3456)). This is a category worth naming explicitly: **downstream enrichment layers can make matches worse, not better.**

**Net assessment:** Grype's own DB is a *third* normalization layer on top of NVD/GHSA/OSV. It improves identifier coverage but introduces a new class of bug where the enrichment, not the source, is wrong.

### 1.2 Trivy

**Release observed:** v0.74.0 (2026-08-14).

**Distro-aware by design.** Trivy's documented policy is to prefer *the Linux distribution's own* advisory over NVD for OS packages, precisely because distributors backport patches without changing version numbers. Trivy openly prioritizes **precision over recall** ([Trivy docs](https://trivy.dev/docs/latest/guide/scanner/vulnerability/)).

**Documented limitation — SBOM round-trip fidelity.** The canonical cross-tool FP/FN case ([trivy discussion #7850](https://github.com/aquasecurity/trivy/discussions/7850)):

- `syft` → CycloneDX → `trivy sbom` reported **0 vulnerabilities**.
- `trivy image` on the same image reported CVE-2024-9143 in `libcrypto3`.
- Cause: Alpine's security tracker keys CVEs to the **source package** (`openssl`), not the binary package (`libcrypto3`). Trivy encodes `SrcName` in `properties` when *it* generates CycloneDX; Syft encodes it as a `?upstream=` PURL qualifier. Consuming Syft's SBOM, Trivy finds no `SrcName` and matches on `libcrypto3` → no hits.
- Trivy's own log at that point emits: `WARN Third-party SBOM may lead to inaccurate vulnerability detection`.

This is the sharpest available illustration of the central thesis: **a vulnerability-matching result is not a property of the image. It is a property of (image, generator, format, consumer) as a tuple.**

**Suppressions are client-side only.** `.trivyignore` is consumed by the CLI; it is not emitted into the SBOM, so no server-side platform honors it ([dependency-track#4862](https://github.com/DependencyTrack/dependency-track/issues/4862), [trivy discussion #8351](https://github.com/aquasecurity/trivy/discussions/8351)).

### 1.3 OSV-Scanner (Google)

**Release observed:** v2.6.0 (2026-09-14). v2 moved the scanner onto Google's OSV-Scalibr framework, adding SBOM generation to scanning ([OSV blog, 2025](http://osv.dev/blog/posts/osv-scanner-v2-beta1-is-ready/)).

**Strength:** it sidesteps CPE entirely. OSV records are keyed to `(ecosystem, package name)` with `affected[].ranges` expressed as `introduced` / `fixed` / `last_affected` events — the ecosystem defines the version comparator, so Debian, Alpine, Maven and npm semantics are each handled natively rather than flattened into a semver guess.

**Documented limitations:**

- **Ecosystem gaps.** OSV coverage is only as complete as its upstream contributors. It does not cover C/C++ OS packages the way distro trackers do.
- **GHSA ingestion stalled for ~10 days in April 2026** for Maven (from April 23) and npm (from April 24), meaning the OSV API and dumps returned nothing new for those ecosystems while scanners relying on OSV missed disclosures ([google/osv.dev#5295](https://github.com/google/osv.dev/issues/5295), [github/advisory-database#7587](https://github.com/github/advisory-database/issues/7587)). GitHub confirmed *"a failure mode in our internal advisory sync process that wasn't handled robustly enough."*
- **Unreviewed GHSA advisories do not reach OSV at all.** CVE-2026-40976 / GHSA-8v8j-3hxp-93wr was live on GitHub but returned 404 from the OSV API because it was unreviewed.

### 1.4 Docker Scout

**Architecture** ([Docker docs](https://docs.docker.com/scout/explore/analysis/)): extracts an SBOM from the image, evaluates it against advisory data, then **stores the resulting CVE list in the image's metadata** rather than in the SBOM. On each analysis, Scout re-evaluates the stored CVE list against updated advisory data.

**Limitations:**

- Because the persisted artifact is a *CVE list, not an SBOM*, the detection is not portable — another tool reading the same image cannot consume Scout's result, and any finding Scout later revises is invisible to tools that already consumed the list.
- Images larger than **10 GB** cannot be analyzed.

### 1.5 Snyk

**Data source model** ([Snyk VulnDB docs](https://docs.snyk.io/scan-fix-and-prevent/scan-with-snyk/snyk-open-source/manage-vulnerabilities/snyk-vulnerability-database)): every entry is analyst-verified, drawn from monitoring NVD and other feeds, GitHub activity, bulk pattern research, and manual audit. It publishes an **Application Feed** and an **OS Feed**.

**Stated independence from NVD** ([Snyk blog, 2024-03-13](https://snyk.io/blog/snyk-users-dont-have-to-worry-about-nvd-delays/)):

- 355 CVEs published in the Snyk Security Database during 2024 had not been analyzed by NVD as of the September update; >500 CVEs as of March 12, 2024.
- Container advisory details *"rely primarily on the Linux distributions' own provided information"* — again for backport reasons.
- **Documented consequence of NVD lag:** where a distro provides no CVSS or "Relative Importance" and Snyk passes through NVD's value, *"those will see delays in CVSS assessment as a result of this incident."* Pre-NVD publication examples cited: CVE-2024-22243 (High, Spring open redirect) and CVE-2024-1597 (Critical, PostgreSQL SQLi).

**Independently measured accuracy:**

- **Doyensec SCA benchmark** (Semgrep Supply Chain vs Snyk vs Dependabot): Dependabot found the most true positives *and* the most false positives; **both Snyk and Dependabot fell below a 15% accuracy rate**; both were *"automatically removed from consideration for automation in CI/CD on the basis of the high false positive counts alone."* Snyk's reachability analysis was documented as **Java-only**, meaning all non-Java findings were pure name+version matching ([PDF](https://www.doyensec.com/resources/Doyensec_Software_Composition_Analysis_Benchmark.pdf)).
- Snyk's own marketing claims a **0.08% false-positive rate** for Snyk API & Web ([2025-07-01](https://snyk.io/blog/minimizing-false-positives-enhancing-security-efficiency/)). This is a vendor figure for the API/Web product class, not for open-source/container matching, and is not comparable to Doyensec's SCA numbers. Treat as marketing, not evidence.

**Cross-database reconciliation is a research problem, not a solved one.** A 2025 study merged 31,267 vulnerability reports from GHSA + Snyk across 10 languages and had to build a *unified* affected-version representation, because OSV adoption is inconsistent — the same advisory may express ranges as `events.introduced`/`fixed`/`last_affected` in one database and as explicit version arrays in another. The authors removed **6,391 duplicate reports** and found 155 duplicate reports lacking CVEs, noting publish dates differ across platforms ([arXiv:2506.12995](https://arxiv.org/pdf/2506.12995)).

### 1.6 Clair / Claircore

**Release observed:** Clair v4.9.0, published 2025-12-10 — the stalest release in this survey. Clair originated at CoreOS and left beta in March 2016; it is now under the quay org ([clair](https://github.com/quay/clair), [claircore](https://github.com/quay/claircore)).

**Architecture.** Claircore is a Go library implementing an **indexer** (walk layers, diff, produce a content-addressable artifact store) and a **matcher** (join manifests against vulnerability data via distro-specific matchers — dpkg, apk, rpm, etc.) ([vulnerability matching](https://quay.github.io/claircore/concepts/vulnerability_matching.html), [indexing concepts](https://github.com/quay/clair/blob/main/Documentation/concepts/indexing.md)). Content-addressable layer storage means identical layers across images are enumerated once.

**Strength:** because the matcher is selected by *distro manifest format* rather than by generic version strings, Clair inherits the distro's own versioning semantics (epoch, release, apk revision, dpkg `debian_revision`) rather than guessing.

**Limitations:** no native source-package indirection handling comparable to Trivy's; no documented reachability/context layer; CVE data quality entirely inherited from upstream, so the CPE/`NA`-version and backport problems in §4 apply with full force. The release cadence suggests a maintenance-mode posture.

### 1.7 A tool named "Clairity" does not exist

An explicit search for a container vulnerability scanner named **Clairity** returned no such project. All results were unrelated entities (Clairity Inc — an FDA-authorized imaging AI company; ClairityDev — a Slack-native AI workflow platform; assorted personal/AI-admin repositories). Code search within `quay/clair` returns nothing.

**Flagged, not invented.** If "Clairity" appears in a tool list, it is a hallucination, a misremembering of *Clair*, or a confusion with *Claircore*.

---

## 2. Vulnerability databases

### 2.1 NVD

**2026 state** ([NIST NVD](https://www.nist.gov/itl/nvd)): a substantial enrichment backlog persists; CISA has prioritized work with explicit emphasis on KEV-listed CVEs; **NVD 2.0 feeds** are the current interface. Anchore documented the 2.0 transition as opaque and its enrichment delays as a recurring operational problem ([Anchore, 2024](https://anchore.com/blog/national-vulnerability-database-opaque-changes-and-answered-changes/)).

**Measured data-quality problems — the most thorough body of evidence in this area:**

| Study | Measurement |
|---|---|
| [Cleaning the NVD](https://arxiv.org/pdf/2006.15074v1.pdf) (Anwar et al.) | 1,835 inconsistent vendor names across 871 groups; ~10% of ~19K distinct vendors affected; 1.8K vendor names collapsible to 871 (≈5% reduction); 6% of product names inconsistent; 3,000+ inconsistently-named products across 700 vendors; CWE field frequently `NVD-CWE-Other` even when the correct CWE is in the free text |
| [VulCPE](https://arxiv.org/html/2505.13895) (2025) | 93.55% of NVD entries carry ≥1 valid CPE; **81.40% of official CPE dictionary strings are never referenced by any CVE**; 14.56% of entries rely on configuration-specific (AND/OR) CPEs; **50.18% of vendor names in NVD CPEs and 47.07% in CVEdetails are inconsistent**; 67% of 67,925 vendor names flagged, collapsing to 32,420 canonical forms; even within consistent vendors, 31.09% of product names are inconsistent |
| [(Un)Reliability of NVD Vulnerable Versions](https://arxiv.org/pdf/1302.4133) (Nguyen & Massacci) | Chrome-specific: of 539 NVD entries, only 167 (31%) were verifiable; **of those, 134 (81%) had wrong version ranges**; median per-version error rate significantly > 5% (p ≈ 1e-4); >7% erroneous overall even assuming all unverifiable entries are correct. Frequently cited upstream for the broader claim that ~25% of Chrome CVE version strings are wrong |
| [Software Vulnerability Analysis Using CPE and CVE](https://arxiv.org/pdf/1705.05347) (Benthin, Sanguino & Uetz, 2017) | **105,591 CPE entries in the CVE feeds did not exist in the CPE dictionary**; 895 CVE entries with no CPE at all; semantically identical products carrying different attribute values; typos in dictionary bindings; **conclusion: "fully automated assignment of a CPE identifier to a software product is impractical and error prone"** |
| [OVANA](https://peasec.de/paper/2021/2021_KuehnBayerWendelbornReuter_OVANAQualityVulnerabilityDatabases_ARES.pdf) | Clustering on (CPE, CWE, CVSSv3) reveals entries so broad they are indistinguishable — CVE-2019-2138 → CVE-2019-2165 form one cluster; libraries counted as part of the host product; missing CPEs; dummy CWE values; outdated CVSSv2 |

**The `ANY`-version structural problem.** NVD represents version ranges by putting `*` in the version attribute and adding `versionStartIncluding` / `versionEndExcluding`. This is not a data-entry mistake — it is the format. Dependency-Track's maintainers documented the consequence directly: *"CPEs with version range **always** have version set to `ANY`. Which means you're pretty much **guaranteed** to encounter `SUBSET` relationships during matching. This isn't even a NVD data quality issue, it's how the NVD has always used version ranges"* ([dependency-track#3178](https://github.com/DependencyTrack/dependency-track/issues/3178)). Enforcing the NIST spec's minimum matching requirements literally discarded so many valid matches that a test BOM yielded **23 findings instead of 366**. The shipped compromise: drop a match when vendor=SUBSET and product=SUPERSET, or vice versa.

**`NA` versions.** NVD CPEs like `cpe:2.3:a:apache:http_server:-:*:*:*:*:*:*:*` (version = `-`, i.e. NA) matched *every* version, causing Dependency-Track to re-surface ~10 false positives on every new version of the component, forever ([dependency-track#3268](https://github.com/DependencyTrack/dependency-track/issues/3268)). Fixed in 4.10; the changelog also records *"Fix false negatives in CPE matching for ANY and NA versions."*

**Range migration.** NVD moved to explicit version ranges in vulnerable-configuration data, with an explicit caveat: *"If the CPEs enumerated in a range contain gaps, then the missing versions likely need to be approved to the Official CPE Dictionary"* ([NVD CPE Range Notification](https://nvd.nist.gov/General/News/CPE-Range-Notification)). Ranges are therefore only as good as dictionary coverage — and 81.40% of that dictionary is unused.

### 2.2 OSV.dev and the GitHub Advisory Database

**GHSA sources** ([GitHub docs](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/github-advisory-database)): GitHub-reported advisories, NVD, npm, FriendsOfPHP, Go Vulncheck, PyPA, Ruby Advisory DB, RustSec, and community PRs. Advisories are stored as **OSV-format JSON**.

Two tiers, and the distinction is critical for FP/FN reasoning:

- **GitHub-reviewed** — mapped to supported ecosystems, validity-checked, with full description and ecosystem/package info. CVSS 3.1 and 4.0.
- **Unreviewed** — *"published automatically into the GitHub Advisory Database, directly from the National Vulnerability Database feed."* **Dependabot does not create alerts for these**, because they are unchecked for validity and completeness.

Two structural gaps:

1. **Incomplete CVE ingestion.** Advisories originating as GitHub security advisories that later receive a CVE, but that fall outside supported ecosystems, are missing entirely — acknowledged by GitHub as *"one small gap in our data"* ([advisory-database#2451](https://github.com/github/advisory-database/issues/2451)).
2. **Range representation loss.** GHSA maintains `last_known_affected_version_range` as a `database_specific` field because *"The OSV schema does not have native support for all of the potential ways GitHub represents vulnerable version ranges internally."* It may appear **in addition to or in place of** OSV range events ([README](https://github.com/github/advisory-database/blob/main/README.md)). **A consumer that reads only standard OSV ranges will silently miss these ranges.** GHSA also warns that `database_specific` values are *"subject to change without notice. Consuming systems should not rely on them."*

**EPSS** is synchronized daily for percentages; percentiles update only when materially different.

**Pipeline fragility.** The April 2026 ten-day sync outage is the concrete demonstration that the OSV → scanner path has single points of failure that no scanner can detect from its own output.

### 2.3 CISA KEV

**What it is not.** runZero's *KEVology*, authored by Tod Beardsley — **former CISA KEV section chief** — reframes KEV as an operational signal rather than a severity list ([PDF](https://www.runzero.com/uploads/documents/reports/KEVology-An-analysis-of-exploits-scores-and-timelines-on-the-CISA-KEV.pdf), [blog](https://www.runzero.com/blog/making-cisa-kev-actionable/), 2026-02).

Key measured findings:

- Of **1,488 KEV entries as of 2026-01-14, only 483 (32%)** are useful for immediate initial access. Of the last twelve KEV additions in 2025, four (33%) qualify.
- **464 KEVs** have an associated Metasploit module; **424** have ATT&CK mappings, and of those ~210 (half) have a Metasploit module or Nuclei template.
- Commodity exploit tooling **often predates KEV addition by days, weeks, or years**.
- Inclusion criteria are narrow: CVE ID, a reasonable mitigation path, CISA-observed exploitation, and relevance to the US FCEB. *"Many KEV vulnerabilities are not remotely exploitable or require authentication."*
- Beardsley singles out a class of CVEs that KEV matching handles badly: vulnerabilities in **fundamental libraries** present in hundreds to thousands of products — naming **CVE-2021-44228 (Log4Shell), CVE-2023-44487 (HTTP/2 Rapid Reset), CVE-2014-0160 (Heartbleed)** — *"particularly notorious for their resistance to easy operational identification by vulnerability management software."* That is precisely the class banner-based matching also fails on.
- Core conclusion: *"no single metric can do prioritization for you."*

Companion dataset: [runZeroInc/kev-collider-data](https://github.com/runZeroInc/kev-collider-data), which warns that re-running against fresh data yields different ratios than the paper.

### 2.4 ENISA European Vulnerability Database (EUVD)

Launched 2025 as an **aggregation** platform over existing national and international sources, with dashboards and multiple source types ([ENISA announcement, 2025](https://www.enisa.europa.eu/news/consult-the-european-vulnerability-database-to-enhance-your-digital-security)). Architecturally it sits *above* upstream sources, which means **EUVD inherits every upstream quality defect in §2.1 without adding independent verification.** It is a discovery/UI layer, not a new trust anchor.

### 2.5 CERT feeds — documented gap

No primary source was retrieved for US-CERT / CISA ICS-CERT advisory feeds or FIRST/EINET in this pass, so their structure and latency are **not characterized here**. The adjacent sourced fact: GHSA ingests ecosystem "CERT-like" databases (npm, FriendsOfPHP, Go Vulncheck, PyPA, Ruby Advisory, RustSec) rather than national CERT feeds. Characterizing the ICS/OT CERT feed picture requires a further retrieval pass.

---

## 3. SBOM-driven vulnerability management

### 3.1 Dependency-Track

**Release observed:** 5.1.1 (2026-09-20).

**Architecture.** Projects ingest SBOMs; analyzers run asynchronously against the BOM, applying internal CPE/vulnerability matching and delegating OS analysis to the Trivy analyzer.

**Documented limitations:**

1. **NVD feed break.** Removal of NVD 1.1 feeds broke the mirroring process; 5.x consumes NVD **2.0** feeds ([changelog](https://docs.dependencytrack.org/changelog/)).
2. **RPM epoch/release field mismatch → 50 false positives.** On an identical Rocky 9.4 SBOM, Dependency-Track's Trivy analyzer reported **77 vulnerabilities** while Trivy CLI reported **27**. Packet inspection showed DT sent `"version": "1:1.12.20-8.el9"` (epoch folded in, no `release` field) while Trivy CLI sent `"version": "1.12.20"` plus `"release": "8.el9"`. The 50 findings unique to DT were, on manual verification against Rocky's official advisories, **all false positives** ([dependency-track#3774](https://github.com/DependencyTrack/dependency-track/issues/3774)).
3. **Third-party analyzer data poisoning.** DT produced a false positive for CVE-2024-43485 on `System.Text.Json` 9.x; root cause was the **OSS Index analyzer** (Sonatype), not DT's own matching ([dependency-track#4568](https://github.com/DependencyTrack/dependency-track/issues/4568), [upstream dotnet/runtime#119773](https://github.com/dotnet/runtime/issues/119773)).
4. **False negatives with unassigned severity.** An SBOM containing genuinely vulnerable `icu-libs@76.1-r0` for CVE-2025-5222 yielded **zero** vulnerabilities in DT; the record existed but with severity `UNASSIGNED`. Grype found it ([dependency-track#5370](https://github.com/DependencyTrack/dependency-track/issues/5370)).
5. **Suppression architecture is project-scoped only.** `FALSE_POSITIVE` can only be set per project and per component version, so an ecosystem-wide bad CVE↔component mapping must be suppressed once per project per version. No global CVE↔component (PURL/CPE) suppression exists ([dependency-track#5992](https://github.com/DependencyTrack/dependency-track/issues/5992)).
6. **VEX and `.trivyignore` are ignored on ingestion.** Externally attached VEX is discarded; `.trivyignore` is client-side only. DT supports **CycloneDX VEX but not OpenVEX**, and VEX can only be applied to findings that already exist — which appear only after asynchronous analysis completes. Direct OpenVEX upload **fails schema validation**. The only working path is: upload BOM → download DT's generated VEX → mutate into DT's schema → re-upload ([dependency-track#4862](https://github.com/DependencyTrack/dependency-track/issues/4862)).

Item 6 is the most consequential for any real deployment: **there is no reliable way to carry a CI-time suppression decision into a continuously-re-analyzed server-side SBOM platform.**

### 3.2 CycloneDX and SPDX

**Specs observed:** CycloneDX 1.7.2 (2026-09-17); SPDX 3.0.1 (2024-12-17), with v3.1 still at RC1.

**The empirical tradeoff.** A 2025 study generated SBOMs from **2,225 Docker images** using Trivy/Syft in both CycloneDX and SPDX, then scored NTIA compliance. Its central finding: **the choice of SBOM-generation tooling affected NTIA compliance more than the choice of format** ([MSR4PS, 2025](https://www.cs.montana.edu/izurieta/pubs/MSR4PS_2025.pdf)).

**Format-specific losses are real, not theoretical:**

- SPDX 2.x cannot express Go `mainModule`, causing Grype to match against all versions ([grype#1245](https://github.com/anchore/grype/issues/1245)).
- Neither SPDX nor CycloneDX has a *standard* slot for Trivy's `SrcName`/`SrcVersion` — Trivy puts it in `properties`, Syft puts it in a PURL `upstream=` qualifier. **Two valid SBOMs of the same image carry this fact in incompatible places**, and at least one consumer (Trivy) only reads its own encoding.
- Syft's Go `replace`-directive handling emits structurally invalid PURLs (`pkg:golang/../../@(devel)`) that Trivy rejects outright ([syft#4025](https://github.com/anchore/syft/issues/4025)).

**Honest conclusion:** CycloneDX vs SPDX is largely a *fidelity contest neither format is currently winning*, because the information scanners need does not have a standardized home in either. Syft-json, a vendor format, currently preserves strictly more matching-relevant metadata than either standard.

### 3.3 OpenSPG / K8SPG

**Release observed:** v0.8 (2025-06-29). OpenSPG applies knowledge-graph reasoning over supply-chain artifacts — the most architecturally ambitious entrant here.

**Documented limitations** ([openspg#536](https://github.com/OpenSPG/openspg/issues/536)):

- **Concept rules execute at ingestion/build time, not query time.** Nothing is ever created at query time; queries only compute over what ingestion materialized. Misunderstand this and you will debug the wrong layer.
- Three concrete server-side defects: **#622** — nodes created by `createNodeInstance` lack an `id` property, so downstream rule runs die with an NPE that `LocalReasonerRunner` **silently swallows**; **#623** — generated records aren't standardized until the sink stage, so propagation stops after one hop; **#621** — string property values are stored double-JSON-encoded, making numeric/date constraints match zero rows.
- **Errors are invisible to operators:** *"no error reaches the client or `docker logs` — the stack trace only lands in `/logs/openspgapp/common-error.log` inside the server container."*
- Stale builder checkpoint directories (`*ckpt*`) **silently skip already-seen records** on re-runs.

For a category whose entire purpose is trustworthy automated inference, **silent failure modes with no client-visible error** are disqualifying without external verification tooling. At v0.8 this is a research-grade component, not production infrastructure.

### 3.4 GUAC

**Release observed:** v1.1.0 (2026-03-13).

GUAC's premise is that the real problem is not scanning but **SBOM sprawl**: thousands of partial, point-in-time SBOMs that cannot be composed. GUAC aggregates them into a graph and enriches nodes with attestations and dependencies, letting you answer "is this artifact affected?" across a whole supply chain.

**Documented limitations:**

- **SBOM sprawl is the stated problem, not solved by it.** GUAC requires ingesting the sprawl first; the cost model is ingestion + graph storage + reasoning.
- **Missing transitive dependencies** remain a known gap in upstream SBOMs; GUAC can only compose what it is given.
- **Point-in-time limitation.** A component snapshot is not a running system. A clean SBOM says nothing about what the deployed binary actually calls.

**Independent accuracy evaluation:** none found. Searches returned only project documentation, the GitHub repository, launch posts, and vendor explainers. The only quantitative GUAC-specific material is a vendor graph-database comparison (ingestion/query benchmarks, no security-accuracy data). **Treat the absence of an accuracy evaluation as a first-order limitation** — see §7.

---

## 4. Version and range matching

### 4.1 Non-semver version strings in the wild

Each of these appears in production inventories, and each defeats naive comparison:

| Form | Example | Where seen |
|---|---|---|
| Git SHA as version | `@ed68ef82c095e0d48ec87eccea555d944a631a4c` | [grype#2606](https://github.com/anchore/grype/issues/2606) |
| Go pseudo-version | `v0.0.0-20230323144144-5bcd846fa16e` | [grype#1245](https://github.com/anchore/grype/issues/1245) |
| Conan revision suffix | `1.3#06023034579559bb64357db3a53f88a4` | [grype#1737](https://github.com/anchore/grype/issues/1737) |
| RPM epoch + release | `1:1.12.20-8.el9` | [dependency-track#3774](https://github.com/DependencyTrack/dependency-track/issues/3774) |
| Alpine apk revision | `3.3.2-r0` | [trivy#7850](https://github.com/aquasecurity/trivy/discussions/7850) |
| Unpinned-development marker | `(devel)` | [syft#4025](https://github.com/anchore/syft/issues/4025) |
| Non-strict semver | `v46` (not `v46.0.0`) | [grype#2606](https://github.com/anchore/grype/issues/2606) |
| Floating tag | `6.0-alpine`, `latest` | [trivy#7850](https://github.com/aquasecurity/trivy/discussions/7850) |

### 4.2 Source-package vs binary-package indirection

Distros publish advisories against the **source** package; inventories observe the **binary** package. Alpine: CVE-2024-9143 is filed under `openssl`, shipped as `libcrypto3`/`libssl3`. This single fact caused a **0-findings** Trivy result on a real vulnerable image ([trivy#7850](https://github.com/aquasecurity/trivy/discussions/7850)) and is the same class of bug that produced Greenbone false positives ([Greenbone forum](https://forum.greenbone.net/t/false-positive-of-cve-2015-8960/18656)). No standard SBOM field reliably carries this mapping.

### 4.3 Backports and vendor-prefixed versioning

The most-cited failure in the corpus, and the reason distro-first advisory selection exists:

- **Trivy** prefers distro advisories over NVD for exactly this reason ([docs](https://trivy.dev/docs/latest/guide/scanner/vulnerability/)).
- **Snyk** makes container advisories rely primarily on distro-provided assessment ([blog](https://snyk.io/blog/snyk-users-dont-have-to-worry-about-nvd-delays/)).
- **Shodan** states it outright: *"If the security patch doesn't change the version number (ex. running an enterprise Linux distribution) then it won't be detected as fixed by Shodan"* ([docs](https://help.shodan.io/mastery/vulnerability-assessment)).
- **Vuls** documents the NVD-side version of this and the PURL-precedence rules used to work around it ([Vuls docs](https://help.vuls.biz/en/manual/scan/cpe/assign_cpe_purl/)).
- **USENIX 2025** identifies backporting as one of three root causes of banner-based FP, alongside inaccurate banner→CPE mapping and incorrect CPE↔CVE association ([paper](https://www.usenix.org/system/files/usenixsecurity25-huang-szu-chun.pdf)).

Distros also ship **vendor-prefixed versions** (`1:1.2.20-8.el9`, `2:1.12.20-8.el9~deb12u1`), which combine epoch, upstream version, revision and distro suffix into a string no generic semver comparator handles.

### 4.4 CPE wildcards: `ANY`, `NA`, SUBSET/SUPERSET

- `version` = `*` (ANY) is how NVD encodes *every* version range → guarantees SUBSET relations during matching.
- `version` = `-` (NA) previously matched every version in Dependency-Track → recurring FPs on every new component version ([#3268](https://github.com/DependencyTrack/dependency-track/issues/3268)).
- Component-side CPEs with a wildcard vendor (`cpe:2.3:a:*:util-linux-setarch:2.37.4`) over-match CVEs with wildcard products (`cpe:2.3:a:pascom_cloud_phone_system:*`) → FPs ([#3178](https://github.com/DependencyTrack/dependency-track/issues/3178)).
- Literal NIST spec compliance is *also* wrong: it discarded 343 of 366 valid matches in testing.

### 4.5 Floating and unbounded ranges

An open-ended range (`< 3.49.1`) says nothing about versions released after the advisory was written. Grype's SQLite incident is the sharpest case: the missing lower bound turned a non-vulnerable 3.24.0 into a false positive. GitHub's `last_known_affected_version_range` field exists for exactly this class of unrepresentable range and is **invisible to plain OSV consumers**.

### 4.6 Missing fix-version data

Grype cannot populate `FIXED-IN` for CVE-2023-45853 / CVE-2022-37434 because neither NVD nor GHSA carries it; CPE-based inference was tried and judged unreliable ([#1764](https://github.com/anchore/grype/issues/1764)). Practically: **a "no fix available" result is not evidence that no fix exists.**

### 4.7 The state of the art is not good

Two 2025 studies bound the ceiling:

- **Affected-version identification, 12 tools, 1,128 real C/C++ vulnerabilities** ([arXiv:2509.03876](https://arxiv.org/html/2509.03876)): **no tool exceeds 45.0% accuracy.** Best (VCCFinder) is 44.9%. Ensembling improves results by up to 10.1% but **overall accuracy still remains below 60%**. Every tool misses part of the affected version set for at least 30% of vulnerabilities. Root causes: heuristic over-reliance, insufficient semantic modelling, inflexible matching. Add-only patches, cross-file changes, and multi-branch development degrade results further.
- **Automated detection of affected libraries** ([Springer, 2025](https://link.springer.com/article/10.1007/s10515-025-00540-6)): LibAlarm, an LLM-based approach, improves F1 by over 14% over baselines and **detects over 40% newly-affected libraries** — i.e. 40% of the problem is finding which libraries are *newly* implicated, not just matching known ones.

Read together: **rule- and version-based matching is capped near 50% accuracy on hard cases; the frontier is semantic/LLM analysis of patch content and code paths.**

---

## 5. Live-network matching (no SBOM, no agent)

### 5.1 Rapid7 Project Sonar

Internet-wide IPv4 scanning underpinning Rapid7's research corpus and product data ([Rapid7](https://www.rapid7.com/research/project-sonar/)). Provides the raw service/version observations that everything downstream consumes.

### 5.2 Shodan — the strongest evidence in this report

**Shodan's own documentation is unusually candid** ([docs](https://help.shodan.io/mastery/vulnerability-assessment)):

- Every banner carries a `vulns` object keyed by CVE, each with a **`verified` boolean**.
- **Unverified** = *"implied based on the metadata we've collected. For example, if a server is running an old version of Apache then we will associate known issues with that version."* Shodan states unverified vulnerabilities *"can have significant false positives"* and *"should be seen as a starting point for further investigation."*
- **Shodan Monitor only sends notifications for verified vulnerabilities.**
- Explicitly acknowledged failure: patched enterprise Linux is never recognized as fixed.

**Independent measurement — USENIX Security 2025, "Trust but Verify"** ([paper](https://www.usenix.org/system/files/usenixsecurity25-huang-szu-chun.pdf)):

| Measurement | Value |
|---|---|
| Shodan payload-based CVEs tracked | 38 (ONYPHE 54; only **8** in common) |
| Shodan banner-based CVEs tracked | **8,199** (ONYPHE 64; only **10** in common) |
| Nuclei-verified FPs among Shodan banner detections | **95%** |
| CVEs where Nuclei contradicts >95% of Shodan banner detections | **18 of 21** |
| CVEs with meaningful agreement | 3 |
| Shodan correct on vulnerable Docker instances | 12 of 19 |
| Shodan correct on non-vulnerable Docker instances | 16 of 24 |
| Shodan payload + banner overlap for the 2 CVEs where it runs both | **zero** |

That last row deserves emphasis: **for the two CVEs where Shodan runs both detection methods, its own "verified" and "unverified" result sets have zero overlap in endpoints — which logically implies a ~100% FP rate for one of them.**

**Failure decomposition** (Shodan's false negatives split cleanly by cause):

- Two FNs where **Shodan had the correct version but did not emit the CVE tag** — a pure binding failure, not a detection failure.
- Two FNs where **Shodan failed to detect the service on the open port at all** — including a service Shodan *does* payload-detect but returned `No information available` for throughout the experiment.
- One FP where a non-vulnerable version shared the same version string as a vulnerable one — the backport problem again.

**Scan cadence is unreliable and materially affects results.** Across nine Jenkins containers, port 50000 received 28 scan results in 7 days while port 8080 received 10; four Apache instances on port 80 were scanned 5, 1, and 2 times respectively. **A point-in-time snapshot of an internet scanner's data has a sampling error that is itself unquantified.**

**Bottom line from the authors:** for Shodan, *"defenders might face massive underreporting of vulnerable endpoints"* via payload methods, *"while for banner-based detections they face massive overreporting."*

### 5.3 Censys

**Vendor benchmark** ([Censys, 2024](https://anchor-u.com/wp-content/uploads/Censys-vs.-Shodan-v2-2024.pdf)) — 300+ honeypots on a staggered activation schedule in Google Cloud:

- **Coverage:** Censys discovered **100%** of honeypot services within one week; Shodan averaged **57%**.
- **Speed:** first 24h — Censys 80.6%–90.2% depending on port, Shodan 12%.
- **Mean time to discovery:** Censys **~12.3 hours**, Shodan **~70 hours** (nearly 6×).

Caveat: vendor-published benchmark of the vendor's own engine. Methodology is sound and directionally consistent with the independent Brazilian study below, but the numbers are not independently audited.

**Independent study** (Ponce et al., 2024, Brazilian internet, [full text](https://exa.ai/library/publication/bcdclpd7w5y)):

- Over a 31-day window: Censys probed **1.7× more** Brazilian devices than Shodan. Split: 44.1% of the 14.9M IPs seen were Shodan-only, 5.5% Censys-only; together they touched **17.2%** of LACNIC space.
- **Shodan probes faster but enriches more:** Shodan mean re-probe interval **5.44 ± 4.07 days** vs Censys **7.60 ± 4.84 days**.
- **Enrichment asymmetry:** Shodan returns ~16 supplementary fields per probe including inferred CPE codes and inferred CVEs. Censys returns ~5, including the inferred product CPE but **not** inferred CVEs.
- **Combining them is strictly better:** merging both engines raised MySQL daily probes from 5,517 to 9,793 (1.8×), and inferring vulnerabilities from engine-reported CPEs against NIST catalog ranges yielded a **1.7× larger vulnerable-host picture on day one** of a CVE's publication.

**Implication:** Shodan and Censys are **complementary in coverage, freshness, and enrichment**. Neither substitutes for the other, and the single-CPE-plus-NVD-range approach is exactly the naive matching §4 shows to be unreliable.

### 5.4 Nmap

Nmap's `vulns` NSE library defines an explicit **vulnerability state model** including `VULNERABLE` and **`LIKELY_VULN`**, the latter documented as the outcome of simple version comparison ([nmap.org](https://nmap.org/nsedoc/lib/vulns.html)).

That state distinction is a quietly important design decision: **Nmap is the only tool in this survey that refuses to collapse "version string looks vulnerable" into "vulnerable."** Credentialed NSE scripts can confirm a vulnerability rather than infer it from a banner. The cost is that Nmap requires network access to each target and produces per-target results with no fleet-wide inventory model.

### 5.5 Nessus / Tenable

- **CPE enumeration plugin 45590** ([Tenable](https://www.tenable.com/plugins/nessus/45590)) performs best-effort *computed* CPE derivation — Nessus does not look up CPEs; it constructs them and matches them. Every §4.4 CPE wildcard defect therefore applies directly.
- Tenable documents software inventory/version enumeration as a distinct capability ([Tenable docs](https://docs.tenable.com/cyber-exposure-studies/software-inventory/Content/DeterminingSoftwareAuthorizationSupport.htm)) — the correct architectural instinct: *identify first, match second*.

### 5.6 OpenVAS / Greenbone

- **CVE-2015-8960 false positive** report, including the backport origin and a record that Greenbone could not honor certain CPE constraints at all ([forum thread, 2024](https://forum.greenbone.net/t/false-positive-of-cve-2015-8960/18656)).
- **CVE-2025-24016 coverage** discussion — whether a newly disclosed CVE was yet in the feed ([forum thread, 2025](https://forum.greenbone.net/t/question-on-cve-2025-24016-coverage/21389)).

The second point is worth isolating: **feed coverage latency is a distinct failure class from matching correctness.** A scanner that would have matched correctly still reports nothing if the advisory is absent. Every scanner inherits its feed's latency, and **no scanner surfaces its own feed-completeness status as a first-class output.**

---

## 6. Cross-cutting synthesis

### 6.1 Why version-only matching cannot be fixed by better version comparison

The very high FP rate holds **even when the SBOM is generated accurately from lockfiles with strong package managers.** The conclusion from that literature is that a perfect SBOM is not the missing piece — the *package-level granularity* of downstream matching is:

> *"We hypothesized that even with a perfect, ground-truth SBOM, the coarse, package-level analysis performed by downstream scanners might still produce unreliable results."*

Function-call analysis pruned the majority of false alarms. Note also that Grype **silently ignored** one library while another scanner did not — the same SBOM produced different component sets from different tools.

### 6.2 The five-layer reliability stack

Ranking layers by how much they degrade end-to-end accuracy, worst first:

1. **Version-range binding** — capped near 45–60% accuracy even with the best 2025 tooling (§4.7).
2. **Identifier binding** — 50%+ vendor-name inconsistency in NVD, 81.4% dictionary underuse, source-vs-binary indirection (§2.1, §4.2).
3. **SBOM fidelity** — SPDX cannot express Go main modules; no standard field for source packages; vendor formats carry strictly more (§3.2).
4. **Feed freshness** — NVD backlog, GHSA unreviewed gap, the April 2026 OSV outage, Greenbone coverage lag (§2, §5.6).
5. **Cross-tool composition** — 50 FPs from one RPM field convention; 0-vs-N findings from one source-package encoding (§1.2, §3.1).

### 6.3 What actually improves accuracy, per the evidence

- **Distro-advisory-first matching.** Unanimous across Trivy, Snyk, Clair, Vuls. Backports make upstream version ranges structurally wrong.
- **Reachability / function-call analysis.** 61.9% FP reduction (Zhou et al.); Doyensec found reachability materially separates tools — and that its absence is why Snyk/Dependabot fell below 15% accuracy outside Java.
- **Payload-based verification over banner inference.** USENIX: payload detections are more accurate for Shodan and ONYPHE; banner detections 95% FP. **Verify, don't infer.**
- **Explicit uncertainty states.** Nmap's `LIKELY_VULN` is more honest than a flat finding list.
- **Enrichment with multiple independent signals.** Beardsley: no single metric suffices — combine CVSS, EPSS, SSVC, Metasploit/Nuclei availability, ATT&CK mapping, and timelines.
- **Multiple independent network sensors.** Censys + Shodan combined: 1.8× coverage, 1.7× faster vulnerable-host picture.

### 6.4 Architectural guidance for anyone building on this stack

*Reconstructed from §6.3 and the tool-specific findings above; the subagent's original §6.4/§6.5 text was truncated and is not reproduced verbatim.*

1. **Carry a confidence tier per finding.** Separate "advisory says this range matches the observed string" from "verified exploitable." Almost nothing in the 2026 tool landscape does this, and the USENIX result shows the conflation costs ~95% FP.
2. **Never let a scanner's output be the only record.** Docker Scout's stored CVE list is not portable; `.trivyignore` does not survive to the server; GHSA unreviewed entries do not reach OSV. **Preserve the raw inventory and re-derive findings**, so that a fix to the database can be replayed.
3. **Model provenance per fact, not per finding.** Each observation should carry how it was obtained (banner / manifest / dpkg / API / probe) and each match should carry which advisory source and which range representation produced it. Without this, a wrong answer cannot be localised to the layer that produced it.
4. **Track feed freshness as a first-class output.** Every scanner inherits its feed's latency invisibly (§5.6). Exposing "last successful ingest per source, per ecosystem" is a cheap, high-value differentiator that no tool in the survey provides.
5. **Treat normalisation as its own component with its own test suite.** Identifier problems (§2.1) and version-string problems (§4.1) are where most false positives originate, and they are testable independently of any CVE database.
6. **Represent "unknown" explicitly.** A version string that cannot be parsed, an advisory with no range, an asset with no banner — these are the three states that most systems silently coerce into a false "not vulnerable." Nmap's `LIKELY_VULN` is the precedent for doing better.
7. **Make suppression global and portable, not per-project.** The Dependency-Track finding (#5992) shows the current model forces re-suppression of an ecosystem-wide bad mapping once per project per version.

---

## 7. Research gaps identified by this survey

Explicitly recorded so the project's claims are not overstated and so these are addressable as contributions.

1. **No independent accuracy evaluation of GUAC exists.** Only project documentation, launch posts, and vendor explainers were found. The only quantitative material is a vendor graph-database benchmark with no security-accuracy data.
2. **No peer-reviewed precision/recall measurement for OSV-Scanner itself.** Third-party consumers are measured against OSV data, which makes OSV correct by construction.
3. **No peer-reviewed publication of OpenSPG in a vulnerability-management knowledge-graph context.** If the project builds on it, that is an engineering choice, not an evidence-backed one.
4. **No PURL accuracy measurement at NVD/CVE scale.** The nearest work supplies an (ecosystem, component, version, vuln-id) benchmark but uses OSV coordinates as its reference and does not quantify identifier-normalisation loss — even though PURL is what OSV and GUAC use natively.
5. **No absolute ground truth for asset discovery.** Only one sector-specific study (Dutch municipalities) establishes true ground truth, for one country.
6. **CERT/ICS-CERT feed structure and latency were not characterized** in this pass.
7. **No retrieved study reports end-to-end results for a discovery-to-CVE pipeline.** Components exist in isolation — asset discovery, version binding, range matching, prioritisation — but no published work measures the composed system's precision and recall. **This is the gap the project targets.**
