"""Ecosystem-aware version normalisation.

This is the first real module because it is the highest-value part of the
identifier layer and it is testable with no CVE data at all. Every fixture in
``tests/fixtures/version_cases.json`` is a version string taken verbatim from a
documented production failure, not an invented example.

The failure this module exists to prevent (dependency-track#3774): on an
identical Rocky 9.4 SBOM, Dependency-Track reported 77 vulnerabilities and
Trivy CLI reported 27, and all 50 findings unique to Dependency-Track were
verified false positives. Root cause: DT sent ``version: "1:1.12.20-8.el9"``
with the epoch folded in and no release field, while Trivy sent
``version: "1.12.20"`` plus ``release: "8.el9"``.

Design commitments:

* Parsing failure returns ``confidence=0.0`` and ``upstream=None``. It never
  guesses, and it never returns something that looks comparable.
* Each ecosystem gets its own comparator, because a generic semver comparison is
  wrong for RPM, Debian, apk, and PyPI.
* Every non-obvious decision is recorded in ``notes`` so a wrong parse is
  diagnosable from the database alone.
"""

from __future__ import annotations

import re
from typing import Final

from packaging.version import InvalidVersion
from packaging.version import parse as pep440_parse

from infravce.models import Ecosystem, NormalisedVersion

__all__ = [
    "UnresolvableVersion",
    "detect_ecosystem",
    "normalise",
    "normalise_many",
]


class UnresolvableVersion(NormalisedVersion):
    """A version string that must not be used for range comparison.

    Constructed with ``upstream=None`` and ``confidence=0.0`` so that every
    downstream range comparison refuses it. ``is_resolved`` is therefore False.
    """

    @classmethod
    def for_raw(
        cls,
        raw: str,
        *,
        ecosystem: Ecosystem = Ecosystem.UNKNOWN,
        notes: tuple[str, ...] = (),
    ) -> UnresolvableVersion:
        return cls(
            ecosystem=ecosystem,
            raw=raw,
            upstream=None,
            confidence=0.0,
            notes=notes or ("unresolvable; excluded from range comparison",),
        )


# --------------------------------------------------------------------------- #
# Detection
# --------------------------------------------------------------------------- #

#: Immutable references carry no version at all. grype#2606 recorded the SHA as
#: the version and produced false positives against unrelated GHSA records.
_GIT_SHA = re.compile(r"^[0-9a-f]{7,40}$", re.IGNORECASE)
_DIGEST = re.compile(r"^(sha256|sha1|sha512|md5):[0-9a-f]{32,}$", re.IGNORECASE)
_GO_PSEUDOVERSION = re.compile(r"^v0\.0\.0-\d{14}-[0-9a-f]{12}$", re.IGNORECASE)
_RPM_EVR = re.compile(
    r"^(?:(?P<epoch>\d+):)?(?P<upstream>[^-]+)-(?P<release>[^-]+)(?:\.(?P<arch>.+))?$"
)
_RPM_EVR_PLAIN = re.compile(r"^(?:(?P<epoch>\d+):)?(?P<upstream>[0-9][^-]*)$")
#: A trailing ``.el9``/``.fc38``/``.rocky``/``.amzn2`` is an RPM vendor release.
_RPM_VENDOR_RELEASE = re.compile(
    r"\.(?:el\d+|fc\d+|rocky|amzn\d?|oe\d+|sles\d*|scientific|centos)\d*$", re.IGNORECASE
)
#: Debian/Debian-derived revision: ``10+deb12u12``, ``-12u5``, ``-1ubuntu1``.
_DEBIAN_REVISION = re.compile(r"(?:^|[-+.])(?:deb\d+u?\d*|ubuntu\d*)\d*$", re.IGNORECASE)
#: Characters that never appear in a distribution package version. Their presence
#: means the string is some other kind of identifier (a VCS ref, a Conan recipe
#: revision, a wildcard) that happens to reach the normaliser, and accepting it
#: would produce a comparable value for something that is not a release.
_NON_VERSION_CHARS = re.compile(r"[#*@\\/|]|^git-|^vcs-")

