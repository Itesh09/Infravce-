# 03 — Evaluation Plan

**Status:** design proposal, v0.1
**Purpose:** this document exists because the project's central contribution is an *evaluation*, and because the literature review identified twelve recurring methodological limitations that this study must not repeat.

---

## 1. Why the evaluation is the contribution

The gap in `docs/01` §3.2 is not that no good CVE checker exists. It is that **no published work measures the composition** of discovery → identification → applicability → confidence as one system against ground truth. Every existing tool is evaluated in isolation, and cross-tool comparisons are confounded by the fact that different tools query different databases (correlation **r = 0.88** between database overlap and report similarity).

So the first deliverable is not a scanner. It is **a benchmark and a measurement**, with the checker as the system under test.

---

## 2. Threats to validity, taken from the literature

The literature review recorded twelve recurring limitations. These are design constraints, not a limitations section to write at the end.

| # | Threat in prior work | How this study addresses it |
|---|---|---|
| 1 | **Benchmarks are small and self-annotated** (VEX-Bench: 75 cases; HARP: one organisation; Triage-JS: 1,883 packages) | Ground truth is **constructed**, not annotated by the authors, so it is independent of the system's own logic |
| 2 | **Reference dataset is part of the system under test** (Mandl et al.'s ground truth *is* OSV ⇒ OSV perfect by construction) | Ground truth is assembled from **multiple independent sources**, and disagreements are recorded rather than resolved silently |
| 3 | **Errors are almost all false positives; metrics hide it** (92% FP, >95% banner FP) | **FP and FN reported separately and never combined into a single headline number.** A single F1 would be the least informative output of this study |
| 4 | **Passive string-based identification is the weakest link** | Identification accuracy is measured *separately* from applicability accuracy, so the two are never conflated |
| 5 | **Coverage never complete, freshness never guaranteed** (Shodan omitted 52.07% of confirmed-vulnerable endpoints) | The benchmark reports **recall against known assets**, and the system emits a coverage report as a first-class output |
| 6 | **Platforms disagree systematically** | Ground truth includes a **deliberately ambiguous** subset; disagreement is measured, not resolved |
| 7 | **Asset attribution lossy and noisy** (58% recall, 62% FP) | Attribution is measured as its own task and reported separately from detection |
| 8 | **LLM results backbone-dependent** | No LLM in the core path. Any LLM experiment is an ablation with the backbone named and the non-LLM baseline shown |
| 9 | **Performance decays from decision to justification** | If any explanation is generated, binary and justification accuracy are reported **separately** (VEX-Bench's largest gap was 15.5 points) |
| 10 | **Validation bounded by the validator** | Verification is by non-destructive protocol checks only. **"Reacts to a probe" is not "exploitable"**, and the report must say so |
| 11 | **Point-in-time snapshots decay** | Ground truth is versioned, with the advisory snapshot used, so results are reproducible later |
| 12 | **Ground truth for asset discovery barely exists** | This study builds a lab ground truth with a known-complete asset list, and states its scope limits plainly |

---

## 3. The benchmark: **INFRA-CVE-Bench**

### 3.1 Two components

**Component A — controlled lab environment (primary).**

A Docker-based lab with a **known-complete asset manifest**, so discovery recall is measurable against an actual answer rather than a union-of-tools guess. Built to contain, by construction:

- **Backport cases** — a Debian and an Alpine package with a known upstream CVE already fixed downstream. The correct answer is `not_affected`, and version comparison alone gets it wrong. This is the single most important case class, because it is where existing tools fail and where the published CVE data is categorically misleading.
- **Never-present cases** — packages where the vulnerable code was never shipped (the squid CVE-2005-3258 pattern).
- **Deferred-patch cases** — `<no-dsa>` / `<postponed>`: vulnerable, unpatched. Must not be downgraded.
- **Ambiguous-identity cases** — deliberately split vendor namespaces (the poco/pocoproject pattern).
- **Unparseable-version cases** — SHA-pinned references, `(devel)` markers, truncated semver. Correct behaviour is `unresolved`, **not** a false positive.
- **Decoy services** — banners advertising a vulnerable version that the actual service is not running.
- **WAF/CDN-fronted origins** — a real backend behind a proxy that hides it, to measure the discovery blind spot.
- **Unattributable assets** — assets that exist but are not the operator's, to measure the attribution problem honestly.
- **Known-safe services** — to measure FP rate on a realistic mix rather than only on positives.

**Component B — public dataset arm (external validity).**

Public container images and datasets, scored against the same metric definitions, to check that lab results generalise. Ground truth here is weaker, so **it is reported separately and never pooled with Component A.** Pooling a constructed ground truth with a self-declared one would reproduce the exact methodological trap the literature warns about.

### 3.2 Ground-truth construction rules

1. **Every ground-truth label cites a source** — a DSA, a distro tracker status, a vendor advisory, a commit. No label without provenance, mirroring the system's own requirement.
2. **Multiple independent sources per label where available**; disagreements recorded as `under_investigation` rather than resolved by fiat. Following Debian's own practice.
3. **Blind labelling**: labels are frozen and committed before the system is run against them, so the system cannot be tuned to the answer.
4. **Versioned**: ground truth records the advisory snapshot date, since CVE data decays (threat 11).
5. **Ambiguity is a label.** If the correct answer genuinely is "depends," that is the label — not a discarded sample.

---

## 4. Metrics

### 4.1 Primary metrics — reported separately, never as one number

| Metric | Definition | Baseline it competes with |
|---|---|---|
| **False-positive rate** | findings not present in ground truth ÷ all findings | 92% (Zhou et al.); >95% banner (USENIX); 88.8% (Ponta et al.) |
| **False-negative rate** | ground-truth-affected assets missed ÷ all affected assets | Shodan's 52.07% underreporting (USENIX) |
| **Backport discrimination accuracy** | correct `not_affected` on backported packages | none published; this is new |
| **Unknown-handling accuracy** | correct `unresolved`/`under_investigation` on unparseable or undetermined cases | none published; this is new |

**Precision and recall are reported, but F1 is explicitly not the headline.** A single F1 would let a large recall gain conceal a 92% FP rate — which is precisely how the prior work's problem stayed invisible.

### 4.2 Secondary metrics — where the contribution actually is

| Metric | Why it matters |
|---|---|
| **Per-stage accuracy** (discovery → identification → applicability → verification) | Locates the error. "92% FP" is useless; "identification is fine, applicability on backports is 30%" is actionable. |
| **Provenance completeness** | % of findings whose full evidence chain is reproducible. Tests P1 directly. |
| **Confidence-tier calibration** | For each tier, the observed precision. **A `WEAK` tier that is 90% wrong is worse than useless** — it looks like signal. This is the metric that tests whether grading works at all. |
| **Verification yield** | % of `INFERRED` findings promoted to `VERIFIED`, and cost per promotion. Decides whether verification is worth building. |
| **Dissent rate** | % of findings where applicability sources disagreed. Measures how much the precedence rules are doing. |
| **Freshness-report accuracy** | Does the coverage report correctly predict when a scan will be incomplete? Tests P6 against the OSV-outage scenario. |
| **Suppression correctness** | Do global suppressions remove the right findings, with an intact audit trail? |

### 4.3 Baselines

Compared against, all measured on identical ground truth:

1. **Grype** (SBOM path) — the de facto reference implementation.
2. **Trivy** (image path) — the precision-first alternative; note the SBOM-path divergence (#7850) is itself a measured result.
3. **OSV-Scanner** — ecosystem-native, CPE-free.
4. **Banner-only naive matching** — `(product, version)` against NVD ranges, no provenance, no tiering. **This is the honest null hypothesis** and is the most informative comparison, because it isolates the contribution of everything added on top.
5. **CPE-computed (Nessus-style)** — demonstrates why computed CPEs inherit all wildcard defects.

**Every baseline is run through the same ground truth and the same metric code.** Baselines are not quoted from their own marketing: Snyk claims a 0.08% FP rate for its API/Web class, while the independent Doyensec benchmark put Snyk below 15% accuracy — a reminder to prefer measured numbers.

---

## 5. Evaluation questions

Each maps to a hypothesis in `docs/01` §4.1.

| # | Question | Method | Success criterion |
|---|---|---|---|
| **E1** | Does provenance grounding reduce FP without losing recall? (H1) | Ablation: full system vs. provenance-stripped variant, same ground truth | FP down significantly; recall within noise. **A recall loss is a failed result, not a trade-off** |
| **E2** | Does distro-first applicability fix backports? (H2) | Backport case class only | Materially higher accuracy than NVD-ranges-only (the baseline) |
| **E3** | Is the confidence tier calibrated? (H3) | Observed precision per tier | Monotonic and separated. Non-monotonic tiers ⇒ report as a negative result |
| **E4** | Does non-destructive verification close the last gap? (H4) | Compare `INFERRED` vs `VERIFIED` precision; measure yield and cost | `VERIFIED` precision materially above `INFERRED` |
| **E5** | Is feed-completeness reporting useful? (H5) | Replay a simulated feed outage; does the report predict the gap? | Outage is visible in the report |
| **E6** | Where do errors actually come from? | Per-stage breakdown | Produces a ranked list of improvement targets |
| **E7** | Do tools agree? | Cross-tool agreement matrix on identical input | Quantifies the r=0.88 database-overlap effect locally |

**E6 is the most likely to produce a genuinely new finding**, because the literature has no per-stage attribution for a composed pipeline.

---

## 6. Threats to this study's own validity

Stated up front, not buried.

1. **Lab results may not generalise.** Component A has a known-complete manifest; real infrastructure does not. Component B is reported separately for this reason.
2. **The lab is built by the same person evaluating it.** Mitigation: ground truth is derived from distro/vendor sources, not from inspecting the lab; and the blind-labelling rule in §3.2.
3. **Small-N.** A lab of this size will not produce statistically strong results. Reported as exact counts with Wilson intervals, not as percentages implying precision that does not exist. This mirrors VEX-Bench's 75-case weakness and does not pretend otherwise.
4. **The null hypothesis may win.** If naive matching matches the full system on FP rate, the honest conclusion is that provenance did not help on this workload. That is a publishable negative result and will be reported as one.
5. **Verification cannot prove exploitability.** Per threat 10, a service that reacts to a probe is not a service that is exploitable. All language in the report will respect that distinction.
6. **Reachability is out of scope, so `not_affected` claims are weak.** Any `not_affected` this system emits from version or exposure reasoning is a *hypothesis for review*, never a coverage claim. CISA's own guidance requires human validation here, and the project will not exceed what the standard permits.
7. **Snapshot decay.** Results are only valid for the advisory snapshot date, which is recorded in every artefact.

---

## 7. Deliverables from the evaluation

1. **INFRA-CVE-Bench** — the lab environment, ground truth with provenance, and harness. Re-runnable by others.
2. **Measurement report** — per-stage metrics, baselines, ablations, with FP/FN separated and negative results included.
3. **Error taxonomy** — the ranked list from E6, which is the reusable contribution: *where* infrastructure CVE matching fails, with evidence, rather than another tool that fails somewhere undisclosed.
4. **Honest limitations** — this document, updated with what actually happened.
