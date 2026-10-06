Towards Effective & Scalable Vulnerability Management :: Security BSides Las Vegas 2023 :: pretalx

[Skip to main content](#content)

<div id="top-bg" class="header bg-primary">

</div>

<div id="main-container" class="container">

<div>

# <a href="%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20/bsideslv23/%0A%20%20%20%20%0A" class="no-underline"><img src="/media/bsideslv23/img/BSidesLV_logo_1D91awL.png" id="event-logo" loading="lazy" alt="The event’s logo" /></a>

<div class="header-wrapper">

<div id="header-tabs">

<a href="/bsideslv23/schedule/" class="header-tab"><em></em> Schedule</a> <a href="/bsideslv23/talk/" class="header-tab active"><em></em> Sessions</a> <a href="/bsideslv23/speaker/" class="header-tab"><em></em> Speakers</a>

</div>

<div class="header-row-right">

[login](/bsideslv23/login/?next=%2Fbsideslv23%2Ftalk%2Freview%2FVCYNCXSUHPFBAGJLGMKHTJB7CHF99FHV)

</div>

</div>

</div>

<div id="main-card" class="card">

<div id="content" role="main">

<div class="page-heading">

## Towards Effective & Scalable Vulnerability Management

</div>

<div class="talk-layout">

<div class="talk-content">

<div class="section abstract">

While the security landscape is constantly changing, our approach toward vulnerability management hasn't changed much over the last couple of decades.

The increasing reliance on third-party code, the growing number of vulnerabilities being discovered, as well as the increased visibility into our software stack in the advent of Log4Shell and the adoption of SBOM, make a more effective and scalable vulnerability management paradigm a necessity.

What would such a paradigm look like?

Join me in this interactive discussion as we'll explore the challenges of vulnerability management and highlight potential solutions.  
We'll discuss current frameworks and standards that can help address this issue, such as CSAF and VEX, and demonstrate how once adopted, they can be used towards automating many aspects of vulnerability management which today are manual and extremely time-consuming.

We'll explore how to use exploitability as a strong signal for prioritization, and how automation can play a crucial role in making vulnerability management more effective and scalable.  
By the end of this talk, you'll have a deeper understanding of vulnerability management and practical insights on how to improve your organization's security posture. Let's explore the future of vulnerability management together!

</div>

------------------------------------------------------------------------

<div class="section description">

1.  Introduction - where do we stand? (10 minutes)

In this section I will describe the current state of vulnerability management and the challenges organizations face, including:

- Most of the code running in a production environment is third-party code (commercial or open-source).  
  While this allows focus on the core business logic and increase velocity, it comes with inherent risks.
- The number of vulnerabilities discovered each year is steadily rising
- Exploitation of known vulnerabilities remains one of the most common attack vectors
- Organizations can't keep up and are left with huge vulnerability backlogs
- Current prioritization by CVSS score is suboptimal at best
- These challenges will only intensify over time  
  I will present insights from research we conducted analyzing the public attack surface for CISA KEV vulnerabilities.

1.  The promise and peril of SBOM (10 minutes)

In this section, I will discuss the events that led to the increased adoption of SBOM (Software Bill of Material), shortly explain what is it and what is the problem it tries to solve. We will then discuss some of the challenges standing in the way of SBOM living up to its full potential and review some of the work being done in various governmental work streams as well as in the open-source community around advancing the SBOM ecosystem (adoption, tooling, sharing & exchanging of SBOMs and more…).  
I will also argue that SBOM alone isn’t a silver bullet as it is a double-edged sword - with increased visibility comes increased noise which only aggravates the issues discussed in the first section.

1.  What do we need to solve? (5 minutes)

Given all of the above we still need a way to answer the “Am I affected?” question at scale.  
In this section, we will briefly discuss some of the current alternatives for answering this question and their shortcomings. Including: vulnerability scans, independent Investigation, asking the vendor, and relying on security advisories.

1.  A way forward? (10 min)

In this section, I will suggest a shift in the vulnerability management paradigm I believe is inevitable to adopt in order to effectively cope with the challenges presented - as patching everything is impractical, and current prioritization strategies are suboptimal, we need to strive to adopt a risk-oriented approach where we prioritize vulnerabilities based on exploitability.

This cannot happen without automation.

I will present the Common Security Advisory Framework (CSAF) and the Vulnerability Exploitability Exchange (VEX) and discuss how they can help with some of the challenges we discussed. I will offer an outlook into a future in which these standards gain wide adoption and are integrated into security tools and demonstrate how that can lead to effective and scalable vulnerability management.

1.  How will this look like? (5 min)

In this section, we will present an example of such an ideal flow in a visual manner.  
A potential flow could be for example:  
A new critical vulnerability that can only be exploited remotely and requires a specific configuration to be in place for effective exploitation has been discovered in a library used by millions of different applications worldwide.  
Luckily, you have an SBOM of your entire environment. You query the SBOM to find 100 occurrences in your environment. Out of these 100 occurrences, 80 are part of 10 different commercial and open-source products and 20 are part of your proprietary code. For 8 out of the 10 commercial and open source products, your security tool was able to automatically ingest their CSAF with VEX statements saying that they are unaffected by the vulnerability with the justification: `vulnerable_code_not_present`.  
You are left with a total of 16 occurrences in 2 third-party applications as well as 20 occurrences in your proprietary code. Luckily, you also have a runtime analysis based tool that determined that only 5 of the remaining occurrences in your proprietary code and 8 occurrences in one of the relevant third-party applications are actually loaded to memory, the rest are installed but are not in use, the tool automatically updated the SBOM with the corresponding VEX statements saying that these 25 instances are not exploitable with the justification `vulnerable_code_not_in_execute_path`.  
You are left with 13 occurrences in 2 potentially vulnerable applications containing the vulnerable library  
As a strong believer in layered defense, you also have a network security tool that determined that the third-party application isn’t exposed to the network and hence updated the VEX statements for all 8 occurrences of it as `Not Exploitable` with the justification: `vulnerable_code_cannot_be_controlled_by_adversary`.

All this happened automatically without any human intervention.  
All you are left to triage are 5 occurrences of the vulnerable component in your proprietary code.

You validate the configuration of the hosts containing the 5 loaded, reachable via the network vulnerable instances and see that only one of the hosts has the configuration required for successful exploitation. You manually update the VEX statements of the remaining 4 occurrences as `Not Exploitable` with the justification: `vulnerable_code_cannot_be_controlled_by_adversary`.

You open a ticket for the relevant team to patch the final exploitable occurrence of the application using the vulnerable library and go make yourself a cup of coffee :)

