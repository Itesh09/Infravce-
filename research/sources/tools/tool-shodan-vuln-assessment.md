<div class="quickbar">

- [Shodan](https://www.shodan.io)
- [Developers](https://developer.shodan.io)
- [Monitor](https://monitor.shodan.io)
- [View All...](https://www.shodan.io/about/products)

<div class="clear">

</div>

</div>

<div class="container u-full-width">

<div class="row">

<div class="twelve columns">

<div class="navbar">

<a href="/" class="title"><img src="/images/logo.png" width="112" height="32" alt="Shodan" /> <span>Help Center</span></a>

<div class="searchbox">

<div class="input-wrapper">

</div>

</div>

</div>

</div>

</div>

</div>

  
  

<div class="container">

<div class="section row content">

<div class="twelve columns card card-padding">

## Understanding Shodan Vulnerability Assessment

There are 2 types of vulnerabilities that can be attached to the banners in Shodan: **verified** and **unverified**. Unverified vulnerabilities are vulnerabilities that are implied based on the metadata we've collected. For example, if a server is running an old version of Apache then we will associate known issues with that version and set the associated verified property in the banner to **False**. Shodan has increasingly also started to verify vulnerabilities when possible. If a verified vulnerability is discovered then we set the verified property to **True**. Unverified vulnerabilities can have significant false positives depending on the device/ software so they typically require additional verification to make sure the service is vulnerable. They should be seen as a starting point for further investigation. Note that [Shodan Monitor](https://monitor.shodan.io) only sends out notifications for **verified** vulnerabilities.

On the website, we will tell you if some of the vulnerabilities are unverified with a small visual disclaimer:

![](/images/vulnerability-disclaimer.png)

And within the data itself there is a `verified` property that will tell you whether it's been verified or not.

#### Sample Data

All vulnerability information is stored in a `vulns` property in the banner. You can see how it looks like from the **Raw** tab on the IP information page on the website or by looking at the API response directly. The top-level `vulns` property is an object where the keys are the vulnerability identifiers (ex. `CVE-2014-0160`) and the values contain the information about the vulnerability.

``` json
{
    "CVE-2008-2939": {
        "references": [
            "http://lists.apple.com/archives/security-announce/2009/May/msg00002.html",
            "http://lists.opensuse.org/opensuse-security-announce/2008-11/msg00000.html",
            "http://marc.info/?l=bugtraq&m=123376588623823&w=2",
            "http://marc.info/?l=bugtraq&m=125631037611762&w=2",
            "http://rhn.redhat.com/errata/RHSA-2008-0967.html",
            "http://sunsolve.sun.com/search/document.do?assetkey=1-26-247666-1",
            "http://support.apple.com/kb/HT3549",
        ],
        "verified": false,
        "cvss": 4.3,
        "summary": "Cross-site scripting (XSS) vul..."
    },
    "CVE-2010-0408": {
        "references": [
            "http://httpd.apache.org/security/vulnerabilities_22.html",
            "http://www.vupen.com/english/advisories/2010/1411",
            "https://bugzilla.redhat.com/show_bug.cgi?id=569905"
        ],
        "verified": false,
        "cvss": 5,
        "summary": "The ap_proxy_ajp_request function in mod_proxy_ajp..."
    }
}
```

##### Frequently Asked Questions

**Which vulnerabilities does Shodan verify?**

You can get that list by using the `vuln.verified` facet and searching across all results. The [facet analysis](https://www.shodan.io/search/facet?query=net%3A0%2F0&facet=vuln.verified) page of the main Shodan website can be used to see the results or you can run a command via the CLI such as `shodan stats --facets vuln.verified:100 net:0/0`.

**I patched my service and it's still showing as vulnerable**

Most likely the vulnerability you're seeing is an **unverified** vulnerability that Shodan is associating based on metadata. If the security patch doesn't change the version number (ex. running an enterprise Linux distribution) then it won't be detected as fixed by Shodan.

**Can you start checking/ verifying a new issue?**

Maybe! We can't check for every vulnerability across the Internet but if there's something you think we should verify let us know by requesting a new verified vulnerability via <support@shodan.io>.

</div>

  

  
  

<div class="container">

<div class="row">

<div class="three columns">

###### Products

- <a href="https://monitor.shodan.io" class="light">Monitor</a>
- <a href="https://www.shodan.io" class="light">Search Engine</a>
- <a href="https://developer.shodan.io" class="light">Developer API</a>
- <a href="https://maps.shodan.io" class="light">Maps</a>

</div>

<div class="three columns">

######  

- <a href="https://enterprise.shodan.io" class="light">Bulk Data</a>
- <a href="https://images.shodan.io" class="light">Images</a>
- <a href="https://snippets.shodan.io" class="light">Snippets</a>

</div>

<div class="three columns">

###### Pricing

- <a href="https://www.shodan.io/store/member" class="light">Membership</a>
- <a href="https://developer.shodan.io/pricing" class="light">API Subscriptions</a>
- <a href="https://enterprise.shodan.io" class="light">Enterprise</a>

</div>

<div class="three columns">

###### Contact Us

- <a href="mailto:support@shodan.io" class="light">support@shodan.io</a>

- ##### <a href="https://twitter.com/shodanhq" class="f-lightgrey"><em></em></a>  <a href="https://www.linkedin.com/company/shodan/" class="f-lightgrey"><em></em></a>  <a href="https://www.facebook.com/shodan.io" class="f-lightgrey"><em></em></a>

Shodan ® - All rights reserved

</div>

</div>

</div>

</div>

</div>