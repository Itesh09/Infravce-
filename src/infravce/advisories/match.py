"""Match observations to advisories through the applicability engine.

The contract is narrow on purpose: this module decides *which* advisory record
applies to *which* observation, and hands every verdict question to
:mod:`infravce.applicability.engine`. It contains no comparison logic of its
own, because a second implementation of "is this version affected" is how the
two halves of a benchmark stop agreeing.

Three record shapes are supported, in the order the engine prefers them:

1. **A distribution state** (``distro_state`` + ``fixed_version``) — Debian,
   Alpine and vendor trackers. Goes through :func:`decide`, which applies source
   precedence and the tracker-state mapping.
2. **OSV ranges** (``affected_ranges`` of ``(introduced, fixed)``) — upstream
   feeds. Goes through :func:`decide_range` using the advisory's own ecosystem
   comparator, not the observer's, because the range is expressed in the
   publisher's version scheme.
3. **An enumerated version list** — legacy and hand-authored fixtures. Exact
   membership only; absence is reported as not affected with the justification
   recorded, never silently.
"""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import UTC, datetime

from infravce.applicability.engine import VerdictOutcome, decide, decide_range, parse_state
from infravce.models import (
    Applicability,
    ApplicabilityVerdict,
    Ecosystem,
    Justification,
    Observation,
    RangeRepresentation,
)

from .ingest import AdvisoryRecord

__all__ = ["ApplicabilityVote", "match_observations"]

#: Retained as an alias for the public API. The previous implementation was a
#: frozen dataclass inheriting from a pydantic model, which is invalid and was
#: one of the reasons this path was never exercised.
ApplicabilityVote = Applicability

_NON_NAME = re.compile(r"[^a-z0-9.+_-]+")
_OS_PACKAGE_ECOSYSTEMS = {Ecosystem.DEBIAN, Ecosystem.UBUNTU, Ecosystem.RPM, Ecosystem.APK}
_RANGE_REPRESENTATION = {
    Ecosystem.DEBIAN: RangeRepresentation.DPKG_STATUS,
    Ecosystem.UBUNTU: RangeRepresentation.DPKG_STATUS,
    Ecosystem.APK: RangeRepresentation.APK_STATUS,
    Ecosystem.RPM: RangeRepresentation.RPM_EVR,
}


def _norm_product(value: str) -> str:
    """Collapse the spellings the same package appears under.

    ``Apache httpd``, ``apache_httpd`` and ``apache2`` are one package in the
    Debian namespace. This is deliberately conservative: it normalises
    punctuation and case, and refuses to fuzzy-match, because attaching an
    advisory to the wrong product is worse than reporting no match.
    """
    lowered = (value or "").strip().lower()
    return _NON_NAME.sub("-", lowered).strip("-")


def _ecosystem_string(record: AdvisoryRecord, observation: Observation) -> str:
    if record.ecosystem is not Ecosystem.UNKNOWN:
        return record.ecosystem.value
    version = observation.resolved_version
    return version.ecosystem.value if version else Ecosystem.UNKNOWN.value


def _fix_available(record: AdvisoryRecord) -> bool | None:
    """Whether the record publishes a version that resolves the issue."""
    if record.fixed_version:
        return True
    if record.affected_ranges:
        return any(fixed for _, fixed in record.affected_ranges)
    return None


def _vote(
    observation: Observation,
    record: AdvisoryRecord,
    *,
    verdict: ApplicabilityVerdict,
    evidence: str,
    justification: Justification | None = None,
    evidence_quality: str = "exact",
) -> Applicability:
    return Applicability(
        observation_id=observation.observation_id,
        advisory_source=record.source,
        advisory_id=record.advisory_id,
        range_representation=_RANGE_REPRESENTATION.get(
            record.ecosystem, RangeRepresentation.OSV_EVENTS
        ),
        verdict=verdict,
        justification=justification,
        evidence=evidence,
        advisory_published_at=record.published_at,
        evaluated_at=datetime.now(UTC),
        severity=record.severity,
        cvss=record.cvss,
        summary=record.summary,
        aliases=record.aliases,
        evidence_quality=evidence_quality,
        fix_available=_fix_available(record),
    )