1.  Final words and open discussion (5 minutes)

We will discuss some of the outstanding challenges on the road to that vision and open the floor for questions/open discussion.

</div>

<div class="section talk-speakers">

<div class="talk-speaker-card">

<div class="talk-speaker-avatar">

<img src="/media/avatars/H7TP9B_RFTE8Gg_thumbnail_default.webp" class="user-avatar" loading="lazy" />

</div>

<div class="talk-speaker-text">

<div class="talk-speaker-name">

Yotam Perkal

</div>

<div class="talk-speaker-bio">

Yotam leads the vulnerability research team at Rezilion, focusing on research around vulnerability validation, mitigation, and remediation. He is passionate about Cyber Security and Machine Learning and is especially intrigued by the intersection between the domains, whether it be using ML in order to help solve Cyber Security challenges or exploring the challenges in securing ML applications. Prior to Rezilion, Yotam filled several roles at PayPal Security organization, dealing with vulnerability management, threat intelligence, and Insider threat. Additionally, Yotam is also a member of the PyCon Israel organization committee and takes part in several OpenSSF working groups around open-source security as well as several CISA workstreams around SBOM and VEX.

</div>

</div>

</div>

</div>

<div class="section">

</div>

</div>

<div class="talk-card talk-card-schedule" style="--track-color:#12ad2e">

<div class="talk-facts">

<div class="talk-fact">

<span class="talk-track-swatch"></span> Common Ground · Talk-20m

</div>

</div>

<div class="talk-actions">

<a href="/bsideslv23/talk/BUC7QH/feedback/" class="btn btn-success"><em></em> Feedback</a>

</div>

</div>

</div>

</div>

</div>

powered by <a href="/redirect/?url=https%3A//pretalx.com%3AFZHsiuBcrC2IlEJJu6SMtZpwByWhWO8BK25RGYOfxHY" rel="noopener" target="_blank">pretalx</a> · [Contact us](mailto:cfp@bsideslv.org) · <a href="https://bsideslv.org/" rel="noopener" target="_blank">Imprint</a> · <a href="/redirect/?url=/bsideslv23/privacy%3AqM17ESki9HXSRxdOpNeLIKT6jwsT2X8qiUVzG6d28Ak" rel="noopener" target="_blank">Privacy</a>

</div>

<div class="modal-card-content">

<figure class="text-center text-muted">

</figure>

</div>