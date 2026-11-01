# INFRA-CVE — B.Tech Project Evaluation 3 Presentation (Markdown Source)

> Format source for the Evaluation 3 presentation. Each slide below is kept to a
> small paragraph budget (max ~2 short paragraphs per page). Replace bracketed
> placeholders with the team's own content (screenshots, diagrams, numbers).

---

## Table of Contents

1. Title Slide
2. Project Title
3. Team Members
4. Mentor/Guide Name
5. Department & Institution
6. Introduction
7. Project Overview
8. Problem Statement
9. Objectives
10. Scope of the Project
11. Functional Specifications (CO4)
12. Identified System Requirements
13. Functional Requirements List
14. Non-Functional Requirements
15. Quantification and Completeness Analysis
16. Selection of Computing Framework / SDLC Model (CO4)
17. Evaluation of Different SDLC Models
18. Justification for Selected Framework/Model
19. Implementation Strategy
20. Use of Latest Design Tools (CO5)
21. Tools and Technologies Used
22. Reason for Tool Selection
23. Advantages and Relevance to the Project and System Design and Architecture (CO4)
24. System Architecture Diagram
25. Data Flow Diagrams / UML Diagrams
26. Database Design (if applicable)
27. Appropriateness of Design (CO4)
28. Design Principles Applied
29. Modularity, Scalability, and Maintainability
30. Design Validation and Review
31. Synchronization of Functionality with Design (CO4, CO5)
32. Mapping of Functional Requirements to Design Components
33. Integration and Testing
34. Traceability Matrix
35. Implementation Overview
36. Modules Developed
37. Key Features Demonstration (screenshots or flow)
38. Results and Discussion
39. Achieved Outcomes
40. Comparison with Objectives
41. Conclusion and Future Work
42. Summary of Work Done
43. Limitations
44. Future Enhancements
45. References
46. Tools, Frameworks, and Research Papers
47. Q&A / Thank You

---

## Slide 1 — Table of Contents

- Contains all slides listed above in the Table of Contents section.
- Keep the list short; remove irrelevant entries and add explicit ones as needed.

## Slide 2 — Title Slide

INFRA-CVE: A Provenance-Grounded, Confidence-Tiered Automatic CVE Checker for Entire Infrastructure.

