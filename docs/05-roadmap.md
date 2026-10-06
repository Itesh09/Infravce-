# 05 — Project Roadmap

**Working title:** INFRA-CVE — a provenance-grounded, confidence-tiered automatic CVE checker for infrastructure
**Assumed timeline:** 6–8 months, part-time, with a working evaluation at the end.

The ordering principle: **the evaluation is the contribution, so ground truth and the harness come before the checker.** Building a scanner first and evaluating it afterwards is how the field ended up unable to say where its errors come from.

---

## Phase 0 — Research and problem framing ✅ complete

| Task | Output | Status |
|---|---|---|
| Survey the tool landscape and data layer | `research/raw/01-tool-landscape-and-scanners.md` | done |
| Survey academic literature with verification ledger | `research/raw/02-academic-literature-review.md` (133 KB, 79 URLs) | done |
| Survey practitioner pain points and incident cases | `research/raw/03-practitioner-pain-points.md` | done |
| Archive all sources locally | 174 sources, 155 in full (66 MB), 19 stubbed as paywalled | done |
| Identify and defend the gap | `docs/01-problem-and-gap.md` | done |
| Design architecture | `docs/02-architecture.md` | done |
| Design evaluation | `docs/03-evaluation-plan.md` | done |

**Gate:** the gap must be defensible to an examiner who knows the field. If it is not, fix it here rather than after six months of building.

---

## Phase 1 — Ground truth and harness (weeks 1–4)

**Deliverable first, not last.** Without this there is nothing to measure against.

- [ ] **Lab environment** — Docker Compose topology with a versioned asset manifest covering all nine case classes in `docs/03` §3.1
- [ ] **Backport cases** — locate Debian and Alpine packages with confirmed upstream CVEs already fixed downstream. Source: `security-tracker.debian.org`, Alpine secdb, package changelogs. Record the DSA/status as the label's evidence.
- [ ] **Decoy services** — banners advertising a vulnerable version while running something else
- [ ] **WAF/CDN-fronted origin** — backend hidden behind a proxy
- [ ] **Unattributable asset** — present but not operator-owned
- [ ] **Ground-truth file** — one record per (asset, CVE) with: label, evidence source, evidence quote, advisory snapshot date
- [ ] **Blind labelling** — freeze and commit ground truth *before* the system runs against it
- [ ] **Metric harness** — FP and FN computed separately, never fused into a headline F1
- [ ] **Baseline runners** — Grype, Trivy, OSV-Scanner, and the naive banner+version matcher, all through identical ground truth

**Milestone M1:** baselines measured on frozen ground truth. *At this point there is already a reportable result: how badly do existing tools do on backport cases?*

**Risk:** the backport case set is the hardest part. If few clean cases can be sourced from distro trackers, the project's central claim weakens. Mitigation: start sourcing in week 1, not week 3; the Debian tracker has machine-readable data and its `<not-affected>` entries are exactly the target.

---

## Phase 2 — Core pipeline, identifier-first (weeks 4–9)

Build the parts that are testable without any CVE data, because they are where a large share of false positives originate.

- [ ] **Version normaliser** — ecosystem-specific comparators: PEP 440, RPM EVR, dpkg, apk, semver, Go pseudo-versions, Maven. Parse failures return `null` + `resolution_confidence = 0.0` and **halt the pipeline for that observation**
- [ ] **Normaliser test suite** — including the real strings from the tool survey: SHA-pinned actions, `1.3#0602…` Conan revisions, `1:1.12.20-8.el9`, `3.3.2-r0`, `(devel)`, `v46`
- [ ] **Identity resolver** — PURL primary, CPE 2.3 fallback, vendor-alias **as data not code**
- [ ] **Observation store** — SQLite schema from `docs/02` §3.1, with provenance on every row
- [ ] **Advisory ingest** — OSV, GHSA, NVD 2.0, **distro trackers (dpkg status, apk secdb, RHSA)**. All cached locally, all with per-source freshness timestamps
- [ ] **Applicability engine** — source precedence per P3; the four Debian states mapped with `<undetermined>` → `under_investigation`
- [ ] **Naive baseline as an in-process comparison** — the null hypothesis, run on every scan

**Milestone M2:** full pipeline end-to-end, naive baseline measured, no verification or prioritisation yet.

**Risk:** the `ANY`/`NA` CPE problem. Mitigation: PURL-first and treat CPE fallback as a measurable residual (this is open question 1 in `docs/02` §7 — report the residual rather than hide it).

