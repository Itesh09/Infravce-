<div md-component="skip">

<a href="#vulnerability-scanning" class="md-skip">Skip to content</a>

</div>

<div md-component="announce">

</div>

<div md-color-scheme="default" md-component="outdated" hidden="">

<div class="md-banner__inner md-grid md-typeset">

You're not viewing the latest version of the documentation. [**Click here to go to latest.**](../../../..)

</div>

</div>

<div class="md-header md-header--shadow md-header--lifted" md-component="header">

<a href="../../.." class="md-header__button md-logo" aria-label="Trivy" data-md-component="logo" title="Trivy"><img src="../../../imgs/logo-white.svg" alt="logo" /></a> ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTMgNmgxOHYySDN6bTAgNWgxOHYySDN6bTAgNWgxOHYySDN6IiAvPjwvc3ZnPg==)

<div class="md-header__title" md-component="header-title">

<div class="md-header__ellipsis">

<div class="md-header__topic">

<span class="md-ellipsis"> Trivy </span>

</div>

<div class="md-header__topic" md-component="header-topic">

<span class="md-ellipsis"> Vulnerability </span>

</div>

</div>

</div>

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTkuNSAzQTYuNSA2LjUgMCAwIDEgMTYgOS41YzAgMS42MS0uNTkgMy4wOS0xLjU2IDQuMjNsLjI3LjI3aC43OWw1IDUtMS41IDEuNS01LTV2LS43OWwtLjI3LS4yN0E2LjUyIDYuNTIgMCAwIDEgOS41IDE2IDYuNSA2LjUgMCAwIDEgMyA5LjUgNi41IDYuNSAwIDAgMSA5LjUgM20wIDJDNyA1IDUgNyA1IDkuNVM3IDE0IDkuNSAxNCAxNCAxMiAxNCA5LjUgMTIgNSA5LjUgNSIgLz48L3N2Zz4=)

<div class="md-search" md-component="search" role="dialog">

<div class="md-search__inner" role="search">

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTkuNSAzQTYuNSA2LjUgMCAwIDEgMTYgOS41YzAgMS42MS0uNTkgMy4wOS0xLjU2IDQuMjNsLjI3LjI3aC43OWw1IDUtMS41IDEuNS01LTV2LS43OWwtLjI3LS4yN0E2LjUyIDYuNTIgMCAwIDEgOS41IDE2IDYuNSA2LjUgMCAwIDEgMyA5LjUgNi41IDYuNSAwIDAgMSA5LjUgM20wIDJDNyA1IDUgNyA1IDkuNVM3IDE0IDkuNSAxNCAxNCAxMiAxNCA5LjUgMTIgNSA5LjUgNSIgLz48L3N2Zz4=) ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTIwIDExdjJIOGw1LjUgNS41LTEuNDIgMS40Mkw0LjE2IDEybDcuOTItNy45MkwxMy41IDUuNSA4IDExeiIgLz48L3N2Zz4=)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTE5IDYuNDEgMTcuNTkgNSAxMiAxMC41OSA2LjQxIDUgNSA2LjQxIDEwLjU5IDEyIDUgMTcuNTkgNi40MSAxOSAxMiAxMy40MSAxNy41OSAxOSAxOSAxNy41OSAxMy40MSAxMnoiIC8+PC9zdmc+)

<div class="md-search__output">

<div class="md-search__scrollwrap" tabindex="0" md-scrollfix="">

<div class="md-search-result" md-component="search-result">

<div class="md-search-result__meta">

Initializing search

</div>

</div>

</div>

</div>

</div>

</div>

<div class="md-header__source">

<a href="https://github.com/aquasecurity/trivy" class="md-source" data-md-component="source" title="Go to repository"></a>

<div class="md-source__icon md-icon">

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCA0NDggNTEyIj48IS0tISBGb250IEF3ZXNvbWUgRnJlZSA3LjEuMCBieSBAZm9udGF3ZXNvbWUgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbSBMaWNlbnNlIC0gaHR0cHM6Ly9mb250YXdlc29tZS5jb20vbGljZW5zZS9mcmVlIChJY29uczogQ0MgQlkgNC4wLCBGb250czogU0lMIE9GTCAxLjEsIENvZGU6IE1JVCBMaWNlbnNlKSBDb3B5cmlnaHQgMjAyNSBGb250aWNvbnMsIEluYy4tLT48cGF0aCBkPSJNNDM5LjYgMjM2LjEgMjQ0IDQwLjVjLTUuNC01LjUtMTIuOC04LjUtMjAuNC04LjVzLTE1IDMtMjAuNCA4LjRMMTYyLjUgODFsNTEuNSA1MS41YzI3LjEtOS4xIDUyLjcgMTYuOCA0My40IDQzLjdsNDkuNyA0OS43YzM0LjItMTEuOCA2MS4yIDMxIDM1LjUgNTYuNy0yNi41IDI2LjUtNzAuMi0yLjktNTYtMzcuM0wyNDAuMyAxOTl2MTIxLjljMjUuMyAxMi41IDIyLjMgNDEuOCA5LjEgNTUtNi40IDYuNC0xNS4yIDEwLjEtMjQuMyAxMC4xcy0xNy44LTMuNi0yNC4zLTEwLjFjLTE3LjYtMTcuNi0xMS4xLTQ2LjkgMTEuMi01NnYtMTIzYy0yMC44LTguNS0yNC42LTMwLjctMTguNi00NUwxNDIuNiAxMDEgOC41IDIzNS4xQzMgMjQwLjYgMCAyNDcuOSAwIDI1NS41czMgMTUgOC41IDIwLjRsMTk1LjYgMTk1LjdjNS40IDUuNCAxMi43IDguNCAyMC40IDguNHMxNS0zIDIwLjQtOC40bDE5NC43LTE5NC43YzUuNC01LjQgOC40LTEyLjggOC40LTIwLjRzLTMtMTUtOC40LTIwLjQiIC8+PC9zdmc+)

</div>

<div class="md-source__repository">

GitHub

</div>

</div>

<div class="md-grid">

- <a href="../../../../../" class="md-tabs__link">Home</a>
- <a href="../../../getting-started/" class="md-tabs__link">Getting Started</a>
- <a href="../../../tutorials/overview/" class="md-tabs__link">Tutorials</a>
- <a href="../../" class="md-tabs__link">User Guide</a>
- <a href="../../../ecosystem/" class="md-tabs__link">Ecosystem</a>
- <a href="../../../community/principles/" class="md-tabs__link">Contributing</a>
- <a href="../../../commercial/compare/" class="md-tabs__link">Enterprise</a>

</div>

</div>

<div class="md-container" md-component="container">

<div class="md-main" role="main" md-component="main">

<div class="md-main__inner md-grid">

<div class="md-sidebar md-sidebar--primary" md-component="sidebar" md-type="navigation">

<div class="md-sidebar__scrollwrap">

<div class="md-sidebar__inner">

<a href="../../.." class="md-nav__button md-logo" aria-label="Trivy" data-md-component="logo" title="Trivy"><img src="../../../imgs/logo-white.svg" alt="logo" /></a> Trivy

<div class="md-nav__source">

<a href="https://github.com/aquasecurity/trivy" class="md-source" data-md-component="source" title="Go to repository"></a>

<div class="md-source__icon md-icon">

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCA0NDggNTEyIj48IS0tISBGb250IEF3ZXNvbWUgRnJlZSA3LjEuMCBieSBAZm9udGF3ZXNvbWUgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbSBMaWNlbnNlIC0gaHR0cHM6Ly9mb250YXdlc29tZS5jb20vbGljZW5zZS9mcmVlIChJY29uczogQ0MgQlkgNC4wLCBGb250czogU0lMIE9GTCAxLjEsIENvZGU6IE1JVCBMaWNlbnNlKSBDb3B5cmlnaHQgMjAyNSBGb250aWNvbnMsIEluYy4tLT48cGF0aCBkPSJNNDM5LjYgMjM2LjEgMjQ0IDQwLjVjLTUuNC01LjUtMTIuOC04LjUtMjAuNC04LjVzLTE1IDMtMjAuNCA4LjRMMTYyLjUgODFsNTEuNSA1MS41YzI3LjEtOS4xIDUyLjcgMTYuOCA0My40IDQzLjdsNDkuNyA0OS43YzM0LjItMTEuOCA2MS4yIDMxIDM1LjUgNTYuNy0yNi41IDI2LjUtNzAuMi0yLjktNTYtMzcuM0wyNDAuMyAxOTl2MTIxLjljMjUuMyAxMi41IDIyLjMgNDEuOCA5LjEgNTUtNi40IDYuNC0xNS4yIDEwLjEtMjQuMyAxMC4xcy0xNy44LTMuNi0yNC4zLTEwLjFjLTE3LjYtMTcuNi0xMS4xLTQ2LjkgMTEuMi01NnYtMTIzYy0yMC44LTguNS0yNC42LTMwLjctMTguNi00NUwxNDIuNiAxMDEgOC41IDIzNS4xQzMgMjQwLjYgMCAyNDcuOSAwIDI1NS41czMgMTUgOC41IDIwLjRsMTk1LjYgMTk1LjdjNS40IDUuNCAxMi43IDguNCAyMC40IDguNHMxNS0zIDIwLjQtOC40bDE5NC43LTE5NC43YzUuNC01LjQgOC40LTEyLjggOC40LTIwLjRzLTMtMTUtOC40LTIwLjQiIC8+PC9zdmc+)

