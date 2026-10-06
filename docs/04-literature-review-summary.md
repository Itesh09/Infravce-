# 04 — Literature Review Summary

**Purpose:** a condensed, citable summary for the project report. The full review with per-paper detail, verification status, and the 79-URL ledger is in `research/raw/02-academic-literature-review.md` (133 KB). Tooling detail is in `research/raw/01-tool-landscape-and-scanners.md`. Practitioner evidence is in `research/raw/03-practitioner-pain-points.md`.

**Verification convention used throughout:** a claim is marked **[V]** if the primary source was retrieved and read, and **[S]** if it rests on a search snippet or third-party description only.

---

## 1. Structure of the field

Infrastructure vulnerability management is not one problem but a **chain of five**, each with its own tooling and its own failure mode:

```
  discovery  →  identification  →  applicability  →  prioritisation  →  remediation
  (assets)      (what/version)      (are we hit)      (what first)        (what can we)
     ↑               ↑                   ↑                 ↑                  ↑
  EASM,          CPE/PURL,          NVD, OSV,          CVSS, EPSS,      patch mgmt,
  Shodan,        SBOM, banners      distro trackers    KEV, SSVC        VEX
  CT logs
```

The critical insight from the literature is that **each arrow is a separate research area with strong evidence about its own accuracy, and almost no evidence about the accuracy of their composition.** This project addresses the composition.

---

## 2. Discovery — you cannot check what you cannot see

**Method comparison (Rapid7).** Every method has a documented blind spot: deployed agents miss unmanaged hosts; passive network data (NetFlow, DHCP/ARP) requires per-segment deployment and provides no telemetry for silent devices; active scanning misses CDN-fronted origins; tool-data ingestion inherits each tool's disagreements. Rapid7's conclusion is that most organisations do not have 100% agent coverage. **[V]**

**Seed-list dependence.** Scanners "require a manual list of IP addresses or ranges to scan. If a server is not on the list, it is not scanned." **[S]** — vendor source, but the qualitative claim is uncontested.

**Certificate Transparency.** Publishing a TLS certificate requires a hostname, so subdomain enumeration is an unavoidable side effect of running a web-accessible system. Intruder's research used public CT logs with no access or cooperation to find exposed backup archives containing directory listings, credentials, and source code. **[V]**

**Attribution is the weakest link.** Angelova et al. (WEIS 2026) compared WHOIS-derived IP ranges for Dutch municipalities against self-reported ranges: **58% recall, 62% false positives, and 94% overestimation of vulnerable hosts** — nearly all reported "vulnerabilities" came from addresses the municipalities do not own. **[V]**

