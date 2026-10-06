<img src="https://static.scarf.sh/a.png?x-pxid=47937257-839d-491d-b693-703d11b910ad" style="display:none" referrerpolicy="no-referrer-when-downgrade" />

<div>

# [![Dependency-Track logo](/images/dt-logo-white-text.svg)](/)v4.14

- [Introduction](/)

<!-- -->

- [Getting Started](/getting-started/distributions/)
  - [Distributions](/getting-started/distributions/)
  - [Deploying Docker Container](/getting-started/deploy-docker/)
  - [Deploying on Kubernetes](/getting-started/deploy-kubernetes/)
  - [Deploying the Executable WAR](/getting-started/deploy-exewar/)
  - [Initial Startup](/getting-started/initial-startup/)
  - [Configuration](/getting-started/configuration/)
  - [Database Support](/getting-started/database-support/)
  - [Data Directory](/getting-started/data-directory/)
  - [Recurring Tasks](/getting-started/recurring-tasks/)
  - [LDAP Configuration](/getting-started/ldap-configuration/)
  - [OpenID Connect Configuration](/getting-started/openidconnect-configuration/)
  - [Internal Certificate Authorities](/getting-started/internal-ca/)
  - [Monitoring](/getting-started/monitoring/)
  - [Telemetry](/getting-started/telemetry/)
- [Usage](/usage/cicd/)
  - [Continuous Integration & Delivery](/usage/cicd/)
  - [Continuous Transparency](/usage/continuous-transparency/)
  - [Impact Analysis](/usage/impact-analysis/)
  - [Policy Compliance](/usage/policy-compliance/)
  - [Procurement](/usage/procurement/)
  - [U.S. Executive Order 14028](/usage/executive-order-14028/)
  - [Community Usage Examples](/usage/community-usage-examples/)
  - [Collection Projects](/usage/collection-projects/)
- [Analysis Types](/analysis-types/known-vulnerabilities/)
  - [Known Vulnerability Analysis](/analysis-types/known-vulnerabilities/)
  - [Outdated Component Analysis](/analysis-types/outdated-components/)
  - [License Evaluation](/analysis-types/license/)
  - [Component Identity](/analysis-types/component-identity/)
  - [Integrity Verification](/analysis-types/integrity-verification/)
- [Datasources](/datasources/nvd/)
  - [National Vulnerability Database](/datasources/nvd/)
  - [GitHub Advisories](/datasources/github-advisories/)
  - [Open Source Vulnerabilities](/datasources/osv/)
  - [Sonatype OSS Index](/datasources/ossindex/)
  - [Snyk](/datasources/snyk/)
  - [Trivy](/datasources/trivy/)
  - [VulnDB](/datasources/vulndb/)
  - [Datasource Routing](/datasources/routing/)
  - [Repositories](/datasources/repositories/)
  - [Internal Components](/datasources/internal-components/)
  - [Private Vulnerability Repository](/datasources/private-vuln-repo/)
- [Triage Results](/triage/auditing-basics/)
  - [Auditing Basics](/triage/auditing-basics/)
  - [Analysis States](/triage/analysis-states/)
  - [Suppression](/triage/suppression/)
- [Integrations](/integrations/ecosystem/)
  - [Ecosystem Overview](/integrations/ecosystem/)
  - [File Formats](/integrations/file-formats/)
  - [Fortify SSC](/integrations/fortify-ssc/)
  - [Kenna Security](/integrations/kenna/)
  - [DefectDojo](/integrations/defectdojo/)
  - [Notifications](/integrations/notifications/)
  - [REST API](/integrations/rest-api/)
  - [ThreadFix](/integrations/threadfix/)
  - [SVG Badges](/integrations/badges/)
  - [Community Integrations](/integrations/community-integrations/)
- [Best Practices](/best-practices/)
  - [Best Practices](/best-practices/)
- [FAQ](/FAQ/)
  - [Frequently Asked Questions](/FAQ/)
- [Terminology](/terminology/)
  - [Terminology](/terminology/)
- [Administration](/administration/users-and-permissions/)
  - [Users and Permissions](/administration/users-and-permissions/)

<!-- -->

- [Change Log](/changelog/)

</div>

<div class="section main">

<div class="version-banner">