_APK = re.compile(r"^(?P<upstream>[^-]+)-r(?P<distro_revision>\d+)(?:-.*)?$")
_DEBIAN = re.compile(r"^(?P<upstream>.+?)(?:-(?P<distro_revision>[A-Za-z0-9.+~]+))?$")
_SEMVER = re.compile(
    r"^(?P<upstream>\d+\.\d+\.\d+)"
    r"(?:-(?P<pre_release>[0-9A-Za-z.-]+))?"
    r"(?:\+(?P<build_metadata>[0-9A-Za-z.-]+))?$"
)
_SEMVER_LOOSE = re.compile(r"^v?(\d+)(?:\.(\d+))?$")
_CONAN = re.compile(r"^(?P<upstream>[^#]+)#(?P<local_revision>[0-9a-fA-F]{12,})$")
_DEVEL = re.compile(r"^\(devel\)$")
_EMPTY = re.compile(
    r"^(latest|stable|main|edge|rolling|head|master|nightly|-|unknown|n/a"
    r"|\((?:unknown|devel|unstable|testing)\))$",
    re.I,
)
#: Placeholders that parse as valid numbers but denote no particular release.
#:
#: `999999` is the sharpest case in this set: it is a well-formed dotted version,
#: so a parser that only checks the shape accepts it, and then a range comparison
#: reports a real-looking verdict about a build nobody ever made. Observed in the
#: lab's CI fixture, where it stands for "rolling/dev placeholder".
_SENTINEL_VERSIONS = frozenset(
    {
        "999999",
        "9999999",
        "999999999",
        "000000",
        "0000",
        "0.0.0",
        "1.0.0.0.0",
    }
)

_PYTHON_MARKERS: Final = (
    "python",
    "pip",
    "pypi",
    "django",
    "flask",
    "requests",
    "urllib3",
    "setuptools",
)
_NODE_MARKERS: Final = ("node", "npm", "yarn", "pnpm", ".js", "lodash", "react", "webpack")
_GO_MARKERS: Final = ("golang", "gopath")
_ALPINE_MARKERS: Final = ("alpine", "apk", "musl")
_RPM_FAMILY_MARKERS: Final = (
    "rhel",
    "redhat",
    "centos",
    "fedora",
    "rocky",
    "almalinux",
    "oracle",
    "amzn",
    "amazon",
    "suse",
    "sles",
    "opensuse",
    "rhel-family",
)
_DEBIAN_FAMILY_MARKERS: Final = ("debian", "apt", "ubuntu", "raspbian", "kali", "mint")


