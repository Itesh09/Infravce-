"""Authorised-only, non-destructive active probes.

Scope discipline (docs/06-ethics-and-scope.md): this module only ever opens a TCP
connection, reads what the service volunteers, and optionally sends one HTTP
``HEAD`` request. It does not authenticate, does not send a payload, does not
follow redirects, and does not retry a failed probe. That is enough to identify a
version and not enough to change state.

The safety boundary is structural, not advisory:

* :class:`ActiveProbeConfig.authorised` must be set explicitly, **and**
* the host must match the configured allowlist (exact, subdomain suffix, or CIDR).

A caller that forgets either gets an empty list, never a silent scan.

What this can and cannot establish is deliberately visible in the output. A
banner is an operator-controlled string; the project's own literature records
>95% false positives for banner-derived CVE claims. So banner observations are
emitted with their raw evidence and are *never* treated as verified versions.
"""

from __future__ import annotations

import ipaddress
import re
import socket
import ssl
from dataclasses import dataclass, field
from datetime import UTC, datetime

from infravce.models import AcquisitionMethod, Ecosystem, Observation
from infravce.normalise.versions import normalise

__all__ = [
    "ActiveProbeConfig",
    "ProbeTarget",
    "PortResult",
    "banner_probe",
    "probe_ports",
    "scan_ports",
]

#: Ports worth trying when the caller does not name any. Kept short on purpose:
#: a full 65k sweep is a different tool with different authorisation needs.
DEFAULT_PORTS: tuple[int, ...] = (
    21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
    3000, 3306, 5432, 6379, 8000, 8080, 8443, 8888, 9000, 9090, 11434,
)

#: Ports we speak TLS to by default. ``--tls`` can add more.
TLS_PORTS: frozenset[int] = frozenset({443, 465, 636, 993, 995, 8443, 9443})

#: Banner/header product -> the package name the distribution tracker uses.
#: This is a hypothesis, recorded as such, not an identity resolution: the alias
#: table cannot help because a banner reports marketing names ("Apache httpd")
#: while Debian indexes source packages ("apache2").
_PRODUCT_MAP: dict[str, str] = {
    "nginx": "nginx",
    "openresty": "nginx",
    "apache": "apache2",
    "httpd": "apache2",
    "openssh": "openssh",
    "openssl": "openssl",
    "libressl": "libressl",
    "vsftpd": "vsftpd",
    "proftpd": "proftpd",
    "pure-ftpd": "pure-ftpd",
    "exim": "exim4",
    "postfix": "postfix",
    "dovecot": "dovecot",
    "mysql": "mysql-server",
    "mariadb": "mariadb-server",
    "redis": "redis",
    "memcached": "memcached",
    "postgresql": "postgresql",
    "php": "php",
    "tomcat": "tomcat9",
    "jetty": "jetty9",
    "iis": "iis",
    "caddy": "caddy",
    "lighttpd": "lighttpd",
    "squid": "squid",
    "haproxy": "haproxy",
    "varnish": "varnish",
    "jenkins": "jenkins",
    "grafana": "grafana",
    "prometheus": "prometheus",
}

#: ``name/1.2.3`` inside a Server/X-Powered-By header or a service banner.
_TOKEN = re.compile(
    r"(?P<name>[A-Za-z][A-Za-z0-9._-]{1,24})[/ ](?P<version>\d+(?:\.\d+)+[A-Za-z0-9.~+_-]*)"
)
#: ``SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.5`` uses an underscore separator.
_SSH = re.compile(r"SSH-\d\.\d-(?P<name>[A-Za-z]+)[-_](?P<version>\d+(?:\.\d+)+[A-Za-z0-9.~+_-]*)")

#: Headers that describe the server, in trust order. ``Date`` and ``ETag`` are
#: excluded deliberately: they contain digits and would produce phantom products.
_SERVER_HEADERS = ("server", "x-powered-by", "x-aspnet-version", "x-generator", "via")


@dataclass(frozen=True, slots=True)
class ProbeTarget:
    host: str
    port: int | None = None


@dataclass(frozen=True, slots=True)
class ActiveProbeConfig:
    authorised: bool = False
    allowlist: tuple[str, ...] = ()
    max_concurrent: int = 1
    timeout_s: float = 2.0
    tls_ports: frozenset[int] = field(default_factory=lambda: TLS_PORTS)

    def allows(self, host: str) -> bool:
        return _is_allowed(host, self)


