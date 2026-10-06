# 02 — System Architecture

**Status:** design proposal, v0.1
**Design driver:** every architectural choice below is traceable to a documented failure in `docs/01`. Where a choice is a judgement call rather than an evidence-driven fix, it is marked **[judgement]**.

---

## 1. Design principles

Each principle exists because the corresponding failure is measured, not hypothetical.

| # | Principle | Failure it addresses |
|---|---|---|
| P1 | **A result is a fact plus its provenance.** No fact exists without recording how it was obtained. | 95% FP from banner inference; matching result is a property of (asset, generator, format, consumer) |
| P2 | **Uncertainty is a value, not an error.** `unknown` is a first-class state and is never coerced to "safe". | NVD `NA`/ANY wildcards; Dependency-Track's false negatives on `UNASSIGNED` severity; CISA's `under_investigation` |
| P3 | **Distro truth beats upstream truth for OS packages.** | Backports: CVE-2025-9086/curl, CVE-2005-3258/squid; Shodan's documented inability to see fixed enterprise Linux |
| P4 | **Infer and verify are different states.** Version match ≠ vulnerable. | Nmap's `LIKELY_VULN` precedent; USENIX payload-vs-banner result |
| P5 | **Preserve the inventory; re-derive findings.** Never store only the conclusion. | Docker Scout's non-portable CVE list; `.trivyignore` not surviving to the server |
| P6 | **Report coverage and freshness as outputs.** | Greenbone feed-latency invisibility; OSV's 10-day ingestion outage being undetectable from scanner output |
| P7 | **Safe by default.** Non-destructive verification only. | OT/ICS scanning hazard; MOVEit/FortiJump lesson that exposure ≠ permission to attack |

---

## 2. System overview

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                          CONTROL PLANE                                  │
 │   policy · scheduling · state store · provenance ledger · audit log     │
 └───────────────▲─────────────────────────────────────▲───────────────────┘
                 │                                     │
   ┌─────────────┴──────────┐            ┌─────────────┴──────────────┐
   │   DISCOVERY PLANE      │            │     ANALYSIS PLANE         │
   │                        │            │                            │
   │  ┌──────────────────┐  │  assets    │  ┌──────────────────────┐  │
   │  │ passive sources  │  │  +         │  │ identification       │  │
   │  │ CT logs, DNS,    │  │  evidence  │  │ banner→product,      │  │
   │  │ certificate,     │──┼───────────▶│  │ CPE/PURL resolution  │  │
   │  │ WHOIS, ASN       │  │            │  └──────────┬───────────┘  │
   │  └──────────────────┘  │            │             │              │
   │  ┌──────────────────┐  │            │  ┌──────────▼───────────┐  │
   │  │ declared sources │  │            │  │ applicability        │  │
   │  │ CMDB, inventory, │  │            │  │ distro-first,        │  │
   │  │ SBOMs, IaC       │──┼───────────▶│  │ backport-aware       │  │
   │  └──────────────────┘  │            │  └──────────┬───────────┘  │
   │  ┌──────────────────┐  │            │             │              │
   │  │ active probing   │  │            │  ┌──────────▼───────────┐  │
   │  │ authorised only, │  │            │  │ corroboration        │  │
   │  │ non-destructive  │──┼───────────▶│  │ multi-source         │  │
   │  └──────────────────┘  │            │  │ agreement check      │  │
   └────────────────────────┘            │  └──────────┬───────────┘  │
                                         │             │              │
                                         │  ┌──────────▼───────────┐  │
                                         │  │ verification         │  │
                                         │  │ non-destructive      │  │
                                         │  │ protocol checks      │  │
                                         │  └──────────┬───────────┘  │
                                         │             │              │
                                         │  ┌──────────▼───────────┐  │
                                         │  │ prioritisation       │  │
                                         │  │ EPSS·KEV·SSVC·       │  │
                                         │  │ exposure·criticality │  │
                                         │  └──────────┬───────────┘  │
                                         └─────────────┼──────────────┘
                                                       │
                                         ┌─────────────▼──────────────┐
                                         │   REPORTING PLANE          │
                                         │  confidence-tiered findings │
                                         │  coverage + freshness       │
                                         │  human-review queue        │
                                         └────────────────────────────┘