def detect_ecosystem(product: str, version: str) -> Ecosystem:
    """Infer the ecosystem from a product and version string.

    Deliberately conservative, and ordered **shape-first**: the version string is
    the stronger signal, because an inventory records the *package* name
    (``openssl``, ``libcrypto3``) while the distribution shows up in the version
    (``1:1.12.20-8.el9``, ``3.3.2-r0``, ``7.88.1-10+deb12u12``). Product names
    are only used as a tiebreaker for shapes that two ecosystems share.

    An ambiguous input resolves to :attr:`Ecosystem.UNKNOWN` rather than a
    guess, because a wrong ecosystem picks the wrong comparator, which is the
    exact bug class this module exists to remove.
    """
    p = (product or "").lower()
    v = (version or "").strip()

    if not v or _is_immutable_ref(v) or _DEVEL.match(v) or _EMPTY.match(v):
        return Ecosystem.UNKNOWN

    # --- shapes that are unique to one ecosystem ---------------------------
    if _GO_PSEUDOVERSION.match(v):
        return Ecosystem.GOLANG
    if _CONAN.match(v):
        return Ecosystem.CONAN
    if re.search(r"\.(?:whl|tar\.gz|zip)$", v, re.IGNORECASE) or re.match(r"^(?:py|cp)\d", v):
        return Ecosystem.PYPI
    if re.search(r"\.(?:jar|pom)$", v, re.IGNORECASE) or "maven" in p or "java" in p:
        return Ecosystem.MAVEN

    # --- apk ``version-rN``. Shared with Maven's ``1.0-r1``, so tiebreak. --
    # A lowercase ``-r<digits>`` suffix is the apk build-revision convention;
    # Maven marks release candidates as ``-RC1`` and snapshots as ``-SNAPSHOT``,
    # so the case of the ``r`` is what separates them. Real Alpine inventories
    # carry no distro marker in the package name (trivy#7850's case was
    # ``libcrypto3``), so an explicit Java context is required to override.
    if _APK.match(v):
        if _is_java_context(p):
            return Ecosystem.MAVEN
        return Ecosystem.APK

    # --- RPM EVR. An epoch prefix is a strong RPM signal on its own. -------
    rpm_plain = _RPM_EVR_PLAIN.match(v)
    if rpm_plain and rpm_plain.group("epoch") is not None:
        return Ecosystem.RPM

    evr = _RPM_EVR.match(v)
    if evr:
        release = evr.groupdict().get("release") or ""
        if _RPM_VENDOR_RELEASE.search(release):
            return Ecosystem.RPM
        if any(m in p for m in _RPM_FAMILY_MARKERS):
            return Ecosystem.RPM
        if _DEBIAN_REVISION.search(v) or any(m in p for m in _DEBIAN_FAMILY_MARKERS):
            return Ecosystem.DEBIAN
        return Ecosystem.UNKNOWN

    # --- debian revision without a vendor release -------------------------
    if _DEBIAN_REVISION.search(v):
        return Ecosystem.DEBIAN

    # --- product-name hints for shapes that carry no distro signal ---------
    if any(m in p for m in _PYTHON_MARKERS):
        return Ecosystem.PYPI
    if any(m in p for m in _NODE_MARKERS):
        return Ecosystem.NPM
    if any(m in p for m in _GO_MARKERS):
        return Ecosystem.GOLANG
    if _SEMVER.match(v.lstrip("v")):
        return Ecosystem.SEMVER

    return Ecosystem.UNKNOWN


def _is_java_context(product: str) -> bool:
    """Whether the product name indicates a Java artifact.

    Used only to break the ``1.0-r1`` tie between apk and Maven. Kept as a named
    predicate so the decision lives in one place, since getting it wrong swaps a
    whole comparator for every package that matches.
    """
    return "maven" in product or "java" in product or "javax" in product


def _is_immutable_ref(value: str) -> bool:
    return bool(_GIT_SHA.match(value) or _DIGEST.match(value))


# --------------------------------------------------------------------------- #
# Normalisation
# --------------------------------------------------------------------------- #


