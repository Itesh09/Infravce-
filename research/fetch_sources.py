#!/usr/bin/env python3
"""
Archive and fetch every source cited in the research phase.

Reads research/sources.json (the manifest), downloads each URL, converts HTML to
Markdown, and writes research/sources/DOWNLOAD_LOG.csv with a status per URL.

Usage:
    python3 research/fetch_sources.py            # fetch everything not already cached
    python3 research/fetch_sources.py --verify   # re-check cached files only, no network
    python3 research/fetch_sources.py --retry-failed
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
MANIFEST = ROOT / "sources.json"
LOG = SOURCES / "DOWNLOAD_LOG.csv"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0 Safari/537.36"
)
TIMEOUT = 90
RETRIES = 2


def slug(url: str) -> str:
    """Stable, readable, filesystem-safe stem for a URL."""
    parsed = urlparse(url)
    host = parsed.netloc.replace("www.", "")
    tail = (parsed.path or "/").strip("/")
    tail = re.sub(r"\.(html?|php|aspx?)$", "", tail, flags=re.I)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", f"{host}_{tail}") if tail else host
    stem = re.sub(r"-{2,}", "-", stem).strip("-")
    if len(stem) > 110:
        digest = hashlib.sha1(url.encode()).hexdigest()[:8]
        stem = f"{stem[:100]}-{digest}"
    return stem.lower()


def build_manifest() -> list[dict]:
    if not MANIFEST.exists():
        sys.exit(f"manifest not found: {MANIFEST}")
    entries = json.loads(MANIFEST.read_text())
    seen: set[str] = set()
    out: list[dict] = []
    for e in entries:
        url = e["url"].strip()
        if url in seen:
            continue
        seen.add(url)
        out.append({**e, "url": url})
    return out


def already_ok(entry: dict) -> Path | None:
    for ext in (".pdf", ".md", ".html", ".txt"):
        p = SOURCES / entry["category"] / f"{entry['id']}{ext}"
        if p.exists() and p.stat().st_size > 1200:
            return p
    return None


def fetch(entry: dict) -> dict:
    dest_dir = SOURCES / entry["category"]
    dest_dir.mkdir(parents=True, exist_ok=True)
    url = entry["url"]
    row = {
        "id": entry["id"],
        "category": entry["category"],
        "title": entry.get("title", ""),
        "cited_in": entry.get("cited_in", ""),
        "url": url,
        "file": "",
        "bytes": 0,
        "status": "",
        "note": "",
    }

    cached = already_ok(entry)
    if cached and not entry.get("_force"):
        row.update(file=str(cached.relative_to(ROOT)), bytes=cached.stat().st_size,
                   status="CACHED", note="already archived")
        return row

    last_err = ""
    for attempt in range(1, RETRIES + 1):
        with tempfile.TemporaryDirectory() as tmp:
            blob = Path(tmp) / "blob"
            cmd = [
                "curl", "-sSL", "--compressed", "--max-time", str(TIMEOUT),
                "-A", UA, "-o", str(blob), "-w", "%{http_code}",
                url,
            ]
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT + 20)
                code = (proc.stdout or "").strip()[-3:]
            except subprocess.TimeoutExpired:
                last_err = "timeout"
                code = "000"

            if code and not code.startswith(("2", "3")):
                last_err = f"http {code}"
                if code == "000":
                    last_err = "connection failed"
                time.sleep(1.5 * attempt)
                continue

            if not blob.exists() or blob.stat().st_size < 1200:
                last_err = f"empty body ({code})"
                time.sleep(1.5 * attempt)
                continue

            head = blob.read_bytes()[:5]
            ctype = ""
            if head.startswith(b"%PDF"):
                out = dest_dir / f"{entry['id']}.pdf"
                out.write_bytes(blob.read_bytes())
            else:
                try:
                    ctype = subprocess.run(
                        ["file", "-b", "--mime-type", str(blob)],
                        capture_output=True, text=True).stdout.strip()
                except Exception:
                    ctype = ""
                if "html" in ctype or ctype in ("", "text/plain", "application/xhtml+xml"):
                    md = dest_dir / f"{entry['id']}.md"
                    conv = subprocess.run(
                        ["pandoc", "-f", "html", "-t", "gfm", "--wrap=none",
                         "-M", "title=" + (entry.get("title") or url), str(blob)],
                        capture_output=True, text=True)
                    text = conv.stdout or blob.read_text("utf-8", errors="ignore")
                    text = re.sub(r"\n{4,}", "\n\n\n", text).strip()
                    if len(text) < 600:
                        # JS-rendered page: keep a stub plus the raw body for later retry
                        out = dest_dir / f"{entry['id']}.html"
                        out.write_bytes(blob.read_bytes())
                        row.update(status="STUB", note="JS-rendered; saved raw HTML")
                    else:
                        md.write_text(text, encoding="utf-8")
                        out = md
                        row["note"] = "html->markdown"
                else:
                    out = dest_dir / f"{entry['id']}{Path(blob.name).suffix or '.bin'}"
                    out.write_bytes(blob.read_bytes())

            size = out.stat().st_size
            row.update(file=str(out.relative_to(ROOT)), bytes=size, status="OK")
            if not row["note"]:
                row["note"] = out.suffix.lstrip(".") or "binary"
            return row

    row.update(status="FAILED", note=last_err or "unknown")
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="check cached files, no network")
    ap.add_argument("--retry-failed", action="store_true", help="retry only FAILED rows")
    ap.add_argument("--category", default=None, help="limit to one category")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    manifest = build_manifest()
    if args.category:
        manifest = [e for e in manifest if e["category"] == args.category]

    previous: dict[str, dict] = {}
    if LOG.exists():
        with LOG.open(newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                previous[r["url"]] = r
        if args.retry_failed:
            manifest = [e for e in manifest if previous.get(e["url"], {}).get("status") == "FAILED"]

    if args.verify:
        for e in manifest:
            p = already_ok(e)
            print(f"{'OK  ' if p else 'MISS'}  {e['id']}  {e['url']}")
        return 0

    print(f"fetching {len(manifest)} sources with {args.workers} workers ...", flush=True)
    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(fetch, e): e for e in manifest}
        for i, fut in enumerate(concurrent.futures.as_completed(futs), 1):
            r = fut.result()
            results.append(r)
            mark = {"OK": "+", "CACHED": "=", "STUB": "~", "FAILED": "!"}.get(r["status"], "?")
            print(f"  [{i:>3}/{len(manifest)}] {mark} {r['id']:<8} {r['status']:<6} {r['note'][:40]}", flush=True)

    by_url = {r["url"]: r for r in results}
    merged = []
    for e in manifest:
        r = by_url.get(e["url"])
        if r is None:
            r = previous.get(e["url"], {**e, "file": "", "bytes": 0, "status": "MISSING", "note": ""})
        merged.append(r)

    with LOG.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "category", "title", "cited_in", "url", "file", "bytes", "status", "note"])
        w.writeheader()
        w.writerows(merged)

    tally: dict[str, int] = {}
    for r in merged:
        tally[r["status"]] = tally.get(r["status"], 0) + 1
    print("\nsummary:", ", ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    print(f"total bytes: {sum(int(r['bytes'] or 0) for r in merged):,}")
    print(f"log: {LOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