This is the documentation for Dependency-Track v4.x. The documentation for v5.x can be found at [dependencytrack.github.io/docs](https://dependencytrack.github.io/docs/).

</div>

<div class="page-header">

## Dependency-Track

### Change Log

</div>

Subscribe with [RSS](/feed.xml) to keep up with the latest changes.

<div class="changelog">

<div class="changelog-item">

### v4.14.4 <a href="#v4-14-4" class="anchor">#</a>

<span class="date">September 14, 2026</span> <span class="badge patch">patch</span>

**Features:**

- Add support for ingestion of CycloneDX 1.7 BOMs - [apiserver/#6966](https://github.com/DependencyTrack/dependency-track/pull/6966)
- Use modern CycloneDX tools metadata in BOM exports - [apiserver/#7259](https://github.com/DependencyTrack/dependency-track/pull/7259)
- Remove unnecessary enrichment when querying for individual projects - [apiserver/#7258](https://github.com/DependencyTrack/dependency-track/pull/7258)
- Stop bumping `AffectedVersionAttribution.lastSeen` on every mirroring run - [apiserver/#7257](https://github.com/DependencyTrack/dependency-track/pull/7257)
- Reduce churn of vulnerable software associations during mirroring - [apiserver/#7256](https://github.com/DependencyTrack/dependency-track/pull/7256)

**Fixes:**

- Fix HTTP 500 when deleting vulnerabilities that are referenced by analyses - [apiserver/#7260](https://github.com/DependencyTrack/dependency-track/pull/7260)
- Fix `User-Agent` header missing for various HTTP requests - [apiserver/#7254](https://github.com/DependencyTrack/dependency-track/pull/7254)
- Fix Jira notification tests reporting success when no issue was created - [apiserver/#6792](https://github.com/DependencyTrack/dependency-track/pull/6792)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.14.4](https://github.com/DependencyTrack/dependency-track/milestone/70?closed=1)
- [Frontend milestone 4.14.4](https://github.com/DependencyTrack/frontend/milestone/55?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@AKSHATSPAR](https://github.com/AKSHATSPAR), [@valentijnscholten](https://github.com/valentijnscholten)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 94b907639f56fadce3e20026178d0c6d7f4ff2a0                         |
| SHA-256   | 08a8f517f571e5c2a3c4392de044ae8668beb0b2dec1bf172082676d1a9f9ad1 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 54ef0146414037b875d2670a1e282845d13a5516                         |
| SHA-256   | 5b993cfe4cf7855feba8b7454a529100186537f46ebbe9651b6c720ab184a9d1 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 3b7995b2f56f78a0f7c52f4cc420b2fa994e8ff7                         |
| SHA-256   | 8de5e7e888efce5c32cca0e60d70d47ec0d2a30de50dac2b3d4738af4cbe2f51 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.14.4/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.14.4/bom.json)

<a href="cloudcannon:collections/_posts/2026-09-14-v4.14.4.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.14.3 <a href="#v4-14-3" class="anchor">#</a>

<span class="date">July 20, 2026</span> <span class="badge patch">patch</span>

**Features:**

- Improve VEX import performance - [apiserver/#6141](https://github.com/DependencyTrack/dependency-track/pull/6141)
- Include `groupBy` parameter in DefectDojo finding upload - [apiserver/#6130](https://github.com/DependencyTrack/dependency-track/pull/6130)
- Include analysis detail in DefectDojo finding payload - [apiserver/#6181](https://github.com/DependencyTrack/dependency-track/pull/6181)
- Improve performance of OSV mirroring - [apiserver/#6345](https://github.com/DependencyTrack/dependency-track/pull/6345)
- Show exploit predictions from all sources - [frontend/#1523](https://github.com/DependencyTrack/frontend/pull/1523)

**Fixes:**

- Reject parent objects with null UUID when creating, updating or patching projects - [apiserver/#6355](https://github.com/DependencyTrack/dependency-track/pull/6355)
- Fix NPE and redundant queries in VEX / VDR export - [apiserver/#6614](https://github.com/DependencyTrack/dependency-track/pull/6614)
- Prevent duplicate downloads when using export and download buttons - [frontend/#1659](https://github.com/DependencyTrack/frontend/pull/1659)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.14.3](https://github.com/DependencyTrack/dependency-track/milestone/65?closed=1)
- [Frontend milestone 4.14.3](https://github.com/DependencyTrack/frontend/milestone/48?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@ElenaStroebele](https://github.com/ElenaStroebele), [@heyiamwahab236](https://github.com/heyiamwahab236), [@webdevred](https://github.com/webdevred), [@yuwwx](https://github.com/yuwwx)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 40db3eb67df441382971c8fb6566b86bc65976f4                         |
| SHA-256   | 11a5c85616b745803b5653016d9da2195f2e23ac66fe6a85d2ae2b4661d393a9 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 71a8e224166a55efb163922bb9874c151b3d95eb                         |
| SHA-256   | 4cbedd435f0f07b520216e4c30b9c81ca9a43044c569285ed1aa2e4f1533f5be |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | be91ca477d92f492cdd4e5d215e3154f97c50be5                         |
| SHA-256   | de3d76d978689d0fe571683cfeedf7fea095a1fd03f86cf622a099b5b72f4477 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.14.3/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.14.3/bom.json)

<a href="cloudcannon:collections/_posts/2026-07-20-v4.14.3.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.14.2 <a href="#v4-14-2" class="anchor">#</a>

<span class="date">May 07, 2026</span> <span class="badge patch">patch</span>

**Features:**

- Improve performance of vuln data source mirroring - [apiserver/#6040](https://github.com/DependencyTrack/dependency-track/pull/6040)
- Handle epoch PURL qualifier for version comparison - [apiserver/#6083](https://github.com/DependencyTrack/dependency-track/pull/6083)
- Add project filters to component identity search - [apiserver/#6087](https://github.com/DependencyTrack/dependency-track/pull/6087)

**Fixes:**

- Fix incorrect format of Composer packages being sent to Trivy - [apiserver/#6117](https://github.com/DependencyTrack/dependency-track/pull/6117)
- Fix incorrect version comparison of NuGet packages when v-prefix is present - [apiserver/#6116](https://github.com/DependencyTrack/dependency-track/pull/6116)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.14.2](https://github.com/DependencyTrack/dependency-track/milestone/64?closed=1)
- [Frontend milestone 4.14.2](https://github.com/DependencyTrack/frontend/milestone/36?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@Abdelmonem-BEN-NACEUR](https://github.com/Abdelmonem-BEN-NACEUR), [@hoobio](https://github.com/hoobio)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 953074d95757bea162931b7811885945bbe992aa                         |
| SHA-256   | 3ff379380d35b9ff924014b680e7f3718c119f59b2cc4ee6ece4345a3ca1c110 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 53f3198f5422e1117f53859c5f42403f48a4a4e3                         |
| SHA-256   | fca1c0c69d543f4be3501f04d3293beef5b5db9fbad24d55cfc70ea2cc8e2b4f |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 3ee09446776c3f65503fa7183e95ef8864b19946                         |
| SHA-256   | 2cb995d67f13b9d909609978f715c0649e717794ff231825089bfaf2ccd79516 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.14.2/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.14.2/bom.json)

<a href="cloudcannon:collections/_posts/2026-05-07-v4.14.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.14.1 <a href="#v4-14-1" class="anchor">#</a>

<span class="date">April 03, 2026</span> <span class="badge patch">patch</span>

**Features:**

- Add support for NuGet versioning scheme - [apiserver/#5958](https://github.com/DependencyTrack/dependency-track/pull/5958)
- Add support for Composer versioning scheme - [apiserver/#5963](https://github.com/DependencyTrack/dependency-track/pull/5963)
- Document age and version distance operational policy criteria - [apiserver/#5964](https://github.com/DependencyTrack/dependency-track/pull/5964)
- Use ecosystem-aware version comparison for latest version detection - [apiserver/#5995](https://github.com/DependencyTrack/dependency-track/pull/5995)
- Support Sonatype Guide tokens for OSS Index analyzer - [apiserver/#5996](https://github.com/DependencyTrack/dependency-track/pull/5996)
- Improve Chinese translations - [frontend/#1490](https://github.com/DependencyTrack/frontend/pull/1490)

**Fixes:**

- Fix PURL-specific version matching being bypassed for components with CPE - [apiserver/#5959](https://github.com/DependencyTrack/dependency-track/pull/5959)
- Fix wasteful existence queries - [apiserver/#5960](https://github.com/DependencyTrack/dependency-track/pull/5960)
- Fix potentially wrong version being used for CPE comparison - [apiserver/#5962](https://github.com/DependencyTrack/dependency-track/pull/5962)
- Fix scheduled notification query failing when ID columns are not of type BIGINT - [apiserver/#5979](https://github.com/DependencyTrack/dependency-track/pull/5979)
- Avoid NPE when computing Trivy pkgType - [apiserver/#5987](https://github.com/DependencyTrack/dependency-track/pull/5987)
- Remove leading whitespace from vulnerability badge SVG template - [apiserver/#6000](https://github.com/DependencyTrack/dependency-track/pull/6000)
- Fix Japanese Trivy analyzer strings - [frontend/#1489](https://github.com/DependencyTrack/frontend/pull/1489)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.14.1](https://github.com/DependencyTrack/dependency-track/milestone/50?closed=1)
- [Frontend milestone 4.14.1](https://github.com/DependencyTrack/frontend/milestone/35?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@Zureno](https://github.com/Zureno), [@jonbally](https://github.com/jonbally), [@retanoj](https://github.com/retanoj), [@shayFoo](https://github.com/shayFoo), [@stohrendorf](https://github.com/stohrendorf)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 750b0c768208d7c6b7e32e8f1a7500eb94788069                         |
| SHA-256   | 142bdfa36defffc2304d03f9ef7ecd162f1185dcbc00933a73529cac7f12980c |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 61eac5828458dfea46507c26f3384bb452ebeefe                         |
| SHA-256   | 6cedc727a3f8eb2343397e50a1b5515a99c2a361b7c55aa60dbeff85c1f4af2d |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | a08b4280aad4e9946908ca6fd05e1fbc0ad0f1af                         |
| SHA-256   | e13d9b729d2082fcfb440bc1deb6f373290d1ead414447d8834368b4dbceec27 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.14.1/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.14.1/bom.json)

<a href="cloudcannon:collections/_posts/2026-04-03-v4.14.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.14.0 <a href="#v4-14-0" class="anchor">#</a>

<span class="date">March 09, 2026</span> <span class="badge major">major</span>

**Highlights:**

- **Ecosystem-aware version matching**. Vulnerability analysis now uses version comparison algorithms native to the component’s ecosystem, rather than relying on generic semantic versioning. For example, Debian versions are compared using the [dpkg sorting algorithm](https://manpages.debian.org/stretch/dpkg-dev/deb-version.5.en.html#Sorting_algorithm). Supported ecosystems are Alpine Linux, Debian, Go, Maven, NPM, PyPI, and RPM.
- **Distro-aware vulnerability matching**. Linux distributions like Debian backport security fixes to older releases, meaning a component may be vulnerable in one distro release but not another. Dependency-Track now uses the `distro` qualifier of package URLs (e.g., `pkg:deb/debian/`<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="1b777279786e69772f6f2d2f5b23352a2f352a3629"><code class="language-plaintext highlighter-rouge">[email protected]</code></a>`%2Bdeb13u2?distro=debian-13.3`) to determine the OS release and match vulnerabilities accordingly. Currently supported for Alpine Linux, Debian, and Ubuntu.
  - **Note**: Requires vulnerability data from OSV, as the NVD does not contextualize version ranges by OS release. Not all BOM generators populate the `distro` PURL qualifier today.
- **CVSSv4 support**. Upstream vulnerability sources are increasingly publishing CVSSv4 scores. Dependency-Track now ingests and displays CVSSv4 vectors and derived severities alongside existing CVSSv2 and CVSSv3 data.

**Features:**

- Include project UUID in log messages - [apiserver/#5500](https://github.com/DependencyTrack/dependency-track/pull/5500)
- Add support for incremental mirroring of OSV - [apiserver/#5537](https://github.com/DependencyTrack/dependency-track/pull/5537)
- Add internal status policy condition support - [apiserver/#5570](https://github.com/DependencyTrack/dependency-track/pull/5570)
- Implement VERS approach for PURL version matching - [apiserver/#5591](https://github.com/DependencyTrack/dependency-track/pull/5591)
- Add projectUuid via MDC to logger statements within VEX upload - [apiserver/#5615](https://github.com/DependencyTrack/dependency-track/pull/5615)
- Specify newer version of Docker Compose in README - [apiserver/#5648](https://github.com/DependencyTrack/dependency-track/pull/5648)
- Add configurable base URL for OSS Index API - [apiserver/#5736](https://github.com/DependencyTrack/dependency-track/pull/5736)
- Update OSS Index documentation - [apiserver/#5774](https://github.com/DependencyTrack/dependency-track/pull/5774)
- Improve efficiency and caching behaviour of OSS Index analyzer - [apiserver/#5793](https://github.com/DependencyTrack/dependency-track/pull/5793)
- Switch to G1GC and limit default Docker Compose memory to 4GB - [apiserver/#5794](https://github.com/DependencyTrack/dependency-track/pull/5794)
- Add EPSS score support for GitHub Advisory vulnerabilities - [apiserver/#5829](https://github.com/DependencyTrack/dependency-track/pull/5829)
- Add page on users and permissions to documentation - [apiserver/#5831](https://github.com/DependencyTrack/dependency-track/pull/5831)
- Include CVSS vectors and metadata in Finding model - [apiserver/#5844](https://github.com/DependencyTrack/dependency-track/pull/5844)
- Tweak vulnerability persistence logic - [apiserver/#5862](https://github.com/DependencyTrack/dependency-track/pull/5862)
- Add CVSSv4 support - [apiserver/#5863](https://github.com/DependencyTrack/dependency-track/pull/5863)
- Delete NVD feed timestamp files during v4.14.0 upgrade - [apiserver/#5886](https://github.com/DependencyTrack/dependency-track/pull/5886)
- Bump SPDX license list to v3.28.0 - [apiserver/#5888](https://github.com/DependencyTrack/dependency-track/pull/5888)
- Bump CWE dictionary to v4.19.1 - [apiserver/#5889](https://github.com/DependencyTrack/dependency-track/pull/5889)
- Make username optional for Repositories Bearer Auth - [frontend/#1128](https://github.com/DependencyTrack/frontend/pull/1128)
- Improve German Translation - [frontend/#1227](https://github.com/DependencyTrack/frontend/pull/1227)
- Add suffix to vulnerability locale keys - [frontend/#1276](https://github.com/DependencyTrack/frontend/pull/1276)
- Add match mode selector to internal component config - [frontend/#1283](https://github.com/DependencyTrack/frontend/pull/1283)
- Display license ID - [frontend/#1311](https://github.com/DependencyTrack/frontend/pull/1311)
- Support for scope mentioned in CycloneDX format - [frontend/#1319](https://github.com/DependencyTrack/frontend/pull/1319)
- Add support for IS_INTERNAL policy condition - [frontend/#1394](https://github.com/DependencyTrack/frontend/pull/1394)
- Add Traditional Chinese (zh-TW) language support - [frontend/#1412](https://github.com/DependencyTrack/frontend/pull/1412)
- Remove database information from About dialogue - [frontend/#1421](https://github.com/DependencyTrack/frontend/pull/1421)
- Add OSS Index Base URL configuration field - [frontend/#1431](https://github.com/DependencyTrack/frontend/pull/1431)
- Add CVSSv4 support - [frontend/#1455](https://github.com/DependencyTrack/frontend/pull/1455)
- Add missing internal_status i18n key for zh-TW locale - [frontend/#1456](https://github.com/DependencyTrack/frontend/pull/1456)

**Fixes:**

- Fix sneaky double quote - [apiserver/#5420](https://github.com/DependencyTrack/dependency-track/pull/5420)
- Fix incorrect UTF-8 encoding in notification payload - [apiserver/#5574](https://github.com/DependencyTrack/dependency-track/pull/5574)
- Fix excessive memory usage of Nix analyzer - [apiserver/#5653](https://github.com/DependencyTrack/dependency-track/pull/5653)
- Fix wrong NPM component coordinate separator for Trivy analysis - [apiserver/#5679](https://github.com/DependencyTrack/dependency-track/pull/5679)
- Fix performance issue with PURL lookups - [apiserver/#5711](https://github.com/DependencyTrack/dependency-track/pull/5711)
- Fall back to generic versioning scheme if no PURL is available - [apiserver/#5714](https://github.com/DependencyTrack/dependency-track/pull/5714)
- Fix incorrect URL for VulnDB analyzer - [apiserver/#5751](https://github.com/DependencyTrack/dependency-track/pull/5751)
- Ensure container zombie processes are reaped - [apiserver/#5758](https://github.com/DependencyTrack/dependency-track/pull/5758)
- Fix singleton events not being labelled as such - [apiserver/#5775](https://github.com/DependencyTrack/dependency-track/pull/5775)
- Consider OS distro during vulnerability matching - [apiserver/#5783](https://github.com/DependencyTrack/dependency-track/pull/5783)
- Fix re-initialization of teams when opening create-modal - [frontend/#1410](https://github.com/DependencyTrack/frontend/pull/1410)

**Upgrade Notes:**

- To backfill CVSSv4 and EPSS data, mirror watermarks for NVD and GitHub Advisories will be reset,  
  triggering a full re-mirror on next invocation.

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.14.0](https://github.com/DependencyTrack/dependency-track/milestone/49?closed=1)
- [Frontend milestone 4.14.0](https://github.com/DependencyTrack/frontend/milestone/34?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@anantk24](https://github.com/anantk24), [@AndreVirtimo](https://github.com/AndreVirtimo), [@arjavdongaonkar](https://github.com/arjavdongaonkar), [@brianf](https://github.com/brianf), [@ch8matt](https://github.com/ch8matt), [@ElenaStroebele](https://github.com/ElenaStroebele), [@fupgang](https://github.com/fupgang), [@Granjow](https://github.com/Granjow), [@jonbally](https://github.com/jonbally), [@jvirgovic](https://github.com/jvirgovic), [@setchy](https://github.com/setchy), [@snieguu](https://github.com/snieguu), [@stohrendorf](https://github.com/stohrendorf), [@tobiasgies](https://github.com/tobiasgies), [@valentijnscholten](https://github.com/valentijnscholten), [@WoozyMasta](https://github.com/WoozyMasta), [@wengct](https://github.com/wengct)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | a06d7f57876befc80b6653fcc44b321958388f12                         |
| SHA-256   | 2e3d5bcfb7b5d4ad4daf789bc5ca3802ef05d012c516090e8bc5323f46585f53 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 6573a4522dd84520859ab951d86d8a9e4dd43fb2                         |
| SHA-256   | a8edd7c94ba811bae73d9213d769687c493e1bd95435dbe39dfeee28ff1f8008 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 8a822e22c6c087b0e46f9478f9b342d2e2bad162                         |
| SHA-256   | 9a96be982a80c6c8714ad8d22a932d013a6b3593744083d551a7fb2b4a281aa3 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.14.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.14.0/bom.json)

<a href="cloudcannon:collections/_posts/2026-03-09-v4.14.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.13.6 <a href="#v4-13-6" class="anchor">#</a>

<span class="date">November 17, 2025</span> <span class="badge patch">patch</span>

Starting with this release, we’re publishing a new container image variant for the *apiserver* and *bundled* distributions. The variant is based on [Alpine Linux](https://www.alpinelinux.org/) and uses [jlink](https://dev.java/learn/jlink/) to ship a minimal Java Runtime Environment (JRE). As a result, image size is decreased by over 55% (~350MB vs. ~150MB uncompressed), and attack surface is reduced due to fewer operating system packages. It uses Java 25 and enables [compact object headers](https://openjdk.org/jeps/519) by default, leading to lower memory footprint.

To use the new image variant, append the `-alpine` suffix to the image tag, e.g.:

- `docker.io/dependencytrack/apiserver:latest-alpine`
- `docker.io/dependencytrack/bundled:4.13.6-alpine`

The previous Debian-based image variant continues to be the default for now, but will eventually be discontinued in a future release. Users experiencing issues with `alpine` images can safely fall back to non-`alpine` variants.

**Features:**

- Add Alpine-based container variants - [apiserver/#5533](https://github.com/DependencyTrack/dependency-track/pull/5533)
- Update Ukrainian translation - [frontend/#1385](https://github.com/DependencyTrack/frontend/pull/1385)

**Fixes:**

- Improve performance of database migration to v4.13.5 - [apiserver/#5419](https://github.com/DependencyTrack/dependency-track/pull/5419)
- Ignore stale Lucene index entries - [apiserver/#5428](https://github.com/DependencyTrack/dependency-track/pull/5428)
- Fix typo in email notification template - [apiserver/#5434](https://github.com/DependencyTrack/dependency-track/pull/5434)
- Fix referential integrity violation during bulk project deletion - [apiserver/#5446](https://github.com/DependencyTrack/dependency-track/pull/5446)
- Fix referential integrity violation during team deletion - [apiserver/#5447](https://github.com/DependencyTrack/dependency-track/pull/5447)
- Fix NPE in Composer component metadata analyzer - [apiserver/#5519](https://github.com/DependencyTrack/dependency-track/pull/5519)
- Fix XML External Entity injection via validation of CycloneDX BOMs in XML format - [apiserver/#5528](https://github.com/DependencyTrack/dependency-track/pull/5528) / [GHSA-93r8-3g93-w2gq](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-93r8-3g93-w2gq)
- Fix OSS Index documentation link - [apiserver/#5531](https://github.com/DependencyTrack/dependency-track/pull/5531)
- Change `toString()` method of `Project` to use name and version instead of PURL - [apiserver/#5532](https://github.com/DependencyTrack/dependency-track/pull/5532)
- Fix broken routing when `BASE_PATH` is configured - [frontend/#1381](https://github.com/DependencyTrack/frontend/pull/1381)
- Fix policy tag selection dialogue using the wrong REST API endpoint - [frontend/#1382](https://github.com/DependencyTrack/frontend/pull/1382)
- Fix persistent Cross-Site-Scripting via welcome message - [frontend/#1383](https://github.com/DependencyTrack/frontend/pull/1383) / [GHSA-7xvh-c266-cfr5](https://github.com/DependencyTrack/frontend/security/advisories/GHSA-7xvh-c266-cfr5)
- Fix redirect loop when authenticated user is lacking permissions - [frontend/#1386](https://github.com/DependencyTrack/frontend/pull/1386)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.13.6](https://github.com/DependencyTrack/dependency-track/milestone/60?closed=1)
- [Frontend milestone 4.13.6](https://github.com/DependencyTrack/frontend/milestone/45?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@ElenaStroebele](https://github.com/ElenaStroebele), [@arjavdongaonkar](https://github.com/arjavdongaonkar), [@aurifi](https://github.com/aurifi), [@ch8matt](https://github.com/ch8matt), [@illenko](https://github.com/illenko), [@sahibamittal](https://github.com/sahibamittal), [@snieguu](https://github.com/snieguu), [@stohrendorf](https://github.com/stohrendorf)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                 |
|:----------|:-----------------------------------------|
| SHA-1     | 3964cf821761609912487077fa41d513dad37d1a |
| SHA-256   | 8f2aa10424403b2b201d0c48b243ea3bbe458761 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 1048a039391992fc36b23433d8987689baca33e68cc2130254787d1a3d1c66cc |
| SHA-256   | ab47deb0c5be2d947d57cf5862fef714023b4ce4d794ac00a855cf7590eb111e |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 525b47c72fb3bdbb675b5c5414319e5f19e43b03                         |
| SHA-256   | 84440921692e95c88378e1f82738ccea24c2fb038083b42b3f1c98b1f6702a4a |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.13.6/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.13.6/bom.json)

<a href="cloudcannon:collections/_posts/2025-11-17-v4.13.6.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.13.5 <a href="#v4-13-5" class="anchor">#</a>

<span class="date">October 07, 2025</span> <span class="badge patch">patch</span>

**Important Notice:**

Sonatype has started to enforce an authentication requirement for OSS Index.

The [OSS Index analyzer](/datasources/ossindex/) has historically been enabled by default for Dependency-Track, and configuration of credentials for authentication was not strictly necessary.

This has now changed, and users who wish to continue using OSS Index will need to register for a free account, and configure credentials in the analyzer’s settings.

Please refer to [Sonatype’s announcement](https://ossindex.sonatype.org/doc/auth-required) for further details.

In the midterm, we’ll be looking into enabling OSV per default to compensate for this change.

**Fixes:**

- Fix CPE matching not being fully case-insensitive - [apiserver/#5299](https://github.com/DependencyTrack/dependency-track/pull/5299)
- Improve detection whether version of a github PURL is a commit SHA or release tag - [apiserver/#5350](https://github.com/DependencyTrack/dependency-track/pull/5350)
- Make OSS Index credentials required - [apiserver/#5351](https://github.com/DependencyTrack/dependency-track/pull/5351)
- Fix occasional NullPointerException when mirroring the NVD via REST API - [apiserver/#5352](https://github.com/DependencyTrack/dependency-track/pull/5352)
- Fix `/api/v1/tag/policy/{uuid}` endpoint returning more tags than are assigned to a policy - [apiserver/#5353](https://github.com/DependencyTrack/dependency-track/pull/5353)
- Fix possible failure of NVD mirroring due to corrupted timestamp files - [apiserver/#5354](https://github.com/DependencyTrack/dependency-track/pull/5354)
- Fix BOM validation failing due to unrecognized new SPDX license IDs - [apiserver/#5355](https://github.com/DependencyTrack/dependency-track/pull/5355)
- Fix new SPDX license IDs not being recognized - [apiserver/#5356](https://github.com/DependencyTrack/dependency-track/pull/5356)
- Fix high CPU utilization when watchdog logger is configured - [apiserver/#5357](https://github.com/DependencyTrack/dependency-track/pull/5357)
- Fix NullPointerException in GithubMetaAnalyzer when analyzing GitHub Actions - [apiserver/#5359](https://github.com/DependencyTrack/dependency-track/pull/5359)
- Fix connection reset during OSV mirroring - [apiserver/#5360](https://github.com/DependencyTrack/dependency-track/pull/5360)
- Fix compatibility of custom NuGet repositories with JFrog Artifactory - [apiserver/#5381](https://github.com/DependencyTrack/dependency-track/pull/5381)
- Fix custom NuGet repositories not working with Sonatype Nexus - [apiserver/#5381](https://github.com/DependencyTrack/dependency-track/pull/5381)
- Fix possible disclosure of private NuGet repository credentials to api.nuget.org - [apiserver/#5381](https://github.com/DependencyTrack/dependency-track/pull/5381) / [GHSA-83g2-vgqh-mgxc](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-83g2-vgqh-mgxc)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.13.5](https://github.com/DependencyTrack/dependency-track/milestone/59?closed=1)
- [Frontend milestone 4.13.5](https://github.com/DependencyTrack/frontend/milestone/44?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@colinfyfe](https://github.com/colinfyfe), [@framayo](https://github.com/framayo), [@jonbally](https://github.com/jonbally), [@snieguu](https://github.com/snieguu), [@stohrendorf](https://github.com/stohrendorf)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | f38abe7b93f7cb88f3bba4c78c30a9ce7dc45c0d                         |
| SHA-256   | bf55097e63b46ed16042024636b855f676ba67e6e5824e7da80f3cec863a3f77 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 5aea8e0662f8aa4d9e53b52c14367c5345602e34                         |
| SHA-256   | 4a373de4d5aca924fb533ebfc7e1eb4fb5a249d81c948bd367a52fa53125a610 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | e441f28a656b710766a9fd85360872bc9330d14c                         |
| SHA-256   | fb67bf767e2142b72dbd226b984a1faee9e491d108ccfd29860a49e0b5b15a12 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.13.5/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.13.5/bom.json)

<a href="cloudcannon:collections/_posts/2025-10-07-v4.13.5.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.13.4 <a href="#v4-13-4" class="anchor">#</a>

<span class="date">August 26, 2025</span> <span class="badge patch">patch</span>

This release primarily addresses the [removal of NVD 1.1 data feeds](https://www.nist.gov/itl/nvd), which caused Dependency-Track’s NVD mirroring process to fail. With this release, Dependency-Track will consume the new 2.0 data feeds.

Users who cannot perform this upgrade immediately can configure NVD mirroring to be performed via the NVD REST API instead. Refer to the [NVD datasource documentation](/datasources/nvd/#mirroring-via-nvd-rest-api) for details.

**Features:**

- Migrate to NVD 2.0 data feeds - [apiserver/#5236](https://github.com/DependencyTrack/dependency-track/pull/5236)

**Fixes:**

- Handle URLs in composer package metadata pattern - [apiserver/#5234](https://github.com/DependencyTrack/dependency-track/pull/5234)
- Fix failing TrivyAnalysisTaskIntegrationTest - [apiserver/#5241](https://github.com/DependencyTrack/dependency-track/pull/5241)
- Handle `adduser` / `addgroup` removal in Debian base image - [apiserver/#5246](https://github.com/DependencyTrack/dependency-track/pull/5246)
- Fix inconsistent ordering in findings endpoints - [apiserver/#5247](https://github.com/DependencyTrack/dependency-track/pull/5247)
- Fix failing Trivy OS matching for distro versions with special characters - [apiserver/#5249](https://github.com/DependencyTrack/dependency-track/pull/5249)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.13.4](https://github.com/DependencyTrack/dependency-track/milestone/58?closed=1)
- [Frontend milestone 4.13.4](https://github.com/DependencyTrack/frontend/milestone/43?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 048b46829358cfde1f4d90b9298984224c75f6ae                         |
| SHA-256   | 2ca674108a08bf71642ddec6704125fae720161c4c40268fd19557e8b116d9d0 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | b3eb198254783462dc7d147791537fa50b11483e                         |
| SHA-256   | a8252f66f9b3c9253553e1d2a40fb0169f90c31895e36f57bc5992068ff473f5 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 827522ca8079450a8560a58a1b4e71add0a5d630                         |
| SHA-256   | d0e604300d52047c32a98a51aa32e1cf2276525fa81557c4c95f1ad49f30d820 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.13.4/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.13.4/bom.json)

<a href="cloudcannon:collections/_posts/2025-08-26-v4.13.4.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.13.3 <a href="#v4-13-3" class="anchor">#</a>

<span class="date">August 04, 2025</span> <span class="badge patch">patch</span>

**Features:**

- Add AWS Cognito configuration example - [apiserver/#5172](https://github.com/DependencyTrack/dependency-track/pull/5172)

**Fixes:**

- Fix too many query parameters when retrieving vuln aliases - [apiserver/#5167](https://github.com/DependencyTrack/dependency-track/pull/5167)
- Add apiserver health check to Compose files - [apiserver/#5171](https://github.com/DependencyTrack/dependency-track/pull/5171)
- Fix OSV ubuntu advisory containing severity without type - [apiserver/#5168](https://github.com/DependencyTrack/dependency-track/pull/5168)
- Handle dangling SPDX expression operators - [apiserver/#5173](https://github.com/DependencyTrack/dependency-track/pull/5173)
- Fix BOM export failing for projects of type NONE - [apiserver/#5178](https://github.com/DependencyTrack/dependency-track/pull/5178)
- Add whitespace sanitization in fuzzySearch CPE to fix CPE validation errors - [apiserver/#5176](https://github.com/DependencyTrack/dependency-track/pull/5176)
- Ensure VulnerableSoftware query is able to leverage indexes - [apiserver/#5177](https://github.com/DependencyTrack/dependency-track/pull/5177)
- Bulk load component relationships for BOM export - [apiserver/#5179](https://github.com/DependencyTrack/dependency-track/pull/5179)
- Improve Composer meta analyzer’s ability to deal with minified metadata - [apiserver/#5175](https://github.com/DependencyTrack/dependency-track/pull/5175)
- Fix failing v4.13.1 migration for H2 deployments that pre-date v4.11.0 - [apiserver/#5180](https://github.com/DependencyTrack/dependency-track/pull/5180)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.13.3](https://github.com/DependencyTrack/dependency-track/milestone/57?closed=1)
- [Frontend milestone 4.13.3](https://github.com/DependencyTrack/frontend/milestone/42?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@ch8matt](https://github.com/ch8matt), [@jonbally](https://github.com/jonbally), [@vdieieva](https://github.com/vdieieva)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | ba7866fa7b8be30f2058606ee77539b126ab61f1                         |
| SHA-256   | 8b6b2f29bdfd6f3e81ed2c9754a3ab2b4e27bbb9c33e52f720700d7e73558adb |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 70ac64f18c4b219d283df0c056e74f001287159b                         |
| SHA-256   | 1ae9984304854845cc5741d1dd1288e7b0a748539f448e0d0899ef635bb33c28 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 5eeea5e7bd1db7c40f45380580518eea7bdc53d7                         |
| SHA-256   | f5bdf91803fb99b966f38be60b937adec96036b80bf7a793d32bb51b67f6fd7b |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.13.3/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.13.3/bom.json)

<a href="cloudcannon:collections/_posts/2025-08-04-v4.13.3.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.13.2 <a href="#v4-13-2" class="anchor">#</a>

<span class="date">May 09, 2025</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix failing v4.13.1 migration for MSSQL deployments that pre-date v4.11.0 - [apiserver/#4911](https://github.com/DependencyTrack/dependency-track/pull/4911)
- Fix summary notifications not sent when “skip if unchanged” is enabled - [apiserver/#4913](https://github.com/DependencyTrack/dependency-track/pull/4913)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.13.2](https://github.com/DependencyTrack/dependency-track/milestone/56?closed=1)
- [Frontend milestone 4.13.2](https://github.com/DependencyTrack/frontend/milestone/41?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 845f970ba9c00a26d6d0b5a77c24cd12ee5feeea                         |
| SHA-256   | f1d66b81a44d7d3528fad42d1e1fb498e2151c2c5e78c1070942be54456bf7d1 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 61d5c535ab19a6f67e48ee8efa20bf9656d084f7                         |
| SHA-256   | 4494b0090cd699db2099248c0fdd67a07d130731bbc476287251aa84d008bfa4 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 987a3b3a37fad4143b295ff9a7fcbacef7e915f4                         |
| SHA-256   | 94fc935e62a657e5f10bff9b9a8657841f0c2f2e53fd234c881580874bb95f14 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.13.2/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.13.2/bom.json)

<a href="cloudcannon:collections/_posts/2025-05-09-v4.13.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.13.1 <a href="#v4-13-1" class="anchor">#</a>

<span class="date">April 30, 2025</span> <span class="badge patch">patch</span>

**Features:**

- Show collection projects using a tag in the tags list - [frontend/#1241](https://github.com/DependencyTrack/frontend/pull/1241)

**Fixes:**

- Fix `NEW_VULNERABILITIES_SUMMARY` notification dispatch failing for PostgreSQL - [apiserver/#4859](https://github.com/DependencyTrack/dependency-track/pull/4859)
- Fix team email addresses not being available when publishing scheduled notification emails - [apiserver/#4860](https://github.com/DependencyTrack/dependency-track/pull/4860)
- Prevent duplicate tag names and relationships - [apiserver/#4861](https://github.com/DependencyTrack/dependency-track/pull/4861)
- Fix missing `NONE` value in classifier check constraint - [apiserver/#4887](https://github.com/DependencyTrack/dependency-track/pull/4887)
- Improve stability of tag binding - [apiserver/#4885](https://github.com/DependencyTrack/dependency-track/pull/4885)
- Fix tag deletion failing when tag is used by project collection logic - [apiserver/#4888](https://github.com/DependencyTrack/dependency-track/pull/4888)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.13.1](https://github.com/DependencyTrack/dependency-track/milestone/55?closed=1)
- [Frontend milestone 4.13.1](https://github.com/DependencyTrack/frontend/milestone/40?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | b5e613f1f484179e770333828ef25c020ed9f03a                         |
| SHA-256   | c88b2e7879b1d534741ce5483f96621b650d6a4dcacabb470eeeeb43e7c7c627 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 173511869286b1335950bd07477421d684c96251                         |
| SHA-256   | 53c7fca478125fad1c35d6732815a6c09e120abc6ea57a8a88eb2af3ed2efab2 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | ad0926abed617069934cf198670d7dba4e3f6867                         |
| SHA-256   | 0ae8950c4aa0713dc52812225720cb27cf2da17d32badcda9c2be8c3872720e6 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.13.1/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.13.1/bom.json)

<a href="cloudcannon:collections/_posts/2025-04-30-v4.13.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.13.0 <a href="#v4-13-0" class="anchor">#</a>

<span class="date">April 07, 2025</span> <span class="badge major">major</span>

**Highlights:**

- **API Key Overhaul**. API keys are no longer stored as plain text values in the database, but as SHA3-256 hashes. It will no longer be possible to view the full, plain text API keys in the administration panel. Instead, full keys will only be shown *once* after their creation. To allow keys to be identifiable despite this change, the API key format was adjusted to include a *public identifier* portion. Keys generated by version 4.13.0 and later will follow the format `odt_<publicId>_<key>`, where `publicId` consists of 8 random characters, and `key` of the usual 32 random characters. The public ID is intended to identify API keys without disclosing their secret. It will be visible in the UI, and it will also appear in logs.
  - Keys generated by earlier versions of Dependency-Track will continue to work, in their case the first 5 characters are assumed to be the public ID.
  - *This feature was discussed and demoed in our February community meeting! Watch it [here](https://www.youtube.com/watch?v=UphB2IDv1Rk&t=280s)*
- **Collection Projects**. Dependency-Track has had support for project hierarchies for a while, but until now their utility was still somewhat limited. Collection projects change this, as they allow parent projects to act as aggregates of their children. While they are a major improvement to the project hierarchy mechanism, there is still more work to be done. And the team is always looking for feedback on how to make it better.
  - *This feature was discussed and demoed in our January community meeting! Watch it [here](https://www.youtube.com/watch?v=DSyf-g2FF_w&t=745s)*
- **Scheduled Summary Notifications**. Instead of publishing notifications immediately when a new vulnerability or policy violation is identified, it is now possible to configure scheduled summary notifications. This aids in reducing alert fatigue. Refer to the [notifications documentation](/integrations/notifications/#configuring-scheduled-notifications) for more details.
- **Reduced Memory Footprint**. The persistence framework used by Dependency-Track to interact with the database comes with overambitious caching enabled per default. Disabling this cache mechanism has been a recommendation the team gave to users struggling with memory requirements for a while. After evaluating whether it provides any justifiable benefit at all, it was decided to turn this feature off entirely. Users with large portfolios should see a noticeable drop in heap utilization and pressure on the garbage collector.
- **Observability Improvements**. Logs emitted while handling REST API requests now include context about the authenticated user, the path of the endpoint being called, as well as the request method. This makes it easier to trace *where* problems are occurring, and *who* initiated the requests that cause them.

**Features:**

- Introduce collection projects for better utilization of project hierarchies - [apiserver/#3258](https://github.com/DependencyTrack/dependency-track/pull/3258)
- Add property to control `verified` flag in DefectDojo integration - [apiserver/#4273](https://github.com/DependencyTrack/dependency-track/pull/4273)
- Disable DataNucleus L2 cache globally - [apiserver/#4310](https://github.com/DependencyTrack/dependency-track/pull/4310)
- Optimize vulnerability synchronization logic to not perform redundant writes - [apiserver/#4359](https://github.com/DependencyTrack/dependency-track/pull/4359)
- Add REST API endpoint for batch deletion of projects - [apiserver/#4383](https://github.com/DependencyTrack/dependency-track/pull/4383)
- Update link to Azure DevOps Extension in docs - [apiserver/#4423](https://github.com/DependencyTrack/dependency-track/pull/4423)
- Reduce database round-trips during BOM processing - [apiserver/#4486](https://github.com/DependencyTrack/dependency-track/pull/4486)
- Postpone deprecation of unauthenticated access to Badge API - [apiserver/#4502](https://github.com/DependencyTrack/dependency-track/pull/4502)
- Clarify descriptions of component analysis cache properties - [apiserver/#4504](https://github.com/DependencyTrack/dependency-track/pull/4504)
- Add debug logging for Composer meta analyzer - [apiserver/#4546](https://github.com/DependencyTrack/dependency-track/pull/4546)
- Clarify OpenAPI endpoint location in the docs - [apiserver/#4556](https://github.com/DependencyTrack/dependency-track/pull/4556)
- Migrate API keys to new format - [apiserver/#4566](https://github.com/DependencyTrack/dependency-track/pull/4566), [apiserver/#4682](https://github.com/DependencyTrack/dependency-track/pull/4682)
- Update quickstart Compose file to use Postgres instead of H2 - [apiserver/#4576](https://github.com/DependencyTrack/dependency-track/pull/4576)
- Add SecObserve to community integrations - [apiserver/#4580](https://github.com/DependencyTrack/dependency-track/pull/4580)
- Track “last vulnerability analysis” timestamp for projects - [apiserver/#4642](https://github.com/DependencyTrack/dependency-track/pull/4642)
- Implement basic telemetry collection - [apiserver/#4651](https://github.com/DependencyTrack/dependency-track/pull/4651)
- Prevent application startup when migrations fail - [apiserver/#4681](https://github.com/DependencyTrack/dependency-track/pull/4681)
- Add support for Snyk API version 2024-10-15 - [apiserver/#4715](https://github.com/DependencyTrack/dependency-track/pull/4715)
- Add REST API endpoint for bulk creation of tags - [apiserver/#4766](https://github.com/DependencyTrack/dependency-track/pull/4766)
- Update Azure AD configuration docs to Entra ID - [apiserver/#4778](https://github.com/DependencyTrack/dependency-track/pull/4778)
- Make it configurable whether Trivy should scan only OS packages, only libraries, or both - [apiserver/#4782](https://github.com/DependencyTrack/dependency-track/pull/4782)
- Add support for scheduled summary notifications - [apiserver/#4783](https://github.com/DependencyTrack/dependency-track/pull/4783)
- Add ability to configure the DefectDojo test title - [apiserver/#4796](https://github.com/DependencyTrack/dependency-track/pull/4796)
- Bump SPDX license list to v3.26.0 - [apiserver/#4800](https://github.com/DependencyTrack/dependency-track/pull/4800)
- Bump CWE dictionary to v4.16 - [apiserver/#4801](https://github.com/DependencyTrack/dependency-track/pull/4801)
- Add new optional column *Classifier* in project component view - [frontend/#1058](https://github.com/DependencyTrack/frontend/pull/1058)
- Remove deprecation notice of toggle for unauthenticated access to SVG badges - [frontend/#1129](https://github.com/DependencyTrack/frontend/pull/1129)
- Add timestamp formatting to chart tooltips - [frontend/#1152](https://github.com/DependencyTrack/frontend/pull/1152)
- Handle new API key format and generation process - [frontend/#1157](https://github.com/DependencyTrack/frontend/pull/1157)
- Add telemetry admin view - [frontend/#1164](https://github.com/DependencyTrack/frontend/pull/1164)
- Add autocomplete to project collection logic tag dropdown - [frontend/#1198](https://github.com/DependencyTrack/frontend/pull/1198)

**Fixes:**

- Fix failure to synchronize vulnerability aliases when the source of a vulnerability is unrecognized - [apiserver/#4767](https://github.com/DependencyTrack/dependency-track/pull/4767)
- Fix possible NPE during affected version attribution sync - [apiserver/#4798](https://github.com/DependencyTrack/dependency-track/pull/4798)
- Fix occasional JsonParseException during NVD API mirroring - [apiserver/#4814](https://github.com/DependencyTrack/dependency-track/pull/4814)
- Fix UpgradeInitializer halting the entire process upon failure - [apiserver/#4818](https://github.com/DependencyTrack/dependency-track/pull/4818)
- Fix column visibility preference not considered for project list - [frontend/#1169](https://github.com/DependencyTrack/frontend/pull/1169)
- Fix tag autocomplete dropdown library style overriding issue - [frontend/#1213](https://github.com/DependencyTrack/frontend/pull/1213)

**Upgrade Notes:**

**Please make a database backup before upgrading!** Some changes in this release are **irreversible**,  
and you won’t be able to roll back simply by downgrading the application version!

- Existing API keys will be automatically hashed during this upgrade. It will not be possible to view them in plain text ever again after the upgrade completed. Outside of making a database backup, consider noting down all the keys you might need somewhere safe before performing this upgrade.
- Dependency-Track instances will automatically share minimal telemetry information on a daily basis. Find a list of collected data, as well as instructions for opting out, in the [telemetry documentation](/getting-started/telemetry/).

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.13.0](https://github.com/DependencyTrack/dependency-track/milestone/38?closed=1)
- [Frontend milestone 4.13.0](https://github.com/DependencyTrack/frontend/milestone/23?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@2000rosser](https://github.com/2000rosser), [@AndreVirtimo](https://github.com/AndreVirtimo), [@Gepardgame](https://github.com/Gepardgame), [@Granjow](https://github.com/Granjow), [@LaVibeX](https://github.com/LaVibeX), [@MM-msr](https://github.com/MM-msr), [@Malaydewangan09](https://github.com/Malaydewangan09), [@Rudra-Garg](https://github.com/Rudra-Garg), [@SaberStrat](https://github.com/SaberStrat), [@StefanFl](https://github.com/StefanFl), [@VinodAnandan](https://github.com/VinodAnandan), [@Zargath](https://github.com/Zargath), [@ad8-adriant](https://github.com/ad8-adriant), [@dhfherna](https://github.com/dhfherna), [@jayolee](https://github.com/jayolee), [@mge-mm](https://github.com/mge-mm), [@mikael-carneholm-2-wcar](https://github.com/mikael-carneholm-2-wcar), [@mjwrona](https://github.com/mjwrona), [@rbt-mm](https://github.com/rbt-mm), [@rkg-mm](https://github.com/rkg-mm), [@stohrendorf](https://github.com/stohrendorf), [@valentijnscholten](https://github.com/valentijnscholten)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | c5ef70f1e8df186a929a7c2ad24962a3b97af379                         |
| SHA-256   | 0f2af7a93a21850da62c2b2e86babfb0b0f18abd80f380dfb80bf84c59f605e4 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | feeac3362ae6ea5d42cf6dde7e5e079599372eaa                         |
| SHA-256   | a81e61f1e21a732474a11345d71e7853d50ec2faea1f7d44bacfb29902673ebd |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 5f18d23205cff4627ff6330bca9f70f71810da89                         |
| SHA-256   | e64676821351096cce62735d28a15b2ae62c4ba66c1b295ab119a9b83f94eef0 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.13.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.13.0/bom.json)

<a href="cloudcannon:collections/_posts/2025-04-07-v4.13.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.12.7 <a href="#v4-12-7" class="anchor">#</a>

<span class="date">March 12, 2025</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix NPE during NVD mirroring via REST API when encountering invalid CPEs - [apiserver/#4734](https://github.com/DependencyTrack/dependency-track/pull/4734)
- Remove erroneous client-side caching in Trivy analyzer - [apiserver/#4736](https://github.com/DependencyTrack/dependency-track/pull/4736)
- Fix notification limiting to tags not working reliably - [apiserver/#4737](https://github.com/DependencyTrack/dependency-track/pull/4737)
- Fix tags from BOM upload request not being applied for existing projects - [apiserver/#4740](https://github.com/DependencyTrack/dependency-track/pull/4740)
- Fix component properties not being cloned - [apiserver/#4746](https://github.com/DependencyTrack/dependency-track/pull/4746)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.12.7](https://github.com/DependencyTrack/dependency-track/milestone/54?closed=1)
- [Frontend milestone 4.12.7](https://github.com/DependencyTrack/frontend/milestone/39?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | a3a30181b15a14bcd3ea3ef7ed338d2ce5e86bb5                         |
| SHA-256   | cc271be5577eee0a562c19acd60a693accbe6b8b1a24294472a43462f6aa94fd |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 2c416320eda0aee60a268047643da006ad7edf24                         |
| SHA-256   | 48defc20ebe19214bb7cf73bf61f8c09f467d0c8585a5e6c0671ad563bbd4884 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 4d42a3251d35746bb198018fec273b17a91761e6                         |
| SHA-256   | 8c808d7d4ec2442970e8a79f8bb67b9422a69e377a682a4fe47057e7b0cad642 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.12.7/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.12.7/bom.json)

<a href="cloudcannon:collections/_posts/2025-03-12-v4.12.7.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.12.6 <a href="#v4-12-6" class="anchor">#</a>

<span class="date">February 24, 2025</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix possible NPEs in `TrivyAnalysisTask` - [apiserver/#4671](https://github.com/DependencyTrack/dependency-track/pull/4671)
- Analyze all components of a project at once instead of in batches - [apiserver/#4673](https://github.com/DependencyTrack/dependency-track/pull/4673)
- Fix notification webhook sending blank header - [apiserver/#4680](https://github.com/DependencyTrack/dependency-track/pull/4680)
- Fix local file inclusion via notification templates - [apiserver/#4685](https://github.com/DependencyTrack/dependency-track/pull/4685) / [GHSA-9582-88hr-54w3](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-9582-88hr-54w3)
- Fix policy violation tab indicators being populated incorrectly - [frontend/#1172](https://github.com/DependencyTrack/frontend/pull/1172)
- Fix wrong policy violation tab indicator visibility conditions - [frontend/#1175](https://github.com/DependencyTrack/frontend/pull/1175)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.12.6](https://github.com/DependencyTrack/dependency-track/milestone/53?closed=1)
- [Frontend milestone 4.12.6](https://github.com/DependencyTrack/frontend/milestone/38?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@LennartC](https://github.com/LennartC)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | f59a0777e631a6bd4e4dc7b42c3df2ac9e8ce4d8                         |
| SHA-256   | 4196b1eb91cb27304a53a0b897f0ffb766e3f49607094880618b480ce9ee3124 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | be4ed743244851cd47873cbbb6c065f0c2eace9d                         |
| SHA-256   | e036fc1bd0d0914f421307a59911cb7cab1ba158599b125e404a4a3079e6ea26 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 118b6fe222bb7192ca15610dd9c0481f055f93b4                         |
| SHA-256   | d3cb53bccb46f20f735ac8716e147d6e99bf7a028ecb492b63aa3718167595ff |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.12.6/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.12.6/bom.json)

<a href="cloudcannon:collections/_posts/2025-02-24-v4.12.6.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.12.5 <a href="#v4-12-5" class="anchor">#</a>

<span class="date">February 17, 2025</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix failure to mirror NVD via REST API due to broken CVSSv4 metric deserialization - [apiserver/#4656](https://github.com/DependencyTrack/dependency-track/pull/4656)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.12.5](https://github.com/DependencyTrack/dependency-track/milestone/52?closed=1)
- [Frontend milestone 4.12.5](https://github.com/DependencyTrack/dependency-track/milestone/37?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | d5c8c84612e6f09dcbefe596545c11384615f14c                         |
| SHA-256   | b0e9a93c06fb92d2c4bba2724689d58cc8455ac92c42cb5cf844686fad2d2820 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | c4c020b2652413f99daf41965231a8c17f90e2a8                         |
| SHA-256   | ba569456a971f772d4d8a70fddc6fea2c9d4fbc6b12dfc7458d102dc97ed0206 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 4be2ae18d5a09116272cf608cf32b9d0cf3550b5                         |
| SHA-256   | 5ddcca1d95fb7fc39110c866ad943353f6515538b3a6408478df8805823e45fa |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.12.5/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.12.5/bom.json)

<a href="cloudcannon:collections/_posts/2025-02-17-v4.12.5.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.12.4 <a href="#v4-12-4" class="anchor">#</a>

<span class="date">February 10, 2025</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix possible NPEs during tag binding - [apiserver/#4595](https://github.com/DependencyTrack/dependency-track/pull/4595)
- Fix false negatives in CPE matching for ANY and NA versions - [apiserver/#4612](https://github.com/DependencyTrack/dependency-track/pull/4612)
- Refactor `VulnerabilityAnalysisTask` to be more efficient - [apiserver/#4625](https://github.com/DependencyTrack/dependency-track/pull/4625)
- Refactor `VulnerabilityManagementUploadTask` to be more efficient - [apiserver/#4626](https://github.com/DependencyTrack/dependency-track/pull/4626)
- Bump Temurin base image to `21.0.6_7` - [apiserver/#4628](https://github.com/DependencyTrack/dependency-track/pull/4628)
- Fix erroneous URL-encoding of the Maven groupId - [apiserver/#4629](https://github.com/DependencyTrack/dependency-track/pull/4629)
- Handle invalid CVSS vectors and processing failures for OSV - [apiserver/#4638](https://github.com/DependencyTrack/dependency-track/pull/4638)
- Fix broken ordering by SWID Tag ID in component search view - [frontend/#1155](https://github.com/DependencyTrack/frontend/pull/1155)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.12.4](https://github.com/DependencyTrack/dependency-track/milestone/48?closed=1)
- [Frontend milestone 4.12.4](https://github.com/DependencyTrack/frontend/milestone/33?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 6467242cb3ce65fb128ded6e4d40bd45bf3c74f3                         |
| SHA-256   | 9abd2ec5091645779d1eecbcad0ed78c4175565fe93eddce8b600113fe66f476 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | a27297edf0da4d208c3b89d31fcd441958767e48                         |
| SHA-256   | fe490211de5988fb651a8e869e36d46c33caca030b26a61172e9fc49b0d94404 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 182da8ebc1cde3a5ca89db6649afdd19be4f63a4                         |
| SHA-256   | bf2cb6079d36b113645f4c9dd31441bbcdd188b7a003f05947569007ff9d4713 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.12.4/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.12.4/bom.json)

<a href="cloudcannon:collections/_posts/2025-02-10-v4.12.4.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.12.3 <a href="#v4-12-3" class="anchor">#</a>

<span class="date">January 27, 2025</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix broken pagination in `/api/v1/cwe` endpoint - [apiserver/#4459](https://github.com/DependencyTrack/dependency-track/pull/4459)
- Fix notification tests not working for Jira - [apiserver/#4460](https://github.com/DependencyTrack/dependency-track/pull/4460)
- Fix component de-duplication potentially causing duplicate dependency graph entries - [apiserver/#4461](https://github.com/DependencyTrack/dependency-track/pull/4461)
- Fix component SWID tag ID not being considered in project cloning - [apiserver/#4481](https://github.com/DependencyTrack/dependency-track/pull/4481)
- Fix `onlyOutdated` ungrouped component filtering - [apiserver/#4513](https://github.com/DependencyTrack/dependency-track/pull/4513)
- Fix REST endpoints for adding tags - [apiserver/#4543](https://github.com/DependencyTrack/dependency-track/pull/4543)
- Recreate outdated check constraints for `CLASSIFIER` columns - [apiserver/#4545](https://github.com/DependencyTrack/dependency-track/pull/4545)
- Handle GitHub GraphQL API rate limiting - [apiserver/#4581](https://github.com/DependencyTrack/dependency-track/pull/4581)
- Fix affected projects tab not being updated when switching between vulnerability aliases - [frontend/#509](https://github.com/DependencyTrack/frontend/pull/509)
- Prefill *Team* input in *Create Project* dialog based on user’s team membership - [frontend/#1110](https://github.com/DependencyTrack/frontend/pull/1110)
- Add buttons to add/delete/edit *Affected Components* of internal vulnerabilities - [frontend/#1113](https://github.com/DependencyTrack/frontend/pull/1113)
- Bump dompurify to 2.5.8 - [frontend/#1144](https://github.com/DependencyTrack/frontend/pull/1144)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.12.3](https://github.com/DependencyTrack/dependency-track/milestone/47?closed=1)
- [Frontend milestone 4.12.3](https://github.com/DependencyTrack/frontend/milestone/32?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@Gepardgame](https://github.com/Gepardgame), [@sedan07](https://github.com/sedan07), [@sephiroth-j](https://github.com/sephiroth-j)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 3d315e8d6637a69a5db4f3f545391bb007ee6ae8                         |
| SHA-256   | 41d925a83b6720824ccd7b0ec5e04c8d52a21fe138418256abef191ac6f99dbc |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 1ed5ad7b1afa61fbefbe30cc4d1587d5ae255966                         |
| SHA-256   | 1348c4fd3ed6ba73bd808c27ae0f64da0137fb2edeeb494f93852e75d53d821a |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 40e7690e3194ebf7d047a0058fa6f1d7166505ee                         |
| SHA-256   | 40e0d81013f2713c66a7aee661881cac896091a58520c7a020f0515e9c347694 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.12.3/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.12.3/bom.json)

<a href="cloudcannon:collections/_posts/2025-01-27-v4.12.3.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.12.2 <a href="#v4-12-2" class="anchor">#</a>

<span class="date">December 04, 2024</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix possible enumeration of managed users via `/api/v1/user/login` endpoint - [GHSA-9w3m-hm36-w32w](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-9w3m-hm36-w32w)
- Reduce memory usage of metrics update tasks - [apiserver/#4377](https://github.com/DependencyTrack/dependency-track/pull/4377)
- Fix CPE matching for NVD mirroring via REST API - [apiserver/#4378](https://github.com/DependencyTrack/dependency-track/pull/4378)
- Fix incorrect CWE schema in OpenAPI spec - [apiserver/#4379](https://github.com/DependencyTrack/dependency-track/pull/4379)
- Fix NullPointerException when fetching findings - [apiserver/#4380](https://github.com/DependencyTrack/dependency-track/pull/4380)
- Fix policy evaluation not happening upon creation of update of individual components - [apiserver/#4381](https://github.com/DependencyTrack/dependency-track/pull/4381)
- Fix nullable metrics fields having getters of primitive type - [apiserver/#4382](https://github.com/DependencyTrack/dependency-track/pull/4382)
- Fix Trivy analyzer vulnerability matching for Go packages - [apiserver/#4395](https://github.com/DependencyTrack/dependency-track/pull/4395)
- Fix too frequent notifications during GHSA mirroring - [apiserver/#4417](https://github.com/DependencyTrack/dependency-track/pull/4417)
- Fix `project.active` field being nullable - [apiserver/#4418](https://github.com/DependencyTrack/dependency-track/pull/4418)
- Fix NullPointerException when cloning projects with broken dependency graph - [apiserver/#4419](https://github.com/DependencyTrack/dependency-track/pull/4419)
- Fix missing CycloneDX JSON content type for `/api/v1/bom/cyclonedx/component/{uuid}` endpoint - [apiserver/#4420](https://github.com/DependencyTrack/dependency-track/pull/4420)
- Fix no error being displayed when submitting and invalid welcome message - [frontend/#1099](https://github.com/DependencyTrack/frontend/pull/1099)
- Fix tags with special characters breaking the tags table - [frontend/#1100](https://github.com/DependencyTrack/frontend/pull/1100)
- Fix broken NGINX IPv6 listening - [frontend/#1101](https://github.com/DependencyTrack/frontend/pull/1101)
- Fix viewing of component properties requiring the `PORTFOLIO_MANAGEMENT` permission - [frontend/#1102](https://github.com/DependencyTrack/frontend/pull/1102)
- Fix missing URI encoding for vulnerability IDs - [frontend/#1103](https://github.com/DependencyTrack/frontend/pull/1103)
- Improve Russian translation - [frontend/#1109](https://github.com/DependencyTrack/frontend/pull/1109)

**Upgrade Notes:**

- `ACTIVE` columns in the `PROJECT` table that previously had `NULL` values will be updated to `TRUE` automatically upon upgrade. The column is further assigned a default value of `TRUE`. No manual action is required. The SQL statements executed by Dependency-Track can be found [here](https://github.com/DependencyTrack/dependency-track/blob/92f0d605ce4fdff4a20ff408c748dd1023786fb4/src/main/java/org/dependencytrack/upgrade/v4122/v4122Updater.java#L45-L82).

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.12.1](https://github.com/DependencyTrack/dependency-track/milestone/46?closed=1)
- [Frontend milestone 4.12.1](https://github.com/DependencyTrack/frontend/milestone/31?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@Gepardgame](https://github.com/Gepardgame), [@Shortfinga](https://github.com/Shortfinga), [@WoozyMasta](https://github.com/WoozyMasta), [@antoinbo](https://github.com/antoinbo), [@calderonth](https://github.com/calderonth), [@fupgang](https://github.com/fupgang), [@rissson](https://github.com/rissson), [@wratner](https://github.com/wratner)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 114d6a9f8b87a307be324f155daf3454dcc269bb                         |
| SHA-256   | ef6bb4ce3ebea410b620a91cf8347ab1e95c32b3f166103c749ece97f4098591 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | a15db1b85d0ac29977724deb3f9a65428c929d39                         |
| SHA-256   | a8aba7cd926de3deeea31290be830ee90282128f1820fddde3ec8b346bba1bdd |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | b1e520a4aa0d3a3dc65aa5ab7da93b81c84edf43                         |
| SHA-256   | 0a8790def4abe6ab3c5294928cc816a266c2b746ec39b0c1f140b8a2f4c0ad74 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.12.2/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.12.2/bom.json)

<a href="cloudcannon:collections/_posts/2024-12-04-v4.12.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.12.1 <a href="#v4-12-1" class="anchor">#</a>

<span class="date">October 25, 2024</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix logs not containing usernames of deleted users - [apiserver/#4232](https://github.com/DependencyTrack/dependency-track/pull/4232)
- Fix unintended manual flushing mode due to DataNucleus ExecutionContext pooling - [apiserver/#4233](https://github.com/DependencyTrack/dependency-track/pull/4233)
- Prevent duplicate policy violations - [apiserver/#4234](https://github.com/DependencyTrack/dependency-track/pull/4234)
- Enhance policy violation de-duplication logic - [apiserver/#4235](https://github.com/DependencyTrack/dependency-track/pull/4235)
- Fix inaccuracies of Trivy analyzer - [apiserver/#4258](https://github.com/DependencyTrack/dependency-track/pull/4258)
- Fix redundant query for “ignore unfixed” config during Trivy analysis - [apiserver/#4259](https://github.com/DependencyTrack/dependency-track/pull/4259)
- Fix CycloneDX deserialization failure for `OrganizationalContact` without `name` - [apiserver/#4271](https://github.com/DependencyTrack/dependency-track/pull/4271)
- Update *Deploying Docker* guide to Compose v2 - [apiserver/#4301](https://github.com/DependencyTrack/dependency-track/pull/4301)
- Fix `ERROR 400 Ambiguous URI path separator` for path parameters with encoded slashes - [apiserver/#4309](https://github.com/DependencyTrack/dependency-track/pull/4309)
- Fix excessive memory usage of portfolio repository meta analysis - [apiserver/#4317](https://github.com/DependencyTrack/dependency-track/pull/4317)
- Add `.gitattributes` to fix prettier behavior on Windows - [frontend/#1043](https://github.com/DependencyTrack/frontend/pull/1043)
- Fix state of sidebar not being saved for non-SNAPSHOT versions - [frontend/#1044](https://github.com/DependencyTrack/frontend/pull/1044)
- Fix OIDC users not being displayed in *Teams* view - [frontend/#1045](https://github.com/DependencyTrack/frontend/pull/1045)
- Fix creation of multiple projects not working without page reload - [frontend/#1046](https://github.com/DependencyTrack/frontend/pull/1046)
- Always display project nodes in dependency graph using name and version - [frontend/#1049](https://github.com/DependencyTrack/frontend/pull/1049)
- Fix caching issues upon upgrade - [frontend/#1051](https://github.com/DependencyTrack/frontend/pull/1051)
- Fix *Add Version* button being clickable without a version name being set - [frontend/#1052](https://github.com/DependencyTrack/frontend/pull/1052)
- Fix missing URI encoding of tag names - [frontend/#1057](https://github.com/DependencyTrack/frontend/pull/1057)
- Fix broken breadcrumb navigation for non-English languages - [frontend/#1068](https://github.com/DependencyTrack/frontend/pull/1068)
- Fix broken NGINX IPv6 listening - [frontend/#1069](https://github.com/DependencyTrack/frontend/pull/1069)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.12.1](https://github.com/DependencyTrack/dependency-track/milestone/45?closed=1)
- [Frontend milestone 4.12.1](https://github.com/DependencyTrack/frontend/milestone/21?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects: [@Gepardgame](https://github.com/Gepardgame), [@IdrisGit](https://github.com/IdrisGit), [@danihengeveld](https://github.com/danihengeveld), [@rissson](https://github.com/rissson), [@rkg-mm](https://github.com/rkg-mm)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 18911ef4fa28531d97293bd70de2ebb4033e5b5c                         |
| SHA-256   | 682a3ffe268c59b0df03a55fd72b56d46299db3fd2cfe081966d8d57fbbea4f6 |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | b3f3eb8cb5c8021ba7bdb37a5717cd2672550385                         |
| SHA-256   | dc1a3e65e8ce767e39925bf329be8eff29ff09eebc627db8efd0e1b5ff6db573 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 23c991a3540da5fc3c08fbcebc3c1b7bd3801402                         |
| SHA-256   | 22f1a73db7df0340bb6d75042bfeb73ed375fc5659b4d609844763111bea4c81 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.12.1/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.12.1/bom.json)

<a href="cloudcannon:collections/_posts/2024-10-25-v4.12.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.12.0 <a href="#v4-12-0" class="anchor">#</a>

<span class="date">October 01, 2024</span> <span class="badge major">major</span>

**Highlights:**

- **Tags, Tags, Tags**. This release contains a breadth of tag-related features:
  - Alerts can be limited to projects with specific tags
  - Projects can be included or excluded from BOM validation using tags
  - Projects can be tagged as part of a BOM upload request
  - Tag input fields of the frontend now offer auto-complete
- **Tag Management**. It is now possible to view and manage tags in the system through the new *tag management* view, and associated REST API endpoints. This makes it possible to see how many, and which projects, policies, and alerts are associated with a given tag. Projects, policies, and alerts can be un-tagged, and tags can be deleted altogether.
  - *This feature was discussed and demoed in our July community meeting! Watch it [here](https://www.youtube.com/watch?v=rvigQKVvoN8&t=543s)*
- **Global Policy Violation Audit View**. Analog to the *Global Vulnerability Audit View* shipped in version 4.11.0, this release includes a new interface to discover and filter policy violations across all projects in the portfolio.
- **Authorization for Badges**. Badges were previously not protected by authentication and authorization, and thus were disabled by default. With this release, unauthenticated access is deprecated. Instead, authenticating as a team with `VIEW_BADGES` permission is required. This can be combined with portfolio access control, such that a key can only access the badges of a subset of projects. Refer to the [badges documentation](/integrations/badges/) for details.
- **Modernization**. Behind the scenes, the tech stack that Dependency-Track is built on was upgraded to the latest and greatest. We moved from Java 17 to Java 21, from Java EE to Jakarta EE 10, from Jetty 10 to Jetty 12, and from Swagger v2 to OpenAPI v3.

**Features:**

- Exclude pre-releases from NuGet latest version check - [apiserver/#3468](https://github.com/DependencyTrack/dependency-track/pull/3468)
- Add global audit view for policy violations - [apiserver/#3544](https://github.com/DependencyTrack/dependency-track/pull/3544)
- Raise baseline Java version to 21 - [apiserver/#3682](https://github.com/DependencyTrack/dependency-track/pull/3682)
- Include whether a project’s version is active in the `/api/v1/project/{uuid}` response - [apiserver/#3691](https://github.com/DependencyTrack/dependency-track/pull/3691)
- Remove legacy `BomUploadProcessingTask` - [apiserver/#3722](https://github.com/DependencyTrack/dependency-track/pull/3722)
- Gracefully handle `NotSortableException`s in the REST API - [apiserver/#3724](https://github.com/DependencyTrack/dependency-track/pull/3724)
- Migrate REST API docs from Swagger v2 to OpenAPI v3 - [apiserver/#3726](https://github.com/DependencyTrack/dependency-track/pull/3726)
- Migrate to Jakarta EE 10 and Jetty 12 - [apiserver/#3730](https://github.com/DependencyTrack/dependency-track/pull/3730)
- Add support for EPSS policy conditions - [apiserver/#3746](https://github.com/DependencyTrack/dependency-track/pull/3746)
- Consider the group/namespace when searching components - [apiserver/#3761](https://github.com/DependencyTrack/dependency-track/pull/3761)
- Add notification for BOM validation failures - [apiserver/#3796](https://github.com/DependencyTrack/dependency-track/pull/3796)
- Bump CWE dictionary to v4.14 - [apiserver/#3819](https://github.com/DependencyTrack/dependency-track/pull/3819)
- Add ability to tag project upon BOM upload - [apiserver/#3843](https://github.com/DependencyTrack/dependency-track/pull/3843)
- Improve performance of finding retrieval via REST API - [apiserver/#3869](https://github.com/DependencyTrack/dependency-track/pull/3869)
- Add REST endpoints for tag retrieval - [apiserver/#3881](https://github.com/DependencyTrack/dependency-track/pull/3881)
- Deprecate `/api/v1/tag/{policyUuid}` in favor of `/api/v1/tag/policy/{uuid}` - [apiserver/#3887](https://github.com/DependencyTrack/dependency-track/pull/3887)
- Enable string de-duplication JVM option per default - [apiserver/#3893](https://github.com/DependencyTrack/dependency-track/pull/3893)
- Add REST endpoints for bulk tagging & un-tagging of projects - [apiserver/#3894](https://github.com/DependencyTrack/dependency-track/pull/3894)
- Add REST endpoint for tag deletion - [apiserver/#3896](https://github.com/DependencyTrack/dependency-track/pull/3896)
- Add OIDC Documentation for OneLogin - [apiserver/#3921](https://github.com/DependencyTrack/dependency-track/pull/3921)
- Add REST endpoints to tag and untag policies in bulk - [apiserver/#3924](https://github.com/DependencyTrack/dependency-track/pull/3924)
- Support the `component.authors` field of CycloneDX v1.6 - [apiserver/#3969](https://github.com/DependencyTrack/dependency-track/pull/3969)
- Make project cloning an atomic operation - [apiserver/#3982](https://github.com/DependencyTrack/dependency-track/pull/3982)
- Add option to test notifications - [apiserver/#3983](https://github.com/DependencyTrack/dependency-track/pull/3983)
  - *This feature was demoed in our September community meeting! Watch it [here](https://www.youtube.com/watch?v=hzelt7jv6dE&t=684s)*
- Log warning when dependency graph is missing the root node - [apiserver/#3990](https://github.com/DependencyTrack/dependency-track/pull/3990)
- Add ability to limit notifications to projects with specific tags - [apiserver/#4031](https://github.com/DependencyTrack/dependency-track/pull/4031)
  - *This feature was demoed in our September community meeting! Watch it [here](https://www.youtube.com/watch?v=hzelt7jv6dE&t=778s)*
- Enhance badge API to require authorization - [apiserver/#4059](https://github.com/DependencyTrack/dependency-track/pull/4059)
- Support assigning of teams for portfolio ACL when creating a project - [apiserver/#4093](https://github.com/DependencyTrack/dependency-track/pull/4093)
- Disable redundant shutdown hook of the embedded H2 database - [apiserver/#4106](https://github.com/DependencyTrack/dependency-track/pull/4106)
- Support inclusion and exclusion of projects from BOM validation with tags - [apiserver/#4109](https://github.com/DependencyTrack/dependency-track/pull/4109)
  - *This feature was demoed in our September community meeting! Watch it [here](https://www.youtube.com/watch?v=hzelt7jv6dE&t=568s)*
- Update Dependency-Track’s own BOM to CycloneDX v1.5 - [apiserver/#4110](https://github.com/DependencyTrack/dependency-track/pull/4110)
- Migrate Trivy integration to use Protobuf instead of JSON - [apiserver/#4116](https://github.com/DependencyTrack/dependency-track/pull/4116)
- Support customizable welcome message to display on login page - [apiserver/#4131](https://github.com/DependencyTrack/dependency-track/pull/4131)
- Raise maximum length of team names from 50 to 255 characters - [apiserver/#4134](https://github.com/DependencyTrack/dependency-track/pull/4134)
- Improve Jetty startup time - [apiserver/#4134](https://github.com/DependencyTrack/dependency-track/pull/4134)
- Support configuration of system-wide default locale - [apiserver/#4136](https://github.com/DependencyTrack/dependency-track/pull/4136)
- Bump SPDX license list to v3.25.0, bringing in 34 new licenses - [apiserver/#4145](https://github.com/DependencyTrack/dependency-track/pull/4145)
- Include team name in audit trail when auditing vulnerabilities with API key - [apiserver/#4154](https://github.com/DependencyTrack/dependency-track/pull/4154)
- Introduce `isLatest` flag for projects, and allow policies to be limited to latest version - [apiserver/#4184](https://github.com/DependencyTrack/dependency-track/pull/4184)
- Ensure modifying project endpoints are transactional - [apiserver/#4194](https://github.com/DependencyTrack/dependency-track/pull/4194)
- Support for serving the frontend from a custom path - [frontend/#801](https://github.com/DependencyTrack/frontend/pull/801)
- Add dynamic policy violation badges - [frontend/#810](https://github.com/DependencyTrack/frontend/pull/810)
- Add quick search for projects also using a component - [frontend/#848](https://github.com/DependencyTrack/frontend/pull/848)
- Add database name and version to *About* dialog - [frontend/#870](https://github.com/DependencyTrack/frontend/pull/870)
- Make *Severity* and *CWE* columns of findings table sortable - [frontend/#907](https://github.com/DependencyTrack/frontend/pull/907)
- Raise baseline Node version to 20 - [frontend/#927](https://github.com/DependencyTrack/frontend/pull/927)
- Add autocomplete support for tag inputs - [frontend/#936](https://github.com/DependencyTrack/frontend/pull/936)
- Save user preference for expanded navigation sidebar - [frontend/#988](https://github.com/DependencyTrack/frontend/pull/988)
- Add ability to download component table as CSV - [frontend/#993](https://github.com/DependencyTrack/frontend/pull/993)
- Add confirmation prompt for project deletion - [frontend/#996](https://github.com/DependencyTrack/frontend/pull/996)

**Fixes:**

- Fix wrong types in OpenAPI spec for UNIX timestamp fields - [apiserver/#3731](https://github.com/DependencyTrack/dependency-track/pull/3731)
- Fix `JDOUserException` when multiple licenses match a component’s license name - [apiserver/#3958](https://github.com/DependencyTrack/dependency-track/pull/3958)
- Fix broken anchors in documentation - [apiserver/#3965](https://github.com/DependencyTrack/dependency-track/pull/3965)
- Fix BOM validation failing for XML with multiple namespaces - [apiserver/#4020](https://github.com/DependencyTrack/dependency-track/pull/4020)
- Handle breaking change in Trivy 0.54.0 server API - [apiserver/#4023](https://github.com/DependencyTrack/dependency-track/pull/4023)
- Fix project link for new vulnerable dependency for email - [apiserver/#4026](https://github.com/DependencyTrack/dependency-track/pull/4026)
- Fix occasional `column list index is out of range` exceptions - [apiserver/#4104](https://github.com/DependencyTrack/dependency-track/pull/4104)
- Fix missing URL encoding for repository metadata analyzers - [apiserver/#4107](https://github.com/DependencyTrack/dependency-track/pull/4107)
- Fix project being rendered as PURL in email notifications - [apiserver/#4108](https://github.com/DependencyTrack/dependency-track/pull/4108)
- Fix incorrect rendering of special characters in email notifications - [apiserver/#4141](https://github.com/DependencyTrack/dependency-track/pull/4141)
- Use empty string instead of SNAPSHOT as version in BOM download if project doesn’t have a version - [apiserver/#4142](https://github.com/DependencyTrack/dependency-track/pull/4142)
- Handle empty component and service names in uploaded BOMs - [apiserver/#4146](https://github.com/DependencyTrack/dependency-track/pull/4146)
- Handle existing duplicate component properties - [apiserver/#4147](https://github.com/DependencyTrack/dependency-track/pull/4147)
- Fix infinite recursion during policy condition serialization - [apiserver/#4165](https://github.com/DependencyTrack/dependency-track/pull/4165)
- Fix `directDependencies` of cloned projects referring to original component UUIDs - [apiserver/#4153](https://github.com/DependencyTrack/dependency-track/pull/4171)
- Fix CPE not being imported from CycloneDX `metadata.component` - [apiserver/#4174](https://github.com/DependencyTrack/dependency-track/pull/4174)
- Fix update of an internal vulnerability clearing associated *Affected Components* - [apiserver/#4208](https://github.com/DependencyTrack/dependency-track/pull/4208)
- Fix metrics endpoint API docs erroneously claiming to return project and component data - [apiserver/#4195](https://github.com/DependencyTrack/dependency-track/pull/4195)
- Fix `IndexOutOfBoundsException` when mirroring OSV vulnerability without severity - [apiserver/#4196](https://github.com/DependencyTrack/dependency-track/pull/4196)
- Fix vulnerability endpoints returning projects and components that the principal shouldn’t have access to when portfolio ACL is enabled - [apiserver/#4201](https://github.com/DependencyTrack/dependency-track/pull/4201)
- Fix links with `href="#"` being pushed to Vue router - [frontend/#1012](https://github.com/DependencyTrack/frontend/pull/1012)

**Upgrade Notes:**

- The API server now requires Java 21 or newer. Users deploying Dependency-Track via containers don’t have to do anything, since those have been shipped with Java 21 since version 4.10.0. Users deploying Dependency-Track as JAR will need to upgrade their Java installation accordingly.
- The `/api/swagger.json` endpoint no longer exists. The REST API documentation is now available at `/api/openapi.json` and `/api/openapi.yaml` respectively. The documentation format follows the OpenAPI v3 specification, the Swagger v2 format is no longer provided.
- The `/api/v1/tag/{policyUuid}` REST API endpoint has been deprecated in favor of `/api/v1/tag/policy/{uuid}`. Users relying on the outdated endpoint for their custom integrations are encouraged to migrate to the new endpoint.
- The legacy BOM processing logic was removed. The *BOM Processing V2* option introduced in v4.11 is now the default and the only available option. To gauge the impact of this change, consider enabling the experimental option in an existing v4.11 deployment first.
- Deletion of tags requires the new `TAG_MANAGEMENT` permission. The permission is *not* added to existing users or teams automatically. Administrators should assign it to users and teams as needed.
- Accessing badges requires the new `VIEW_BADGES` permission. The permission is *not* added to existing users or teams automatically. Administrators should assign it to users and teams as needed.
- Unauthenticated access to badges is *deprecated* and will be fully removed in v4.13.
- To support serving of the frontend from custom paths ([frontend/#801](https://github.com/DependencyTrack/frontend/pull/801)), frontend containers can currently not function with a read-only filesystem (as commonly used in Kubernetes environments). Refer to [frontend/#940](https://github.com/DependencyTrack/frontend/issues/940) for details.

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.12.0](https://github.com/DependencyTrack/dependency-track/milestone/27?closed=1)
- [Frontend milestone 4.12.0](https://github.com/DependencyTrack/frontend/milestone/21?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects: [@2000rosser](https://github.com/2000rosser), [@Gepardgame](https://github.com/Gepardgame), [@JCHacking](https://github.com/JCHacking), [@SaberStrat](https://github.com/SaberStrat), [@Squixx](https://github.com/Squixx), [@aravindparappil46](https://github.com/aravindparappil46), [@brentos99](https://github.com/fupgang), [@gbonnefille](https://github.com/gbonnefille), [@mehab](https://github.com/mehab), [@nvcastelli](https://github.com/nvcastelli), [@peterakimball](https://github.com/peterakimball), [@rbt-mm](https://github.com/rbt-mm), [@rcsilva83](https://github.com/rcsilva83), [@rh0dy](https://github.com/rh0dy), [@rkg-mm](https://github.com/rkg-mm), [@setchy](https://github.com/setchy)

###### dependency-track-apiserver.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 0cfe5d6cd014a0a25cdb0379e5a75596adc3d448                         |
| SHA-256   | 83d31e132643249f7752154adc49690353484a66de6e77db7e25f0c1309528eb |

###### dependency-track-bundled.jar

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | f7a1af3a5bf5f5b864d0db519fe2944391496f32                         |
| SHA-256   | 3b4e27b29fd8a19cc5a250d394df43e0b046781f4d37c11720f8db8b9714d669 |

###### frontend-dist.zip

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 312dd2186deb81e50da00f2d42888711352f7853                         |
| SHA-256   | 589eb0aae9a3fbdfde4bdd4dda000a2fb6e08a27e66a52ef9b17c1eaa022d46e |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.12.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.12.0/bom.json)

<a href="cloudcannon:collections/_posts/2024-10-01-v4.12.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.11.7 <a href="#v4-11-7" class="anchor">#</a>

<span class="date">August 14, 2024</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix `directDependencies`, `externalReferences`, and `metadata` fields missing from `/api/v1/project/{uuid}` response when not already cached - [apiserver/#4071](https://github.com/DependencyTrack/dependency-track/pull/4071)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.11.7](https://github.com/DependencyTrack/dependency-track/milestone/44?closed=1)
- [Frontend milestone 4.11.7](https://github.com/DependencyTrack/frontend/milestone/29?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.7/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 9a916abcbb478a4dbad101f5335acdf2b8462062                         |
| SHA-256   | 2df1b2ea67a16cdc6108c3ac2f538018e529205ce5f36a6da78f2feefeddd2c8 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.7/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | c5a30ee550af8a943bb77167e515fb6422e51b36                         |
| SHA-256   | 4665cdd14351d7b1c41004ffc57791297c4ec5fc7f958635cff246d1b1a95eed |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.11.7/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | f481a9fca8e9f1eca7693cd638eef0eb5a1ed5a2                         |
| SHA-256   | 332cc69c102c3df90f41c10687b78553dfb8bf6a66ffb6236f97d24fc932b2b7 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.7/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.11.7/bom.json)

<a href="cloudcannon:collections/_posts/2024-08-14-v4.11.7.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.11.6 <a href="#v4-11-6" class="anchor">#</a>

<span class="date">August 10, 2024</span> <span class="badge patch">patch</span>

**Enhancements:**

- Improve French translation - [frontend/#964](https://github.com/DependencyTrack/frontend/pull/964)

**Fixes:**

- Handle breaking change in Trivy v0.54.0 server API - [apiserver/#4040](https://github.com/DependencyTrack/dependency-track/pull/4040)
- Fix validation error when XML BOM declares multiple namespaces - [apiserver/#4041](https://github.com/DependencyTrack/dependency-track/pull/4041)
- Fix `JDOUserException` when multiple licenses match a component’s license name - [apiserver/#4042](https://github.com/DependencyTrack/dependency-track/pull/4042)
- Fix anchors in changelog documentation - [apiserver/#4043](https://github.com/DependencyTrack/dependency-track/pull/4043)
- Fix project link for new vulnerable dependency in email notifications - [apiserver/#4044](https://github.com/DependencyTrack/dependency-track/pull/4044)
- Fix `parent` field occasionally missing in `/api/v1/project/{uuid}` responses - [apiserver/#4049](https://github.com/DependencyTrack/dependency-track/pull/4049)
- Fix VEX export returning invalid CycloneDX - [apiserver/#4054](https://github.com/DependencyTrack/dependency-track/pull/4054)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.11.6](https://github.com/DependencyTrack/dependency-track/milestone/43?closed=1)
- [Frontend milestone 4.11.6](https://github.com/DependencyTrack/frontend/milestone/28?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@2000rosser](https://github.com/2000rosser), [@JCHacking](https://github.com/JCHacking), [@SaberStrat](https://github.com/SaberStrat), [@molusk](https://github.com/molusk), [@philippn](https://github.com/philippn)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.6/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | daab7ed5b760ff909e4b9cc041b89c3374c1d955                         |
| SHA-256   | a76cc3417728bdc880f41af613e543d3e5f033d7b0b1db84ffb397bcbcb3936b |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.6/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 8ff2bd4db69e7083d501a4c489f703677044a5f0                         |
| SHA-256   | fd1c25e2b2d727f377eeec8240370558a9796225fe4dc0f258021b1061fbc36f |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.11.6/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | c91bede201957c994f338a043a44ebd32824319e                         |
| SHA-256   | 55ea0735b80c8cc17d31590ba16c3650943a3cdb595accf3540fefd1670ee1b9 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.6/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.11.6/bom.json)

<a href="cloudcannon:collections/_posts/2024-08-10-v4.11.6.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.11.5 <a href="#v4-11-5" class="anchor">#</a>

<span class="date">July 08, 2024</span> <span class="badge patch">patch</span>

This release primarily addresses an inability to mirror the NVD via its REST API. The NVD REST API recently experienced increased load, causing service disruptions. Dependency-Track users who opted into API mirroring will have seen symptoms of this as `NvdApiException: NVD Returned Status Code: 503` errors in the logs.

To reduce load on their systems, [NIST started to block](https://github.com/jeremylong/Open-Vulnerability-Project/issues/184#issuecomment-2214217254) requests with a certain `User-Agent` header, which Dependency-Track happens to use. Upgrading to v4.11.5 will allow Dependency-Track to no longer be subject to this block.

Users who can’t immediately update, yet are reliant on NVD data being current, can switch back to the feed file based mirroring by disabling *Enable mirroring via API* in the administration panel.

**Fixes:**

- Fix broken NVD mirroring via REST API - [apiserver/#3940](https://github.com/DependencyTrack/dependency-track/pull/3940)
- Fix BOM processing V2 dispatching `BOM_CONSUMED` and `BOM_PROCESSED` notification with scope `SYSTEM` instead of `PORTFOLIO` - [apiserver/#3941](https://github.com/DependencyTrack/dependency-track/pull/3941)
- Fix BOM export producing invalid CycloneDX for custom licenses - [apiserver/#3942](https://github.com/DependencyTrack/dependency-track/pull/3942)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.11.5](https://github.com/DependencyTrack/dependency-track/milestone/42?closed=1)
- [Frontend milestone 4.11.5](https://github.com/DependencyTrack/frontend/milestone/27?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@2000rosser](https://github.com/2000rosser)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.5/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 8fd45ea6ae725e8e7dac59ec9d471fcdaeb42c6d                         |
| SHA-256   | c39c15849cbb7dd19833ea689c20aaf92bc9f6965b758961e1d2a01a2b09f86f |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.5/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | eba6cbaa6c2da9ffb295da83ed39af68ff4130a8                         |
| SHA-256   | 7ebb11573b2a59084ed98fe92d363240c910dc7b5aa7ebeda64bee7d47089d9a |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.11.5/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 0992c02871d536eaa1d3971a01ce815daf115129                         |
| SHA-256   | fa427fd6dde55fe6a327a82f52edcdbe29a04f23d360742fe446b0c8e1714647 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.5/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.11.5/bom.json)

<a href="cloudcannon:collections/_posts/2024-07-08-v4.11.5.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.11.4 <a href="#v4-11-4" class="anchor">#</a>

<span class="date">June 24, 2024</span> <span class="badge patch">patch</span>

**Enhancements:**

- Add support for ingestion of CycloneDX v1.6 BOMs - [apiserver/#3863](https://github.com/DependencyTrack/dependency-track/pull/3863)
- Improve German translation - [frontend/#917](https://github.com/DependencyTrack/frontend/pull/917)
- Improve Chinese translation - [frontend/#918](https://github.com/DependencyTrack/frontend/pull/918)

**Fixes:**

- Fix inverted “show inactive” filter in vulnerability audit view - [apiserver/#3864](https://github.com/DependencyTrack/dependency-track/pull/3864)
- Fix BOM validation failing when URL contains encoded `[` and `]` characters - [apiserver/#3866](https://github.com/DependencyTrack/dependency-track/pull/3866)
- Fix external references not being updated via `POST /v1/component` - [apiserver/#3867](https://github.com/DependencyTrack/dependency-track/pull/3867)
- Fix possible XXE injection during CycloneDX validation and parsing - [GHSA-7r6q-xj4c-37g4](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-7r6q-xj4c-37g4) / [apiserver/#3871](https://github.com/DependencyTrack/dependency-track/pull/3871)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.11.4](https://github.com/DependencyTrack/dependency-track/milestone/41?closed=1)
- [Frontend milestone 4.11.4](https://github.com/DependencyTrack/frontend/milestone/26?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@2000rosser](https://github.com/2000rosser), [@fupgang](https://github.com/fupgang), [@sahibamittal](https://github.com/sahibamittal), [@zeed-w-beez](https://github.com/zeed-w-beez)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.4/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 19531d4f02cccf26478b3a63feba355da8726b3f                         |
| SHA-256   | 9a09259ba4c19d02b81a39fb5894df758f19ff1bb43538d4b999b4a5789a9d9b |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.4/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 3c4bb658783157ae9c408b8323e25e55c9ab25fd                         |
| SHA-256   | 73fc867d347da8a8af14f8c6812e13b870037a28d7de83e2837db9c27d840100 |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.11.4/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 5c462c69fd18bdcd87dc2c2d757a1eb268e6e679                         |
| SHA-256   | ea747f848de6a6def6f73209d7f43424c6314d09bc8ea37be621be50dbac755b |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.4/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.11.4/bom.json)

<a href="cloudcannon:collections/_posts/2024-06-24-v4.11.4.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.11.3 <a href="#v4-11-3" class="anchor">#</a>

<span class="date">June 03, 2024</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix `JDODataStoreException` for unresolved licenses during BOM upload processing - [apiserver/#3801](https://github.com/DependencyTrack/dependency-track/pull/3801)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.11.3](https://github.com/DependencyTrack/dependency-track/milestone/40?closed=1)
- [Frontend milestone 4.11.3](https://github.com/DependencyTrack/frontend/milestone/25?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.3/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | ff4284ce635f4da916e907af20bb0e9339349ecd                         |
| SHA-256   | f1e34cc7a0c5e2fe444e934aa221853ac762ee79997bc10fa712ee6ac8f776d8 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.3/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | beea18173e6a52180ac1a8ee721dd7f775eaaf2d                         |
| SHA-256   | d62557345bb244b5d34e7a56d057e264044524d8df7964df23383a2ace658cbd |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.11.3/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | dc7859636f1bf7a3772dc0e8de27535031511a4c                         |
| SHA-256   | 88684d3bbd0aa2ff300ae419653f85957deaf00d9ca615a747386997b3f0e154 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.3/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.11.3/bom.json)

<a href="cloudcannon:collections/_posts/2024-06-03-v4.11.3.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.11.2 <a href="#v4-11-2" class="anchor">#</a>

<span class="date">June 01, 2024</span> <span class="badge patch">patch</span>

**Fixes:**

- Handle breaking change in Trivy v0.51.2 server API - [apiserver/#3785](https://github.com/DependencyTrack/dependency-track/pull/3785)
- Fix licenses not being resolved by name - [apiserver/#3786](https://github.com/DependencyTrack/dependency-track/pull/3786)
- Fix project name not showing in Jira tickets for *NEW_VULNERABLE_DEPENDENCY* notifications - [apiserver/#3787](https://github.com/DependencyTrack/dependency-track/pull/3787)
- Fix parsing of NuGet timestamps with offset - [apiserver/#3788](https://github.com/DependencyTrack/dependency-track/pull/3788)
- Fix Slack notifications failing when no base URL is configured - [apiserver/#3792](https://github.com/DependencyTrack/dependency-track/pull/3792)
- Fix project version dropdown exceeding the screen size - [frontend/#882](https://github.com/DependencyTrack/frontend/pull/882)
- Update English translation - [frontend/#883](https://github.com/DependencyTrack/frontend/pull/883)
- Update French translation - [frontend/#884](https://github.com/DependencyTrack/frontend/pull/884)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.11.2](https://github.com/DependencyTrack/dependency-track/milestone/39?closed=1)
- [Frontend milestone 4.11.2](https://github.com/DependencyTrack/frontend/milestone/24?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@aravindparappil46](https://github.com/aravindparappil46), [@lgrguricmileusnic](https://github.com/lgrguricmileusnic), [@molusk](https://github.com/molusk), [@sahibamittal](https://github.com/sahibamittal)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.2/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 174956bf3cd2dab16cfd36e7ab1b5d7001b99160                         |
| SHA-256   | 135cf4361bbbc65f488796bf196c8d2d3cbebec931b249e037551c6fbbae2ed7 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.2/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | af75c903b033418ea6326cbb4e6885afba99ee94                         |
| SHA-256   | 5020ac51158038439b7482d5c5fec151773162724dce1779249bf73053456d34 |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.11.2/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 1119cb6abbcdfe014f013205d40ae11668bd5c83                         |
| SHA-256   | 9d122fc6ddea378afc87bf555949f6c201281c9289a36ae97900b7bee4cbc7f5 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.2/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.11.2/bom.json)

<a href="cloudcannon:collections/_posts/2024-06-01-v4.11.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.11.1 <a href="#v4-11-1" class="anchor">#</a>

<span class="date">May 19, 2024</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix failing JSON BOM validation when `specVersion` is not one of the first fields - [apiserver/#3698](https://github.com/DependencyTrack/dependency-track/pull/3698)
- Fix broken global vuln audit view for MSSQL - [apiserver/#3701](https://github.com/DependencyTrack/dependency-track/pull/3701)
- Fix OS package vulnerabilities not being detected by Trivy - [apiserver/#3729](https://github.com/DependencyTrack/dependency-track/pull/3729)
- Improve Japanese translation - [frontend/#869](https://github.com/DependencyTrack/frontend/pull/869)
- Fix broken *Vulnerabilities* progress bar in *Project* -\> *Components* view - [frontend/#873](https://github.com/DependencyTrack/frontend/pull/873)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.11.1](https://github.com/DependencyTrack/dependency-track/milestone/37?closed=1)
- [Frontend milestone 4.11.1](https://github.com/DependencyTrack/frontend/milestone/22?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@aravindparappil46](https://github.com/aravindparappil46), [@fnxpt](https://github.com/fnxpt), [@tiwatsuka](https://github.com/tiwatsuka)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.1/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | aa3d8ffc6b8f9d15a801148a93275ebeba922010                         |
| SHA-256   | ed08e60e0761ced93454c14194da02be5950805911dbc7f7c611bdf0e753b437 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.1/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | c57f1b8c003d95daa871096cbc37a6c03cd08907                         |
| SHA-256   | e7613d6654083ab6e2c4ae24459444efe4d83df5d2c4d27e58a94bc809e2627a |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.11.1/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 995e21388806efc102bf7bc14bc6ac5a3c354fc7                         |
| SHA-256   | 27e7d91ba0fe3b54dcbef8a7c44c1ee0b9afe2ba3d96c47b55d3beca68206fd2 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.1/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.11.1/bom.json)

<a href="cloudcannon:collections/_posts/2024-05-19-v4.11.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.11.0 <a href="#v4-11-0" class="anchor">#</a>

<span class="date">May 07, 2024</span> <span class="badge major">major</span>

**Highlights:**

- **Optimized BOM Ingestion**. The logic that governs how uploaded BOMs are processed and ingested into Dependency-Track has been overhauled to be more reliable and efficient. Further, BOM processing is now an atomic operation, such that errors occurring midway do not cause a partial state to be left behind. De-duplication of components and services is more predictable, and log messages emitted during processing contain additional context, making them easier to correlate. Because the new implementation can have a big impact on how Dependency-Track behaves regarding BOM uploads, it is disabled by default for this release. It may be enabled in the administration panel under *Configuration* -\> *Experimental*.
- **BOM Validation**. Historically, Dependency-Track did not validate uploaded BOMs and VEXs against the CycloneDX schema. While this allowed BOMs to be processed that did not strictly adhere to the schema, it could also lead to confusion when uploaded files were accepted, but then failed to be ingested during asynchronous processing. Starting with this release, uploaded files will be rejected if they fail schema validation. Note that this may reveal issues in BOM generators that currently produce invalid CycloneDX documents. Validation may be turned off in the administration panel under *Configuration* -\> *BOM Formats*.
  - *This feature was demoed in our April community meeting! Watch it [here](https://www.youtube.com/watch?v=3iIeajRJK8o&t=450s)*
- **Global Vulnerability Audit View**. This new interface allows users to discover and filter vulnerabilities that affect their portfolio, across all projects. When portfolio access control is enabled, this view is limited to projects a user has explicit access to. It is possible to inspect individual findings, or aggregates grouped by vulnerability, making it possible to spot the most prevalent vulnerabilities.
  - *This feature was demoed in our April community meeting! Watch it [here](https://www.youtube.com/watch?v=3iIeajRJK8o&t=572s).*
- **Trivy Analyzer Integration**. It is now possible to leverage [Trivy](https://trivy.dev/) in [server mode](https://aquasecurity.github.io/trivy/v0.50/docs/references/modes/client-server/) for vulnerability analysis.
  - Refer to the [analyzer’s documentation](/datasources/trivy/) for further details, in particular the [known limitations](/datasources/trivy/#known-limitations).
  - *This feature was demoed in our April community meeting! Watch it [here](https://www.youtube.com/watch?v=3iIeajRJK8o&t=725s).*
- **Extended Localization**. The UI now supports 12 additional languages. Users can change their language preference in their profile settings. While the Portuguese, Brazilian Portuguese, and Spanish translations were provided by a native speaker (thanks [@fnxpt](https://github.com/fnxpt)!), the majority of languages are currently machine-translated. Translation improvements are a great way to contribute to the project, please find additional details [here](https://github.com/DependencyTrack/frontend?tab=readme-ov-file#internationalization-i18n).
- **Official Helm Chart**. The Dependency-Track project now offers an official Helm chart for Kubernetes deployments. Community input and contributions are highly requested. The chart repository can be found at <https://github.com/DependencyTrack/helm-charts>. It is also available through [Artifact Hub](https://artifacthub.io/packages/helm/dependencytrack/dependency-track).

**Features:**

- Add global vulnerability audit view - [apiserver/#2472](https://github.com/DependencyTrack/dependency-track/pull/2472)
- Add support for vulnerability analysis with Trivy - [apiserver/#3259](https://github.com/DependencyTrack/dependency-track/pull/3259)
- Return processing token when cloning a project - [apiserver/#3260](https://github.com/DependencyTrack/dependency-track/pull/3260)
- Only show projects that haven’t been added to the team yet when configuring ACLs - [apiserver/#3261](https://github.com/DependencyTrack/dependency-track/pull/3261)
- Clarify OpenID Connect group mapping to teams - [apiserver/#3269](https://github.com/DependencyTrack/dependency-track/pull/3269)
- Add option to configure token for Webhook notifications - [apiserver/#3275](https://github.com/DependencyTrack/dependency-track/pull/3275)
- Add notifications for user creation and deletion - [apiserver/#3275](https://github.com/DependencyTrack/dependency-track/pull/3275)
- Pre-process CWE dictionary, drop `CWE` table - [apiserver/#3284](https://github.com/DependencyTrack/dependency-track/pull/3284)
- Add “Show in Dependency Graph” button in “Affected Projects” list - [apiserver/#3285](https://github.com/DependencyTrack/dependency-track/pull/3285)
- Document risk score calculation - [apiserver/#3347](https://github.com/DependencyTrack/dependency-track/pull/3347)
- Make processing of uploaded BOMs atomic - [apiserver/#3357](https://github.com/DependencyTrack/dependency-track/pull/3357)
- Improve performance of BOM processing - [apiserver/#3357](https://github.com/DependencyTrack/dependency-track/pull/3357)
- Add more context to logs emitted during BOM processing - [apiserver/#3357](https://github.com/DependencyTrack/dependency-track/pull/3357)
  - BOM format, spec version, serial number, and version
  - Project UUID, name, and version
- Store severities in database instead of computing them ad-hoc in-memory - [apiserver/#3408](https://github.com/DependencyTrack/dependency-track/pull/3408)
- Add OIDC docs for large enterprise configuration using Azure AD - [apiserver/#3414](https://github.com/DependencyTrack/dependency-track/pull/3414)
- Make subject prefix for email notifications configurable - [apiserver/#3422](https://github.com/DependencyTrack/dependency-track/pull/3422)
- Support toggling between active / inactive projects in the “Affected Projects” list - [apiserver/#3425](https://github.com/DependencyTrack/dependency-track/pull/3425)
- Add attribution notice to NVD documentation - [apiserver/#3490](https://github.com/DependencyTrack/dependency-track/pull/3490)
- Bump CWE dictionary to v4.13 - [apiserver/#3491](https://github.com/DependencyTrack/dependency-track/pull/3491)
- Align retry configuration and behavior across analyzers - [apiserver/#3494](https://github.com/DependencyTrack/dependency-track/pull/3494)
- Add support for component properties - [apiserver/#3499](https://github.com/DependencyTrack/dependency-track/pull/3499)
- Add auto-generated changelog to GitHub releases - [apiserver/#3502](https://github.com/DependencyTrack/dependency-track/pull/3502)
- Bump SPDX license list to v3.23, bringing in 91 new licenses - [apiserver/#3508](https://github.com/DependencyTrack/dependency-track/pull/3508)
- Validate uploaded BOMs against CycloneDX schema prior to processing them - [apiserver/#3522](https://github.com/DependencyTrack/dependency-track/pull/3522)
- Improve observability of Lucene search indexes - [apiserver/#3535](https://github.com/DependencyTrack/dependency-track/pull/3535)
- Add support for Hackage repositories - [apiserver/#3549](https://github.com/DependencyTrack/dependency-track/pull/3549)
- Add support for Nix repositories - [apiserver/#3549](https://github.com/DependencyTrack/dependency-track/pull/3549)
- Add *required permissions* to OpenAPI descriptions of endpoints - [apiserver/#3557](https://github.com/DependencyTrack/dependency-track/pull/3557)
- Add support for exporting findings in SARIF format - [apiserver/#3561](https://github.com/DependencyTrack/dependency-track/pull/3561)
- Ingest vulnerability alias information from VulnDB - [apiserver/#3588](https://github.com/DependencyTrack/dependency-track/pull/3588)
- Properly validate UUID request parameters to prevent internal server errors - [apiserver/#3590](https://github.com/DependencyTrack/dependency-track/pull/3590)
- Document pagination query parameters in OpenAPI specification - [apiserver/#3625](https://github.com/DependencyTrack/dependency-track/pull/3625)
- Document sorting query parameters in OpenAPI specification - [apiserver/#3631](https://github.com/DependencyTrack/dependency-track/pull/3631)
- Gracefully handle unique constraint violations - [apiserver/#3648](https://github.com/DependencyTrack/dependency-track/pull/3648)
- Log debug information upon possible secret key corruption - [apiserver/#3651](https://github.com/DependencyTrack/dependency-track/pull/3651)
- Add support for worker pool drain timeout - [apiserver/#3657](https://github.com/DependencyTrack/dependency-track/pull/3657)
- Fall back to no authentication when OSS Index API token decryption fails - [apiserver/#3661](https://github.com/DependencyTrack/dependency-track/pull/3661)
- Include project details in MS Teams notification for *BOM_PROCESSING_FAILED* - [apiserver/#3666](https://github.com/DependencyTrack/dependency-track/pull/3666)
- Show component count in projects list - [frontend/#683](https://github.com/DependencyTrack/frontend/pull/683)
- Add current *fail*, *warn*, and *info* values to bottom of policy violation metrics - [frontend/#707](https://github.com/DependencyTrack/frontend/pull/707)
- Remove unused policy violation widget - [frontend/#710](https://github.com/DependencyTrack/frontend/pull/710)
- Use consistent coloring for “Suppressed” metrics - [frontend/#712](https://github.com/DependencyTrack/frontend/pull/712)
- Show policy violations by state and classification - [frontend/#717](https://github.com/DependencyTrack/frontend/pull/717)
- Show footer counters in “Portfolio Vulnerabilities” metrics - [frontend/#718](https://github.com/DependencyTrack/frontend/pull/718)
- Improve UX of the project active / inactive toggle - [frontend/#721](https://github.com/DependencyTrack/frontend/pull/721)
- Show publisher name when expanding rows in the “Alerts” table - [frontend/#728](https://github.com/DependencyTrack/frontend/pull/728)
- Improve tooltip clarity for project vulnerabilities - [frontend/#733](https://github.com/DependencyTrack/frontend/pull/733)
- Show badges on “Policy Violations” tab - [frontend/#744](https://github.com/DependencyTrack/frontend/pull/744)
- Add ESLint and prettier for consistent code formatting - [frontend/#752](https://github.com/DependencyTrack/frontend/pull/752)
- Display *created* and *last used* timestamps for API keys - [frontend/#768](https://github.com/DependencyTrack/frontend/pull/768)
- Display API key comments and make them editable - [frontend/#768](https://github.com/DependencyTrack/frontend/pull/768)
- Add *internal* column to component search view - [frontend/#775](https://github.com/DependencyTrack/frontend/pull/775)
- Add *classification* badge to component details to highlight *internal* components - [frontend/#776](https://github.com/DependencyTrack/frontend/pull/776)
- Add *group* to component breadcrumb - [frontend/#777](https://github.com/DependencyTrack/frontend/pull/777)
- Add *deprecated* column to license list - [frontend/#792](https://github.com/DependencyTrack/frontend/pull/792)
- Use *concise* endpoint to populate license list - [frontend/#793](https://github.com/DependencyTrack/frontend/pull/793)
- Display *comment* field of external references - [frontend/#803](https://github.com/DependencyTrack/frontend/pull/803)
- Add support for 12 new languages, and localization based on browser language or custom preference - [frontend/#805](https://github.com/DependencyTrack/frontend/pull/805)
- Improve contrast ratio on progress bars - [frontend/#816](https://github.com/DependencyTrack/frontend/pull/816)
- Add language picker to profile dropdown - [frontend/#824](https://github.com/DependencyTrack/frontend/pull/824)
- Display EPSS score and percentile on vulnerability view - [frontend/#832](https://github.com/DependencyTrack/frontend/pull/832)

**Fixes:**

- Fix policy violations not being considered when cloning a project - [apiserver/#3248](https://github.com/DependencyTrack/dependency-track/pull/3248)
- Fix `StackOverflowError` when processing BOMs with deeply nested component structures - [apiserver/#3357](https://github.com/DependencyTrack/dependency-track/pull/3357)
- Fix inconsistent component de-duplication during BOM processing, causing varying components counts in successive uploads - [apiserver/#3357](https://github.com/DependencyTrack/dependency-track/pull/3357)
- Fix components erroneously being de-duplicated when only a single attribute of their [component identity](https://docs.dependencytrack.org/analysis-types/component-identity/) is identical - [apiserver/#3357](https://github.com/DependencyTrack/dependency-track/pull/3357)
- Fix components defined in the BOM node `metadata.component.components` not being imported - [apiserver/#3357](https://github.com/DependencyTrack/dependency-track/pull/3357)
- Fix withdrawn GitHub Advisories being mirrored - [apiserver/#3394](https://github.com/DependencyTrack/dependency-track/pull/3394)
- Fix broken image in OIDC documentation - [apiserver/#3411](https://github.com/DependencyTrack/dependency-track/pull/3411)
- Fix VulnDB parser being unable to import vulnerability records when `nvd_additional_information` is empty - [apiserver/#3437](https://github.com/DependencyTrack/dependency-track/pull/3437)
- Fix `URISyntaxException` when NPM PURL contains special characters - [apiserver/#3456](https://github.com/DependencyTrack/dependency-track/pull/3456)
- Fix finding attribution date not being retained when cloning a project - [apiserver/#3488](https://github.com/DependencyTrack/dependency-track/pull/3488)
- Fix Cargo repository metadata analyzer not being invoked - [apiserver/#3511](https://github.com/DependencyTrack/dependency-track/pull/3511)
- Fix type of `purl` fields in Swagger docs - [apiserver/#3512](https://github.com/DependencyTrack/dependency-track/pull/3512)
- Fix CI build status badge - [apiserver/#3513](https://github.com/DependencyTrack/dependency-track/pull/3513)
- Fix `bom` and `vex` request fields not being visible in OpenAPI spec - [apiserver/#3557](https://github.com/DependencyTrack/dependency-track/pull/3557)
- Fix unclear error response when base64 encoded `bom` and `vex` values exceed character limit - [apiserver/#3558](https://github.com/DependencyTrack/dependency-track/pull/3558)
- Fix unhandled `NotFoundException`s causing a `HTTP 500` response - [apiserver/#3559](https://github.com/DependencyTrack/dependency-track/pull/3559)
- Fix inability to store PURLs longer than 255 characters - [apiserver/#3560](https://github.com/DependencyTrack/dependency-track/pull/3560)
- Disable automatic API key generation for newly created teams - [apiserver/#3574](https://github.com/DependencyTrack/dependency-track/pull/3574)
- Fix severity not being set for vulnerabilities from VulnDB - [apiserver/#3595](https://github.com/DependencyTrack/dependency-track/pull/3595)
- Fix `JDOFatalUserException` for long reference URLs from OSS Index - [apiserver/#3650](https://github.com/DependencyTrack/dependency-track/pull/3650)
- Fix unhandled `ClientErrorException`s causing a `HTTP 500` response - [apiserver/#3659](https://github.com/DependencyTrack/dependency-track/pull/3659)
- Fix unique constraint violation during NVD mirroring via feed files - [apiserver/#3664](https://github.com/DependencyTrack/dependency-track/pull/3664)
- Fix `VUE_APP_SERVER_URL` being ignored - [frontend/#682](https://github.com/DependencyTrack/frontend/pull/682)
- Fix visibility of “Vulnerabilities” and “Policy Violations” columns not being toggle-able individually - [frontend/#686](https://github.com/DependencyTrack/frontend/pull/686)
- Fix finding search routes - [frontend/#689](https://github.com/DependencyTrack/frontend/pull/689)
- Fix CI build status badge - [frontend/#699](https://github.com/DependencyTrack/frontend/pull/699)
- Fix incorrect calculation of “Audited Violations” and “Audited Vulnerabilities” percentages - [frontend/#704](https://github.com/DependencyTrack/frontend/pull/704)
- Fix percentage calculation to consistently round to two decimal places - [frontend/#708](https://github.com/DependencyTrack/frontend/pull/708)
- Fix percentage calculation edge cases - [frontend/#719](https://github.com/DependencyTrack/frontend/pull/719)
- Fix “Outdated Only” button being disabled when dependency graph is not available - [frontend/#725](https://github.com/DependencyTrack/frontend/pull/725)
- Fix redundant requests to `/api/v1/component` when loading project page - [frontend/#726](https://github.com/DependencyTrack/frontend/pull/726)
- Fix column visibility preferences triggering redundant requests - [frontend/#727](https://github.com/DependencyTrack/frontend/pull/727)
- Fix `@<version>` being appended when rendering CPEs in “Affected Components” view - [frontend/#748](https://github.com/DependencyTrack/frontend/pull/748)
- Fix aliases not being displayed in vulnerabilities list - [frontend/#766](https://github.com/DependencyTrack/frontend/pull/766)
- Fix link to *portfolio access control* view - [frontend/#774](https://github.com/DependencyTrack/frontend/pull/774)
- Fix *Download BOM* button requiring higher privileges than necessary - [frontend/#812](https://github.com/DependencyTrack/frontend/pull/812)

**Upgrade Notes:**

- To enable the optimized BOM ingestion, toggle the *BOM Processing V2* option in the administration panel under *Configuration* -\> *Experimental*
- Validation of uploaded BOMs and VEXs is enabled per default, but can be disabled in the administration panel under *Configuration* -\> *BOM Formats* -\> *BOM Validation*
- The `CWE` table is dropped automatically upon upgrade, it has been unused since v4.5
- The default logging configuration ([logback.xml](https://github.com/DependencyTrack/dependency-track/blob/master/src/main/docker/logback.xml)) was updated to include the [Mapped Diagnostic Context](https://logback.qos.ch/manual/mdc.html) (MDC)
  - Users who [customized their logging configuration](/getting-started/monitoring/#custom-logging-configuration) are recommended to follow this change
- Severities of vulnerabilities that previously had `NULL` severities in the database will be computed and updated automatically upon upgrade, based on CVSSv2, CVSSv3, and OWASP Risk Rating scores
  - Database updates are batched, the entire procedure should complete 30s to 1min
- The following configuration properties were renamed:
  - `ossindex.retry.backoff.max.duration` → `ossindex.retry.backoff.max.duration.ms`
  - `snyk.retry.exponential.backoff.multiplier` → `snyk.retry.backoff.multiplier`
  - `snyk.retry.exponential.backoff.initial.duration.seconds` → `snyk.retry.backoff.initial.duration.ms`
  - `snyk.retry.exponential.backoff.max.duration.seconds` → `snyk.retry.backoff.max.duration.ms`
- Configuration properties for retry durations are now specified in milliseconds instead of seconds
- The following default values for configuration properties have changed:
  - `ossindex.retry.backoff.max.duration.ms`: 600000ms (10min) → 60000ms (1min)
- The `name` tag of the `resilience4j_retry_calls_total` for OSS Index has changed from `ossIndexRetryer` to `ossindex-api`
- The types of the following columns are changed from `VARCHAR(255)` to `VARCHAR(786)` automatically upon upgrade:
  - `COMPONENT.PURL`
  - `COMPONENT.PURLCOORDINATES`
  - `COMPONENTANALYSISCACHE.TARGET`
  - `PROJECT.PURL`

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.11.0](https://github.com/DependencyTrack/dependency-track/milestone/25?closed=1)
- [Frontend milestone 4.11.0](https://github.com/DependencyTrack/frontend/milestone/16?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@2000rosser](https://github.com/2000rosser), [@AnthonyMastrean](https://github.com/AnthonyMastrean), [@LaVibeX](https://github.com/LaVibeX), [@MangoIV](https://github.com/MangoIV), [@Robbilie](https://github.com/Robbilie), [@VithikaS](https://github.com/VithikaS), [@a5a351e7](https://github.com/a5a351e7), [@acdha](https://github.com/acdha), [@aravindparappil46](https://github.com/aravindparappil46), [@baburkin](https://github.com/baburkin), [@fnxpt](https://github.com/fnxpt), [@kepten](https://github.com/kepten), [@leec94](https://github.com/leec94), [@lukas-braune](https://github.com/lukas-braune), [@malice00](https://github.com/malice00), [@mehab](https://github.com/mehab), [@mge-mm](https://github.com/mikkeschiren), [@mykter](https://github.com/mykter), [@rbt-mm](https://github.com/rbt-mm), [@rkesters](https://github.com/rkesters), [@rkg-mm](https://github.com/rkg-mm), [@sahibamittal](https://github.com/sahibamittal), [@sebD](https://github.com/sebD), [@setchy](https://github.com/setchy), [@validide](https://github.com/validide)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.0/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | a9dae58a25c8aeeb54134ff054214505eb170db9                         |
| SHA-256   | 03160957fced99c3d923bbb5c6cb352740da1970bd4775b52bb451b95c4cefaf |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.0/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 59b78c3f6b1979ba29c1bd754b7dc1005101fc49                         |
| SHA-256   | 1a34808cd6c7a9bf7b181e4f175c077f1ee5d5a9daf327b330db9b1c63aac2d3 |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.11.0/frontend-dist.zip)

| Algorithm | Checksum                                                                           |
|:----------|:-----------------------------------------------------------------------------------|
| SHA-1     | 80cddddaf5c9c73676065d4ab6fe7b3eff3ec8de                                           |
| SHA-256   | 9c51c337f4b2a7e78730c70473cd24070773a0982d1c0ee6c13f9a6f18a756d5 frontend-dist.zip |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.11.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.11.0/bom.json)

<a href="cloudcannon:collections/_posts/2024-05-07-v4.11.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.10.1 <a href="#v4-10-1" class="anchor">#</a>

<span class="date">December 19, 2023</span> <span class="badge patch">patch</span>

This release fixes various defects in the API server.  
There are no changes for the frontend, the latest version of it remains 4.10.0.

**NVD Data Feed Retirement Update:**

The NVD has [announced](https://groups.google.com/a/list.nist.gov/g/nvd-news/c/aofnAd3HP2g) that retirement of the legacy data feeds has been delayed *until further notice*. Dependency-Track users who:

- ran into issues with the new NVD REST API integration, or
- did not have the time yet to migrate

can safely continue consuming the legacy feeds, or switch back to it.

**Fixes:**

- Fix alert rules not working for projects where the `ACTIVE` column is `NULL` - [apiserver/#3306](https://github.com/DependencyTrack/dependency-track/pull/3306)
- Fix NPE in version distance policy evaluation when project has no direct dependencies - [apiserver/#3308](https://github.com/DependencyTrack/dependency-track/pull/3308)
- Fix `ClassCastException` when updating an existing `ProjectMetadata#authors` field - [apiserver/#3312](https://github.com/DependencyTrack/dependency-track/pull/3312)
- Fix NPE in GitHub repository metadata analysis for components without version - [apiserver/#3315](https://github.com/DependencyTrack/dependency-track/pull/3315)
- Fix last modified timestamp for NVD mirroring via REST API not taking effect until restart - [apiserver/#3323](https://github.com/DependencyTrack/dependency-track/pull/3323)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.10.1](https://github.com/DependencyTrack/dependency-track/milestone/35?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@jadyndev](https://github.com/jadyndev)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.10.1/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 1d728ce1788e5db8b3a9308338a9e7e8ab5af12e                         |
| SHA-256   | e30731cd1915d3a1578cf5d8c8596d247fb11a82a3fe4c1ba2fb9fad01667aef |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.10.1/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | be32e1bc64d0b9b8019e340717d4ae3c12442ecd                         |
| SHA-256   | ffa0ab6dc9be894d0887ca3e10c4ffe3a333305d98de940413fcdbb05e2bcebd |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.10.1/bom.json)

<a href="cloudcannon:collections/_posts/2023-12-19-v4.10.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.10.0 <a href="#v4-10-0" class="anchor">#</a>

<span class="date">December 08, 2023</span> <span class="badge major">major</span>

Dependency-Track has historically relied on file-based data feeds to mirror contents of the National Vulnerability Database (NVD). These feeds are being [retired on December 15th 2023](https://nvd.nist.gov/General/News/change-timeline), although they [may be available up until December 18th](https://groups.google.com/a/list.nist.gov/g/nvd-news/c/a4bDL8nofOk).

As a consequence, this release includes support for mirroring the NVD via its REST API instead. This integration will be optional for Dependency-Track v4.10, but mandatory for later releases. Users are encouraged to enable REST API mirroring now, to ensure a smooth transition. Refer to the [NVD datasource documentation](/datasources/nvd/#mirroring-via-nvd-rest-api) to learn more.

**Features:**

- Add support for mirroring the NVD via its REST API - [apiserver/#3175](https://github.com/DependencyTrack/dependency-track/pull/3175)
  - Refer to the [NVD datasource documentation](/datasources/nvd/#mirroring-via-nvd-rest-api) for details
- Add retries with exponential backoff for NVD feed downloads - [apiserver/#3154](https://github.com/DependencyTrack/dependency-track/pull/3154)
- Add support for CycloneDX `metadata.supplier`, `metadata.manufacturer`, `metadata.authors`, and `component.supplier` - [apiserver/#3090](https://github.com/DependencyTrack/dependency-track/pull/3090), [apiserver/#3179](https://github.com/DependencyTrack/dependency-track/pull/3179)
- Add support for authenticating with public / non-internal repositories - [apiserver/#2876](https://github.com/DependencyTrack/dependency-track/pull/2876)
- Add support for fetching latest versions from GitHub - [apiserver/#3112](https://github.com/DependencyTrack/dependency-track/pull/3112)
  - Applicable to components with `pkg:github/<owner>/<repository>@<version>` package URLs
- Improve efficiency of search index operations - [apiserver/#3116](https://github.com/DependencyTrack/dependency-track/pull/3116)
- Add option to emit log for successfully published notifications, and improve logging around notifications in general - [apiserver/#3211](https://github.com/DependencyTrack/dependency-track/pull/3211)
- Use Java 21 JRE in container images - [apiserver/#3089](https://github.com/DependencyTrack/dependency-track/pull/3089)
- Tweak container health check to prevent `wget` zombie processes on slow hosts - [apiserver/#3245](https://github.com/DependencyTrack/dependency-track/pull/3245)
- Expose `alpine_event_processing_seconds` metric for monitoring of event processing durations
- Add average event processing duration to Grafana dashboard - [apiserver/#3173](https://github.com/DependencyTrack/dependency-track/pull/3173)
- Add guidance for `413 Content Too Large` errors upon BOM upload - [apiserver/#3167](https://github.com/DependencyTrack/dependency-track/pull/3167)
- Improve OIDC documentation - [apiserver/#3186](https://github.com/DependencyTrack/dependency-track/pull/3186)
- Add “Show in Dependency-Graph” button to component search results - [frontend/#572](https://github.com/DependencyTrack/frontend/pull/572)

**Fixes:**

- Fix false positives in CPE matching due to ambiguous *vendor*-*product* relations - [apiserver/#3209](https://github.com/DependencyTrack/dependency-track/pull/3209)
- Fix failure to delete policy violations when they have an audit trail - [apiserver/#3228](https://github.com/DependencyTrack/dependency-track/pull/3228)
- Fix teams not being assignable to alerts with custom email publishers - [apiserver/#3232](https://github.com/DependencyTrack/dependency-track/pull/3232)
- Fix inability to rebuild search indexes for more than one entity type at a time - [apiserver/#2987](https://github.com/DependencyTrack/dependency-track/issues/2987)
- Fix trailing comma in default Slack notification template - [apiserver/#3172](https://github.com/DependencyTrack/dependency-track/pull/3172)
- Fix NPE when affected node in OSV does not define a package - [apiserver/#3194](https://github.com/DependencyTrack/dependency-track/pull/3194)
- Fix NPE for BOM_PROCESSING_FAILED notifications when parsing of the BOM failed - [apiserver/#3198](https://github.com/DependencyTrack/dependency-track/pull/3198)
- Fix gradual performance degradation of portfolio vulnerability analysis - [apiserver/#3222](https://github.com/DependencyTrack/dependency-track/pull/3222)
- Fix erroneous warning log during VEX import - [apiserver/#3233](https://github.com/DependencyTrack/dependency-track/pull/3233)
- Fix `project.active` defaulting to `false` when creating projects via REST API - [apiserver/#3244](https://github.com/DependencyTrack/dependency-track/pull/3244)
- Fix OIDC login button moving before it can be clicked - [frontend/#616](https://github.com/DependencyTrack/frontend/pull/616)
- Fix input fields losing focus while editing alerts - [frontend/#619](https://github.com/DependencyTrack/frontend/pull/619)
- Fix switching between project versions being broken on tabs other than “Overview” - [frontend/#659](https://github.com/DependencyTrack/frontend/pull/659)
- Fix notification level not being modifiable for existing alerts - [frontend/#661](https://github.com/DependencyTrack/frontend/pull/661)

**Upgrade Notes:**

- The `CPE` table is no longer needed and will be dropped automatically upon upgrade - [apiserver/#3117](https://github.com/DependencyTrack/dependency-track/issues/3117)
- A warning will be logged when mirroring the NVD through its legacy data feeds
  - Refer to the [NVD datasource documentation](/datasources/nvd/#mirroring-via-nvd-rest-api) to learn how to switch to API-based mirroring
- As the Grafana dashboard is not managed by Dependency-Track, users wishing to update it will need to re-import it into their Grafana instance.

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.10.0](https://github.com/DependencyTrack/dependency-track/milestone/25?closed=1)
- [Frontend milestone 4.10.0](https://github.com/DependencyTrack/frontend/milestone/16?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@AbdelHajou](https://github.com/AbdelHajou), [@Nikemare](https://github.com/Nikemare), [@acdha](https://github.com/acdha), [@dimitri-rebrikov](https://github.com/dimitri-rebrikov), [@jadyndev](https://github.com/jadyndev), [@leec94](https://github.com/leec94), [@mehab](https://github.com/mehab), [@melba-lopez](https://github.com/melba-lopez), [@rbt-mm](https://github.com/rbt-mm), [@rkg-mm](https://github.com/rkg-mm), [@willienel](https://github.com/willienel), [@ybelMekk](https://github.com/ybelMekk)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.10.0/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | c308b1f6a2d73fc2bba9da2cc33bf7e3ec49e851                         |
| SHA-256   | d06f4550e16451ccb7843c36534172744934a7dc69e1d48e970a6eec24e49dc3 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.10.0/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | b94fb9cbaa91c4e332bcec266e10a0f325f12e22                         |
| SHA-256   | cf27db44e637b4bc551c16e659e81890f4c5d4f3b4ea9893ebf1717bff98b999 |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.10.0/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 217bcaab3a7da2ae2fab3103055f9503aef5db07                         |
| SHA-256   | 2f6f524c45afcc4a90128cab22a557bf41b88c716aaf0992eb6bb2239ce1469c |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.10.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.10.0/bom.json)

<a href="cloudcannon:collections/_posts/2023-12-08-v4.10.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.9.1 <a href="#v4-9-1" class="anchor">#</a>

<span class="date">October 30, 2023</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix failure to import BOMs in XML format when they contain multiple `metadata>tools` nodes - [apiserver/#3125](https://github.com/DependencyTrack/dependency-track/pull/3125)
- Fix failure to parse BOMs in XML format when the `metadata>component` nodes has `properties` - [apiserver/#3125](https://github.com/DependencyTrack/dependency-track/pull/3125)
- Fix failure to parse BOMs in XML format when the `component>hashes` node is empty - [apiserver/#3141](https://github.com/DependencyTrack/dependency-track/pull/3141)
- Fix impossible SQL query conditions causing DB indexes to be bypassed - [apiserver/#3126](https://github.com/DependencyTrack/dependency-track/pull/3126)
- Fix failure to start the application when using a logging config with JSON output - [apiserver/#3129](https://github.com/DependencyTrack/dependency-track/pull/3129)
- Fix NGINX failing to start when IPv6 is not available - [frontend/#623](https://github.com/DependencyTrack/frontend/pull/623)
- Fix NGINX entrypoint failing to detect mounted `config.json` under containerd - [frontend/#624](https://github.com/DependencyTrack/frontend/pull/624)
- Fix external references being cleared when updating a project via UI - [frontend/#628](https://github.com/DependencyTrack/frontend/pull/628)

For a complete list of changes, refer to the respective GitHub milestone:

- [API server milestone 4.9.1](https://github.com/DependencyTrack/dependency-track/milestone/34?closed=1)
- [Frontend milestone 4.9.1](https://github.com/DependencyTrack/frontend/milestone/17?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@muellerst-hg](https://github.com/muellerst-hg)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.9.1/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 99da5f705c3b0048ecf621e8c738a87147c693d9                         |
| SHA-256   | 5d925f08f85fe7f39231357c4a4c8057fd354e048b7c9407efb20af78033ecec |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.9.1/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 487801d69bffb2e8def5aad9aa55c34be8cddcb2                         |
| SHA-256   | 19ac4ede2932ff54c42e0466cdf7d5b410f7a44784562f237fc5b4b8891a8dc8 |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.9.1/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | d45d09a8ffb4c36f2fac78149d5f7cefe31a280b                         |
| SHA-256   | 6bc0bf9ecb8e7dc26eb3bfe9beecc41c5d11e5ccb902f19f0445aaa5860a1980 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.9.1/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.9.1/bom.json)

<a href="cloudcannon:collections/_posts/2023-10-30-v4.9.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.9.0 <a href="#v4-9-0" class="anchor">#</a>

<span class="date">October 16, 2023</span> <span class="badge major">major</span>

**Features:**

- Support import of CycloneDX v1.5 BOMs - [apiserver/#2850](https://github.com/DependencyTrack/dependency-track/issues/2850)
- Introduce `odt_` prefix for API keys to ease leak detection - [apiserver/#3047](https://github.com/DependencyTrack/dependency-track/pull/3047)
- Add support for SPDX license expressions - [apiserver/#2400](https://github.com/DependencyTrack/dependency-track/pull/2400)
  - Refer to [Policy Compliance](/usage/policy-compliance/#license-violation) for details on how license expressions behave in policies
- Update SPDX license list to v3.21 - [apiserver/#3006](https://github.com/DependencyTrack/dependency-track/pull/3006)
- Support resolving of custom licenses by name, instead of only by ID - [apiserver/#2769](https://github.com/DependencyTrack/dependency-track/pull/2769)
- Add version distance policy condition - [apiserver/#2537](https://github.com/DependencyTrack/dependency-track/pull/2537)
- Separate policy evaluation into its own background task - [apiserver/#2523](https://github.com/DependencyTrack/dependency-track/pull/2523)
- Allow policy violation state to be set via API - [apiserver/#2997](https://github.com/DependencyTrack/dependency-track/pull/2997)
- Add “Outdated only” and “Direct only” options for viewing components of a project - [apiserver/#2568](https://github.com/DependencyTrack/dependency-track/pull/2568)
- Update bundled CWE dictionary to v4.12 - [apiserver/#2877](https://github.com/DependencyTrack/dependency-track/pull/2877)
- Reduce number of API requests necessary to populate the dependency graph of a project - [apiserver/#2623](https://github.com/DependencyTrack/dependency-track/pull/2623)
- Include JDBC connectors for Google Cloud SQL - [apiserver/#2651](https://github.com/DependencyTrack/dependency-track/pull/2651)
- Update default Snyk API version to `2023-06-22` - [apiserver/#2911](https://github.com/DependencyTrack/dependency-track/pull/2911)
- Log warnings when analyses from VEX could not be applied - [apiserver/#2989](https://github.com/DependencyTrack/dependency-track/pull/2989)
- Update Docker base image latest Debian stable - [apiserver/#2904](https://github.com/DependencyTrack/dependency-track/pull/2904)
- Update temurin base image to `17.0.8.1_1` - [apiserver/#3069](https://github.com/DependencyTrack/dependency-track/pull/3069)
- Add extensive test suite for CPE matching logic - [apiserver/#2243](https://github.com/DependencyTrack/dependency-track/issues/2243)
- Update documentation for private vulnerability database - [apiserver/#2990](https://github.com/DependencyTrack/dependency-track/pull/2990)
- Add docs and example config for logging in JSON format - [apiserver/#2933](https://github.com/DependencyTrack/dependency-track/pull/2933)
- Add note about required plan for the Snyk integration to docs - [apiserver/#2899](https://github.com/DependencyTrack/dependency-track/pull/2899)
- Update example Grafana dashboard - [apiserver/#2788](https://github.com/DependencyTrack/dependency-track/pull/2780)
- Add Docker Compose files for simplified local testing - [apiserver/#2675](https://github.com/DependencyTrack/dependency-track/pull/2675)
- Add auto-provisioning of Grafana to Docker Compose development setup - [apiserver/#2879](https://github.com/DependencyTrack/dependency-track/pull/2879)
- Hide username and password fields on login view when OIDC is enabled - [frontend/#613](https://github.com/DependencyTrack/frontend/pull/613)
- Make NGINX listen on both IPv4 and IPv6 interfaces - [frontend/#427](https://github.com/DependencyTrack/frontend/pull/427)
- Display external references and description in project overview - [frontend/#485](https://github.com/DependencyTrack/frontend/pull/485)
- Use separate icons for current and out-of-date components to improve accessibility - [frontend/#311](https://github.com/DependencyTrack/frontend/issues/311)
- Propagate `searchText` query parameter to list views - [frontend/#563](https://github.com/DependencyTrack/frontend/pull/563)
- Raise baseline NodeJS version to 18 - [frontend/#470](https://github.com/DependencyTrack/frontend/issues/470)
- Upgrade CoreJS to 3.x - [frontend/#548](https://github.com/DependencyTrack/frontend/pull/548)

**Fixes:**

- Fix memory leak in policy evaluation - [apiserver/#2872](https://github.com/DependencyTrack/dependency-track/pull/2872)
- Fix memory leak in VEX upload processing - [apiserver/#2873](https://github.com/DependencyTrack/dependency-track/pull/2873)
- Fix VDR export erroneously containing non-vulnerable components - [apiserver/#2878](https://github.com/DependencyTrack/dependency-track/pull/2878)
- Fix VEX export erroneously containing dependency graph - [apiserver/#3067](https://github.com/DependencyTrack/dependency-track/pull/3067)
- Fix false positives in CPE matching when *version* attribute of a CVE’s CPE is `NA` - [apiserver/#1832](https://github.com/DependencyTrack/dependency-track/issues/1832)
- Fix false negatives in CPE matching when *part* or *vendor* attribute of a component’s CPE is `ANY` - [apiserver/#2988](https://github.com/DependencyTrack/dependency-track/issues/2988)
- Fix Uncaught internal server error when fetching components by hash if *Portfolio Access Control* is enabled - [apiserver/#2953](https://github.com/DependencyTrack/dependency-track/pull/2953)
- Fix *Affected Component* format for CPEs with version ranges - [apiserver/#2967](https://github.com/DependencyTrack/dependency-track/pull/2967)
- Fix missing duplicate check when cloning projects - [apiserver/#2966](https://github.com/DependencyTrack/dependency-track/pull/2966)
- Fix `NullPointerException` when checking for existence of projects without version - [apiserver/#3068](https://github.com/DependencyTrack/dependency-track/pull/3068)
- Fix module import issues when working on the code base with Eclipse - [apiserver/#2971](https://github.com/DependencyTrack/dependency-track/pull/2971)
- Fix version distance policy being evaluated despite not being configured - [apiserver/#2980](https://github.com/DependencyTrack/dependency-track/pull/2980)
- Fix `@JsonIgnore` having no effect on `transient` fields - [apiserver/#3051](https://github.com/DependencyTrack/dependency-track/pull/3051)
- Fix misleading docs about authentication and authorization enforcement being optional - [apiserver/#3047](https://github.com/DependencyTrack/dependency-track/pull/3047)
- Fix default Slack notification template producing invalid JSON for `PROJECT_AUDIT_CHANGE` notifications - [apiserver/#2838](https://github.com/DependencyTrack/dependency-track/issues/2838)
- Fix default Mattermost notification template producing invalid JSON for `NEW_VULNERABLE_DEPENDENCY` notifications - [apiserver/#3093](https://github.com/DependencyTrack/dependency-track/issues/3093)
- Fix number of project versions displayed in dropdown being limited to 10 - [frontend/#397](https://github.com/DependencyTrack/frontend/issues/397)
- Fix unauthenticated users not being redirected to login page - [frontend/#502](https://github.com/DependencyTrack/frontend/pull/502)
- Fix no permissions being defined for dashboard route - [frontend/#506](https://github.com/DependencyTrack/frontend/pull/506)
- Fix regression in Docker Compose file regarding application directory - [frontend/#494](https://github.com/DependencyTrack/frontend/pull/494)
- Fix external references dropdown rendering outside the screen - [frontend/#539](https://github.com/DependencyTrack/frontend/issues/539)
- Fix vulnerability aliases not being displayed in expanded rows of findings table - [frontend/#559](https://github.com/DependencyTrack/frontend/pull/559)
- Fix type error in external references dropdown - [frontend/#565](https://github.com/DependencyTrack/frontend/pull/565)
- Fix license expression input fields - [frontend/#580](https://github.com/DependencyTrack/frontend/pull/580)
- Fix wrong message being displayed when creating policies - [frontend/#610](https://github.com/DependencyTrack/frontend/pull/610)
- Fix file permissions of NGINX config file - [frontend/#611](https://github.com/DependencyTrack/frontend/pull/576)

**Upgrade Notes:**

- API keys generated after the upgrade will be prefixed with `odt_`. Existing API keys without this prefix will continue to work. The prefix is configurable via `alpine.api.key.prefix`, although customization is not recommended. Refer to [Configuration](/getting-started/configuration/) for details.
- Users ingesting SBOMs with CPE data may notice an uptick in vulnerabilities being identified by the internal analyzer. This is expected as a result of [apiserver/#2988](https://github.com/DependencyTrack/dependency-track/issues/2988) being fixed. If newly identified vulnerabilities turn out to be largely false positives, let the project team know by [reporting a defect](https://github.com/DependencyTrack/dependency-track/issues/new?assignees=&labels=defect%2Cin+triage&projects=&template=defect-report.yml).

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.9.0](https://github.com/DependencyTrack/dependency-track/milestone/24?closed=1)
- [Frontend milestone 4.9.0](https://github.com/DependencyTrack/frontend/milestone/14?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@HagarJNode](https://github.com/HagarJNode), [@Meroje](https://github.com/Meroje), [@Nikemare](https://github.com/Nikemare), [@RingoDev](https://github.com/RingoDev), [@Shawyeok](https://github.com/Shawyeok), [@dustin-decker](https://github.com/dustin-decker), [@hborchardt](https://github.com/hborchardt), [@heubeck](https://github.com/heubeck), [@mattmatician](https://github.com/mattmatician), [@melba-lopez](https://github.com/melba-lopez), [@muellerst-hg](https://github.com/muellerst-hg), [@nathan-mittelette](https://github.com/nathan-mittelette), [@sahibamittal](https://github.com/sahibamittal), [@sephiroth-j](https://github.com/sephiroth-j), [@syalioune](https://github.com/syalioune), [@takumakume](https://github.com/takumakume), [@valentijnscholten](https://github.com/valentijnscholten), [@walterdeboer](https://github.com/walterdeboer)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.9.0/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | cd4ec4f1ed075f37476f46da11451158d7460502                         |
| SHA-256   | 281f091107ef79d9b1e9361dc78608260b364eaa7dbbaeb29d4f7aef1a4bf67b |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.9.0/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 6f3a077219fb49a502a88fcbb40e05865a23f5c5                         |
| SHA-256   | 4ca0b061ed83fa0b34ede8158f3ec0e2a7380c2736731995cf330f809076951f |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.9.0/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 151f24f7b92e93dcf6600c4b8ee9e0ebd7b3560b                         |
| SHA-256   | 1ff2ace778d08529b42ee297fb6e3b0bbe8b2593b2b8686e8b3e3c9472663c2a |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.9.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.9.0/bom.json)

<a href="cloudcannon:collections/_posts/2023-10-16-v4.9.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.8.2 <a href="#v4-8-2" class="anchor">#</a>

<span class="date">May 17, 2023</span> <span class="badge patch">patch</span>

This release fixes a regression in the API server related to fetching of policy violations, which was introduced in 4.8.1.  
There are no changes for the frontend, the latest version of it remains 4.8.1.

**Fixes:**

- Fix policy violations endpoint erroneously returning violations for all projects when no `searchText` parameter is provided - [apiserver/#2766](https://github.com/DependencyTrack/dependency-track/issues/2766)
- Fix signals (e.g. `SIGTERM`) not being handled by the JVM process inside the container image, preventing graceful shutdown - [apiserver/#2750](https://github.com/DependencyTrack/dependency-track/pull/2750)

For a complete list of changes, refer to the respective GitHub milestone:

- [API server milestone 4.8.2](https://github.com/DependencyTrack/dependency-track/milestone/33?closed=1)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.2/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | bfc8758eb30ab90f4280cb37ea959964f74706b9                         |
| SHA-256   | 2b1d249d98f72b863deb4769665efc119a3ef8db195838decddce9a2a12f36b4 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.2/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 52bd8b0c0646d0759e30f5b1600f5fb17e4ede36                         |
| SHA-256   | 2f8171cd2a93f060110e0f7f5f1555a17db11de0a3cb0cb5b6068dfe3cd8e5e3 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.2/bom.json)

<a href="cloudcannon:collections/_posts/2023-05-17-v4.8.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.8.1 <a href="#v4-8-1" class="anchor">#</a>

<span class="date">May 16, 2023</span> <span class="badge patch">patch</span>

**Fixes:**

- Fix unrelated vulnerabilities being correlated during alias synchronization - [apiserver/#2194](https://github.com/DependencyTrack/dependency-track/issues/2194)
- Fix `NullPointerException` when email alert is configured with just teams as destination - [apiserver/#2698](https://github.com/DependencyTrack/dependency-track/issues/2698)
- Fix broken pagination in DefectDojo integration - [apiserver/#2707](https://github.com/DependencyTrack/dependency-track/issues/2707)
- Fix search function in policy violation tab not working - [apiserver/#2622](https://github.com/DependencyTrack/dependency-track/issues/2622)
- Fix `PATCH /api/v1/project` endpoint not updating external references - [apiserver/#2695](https://github.com/DependencyTrack/dependency-track/issues/2695)
- Fix `NullPointerException` in DefectDojo integration - [apiserver/#2628](https://github.com/DependencyTrack/dependency-track/issues/2628)
- Fix retrieval of OIDC JWK sets not respecting HTTP proxy settings - [apiserver/#2696](https://github.com/DependencyTrack/dependency-track/issues/2696)
- Lower log level for repository meta analyzer to `WARN` and include exception details - [apiserver/#2697](https://github.com/DependencyTrack/dependency-track/pull/2697)
- Add missing config docs for `alpine.oidc.client.id` - [apiserver/#2743](https://github.com/DependencyTrack/dependency-track/pull/2743)
- Fix not all vulnerability aliases being displayed in the UI - [frontend/#477](https://github.com/DependencyTrack/frontend/issues/477)
- Fix broken vulnerability alias links - [frontend/#486](https://github.com/DependencyTrack/frontend/issues/486)
- Fix broken project tag links on tabs other than “Overview” - [frontend/#483](https://github.com/DependencyTrack/frontend/issues/483)
- Fix broken project version links on tabs other than “Overview” - [frontend/#495](https://github.com/DependencyTrack/frontend/issues/495)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.8.1](https://github.com/DependencyTrack/dependency-track/milestone/32?closed=1)
- [Frontend milestone 4.8.1](https://github.com/DependencyTrack/frontend/milestone/15?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to fix defects:  
[@heubeck](https://github.com/heubeck), [@jakubrak](https://github.com/jakubrak), [@sahibamittal](https://github.com/sahibamittal), [@valentijnscholten](https://github.com/valentijnscholten)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.1/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 553d17a940220d79b686ce6b64d65c0854915f1b                         |
| SHA-256   | 56db674f5b467eac0a5b3fde99bc6285fd9135ad84e8fa0328ed6ace64fc723c |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.1/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | b2f0e053083ac672a9eaef19f7363ac854bdb91a                         |
| SHA-256   | e1bd03ea89b312c2125791a0d46ca99aa62365140a4f175d2f45cbb1d59a87a6 |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.8.1/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 01bc042e1f510e089b9db937852dbcde69eca603                         |
| SHA-256   | f946994c0f66647bd34c9e10997f2b62c08ab17ebbfe42edf149be12a47b2278 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.1/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.8.1/bom.json)

<a href="cloudcannon:collections/_posts/2023-05-16-v4.8.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.8.0 <a href="#v4-8-0" class="anchor">#</a>

<span class="date">April 18, 2023</span> <span class="badge major">major</span>

**Celebrating 10 years of OWASP Dependency-Track**

Dependency-Track is celebrating its 10th anniversary this year!  
Read the announcement from Steve Springett, creator of Dependency-Track, on [the OWASP blog](https://owasp.org/blog/2023/01/10/Celebrating-10-years-of-Dependency-Track.html).

**Highlights:**

- **Improved frontend UX**.
  - Navigating through the UI, switching tabs etc. now properly updates the URL in the browser. This makes it possible to share links to specific pages with others, and not lose context entirely when using the browser’s “go back” functionality.
  - Criteria for the component search is now encoded in the URL, which allows “deep-linking” to searches, making it easier to collaborate with colleagues.
  - The UI will now remember various user preferences, i.e. selected columns, numbers of search results per page, whether to show inactive projects, and much more.
  - The dependency graph now optionally displays indicator icons for outdated components.
- **Polished policy engine.** The policy engine received lots of love in this release, ranging from various bugfixes, to newly supported policy conditions.
- **Reduced resource footprint for vulnerability database mirroring**. Downloading and processing vulnerability data from the NVD, GitHub, and OSV has historically been a heavy task that could cause large spikes in JVM heap usage. Due to various improvements, mirroring will now be faster, and a lot more lightweight (see [apiserver/#2575](https://github.com/DependencyTrack/dependency-track/pull/2575) for comparisons).

**Features:**

- Reduce log level for some recurring tasks to `debug` - [apiserver/#2325](https://github.com/DependencyTrack/dependency-track/pull/2325)
- Reduce log level for Defect Dojo pagination advancement to `info` - [apiserver/#2338](https://github.com/DependencyTrack/dependency-track/issues/2338)
- Add User-Agent header to Snyk requests - [apiserver/#2396](https://github.com/DependencyTrack/dependency-track/pull/2396)
- Allow updating only the project’s parent via `PATCH`, without having to worry about any other project properties. - [apiserver/#2401](https://github.com/DependencyTrack/dependency-track/issues/2401)
- Include version of affected projects in Jira notification template - [apiserver/#2408](https://github.com/DependencyTrack/dependency-track/pull/2408)
- Add support for regular expressions in policy conditions - [apiserver/#2144](https://github.com/DependencyTrack/dependency-track/issues/2144)
- Show version status information on dependency graph nodes - [apiserver/#2273](https://github.com/DependencyTrack/dependency-track/pull/2273)
- Add support for component age in policy conditions - [apiserver/#772](https://github.com/DependencyTrack/dependency-track/issues/772)
- Skip superfluous component metrics calculation during OSS Index analysis - [apiserver/#2466](https://github.com/DependencyTrack/dependency-track/pull/2466)
- Handle deleted projects gracefully when processing uploaded BOMs - [apiserver/#2467](https://github.com/DependencyTrack/dependency-track/pull/2467)
- Include persistence framework in logging configuration - [apiserver/#2483](https://github.com/DependencyTrack/dependency-track/pull/2483)
- Drop dependency on Unirest library - [apiserver/#2350](https://github.com/DependencyTrack/dependency-track/issues/2350)
- Simplify and speed up vulnerability metrics calculation - [apiserver/#2481](https://github.com/DependencyTrack/dependency-track/pull/2481)
- Add developer documentation for skipping NVD mirroring - [apiserver/#2547](https://github.com/DependencyTrack/dependency-track/pull/2547)
- Execute NVD and EPSS mirroring on multi-threaded event service - [apiserver/#2526](https://github.com/DependencyTrack/dependency-track/pull/2526)
- Reduce memory footprint of vulnerability mirroring tasks - [apiserver/#2525](https://github.com/DependencyTrack/dependency-track/pull/2525)
- Allow for prevention of re-opening Defect Dojo findings via “do not reactivate” flag - [apiserver/#2424](https://github.com/DependencyTrack/dependency-track/issues/2424)
- Add support for vulnerability ID in policy conditions - [apiserver/#2557](https://github.com/DependencyTrack/dependency-track/issues/2557)
- Add support for matching of non-existent CPEs and Package URLs in policy conditions - [apiserver/#2587](https://github.com/DependencyTrack/dependency-track/issues/2587)
- Ingest remediation details from Snyk - [apiserver/#2571](https://github.com/DependencyTrack/dependency-track/issues/2571)
- Handle errors from repository metadata analyzers more gracefully - [apiserver/#2563](https://github.com/DependencyTrack/dependency-track/pull/2563)
- Add support for CPAN repositories - [apiserver/#639](https://github.com/DependencyTrack/dependency-track/issues/639)
- Allow inclusion of H2 web console for local development purposes - [apiserver/#2592](https://github.com/DependencyTrack/dependency-track/pull/2592)
- Add `BOM_PROCESSING_FAILED` notification - [apiserver/#2264](https://github.com/DependencyTrack/dependency-track/issues/2264)
- Ingest vulnerability publication time from Snyk - [apiserver/#2626](https://github.com/DependencyTrack/dependency-track/pull/2626)
- Add health endpoints - [apiserver/#1001](https://github.com/DependencyTrack/dependency-track/issues/1001)
- Include dependency graph in CycloneDX exports - [apiserver/#2616](https://github.com/DependencyTrack/dependency-track/issues/2616)
- Allow for vulnerability alias synchronization to be disabled for each source that supports it - [apiserver/#2670](https://github.com/DependencyTrack/dependency-track/pull/2670)
- Reduce heap usage during NVD mirroring - [apiserver/#2575](https://github.com/DependencyTrack/dependency-track/pull/2575)
- Support Jira authentication with personal access token - [apiserver/#2641](https://github.com/DependencyTrack/dependency-track/issues/2641)
- Allow parent project to be specified when upload a BOM - [apiserver/#2412](https://github.com/DependencyTrack/dependency-track/issues/2412)
- Update branding - [frontend/#387](https://github.com/DependencyTrack/frontend/pull/387)
- Add deep linking capability throughout the entire UI - [frontend/#391](https://github.com/DependencyTrack/frontend/pull/391)
- Remember UI user preferences (selected columns, page sizes, etc.) - [frontend/#348](https://github.com/DependencyTrack/frontend/issues/348)
- Add deep linking for component search - [frontend/#425](https://github.com/DependencyTrack/frontend/issues/425)
- Make removing a project parent relationship more convenient - [frontend/#424](https://github.com/DependencyTrack/frontend/pull/424)
- Display multiple aliases in a vertical rather than horizontal list - [frontend/#315](https://github.com/DependencyTrack/frontend/pull/315)
- Display aliases column in all vulnerability list views - [frontend/#315](https://github.com/DependencyTrack/frontend/pull/315)
- Add optional tags column to projects list view - [frontend/#319](https://github.com/DependencyTrack/frontend/pull/319)

**Fixes:**

- Fix unhandled exceptions when fetching repository metadata for Composer components that no longer exist - [apiserver/#2134](https://github.com/DependencyTrack/dependency-track/issues/2134)
- Fix invalid group name of Jira configuration properties - [apiserver/#2313](https://github.com/DependencyTrack/dependency-track/issues/2313)
- Fix duplicate policy violations caused by the “Package URL” policy condition - [apiserver/#1925](https://github.com/DependencyTrack/dependency-track/issues/1925)
- Fix policies with operator `ALL` behaving as if operator `ANY` was used - [apiserver/#2212](https://github.com/DependencyTrack/dependency-track/issues/2212)
- Fix 2023 NVD feeds not being fetched unless DT is restarted in new year - [apiserver/#2349](https://github.com/DependencyTrack/dependency-track/issues/2349)
- Fix VulnDB analysis results not being cached properly - [apiserver/#2436](https://github.com/DependencyTrack/dependency-track/pull/2436)
- Fix incomplete ingestion of dependency graph from hierarchically merged BOMs - [apiserver/#2411](https://github.com/DependencyTrack/dependency-track/issues/2411)
- Remove unnecessary `parentUuid` field from project model - [apiserver/#2439](https://github.com/DependencyTrack/dependency-track/issues/2439)
- Fix `AlreadyClosedException` when committing search indexes - [apiserver/#2379](https://github.com/DependencyTrack/dependency-track/issues/2379)
- Prevent OSV ecosystems being selected multiple times - [apiserver/#2473](https://github.com/DependencyTrack/dependency-track/issues/2473)
- Fix `NullPointerException` when computing enabled OSV ecosystems - [apiserver/#2527](https://github.com/DependencyTrack/dependency-track/pull/2527)
- Fix Finding Packaging Format (FPF) export containing internal technical fields - [apiserver/#2469](https://github.com/DependencyTrack/dependency-track/issues/2469)
- Fix ACL definitions not being cloned when cloning a project - [apiserver/#2493](https://github.com/DependencyTrack/dependency-track/issues/2493)
- Fix email notification for `PROJECT_AUDIT_CHANGE` missing some information - [apiserver/#2420](https://github.com/DependencyTrack/dependency-track/issues/2420)
- Fix not all tags being checked when evaluating “limit to” for policies - [apiserver/#2586](https://github.com/DependencyTrack/dependency-track/pull/2586)
- Fix internal server error when fetching all projects while ACL is enabled - [apiserver/#2583](https://github.com/DependencyTrack/dependency-track/issues/2583)
- Fix failures to import BOMs when component author fields exceed 255 characters - [apiserver/#2488](https://github.com/DependencyTrack/dependency-track/issues/2488)
- Fix incomplete implementation of [apiserver/#2313](https://github.com/DependencyTrack/dependency-track/issues/2313) - [apiserver/#2610](https://github.com/DependencyTrack/dependency-track/pull/2610)
- Fix dependency graph in UI being deleted after exporting project as CycloneDX - [apiserver/#2494](https://github.com/DependencyTrack/dependency-track/issues/2494)
- Fix project URL in email and Cisco WebEx notifications - [apiserver/#2631](https://github.com/DependencyTrack/dependency-track/pull/2631)
- Fix OSV overriding CVE data when NVD mirroring is also enabled - [apiserver/#2293](https://github.com/DependencyTrack/dependency-track/issues/2293)
- Fix redundant `POLICY_VIOLATION` notifications for existing violations - [apiserver/#2655](https://github.com/DependencyTrack/dependency-track/issues/2655)
- Fix email of LDAP users not being persisted - [apiserver/#2320](https://github.com/DependencyTrack/dependency-track/issues/2320)
- Fix email of OIDC users not being persisted - [apiserver/#2647](https://github.com/DependencyTrack/dependency-track/issues/2647)
- Fix VEX import not working for vulnerabilities from OSV, Snyk, and VulnDB - [apiserver/#2538](https://github.com/DependencyTrack/dependency-track/issues/2538)
- Fix missing project and component information in Microsoft Teams notifications - [apiserver/#2638](https://github.com/DependencyTrack/dependency-track/issues/2638)
- Fix API server not respecting HTTP proxy settings when communicating with OIDC Identity Provider - [apiserver/#1940](https://github.com/DependencyTrack/dependency-track/issues/1940)
- Fix potential *Invalid state. Transaction has already started* error during repository metadata analysis - [apiserver/#2678](https://github.com/DependencyTrack/dependency-track/pull/2678)
- Fix broken link to affected projects - [frontend/#417](https://github.com/DependencyTrack/frontend/pull/417)
- Fix duplicate PURL version in *Affected Components* tab of vulnerability details - [frontend/#454](https://github.com/DependencyTrack/frontend/pull/454)

**Upgrade Notes:**

- The `parentUuid` field has been removed from the project model and will thus no longer be returned by the REST API ([apiserver/#2439](https://github.com/DependencyTrack/dependency-track/issues/2439))
- Due to [apiserver/#2469](https://github.com/DependencyTrack/dependency-track/issues/2469), the File Packaging Format (FPF) version has been bumped to 1.2; Refer to [File Formats](/integrations/file-formats/) for details
- Synchronization of vulnerability aliases is now disabled by default for OSV and Snyk ([apiserver/#2670](https://github.com/DependencyTrack/dependency-track/pull/2670))

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.8.0](https://github.com/DependencyTrack/dependency-track/milestone/23?closed=1)
- [Frontend milestone 4.8.0](https://github.com/DependencyTrack/frontend/milestone/11?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.

Special thanks to everyone who contributed code to implement enhancements and fix defects:  
[@Ehoky](https://github.com/Ehoky), [@Gator8](https://github.com/Gator8), [@Hunroll](https://github.com/Hunroll), [@StephenKing](https://github.com/StephenKing), [@ch8matt](https://github.com/ch8matt), [@jkowalleck](https://github.com/jkowalleck), [@lme-nca](https://github.com/lme-nca), [@malice00](https://github.com/malice00), [@mcombuechen](https://github.com/mehab), [@msymons](https://github.com/msymons), [@mvandermade](https://github.com/mvandermade), [@rbt-mm](https://github.com/rbt-mm), [@roadSurfer](https://github.com/roadSurfer), [@s-spindler](https://github.com/s-spindler), [@sahibamittal](https://github.com/sahibamittal), [@syalioune](https://github.com/valentijnscholten), [@walterdeboer](https://github.com/walterdeboer), [@zgael](https://github.com/zgael)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.0/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 883754d3ed227a124976c3f9247345be48cc0561                         |
| SHA-256   | 0ab7e3a1d0cd308a9193a6bec7b561f3911d19052312a82e4a59607d4ff50fd0 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.0/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 979f02a5bf3ea5d8b0bba7d4e73a725de1920219                         |
| SHA-256   | af9f6d79e7828b4f744f9f82215486c0b5649abf6544d0374c945b2ab5d8b58a |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.8.0/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 852b8a16aa8d07ccd46b4bec38cda736c6271c42                         |
| SHA-256   | 40cffc6fcaafe4a23d2c347958c2e3f43e3c02afe3def238bfd4615684803537 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.8.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.8.0/bom.json)

<a href="cloudcannon:collections/_posts/2023-04-18-v4.8.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.7.1 <a href="#v4-7-1" class="anchor">#</a>

<span class="date">January 31, 2023</span> <span class="badge patch">patch</span>

**Fixes:**

- Resolved a defect that caused BOM uploads to fail when the BOM file contained a byte order mark - [apiserver/#2312](https://github.com/DependencyTrack/dependency-track/issues/2312)
- Resolved a defect that caused updating projects to fail when their `active` status was `null` - [apiserver/#2317](https://github.com/DependencyTrack/dependency-track/issues/2317)
- Resolved a defect that prevented teams from being deleted when portfolio access control was enabled - [apiserver/#2374](https://github.com/DependencyTrack/dependency-track/issues/2374)
- Move “Use Cases” documentation page to “Community Usage Examples” and clarify its purpose - [apiserver/#2403](https://github.com/DependencyTrack/dependency-track/pull/2403)
- Resolved a defect that caused vulnerability alias synchronization to fail for VulnDB - [apiserver/#2428](https://github.com/DependencyTrack/dependency-track/pull/2428)
- Fixed typo in monitoring documentation - [apiserver/#2430](https://github.com/DependencyTrack/dependency-track/pull/2430)
- Resolved a defect that caused component details to not be displayed in policy violations tab - [frontend/#373](https://github.com/DependencyTrack/frontend/issues/373)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.7.1](https://github.com/DependencyTrack/dependency-track/milestone/31?closed=1)
- [Frontend milestone 4.7.1](https://github.com/DependencyTrack/frontend/milestone/13?closed=1)

We thank all organizations and individuals who contributed to this release, from logging issues to taking part in discussions on GitHub & Slack to testing of fixes.  
Special thanks to everyone who contributed code to fix defects:

[@JoergBruenner](https://github.com/JoergBruenner), [@mehab](https://github.com/mehab), [@rbt-mm](https://github.com/rbt-mm), [@sergioasantiago](https://github.com/sergioasantiago), [@syalioune](https://github.com/syalioune)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.7.1/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | ef119b6f5fb422687e5152528bdb3e40e89c8733                         |
| SHA-256   | 7fbccad45c730226ab9df1ff51aaa2dba90b93cf22547bbe395d3f3b849c8371 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.7.1/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 94ca9179dad020c45adfdf0152b3f20081f7cf8b                         |
| SHA-256   | fe3fad9d43235df30880e547f838f65fe6365919dbc19107e4da349a5dce104f |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.7.1/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 1c1412a09a64d08ae44cb3c9c980bfbb2786ff53                         |
| SHA-256   | 95aed5a69c6e1db5ab05eaa57f511d5e16f92bafd67839be63f136ea78e11252 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.7.1/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.7.1/bom.json)

<a href="cloudcannon:collections/_posts/2023-01-31-v4.7.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.7.0 <a href="#v4-7-0" class="anchor">#</a>

<span class="date">December 16, 2022</span> <span class="badge major">major</span>

**Highlights:**

- **Hierarchical Project Relationships**. Projects can now be organized in hierarchies, using simple parent-child-relationships. Hierarchies are visualized in the UI, and allow projects to inherit various configurations from their parent, including notification rules and applicable policies.
- **Improved Dependency Graph**. The dependency graph can now be displayed in its entirety. Previously, the depth was limited to only three levels. Additionally, it’s now possible to navigate from a specific component (e.g. from the *Audit Vulnerabilities* tab) directly to the dependency graph. In doing so, Dependency-Track will show all paths in the graph leading up to this component, making it easy to understand how a given component is introduced to the project.
- **Snyk Integration (Beta)**. Dependency-Track can now make use of [Snyk](https://snyk.io/) to scan and continuously monitor components for vulnerabilities. This provides access to Snyk’s proprietary vulnerability database, maintained by their dedicated research team. The Snyk integration requires a paid subscription with REST API access.
- **Jira Integration**. It is now possible to publish notifications to Jira, making it easier to integrate events that require action to be taken into existing Jira workflows.

**Features:**

- Added support for hierarchical project relationships - [apiserver/#84](https://github.com/DependencyTrack/dependency-track/issues/84)
  - Added support for including project children in alert rule limitations - [apiserver/#2013](https://github.com/DependencyTrack/dependency-track/pull/2013)
  - Added support for including project children in policies - [apiserver/#2215](https://github.com/DependencyTrack/dependency-track/issues/2215)
- Added support for vulnerability analysis with Snyk - [apiserver/#365](https://github.com/DependencyTrack/dependency-track/issues/365)
- Added ability to focus on certain components in the dependency graph - [frontend/#336](https://github.com/DependencyTrack/frontend/pull/336)
- Added support for OWASP Risk Rating methodology - [apiserver/#1493](https://github.com/DependencyTrack/dependency-track/issues/1493)
- Added source attributions for affected component version ranges of mirrored vulnerabilities - [apiserver/#1815](https://github.com/DependencyTrack/dependency-track/issues/1815)
- Added support for limiting alerts to selection of teams - [apiserver/#1608](https://github.com/DependencyTrack/dependency-track/issues/1608)
- Added support for optional `EXTRA_JAVA_OPTIONS` environment variable in API server container - [apiserver/#2040](https://github.com/DependencyTrack/dependency-track/pull/2040)
- Improved component batching behavior and resilience of the OSS Index analyzer - [apiserver/#2023](https://github.com/DependencyTrack/dependency-track/issues/2023)
- Added option to include ACLs when cloning a project - [apiserver/#1534](https://github.com/DependencyTrack/dependency-track/issues/1534)
- Added *Reanalyze* button to the *Audit Vulnerabilities* tab - [apiserver/#2128](https://github.com/DependencyTrack/dependency-track/pull/2128)
- Added support for custom licenses - [apiserver/#2153](https://github.com/DependencyTrack/dependency-track/pull/2153)
- Added Jira notification publisher - [apiserver/#2118](https://github.com/DependencyTrack/dependency-track/issues/2118)
- Added documentation for setting up OIDC with Google - [apiserver/#2185](https://github.com/DependencyTrack/dependency-track/pull/2185)
- Added support for license URLs - [apiserver/#1977](https://github.com/DependencyTrack/dependency-track/pull/1977)
- Allow bypassing of system requirements check - [apiserver/#2197](https://github.com/DependencyTrack/dependency-track/issues/2197)
- Added Swagger types for BOM operations of the REST API - [apiserver/#2230](https://github.com/DependencyTrack/dependency-track/pull/2230)
- Include commenter in `PROJECT_AUDIT_CHANGE` email notifications - [apiserver/#2227](https://github.com/DependencyTrack/dependency-track/pull/2227)
- Added ability to check for unresolved licenses in policy conditions - [apiserver/#1518](https://github.com/DependencyTrack/dependency-track/issues/1518)
- Added proper caching for repository meta analysis - [apiserver/#1943](https://github.com/DependencyTrack/dependency-track/issues/1943)
- Added health check, corruption check, and ability to manually trigger rebuilds for search indexes - [apiserver/#2200](https://github.com/DependencyTrack/dependency-track/pull/2200)
- Added support for project metadata, including ingestion from uploaded BOMs - [apiserver/#1200](https://github.com/DependencyTrack/dependency-track/issues/1200)
- Added use case examples to documentation - [apiserver/#2211](https://github.com/DependencyTrack/dependency-track/pull/2211)
- Added Azure DevOps extension to community integrations - [apiserver/#2258](https://github.com/DependencyTrack/dependency-track/pull/2258)
- Added total heap size and CPU usage lines to sample Grafana dashboard - [apiserver/#2256](https://github.com/DependencyTrack/dependency-track/pull/2256)
- Do not create temporary database connection pools when executing upgrades - [apiserver/#2232](https://github.com/DependencyTrack/dependency-track/pull/2232)
- Added persistence metrics to sample Grafana dashboard - [apiserver/#2245](https://github.com/DependencyTrack/dependency-track/issues/2245)
- Added ability to search for components by identity within a specific project - [apiserver/#2228](https://github.com/DependencyTrack/dependency-track/issues/2228)
- Treat tag names as case-insensitive - [apiserver/#1717](https://github.com/DependencyTrack/dependency-track/issues/1717)
- Added notification for newly created projects - [apiserver/#2173](https://github.com/DependencyTrack/dependency-track/issues/2173)
- Added ability to [configure database connection pools](/getting-started/database-support/#connection-pooling) separately - [apiserver/#2238](https://github.com/DependencyTrack/dependency-track/pull/2238)
- Added ability to [configure the secret key path](/getting-started/configuration/#secret-key) - [apiserver/#2238](https://github.com/DependencyTrack/dependency-track/pull/2238)
- Include services in the BOM distributed for the API server - [apiserver/#2175](https://github.com/DependencyTrack/dependency-track/pull/2175)
- Added support for Vulnerability Disclosure Report (VDR) exports - [apiserver/#1800](https://github.com/DependencyTrack/dependency-track/issues/1800)
- Make projects clickable in ACL configuration view - [frontend/#320](https://github.com/DependencyTrack/frontend/pull/320)
- Display component version status in *Audit Vulnerabilities* and *Exploit Predictions* tab - [frontend/#356](https://github.com/DependencyTrack/frontend/issues/356)
- Display last BOM import timestamp in project overview - [frontend/#147](https://github.com/DependencyTrack/frontend/issues/147)

**Fixes:**

- Fix dependency graph only showing 3 levels of transitive relationships - [frontend/#85](https://github.com/DependencyTrack/frontend/issues/85)
- Fix alert limitations to not be applied for `POLICY_VIOLATION` and `PROJECT_AUDIT_CHANGE` notifications - [apiserver/#975](https://github.com/DependencyTrack/dependency-track/issues/975)
- Fix NVD mirroring to fail when using CIFS volumes - [apiserver/#2048](https://github.com/DependencyTrack/dependency-track/issues/2048)
- When determining the latest version of a Maven component, use the `release` version advertised by the repository, instead of `latest` - [apiserver/#2075](https://github.com/DependencyTrack/dependency-track/issues/2075)
- Fix incorrect project URL in email notifications - [apiserver/#2172](https://github.com/DependencyTrack/dependency-track/pull/2172)
- Fix missing project information in `NEW_VULNERABLE_DEPENDENCY` notification emails - [apiserver/#2139](https://github.com/DependencyTrack/dependency-track/issues/2139)
- Fix search indexes not being (re-) built - [apiserver/#2104](https://github.com/DependencyTrack/dependency-track/issues/2104)
- Fix *Component* in *Affected Components* tab of vulnerability details showing `undefined` in some cases - [apiserver/#2231](https://github.com/DependencyTrack/dependency-track/issues/2231)
- Fix incorrect datasource for `instance` dropdown in sample Grafana dashboard - [apiserver/#2068](https://github.com/DependencyTrack/dependency-track/pull/2068)
- Fix broke heap usage gauge in sample Grafana dashboard - [apiserver/#2073](https://github.com/DependencyTrack/dependency-track/pull/2073)
- Fix CPEs not matching on identical versions - [apiserver/#2240](https://github.com/DependencyTrack/dependency-track/pull/2240)
- Fix inability to delete teams that are part of one or more ACL - [apiserver/#1532](https://github.com/DependencyTrack/dependency-track/issues/1532)

**Upgrade Notes:**

- Creating new or searching for existing tags will now treat tag names as case-insensitive ([apiserver/#1717](https://github.com/DependencyTrack/dependency-track/issues/1717)). Users relying on tags being treated as case-sensitive (e.g. `critical` and `CRITICAL` being treated as different) should review their use of tags prior to upgrading.
- Names of the HikariCP connection pools in the exposed Prometheus metrics have changed from `HikariPool-3` and `HikariPool-4` to `transactional` and `non-transactional` ([apiserver/#2238](https://github.com/DependencyTrack/dependency-track/pull/2238)). Users monitoring those pools are advised to update their monitoring configuration accordingly (e.g. Grafana dashboards).
- Distribution of the API server SBOM in XML format has been dropped ([apiserver/#2175](https://github.com/DependencyTrack/dependency-track/pull/2175)). Users consuming the API server BOM in XML format should migrate to consuming the JSON-formatted BOM instead.

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.7.0](https://github.com/DependencyTrack/dependency-track/milestone/22?closed=1)
- [Frontend milestone 4.7.0](https://github.com/DependencyTrack/frontend/milestone/10?closed=1)

We thank all organizations and individuals who contributed to this release.  
Special thanks to everyone who contributed code to implement enhancements and fix defects:

[@AZenker](https://github.com/AZenker), [@JoergBruenner](https://github.com/JoergBruenner), [@KramNamez](https://github.com/KramNamez), [@Mvld3r](https://github.com/Mvld3r), [@Zargath](https://github.com/Zargath), [@awegg](https://github.com/awegg), [@ch8matt](https://github.com/ch8matt), [@japurva1502](https://github.com/japurva1502), [@kekkegenkai](https://github.com/kekkegenkai), [@mehab](https://github.com/mehab), [@nathan-mittelette](https://github.com/nathan-mittelette), [@omerlh](https://github.com/omerlh), [@rbt-mm](https://github.com/rbt-mm), [@ribbybibby](https://github.com/ribbybibby), [@s-spindler](https://github.com/s-spindler), [@sahibamittal](https://github.com/sahibamittal), [@syalioune](https://github.com/syalioune), [@valentijnscholten](https://github.com/valentijnscholten)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.7.0/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 99f1a012a983b8256d9346e64d3dd27e92d1c808                         |
| SHA-256   | 373e8efa1a8995193b7c068ea34974040627553647905d38e1dce053333eeb10 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.7.0/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | c7faee42162e1712377fbd8a03dfd9e3ef251a23                         |
| SHA-256   | 631807c24fd76c0f44d4494a44147e0414ab471ac1e12fe4ebff054f363a8f0f |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.7.0/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 8696218e07d438896f236f691f2ca658faf0377a                         |
| SHA-256   | 23cc72eea3361edeaff84efe0a1a0327e47367419466307867103bac2b14ad75 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.7.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.7.0/bom.json)

<a href="cloudcannon:collections/_posts/2022-12-16-v4.7.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.6.3 <a href="#v4-6-3" class="anchor">#</a>

<span class="date">November 18, 2022</span> <span class="badge patch">patch</span>

This release fixes a defect in the caching of vulnerability analysis results from external sources.  
There are no changes for the frontend, the latest version of it remains 4.6.1.

**Fixes:**

- Resolved a defect that caused the [component analysis cache](/analysis-types/known-vulnerabilities/#analysis-result-cache) validity period to be too short - [\#2115](https://github.com/DependencyTrack/dependency-track/issues/2115)

**Upgrade Notes:**

- The value of the `scanner.analysis.cache.validity.period` configuration property will be reset to 12 hours during the automated upgrade. No manual actions are required.

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.6.3](https://github.com/DependencyTrack/dependency-track/milestone/30?closed=1)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.3/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 68b806410c2e68fe8c586b93044f29a648f96466                         |
| SHA-256   | d9b5337419addee26658da8e421f0286aaa92160b8f6f85caca83aa1a328611f |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.3/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | ac2a60bc8fedad714fa55c2aaad44533fa2086d7                         |
| SHA-256   | 1229681b5d1dc399ec662946969f7ef225bc7e6381861d8eb35e31d431b25714 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.3/bom.json)

<a href="cloudcannon:collections/_posts/2022-11-18-v4.6.3.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.6.2 <a href="#v4-6-2" class="anchor">#</a>

<span class="date">October 24, 2022</span> <span class="badge patch">patch</span>

This release fixes a cross-site scripting (XSS) vulnerability in the frontend. The bundled distribution has been updated to include the fixed frontend version. There are no changes for the API server distribution.

**Fixes:**

- Resolved a defect that caused HTML tags in vulnerability descriptions to be rendered on the vulnerability details page - [\#300](https://github.com/DependencyTrack/frontend/pull/300)

**Security:**

- Fixed a cross-site scripting vulnerability in the vulnerability details page - [GHSA-c33w-pm52-mqvf](https://github.com/DependencyTrack/frontend/security/advisories/GHSA-c33w-pm52-mqvf)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.6.2](https://github.com/DependencyTrack/dependency-track/milestone/28?closed=1)
- [Frontend milestone 4.6.1](https://github.com/DependencyTrack/frontend/milestone/12?closed=1)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.2/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 313b2ee9bd957f8bd2b0baba524044197501b2a9                         |
| SHA-256   | 7ee92f572cebe6d8d8f9e37ab6067e5849c83c56c98b38a21418557260efbfdc |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.2/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | e009cc9345ae5bdb321c651df769a6d02dfc5a67                         |
| SHA-256   | 0e67de28a99aec1d2e3c4592b42f04e86084129f58f3d338b572fdc5b7064899 |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.6.2/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 67843f34745d4983da001ca158c0fa6aba814427                         |
| SHA-256   | f0cb536946117068f26845eee89975e4d7feac0b7c806bae505172e85bfadf76 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.2/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.6.1/bom.json)

<a href="cloudcannon:collections/_posts/2022-10-24-v4.6.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.6.1 <a href="#v4-6-1" class="anchor">#</a>

<span class="date">October 13, 2022</span> <span class="badge patch">patch</span>

**Fixes:**

- Resolved defect that caused policy name and violation state to not be displayed in the violations audit tab - [\#2043](https://github.com/DependencyTrack/dependency-track/issues/2043)

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.6.1](https://github.com/DependencyTrack/dependency-track/milestone/28?closed=1)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.1/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | f3c8e2007f2795b12f438b6b9318c4d5c448fa0b                         |
| SHA-256   | e293756b5e27d6c3213dfbeead946bf220d278d418c817c74a81fda395764977 |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.1/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | da0d27cd635de292bcae112c816b97c1b1d50107                         |
| SHA-256   | 0a8530aab97bedbc33575a5ff18677eef1bcc555bb038150229bc5147c7ef522 |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.1/bom.json)

<a href="cloudcannon:collections/_posts/2022-10-13-v4.6.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.6.0 <a href="#v4-6-0" class="anchor">#</a>

<span class="date">October 11, 2022</span> <span class="badge major">major</span>

**Highlights:**

- **Vulnerability Aliases**. By ingesting data from multiple sources of vulnerability intelligence, there will be cases where different advisories describe the same vulnerability. For example, [CVE-2022-31197](https://nvd.nist.gov/vuln/detail/CVE-2022-31197) and [GHSA-r38f-c4h4-hqq2](https://github.com/pgjdbc/pgjdbc/security/advisories/GHSA-r38f-c4h4-hqq2) describe the same defect, yet their descriptions and risk ratings differ. Dependency-Track 4.6 now recognizes when multiple advisories alias each other, and includes this information in notifications and REST API responses. Aliases will additionally be considered when calculating portfolio metrics, so that duplicate vulnerabilities do not skyrocket the risk scoring. Further improvements to aliases will be coming in future releases.
- **OSV Integration (Beta)**. Dependency-Track now optionally mirrors vulnerability intelligence data from the Open Source Vulnerabilities database ([OSV](https://osv.dev/)). OSV normalizes and enriches data from multiple other vulnerability databases. Mirroring can be limited to a configurable selection of ecosystems.
- **New Policy Conditions**.
  - Using the tag condition, policies can be restricted to projects with certain properties or priorities (e.g. *high-risk*, *internet-facing*, etc.)
  - Using the CWE condition, policies can assist in prioritizing findings of certain weaknesses
  - Using the component hash condition, policies can be used to flag usage of malicious or tainted packages
- **Performance**. Various improvements, most prominently regarding metrics updates. Organizations, especially those with large portfolios of multiple thousands of projects, will see a drastic reduction in runtime and resource usage.
- **Observability**. By exposition of system metrics via the Prometheus text-based format, operators can now monitor their instances using Prometheus, Grafana, or other compatible observability stacks. Metrics exposition is optional and must be enabled, refer to the [monitoring](/getting-started/monitoring/) documentation for details.
- **Customization**. Users with advanced customization needs can now create and modify notification templates, as well as specify custom intervals for recurring tasks. Refer to the [notifications](/integrations/notifications/) and [recurring tasks](/getting-started/recurring-tasks/) documentation for details.
- **Authentication for Internal Repositories**. Dependency-Track can now authenticate with artifact repositories like Nexus Repository Manager or Artifactory to fetch information about internal artifacts.

**Features:**

- Added support for authentication with internal package repositories - [\#881](https://github.com/DependencyTrack/dependency-track/issues/881)
- Added support for configuration of [recurring tasks](/getting-started/recurring-tasks/) intervals - [\#1542](https://github.com/DependencyTrack/dependency-track/issues/1542)
- Added support for policy violation badges - [\#1690](https://github.com/DependencyTrack/dependency-track/issues/1690)
- Added support for disabling alerts - [\#1173](https://github.com/DependencyTrack/dependency-track/issues/1173)
- Added support for CWEs in policy conditions - [\#1768](https://github.com/DependencyTrack/dependency-track/issues/1768)
- Added support for component hashes in policy conditions - [\#1775](https://github.com/DependencyTrack/dependency-track/issues/1775)
- Added support for tags in policy conditions - [\#1565](https://github.com/DependencyTrack/dependency-track/issues/1565)
- Added support for fuzzy CPE matching - [\#1799](https://github.com/DependencyTrack/dependency-track/pull/1799)
- Added support for notification publishing via Mattermost - [\#1702](https://github.com/DependencyTrack/dependency-track/pull/1702)
- Added support for reimporting findings to an existing DefectDojo test instead of creating a new test upon each upload - [\#1622](https://github.com/DependencyTrack/dependency-track/issues/1622)
- Added support for ingesting and displaying component author information - [\#1726](https://github.com/DependencyTrack/dependency-track/issues/1726)
- Added support for vulnerability aliases - [\#1912](https://github.com/DependencyTrack/dependency-track/pull/1912)
- Added support for custom notification templates - [\#275](https://github.com/DependencyTrack/dependency-track/issues/275)
- Added experimental [OSV integration](/datasources/osv/) - [\#931](https://github.com/DependencyTrack/dependency-track/issues/931)
- Added support for Prometheus [metrics exposition](/getting-started/monitoring/) - [\#1796](https://github.com/DependencyTrack/dependency-track/pull/1796)
- Refactored metrics update functionality to be faster and more efficient - [\#1704](https://github.com/DependencyTrack/dependency-track/pull/1704)
- Upgraded to Java 17 - [\#1804](https://github.com/DependencyTrack/dependency-track/pull/1804)
- Removed source maps from frontend production build - [\#192](https://github.com/DependencyTrack/frontend/issues/192)
- Added name of the authenticated user to the profile menu in the UI - [\#167](https://github.com/DependencyTrack/frontend/issues/167)
- Added support for performing cross-site frontend requests with cookies - [\#156](https://github.com/DependencyTrack/frontend/issues/156)
- Added columns for CVSS and EPSS to the component vulnerabilities view - [\#1948](https://github.com/DependencyTrack/dependency-track/issues/1948)
- Added listing of affected projects to email notification templates - [\#2005](https://github.com/DependencyTrack/dependency-track/issues/2005)

**Fixes:**

- Resolved defect that made it impossible to delete a project when assigned to a policy - [\#1852](https://github.com/DependencyTrack/dependency-track/issues/1852)
- Resolved defect related non-thread-safe usage of the internal Lucene search index - [\#1791](https://github.com/DependencyTrack/dependency-track/issues/1797)
- Resolved defect that caused the subject of email notifications saying `null` in certain situations - [\#1818](https://github.com/DependencyTrack/dependency-track/issues/1818)
- Resolved defect that caused the VulnDB analyzer failing to mark components as vulnerable - [\#1780](https://github.com/DependencyTrack/dependency-track/issues/1780)
- Resolved defect where the `affectedComponents` field of vulnerabilities would not be populated - [\#1766](https://github.com/DependencyTrack/dependency-track/issues/1766)
- Resolved defect that caused vulnerability details taking too long to load - [\#1765](https://github.com/DependencyTrack/dependency-track/issues/1765)
- Resolved defect that caused an internal server error when uploading a VEX document via HTTP `PUT` - [\#1836](https://github.com/DependencyTrack/dependency-track/issues/1836)
- Resolved defect that caused an internal server error when creating a vulnerability without CWEs - [\#1664](https://github.com/DependencyTrack/dependency-track/issues/1664)
- Resolved defect that caused an internal server error when submitting analysis details with more than 255 characters - [\#1661](https://github.com/DependencyTrack/dependency-track/issues/1661)
- Resolved defect that caused an internal server error when importing a SaaSBOM - [\#1790](https://github.com/DependencyTrack/dependency-track/issues/1790)
- Resolved defect that caused NVD mirroring notifications not working correctly - [\#1429](https://github.com/DependencyTrack/dependency-track/issues/1429)
- Resolved defect that caused VEX import not ingesting analyses for internal vulnerabilities - [\#1692](https://github.com/DependencyTrack/dependency-track/issues/1765)
- Resolved defect that caused excessive memory utilization when identifying internal components - [\#1947](https://github.com/DependencyTrack/dependency-track/issues/1947)
- Resolved defect that caused wrong project tags to be displayed after switching versions - [\#188](https://github.com/DependencyTrack/frontend/issues/188)
- Resolved defect that caused component licenses to not be displayed on some occasions - [\#223](https://github.com/DependencyTrack/frontend/issues/223)
- Resolved defect that caused horizontal scroll bars to be displayed unnecessarily in the UI - [\#248](https://github.com/DependencyTrack/frontend/issues/248)
- Resolved defect that made it impossible to provide component hashes in uppercase - [\#1174](https://github.com/DependencyTrack/dependency-track/issues/1174)
- Resolved defect that prevented vulnerabilities in PHP components to be identified based on GitHub Advisories data - [\#1998](https://github.com/DependencyTrack/dependency-track/issues/1998)
- Resolved defect that caused a `NumberFormatException` to be thrown when resolving CWEs for findings - [\#2029](https://github.com/DependencyTrack/dependency-track/issues/2029)
- Resolved projects search filter not working when viewing projects by tag - [\#405](https://github.com/DependencyTrack/dependency-track/issues/405)
- Resolved notifications with group `NEW_VULNERABLE_DEPENDENCY` not working at all - [\#1611](https://github.com/DependencyTrack/dependency-track/issues/1611)
- Resolved multiple minor UI defects related to API key management - [\#240](https://github.com/DependencyTrack/frontend/pull/240)
- Resolved UI defect that caused vulnerability details not being displayed when only the CVSS vector, but not the scores were returned by the API - [\#239](https://github.com/DependencyTrack/frontend/pull/239)
- Resolved UI defect that caused an incorrect tooltip being displayed for the email field in the email configuration test modal - [\#161](https://github.com/DependencyTrack/frontend/issues/161)
- Resolved UI defect that caused the policy management view to not be updated when restricting a policy to a project - [\#169](https://github.com/DependencyTrack/frontend/issues/169)
- Resolved UI defect that caused input fields losing focus after saving - [\#98](https://github.com/DependencyTrack/frontend/issues/98)

**Security:**

- Fixed a defect that could cause API keys to be logged in clear text when handling API requests using keys with insufficient permissions - [GHSA-gh7v-4hxp-gqp4](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-gh7v-4hxp-gqp4)

**Upgrade Notes:**

- The new baseline Java version is 17 ([\#1804](https://github.com/DependencyTrack/dependency-track/pull/1804))
  - Java versions later than 17 may work as well, but haven’t been tested
  - Users deploying DT via [executable WAR](/getting-started/deploy-exewar/) will need to upgrade Java accordingly
  - Users deploying DT via [containers](/getting-started/deploy-docker/) don’t need to do anything
- The embedded H2 database has been upgraded to major version 2
  - Manual upgrade steps are required, refer to the [H2 v2 migration guide](/getting-started/database-support/#migrating-to-h2-v2)
  - **Without the manual migration, Dependency-Track 4.6 will not work with H2 databases created by earlier versions**
  - **Reminder**: H2 is not, and never has been, supported for production usage
- With [\#1429](https://github.com/DependencyTrack/dependency-track/issues/1429), handling of notification levels has changed
  - Previously, an alert with level `ERROR` would trigger on notifications with levels `ERROR`, `WARNING`, and `INFORMATIONAL`
  - Now, an alert with level `ERROR` will only trigger on notifications with level `ERROR`
  - An alert with level `WARNING` will trigger on notifications with level `WARNING` and `ERROR` etc.
  - The new behavior is similar to how structured logging libraries work
  - This change primarily affects notifications of the `SYSTEM` scope, which are used to report statuses of various tasks, e.g. `DATASOURCE_MIRRORING`
  - Notifications in the `PORTFOLIO` scope (e.g. `NEW_VULNERABILITY`) all have the `INFORMATIONAL` level
  - Users who configured alerts with scope `PORTFOLIO` and level `ERROR` should change the level to `INFORMATIONAL` after the upgrade

For a complete list of changes, refer to the respective GitHub milestones:

- [API server milestone 4.6](https://github.com/DependencyTrack/dependency-track/milestone/21?closed=1)
- [Frontend milestone 4.6](https://github.com/DependencyTrack/frontend/milestone/8?closed=1)

We thank all organizations and individuals who contributed to this release.  
Special thanks to everyone who contributed code to implement enhancements and fix defects:

*@AbdelHajou, @awegg, @dGuerr, @k3rnelpan1c-dev, @maaheeb, @officerNordberg, @rbt-mm, @rkg-mm, @s-spindler, @sahibamittal, @stephan-strate, @syalioune, @tmehnert, @yangsec888*

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.0/dependency-track-apiserver.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | e40fb14764fb5eb9fcd654472434c3701c44f208                         |
| SHA-256   | 29d422816b593ddef89b07e9bc1c72a5cfb141eaea4a1d59615309089bab03ea |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.0/dependency-track-bundled.jar)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 9e1b283c442e1bfb2c5c4ea23b1a1590cf7afc5d                         |
| SHA-256   | 1e6ba17e6dc1f6422826a020ece5ec6ae2bef1aa9ae563f57653ed6bc0944f14 |

###### [frontend-dist.zip](https://github.com/DependencyTrack/frontend/releases/download/4.6.0/frontend-dist.zip)

| Algorithm | Checksum                                                         |
|:----------|:-----------------------------------------------------------------|
| SHA-1     | 0f8967a4f777d33fd285d7fe8786f08690ffedd9                         |
| SHA-256   | 14791981d23850b72e39cee8c6378c6e25de0f8f5ee46b5c244c28bd6262db9a |

###### Software Bill of Materials (SBOM)

- API Server: [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.6.0/bom.json)
- Frontend: [bom.json](https://github.com/DependencyTrack/frontend/releases/download/4.6.0/bom.json)

<a href="cloudcannon:collections/_posts/2022-10-11-v4.6.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.5.0 <a href="#v4-5-0" class="anchor">#</a>

<span class="date">May 18, 2022</span> <span class="badge major">major</span>

**Features:**

- Added support for consuming [VEX](https://cyclonedx.org/capabilities/vex/) - [\#1387](https://github.com/DependencyTrack/dependency-track/issues/1387)
- Added support for management of internal vulnerabilities - [\#96](https://github.com/DependencyTrack/dependency-track/issues/96)
  - Added new `VULNERABILITY_MANAGEMENT` permission, which is required to create, edit and delete internal vulnerabilities
- Added support for [EPSS](https://www.first.org/epss/model) - [\#1178](https://github.com/DependencyTrack/dependency-track/issues/1178)
- Added support for notifications on policy violations - [\#1396](https://github.com/DependencyTrack/dependency-track/issues/1396)
- Added support for fetching projects by classifier - [\#1185](https://github.com/DependencyTrack/dependency-track/issues/1185)
- Added support for multiple CWEs being assigned to vulnerabilities - [\#1467](https://github.com/DependencyTrack/dependency-track/issues/1467)
  - API, FPF and notifications now include an additional JSON array field `cwes`
  - The `cwe` field is still supported, but deprecated, and will be removed in a later release
- Added new `VIEW_POLICY_VIOLATION` permission that grants read-only access to policy violations and the audit trail - [\#1433](https://github.com/DependencyTrack/dependency-track/issues/1433)
- Added ability to modify specific project fields via `PATCH` requests - [\#1586](https://github.com/DependencyTrack/dependency-track/pull/1586)
- Grant access to the team that created a project via BOM upload when portfolio ACL is enabled - [\#1529](https://github.com/DependencyTrack/dependency-track/pull/1529)
- Improved resource efficiency of portfolio metrics updates - [\#1481](https://github.com/DependencyTrack/dependency-track/pull/1481)
- Reversed order of NVD feed downloads so that latest vulnerabilities are loaded first - [\#1557](https://github.com/DependencyTrack/dependency-track/pull/1557)
- Included policy violation analysis in daily portfolio analysis - [\#1492](https://github.com/DependencyTrack/dependency-track/pull/1492)
- Added OIDC setup example for Azure AD - [\#1564](https://github.com/DependencyTrack/dependency-track/pull/1564)

**Fixes:**

- Resolved defect where the `VULNERABILITY_ANALYSIS` permission was required to see policy violations - [\#126](https://github.com/DependencyTrack/frontend/issues/126)
- Resolved defect where audit trail entries were generated for `Justification` and `Response`, even though they didn’t actually change - [\#1566](https://github.com/DependencyTrack/dependency-track/pull/1566)
- Resolved defect where vulnerabilities from GitHub Advisories could not be matched with Go modules - [\#1574](https://github.com/DependencyTrack/dependency-track/issues/1574)
- Resolved defect where filtering projects by tag would ignore the active / inactive filter - [\#1501](https://github.com/DependencyTrack/dependency-track/issues/1501)
- Resolved defect where NVD mirroring could not be enabled - [\#1576](https://github.com/DependencyTrack/dependency-track/issues/1576)
- Updated URL of the Atlassian package repository - [\#1568](https://github.com/DependencyTrack/dependency-track/pull/1568)
- Resolved multiple defects in calculation of portfolio metrics - [\#1530](https://github.com/DependencyTrack/dependency-track/pull/1530)
- Resolved defect where incomplete NVD data could be mirrored - [\#1480](https://github.com/DependencyTrack/dependency-track/pull/1480)
- Resolved defect where portfolio changes wouldn’t immediately be reflected in results of the search API - [\#1605](https://github.com/DependencyTrack/dependency-track/issues/1605)
- Resolved defect where policy violations of type *Security* would not be displayed - [\#91](https://github.com/DependencyTrack/frontend/issues/91)
- Resolved defect where analysis justification and response would be reset when suppressing a finding - [\#140](https://github.com/DependencyTrack/frontend/pull/140)
- Resolved defect where the analysis status of policy violations would not be displayed - [\#130](https://github.com/DependencyTrack/frontend/pull/130)

**Security:**

**Upgrade Notes:**

- The `nist` directory inside the Dependency-Track data directory will be deleted upon upgrade. This will force the NVD to be downloaded and reprocessed.
- Users and teams with `POLICY_VIOLATION_ANALYSIS` permission are automatically granted the `VIEW_POLICY_VIOLATION` permission during the automatic upgrade.
- Location of `config.json` in the frontend container changed from `/app/static/config.json` to `/opt/owasp/dependency-track-frontend/static/config.json`

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.5.0/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 8db4707e3458b122e73cce92e7dc143c115db962                         |
| SHA-256   | 0c3d75501a0545f90e862aa0e2920f0c6146abcd436983531de7757ff294f568 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.5.0/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 984aafe85ac2dc361f9b0adf3c26d99decbab641                         |
| SHA-256   | 360176e810072b9ad393ba4f36e261c333ba45f4a662fe6b180e7481d70a14e1 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.5.0/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.5.0/bom.xml)

<a href="cloudcannon:collections/_posts/2022-05-18-v4.5.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.4.2 <a href="#v4-4-2" class="anchor">#</a>

<span class="date">March 04, 2022</span> <span class="badge patch">patch</span>

**Features:**

- Added advanced configuration options for controlling outbound HTTP connection timeouts - [1431](https://github.com/DependencyTrack/dependency-track/issues/1431)

**Fixes:**

- Resolved defect that resulted in a server error when suppressing a vulnerability - [1409](https://github.com/DependencyTrack/dependency-track/issues/1409)

**Security:**

**Upgrade Notes:**

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.2/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 172f569eb85f1182500571a160b134e8b1005ebf                         |
| SHA-256   | 5869df68cd29d48366d653a697bc198e0f3396c2897cd4a668743fc7157fb8df |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.2/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 49e73a820426a39ab83e6ec2a12f1c24e198a144                         |
| SHA-256   | d1570efdb61f7a2aa264f8103f6285e5330818087d3c54456e1b5335a3ca681f |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.2/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.2/bom.xml)

<a href="cloudcannon:collections/_posts/2022-03-04-v4.4.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.4.1 <a href="#v4-4-1" class="anchor">#</a>

<span class="date">February 18, 2022</span> <span class="badge patch">patch</span>

**Features:**

- **Fixes:**
- Resolved defect where the automatic upgrade failed on Microsoft SQL Server databases

**Security:**

**Upgrade Notes:**

- For MSSQL users only: If an upgrade to v4.4.0 was previously attempted and no rollback was performed yet, the following SQL statement must be executed before launching v4.4.1: `DELETE FROM "PERMISSION" WHERE "NAME" = 'VIEW_VULNERABILITY'`

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.1/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 9d6f20709009193540c4c152f0c0757d3b26bd5e                         |
| SHA-256   | c3eaeee440bfd1a734fb009983c97792407b107d64d4e9035a179b9b27c8ca49 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.1/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | ebadb4576ea419eb42807f5ef2bedb572de02df0                         |
| SHA-256   | e7b5e0ac00bc0e1021dc7a6571e02392c6854b12bba2ceea543c3959b7572524 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.1/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.1/bom.xml)

<a href="cloudcannon:collections/_posts/2022-02-18-v4.4.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.4.0 <a href="#v4-4-0" class="anchor">#</a>

<span class="date">February 17, 2022</span> <span class="badge major">major</span>

**Features:**

- Expanded vulnerability auditing and BOM export capabilities to include Vulnerability Exploitability Exchange (VEX) - [\#1365](https://github.com/DependencyTrack/dependency-track/issues/1365)
- Added Download BOM option to frontend supporting inventory, inventory with vulnerabilities, and vex - [\#1365](https://github.com/DependencyTrack/dependency-track/issues/1365)
- Added support for GitHub Advisories as a source of vulnerability intelligence - [\#1225](https://github.com/DependencyTrack/dependency-track/issues/1225)
- Removed legacy support for NPM Advisories and NPM Audit - [\#1225](https://github.com/DependencyTrack/dependency-track/issues/1225)
- Added support for CycloneDX external references to component details - [\#920](https://github.com/DependencyTrack/dependency-track/issues/920)
- Added new `VIEW_VULNERABILITY` permission that grants read-only access to project vulnerabilities and the audit trail. The permission also grants access to the findings API.
- Added support for ARM64 (including AArch64) container images - [\#1213](https://github.com/DependencyTrack/dependency-track/issues/1213)
- Added Dependency-Track SBOMs for frontend and API Server to `/.well-known/sbom` - [\#1363](https://github.com/DependencyTrack/dependency-track/issues/1363)
- Added API endpoint for teams/self specific to API key principals - [\#861](https://github.com/DependencyTrack/dependency-track/issues/861)
- Added support for Cisco WebEx as a target for alerts and notifications - [\#1170](https://github.com/DependencyTrack/dependency-track/pull/1170)
- NVD feed location is now configurable to support mirrors - [\#1274](https://github.com/DependencyTrack/dependency-track/pull/1274)
- Added support for OSS Index external references to increase CVE association - [\#1197](https://github.com/DependencyTrack/dependency-track/pull/1197)
- Added separate log events for “invalid username/password” and “account locked” - [\#1189](https://github.com/DependencyTrack/dependency-track/issues/1189)
- Added i18n support for vulnerability audit states - [\#946](https://github.com/DependencyTrack/dependency-track/issues/946)
- Added policy violations column to projects page - [\#94](https://github.com/DependencyTrack/frontend/issues/94)

**Fixes:**

- Resolved defect where the project a component belongs to may not be returned in API response - [\#1227](https://github.com/DependencyTrack/dependency-track/issues/1227)
- Resolved defect where notifications limited to specific projects weren’t properly limited - [\#1150](https://github.com/DependencyTrack/dependency-track/issues/1150)
- Resolved NPE in `GoModulesMetaAnalyzer` when a component without group was analyzed - [\#1220](https://github.com/DependencyTrack/dependency-track/pull/1220)
- Add workaround for OSS Index ignoring the component version when prefixed with `v` - [\#1220](https://github.com/DependencyTrack/dependency-track/pull/1220)
- Resolved OIDC post-login redirects for identity providers that do not support custom parameters in the `redirect_uri` parameter - [\#113](https://github.com/DependencyTrack/frontend/pull/113)
- Resolved defect that produced JDOObjectNotFoundException on heavy loads - [\#1168](https://github.com/DependencyTrack/dependency-track/issues/1168)
- Optimized performance of VulnerabilityAnalysisTask that previously caused high load - [\#1212](https://github.com/DependencyTrack/dependency-track/issues/1212)
- Resolved defect that prevented vulnerability identification for some hardware devices - [\#1320](https://github.com/DependencyTrack/dependency-track/issues/1320)
- Updated docker-compose.yml to include correct CORS configuration - [\#1325](https://github.com/DependencyTrack/dependency-track/issues/1325)
- Resolved incompatible dependency issue with VulnDB integration - [\#1349](https://github.com/DependencyTrack/dependency-track/issues/1349)
- The upload button in the UI is now deactivated until a file is specified - [\#86](https://github.com/DependencyTrack/frontend/issues/86)
- Resolved issue where tooltip in UI graphs may not be displayed - [\#92](https://github.com/DependencyTrack/frontend/issues/92)
- Resolved issue where `v` in some ecosystem versions caused issue with analysis - [\#1243](https://github.com/DependencyTrack/dependency-track/issues/1243) [\#1220](https://github.com/DependencyTrack/dependency-track/pull/1220)
- Resolved issue with BOMs containing UTF-8 byte order markers where rejected as invalid - [\#1214](https://github.com/DependencyTrack/dependency-track/issues/1214)
- Resolved issue where consuming a BOM with zero components would not trigger a metric update - [\#1183](https://github.com/DependencyTrack/dependency-track/issues/1183)

**Security:**

**Upgrade Notes:**

- Users and teams with `VULNERABILITY_ANALYSIS` permission are automatically granted the `VIEW_VULNERABILITY` permission during the automatic upgrade.

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.0/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | c81d753ce4376cee1ae4d2a8cf9710a9b8ceee45                         |
| SHA-256   | 31e685e79b658f661ce28f8c5cbc96906d23d408a2ade70ff7e7a8e20f054972 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.0/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 2b15b51c64938997ec9fbcf66054436064d9ef23                         |
| SHA-256   | c45835bc09ffe30c3b8ab675267259120230992bc984348293ae32b28ce1b54c |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.0/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.4.0/bom.xml)

<a href="cloudcannon:collections/_posts/2022-02-17-v4.4.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.3.6 <a href="#v4-3-6" class="anchor">#</a>

<span class="date">September 20, 2021</span> <span class="badge patch">patch</span>

**Features:**

**Fixes:**

- Added missing policy violation analysis on projects with empty component list [\#1183](https://github.com/DependencyTrack/dependency-track/issues/1183)

**Security:**

- Added additional audit logging for login attempts where the account has been locked out [\#1189](https://github.com/DependencyTrack/dependency-track/issues/1189)

**Upgrade Notes:**

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.6/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | d41721f52bfb17c9ba507a1ac01532071643d8ac                         |
| SHA-256   | 83f0bc7199677e3f6f84a76673b936ca73a6b8f54d5cb7cf181f77d548d47a6b |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.6/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 31fb39d8fecb6ec1e5c02d0fdede7a3e7e1cd952                         |
| SHA-256   | 3b0d1905291cf74af8f9e3bd81366d2b6c278ffe4b3940c0bb649871f6dfd15d |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.6/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.6/bom.xml)

<a href="cloudcannon:collections/_posts/2021-09-20-v4.3.6.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.3.5 <a href="#v4-3-5" class="anchor">#</a>

<span class="date">September 20, 2021</span> <span class="badge patch">patch</span>

No changes in this release.

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.5/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | d13ea84585009e70da2745690f4580b8db2a6e75                         |
| SHA-256   | 5334a13a5cc0662986d1643463c22bd6a7f3875165ad89296e2f9704b51acec5 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.5/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 2aee316ac07c5941a7ba734c30bec4f517cc2df1                         |
| SHA-256   | 3053e47cee828f459bede221159d68a61294670c3aed0720901273c7f3091256 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.5/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.5/bom.xml)

<a href="cloudcannon:collections/_posts/2021-09-20-v4.3.5.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.3.4 <a href="#v4-3-4" class="anchor">#</a>

<span class="date">August 31, 2021</span> <span class="badge patch">patch</span>

**Features:**

**Fixes:**

- Logic issue that causes inconsistent vulnerability findings when uploading the same BOM to different projects - [\#1176](https://github.com/DependencyTrack/dependency-track/issues/1176)

**Security:**

**Upgrade Notes:**

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.4/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 813e3a7207e47a7ee6769a1e74b040942f8995b5                         |
| SHA-256   | 1f8bae644dc6982933ec080167d90a66d8090055d75aad7e924a91a9cb8783c8 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.4/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 11db7cb3cf83b4e0d6ac121061b42d3f7e3c2c4e                         |
| SHA-256   | f6a2012a352294371e8396396e4659789c43c40931ada0d89e5c17352de0d1f1 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.4/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.4/bom.xml)

<a href="cloudcannon:collections/_posts/2021-08-31-v4.3.4.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.3.3 <a href="#v4-3-3" class="anchor">#</a>

<span class="date">August 20, 2021</span> <span class="badge patch">patch</span>

**Features:**

**Fixes:**

- Persistence issue related to manual server-side pagination that may cause `JDOObjectNotFoundException: No such database row` - [\#1059](https://github.com/DependencyTrack/dependency-track/issues/1059)
- Persistence issue that may result in ‘unknown’ project names for affect projects in the UI - [\#1154](https://github.com/DependencyTrack/dependency-track/issues/1154)
- Updated frontend to v4.3.1 which includes minor fixes and dependency updates

**Security:**

**Upgrade Notes:**

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.3/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | e28bc741856904115e54dd5bf2ef09addde011e8                         |
| SHA-256   | b748e9b43a25068dc5096f5a68d2e21d5450fca1d3805350042a566c4506d2ba |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.3/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | e884e3e32e18ff608837cc2d33b1d1760a00d0c7                         |
| SHA-256   | 05b87a43da078a684126f752d83a8da7488a8c02ef6d9ae9d3f0b347baec1832 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.3/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.3/bom.xml)

<a href="cloudcannon:collections/_posts/2021-08-20-v4.3.3.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.3.2 <a href="#v4-3-2" class="anchor">#</a>

<span class="date">August 07, 2021</span> <span class="badge patch">patch</span>

**Features:**

**Fixes:**

- Resoled an issue with portfolio access control where a user belonging to multiple teams will not have access to the aggregate of all projects or components they’re permitted to - [\#1132](https://github.com/DependencyTrack/dependency-track/issues/1132)

**Security:**

**Upgrade Notes:**

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.2/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 9746e03d0bd7dc02ca1d94aa29a6445144fb7589                         |
| SHA-256   | 283282536ec276bf048428fc02aee119ff9e42f995c67cf169e2bd2a7a92cd31 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.2/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 1cb384c6f5fc457cddbb93c55b7188cf5b446f6f                         |
| SHA-256   | cbab1409dc262d461db99587bd99fe6b0677fde36414b3c6c965b14640aec29b |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.2/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.2/bom.xml)

<a href="cloudcannon:collections/_posts/2021-08-07-v4.3.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.3.1 <a href="#v4-3-1" class="anchor">#</a>

<span class="date">August 03, 2021</span> <span class="badge patch">patch</span>

**Features:**

**Fixes:**

- Resolves an issue introduced in Datanucleus 5.2.8 that lead to invalid SQL generation on Postgres databases - [\#1129](https://github.com/DependencyTrack/dependency-track/issues/1129)

**Security:**

**Upgrade Notes:**

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.1/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 6c188379b93f2b4052bb73649608db69175b0efc                         |
| SHA-256   | 6008b32cc3cf6b13d0e7efaff335290102580bd6b518f50d630b99280a9b5538 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.1/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 9ff235da5d4b6fb9e9fe4b6762c5dfa8d83073e9                         |
| SHA-256   | a64885b7146e7b74e0099a691781ef6417f094fd7424768cf25a86a7de642b00 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.1/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.1/bom.xml)

<a href="cloudcannon:collections/_posts/2021-08-03-v4.3.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.3.0 <a href="#v4-3-0" class="anchor">#</a>

<span class="date">August 02, 2021</span> <span class="badge major">major</span>

**Features:**

- Implemented Portfolio Access Control (beta) - [\#140](https://github.com/DependencyTrack/dependency-track/issues/140)
- OpenID Connect: Source user claims from `/userinfo` *and* ID token - [\#1008](https://github.com/DependencyTrack/dependency-track/issues/140)
  - Resolves an issue where some IdPs would provide specific claims only in one and not the other of the two
- Added Go Modules repository support
- Added timeout for idle transactions - [\#941](https://github.com/DependencyTrack/dependency-track/issues/941)
- Components with missing or unknown license are now evaluated against policy condition - [\#1105](https://github.com/DependencyTrack/dependency-track/issues/1105)

**Fixes:**

- Resolved issue where active projects could only be displayed when showing inactive projects - [\#963](https://github.com/DependencyTrack/dependency-track/issues/963)
- Resolved high load issues with Postgres while simultaneously increasing performance for all database platforms - [\#1026](https://github.com/DependencyTrack/dependency-track/issues/1026)
- Resolved issue with OSS Index where PURLs without a version will lead to scan failure - [\#1115](https://github.com/DependencyTrack/dependency-track/issues/1115)

**Security:**

Portfolio ACL logic has been implemented. In its current form, Portfolio Access Control is a beta feature in v4.3. As a result, the project will not treat bypass or absent ACL logic as a security defect. There are a few known gaps in ACL logic that will exist in v4.3. These gaps are tracked in [\#1127](https://github.com/DependencyTrack/dependency-track/issues/1127).

ACL logic covers:

- /v1/bom/\*
  - Uploading SBOMs to projects or exporting SBOMs from projects or components
- v1/component/\*
  - CRUD operations on components
- /v1/finding/\*
  - Security findings for projects and components
- /v1/metrics/\*
  - Project and component metrics
- /v1/project/\*
  - \_RUD operations on projects
- /v1/service/\*
  - CRUD operations on components
- /v1/violation/\*
  - Project and component policy violations
- /v1/vulnerability/\*
  - CRUD operations on vulnerable projects or components

The user interface clearly states that Portfolio Access Control is beta. By default, Portfolio Access Control is disabled.

**Upgrade Notes:**

- OpenID Connect: The client ID of the frontend has to be passed to the API server via the `alpine.oidc.client.id` property
  - Required for the API server to be able to validate ID tokens. Refer to the [OIDC documentation](/getting-started/openidconnect-configuration/) for details.
- Removed legacy support for SPDX (RDF and tag/value) - [\#1053](https://github.com/DependencyTrack/dependency-track/issues/1053)
- Removed legacy support for the traditional WAR (was previously deprecated and unsupported) - [\#1070](https://github.com/DependencyTrack/dependency-track/issues/1070)

###### [dependency-track-apiserver.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.0/dependency-track-apiserver.jar)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 1c19a467705631c3c4449fa3f95c9d4a73d26caa                         |
| SHA-256   | 34e0cc69eb6934d9e25573d29870cefce75d07d97fb06d58e8830f566256e1dc |

###### [dependency-track-bundled.jar](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.0/dependency-track-bundled.jar)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 3e3a9edb9a9077fc5e2b2634f5967d1a61b0e1cb                         |
| SHA-256   | 78c5a7acf02d5d5f7231c444fdc58b38f12ebec20453c51106200ca0d644b387 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.0/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.3.0/bom.xml)

<a href="cloudcannon:collections/_posts/2021-08-02-v4.3.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.2.2 <a href="#v4-2-2" class="anchor">#</a>

<span class="date">May 07, 2021</span> <span class="badge patch">patch</span>

**Features:**

**Fixes:**

- Resolved issue originating from changes in the NVD JSON feed which prevented the identification of vulnerabilities by a components CPE. ([\#1018](https://github.com/DependencyTrack/dependency-track/issues/1018)), ([\#1033](https://github.com/DependencyTrack/dependency-track/issues/1033))

**Security:**

**Upgrade Notes:**

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.2/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 60a87ecafd9ba4b0ba119a65e1a041b0c5f576ea                         |
| SHA-256   | bd20dbee794fa0c37c345526204058dbfbdd734acaf257783f9cb47e2cf17c63 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.2/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 748b3fbf89efb61d29a468e3cd1c90bfcaeb3c4e                         |
| SHA-256   | 93948be57b0e7864b872a2869c840c50bf9f2b3d1e9cc75794abea4c53038851 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.2/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 35b61e4309303a7ad605c21cfa5eddcbabcfa15f                         |
| SHA-256   | 965508b98df6701ffea13ec9bcfb2f3d8a7e14eba95a68f5c266a2b75b1db109 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.2/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.2/bom.xml)

<a href="cloudcannon:collections/_posts/2021-05-07-v4.2.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.2.1 <a href="#v4-2-1" class="anchor">#</a>

<span class="date">March 20, 2021</span> <span class="badge patch">patch</span>

**Features:**

**Fixes:**

- Resolves an issue in OIDC support where “email” could not be used as the username claim

**Security:**

**Upgrade Notes:**

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.1/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 92a0e935c7d4309e67fc7eb149191d96a1635c8b                         |
| SHA-256   | 80cc253d05ccb91aa432667bf7d418bc8327f82b1dfe770aec71c434d0ecd308 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.1/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 930d89d1a37e85130a6603969f30253fe842a6e0                         |
| SHA-256   | 2b27c6f1918a897f22b48542010611c67fa137f399521a45c900ee59120b81c5 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.1/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 7a3061da05f67fd4f98b149eeb6d588389d1b202                         |
| SHA-256   | 06da5d59c8404f31d3497d163a2d3fe75f35af50374339315c6161dd0b989637 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.1/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.1/bom.xml)

<a href="cloudcannon:collections/_posts/2021-03-20-v4.2.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.2.0 <a href="#v4-2-0" class="anchor">#</a>

<span class="date">March 17, 2021</span> <span class="badge major">major</span>

**Features:**

- Added support for capturing dependency graphs from CycloneDX SBOMs
- Added dynamic visualization of dependency graphs in user interface
- Added support for services defined in CycloneDX SBOMs
- Added support for CWE v4
- Add support for *version* policy conditions and version comparisons in the *coordinates* condition ([\#390](https://github.com/DependencyTrack/dependency-track/pull/930))
- Detail modals for projects, components, services, and vulnerabilities now display the object’s UUID

**Fixes:**

- Added support for Fortify SSC 20.1 and higher. This fixes a breaking change introduced in SSC 20.1
- Added missing database index to increase performance when a large number of components are in the portfolio
- Fixed multiple issues when cloning projects

**Security:**

**Upgrade Notes:**

- OpenID Connect: To facilitate support for post-login redirects, the *valid redirect URIs* client setting in IdPs *may* need to be updated. Refer to the [OIDC documentation](/getting-started/openidconnect-configuration/) for details.
- The internal port the frontend container listens on has changed from port 80 to port 8080. docker-compose files may need to be updated to reflect this change. Updated compose files are [available for download](https://dependencytrack.org/docker-compose.yml).
- Starting with Dependency-Track v4.2, the API Server and the Frontend now have the same major and minor (semantic) version. Patch versions however, may continue to be unique.

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.0/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | f1776e778405b5f6be2903d317463a74153c5319                         |
| SHA-256   | a47a3073def269e810d53de781cd7c22620e94ca80df3f781d528a7a5fe4c779 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.0/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | c3c2f931cc4f835eddd0013a885e13c16f990ea9                         |
| SHA-256   | 7d61818c281c6540ff4273d4d4c5d9d6e63b86b55f13e92fca7ba2921613800c |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 1634d6cf94761d3b0839f4b4a4d9fdd53d314ba6                         |
| SHA-256   | 792dc2adcc33c936629d014dacca8965d001bd1d236893df50dc88dc332d4d21 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.0/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.2.0/bom.xml)

<a href="cloudcannon:collections/_posts/2021-03-17-v4.2.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.1.0 <a href="#v4-1-0" class="anchor">#</a>

<span class="date">February 09, 2021</span> <span class="badge major">major</span>

**Features:**

- Added support for vulnerabilities in policy violations
- Added Packagist (PHP Composer) repository support
- Added Rust Cargo repository support
- Added integration support for DefectDojo
- Added the addition of a notes field for components
- Updated Java requirements to Java 11

**Fixes:**

- Fixed issue that prevented SWID tag ID from being persisted when BOMs were consumed
- Added prevention that should detect future occurrences pagination of the NPM Advisory API not working

**Security:**

**Upgrade Notes:**

- Support for Java 8 was dropped. API Server now requires Java 11

- Downloading a CycloneDX BOM for a project now results in the IANA media types in the response header.

  `application/vnd.cyclonedx+xml`

  `application/vnd.cyclonedx+json`

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.1.0/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | ed951e6a1db32b5541b646f7595cce28345c816d                         |
| SHA-256   | e459525d279abef75f0d6cef756636503b1040939778df14decaaca65d284db1 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.1.0/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 669955757d9f5fe1e145ac61e761358986697b3d                         |
| SHA-256   | a33f70500087fc6cfa9ffdeba1ac20de474ba28c1572f85337f04765e961f66c |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.1.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | a2ab12792eebcf420e6f0b07baa4a49bce5e0082                         |
| SHA-256   | c47fa7e5c2049e1f677b552838b7b5ee6971dfdee942f2e3ce1f0aa708a9dfaa |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.1.0/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.1.0/bom.xml)

<a href="cloudcannon:collections/_posts/2021-02-09-v4.1.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.0.1 <a href="#v4-0-1" class="anchor">#</a>

<span class="date">January 12, 2021</span> <span class="badge minor">minor</span>

**Fixes:**

- Fixes issue that resulted in policy violations being returned for all projects rather than the project for which the query is made for.

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.1/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 5fb224978c700f5c38d49527669da262a324a9be                         |
| SHA-256   | d46594ec65c0a30b645eb13419bdc36df41cc6d71053b8bb9efdee80d4de7b99 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.1/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | d9275f0b660b54205ec811c0d0cab9f584ba2a91                         |
| SHA-256   | 89e155529036c5f8eb977f0c611eac2abc9496c55d2c49dd4dec14dbc5acb431 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.1/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 59b571d0b1ee97a12342938d0d3b17b287c86ad4                         |
| SHA-256   | a54b564123873ea3c2378c2dce5a9ecf0000df6ee0721f9d3ddf0349ba4c575f |

###### Software Bill of Materials (SBOM)

- [bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.1/bom.json)
- [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.1/bom.xml)

<a href="cloudcannon:collections/_posts/2021-01-12-v4.0.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v4.0.0 <a href="#v4-0-0" class="anchor">#</a>

<span class="date">January 03, 2021</span> <span class="badge major">major</span>

**Features:**

- Flexible, project-centric data model
- Added policy engine, configurable policies, policy evaluation, and auditing workflow
- Added default license groups
- Anonymous access to Sonatype OSS Index is now enabled by default
- Component vulnerabilities are now attributed to the analyzers responsible for finding them
- Added support for CycloneDX 1.2 and SPDX 2.2
- Added component support for Blake2b and Blake3 hash algorithms
- Added component support for SWID Tag ID
- Projects now have identity, similar to components, and support coordinates (group, name, version), CPE, Package URL, and SWID Tag ID
- Added support for firmware and container component types
- When generating a CycloneDX BOM from a project or component, v1.2 of the spec is now produced
- Updated SPDX license list to v3.11
- Dropped support for NVD JSON v1.0 data feeds
- Optimized NVD mirroring logic
- Inactive projects are omitted from portfolio metrics
- Updates to the notification email template for BOM consumed and BOM processed

**Fixes:**

- Fixed issue with scoped NPM packages not being identified correctly
- Fixed issue that failed to report new vulnerabilities on existing components
- Fixed broken weakness (CWE) link on some vulnerabilities
- Fixed failure on mail notifications when multiple addresses were configured
- Fixed container healthcheck to specify use of no-proxy
- Fixed issue where component descriptions in a BOM were not being saved

**Security:**

**Upgrade Notes:**

- The Dependency-Track v4 data model is incompatible with previous releases. As a result, it is not possible to simply upgrade as with previous versions. A data migration is required to update from 3.8 to 4.0. The migration is a standalone set of scripts that must be executed against the database in order to migrate the data to the new model. Refer to the official [v3.8.0 to v4.0.0 Migration Project](https://github.com/DependencyTrack/v3.8.0-v4.0.0-migration) for more information.
- Four Dependency-Track distribution variants are provided. Refer to [Distributions](/getting-started/distributions/) for details.
- The traditional WAR distribution is deprecated and no longer supported. It is still being produced as of this release but will be discontinued in a future release.
- Docker images have been moved from the OWASP organization on Docker Hub to a dedicated [Dependency-Track organization](https://hub.docker.com/u/dependencytrack).
- The FrontEnd requires deployment to the root (“/”) context. Deploying to any context other than root is no longer supported.
- Some APIs have changed as of this release. APIs that were specific to the global component model have been removed. APIs that referenced a ‘dependency’ in the model have changed. Components are now assigned directly to projects themselves, thus eliminating the need for ‘dependency’ objects in v4.
- The MySQL Connector distributed with the Docker image has been updated to version 8.0.22. When using MySQL, `ALPINE_DATABASE_DRIVER_PATH` has to be set to `/extlib/mysql-connector-java-8.0.22.jar`. Note that `ALPINE_DATABASE_DRIVER` may need to be updated as well. Refer to the [official upgrading instructions](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-upgrading-to-8.0.html).
- The Postgres driver distributed with the Docker image has been updated to version 42.2.18. When using Postgres, `ALPINE_DATABASE_DRIVER_PATH` has to be set to `/extlib/postgresql-42.2.18.jar`.

###### [dependency-track-apiserver.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.0/dependency-track-apiserver.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 9124352542544c5662d3ebf34d951e61f08ff231                         |
| SHA-256   | 6b6b8d608b467da087fb7ebe12fb6bbb2a418d97168baa186b1320fdb3b49a91 |

###### [dependency-track-bundled.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.0/dependency-track-bundled.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 9a4f516e5fcd6eae117465732e3dcaa69227d238                         |
| SHA-256   | 2e66976b5f890186e64255484f262564e23e8a3ce482769374959c7ddc55c42c |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | a489586be032890ec6cddc5ec839da57026837a7                         |
| SHA-256   | 152819d9b80377f6b672fbdc6448d7ea250f3bba43c479c335404faa700d9b24 |

###### Software Bill of Materials (SBOM)

[bom.json](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.0/bom.json) [bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/4.0.0/bom.xml)

<a href="cloudcannon:collections/_posts/2021-01-03-v4.0.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.8.0 <a href="#v3-8-0" class="anchor">#</a>

<span class="date">March 22, 2020</span> <span class="badge major">major</span>

**Bundled frontend: [v1.0.0](https://github.com/DependencyTrack/frontend/releases/tag/1.0.0)**

**Features:**

- New user interface based on Vue.js and Bootstrap.
- User interface can optionally be deployed and upgraded independently of the Dependency-Track server.
- Package repositories are now configurable.
- Package repositories can now be identified as ‘internal’. Components identified as ‘internal’ will be analyzed using internal repositories.
- Added additional logging and notifications for OSS Index and NPM Audit analyzers.
- Added the ability to publish system notifications when vulnerability analyzers encounter communication or other errors.
- Added several occurrences of counts for various items throughout the UI.

**Fixes:**

- Corrected the percentage value of findings audited.
- Fixed URL to Maven Central which prevented the MavenMetaAnalyzer from retrieving component metadata.
- Changed logging behavior when internal components are identified.
- Improved accuracy of internal CPE analyzer which may have lead to false negatives in some situations.
- Fixed issue where the CPE value defined in a BOM was not being persisted if the component previously existed.
- Fixed issue which prevented the HexMetaAnalyzer from executing preventing it from retrieving component metadata for Erlang or Elixir components.

**Security:**

- All Dependency-Track server releases now include a complete CycloneDX software bill-of-materials.
- Added missing permission checks to repository API endpoints.

**Upgrade Notes:**

- The `nist` and `index` directories inside the Dependency-Track data directory will be deleted upon upgrade. This will force the NVD to be downloaded and reprocessed and the indexes to be rebuilt.
- The internal vulnerable software dictionary, generated automatically from the NVD, will be wiped upon upgrade. This will take several minutes to complete and should not be interrupted.

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.8.0/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 091627dfa144a1313bf9090d8f67b4760e635b23                         |
| SHA-256   | 56674c40da9dc4277b6c8238d0dc6cc28bdf3b4cc51b7b845606b1a2c149070b |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.8.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 1db04afbc1b66421dd6fe0db816ec14362b895d1                         |
| SHA-256   | 9fd73c4ea24352b6165106c1d5a1b88bd43ea9e6ba0e15a733a217a59d7bd268 |

###### Software Bill-of-Materials (SBOM)

[bom.xml](https://github.com/DependencyTrack/dependency-track/releases/download/3.8.0/bom.xml)

<a href="cloudcannon:collections/_posts/2020-03-22-v3.8.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.7.1 <a href="#v3-7-1" class="anchor">#</a>

<span class="date">January 07, 2020</span> <span class="badge minor">minor</span>

**Features:**

- Added additional debug logging to metric update tasks

**Fixes:**

- Fixed portfolio metrics issue that allowed multiple operations to be executed simultaneously leading to performance degradation

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.7.1/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 5cd02dc5c6ca8aba3cea1ad5ad03d039ecdd757c                         |
| SHA-256   | f80f527d96692a45f3bba86849551debf4b407bd880f104b890912975cc865ca |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.7.1/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 766d5394ce7a5a0e08c96a55930adc3377897d99                         |
| SHA-256   | 4e6233013af574585d93dd99586455a810ea434c3bc5da95e53aad45751f5bc2 |

<a href="cloudcannon:collections/_posts/2020-01-07-v3.7.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.7.0 <a href="#v3-7-0" class="anchor">#</a>

<span class="date">December 16, 2019</span> <span class="badge major">major</span>

**Features:**

- Application context is now configurable in the Docker container
- SVG badges may now be retrieved via the project name and version
- Added Hex repository support for Erlang, Elixir, and other BEAM languages
- Added configurable support for defining components as internal which are not subject to external analysis
- Increased CPE analysis precision for components with CPEs containing a value in the update field

**Fixes:**

- Fixed defect in /api/v1/project that returned a server error if the ‘name’ parameter was specified
- Fixed defect resulting in invalid gzip response body when Accept-Encoding was not specified
- Fixed defect resulting in licenses not being loaded if Dependency-Track is deployed to a directory containing a space
- Changed behavior when parsing an invalid CPE to display a single line warning rather than the full stack trace
- Fixed defect resulting in a project not being able to be deleted when that project was part of a notification rule
- Fixed encoding issue affecting project names containing special characters

**Security:**

- [GHSA-4gqv-hcmg-jw33](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-4gqv-hcmg-jw33) Cross-Site Scripting (XSS): Persistent
- [GHSA-6j82-qv49-r46p](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-6j82-qv49-r46p) Cross-Site Scripting (XSS): Persistent

**Upgrade Notes:**

- Support for consuming Dependency-Check v4.x XML reports has been removed
- The following can safely be (optionally) dropped upon a successful upgrade (consult log):
  - Tables:
    - SCANS_COMPONENTS
    - SCAN
  - Columns:
    - LAST_SCAN_IMPORTED (in PROJECT table)

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.7.0/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | e946c65ec0ff5ba12e843789b917caab635bfe62                         |
| SHA-256   | bd02a522a8c9beeb8dd7964f07eb27a7a02ce8bbf6a7c8af3378bb26fc98a087 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.7.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 22da81fb91b5641fcb805c74063c11e521fe0ad4                         |
| SHA-256   | 9207e25b19d34b57804f25e9881e663ebb56333520b039c5ccfd93209295b0a1 |

<a href="cloudcannon:collections/_posts/2019-12-16-v3.7.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.6.1 <a href="#v3-6-1" class="anchor">#</a>

<span class="date">October 01, 2019</span> <span class="badge minor">minor</span>

**Fixes:**

- Fixed issue that prevented upgrades to 3.6.0 when using Microsoft SQL Server

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.6.1/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | f18f248d2601878b3d437e3c6539311dc4a31c47                         |
| SHA-256   | b24cc49e8483c4841d6bc3efa9c1f944836a9524028960ee463ae4db7dac7c02 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.6.1/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | b758993e26f812494ca0191e7ad39037f2cd79ea                         |
| SHA-256   | da128b3602ea4e0214558074abd3df30201e7d858b79a7abb5065d358db19b40 |

<a href="cloudcannon:collections/_posts/2019-10-01-v3.6.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.6.0 <a href="#v3-6-0" class="anchor">#</a>

<span class="date">September 28, 2019</span> <span class="badge major">major</span>

**Features:**

- Added configurable option to enable/disable BOMs based on format (CycloneDX enabled by default)
- Added support for the official CPE v2.3 dictionary and vulnerabilities with CPEs of affected products
- Added ability to identify vulnerabilities in components solely by their CPE
- Added full support for VulnDB as a source of vulnerability intelligence
- Added support for SVG badges
- Added additional logging during metrics updates
- Docker container now supports Kubernetes and OpenShift
- Docker container now has configurable support for specifying logging levels
- Added Inherited Risk Score to project list view with the ability to sort on risk score
- Added an ‘active’ flag to projects with the default behavior of hiding inactive projects
- Added BOM_CONSUMED and BOM_PROCESSED notifications which can optionally deliver BOMs via webhooks
- Added support for last BOM imported including the BOM type and version
- Added an API to lookup a project by its name and version
- Added analysis interval throttle to prevent repeated analysis requests for the same components
- Slack and email alerts now contain links back to Dependency-Track
- Added support for Java 11

**Fixes:**

- Fix for GLOBAL_AUDIT_CHANGE not including affected projects
- Fixed issue that prevented Dependency-Track for working with non-default URL contexts
- Fixed intermittent persistence issue resulting in NPE in BomUploadProcessingTask
- Fixed issue resulting in incorrect percentage audited on project findings
- Fixed OSS Index analyzer in response to the URL changes from ossindex.net to ossindex.sonatype.org

**Upgrade Notes:**

- Support for SPDX BOMs and Dependency-Check XML reports are disabled by default
- Replaced embedded Dependency-Check library with internal CPE analyzer
- Dependency-Track no longer mirrors XML data feeds from the NVD

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.6.0/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 6cd17d5a31472f7f60e674e2d7fc2e3050085808                         |
| SHA-256   | bbb72fa3b6246b7afa7c22b103f0c85daf82565a38ae12973043775e6b27fd6e |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.6.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | f7b88825dbaf8b837977954f5a7e506952ed8361                         |
| SHA-256   | a1d0d308a46d30399e9ff9a0334fe3be70345aa12c30c0d1d6bfccdcafe062e2 |

<a href="cloudcannon:collections/_posts/2019-09-28-v3.6.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.5.1 <a href="#v3-5-1" class="anchor">#</a>

<span class="date">July 17, 2019</span> <span class="badge minor">minor</span>

**Fixes:**

- [GHSA-jp9v-w6vw-9m5v](https://github.com/DependencyTrack/dependency-track/security/advisories/GHSA-jp9v-w6vw-9m5v) Cross-Site Scripting (XSS): Persistent

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.5.1/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | aafdfa3142dc478b95f1d6ffc268b2a1832ccb29                         |
| SHA-256   | 73bbe06a22f84ce7b099da3c552e267c980f0f8c58ca6cccdd3eaa210bfe9b6c |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.5.1/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | cf71dbf7ae697038d6a42485f14991f343ffdeff                         |
| SHA-256   | 271705e72e94e9f9fb36159ea110a05ff465c4d1f2572a89570774e57c08a247 |

<a href="cloudcannon:collections/_posts/2019-07-17-v3.5.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.5.0 <a href="#v3-5-0" class="anchor">#</a>

<span class="date">June 07, 2019</span> <span class="badge major">major</span>

**Features:**

- Improved performance, reliability, and quality
- Added support for importing CycloneDX v1.1 BOMs
- Added additional logging and enhanced logging configuration
- Added configurable CORS support

**Fixes:**

- Numerous. The majority of known defects have been resolved

**Upgrade Notes:**

Two new LDAP properties were introduced in v3.5.0 that affect LDAP configuration. The properties are:

- alpine.ldap.groups.search.filter
- alpine.ldap.users.search.filter

Refer to [Configuration](/getting-started/configuration/) and [Deploying Docker Container](/getting-started/deploy-docker/) for details.

Additional properties introduced in this release are:

- alpine.database.pool.enabled
- alpine.database.pool.max.size
- alpine.database.pool.idle.timeout
- alpine.database.pool.max.lifetime

Under most situations, changing these values is not recommended and may introduce unintended consequences. One important change introduced in this release is the default value of `alpine.database.pool.max.lifetime` has changed from 30 minutes (in previous releases) to 10 minutes.

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.5.0/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 7d66f0530d74ff9bc0de628d5e76b5ee6ed6ead7                         |
| SHA-256   | 8bbf820fde7843a680fd51eed831aeddd61507f5420abb68b46859168cc98919 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.5.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 0bb9a0737a36ebbcd88fe91ca595f12957e85583                         |
| SHA-256   | 143ed44988419ba84cc3956e602e297f025149f19faa65f32c0e8311b71fed5b |

<a href="cloudcannon:collections/_posts/2019-06-07-v3.5.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.4.1 <a href="#v3-4-1" class="anchor">#</a>

<span class="date">April 16, 2019</span> <span class="badge minor">minor</span>

**Fixes:**

- Fixed defect that caused high CPU consumption (via thread exhaustion) in some cases when NPM Audit was enabled.

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.4.1/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | f8da8e34a3cabcf72b721488f5294710ff632bf6                         |
| SHA-256   | 72391cc636c2159ffc0c516f2001688129a3b6424164c98ce9045c0fd5c3219b |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.4.1/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 1cdb5b6c5698229b21acbc610df77ec819ad5180                         |
| SHA-256   | 619e9ae00feb9f9723bef68981d32932d2d5cdf808b192619bf072d525224f5e |

<a href="cloudcannon:collections/_posts/2019-04-16-v3.4.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.4.0 <a href="#v3-4-0" class="anchor">#</a>

<span class="date">December 22, 2018</span> <span class="badge major">major</span>

**Features:**

- Improvements to Findings API
- Created Finding Packaging Format for the native exporting of findings
- Added support for external integrations including:
  - Fortify Software Security Center
  - Kenna Security
- Added repository (and outdated version detection) support for NuGet and PyPI
- Updated SPDX license list to v3.3
- Added support for identifying FSF Libre licenses
- Updated Java version in Docker container
- Docker container can now be fully configured with environment variables
- Added Test Configuration button when configuring SMTP settings
- Added logfile rotation with default 10MB cap (configurable)

**Fixes:**

- Corrected issue that incorrectly returned suppressed vulnerabilities when queried for non-suppressed ones
- Fixed issue that resulted in server/UI timeouts due to excessive license payload
- Fixed NPE that occurred when the configured SMTP server didn’t require authentication
- Added workaround for outstanding OSS Index defect where the service didn’t process PackageURLs containing qualifiers
- Updated OpenUnirest which addressed configuration issue with library not honoring proxy server settings

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.4.0/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 676e04e0ef002e371da3b5eab239b0ab55dffe57                         |
| SHA-256   | 006801f124d190e929ab7e6352adcc0bf89047259eff5a15cf4d54a01d7b402d |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.4.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 15309c0818034ac99f603b52f242748b255818b9                         |
| SHA-256   | 624fa3e7f458b163a0bbb8f05ee7cb1cf052d6d4ea53ff2b43686dd55bb83135 |

<a href="cloudcannon:collections/_posts/2018-12-22-v3.4.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.3.1 <a href="#v3-3-1" class="anchor">#</a>

<span class="date">November 13, 2018</span> <span class="badge minor">minor</span>

**Features:**

- Improved findings API to support a wider range of use-cases

**Fixes:**

- When importing some npm dependencies (via Dependency-Check report), some modules would get misidentified causing an NPE
- Fixed non-standard Java versioning schemes (such as Debian OpenJDK) that caused version comparison to fail
- Corrected issue that resulted in suppressed vulnerabilities to be returned from a query as if they were not suppressed
- Fixed issue preventing saving of SMTP settings with anonymous authentication

**Upgrade Notes:**

The format of the findings API has changed and will not be versioned. This API is used to present findings from the audit tab in the UI. If this API was being used outside the UI, please note that the response format has changed.

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.3.1/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | f7a0fcf9568a765b9bb3cdf3465f475810c333e8                         |
| SHA-256   | f5693cab665932c80e7056c37ed93bf61a1638e252e48e9c0717b8d0c4740ea4 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.3.1/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | bfcf20a5cb87d562b781419f7b989c35ff67e390                         |
| SHA-256   | 91156bc404ab84a09e912302888ef06c52813764e88ad73039550a9ff2e82b91 |

<a href="cloudcannon:collections/_posts/2018-11-13-v3.3.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.3.0 <a href="#v3-3-0" class="anchor">#</a>

<span class="date">October 25, 2018</span> <span class="badge major">major</span>

**Features:**

- The ability to manually upload a CycloneDX or SPDX BOM from the user interface
- Optional automated provisioning of LDAP users
- Optional synchronization of team membership based on a users LDAP group membership
- Added API that provides component metadata from a project in CycloneDX format
- Added ability to track the progress of work performed when a BOM is uploaded
- Added tracking of audited and unaudited metrics
- Added ability to add new project version and optionally clone source metadata
- Added ability to search by tag name when displaying projects
- Added checksum generation when publishing a release (backported to 3.2.2)
- The NSP Advisory API has been removed and replaced with the NPM Public Advisory API (backported to v3.2.1)

**Fixes:**

- Fixed numerous LDAP compatibility issues
- Added additional logging when BOM upload is not in a supported format

**Upgrade Notes:**

This release of Dependency-Track supports a wide range of LDAP implementations and has been tested with Active Directory, ApacheDS, Fedora 389 Directory, and NetIQ/Novell eDirectory. In order to ensure compatibility, some existing LDAP configuration properties have been changed.

<div class="language-ini highlighter-rouge">

<div class="highlight">

``` highlight
# This property has been removed
alpine.ldap.domain
```

</div>

</div>

<div class="language-ini highlighter-rouge">

<div class="highlight">

``` highlight
# This property now refers to the users DN
alpine.ldap.bind.username
```

</div>

</div>

<div class="language-ini highlighter-rouge">

<div class="highlight">

``` highlight
# Format now applies only to the value of alpine.ldap.attribute.name. 
# Examples have been modified. A users DN is no longer a valid format.
alpine.ldap.auth.username.format
```

</div>

</div>

<div class="language-ini highlighter-rouge">

<div class="highlight">

``` highlight
# New properties
alpine.ldap.groups.filter
alpine.ldap.user.groups.filter
alpine.ldap.user.provisioning
alpine.ldap.team.synchronization
```

</div>

</div>

**See Also:**

- [Configuration](/getting-started/configuration/) (updated)
- [LDAP Configuration](/getting-started/ldap-configuration/) (examples)

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.3.0/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 413b47068dd1272f0ea6c4af67dc1465fcf10674                         |
| SHA-256   | 5632d6efa8c6ea2633bb767d09c73c4ee68e9319b638ce00da4c422f5123c906 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.3.0/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | 1a8dc64a7535375fdd4ff789eeb9d3635dcba019                         |
| SHA-256   | 96e20c0b72e3d8c460dfe3ce2b9aca72c6114492747db9afffca9784c64d23b9 |

<a href="cloudcannon:collections/_posts/2018-10-25-v3.3.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.2.2 <a href="#v3-2-2" class="anchor">#</a>

<span class="date">October 02, 2018</span> <span class="badge minor">minor</span>

**Fixes:**

- Critical defect which may lead to duplicate or erroneous requests to NPM Audit API

**Changes:**

- Added checksums.xml including SHA-1, SHA-256, SHA-512 checksums for traditional and embedded wars to GitHub releases.

###### [dependency-track-embedded.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.2.2/dependency-track-embedded.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | fead4ed834b4738b8c19c427ae57653f7af4a3b8                         |
| SHA-256   | ee53ceacb07b0b0b4dfa88e2bdc2e905668f0dd6d42ca1000b3204d0a2ee1842 |

###### [dependency-track.war](https://github.com/DependencyTrack/dependency-track/releases/download/3.2.2/dependency-track.war)

|           |                                                                  |
|-----------|------------------------------------------------------------------|
| Algorithm | Checksum                                                         |
| SHA-1     | defbb7a40bb12c3beacdeb43fb5fd325d226da50                         |
| SHA-256   | c154f0f07c9875d602d3e1df93d93d617e83f350ef683bdb16eb193d03a86ea5 |

<a href="cloudcannon:collections/_posts/2018-10-02-v3.2.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.2.1 <a href="#v3-2-1" class="anchor">#</a>

<span class="date">September 21, 2018</span> <span class="badge minor">minor</span>

**Features:**

- The NSP Advisory API has been removed and replaced with the NPM Public Advisory API

**Fixes:**

- Processing and permission corrections to new multi-part BOM upload API
- UI corrections for vulnerabilities with unassigned severity
- Fixes for displaying and processing of vulnerabilities without CVSS scores
- Minor changes to severity colour scheme

**Upgrade Notes:**

All previous NSP vulnerabilities will automatically be migrated to NPM vulnerabilities. No additional action is required. Unlike NSP vulnerabilities, NPM does not provide CVSS scores or vectors. Therefore all NPM vulnerabilities will no longer display the CVSS vector, or the base, impact, or exploitability scores and corresponding chart data.

<a href="cloudcannon:collections/_posts/2018-09-21-v3.2.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.2.0 <a href="#v3-2-0" class="anchor">#</a>

<span class="date">September 06, 2018</span> <span class="badge major">major</span>

**Features:**

- Configurable notifications of new vulnerabilities, vulnerable dependencies, analysis decision changes, and system events
- Added Slack, Microsoft Teams, Outbound Webhook, Email, and system console notification publishers
- Replaced NSP Check API with NPM Audit API
- Added support for Sonatype OSS Index
- Updated SPDX license IDs to v3.2
- General improvements in logging when error conditions are encountered
- Improvements to Dependency-Check XML report parsing
- Added native CPE 2.2 and 2.3 parsing capability
- Enhanced administrative interface with options for repositories and general configuration
- Updated Java version used in Docker container

**Fixes:**

- The audit table did not reflect the correct analysis and suppressed data
- Added validation when processing Dependency-Check XML reports containing invalid Maven GAVs
- Corrected issue with NVD mirroring affecting Docker containers and case-sensitive filesystems

**Upgrade Notes:**

- The PROJECT_CREATION_UPLOAD permission was introduced in this release. Existing API keys that need the ability to dynamically create projects (without providing them full PORTFOLIO_MANAGEMENT permission) will need this permission added to their account or through their team membership.

- The SYSTEM_CONFIGURATION permission was introduced in this release. Existing administrative users that need the ability to perform more general purpose system configurations need to add this permission to their accounts.

- Upgrades to v3.2.0 can be successfully performed from systems running v3.1.x. If a previous version is being used, an upgrade to 3.1.x is required prior to upgrading to v3.2.0.

<a href="cloudcannon:collections/_posts/2018-09-06-v3.2.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.1.1 <a href="#v3-1-1" class="anchor">#</a>

<span class="date">June 20, 2018</span> <span class="badge minor">minor</span>

**Fixes:**

- Fixed issue where new permissions were not being added to database on upgrades

<a href="cloudcannon:collections/_posts/2018-06-20-v3.1.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.1.0 <a href="#v3-1-0" class="anchor">#</a>

<span class="date">June 19, 2018</span> <span class="badge major">major</span>

**Features:**

- Support for advanced auditing workflow to easily triage findings
- Support for external repositories to retrieve additional component metadata from
- Support for SPDX 3.1 license IDs
- NVD mirroring support for Dependency-Check (and other) clients
- Support for out-of-date version detection (rubygems, maven, and npm)
- Enhanced API to (optionally) autocreate project on bom/scan upload
- Better support for Dependency-Check “relatedDependencies”
- Added individual component metrics (independent of dependency metrics)
- Added per project and per component overview with metrics and refresh support
- Specific table columns can now be sorted with full pagination support
- Improved error logging when issues are encountered during BOM and scan processing
- Enhanced LDAP integration to support strong authentication mechanisms and configurable user formats
- General performance improvements on multi-core machines
- Minor enhancements to user interface

**Fixes:**

- Fixed defect that prevented paginated results on project tag searches
- Fixed defect affecting GAV identifiers in Dependency-Check Gradle/CLI reports not being in parenthesis

**Upgrade Notes:**

- The VULNERABILITY_ANALYSIS permission was introduced in this release. Existing users that need the ability to audit findings will need this permission added to their account or through their team membership.
- MySQL now requires ANSI_QUOTES to be added to the SQL mode. Refer to [Database Support](/getting-started/database-support/) for details.

<a href="cloudcannon:collections/_posts/2018-06-19-v3.1.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.0.4 <a href="#v3-0-4" class="anchor">#</a>

<span class="date">May 02, 2018</span> <span class="badge minor">minor</span>

**Fixes:**

- Fixed defect resulting in incorrect results returned when filtering on components in the project view
- Synced CycloneDX specification to latest v1.0.1 release

<a href="cloudcannon:collections/_posts/2018-05-02-v3.0.4.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.0.3 <a href="#v3-0-3" class="anchor">#</a>

<span class="date">April 13, 2018</span> <span class="badge minor">minor</span>

**Fixes:**

- Fixed defect resulting in incorrect vulnerability counts for projects
- Fixed defect which prevented project metrics from returning results
- Fixed issue related to the assignment of tags on project creation
- Added the VIEW_PORTFOLIO permission to the ‘automation’ team on new installs
- Updated several dependencies
- Performance improvements in database connection pool
- Fixed defect where database connections were not being reconnected if the connection was lost
- Fixed multiple defects related to component reconciliation when processing BOM and scan uploads

<a href="cloudcannon:collections/_posts/2018-04-13-v3.0.3.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.0.2 <a href="#v3-0-2" class="anchor">#</a>

<span class="date">March 30, 2018</span> <span class="badge minor">minor</span>

**Fixes:**

- Responded to changes in NVD data feed URLs by correcting the XML 1.2 and 2.0 URLs used for mirroring.

<a href="cloudcannon:collections/_posts/2018-03-30-v3.0.2.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.0.1 <a href="#v3-0-1" class="anchor">#</a>

<span class="date">March 29, 2018</span> <span class="badge minor">minor</span>

**Fixes:**

- Fixed data model issue which prevented multiple versions of the same project name from being persisted.
- Fixed issue in admin console which did not properly display the number of team members.

**Upgrade Notes:**

If v3.0.0 was deployed, shutdown Dependency-Track, execute the following statement against the database, and deploy v3.0.1.

<div class="language-sql highlighter-rouge">

<div class="highlight">

``` highlight
/*
Removes the constraint on having a unique project name thus preventing
multiple versions of the project from existing.
https://github.com/DependencyTrack/dependency-track/issues/118
*/
ALTER TABLE PROJECT DROP CONSTRAINT PROJECT_NAME_IDX;
```

</div>

</div>

<a href="cloudcannon:collections/_posts/2018-03-29-v3.0.1.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

<div class="changelog-item">

### v3.0.0 <a href="#v3-0-0" class="anchor">#</a>

<span class="date">March 27, 2018</span> <span class="badge major">major</span>

Project Reboot Successful! This is the first release after being developed from the ground up.

**Features:**

- Dramatically increases visibility into the use of vulnerable components
- Supports an unlimited number of projects and components
- Projects can range from applications, operating systems, firmware, to IoT devices
- Tracks vulnerabilities across entire project portfolio
- Tracks vulnerabilities by component
- Easily identify projects that are potentially vulnerable to newly published vulnerabilities
- Supports standardized SPDX license ID’s and tracks license use by component
- Supports CycloneDX and SPDX bill-of-material formats
- Easy to read metrics for components, projects, and portfolio
- API-first design facilitates easy integration with other systems
- API documentation available in Swagger 2.0 (OpenAPI 3 support coming soon)
- Flexible authentication supports internally managed users, Active Directory/LDAP, and API Keys
- Simple to install and configure. Get up and running in just a few minutes

**Fixes:**

<a href="cloudcannon:collections/_posts/2018-03-27-v3.0.0.md" class="btn"><strong>✎</strong> Update Entry</a>

</div>

</div>

</div>