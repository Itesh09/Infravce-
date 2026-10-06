<div class="container" itemscope="" itemtype="http://schema.org/Article">

<div class="skipLink">

[Skip to site navigation (Press enter)](#nav)

</div>

<div class="content" role="main">

<div class="msgHead">

# <span class="subject"><a href="/search?l=debian-security-tracker-commits@alioth-lists.debian.net&amp;q=subject:%22%5C%5BGit%5C%5D%5C%5Bsecurity%5C-tracker%5C-team%5C%2Fsecurity%5C-tracker%5C%5D%5C%5Bmaster%5C%5D+Update+NOTEs+and+mark+CVE%5C-2025%5C-9086%5C%2Fcurl+as+not+affecting+bookworm%22&amp;o=newest" rel="nofollow"><span itemprop="name">[Git][security-tracker-team/security-tracker][master] Update NOTEs and mark CVE-2025-9086/curl as not affecting bookworm</span></a></span>

<span class="sender pipe"><a href="/search?l=debian-security-tracker-commits@alioth-lists.debian.net&amp;q=from:%22Carlos+Henrique+Lima+Melara+%5C%28%40charles%5C%29%22" rel="nofollow"><span itemprop="author" itemscope="" itemtype="http://schema.org/Person"><span itemprop="name">Carlos Henrique Lima Melara (@charles)</span></span></a></span> <span class="date"><a href="/search?l=debian-security-tracker-commits@alioth-lists.debian.net&amp;q=date:20260113" rel="nofollow">Tue, 13 Jan 2026 16:59:06 -0800</a></span>

</div>

<div class="msgBody" itemprop="articleBody">


    Carlos Henrique Lima Melara pushed to branch master at Debian Security Tracker 
    / security-tracker


    Commits:
    8a523acb by Carlos Henrique Lima Melara at 2026-01-13T21:56:19-03:00
    Update NOTEs and mark CVE-2025-9086/curl as not affecting bookworm

    Upstream had initially the wrong commit marked as introducing the
    vulnerability, turns out samueloph discovered it was introduced much
    later and it doesn't affect bookworm and older.

    - - - - -


    1 changed file:

    - data/CVE/list


    Changes:

    =====================================
    data/CVE/list
    =====================================
    @@ -47962,9 +47962,9 @@ CVE-2025-9086 (1. A cookie is set using the `secure` 
    keyword for `https://target
            {DLA-4432-1}
            - curl 8.16.0~rc2-1
            [trixie] - curl 8.14.1-2+deb13u1
    -       [bookworm] - curl <no-dsa> (Minor issue)
    +       [bookworm] - curl <not-affected> (Vulnerable code introduced later)
            NOTE: https://curl.se/docs/CVE-2025-9086.html
    -       NOTE: Introduced with: 
    https://github.com/curl/curl/commit/f24dc09d209a2f91ca38d854f0c15ad93f3d7e2d 
    (curl-7_31_0)
    +       NOTE: Introduced with: 
    https://github.com/curl/curl/commit/1aea05a6c2699e80c75936d58569851555acd603 
    (curl-8_13_0)
            NOTE: Fixed by: 
    https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb62b45dd37711300 
    (rc-8_16_0-1)
     CVE-2025-10148 (curl's websocket code did not update the 32 bit mask pattern 
    for each  ...)
            - curl 8.16.0-1


    View it on GitLab: 
    https://salsa.debian.org/security-tracker-team/security-tracker/-/commit/8a523acb00860e336ed26a4b517816337c6ba26b

    -- 
    View it on GitLab: 
    https://salsa.debian.org/security-tracker-team/security-tracker/-/commit/8a523acb00860e336ed26a4b517816337c6ba26b
    You're receiving this email because of your account on salsa.debian.org.

    _______________________________________________
    debian-security-tracker-commits mailing list
    [email protected]
    https://alioth-lists.debian.net/cgi-bin/mailman/listinfo/debian-security-tracker-commits

</div>

<div class="msgButtons margintopdouble">

- <a href="msg72205.html" class="button buttonleft" accesskey="p">Previous message</a>
- <a href="index.html#72206" class="button" accesskey="c">View by thread</a>
- <a href="maillist.html#72206" class="button" accesskey="i">View by date</a>
- <a href="msg72207.html" class="button buttonright" accesskey="n">Next message</a>

</div>

<span id="tslice"></span>

<div class="tSliceList margintopdouble">

</div>

<div class="overflow msgActions margintopdouble">

<div class="msgReply">

## Reply via email to

</div>

</div>

</div>

<div class="aside" role="complementary">

<div class="logo">

[<img src="/logo.png" width="247" height="88" alt="The Mail Archive" />](/)

</div>

Search the site

<div id="nav" class="nav margintop" role="navigation">

- [The Mail Archive home](/)
- [debian-security-tracker-commits - all messages](/debian-security-tracker-commits@alioth-lists.debian.net/)
- [debian-security-tracker-commits - about the list](/debian-security-tracker-commits@alioth-lists.debian.net/info.html)
- <a href="/search?l=debian-security-tracker-commits@alioth-lists.debian.net&amp;q=subject:%22%5C%5BGit%5C%5D%5C%5Bsecurity%5C-tracker%5C-team%5C%2Fsecurity%5C-tracker%5C%5D%5C%5Bmaster%5C%5D+Update+NOTEs+and+mark+CVE%5C-2025%5C-9086%5C%2Fcurl+as+not+affecting+bookworm%22&amp;o=newest&amp;f=1" id="e" title="e">Expand</a>
- [Previous message](msg72205.html "p")
- [Next message](msg72207.html "n")

</div>

<div class="listlogo margintopdouble">

</div>

<div class="margintopdouble">

</div>

</div>

</div>

<div class="footer" role="contentinfo">

- [The Mail Archive home](/)
- [Add your mailing list](/faq.html#newlist)
- [FAQ](/faq.html)
- [Support](/faq.html#support)
- [Privacy](/faq.html#privacy)
- <a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="3f090609095a5e0b5d0809080b5c600a0e5b0a5e0a0e5a0c5c0e0f090609060d7f58505b5e4d5b11525e5653">[email protected]</a>

</div>