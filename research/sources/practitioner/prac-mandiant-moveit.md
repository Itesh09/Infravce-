<div class="VUoKZ" aria-hidden="true">

<div class="TRHLAc">

</div>

</div>

<div class="T4LgNb" jsname="a9kxte">

<div class="kFwPee" jsname="qJTHM">

<div class="section nRhiJb-DARUcf">

<div class="Wdmc0c nRhiJb-DbgRPb-wNfPc-cGMI2b">

<div class="Qwf2Db-MnozTc Qwf2Db-MnozTc-OWXEXe-MnozTc-qWD73c nRhiJb-BFbNVe-r8s4j-bMElCd dIsJJe" track-name="threat intelligence" track-type="tag">

Threat Intelligence

</div>

<div class="nRhiJb-ObfsIf">

<div class="nRhiJb-kR0ZEf-OWXEXe-GV1x9e-R6PoUb">

</div>

<div class="nRhiJb-kR0ZEf-OWXEXe-GV1x9e-EehZO nRhiJb-fmcmS-oXtfBe">

# 

<div class="Qwf2Db-MnozTc Qwf2Db-MnozTc-OWXEXe-MnozTc-ibL1re">

<span class="FewWi"></span>Zero-Day Vulnerability in MOVEit Transfer Exploited for Data Theft

</div>

</div>

</div>

<div class="nRhiJb-fmcmS-oXtfBe dEogG">

June 2, 2023

</div>

</div>

</div>

<div class="EKklye">

<div class="nRhiJb-DARUcf ZWw7T">

<div class="npzWPc">

<div class="dzoHJ">

<div class="nRhiJb-DX2B6 nRhiJb-DX2B6-OWXEXe-h30Snd">

<div class="nRhiJb-j5y3u">

- <a href="https://x.com/intent/tweet?text=Zero-Day%20Vulnerability%20in%20MOVEit%20Transfer%20Exploited%20for%20Data%20Theft%20@googlecloud&amp;url=https://cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft" class="nRhiJb-ARYxNe" data-track-name="x" data-track-type="social share" data-track-metadata-eventdetail="x.com/intent/tweet?text=Zero-Day Vulnerability in MOVEit Transfer Exploited for Data Theft%20@googlecloud&amp;url=cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft" data-track-metadata-module="social icons" target="_blank" rel="noopener"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS1EWDJCNiBuUmhpSmItQnoxMTJjLU9XWEVYZS1uU3VRZiIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMTMuOSwxMC41TDIxLjEsMmgtMS43bC02LjMsNy40TDgsMkgyLjJsNy42LDExLjFMMi4yLDIyaDEuN2w2LjctNy44TDE2LDIyaDUuOEwxMy45LDEwLjVMMTMuOSwxMC41eiBNMTEuNSwxMy4ybC0wLjgtMS4xIEw0LjYsMy4zaDIuN2w1LDcuMWwwLjgsMS4xbDYuNSw5LjJoLTIuN0wxMS41LDEzLjJMMTEuNSwxMy4yeiIgLz48L3N2Zz4=" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-DX2B6 nRhiJb-Bz112c-OWXEXe-nSuQf" /></a>
- <a href="https://www.linkedin.com/shareArticle?mini=true&amp;url=https://cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft&amp;title=Zero-Day%20Vulnerability%20in%20MOVEit%20Transfer%20Exploited%20for%20Data%20Theft" class="nRhiJb-ARYxNe" data-track-name="linkedin" data-track-type="social share" data-track-metadata-eventdetail="www.linkedin.com/shareArticle?mini=true&amp;url=cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft&amp;title=Zero-Day Vulnerability in MOVEit Transfer Exploited for Data Theft" data-track-metadata-module="social icons" target="_blank" rel="noopener"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS1EWDJCNiBuUmhpSmItQnoxMTJjLU9XWEVYZS1uU3VRZiIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMjAgMkg0Yy0xLjEgMC0xLjk5LjktMS45OSAyTDIgMjBjMCAxLjEuOSAyIDIgMmgxNmMxLjEgMCAyLS45IDItMlY0YzAtMS4xLS45LTItMi0yek04IDE5SDV2LTloM3Y5ek02LjUgOC4zMWMtMSAwLTEuODEtLjgxLTEuODEtMS44MVM1LjUgNC42OSA2LjUgNC42OXMxLjgxLjgxIDEuODEgMS44MVM3LjUgOC4zMSA2LjUgOC4zMXpNMTkgMTloLTN2LTUuM2MwLS44My0uNjctMS41LTEuNS0xLjVzLTEuNS42Ny0xLjUgMS41VjE5aC0zdi05aDN2MS4yYy41Mi0uODQgMS41OS0xLjQgMi41LTEuNCAxLjkzIDAgMy41IDEuNTcgMy41IDMuNVYxOXoiIC8+PC9zdmc+" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-DX2B6 nRhiJb-Bz112c-OWXEXe-nSuQf" /></a>
- <a href="https://www.facebook.com/sharer/sharer.php?caption=Zero-Day%20Vulnerability%20in%20MOVEit%20Transfer%20Exploited%20for%20Data%20Theft&amp;u=https://cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft" class="nRhiJb-ARYxNe" data-track-name="facebook" data-track-type="social share" data-track-metadata-eventdetail="www.facebook.com/sharer/sharer.php?caption=Zero-Day Vulnerability in MOVEit Transfer Exploited for Data Theft&amp;u=cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft" data-track-metadata-module="social icons" target="_blank" rel="noopener"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS1EWDJCNiBuUmhpSmItQnoxMTJjLU9XWEVYZS1uU3VRZiIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMjAgMkg0Yy0xLjEgMC0xLjk5LjktMS45OSAyTDIgMjBjMCAxLjEuOSAyIDIgMmgxNmMxLjEgMCAyLS45IDItMlY0YzAtMS4xLS45LTItMi0yem0tMSAydjNoLTJjLS41NSAwLTEgLjQ1LTEgMXYyaDN2M2gtM3Y3aC0zdi03aC0ydi0zaDJWNy41QzEzIDUuNTcgMTQuNTcgNCAxNi41IDRIMTl6IiAvPjwvc3ZnPg==" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-DX2B6 nRhiJb-Bz112c-OWXEXe-nSuQf" /></a>
- <a href="mailto:?subject=Zero-Day%20Vulnerability%20in%20MOVEit%20Transfer%20Exploited%20for%20Data%20Theft&amp;body=Check%20out%20this%20article%20on%20the%20Cloud%20Blog:%0A%0AZero-Day%20Vulnerability%20in%20MOVEit%20Transfer%20Exploited%20for%20Data%20Theft%0A%0A%0A%0Ahttps://cloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft" class="nRhiJb-ARYxNe" data-track-name="email" data-track-type="social share" data-track-metadata-eventdetail="mailto:?subject=Zero-Day Vulnerability in MOVEit Transfer Exploited for Data Theft&amp;body=Check%20out%20this%20article%20on%20the%20Cloud%20Blog:%0A%0AZero-Day Vulnerability in MOVEit Transfer Exploited for Data Theft%0A%0A%0A%0Acloud.google.com/blog/topics/threat-intelligence/zero-day-moveit-data-theft" data-track-metadata-module="social icons" target="_blank" rel="noopener"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS1EWDJCNiBuUmhpSmItQnoxMTJjLU9XWEVYZS1uU3VRZiIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMjAgNEg0Yy0xLjEgMC0yIC45LTIgMnYxMmMwIDEuMS45IDIgMiAyaDE2YzEuMSAwIDItLjkgMi0yVjZjMC0xLjEtLjktMi0yLTJ6bS0uOCAyTDEyIDEwLjggNC44IDZoMTQuNHpNNCAxOFY3Ljg3bDggNS4zMyA4LTUuMzNWMThINHoiIC8+PC9zdmc+" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-DX2B6 nRhiJb-Bz112c-OWXEXe-nSuQf" /></a>