```

---

## 3. The core data model

This is the part that matters most. Most tooling collapses to `(asset, cve, version)`. The provenance-bearing model is the contribution.

### 3.1 Observation — what was seen, and how

```
Observation
  asset_id            → which asset
  observed_at         → timestamp
  acquisition_method  → banner | tcp_probe | tls_cert | http_header | dns |
                        dpkg_query | rpm_query | manifest | lockfile | sbom |
                        cloud_api | ct_log | whois | agent_report
  evidence            → raw bytes / hash of what was actually seen
  raw_product         → vendor string as reported, unnormalised
  raw_version         → version string as reported, unnormalised
  resolved_product    → canonical vendor/product after normalisation
  resolved_version    → canonical (epoch, upstream, release, distro) tuple
  resolution_confidence → 1.0 exact | 0.9 parsed | 0.5 inferred | 0.0 unresolved
  parse_notes         → e.g. "rpm epoch folded", "conan revision stripped"
```

**Why this shape.** It directly implements P1 and makes the Dependency-Track↔Trivy divergence *diagnosable*: both would produce observations, and the 50 false positives would localise to `resolved_version` parsing on one side. It also makes the grype#2606 SHA-pinned-action case representable — `raw_version` = the SHA, `resolution_confidence` = 0.0, so no range comparison is attempted and no false positive is emitted.

### 3.2 Applicability — is this version actually affected

```
Applicability
  observation_id   → links to Observation
  advisory_source  → distro_tracker | vendor_advisory | nvd | osv | ghsa | fss
  advisory_id      → DSA-5588-1 | CVE-2024-9143 | GHSA-xxxx
  range_representation → nvd_start_excluding | osv_events | dpkg_status |
                         apk_status | rpm_evr | github_lkavr
  verdict          → affected | not_affected | fixed | under_investigation
  justification    → CISA's five values (only for not_affected)
  evidence         → the specific upstream/dpkg/apk fact used
  precedence_rank  → which source won, and what it outranked
```

**Why `range_representation` is a first-class field.** NVD encodes every range as version `*` plus `versionStart*` — Dependency-Track's maintainers note this *"isn't even a NVD data quality issue, it's how the NVD has always used version ranges,"* which guarantees SUBSET/SUPERSET relations. A distro tracker's answer is a **status**, not a range. Representing both explicitly is what allows P3 to be enforced rather than hoped for.

### 3.3 Finding — the graded output

```
Finding
  asset_id, cve_id
  confidence_tier     → VERIFIED | STRONGLY_INFERRED | INFERRED | WEAK | UNRESOLVED
  supporting_observations[]  → every observation that contributed
  applicability_votes[]     → every source's verdict, including dissent
  priority_score + breakdown
  evidence_bundle     → reproducible: inputs, source snapshots, versions
  suppression_state   → active suppression, with global scope