_EPOCH = re.compile(r"^\d+:")


def _upstream_only(value: str) -> str:
    """Drop an epoch and a distribution revision.

    Used only when the observation has no revision of its own: a banner says
    ``2.4.69`` while the tracker's boundary is ``2.4.69-1~deb12u1``, and
    comparing them literally makes every Debian package look one revision
    behind its own fix.
    """
    text = value.strip()
    text = _EPOCH.sub("", text)
    if "-" in text:
        text = text.rsplit("-", 1)[0]
    return text


def _has_revision(value: str) -> bool:
    """Whether a distribution version carries a revision after its epoch.

    ``2.4.69-1~deb12u1`` does; ``1:3.0.1`` does not. The distinction matters when
    reducing to upstream only: without a revision the boundary *is* the upstream
    release, so equality means the fix is present. With one, the revision is the
    patch and the observed upstream version may still be the unpatched build.
    """
    return "-" in _EPOCH.sub("", value.strip())


def _matches_fixed_upstream(
    installed_upstream: str,
    segments: tuple[tuple[str | None, str | None], ...],
    ecosystem: str,
) -> bool:
    """Whether an upstream-only version equals a *revisioned* fix boundary.

    ``2.4.69`` is *less than* ``2.4.69-1~deb12u1`` in dpkg ordering, so a banner
    reporting the upstream version of a patched package is exactly the unpatched
    build that the revision fixes. Comparing upstream-only would call the two
    equal and clear it, which is a false negative; treating it as affected is
    the conservative direction and the finding is capped at ``WEAK`` because the
    distribution revision was never observed.

    A boundary with no revision (``fixed: 3.0.1``) is excluded: there the fix is
    the upstream release itself, and equality genuinely means patched.
    """
    from infravce.applicability.comparators import compare_versions

    for _introduced, fixed in segments:
        if not fixed or not _has_revision(fixed):
            continue
        boundary = _upstream_only(fixed)
        try:
            if compare_versions(ecosystem, installed_upstream, boundary) == 0:
                return True
        except ValueError:
            continue
    return False


def _needs_upstream_comparison(record: AdvisoryRecord, installed: str) -> bool:
    """Whether the installed string must be reduced to its upstream version.

    Any distro comparison needs this when the observation has no revision of its
    own. A banner reports ``2.4.69`` or ``10.5p1`` while the tracker's boundary is
    ``2.4.69-1~deb12u1`` or ``1:3.0.1``: comparing them literally either makes
    every package look one revision behind its own fix, or -- for the epoch --
    makes an ancient fix boundary look *newer* than a current upstream version,
    which reports twenty-year-old CVEs against a patched service.

    The trigger is therefore the observation's shape, not the boundary's: an
    installed version with no ``-`` revision is upstream-only evidence for a
    distribution record, whatever the tracker happens to publish.
    """
    return record.ecosystem in _OS_PACKAGE_ECOSYSTEMS and "-" not in installed