</div>

</div>

</div>

</div>

</div>

<div>

<div class="section nRhiJb-DARUcf">

<div class="nRhiJb-DbgRPb-wNfPc-ma6Yeb nRhiJb-DbgRPb-wNfPc-cGMI2b">

<div class="section DA9Qj nRhiJb-ObfsIf nRhiJb-fmcmS-oXtfBe">

<div class="nRhiJb-kR0ZEf-OWXEXe-GV1x9e-c5RTEf">

</div>

<div class="nRhiJb-kR0ZEf-OWXEXe-GV1x9e-qWD73c">

##### Mandiant

</div>

</div>

</div>

</div>

<div class="nRhiJb-DARUcf">

<div class="nRhiJb-ObfsIf nRhiJb-DbgRPb-wNfPc-ma6Yeb nRhiJb-DbgRPb-qWD73c-cGMI2b">

<div class="nRhiJb-kR0ZEf-OWXEXe-GV1x9e-ibL1re dzoHJ">

</div>

<div class="OYL9D nRhiJb-kR0ZEf-OWXEXe-GV1x9e-OiUrBf" jsname="tx2NYc">

<div class="section Wy08Ac nRhiJb-qJTHM-OWXEXe-hJDwNd nRhiJb-DbgRPb-II5mzb-cGMI2b">

<div jsaction="rcuQ6b:npT2md" jscontroller="M0Q3Qb" is-cws-richtext="true">

Written by: Nader Zaveri, Jeremy Kennelly, Genevieve Stark, Matthew McWhirt, Dan Nutting, Kimberly Goody, Justin Moore, Joe Pisano, Zander Work, Peter Ukhanov, Juraj Sucik, Will Silverstone, Zach Schramm, Greg Blaum, Ollie Styles, Nicholas Bennett, Josh Murchie

------------------------------------------------------------------------

</div>

</div>

<div class="section Wy08Ac nRhiJb-qJTHM-OWXEXe-hJDwNd nRhiJb-DbgRPb-II5mzb-cGMI2b">

<div jsaction="rcuQ6b:npT2md" jscontroller="M0Q3Qb" is-cws-richtext="true">

*UPDATE (June 9): On June 6, 2023, Mandiant merged UNC4857 into* <a href="https://cloud.google.com/blog/topics/threat-intelligence/fin11-email-campaigns-precursor-for-ransomware-data-theft" rel="noopener" target="_blank"><em>FIN11</em></a> *based on targeting, infrastructure, certificate and data leak site (DLS) overlaps. This blog post has been updated to reflect the new attribution and supporting evidence.*

Mandiant has observed wide exploitation of a zero-day vulnerability in the MOVEit Transfer secure managed file transfer software for subsequent data theft. This vulnerability was announced by <a href="https://community.progress.com/s/article/MOVEit-Transfer-Critical-Vulnerability-31May2023" rel="noopener" target="_blank"><u>Progress Software Corporation</u></a> on May 31, 2023 and has been assigned CVE-2023-34362. Based on initial analysis from Mandiant incident response engagements, the earliest evidence of exploitation occurred on May 27, 2023 resulting in deployment of web shells and data theft. In some instances, data theft has occurred within minutes of the deployment of web shells. The seemingly opportunistic nature of this campaign and the subsequent data theft is consistent with activity we’ve seen from extortion actors; however, victims did not initially receive any ransom demands. Then on June 6, 2023, a post on the CL0P^\_-LEAKS data leak site (DLS) claimed responsibility for this activity and threatened to post stolen data if victims did not pay an extortion fee. Mandiant initially attributed this activity to UNC4857, which has now been merged into FIN11 based on targeting, infrastructure, certificate, and DLS overlaps. This campaign has impacted organizations operating in a wide range of industries based in Canada, India, and the U.S., but the impact is almost certainly broader than Mandiant has directly observed.

- Following exploitation of the vulnerability, the threat actors are deploying a newly discovered LEMURLOOT web shell with filenames that masquerade as human.aspx, which is a legitimate component of the MOVEit Transfer software. Mandiant has observed several POST requests made to the legitimate guestaccess.aspx file before interaction with the LEMURLOOT webshell, indicating SQL injection attacks were directed towards that file.
- We have observed LEMURLOOT samples with the filenames human2.aspx and \_human2.aspx. Various samples with the name human2.aspx were uploaded to VirusTotal beginning on May 28, 2023. Samples of LEMURLOOT have been uploaded to public repositories from several additional countries—including Italy, Pakistan, and Germany—suggesting that UNC4857 has also impacted organizations in these nations.
- LEMURLOOT provides functionality tailored to execute on a system running MOVEit Transfer software, including the ability to generate commands to enumerate files and folders, retrieve configuration information, and create or delete a user with a hard-coded name. Initial analysis suggests that the LEMURLOOT web shell is being used to steal data previously uploaded by the users of individual MOVEit Transfer systems.
- Mandiant is aware of multiple cases where large volumes of files have been stolen from victims' MOVEit transfer systems. LEMURLOOT can also steal Azure Storage Blob information, including credentials, from the MOVEit Transfer application settings, suggesting that actors exploiting this vulnerability may be stealing files from Azure in cases where victims are storing appliance data in Azure Blob storage, although it is unclear if theft is limited to data stored in this way.
- In many cases, the scanning and exploitation leading to the delivery of LEMURLOOT was sourced from IP addresses in the range 5.252.188.0/22, however interaction with the web shell and data theft came from different systems. Many of the hosts used to support these second-stage operations hosted RDP services with certificates generated between May 19 and 22, which is suggestive of when this infrastructure may have been staged.