B.Tech Project Evaluation 3 -- Initial Implementation and Synchronization (Rubric #R3).

## Slide 3 — Project Title

The project title for the evaluation is INFRA-CVE, positioned as a cybersecurity tool that
checks entire infrastructure against known CVEs with provenance and honest confidence.

## Slide 4 — Team Members

- Student 1: Itesh Jung Shahi, System ID 2023837775
- Student 2: Amit Kumar, System ID 2023345474
- Student 3: [Insert name and system ID]

## Slide 5 — Mentor/Guide Name

Dr. Deepthi P S, Associate Professor, Department of Computer Science & Engineering,
Sharda School of Engineering and Technology.

## Slide 6 — Department & Institution

Department of Computer Science & Engineering, Sharda School of Engineering and Technology.

## Slide 7 — Introduction

Existing infrastructure CVE tooling is measured at roughly 92% false positives even on verified
SBOMs, and no work has measured the composed discovery-to-confidence pipeline against ground
truth.

## Slide 8 — Project Overview

INFRA-CVE reads installed software (system package DB or manifest), normalises it, checks trusted
advisory sources (OSV, Debian, Alpine), applies distro-aware logic, stores provenance, and reports
findings with honest confidence tiers.

## Slide 9 — Problem Statement

Organisations use many systems, applications and packages together; most tools only match
package name plus version against a CVE list, causing huge false alert counts because backports
patch older versions without changing upstream versions.

## Slide 10 — Objectives

Reduce false CVE alerts, record clear evidence, assign honest confidence levels, and keep reporting
simple and safe for non-technical readers.

## Slide 11 — Scope of the Project

MVP scope: Linux host package databases (dpkg/apk), manifests, banner probes, OSV advisory lookup,
distro-aware applicability, verification, scoring, reporting.

## Slide 12 — Functional Specifications (CO4)

Functional requirements FR1 through FR8: asset input, identity mapping, version normalisation,
advisory lookup, distro-aware check, provenance storage, confidence tiers, simple report.

## Slide 13 — Identified System Requirements

Hardware: Intel Core i3 or higher, 4 GB RAM minimum (8 GB preferred), 50 GB free disk space.
Software: Linux/Windows, Python 3.10+, SQLite, requests/packaging/python-dateutil, OSV.dev,
Debian Security Tracker, Alpine secdb.

## Slide 14 — Functional Requirements List

FR1: Accept package info read-only (dpkg/apk query or manifest file).
FR2: Map each package to a standard form (PURL).
FR3: Normalise and compare versions correctly for different systems.
FR4: Check CVEs from OSV and distro security trackers.
FR5: Distro-aware check preferring distro fix info over upstream ranges.
FR6: Store provenance for everything seen.
FR7: Assign confidence tiers: Verified, Strongly Inferred, Inferred, Weak or Unresolved.
FR8: Simple report with proof and confidence.

## Slide 15 — Non-Functional Requirements

NFR1: Safety — strictly read-only.
NFR2: Clarity — easy for non-technical users.
NFR3: Honesty — say "unknown" when proof is missing.
NFR4: Reproducibility — same input plus same data gives same result.
NFR5: Lightweight — runs on a normal laptop.
NFR6: Evidence-Based — every reported CVE has stored evidence.

## Slide 16 — Quantification and Completeness Analysis

Baseline: 92% false positive rate for downstream scanners even with verified SBOMs. The MVP was
quantified against live scans (banner, inventory, web app) to show honest behaviour.

## Slide 17 — Selection of Computing Framework / SDLC Model (CO4)

Selected SDLC model: [Insert chosen framework/model, e.g., Agile/Waterfall].

## Slide 18 — Evaluation of Different SDLC Models

Compare at least two SDLC models (for example Agile iteration vs Waterfall phase gates) against
project needs: safety-critical advisory checking, rapid demo, academic timeline.

## Slide 19 — Justification for Selected Framework/Model

Choose one and justify: safety/read-only constraints, rapid evaluation delivery, academic deadlines.

## Slide 20 — Implementation Strategy

Strategy: discovery -> advisory ingest -> applicability -> verification -> scoring -> report,
incrementally demoed on Debian 12 hosts and a web application (Juice Shop).

## Slide 21 — Use of Latest Design Tools (CO5)

Use current design/authoring tools for diagrams, reports and code; latest design tools support the
design-to-implementation synchronisation requirement.

## Slide 22 — Tools and Technologies Used

Python, pydantic, httpx, pytest, mypy, ruff, OSV.dev, Debian Security Tracker, Alpine secdb,
Docker, SQLite, Markdown reporting, LaTeX for evaluation documents.

## Slide 23 — Reason for Tool Selection

All tools, databases and libraries are free and open source; no paid software, API or license;
runs on a normal laptop.

## Slide 24 — Advantages and Relevance to the Project and System Design and Architecture (CO4)

Design advantages: provenance grounding, distro-first logic, honest confidence, simple reporting.

## Slide 25 — System Architecture Diagram

[Insert architecture diagram: Discovery -> Ingest -> Applicability -> Verification -> Scoring -> Report].

## Slide 26 — Data Flow Diagrams / UML Diagrams

[Insert data flow / UML diagram for the pipeline].

## Slide 27 — Database Design (if applicable)

SQLite provenance store; raw version, normalised version, source, timestamp, advisory source,
reason, evidence link.

## Slide 28 — Appropriateness of Design (CO4)

Design is appropriate because it maps directly to requirements without scope creep.

## Slide 29 — Design Principles Applied

Provenance-grounded decisions, distro-first comparison, confidence tiers, honest unknown handling.

## Slide 30 — Modularity, Scalability, and Maintainability

Modules are small and single-purpose; maintainable for future ecosystems and assets.

## Slide 31 — Design Validation and Review

Design reviewed against requirements and threats-to-validity before implementation.

## Slide 32 — Synchronization of Functionality with Design (CO4, CO5)

Design components implemented: asset reader, identity resolver, version normaliser, advisory
ingestor, applicability engine, provenance store, confidence engine, report generator.

## Slide 33 — Mapping of Functional Requirements to Design Components

FR1-FR8 mapped onto the implemented components.

## Slide 34 — Integration and Testing

Integration and testing performed across discovery, ingest, applicability, verification and report.

## Slide 35 — Traceability Matrix

Traceability from requirements to implementation to results.

## Slide 36 — Implementation Overview

Implemented MVP modules under `src/infravce/`: discovery, advisories, applicability, verification,
reporting, prioritisation, CLI.

## Slide 37 — Modules Developed

List the developed modules and their responsibilities.

## Slide 38 — Key Features Demonstration (screenshots or flow)

[Insert screenshot: banner scan / inventory scan / Juice Shop scan].
[Insert flow diagram of the key features].

## Slide 39 — Results and Discussion

Live and inventory scans produced findings; Juice Shop scan produced 71 findings with top critical
CVE-2015-9235.

## Slide 40 — Achieved Outcomes

MVP delivered; tests green; live demos validated.

## Slide 41 — Comparison with Objectives

Achieved outcomes compared against the seven project objectives.

## Slide 42 — Conclusion and Future Work

Conclusion: INFRA-CVE demonstrates provenance-grounded, confidence-tiered CVE checking.

## Slide 43 — Summary of Work Done

Work summary: discovery, ingest, matching, verification, reporting, tests, demos.

## Slide 44 — Limitations

Honest limitations: live webapp banner mapping, specific ecosystem coverage, advisory freshness.

## Slide 45 — Future Enhancements

Future enhancements: more ecosystems, CI/CD integration, container SBOM scanning, issue export.

## Slide 46 — References

OSV.dev, Debian Security Tracker, Alpine secdb, literature (arXiv:2511.20313), project docs.

## Slide 47 — Tools, Frameworks, and Research Papers

Tools: Python, pydantic, httpx, pytest, mypy, ruff, Docker; research: Grype/Trivy, SBOM studies.

## Slide 48 — Q&A / Thank You

Thank you.