</div>

<div class="md-source__repository">

GitHub

</div>

</div>

<a href="../../../../../" class="md-nav__link"><span class="md-ellipsis"> Home </span></a>

<span class="md-ellipsis"> Getting Started </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Getting Started

- <a href="../../../getting-started/" class="md-nav__link"><span class="md-ellipsis"> First steps </span></a>
- <a href="../../../getting-started/installation/" class="md-nav__link"><span class="md-ellipsis"> Installation </span></a>
- <a href="../../../getting-started/signature-verification/" class="md-nav__link"><span class="md-ellipsis"> Signature Verification </span></a>
- <a href="../../../getting-started/faq/" class="md-nav__link"><span class="md-ellipsis"> FAQ </span></a>

<span class="md-ellipsis"> Tutorials </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Tutorials

<a href="../../../tutorials/overview/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>

<span class="md-ellipsis"> CI/CD </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> CI/CD

- <a href="../../../tutorials/integrations/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../../tutorials/integrations/github-actions/" class="md-nav__link"><span class="md-ellipsis"> GitHub Actions </span></a>
- <a href="../../../tutorials/integrations/circleci/" class="md-nav__link"><span class="md-ellipsis"> CircleCI </span></a>
- <a href="../../../tutorials/integrations/travis-ci/" class="md-nav__link"><span class="md-ellipsis"> Travis CI </span></a>
- <a href="../../../tutorials/integrations/gitlab-ci/" class="md-nav__link"><span class="md-ellipsis"> GitLab CI </span></a>
- <a href="../../../tutorials/integrations/bitbucket/" class="md-nav__link"><span class="md-ellipsis"> Bitbucket Pipelines </span></a>
- <a href="../../../tutorials/integrations/aws-codepipeline/" class="md-nav__link"><span class="md-ellipsis"> AWS CodePipeline </span></a>
- <a href="../../../tutorials/integrations/aws-security-hub/" class="md-nav__link"><span class="md-ellipsis"> AWS Security Hub </span></a>
- <a href="../../../tutorials/integrations/azure-devops/" class="md-nav__link"><span class="md-ellipsis"> Azure </span></a>

<span class="md-ellipsis"> Kubernetes </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Kubernetes

- <a href="../../../tutorials/kubernetes/cluster-scanning/" class="md-nav__link"><span class="md-ellipsis"> Cluster Scanning </span></a>
- <a href="../../../tutorials/kubernetes/kyverno/" class="md-nav__link"><span class="md-ellipsis"> Kyverno </span></a>
- <a href="../../../tutorials/kubernetes/gitops/" class="md-nav__link"><span class="md-ellipsis"> GitOps </span></a>

<span class="md-ellipsis"> Misconfiguration </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Misconfiguration

- <a href="../../../tutorials/misconfiguration/terraform/" class="md-nav__link"><span class="md-ellipsis"> Terraform scanning </span></a>
- <a href="../../../tutorials/misconfiguration/custom-checks/" class="md-nav__link"><span class="md-ellipsis"> Custom Checks with Rego </span></a>

<span class="md-ellipsis"> Signing </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Signing

- <a href="../../../tutorials/signing/vuln-attestation/" class="md-nav__link"><span class="md-ellipsis"> Vulnerability Scan Record Attestation </span></a>

<span class="md-ellipsis"> Shell </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Shell

- <a href="../../../tutorials/shell/shell-completion/" class="md-nav__link"><span class="md-ellipsis"> Completion </span></a>

<span class="md-ellipsis"> Additional Resources </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Additional Resources

- <a href="../../../tutorials/additional-resources/references/" class="md-nav__link"><span class="md-ellipsis"> Additional Resources </span></a>
- <a href="../../../tutorials/additional-resources/community/" class="md-nav__link"><span class="md-ellipsis"> Community References </span></a>
- <a href="../../../tutorials/additional-resources/cks/" class="md-nav__link"><span class="md-ellipsis"> CKS Reference </span></a>

<span class="md-ellipsis"> User Guide </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> User Guide

<a href="../../" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>

<span class="md-ellipsis"> Target </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Target

- <a href="../../target/container_image/" class="md-nav__link"><span class="md-ellipsis"> Container Image </span></a>
- <a href="../../target/filesystem/" class="md-nav__link"><span class="md-ellipsis"> Filesystem </span></a>
- <a href="../../target/rootfs/" class="md-nav__link"><span class="md-ellipsis"> Rootfs </span></a>
- <a href="../../target/repository/" class="md-nav__link"><span class="md-ellipsis"> Code Repository </span></a>
- <a href="../../target/vm/" class="md-nav__link"><span class="md-ellipsis"> Virtual Machine Image </span></a>
- <a href="../../target/kubernetes/" class="md-nav__link"><span class="md-ellipsis"> Kubernetes </span></a>
- <a href="../../target/sbom/" class="md-nav__link"><span class="md-ellipsis"> SBOM </span></a>

<span class="md-ellipsis"> Scanner </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Scanner

<span class="md-ellipsis"> Vulnerability </span> <span class="md-nav__icon md-icon"></span> <a href="./" class="md-nav__link md-nav__link--active"><span class="md-ellipsis"> Vulnerability </span></a>

<span class="md-nav__icon md-icon"></span> Table of contents

- <a href="#os-packages" class="md-nav__link"><span class="md-ellipsis"> OS Packages </span></a>
  - <a href="#supported-os" class="md-nav__link"><span class="md-ellipsis"> Supported OS </span></a>
  - <a href="#data-sources" class="md-nav__link"><span class="md-ellipsis"> Data Sources </span></a>
    - <a href="#data-source-selection" class="md-nav__link"><span class="md-ellipsis"> Data Source Selection </span></a>
    - <a href="#severity-selection" class="md-nav__link"><span class="md-ellipsis"> Severity Selection </span></a>
  - <a href="#third-party-packages" class="md-nav__link"><span class="md-ellipsis"> Third-Party Packages </span></a>
  - <a href="#unfixed-vulnerabilities" class="md-nav__link"><span class="md-ellipsis"> Unfixed Vulnerabilities </span></a>
- <a href="#language-specific-packages" class="md-nav__link"><span class="md-ellipsis"> Language-specific Packages </span></a>
  - <a href="#supported-languages" class="md-nav__link"><span class="md-ellipsis"> Supported Languages </span></a>
  - <a href="#langpkg-data-sources" class="md-nav__link"><span class="md-ellipsis"> Data Sources </span></a>
- <a href="#non-packaged-software" class="md-nav__link"><span class="md-ellipsis"> Non-packaged software </span></a>
- <a href="#detection-behavior" class="md-nav__link"><span class="md-ellipsis"> Detection Behavior </span></a>
  - <a href="#handling-software-installed-via-os-packages" class="md-nav__link"><span class="md-ellipsis"> Handling Software Installed via OS Packages </span></a>
  - <a href="#handling-packages-with-unspecified-versions" class="md-nav__link"><span class="md-ellipsis"> Handling Packages with Unspecified Versions </span></a>
- <a href="#package-detection" class="md-nav__link"><span class="md-ellipsis"> Package Detection </span></a>
  - <a href="#detection-priority" class="md-nav__link"><span class="md-ellipsis"> Detection Priority </span></a>
  - <a href="#enabling-a-subset-of-package-types" class="md-nav__link"><span class="md-ellipsis"> Enabling a Subset of Package Types </span></a>
  - <a href="#filtering-by-package-relationships" class="md-nav__link"><span class="md-ellipsis"> Filtering by Package Relationships </span></a>
- <a href="#kubernetes" class="md-nav__link"><span class="md-ellipsis"> Kubernetes </span></a>
  - <a href="#data-sources_1" class="md-nav__link"><span class="md-ellipsis"> Data Sources </span></a>
- <a href="#databases" class="md-nav__link"><span class="md-ellipsis"> Databases </span></a>
- <a href="#configuration" class="md-nav__link"><span class="md-ellipsis"> Configuration </span></a>
  - <a href="#overriding-os-version" class="md-nav__link"><span class="md-ellipsis"> Overriding OS version </span></a>
  - <a href="#severity-selection_1" class="md-nav__link"><span class="md-ellipsis"> Severity selection </span></a>

<span class="md-ellipsis"> Misconfiguration </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Misconfiguration

<a href="../misconfiguration/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>

<a href="../misconfiguration/config/config/" class="md-nav__link"><span class="md-ellipsis"> Configuration </span></a>

<span class="md-ellipsis"> Policy </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Policy

- <a href="../misconfiguration/check/builtin/" class="md-nav__link"><span class="md-ellipsis"> Built-in Checks </span></a>

<span class="md-ellipsis"> Custom Checks </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Custom Checks

- <a href="../misconfiguration/custom/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../misconfiguration/custom/data/" class="md-nav__link"><span class="md-ellipsis"> Data </span></a>
- <a href="../misconfiguration/custom/combine/" class="md-nav__link"><span class="md-ellipsis"> Combine </span></a>
- <a href="../misconfiguration/custom/selectors/" class="md-nav__link"><span class="md-ellipsis"> Selectors </span></a>
- <a href="../misconfiguration/custom/schema/" class="md-nav__link"><span class="md-ellipsis"> Schemas </span></a>
- <a href="../misconfiguration/custom/testing/" class="md-nav__link"><span class="md-ellipsis"> Testing </span></a>
- <a href="../misconfiguration/custom/debug/" class="md-nav__link"><span class="md-ellipsis"> Debugging Policies </span></a>
- <a href="../misconfiguration/custom/contribute-checks/" class="md-nav__link"><span class="md-ellipsis"> Contribute Checks </span></a>