Analysis of this intrusion activity is ongoing and will be reflected on the <u>CAMP.23.037</u> page within Mandiant Advantage; we will also update this blog post if and when additional information becomes available. Along with this blog post, Mandiant has produced a detailed <a href="https://services.google.com/fh/files/misc/moveit-containment-hardening-guide-rpt-en.pdf" rel="noopener" target="_blank"><u>MOVEit Containment and Hardening</u></a> guide to assist organizations with this event. The document contains guidance on the following key items:

- Containment Measures
- Application and Infrastructure Hardening
- Logging and Hunting Recommendations

## LEMURLOOT Analysis

LEMURLOOT is a web shell written in C# tailored to interact with the MOVEit Transfer platform. The malware authenticates incoming connections via a hard-coded password and can run commands that will download files from the MOVEit Transfer system, extract its Azure system settings, retrieve detailed record information, create and insert a particular user, or delete this same user. Data returned to the system interacting with LEMURLOOT is gzip compressed.

### Authentication and Database Connection

LEMURLOOT first checks if an incoming HTTP request contains the header field X-siLock-Comment and a corresponding 36-character GUID-formatted value, which varies across samples. It effectively uses this GUID as a password and returns an HTTP 404 status code to clients that do not pass the expected header field and value.

If the correct password is passed to LEMURLOOT, it sends a header response X-siLock-Comment and value comment, indicating the connection is successful and can accept tasking. The malware connects to a SQL server from the executing host using the settings retrieved using SystemSettings.DatabaseSettings(). It then processes data received from the connecting client, parsing expected commands from the following HTTP header fields: X-siLock-Step1, X-siLock-Step2, and X-siLock-Step3.

### X-siLock-Step1 Command Sequence

1.  If the value of the header field X-siLock-Step1 is -1, LEMURLOOT retrieves and returns the Azure system settings from MOVEit Transfer, including the configured Azure Blog storage account, and its associated key and container (AzureBlobStorageAccount, AzureBlobKey, and AzureBlobContainer). It then performs SQL queries to retrieve files, file size, folders, file owners, and institution name data. The resulting data is gzip compressed and returned to the client interacting with LEMURLOOT.
2.  If the X-siLock-Step1 header field value is -2, it deletes a user account with the LoginName and RealName set to "Health Check Service" using the SQL command in Figure 1. Note that this user is inserted using the following functionality.

<!-- -->

    Delete FROM users WHERE RealName='Health Check Service' 

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;display:block;font-size:16px;font-style:italic;margin-top:8px;width:100%;text-align:center">

Figure 1: MOVEit user deletion command

</div>

</div>

### X-siLock-Step2 and X-siLock-Step3 Command Sequence 

1.  If the value of header field X-siLock-Step1 is neither -1 or -2, the malware parses the values from header fields X-siLock-Step2 and X-siLock-Step3 and stores them in variables named fileid and folderid, respectively.
2.  If the values of fileid and folderid are not null, the malware retrieves the file from the local MOVEit Transfer system with these same values, gzip compresses it, and returns it to the connecting client.
3.  If the fileid and folderid variables are null, LEMURLOOT attempts to identify an existing account with permission level “30” and InstID = the value set from "X-siLock-Step1" otherwise it creates a new account with a randomly generated username and with LoginName and RealName values set to "Health Check Service" This account is inserted it into an active MOVEit application session.

## Attribution

Mandiant initially attributed this activity to UNC4857, which has now been merged into FIN11 based on targeting, infrastructure, certificate, and data leak site (DLS) overlaps. The activity is reminiscent of prior mass exploitation events targeting file transfer software and leading to FIN11-attributed data theft extortion via the CL0P^\_- LEAKS data leak site (DLS).

- FIN11-attributed data theft extortion has occurred following exploitation of multiple other file transfer systems. From late 2020 to early 2021, threat actors <a href="https://cloud.google.com/blog/topics/threat-intelligence/accellion-fta-exploited-for-data-theft-and-extortion" rel="noopener" target="_blank"><u>exploited</u></a> multiple zero-day vulnerabilities in Accellion's legacy File Transfer Appliance (FTA) to install the DEWMODE web shell. Similarly, in early 2023, threat actors exploited GoAnywhere Managed File Transfer (MFT) vulnerability CVE-2023-0669.
- Mandiant has identified numerous overlaps in the ISPs, netblocks, and IP addresses used in this campaign and historical FIN11 operations.
  - Notably, an IP address that was attempting exploitation of CVE-2023-34362 was used by FIN11 as early as mid-January 2023. At the time this system was first used by FIN11 it was hosting an RDP service on TCP port 3389. This service was still active and presenting the same x509 certificate when UNC4857's use of the system began.
- On June 5, 2023, Bleeping Computer claimed that someone affiliated with the CLOP ransomware group stated that they were behind incidents in which the MOVEit transfer system vulnerability was exploited for data theft. On June 6, 2023, a post on the CL0P^\_- LEAKS DLS claimed responsibility for this activity (Figure 2).

</div>

</div>

<div class="section QzPuud">

<div>

<div class="section">

<figure class="NEBdNd">
<section class="PBkdHd DhGbH" data-jscontroller="SCGBie" data-jsaction="rcuQ6b:npT2md">
<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/moveit-fig2-leaks-post_oyvd.max-1600x1600.png" class="JcsBte mZzdH ZOnyjc" data-jsname="P3Vluc" data-jsaction="click:HTIlC" loading="lazy" alt="https://storage.googleapis.com/gweb-cloudblog-publish/images/moveit-fig2-leaks-post_oyvd.max-1600x1600.png" />
<section class="glue-modal glue-modal--dark QHdDac" role="dialog" aria-modal="true">
<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/moveit-fig2-leaks-post_oyvd.max-1600x1600.png" class="JcsBte mZzdH ZOnyjc" data-jsname="P3Vluc" data-jsaction="click:HTIlC" loading="lazy" alt="https://storage.googleapis.com/gweb-cloudblog-publish/images/moveit-fig2-leaks-post_oyvd.max-1600x1600.png" />
</section>
</section>
</figure>

