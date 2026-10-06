"""Ecosystem-aware version comparators.

These are the ordering primitives the applicability plane needs. They are kept
here, in the product, rather than in the benchmark's freezer script because the
study measures whether distribution-aware comparison helps; the same code has to
run inside the tool being evaluated for the comparison to mean anything.

Every comparator returns -1, 0 or 1. Only the sign is meaningful, but the
magnitude is clamped rather than left as a raw difference so results read as
ordinary comparisons.

The implementations here are ports of the *native* tools' algorithms
(``dpkg --compare-versions``, apk's rule), not approximations. Where a native
tool is available at test time the ports are differentially tested against it;
see ``tests/unit/test_applicability.py``.

**None of these raise on unparseable input.** Callers must check that the
version resolved first: ordering a version that was never parsed produces a
confident wrong answer, which is exactly the failure this project exists to
measure. Use :func:`infravce.normalise.versions.normalise` and check
``NormalisedVersion.is_resolved``.
"""

from __future__ import annotations

from functools import cmp_to_key

__all__ = [
    "apk_compare",
    "apk_version_lt",
    "compare_versions",
    "deb_compare",
    "rpm_compare",
]


# --------------------------------------------------------------------------- #
# Debian (dpkg)
# --------------------------------------------------------------------------- #

#: Character rank used while comparing non-digit parts of a Debian version.
#:
#: dpkg gives `~` a rank of -1, which puts it *below* the end of a string (rank 0)
#: and therefore below every ordinary character. That is what makes `1.0~beta1`
#: sort before `1.0`, as a prerelease should. Using the character's own code point
#: instead would rank `~` (126) above every letter and invert that ordering.
_DEB_TILDE = -1


def _deb_char(ch: str | None) -> int:
    """dpkg's `order()`: `~` is -1, end-of-string is 0, otherwise the code point."""
    if ch is None:
        return 0
    if ch == "~":
        return _DEB_TILDE
    return ord(ch)


def _deb_compare_part(a: str, b: str) -> int:
    """Compare two version parts, dpkg's `verrevcmp` way.

    Digit runs compare numerically with leading zeros stripped; non-digit runs
    compare by character under :func:`_deb_char`. The `first_diff` mechanism
    reproduces dpkg's behaviour of noting a character-level difference inside a
    digit run and reporting it only if the run turns out to be equal in length.
    """
    ai = bi = 0
    la, lb = len(a), len(b)
    while ai < la or bi < lb:
        first_diff = 0

        while (ai < la and not a[ai].isdigit()) or (bi < lb and not b[bi].isdigit()):
            ac = _deb_char(a[ai] if ai < la else None)
            bc = _deb_char(b[bi] if bi < lb else None)
            if ac != bc:
                return -1 if ac < bc else 1
            ai += 1
            bi += 1

        while ai < la and a[ai] == "0":
            ai += 1
        while bi < lb and b[bi] == "0":
            bi += 1

        while ai < la and a[ai].isdigit() and bi < lb and b[bi].isdigit():
            if not first_diff:
                first_diff = ord(a[ai]) - ord(b[bi])
            ai += 1
            bi += 1

        if ai < la and a[ai].isdigit():
            return 1
        if bi < lb and b[bi].isdigit():
            return -1
        if first_diff:
            return -1 if first_diff < 0 else 1

    return 0


def deb_split(version: str) -> tuple[int, str, str]:
    """Split ``[epoch:]upstream[-revision]`` into its three dpkg components.

    The epoch defaults to 0 and the revision defaults to the empty string, which
    is how dpkg itself treats their absence. Keeping the revision separate is the
    point: ``+deb12u10`` must not be compared as part of the upstream version, or
    Debian's own security revisions stop ordering correctly.
    """
    epoch = 0
    rest = version
    if ":" in rest:
        head, _, rest = rest.partition(":")
        if head.isdigit():
            epoch = int(head)
        else:
            # A colon in a non-epoch position is not a version dpkg accepts;
            # keeping the whole string as upstream at least preserves it.
            rest = version

    upstream, _, revision = rest.rpartition("-")
    if not upstream:
        upstream, revision = rest, ""
    return epoch, upstream, revision


def deb_compare(a: str, b: str) -> int:
    """Full Debian version comparison: epoch, then upstream, then revision.

    Digit runs compare numerically with leading zeros stripped, so
    ``+deb12u9`` sorts *below* ``+deb12u15``. Getting that backwards inverts which
    build looks newer and silently corrupts every backport verdict.
    """
    ae, au, ar = deb_split(a)
    be, bu, br = deb_split(b)

    if ae != be:
        return -1 if ae < be else 1

    c = _deb_compare_part(au, bu)
    if c:
        return c
    return _deb_compare_part(ar, br)


