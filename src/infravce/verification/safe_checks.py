"""Safe, read-only verification of an observation's version.

The question this module answers is *not* "is the package vulnerable" — that is
the applicability engine's job — but "is the version I am about to reason about
actually the version that is installed". Those are different claims, and the
benchmark's whole premise is that tools conflate them.

Since active checks are restricted to read-only, single requests (docs/06), the
strongest honest evidence available is **independent agreement**:

* a declared inventory (SBOM, lockfile, manifest, package database) that records
  an exact version at high resolution confidence, or
* two observations of the same asset and product, obtained by different methods,
  reporting the same version.

A single banner is explicitly *not* verification. Banners are operator-controlled
strings; the literature in ``docs/04`` measured >95% false positives on banner-
derived CVE claims. Treating one banner as verified would reintroduce exactly the
failure this project exists to remove.
"""

from __future__ import annotations

from collections import defaultdict

from infravce.models import AcquisitionMethod, Observation

__all__ = ["verify_observations", "safe_verify"]

#: Methods that record a version an operator declared, rather than a string a
#: service volunteered. These can stand alone at high resolution confidence.
_DECLARED = frozenset(
    {
        AcquisitionMethod.SBOM,
        AcquisitionMethod.LOCKFILE,
        AcquisitionMethod.MANIFEST,
        AcquisitionMethod.PACKAGE_DB,
        AcquisitionMethod.AGENT_REPORT,
        AcquisitionMethod.DECLARED_CMDB,
        AcquisitionMethod.DECLARED_IAC,
    }
)

#: A declared version below this resolution confidence is not treated as
#: verified: the normaliser itself was unsure, so agreement adds nothing.
_MIN_DECLARED_CONFIDENCE = 0.85


def verify_observations(observations: list[Observation]) -> dict[str, bool]:
    """Map ``observation_id`` to whether its version is independently confirmed."""
    by_key: dict[tuple[str, str, str], list[Observation]] = defaultdict(list)
    for observation in observations:
        if not observation.is_usable_for_matching:
            continue
        version = observation.resolved_version
        key = (
            observation.asset_id,
            (observation.resolved_product or observation.raw_product).lower(),
            (version.upstream if version and version.upstream else observation.raw_version),
        )
        by_key[key].append(observation)

    verified: dict[str, bool] = {}
    for observation in observations:
        if not observation.is_usable_for_matching:
            verified[observation.observation_id] = False
            continue
        version = observation.resolved_version
        key = (
            observation.asset_id,
            (observation.resolved_product or observation.raw_product).lower(),
            (version.upstream if version and version.upstream else observation.raw_version),
        )
        peers = by_key[key]
        methods = {peer.acquisition_method for peer in peers}

        declared = any(
            peer.acquisition_method in _DECLARED
            and peer.resolution_confidence >= _MIN_DECLARED_CONFIDENCE
            for peer in peers
        )
        independent_agreement = len(methods) >= 2
        verified[observation.observation_id] = declared or independent_agreement
    return verified


#: Backwards-compatible name used by the CLI and the original pipeline.
def safe_verify(observations: list[Observation]) -> dict[str, bool]:
    return verify_observations(observations)