<div class="nRhiJb-cHYyed nRhiJb-DbgRPb-R6PoUb-ma6Yeb ZpqjUe">

<div jsaction="rcuQ6b:npT2md" jscontroller="M0Q3Qb" is-cws-richtext="true">

Figure 2: CL0P^\_- LEAKS DLS post

</div>

</div>

</div>

</div>

</div>

<div class="section Wy08Ac nRhiJb-qJTHM-OWXEXe-hJDwNd nRhiJb-DbgRPb-II5mzb-cGMI2b">

<div jsaction="rcuQ6b:npT2md" jscontroller="M0Q3Qb" is-cws-richtext="true">

## Implications

Mandiant routinely observes threat actors with varying motivations targeting sensitive data. For example, state-sponsored threat actors have demonstrated ongoing interest in targeting entities with policy research, military and government files, intellectual property, and personally identifiable information. Cyber criminals can also directly monetize stolen data via extortion operations, post it for sale on underground forums, or leverage it in secondary operations such as business email compromise.

Mandiant has not yet directly observed any extortion emails sent to confirmed victims. However, in prior cases where FIN11 exploited vulnerabilities in secure file transfer systems, the threat actors did not send extortion emails demanding a payment in return for not publishing the data on the CL0P^\_- LEAKS DLS until several weeks later. It is plausible that FIN11 delayed sending the ransom emails in an attempt to extend the amount of time that the zero-day vulnerabilities remained undetected and thus increase the number of victims and/or capacity to negotiate with a large number of victims simultaneously. Although the CLOP brand has posted to their DLS suggesting victims should initiate contact, if their TTPs remain consistent it is likely that the group will begin to initiate contact with some impacted organizations in the coming days and/or weeks.

## Detections

The following YARA rules are not intended to be used on production systems or to inform blocking rules without first being validated through an organization's own internal testing processes to ensure appropriate performance and limit the risk of false positives. These rules are intended to serve as a starting point for hunting efforts to identify LEMURLOOT payloads; however, they may need adjustment over time if the malware family changes.

 

    rule M_Webshell_LEMURLOOT_DLL_1 {
        meta:
            disclaimer = "This rule is meant for hunting and is not tested to run in a production environment"
            description = "Detects the compiled DLLs generated from human2.aspx LEMURLOOT payloads."
            sample = "c58c2c2ea608c83fad9326055a8271d47d8246dc9cb401e420c0971c67e19cbf"
            date = "2023/06/01"
            version = "1"
        strings:
            $net = "ASP.NET"
            $human = "Create_ASP_human2_aspx"
            $s1 = "X-siLock-Comment" wide
            $s2 = "X-siLock-Step3" wide
            $s3 = "X-siLock-Step2" wide
            $s4 = "Health Check Service" wide
            $s5 = "attachment; filename={0}" wide
        condition:
            uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550 and
            filesize < 15KB and
            $net and
            (
                ($human and 2 of ($s*)) or
                (3 of ($s*))
            )
    }

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;display:block;font-size:16px;font-style:italic;margin-top:8px;width:100%;text-align:center">

YARA rule for detecting compiled LEMURLOOT DLLs

</div>

<div style="color:#5f6368;display:block;font-size:16px;font-style:italic;margin-top:8px;width:100%;text-align:center">

 

</div>

</div>

    rule M_Webshell_LEMURLOOT_1 {
        meta:
            disclaimer = "This rule is meant for hunting and is not tested to run in a production environment"
            description = "Detects the LEMURLOOT ASP.NET scripts"
            md5 = "b69e23cd45c8ac71652737ef44e15a34"
            sample = "cf23ea0d63b4c4c348865cefd70c35727ea8c82ba86d56635e488d816e60ea45x"
            date = "2023/06/01"
            version = "1"
        strings:
            $head = "<%@ Page"
            $s1 = "X-siLock-Comment"
            $s2 = "X-siLock-Step"
            $s3 = "Health Check Service"
            $s4 = /pass, \"[a-z0-9]{8}-[a-z0-9]{4}/
            $s5 = "attachment;filename={0}"
        condition:
            filesize > 5KB and filesize < 10KB and
            (
                ($head in (0..50) and 2 of ($s*)) or
                (3 of ($s*))
            )
    }

<div style="color:#5f6368;display:block;font-size:16px;font-style:italic;margin-top:8px;width:100%;text-align:center">

YARA rule for detecting LEMURLOOT ASP.NET scripts

</div>

## Indicators

<div>

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