```

`supporting_observations[]` and `applicability_votes[]` are the anti-95%-FP mechanism. A finding that rests on one weak banner observation and one advisory match is visibly different from one corroborated across three sources — and the difference is machine-visible rather than buried in a confidence float.

**Precedent for the tier names:** Nmap's `VULNERABLE` vs `LIKELY_VULN`; CISA's `fixed` vs `under_investigation`; Shodan's own `verified` boolean (with the crucial addition that Shodan's *unverified* bucket is 95% wrong — hence this project does not treat "advisory matches version" as better than "unknown").

---

## 4. Module design

### 4.1 Discovery plane

Three source classes, because each has a documented blind spot (Rapid7's taxonomy) and no single method suffices.

| Source | Finds | Blind spot | Safety |
|---|---|---|---|
| **Passive** — CT logs, DNS, certificate transparency, WHOIS/ASN, cloud APIs | forgotten hosts, orphaned subdomains, shadow infrastructure | needs a name to exist; CT proves control of a name, not liveness of a service | fully safe |
| **Declared** — CMDB, IaC state, SBOMs, package manifests | what the organisation believes it runs; rich internal detail | only what is declared — the seed-list failure | fully safe |
| **Active** — TCP service probing, TLS handshake, HTTP header retrieval | real liveness, real banner, service actually listening | needs authorisation; **excluded entirely for OT/ICS segments** | non-destructive only |

**Attribution is a separate concern and is expected to fail.** Angelova et al. measured WHOIS attribution at 58% recall / 62% FP / 94% overestimation. The system therefore **never asserts ownership**; it records attribution as a hypothesis with its own confidence, and treats unattributed external assets as a distinct queue rather than silently including or excluding them.

**[judgement]** Active discovery is restricted to an explicit allowlist of CIDRs and hostnames. No CIDR is ever inferred from WHOIS or ASN data. Automatic expansion into "adjacent" ranges is the single most likely way this project could cause harm, and it is designed out.

### 4.2 Identification plane

Two stages, kept separate so failure is attributable.

**Stage A — normalise.** Parse the raw version string into a structured form using an **ecosystem-specific** comparator: RPM `epoch:upstream-release`, dpkg `upstream-debian_revision`, apk `version-rN`, semver, Python PEP 440, Go pseudo-versions, Maven. This is where the Dependency-Track ↔ Trivy 50-FP divergence lived, and it is the correct place to fix it because it is testable without any CVE data.

**Stage B — resolve identity.** Map `(raw_product, raw_version)` to a canonical identity: PURL where the ecosystem supports it, CPE 2.3 otherwise, with an explicit vendor-alias table. Aliases are **data, not code** — the 50.18% vendor-name inconsistency in NVD and the poco/pocoproject case are both table entries, not special cases. **[judgement]** This is where a modest alias table plus fuzzy matching gets most of the benefit, and where an LLM would be an unjustified dependency: identity resolution is a lookup problem with a measurable answer, not a reasoning problem.

**Non-negotiable:** when the version cannot be parsed, `resolved_version` is null and `resolution_confidence` is 0.0. The pipeline must not proceed to a range comparison. This is the single most important guard in the system.

### 4.3 Applicability plane

**Source precedence**, per P3:

```
1. Distribution / vendor security tracker     (dpkg status, apk tracker, RHSA/DSA,
                                              vendor PSIRT)     ← default for OS packages
