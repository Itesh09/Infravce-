# 01 — Problem Statement and Research Gap Analysis

**Project:** an automatic CVE checker for an entire infrastructure
**Field:** cybersecurity / vulnerability management
**Date:** 2026-10-01
**Evidence base:** 174 sources archived in `research/sources/`; 155 retrieved in full (66 MB), 19 preserved as explicitly-marked stubs because they are paywalled. Full survey in `research/raw/`.

---

## 1. The problem, stated precisely

Every organisation already has "a CVE checker." What nobody has is a CVE checker they can **trust for an entire infrastructure**, where:

1. **Discovery is continuous and outside-in**, not a seed list someone maintains.
2. **Every finding carries its own evidence and an honest confidence level**, rather than a flat list of "CVE + version" pairs.
3. **Distribution-specific truth overrides upstream version ranges**, because vendors backport.
4. **The output is a ranked, explainable decision**, not a count.

The reason none of the four currently holds is not missing engineering effort. It is that the field measures the *wrong* thing, and no published work has measured the composition of the pieces.

---

## 2. What the research establishes (the evidence for the gap)

### 2.1 The false-positive problem is measured, severe, and not caused by bad SBOMs

| Finding | Number | Source |
|---|---|---|
| FP rate of SBOM-based scanners on **lock-file-verified** SBOMs | **92.0%** (9 TP / 113 findings) | Zhou, Dacier & Konstantinou, arXiv:2511.20313 |
| FP pruned by function-call analysis | 61.9% (113 → 42) | same |
| Snyk and Dependabot accuracy in an independent SCA benchmark | **both below 15%** | Doyensec SCA benchmark |
| OSS component findings false-positive for actual exploitability | **88.8%** | Ponta et al., via JKU thesis |
| Banner-based CVE detections false-positive (Shodan, Nuclei-verified) | **>95%**; contradicted for 18 of 21 CVEs | Huang et al., USENIX Sec '25 |
| Accuracy ceiling for affected-version identification, 12 tools, 1,128 real vulns | **no tool above 45.0%** | arXiv:2509.03876 |

The Zhou et al. result is the load-bearing one, because it **rules out the easiest explanation.** They built SBOMs verified against lock files, so the SBOM was not the problem. Their conclusion: *"even with a perfect, ground-truth SBOM, the coarse, package-level analysis performed by downstream scanners might still produce unreliable results."* The failure is in the **binding step**, not the inventory step.

### 2.2 Version-based applicability is structurally wrong, and the authority says so

- **Debian's own tracker** requires manual code/commit research to decide applicability, not version comparison, and maintains `<not-affected>`, `<no-dsa>`, `<postponed>`, `<undetermined>` states precisely because versions are insufficient ([security-team.debian.org](https://security-team.debian.org/security_tracker.html)).
- **CVE-2025-9086 (curl)**: the correct fix landed in 8.13.0, so Debian bookworm is `<not-affected>`. Version comparison against the upstream range produces a false positive on a fully patched system.
- **CVE-2005-3258 (squid)**: `<not-affected>` because the bug was introduced in a patch Debian never applied — vulnerable code was never shipped.
- **Shodan documents its own limitation**: *"If the security patch doesn't change the version number (ex. running an enterprise Linux distribution) then it won't be detected as fixed."*
- **Docker's workaround** is to refuse to use `fixed` at all and emit `not_affected` with `inline_mitigations_already_exist` — a claim CISA defines as a mitigation that *"cannot be subverted by the attacker and cannot be configured or disabled by the user."*

**Conclusion:** upstream version ranges are not merely imprecise; for backported distributions they are *categorically wrong*, and the correct answer lives in a different database that no scanner treats as primary.

### 2.3 The identifier layer is measurably broken

| Defect | Measurement | Source |
|---|---|---|
| Vendor names inconsistent in NVD CPEs | **50.18%** (and 47.07% in CVEdetails) | VulCPE, arXiv:2505.13895 |
| CPE dictionary strings never referenced by any CVE | **81.40%** | same |
| Chrome CVE version ranges that were wrong | **134 of 167 verifiable (81%)** | Nguyen & Massacci, arXiv:1302.4133 |
| NVD version-range entries that were correct | **31%** verifiable at all | same |
| NVD CPE entries absent from the official dictionary | **105,591** | Benthin et al., arXiv:1705.05347 |
| NVD structured-CPE vs free-text consistency | **11.5%** | VERNIER |
| Cross-database exact match, NVD vs other VDBs | **20.3%** | VERNIER |
| Tools agreeing on vulnerability *count* (927 images) | **15.3%** | Boles et al. |
| Cross-tool agreement, 7 VEX tools | max Jaccard **0.694**; overall **0%** | Churakova et al., arXiv:2503.14388 |
| Root cause of cross-tool disagreement | DB overlap correlates **r = 0.88** | same |