|                                   |                                                                   |
|-----------------------------------|-------------------------------------------------------------------|
| **MD5**                           | **SHA256**                                                        |
| 00c6bce35c40ce1601aa06c4e808c0f1  | 38e69f4a6d2e81f28ed2dc6df0daf31e73ea365bd2cfc90ebc31441404cca264  |
| 04b474e8db353d368e2d791ba5dee6d6  | 3a977446ed70b02864ef8cfa3135d8b134c93ef868a4cc0aa5d3c2a74545725b  |
| 11eadcf3f1bc9b0ed6994c3ede299ce8  | b1c299a9fe6076f370178de7b808f36135df16c4e438ef6453a39565ff2ec272  |
| 317552cac7035e35f7bdfc2162dfd29c  | c77438e8657518221613fbce451c664a75f05beea2184a3ae67f30ea71d34f37  |
| 359a1141a79480555aa996fd6d9e4af1  | 702421bcee1785d93271d311f0203da34cc936317e299575b06503945a6ea1e0  |
| 44d8e68c7c4e04ed3adacb5a88450552  | 387cee566aedbafa8c114ed1c6b98d8b9b65e9f178cf2f6ae2f5ac441082747a  |
| 45685c190c91ebe0966e8a0aeca31280  | 4359aead416b1b2df8ad9e53c497806403a2253b7e13c03317fc08ad3b0b95bf  |
| 538d6e172d18d4cebeac211873779ba5  | daaa102d82550f97642887514093c98ccd51735e025995c2cc14718330a856f4  |
| 67fca3e84490dfdddf72e9ba558b589a  | 6015fed13c5510bbb89b0a5302c8b95a5b811982ff6de9930725c4630ec4011d  |
| 7d5e5537c5346d764f067f66cca426ba  | 9d1723777de67bc7e11678db800d2a32de3bcd6c40a629cd165e3f7bbace8ead  |
| 8cd6c75e6160b90de2a52c967b3d4846  | c56bcb513248885673645ff1df44d3661a75cfacdce485535da898aa9ba320d4  |
| 8d88e451e39506ae258f3aa99da8db9a  | 0ea05169d111415903a1098110c34cdbbd390c23016cd4e179dd9ef507104495  |
| 911230b5dca1c43f6d22e65c66b0f6b1  | d49cf23d83b2743c573ba383bf6f3c28da41ac5f745cde41ef8cd1344528c195  |
| 96d467fd9663cf2e5572f8529e54f13e  | 5b566de1aa4b2f79f579cdac6283b33e98fdc8c1cfa6211a787f8156848d67ff  |
| 9f3c306dabc3f349b343251f4443412c  | f0d85b65b9f6942c75271209138ab24a73da29a06bc6cc4faeddcb825058c09d  |
| a85299f78ab5dd05e7f0f11ecea165ea  | fe5f8388ccea7c548d587d1e2843921c038a9f4ddad3cb03f3aa8a45c29c6a2f  |
| b1bdad086567efd202babf56eac17e1d  | 9e89d9f045664996067a05610ea2b0ad4f7f502f73d84321fb07861348fdc24a  |
| b52e56bfc03878cc5cb9eae9d3896808  | ea433739fb708f5d25c937925e499c8d2228bf245653ee89a6f3d26a5fd00b7a  |
| b69e23cd45c8ac71652737ef44e15a34  | cf23ea0d63b4c4c348865cefd70c35727ea8c82ba86d56635e488d816e60ea45  |
| bf7c1dd613101c0a95027249a5fcb759  | 2413b5d0750c23b07999ec33a5b4930be224b661aaf290a0118db803f31acbc5  |
| c2db1091eb7bac28461877f736d86d83  | 348e435196dd795e1ec31169bd111c7ec964e5a6ab525a562b17f10de0ab031d  |
| d71a6b5ae3d89dc33cbbb6877e493d52  | b9a0baf82feb08e42fa6ca53e9ec379e79fbe8362a7dac6150eb39c2d33d94ad  |
| ddd95f1c76a1d50b997b2e64274f386a  | a1269294254e958e0e58fc0fe887ebbc4201d5c266557f09c3f37542bd6d53d7  |
| e9a5f0c7656329ced63d4c8742da51b4  | 48367d94ccb4411f15d7ef9c455c92125f3ad812f2363c4d2e949ce1b615429a  |
| eea4d43f9e3700ebcd61405776eb249a  | d477ec94e522b8d741f46b2c00291da05c72d21c359244ccb1c211c12b635899  |
| fbba113d1d121220fa43f90b3a20870a  | 3ab73ea9aebf271e5f3ed701286701d0be688bf7ad4fb276cb4fbe35c8af8409  |

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<div style="color:#5f6368;display:block;font-size:16px;font-style:italic;margin-top:8px;width:100%;text-align:center">

LEMURLOOT Samples

</div>

</div>

## Mandiant Security Validation Actions

Organizations can validate their security controls using the following actions with <a href="https://cloud.google.com/security/products/mandiant-security-validation" rel="noopener" target="_blank"><u>Mandiant Security Validation</u></a>.

  

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

<div style="color:#5f6368;overflow-x:auto;overflow-y:hidden;width:100%">

|             |                                                                                                            |
|-------------|------------------------------------------------------------------------------------------------------------|
| **VID**     | **Name**                                                                                                   |
| A106-469    | Malicious File Transfer - LEMURLOOT, Download, Variant \#1                                                 |
| A106-467    | Malicious File Transfer - LEMURLOOT, Download, Variant \#2                                                 |
| A106-472    | Malicious File Transfer - LEMURLOOT, Download, Variant \#3                                                 |
| A106-468    | Web Application Vulnerability - FIN11, MOVEit Transfer SQL Injection CVE-2023-34362                        |
| A106-470    | Web Shell Activity - FIN11, LEMURLOOT, Delete Database User                                                |
| A106-471    | Web Shell Activity - FIN11, LEMURLOOT, Retrieve File                                                       |
| S100-281    | Malicious Activity Scenario - Campaign 23-037, FIN11 Utilizing a Critical Vulnerability in MOVEit Transfer |

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

## Acknowledgements

Beyond the listed authors are dozens of consultants and analysts who have already been working to help our clients with cases related to exploitation of CVE-2023-34362. We would also like to specifically thank Raymond Leong from the Mandiant FLARE team for his invaluable support.

</div>

</div>

</div>

<div class="section kcBhad">

<div class="section Fabbec">

<span class="WrMNjb">Posted in</span>

- <a href="https://cloud.google.com/blog/topics/threat-intelligence" data-track-metadata-position="body" data-track-metadata-eventdetail="cloud.google.com/blog/topics/threat-intelligence" data-track-metadata-module="tag list" data-track-metadata-module_headline="posted in">Threat Intelligence</a>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<div class="section nRhiJb-DARUcf" track-metadata-module="related articles" track-metadata-module_headline="related articles">

<div class="nRhiJb-DbgRPb-c5RTEf-ma6Yeb nRhiJb-DbgRPb-wNfPc-cGMI2b">

##### Related articles

<div class="section m9cUGf HGev3 nJD2Qe nRhiJb-ObfsIf">

<div class="QaGyvd nRhiJb-kR0ZEf-OWXEXe-GV1x9e-c5RTEf nRhiJb-kR0ZEf-OWXEXe-GV1x9e-qWD73c-V2iZpe">

<div class="mA0uBe">

<a href="https://cloud.google.com/blog/topics/threat-intelligence/vulnerability-discovery-and-exploitation-trends-in-the-ai-era" class="lD2oe" data-track-name="vulnerability discovery and exploitation trends in the ai era" data-track-type="card" data-track-metadata-eventdetail="cloud.google.com/blog/topics/threat-intelligence/vulnerability-discovery-and-exploitation-trends-in-the-ai-era"></a>

<div class="AhkbS">

<div class="hqnDEf">

<div class="section PBkdHd">

<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BANN.max-700x700.png" class="D5RK8d" loading="lazy" alt="https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BANN.max-700x700.png" />

</div>

</div>

<div class="JUOx5b">

<div class="Qwf2Db-MnozTc Qwf2Db-MnozTc-OWXEXe-MnozTc-qWD73c nRhiJb-DbgRPb-c5RTEf-ma6Yeb nRhiJb-BFbNVe-r8s4j-bMElCd FI6Gl nRhiJb-fmcmS-oXtfBe" track-name="threat intelligence" track-type="tag">

