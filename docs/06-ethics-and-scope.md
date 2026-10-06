# 06 — Ethics, Legal Scope, and Safety Boundaries

**Read this before writing any scanning code.** This is a project about identifying vulnerabilities in infrastructure, which sits close to activity that is regulated and criminalised if done without authorisation. The boundaries below are design constraints, not disclaimers.

---

## 1. Authorisation boundary — the hard line

**The checker may only ever scan infrastructure the operator owns or has explicit written permission to assess.**

Concretely, the design forbids:

| Forbidden | Why |
|---|---|
| Scanning third-party infrastructure, ever | Unauthorised access is a criminal offence in most jurisdictions regardless of intent. No exception for "it's just a port scan." |
| Inferring scan targets from WHOIS, ASN, or certificate data | The Angelova et al. measurement — 58% recall, 62% FP, **94% overestimation** — means inferred ownership is wrong most of the time. Scanning on that basis would mean scanning other people's hosts. |
| CIDR expansion beyond an explicit allowlist | "Adjacent" ranges belong to someone else. This is the single most likely way this project could cause harm, so it is designed out. |
| Any use of results from a previous scan of a third party | Tainted input is still unauthorised input. |

**Enforcement, not policy:** active discovery reads targets only from an operator-supplied allowlist file. There is no code path that adds a target from an external source. This is a structural guarantee, not a guideline.

---

## 2. Non-destructive operation

**Every active check is read-only, single-request, and justified as a version-identification probe.**

Permitted:
- TCP connect to identify an open port
- TLS handshake and certificate retrieval
- HTTP `HEAD` or `GET` of a version-identifying endpoint
- Reading a version string from a banner

Forbidden:
- **Sending exploit payloads of any kind**
- **Any request that changes server state** — no writes, no uploads, no configuration changes
- Fuzzing, resource exhaustion, or stress testing
- Authentication attempts against third-party services
- Scanning at a rate that could degrade the target (rate-limited by default)

**Why this boundary is both ethical and technically correct.** The realistic attacker path against internet-facing infrastructure is mass exploitation of known appliances and managed file-transfer software — the MOVEit, Citrix Bleed, Ivanti, and FortiJump pattern (`research/raw/03` §5). A defender's verifier has no legitimate need to be an attacker. And the project's own authorisation would be for *identification*, not attack.

**Verification is read-only by design.** The `VERIFIED` tier means "a safe, independent read-only check confirmed the service is running the affected version." It does **not** mean "exploitable." The literature is explicit that validation is bounded by the validator, and the report will respect that distinction in its language.

---

## 3. Operational technology and critical infrastructure — out of scope

**Active scanning is excluded entirely for OT/ICS networks.**

Reasons, in order of weight:
1. **Safety.** Scanning a control network can interfere with physical processes. Intrusion of an ICS environment is a real accident class, not a hypothetical.
2. **Unsuitability.** OT devices frequently use protocols with no safe enumeration, and legacy firmware may crash on unexpected input.
3. **Legal exposure.** Scanning critical infrastructure attracts regulatory attention regardless of authorisation.

For OT/ICS, the system will operate in **passive-only mode**: consume the operator's declared asset inventory and advisory data, perform no packets to the network. This limitation will be stated in the output, not silently applied.

---

## 4. Data handling and disclosure

### 4.1 What the tool stores

Observations, findings, and evidence bundles — all of which may contain internal hostnames, IP addresses, software versions, and banner text. Treated as **confidential internal security data**:

- Stored locally; the project ships no hosted service and no telemetry.
- No outbound calls except to public advisory APIs, and only advisory requests.
- Logs must not record full banner payloads by default (they can contain credentials in misconfigured services).
- Reports are generated for the operator; publication is their decision, not the tool's.

### 4.2 If a real vulnerability is found

The project is a *defensive* tool, so findings are the operator's to handle. But the case may arise where a finding affects third-party software in a way worth reporting upstream.

Procedure, agreed **before** it happens rather than improvised:

1. **Do not** test or verify on any third-party system to confirm it.
2. **Do not** disclose publicly on first sight.
3. Route via the vendor's published security contact or the relevant CERT/coordinator.
4. **Responsible-disclosure timing:** a 90-day window from first report is the community norm. A critical, actively-exploited vulnerability is reported faster.
5. If the operator's own infrastructure was affected, that is a finding to hand to them, not one to publish.

**[judgement]** The likelihood of this arising is low — the benchmark is a lab the operator controls — but the procedure is written down so the decision is not made under pressure.

---

## 5. Ethical position on the underlying research

The project consumes publicly available vulnerability data (NVD, OSV, GHSA, distro trackers) and openly published research. No attempt is made to obtain data that is not already public.

Two limits observed throughout:

- **No scraping behind authentication or paywalls.** 19 of 174 sources were paywalled; they are recorded in `research/sources/UNRESOLVED_SOURCES.md` and are **not quoted** in the project report. A paywall is a signal, not an obstacle.
- **No bypassing of access controls** on any advisory database. Public APIs are used within their stated rate limits, with backoff.

**Attribution of prior work is exact.** Every claim in `docs/04` is traceable to a URL in the verification ledger, with a VERIFIED/UNVERIFIED marker. Where a number came from a vendor's own marketing, it is labelled `[vendor-claim]` and not presented as fact — for example, runZero's "40% of assets invisible," which could not be traced to a primary source and is therefore not used.

---

## 6. Privacy

- **No personal data collection.** Hosts and services, not people. No user accounts, no tracking, no third-party analytics.
- **WHOIS/attribution data** is used to *avoid* scanning the wrong thing and to label attribution as a hypothesis. It is not used to build profiles of asset owners.
- **Employee privacy** — some banner data can reveal internal hostnames and user accounts. The tool stores what is needed for matching; it is not a personnel-monitoring system, and its output should not be used as one.

---

## 7. Known limitations of this project's own safety posture

Stated plainly, because a security tool that overclaims its safety is itself a risk:

1. **Active probing is inherently intrusive.** Even read-only, opening TCP connections to a service is visible to its operators and may trip alerting. Operators should know their own IDS will fire.
2. **Verification can be misread as exploitation.** The `VERIFIED` tier means a read-only probe succeeded. It is not evidence of exploitability and must not be reported as such.
3. **"Not affected" is a hypothesis.** Any `not_affected` the system emits from version or exposure reasoning is a *candidate for human review*, never a coverage claim. CISA requires human validation for exactly these judgements, and the project will not exceed what the standard permits.
4. **Passive discovery has no such guarantee.** A complete-looking asset list may still miss things, particularly CDN-fronted origins and cloud-only assets.
5. **The benchmark's completeness is artificial.** The lab has a known-complete manifest. Real infrastructure does not, and results from the lab must not be presented as a coverage claim about any real network.

---

## 8. Pre-flight checklist before any scan runs

- [ ] Written authorisation exists for every target in the allowlist
- [ ] Allowlist contains no inferred or expanded ranges — operator-supplied only
- [ ] OT/ICS segments excluded or set to passive-only
- [ ] Rate limits configured conservatively
- [ ] No state-changing checks compiled in (verify by reading the probe module)
- [ ] Log verbosity set so banner contents are not recorded
- [ ] Operator informed that IDS/alerting will trigger
- [ ] Disclosure procedure (`§4.2`) read and understood

**If any box is unticked, the scan does not run.**