def normalise(
    raw_version: str | None,
    *,
    ecosystem: Ecosystem | None = None,
    product: str = "",
) -> NormalisedVersion:
    """Parse ``raw_version`` into a comparable, decomposed form.

    ``None`` is a first-class input, not an error: an observation that recorded
    a product but no version is common (a stripped banner, a partial CT-log
    entry) and must yield an unresolved result rather than raise, so the gap
    stays visible in the report instead of crashing the run.

    Returns an :class:`UnresolvableVersion` rather than raising, because an
    unparseable version is an expected, recorded outcome and not an exceptional
    one. Callers check ``is_resolved`` before any comparison.
    """
    if raw_version is None:
        return UnresolvableVersion.for_raw("")

    raw = raw_version.strip()
    if not raw:
        return UnresolvableVersion.for_raw(raw, notes=("empty version string",))

    eco = ecosystem or detect_ecosystem(product, raw)
    notes: list[str] = []

    if _is_immutable_ref(raw):
        notes.append(
            "immutable reference (git sha or digest): carries no version, "
            "range comparison is meaningless"
        )
        return UnresolvableVersion.for_raw(raw, ecosystem=eco, notes=tuple(notes))
    if _DEVEL.match(raw):
        return UnresolvableVersion.for_raw(
            raw, ecosystem=eco, notes=("'(devel)' marker: unpinned build",)
        )
    if _EMPTY.match(raw):
        return UnresolvableVersion.for_raw(
            raw,
            ecosystem=eco,
            notes=(f"'{raw}' is a floating tag, not a version",),
        )
    if raw in _SENTINEL_VERSIONS or raw.lower() in _SENTINEL_VERSIONS:
        return UnresolvableVersion.for_raw(
            raw,
            ecosystem=eco,
            notes=(
                f"'{raw}' is a well-formed but non-specific placeholder version; "
                "it parses as a number and denotes no particular release",
            ),
        )
    # Checked before any ecosystem handler, because the loose Debian pattern and
    # the RPM plain pattern both accept strings carrying these characters.
    #
    # Conan is the exception: `#` is its own recipe-revision separator and the
    # handler parses it correctly, so it must reach its handler. Everything else
    # carrying these characters is a reference that no distro version uses.
    if _NON_VERSION_CHARS.search(raw) and not (
        "#" in raw and eco is Ecosystem.CONAN
    ):
        return UnresolvableVersion.for_raw(
            raw,
            ecosystem=eco,
            notes=(
                f"'{raw}' carries characters or a scheme that no distribution "
                "version uses; it is a reference of some kind, not a release",
            ),
        )

    handlers = {
        Ecosystem.RPM: _normalise_rpm,
        Ecosystem.DEBIAN: _normalise_debian,
        Ecosystem.UBUNTU: _normalise_debian,
        Ecosystem.APK: _normalise_apk,
        Ecosystem.PYPI: _normalise_pep440,
        Ecosystem.GOLANG: _normalise_go,
        Ecosystem.CONAN: _normalise_conan,
        Ecosystem.SEMVER: _normalise_semver,
        Ecosystem.MAVEN: _normalise_maven,
        Ecosystem.NPM: _normalise_semver,
        Ecosystem.NUGET: _normalise_semver,
        Ecosystem.UNKNOWN: _normalise_unknown,
    }
    try:
        return handlers[eco](raw, eco, notes)
    except Exception as exc:
        return UnresolvableVersion.for_raw(
            raw, ecosystem=eco, notes=(*notes, f"parse error: {type(exc).__name__}")
        )


def normalise_many(
    pairs: list[tuple[str, str]],
    *,
    ecosystem: Ecosystem | None = None,
) -> list[NormalisedVersion]:
    """Normalise ``(product, version)`` pairs, inferring per item when needed."""
    return [normalise(version, ecosystem=ecosystem, product=product) for product, version in pairs]


# --------------------------------------------------------------------------- #
# Per-ecosystem handlers
# --------------------------------------------------------------------------- #