Threat Intelligence

</div>

### Vulnerability Discovery and Exploitation Trends in the AI Era

By Google Threat Intelligence Group • 17-minute read

</div>

</div>

</div>

</div>

<div class="QaGyvd nRhiJb-kR0ZEf-OWXEXe-GV1x9e-c5RTEf nRhiJb-kR0ZEf-OWXEXe-GV1x9e-qWD73c-V2iZpe">

<div class="mA0uBe">

<a href="https://cloud.google.com/blog/topics/threat-intelligence/defending-against-active-exploitation-of-citrix-netscaler-adc-and-gateway-appliances" class="lD2oe" data-track-name="defending against active exploitation of citrix netscaler adc and gateway appliances" data-track-type="card" data-track-metadata-eventdetail="cloud.google.com/blog/topics/threat-intelligence/defending-against-active-exploitation-of-citrix-netscaler-adc-and-gateway-appliances"></a>

<div class="AhkbS">

<div class="hqnDEf">

<div class="section PBkdHd">

<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BANN.max-700x700.png" class="D5RK8d" loading="lazy" alt="https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BANN.max-700x700.png" />

</div>

</div>

<div class="JUOx5b">

<div class="Qwf2Db-MnozTc Qwf2Db-MnozTc-OWXEXe-MnozTc-qWD73c nRhiJb-DbgRPb-c5RTEf-ma6Yeb nRhiJb-BFbNVe-r8s4j-bMElCd FI6Gl nRhiJb-fmcmS-oXtfBe" track-name="threat intelligence" track-type="tag">

Threat Intelligence

</div>

### Defending Against Active Exploitation of Citrix NetScaler ADC and Gateway Appliances

By Mandiant • 29-minute read

</div>

</div>

</div>

</div>

<div class="QaGyvd nRhiJb-kR0ZEf-OWXEXe-GV1x9e-c5RTEf nRhiJb-kR0ZEf-OWXEXe-GV1x9e-qWD73c-V2iZpe">

<div class="mA0uBe">

<a href="https://cloud.google.com/blog/topics/threat-intelligence/shinyhunters-renewed-mass-exploitation-campaign-targeting-oracle-peoplesoft" class="lD2oe" data-track-name="shinyhunters renewed mass exploitation campaign targeting oracle peoplesoft" data-track-type="card" data-track-metadata-eventdetail="cloud.google.com/blog/topics/threat-intelligence/shinyhunters-renewed-mass-exploitation-campaign-targeting-oracle-peoplesoft"></a>

<div class="AhkbS">

<div class="hqnDEf">

<div class="section PBkdHd">

<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BANN.max-700x700.png" class="D5RK8d" loading="lazy" alt="https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BANN.max-700x700.png" />

</div>

</div>

<div class="JUOx5b">

<div class="Qwf2Db-MnozTc Qwf2Db-MnozTc-OWXEXe-MnozTc-qWD73c nRhiJb-DbgRPb-c5RTEf-ma6Yeb nRhiJb-BFbNVe-r8s4j-bMElCd FI6Gl nRhiJb-fmcmS-oXtfBe" track-name="threat intelligence" track-type="tag">

Threat Intelligence

</div>

### ShinyHunters Renewed Mass Exploitation Campaign Targeting Oracle PeopleSoft

By Mandiant • 18-minute read

</div>

</div>

</div>

</div>

<div class="QaGyvd nRhiJb-kR0ZEf-OWXEXe-GV1x9e-c5RTEf nRhiJb-kR0ZEf-OWXEXe-GV1x9e-qWD73c-V2iZpe">

<div class="mA0uBe">

<a href="https://cloud.google.com/blog/topics/threat-intelligence/hardening-code-pipelines-and-ci-cd-infrastructure" class="lD2oe" data-track-name="proactive defense: hardening code pipelines and ci/cd infrastructure" data-track-type="card" data-track-metadata-eventdetail="cloud.google.com/blog/topics/threat-intelligence/hardening-code-pipelines-and-ci-cd-infrastructure"></a>

<div class="AhkbS">

<div class="hqnDEf">

<div class="section PBkdHd">

<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BANN.max-700x700.png" class="D5RK8d" loading="lazy" alt="https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BANN.max-700x700.png" />

</div>

</div>

<div class="JUOx5b">

<div class="Qwf2Db-MnozTc Qwf2Db-MnozTc-OWXEXe-MnozTc-qWD73c nRhiJb-DbgRPb-c5RTEf-ma6Yeb nRhiJb-BFbNVe-r8s4j-bMElCd FI6Gl nRhiJb-fmcmS-oXtfBe" track-name="threat intelligence" track-type="tag">

Threat Intelligence

</div>

### Proactive Defense: Hardening Code Pipelines and CI/CD Infrastructure

By Mandiant • 15-minute read

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

### Footer Links

<div class="section nRhiJb-haF9Wb r2W5Od">

<div class="section nRhiJb-DX2B6">

<div class="nRhiJb-j5y3u">

#### Follow us

