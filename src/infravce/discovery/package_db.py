"""Host package-database discovery.

A banner tells you what a service *claims* to be. The package database tells you
what is actually installed, at the exact version, including the distribution
revision that decides whether a backported fix is present. For CVE matching that
difference is the whole ballgame: ``2.4.69`` and ``2.4.69-1~deb12u3`` are the same
upstream release but only one of them may contain the patch.

This module is read-only and local. It parses the two formats that cover almost
every Linux host:

* ``/var/lib/dpkg/status`` (Debian, Ubuntu) — RFC822-style stanzas, only entries
  whose ``Status`` is ``install ok installed``.
* ``/lib/apk/db/installed`` (Alpine) — the same shape with one-letter keys.

Two details are deliberate and easy to get wrong:

1. **The source package is what advisories index.** Debian's tracker and Alpine's
   secdb key on ``openssl``, not on ``libssl3``; querying the binary package
   name returns an empty result that looks like "no vulnerabilities". The
   ``Source``/``o`` field is used when present.
2. **The version is kept verbatim.** ``raw_version`` carries the full
   ``1:10.5p1-1`` or ``3.0.11-1~deb12u2`` string. Downstream comparison needs the
   epoch and revision, and normalisation is the layer that decomposes it.
"""

from __future__ import annotations

import socket
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from infravce.models import AcquisitionMethod, Ecosystem, Observation
from infravce.normalise.versions import normalise

__all__ = [
    "PackageRecord",
    "detect_host_os",
    "inventory_observations",
    "parse_apk_installed",
    "parse_dpkg_status",
    "read_host_inventory",
]

#: Where a Debian-family host keeps its installed-package database.
DPKG_STATUS = Path("/var/lib/dpkg/status")
#: Where an Alpine host keeps its installed-package database.
APK_INSTALLED = Path("/lib/apk/db/installed")


@dataclass(frozen=True, slots=True)
class PackageRecord:
    """One installed package, exactly as the package manager recorded it."""

    name: str
    version: str
    source: str = ""
    architecture: str = ""
    status: str = "installed"
    manager: str = "dpkg"

    @property
    def advisory_name(self) -> str:
        """The name an advisory feed indexes: the source package when known."""
        return (self.source or self.name).strip().lower()


def _stanzas(text: str) -> list[dict[str, str]]:
    """Split RFC822-style package records into field maps.

    Continuation lines (leading whitespace) belong to the previous field, which
    matters for ``Description``; no field we read uses them, but silently
    treating them as new fields would corrupt the next stanza's first key.
    """
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    last_key: str | None = None
    for line in text.splitlines():
        if not line.strip():
            if current:
                records.append(current)
                current = {}
                last_key = None
            continue
        if line[0] in " \t" and last_key is not None:
            current[last_key] = f"{current[last_key]} {line.strip()}".strip()
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        last_key = key.strip().lower()
        current[last_key] = value.strip()
    if current:
        records.append(current)
    return records


def parse_dpkg_status(text: str) -> list[PackageRecord]:
    """Installed packages from a dpkg status file (or its saved copy)."""
    out: list[PackageRecord] = []
    for stanza in _stanzas(text):
        name = stanza.get("package", "").strip()
        version = stanza.get("version", "").strip()
        if not name or not version:
            continue
        status = stanza.get("status", "install ok installed").strip()
        # ``deinstall ok config-files`` and ``install ok unpacked`` are not
        # installed: matching CVEs against them would report a package that is
        # not on disk.
        fields = status.split()
        if len(fields) >= 3 and (fields[1] != "ok" or fields[2] != "installed"):
            continue
        source = stanza.get("source", "").strip()
        if source:
            # ``openssl (3.0.11-1~deb12u2)`` -> ``openssl``
            source = source.split("(", 1)[0].split(" ", 1)[0].strip()
        out.append(
            PackageRecord(
                name=name,
                version=version,
                source=source,
                architecture=stanza.get("architecture", "").strip(),
                status=status,
                manager="dpkg",
            )
        )
    return out


def parse_apk_installed(text: str) -> list[PackageRecord]:
    """Installed packages from an apk ``installed`` database."""
    out: list[PackageRecord] = []
    for stanza in _stanzas(text):
        name = stanza.get("p", "").strip()
        version = stanza.get("v", "").strip()
        if not name or not version:
            continue
        out.append(
            PackageRecord(
                name=name,
                version=version,
                source=stanza.get("o", "").strip(),
                architecture=stanza.get("a", "").strip(),
                manager="apk",
            )
        )
    return out


#: ``/etc/os-release`` ID -> our ecosystem. Alpine reports ``ID=alpine`` and the
#: others are self-describing; an unknown ID stays UNKNOWN rather than guessing.
_OS_ID = {
    "debian": Ecosystem.DEBIAN,
    "ubuntu": Ecosystem.UBUNTU,
    "alpine": Ecosystem.APK,
    "rhel": Ecosystem.RPM,
    "centos": Ecosystem.RPM,
    "rocky": Ecosystem.RPM,
    "almalinux": Ecosystem.RPM,
    "fedora": Ecosystem.RPM,
    # Kali is Debian-derived but rolling, so it has no Debian release number.
    # The ecosystem is right; the release stays unknown rather than being
    # guessed from the Kali year, which would select the wrong fix boundaries.
    "kali": Ecosystem.DEBIAN,
}