def _normalise_rpm(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    """RPM epoch:upstream-release.

    ``1:1.12.20-8.el9`` decomposes to epoch=1, upstream=1.12.20, release=8.el9.
    Keeping release separate is what makes comparison against an rpm-evr range
    correct instead of string-equal.
    """
    m = _RPM_EVR.match(raw) or _RPM_EVR_PLAIN.match(raw)
    if not m:
        return UnresolvableVersion.for_raw(raw, ecosystem=eco)

    epoch = int(m.group("epoch")) if m.group("epoch") else None
    upstream = m.group("upstream")
    release = m.groupdict().get("release")

    if release and release.count(".") == 1 and upstream.count(".") >= 2:
        notes.append("interpreted as epoch:upstream-release")

    return NormalisedVersion(
        ecosystem=eco,
        raw=raw,
        epoch=epoch,
        upstream=upstream,
        release=release,
        confidence=0.95 if release else 0.8,
        notes=tuple(notes),
    )


def _normalise_debian(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    """Debian ``upstream-debian_revision``.

    Trimming a leading epoch (``1:``) is common in dpkg-derived data. Debian's
    own applicability data is a *status*, not a range, so the parsed version is
    only ever used to look up that status.

    A version is required to start with a digit. Without that check this handler
    accepted ``*``, ``git-abc1234`` and ``1.3#0602`` and produced a confident
    parse, because it splits on ``-`` and otherwise passes the body through
    unexamined. That is the exact failure the guard exists to prevent: a wildcard
    or a VCS ref resolving to a comparable value, which then yields a verdict
    about a build that does not exist.
    """
    body = raw[2:] if raw[:2].isdigit() and raw[1:2] == ":" else raw
    epoch = int(raw[:1]) if body is not raw else None
    if epoch is not None:
        notes.append("stripped leading dpkg epoch")

    if not body or not body[0].isdigit():
        notes.append("does not start with a digit, so it is not a Debian version")
        return UnresolvableVersion.for_raw(raw, ecosystem=eco, notes=tuple(notes))

    # `#` marks a Conan recipe revision, not a Debian version. Left unchecked it
    # passed through as a plausible-looking upstream.
    if "#" in body:
        notes.append("contains '#', which is a Conan recipe revision marker")
        return UnresolvableVersion.for_raw(raw, ecosystem=eco, notes=tuple(notes))

    if "-" in body:
        upstream, _, rev = body.rpartition("-")
        if upstream:
            return NormalisedVersion(
                ecosystem=eco,
                raw=raw,
                epoch=epoch,
                upstream=upstream,
                distro_revision=rev,
                confidence=0.9,
                notes=tuple(notes),
            )
    return NormalisedVersion(
        ecosystem=eco, raw=raw, epoch=epoch, upstream=body, confidence=0.7, notes=tuple(notes)
    )


def _normalise_apk(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    """Alpine ``version-rN``.

    The ``-rN`` suffix is the apk build revision. Alpine's secdb keys advisories
    to the *source* package, so this parse exists to resolve source/binary
    indirection rather than to compare against an upstream range.
    """
    m = _APK.match(raw)
    if not m:
        return UnresolvableVersion.for_raw(raw, ecosystem=eco)
    return NormalisedVersion(
        ecosystem=eco,
        raw=raw,
        upstream=m.group("upstream"),
        distro_revision=f"r{m.group('distro_revision')}",
        confidence=0.95,
        notes=(*notes, "apk build revision separated from upstream version"),
    )


def _normalise_pep440(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    """PEP 440 via ``packaging``, the same library PyPA tooling uses.

    Local versions (``+local``) and epochs (``1!2.0``) are decomposed rather
    than string-matched, because PyPI advisories express ranges over them.
    """
    candidate = raw[2:] if raw[:2].isdigit() and raw[1:2] == "!" else raw
    # ``packaging>=22`` dropped ``LegacyVersion``, so ``parse`` returns either a
    # ``Version`` or raises ``InvalidVersion``. There is no third case left to
    # check here.
    try:
        v = pep440_parse(candidate)
    except InvalidVersion:
        return UnresolvableVersion.for_raw(raw, ecosystem=eco)

    if v.local is not None:
        notes.append(f"local version segment '+{v.local}' extracted")
    if v.pre is not None:
        notes.append(f"pre-release '{v.pre}' extracted")
    # PEP 440 treats an absent epoch as 0. Normalising that to None keeps
    # ``None`` meaning "no epoch present" consistently across all ecosystems.
    epoch = v.epoch if v.epoch else None
    if epoch is not None:
        notes.append(f"epoch {epoch} extracted")

    # ``packaging`` keeps the ``N!`` epoch prefix inside ``base_version``, so the
    # epoch has to be stripped here or it would be compared twice.
    upstream = str(v.base_version)
    if epoch is not None:
        upstream = upstream.split("!", 1)[1] if "!" in upstream else upstream

    return NormalisedVersion(
        ecosystem=eco,
        raw=raw,
        epoch=epoch,
        upstream=upstream,
        pre_release=str(v.pre) if v.pre is not None else None,
        build_metadata=str(v.post) if v.post is not None else None,
        local_revision=v.local,
        confidence=0.95,
        notes=tuple(notes),
    )


def _normalise_go(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    """Go module versions, including pseudo-versions.

    ``v0.0.0-20230323144144-5bcd846fa16e`` is a timestamp-and-commit
    pseudo-version: it identifies a commit, not a release, so no release range
    can be compared against it.
    """
    if _GO_PSEUDOVERSION.match(raw):
        return UnresolvableVersion.for_raw(
            raw,
            ecosystem=eco,
            notes=(
                "go pseudo-version identifies a commit, not a release; "
                "no release range is comparable",
            ),
        )
    v = raw[1:] if raw.startswith("v") else raw
    m = _SEMVER.match(v) or _SEMVER_LOOSE.match(v)
    if not m:
        return UnresolvableVersion.for_raw(raw, ecosystem=eco)
    upstream = v if m.re is _SEMVER else _pad_loose(m)
    return NormalisedVersion(
        ecosystem=eco,
        raw=raw,
        upstream=upstream,
        pre_release=m.groupdict().get("pre_release"),
        confidence=0.9,
        notes=tuple(notes),
    )


def _pad_loose(m: re.Match[str]) -> str:
    """``v46`` -> ``46.0.0``. syft#4025's invalid PURL came from this class."""
    major = m.group(1)
    minor = m.group(2) or "0"
    return f"{major}.{minor}.0"


def _normalise_conan(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    """Conan ``version#revision``.

    grype#1737 recorded the revision in the version field, breaking both CPE
    and PURL construction downstream.
    """
    m = _CONAN.match(raw)
    if not m:
        return UnresolvableVersion.for_raw(raw, ecosystem=eco)
    notes.append("conan revision separated from version")
    return NormalisedVersion(
        ecosystem=eco,
        raw=raw,
        upstream=m.group("upstream"),
        local_revision=m.group("local_revision"),
        confidence=0.9,
        notes=tuple(notes),
    )


def _normalise_semver(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    v = raw[1:] if raw.startswith("v") else raw
    m = _SEMVER.match(v)
    if m:
        return NormalisedVersion(
            ecosystem=eco,
            raw=raw,
            upstream=m.group("upstream"),
            pre_release=m.group("pre_release"),
            build_metadata=m.group("build_metadata"),
            confidence=0.95,
            notes=tuple(notes),
        )
    m = _SEMVER_LOOSE.match(v)
    if m:
        notes.append(f"non-strict semver '{raw}' padded to {_pad_loose(m)}")
        return NormalisedVersion(
            ecosystem=eco, raw=raw, upstream=_pad_loose(m), confidence=0.6, notes=tuple(notes)
        )
    return UnresolvableVersion.for_raw(raw, ecosystem=eco)


def _normalise_maven(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    v = raw[1:] if raw.startswith("v") else raw
    m = _SEMVER.match(v) or _SEMVER_LOOSE.match(v)
    if not m:
        return UnresolvableVersion.for_raw(raw, ecosystem=eco)
    upstream = v if m.re is _SEMVER else _pad_loose(m)
    return NormalisedVersion(
        ecosystem=eco, raw=raw, upstream=upstream, confidence=0.9, notes=tuple(notes)
    )


def _normalise_unknown(raw: str, eco: Ecosystem, notes: list[str]) -> NormalisedVersion:
    """Last resort.

    A bare version is still recorded, but at low confidence and explicitly
    flagged, because comparing an unvalidated parse against an NVD range is
    exactly the operation that produced the measured false positives.
    """
    v = raw[1:] if raw.startswith("v") else raw
    if re.fullmatch(r"\d+(\.\d+)*", v):
        notes.append("untyped version: comparator unvalidated, low confidence")
        return NormalisedVersion(
            ecosystem=eco, raw=raw, upstream=v, confidence=0.4, notes=tuple(notes)
        )
    notes.append("unrecognised version format")
    return UnresolvableVersion.for_raw(raw, ecosystem=eco, notes=tuple(notes))
