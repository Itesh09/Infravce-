# Practitioner Pain Points and External Attack-Surface Workflows

**Date of research:** 2026-10-01
**Scope:** 2023–2026 practitioner talks, engineering blogs, incident-response research, community threads, and standards documents.

**Evidence quality tiers used throughout:**

- **[A]** authoritative primary source — vendor/distro/government/peer-reviewed/incident-response research
- **[P]** practitioner — conference talks, engineering blogs, community threads
- **[vendor-claim]** marketing or an undisclosed-dataset study; used only where the underlying behaviour is independently documented elsewhere

Where a number could not be traced to a primary document, that is stated. Vendor marketing figures are not treated as fact.

---

## 1. The vulnerability-management program is drowning in volume and low-quality data

### Volume growth is now structural, not cyclical

2024 produced **40,009 CVEs, up 38.83% year-over-year**; the top five CNAs alone accounted for **17,473 (43.67%)**, **6,292 records had no NVD CWE assignment**, and **695 were rejected** — [jgamblin.com/2024-cve-data-review](https://jgamblin.com/2025/01/05/2024-cve-data-review/) **[P]**

Speaking at BSides Munich 2025, Jerry Gamblin put the trajectory plainly: analysts *"were able to keep up when it was 20,000 CVEs a year… in the last 3 years, we've had about a 30% year-over-year growth. Last year, we broke 40,000 CVEs published for the first time. This year… closer to 55,000… and it's just not scaling."* The same talk notes NVD's enrichment backlog over **24,000 CVEs** awaiting processing, and that GitHub's global advisory database has roughly **130,000 GHSA entries** — meaning a stack can carry real risk with no CVE at all. Gamblin's explicit recommendation: *"we would kind of throw away CVSS today."* — [BSides Munich 2025 deck](https://rogolabs.net/Talks/Navigating%20the%20Volatile%20Vulnerability%20Landscape%20-%20BSides%20Munich.pdf) **[P]**

The practical consequence is stated bluntly by NIST's own coverage: CISA's NVD enriched nearly **42,000 CVEs in 2025 (~45% more than the year prior)**, its backlog exceeded **30,000**, and NIST had to narrow automated prioritization to **critical CVEs only** — [CSO on NIST CVE analysis](https://www.csoonline.com/article/4159882/nist-cuts-down-cve-analysis-amid-vulnerability-overload.html) **[A-adjacent, trade press]**

### Triage, not scanning, is the bottleneck

The clearest practitioner framing comes from Yotam Perkal (ex-PayPal vulnerability management) at BSides LV: *"vulnerability triage is by far one of the most painful processes in cybersecurity, anyone who has done it for a while has the scars to show it,"* because *"a vulnerability is only relevant in context"* — one CVE can appear a thousand times in an environment and be irrelevant every time but a few, [AllBSides transcript](https://allbsides.com/talk/sf_FdCqOSLg.html) **[P]**

His BSidesLV 2023 abstract frames the same problem as structural: most production code is third-party, discovery volume rises yearly, known-vulnerability exploitation *"remains one of the most common attack vectors,"* organizations *"can't keep up and are left with huge vulnerability backlogs,"* and *"current prioritization by CVSS score is suboptimal at best"* — [pretalx](https://pretalx.com/bsideslv23/talk/review/VCYNCXSUHPFBAGJLGMKHTJB7CHF99FHV) **[P]**

Community discussion matches: practitioners on r/devsecops identify "CVE alerts fatigue" as the dominant current challenge; a separate r/cybersecurity discussion argues attack-path and exploitability should displace CVSS dashboards as the primary decision input.

### The measurable false-positive burden

- **88.8%** of reported vulnerabilities in open-source components were false positives when assessed for actual exploitability, driven by simplistic component-to-vulnerability matching that ignores configuration and deployment context (Ponta et al., cited in [JKU thesis on VEX distribution](https://epub.jku.at/obvulihs/download/pdf/12450868)) **[A-secondary]**
- Practitioner datapoint of the same effect: the Isovalent talk at BSides London 2025 describes CI/CD vulnerability scanning blocked by noise — *"development teams do not want to deal with… false positives just for one CI that might actually be applicable"* — with one pipeline showing **2,550 false positives**. After wiring VEX into the pipeline, scans *"are mostly green about 85 to 90% of the time,"* and the workload shifted to dev teams with CODEOWNERS review gating, [AllBSides transcript](https://allbsides.com/talk/L6wGj4fef98.html) **[P]**

### Fragmentation is an architectural tax, not a complaint

The NVD is no longer the only system of record: CVE, GHSA, OSV, EUVD, vendor advisories, and CISA KEV all disagree on scope and cadence. Gamblin anticipates fragmentation continuing: *"I am not willing to bet money that in two years… there won't be three or four different vulnerability standards that companies have to deal with."* Mapping CVE↔GHSA↔OSV and reconciling conflicting CVSS scores becomes a data-engineering project, not a config toggle, [BSides Munich 2025](https://rogolabs.net/Talks/Navigating%20the%20Volatile%20Vulnerability%20Landscape%20-%20BSides%20Munich.pdf) **[P]**

---

## 2. Backported and silent patches break version-based detection

This is the least-solved problem in the entire workflow, and the official record is unambiguous about why.

### The distribution reality

Distributions fix CVEs by backporting without moving the upstream-looking version string. Debian's own tracker documents the downstream-analysis problem this creates: triage *"is based on research and not just in the CVE description in order to prevent integrating false positives or incorrect data in the security tracker. For example, if the CVE id says that something is vulnerable prior to version X, you need to check if that is the case as well as for the information given on distribution specific issues."* Proper research *"should include reading the code, finding fixes/commits in the upstream repository, or even writing patches yourself if you have the time and skills to do that."* — [Debian Security Tracker](https://security-team.debian.org/security_tracker.html) **[A]**

Debian tracks the resulting states explicitly, and they map directly onto scanner pain:

| Debian state | Meaning | Real-world consequence for scanners |
|---|---|---|
| `<not-affected>` | Vulnerable code absent, or fixed before the package was ever uploaded | Naive version matching still flags it as vulnerable |
| `<no-dsa>` (Minor issue) | Will be fixed *"via a point update or by piggypacking the fix with a future update for a more severe issue"* — i.e. **no patch exists yet** | Asset looks "not critical" but is unpatched |
| `<postponed>` | Fix queued for a future advisory | Same, with a longer horizon |
| `<undetermined>` | *"someone needs to come back and revisit the issue"* | Unresolvable signal; must be treated as unknown, not safe |

Concrete, current examples from the Debian record:

- **CVE-2025-9086 (curl):** upstream initially marked the wrong commit as introducing the vulnerability; the correct fix landed in `curl-8_13_0`, so `[bookworm] - curl <not-affected> (Vulnerable code introduced later)`. Any consumer checking "am I below the upstream fixed version?" gets a false positive on a fully patched distro package — [Debian tracker commit](https://www.mail-archive.com/debian-security-tracker-commits@alioth-lists.debian.net/msg72206.html) **[A]**
- **CVE-2005-3258 (squid):** `<not-affected>` purely because *"Bug was introduced in a patch to squid-2.5.STABLE10, this patch was never applied to the Debian package"* — the vulnerable code was never in the shipped artifact — [Debian Security Tracker](https://security-team.debian.org/security_tracker.html) **[A]**
- **python3.11 backport batch:** an LTS maintainer backported ~13 CVEs into `3.11.2-6+deb12u7` for bookworm, one of which *"was fixed upstream before 3.11 was branched off,"* and dropped another patch because the originating fix was an unreviewed upstream PR — [Debian release list](https://linux.debian.devel.release.narkive.com/Aytbrshn/processed-bookworm-pu-package-python3-11-3-11-2-6-deb12u7) **[A]**

Debian is explicit that its own data is imperfect: the generated site *"still has some false positives; with respect to packages in stable that are present in stable, but not vulnerable, these need to be triaged individually."* And severity is judged *"against the binaries as provided by Debian,"* so upstream severity cannot be inherited, **[A]**

### How the industry is trying to encode this

Docker's Hardened Images documentation resolves `fixed` vs `not_affected` by declining to use `fixed` at all: *"DHI does not use `fixed`. VEX-enabled scanners may not handle `fixed` consistently, so when Docker backports an upstream patch where the version number alone would not reflect the fix, it uses `not_affected` with `inline_mitigations_already_exist` justification instead."* — [docs.docker.com/dhi](https://docs.docker.com/dhi/explore/security-concepts/vex/) **[A/vendor]**

That is a workaround for a tooling gap, with a security cost: `inline_mitigations_already_exist` requires the mitigation *"cannot be subverted by the attacker and cannot be configured or disabled by the user"* (CISA's definition) — a strong claim to automate for a backport.

The practitioner-level framing: scanners that only compare version strings will flag patched OpenSSH/OpenSSL/curl/Nginx builds from major distros as vulnerable, generating a permanent low-grade noise floor that trains teams to ignore findings — [sitehost.nz](https://sitehost.nz/blog/vulnerability-scans-backported-patches) **[P]**

---

## 3. Reachability and VEX: "not reachable" ≠ "not exploitable" ≠ `not_affected`

### The vocabulary the standard actually defines

CISA's *Minimum Requirements for VEX* fixes the machine-readable vocabulary: `status` MUST be one of **`not_affected`**, **`affected`**, **`fixed`**, **`under_investigation`**. For `not_affected`, a `justification` SHOULD be provided (else an `impact_statement` MUST be), drawn from exactly five values — [CISA](https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf) **[A]**

| Justification | What it actually requires to prove |
|---|---|
| `component_not_present` | Reliable SBOM/attestation |
| `vulnerable_code_not_present` | Build-level evidence |
| `vulnerable_code_not_in_execute_path` | *"cannot be executed due to the way it is used by the product"* — complete call-graph/runtime evidence |
| `vulnerable_code_cannot_be_controlled_by_adversary` | Present and used, but the attacker cannot trigger it — configuration + exposure analysis |
| `inline_mitigations_already_exist` | Built-in protections that *"cannot be subverted by the attacker and cannot be configured or disabled by the user"* |

For `affected`, an `action_statement` is **MUST**-required.

### Where the standard itself concedes the hard part

CISA's *When to Issue a VEX* is the most useful document for understanding why this workflow still fails in practice ([CISA PDF](https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf)) **[A]**:

- Consuming tools *"should sufficiently validate the accuracy of VEX information, **involving human analysts when necessary**"* to reduce false positives.
- Automation helps with format and transport, but *"some parts, e.g., the analysis of whether the product is affected, **might still be hard to automate**."*
- Only `component_not_present` and `vulnerable_code_not_present` may be inherited downstream (unless the code is re-introduced). **Every `vulnerable_code_not_in_execute_path` or `vulnerable_code_cannot_be_controlled_by_adversary` claim must be re-derived per product** — because a downstream rebuild can change whether the code is reachable.
- Consumers must *"evaluate all supply chain paths and deconflict VEX information for multiple occurrences of the same upstream component,"* and *"accurate SBOM information is important in understanding supply chain paths."*

That inheritance rule is the crux: **reachability is a property of the build, not the dependency.** A vendor's `vulnerable_code_not_in_execute_path` claim about a library says nothing about your binary that statically linked it differently.

### The evidence burden is where reachability analysis breaks

The Savant paper documents the fundamental limit: version-only SCA produces false positives when vulnerable APIs are never called, but accurate control- and data-flow analysis is computationally expensive and **can itself miss vulnerabilities** (incomplete analysis, reflection, dynamic dispatch, configuration-dependent paths) — turning a false negative into a silent compromise, [arXiv:2506.17798](https://arxiv.org/html/2506.17798v2) **[A]**

OpenShift's engineering triage guidance encodes this conservatism: it requires per-release-branch analysis because features and reachability differ by version, and instructs triagers that absent branches or dependencies must remain `Uncertain` / `Unaffected` **based on evidence**, not assumption — [openshift-eng](https://github.com/openshift-eng/ai-helpers/blob/main/plugins/node-cve/commands/triage.md) **[A/practitioner]**

### Format fragmentation is a documented, unresolved tax

At least four VEX profiles are in production use — OpenVEX, CycloneDX VEX, CSAF VEX, SPDX 3.1 VEX — and they do not map cleanly. CycloneDX offers five granular reasons (`requires_configuration`, `requires_environment`, `protected_at_runtime`, …) that all collapse into CISA's single `vulnerable_code_cannot_be_controlled_by_adversary`, so converting **to** OpenVEX is deterministic but converting **from** it is lossy — [CycloneDX discussion #609](https://github.com/CycloneDX/specification/discussions/609) **[A]**

A community crosswalk flags `false_positive` → `not_affected` as genuinely **contested** (CycloneDX's `false_positive` state carries no justification, so it cannot be a valid OpenVEX statement at all) and marks the `cannot_be_controlled_by_adversary` group as `lossy` / `reverse_ambiguous`.

**Bottom line:** `not_affected` is a *claim someone must defend with evidence*, not a field a tool can infer. Treating any of these justifications as automatically filterable without validating the underlying proof is how reachability filtering turns into blind spots.

---

## 4. External asset discovery: the inventory *is* the vulnerability program

### The seed-list problem

Standard vulnerability scanners are architected around a manual input: *"They share a single point of failure: they require a manual list of IP addresses or ranges to scan. **If a server is not on the list, it is not scanned.**"* — [Precursor](https://www.precursorintelligence.com/blog/easm-vs-vulnerability-scanning) **[vendor]**

The same source cites "IBM's 2024 report indicates that 38% of breaches originate from unmanaged assets" — **second-hand and unverified**; the qualitative claim (unmanaged assets as breach origin) is well supported, the specific figure is not sourced to a primary document.

An empirical demonstration: Intruder's researchers used **public Certificate Transparency logs** (no access, no cooperation required) and found backup archives listing directory contents, active credentials, and source code on exposed hosts. Because publishing a TLS certificate requires a hostname, subdomain enumeration is an unavoidable side effect for defenders who want web-accessible systems — [Intruder](https://www.intruder.io/research/shadow-it-risks) **[vendor, but methodologically transparent and reproducible]**

The same research shows why per-domain review understates blast radius: one web-hosting provider was propagating vulnerable code, yielding **100 vulnerable hosts following the same naming conventions with the same vulnerability** — per-domain you'd see "one vulnerable site"; only enumeration reveals the shared provider as the unit of blast radius.

### Detection-method coverage gaps are measured, not argued

The USENIX Security 2025 study is the strongest empirical evidence here. It compared commercial internet-wide search engines and their CVE coverage against **payload-based validation**: Shodan tracked **38 CVEs**, ONYPHE **54**, with only **8 overlapping** — roughly 6 of every 7 CVEs found by one platform was invisible to the other. Across **37 CVEs** and **104,930 vulnerable endpoints**, banner/response-based detection produced substantial false positives, while verified Nuclei templates confirmed substantially more genuinely exploitable endpoints and exposed systematic **underreporting** of real-world exposure by search-engine-derived CVE inventories — [USENIX PDF](https://www.usenix.org/system/files/usenixsecurity25-huang-szu-chun.pdf) **[A/peer-reviewed]**

Read practically: CVE inventories attached to internet-wide search platforms are (a) mutually inconsistent and (b) systematically biased. Useful for hypothesis generation, not for coverage claims.

### Every discovery method has a blind spot, which is why single-method programs fail

Rapid7's engineering breakdown is the best available taxonomy, and every row has a hole — [Rapid7](https://www.rapid7.com/blog/post/2024/10/17/understanding-your-attack-surface-different-approaches-to-asset-discovery/) **[vendor/practitioner]**:

- **Deployed agents:** *"the problem that is encountered is that you cannot discover assets that do not have that software agent installed."* An IT-management agent *"will typically lack security controls, vulnerability and exposure context."*
- **Tool-data ingestion (CAASM):** broadest visibility, but *"since your tools might not agree on the fundamental aspects like the number of assets, it's necessary to ingest data across them to get closer to a truer picture."*
- **Passive network data (NetFlow, DHCP/ARP):** catches rogue devices on watched segments, but these agents *"need to be deployed on a specific network segment otherwise they won't be able to discover unknown assets."*
- **Active network scanning:** necessary but insufficient — *"The most difficult-to-discover Shadow IT assets can also be the most vulnerable, because they won't have the necessary security controls enabled. These assets are not discoverable through network data alone, as they provide no telemetry."*

Rapid7's framing: *"most organizations do not have 100% deployment coverage of agents."*

### CDN/WAF masking is an active blind spot

Cycognito's telemetry-based study reports enterprises in its dataset operating an average of **12 distinct WAF products (median 11), some over 30** — *"years of overlapping procurement, regional rollouts, and siloed security practices."* Its headline finding: **over 50% of enterprise external assets lack WAF protection**, attributed less to absent spend than to organizational fragmentation. It names the "unknown unknowns" explicitly: assets *"not part of any formal inventory"* — [Cycognito](https://www.cycognito.com/blog/state-of-waf-protection/) **[vendor, dataset undisclosed — methodology not independently verifiable]**

A real user complaint captures the practitioner experience: *"almost everything is good at finding assets but the prioritization stories feel thin. Basically 'here's your attack surface, good luck'"* — r/cybersecurity **[P]**

**Discovery is table stakes; the failure has moved to attribution and prioritization.**

---

## 5. Exploited-CVE detection failures: 4 incidents, 4 different failed stages

Chosen because each fails at a *different* stage of the workflow.

### MOVEit Transfer (CVE-2023-34362) — detection-speed failure: exploit preceded disclosure

Google Cloud Mandiant's post-mortem: exploitation was observed on **May 27, 2023**, four days *before* the May 31 public announcement of CVE-2023-34362. Attackers placed LEMURLOOT web shells, exfiltrated data, and in many cases **stole it within minutes** of exploitation. The entire detection window for the defenders Mandiant worked with existed only after mass exploitation was already underway, [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft) **[A/incident-response]**

**Which control failed:** neither scanning nor asset inventory. The gap is *time between exploit and advisory* plus near-zero dwell time. **Any workflow whose trigger is "new CVE published" is structurally blind to the first 4+ days.**

### Citrix Bleed (CVE-2023-4966) — exposure-management failure: slow patching of ubiquitous appliances

Citrix NetScaler session-token leakage led to mass exploitation that persisted and **expanded** into 2024, driven by ubiquitous deployment and sluggish patching of internet-facing appliances. The vulnerability was trivially detectable post-exploitation (session hijacking), yet stayed unpatched for months because appliances are business-critical and typically cannot auto-update — [Darktrace](https://www.darktrace.com/blog/stemming-the-citrix-bleed-vulnerability-with-darktraces-activeai-platform) **[vendor, self-interested; the sustained timeline is independently well corroborated]**

**Which control failed:** CVE intake and patch SLA for internet-facing edge infrastructure. Asset exposure was never in question; the question was whether anyone was checking exposure continuously.

### Ivanti Connect Secure (CVE-2023-46805 + CVE-2024-21887) — detection-content failure: the incident response *became* the blind spot

The most instructive case. During internal investigations, threat actors modified the **WIREFIRE** (aka GIFTEDVISITOR) web-shell implant — changing its code specifically to **evade publicly available YARA rules** — producing a variant that defenders were actively hunting for and could not detect — [Quo Intelligence](https://quointelligence.eu/2024/01/unc5221-unreported-and-undetected-wirefire-web-shell-variant/) **[A/threat-intel]**

**Which control failed:** signature-based detection coverage on the very indicator used for scoping. Signature IOC sets have a half-life measured in days, and forensic tooling itself became the evasion target.

### FortiGate / FortiJump (CVE-2024-47575) — disclosure-lag failure: exploitation preceded and outlasted the advisory

Bishop Fox reports exploitation of this FortiOS authentication-bypass flaw from **at least June 2024**, with news of in-the-wild exploitation circulating *before* the vendor advisory — the same pattern as MOVEit, six months of active exploitation that a CVE-triggered workflow cannot see — [Bishop Fox](https://bishopfox.com/blog/a-look-at-fortijump-cve-2024-47575) **[A/research]**

This is a **no-authentication-required** flaw on edge devices — asset exposure was never in question; the question was whether anyone was checking exposure continuously.

**Cross-cutting lesson:** in all four, the exploit ran against **internet-facing, well-known appliances and managed file-transfer software**. The failure was never "we didn't scan the host." It was timing, patch latency, indicator decay, or advisory lag — all upstream of scanner capability.

---

## 6. Where the field is heading (2024–2026)

**EPSS + KEV + SSVC as the prioritisation layer, VEX/SBOM as the applicability layer.** The layered pattern is now consensus. Avinash Nutalapati (BSidesLV 2025) lays out a phased rollout — EPSS + KEV integration first, then SBOM pilots, then CVSS v4, then VEX and reachability analysis, then SSVC decision trees last — with the key operational insight: **"the security tool severity is not the organization severity,"** and VEX integration *"requires a good amount of manual efforts and a major part of that human resources definitely skilled staff is required."* She also flags the audit-collision risk: inform audit teams of the new rating method or *"you just don't end up having an audit finding on critical vulnerability just because tool severity says it's critical"* — [AllBSides](https://allbsides.com/talk/pvRFP3aht7g.html) **[P]**

**Reduce 100 findings to 1 via layered evidence.** Perkal's target-state flow is the clearest published example of reachability used as a funnel rather than a gate: **100 occurrences** in an SBOM → vendor CSAF/VEX eliminates 80 as `vulnerable_code_not_present` → runtime analysis marks 25 as `vulnerable_code_not_in_execute_path` → network tooling marks 8 as `vulnerable_code_cannot_be_controlled_by_adversary` → human config validation marks 4 more → **5 occurrences left**, of which configuration checks identify **1** as actually exploitable. He labels this *"maybe a bit optimistic but it's a good start"* — [transcript](https://allbsides.com/talk/sf_FdCqOSLg.html) **[P]**

**Shifting VEX authorship to the teams with context.** The Isovalent workflow hands VEX maintenance to owning dev teams via PRs, gates merges through CODEOWNERS plus security approval, and generates markdown portals for customers who can't consume machine-readable VEX — explicitly to end *"the people who sent me these spreadsheets."* Notably, the talk reports Prisma Cloud lacking VEX processing functionality *"and doesn't have it on their road map at the moment"* — i.e. **a mainstream scanner cannot consume VEX** — [AllBSides](https://allbsides.com/talk/L6wGj4fef98.html) **[P]**

**Decentralised, AI-assisted intelligence aggregation.** Gamblin's closing position: the era of a single source of truth has ended; the work is aggregating N partial perspectives with different identifiers, scales and update cadences — mapping CVE↔GHSA↔OSV IDs, reconciling conflicting CVSS, building internal knowledge graphs, with LLMs applied to ingesting unstructured advisory text.

**Platform convergence (EASM + CAASM + CSPM + XDR → exposure management).** The observable market direction is consolidation into continuous, agent-based, attack-path-aware exposure platforms rather than more periodic scanners. Sizing claims (e.g. "two-thirds fewer breaches by 2026" for CTEM) are **forecasts, not measurements** — [vendor-claim, not validated].

**The uncomfortable practitioner question nobody has answered.** From a BSides London 2025 Q&A on VEX, asked directly: what if the threat is a **backdoor in the tool** — not a CVE at all? The answer on record: *"I don't think VEX solves that like that level of problem to be quite honest with you."* Automated applicability filtering, if scoped to CVE-matching, has nothing to say about intentional supply-chain compromise.

---

## Pain points ranked by impact

### 1. You cannot detect what you don't know exists — and CVE-matching only sees what you're told about

Every layer of the workflow (scanner seed lists, SBOM scope, VEX product IDs, patch applicability) is keyed to a declared inventory. Agents miss unmanaged hosts; passive network data misses silent devices; banner matching misses CDN-fronted origins and is measured as mutually inconsistent and underreporting (Shodan 38 vs ONYPHE 54 CVEs, 8 shared; 52.07% of confirmed-vulnerable endpoints unreported). CT logs prove unauthenticated enumeration of forgotten infrastructure. Compounding: ownership attribution is itself unsolved — the honest practitioner framing is *"here's your attack surface, good luck."*

**Mitigation:** continuous outside-in discovery as a first-class feed into the checker, not a periodic audit; and report coverage and confidence **per discovery method** rather than as a single number.

### 2. Version-based patch applicability is structurally wrong, and the authoritative data proves it

Distributions backport silently, defer patches as `<no-dsa>`/`<postponed>`, ship code where the bug was never present, and can even mis-record which commit introduced a bug (CVE-2025-9086/curl). A checker comparing version strings against upstream advisories generates permanent false positives on exactly the platforms that patch fastest. Compounding: reachability — the only real answer — is a property of the build, so CISA permits inheritance of `not_affected` **only** for component/code absence, never for reachability.

**Mitigation:** distribution-aware applicability data (Debian tracker, DSA records) + explicit `unknown` state; and accept that "fixed" must be re-derived per artifact.

### 3. Alert volume has outrun human triage capacity, and severity doesn't rank risk

40,009 CVEs in 2024 (+38.8%) with 6,292 lacking CWE and 695 rejected; NVD backlog >24,000–30,000; NIST narrowing automation to critical-only; ~88.8% of OSS component findings false-positive for exploitability; practitioner pipelines drowning in 2,550 FPs per CI. CVSS measures theoretical impact, not likelihood or context.

**Mitigation:** EPSS + KEV + SSVC as an automated first filter, VEX/reachability as the second, humans on the residue — and state plainly that reachability analysis remains largely manual.

### 4. Exploit-to-advisory lag makes CVE-triggered workflows structurally too slow

MOVEit: exploited May 27, announced May 31, exfiltration within minutes. FortiJump: exploited from at least June 2024, news circulating pre-advisory. In both cases the defenders' window was days-to-hours against attackers who moved first and left quickly. No scanner or prioritisation scheme recovers that time.

**Mitigation:** assume pre-disclosure exploitation; drive detection from asset-exposure monitoring and KEV matching, not from advisory arrival.

### 5. Detection content decays faster than vulnerabilities appear

The Ivanti WIREFIRE variant was written specifically to evade the public YARA rules defenders were hunting with. Signature-based IOC sets are per-incident and short-lived.

**Mitigation:** behavioural detection and asset-centric scoping over indicator matching.

### 6. The applicability and compliance standards themselves are fragmented and partly undecidable

Four VEX profiles with lossy, contested mappings; `component_not_present` vs `false_positive` not reconcilable in one direction; containers to map CVE↔GHSA↔OSV and reconcile conflicting CVSS; mainstream scanners (Prisma Cloud) unable to consume VEX; binary-delta proof (the NixOS-style evidence requirement) still community practice rather than standard.

**Mitigation:** pick one format, automate only the deterministic conversions, budget humans for the contested cells.

### 7. VEX/reachability tooling is automatable only in its easy cases

CISA states outright that *"the analysis of whether the product is affected might still be hard to automate"* and requires human analyst validation. Savant documents that accurate flow analysis is expensive **and** can miss vulnerabilities — reachability filtering trades false positives for false negatives, and false negatives are invisible.

**Mitigation:** treat reachability as risk-reduction, never as a coverage claim. Always report what the tool could not decide.

### 8. Nothing in this pipeline addresses the vulnerabilities that have no CVE

GHSA-only advisories (~130,000 and growing), future fragments of the CVE ecosystem, and outright supply-chain backdoors fall outside a workflow whose trigger is a CVE. Practitioners are noticing.

**Mitigation:** keep behavioural and provenance-based controls as a parallel, non-CVE-dependent program, and make the checker's CVE-dependence explicit rather than implicit.

---

## Sources and how to treat them

**Authoritative / primary [A]:** Debian Security Tracker · Debian tracker commit (CVE-2025-9086) · Debian LTS python3.11 backport batch · CISA Minimum Requirements for VEX · CISA When to Issue a VEX · USENIX Security 2025 (CVE detection coverage measurement) · Savant (reachability limits, arXiv 2506.17798) · CycloneDX VEX mapping discussion #609 · cve-bin-tool triaging docs · Docker DHI VEX policy · JKU thesis on VEX distribution (secondary citation of Ponta et al.) · Mandiant MOVEit post-mortem · Quo Intelligence WIREFIRE variant · Bishop Fox FortiJump

**Engineering / practitioner [P]:** OpenShift node-cve triage · Gamblin 2024 CVE data review · Gamblin BSides Munich 2025 deck + transcript · Perkal BSidesLV 2023 abstract + transcript · Nutalapati BSidesLV 2025 transcript · Isovalent BSides London 2025 transcript · Rapid7 asset discovery methods · Intruder CT-log shadow IT research · NIST/CVE-overload coverage (CSO) · r/devsecops alert-fatigue thread · r/cybersecurity exploitability-vs-CVSS thread

**Vendor — methodology disclosed, findings plausible:** Cycognito WAF study (dataset undisclosed) · Precursor seed-list analysis · sitehost.nz backport explainer · Darktrace Citrix Bleed (vendor with self-interest)

**Vendor marketing — do not cite as fact:** runZero "40% invisible assets" · ZeroFox EASM · ThingsRecon