- <a href="https://www.x.com/googlecloud" class="nRhiJb-ARYxNe" target="_blank" rel="noopener" data-track-name="x" data-track-type="social link" data-track-metadata-position="footer" data-track-metadata-eventdetail="www.x.com/googlecloud" data-track-metadata-module="footer" data-track-metadata-module_headline="follow us"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTEzLjksMTAuNUwyMS4xLDJoLTEuN2wtNi4zLDcuNEw4LDJIMi4ybDcuNiwxMS4xTDIuMiwyMmgxLjdsNi43LTcuOEwxNiwyMmg1LjhMMTMuOSwxMC41TDEzLjksMTAuNXogTTExLjUsMTMuMmwtMC44LTEuMSBMNC42LDMuM2gyLjdsNSw3LjFsMC44LDEuMWw2LjUsOS4yaC0yLjdMMTEuNSwxMy4yTDExLjUsMTMuMnoiIC8+PC9zdmc+" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-xgZe3c nRhiJb-Bz112c-OWXEXe-DX2B6" /></a>
- <a href="https://www.youtube.com/googlecloud" class="nRhiJb-ARYxNe" target="_blank" rel="noopener" data-track-name="youtube" data-track-type="social link" data-track-metadata-position="footer" data-track-metadata-eventdetail="www.youtube.com/googlecloud" data-track-metadata-module="footer" data-track-metadata-module_headline="follow us"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTIzLjc0IDcuMXMtLjIzLTEuNjUtLjk1LTIuMzdjLS45MS0uOTYtMS45My0uOTYtMi40LTEuMDJDMTcuMDQgMy40NyAxMiAzLjUgMTIgMy41cy01LjAyLS4wMy04LjM3LjIxYy0uNDYuMDYtMS40OC4wNi0yLjM5IDEuMDJDLjUyIDUuNDUuMjggNy4xLjI4IDcuMVMuMDQgOS4wNSAwIDEwLjk4VjEzYy4wNCAxLjk0LjI4IDMuODcuMjggMy44N3MuMjQgMS42NS45NiAyLjM4Yy45MS45NSAyLjEuOTIgMi42NCAxLjAyIDEuODguMTggNy45MS4yMiA4LjEyLjIyIDAgMCA1LjA1LjAxIDguNC0uMjMuNDYtLjA2IDEuNDgtLjA2IDIuMzktMS4wMi43Mi0uNzIuOTYtMi4zNy45Ni0yLjM3cy4yNC0xLjk0LjI1LTMuODd2LTIuMDJjLS4wMi0xLjkzLS4yNi0zLjg4LS4yNi0zLjg4ek05LjU3IDE1LjVWOC40OUwxNiAxMi4xMyA5LjU3IDE1LjV6IiAvPjwvc3ZnPg==" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-xgZe3c nRhiJb-Bz112c-OWXEXe-DX2B6" /></a>
- <a href="https://www.linkedin.com/showcase/google-cloud" class="nRhiJb-ARYxNe" target="_blank" rel="noopener" data-track-name="linkedin" data-track-type="social link" data-track-metadata-position="footer" data-track-metadata-eventdetail="www.linkedin.com/showcase/google-cloud" data-track-metadata-module="footer" data-track-metadata-module_headline="follow us"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTIwIDJINGMtMS4xIDAtMS45OS45LTEuOTkgMkwyIDIwYzAgMS4xLjkgMiAyIDJoMTZjMS4xIDAgMi0uOSAyLTJWNGMwLTEuMS0uOS0yLTItMnpNOCAxOUg1di05aDN2OXpNNi41IDguMzFjLTEgMC0xLjgxLS44MS0xLjgxLTEuODFTNS41IDQuNjkgNi41IDQuNjlzMS44MS44MSAxLjgxIDEuODFTNy41IDguMzEgNi41IDguMzF6TTE5IDE5aC0zdi01LjNjMC0uODMtLjY3LTEuNS0xLjUtMS41cy0xLjUuNjctMS41IDEuNVYxOWgtM3YtOWgzdjEuMmMuNTItLjg0IDEuNTktMS40IDIuNS0xLjQgMS45MyAwIDMuNSAxLjU3IDMuNSAzLjVWMTl6IiAvPjwvc3ZnPg==" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-xgZe3c nRhiJb-Bz112c-OWXEXe-DX2B6" /></a>
- <a href="https://www.instagram.com/googlecloud/" class="nRhiJb-ARYxNe" target="_blank" rel="noopener" data-track-name="instagram" data-track-type="social link" data-track-metadata-position="footer" data-track-metadata-eventdetail="www.instagram.com/googlecloud/" data-track-metadata-module="footer" data-track-metadata-module_headline="follow us"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTEyLDAgQzE1LjMsMCAxNS43LDAgMTcsMCBDMTguMywwLjEgMTkuMSwwLjMgMTkuOSwwLjYgQzIwLjcsMC45IDIxLjMsMS4zIDIyLDIgQzIyLjcsMi43IDIzLjEsMy40IDIzLjMsNC4yIEMyMy42LDUgMjMuOCw1LjggMjMuOSw3LjEgQzI0LDguMyAyNCw4LjcgMjQsMTIgQzI0LDE1LjMgMjQsMTUuNyAyMy45LDE2LjkgQzIzLjgsMTguMiAyMy42LDE5IDIzLjMsMTkuOCBDMjMsMjAuNiAyMi42LDIxLjIgMjEuOSwyMS45IEMyMS4zLDIyLjYgMjAuNiwyMyAxOS44LDIzLjMgQzE5LDIzLjYgMTguMiwyMy44IDE2LjksMjMuOSBDMTUuNywyNCAxNS4zLDI0IDEyLDI0IEM4LjcsMjQgOC4zLDI0IDcsMjQgQzUuNywyMy45IDQuOSwyMy43IDQuMSwyMy40IEMzLjMsMjMuMSAyLjcsMjIuNyAyLDIyIEMxLjMsMjEuMyAwLjksMjAuNiAwLjcsMTkuOCBDMC40LDE5IDAuMiwxOC4yIDAuMSwxNi45IEMwLDE1LjcgMCwxNS4zIDAsMTIgQzAsOC43IDAsOC4zIDAuMSw3LjEgQzAuMSw1LjggMC4zLDQuOSAwLjYsNC4xIEMwLjksMy40IDEuMywyLjcgMiwyIEMyLjcsMS4zIDMuNCwwLjkgNC4xLDAuNiBDNC45LDAuMyA1LjgsMC4xIDcuMSwwLjEgQzguMywwIDguNywwIDEyLDAgWiBNMTIsMi4yIEM4LjgsMi4yIDguNCwyLjIgNy4yLDIuMiBDNiwyLjMgNS4zLDIuNSA0LjksMi42IEM0LjQsMi45IDQsMy4xIDMuNSwzLjUgQzMuMSwzLjkgMi44LDQuMyAyLjYsNC45IEMyLjUsNS4zIDIuMyw2IDIuMyw3LjIgQzIuMiw4LjQgMi4yLDguOCAyLjIsMTIgQzIuMiwxNS4yIDIuMiwxNS41IDIuMywxNi44IEMyLjMsMTcuOSAyLjUsMTguNiAyLjcsMTkgQzIuOSwxOS42IDMuMiwyMCAzLjYsMjAuNCBDNCwyMC44IDQuNCwyMS4xIDUsMjEuMyBDNS40LDIxLjUgNiwyMS42IDcuMiwyMS43IEM4LjQsMjEuOCA4LjgsMjEuOCAxMiwyMS44IEMxNS4yLDIxLjggMTUuNSwyMS44IDE2LjgsMjEuNyBDMTcuOSwyMS43IDE4LjYsMjEuNSAxOSwyMS4zIEMxOS42LDIxLjEgMjAsMjAuOCAyMC40LDIwLjQgQzIwLjgsMjAgMjEuMSwxOS42IDIxLjMsMTkgQzIxLjUsMTguNiAyMS42LDE4IDIxLjcsMTYuOCBDMjEuOCwxNS42IDIxLjgsMTUuMiAyMS44LDEyIEMyMS44LDguOCAyMS44LDguNSAyMS43LDcuMiBDMjEuNyw2LjEgMjEuNSw1LjQgMjEuMyw1IEMyMS4xLDQuNCAyMC44LDQgMjAuNCwzLjYgQzIwLDMuMiAxOS42LDIuOSAxOSwyLjcgQzE4LjYsMi41IDE4LDIuNCAxNi44LDIuMyBDMTUuNiwyLjIgMTUuMiwyLjIgMTIsMi4yIFogTTEyLDUuOCBDMTUuNCw1LjggMTguMiw4LjYgMTguMiwxMiBDMTguMiwxNS40IDE1LjQsMTguMiAxMiwxOC4yIEM4LjYsMTguMiA1LjgsMTUuNCA1LjgsMTIgQzUuOCw4LjYgOC42LDUuOCAxMiw1LjggWiBNMTIsMTYgQzE0LjIsMTYgMTYsMTQuMiAxNiwxMiBDMTYsOS44IDE0LjIsOCAxMiw4IEM5LjgsOCA4LDkuOCA4LDEyIEM4LDE0LjIgOS44LDE2IDEyLDE2IFogTTE4LjQsNyBDMTcuNjI2ODAxNCw3IDE3LDYuMzczMTk4NjUgMTcsNS42IEMxNyw0LjgyNjgwMTM1IDE3LjYyNjgwMTQsNC4yIDE4LjQsNC4yIEMxOS4xNzMxOTg2LDQuMiAxOS44LDQuODI2ODAxMzUgMTkuOCw1LjYgQzE5LjgsNi4zNzMxOTg2NSAxOS4xNzMxOTg2LDcgMTguNCw3IFoiIC8+PC9zdmc+" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-xgZe3c nRhiJb-Bz112c-OWXEXe-DX2B6" /></a>
- <a href="https://www.facebook.com/googlecloud/" class="nRhiJb-ARYxNe" target="_blank" rel="noopener" data-track-name="facebook" data-track-type="social link" data-track-metadata-position="footer" data-track-metadata-eventdetail="www.facebook.com/googlecloud/" data-track-metadata-module="footer" data-track-metadata-module_headline="follow us"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTIwIDJINGMtMS4xIDAtMS45OS45LTEuOTkgMkwyIDIwYzAgMS4xLjkgMiAyIDJoMTZjMS4xIDAgMi0uOSAyLTJWNGMwLTEuMS0uOS0yLTItMnptLTEgMnYzaC0yYy0uNTUgMC0xIC40NS0xIDF2MmgzdjNoLTN2N2gtM3YtN2gtMnYtM2gyVjcuNUMxMyA1LjU3IDE0LjU3IDQgMTYuNSA0SDE5eiIgLz48L3N2Zz4=" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-xgZe3c nRhiJb-Bz112c-OWXEXe-DX2B6" /></a>

