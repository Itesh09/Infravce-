#!/usr/bin/env python3
"""
Fourth pass: backfill titles for the `lit-*` manifest entries, then re-run the
open-mirror recovery for them.

The first manifest builder parsed the verification ledger, which carries URLs
but no titles, so the Semantic Scholar / arXiv title search in recover_open.py
had nothing to query with. This script mines the titles back out of the
literature review's section headings and re-attempts retrieval.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIT = ROOT / "raw" / "02-academic-literature-review.md"
SOURCES = ROOT / "sources"
LOG = SOURCES / "DOWNLOAD_LOG.csv"
MANIFEST = ROOT / "sources.json"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.76"


def mine_titles() -> dict[str, str]:
    """Map bare URL -> best-guess paper title from the review's headings and inline text."""
    text = LIT.read_text(encoding="utf-8")
    out: dict[str, str] = {}

    # Section headings look like:  ### 1.1 Author — "Title" — **VERIFIED**
    for m in re.finditer(r'^#{2,4}\s+[\d.]+\s+.*?[""“]([^""”]{8,160})[""”]', text, flags=re.M):
        start, end = m.start(), min(len(text), m.end() + 900)
        block = text[start:end]
        for u in re.findall(r"https?://[^\s)|]+", block):
            out.setdefault(u.rstrip(".,;"), m.group(1).strip())

    # Fallback: any bullet line that pairs a quoted title with a URL
    for m in re.finditer(r'[""“]([^""”]{10,160})[""”][^\n]{0,200}?(https?://[^\s)|]+)', text):
        out.setdefault(m.group(2).rstrip(".,;"), m.group(1).strip())
    return out


def jfetch(url: str):
    try:
        p = subprocess.run(["curl", "-sSL", "--max-time", "40", "-A", UA, url],
                           capture_output=True, text=True, timeout=55)
        return json.loads(p.stdout) if p.stdout.strip() else None
    except Exception:
        return None


def save_pdf(url: str, dest: Path) -> bool:
    tmp = dest.with_suffix(".part")
    try:
        p = subprocess.run(["curl", "-sSL", "--max-time", "90", "-A", UA, "-o", str(tmp),
                            "-w", "%{http_code}", url], capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        tmp.unlink(missing_ok=True)
        return False
    code = (p.stdout or "").strip()[-3:]
    if code.startswith(("2", "3")) and tmp.exists() and tmp.stat().st_size > 2000 and tmp.read_bytes()[:5] == b"%PDF":
        dest.write_bytes(tmp.read_bytes())
        tmp.unlink(missing_ok=True)
        return True
    tmp.unlink(missing_ok=True)
    return False


def main() -> int:
    titles = mine_titles()
    manifest = json.loads(MANIFEST.read_text())
    filled = 0
    for e in manifest:
        if e.get("title"):
            continue
        t = titles.get(e["url"]) or titles.get(e["url"].rstrip("/"))
        if t:
            e["title"] = t
            filled += 1
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"backfilled {filled} titles into the manifest\n")

    rows = list(csv.DictReader(LOG.open(newline="", encoding="utf-8")))
    by_url = {e["url"]: e for e in manifest}
    stubs = [r for r in rows if r["status"] == "STUB"]

    for r in stubs:
        url = r["url"]
        title = by_url.get(url, {}).get("title", "")
        r["title"] = title
        dest = SOURCES / r["category"] / r["id"]
        if not title:
            print(f"  SKIP        {r['id']:<24} no title mined")
            continue

        # Semantic Scholar
        data = jfetch("https://api.semanticscholar.org/graph/v1/paper/search"
                      f"?query={urllib.parse.quote(title)}&limit=1"
                      "&fields=title,year,venue,externalIds,openAccessPdf,abstract")
        time.sleep(3.5)
        meta = (data or {}).get("data", [None])[0]
        if not meta:
            print(f"  NO-METADATA {r['id']:<24} {title[:48]}")
            continue

        got = None
        oa = (meta.get("openAccessPdf") or {}).get("url")
        if oa and save_pdf(oa, dest.with_suffix(".pdf")):
            got = f"Semantic Scholar openAccessPdf -> {oa}"
        else:
            # arXiv by exact title
            q = urllib.parse.quote(f'ti:"{meta.get("title", title)[:110]}"')
            ax = jfetch(f"https://export.arxiv.org/api/query?search_query={q}&max_results=3")
            time.sleep(1.5)
            for e in ((ax or {}).get("entry") or []):
                aid = str(e.get("id", "")).rsplit("/", 1)[-1].split("v")[0]
                if aid and save_pdf(f"https://arxiv.org/pdf/{aid}", dest.with_suffix(".pdf")):
                    got = f"arXiv preprint {aid} (title match)"
                    break

        if got:
            p = dest.with_suffix(".pdf")
            r.update(status="OK", file=str(p.relative_to(ROOT)), bytes=str(p.stat().st_size), note=got)
            print(f"  RECOVERED   {r['id']:<24} {got[:60]}")
        else:
            p = dest.with_suffix(".md")
            r.update(status="STUB", note=f"title-mined but paywalled: {title[:70]}")
            # keep the stub but enrich it with the mined title
            if p.exists():
                p.write_text(f"# {title}\n\n> **Full text not retrieved** — paywalled at time of archiving.\n"
                             f"Obtain via institutional access before quoting in the report.\n\n- **URL:** {url}\n",
                             encoding="utf-8")
            print(f"  PAYWALLED   {r['id']:<24} {title[:52]}")

    with LOG.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "category", "title", "cited_in", "url", "file", "bytes", "status", "note"])
        w.writeheader()
        w.writerows(rows)

    tally: dict[str, int] = {}
    for r in rows:
        tally[r["status"]] = tally.get(r["status"], 0) + 1
    print("\nfinal tally:", ", ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