def _os_release_label(ecosystem: Ecosystem, version_id: str) -> str | None:
    """Translate ``VERSION_ID`` into the string OSV expects for that ecosystem."""
    version_id = version_id.strip()
    if not version_id:
        return None
    if ecosystem is Ecosystem.APK:
        return version_id if version_id.startswith("v") else f"v{version_id}"
    if ecosystem in {Ecosystem.DEBIAN, Ecosystem.RPM}:
        # ``12`` / ``12.5`` select a release; ``2026.3`` (Kali) and
        # ``kali-rolling`` do not, and pretending they do queries an ecosystem
        # that does not exist. Two digits covers every Debian/RHEL release that
        # exists without accepting a year.
        major = version_id.split(".", 1)[0]
        return version_id if major.isdigit() and len(major) <= 2 else None
    if ecosystem is Ecosystem.UBUNTU:
        # OSV spells Ubuntu releases with the support tier; LTS is the common
        # case and the only one this MVP claims to know.
        return f"{version_id}:LTS" if version_id.endswith(".04") else version_id
    return version_id


def detect_host_os(root: Path | str = "/") -> tuple[Ecosystem, str | None, str]:
    """Read ``/etc/os-release`` and return ``(ecosystem, osv_release, pretty_name)``."""
    path = Path(root) / "etc/os-release"
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return Ecosystem.UNKNOWN, None, "unknown"
    fields: dict[str, str] = {}
    for line in text.splitlines():
        key, sep, value = line.partition("=")
        if sep:
            fields[key.strip()] = value.strip().strip('"').strip("'")
    ecosystem = _OS_ID.get(fields.get("ID", "").lower(), Ecosystem.UNKNOWN)
    release = _os_release_label(ecosystem, fields.get("VERSION_ID", ""))
    return ecosystem, release, fields.get("PRETTY_NAME") or fields.get("NAME") or "unknown"


def inventory_observations(
    packages: Iterable[PackageRecord],
    *,
    asset_id: str,
    ecosystem: Ecosystem,
    evidence_prefix: str = "package database",
) -> list[Observation]:
    """Convert installed packages into exact-version observations."""
    observations: list[Observation] = []
    for package in packages:
        product = package.advisory_name
        if not product:
            continue
        normalised = normalise(package.version, ecosystem=ecosystem, product=product)
        resolved = normalised if normalised.is_resolved else None
        observations.append(
            Observation(
                asset_id=asset_id,
                acquisition_method=AcquisitionMethod.PACKAGE_DB,
                evidence=(
                    f"{evidence_prefix}: {package.manager} {package.name}="
                    f"{package.version} (source {product})"
                ),
                raw_product=product,
                raw_version=package.version,
                resolved_product=product,
                resolved_version=resolved,
                resolution_confidence=resolved.confidence if resolved else 0.0,
                parse_notes=tuple(normalised.notes),
            )
        )
    return observations


def _detect_manager(path: Path) -> str | None:
    name = path.name.lower()
    if name == "status" or name.endswith(".status") or "dpkg" in str(path).lower():
        return "dpkg"
    if name == "installed" or "apk" in str(path).lower():
        return "apk"
    return None


def read_host_inventory(
    paths: Iterable[Path | str] | None = None,
    *,
    root: Path | str = "/",
    asset_id: str | None = None,
) -> tuple[list[Observation], Ecosystem, str | None, str, list[str]]:
    """Read the local package database(s).

    Returns ``(observations, ecosystem, os_release, asset_id, gaps)``. A missing
    database is reported as a gap, never as an empty host: "checked, nothing
    installed" and "could not check" must not look the same.
    """
    root_path = Path(root)
    ecosystem, os_release, pretty = detect_host_os(root_path)
    host = asset_id or socket.gethostname() or "localhost"
    gaps: list[str] = []

    candidates: list[Path] = []
    if paths:
        candidates = [Path(p) for p in paths]
    else:
        dpkg = root_path / DPKG_STATUS.relative_to("/")
        apk = root_path / APK_INSTALLED.relative_to("/")
        for candidate in (dpkg, apk):
            if candidate.exists():
                candidates.append(candidate)

    if not candidates:
        gaps.append(
            "no package database found (looked for /var/lib/dpkg/status and "
            "/lib/apk/db/installed); pass --inventory with a saved copy"
        )

    observations: list[Observation] = []
    for path in candidates:
        try:
            text = path.read_text(errors="replace")
        except OSError as exc:
            gaps.append(f"{path}: unreadable ({type(exc).__name__})")
            continue
        manager = _detect_manager(path)
        if manager == "apk":
            packages = parse_apk_installed(text)
            package_ecosystem = Ecosystem.APK if ecosystem is Ecosystem.UNKNOWN else ecosystem
        elif manager == "dpkg":
            packages = parse_dpkg_status(text)
            package_ecosystem = Ecosystem.DEBIAN if ecosystem is Ecosystem.UNKNOWN else ecosystem
        else:
            gaps.append(f"{path}: unrecognised package database format")
            continue
        if not packages:
            gaps.append(f"{path}: parsed zero packages")
            continue
        observations.extend(
            inventory_observations(
                packages,
                asset_id=host,
                ecosystem=package_ecosystem,
                evidence_prefix=f"{path} on {pretty}",
            )
        )
    return observations, ecosystem, os_release, host, gaps