</div>

</div>

</div>

<div class="section nRhiJb-hlZHHf rtKYfe">

<div class="nRhiJb-vQnuyc UXgbsb">

<a href="https://cloud.google.com/" class="ZOs9zc" data-track-name="google" data-track-type="footer link" data-track-metadata-position="footer" data-track-metadata-eventdetail="cloud.google.com/" data-track-metadata-module="footer" title="Google Cloud"><img src="https://www.gstatic.com/cgc/super_cloud_gradient.png" class="nRhiJb-vQnuyc-RJLb9c" alt="Cloud logo" /></a>

</div>

- <a href="https://cloud.google.com/" class="nRhiJb-Fx4vi" data-track-name="google cloud" data-track-type="footer link" data-track-metadata-position="footer" data-track-metadata-eventdetail="cloud.google.com/" data-track-metadata-module="footer">Google Cloud</a>
- <a href="https://cloud.google.com/products/" class="nRhiJb-Fx4vi" data-track-name="google cloud products" data-track-type="footer link" data-track-metadata-position="footer" data-track-metadata-eventdetail="cloud.google.com/products/" data-track-metadata-module="footer">Google Cloud Products</a>
- <a href="https://myaccount.google.com/privacypolicy?hl=en-US" class="nRhiJb-Fx4vi" target="_blank" data-track-name="privacy" data-track-type="footer link" data-track-metadata-position="footer" data-track-metadata-eventdetail="myaccount.google.com/privacypolicy?hl=en-US" data-track-metadata-module="footer">Privacy</a>
- <a href="https://myaccount.google.com/termsofservice?hl=en-US" class="nRhiJb-Fx4vi" target="_blank" data-track-name="terms" data-track-type="footer link" data-track-metadata-position="footer" data-track-metadata-eventdetail="myaccount.google.com/termsofservice?hl=en-US" data-track-metadata-module="footer">Terms</a>
- <a href="https://cloud.google.com/blog/#" class="nRhiJb-Fx4vi glue-footer__link glue-cookie-notification-bar-control" aria-hidden="true" role="button" tabindex="0" target="_blank" data-track-name="cookies management controls" data-track-type="footer link" data-track-metadata-position="footer" data-track-metadata-eventdetail="#" data-track-metadata-module="footer">Cookies management controls</a>

<!-- -->

- <a href="https://support.google.com" class="nRhiJb-Fx4vi" target="_blank" data-track-name="help" data-track-type="footer link" data-track-metadata-position="footer" data-track-metadata-eventdetail="support.google.com" data-track-metadata-module="footer"><img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUteWVQZTVjLWg5ZDNoZCIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnptMSAxN2gtMnYtMmgydjJ6bTIuMDctNy43NWwtLjkuOTJDMTMuNDUgMTIuOSAxMyAxMy41IDEzIDE1aC0ydi0uNWMwLTEuMS40NS0yLjEgMS4xNy0yLjgzbDEuMjQtMS4yNmMuMzctLjM2LjU5LS44Ni41OS0xLjQxIDAtMS4xLS45LTItMi0ycy0yIC45LTIgMkg4YzAtMi4yMSAxLjc5LTQgNC00czQgMS43OSA0IDRjMCAuODgtLjM2IDEuNjgtLjkzIDIuMjV6IiAvPjwvc3ZnPg==" class="nRhiJb-Bz112c nRhiJb-Bz112c-OWXEXe-xgZe3c nRhiJb-Bz112c-OWXEXe-yePe5c-h9d3hd" />Help</a>
- Language‪English‬‪Deutsch‬‪Français‬‪한국어‬‪日本語‬

</div>