@dataclass(frozen=True, slots=True)
class PortResult:
    host: str
    port: int
    open: bool
    tls: bool = False
    banner: str = ""
    http_status: str | None = None
    headers: tuple[tuple[str, str], ...] = ()
    certificate: dict[str, str] = field(default_factory=dict)
    error: str | None = None


def _is_allowed(host: str, cfg: ActiveProbeConfig) -> bool:
    """Whether active probing of ``host`` is authorised.

    Hostnames match exactly or as a subdomain suffix (``.example.com``). IPs match
    exactly or by CIDR. A bare suffix such as ``example.com`` intentionally does
    *not* authorise ``notexample.com``.
    """
    if not cfg.authorised or not cfg.allowlist:
        return False
    host = host.strip().lower()
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        for entry in cfg.allowlist:
            candidate = entry.strip().lower()
            if not candidate:
                continue
            if candidate.startswith("."):
                if host.endswith(candidate) and host != candidate.lstrip("."):
                    return True
            elif host == candidate or host.endswith(f".{candidate}"):
                return True
        return False
    for entry in cfg.allowlist:
        candidate = entry.strip()
        try:
            if "/" in candidate:
                if ip in ipaddress.ip_network(candidate, strict=False):
                    return True
            elif ip == ipaddress.ip_address(candidate):
                return True
        except ValueError:
            continue
    return False


def _read_available(sock: socket.socket, limit: int = 8192) -> bytes:
    """Read whatever the peer volunteers until it stops or the limit is hit."""
    chunks: list[bytes] = []
    total = 0
    while total < limit:
        try:
            chunk = sock.recv(min(2048, limit - total))
        except (TimeoutError, socket.timeout):
            break
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        # Headers end at the first blank line; a service banner usually arrives
        # in one packet and then waits for input.
        if b"\r\n\r\n" in b"".join(chunks):
            break
    return b"".join(chunks)


def _parse_headers(payload: bytes) -> tuple[str | None, tuple[tuple[str, str], ...]]:
    text = payload.decode("latin-1", errors="replace")
    lines = text.split("\r\n")
    status = lines[0].strip() if lines and lines[0].startswith("HTTP/") else None
    headers: list[tuple[str, str]] = []
    for line in lines[1:]:
        if not line or ":" not in line:
            break
        name, _, value = line.partition(":")
        headers.append((name.strip().lower(), value.strip()))
    return status, tuple(headers)


def _probe_one(host: str, port: int, cfg: ActiveProbeConfig) -> PortResult:
    try:
        sock = socket.create_connection((host, port), timeout=cfg.timeout_s)
    except OSError as exc:
        return PortResult(host, port, False, error=f"{type(exc).__name__}: {exc}")

    with sock:
        sock.settimeout(cfg.timeout_s)
        use_tls = port in cfg.tls_ports
        certificate: dict[str, str] = {}
        if use_tls:
            context = ssl.create_default_context()
            # Identification only: the certificate is evidence, not a trust
            # decision, and a scan must not fail because a lab uses a self-signed
            # cert.
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            try:
                sock = context.wrap_socket(sock, server_hostname=host)
                der = sock.getpeercert(binary_form=True)
                if der:
                    certificate = {"sha256": _sha256(der)}
            except ssl.SSLError as exc:
                return PortResult(host, port, True, tls=True, error=f"TLS: {exc}")

        initial = b""
        try:
            initial = _read_available(sock)
        except OSError:
            initial = b""

        # One HEAD request, only if the peer looks like HTTP or has said nothing.
        if not initial or initial.startswith(b"HTTP/"):
            request = (
                f"HEAD / HTTP/1.0\r\nHost: {host}\r\n"
                "User-Agent: infravce/0.1 (read-only version identification)\r\n\r\n"
            ).encode()
            try:
                sock.sendall(request)
                response = _read_available(sock)
            except OSError:
                response = b""
        else:
            response = initial

    status, headers = _parse_headers(response)
    banner = response.decode("latin-1", errors="replace").split("\r\n\r\n", 1)[0][:2000]
    return PortResult(
        host=host,
        port=port,
        open=True,
        tls=use_tls,
        banner=banner or initial.decode("latin-1", errors="replace")[:2000],
        http_status=status,
        headers=headers,
        certificate=certificate,
    )


def _sha256(data: bytes) -> str:
    import hashlib

    return hashlib.sha256(data).hexdigest()


def scan_ports(
    host: str,
    ports: tuple[int, ...] | list[int] | None = None,
    cfg: ActiveProbeConfig | None = None,
) -> list[PortResult]:
    """Probe ``ports`` on ``host``; refuse everything when not authorised."""
    cfg = cfg or ActiveProbeConfig()
    if not _is_allowed(host, cfg):
        return []
    selected = tuple(ports) if ports else DEFAULT_PORTS
    results: list[PortResult] = []
    for port in selected:
        if not 0 < int(port) < 65536:
            continue
        results.append(_probe_one(host, int(port), cfg))
    return results