def _evaluate(observation: Observation, record: AdvisoryRecord) -> Applicability | None:
    """One record against one observation, or ``None`` when it says nothing."""
    installed = observation.raw_version or (
        observation.resolved_version.raw if observation.resolved_version else ""
    )
    if not installed:
        return None
    ecosystem = _ecosystem_string(record, observation)
    is_os_package = record.ecosystem in _OS_PACKAGE_ECOSYSTEMS
    approximate = _needs_upstream_comparison(record, installed)
    compared = _upstream_only(installed) if approximate else installed
    quality = "approximate" if approximate else "exact"
    caveat = (
        " (upstream-only comparison: the observation carries no distribution "
        "revision, so the tracker's revision boundary was not applied)"
        if approximate
        else ""
    )

    try:
        if record.distro_state:
            state = parse_state(record.distro_state)
            if approximate and state.value == "resolved" and record.fixed_version:
                distro_segments: tuple[tuple[str | None, str | None], ...] = (
                    (None, _upstream_only(record.fixed_version)),
                )
                outcome = decide_range(
                    compared,
                    ecosystem,
                    distro_segments,
                    source=record.source,
                )
                if (
                    outcome.verdict is ApplicabilityVerdict.NOT_AFFECTED
                    and _matches_fixed_upstream(
                        compared, ((None, record.fixed_version),), ecosystem
                    )
                ):
                    outcome = VerdictOutcome(
                        verdict=ApplicabilityVerdict.AFFECTED,
                        reason=(
                            f"installed upstream {compared} is the release the fix "
                            f"{record.fixed_version} patches; the distribution "
                            "revision was not observed, so the patch state is unknown "
                            "and the vulnerable build is assumed"
                        ),
                    )
                return _vote(
                    observation,
                    record,
                    verdict=outcome.verdict,
                    evidence=outcome.reason + caveat,
                    justification=outcome.justification,
                    evidence_quality=quality,
                )
            verdict, decision, outcome = decide(
                compared,
                ecosystem,
                {record.source: (state, record.fixed_version)},
                is_os_package=is_os_package,
                product=record.product,
            )
            evidence = outcome.reason
            if decision.fallback_reason:
                evidence = f"{evidence} ({decision.fallback_reason})"
            return _vote(
                observation,
                record,
                verdict=verdict,
                evidence=evidence + caveat,
                justification=outcome.justification,
                evidence_quality=quality,
            )

        if record.affected_ranges:
            segments: tuple[tuple[str | None, str | None], ...] = record.affected_ranges
            if approximate:
                segments = tuple(
                    (
                        _upstream_only(introduced) if introduced else None,
                        _upstream_only(fixed) if fixed else None,
                    )
                    for introduced, fixed in record.affected_ranges
                )
            outcome = decide_range(compared, ecosystem, segments, source=record.source)
            if (
                approximate
                and outcome.verdict is ApplicabilityVerdict.NOT_AFFECTED
                and _matches_fixed_upstream(compared, record.affected_ranges, ecosystem)
            ):
                # The observation is upstream-only and sits exactly on a
                # revisioned fix boundary. Whether the installed build carries
                # that revision is unknown, so the vulnerable build is assumed.
                outcome = VerdictOutcome(
                    verdict=ApplicabilityVerdict.AFFECTED,
                    reason=(
                        f"installed upstream {compared} equals the release the fix "
                        "patches; the distribution revision was not observed, so "
                        "the patch state is unknown and the vulnerable build is assumed"
                    ),
                )
            return _vote(
                observation,
                record,
                verdict=outcome.verdict,
                evidence=outcome.reason + caveat,
                justification=outcome.justification,
                evidence_quality=quality,
            )

        if record.versions:
            installed_norm = installed.strip()
            if installed_norm in {v.strip() for v in record.versions}:
                return _vote(
                    observation,
                    record,
                    verdict=ApplicabilityVerdict.AFFECTED,
                    evidence=(
                        f"installed version {installed!r} is one of the versions the "
                        f"advisory {record.advisory_id} enumerates as affected"
                    ),
                    evidence_quality=quality,
                )
            return _vote(
                observation,
                record,
                verdict=ApplicabilityVerdict.NOT_AFFECTED,
                evidence=(
                    f"installed version {installed!r} is not among the versions the "
                    f"advisory {record.advisory_id} enumerates"
                ),
                justification=Justification.VULNERABLE_CODE_NOT_PRESENT,
                evidence_quality=quality,
            )
    except Exception as exc:  # a broken record must not take the scan down
        return _vote(
            observation,
            record,
            verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
            evidence=f"could not evaluate {record.advisory_id}: {type(exc).__name__}: {exc}",
        )
    return None


def match_observations(
    observations: list[Observation],
    advisories: list[AdvisoryRecord],
) -> list[Applicability]:
    """Every advisory vote for every usable observation."""
    index: dict[str, list[AdvisoryRecord]] = defaultdict(list)
    for record in advisories:
        index[_norm_product(record.product)].append(record)

    votes: list[Applicability] = []
    for observation in observations:
        if not observation.is_usable_for_matching:
            continue
        products = {
            _norm_product(p)
            for p in (
                observation.resolved_product or "",
                observation.raw_product or "",
            )
            if p
        }
        for product in products:
            for record in index.get(product, ()):
                vote = _evaluate(observation, record)
                if vote is not None:
                    votes.append(vote)
    return votes