2. Ecosystem-native advisory (OSV/GHSA)      ← default for language packages
3. Vendor advisory                            ← when the vendor ships one
4. NVD / CPE ranges                           ← last resort; NOT trusted for OS packages
```

Debian's tracker states the reason directly: triage *"is based on research and not just in the CVE description in order to prevent integrating false positives or incorrect data in the security tracker."* A system that automates triage must prefer the source that encodes that research, and must record when it falls back to (4) — because a fallback to NVD for an OS package is a known-wrong answer, not a best-effort guess.

**`<undetermined>` handling.** Debian's `<undetermined>` means *"someone needs to come back and revisit the issue."* The system maps this to `under_investigation`, **never** to `not_affected`. Same for `<no-dsa>` and `<postponed>`, which mean *no patch yet* — an unpatched asset must not be presented as low priority.

### 4.4 Verification plane

The decisive module, per H4. Non-destructive only, per P7.

- **Passive confirmation** — a second, independent source agrees on identity. Cheapest, always safe, and catches the majority of banner-inference errors.
- **Safe protocol checks** — request a version-identifying endpoint, compare the response against the candidate range. Read-only, single request, no state change. Explicitly **not** exploitation, and never sends a payload that could alter state.
- **Configuration evidence** — for `vulnerable_code_cannot_be_controlled_by_adversary`-class claims: is the service internet-reachable at all? Is it behind auth? These are observations about exposure, not about the software's internals, and they are cheap and reliable.

**Explicitly out of scope:** sending exploit payloads, fuzzing, or anything that changes service state. Justification is both ethical and practical: MOVEit and FortiJump show the realistic attacker path is mass exploitation of internet-facing services, so a defender's verifier has no legitimate need to be an attacker — and the project's own authorisation is for identification, not attack.

### 4.5 Prioritisation plane

**No single metric, per Beardsley.** Explicit multi-signal combination, each contribution reported separately so a human can see the breakdown:

| Signal | Use | Known limitation, carried into output |
|---|---|---|
| KEV membership | strong positive | only 32% useful for initial access; US-FCEB relevance; misses library CVEs |
| EPSS | likelihood | trailing indicator; 42/57 pre-KEV CVEs had low EPSS; recall 27% at τ≥0.1 |
| SSVC decision tree | explicit, auditable decision | decision quality depends on inputs; keep the tree visible |
| **Internet exposure** | attacker reachability | depends on attribution quality, which is itself 58% recall |
| Service criticality | business impact | requires declared input; absent → `unknown`, not "low" |
| Asset count of same CVE | blast radius | library CVEs hit everywhere; Beardsley names this exact class |
| CVSS | last, weighted low | Gamblin: *"we would kind of throw away CVSS today"* |

Exposure and criticality are given real weight rather than a token role because they are the two signals practitioners consistently report as missing once a scanner has run — and both are **directly observable from the discovery plane** the system already has. That is the practical advantage over a scanner that never sees the network.

### 4.6 Reporting plane

Three mandatory outputs. The first is the one no existing tool provides.

1. **Coverage and freshness report** — per source, per ecosystem: last successful ingest, record counts, and known gaps. Motivated by the OSV 10-day ingestion outage and Greenbone's feed-coverage lag, both of which were invisible in scanner output. **If a feed is stale, the system says so instead of reporting "no vulnerabilities."**
2. **Confidence-tiered findings** with the evidence bundle and the applicability vote breakdown.
3. **Human-review queue**, ordered by *expected information gain* rather than severity — items where a cheap check would collapse the uncertainty. **[judgement]** This directly addresses practitioner pain: "here's your attack surface, good luck" becomes "here are 12 things, and here is the one check that resolves each."

---

## 5. Technology choices

| Layer | Choice | Why |
|---|---|---|
| Language | **Python 3.12+** | Ecosystem-native package parsers already exist for dpkg/rpm/apk/semver/PEP440; a from-scratch parser would be a worse version of the problem |
| Version comparison | `packaging` (PEP 440), `rpm-vercmp` or equivalent for EVR, ecosystem adapters for apk/dpkg | Comparable semantics, not generic semver |
| Identity | PURL as primary, CPE 2.3 as fallback | PURL is what OSV/GHSA use natively; CPE remains necessary for OS packages |
| Advisory data | OSV + GHSA + distro trackers + NVD 2.0, **cached locally** | Local cache is required by P5 (re-derive, don't store conclusions) and makes rate limits a solved problem |
| State | SQLite for the observation ledger; Postgres optional | SQLite is sufficient for a lab-scale study and keeps the whole thing reproducible from one file |
| Probing | `asyncio` sockets; no external scanner dependency | P7 requires controlling exactly what is sent; shelling out to Nmap would surrender that control |
| Interfaces | CLI first, then a read-only HTTP API | Report generation is a first-class deliverable, not an afterthought |

**Deliberately not used:** LLM components in the core path. Justified in `docs/01` §4.2 — LLM results in this exact task area are backbone-dependent and collapsed from >92% to 6.3% on a weaker backbone. Any LLM use is an ablation measured against the non-LLM baseline.

---

## 6. What is deliberately not built

| Not built | Reason |
|---|---|
| Exploit generation or execution | Unauthorised, unsafe, and unnecessary for the stated problem |
| Full reachability/call-graph analysis | Savant: expensive *and* can itself miss vulnerabilities. Would trade visible FPs for invisible FNs. Reported as risk reduction, never as coverage. |
| Zero-day discovery | A different problem with a much higher bar (TitanCA, Antiproof, BUGSTONE-E2E) |
| OT/ICS active scanning | Inappropriate in critical infrastructure; explicitly out of scope |
| Automatic VEX generation | CISA: the applicability analysis *"might still be hard to automate"*; emitting `not_affected` without evidence is exactly how reachability filtering becomes a blind spot. The system will *consume* VEX and *suggest* statuses, never assert them. |
| Cloud/CDP-provider-wide scanning | Requires authorisation this project does not have |

---

## 7. Open design questions

1. **CPE fallback quality.** With PURL as primary, how much of the residual OS-package matching rests on CPE — and is that residual auditable? This touches the literature's largest identifier-layer gap (no PURL accuracy measurement at NVD scale).
2. **Attribution policy.** Angelova et al.'s 94% overestimation means external discovery will produce many findings the operator does not own. Options: separate queue (chosen), or require confirmation. Needs a usability check with a real operator.
3. **Suppression scope.** Dependency-Track forces per-project, per-version suppression (#5992). A global CVE↔component suppression is clearly better, but it needs a security argument: who may suppress, and what audit trail is required?
4. **Verification cost.** How many findings can be moved from `INFERRED` to `VERIFIED` per unit time, and does that throughput change what a human actually reviews? This is the metric that decides whether verification is worth building at all.
5. **Does the confidence tier change behaviour?** The strongest version of H3 is behavioural: analysts work the queue in tier order, so time-to-resolution on `VERIFIED`-able items falls. Without a human-subject study this stays a claim, not a result.