The last row is the most useful for design: **which vulnerability database a tool queries explains its results better than the tool's own matching logic.**

### 2.4 Prioritisation signals are weaker than assumed

- **EPSS is a trailing indicator**: of 57 CVEs from 2023+ later added to KEV, **42 had consistently low EPSS** before inclusion; across 250 KEV entries, more than two-thirds sat below EPSS's own 36% threshold at inclusion.
- **Fewer than 20% of KEV CVEs received a high-confidence EPSS score before exploitation was public.**
- **KEV recall is structurally capped**: only ~83% of 2025 KEV additions had *any* EPSS score at decision time; recall 65% at τ≥0.001, **27% at τ≥0.1.**
- **KEV itself is narrow**: of 1,488 entries, only **483 (32%)** are useful for immediate initial access; inclusion requires relevance to the US FCEB; many are not remotely exploitable.
- Beardsley (ex-CISA KEV section chief) singles out the worst class: **library CVEs** — Log4Shell, HTTP/2 Rapid Reset, Heartbleed — as *"particularly notorious for their resistance to easy operational identification by vulnerability management software."*
- His conclusion: ***"no single metric can do prioritization for you."***

### 2.5 Asset discovery and attribution fail before matching even starts

- **Seed lists are the single point of failure**: *"If a server is not on the list, it is not scanned."*
- **CT logs** allow unauthenticated enumeration of forgotten infrastructure (Intruder's research found exposed backup archives with credentials and source code).
- **Every discovery method has a blind spot** (Rapid7): agents miss unmanaged hosts; passive network data misses silent devices; active scanning misses CDN-fronted origins; none sees cloud-only assets.
- **Attribution is lossy and noisy** (Angelova et al., WEIS 2026): WHOIS-derived ranges vs self-reported for Dutch municipalities gave **58% recall, 62% FP, and 94% overestimation of vulnerable hosts** — nearly all "vulnerabilities" came from addresses the municipalities do not own.
- Large organisations: conventional scanning **misses most assets** (Gelernter et al., ASIA CCS '24).
- Platform inventories disagree systematically: Shodan tracked 38 CVEs, ONYPHE 54, only 8 shared.

### 2.6 The window is often already closed before a CVE exists

- **MOVEit**: exploited **May 27**, announced **May 31**; data stolen within minutes. Four days of exploitation no CVE-triggered workflow could see.
- **FortiJump**: exploited from **at least June 2024**, news circulating before the advisory — six months.
- **Ivanti/WIREFIRE**: attackers modified their implant specifically to **evade the public YARA rules defenders were using to hunt it**.

Common factor: all three hit internet-facing, well-known infrastructure. The failure was never "we didn't scan the host" — it was timing, patch latency, indicator decay, and advisory lag.

---

## 3. The gap

### 3.1 What exists, and what each piece fails to do

| Existing capability | Covers | Does not cover |
|---|---|---|
| Grype / Trivy / OSV-Scanner / Snyk / Clair | image & SBOM version matching | external assets, backport truth, confidence tiering, evidence |
| Dependency-Track / GUAC | SBOM storage & composition | external assets, accuracy validation, ownership |
| Shodan / Censys | external host & banner discovery | correct CVE binding (95% FP), ownership, verified exploitation |
| Nmap / OpenVAS / Nessus | authenticated service scanning | fleet inventory, cross-source reconciliation, modern vuln-data semantics |
| EPSS / KEV / SSVC / CVSS | prioritisation signals | applicability — none knows whether your asset is affected |
| VEX (4 profiles) | applicability *statements* | CISA: analysis *"might still be hard to automate"*; requires human validation; mapping between profiles is lossy |

### 3.2 The specific gap this project targets

> **No published work evaluates an end-to-end pipeline that begins with outside-in asset discovery, produces per-observation provenance, resolves distribution-specific applicability, and emits findings with graded confidence and evidence — measured against ground truth.**

Confirmed by the literature review's own gap analysis (§ "What I could not find", item 9): *"no retrieved work combines LLM reasoning with network-wide asset discovery and dependency matching, which is exactly this project's configuration… no retrieved paper reports end-to-end results for a discovery-to-CVE pipeline."*

Corroborating gaps found in the tool survey:

1. **No independent accuracy evaluation of GUAC** exists.
2. **No peer-reviewed precision/recall for OSV-Scanner itself.**
3. **No PURL accuracy measurement at NVD/CVE scale**, despite PURL being what OSV and GUAC use natively.
4. **No absolute ground truth for asset discovery** except one sector in one country.
5. **No scan tool exposes its own feed-completeness status as a first-class output** — a scanner that would match correctly still reports nothing if the advisory is absent.

### 3.3 Why existing tools cannot simply be composed to fill it

Composition fails at three specific joints, each with a documented instance:

| Joint | Failure | Evidence |
|---|---|---|
| SBOM producer → SBOM consumer | Syft→CycloneDX→Trivy = **0 vulns**; Trivy direct = CVE-2024-9143. Alpine advisories key on source package `openssl`, inventory shows binary `libcrypto3`. | trivy discussion #7850 |
| Inventory → matcher | Same Rocky 9.4 SBOM: Dependency-Track **77** vs Trivy CLI **27**. 50 findings were verified false positives — RPM epoch/release field split. | dependency-track#3774 |
| Suppression → re-analysis | `.trivyignore` never reaches the server; DT discards attached VEX; OpenVEX upload fails schema validation. | trivy #8351, DT #4862 |

**A vulnerability-matching result is a property of (asset, generator, format, consumer) as a tuple — not a property of the asset.** No existing tool's output is portable, and no suppression decision survives a re-analysis.

---

## 4. The research question

> Can an infrastructure-wide CVE checker reduce false positives substantially below the published baseline (92% FP on verified SBOMs, >95% FP for banner matching, <15% accuracy for name+version tools) **without losing coverage**, by grounding every finding in per-observation provenance and distribution-specific applicability, and by reporting an explicit `unknown` state instead of coercing uncertainty into "safe"?

### 4.1 Hypotheses

- **H1 — Provenance grounding.** Attaching an acquisition method to every observation lets the checker distinguish *observed*, *inferred*, and *unresolved*, reducing false positives without reducing recall.
- **H2 — Distribution-first applicability.** Preferring distro/vendor advisories over upstream NVD ranges for OS packages reduces false positives on backported systems, where upstream ranges are categorically wrong.
- **H3 — Graded confidence.** Emitting an explicit confidence tier and an `unknown` state, rather than a binary verdict, changes what a human reviewer must look at — and is the property practitioners actually lack.
- **H4 — Verification closes the last gap.** Moving findings from `inferred` to `verified` via safe, non-destructive protocol probing eliminates the class of FP that banner inference cannot touch. This is what the USENIX result shows is decisive (payload detection vs banner inference).
- **H5 — Feed completeness is reportable.** Exposing per-source ingest freshness and coverage makes silent detection gaps visible, which no current tool does.

### 4.2 Explicit non-goals

- **Not** a vulnerability *discovery* system. TitanCA, BUGSTONE-E2E, Antiproof, and OpenAnt cover zero-day discovery; that is a different and much larger problem, and their 2025–2026 results set a bar this project does not attempt.
- **Not** a replacement for authenticated scanners (Nessus, OpenVAS) on a managed fleet. Active scanning of OT/ICS is inappropriate in critical infrastructure, and this project will not do it.
- **Not** an LLM-based reasoner in the first iteration. The literature is clear that LLM results are backbone-dependent and decay: on false-positive suppression, the best agent configuration fell from >92% to **6.3%** purely on backbone choice. Any LLM component must be an ablation, never the load-bearing path.
- **Not** a scanner of third-party infrastructure. Scope is strictly the operator's own assets (§ `docs/06`).

---

## 5. Contributions claimed

1. **An end-to-end evaluation that does not exist.** A benchmark measuring discovery → identification → applicability → confidence as one composed system, against ground truth, compared against the published baselines above.
2. **Provenance as a first-class data model.** Every observation carries its acquisition method and evidence; every finding carries the advisory source and range representation that produced it. This makes a wrong answer localisable to a layer — the property that lets the system improve rather than just report.
3. **An honest `unknown` state.** Precedent exists and is respected: Nmap distinguishes `LIKELY_VULN` from `VULNERABLE`; CISA defines `under_investigation`. Almost no operational tool emits this.
4. **Feed-completeness as a first-class output.** Per-source, per-ecosystem ingest freshness and coverage, addressing a failure mode that is currently invisible.
5. **Measured, honest handling of reachability.** Reported as risk reduction, never as coverage — because Savant documents that flow analysis is expensive *and* can itself miss vulnerabilities, trading visible false positives for invisible false negatives.

---

## 6. Honest limitations of this gap analysis

- The 92% and 97.5% FP figures come from **manual validation of four repositories**. They are a case study, not a population estimate. This project will report its own numbers on the same basis and label them so.
- **No absolute ground truth for asset discovery exists.** WEIS 2026's Dutch-municipality study is the only true ground truth found, for one sector in one country. The project will build its own ground truth for a controlled lab network and will say so.
- 19 of 174 sources are **paywalled and were not read in full**; they are listed in `research/sources/UNRESOLVED_SOURCES.md` and must not be quoted until obtained.
- The literature review's own analysis warns that **reference datasets are part of the system under test** in several studies (Mandl et al.'s ground truth *is* OSV, so OSV is perfect by construction; HARP's labels come from the same organisation that trains its adapters). Any comparison this project makes must state which side of that problem each baseline sits on.
