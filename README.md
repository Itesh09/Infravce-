# INFRA-CVE

**A provenance-grounded, confidence-tiered automatic CVE checker for entire infrastructure — and the benchmark that measures whether it works.**

Final-year cybersecurity project. Built on the finding that existing infrastructure CVE tooling is measured at **92% false positives** even on verified SBOMs, and that **no published work has measured the composed discovery → identification → applicability → confidence pipeline** against ground truth.

---

## The finding this is built on

Using SBOMs verified against lock files, Grype and Trivy together produced 113 findings of which **9 were true positives — a 92.0% false-positive rate** (Zhou, Dacier & Konstantinou, arXiv:2511.20313). Function-call analysis pruned 61.9% of the noise.

The authors' conclusion is the design brief:

> *"even with a perfect, ground-truth SBOM, the coarse, package-level analysis performed by downstream scanners might still produce unreliable results."*

**A perfect inventory does not fix a coarse matcher.** Everything here follows from that.

---

## Documentation

| Doc | What it covers |
|---|---|
| [`docs/01-problem-and-gap.md`](docs/01-problem-and-gap.md) | Problem statement, evidence for the gap, the research question, hypotheses, contributions, honest limitations |
| [`docs/02-architecture.md`](docs/02-architecture.md) | Design principles, system diagram, the provenance data model, module design, technology choices, open questions |
| [`docs/03-evaluation-plan.md`](docs/03-evaluation-plan.md) | Threats to validity, the INFRA-CVE-Bench design, metrics, baselines, evaluation questions |
| [`docs/04-literature-review-summary.md`](docs/04-literature-review-summary.md) | Condensed citable review for the report |
| [`docs/05-roadmap.md`](docs/05-roadmap.md) | Six phases, milestones, scope-cut order |
| [`docs/06-ethics-and-scope.md`](docs/06-ethics-and-scope.md) | Authorisation boundary, non-destructive operation, OT/ICS exclusion, disclosure procedure, pre-flight checklist |

## Research archive

Everything cited is downloaded to disk, not just linked.

| Path | Contents |
|---|---|
| [`research/raw/01-tool-landscape-and-scanners.md`](research/raw/01-tool-landscape-and-scanners.md) | Grype, Trivy, OSV-Scanner, Snyk, Clair, Dependency-Track, Shodan, Censys, Nmap, Nessus, OpenVAS + NVD/OSV/KEV data quality, with every documented limitation cited to a primary source |
| [`research/raw/02-academic-literature-review.md`](research/raw/02-academic-literature-review.md) | 133 KB, 7 sections, 79-URL verification ledger, recurring-limitations analysis, explicit gap list |
| [`research/raw/03-practitioner-pain-points.md`](research/raw/03-practitioner-pain-points.md) | Conference talks, backport reality, VEX/reachability limits, 4 incident case studies, pain points ranked by impact |
| `research/sources/` | **174 sources, 155 archived in full (66 MB)** across `papers/`, `standards/`, `tools/`, `practitioner/`, `blogs/` |
| `research/sources/DOWNLOAD_LOG.csv` | Per-source status, size, file path, retrieval note |
| `research/sources/UNRESOLVED_SOURCES.md` | 19 paywalled sources — **not quoted anywhere**, pending institutional access |

### Reproducing the archive

```bash
python3 research/build_manifest.py          # rebuild the URL manifest
python3 research/fetch_sources.py           # download (caches; skips what it has)
python3 research/fetch_sources.py --verify  # check cached files, no network
python3 research/retry_failed.py            # alternate routes for failures
python3 research/recover_open.py            # Semantic Scholar / arXiv mirrors
python3 research/recover_titles.py          # backfill titles, retry paywalled
```

---

## Key evidence, with numbers

| Finding | Value | Source |
|---|---|---|
| FP rate on **lock-file-verified** SBOMs | **92.0%** | arXiv:2511.20313 |
| FPs pruned by function-call analysis | 61.9% | same |
| Snyk / Dependabot accuracy, independent benchmark | **<15%** | Doyensec SCA benchmark |
| Banner-based CVE detections false-positive | **>95%** | USENIX Sec '25 |
| Confirmed-vulnerable endpoints Shodan missed | **52.07%** | same |
| Vendor names inconsistent in NVD CPEs | **50.18%** | arXiv:2505.13895 |
| CPE dictionary strings unused by any CVE | **81.40%** | same |
| Chrome CVE version ranges that were wrong | **81%** of verifiable | arXiv:1302.4133 |
| Cross-tool agreement (7 VEX tools) | max Jaccard **0.694** | arXiv:2503.14388 |
| Root cause of cross-tool disagreement | DB overlap, **r = 0.88** | same |
| Accuracy ceiling, affected-version ID, 12 tools | **<45%** | arXiv:2509.03876 |
| KEV entries useful for initial access | **32%** | runZero KEVology |
| EPSS recall against KEV at τ≥0.1 | **27%** | arXiv:2411.02618 |
| WHOIS attribution recall / FP | **58% / 62%** | WEIS 2026 |
| WHOIS overestimation of vulnerable hosts | **94%** | same |
| LLM FP-suppression, best config → weakest backbone | **92% → 6.3%** | arXiv:2601.22952 |

---

## Design principles

Each exists because the corresponding failure is measured, not hypothetical.

1. **A result is a fact plus its provenance.** No fact without recording how it was obtained.
2. **Uncertainty is a value.** `unknown` is a first-class state, never coerced to "safe".
3. **Distro truth beats upstream truth** for OS packages. Backports make upstream ranges categorically wrong.
4. **Infer and verify are different states.** Version match ≠ vulnerable.
5. **Preserve the inventory, re-derive findings.** Never store only the conclusion.
6. **Report coverage and freshness as outputs.** A stale feed must not read as "no vulnerabilities".
7. **Safe by default.** Read-only checks only; no state-changing requests, ever.

---

## Status

| Phase | State |
|---|---|
| 0 — Research and gap | ✅ complete |
| 1 — Ground truth and harness | ⬜ next |
| 2 — Core pipeline | ⬜ |
| 3 — Verification and confidence | ⬜ |
| 4 — Prioritisation and reporting | ⬜ |
| 5 — Full evaluation and write-up | ⬜ |
| 6 — Hardening and delivery | ⬜ |

**Before writing scanning code, read [`docs/06-ethics-and-scope.md`](docs/06-ethics-and-scope.md).** The authorisation boundary is enforced structurally, not by policy.