---

## Phase 3 — Verification and confidence (weeks 9–13)

The layer that decides whether the project beats the null hypothesis.

- [ ] **Confidence tiering** — `VERIFIED` / `STRONGLY_INFERRED` / `INFERRED` / `WEAK` / `UNRESOLVED`
- [ ] **Corroboration** — multi-source agreement on identity
- [ ] **Safe protocol checks** — read-only, single request, no state change. Whitelisted checks only
- [ ] **Exposure evidence** — internet-reachable, auth-gated, internal-only. Observations, not inferences
- [ ] **Evidence bundles** — every finding reproducible: inputs, source snapshots, tool versions
- [ ] **Ablation E1** — full system vs. provenance-stripped variant

**Milestone M3:** E1 and E4 answered. *If the ablation shows no FP reduction, that is a publishable negative result and gets reported as one.*

**Risk:** verification becomes a rabbit hole into exploitation. **Hard boundary: no payload that alters state, no fuzzing.** If a check cannot be justified as a read-only version-identification request, it does not ship.

---

## Phase 4 — Prioritisation and reporting (weeks 13–16)

- [ ] **Multi-signal prioritiser** — KEV, EPSS, SSVC tree, exposure, criticality, blast radius, CVSS weighted low. **Every contribution reported separately**, so the breakdown is auditable
- [ ] **Criticality input** — from a declared file; **absent → `unknown`, never "low"**
- [ ] **Coverage & freshness report** — per source, per ecosystem: last ingest, counts, gaps. Must correctly predict incompleteness
- [ ] **Review queue** — ordered by expected information gain, not severity
- [ ] **Suppression** — global CVE↔component scope, with an audit trail and named authoriser
- [ ] **E5** — replay a simulated feed outage; does the report catch it?

**Milestone M4:** a complete run producing all three mandated outputs.

---

## Phase 5 — Full evaluation and write-up (weeks 16–22)

- [ ] Run E1–E7 from `docs/03` §5
- [ ] Per-stage error breakdown → **error taxonomy** (E6). The most reusable output
- [ ] Cross-tool agreement matrix (E7)
- [ ] Component B: public dataset arm, **reported separately, never pooled**
- [ ] Calibrate confidence tiers — observed precision per tier. If tiers are not monotonic, report the negative result
- [ ] Write the report: problem, literature, design, evaluation, limitations
- [ ] Package INFRA-CVE-Bench so others can re-run it
- [ ] **Restate every limitation from `docs/03` §6 against what actually happened**

---

## Phase 6 — Hardening and delivery (weeks 22–26)

- [ ] Threat model the checker itself — it parses untrusted banners and untrusted advisory data
- [ ] Rate limiting and backoff against public advisory APIs
- [ ] CI: tests, lint, type checking
- [ ] Documentation: user guide, architecture, contributing
- [ ] Demo on the lab environment
- [ ] Optional public write-up of the benchmark (the error taxonomy is the part worth publishing)

---

## Milestone summary

| Phase | Weeks | Milestone | Reportable result |
|---|---|---|---|
| 0 | done | Gap defended | Literature review, source archive |
| 1 | 1–4 | M1 baselines on frozen ground truth | How existing tools fail on backports |
| 2 | 4–9 | M2 pipeline end-to-end | Identifier-layer accuracy in isolation |
| 3 | 9–13 | M3 verification + E1/E4 | Does provenance+verification reduce FP? |
| 4 | 13–16 | M4 full system output | Prioritisation + coverage reporting |
| 5 | 16–22 | M5 complete evaluation | **Error taxonomy** — the main contribution |
| 6 | 22–26 | M6 delivered | Reproducible benchmark + report |

---

## Scope control — what gets cut, in order

If time runs short, cut from the bottom. The evaluation must survive; the features need not.

1. **Cloud-provider integrations** — cut first. Passive discovery covers most of the value.
2. **CPE fallback breadth** — narrow it, measure the residual, report it honestly.
3. **Component B (public dataset arm)** — report Component A only, and state that external validity was not established.
4. **Suppression UI** — a file is enough.
5. **Blast-radius scoring** — keep KEV/EPSS/exposure, drop the rest.

**Never cut:** ground truth provenance, the naive baseline, FP/FN separation, the coverage report, or the limitations section. Those are the project.
