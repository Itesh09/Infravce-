<div class="wrapper">

<div class="top-bar">

<div class="logo">

<a href="/" aria-label="Home page"><img src="/static/img/logo.png" class="logo-img-light" srcset="/static/img/logo.png, /static/img/logo@4x.png 4x" width="54" height="20" alt="OSV logo" /> <img src="/static/img/logo-dark.png" class="logo-img-dark" srcset="/static/img/logo-dark.png, /static/img/logo-dark@4x.png 4x" width="54" height="20" alt="OSV logo" /></a>

</div>

- [Vulnerability Database](/list)
- [Blog](/blog)
- <a href="https://google.github.io/osv.dev/faq/" target="_blank">FAQ</a>
- <a href="https://google.github.io/osv.dev/" target="_blank">Docs</a>
  - <div class="search-toggle-container">

    <span class="material-icons">arrow_forward</span>
    <span class="material-icons">search</span>

    </div>

  - <a href="/blog/index.xml" class="logo-img" target="_blank" aria-label="RRS Feed"><img src="/static/img/feed.svg" class="logo-link" width="24" height="24" alt="RSS Feed" /></a>

  - <span class="material-icons icon-light-mode">light_mode</span> <span class="material-icons icon-dark-mode">dark_mode</span>

  - <a href="https://github.com/google/osv.dev" class="logo-img" target="_blank" aria-label="Go to our github page"><img src="/static/img/github-mark-white.svg" class="logo-link" width="24" height="24" alt="Github Logo" /></a>

</div>

<div class="blog-post-page">

<div class="mdc-layout-grid">

<div class="mdc-layout-grid__inner">

<div class="mdc-layout-grid__cell--span-12 post">

# OSV-Scanner v2.0.0-beta1 is ready!

<div class="author">

Posted by The OSV Team on Jan 29, 2025

</div>

<div class="content">

Today we’re excited to announce that the <a href="https://github.com/google/osv-scanner/releases/tag/v2.0.0-beta1" target="_blank" rel="noopener noreferrer">first beta of OSV-Scanner V2</a> is ready! The team has been hard at work in the past months to revamp OSV-Scanner under the hood (transitioning to <a href="https://github.com/google/osv-scalibr" target="_blank" rel="noopener noreferrer">OSV-Scalibr</a> , which we <a href="https://security.googleblog.com/2025/01/osv-scalibr-library-for-software.html" target="_blank" rel="noopener noreferrer">announced earlier this month</a> ) and building several new significant features.

This beta release does *not* introduce any breaking CLI changes - existing OSV-Scanner can use the tool in exactly the same way. The beta period is expected to last approximately one month. However, as this is a beta release, there may be breaking changes in the final release compared to the beta.

## Layer and base image-aware container scanning

A significant new feature is a rewritten, layer-aware container scanning support for Debian, Ubuntu, and Alpine container images. OSV-Scanner can now analyze container images to provide:

- Layers where a package was first introduced
- Layer history and commands
- Base images the image is based on
- OS/Distro the container is running on

This layer analysis leverages <a href="https://github.com/google/osv-scalibr" target="_blank" rel="noopener noreferrer">OSV-Scalibr</a> , and supports the following OSes and languages:

Distro Support:

- Alpine OS
- Debian
- Ubuntu

Language Artifacts Support:

- Go
- Java
- Node
- Python

Base image identification also leverages a <a href="https://docs.deps.dev/api/v3alpha/#querycontainerimages" target="_blank" rel="nofollow noopener noreferrer">new experimental API</a> provided by deps.dev. Check out their <a href="https://blog.deps.dev/base-container-image/index.html" target="_blank" rel="nofollow noopener noreferrer">technical blog post</a> for details on how this data is collected and queried.

For usage, run the new `scan image` command:

<div class="highlight">

``` chroma
osv-scanner scan image <image-name>:<tag>
```

</div>

Check out our <a href="https://google.github.io/osv-scanner/usage/scan-image" target="_blank" rel="noopener noreferrer">documentation</a> for more details.

## Interactive HTML output

A new interactive HTML output is now available. This provides a lot more interactivity and information compared to terminal only outputs, including:

- Severity breakdown
- Package and ID filtering
- Vulnerability importance filtering
- Full vulnerability advisory entries

And additionally for container image scanning:

- Layer filtering
- Image layer information
- Base image identification

![Illustration of HTML output for container image scanning](html-container.gif)

## Guided Remediation for Maven pom.xml

Last year we released a feature called <a href="https://osv.dev/blog/posts/announcing-guided-remediation-in-osv-scanner/" target="_blank" rel="noopener noreferrer">guided remediation</a> for npm. We have now expanded support to Maven pom.xml.

With guided remediation support for Maven, you can remediate vulnerabilities in both direct and transitive dependencies through direct version updates or overriding versions through dependency management.

We’ve introduced a few new features for our Maven support:

- A new remediation strategy `override` is introduced.
- Support for reading and writing pom.xml files, including writing changes to local parent pom files.
- Private registry can be specified to fetch Maven metadata.

The guided remediation support for Maven is only available in the non-interactive mode. For basic usage, run the following command:

<div class="highlight">

``` chroma
osv-scanner fix --non-interactive --strategy=override -M path/to/pom.xml
```

</div>

We also introduced machine readable output for guided remediation that makes it easier to integrate guided remediation into your workflow.

For more usage details on guided remediation, please see our <a href="https://google.github.io/osv-scanner/experimental/guided-remediation/" target="_blank" rel="noopener noreferrer">documentation</a> .

## Enhanced Dependency Extraction with `osv-scalibr`

With the help from <a href="https://github.com/google/osv-scalibr" target="_blank" rel="noopener noreferrer">OSV-Scalibr</a> , we now also have expanded support for the kinds of dependencies we can extract from projects and containers:

### Source manifests and lockfiles

- Haskell: `cabal.project.freeze`, `stack.yaml.lock`
- .NET: `deps.json`
- Python: `uv.lock`

### Artifacts

- node_modules
- Python wheels
- Java uber jars
- Go binaries

The full list of supported formats can be found <a href="https://google.github.io/osv-scanner/supported-languages-and-lockfiles/" target="_blank" rel="noopener noreferrer">here</a> .

The first beta doesn’t enable every single extractor currently available in OSV-Scalibr today. We’ll continue to add more leading up to the final 2.0.0 release.

OSV-Scalibr also makes it incredibly easy to add new extractors. Please file a <a href="https://github.com/google/osv-scalibr/issues" target="_blank" rel="noopener noreferrer">feature request</a> if a format you’re interested in is missing!

## Feedback and testing

You can find our latest release on GitHub <a href="https://github.com/google/osv-scanner/releases/tag/v2.0.0-beta1" target="_blank" rel="noopener noreferrer">here</a> , and our updated V2 documentation <a href="https://google.github.io/osv-scanner/" target="_blank" rel="noopener noreferrer">here</a> .

We still expect changes to be made, smaller new features to be added, and bugs to be shaken out leading up to the final v2.0.0 release. If you do give this a try, we’d appreciate any feedback you might have on our discussion topics:

- <a href="https://github.com/google/osv-scanner/discussions/1529" target="_blank" rel="noopener noreferrer">General V2 feedback</a>
- <a href="https://github.com/google/osv-scanner/discussions/1521" target="_blank" rel="noopener noreferrer">Container scanning feedback</a>

The OSV project is fully open source, and guided by the feedback from our open source community. Together we can build better open source tools to make vulnerability management easier and less noisy!

</div>

</div>

</div>

</div>

</div>

</div>