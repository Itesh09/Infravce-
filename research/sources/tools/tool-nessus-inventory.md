<div class="foundation-wrap off-canvas-wrapper">

<div class="off-canvas-wrapper-inner" off-canvas-wrapper="">

<div class="off-canvas-content inner-wrap" off-canvas-content="">

<div class="title-bar-container" sticky-container="">

<a href="#" class="skip-to-content fluid-skip showOnFocus">Skip To Main Content</a>

<div class="middle title-bar-section outer-row clearfix">

<div class="menu-icon-container relative clearfix">

<div class="central-account-wrapper">

<div class="central-dropdown">

<span class="central-account-drop"><span class="central-account-image"></span><span class="central-account-text">Account</span></span>

<div class="central-dropdown-content">

<span class="MCCentralLink central-dropdown-content-settings">Settings</span>

------------------------------------------------------------------------

<span class="MCCentralLink central-dropdown-content-logout">Logout</span>

</div>

</div>

</div>

</div>

</div>

<div class="title-bar-layout outer-row">

<div class="logo-wrapper">

<a href="/" class="logo" alt="Logo"></a>

</div>

<div class="navigation-wrapper nocontent">

- placeholder

</div>

<div class="central-account-wrapper">

<div class="central-dropdown">

<span class="central-account-drop"><span class="central-account-image"></span><span class="central-account-text">Account</span></span>

<div class="central-dropdown-content">

<span class="MCCentralLink central-dropdown-content-settings">Settings</span>

------------------------------------------------------------------------

<span class="MCCentralLink central-dropdown-content-logout">Logout</span>

</div>

</div>

</div>

<div class="nav-search-wrapper">

<div class="nav-search row">

<div class="search-bar search-bar-container needs-pie">

<div class="search-filter-wrapper">

<span id="search-filters-label" class="invisible-label">Filter: </span>

<div class="search-filter" aria-haspopup="true" aria-controls="sf-content" aria-expanded="false" aria-label="Search Filter" title="All Files" role="button" tabindex="0">

</div>

<div id="sf-content" class="search-filter-content">

- <span id="filterSelectorLabel-00001">All Files</span>

</div>

</div>

<div class="search-submit-wrapper" dir="ltr">

<div class="search-submit" title="Search" role="button" tabindex="0">

<span class="invisible-label">Submit Search</span>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<div class="main-section">

<div class="row outer-row sidenav-layout">

<div class="sidenav-container">

</div>

<div class="body-container">

<div mc-content-body="True">

<div id="cmdSuContainer" style="height:0;overflow:hidden;opacity:0;pointer-events:none;" aria-hidden="true">

<div id="auto">

<div ng-controller="SearchautoController">

<div bind-html-compile="autocompleteHtml">

</div>

</div>

</div>

</div>

<div id="topContentHeader">

<div class="breadcrumbsContainer">

<span class="mc-variable Skin.Breadcrumb variable">Tenable Cyber Exposure Study - Establishing a Software Inventory</span>: 

<div class="nocontent">

<div class="MCBreadcrumbsBox_0 breadcrumbs" role="navigation" aria-label="Breadcrumbs" mc-breadcrumbs-divider=" &gt; " mc-breadcrumbs-count="100" mc-toc="True">

<span class="MCBreadcrumbsPrefix">Tenable Agent: </span>

</div>

</div>

</div>

<div class="languageVersionSwitcher">

</div>

</div>

<div id="mcContentBody" class="section">

<div id="mcTopic">

<div id="mc-main-content" role="main">

# Determining Software Authorization and Support