<a href="../secret/" class="md-nav__link"><span class="md-ellipsis"> Secret </span></a>

<a href="../license/" class="md-nav__link"><span class="md-ellipsis"> License </span></a>

<span class="md-ellipsis"> Coverage </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Coverage

<a href="../../coverage/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>

<span class="md-ellipsis"> OS </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> OS

- <a href="../../coverage/os/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../coverage/os/alma/" class="md-nav__link"><span class="md-ellipsis"> AlmaLinux </span></a>
- <a href="../../coverage/os/alpine/" class="md-nav__link"><span class="md-ellipsis"> Alpine Linux </span></a>
- <a href="../../coverage/os/amazon/" class="md-nav__link"><span class="md-ellipsis"> Amazon Linux </span></a>
- <a href="../../coverage/os/azure/" class="md-nav__link"><span class="md-ellipsis"> Azure Linux (CBL-Mariner) </span></a>
- <a href="../../coverage/os/bottlerocket/" class="md-nav__link"><span class="md-ellipsis"> Bottlerocket </span></a>
- <a href="../../coverage/os/centos/" class="md-nav__link"><span class="md-ellipsis"> CentOS </span></a>
- <a href="../../coverage/os/chainguard/" class="md-nav__link"><span class="md-ellipsis"> Chainguard </span></a>
- <a href="../../coverage/os/coreos/" class="md-nav__link"><span class="md-ellipsis"> CoreOS </span></a>
- <a href="../../coverage/os/debian/" class="md-nav__link"><span class="md-ellipsis"> Debian </span></a>
- <a href="../../coverage/os/echo/" class="md-nav__link"><span class="md-ellipsis"> Echo </span></a>
- <a href="../../coverage/os/minimos/" class="md-nav__link"><span class="md-ellipsis"> MinimOS </span></a>
- <a href="../../coverage/os/oracle/" class="md-nav__link"><span class="md-ellipsis"> Oracle Linux </span></a>
- <a href="../../coverage/os/photon/" class="md-nav__link"><span class="md-ellipsis"> Photon OS </span></a>
- <a href="../../coverage/os/rhel/" class="md-nav__link"><span class="md-ellipsis"> Red Hat </span></a>
- <a href="../../coverage/os/rocky/" class="md-nav__link"><span class="md-ellipsis"> Rocky Linux </span></a>
- <a href="../../coverage/os/suse/" class="md-nav__link"><span class="md-ellipsis"> SUSE </span></a>
- <a href="../../coverage/os/ubuntu/" class="md-nav__link"><span class="md-ellipsis"> Ubuntu </span></a>
- <a href="../../coverage/os/wolfi/" class="md-nav__link"><span class="md-ellipsis"> Wolfi </span></a>
- <a href="../../coverage/os/google-distroless/" class="md-nav__link"><span class="md-ellipsis"> Google Distroless (Images) </span></a>

<span class="md-ellipsis"> Language </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Language

- <a href="../../coverage/language/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../coverage/language/c/" class="md-nav__link"><span class="md-ellipsis"> C/C++ </span></a>
- <a href="../../coverage/language/dart/" class="md-nav__link"><span class="md-ellipsis"> Dart </span></a>
- <a href="../../coverage/language/dotnet/" class="md-nav__link"><span class="md-ellipsis"> .NET </span></a>
- <a href="../../coverage/language/elixir/" class="md-nav__link"><span class="md-ellipsis"> Elixir </span></a>
- <a href="../../coverage/language/golang/" class="md-nav__link"><span class="md-ellipsis"> Go </span></a>
- <a href="../../coverage/language/java/" class="md-nav__link"><span class="md-ellipsis"> Java </span></a>
- <a href="../../coverage/language/julia/" class="md-nav__link"><span class="md-ellipsis"> Julia </span></a>
- <a href="../../coverage/language/nodejs/" class="md-nav__link"><span class="md-ellipsis"> Node.js </span></a>
- <a href="../../coverage/language/php/" class="md-nav__link"><span class="md-ellipsis"> PHP </span></a>
- <a href="../../coverage/language/python/" class="md-nav__link"><span class="md-ellipsis"> Python </span></a>
- <a href="../../coverage/language/ruby/" class="md-nav__link"><span class="md-ellipsis"> Ruby </span></a>
- <a href="../../coverage/language/rust/" class="md-nav__link"><span class="md-ellipsis"> Rust </span></a>
- <a href="../../coverage/language/swift/" class="md-nav__link"><span class="md-ellipsis"> Swift </span></a>

<span class="md-ellipsis"> IaC </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> IaC

- <a href="../../coverage/iac/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../coverage/iac/ansible/" class="md-nav__link"><span class="md-ellipsis"> Ansible </span></a>
- <a href="../../coverage/iac/azure-arm/" class="md-nav__link"><span class="md-ellipsis"> Azure ARM Template </span></a>
- <a href="../../coverage/iac/cloudformation/" class="md-nav__link"><span class="md-ellipsis"> CloudFormation </span></a>
- <a href="../../coverage/iac/docker/" class="md-nav__link"><span class="md-ellipsis"> Docker </span></a>
- <a href="../../coverage/iac/helm/" class="md-nav__link"><span class="md-ellipsis"> Helm </span></a>
- <a href="../../coverage/iac/kubernetes/" class="md-nav__link"><span class="md-ellipsis"> Kubernetes </span></a>
- <a href="../../coverage/iac/terraform/" class="md-nav__link"><span class="md-ellipsis"> Terraform </span></a>

<span class="md-ellipsis"> Others </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Others

- <a href="../../coverage/others/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../coverage/others/activestate/" class="md-nav__link"><span class="md-ellipsis"> ActiveState Images </span></a>
- <a href="../../coverage/others/bitnami/" class="md-nav__link"><span class="md-ellipsis"> Bitnami Images </span></a>
- <a href="../../coverage/others/conda/" class="md-nav__link"><span class="md-ellipsis"> Conda </span></a>
- <a href="../../coverage/others/rapidfort/" class="md-nav__link"><span class="md-ellipsis"> RapidFort Images </span></a>
- <a href="../../coverage/others/rootio/" class="md-nav__link"><span class="md-ellipsis"> Root.io Images </span></a>
- <a href="../../coverage/others/seal/" class="md-nav__link"><span class="md-ellipsis"> Seal Security </span></a>
- <a href="../../coverage/others/rpm/" class="md-nav__link"><span class="md-ellipsis"> RPM Archives </span></a>

<a href="../../coverage/kubernetes/" class="md-nav__link"><span class="md-ellipsis"> Kubernetes </span></a>

<span class="md-ellipsis"> Configuration </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Configuration

- <a href="../../configuration/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../configuration/filtering/" class="md-nav__link"><span class="md-ellipsis"> Filtering </span></a>
- <a href="../../configuration/skipping/" class="md-nav__link"><span class="md-ellipsis"> Selecting Files </span></a>
- <a href="../../configuration/reporting/" class="md-nav__link"><span class="md-ellipsis"> Reporting </span></a>
- <a href="../../configuration/cache/" class="md-nav__link"><span class="md-ellipsis"> Cache </span></a>
- <a href="../../configuration/db/" class="md-nav__link"><span class="md-ellipsis"> Databases </span></a>
- <a href="../../configuration/others/" class="md-nav__link"><span class="md-ellipsis"> Others </span></a>

<span class="md-ellipsis"> Supply Chain </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Supply Chain

<a href="../../supply-chain/sbom/" class="md-nav__link"><span class="md-ellipsis"> SBOM </span></a>

<span class="md-ellipsis"> Attestation </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Attestation

- <a href="../../supply-chain/attestation/sbom/" class="md-nav__link"><span class="md-ellipsis"> SBOM </span></a>
- <a href="../../supply-chain/attestation/vuln/" class="md-nav__link"><span class="md-ellipsis"> Cosign Vulnerability Scan Record </span></a>
- <a href="../../supply-chain/attestation/rekor/" class="md-nav__link"><span class="md-ellipsis"> SBOM Attestation in Rekor </span></a>

<span class="md-ellipsis"> VEX </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> VEX

- <a href="../../supply-chain/vex/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../supply-chain/vex/repo/" class="md-nav__link"><span class="md-ellipsis"> VEX Repository </span></a>
- <a href="../../supply-chain/vex/file/" class="md-nav__link"><span class="md-ellipsis"> Local VEX Files </span></a>
- <a href="../../supply-chain/vex/sbom-ref/" class="md-nav__link"><span class="md-ellipsis"> VEX SBOM Reference </span></a>
- <a href="../../supply-chain/vex/oci/" class="md-nav__link"><span class="md-ellipsis"> VEX Attestation </span></a>

<span class="md-ellipsis"> Compliance </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Compliance

- <a href="../../compliance/compliance/" class="md-nav__link"><span class="md-ellipsis"> Built-in Compliance </span></a>
- <a href="../../compliance/contrib-compliance/" class="md-nav__link"><span class="md-ellipsis"> Custom Compliance </span></a>

<span class="md-ellipsis"> Plugins </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Plugins

- <a href="../../plugin/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../plugin/user-guide/" class="md-nav__link"><span class="md-ellipsis"> User guide </span></a>
- <a href="../../plugin/developer-guide/" class="md-nav__link"><span class="md-ellipsis"> Developer guide </span></a>