**Organisations miss most of their own assets.** Gelernter et al. (ASIA CCS '24) found conventional scanning misses most assets of large organisations, and proposed a taxonomy spanning on-premise, cloud, and outsourced infrastructure. **[V]**

**Platform inventories disagree systematically.** Shodan tracked 38 CVEs and ONYPHE 54 across the same period, with only 8 in common. **[V]**

---

## 3. Identification — the string-matching wall

### 3.1 CPE is broken at scale

| Measurement | Value | Source |
|---|---|---|
| Vendor names inconsistent in NVD CPEs | **50.18%** | VulCPE, arXiv:2505.13895 **[V]** |
| CPE dictionary strings never used by any CVE | **81.40%** | same **[V]** |
| NVD version-range entries verifiable | **31%** (167 of 539, Chrome) | Nguyen & Massacci, arXiv:1302.4133 **[V]** |
| Of those verifiable, ranges that were **wrong** | **81%** (134 of 167) | same **[V]** |
| NVD CPE entries absent from the official dictionary | **105,591** | Benthin et al., arXiv:1705.05347 **[V]** |
| Structured CPE vs free-text consistency within NVD | **11.5%** | VERNIER **[V]** |
| Cross-VDB exact match (NVD vs others) | **20.3%** | VERNIER **[V]** |
| Conclusion on automated CPE assignment | *"fully automated assignment of a CPE identifier to a software product is impractical and error prone"* | Benthin et al. **[V]** |

### 3.2 OSV's design avoids the problem — and has its own

OSV keys advisories to `(ecosystem, package name)` with `introduced` / `fixed` / `last_affected` events, letting each ecosystem define its own comparator. This is a genuine architectural improvement over CPE. **[V]**

Its limits: coverage depends on contributors; C/C++ OS packages are poorly covered; GHSA ingestion stalled for ~10 days in April 2026, and unreviewed GHSA advisories never reach OSV at all. **[V]**

**Important caveat on the evidence:** Mandl et al.'s ground truth *is* OSV, so OSV is **perfect by construction** in that study. No independent precision/recall measurement of OSV-Scanner itself was found. **[V]**

### 3.3 The version-string problem

Production inventories contain version strings that defeat naive comparison: Git SHAs, Go pseudo-versions, Conan revisions, RPM `epoch:upstream-release`, apk `-rN` revisions, `(devel)` markers, truncated semver, floating tags. Each is documented in a specific tool issue, and each produces a false positive. **[V]**

**The sharpest single illustration:** an SBOM generated by Syft and consumed by Trivy reported **0 vulnerabilities** on an image where Trivy's direct scan found CVE-2024-9143 — because Alpine's tracker keys the CVE to source package `openssl` while the inventory shows binary package `libcrypto3`, and no standard SBOM field carries that mapping. Trivy's own log warns: *"Third-party SBOM may lead to inaccurate vulnerability detection."* **[V]**

---

## 4. Applicability — the layer where upstream data is actively misleading

### 4.1 Backports

Debian's security tracker requires manual research — reading code, finding upstream commits, sometimes writing patches — to decide applicability, and states that severity is judged *"against the binaries as provided by Debian,"* so upstream severity cannot be inherited. **[V]**

Documented states and their scanner consequences:

| State | Meaning | Consequence for a version matcher |
|---|---|---|
| `<not-affected>` | vulnerable code absent, or fixed before upload | false positive |
| `<no-dsa>` | will be fixed later — **no patch yet** | looks non-critical, is unpatched |
| `<postponed>` | fix queued | same, longer horizon |
| `<undetermined>` | needs revisiting | unresolvable; must not be read as safe |

Concrete cases: **CVE-2025-9086 (curl)** — correct fix in 8.13.0, so bookworm is `<not-affected>`; version comparison yields a false positive on a patched system. **CVE-2005-3258 (squid)** — `<not-affected>` because the bug was introduced in a patch Debian never applied. **[V]**

Shodan documents the general failure itself: *"If the security patch doesn't change the version number (ex. running an enterprise Linux distribution) then it won't be detected as fixed by Shodan."* **[V]**

### 4.2 The SBOM-quality red herring

Two studies rule out "bad SBOMs" as the main explanation:

- **Benedetti & Cofano (ACNS 2025):** generated SBOMs from 2,225 Python projects. Precision was low across the board (cdxgen 17.08%, ORT 16.31%, Syft 12.39%, Trivy 12.17%), because **~75% of SBOM-listed dependencies are never actually installed** — manifests list what *could* be needed, not what was resolved. Only a lockfile-based generator (PIP-sbom) reached 80.95% precision. **[V]**
- **Zhou, Dacier & Konstantinou (arXiv:2511.20313):** using SBOMs verified against lock files as ground truth, Grype and Trivy produced 113 findings of which **9 were true positives — a 92.0% false-positive rate.** Function-call analysis pruned 61.9%. The authors' conclusion is that the problem is not the SBOM but *"the coarse, package-level analysis performed by downstream scanners."* **[V]**

**This is the finding the whole project rests on: a perfect inventory does not fix a coarse matcher.**

### 4.3 Reachability and VEX

CISA's *Minimum Requirements for VEX* defines four statuses and five `not_affected` justifications. CISA's *When to Issue a VEX* is candid about the hard part: consumers *"should sufficiently validate the accuracy of VEX information, involving human analysts when necessary,"* and the applicability analysis *"might still be hard to automate."* Critically, **only `component_not_present` and `vulnerable_code_not_present` may be inherited downstream**; every reachability claim must be re-derived per product, because a downstream rebuild can change reachability. **[V]**

The trade-off is documented by Savant (arXiv:2506.17798): accurate flow analysis is expensive **and can itself miss vulnerabilities** via reflection, dynamic dispatch, and configuration-dependent paths — converting false positives into silent false negatives. **[V]**

Four VEX profiles are in production use and do not map cleanly; CycloneDX's five granular reasons collapse into CISA's single `cannot_be_controlled_by_adversary`, making conversion lossy in one direction. **[V]**

A practitioner datapoint: wiring VEX into a CI pipeline took one organisation from 2,550 false positives to scans "mostly green about 85 to 90% of the time" — but with manual VEX authoring by owning teams through CODEOWNERS-gated PRs. **[S]** — conference transcript.

---

## 5. Prioritisation — every signal is weaker than assumed

**EPSS is a trailing indicator.** Of 57 CVEs from 2023+ later added to KEV, **42 had consistently low EPSS** before inclusion; across 250 KEV entries, more than two-thirds sat below EPSS's own 36% threshold at inclusion. **[V]**

**KEV recall is capped.** Only ~83% of 2025 KEV additions had any EPSS score at decision time; recall 65% at τ≥0.001 and **27% at τ≥0.1**. **[V]**

**KEV itself is narrow.** Of 1,488 entries (2026-01-14), only **483 (32%)** are useful for immediate initial access. Inclusion requires US FCEB relevance; many entries are not remotely exploitable or require authentication. 464 have Metasploit modules; 424 have ATT&CK mappings. **[V]**

**Library CVEs defeat KEV matching specifically.** Beardsley — a former CISA KEV section chief — names CVE-2021-44228 (Log4Shell), CVE-2023-44487 (HTTP/2 Rapid Reset), and CVE-2014-0160 (Heartbleed) as *"particularly notorious for their resistance to easy operational identification by vulnerability management software."* His conclusion: ***"no single metric can do prioritization for you."*** **[V]**

**CVSS is widely discounted in practice.** Gamblin (BSides Munich 2025) on a 40,009-CVE year: *"we would kind of throw away CVSS today."* **[S]** — conference talk. Volume: ~30% year-over-year growth, ~55,000 CVEs expected in the following year, NVD backlog >24,000. **[V/S]**

**ML prioritisation is promising but thin.** HARP (arXiv:2608.19430) reports P@K of 0.83–0.84 on a 7B backbone vs 0.49–0.51 for the best non-LLM baseline — but its ground truth comes from **one organisation's** IT/security team, and the same organisation trains its adapters. VEX-Bench shows LLM performance collapses on weaker backbones. **[V]**

---

## 6. Emerging work: LLM and agentic approaches

The 2025–2026 frontier is agentic pipelines. Four systems define the current bar, and all four target **code-level zero-day discovery**, not infrastructure CVE matching:

- **TitanCA** (SMU/GovTech) — four-module LLM agent pipeline; 203 confirmed zero-days, 118 CVEs, 127,000+ repositories analysed. **[V]**
- **BUGSTONE-E2E** — mines 2,710 verified fixing commits into 1,033 detection rules across 56 CWE families, packaged as 172 skills; runtime evidence for 644 of 2,933 findings. **[V]**
- **Antiproof** — neuro-symbolic detector synthesis plus proof-of-exploitability oracles; 44/46 BountyBench and 20/20 KEVBench, 12 CVEs assigned. **[V]**
- **OpenAnt** — reachability-filtered decomposition (97% surface reduction), adversarial attacker simulation, and ephemeral Docker exploit environments; 75.8% of findings reproduced. **[V]**

**Two results from this wave are directly relevant to infrastructure work:**

1. **Narrowing the analysis surface by reachability is the single most effective FP reducer** — 61.9% (Zhou et al.), 63.3% (earlier measurement on the same line of work), and OpenAnt's 97% surface reduction. **[V]**
2. **A narrowing funnel beats a bigger model.** BUGSTONE-E2E's explicit claim is that assigning one agent per candidate *"substantially lowers the required agent capability, enabling effective verification using smaller, cost-efficient models."* **[V]**

**And one warning:** on false-positive suppression for code alerts, the best agent configuration started above 92% and fell to **6.3%** on a weaker backbone, with gains entirely backbone-dependent. **[V]** This is why the project has no LLM in its core path.

---

## 7. The twelve recurring limitations

Recorded so the project states them as properties of the problem rather than discovering them again:

1. Benchmarks are small, self-annotated, internally derived.
2. Reference datasets are part of the system under test.
3. Errors are overwhelmingly false positives; F1 hides this.
4. Passive string-based identification is the weakest link.
5. Coverage is never complete; freshness never guaranteed.
6. Platforms disagree systematically, not randomly.
7. Asset-to-owner attribution is lossy **and** noisy.
8. LLM results are backbone- and scaffold-dependent, and decay fast.
9. Performance degrades from binary decision to justification.
10. Validation is bounded by the validator.
11. Point-in-time snapshots decay.
12. Ground truth for asset discovery barely exists.

---

## 8. The gap, restated

Seven gaps found in the literature itself, plus the central one:

1. **No peer-reviewed evaluation of PURL accuracy** or PURL↔CPE mapping loss at NVD/CVE scale — despite PURL being what OSV and GUAC use natively.
2. **No independent accuracy evaluation of GUAC.** Documentation and vendor claims only.
3. **No peer-reviewed precision/recall for OSV-Scanner** itself.
4. **No peer-reviewed OpenSPG work in a vulnerability-management KG context.**
5. **No absolute ground truth for asset discovery** beyond one sector in one country.
6. **Incomplete author metadata** for a few prioritisation and tool-comparison studies.
7. **No rigorous subdomain-enumeration recall benchmark** against absolute ground truth; existing comparisons use union-of-tools ground truth, which cannot establish absolute recall.
8. **No evaluation of LLM-based systems for whole-infrastructure CVE checking** — no retrieved work combines LLM reasoning with network-wide asset discovery and dependency matching, and no paper reports end-to-end results for a discovery-to-CVE pipeline.

**Item 8 is this project's contribution.** It should be presented as filling an unevaluated *configuration*, not as reproducing a validated result.
