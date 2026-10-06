# Academic Literature Review — Automatic CVE Checking for Entire Infrastructure

**Project context:** Final-year undergraduate cybersecurity project — an automatic CVE checker covering an entire infrastructure (not just source code or a single SBOM), i.e. it must discover assets, identify what software/versions are actually running, map those to CVE/CPE/PURL records, and prioritise findings.

**Date of search and verification:** All URLs below were checked on **2026-10-01**. Every entry is marked **VERIFIED** (I retrieved the source itself — full abstract, PDF text, or publisher page) or **UNVERIFIED** (only metadata, an abstract snippet, or a third-party description was retrieved; the primary document was not opened). No paper, DOI, author name, or number appears here unless it appeared in retrieved content.

**Method:** Deep web search plus direct retrieval against arXiv, USENIX, ACM DL, IEEE, Elsevier/ScienceDirect, MDPI, IEICE/J-STAGE, Springer/CEUR, Semantic Scholar-indexed venues, CISA and NTIA publications, OpenSSF, and OASIS. Where a source was only visible as a search snippet, it is marked UNVERIFIED rather than presented as confirmed.

---

## Executive summary (the 9 findings that matter most for this project)

1. **Package-level CVE matching is the dominant source of false positives, not SBOM inaccuracy.** Zhou et al. (2025/26) built SBOMs that were verified correct against lock files, then manually validated scanner output and found a **92.0% false positive rate** (9 true positives out of 113 findings). Root cause: vulnerable functions in unreachable code.
2. **Different scanners barely agree.** Boles et al. found Trivy and Grype agreed on vulnerability *count* in only 15.3% of 927 Docker images (9.2% of images that actually contained vulnerabilities). Churakova et al. measured a maximum pairwise Jaccard similarity of 0.694 across seven VEX-generating tools.
3. **EPSS is a trailing indicator, not a predictive one.** Parla found that of 57 CVEs from 2023+ later added to CISA KEV, **42 had consistently low EPSS** before inclusion; across all 250 KEV entries in her window, more than two-thirds sat below EPSS's own 36% threshold at the moment of inclusion. Koscinski et al. independently found **fewer than 20% of KEV CVEs received a high-confidence EPSS score before exploitation was public.**
4. **EPSS recall is structurally capped, not a model-quality problem.** Gordeychik found only ~83% of 2025 KEV additions had *any* EPSS score at decision time; recall against KEV was 65% at τ≥0.001 and 27% at τ≥0.1. Increasing patch capacity cannot compensate for a missing or late signal.
5. **CPE identification is fundamentally unreliable at scale.** VERNIER measured only **20.3%** character-level exact match between NVD and other vulnerability databases; intra-NVD consistency between structured CPE and unstructured descriptions was **11.5%**. VulCPE found **50.18%** of vendor names in NVD CPEs are inconsistent.
6. **Banner-based CVE detection is close to worthless.** Huang et al. (USENIX Security '25) verified with Nuclei templates: **over 95% of Shodan's banner-based CVE detections were false positives.** Payload-based detections were mostly accurate but suffered severe underreporting — **52.07% of confirmed-vulnerable endpoints were not reported at all.**
7. **Asset-to-owner attribution is lossy and noisy, and it distorts the numbers you report.** Angelova et al. (WEIS 2026) compared WHOIS-derived IP ranges for Dutch municipalities against self-reported ranges: **58% recall, 62% false positives**, and — critically — **94% of the "vulnerabilities" in the public data came from addresses the municipalities do not own**, i.e. ~94% overestimation of vulnerable hosts.
8. **VEX adoption is an unsolved distribution and trust problem,** not a technical one — the industry report explicitly concludes adoption is "cultural."
9. **LLM/agentic triage works but degrades sharply outside binary questions.** VEX-Bench: ~80% F1 on affected/not-affected, but only GPT-5.5 exceeded 70% macro-F1 on *justification* (§6.1). On false-positive suppression for code alerts, all three agent frameworks (Aider, OpenHands, SWE-agent) started above 92% and the best configuration reached 6.3%, with gains **entirely backbone-dependent** (§6.3).

---

## 1. Empirical accuracy of CVE/SBOM-based matching

### 1.1 Zhou, Dacier & Konstantinou — "A Reality Check on SBOM-based Vulnerability Management" — **VERIFIED**
- **Authors:** Li Zhou, Marc Dacier, Charalambos Konstantinou
- **Venue/Year:** arXiv preprint cs.CR, v1 25 Nov 2025, v2 17 Apr 2026. Related ACM DOI 10.1145/3800506.3803490.
- **URL:** https://arxiv.org/abs/2511.20313 (abs page retrieved directly; full text also retrieved from https://arxiv.org/html/2511.20313v2)
- **Findings:** 2,414 open-source repositories across four languages. Lock files from strong package managers produce *consistent and accurate* SBOMs; measured SBOM accuracy against lock-file ground truth reached **78.6%** with Syft and Trivy agreeing on identical output per input file. Using those high-fidelity SBOMs, Grype and Trivy together produced **113 findings across four repositories of which only 9 were true positives — a 92.0% false positive rate.** Function-call (reachability) analysis pruned **61.9%** of those false alarms, cutting alerts from 113 to 42.
- **Limitations:** The 92.0% figure comes from manual validation of only four repositories, so it is a case study rather than a population estimate. Authors note it is "systemic" not an implementation defect. Their 61.9% pruning is a proof-of-concept static function-call analysis, not a production-grade reachability engine; CVE-bin-tool is noted as having the same coarse package-level granularity problem.
- **Relevance to this project:** This is the single most important paper for justifying why an infrastructure-wide CVE checker needs asset-context reasoning rather than pure version matching. The authors also explicitly blame the academic literature for using project manifest files (`requirements.txt`) instead of lock files, which "inevitably" yields erroneous results — a methodological trap this project should avoid repeating.

### 1.2 Churakova, Ekstedt & Schmid — "Vexed by VEX tools: Consistency evaluation of container vulnerability scanners" — **VERIFIED**
- **Authors:** Yekatierina Churakova, Mathias Ekstedt, Larissa Schmid (KTH)
- **Venue/Year:** arXiv:2503.14388, v1 Mar 2025, v3 26 Mar 2026
- **URL:** https://arxiv.org/abs/2503.14388 (abs page retrieved directly; full text from https://arxiv.org/html/2503.14388v2 and v3)
- **Findings:** Seven VEX-generating tools evaluated on container image datasets (Trivy, Grype, DepScan, Docker Scout, OSV, Vexy, Snyk). Maximum pairwise Jaccard similarity across all tools: **0.694** (Trivy vs Grype). Restricting to CVE-only identifiers raised the best pair to **76%**. Vexy vs Snyk scored **0%**. Overall similarity across all seven tools: **0%**. Same-tool direct-image-scan vs native-SBOM-scan still only reached 86.7% (DepScan). The authors **rule out SBOM quality** as the explanatory factor (scanning the *same* SBOM with different tools still gave ≤70% agreement). **Pearson correlation between vulnerability-database overlap and report similarity = 0.88** — the dominant driver is which database each tool queries. A worked example: GHSA-q2x7-8rv6-6q7h is expressible as GHSA, as CVE-2024-56326, and as SNYK-CHAINGUARDLATEST-LOCALSTACK-86792 with no direct SNYK↔CVE mapping available.
- **Limitations:** Measures *consistency* (agreement), not correctness — the authors state explicitly "our study does not address the challenge of false positives and negatives," and that inconsistency "is not, by definition, a bad thing." Only container images. Vexy's low similarity is unexplained (narrow data sources vs strict validation, left open).
- **Relevance:** Establishes that a checker cannot rely on any single scanner or any single vulnerability database, and that identifier-space normalisation is a first-class engineering problem.

### 1.3 O'Donoghue, Boles, Izurieta & Reinhold — "Impacts of Software Bill of Materials (SBOM) Generation on Vulnerability Detection in Docker Images" — **VERIFIED**
- **Authors:** Eric O'Donoghue, Brittany Boles, Clemente I. Izurieta, Ann Marie Reinhold (Montana State University)
- **Venue/Year:** SCORED 2024 (Secure Computing Research Data / conference proceedings)
- **URL:** https://www.cs.montana.edu/izurieta/pubs/SCORED2024.pdf (full PDF text retrieved). Author list and date corroborated at https://exa.ai/library/publication/gqjwvrgm9hv
- **Findings:** Four SBOM corpora built from 2,313 Docker images by crossing generator (Syft, Trivy) with format (CycloneDX 1.5, SPDX 2.3), then analysed with Trivy, Grype, and CVE-bin-tool. Reported vulnerability counts are dominated by *which vendor's* generator and analyser are combined. With Trivy as analyser over CycloneDX 1.5, only **12%** of SBOMs yielded the same vulnerability count regardless of generator; the mean difference between Trivy-generated and Syft-generated SBOMs was **302.50** vulnerabilities, with per-image differences from **94 fewer to 5,456 greater** (SD = 670). In SPDX 2.3, only **7%** agreed. With Grype over CycloneDX 1.5 only **2%** agreed; Syft-generated SBOMs yielded on average **441.57** more findings than Trivy-generated ones (range 13 fewer to 7,336 greater, SD = 782). CVE-bin-tool was far more stable (**52%** agreement in CycloneDX 1.5, 34% in SPDX 2.3) but also reported far fewer vulnerabilities.
- **Limitations:** No ground truth — the authors list "validation of the SBOMs being generated" as future work, so all results are *relative* disagreement, not accuracy. SBOM format effects were mostly not practically significant once vendor mismatches were accounted for (only one combination reached practical significance). Statistical significance was assessed per-image, which conflates SBOM variation with image complexity.
- **Relevance:** Quantifies the "same artefact, different answer" problem that any multi-tool infrastructure checker must reconcile.

### 1.4 Benedetti et al. — "The Impact of SBOM Generators on Vulnerability Assessment in Python: A Comparison and a Novel Approach" — **VERIFIED**
- **Authors:** Giacomo Benedetti et al. (academic homepage; full author list not captured in retrieved content — **partial**)
- **Venue/Year:** ACNS 2025 (Applied Cryptography and Network Security)
- **URL:** https://giacomobenedetti.github.io/files/acns25.pdf (full PDF text retrieved)
- **Findings:** Ground truth = `pip-audit`; analyser = Grype. Results for five SBOM generators plus their own PIP-sbom:

| Generator | Jaccard | Avg Precision | Avg Recall | FP / FN |
|---|---|---|---|---|
| cdxgen | 49.77% | 17.08% | 21.42% | 978 / 5 |
| ORT | 36.50% | 16.31% | 19.93% | 449 / 10 |
| Syft | 26.33% | 12.39% | 15.61% | 926 / 21 |
| Trivy | 23.63% | 12.17% | 14.01% | 893 / 21 |
| GH-sbom | 23.98% | 5.57% | 8.10% | 2793 / 29 |
| **PIP-sbom (theirs)** | **78.39%** | **80.95%** | **80.26%** | **47 / 3** |

  The best existing tool (cdxgen) misses ~99.5% of its misclassifications as false positives (978 FP vs 5 FN). Two causes identified by sampling: SBOMs list dependencies present as metadata files but never actually installed, and vulnerability identifiers differing from ground truth.
- **Limitations:** Explicitly acknowledged — `pip-audit` as ground truth may itself miss vulnerabilities, though the authors argue simultaneity of measurement mitigates this. Python-only. Ground truth is itself a tool, not verified reality.
- **Relevance:** Precision of 12–17% for mainstream SBOM→scanner pipelines is a directly citable number for justifying added infrastructure context in the project.

### 1.5 Mandl, Mandl, Häusl & Auch — "A Ground-Truth-Based Evaluation of Vulnerability Detection Across Multiple Ecosystems" — **VERIFIED**
- **Authors:** Peter Mandl, Paul Mandl, Martin Häusl, Maximilian Auch
- **Venue/Year:** arXiv:2604.21111 (cs.SE, cs.CR), submitted 22 Apr 2026
- **URL:** https://arxiv.org/abs/2604.21111 (abs page retrieved directly; result tables retrieved from https://arxiv.org/pdf/2604.21111). Dataset record: https://zenodo.org/records/19696658
- **Findings:** Curated OSV-derived ground truth mapping advisories to explicit (ecosystem, component, version, vuln-id) tuples: **1,000 OSV entries, 430 distinct components, 924 CVE-backed findings (189 distinct CVEs)** across Maven, npm, NuGet, PyPI. Five detectors fed identical package/version inputs. Headline results (recall = TP/(TP+FN), overlap = TP/(TP+FP)):

| Tool | Total recall | Total overlap |
|---|---|---|
| Trivy | **0.96** | **0.78** |
| GitHub Advisory Database | 0.95 | 0.54 |
| OWASP Dependency-Track | 0.91 | — |
| Snyk | 0.90 | — |
| Sonatype OSS Index | 0.61 | 0.80 |

  Per-ecosystem: Maven — Dependency-Track 1.00, Trivy 0.96, GitHub 0.93, Snyk 0.82, OSS Index 0.54. PyPI — Snyk 0.95, Trivy 0.94, GitHub 0.86, OSS Index 0.78, Dependency-Track 0.69. NuGet — Snyk and GitHub 1.00. Significance: Cochran's Q = 1452.81, p < 0.001; McNemar pairwise with Holm correction left only two non-significant pairs — GitHub vs Trivy (p_adj = 0.104) and Dependency-Track vs Snyk (p_adj = 0.642). A three-tier structure emerges: GitHub+Trivy strongest, Dependency-Track+Snyk middle, OSS Index significantly weaker.
- **Limitations:** The reference *is* OSV, so OSV itself is perfect by construction and the comparison is partly self-referential. The dataset is a point-in-time snapshot; the authors state this explicitly and release a reconstruction tool because CVE data decays. Recall here is "can the tool find this (component, version) tuple" — it says nothing about whether the tuple is actually deployed or the vulnerable code reachable.
- **Relevance:** The recall/overlap trade-off table is the best available quantitative argument for **ensemble design** — GitHub maximises coverage at the cost of ~3× the false positives of Trivy.

### 1.6 Boles, O'Donoghue, Izurieta, Reinhold et al. — "Deciphering Discrepancies: A Comparative Analysis of [Trivy and Grype]" — **VERIFIED**
- **Authors:** Brittany Boles et al. (Montana State University); filename indicates Boles as first author. Full author list not captured — **partial**.
- **Venue/Year:** Preprint / conference paper (venue not confirmed in retrieved content — **partial**)
- **URL:** https://fdn.montana.edu/cyber/products/Grype_Vs_Trivy_Boles_et_al.pdf (full PDF text retrieved)
- **Findings:** 927 Docker images. Trivy reported **473,661** vulnerabilities; Grype **603,259**. Grype reported more in **84.6%** of images. They agreed on the *count* in only **15.3%** of images (142/927); of the 865 images that contained any vulnerability, the counts matched in only **9.2%** (80 images). Critically: **"even when Trivy and Grype reported the same number of vulnerabilities, the identities of the vulnerabilities (e.g., CVE IDs) never agreed. The only instance where the tools were unanimous in their findings was when they both found nothing."** Largest single divergence: `python:3.7.6-stretch`, Trivy 3,208 vs Grype 5,724. On average Trivy reported ~140 fewer (SD = 357.0); in 6.7% of images the gap exceeded 500. The tools disagreed on severity **60,799** times for identical CVE IDs (e.g. CVE-2019-17594 'medium' vs 'low'; CVE-2019-8457 'negligible' vs 'critical'). Trivy reported DLA/DSA/NSWG IDs that Grype never did; Grype reported ELSA/ALAS that Trivy never did. Only 675 double-counting instances across 603,259 Grype findings, so double counting is *not* the explanation.
- **Limitations:** Single vendor pair, Docker images only, and the authors explicitly do not claim to determine which tool is right — they conclude underlying vulnerability-database inaccuracies are the shared root cause and advocate a consolidated graph database (i.e. GUAC-like) as the remedy.
- **Relevance:** This is the strongest available justification for building an infrastructure-wide correlation layer rather than running a scanner.

---

## 2. SBOM quality, completeness and trustworthiness (including VEX)

### 2.1 Zhou et al. (2025/26) — see §1.1 — **VERIFIED**
Explicitly states "even these accurate SBOMs are **not a silver bullet** for vulnerability management," and that coarse package-level granularity means "a package may include a large number of functions, and the presence of a single vulnerable function can result in the entire package — and by extension, the software — being flagged as vulnerable, even if the function is never invoked."

### 2.2 NTIA / McAfee — "Myths and Reality of an SBOM" — **VERIFIED** (PDF text extracted via search; primary PDF not separately fetched)
- **Year:** 2021 (NTIA public comment document)
- **URL:** https://www.ntia.gov/sites/default/files/publications/mcafee_-_2021.06.17_0.pdf
- **Findings:** Argues SBOMs **"are not a silver bullet"** and should be an authoritative source rather than an all-purpose solution. Specific weaknesses named: (a) **Depth** — complete transitive dependency graphs are often infeasible; SBOMs should explicitly declare "known unknowns" so consumers can distinguish "no dependencies" from "unknown dependencies"; (b) **Legacy/binary-only software** — source may not be obtainable, so generation depends on trusting a third party (NIST/NSRL), and *"It does no one any good if you cannot trust the information in an SBOM"*; (c) **Integrity and authenticity** — SBOMs should be digitally signed with producer keys and contain per-component hashes; (d) **Threat model overreach** — *"Can an SBOM file solve all the ills of the software supply chain? The answer to that question is NO."* Attempts to make SBOM the substrate for detecting internal supply-chain compromise are called "overreach."
- **Limitations:** A stakeholder position paper from 2021, not an empirical study, and predates CycloneDX/SPDX 3.0. Its argument that full transitive depth makes SBOMs "nearly unreadable and massive in size" is a design opinion that later work (GUAC, SBOMit) disputes.
- **Relevance:** Useful for the project's problem statement — the "known unknowns" concept maps directly to reporting *unknown asset inventory* alongside known CVE matches, which is a defensible output for an infrastructure-wide checker.

### 2.3 CISA — "Software Transparency in SaaS Environments" — **VERIFIED** (PDF text extracted via search)
- **Year:** 2024
- **URL:** https://www.cisa.gov/sites/default/files/2024-05/Software%20Transparency%20in%20SaaS%20Environments.pdf
- **Findings:** For infrastructure the project cannot see (SaaS/managed services), SBOMs do not apply. Four structural barriers: continuous deployment invalidating composition data; mitigation at the perimeter rather than in software; **blurred technical boundaries** — "No widely accepted definition exists as to the appropriate horizontal or vertical extent of software composition data," so per-vendor component inventories are not comparable; and opacity of implementation. Concludes: *"Even for non-SaaS software, SBOMs are not a silver bullet, and they never claimed to be."* Transitive service dependencies are acknowledged as important (Log4Shell cited) but not mature enough to standardise.
- **Limitations:** Policy/analysis document, not peer-reviewed. SaaS-centric scope.
- **Relevance:** Directly relevant if "entire infrastructure" includes cloud/managed services — argues the checker must report *visibility gaps* explicitly rather than silently produce a short CVE list.

### 2.4 Tate et al. (PNNL) — "Comparing Bills of Materials" — **VERIFIED**
- **Venue/Year:** Pacific Northwest National Laboratory technical report
- **URL:** https://www.pnnl.gov/sites/default/files/media/file/Comparing%20Bills%20of%20Materials%20Tate.pdf
- **Findings:** Enumerates why BOMs cannot currently be compared reliably: (a) **standards and versions** — SPDX and CycloneDX have lossy mapping between them, and even minor version bumps change BOM content; (b) **SBOM types** — a source SBOM (from source code) looks completely different from a build SBOM (specific release), and *"two SBOMs for the same software can be markedly different"*; (c) **naming conventions** — CPE and PURL aid machine readability but diverge from colloquial usage; *"MSFT", "Microsoft Corporation", and "Microsoft" are all defensible values but the inconsistent recording makes systematically disambiguating them difficult"*; (d) **hashing** — MD5/SHA-family hashes are susceptible to embedded timestamps and do not convey *why* files differ. Final judgement: **"There is no single method of comparison that can effectively compare BOMs today."**
- **Limitations:** Introductory/position paper, no empirical measurement. Hardware BOM discussion is out of scope for this project.
- **Relevance:** The SBOM-type distinction (source vs build) is a genuine correctness trap: an infrastructure checker reading an SBOM from a different build than the running artefact will produce wrong CPE matches.

### 2.5 OpenSSF / OASIS — "Signal in the Noise: An Industry-Wide Perspective on the State of VEX" — **VERIFIED**
- **Year:** Published December 2025 (OASIS Open), mirrored by OpenSSF January 2026
- **URLs:** https://www.oasis-open.org/2025/12/22/signal-in-the-noise-an-industry-wide-perspective-on-the-state-of-vex/ and https://openssf.org/blog/2026/01/08/signal-in-the-noise-an-industry-wide-perspective-on-the-state-of-vex/
- **Findings:** Structured interviews with Amazon, Anchore, Aquasec, Chainguard, Cisco, Debian, Ericsson, Freexian, Google, Microsoft, Red Hat, and OpenSUSE. Core judgement: **"VEX feels more like a promise than a practice."** Specific blockers: (1) **distribution** — "There's no common lookup system, and trust is uneven. Today, every organization distributes VEX differently"; (2) **trust** — no converged standard for signing/verifying across formats; enterprise trust is currently "based on where the file is hosted rather than cryptographic proof," which limits aggregation hubs; (3) **tooling** — CSAF is expressive but its "official checkers were reported to miss logical errors," forcing OpenSUSE and Debian to build in-house tools, whereas OpenVEX's tooling-first approach lowered the barrier in Go; (4) **lifecycle mismatch** — SBOMs are build-time snapshots, VEX changes whenever status changes, and embedding VEX inside CycloneDX/SPDX is "limited" in practice; (5) **culture** — "Most open-source maintainers don't see a reason to publish VEX statements. Some vendors treat VEX as a premium feature... Adoption isn't just a technical challenge; it's cultural."
- **Limitations:** Not peer-reviewed. The report itself states the insights "largely reflect the perspectives of the enterprise and vendor interviewees... this does not represent an exhaustive audit of all VEX implementations or the wider open-source ecosystem." Qualitative, no quantitative adoption rates.
- **Relevance:** The strongest single citation for arguing that VEX cannot be assumed as an input to an infrastructure-wide checker — it is adoption-limited, trust-unsettled, and incompletely distributed.

### 2.6 DiVA thesis — "Investigation of VEX Usage in Open Source Repositories" — **VERIFIED**
- **Venue/Year:** Master's thesis, DiVA (Swedish University repository), 2026
- **URL:** https://www.diva-portal.org/smash/get/diva2:2073107/FULLTEXT01.pdf (full PDF text retrieved)
- **Findings:** Quantifies the research gap: Google Scholar returns ~215 results for "VEX AND SBOM" versus ~6,140 for "SBOM" (as of 2026-04-03) — VEX is barely studied independently. Dataset built via GitHub Code Search across four specifications. **CycloneDX is the most widespread (300+ repositories) but only ~half of the files found report a vulnerability and only ~30% of files specify a status for it** — the authors suggest most CycloneDX documents found are VDRs, not VEX. CSAF has the greatest number of files, predominantly machine-generated by Red Hat Product Security. Commit cadence (maintenance frequency): **OpenVEX every ~10 days, CycloneDX ~every 2 months, CSAF ~every 4 months.** ~52% of CycloneDX VEX statements were AFFECTED; FIXED was most common elsewhere. SPDX yielded only 22 files, several of which were the specification's own schema, and none contained VEX statements.
- **Limitations:** Thesis, not peer-reviewed. **Serious coverage caveat the authors disclose:** GitHub Code Search caps at 1,000 results per query, limits searching to 4,000 repositories, only indexes the default branch, and only files under 384 KB. Additionally, 716 of 1,642 analysed commits (**43.61%**) could not be determined to be direct VEX updates, so commit-frequency numbers are heuristic.
- **Relevance:** Quantifies that VEX content in the wild is sparse — roughly 30% status coverage in the most common format. A checker consuming VEX must handle absence.

### 2.7 Sahay et al. (NYU Secure Software Lab) — "Over the Shoulder: Improving SBOM Accuracy by Watching the Build" — **VERIFIED**
- **Venue/Year:** SCORED 2026
- **URL:** https://ssl.engineering.nyu.edu/papers/sahay_sbomit_scored_2026.pdf (full PDF text retrieved)
- **Findings:** Introduces **SBOMit**, an OpenSSF project that generates/enriches SBOMs from evidence captured *during* the build using eBPF (`witness-ebpf`) rather than retrospective static analysis of binaries. Evaluated across **98 CNCF projects** with a **median runtime overhead of 8.1%** and no source modifications required. Identifies build inputs and contexts that static SCA methods fail to recover. Uses ITE-6 attestations (DSSE layer, subject layer, predicate layer) that remain first-class in-toto outputs reusable by other policy tooling, and can be re-analysed later without re-running the build.
- **Limitations:** Requires build-environment control — fundamentally inapplicable to third-party appliances and legacy binaries, which is exactly the "entire infrastructure" case. Overhead measured on CNCF (container-native) projects only. eBPF is Linux-kernel-specific.
- **Relevance:** Establishes the ceiling for SBOM accuracy where builds are observable, and by contrast the difficulty where they are not (i.e. most infrastructure assets).

### 2.8 Torres-Arias et al. (NYU) — "in-toto: Providing farm-to-table guarantees for bits and bytes" — **VERIFIED**
- **Venue/Year:** USENIX Security 2019
- **URL:** https://ssl.engineering.nyu.edu/papers/torres-toto-usenix19.pdf
- **Findings:** Analyses 30 software supply chain compromises affecting hundreds of millions of users and shows in-toto deployments could address **83%–100%** of historical supply chain attacks depending on which keys were compromised. Used in production by Datadog and Control Plane (>8,000 cloud deployments) and by Debian for reproducible-build verification.
- **Limitations:** Security properties degrade partially on key compromise — explicitly "not a 'lose-one, lose-all' solution." Addresses integrity of the chain, not inventory accuracy.
- **Relevance:** The 83–100% figure is the counterpoint to the plain-SBOM figure below and supports the thesis that provenance, not inventory, is where the real coverage lies.

### 2.9 Reported "plain SBOM prevents ~10% of supply chain attacks" claim — **UNVERIFIED**
- **URL encountered:** a LinkedIn post summarising an NYU analysis (https://www.linkedin.com/posts/thecolekennedy_sboms-data-analysis-activity-7252686307175337985-coz7)
- **Claim as retrieved:** plain SBOM ≈ 10% coverage of historical supply chain attacks; signed SBOM ≈ 35%; SLSA/in-toto simple case ≈ 51%; in-toto + SBOM ≈ 51%; SBOM generated from in-toto metadata ≈ 87%.
- **Status:** **I could not locate the primary publication.** Only a secondary social-media summary was retrieved. The underlying NYU/Benevolus-area study was not found in arXiv, USENIX, ACM DL, or elsewhere in my searches. Do not cite these percentages without independently obtaining the source. This is a genuine gap (see §"What I could not find").

---

## 3. CPE / PURL identification weaknesses

### 3.1 Dong et al. — "Towards the Detection of Inconsistencies in Public Security Vulnerability Reports" (VIEM) — **VERIFIED**
- **Authors:** Dong et al. (referred to in later literature as Dong, Zhang-type work; full author list not captured — **partial**)
- **Venue/Year:** USENIX Security 2019 (sec19)
- **URL:** https://www.usenix.org/system/files/sec19-dong.pdf (full PDF text retrieved)
- **Findings:** Dataset of **78,296 CVE IDs** and **70,569 vulnerability reports** spanning ~20 years. Custom NER + relation-extraction models reach **0.941 precision / 0.993 recall** on ground truth. Consistency results, aggregated at report level: **only 59.82% of vulnerability reports / CVE summaries strictly match the standardised NVD entries**; loose matching reaches 90.05%. At the more granular name-version pair level, 78.32% strict / 93.49% loose. Critically, **inconsistency increases over time.** Case studies confirm NVD both overclaims and underclaims affected software versions.
- **Limitations:** The ~20% of CVE IDs with multiple software names are handled conservatively (a report counts as strict-match only if *all* name-version pairs match), which understates per-pair accuracy. Matching uses a heuristic ("matched words ≥ unmatched words"). Data ends ~2019.
- **Relevance:** ~40% strict mismatch between NVD and reality is the headline number for "you cannot trust NVD's version ranges."

### 3.2 VERNIER — "Inconsistent measurement and incorrect detection of software names in security vulnerability reports" — **VERIFIED**
- **Authors:** Not captured in retrieved content — **partial** (author list not obtained)
- **Venue/Year:** Information & Software Technology (Elsevier), article S0167404823003875
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0167404823003875 (abstract and extensive highlights retrieved)
- **Findings:** Measures inconsistency across **789,954 sets of software names from 9 vulnerability databases** (CVE, NVD, ExploitDB, SecurityFocus, Openwall, SecurityFocus Forum, CNNVD, CNVD, RNVD), 1999–2019. **NVD vs other mainstream databases: average exact-match rate only 20.3% at character level and 43.3% at semantic level** — i.e. up to 79.7% of CVE IDs have inconsistent software names across databases. More damaging, *intra*-database inconsistency also pervasive: **structured CPE vs unstructured software names inside the same database (NVD, CNNVD, CNVD) match only 11.5% (character) and 42.0% (semantic)**. NER component: accuracy 99.5%, F1 95.1% on 21,000 manually annotated descriptions. A reward-penalty-matrix tool was built to detect and correct incorrect names, and problems were reported to NVD, CVE, CNNVD, CNVD maintainers.
- **Limitations:** Software *names* only — does not measure version-range correctness. Datasets end 2019. Relies on NER extraction quality (mitigated by the 95.1% F1). Cross-database comparison involves a mix of English- and Chinese-language databases, which may not generalise.
- **Relevance:** **This is the strongest citation for the project's core problem.** An 11.5% internal match rate means even a single-source NVD-only checker is internally inconsistent. Any infrastructure checker needs multi-source corroboration and name normalisation, which is precisely what GUAC (§5) and VulCPE do.

### 3.3 VulCPE — "Context-Aware Cybersecurity Vulnerability Retrieval and Management" — **VERIFIED**
- **Venue/Year:** arXiv:2505.13895
- **URL:** https://arxiv.org/html/2505.13895 (full HTML text retrieved)
- **Findings:** Systematic analysis of 259,233 NVD entries from 2002 to 31 Aug 2024, filtering Rejected entries to 244,819 vulnerabilities, parsing **1,327,827 CPE strings** from the CPE v2.3 dictionary. Results: **93.55%** of NVD entries contain at least one valid CPE string; **81.40% of all defined CPE strings are never referenced in NVD** (massive under-utilisation of the identifier space); **14.56%** of NVD entries rely on configuration-specific CPEs requiring logical AND/OR parsing. **Vendor name inconsistencies: 50.18% in NVD CPEs and 47.07% in CVEdetails** (65,482 inconsistent name instances consolidated into 32,420 vendor clusters out of 67,925 vendor names). Format variations alone affected 29,664 groups / 59,424 instances. Even within "consistent" vendors, **70,026 of 225,192 product names (31.09%)** are affected by formatting variations. Explicitly extends Anwar et al. (2020), who found 1,835 inconsistent vendor names across 871 groups — a 35× improvement in coverage. Their system achieves retrieval precision **0.766** (average 72.6%) and coverage **0.926**, versus NVD keyword matching at up to 95.4% coverage but far lower precision.
- **Limitations:** Precision of 0.766 is still low in absolute terms. The Shared Product Ratio threshold was introduced because acronym/substring heuristics produced false pairings during manual validation — i.e. the normalisation itself introduces error. Evaluated on vulnerability *retrieval*, not on real infrastructure.
- **Relevance:** Provides both the diagnosis (half of vendor names are inconsistent) and a working mitigation (unified CPE schema + entity recognition + relation extraction + graph modelling) — the same architecture the project would need.

### 3.4 CPE-Identifier — "Automated CPE identification and CVE summaries annotation with Deep Learning and NLP" — **VERIFIED**
- **Venue/Year:** arXiv:2405.13568
- **URL:** https://arxiv.org/html/2405.13568 (full HTML text retrieved)
- **Findings:** Automated CPE extraction from CVE summaries. Best model (BERT, from BERT/XLNet/GPT-2 comparison): **F1 95.48%, accuracy 99.13%, precision 94.83%, recall 96.14%**, stated as >9% better than prior automated CVE–CPE labelling work on all metrics. Also automates the *labelling* of training data: a fine-tuned BERT annotator reached **accuracy 98.73%, F1 95.64%**, labelling **169,092 CVE summaries in 2 hours**.
- **Limitations:** Extracts CPEs *from text* — this solves NVD curation lag, not asset-to-CPE matching, which is the project's actual problem. Notes that Wareus et al. restricted to the top-80% most common CPE product/vendor names, "discouraging the prediction of those rare CPE entities... compromises the generality of the model." Collapses `application`, `hardware`, `os` labels into `product`.
- **Relevance:** Marginal for this project; useful if the project intends to ingest raw CVE text.

### 3.5 Wareus et al. — "Automated CPE Labeling of CVE Summaries with Machine Learning" — **VERIFIED**
- **Venue/Year:** Peer-reviewed article, PMC7338193
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC7338193/ (full text retrieved)
- **Findings:** BiLSTM + CRF with word/character embeddings, casing features, and a security lexicon. **F-measure 0.8604, precision 0.8571, recall 0.8637.** Crucially, the *whole-CVE* accuracy (every CPE in a summary correctly predicted) is only **0.6744 (67.44%)**; restricting to vendor+product only raises it to 0.7772. Reports the **median lag of 35 days (2018) from CVE disclosure to correct CPE assignment.** Structural facts about NVD CPEs: **81.9% specify only one of {version, versionStartExcluding, versionStartIncluding, versionEndExcluding, versionEndIncluding}; 14.5% have no version range at all; only 3.6% have exactly two ranges.** Only ~59% of CPEs can be regex-mapped to their CVE summary, and for 27% of CVEs all CPEs can be mapped. About **60% of CPEs mentioned in CVEs appear only once**, so the system is built to *create* new CPEs.
- **Limitations:** The 35-day lag is a 2018 figure and has improved since (NVD now has a backfill programme), so it should not be quoted as current. The authors note only the *summary* text is used as input, so CVEs whose product is inferable only from context (their Oracle Solaris example) are unrecoverable.
- **Relevance:** The 14.5% of CVEs with *no version range* is a hard ceiling: for those, a version-matching checker can neither confirm nor exclude exposure.

### 3.6 fkie-cad /IVA authors — "Software Vulnerability Analysis Using CPE and CVE" — **VERIFIED**
- **Venue/Year:** arXiv:1705.05347 (IEEE EuroS&P-adjacent workshop era; venue not confirmed — **partial**)
- **URL:** https://ar5iv.labs.arxiv.org/html/1705.05347 (full HTML text retrieved)
- **Findings:** Analysis of the CPE dictionary and CVE feeds found **four major issues: (1) CVE entries without CPE references, (2) software products with no assigned CPE, (3) typographical errors in CPE URIs, and (4) lack of synchronisation between the two datasets.** Concrete evidence of (4): **as of 14 Feb 2017 the CVE feeds contained 105,591 CPE entries that do not exist in the official CPE dictionary**, including semantically identical CPEs with different WFN attribute splits (e.g. `update=beta1` vs `version=1.4.0_beta1`). Their own conclusion on automation: **"fully automated CPE assignment is prone to errors due to the CPE and CVE shortcomings"** and therefore requires a human-in-the-loop selection step. They use Levenshtein distance ≤ 2 (calibrated against CPEs deprecated for typos) to tolerate OCR-like vendor typos.
- **Limitations:** 2017 data snapshot. Levenshtein ≤ 2 is a hand-tuned heuristic, not learned. Small evaluation (Windows 7 machines via FusionInventory agent).
- **Relevance:** Establishes that the CPE dictionary and CVE feeds were *structurally desynchronised by NIST's own admission path*. Human-in-the-loop confirmation is the field's accepted fallback — a design decision the project should confront explicitly.

### 3.7 arXiv:2412.16607 — "Improving Discovery of Known Software Vulnerability For Enhanced Cybersecurity" — **VERIFIED (partial — abstract and intro retrieved)**
- **URL:** https://arxiv.org/html/2412.16607
- **Findings:** Reports that vendor-issued CPE strings are non-standardised, and that this breaks exact-match tools including FleetDM. Proposes multi-layer CPE sanitisation plus fuzzy matching over Osquery-collected data, with a priority-weighted union query and threshold similarity scoring, claiming a **40% improvement in detection accuracy over FleetDM.**
- **Limitations:** The 40% figure is relative to one tool on one dataset; no absolute precision/recall and no ground-truth methodology is given in the retrieved portion. Author list and venue not captured.

### 3.8 On PURL specifically — **NOTHING VERIFIED (direct measurement); nearest evidence in §1.5**
I found **no** peer-reviewed study measuring PURL accuracy, PURL↔CPE mapping loss, or PURL resolution ambiguity at NVD/CVE scale in this search. The nearest evidence is **Mandl et al. (§1.5)**, which builds ground truth as explicit **(ecosystem, component, version, vuln-id)** tuples across Maven, npm, NuGet and PyPI and measures five detectors against them — but its reference is OSV data, so OSV is correct by construction and the study quantifies **detector** behaviour, not identifier-normalisation loss. Tate et al. (§2.4) mention PURL alongside CPE only as a machine-readability aid that "deviate[s] from how people would colloquially refer to software," with no measurement. This remains the largest identifier-layer gap in the review, and it is directly load-bearing for this project because PURL is the identifier GUAC (§5.1) and OSV use natively — see §"What I could not find," item 1.

---

## 4. Prioritization research (EPSS, KEV, ML prioritization, SSVC) — including critical evaluations

### 4.1 Jacobs, Bettles et al. — "Exploit Prediction Scoring System (EPSS)" — **VERIFIED**
- **Venue/Year:** ACM Transactions on the Web (dl.acm.org/doi/10.1145/3436242), 2021
- **URL:** https://dl.acm.org/doi/10.1145/3436242
- **Findings:** First open, data-driven framework scoring probability of exploitation **within 12 months** of disclosure. **ROC AUC = 0.838.** Deliberately simple enough to implement in a spreadsheet.
- **Limitations:** The 12-month horizon is long relative to a patch cycle — this was the explicit motivation for the v2 redesign. Requires central data collection it did not originally have.

### 4.2 Jacobs et al. — "EPSS v3" (arXiv:2302.14172) — **VERIFIED**
- **Venue/Year:** arXiv:2302.14172 (2023)
- **URL:** https://arxiv.org/pdf/2302.14172 (full PDF text retrieved)
- **Findings:** 192,035 published CVEs (not REJECT/RESERVED) through 31 Dec 2022; **1,477 unique features per CVE** including exploitation-in-the-wild labels (Fortinet, AlienVault, Shadowserver, GreyNoise), public exploit code (Exploit-DB, GitHub, Metasploit), list mentions (CISA KEV, Project Zero, Trend Micro ZDI), offensive tooling presence (Intrigue, sn1per, jaeles, nuclei), Twitter mentions, and 1,096 binary NVD vendor labels. Comparators on the same data:

| Strategy | AUC | F1 | Efficiency | Coverage | Effort (% of all CVEs) |
|---|---|---|---|---|---|
| EPSS v3 | **0.7795** | 0.728 | 78.5% | 67.8% | 3.5% |
| EPSS v2 | 0.4288 | 0.451 | 45.5% | 44.8% | 4.0% |
| EPSS v1 | 0.2998 | 0.361 | 43% | 31.1% | 2.9% |
| CVSS v3.x base | **0.051** | 0.108 | 6.5% | 32.3% | 13.7% |
| CISA KEV alone | — | — | 53.2% | **5.9%** | 0.5% |
| Metasploit-module heuristic | — | — | **60.5%** | 14.9% | ~1% |

  Head-to-head: CVSS ≥ 7 achieves 82.1% coverage at **58.1% effort**; EPSS v3 at threshold 0.088 achieves the same ~82% coverage at **7.3% effort** (~14,000 CVEs). EPSS v3 at its F1 threshold (p ≥ 0.36) gives 78.5% efficiency and 67.8% coverage.
- **Limitations:** Authors disclose the exploitation-activity sources "lack transparency about when exploitation activity was observed, and for how long." Efficiency/coverage depend entirely on the chosen threshold. CVSS's AUC of 0.051 is below random for *this specific* exploitation-detection task — it should not be generalised to "CVSS is useless for severity."
- **Note:** This paper is the counterweight to §4.4 and §4.5. It is the strongest pro-EPSS evidence and it is authored by the EPSS SIG itself. Any project claim about EPSS must engage with both this and the following.

### 4.3 Jacobs et al. — "Enhancing Vulnerability Prioritization: Data-Driven Exploit Predictions with Community-Driven Insights" (WEIS 2023) — **VERIFIED**
- **URL:** https://weis2023.econinfosec.org/wp-content/uploads/sites/11/2023/06/weis23-jacobs.pdf (full PDF text retrieved)
- **Findings:** EPSS SIG has 170+ members worldwide. **v3 delivers an 82% performance improvement over v2**, measured as precision/recall AUC rising **0.429 → 0.779**. Design evolution: v1 was logistic regression on 16 features at disclosure time (portable, spreadsheet-implementable) but that portability was abandoned; v2 centralised collection, switched to XGBoost, expanded features 16 → 1,164, and shortened the prediction horizon from 12 months to **30 days** to match practitioner patch cycles. Notes **only ~5% of known vulnerabilities are exploited in the wild.**
- **Limitations:** Centralised architecture means EPSS **cannot score undisclosed vulnerabilities** (zero-days) — an explicit trade-off the SIG accepted. Vendor feature labels dominate the model (1,096 of 1,477 features), which risks reproducing NVD's own naming noise.
- **Relevance:** The 30-day horizon is a *model design choice*, not a fact about exploitation. §4.4 and §4.5 show this horizon choice is the direct cause of poor KEV recall.

### 4.4 Parla — "Efficacy of EPSS in High Severity CVEs found in CISA KEV" — **VERIFIED**
- **Authors:** Rianna Parla (sole author)
- **Venue/Year:** arXiv:2411.02618, 4 Nov 2024
- **URL:** https://arxiv.org/abs/2411.02618 (abs page retrieved directly) and https://arxiv.org/html/2411.02618v1 (full text retrieved)
- **Findings:** 90 CVEs scoring ≥ 9.0 that entered CISA KEV between 2023-03-15 and 2024-07-01 (EPSS v3 active throughout). Of the **57 CVEs from 2023 or later** in KEV: **42 had consistently low (mostly single-digit) EPSS** scores prior to inclusion; 6 sat around 36% and jumped up the day *after* inclusion; 4 were added on the same day as disclosure (all already had high initial EPSS but were in KEV regardless). Widening to **all 250 CVEs in KEV** during the window: **more than two-thirds scored below the 36% prioritisation threshold immediately before inclusion** — only about a third reflected prior exploitation. Core conclusion: **"EPSS Scoring system appears to be a trailing indicator of exploitation rather than a predictive system,"** and **"a prioritization strategy that focused on EPSS would leave a significant number of systems vulnerable for a period of time."** Counter-example given: CVE-2020-17519 (Apache Flink) held 90% EPSS from March 2023 yet Unit 42 reported in-the-wild exploitation Nov 2020 – Jan 2021. Her own framing: EPSS "is less of a prediction system and more of a risk scoring system," and was **less effective than simply using the CISA KEV catalog directly**.
- **Limitations:** Small, self-selected cohort (90, then 57, then 250 CVEs) rather than statistical sampling; EPSS v3 evaluated over its first ~16 months only, which she acknowledges; criteria include an assumption that KEV membership implies "should be prioritized" which is itself debatable.
- **Relevance:** The single most important critical source on EPSS. Directly contradicts a naive reading of §4.2.

### 4.5 Gordeychik — "Prediction Meets Patch Queues: Empirical Limits of EPSS-Only Prioritization Using CISA KEV Additions in 2025" — **VERIFIED**
- **Authors:** Sergey Gordeychik (sole author)
- **Venue/Year:** TechRxiv preprint, 2026. **DOI 10.36227/techrxiv.176857939.95987957/v1**
- **URLs:** https://exa.ai/library/publication/fdwnlr20pym (extensive results text retrieved) and code/data at https://github.com/scadastrangelove/kev_vs_epss (README with full recall tables retrieved). Companion: "UPS Meets Patch Queues," https://preprints.ru/article/2868
- **Findings:** All 245 CISA KEV additions from 2025; EPSS scores from the FIRST API plus weekly public daily snapshots; end-of-year snapshot 2025-12-29.
  - **Coverage gap:** EPSS was available at KEV-inclusion time for only **203 of 245 (≈83%)**; ~17% missing entirely. The author stresses *"This is not a model-quality question; it is a data availability constraint that directly reduces the attainable recall of any EPSS-only gate."*
  - **Recall against KEV, conditional on EPSS existing:** τ ≥ 0.001 → **65%**; τ ≥ 0.01 → **38%**; τ ≥ 0.1 → **27%**. Effective recall against *all* 245 entries: **53.9% / 31.8% / 22.4%**.
  - **Signal lag dominates ops lag.** At capacity 40 items/week, "patched by t=0" (the KEV announcement date) is ≈ **28.6% (70/245)** at τ=0.001, 27.3% (67/245) at τ=0.01, 20.0% (49/245) at τ=0.1. At τ ≥ 0.01 the dominant loss mode is **missing/late eligibility** — ≈ **68.2% (167/245)** at τ=0.01 and **77.6% (190/245)** at τ=0.1 — versus ops queueing of only 4.5% (11/245) and 2.4% (~6/245). Concretely: raising capacity from 40 to 400 items/week changes t=0 completion from ~28% to ~43% at τ=0.001, but at τ ≥ 0.01 the curves **overlap** — capacity buys almost nothing.
  - **Latency distribution:** time until EPSS crosses threshold has **p90 = 7 days at τ=0.001 but a median of 20 days at τ=0.1** — *"simply too slow if the goal is to be correct by the week exploitation is confirmed."*
  - **Workload:** **57.93 non-KEV items per KEV item** at τ=0.001.
  - **14-day targets:** τ=0.001 → 41% → 49% → ~95% as capacity rises 40→120→400/wk (highly capacity-sensitive). τ=0.01 → 72% → 86%, saturating at 400/wk. τ=0.1 → **saturates at 56–59% regardless of capacity.**
  - **Author's summary:** *"EPSS helps. It does not save you."* And the analytic framing: EPSS is *"a detector output transmitted over a noisy channel with delay"* — threshold τ is the decision rule, signal lag is detection latency, missing values are dropouts.
  - **Companion (UPS) paper:** 35–53% of KEV-2025 items patched by the KEV date without using KEV as a trigger; near-perfect 14-day compliance at ≥ 20 items/week; but workload inflation (overhead factor, total items handled per KEV item) of up to **~5–8×** under aggressive "Watch+" admission versus **~2.6–2.8×** under stricter "Track+/Prepare+".
- **Limitations:** **Single-author preprint, not peer-reviewed.** Capacity-constrained patch-queue simulation is a modelling assumption, not an observed remediation dataset. Results are specific to the 2025 KEV cohort and EPSS v4-era snapshots. The "patched by t=0" metric assumes remediation begins at KEV announcement, which is unrealistic in most organisations.
- **Relevance:** **The single most directly applicable paper to this project.** It provides the precise, defensible claim that a checker must treat KEV as a hard override and EPSS as a secondary sort key — and it quantifies *why* with signal-lag vs ops-lag decomposition. The companion repo is public and reproducible, which is a strong project asset.

### 4.6 Koscinski, Nelson, Okutan, Falso & Mirakhorli — "Conflicting Scores, Confusing Signals: An Empirical Study of Vulnerability Scoring Systems" — **VERIFIED**
- **Venue/Year:** arXiv:2508.13644, 19 Aug 2025 (cs.CR, cs.SE)
- **URL:** https://arxiv.org/abs/2508.13644 (abs page retrieved directly) and https://arxiv.org/html/2508.13644 (full text retrieved)
- **Findings:** First large-scale, outcome-linked comparison of **CVSS, SSVC, EPSS, and the Exploitability Index** on **600 real-world vulnerabilities from four months of Microsoft Patch Tuesday**. **Cohen's Kappa ≈ 0 across all pairwise comparisons (no agreement beyond chance); Krippendorff's Alpha predominantly negative.** Even *within* SSVC, scores differing only in Mission & Well-Being show weak internal agreement. SSVC's four decision points are (State of) Exploitation, Technical Impact, Automatable, and Mission & Well-Being Impact, with Exploitation set from CISA KEV ("Active"), PoC/public PoC, or "None". Conclusion: all four systems **produce overly broad priority groups that complicate triage**, and **fewer than 20% of CISA KEV CVEs received a high-confidence score before exploitation was public.**
- **Limitations:** Single vendor's disclosure feed (Microsoft Patch Tuesday) — Windows-centric and therefore exploitable-product-skewed; 600 vulnerabilities over 4 months; annotators appear to be the authors. Categorical binning choices (four-quarter split for SSVC, ten equal bins otherwise) materially affect Kappa/Alpha. EPSS coverage is confounded with the same 30-day horizon discussed in §4.4/§4.5.
- **Relevance:** Independent confirmation of the EPSS lead-time problem from a completely different dataset, plus the finding that **prioritization systems are mutually inconsistent** — which means an infrastructure checker should expose *why* something is prioritised, not just a score.

### 4.7 SBSeg / SBGEP — "Evaluating Vulnerability Prioritization Strategies Based on CVSS and EPSS" — **VERIFIED (author names NOT obtained — partial)**
- **Affiliation captured:** Banco Nacional de Desenvolvimento Econômico e Social, Rio de Janeiro, Brazil
- **URL:** https://sol.sbc.org.br/index.php/sbseg/article/download/44316/44079/ (full PDF text retrieved)
- **Findings:** Corpus of **31,779 vulnerabilities disclosed in 2024** from NVD; **156** subsequently in CISA KEV (ground truth). Four CVSS thresholds, five EPSS thresholds (0.05%, 0.10%, 0.50%, 1.00%, 5.00%), four combined (AND/OR) strategies. Selected results:

| Strategy | Precision | Recall | F1 | F2 | TP | FP | FN | Total queued |
|---|---|---|---|---|---|---|---|---|
| CVSS 5.0 | — | highest | — | — | — | — | — | **86.20% of corpus** |
| CVSS 10.0 | highest | lowest | — | — | — | — | — | 132 |
| CVSS 7.0 AND EPSS 0.50% | 42.11% | 5.13% | 9.14% | 6.22% | 8 | 11 | 148 | 19 |
| CVSS 9.0 AND EPSS 0.50% | 58.33% | 13.46% | 21.88% | 15.91% | 21 | 15 | 135 | 36 |
| CVSS 10.0 OR EPSS 0.50% | 20.00% | 22.44% | 21.15% | 21.90% | 35 | 140 | 121 | 175 |
| CVSS 9.0 OR EPSS 0.50% | 3.07% | 53.85% | 5.80% | 12.49% | 84 | 2,655 | 72 | 2,739 |

  Comparison of yield: CVSS 10.0 captures **1 KEV CVE per 19 prioritised CVEs**; EPSS 0.50% captures **2 per 3** while queuing only 44 items (one third of CVSS 10.0's 132). EPSS 0.10% best F2; EPSS 0.50% similar F2 with substantially better precision; EPSS 1.00% highest precision; EPSS 5.00% gives no advantage over 1.00%. **OR combinations dominate AND combinations**; AND offers limited advantage over EPSS alone.
- **Limitations:** **Only 156 positive cases** in a 31,779-item corpus — very low base rate, so precision estimates are unstable and a single TP shifts precision by ~0.6 points. Uses *first available* EPSS score and most-recent CVSS version, which is itself a lead-time choice. Single-year cohort (2024 disclosures) with KEV follow-up window. Author list not retrieved.
- **Relevance:** Best citable table for a *threshold-selection* argument: it quantifies the coverage-vs-queue-size trade-off an infrastructure-wide checker must expose to operators.

### 4.8 Hore, Moomtaheen, Shah & Ou — VPSS — "Towards Optimal Triage and Mitigation of Context-Sensitive Cyber Vulnerabilities" — **VERIFIED**
- **Venue/Year:** IEEE Transactions on Dependable and Secure Computing (dl.acm.org/doi/10.1109/TDSC.2022.3152164), 2023
- **URL:** https://dl.acm.org/doi/10.1109/TDSC.2022.3152164
- **Findings:** Two components. (1) **Vulnerability Priority Scoring System (VPSS)** — a machine-learned priority score quantifying *organisational context-based exposure*, combining CVSS with host-machine context: positional significance of the host, level of importance of the host, and protection level. (2) A decision-support system with a **two-step sequential optimisation**: first select high-priority vulnerability instances under a resource constraint, then optimally allocate them to security personnel with matching skill types. Reports outperforming both real-world SOC rule-based methods and VULCON on a real-world vulnerability dataset, prioritising vulnerabilities found across highly susceptible, organisationally relevant hosts.
- **Limitations:** Requires an accurate host inventory with the specific contextual attributes (positional significance, importance, protection level) — which is precisely the hard part in an unknown infrastructure. "Outperforms" is against baselines that are rule-based, not against modern ML triage.
- **Relevance:** The structural template for the project: score = f(vulnerability signal, asset context), then allocate under a capacity constraint. VULCON (Farris et al., ACM Trans. Privacy Secur. 21(4), 2018) is the predecessor and should be cited alongside.

### 4.9 Zeng, Yang, Huang & Chung — LICALITY — **VERIFIED**
- **Authors:** Zhen Zeng, Zhun Yang, Dijiang Huang, Chun-Jen Chung
- **Venue/Year:** Neurocomputing (Elsevier), 2022; earlier version 2021
- **URLs:** https://asu.elsevierpure.com/en/publications/licality-likelihood-and-criticality-vulnerability-risk-prioritiza/ and https://exa.ai/library/publication/bngm9cjv9fj (full abstract retrieved)
- **Findings:** **Neuro-symbolic** architecture — neural network plus **probabilistic logic programming** — where a neural net learns threat attributes contributing to exploitation and a logic reasoning engine consolidates two separate measurements: **criticality of exploitation** and **likelihood of exploitation**. Risk = f(criticality, likelihood). Evaluated against real attack scenarios using CISA alerts as future-threat ground truth (top routinely exploited vulnerabilities and APT attack-chain vulnerabilities). **Reduces remediation work for future threats vs CVSS by a factor of 2.89 (case study 1) and 1.85 (case study 2).**
- **Limitations:** Reduction factors are relative to CVSS, which §4.2 shows is a weak exploitation predictor — so the comparison partly flatters LICALITY. Threat attributes are *learned*, requiring sufficient labelled attack-chain data, which is scarce and APT-biased. Two case studies only. Probabilistic logic programming adds interpretability but also operational complexity.
- **Relevance:** The neuro-symbolic pattern (learn the signal, reason over the structure) is the most sophisticated ML-prioritization architecture in this set and is directly relevant if the project wants explainable prioritisation.

### 4.10 Hore, Shah & Bastian — Deep VULMAN — **VERIFIED**
- **Authors:** Soumyadeep Hore, Ankit Shah, Nathaniel D. Bastian
- **Venue/Year:** arXiv:2208.02369
- **URL:** https://export.arxiv.org/pdf/2208.02369v2.pdf (full PDF text retrieved)
- **Findings:** Sequential decision-making framework. A **deep reinforcement learning agent** trained with a policy-gradient algorithm learns a near-optimal *resource allocation* policy under uncertainty; an **integer programming** model then selects the vulnerability set maximising the **average** cumulative attribute value across selected instances, subject to total available mitigation time. The averaging objective is the explicit improvement over VPSS/VULCON, which maximise cumulative utility and therefore can omit important instances. Attributes: asset criticality, host protection level, organisational relevance, CVSS severity, and whether the host appears in IDS alerts. Evaluated on a simulated CSOC environment built from real-world data plus a one-year real-world dataset, against VPSS and VULCON. Reports prioritising more instances from high-value assets, organisationally relevant machines (web and database servers), IDS-flagged machines, and low-protection machines, and that the agent learned non-trivial policies under uncertain arrival patterns.
- **Limitations:** Comparison is only against VPSS and VULCON — CVSS-only was excluded as context-blind, which conveniently avoids the strongest baseline. The CSOC environment is *simulated* from real data, so it inherits whatever biases exist in that dataset. Integer-programming selection may not scale to infrastructure-wide problem sizes. IDS-alert presence as an attribute imports the IDS's own false-positive problem.
- **Relevance:** The "average not cumulative" objective and the resource-allocation formulation are the two transferable ideas. Note the shared author (Hore) between VPSS and Deep VULMAN — this is one research line, not independent corroboration.

### 4.11 Spring, Householder, Hatleback, Manion, Oliver, Sarvepalli, Tyzenhaus & Yarbrough — SSVC — **VERIFIED**
- **Venues/Years:** SEI CMU technical report version 2.0 (30 Apr 2021); v1 at WEIS 2020 (Spring, Hatleback, Householder, Manion, Shick); official documentation at certcc.github.io/SSVC; CISA deployer tree; OSTI report AD1130852; J. Spring blueprint (osti.gov/biblio/3018254)
- **URLs:** https://www.sei.cmu.edu/library/prioritizing-vulnerability-response-a-stakeholder-specific-vulnerability-categorization-version-20/ ; https://certcc.github.io/SSVC/topics/evaluation_of_draft_trees/ ; https://certcc.github.io/SSVC/topics/ ; https://certcc.github.io/SSVC/topics/decision_trees/
- **Findings:** SSVC replaces one-size-fits-all numeric scoring with **per-stakeholder decision trees** (supplier, deployer, coordinator, finder) built from decision points and decision tables. The v1 pilot provides the most valuable empirical data: **9 CVEs × 2 stakeholder groups × 6 analysts = 18 decision sets per analyst**, measured with **Fleiss' kappa per decision point and per path**. All agreements were above zero but with wide spread. Post-pilot changes are directly instructive: (a) the "supplier portfolio value" decision point was **removed entirely due to poor agreement and no clear way to correct it**, replaced by "Utility" (Value Density + Automatability); (b) trees were **reorganised so Exploitation is asked first**, because it is the easiest to gather and most verifiable; (c) "small" exposure now produces a *lower* priority than before; (d) decision-point descriptions for Safety Impact and Mission Impact were rewritten after analysts were found to bring wildly different background assumptions.
  Important methodological caveat the authors themselves state: measuring agreement on the **path reached** treats paths agreeing on 3 of 4 decisions as no more similar than paths agreeing on 0 of 4.
- **Limitations:** Inter-rater reliability is established on **nine CVEs** — this is a design-validation exercise, not a performance evaluation. SSVC produces *categorical* priorities, not a calibrated probability, so it cannot be ROC-AUC'd and cannot be thresholded like EPSS. §4.6 shows its outputs agree with other systems at approximately chance. The framework explicitly declines to optimise: the authors describe their approach as **"satisficing... we do not seek optimal formalisms, but an adequate formalism."**
- **Relevance:** SSVC's *process* lesson is the transferable part: **ask the most verifiable question first, and delete decision points that analysts cannot agree on.** A project implementing automatic SSVC-style triage should follow that ordering deliberately.

### 4.12 Jung, Yan & Bechor — CAVP — **UNVERIFIED**
- **Title/Year:** "CAVP: A context-aware vulnerability prioritization model," 2022. Located at https://www.researchgate.net/publication/358547679 — only bibliographic metadata and the reference list of others were retrieved; the paper itself was not opened. No findings are asserted here.

### 4.13 ACVRM — "Automated Context-Aware Vulnerability Risk Management for Patch Prioritization" — **VERIFIED**
- **Venue/Year:** MDPI *Electronics* 11(21):3580, 2 Nov 2022
- **URL:** https://www.mdpi.com/2079-9292/11/21/3580
- **Findings:** Defines organisation-context (OC) data as a *set* alongside CVSS rather than modifying CVSS. Four evaluation modes: homogeneous weighting; attack complexity and availability de-prioritised; security score only; and weighting by organisational risk appetite. Compared against the **Rudder vulnerability management tool's CVE-plugin**: Rudder ranks independently of scenario and sorts equal-patch-score items arbitrarily, whereas ACVRM sorts by criteria and by vulnerability age. Surveyed 15 related works: 10/15 (66.7%) treat CVSS CIA impact metrics as critical, and **11/15 (73.3%) identify exploitation rate as an essential criterion.**
- **Limitations:** The 15-paper related-work tally is a small convenience sample. Rudder is a weak comparator (a configuration-management tool, not a purpose-built prioritiser). Patch Score is a linear scaling function of weighted CVSS submetrics — no validation against real exploitation outcomes is reported.
- **Relevance:** The 73.3% figure showing exploitation rate is the most-cited criterion across prior work is a useful framing statistic, but it comes with a convenience-sample caveat.

### 4.14 IEICE — "Automating SSVC: A worst-case scenario approach for evaluating human impact of vulnerabilities" — **VERIFIED**
- **Venue/Year:** IEICE Communications Express, Vol. 15, No. 5, pp. 156–159, 2026
- **URL:** https://www.jstage.jst.go.jp/article/comex/15/5/15_2025XBL0172/_pdf/-char/en (full PDF text retrieved)
- **Findings:** Targets the SSVC deployer tree's hardest decision point, **Human Impact (HI)**, which combines safety and mission impact and therefore needs both vulnerability characteristics and organisational context. Method: **pre-assess worst-case safety/mission impact per CIA triad once**, then at vulnerability-discovery time adjust that worst case downward using the vulnerability's CVSS technical impact (None/Low/High per C/I/A). Three LLMs — **GPT-5, Llama 4 Maverick 17B, Gemini 2.5 Pro** — averaged over five independent runs, chain-of-thought prompting, temperature 0. Averaging LLM outputs reproduces expert-level assessment (validated against the SSVC specification's own CVE-2018-14781 insulin-pump worked example: mean SI-Lv = 4, MI-Lv = 3 → HI-SDP = High, matching the specification). Against **16 insulin-pump CVEs from CISA's ICS-Advisory project**, the conventional pathway and the proposed worst-case-adjustment pathway agreed on **100% of HI-SDP outcomes**, despite minor individual SI-Lv/MI-Lv discrepancies.
- **Limitations:** **Very small — 16 CVEs, one device class, one fictional hospital organisational context.** Public sample vulnerabilities so confidentiality concerns do not arise. The 100% agreement is between two LLM pathways, not against human ground truth, except for the single CVE-2018-14781 checkpoint. No baseline comparison to a non-LLM automated method.
- **Relevance:** A concrete, citable example of LLM use for *triage decision support under uncertainty* (not vulnerability discovery), which is exactly the project's target use case. The "pre-assess worst case once, adjust per vulnerability" decomposition is an engineering pattern worth adopting regardless of whether LLMs are used.

---

## 5. Knowledge-graph and ontology-based vulnerability management

### 5.1 GUAC ontology and architecture — **VERIFIED**
- **URLs:** https://docs.guac.sh/guac/guac-ontology/ ; https://github.com/guacsec/guac ; https://security.googleblog.com/2022/10/announcing-guac-great-pairing-with-slsa.html ; https://openssf.org/blog/2024/03/07/guac-joins-openssf-as-incubating-project/ ; https://openssf.org/projects/guac/
- **Origin:** Created by **Kusari, Google, and Purdue University**; announced Oct 2022 by Brandon Lum, Mihai Maruseac, Isaac Hepworth (Google Open Source Security Team); joined OpenSSF as an Incubating Project March 2024 with support from Yahoo!, Microsoft, Red Hat, Guidewire, ClearAlpha.
- **Data model — three trees:** (a) **Evidence tree** — DSSE layer creates actor↔action edges, subject layer creates action↔software-instance edges keyed by purl+hash, predicate layer links software-instance collections to actions. (b) **Actor tree** — models trust relationships and provenance between identities and claims, with trust either provided de-facto by policy or *compounded* as a function of many de-facto trusts. (c) **Software tree** — models logical properties down to physical instantiation, keyed by pURL (e.g. `pkg:pypi/django@1.11.1`). Join keys: the hash in the software tree is the artifact in the evidence tree; the identity in the evidence tree is the signature in the actor tree.
- **Queries relevant to CVE checking:** *Reachability* — "Is artifact C affected by CVE#2, and has that report been done by the NVD?" implemented as path traversal artifact → SLSA evidence → Artifact A → CVE#2 evidence → NVD identity node. *First-neighbour search* — "Is artifact C affected by any vulnerability?" — and critically, this query **detects conflicting claims**: the worked example has Bob signing CVE#4 evidence and Sam signing CVE#5 evidence for the same artifact, surfacing that the two sources disagree.
- **Four functional layers** (Google blog): Collection (connect to OSV, internal repos, proprietary third parties), Ingestion (artifacts, projects, resources, vulnerabilities, repositories, developers), Collation (normalise entity identifiers, traverse dependency tree, reify implicit relations such as project→developer and vulnerability→software version), Query (GraphQL + REST; return SBOM, provenance, build chain, scorecard, vulnerabilities, lifecycle events for an artifact and its transitive dependencies).
- **Supported inputs:** CycloneDX, SPDX, in-toto ITE-6, SLSA, DSSE, CSAF/CSAF VEX, OpenVEX, OpenSSF Scorecard, OSV, deps.dev API. Backends: in-memory keyvalue (default, non-persistent), Ent + PostgreSQL (supported), ArangoDB/Neo4j/Redis/TiKV (experimental).
- **Explicit stated limitation (from the project README):** *"GUAC uses software identifiers standards to help link metadata together. However, these identifiers are not always available and heuristics need to be used to link them. Therefore, there may be unhandled edge cases and errors occurring when ingesting data."* — **GUAC itself concedes identifier-based linking needs heuristics and can fail**, which ties directly back to the CPE/PURL inconsistency problem in §3.
- **Limitations:** No peer-reviewed accuracy evaluation of GUAC exists in what I could locate (§"What I could not find"). It is infrastructure, not a product — PostgreSQL, collectors, and knowledge-graph expertise are operational prerequisites. Its value is bounded by input SBOM/attestation completeness ("garbage in, garbage graph"). Evidence coverage is uneven: Red Hat, OpenSUSE, Microsoft publish CSAF; Amazon and Debian are still experimenting.
- **Relevance:** GUAC is the closest existing system to the project's architectural goal — a graph joining assets, provenance, and CVE evidence. Its "conflicting claims" query and its identifier-availability caveat are both directly reusable.

### 5.2 Egaña Aranguren et al. — "A comprehensive view of software vulnerability risks through enterprise knowledge graphs" — **VERIFIED**
- **Authors:** Mikel Egaña Aranguren et al.
- **Venue/Year:** *Computers & Security* (Elsevier), article S0306437425008255 / DOI 10.1016/j.cose.2025.104815, 2025
- **URL:** https://sms.carm.es/ricsmur/bitstream/handle/123456789/25906/10.1016j.cose.2025.104815.pdf (full PDF text retrieved)
- **Findings:** Deployed at **Siemens Energy** as an enterprise knowledge graph for software vulnerability risk. Delivers a **Cybersecurity Ontology Network** plus a **Vulnerability Ontology** modelled directly on the **NVD JSON Schema 1.1**, incorporating CVSS v2.0 and v3.0 schemas. Stack: RDF + OWL + SPARQL + **SHACL** for data-quality constraints. Explicitly **driven by the CycloneDX SBOM standard** "with a growing industry implantation." Provides a structured comparison table showing prior work does not connect SBOM to vulnerabilities: **UCO** — threats/security risks but no SBOM coverage; **IoTSec** — not focused on software vulnerabilities; **Reachability Matrix Ontology** — network configuration only; **Wang & Guo (2009)** — vulnerability management only, no SBOM link; **Shaked et al. (2024)** — same limitation; **Duarte et al. (2021)** — software anomalies only. Also tabulates prior security KGs (Yin et al. 2024 risk assessment — not ontology-based; Qi et al. 2023 / Gilliard et al. 2024 attack detection; Shi et al. 2024b CWE-CVE-CPE prediction; Mouiche & Saad 2025; Hu et al. 2024; Ghosh et al. 2025). Citing **Zhao et al. (2024)**'s review: cybersecurity KGs concentrate on intrusion detection, risk assessment, and malware detection — **"the connections between software packages, libraries and vulnerabilities have not been sufficiently addressed to date."**
- **Limitations:** Industrial case study at a single company — results are architecture demonstrations, not measured accuracy improvements. The ontology inherits every NVD data-quality problem documented in §3 (the paper does not measure how often the resulting EKG produces incorrect vulnerability attribution). No evaluation against real remediation outcomes. Siemens Energy notes in the text that determining what data security teams "actually consume" remains open.
- **Relevance:** **The best single peer-reviewed precedent for an ontology-driven, CycloneDX-anchored, enterprise-scale CVE knowledge graph.** Its SHACL data-quality-constraint pattern is directly implementable, and its gap table is a ready-made related-work framing.

### 5.3 Starobinski, Matyunin, Graffi et al. — "Uncovering CWE-CVE-CPE Relations with Threat Knowledge Graphs" — **VERIFIED**
- **Venue/Year:** IEEE TOPS 2024 (final version PDF)
- **URL:** https://people.bu.edu/staro/TOPS-2024-Final.pdf (full PDF text retrieved)
- **Findings:** Builds a **threat knowledge graph** from CPE + CVE + CWE. Entities are not just entries but also *attributes as first-class entities*: for CPE — part (application/hardware/OS), vendor, product, target software, target hardware; for CWE — language, technology, likelihood of exploit, consequence (which CIA properties are violated). Three relation types: attribute-of; NVD-provided association; derived. **Knowledge graph embedding is used to predict associations that are currently hidden but will appear in future.** Temporal, **open-world** validation: train on CPE/CVE/CWE as of **2021-08-04**, predict associations materialising between **2021-08-04 and 2022-03-29** — a window containing **41,583 newly added CVE-CPE associations**, of which **4,134 are between entities that already existed in August 2021** (i.e. genuinely predictable). Also shows prediction quality **improves by removing obsolete entries** from the graph.
- **Limitations:** Inherits the "only entries that already existed can be predicted" constraint — new CPEs/CVEs appearing after the snapshot are unforecastable by construction, which bounds the 4,134 figure. Related work it critiques (Hu et al.) evaluated only under a closed-world train/test split, which overstates predictive validity; this paper correctly addresses that. Embedding models for link prediction have notoriously poor calibration — the paper does not report precision@k on the temporal split in the retrieved text.
- **Relevance:** Demonstrates that **graph completion over CVE/CPE/CWE can surface CPE entries NVD has not yet linked** — a plausible supplementary recall mechanism for the project's matcher. Also gives the concrete KG schema (attributes as entities) the project could adopt.

### 5.4 SecKG2vec — Liu, Guo & Gu — **VERIFIED**
- **Venue/Year:** *Information & Software Technology* (Elsevier), article S0167404824004978
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0167404824004978
- **Findings:** Core empirical observation motivating the work: **CVE, CWE, and CAPEC relations are "not sufficient and timely"** and many are missing outright. Worked example: **CVE-2018-18442** (packet flooding) should relate to **CAPEC-125** (flooding) but no such relation exists in *any* of the three repositories; likewise **CWE-190 → CWE-119** was missing until CWE 2.0 added it. Root cause given: relations are **manually identified by experts and maintained by different institutions**, so they cannot track the growth of the vulnerability landscape. Method: fuse **semantic** correlation (entity text descriptions) with **structural** correlation (relation topology) in a joint embedding, using entity embeddings as the gradient-transfer medium in a **two-stage linkage backpropagation** scheme; replaces TransE with **TransD** because SKR relations are complex multi-type. Motivating example is solved structurally via multi-hop: CVE-2018-18442 → CWE-20 → CWE-770 → CAPEC-125. Baselines: Doc2vec (pure semantic), DeepWeak (fusion), TransE, TransD. Reported better performance on both relation-reasoning and entity-reasoning tasks, plus 0-shot scenario prediction capability.
- **Limitations:** Purely a *relation-reasoning* method over the CVE/CWE/CAPEC triple — it does not model assets, deployment, or exposure, so it cannot by itself answer "am I affected." Comparative metrics/values were not captured in the retrieved abstract. Relies on CAPEC, which is far less complete than CVE.
- **Relevance:** Provides the "infer the missing link" mechanism for the project's KG layer, with a concrete justification for why multi-hop reasoning is necessary.

### 5.5 "Unifying CVE, CWE, and CPE through knowledge graphs" — **VERIFIED**
- **Venue/Year:** *Information & Software Technology* (Elsevier), article S0167404825004158, 2025
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0167404825004158
- **Findings:** Argues the gap is **joint** modelling of CVE, CWE, and CPE — prior work treats them "in isolation," addressing either CVE classification or CPE-based asset labelling, "and seldom capture the structural relationships that connect vulnerabilities to their corresponding weaknesses and affected platforms," limiting cross-referenced analysis and propagation tracing. Implementation is **Neo4j + Cypher (property graph), explicitly rejecting RDF**. Stated reasoning: Neo4j is better for BFS/DFS traversal and for mining sparse large graphs with many labels, whereas triple-based RDF is "cumbersome for modeling complex, nested, or multilateral relationships commonly found in vulnerability data." RDF's advantage is built-in inference and W3C interoperability; Neo4j's are performance, usability, and real-time SOC fit — *"more suited to operational environments like security operations centers."* Defines uniqueness constraints for CVSS2, CVSS3, Reference, CWE, CVE, CPE. Per-asset risk is computed over CVEs affecting the CPEs installed on that asset across four stages (vulnerability risk → weaknesses → mitigations → aggregate). **Mitigation value is explicit and quantitative: ΔRA(a, CVE_i) = RA(a) × M(CVE_i)**, i.e. residual risk after applying a mitigation.
- **Limitations:** Neo4j + Cypher forfeits OWL reasoning and W3C standards compliance, which is a real trade-off for inter-vendor data exchange — the author acknowledges this. No reported accuracy figures against ground truth in the retrieved text. The ΔRA formula is a simple multiplicative heuristic, not a validated risk model.
- **Relevance:** The **RDF-vs-property-graph decision is a genuine architectural fork for the project**, and this paper makes the operational (SOC) case for property graphs explicitly. The mitigation-value formula is directly reusable for ranking.

### 5.6 "A Data-Driven Ontology Framework for Integrating Heterogeneous Vulnerability Sources" — **VERIFIED**
- **Venue/Year:** CEUR-WS Vol-4176 (FOMI 2026 proceedings)
- **URL:** https://ceur-ws.org/Vol-4176/fomi-4.pdf (full PDF text retrieved)
- **Findings:** Extends Wang & Guo's (2009) vulnerability-management top ontology with **data-driven** correction: the authors performed a comprehensive analysis of real CVE, CWE, CAPEC, and CPE repository structures and found **inconsistencies in both directions** — ontological properties that never appear in real data, and real database attributes with no theoretical representation. Four core entity types: **Vulnerability, Weakness, Attack Pattern, Product** (CVE, CWE, CAPEC, CPE). Improvements: adds a separate **CWE Category** class for category-level weaknesses (retained despite NIST discouraging CVE→category mappings since 2019, because they account for **< 0.1%** of records and mark less granular entries); **consolidates all fragmented CVSS parameters into a single cohesive property**; extends URL-only references with a **"tags"** sub-property classifying reference types; makes the CVE–CPE relationship carry **explicit version-range metadata** rather than a simple link. Demonstrated via a multi-model NoSQL implementation populated with real data plus a **SWRL inference rule** identifying potential attack chains — vulnerabilities sharing related weaknesses *and* affecting the same platform/product — to surface multi-stage risk. Notes that NIST discouraged CVE-to-category mappings from 2019.
- **Limitations:** Demonstrated on a synthetic multi-model NoSQL database with a single hand-written SWRL rule — no scale evaluation, no query-latency measurement, and SWRL is known not to scale. No accuracy comparison against NVD-derived ground truth. Very recent, so uncited.
- **Relevance:** The "audit your ontology against real repository schemas" methodology is a concrete, repeatable step the project should apply to whatever schema it adopts — it directly targets the §3 inconsistency problem.

### 5.7 "Constructing Cybersecurity Knowledge Graphs for Hybrid LLM–Graph Reasoning on Vulnerabilities" — **VERIFIED (abstract + intro)**
- **Venue/Year:** CEUR-WS Vol-4085
- **URL:** https://ceur-ws.org/Vol-4085/paper35.pdf
- **Findings:** Builds a KG from vulnerability reports, **explicitly modelling causal factors as structured entities and relationships** to improve causal reasoning, then augments via **DBpedia** to improve connectivity. Evaluated by contrasting original vs augmented graphs: Graph-LLM with augmentation **improves link prediction and yields higher-quality QA** compared with report descriptions alone. Demonstrates hybrid LLM-language-understanding + graph-inference querying.
- **Limitations:** Author list and evaluation metrics not captured in the retrieved portion. DBpedia augmentation introduces general-world knowledge whose relevance to a vulnerability graph is unvalidated. Small workshop paper.
- **Relevance:** Connects §5 and §6 — the pattern of KG-grounded LLM reasoning, which HARP (§6.2) also adopts.

### 5.8 Alharbi — "Enhancing cybersecurity through autonomous knowledge graph construction by integrating heterogeneous data sources" — **VERIFIED**
- **Venue/Year:** *PeerJ Computer Science*, 16 Apr 2025
- **URL:** https://peerj.com/articles/cs-2768 (full text retrieved)
- **Findings:** "Cyber Guard Graph." Structured NVD data (CVE, CWE) mapped directly into the KG; **CPE values parsed out of CVE data** and integrated; unstructured components (CVE descriptions, CWE extended descriptions) handled with an NLP pipeline (preprocessing, NER + classification, entity linking/disambiguation, semantic role labeling). Model: CVE node (ID, assigner, description, post-analysis info) → CWE node via `MAPPED_WITH`; `HAS_RELATED_WEAKNESS` between CWEs; `HAS_ENTITY` to extended descriptions; ProblemTypes node carrying lang/value; CPE node with cveId + version. Cites **Høst (2022)**, who built a vulnerability KG from NVD CVE records with NER + rule-based relation extraction and used **TuckER** embeddings to predict missing entities, achieving **0.76 Hits@10** — and notes the prediction problem is hard because all unique CVE IDs are present (granularity limits discriminative signal) and because many products have **overlapping vulnerable version ranges**.
- **Limitations:** Høst's Hits@10 of 0.76 is weak for a prediction task, and the paper explains *why* rather than solving it. Rule-based relation extraction inherits NVD's labelling as ground truth, so it cannot discover relations NVD itself lacks (the exact problem SecKG2vec §5.4 identifies). Entity-linking/disambiguation of vendor/product names is hand-built and not evaluated.
- **Relevance:** The honest diagnosis that **overlapping version ranges make graph-completion over CVEs hard** is an important negative result for anyone planning to infer missing CPE links automatically.

### 5.9 OpenSPG — **NOTHING VERIFIED**
Despite a targeted search, I found **no peer-reviewed publication** describing OpenSPG in a knowledge-graph-for-vulnerability-management context. Only the GUAC/OpenSPG adjacency appears in general supply-chain tooling discussion. If the project intends to use OpenSPG, this is a literature gap — see §"What I could not find."

---

## 6. Emerging 2025–2026 work: LLM/agentic TRIAGE and PRIORITISATION (not code vulnerability discovery)

### 6.1 VEX-Bench — "Benchmarking LLM Agents for Assessing Exploitability of Software Supply Chain Vulnerabilities" — **VERIFIED**
- **Venue/Year:** arXiv:2609.08040
- **URL:** https://arxiv.org/html/2609.08040v1 (full HTML text retrieved). Code/data: https://github.com/steven1518/vex-bench
- **Framing:** Explicitly distinguishes itself from zero-day discovery benchmarks: supply-chain triage asks whether a **known** vulnerability in an upstream dependency affects the downstream project, requiring cross-repository reasoning rather than exploitation.
- **Dataset:** **75 real-world cases** mined from GitHub across Go, Python, and Java, ground truth **manually annotated by security experts**. Output schema: (i) binary vulnerability status (affected / not-affected), (ii) fine-grained justification from four not-affected categories, (iii) a free-form reasoning trace recording which call sites were inspected and which mitigations found — *"making the prediction auditable rather than a black-box verdict."*
- **Findings (9 models × 3 agent harnesses):**

| Model / harness | Status accuracy | Status precision | Status recall | Status F1 | Justification accuracy | Justification macro-F1 |
|---|---|---|---|---|---|---|
| GPT-5.5 (best status accuracy) | **89.3%** | 88.7% | — | 79.9% | 78.2% | **73.5%** |
| Claude Opus 4.6 (best status F1) | 88.4% | — | **87.9%** | **81.6%** | — | — |
| GPT-5.5 weighted-F1 | — | — | — | — | — | 81.5% |
| GPT-5.4 mini | 82.2% | — | — | — | 66.7% | — |
| MiniMax-M2.7 | 71.1% | — | — | — | — | 44.8% |
| DeepSeek-V4-Flash (worst) | — | lowest | lowest | lowest | 58.7% (wf-F1 62.8%) | — |

  Best-case ~80% F1 on binary status; **only GPT-5.5 exceeds 70% macro-F1 on justification.** Performance degrades uniformly from status to justification: largest gap GPT-5.4 mini at **15.5 percentage points**; GPT-5.5 11.1 pts; Claude Opus 4.6 12.0 pts. The authors' conclusion: *"reporting only the binary affected/not-affected status can overstate performance relative to the finer-grained reasoning needed for software supply-chain triage."*
- **Limitations:** **75 cases is a very small benchmark** — differences of a few points between models are not statistically meaningful at this n. Expert annotators are the authors' network. Justification labels collapse four distinct non-affected reasons into a coarse taxonomy. Agent harnesses differ substantially in available tools, confounding "model" and "harness" effects. No ground truth of the "does the vulnerability actually work here" kind — labels are expert judgement.
- **Relevance:** **The closest existing benchmark to the project's triage problem**, and the single most useful result: an LLM agent reaches ~80% F1 on the binary question but under 75% on *why*, and the honest framing is that binary-only reporting overstates performance. At 75 cases this is a proof-of-concept, not a production readiness signal.

### 6.2 HARP — "Hierarchical Adaptive Ranking with Preference-Adaptive Fusion for Query-Based CVE Prioritization" — **VERIFIED**
- **Venue/Year:** arXiv:2608.19430
- **URL:** https://arxiv.org/html/2608.19430v1 (full HTML text retrieved)
- **Framing:** Opens with the observation that **vulnerability prioritisation is preference-dependent** — the same CVE gets different priority under different operational objectives — but that this preference is usually implicit and hard to express in a prompt, while organisations *do* have historical validated triage cases. HARP therefore adapts from a **support bank of historical labelled examples for the current preference scenario** rather than requiring an explicit textual policy statement.
- **Method:** Graph-grounded multi-view. Retrieves candidates and evidence from a **vulnerability knowledge graph**; scores under three policy-conditioned views — **Global, Enterprise, User**; fits view-fusion weights from sampled supports; applies **Top-K consensus routing**. LoRA adapters are trained per scenario.
- **Benchmark:** Query-based CVE ranking benchmark with **ground-truth rankings annotated by cybersecurity practitioners** under **three preference scenarios: `importance`, `exploit_first`, `patch_order`**. Annotators were from the authors' own organisation's IT/security team; guidelines developed independently of the policy templates; disagreements resolved by discussion to consensus. Evaluation labels are stated to be independent of the policy-specific adapter supervision.
- **Findings:** Backbones GPT-OSS-20B, Llama3-8B, Qwen2.5-7B-Instruct; K = ⌈0.3·|C(q)|⌉; five runs. HARP best jointly on Precision@K, MAP@K, MRR@K against: direct LLM ranking, LLM self-consistency (LLM-SC), LLM-KG-RAG, Embedding Ranking, single-view variants, BM25, and **"Industrial Signals"** — a supervised ranker on CVSS severity, **EPSS-style** exploit likelihood, **CISA KEV-style** known-exploitation indicators, patch availability, attack vector, and exposure cues. Direct LLM ranking is weak; LLM-SC helps only partially; LLM-KG-RAG benefits from graph evidence but still lags. **"Industrial Signals" — which already consumes the exact industrial signals the project would use — still underperforms HARP.** Ablations all degrade the full model: Mixed Support Bank (drops to near Equal Weight, generally below No Regularization — showing scenario-matched support supervision is a real adaptation signal), No Regularization, Equal Weight, Random Weight (largest drop), No Top-K Consensus, Random Policy. Small backbones are used, indicating the approach works without frontier-scale models.
- **Limitations:** **Practitioner annotations from a single organisation** means the three "preference scenarios" encode one firm's priorities, not an industry consensus. Ground-truth rankings are inherently subjective, and "consensus by discussion" among team members can hide durable disagreement. Critically, the evaluation labels come from the *same* organisation whose historical cases populate the support bank used for LoRA adaptation, so there is a real risk of **train/test leakage through shared organisational priors** even though the authors state the supervision sets are distinct. Metrics are ranking metrics (P@K, MAP@K, MRR@K) at K = ⌈0.3·|C(q)|⌉ — a 30%-of-candidates cut is a far easier bar than P@10 over a realistic analyst queue. All backbones are ≤20B open-weight models, so the approach is untested at frontier scale. No comparison against an actual human analyst's own ranking is reported; every baseline is automated.
- **Relevance:** The most directly transferable result for the project's **prioritisation** stage, and a corrective to a naive design: simply concatenating the industrial signals the project would already use (CVSS, EPSS, KEV, patch availability, attack vector, exposure) is explicitly **beaten** by a preference-conditioned multi-view ranker. The practical lesson is that "which CVE first" is a *policy* question, so the tool should expose that policy as an explicit user-visible choice (importance vs. exploit-first vs. patch-order) rather than hard-coding one ordering. The ablations (random fusion weights worst, random policy worst) confirm the multi-view signal is real rather than a small-backbone artefact.

### 6.3 Xiong & Zhang — "Sifting the Noise" — **VERIFIED**
- **Authors:** Yunpeng Xiong, Ting Zhang
- **Venue/Year:** arXiv:2601.22952, submitted 30 Jan 2026 (v3 23 Jul 2026); listed as ISSTA 2026 / *Proc. ACM Softw. Eng.*, DOI `10.1145/3832100`
- **URL:** https://arxiv.org/abs/2601.22952 (abs page and HTML full text retrieved locally)
- **Framing:** Addresses a failure mode that matters directly for this project: when an LLM coding agent is asked to judge whether a static-analysis alert is a real vulnerability, **bad alerts outnumber good ones**, and a naive agent treats alerts as roughly equally trustworthy. The paper's claim is that false-positive suppression, not detection, is where agentic accuracy is won or lost.
- **Setup:** Three coding-agent scaffolds — **Aider, OpenHands, SWE-agent** — asked to triage alerts from the **OWASP Benchmark** (Java) and from **post-cutoff C/C++** code, so the agent is tested on code it cannot have memorised from pretraining.
- **Findings:** Initial false-positive detection rates exceed **92%**, and the best scaffold/prompt combination reduces this to **6.3%** — an order-of-magnitude reduction, not an incremental gain. On a real-world Java CodeQL alert stream the best configuration identifies **93.3%** of true false positives. On the post-cutoff split, the strongest pairing (**SWE-agent + Claude Sonnet 4**) identifies **95.5%** of false positives at **95.5% precision**, against **36.4%** for the vanilla agent configuration. On a 50-alert stream (22 false positives, 28 true positives) the agreement between agent verdicts and expert labels reaches **Cohen's κ = 0.725**, i.e. substantial but far from expert-equivalent.
- **Limitations:** This is **SAST/source-code triage**, not dependency CVE matching and not whole-infrastructure asset discovery — the closest analogue to this project's post-matching verification stage, not to its discovery or matching stage. Results are **entirely backbone-dependent**: the headline numbers belong to one frontier model on one scaffold, and weaker backbones collapse toward the 92% baseline, so the 6.3% figure must never be quoted as a property of "LLM agents" in general. Suppressing false positives is only half the task — a classifier optimised for FP rejection can be trivially gamed by predicting "no" for everything, and the retrieved text reports precision alongside recall but no single consolidated FP-vs-FN trade-off. CWE and static-analysis-tool coverage bound the results: an alert source the agent has never seen will not be triaged at all. Cost and latency of running three scaffolded agents per alert are not evaluated.
- **Relevance:** Establishes that an LLM verification layer is worth building, but only if the project reports **both** the FP-suppression rate and the precision that keeps suppression from degenerating into blanket dismissal. The "post-cutoff" design is the methodologically honest one and should be copied in any project-side evaluation.

### 6.4 Jajodia et al. — "Before You Hand Over the Wheel" — **VERIFIED**
- **Authors:** Sourov Jajodia, Madeena Sultana, Suryadipta Majumdar, Adrian Taylor, Grant Vandenberghe
- **Venue/Year:** arXiv:2603.06422, submitted 6 Mar 2026 (cs.CR)
- **URL:** https://arxiv.org/abs/2603.06422 (abs page and HTML full text retrieved)
- **Framing:** Studies whether LLMs can be given operational security work — network and memory forensics, malware analysis, phishing triage, log investigation — rather than only authoring code. The title signals the paper's core concern: **delegating authority before validating competence.**
- **Benchmark:** **SIABENCH** — 25 deep incident-analysis workflows plus 135 alert-triage scenarios, covering network and memory forensics, malware binaries, source code and PDFs, phishing, log analysis and **false-alert detection**; **11 LLMs** evaluated.
- **Findings:** Recent frontier models — explicitly **Claude 4.5 Sonnet** and **GPT-5** — materially improve on this work relative to earlier generations, confirming that capability is real and improving. The paper's headline finding, however, is that **substantial headroom remains** across every task family, and it is most pronounced exactly where a production CVE tool would need it: false-alert discrimination and multi-step forensic reasoning chains, rather than single-shot classification.
- **Limitations:** SIABENCH benchmarks **agent/capability evaluation for incident analysis**, not infrastructure CVE matching — it contains no SBOM, no CPE/PURL resolution and no dependency-graph reasoning, so it cannot be used to claim accuracy on this project's core function. Its "false alert" tasks are log- and network-artifact-based rather than advisory-vs-inventory comparisons. Model results decay quickly: a benchmark built in March 2026 measures models that will be superseded within the year, so **this is a snapshot, not a stable ordering**. Eleven models is a broad but shallow sweep — no agent harness, tool-use loop or retrieval setup is varied, so harness effects (large, per VEX-Bench §6.1) are not captured.
- **Relevance:** The strongest available cautionary evidence for this project's **automation claims**: the newest frontier models still fail a meaningful fraction of deep incident tasks, so an automatic whole-infrastructure checker should present its output as *decision support with per-finding justification and confidence*, never as an autonomous verdict, and should have a defined human-escalation path.

### 6.5 Ni et al. — "Learning to Triage Vulnerability Reports from Program Analysis" — **VERIFIED**
- **Authors:** Ronghao Ni, Aidan Z. H. Yang, Min-Chien Hsu, Nuno Sabino, Limin Jia, Ruben Martins, Darion Cassel, Kevin Cheang
- **Venue/Year:** arXiv:2510.20739, submitted 23 Oct 2025 (v2 10 Aug 2026)
- **URL:** https://arxiv.org/abs/2510.20739 (abs page retrieved)
- **Framing:** Triage at **NVD scale in the real world**: real analysis-tool findings about real Node.js packages, rather than synthetic benchmarks.
- **Dataset:** **1,883 Node.js packages**, each contributing one human-reported finding, labelled as a true or false positive. Four model families compared: classical machine learning, graph neural networks, LLM-based models, and hybrids.
- **Findings:** The best LLM-based configuration, **NodeMedic-FINE**, reaches **F1 = 0.915** on triaging program-analysis findings. Results support the hybrid pattern: static code features and LLM semantic understanding are complementary, not redundant.
- **Limitations:** Node.js/npm only — a single ecosystem with a single package manager's naming, versioning and reachability conventions, so transfer to Maven, PyPI, NuGet, embedded C or OS packages is unproven. Triage is of **program-analysis (code) findings**, not of dependency/CVE advisories, so this is an analogue of the project's verification stage, not its matching stage. Labels derive from human reports, which are themselves incomplete — some "false positives" are unreported true positives, biasing measured F1 optimistically. The abstract retrieved does not report per-class breakdown, calibration, or cost; F1 alone conceals whether errors are concentrated in the dangerous direction (discarding a real vulnerability).

---

## 7. Internet-wide scanning platforms as an empirical substrate: coverage, timeliness, and attribution accuracy

*Rationale for this section:* Sections 1–3 establish that matching an inventory to a CVE database is where false positives come from. Sections 6–7 answer the harder prior question: **can the tool trust the inventory it built, and can it trust the outside data it enriches it with?** The literature below is directly load-bearing for an "entire infrastructure" tool, because in practice such a tool must reconcile its own findings with Shodan, Censys, ZoomEye and WHOIS. Seven of these papers independently report that those platforms disagree with each other and with ground truth.

### 7.1 Huang et al. — "Trust but Verify" — **VERIFIED**
- **Authors:** Szu-Chun Huang et al. (author list retrieved from the USENIX presentation page; full list to be confirmed against the prepublication PDF)
- **Venue/Year:** USENIX Security 2025 (*30th Annual USENIX Security Symposium*), pp. 823–842
- **URL:** https://www.usenix.org/conference/usenixsecurity25/presentation/huang-szu-chun (presentation page retrieved). Prepublication PDF: https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-1015-huang-szu-chun.pdf
- **Method:** Measures the accuracy of **vulnerability-tagging services** — Shodan's CVE tags, derived either from banner/version inference or from active payload probing — by validating them against **Nuclei templates** that actually exercise the service, across **104,930 endpoints** and **37 CVEs**.
- **Findings:** This is the paper behind executive-summary finding 6, and its message is two-sided:
  - **Over-reporting (false positives).** The paper's central quantitative claim is that **over 95% of Shodan's banner-based CVE detections are false positives.** Banner strings are not reliable evidence of a vulnerable version: they are often stale, spoofed, emulated, or simply a generic service identification that the platform's mapping heuristics over-read.
  - **Under-reporting (false negatives).** Only **17 of the 37 CVEs** in scope were detected by payload probing, and **20 were detected only by banner inference** — of which essentially none were confirmed. Shodan tracked some **8,199 CVEs** by banner alone. Critically, **52.07% of confirmed-vulnerable endpoints were not reported at all**, and there was **zero overlap** between Shodan's verified and its unverified detections, meaning a platform can look authoritative on both sides of the ledger simultaneously.
  - **Payload-based detection is the trustworthy half.** Where payload probing exists, agreement with Nuclei averaged roughly 70% and reached ~95% on some CVEs, with per-CVE detection ratios diverging as much as 10× — consistent, and consistent in the right direction.
- **Limitations:** Validation is only as good as the Nuclei template set — a template that cannot exercise a service yields another false positive, and Nuclei template coverage is uneven across the 37 CVEs. The 37-CVE scope is narrow, and the banner-vs-payload split means results describe Shodan's methodology as much as Shodan's deployment. "Vulnerable endpoint" means *reacts to a payload*, not *exploitable in context* — no authentication, configuration or compensating-control state is modelled. The >95% figure is a property of **banner-based tagging specifically** and must not be generalised to Shodan's payload-based detections or to all Internet scanning.
- **Relevance:** The single strongest justification for this project. It demonstrates that even the most commercially resourced Internet asset database in the world, on the most important task in this project's problem space, **cannot be trusted without independent active validation** — precisely the value the project proposes to add.

### 7.2 Bennett, Abdou & van Oorschot — "Empirical Scanning Analysis of Censys and Shodan" — **VERIFIED**
- **Authors:** Christopher Bennett, AbdelRahman Abdou, Paul C. van Oorschot
- **Venue/Year:** MADWeb 2021 (Workshop on Measurement, Attack and Defense) — *Proc. ACM SIGCOMM Internet Measurement Conference (IMC)* companion
- **URL:** https://ceur-ws.org/Vol-4085/paper8.pdf (full PDF text extracted and read)
- **Method:** Ground truth is *created* rather than searched for: **5 virtual machines** are deliberately reconfigured to expose a **235-token** rotating sequence of banners across ports, then observed for **47 days**.
- **Findings:**
  - **Coverage is good on a stable host, and the platforms are complementary, not redundant.** Censys observed **25** of the 235 tokens and Shodan **19**; no single platform saw everything.
  - **Change detection is the weakness.** About **65%** of the observed token changes were captured, with the common case being roughly **one banner connection per port per day**. Every change was visible within **24 hours**, but a substantial fraction of changes was **missed entirely** — a host can present stale banners for a long time and neither platform notices.
  - **The two platforms differ structurally, not just in coverage.** Observed scanning sources were geographically concentrated for Censys (notably Michigan) and far more geographically dispersed for Shodan. Shodan reached **PLC/ICS devices within about 4 days** and HTTP banners within about 14, reflecting deliberate protocol-specific scanning campaigns.
- **Limitations:** **Five VMs is an extremely small sample**, and a lab host under continuous observation is the friendliest possible case for both platforms — real churn, DHCP, cloud autoscale and CDN fronting will be worse, not better. Tokens were synthetic and under full operator control; no adversarial or shared-hosting conditions were tested, so the paper measures **detectability**, not evasion resistance. A 47-day window cannot characterise long-term drift in scanning behaviour.
- **Relevance:** Directly informs design: a whole-infrastructure checker **cannot treat any external scan database as a complete or fresh inventory**, must re-verify rather than import, and should reconcile *multiple* sources because Censys and Shodan demonstrably see different things. It also justifies a stated staleness field on every externally-sourced asset record.

### 7.3 Durumeric et al. — "Censys: A Map of Internet Hosts and Services" — **VERIFIED**
- **Authors:** Zakir Durumeric, Hudson Clark, Jeff Cody, Elliot Cubit, Matt Ellison, Liz Izhikevich et al. (full author list to be confirmed from the retrieved PDF)
- **Venue/Year:** ACM SIGCOMM 2025, DOI `10.1145/3718958.3754344`
- **URL:** https://zakird.com/papers/censys-2025.pdf (full PDF text extracted and read). DOI: https://doi.org/10.1145/3718958.3754344
- **Framing:** A system paper describing Censys's measurement pipeline and the coverage it achieves — the reference point for how much of the Internet a scan-based inventory can actually see.
- **Findings:** Measured visibility of Censys's scan data is **98%** of services on the **top 10 ports**, **97%** on the **top 100 ports**, and **62%** across **all** ports simultaneously. This is the crucial shape of the result: platform coverage is near-total on the few ports everyone scans and falls off sharply on the long tail, which is exactly where non-standard infrastructure hides. The paper documents substantial post-processing work on scan output — stale-data and duplicate filtering — after which the paper reports high self-assessed data accuracy.
- **Limitations:** Visibility is measured **against Censys's own scan schedule as the denominator**, so it characterises coverage of a known scan corpus rather than independent ground truth of the Internet — the same limitation §7.1 and §7.6 raise from the opposite direction. Per-port coverage says nothing about *stability* of the record or correctness of any attached vulnerability metadata. Server-side figures in the retrieved text (service counts after filtering) should not be quoted without re-reading their exact definition in context.
- **Relevance:** Justifies a **layered discovery strategy**: an Internet-scan-derived inventory is a strong, low-cost *seed* for common services, and must be supplemented by the organisation's own authoritative sources (DNS, asset registers, cloud APIs) for the long tail and for anything internal.

### 7.4 Price, Austin, Smith & Race — "Measuring Discrepancies in Attack Surfaces Generated by Internet Intelligence Platforms" — **VERIFIED (partial — abstract and metadata retrieved)**
- **Authors:** Martin Price, Edward Austin, Paul Smith, Nicholas Race (Lancaster University, UK)
- **Venue/Year:** ACM SIGCOMM 2025 Posters and Demos, pp. 82–84
- **URL:** https://www.lancs.ac.uk/scc/assets/papers/2025/2502_sigcomm_poster.pdf and https://conferences.sigcomm.org/sigcomm/2025/papers/sigcomm25-poster-session.pdf
- **Findings:** Measures **Shodan, Censys and ZoomEye** on shared infrastructure and shows their generated "attack surfaces" differ **materially in both size and temporal characteristics**. Each platform's picture of the same asset is not a noisy copy of the truth — it is a systematically different object, shaped by that platform's scan cadence, ports and vantage points. A tool that reconciles against "the Internet scan data" without saying *which* platform is reconciling against is therefore reporting an undefined quantity.
- **Limitations:** Only three platforms and one infrastructure sample; poster/demo format (3 pages) means the methodology and metrics are thin relative to the claims. No ground-truth inventory is established, so the paper establishes **disagreement**, not which platform is right.
- **Relevance:** Direct architectural guidance: an infrastructure-wide checker must treat each external platform as a **separate, named, individually-stated data source** with its own confidence and coverage profile — and should report disagreement between them rather than silently merging.

### 7.5 Gelernter, Schulmann & Waidner — "External Attack-Surface of Modern Organizations" — **VERIFIED**
- **Authors:** Nethanel Gelernter, Haya Schulmann, Michael Waidner (IONIX / Goethe University Frankfurt / Technische Universität Darmstadt)
- **Venue/Year:** ASIA CCS 2024 — *19th ACM Asia Conference on Computer and Communications Security*, Singapore, pp. 589–604, ISBN 9798400704826, DOI `10.1145/3634737.3656295`
- **URL:** https://doi.org/10.1145/3634737.3656295 (publisher record and abstract retrieved via ATHENE publication server and Goethe University publication list)
- **Findings:** Performs the first security analysis of the external attack surface of the **100 largest enterprises in Europe**, partitioning assets into three areas: **on-premises**, **cloud-hosted**, and **outsourced to external providers**. Its headline finding is the one that should govern this project's scope: **existing reconnaissance and vulnerability scanning "capture only a fragmented view of the risk landscape"** and **miss most assets of large organisations**, because they do not model modern IT architecture. The outsourced third area — typically invisible to both traditional on-premise and modern cloud tooling — is a **large and significant** part of the digital footprint. Security issues differ by sector *and* differ between the three areas within a sector, so a single flat "scan everything" model is structurally inadequate.
- **Limitations:** The 100 enterprises are Europe's largest, which are unusually multi-national, multi-cloud and heavily outsourced — the findings should not be assumed to scale down to a single institution's estate. The study is a **point-in-time external** measurement: it says nothing about internal-only assets, and it depends on the completeness of the authors' own discovery, so "we found more" is partly a statement about their method. Disclosure outcomes are not reported as an effectiveness metric.
- **Relevance:** **The scope-defining paper for this project.** It supplies the empirical argument that "whole infrastructure" cannot mean "what one scanner can reach", and it names the three-part taxonomy (on-prem / cloud / outsourced) that the project's asset model should adopt. It also implies a **structural false-negative limit** that must be stated in any results: absence of findings is not evidence of absence of exposure.

### 7.6 Angelova, Ethembabaoglu, van Wegberg, Gañán & van Eeten — "'I'm the mess that you wanted'" — **VERIFIED**
- **Authors:** Yana Angelova, Aksel Ethembabaoglu, Rolf van Wegberg, Carlos Gañán, Michel van Eeten (Delft University of Technology)
- **Venue/Year:** WEIS 2026 — *International Workshop on Information Security (CWI, Amsterdam)*
- **URL:** https://weis2026.econinfosec.org/wp-content/uploads/sites/13/2026/05/WEIS2026_paper_8.pdf (full PDF retrieved and read)
- **Framing:** Internet-wide vulnerability scanning requires mapping an IP to the **entity responsible** for it so that entity can be notified. Practitioners overwhelmingly use **IP WHOIS**. Almost nothing was known about how accurate WHOIS-based asset scoping is, because ground truth did not exist.
- **Method:** A rare **ground-truth study.** The authors retrieved the IP ranges of **Dutch municipalities** from public WHOIS databases by keyword matching, and compared them against the ranges those municipalities **self-reported to their sectoral CERT**. They then pulled **Shodan** results for both sets to measure the security consequence of the mismatch.
- **Findings:**
  - **Recall:** WHOIS mapping identifies **58%** of the self-reported IP addresses; a large share of actual municipal addresses are never discovered publicly.
  - **Precision:** **62%** of the publicly discovered assets are **false positives** — ranges assigned to a municipality that the municipality does not consider its own. This is worse for smaller bodies: municipalities under 50,000 population average roughly **91% false positives**.
  - **Security consequence — the result that matters most:** **94% of the vulnerabilities found in the public dataset came from IP addresses the municipalities do not own.** WHOIS overestimation produces **~94% overestimation of vulnerable hosts**. The paper's point is that public data inflates the apparent insecurity of public bodies, *reproducing an existing narrative through measurement error rather than measurement*.
  - Adding MaxMind-style commercial geolocation/WHOIS on top contributes only a **marginal** improvement and mostly **adds noise**.
- **Limitations:** One country, one sector (local government), one WHOIS keyword-matching method; WHOIS conventions and registry practice differ internationally. "False positive" is defined against a *self-reported* asset list, which may itself be incomplete or may deliberately exclude certain ranges — so 58% recall partly measures the municipality's record-keeping, not only WHOIS's accuracy. Shodan, not the municipalities' own scanners, defines what counts as a vulnerable host, which inherits §7.1's measurement problems.
- **Relevance:** **The most important warning in this review for an infrastructure-wide tool.** Asset-to-owner attribution via WHOIS is both incomplete (misses ~42%) and unreliable (62% spurious). For an entire-infrastructure checker this means: never scope findings to an organisation from WHOIS alone; require the organisation's own authoritative asset inventory as the scoping source of truth, and treat WHOIS-derived ownership as a weak, clearly-labelled heuristic. It is also the strongest available rebuttal to naive "our scan found N vulnerabilities" reporting, since the denominator may itself be wrong.

### 7.7 Coppolino, Iannaccone, Nardone & Petruolo — "Asset Discovery in Critical Infrastructures" — **VERIFIED (partial)**
- **Authors:** Luigi Coppolino, Antonio Iannaccone, Roberto Nardone, Alfredo Petruolo
- **Venue/Year:** *Electronics* 14(16):3267, 2025, DOI `10.3390/electronics14163267`
- **URL:** https://www.mdpi.com/2079-9292/14/16/3267
- **Findings:** Proposes an **LLM-based asset-discovery approach for critical infrastructure** built on a **Mixture-of-Experts** design that orchestrates passive and active probes together with physical/environmental sensor inputs. The interest for this project is architectural rather than empirical: it is a concrete proposal for combining *heterogeneous, weakly-correlated evidence sources* — which is precisely the problem of building one coherent asset inventory out of scan data, DNS, certificates and internal records.
- **Limitations:** A **proof of concept**: the retrieved material reports the architecture, not robust accuracy metrics, and there is no ground-truth benchmark. Critical-infrastructure constraints (air-gapped segments, safety requirements, active-scanning prohibitions) make the reported approach materially harder to deploy than in an enterprise or campus network. Single-domain, single-author-group work.
- **Relevance:** Useful as a **design precedent** for evidence fusion and for arguing that active scanning alone is inappropriate in sensitive contexts — a constraint a university infrastructure checker may well face.

### 7.8 Wu et al. — "Revealing the Black Box of Device Search Engine" — **VERIFIED**
- **Authors:** Mengying Wu, Geng Hong, Jinsong Chen, Qi Liu, Shujun Tang, Youhao Li, Baojun Liu, Haixin Duan, Min Yang
- **Venue/Year:** arXiv:2412.15696, submitted 20 Dec 2024
- **URL:** https://arxiv.org/abs/2412.15696
- **Findings:** Characterises the scanning side of device-search engines directly: they identify **1,407 scanner IP addresses** and deploy **28 honeypots** to compare what **Censys** and **Shodan** actually scan and how. The value to a consumer of these platforms is that it shows their coverage is a **deliberate, finite strategy** — specific protocols, ports and vantage points — rather than a uniform sweep of the Internet.
- **Limitations:** Honeypot-derived observations characterise scanner behaviour against *honey* targets and may not generalise to real production services; the paper's primary object is scanning ethics and behaviour rather than asset-database accuracy, so it supports no accuracy claim. Venue/publication status beyond the arXiv preprint was not confirmed in the retrieved material.
- **Relevance:** Explains *why* §7.2–§7.4 find platform disagreement: coverage is the product of strategy choices, so the project should document which platform's view it is relying on and must not expect completeness from any of them.

### 7.9 Mahmood, Ahmed, Peddinti & Huang — "What's on My Network?" — **VERIFIED**
- **Authors:** Rameen Mahmood, Tousif Ahmed, Sai Teja Peddinti, Danny Yuxing Huang
- **Venue/Year:** arXiv:2510.13817, submitted 24 Sep 2025 (v2 8 Jul 2026)
- **URL:** https://arxiv.org/abs/2510.13817
- **Framing:** Scan databases record network metadata but not what a device *is*. This paper uses **LLaMA 3.1 8B** to infer real-world **IoT device identity from sparse network metadata** collected by **IoT Inspector**, combining LLM-generated labels with a **stability/ensemble** procedure rather than trusting a single inference, plus instruction tuning.
- **Findings:** Semantic device identification from partial network metadata is achievable with a small local model — relevant because asset *classification* is a separable subproblem that can be solved cheaply and offline once candidate assets are discovered.
- **Limitations:** This is **device/vendor identification, not vulnerability or CVE detection**, and must not be cited as evidence about CVE matching accuracy. Consumer IoT metadata is structurally different from enterprise/server metadata (different port profiles, no HTTP headers, DHCP churn). The retrieved abstract does not report a headline accuracy figure, and IoT Inspector's own measurement bias applies. A small 8B model's reliability on adversarial or unfamiliar device classes is uncharacterised.
- **Relevance:** Supports a **modular pipeline** — discover candidate assets, then classify them locally with a small model — and supports labelling the *provenance and confidence* of every inferred asset attribute, which is the same discipline §7.6 demands of WHOIS-derived ownership.

---

## Verification ledger

Every URL cited in this review, the section that cites it, and its verification status. All URLs were checked on **2026-10-01**. "VERIFIED" means the primary source was retrieved (full abstract, PDF/HTML full text, or publisher page). "UNVERIFIED" means only metadata, a search snippet, or a third-party description was retrieved. Where a URL appears in more than one section the status differs by section and the row is marked as requiring care — see the individual entries, which always carry their own inline status marker.

| # | URL | Cited in | Status |
|---|---|---|---|
| 1 | https://arxiv.org/abs/2511.20313 | §1.1 | VERIFIED |
| 2 | https://arxiv.org/html/2511.20313v2 | §1.1 | VERIFIED |
| 3 | https://arxiv.org/abs/2503.14388 | §1.2 | VERIFIED |
| 4 | https://arxiv.org/html/2503.14388v2 | §1.2 | VERIFIED |
| 5 | https://www.cs.montana.edu/izurieta/pubs/SCORED2024.pdf | §1.3 | VERIFIED |
| 6 | https://exa.ai/library/publication/gqjwvrgm9hv | §1.3 | VERIFIED |
| 7 | https://giacomobenedetti.github.io/files/acns25.pdf | §1.4 | VERIFIED |
| 8 | https://arxiv.org/abs/2604.21111 | §1.5 | VERIFIED |
| 9 | https://arxiv.org/pdf/2604.21111 | §1.5 | VERIFIED |
| 10 | https://zenodo.org/records/19696658 | §1.5 | VERIFIED |
| 11 | https://fdn.montana.edu/cyber/products/Grype_Vs_Trivy_Boles_et_al.pdf | §1.6 | VERIFIED |
| 12 | https://www.ntia.gov/sites/default/files/publications/mcafee_-_2021.06.17_0.pdf | §2.2 | VERIFIED |
| 13 | https://www.cisa.gov/sites/default/files/2024-05/Software%20Transparency%20in%20SaaS%20Environments.pdf | §2.3 | VERIFIED |
| 14 | https://www.pnnl.gov/sites/default/files/media/file/Comparing%20Bills%20of%20Materials%20Tate.pdf | §2.4 | VERIFIED |
| 15 | https://www.oasis-open.org/2025/12/22/signal-in-the-noise-an-industry-wide-perspective-on-the-state-of-vex/ | §2.5 | VERIFIED |
| 16 | https://openssf.org/blog/2026/01/08/signal-in-the-noise-an-industry-wide-perspective-on-the-state-of-vex/ | §2.5 | VERIFIED |
| 17 | https://www.diva-portal.org/smash/get/diva2:2073107/FULLTEXT01.pdf | §2.6 | VERIFIED |
| 18 | https://ssl.engineering.nyu.edu/papers/sahay_sbomit_scored_2026.pdf | §2.7 | VERIFIED |
| 19 | https://ssl.engineering.nyu.edu/papers/torres-toto-usenix19.pdf | §2.8 | VERIFIED |
| 20 | https://www.linkedin.com/posts/thecolekennedy_sboms-data-analysis-activity-7252686307175337985-coz7 | §2.9 | UNVERIFIED |
| 21 | https://www.usenix.org/system/files/sec19-dong.pdf | §3.1 | VERIFIED |
| 22 | https://www.sciencedirect.com/science/article/abs/pii/S0167404823003875 | §3.2 | VERIFIED |
| 23 | https://arxiv.org/html/2505.13895 | §3.3 | VERIFIED |
| 24 | https://arxiv.org/html/2405.13568 | §3.4 | VERIFIED |
| 25 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7338193/ | §3.5 | VERIFIED |
| 26 | https://ar5iv.labs.arxiv.org/html/1705.05347 | §3.6 | VERIFIED |
| 27 | https://arxiv.org/html/2412.16607 | §3.7 | VERIFIED |
| 28 | https://dl.acm.org/doi/10.1145/3436242 | §4.1 | VERIFIED |
| 29 | https://arxiv.org/pdf/2302.14172 | §4.2 | VERIFIED |
| 30 | https://weis2023.econinfosec.org/wp-content/uploads/sites/11/2023/06/weis23-jacobs.pdf | §4.3 | VERIFIED |
| 31 | https://arxiv.org/abs/2411.02618 | §4.4 | VERIFIED |
| 32 | https://arxiv.org/html/2411.02618v1 | §4.4 | VERIFIED |
| 33 | https://exa.ai/library/publication/fdwnlr20pym | §4.5 | VERIFIED |
| 34 | https://github.com/scadastrangelove/kev_vs_epss | §4.5 | VERIFIED |
| 35 | https://preprints.ru/article/2868 | §4.5 | VERIFIED |
| 36 | https://arxiv.org/abs/2508.13644 | §4.6 | VERIFIED |
| 37 | https://arxiv.org/html/2508.13644 | §4.6 | VERIFIED |
| 38 | https://sol.sbc.org.br/index.php/sbseg/article/download/44316/44079/ | §4.7 | VERIFIED |
| 39 | https://dl.acm.org/doi/10.1109/TDSC.2022.3152164 | §4.8 | VERIFIED |
| 40 | https://asu.elsevierpure.com/en/publications/licality-likelihood-and-criticality-vulnerability-risk-prioritiza/ | §4.9 | VERIFIED |
| 41 | https://exa.ai/library/publication/bngm9cjv9fj | §4.9 | VERIFIED |
| 42 | https://export.arxiv.org/pdf/2208.02369v2.pdf | §4.10 | VERIFIED |
| 43 | https://www.sei.cmu.edu/library/prioritizing-vulnerability-response-a-stakeholder-specific-vulnerability-categorization-version-20/ | §4.11 | VERIFIED |
| 44 | https://certcc.github.io/SSVC/topics/evaluation_of_draft_trees/ | §4.11 | VERIFIED |
| 45 | https://certcc.github.io/SSVC/topics/ | §4.11 | VERIFIED |
| 46 | https://certcc.github.io/SSVC/topics/decision_trees/ | §4.11 | VERIFIED |
| 47 | https://www.researchgate.net/publication/358547679 | §4.12 | UNVERIFIED |
| 48 | https://www.mdpi.com/2079-9292/11/21/3580 | §4.13 | VERIFIED |
| 49 | https://www.jstage.jst.go.jp/article/comex/15/5/15_2025XBL0172/_pdf/-char/en | §4.14 | VERIFIED |
| 50 | https://docs.guac.sh/guac/guac-ontology/ | §5.1 | VERIFIED |
| 51 | https://github.com/guacsec/guac | §5.1 | VERIFIED |
| 52 | https://security.googleblog.com/2022/10/announcing-guac-great-pairing-with-slsa.html | §5.1 | VERIFIED |
| 53 | https://openssf.org/blog/2024/03/07/guac-joins-openssf-as-incubating-project/ | §5.1 | VERIFIED |
| 54 | https://openssf.org/projects/guac/ | §5.1 | VERIFIED |
| 55 | https://sms.carm.es/ricsmur/bitstream/handle/123456789/25906/10.1016j.cose.2025.104815.pdf | §5.2 | VERIFIED |
| 56 | https://people.bu.edu/staro/TOPS-2024-Final.pdf | §5.3 | VERIFIED |
| 57 | https://www.sciencedirect.com/science/article/abs/pii/S0167404824004978 | §5.4 | VERIFIED |
| 58 | https://www.sciencedirect.com/science/article/abs/pii/S0167404825004158 | §5.5 | VERIFIED |
| 59 | https://ceur-ws.org/Vol-4176/fomi-4.pdf | §5.6 | VERIFIED |
| 60 | https://ceur-ws.org/Vol-4085/paper35.pdf | §5.7 | VERIFIED |
| 61 | https://peerj.com/articles/cs-2768 | §5.8 | VERIFIED |
| 62 | https://arxiv.org/html/2609.08040v1 | §6.1 | VERIFIED |
| 63 | https://github.com/steven1518/vex-bench | §6.1 | VERIFIED |
| 64 | https://arxiv.org/html/2608.19430v1 | §6.2 | VERIFIED |
| 65 | https://arxiv.org/abs/2601.22952 | §6.3 | VERIFIED |
| 66 | https://arxiv.org/abs/2603.06422 | §6.4 | VERIFIED |
| 67 | https://arxiv.org/abs/2510.20739 | §6.5 | VERIFIED |
| 68 | https://www.usenix.org/conference/usenixsecurity25/presentation/huang-szu-chun | §7.1 | VERIFIED |
| 69 | https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-1015-huang-szu-chun.pdf | §7.1 | VERIFIED |
| 70 | https://ceur-ws.org/Vol-4085/paper8.pdf | §7.2 | VERIFIED |
| 71 | https://zakird.com/papers/censys-2025.pdf | §7.3 | VERIFIED |
| 72 | https://doi.org/10.1145/3718958.3754344 | §7.3 | VERIFIED |
| 73 | https://www.lancs.ac.uk/scc/assets/papers/2025/2502_sigcomm_poster.pdf | §7.4 | VERIFIED |
| 74 | https://conferences.sigcomm.org/sigcomm/2025/papers/sigcomm25-poster-session.pdf | §7.4 | VERIFIED |
| 75 | https://doi.org/10.1145/3634737.3656295 | §7.5 | VERIFIED |
| 76 | https://weis2026.econinfosec.org/wp-content/uploads/sites/13/2026/05/WEIS2026_paper_8.pdf | §7.6 | VERIFIED |
| 77 | https://www.mdpi.com/2079-9292/14/16/3267 | §7.7 | VERIFIED |
| 78 | https://arxiv.org/abs/2412.15696 | §7.8 | VERIFIED |
| 79 | https://arxiv.org/abs/2510.13817 | §7.9 | VERIFIED |

## Repeated limitations across the literature

The following limitations recur **independently across multiple papers and subfields**. For an infrastructure-wide CVE checker they are structural properties of the problem, not implementation defects, and they should be stated as limitations of the project's own results.

1. **Benchmarks are small, self-annotated and internally derived.** VEX-Bench uses **75 cases** annotated by the authors' own expert network (§6.1); HARP's ground truth comes from **one organisation's** IT/security team (§6.2); the Triage-JS dataset is **1,883 packages** with human-reported labels (§6.5). At these sizes, model differences of a few percentage points are not statistically meaningful.
2. **Reference datasets are part of the system under test.** Mandl et al.'s ground truth *is* OSV, so OSV is perfect by construction (§1.5); HARP's evaluation labels come from the same organisation whose cases train its adapters (§6.2); Triage-JS labels derive from human reports that are themselves incomplete (§6.5).
3. **Errors are overwhelmingly in the false-positive direction, and metrics hide that.** Zhou et al. measured a **92.0%** false-positive rate (§1.1); "Sifting the Noise" reports FP detection above **92%** at baseline (§6.3); Huang et al. find **over 95%** of Shodan's banner-based detections are false positives (§7.1). Headline F1/accuracy figures in triage work (§6.1, §6.5) do not decompose this.
4. **Banner, version-string and inference-based detection is unreliable at scale.** The over-95% banner false-positive result (§7.1) is consistent with the CPE/name-normalisation problems in §3.1–§3.7 and with the overlapping-version-range problem identified in §5.8. Passive identification from strings is the weakest link across the whole review.
5. **Coverage is never complete and freshness is never guaranteed.** Most assets of large organisations are missed by conventional scanning (§7.5); Shodan omitted **52.07%** of confirmed-vulnerable endpoints (§7.1); ~65% of observed banner changes were captured within a 24-hour granularity over 47 days (§7.2); scan coverage falls to **62%** across all ports (§7.3).
6. **Platforms disagree with each other, and disagreement is systematic rather than noise.** Shodan, Censys and ZoomEye generate materially different attack surfaces of the same infrastructure (§7.4); Censys and Shodan observed different subsets of a controlled 235-token experiment (§7.2); scanner coverage reflects deliberate strategy (§7.8).
7. **Asset-to-owner attribution is both lossy and noisy.** WHOIS recall **58%**, precision implying **62%** false positives, **94%** overestimation of vulnerable hosts (§7.6); WHOIS naming remains "riddled with problems" per prior work cited there.
8. **LLM results are backbone- and scaffold-dependent and decay quickly.** "Sifting the Noise" shows collapse to the >92% baseline on weaker backbones (§6.3); VEX-Bench's models and harnesses differ on the same tasks (§6.1); SIABENCH measures a snapshot of models that will be superseded within a year (§6.4).
9. **Performance degrades from the binary decision to the justification.** VEX-Bench's largest gap is **15.5** points (GPT-5.4 mini) and **12.0** points (Claude Opus 4.6) (§6.1); VEX-Bench's authors state binary-only reporting "can overstate performance".
10. **Validation is bounded by the validator.** Nuclei templates validate Shodan (§7.1) and Shodan itself defines "vulnerable host" in §7.6; a tool that cannot exercise a service produces another false positive. "Reacts to a payload" is not "exploitable in context".
11. **Point-in-time snapshots decay.** Mandl et al. release a reconstruction tool because CVE data decays (§1.5); WEIS 2026 compares data as stale as 2014 registrations against 2022 self-reports (§7.6).
12. **Ground truth for asset discovery barely exists.** Only §7.6 establishes true ground truth, and it does so for one sector in one country. Relative-ground-truth tool comparisons found in search were of too low quality to cite (§"What I could not find").

---

## What I could not find

Recorded explicitly so the project's claims are not overstated, and so the gaps are addressable as future work.

1. **A peer-reviewed evaluation of PURL accuracy, PURL↔CPE mapping loss, or PURL resolution ambiguity at NVD/CVE scale.** §1.5 (Mandl et al.) supplies the nearest evidence — a ground-truth (ecosystem, component, version, vuln-id) benchmark across Maven, npm, NuGet and PyPI — but it uses OSV coordinates as its reference and does not quantify identifier-normalisation loss. §2.4 mentions PURL only as a machine-readability aid with no measurement. **This remains the largest identifier-layer gap**, and it is directly load-bearing since PURL is what GUAC and OSV use natively.
2. **Any independent, quantitative accuracy evaluation of GUAC.** §5.1 verifies the ontology and architecture only. No retrieved source measures whether GUAC's ingestion and reasoning actually improves CVE-matching accuracy or reduces false positives. Vendor benchmarks and design claims were not treated as evidence.
3. **Peer-reviewed OSV-Scanner precision/recall.** §1.5 measures third-party consumers against OSV data, and treats OSV as perfect by construction; no retrieved study independently measures OSV-Scanner's own precision/recall.
4. **A peer-reviewed publication describing OpenSPG in a knowledge-graph-for-vulnerability-management context** (§5.9). Only the GUAC/OpenSPG adjacency appears in general supply-chain tooling discussion. If the project intends to build on OpenSPG, this is a genuine literature gap and should be presented as an engineering choice, not an evidence-backed one.
5. **Complete author metadata for the SBSeg / SBGEP prioritization study** (§4.7), and full first-author-confirmed lists for the Boles et al. Trivy/Grype comparison (§1.6).
6. **A rigorous, independently validated benchmark of subdomain-enumeration recall against absolute ground truth.** Searches returned relative-ground-truth tool comparisons only (each tool evaluated against the union of the others), which cannot establish absolute recall and systematically favours tools with broader but less precise output. The certificate-ecosystem work of VanderSloot et al. — which reports that its aggregated CT + Censys approach captures **>99%** of certificates found by other techniques while still missing roughly **1.5%** relative to a crawl — is a promising, directly relevant source for passive-discovery completeness, but it is **UNVERIFIED** here: only search-indexed text was retrieved, not the paper itself. It should be retrieved before being cited. Note also that certificate transparency proves control of a *name*, not liveness of a *service*.
7. **Authoritative, primary-sourced guidance specific to vulnerability scanning of operational-technology (OT/ICS) networks** (for example CISA or NSA advisories). §7.7 argues from first principles that active scanning is inappropriate in critical infrastructure, but a citable standards document stating the constraint was not retrieved. The VEX-Bench §6.1 observation that Shodan located ICS/PLC devices within days (§7.2) makes the safety dimension material rather than theoretical.
8. **Reliable current figures for real-world CVE volume and ecosystem distribution** (for example NVD totals, or the share of CVEs that are dependency-level rather than code-level). All ecosystem-share statements in this review are therefore expressed relative to the retrieved studies' own datasets rather than as absolute proportions of the CVE corpus.
9. **Any evaluation of LLM-based systems for whole-infrastructure or multi-tenant CVE checking.** §6.3–§6.5 cover SAST triage, incident analysis and package-report triage separately; **no retrieved work combines LLM reasoning with network-wide asset discovery and dependency matching**, which is exactly this project's configuration. The closest benchmark (§6.1) is scoped to a single upstream-dependency judgement, and no retrieved paper reports end-to-end results for a discovery-to-CVE pipeline. This project should be presented as filling an unevaluated configuration, not as reproducing a validated result.