<span class="md-ellipsis"> Advanced </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Advanced

<a href="../../advanced/modules/" class="md-nav__link"><span class="md-ellipsis"> Modules </span></a>

<a href="../../advanced/air-gap/" class="md-nav__link"><span class="md-ellipsis"> Connectivity and Network considerations </span></a>

<a href="../../advanced/self-hosting/" class="md-nav__link"><span class="md-ellipsis"> Self-Hosting Trivy's Databases </span></a>

<span class="md-ellipsis"> Container Image </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Container Image

<a href="../../advanced/container/embed-in-dockerfile/" class="md-nav__link"><span class="md-ellipsis"> Embed in Dockerfile </span></a>

<a href="../../advanced/container/unpacked-filesystem/" class="md-nav__link"><span class="md-ellipsis"> Unpacked container image filesystem </span></a>

<span class="md-ellipsis"> Private Docker Registries </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Private Docker Registries

- <a href="../../advanced/private-registries/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../advanced/private-registries/docker-hub/" class="md-nav__link"><span class="md-ellipsis"> Docker Hub </span></a>
- <a href="../../advanced/private-registries/ecr/" class="md-nav__link"><span class="md-ellipsis"> AWS ECR (Elastic Container Registry) </span></a>
- <a href="../../advanced/private-registries/gar/" class="md-nav__link"><span class="md-ellipsis"> GAR (Google Artifact Registry) </span></a>
- <a href="../../advanced/private-registries/acr/" class="md-nav__link"><span class="md-ellipsis"> ACR (Azure Container Registry) </span></a>
- <a href="../../advanced/private-registries/self/" class="md-nav__link"><span class="md-ellipsis"> Self-Hosted </span></a>

<a href="../../advanced/telemetry/" class="md-nav__link"><span class="md-ellipsis"> Usage Telemetry </span></a>

<span class="md-ellipsis"> References </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> References

<span class="md-ellipsis"> Configuration </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Configuration

<span class="md-ellipsis"> CLI </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> CLI

<a href="../../references/configuration/cli/trivy/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>

<a href="../../references/configuration/cli/trivy_clean/" class="md-nav__link"><span class="md-ellipsis"> Clean </span></a>

<a href="../../references/configuration/cli/trivy_config/" class="md-nav__link"><span class="md-ellipsis"> Config </span></a>

<a href="../../references/configuration/cli/trivy_convert/" class="md-nav__link"><span class="md-ellipsis"> Convert </span></a>

<a href="../../references/configuration/cli/trivy_filesystem/" class="md-nav__link"><span class="md-ellipsis"> Filesystem </span></a>

<a href="../../references/configuration/cli/trivy_image/" class="md-nav__link"><span class="md-ellipsis"> Image </span></a>

<a href="../../references/configuration/cli/trivy_kubernetes/" class="md-nav__link"><span class="md-ellipsis"> Kubernetes </span></a>

<span class="md-ellipsis"> Module </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Module

- <a href="../../references/configuration/cli/trivy_module/" class="md-nav__link"><span class="md-ellipsis"> Module </span></a>
- <a href="../../references/configuration/cli/trivy_module_install/" class="md-nav__link"><span class="md-ellipsis"> Module Install </span></a>
- <a href="../../references/configuration/cli/trivy_module_uninstall/" class="md-nav__link"><span class="md-ellipsis"> Module Uninstall </span></a>

<span class="md-ellipsis"> Plugin </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Plugin

- <a href="../../references/configuration/cli/trivy_plugin/" class="md-nav__link"><span class="md-ellipsis"> Plugin </span></a>
- <a href="../../references/configuration/cli/trivy_plugin_info/" class="md-nav__link"><span class="md-ellipsis"> Plugin Info </span></a>
- <a href="../../references/configuration/cli/trivy_plugin_install/" class="md-nav__link"><span class="md-ellipsis"> Plugin Install </span></a>
- <a href="../../references/configuration/cli/trivy_plugin_list/" class="md-nav__link"><span class="md-ellipsis"> Plugin List </span></a>
- <a href="../../references/configuration/cli/trivy_plugin_run/" class="md-nav__link"><span class="md-ellipsis"> Plugin Run </span></a>
- <a href="../../references/configuration/cli/trivy_plugin_uninstall/" class="md-nav__link"><span class="md-ellipsis"> Plugin Uninstall </span></a>
- <a href="../../references/configuration/cli/trivy_plugin_update/" class="md-nav__link"><span class="md-ellipsis"> Plugin Update </span></a>
- <a href="../../references/configuration/cli/trivy_plugin_upgrade/" class="md-nav__link"><span class="md-ellipsis"> Plugin Upgrade </span></a>
- <a href="../../references/configuration/cli/trivy_plugin_search/" class="md-nav__link"><span class="md-ellipsis"> Plugin Search </span></a>

<span class="md-ellipsis"> Registry </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Registry

- <a href="../../references/configuration/cli/trivy_registry/" class="md-nav__link"><span class="md-ellipsis"> Registry </span></a>
- <a href="../../references/configuration/cli/trivy_registry_login/" class="md-nav__link"><span class="md-ellipsis"> Registry Login </span></a>
- <a href="../../references/configuration/cli/trivy_registry_logout/" class="md-nav__link"><span class="md-ellipsis"> Registry Logout </span></a>

<a href="../../references/configuration/cli/trivy_repository/" class="md-nav__link"><span class="md-ellipsis"> Repository </span></a>

<a href="../../references/configuration/cli/trivy_rootfs/" class="md-nav__link"><span class="md-ellipsis"> Rootfs </span></a>

<a href="../../references/configuration/cli/trivy_sbom/" class="md-nav__link"><span class="md-ellipsis"> SBOM </span></a>

<a href="../../references/configuration/cli/trivy_server/" class="md-nav__link"><span class="md-ellipsis"> Server </span></a>

<a href="../../references/configuration/cli/trivy_version/" class="md-nav__link"><span class="md-ellipsis"> Version </span></a>

<span class="md-ellipsis"> VEX </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> VEX

- <a href="../../references/configuration/cli/trivy_vex/" class="md-nav__link"><span class="md-ellipsis"> VEX </span></a>
- <a href="../../references/configuration/cli/trivy_vex_repo_download/" class="md-nav__link"><span class="md-ellipsis"> VEX Download </span></a>
- <a href="../../references/configuration/cli/trivy_vex_repo_init/" class="md-nav__link"><span class="md-ellipsis"> VEX Init </span></a>
- <a href="../../references/configuration/cli/trivy_vex_repo_list/" class="md-nav__link"><span class="md-ellipsis"> VEX List </span></a>
- <a href="../../references/configuration/cli/trivy_vex_repo/" class="md-nav__link"><span class="md-ellipsis"> VEX Repo </span></a>

<a href="../../references/configuration/cli/trivy_vm/" class="md-nav__link"><span class="md-ellipsis"> VM </span></a>

<a href="../../references/configuration/config-file/" class="md-nav__link"><span class="md-ellipsis"> Config file </span></a>

<span class="md-ellipsis"> Modes </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Modes

- <a href="../../references/modes/standalone/" class="md-nav__link"><span class="md-ellipsis"> Standalone </span></a>
- <a href="../../references/modes/client-server/" class="md-nav__link"><span class="md-ellipsis"> Client/Server </span></a>

<a href="../../references/troubleshooting/" class="md-nav__link"><span class="md-ellipsis"> Troubleshooting </span></a>

<a href="../../references/terminology/" class="md-nav__link"><span class="md-ellipsis"> Terminology </span></a>

<a href="../../references/abbreviations/" class="md-nav__link"><span class="md-ellipsis"> Abbreviations </span></a>

<span class="md-ellipsis"> Ecosystem </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Ecosystem

- <a href="../../../ecosystem/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../../ecosystem/cicd/" class="md-nav__link"><span class="md-ellipsis"> CI/CD </span></a>
- <a href="../../../ecosystem/ide/" class="md-nav__link"><span class="md-ellipsis"> IDE and Dev tools </span></a>
- <a href="../../../ecosystem/prod/" class="md-nav__link"><span class="md-ellipsis"> Production and Clouds </span></a>
- <a href="../../../ecosystem/reporting/" class="md-nav__link"><span class="md-ellipsis"> Reporting </span></a>

<span class="md-ellipsis"> Contributing </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Contributing

<a href="../../../community/principles/" class="md-nav__link"><span class="md-ellipsis"> Principles </span></a>

<span class="md-ellipsis"> How to contribute </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> How to contribute

- <a href="../../../community/contribute/issue/" class="md-nav__link"><span class="md-ellipsis"> Issues </span></a>
- <a href="../../../community/contribute/discussion/" class="md-nav__link"><span class="md-ellipsis"> Discussions </span></a>
- <a href="../../../community/contribute/pr/" class="md-nav__link"><span class="md-ellipsis"> Pull Requests </span></a>

<span class="md-ellipsis"> Contribute Rego Checks </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Contribute Rego Checks

- <a href="../../../community/contribute/checks/overview/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../../community/contribute/checks/service-support/" class="md-nav__link"><span class="md-ellipsis"> Add Service Support </span></a>

<span class="md-ellipsis"> Contribute Vulnerability Data Sources </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Contribute Vulnerability Data Sources

- <a href="../../../community/contribute/vulnerability-database/overview/" class="md-nav__link"><span class="md-ellipsis"> Overview </span></a>
- <a href="../../../community/contribute/vulnerability-database/add-vulnerability-source/" class="md-nav__link"><span class="md-ellipsis"> Add Vulnerability Advisory Source </span></a>