Once software is enumerated, there are additional plugins that can help determine how many instances of each version of software are running in the environment. This data helps determine software authorization and support. Tenable plugins can enumerate unsupported operating systems, databases, web servers, browsers, and other software. [FINRA Rules](https://www.finra.org/rules-guidance/guidance/reports/2019-report-exam-findings-and-observations/digital-communication) forbid financial institutions from using any digital communication applications that cannot preserve records of business-related communications, such as WhatsApp, Signal, or Telegram. Tenable plugins can be used to detect these applications, saving the organization from large fines levied by the Securities and Exchange Commission (SEC). The following is a sample search using CPE to find a commonly used chat and collaboration application.

<a href="Resources/Images/slackscreenshot.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/slackscreenshot.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1475" data-mc-height="366" tabindex="" /></a>

Packet capture software such as Wireshark and tcpdump tend to be authorized for a small group of users within the organization. Tenable’s software enumeration plugins can assist in discovering the use of this type of software and reducing the number of authorized installations.

The following images display results matching the filter: *CPE* **contains** wireshark. The Wireshark CPE is */a:wireshark:wireshark*, so the full CPE can be searched as well. When using only the *CPE* **contains** filter, the results include Wireshark vulnerabilities as well as an informational plugin for the detection of the Wireshark software. Typically, detection-only plugins are *Info* severity, so the *Severity* filter for *Info* can also be applied to display a list of assets with Wireshark installed.

**Wireshark Software & Vulnerability Detection in <span class="mc-variable Tenable.SecurityCenter variable">Tenable Security Center</span>**

<a href="Resources/Images/wireshark1.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/wireshark1.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1843" data-mc-height="420" tabindex="" /></a>

**Wireshark Software & Vulnerability Detection in <span class="mc-variable Tenable.Cloud variable">Tenable Vulnerability Management</span>**

<a href="Resources/Images/wireshark2.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/wireshark2.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1727" data-mc-height="745" tabindex="" /></a>

**Wireshark Software Detection in <span class="mc-variable Tenable.SecurityCenter variable">Tenable Security Center</span>**

<a href="Resources/Images/wireshark3.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/wireshark3.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1497" data-mc-height="628" tabindex="" /></a>

**Wireshark Software Detection in <span class="mc-variable Tenable.Cloud variable">Tenable Vulnerability Management</span>**

<a href="Resources/Images/wireshark4.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/wireshark4.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1722" data-mc-height="368" tabindex="" /></a>

The output of the [Common Platform Enumeration (CPE) (45590)](https://www.tenable.com/plugins/nessus/45590) plugin provides CPE syntax for operating system and application names that can be used in searches using the *CPE* filter in <span class="mc-variable Tenable.Cloud variable">Tenable Vulnerability Management</span> and the *Application CPE* filter in <span class="mc-variable Tenable.SecurityCenter variable">Tenable Security Center</span>. The **cpe:/a:** syntax represents an application CPE, the **cpe:/o:** syntax represents an operating system CPE, **p-cpe:/** is used for Linux package checks, **cpe:/h:** represents a type of hardware, and **x-cpe:/** is used when NIST does not have a defined CPE. The following is a sample of some of the CPEs from plugin [45590](https://www.tenable.com/plugins/nessus/45590):

- cpe:/a:microsoft:.net_framework:3.0 -\> Microsoft .NET Framework 3.0
- cpe:/a:microsoft:.net_framework:4.8
- cpe:/a:microsoft:ie:11.0.9600.19596
- cpe:/a:microsoft:internet_information_services:7.5.7600.16385
- cpe:/a:microsoft:remote_desktop_connection:6.1.7601.24543
- cpe:/a:microsoft:system_center_endpoint_protection:4.10.0209.0
- cpe:/a:mozilla:firefox:79.0.0
- cpe:/a:oracle:jre:1.8.0_171
- cpe:/a:tenable:nnm:5.6.0
- cpe:/a:vmware:vcenter_converter:6.2.0
- cpe:/a:vmware:vmware_tools:10.2.0.1608
- cpe:/a:vmware:vsphere_client:
- cpe:/a:apache:http_server:2.4.48 -\> Apache Software Foundation Apache HTTP Server
- cpe:/a:apple:safari:15.1 -\> Apple Safari
- cpe:/a:openbsd:openssh:8.6 -\> OpenBSD OpenSSH
- cpe:/a:redhat:ansible -\> Red Hat Ansible
- cpe:/a:vmware:tools:11.2.6.28747 -\> VMWare Tools
- cpe:/a:::6.2.3.15-39
- cpe:/a:apache:http_server -\> Apache Software Foundation Apache HTTP Server
- cpe:/a:cisco:firepower_threat_defense:6.2.3.15.39 -\> Cisco Firepower Threat Defense (FTD)
- cpe:/a:cisco:firepower_threat_defense:6.2.3.15\_(build_39) -\> Cisco Firepower Threat Defense (FTD)
- cpe:/a:openbsd:openssh:7.4 -\> OpenBSD OpenSSH 7.4
- x-cpe:/a:microsoft:dhcp_server:6.1.7601.24498
- x-cpe:/a:tenable:log_correlation_engine_client:windows:5.0.1.0
- x-cpe:/a:slack:slack
- cpe:/o:apple:mac_os_x:12.0.1 -\> Apple Mac OS X
- cpe:/o:cisco:ios_xe
- cpe:/o:linux:linux_kernel:4.4
- cpe:/o:cisco:ios:15.5 -\> Cisco IOS
- cpe:/o:cisco:ios_xe:16.6.3 -\> Cisco IOS XE
- cpe:/h:dell:remote_access_card:8 -\> Dell Remote Access Card

**Plugin Output for Plugin ID 45590 in <span class="mc-variable Tenable.SecurityCenter variable">Tenable Security Center</span>**

<a href="Resources/Images/cpe1.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/cpe1.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="649" data-mc-height="234" tabindex="" /></a>

<a href="Resources/Images/cpe2.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/cpe2.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="645" data-mc-height="270" tabindex="" /></a>

<a href="Resources/Images/cpe3.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/cpe3.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="649" data-mc-height="198" tabindex="" /></a>

The *Unsupported Product Summary - Applications* and *Unsupported Product Summary - All OSes* <span class="mc-variable Tenable.SecurityCenter variable">Tenable Security Center</span> Dashboard Components use the following filters to report unsupported operating systems and applications:

- *Application CPE* **contains** /o
- *Plugin Name* **contains** unsupported

<a href="Resources/Images/cpeo.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/cpeo.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1481" data-mc-height="678" tabindex="" /></a>

- *Application CPE* **contains** /a
- *Plugin Name* **contains** unsupported

<a href="Resources/Images/cpea.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/cpea.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1481" data-mc-height="638" tabindex="" /></a>

<div class="Tip">

**Filter Spotlight**: The **Regex Match** operator can be used to perform more complex searches with the Application CPE filter, as shown below. The *ASD Top 4 Mitigation Strategies - Active OS* and *Application Vulnerability Count*s <span class="mc-variable Tenable.SecurityCenter variable">Tenable Security Center</span> Dashboard Component uses the *Application CPE* regex matches described below.

</div>

<a href="Resources/Images/asdtop4.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/asdtop4.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1062" data-mc-height="266" tabindex="" /></a>

**Apps Only**: *Application CPE* **Regex Match** ^(?\![\s\S\]\*cpe\\\\o)(?=\[\s\S\]\*cpe\\)

<a href="Resources/Images/appsonly.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/appsonly.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1447" data-mc-height="572" tabindex="" /></a>

**OS Only**: *Application CPE* **Regex Match** ^(?\![\s\S\]\*cpe\\\\a)(?=\[\s\S\]\*cpe\\)

<a href="Resources/Images/osonly.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/osonly.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1433" data-mc-height="565" tabindex="" /></a>

**OS & Apps**: *Application CPE* **Regex Match** (cpe\\\\a\[\s\S\]\*cpe\\\\o)\|(cpe\\\\o\[\s\S\]\*cpe\\\\a)

<a href="Resources/Images/osandapps.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/osandapps.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1446" data-mc-height="565" tabindex="" /></a>

**No CPE**: *Application CPE* **Regex Match** ^(?\![\s\S\]\*cpe\\)

<a href="Resources/Images/nocpe.png" class="MCPopupThumbnailLink MCPopupThumbnailPopup"><img src="Resources/Images/nocpe.png" class="MCPopupThumbnail img imgThumbnail" style="max-width: 300px;" data-mc-width="1433" data-mc-height="564" tabindex="" /></a>

 

</div>

<div id="masterFooter">

Copyright © <span class="mc-variable Tenable.Year variable">2026</span> Tenable, Inc. All rights reserved. Tenable, <span class="mc-variable Tenable.Nessus variable">Tenable Nessus</span>, <span class="mc-variable Tenable.LumProdLong variable">Tenable Lumin</span>, Assure, and the Tenable logo are registered trademarks of Tenable, Inc. or its affiliates. All other products or services are trademarks of their respective owners.

</div>

</div>

</div>

<span id="backToTop" title="Back to Top" mc-conditions="TenableConditions.OnlineOnly"></span>

</div>

</div>

</div>

</div>

<span close="true"></span>

</div>

</div>

</div>