def _candidates(result: PortResult) -> list[tuple[str, str, AcquisitionMethod, str]]:
    """Extract ``(display_name, version, method, evidence)`` from one probe.

    Only names in :data:`_PRODUCT_MAP` are accepted. A generic ``name/1.2.3``
    regex over a header block matches ``text/html``, ``ISO-8859-1`` and dozens of
    other non-products, and every one of those becomes a false advisory lookup.
    """
    found: list[tuple[str, str, AcquisitionMethod, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(raw_name: str, version: str, method: AcquisitionMethod, evidence: str) -> None:
        key_name = raw_name.strip().lower()
        package = _PRODUCT_MAP.get(key_name)
        if package is None or not version:
            return
        if (package, version) in seen:
            return
        seen.add((package, version))
        found.append((package, version, method, evidence))

    for name, value in result.headers:
        if name not in _SERVER_HEADERS:
            continue
        lowered = value.lower()
        for token in ("nginx", "openresty", "apache", "httpd", "caddy", "lighttpd",
                      "iis", "php", "tomcat", "jetty", "express", "haproxy"):
            if token in lowered:
                match = _TOKEN.search(value)
                if match:
                    add(token, match.group("version"), AcquisitionMethod.HTTP_HEADER,
                        f"{name}: {value}")
                    break

    banner = result.banner or ""
    ssh = _SSH.search(banner)
    if ssh:
        add(ssh.group("name").lower(), ssh.group("version"),
            AcquisitionMethod.BANNER, f"banner: {ssh.group(0)}")

    for match in _TOKEN.finditer(banner):
        name = match.group("name").lower()
        if name in _PRODUCT_MAP:
            add(name, match.group("version"),
                AcquisitionMethod.BANNER if not banner.startswith("HTTP/") else AcquisitionMethod.HTTP_HEADER,
                f"banner: {match.group(0)}")

    # Versionless but identifiable services: still worth an observation so the
    # report can say "redis on 6379, version not published" rather than omitting
    # the asset.
    lowered_banner = banner.lower()
    for marker, package in (
        ("redis", "redis"),
        ("memcached", "memcached"),
        ("postgresql", "postgresql"),
        ("mariadb", "mariadb-server"),
    ):
        if marker in lowered_banner and not any(p == package for p, _, _, _ in found):
            found.append((package, "", AcquisitionMethod.BANNER, f"banner mentions {marker}"))
    return found


def _observation(
    result: PortResult,
    package: str,
    version: str,
    method: AcquisitionMethod,
    evidence: str,
    *,
    ecosystem: Ecosystem | None,
) -> Observation:
    asset_id = f"{result.host}:{result.port}"
    raw_version = version.strip()
    normalised = normalise(raw_version, ecosystem=ecosystem, product=package) if raw_version else None
    resolved = normalised if normalised is not None and normalised.is_resolved else None
    return Observation(
        asset_id=asset_id,
        observed_at=datetime.now(UTC),
        acquisition_method=method,
        evidence=f"{asset_id} {method.value} {evidence}",
        raw_product=package,
        raw_version=raw_version,
        resolved_product=package,
        resolved_version=resolved,
        resolution_confidence=resolved.confidence if resolved else 0.0,
        parse_notes=(
            *(["banner-derived product name; identity is a hypothesis"] if method is not AcquisitionMethod.HTTP_HEADER else []),
            *((normalised.notes if normalised else ())),
        ),
    )


def probe_ports(
    host: str,
    ports: tuple[int, ...] | list[int] | None = None,
    cfg: ActiveProbeConfig | None = None,
    *,
    ecosystem: Ecosystem | None = None,
) -> list[Observation]:
    """Scan and convert to observations. Returns ``[]`` when unauthorised."""
    results = scan_ports(host, ports, cfg)
    observations: list[Observation] = []
    for result in results:
        if not result.open:
            continue
        for package, version, method, evidence in _candidates(result):
            observations.append(
                _observation(result, package, version, method, evidence, ecosystem=ecosystem)
            )
    return observations


def banner_probe(target: ProbeTarget, cfg: ActiveProbeConfig) -> list[Observation]:
    """Backwards-compatible single-target entry point."""
    if not _is_allowed(target.host, cfg):
        return []
    ports = [target.port] if target.port else None
    return probe_ports(target.host, ports, cfg)