<span class="md-ellipsis"> Maintainer </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Maintainer

- <a href="../../../community/maintainer/pr-review/" class="md-nav__link"><span class="md-ellipsis"> PR Review </span></a>
- <a href="../../../community/maintainer/release-flow/" class="md-nav__link"><span class="md-ellipsis"> Release Flow </span></a>
- <a href="../../../community/maintainer/backporting/" class="md-nav__link"><span class="md-ellipsis"> Backporting </span></a>
- <a href="../../../community/maintainer/help-wanted/" class="md-nav__link"><span class="md-ellipsis"> Help Wanted </span></a>
- <a href="../../../community/maintainer/triage/" class="md-nav__link"><span class="md-ellipsis"> Triage </span></a>

<span class="md-ellipsis"> Enterprise </span> <span class="md-nav__icon md-icon"></span>

<span class="md-nav__icon md-icon"></span> Enterprise

- <a href="../../../commercial/compare/" class="md-nav__link"><span class="md-ellipsis"> Comparison </span></a>
- <a href="../../../commercial/contact/" class="md-nav__link"><span class="md-ellipsis"> Contact Us </span></a>

</div>

</div>

</div>

<div class="md-sidebar md-sidebar--secondary" md-component="sidebar" md-type="toc">

<div class="md-sidebar__scrollwrap">

<div class="md-sidebar__inner">

<span class="md-nav__icon md-icon"></span> Table of contents

- <a href="#os-packages" class="md-nav__link"><span class="md-ellipsis"> OS Packages </span></a>
  - <a href="#supported-os" class="md-nav__link"><span class="md-ellipsis"> Supported OS </span></a>
  - <a href="#data-sources" class="md-nav__link"><span class="md-ellipsis"> Data Sources </span></a>
    - <a href="#data-source-selection" class="md-nav__link"><span class="md-ellipsis"> Data Source Selection </span></a>
    - <a href="#severity-selection" class="md-nav__link"><span class="md-ellipsis"> Severity Selection </span></a>
  - <a href="#third-party-packages" class="md-nav__link"><span class="md-ellipsis"> Third-Party Packages </span></a>
  - <a href="#unfixed-vulnerabilities" class="md-nav__link"><span class="md-ellipsis"> Unfixed Vulnerabilities </span></a>
- <a href="#language-specific-packages" class="md-nav__link"><span class="md-ellipsis"> Language-specific Packages </span></a>
  - <a href="#supported-languages" class="md-nav__link"><span class="md-ellipsis"> Supported Languages </span></a>
  - <a href="#langpkg-data-sources" class="md-nav__link"><span class="md-ellipsis"> Data Sources </span></a>
- <a href="#non-packaged-software" class="md-nav__link"><span class="md-ellipsis"> Non-packaged software </span></a>
- <a href="#detection-behavior" class="md-nav__link"><span class="md-ellipsis"> Detection Behavior </span></a>
  - <a href="#handling-software-installed-via-os-packages" class="md-nav__link"><span class="md-ellipsis"> Handling Software Installed via OS Packages </span></a>
  - <a href="#handling-packages-with-unspecified-versions" class="md-nav__link"><span class="md-ellipsis"> Handling Packages with Unspecified Versions </span></a>
- <a href="#package-detection" class="md-nav__link"><span class="md-ellipsis"> Package Detection </span></a>
  - <a href="#detection-priority" class="md-nav__link"><span class="md-ellipsis"> Detection Priority </span></a>
  - <a href="#enabling-a-subset-of-package-types" class="md-nav__link"><span class="md-ellipsis"> Enabling a Subset of Package Types </span></a>
  - <a href="#filtering-by-package-relationships" class="md-nav__link"><span class="md-ellipsis"> Filtering by Package Relationships </span></a>
- <a href="#kubernetes" class="md-nav__link"><span class="md-ellipsis"> Kubernetes </span></a>
  - <a href="#data-sources_1" class="md-nav__link"><span class="md-ellipsis"> Data Sources </span></a>
- <a href="#databases" class="md-nav__link"><span class="md-ellipsis"> Databases </span></a>
- <a href="#configuration" class="md-nav__link"><span class="md-ellipsis"> Configuration </span></a>
  - <a href="#overriding-os-version" class="md-nav__link"><span class="md-ellipsis"> Overriding OS version </span></a>
  - <a href="#severity-selection_1" class="md-nav__link"><span class="md-ellipsis"> Severity selection </span></a>

</div>

</div>

</div>

<div class="md-content" md-component="content">

<a href="https://github.com/aquasecurity/trivy/blob/main/docs/guide/scanner/vulnerability.md" class="md-content__button md-icon" rel="edit" title="Edit this page"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEwIDIwSDZWNGg3djVoNXYzLjFsMi0yVjhsLTYtNkg2Yy0xLjEgMC0yIC45LTIgMnYxNmMwIDEuMS45IDIgMiAyaDR6bTEwLjItN2MuMSAwIC4zLjEuNC4ybDEuMyAxLjNjLjIuMi4yLjYgMCAuOGwtMSAxLTIuMS0yLjEgMS0xYy4xLS4xLjItLjIuNC0uMm0wIDMuOUwxNC4xIDIzSDEydi0yLjFsNi4xLTYuMXoiIC8+PC9zdmc+" /></a>

# Vulnerability Scanning<a href="#vulnerability-scanning" class="headerlink" title="Permanent link">¶</a>

Trivy detects known vulnerabilities in software components that it finds in the scan target.

The following are supported:

- [OS packages](#os-packages)
- [Language-specific packages](#language-specific-packages)
- [Non-packaged software](#non-packaged-software)
- [Kubernetes components](#kubernetes)

## OS Packages<a href="#os-packages" class="headerlink" title="Permanent link">¶</a>

Trivy is capable of automatically detecting installed OS packages when scanning container images, VM images and running hosts.

<div class="admonition note">

Note

Trivy focuses on packages provided by official OS vendors and may skip [third-party packages](#third-party-packages).

</div>

### Supported OS<a href="#supported-os" class="headerlink" title="Permanent link">¶</a>

See [here](../../coverage/os/#supported-os) for the supported OSes.

### Data Sources<a href="#data-sources" class="headerlink" title="Permanent link">¶</a>

| OS                        | Source                                                                                                                 |
|---------------------------|------------------------------------------------------------------------------------------------------------------------|
| Arch Linux                | [Vulnerable Issues](https://security.archlinux.org/)                                                                   |
| Alpine Linux              | [secdb](https://secdb.alpinelinux.org/)                                                                                |
| Bottlerocket              | [Bottlerocket Security Advisories](https://advisories.bottlerocket.aws/)                                               |
| Wolfi Linux               | [secdb](https://packages.wolfi.dev/os/security.json)                                                                   |
| Chainguard                | [secdb](https://packages.cgr.dev/chainguard/security.json)                                                             |
| MinimOS                   | [secdb](https://packages.mini.dev/advisories/secdb/security.json)                                                      |
| Amazon Linux              | [Amazon Linux Security Center](https://alas.aws.amazon.com/)                                                           |
| Echo                      | [Echo](https://advisory.echohq.com/data.json)                                                                          |
| Debian                    | [Security Bug Tracker](https://security-tracker.debian.org/tracker/) / [OVAL](https://www.debian.org/security/oval/)   |
| Ubuntu                    | [Ubuntu CVE Tracker](https://ubuntu.com/security/cve)                                                                  |
| RHEL/CentOS               | [OVAL](https://www.redhat.com/security/data/oval/v2/) / [Security Data](https://www.redhat.com/security/data/metrics/) |
| AlmaLinux                 | [AlmaLinux Product Errata](https://errata.almalinux.org/)                                                              |
| Rocky Linux               | [Rocky Linux UpdateInfo](https://download.rockylinux.org/pub/rocky/)                                                   |
| Oracle Linux              | [OVAL](https://linux.oracle.com/security/oval/)                                                                        |
| Azure Linux (CBL-Mariner) | [OVAL](https://github.com/microsoft/AzureLinuxVulnerabilityData/)                                                      |
| OpenSUSE/SLES             | [CVRF](http://ftp.suse.com/pub/projects/security/cvrf/)                                                                |
| Photon OS                 | [Photon Security Advisory](https://packages.broadcom.com/photon/photon_cve_metadata/)                                  |
| RapidFort                 | [RapidFort Security Advisories](https://github.com/rapidfort/security-advisories)                                      |
| Root.io                   | [Root.io Patch Feed](https://api.root.io/external/patch_feed)                                                          |
| Seal Security             | [Seal Security vulnerability feed](http://vulnfeed.sealsecurity.io/v1/osv/renamed/vulnerabilities.zip)                 |

#### Data Source Selection<a href="#data-source-selection" class="headerlink" title="Permanent link">¶</a>

Trivy **only** consumes security advisories from the sources listed in the above table.

As for packages installed from OS package managers (`dpkg`, `yum`, `apk`, etc.), Trivy uses the advisory database from the appropriate **OS vendor**.

For example: for a python package installed from `yum` (Amazon linux), Trivy will only get advisories from [ALAS](https://alas.aws.amazon.com/). But for a python package installed from another source (e.g. `pip`), Trivy will get advisories from the `GitLab` and `GitHub` databases.

This advisory selection is essential to avoid getting false positives because OS vendors usually backport upstream fixes, and the fixed version can be different from the upstream fixed version.

#### Severity Selection<a href="#severity-selection" class="headerlink" title="Permanent link">¶</a>

The severity is taken from the selected data source since the severity from vendors is more accurate. Using CVE-2023-0464 as an example, while it is [rated as "HIGH" in NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-0464), Red Hat has marked its 'Impact' as ["Low"](https://access.redhat.com/security/cve/cve-2023-0464). As a result, Trivy will display it as "Low".

The severity depends on the compile option, the default configuration, etc. NVD doesn't know how the vendor distributes the software. Red Hat evaluates the severity more accurately. That's why Trivy prefers vendor scores over NVD.

If the data source does not provide a severity, the severity is determined based on the CVSS score as follows:

| Base Score Range | Severity |
|------------------|----------|
| 0.1-3.9          | Low      |
| 4.0-6.9          | Medium   |
| 7.0-8.9          | High     |
| 9.0-10.0         | Critical |

If the CVSS score is also not provided, it falls back to [NVD](https://nvd.nist.gov/vuln).

NVD and some vendors may delay severity analysis, while other vendors, such as Red Hat, are able to quickly evaluate and announce the severity of vulnerabilities. To avoid marking too many vulnerabilities as "UNKNOWN" severity, Trivy uses severity ratings from other vendors when the NVD information is not yet available. The order of preference for vendor severity data can be found [here](https://github.com/aquasecurity/trivy-db/blob/79d0fbd1e246f3c77eef4b9826fe4bf65940b221/pkg/vulnsrc/vulnerability/vulnerability.go#L17-L19).

You can reference `SeveritySource` in the [JSON reporting format](../../configuration/reporting/#json) to see from where the severity is taken for a given vulnerability.

<div class="highlight">

    "SeveritySource": "debian",

</div>

In addition, you can see all the vendor severity ratings.

<div class="highlight">

    "VendorSeverity": {
      "amazon": 2,
      "cbl-mariner": 4,
      "ghsa": 4,
      "nvd": 4,
      "photon": 4,
      "redhat": 2,
      "ubuntu": 2
    }

</div>

Here is the severity mapping in Trivy:

| Number | Severity |
|:------:|----------|
|   0    | Unknown  |
|   1    | Low      |
|   2    | Medium   |
|   3    | High     |
|   4    | Critical |

If no vendor has a severity, the `UNKNOWN` severity will be used.

### Third-Party Packages<a href="#third-party-packages" class="headerlink" title="Permanent link">¶</a>

Trivy skips vulnerability scanning for packages installed from third-party repositories (e.g., EPEL, Remi, Docker, NVIDIA) because they are not covered by official OS security advisories. Scanning these packages against official advisories would lead to false positives, as the advisories only track packages distributed by the OS vendor.

Trivy identifies third-party packages using heuristic methods such as checking the RPM vendor field or the APT source repository. Since this detection is heuristic-based, it may not identify all third-party packages. In such cases, unrecognized third-party packages will still be scanned against official advisories, which could result in false positives.

Conversely, packages from lesser-known but legitimate OS vendors may be incorrectly classified as third-party and skipped, leading to false negatives. If you notice such cases, please [report it](https://github.com/aquasecurity/trivy/discussions/new?category=bugs).

<div class="admonition note">

Note

This applies to packages that are matched against an OS vendor's advisories. A distribution whose own advisories describe the packages it rebuilds, such as [Echo](../../coverage/os/echo/) and [RapidFort](../../coverage/others/rapidfort/), scans them even when they are classified as third-party. [Seal Security](../../coverage/others/seal/) does both: its own `seal-*` packages are always scanned, while the remaining packages are matched against the base OS vendor's advisories and follow the rule above.

</div>

### Unfixed Vulnerabilities<a href="#unfixed-vulnerabilities" class="headerlink" title="Permanent link">¶</a>

The unfixed/unfixable vulnerabilities mean that the patch has not yet been provided on their distribution. To hide unfixed/unfixable vulnerabilities, you can use the `--ignore-unfixed` flag.

## Language-specific Packages<a href="#language-specific-packages" class="headerlink" title="Permanent link">¶</a>

### Supported Languages<a href="#supported-languages" class="headerlink" title="Permanent link">¶</a>

See [here](../../coverage/language/#supported-languages) for the supported languages.

### Data Sources<a href="#langpkg-data-sources" class="headerlink" title="Permanent link">¶</a>

| Language | Source                                                                                          | Commercial Use | Delay<sup><a href="#fn:1" class="footnote-ref">1</a></sup> |
|----------|-------------------------------------------------------------------------------------------------|:--------------:|:----------------------------------------------------------:|
| PHP      | [PHP Security Advisories Database](https://github.com/FriendsOfPHP/security-advisories)         |       ✅       |                             \-                             |
|          | [GitHub Advisory Database (Composer)](https://github.com/advisories?query=ecosystem%3Acomposer) |       ✅       |                             \-                             |
| Python   | [GitHub Advisory Database (pip)](https://github.com/advisories?query=ecosystem%3Apip)           |       ✅       |                             \-                             |
| Ruby     | [Ruby Advisory Database](https://github.com/rubysec/ruby-advisory-db)                           |       ✅       |                             \-                             |
|          | [GitHub Advisory Database (RubyGems)](https://github.com/advisories?query=ecosystem%3Arubygems) |       ✅       |                             \-                             |
| Node.js  | [Ecosystem Security Working Group](https://github.com/nodejs/security-wg)                       |       ✅       |                             \-                             |
|          | [GitHub Advisory Database (npm)](https://github.com/advisories?query=ecosystem%3Anpm)           |       ✅       |                             \-                             |
| Java     | [GitHub Advisory Database (Maven)](https://github.com/advisories?query=ecosystem%3Amaven)       |       ✅       |                             \-                             |
| Go       | [GitHub Advisory Database (Go)](https://github.com/advisories?query=ecosystem%3Ago)             |       ✅       |                             \-                             |
|          | [Go Vulnerability Database](https://pkg.go.dev/vuln/)                                           |       ✅       |                             \-                             |
| Rust     | [Open Source Vulnerabilities (crates.io)](https://osv.dev/list?q=&ecosystem=crates.io)          |       ✅       |                             \-                             |
| .NET     | [GitHub Advisory Database (NuGet)](https://github.com/advisories?query=ecosystem%3Anuget)       |       ✅       |                             \-                             |
| C/C++    | [GitLab Advisories Community](https://gitlab.com/gitlab-org/advisories-community)               |       ✅       |                          1 month                           |
| Dart     | [GitHub Advisory Database (Pub)](https://github.com/advisories?query=ecosystem%3Apub)           |       ✅       |                             \-                             |
| Elixir   | [GitHub Advisory Database (Erlang)](https://github.com/advisories?query=ecosystem%3Aerlang)     |       ✅       |                             \-                             |
| Swift    | [GitHub Advisory Database (Swift)](https://github.com/advisories?query=ecosystem%3Aswift)       |       ✅       |                             \-                             |
| Julia    | [Open Source Vulnerabilities (Julia)](https://osv.dev/list?q=&ecosystem=Julia)                  |       ✅       |                             \-                             |

## Non-packaged software<a href="#non-packaged-software" class="headerlink" title="Permanent link">¶</a>

If you have software that is not managed by a package manager, Trivy can still detect vulnerabilities in it in some cases:

- [Using SBOM from Sigstore Rekor](../../supply-chain/attestation/rekor/#non-packaged-binaries)
- [Go Binaries with embedded module information](../../coverage/language/golang/#go-binary)
- [Rust Binaries with embedded information](../../coverage/language/rust/#binaries)
- [SBOM embedded in container images](../../supply-chain/sbom/#sbom-detection-inside-targets)

## Detection Behavior<a href="#detection-behavior" class="headerlink" title="Permanent link">¶</a>

Trivy prioritizes precision in vulnerability detection, aiming to minimize false positives while potentially accepting some false negatives. This approach is particularly relevant in two key areas:

- [Handling Software Installed via OS Packages](#handling-software-installed-via-os-packages)
- [Handling Packages with Unspecified Versions](#handling-packages-with-unspecified-versions)

Trivy can also detect only specific packages:

- [Subset of Package Types](#enabling-a-subset-of-package-types)
- [Specific package Relationship](#filtering-by-package-relationships)

### Handling Software Installed via OS Packages<a href="#handling-software-installed-via-os-packages" class="headerlink" title="Permanent link">¶</a>

For files installed by OS package managers, such as `apt`, Trivy exclusively uses advisories from the OS vendor. This means that even if a JAR file is present in a container image, if it was installed via an OS package manager (e.g., `apt`), Trivy will not analyze the JAR file itself and use upstream security advisories.

For example, consider the Python `requests` package in Red Hat Universal Base Image 8:

<div class="highlight">

    [root@987ee49dc93d /]# head -n 3 /usr/lib/python3.6/site-packages/requests-2.20.0-py3.6.egg-info/PKG-INFO
    Metadata-Version: 2.1
    Name: requests
    Version: 2.20.0

</div>

Version 2.20.0 is installed, and this package is installed by `dnf`.

<div class="highlight">

    [root@987ee49dc93d /]# rpm -ql python3-requests | grep PKG-INFO
    /usr/lib/python3.6/site-packages/requests-2.20.0-py3.6.egg-info/PKG-INFO

</div>

At first glance, this might seem vulnerable to [CVE-2023-32681](https://nvd.nist.gov/vuln/detail/CVE-2023-32681), which affects versions of requests prior to v2.31.0. However, Red Hat backported the fix to v2.20.0-3 in [RHSA-2023:4520](https://access.redhat.com/errata/RHSA-2023:4520), and the package is not vulnerable.

- Upstream (PyPI [requests](https://pypi.org/project/requests/)): Fixed in v2.31.0
- Red Hat (`python-requests`): Backported fix applied in v2.20.0-3 (RHSA-2023:4520)

If Trivy were to detect CVE-2023-32681 in this case, it would be a false positive. This illustrates why using the correct security advisory is crucial to avoid false detections. To minimize false positives, Trivy trusts the OS vendor's advisory for software installed via OS package managers and does not use upstream advisories for these packages.

However, this approach may lead to false negatives if the OS vendor's advisories are delayed or missing. In such cases, using [--detection-priority comprehensive](#detection-priority) allows Trivy to consider upstream advisories (e.g., [GitHub Advisory Database](https://github.com/advisories)), potentially increasing false positives but reducing false negatives.

### Handling Packages with Unspecified Versions<a href="#handling-packages-with-unspecified-versions" class="headerlink" title="Permanent link">¶</a>

When a package version cannot be uniquely determined (e.g., `package-a: ">=3.0"`), Trivy typically skips vulnerability detection for that package to avoid false positives. If a lock file is present with fixed versions, Trivy will use those for detection.

To detect potential vulnerabilities even with unspecified versions, use [--detection-priority comprehensive](#detection-priority). This option makes Trivy use the minimum version in the specified range for vulnerability detection. While this may increase false positives if the actual version used is not the minimum, it helps reduce false negatives.

## Package Detection<a href="#package-detection" class="headerlink" title="Permanent link">¶</a>

Vulnerability detection is based on package detection. This section describes the specifics of package detection, which also affect SBOM generation.

### Detection Priority<a href="#detection-priority" class="headerlink" title="Permanent link">¶</a>

Trivy provides a `--detection-priority` flag to control the balance between false positives and false negatives in package/vulnerability detection. This concept is similar to the relationship between [precision and recall](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall) in machine learning evaluation.

<div class="highlight">

    $ trivy image --detection-priority {precise|comprehensive} alpine:3.15

</div>

- `precise`: This mode prioritizes reducing false positives. It results in less noisy vulnerability reports but may miss some potential vulnerabilities.
- `comprehensive`: This mode aims to detect more vulnerabilities, potentially including some that might be false positives. It provides broader coverage but may increase the noise in the results.

The default value is `precise`. Also refer to the [detection behavior](#detection-behavior) section for more information.

Regardless of the chosen mode, user review of detected vulnerabilities is crucial:

- `precise`: Review thoroughly, considering potential missed vulnerabilities.
- `comprehensive`: Carefully investigate each reported vulnerability due to increased false positive possibility.

### Enabling a Subset of Package Types<a href="#enabling-a-subset-of-package-types" class="headerlink" title="Permanent link">¶</a>

It's possible to only enable certain package types if you prefer. You can do so by passing the `--pkg-types` option. This flag takes a comma-separated list of package types.

Available values:

- os
  - Scan OS packages managed by the OS package manager (e.g. `dpkg`, `yum`, `apk`).
- library
  - Scan language-specific packages (e.g. packages installed by `pip`, `npm`, or `gem`).

<div class="highlight">

    $ trivy image --pkg-types os ruby:2.4.0

</div>

Result

<div class="highlight">

    2019-05-22T19:36:50.530+0200    [34mINFO[0m    Updating vulnerability database...
    2019-05-22T19:36:51.681+0200    [34mINFO[0m    Detecting Alpine vulnerabilities...
    2019-05-22T19:36:51.685+0200    [34mINFO[0m    Updating npm Security DB...
    2019-05-22T19:36:52.389+0200    [34mINFO[0m    Detecting npm vulnerabilities...
    2019-05-22T19:36:52.390+0200    [34mINFO[0m    Updating pipenv Security DB...
    2019-05-22T19:36:53.406+0200    [34mINFO[0m    Detecting pipenv vulnerabilities...

    ruby:2.4.0 (debian 8.7)
    =======================
    Total: 7 (UNKNOWN: 0, LOW: 1, MEDIUM: 1, HIGH: 3, CRITICAL: 2)

    +---------+------------------+----------+-------------------+---------------+----------------------------------+
    | LIBRARY | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |              TITLE               |
    +---------+------------------+----------+-------------------+---------------+----------------------------------+
    | curl    | CVE-2018-14618   | CRITICAL | 7.61.0-r0         | 7.61.1-r0     | curl: NTLM password overflow     |
    |         |                  |          |                   |               | via integer overflow             |
    +         +------------------+----------+                   +---------------+----------------------------------+
    |         | CVE-2018-16839   | HIGH     |                   | 7.61.1-r1     | curl: Integer overflow leading   |
    |         |                  |          |                   |               | to heap-based buffer overflow in |
    |         |                  |          |                   |               | Curl_sasl_create_plain_message() |
    +---------+------------------+----------+-------------------+---------------+----------------------------------+
    | git     | CVE-2018-17456   | HIGH     | 2.15.2-r0         | 2.15.3-r0     | git: arbitrary code execution    |
    |         |                  |          |                   |               | via .gitmodules                  |
    +         +------------------+          +                   +               +----------------------------------+
    |         | CVE-2018-19486   |          |                   |               | git: Improper handling of        |
    |         |                  |          |                   |               | PATH allows for commands to be   |
    |         |                  |          |                   |               | executed from...                 |
    +---------+------------------+----------+-------------------+---------------+----------------------------------+
    | libssh2 | CVE-2019-3855    | CRITICAL | 1.8.0-r2          | 1.8.1-r0      | libssh2: Integer overflow in     |
    |         |                  |          |                   |               | transport read resulting in      |
    |         |                  |          |                   |               | out of bounds write...           |
    +---------+------------------+----------+-------------------+---------------+----------------------------------+
    | sqlite  | CVE-2018-20346   | MEDIUM   | 3.21.0-r1         | 3.25.3-r0     | CVE-2018-20505 CVE-2018-20506    |
    |         |                  |          |                   |               | sqlite: Multiple flaws in        |
    |         |                  |          |                   |               | sqlite which can be triggered    |
    |         |                  |          |                   |               | via...                           |
    +---------+------------------+----------+-------------------+---------------+----------------------------------+
    | tar     | CVE-2018-20482   | LOW      | 1.29-r1           | 1.31-r0       | tar: Infinite read loop in       |
    |         |                  |          |                   |               | sparse_dump_region function in   |
    |         |                  |          |                   |               | sparse.c                         |
    +---------+------------------+----------+-------------------+---------------+----------------------------------+

</div>

<div class="admonition info">

Info

This flag filters the packages themselves, so it also affects the list of detected packages in JSON reports and SBOM generation.

</div>

### Filtering by Package Relationships<a href="#filtering-by-package-relationships" class="headerlink" title="Permanent link">¶</a>

Trivy supports filtering vulnerabilities based on the relationship of packages within a project. This is achieved through the `--pkg-relationships` flag. This feature allows you to focus on vulnerabilities in specific types of dependencies, such as only those in direct dependencies.

In Trivy, there are four types of package relationships:

1.  `root`: The root package being scanned
2.  `workspace`: Workspaces of the root package (Currently only `pom.xml`, `yarn.lock` and `cargo.lock` files are supported)
3.  `direct`: Direct dependencies of the root/workspace package
4.  `indirect`: Transitive dependencies
5.  `unknown`: Packages whose relationship cannot be determined

The available relationships may vary depending on the ecosystem. To see which relationships are supported for a particular project, you can use the JSON output format and check the `Relationship` field:

<div class="highlight">

    $ trivy repo -f json /path/to/project

</div>

To scan only the root package and its direct dependencies, you can use the flag as follows:

<div class="highlight">

    $ trivy repo --pkg-relationships root,direct /path/to/project

</div>

By default, all relationships are included in the scan.

<div class="admonition info">

Info

This flag filters the packages themselves, so it also affects the list of detected packages in JSON reports and SBOM generation.

</div>

<div class="admonition warning">

Warning

As it may not provide a complete package list, `--pkg-relationships` cannot be used with `--dependency-tree`, `--vex` or SBOM generation.

</div>

## Kubernetes<a href="#kubernetes" class="headerlink" title="Permanent link">¶</a>

Trivy can detect vulnerabilities in Kubernetes clusters and components by scanning a Kubernetes Cluster, or a KBOM (Kubernetes bill of Material). To learn more, see the [documentation for Kubernetes scanning](../../target/kubernetes/).

### Data Sources<a href="#data-sources_1" class="headerlink" title="Permanent link">¶</a>

| Vendor     | Source                                                                                                                                                       |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Kubernetes | [Kubernetes Official CVE feed](https://kubernetes.io/docs/reference/issues-security/official-cve-feed/)<sup><a href="#fn:1" class="footnote-ref">1</a></sup> |

## Databases<a href="#databases" class="headerlink" title="Permanent link">¶</a>

The information from the above sources is collected and stored in databases that Trivy uses for vulnerability scanning. Trivy automatically fetches, maintains, and caches the relevant databases when performing a vulnerability scan For more information about Trivy's Databases mechanism and configurations, refer to the [Databases document](../../configuration/db/).

## Configuration<a href="#configuration" class="headerlink" title="Permanent link">¶</a>

This section describes vulnerability-specific configuration. Other common options are documented [here](../../configuration/).

### Overriding OS version<a href="#overriding-os-version" class="headerlink" title="Permanent link">¶</a>

By default, Trivy automatically detects the OS during container image scanning and performs vulnerability detection based on that OS. However, in some cases, you may want to scan an image with a different OS version than the one detected. Also, you may want to specify the OS version when OS is not detected. For these cases, Trivy supports a `--distro` flag using the `<family>/<version>` format (e.g. `alpine/3.20`) to set the desired OS version.

### Severity selection<a href="#severity-selection_1" class="headerlink" title="Permanent link">¶</a>

By default, Trivy automatically detects severity (as described [here](#severity-selection)). But there are cases when you may want to use your own source priority. Trivy supports the `--vuln-severity-source` flag for this.

Fill in a list of required sources, and Trivy will check the sources in that order until it finds an existing severity. If no source has the severity - Trivy will use the `UNKNOWN` severity.

<div class="admonition note">

Note

To use the default logic in combination with your sources - use the `auto` value.

</div>

Example logic for the following vendor severity levels when scanning an Alpine image:

<div class="highlight">

    "VendorSeverity": {
      "ghsa": 3,
      "nvd": 4,
    }

</div>

- `--vuln-severity-source auto,nvd` - severity is `CRITICAL`, got from `auto`.
- `--vuln-severity-source alpine,auto` - severity is `CRITICAL`, got from `auto`.
- `--vuln-severity-source alpine,ghsa` - severity is `HIGH`, got from `ghsa`.
- `--vuln-severity-source alpine,alma` - severity is `UNKNOWN`.

<div class="footnote">

------------------------------------------------------------------------

1.  <div id="fn:1">

    <https://github.com/GoogleContainerTools/distroless> <a href="#fnref:1" class="footnote-backref" title="Jump back to footnote 1 in the text">↩︎</a><a href="#fnref2:1" class="footnote-backref" title="Jump back to footnote 1 in the text">↩︎</a>

    </div>

</div>

</div>

</div>

</div>

<a href="../../target/sbom/" class="md-footer__link md-footer__link--prev" aria-label="Previous: SBOM"></a>

<div class="md-footer__button md-icon">

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTIwIDExdjJIOGw1LjUgNS41LTEuNDIgMS40Mkw0LjE2IDEybDcuOTItNy45MkwxMy41IDUuNSA4IDExeiIgLz48L3N2Zz4=)

</div>

<div class="md-footer__title">

<span class="md-footer__direction"> Previous </span>

<div class="md-ellipsis">

SBOM

</div>

</div>

<a href="../misconfiguration/" class="md-footer__link md-footer__link--next" aria-label="Next: Overview"></a>

<div class="md-footer__title">

<span class="md-footer__direction"> Next </span>

<div class="md-ellipsis">

Overview

</div>

</div>

<div class="md-footer__button md-icon">

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTQgMTF2MmgxMmwtNS41IDUuNSAxLjQyIDEuNDJMMTkuODQgMTJsLTcuOTItNy45MkwxMC41IDUuNSAxNiAxMXoiIC8+PC9zdmc+)

</div>

<div class="md-footer-meta md-typeset">

<div class="md-footer-meta__inner md-grid">

<div class="md-copyright">

</div>

<div class="md-social">

<a href="https://twitter.com/AquaTrivy" class="md-social__link" target="_blank" rel="noopener" title="twitter.com"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCA0NDggNTEyIj48IS0tISBGb250IEF3ZXNvbWUgRnJlZSA3LjEuMCBieSBAZm9udGF3ZXNvbWUgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbSBMaWNlbnNlIC0gaHR0cHM6Ly9mb250YXdlc29tZS5jb20vbGljZW5zZS9mcmVlIChJY29uczogQ0MgQlkgNC4wLCBGb250czogU0lMIE9GTCAxLjEsIENvZGU6IE1JVCBMaWNlbnNlKSBDb3B5cmlnaHQgMjAyNSBGb250aWNvbnMsIEluYy4tLT48cGF0aCBkPSJNMzU3LjIgNDhoNzAuNkwyNzMuNiAyMjQuMiA0NTUgNDY0SDMxM0wyMDEuNyAzMTguNiA3NC41IDQ2NEgzLjhsMTY0LjktMTg4LjVMLTUuMiA0OGgxNDUuNmwxMDAuNSAxMzIuOXptLTI0LjggMzczLjhoMzkuMUwxMTkuMSA4OGgtNDJ6IiAvPjwvc3ZnPg==" /></a> <a href="https://github.com/aquasecurity/trivy" class="md-social__link" target="_blank" rel="noopener" title="github.com"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCA1MTIgNTEyIj48IS0tISBGb250IEF3ZXNvbWUgRnJlZSA3LjEuMCBieSBAZm9udGF3ZXNvbWUgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbSBMaWNlbnNlIC0gaHR0cHM6Ly9mb250YXdlc29tZS5jb20vbGljZW5zZS9mcmVlIChJY29uczogQ0MgQlkgNC4wLCBGb250czogU0lMIE9GTCAxLjEsIENvZGU6IE1JVCBMaWNlbnNlKSBDb3B5cmlnaHQgMjAyNSBGb250aWNvbnMsIEluYy4tLT48cGF0aCBkPSJNMTczLjkgMzk3LjRjMCAyLTIuMyAzLjYtNS4yIDMuNi0zLjMuMy01LjYtMS4zLTUuNi0zLjYgMC0yIDIuMy0zLjYgNS4yLTMuNiAzLS4zIDUuNiAxLjMgNS42IDMuNm0tMzEuMS00LjVjLS43IDIgMS4zIDQuMyA0LjMgNC45IDIuNiAxIDUuNiAwIDYuMi0ycy0xLjMtNC4zLTQuMy01LjJjLTIuNi0uNy01LjUuMy02LjIgMi4zbTQ0LjItMS43Yy0yLjkuNy00LjkgMi42LTQuNiA0LjkuMyAyIDIuOSAzLjMgNS45IDIuNiAyLjktLjcgNC45LTIuNiA0LjYtNC42LS4zLTEuOS0zLTMuMi01LjktMi45TTI1Mi44IDhDMTE0LjEgOCA4IDExMy4zIDggMjUyYzAgMTEwLjkgNjkuOCAyMDUuOCAxNjkuNSAyMzkuMiAxMi44IDIuMyAxNy4zLTUuNiAxNy4zLTEyLjEgMC02LjItLjMtNDAuNC0uMy02MS40IDAgMC03MCAxNS04NC43LTI5LjggMCAwLTExLjQtMjkuMS0yNy44LTM2LjYgMCAwLTIyLjktMTUuNyAxLjYtMTUuNCAwIDAgMjQuOSAyIDM4LjYgMjUuOCAyMS45IDM4LjYgNTguNiAyNy41IDcyLjkgMjAuOSAyLjMtMTYgOC44LTI3LjEgMTYtMzMuNy01NS45LTYuMi0xMTIuMy0xNC4zLTExMi4zLTExMC41IDAtMjcuNSA3LjYtNDEuMyAyMy42LTU4LjktMi42LTYuNS0xMS4xLTMzLjMgMi42LTY3LjkgMjAuOS02LjUgNjkgMjcgNjkgMjcgMjAtNS42IDQxLjUtOC41IDYyLjgtOC41czQyLjggMi45IDYyLjggOC41YzAgMCA0OC4xLTMzLjYgNjktMjcgMTMuNyAzNC43IDUuMiA2MS40IDIuNiA2Ny45IDE2IDE3LjcgMjUuOCAzMS41IDI1LjggNTguOSAwIDk2LjUtNTguOSAxMDQuMi0xMTQuOCAxMTAuNSA5LjIgNy45IDE3IDIyLjkgMTcgNDYuNCAwIDMzLjctLjMgNzUuNC0uMyA4My42IDAgNi41IDQuNiAxNC40IDE3LjMgMTIuMUM0MzYuMiA0NTcuOCA1MDQgMzYyLjkgNTA0IDI1MiA1MDQgMTEzLjMgMzkxLjUgOCAyNTIuOCA4TTEwNS4yIDM1Mi45Yy0xLjMgMS0xIDMuMy43IDUuMiAxLjYgMS42IDMuOSAyLjMgNS4yIDEgMS4zLTEgMS0zLjMtLjctNS4yLTEuNi0xLjYtMy45LTIuMy01LjItMW0tMTAuOC04LjFjLS43IDEuMy4zIDIuOSAyLjMgMy45IDEuNiAxIDMuNi43IDQuMy0uNy43LTEuMy0uMy0yLjktMi4zLTMuOS0yLS42LTMuNi0uMy00LjMuN20zMi40IDM1LjZjLTEuNiAxLjMtMSA0LjMgMS4zIDYuMiAyLjMgMi4zIDUuMiAyLjYgNi41IDEgMS4zLTEuMy43LTQuMy0xLjMtNi4yLTIuMi0yLjMtNS4yLTIuNi02LjUtMW0tMTEuNC0xNC43Yy0xLjYgMS0xLjYgMy42IDAgNS45czQuMyAzLjMgNS42IDIuM2MxLjYtMS4zIDEuNi0zLjkgMC02LjItMS40LTIuMy00LTMuMy01LjYtMiIgLz48L3N2Zz4=" /></a>

</div>

</div>

</div>

</div>

<div class="md-dialog" md-component="dialog">

<div class="md-dialog__inner md-typeset">

</div>

</div>