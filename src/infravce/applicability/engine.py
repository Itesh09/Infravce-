"""Source precedence and the distribution-state mapping.

Two decisions live here, and they are the ones the benchmark's central claim
rests on:

1. **Which advisory source is allowed to decide.** Per principle P3
   (``docs/02-architecture.md``), distribution and vendor truth outrank upstream
   NVD for OS packages. This is not a tie-break heuristic: upstream version
   ranges are *categorically wrong* for backported distributions, so preferring
   them does not merely reduce precision, it produces confidently incorrect
   verdicts.

2. **How a distribution's vocabulary maps to a verdict.** Debian's tracker has
   five release states and they do **not** map onto "affected or not affected".
   ``<undetermined>``, ``<no-dsa>`` and ``<postponed>`` mean nobody has finished
   assessing this; mapping them to ``not_affected`` would present an unassessed
   package as safe.

Both are implemented as pure functions over the frozen ground truth's own
vocabulary so the benchmark and the tool share one definition. If they disagree,
the benchmark is measuring the wrong thing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from infravce.applicability.comparators import compare_versions
from infravce.models import (
    AdvisorySource,
    ApplicabilityVerdict,
    Ecosystem,
    Justification,
    RangeRepresentation,
)
from infravce.normalise.versions import normalise

__all__ = [
    "DistributionState",
    "VerdictOutcome",
    "decide",
    "decide_range",
    "parse_state",
    "select_sources",
    "verdict_for_state",
]


class DistributionState(StrEnum):
    """The release states a distribution tracker uses.

    Debian's vocabulary is the reference case because it is the most explicit
    about the difference between "assessed and fine" and "nobody has looked".
    """

    #: Fixed. A version boundary exists, or none was needed.
    RESOLVED = "resolved"
    #: Assessed: this release never contained the vulnerable code.
    NOT_AFFECTED = "not-affected"
    #: Open: the vulnerable code is present and unpatched.
    OPEN = "open"
    #: No DSA issued. Means unpatched, not means safe.
    NO_DSA = "no-dsa"
    #: Someone needs to come back to this. Never safe.
    UNDETERMINED = "undetermined"
    #: Deferred, deliberately not being fixed yet. Never safe.
    POSTPONED = "postponed"
    #: Vulnerable regardless of version.
    VULNERABLE = "vulnerable"
    #: Ends of life. Applies no fix.
    END_OF_LIFE = "end-of-life"
    #: Unrecognised. Treated as unresolved rather than silently as safe.
    UNKNOWN = "unknown"


#: States that assert "nobody has finished assessing this". Every one of them maps
#: to under_investigation, never to not_affected. This is the single most
#: consequential mapping in the system: getting it wrong turns "unknown" into
#: "safe", which is the failure mode that makes people stop patching.
_UNASSESSED = frozenset(
    {
        DistributionState.UNDETERMINED,
        DistributionState.NO_DSA,
        DistributionState.POSTPONED,
        DistributionState.UNKNOWN,
    }
)


def verdict_for_state(
    state: DistributionState,
    installed: str | None,
    fixed_version: str | None,
    ecosystem: str = "debian",
) -> VerdictOutcome:
    """Map one distribution state plus a version comparison to a verdict.

    ``installed`` and ``fixed_version`` are raw strings in the ecosystem's own
    format. Both must be ``None``-free for a version comparison to happen; when
    the tracker gives a status that does not depend on version (``open``,
    ``not-affected``), they are not consulted.

    Returns a :class:`VerdictOutcome` rather than a bare verdict so the reason and
    the comparison are carried with it. The reason is what makes a finding
    auditable, and it is what the evidence bundles are built from.
    """
    if state in _UNASSESSED:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
            reason=(
                f"distribution reports {state.value!r}, which means the assessment "
                "is incomplete rather than that the package is safe"
            ),
            comparison=None,
        )

    if state is DistributionState.NOT_AFFECTED:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.NOT_AFFECTED,
            reason=(
                f"distribution reports {state.value!r}: the vulnerable code was "
                "never present in this release"
            ),
            justification=Justification.VULNERABLE_CODE_NOT_PRESENT,
            comparison=None,
        )

    if state is DistributionState.OPEN:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.AFFECTED,
            reason="distribution reports the issue open with no fix available",
            comparison=None,
        )

    if state is DistributionState.VULNERABLE:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.AFFECTED,
            reason="distribution reports every version affected",
            comparison=None,
        )

    if state is DistributionState.END_OF_LIFE:
        # A release with no security support still has a code state. Where the
        # vulnerable code is present it is affected; the absence of future fixes
        # is a prioritisation input, not an applicability one.
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.AFFECTED,
            reason=(
                "release is end-of-life, so no fix will arrive; applicability "
                "still follows the installed code"
            ),
            comparison=None,
        )

    # RESOLVED is the only state that needs a version comparison.
    if installed is None or fixed_version is None:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
            reason=(
                f"status is {state.value!r} but "
                f"{'installed version' if installed is None else 'fix version'} "
                "is unknown, so there is nothing to compare"
            ),
            comparison=None,
        )

    # A zero fix version is Debian's way of saying "no fix was needed because the
    # code was never there". Comparing against 0 would compare the installed
    # version against the number zero, which is meaningless.
    if fixed_version.strip() in {"0", "0.0"}:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
            reason=(
                f"status is {state.value!r} with fixed_version={fixed_version!r}; "
                "this means no fix was needed rather than that any version is "
                "safe, so the record does not settle the question"
            ),
            comparison=None,
        )

    try:
        result = compare_versions(ecosystem, installed, fixed_version)
    except ValueError as exc:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
            reason=f"cannot compare {installed!r} with {fixed_version!r}: {exc}",
            comparison=None,
        )

    comparison = f"compare_versions({ecosystem!r}, {installed!r}, {fixed_version!r}) == {result}"
    if result >= 0:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.NOT_AFFECTED,
            reason=(
                f"installed {installed} is at or past the fix boundary "
                f"{fixed_version}"
            ),
            justification=Justification.INLINE_MITIGATIONS_ALREADY_EXIST,
            comparison=comparison,
        )
    return VerdictOutcome(
        verdict=ApplicabilityVerdict.AFFECTED,
        reason=f"installed {installed} predates the fix boundary {fixed_version}",
        comparison=comparison,
    )


@dataclass(frozen=True, slots=True)
class VerdictOutcome:
    """A verdict together with the comparison that produced it."""

    verdict: ApplicabilityVerdict
    reason: str
    justification: Justification | None = None
    comparison: str | None = None


@dataclass(frozen=True, slots=True)
class SourceDecision:
    """Which source won, and what it outranked."""

    winner: AdvisorySource | None
    winner_range: RangeRepresentation
    considered: tuple[tuple[AdvisorySource, RangeRepresentation], ...] = ()
    fallback_reason: str | None = None
    outranked: tuple[AdvisorySource, ...] = field(default=())


def select_sources(
    available: dict[AdvisorySource, RangeRepresentation],
    *,
    is_os_package: bool,
) -> SourceDecision:
    """Pick the source allowed to decide, per P3.

    For an OS package the distribution tracker wins if present, and NVD is not
    merely lower-ranked but **disqualified**: an upstream range applied to a
    backported distribution is known-wrong rather than less precise. Falling back
    to it is recorded as a fallback, because that is the condition a reviewer
    needs to see.

    For a language ecosystem package there is no distribution layer, so
    OSV/GHSA is the correct default and NVD is merely the last resort.

    With no sources at all the decision is ``winner=None``. Callers must treat
    that as unresolved rather than as an absence of findings, since the two mean
    different things: "checked, nothing wrong" versus "could not check".
    """
    if not available:
        return SourceDecision(
            winner=None,
            winner_range=RangeRepresentation.UNKNOWN,
            fallback_reason="no advisory source supplied any record for this package",
        )

    ranked = sorted(available.items(), key=lambda kv: kv[0].precedence_rank)
    considered = tuple(ranked)

    if is_os_package:
        for source, representation in ranked:
            if source is AdvisorySource.DISTRO_TRACKER:
                return SourceDecision(
                    winner=source,
                    winner_range=representation,
                    considered=considered,
                    outranked=tuple(s for s, _ in ranked if s is not source),
                )

        # No distribution tracker for this OS package. NVD is still better than
        # nothing, but the answer is known to be weaker and the caller is told so.
        winner, representation = ranked[0]
        return SourceDecision(
            winner=winner,
            winner_range=representation,
            considered=considered,
            fallback_reason=(
                f"no distribution record for an OS package; fell back to "
                f"{winner.value!r}, whose version ranges are unreliable for "
                "backported distributions"
            ),
            outranked=tuple(s for s, _ in ranked if s is not winner),
        )

    winner, representation = ranked[0]
    return SourceDecision(
        winner=winner,
        winner_range=representation,
        considered=considered,
        outranked=tuple(s for s, _ in ranked if s is not winner),
    )


def decide(
    installed_version: str | None,
    ecosystem: str,
    candidates: dict[AdvisorySource, tuple[DistributionState, str | None]],
    *,
    is_os_package: bool,
    product: str = "",
) -> tuple[ApplicabilityVerdict, SourceDecision, VerdictOutcome]:
    """Full decision: pick the source, then map its state to a verdict.

    ``candidates`` maps each source to its ``(state, fixed_version)`` pair. The
    selected source's state is what decides; the others are recorded as
    outranked and are *not* consulted, because consulting them is precisely the
    behaviour P3 forbids.

    The installed version is validated before any comparison is attempted. An
    unresolvable version stops the decision here and yields
    ``under_investigation``: this is the guard from ``docs/02-architecture.md``
    §4.2, and putting it in this function rather than leaving it to callers means
    a caller that forgets it cannot invent a finding from ``(devel)`` or
    ``999999``.
    """
    available = {src: _representation(src) for src in candidates}
    decision = select_sources(available, is_os_package=is_os_package)

    normalised = normalise(installed_version, ecosystem=_ECO_SYSTEM.get(ecosystem), product=product)
    if not normalised.is_resolved:
        reason = (
            f"installed version {installed_version!r} does not resolve to a "
            "comparable value"
        )
        if normalised.notes:
            reason = f"{reason}: {normalised.notes[0]}"
        return (
            ApplicabilityVerdict.UNDER_INVESTIGATION,
            decision,
            VerdictOutcome(verdict=ApplicabilityVerdict.UNDER_INVESTIGATION, reason=reason),
        )

    if decision.winner is None:
        return (
            ApplicabilityVerdict.UNDER_INVESTIGATION,
            decision,
            VerdictOutcome(
                verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
                reason=decision.fallback_reason or "no advisory record available",
            ),
        )

    state, fixed_version = candidates[decision.winner]
    # The distribution's own comparator needs the raw string: it splits epoch and
    # revision itself, and handing it only the normalised upstream would silently
    # discard the Debian revision that decides which build is newer.
    outcome = verdict_for_state(state, installed_version, fixed_version, ecosystem)
    return outcome.verdict, decision, outcome


#: Maps the engine's ecosystem string onto the model's enum, for validation only.
_ECO_SYSTEM = {
    "debian": Ecosystem.DEBIAN,
    "ubuntu": Ecosystem.UBUNTU,
    "apk": Ecosystem.APK,
    "rpm": Ecosystem.RPM,
    "semver": Ecosystem.SEMVER,
    "npm": Ecosystem.NPM,
    "pypi": Ecosystem.PYPI,
    "golang": Ecosystem.GOLANG,
    "go": Ecosystem.GOLANG,
    "maven": Ecosystem.MAVEN,
    "nuget": Ecosystem.NUGET,
}


#: Strings a tracker or an advisory feed uses for the same distribution state.
#: Kept as data so a new spelling does not silently fall through to UNKNOWN and
#: turn an assessed state into "nobody looked".
_STATE_ALIASES: dict[str, DistributionState] = {
    "resolved": DistributionState.RESOLVED,
    "fixed": DistributionState.RESOLVED,
    "not-affected": DistributionState.NOT_AFFECTED,
    "not_affected": DistributionState.NOT_AFFECTED,
    "notaffected": DistributionState.NOT_AFFECTED,
    "open": DistributionState.OPEN,
    "affected": DistributionState.OPEN,
    "vulnerable": DistributionState.VULNERABLE,
    "no-dsa": DistributionState.NO_DSA,
    "nodsa": DistributionState.NO_DSA,
    "undetermined": DistributionState.UNDETERMINED,
    "under_investigation": DistributionState.UNDETERMINED,
    "under-investigation": DistributionState.UNDETERMINED,
    "postponed": DistributionState.POSTPONED,
    "end-of-life": DistributionState.END_OF_LIFE,
    "eol": DistributionState.END_OF_LIFE,
    "unknown": DistributionState.UNKNOWN,
}


def parse_state(value: str | None) -> DistributionState:
    """Parse a tracker state, never guessing at an unrecognised one.

    An unknown spelling maps to :attr:`DistributionState.UNKNOWN`, which is in
    ``_UNASSESSED`` and therefore yields ``under_investigation``. Erring toward
    "unassessed" is the only safe direction: the alternative is a typo in a feed
    turning into a clean bill of health.
    """
    if not value:
        return DistributionState.UNKNOWN
    return _STATE_ALIASES.get(value.strip().lower(), DistributionState.UNKNOWN)


def decide_range(
    installed: str,
    ecosystem: str,
    segments: tuple[tuple[str | None, str | None], ...],
    *,
    source: AdvisorySource = AdvisorySource.OSV,
) -> VerdictOutcome:
    """Evaluate OSV-style ``(introduced, fixed)`` ranges against an installed version.

    This is the range counterpart to :func:`verdict_for_state`: distro trackers
    answer with a status, upstream feeds answer with half-open intervals
    ``[introduced, fixed)``. Both funnel into the same
    :class:`VerdictOutcome` so a finding's evidence reads the same way
    regardless of which source won.

    Semantics, per OSV's schema:

    * ``introduced: "0"`` means "from the beginning of time", not version zero.
    * A segment with no ``fixed`` is still open: affected, with no fix published.
    * An installed version at or past every fixed boundary is *not affected by
      those ranges*. That is a complete answer only because the ranges came from
      a source that claims to enumerate all affected versions for this package.
    """
    if not segments:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
            reason="advisory carries no comparable range",
        )

    saw_closed = False
    last_fixed: str | None = None
    for introduced, fixed in segments:
        try:
            if introduced and introduced.strip() not in {"0", "0.0"}:
                if compare_versions(ecosystem, installed, introduced) < 0:
                    continue  # installed predates this segment
            if fixed is None:
                return VerdictOutcome(
                    verdict=ApplicabilityVerdict.AFFECTED,
                    reason=(
                        f"installed {installed} is at or past introduced "
                        f"{introduced or '0'} and the source publishes no fix"
                    ),
                    comparison=(
                        f"introduced={introduced or '0'} <= {installed} < fixed=none"
                    ),
                )
            saw_closed = True
            last_fixed = fixed
            if compare_versions(ecosystem, installed, fixed) < 0:
                return VerdictOutcome(
                    verdict=ApplicabilityVerdict.AFFECTED,
                    reason=(
                        f"installed {installed} falls inside the affected range "
                        f"[{introduced or '0'}, {fixed})"
                    ),
                    comparison=(
                        f"compare_versions({ecosystem!r}, {installed!r}, {fixed!r}) < 0"
                    ),
                )
        except ValueError as exc:
            return VerdictOutcome(
                verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
                reason=f"cannot evaluate range against {installed!r}: {exc}",
            )

    if saw_closed:
        return VerdictOutcome(
            verdict=ApplicabilityVerdict.NOT_AFFECTED,
            reason=(
                f"installed {installed} is at or past every published fix "
                f"boundary (latest {last_fixed})"
            ),
            justification=Justification.INLINE_MITIGATIONS_ALREADY_EXIST,
            comparison=f"installed >= fixed {last_fixed}",
        )
    return VerdictOutcome(
        verdict=ApplicabilityVerdict.UNDER_INVESTIGATION,
        reason=f"installed {installed} predates every introduced boundary in the record",
    )


def _representation(source: AdvisorySource) -> RangeRepresentation:
    """The range representation a source natively uses.

    A tracker answers with a status, NVD with a range. The distinction is kept
    because it is what makes the precedence rule checkable rather than implicit.
    """
    return {
        AdvisorySource.DISTRO_TRACKER: RangeRepresentation.DPKG_STATUS,
        AdvisorySource.OSV: RangeRepresentation.OSV_EVENTS,
        AdvisorySource.GHSA: RangeRepresentation.GITHUB_LKAVR,
        AdvisorySource.NVD: RangeRepresentation.NVD_RANGE,
        AdvisorySource.VENDOR_ADVISORY: RangeRepresentation.VENDOR_RANGE,
        AdvisorySource.UNKNOWN: RangeRepresentation.UNKNOWN,
    }[source]