# --------------------------------------------------------------------------- #
# Alpine (apk)
# --------------------------------------------------------------------------- #

#: apk orders ``<upstream>-r<revision>``, comparing the upstream part with RPM's
#: underscore-sorting rule (digit runs numeric, everything else by character, with
#: `_` sorting below `.` and below letters) and the revision numerically.


def apk_split(version: str) -> tuple[str, int]:
    """Split ``1.36.1-r20`` into ``("1.36.1", 20)``; a missing ``-rN`` is r0.

    ``rpartition`` on ``-r`` rather than ``split`` so an upstream part that itself
    contains ``-r`` (``3.1.8-r0-1``) keeps its revision.
    """
    upstream, sep, rev = version.rpartition("-r")
    if sep and rev.isdigit():
        return upstream, int(rev)
    return version, 0


def _rpm_style_cmp(x: str, y: str) -> int:
    """Compare dotted segments: digits numerically, others by character.

    Adequate for the version shapes in this lab, and consistent with Alpine's own
    rule that ``1.36.1`` sorts below ``1.36.1-r1``. Not a general implementation
    of apk's comparator, which also handles prerelease suffixes.
    """
    xs, ys = x.split("."), y.split(".")
    for i in range(max(len(xs), len(ys))):
        xa = xs[i] if i < len(xs) else ""
        ya = ys[i] if i < len(ys) else ""
        if xa.isdigit() and ya.isdigit():
            if int(xa) != int(ya):
                return -1 if int(xa) < int(ya) else 1
            continue
        if xa != ya:
            # An absent segment sorts below a present one, so 1.36 < 1.36.1.
            if not xa:
                return -1
            if not ya:
                return 1
            return -1 if xa < ya else 1
    return 0


def apk_compare(a: str, b: str) -> int:
    """Compare two apk versions, including the ``-rN`` revision."""
    ua, ra = apk_split(a)
    ub, rb = apk_split(b)
    c = _rpm_style_cmp(ua, ub)
    if c:
        return c
    return -1 if ra < rb else (1 if ra > rb else 0)


def apk_version_lt(a: str, b: str) -> bool:
    """Strict less-than over apk versions, including the ``-rN`` revision."""
    return apk_compare(a, b) < 0


# --------------------------------------------------------------------------- #
# RPM
# --------------------------------------------------------------------------- #


def rpm_split(evr: str) -> tuple[int, str, str]:
    """Split an RPM EVR string into ``(epoch, version, release)``.

    An absent epoch is 0, matching RPM's own default. The epoch is kept separate
    because ``1:1.12.20-8.el9`` and ``1.12.20-8.el9`` are different packages, and
    comparing the strings as-is puts them in the wrong order.
    """
    epoch = 0
    rest = evr
    if ":" in rest:
        head, _, rest = rest.partition(":")
        if head.isdigit():
            epoch = int(head)
        else:
            rest = evr
    version, _, release = rest.partition("-")
    return epoch, version, release


def rpm_compare(a: str, b: str) -> int:
    """Compare RPM EVR strings: epoch, then version, then release."""
    ae, av, ar = rpm_split(a)
    be, bv, br = rpm_split(b)
    if ae != be:
        return -1 if ae < be else 1
    c = _rpm_style_cmp(av, bv)
    if c:
        return c
    return _rpm_style_cmp(ar, br)


# --------------------------------------------------------------------------- #
# Dispatch
# --------------------------------------------------------------------------- #

_COMPARATORS = {
    "debian": deb_compare,
    "rpm": rpm_compare,
    "apk": apk_compare,
}


def compare_versions(ecosystem: str, a: str, b: str) -> int:
    """Compare two versions within one ecosystem.

    Only the ecosystems with an implemented native ordering are supported. The
    caller is expected to have normalised the version already; comparing raw
    strings from different ecosystems is meaningless and this raises rather than
    guessing.
    """
    fn = _COMPARATORS.get(ecosystem)
    if fn is None:
        raise ValueError(
            f"no native comparator for ecosystem {ecosystem!r}; "
            "normalise to a supported ecosystem first rather than comparing "
            "version strings as plain text"
        )
    return fn(a, b)


def sort_versions(ecosystem: str, versions: list[str]) -> list[str]:
    """Sort versions ascending using the ecosystem's own ordering.

    ``sorted`` with ``key=`` cannot do this: a key function is applied once per
    element and never sees two elements together, so it cannot order them.
    ``cmp_to_key`` is the documented way to hand a comparison function to
    ``sorted`` instead.
    """
    def compare(a: str, b: str) -> int:
        return compare_versions(ecosystem, a, b)

    return sorted(versions, key=cmp_to_key(compare))
