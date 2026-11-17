#!/usr/bin/env python3
"""Write docs/sitemap.xml and docs/robots.txt.

Includes every docs/**/index.html (plus other .html pages) except thanks/, dl/, 404 and pages
with <meta name="robots" content="noindex">. lastmod = last git commit date of the file (or today).
hreflang: pairs listed in docs/data/hreflang.json ({"pairs":[{"en": "en/...", "he": "..."}]}) get reciprocal
<xhtml:link rel="alternate"> entries (he is x-default).
    python3 tools/site/build_sitemap.py [--base URL]   (default: site_config.BASE_URL)
The site is served from the domain root, so docs/robots.txt is the host's robots.txt.
"""
import argparse
import datetime
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from site_config import BASE_URL  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
DEFAULT_BASE = BASE_URL
EXCLUDE_DIRS = {"thanks", "dl", "assets", "data"}
PRIORITY = {"": "1.0", "products": "0.9", "tools": "0.9", "p": "0.9", "legal": "0.3"}


def lastmod(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)], cwd=REPO,
                             capture_output=True, text=True, timeout=10).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.today().isoformat()


def pages():
    for f in sorted(DOCS.rglob("*.html")):
        rel = f.relative_to(DOCS)
        if rel.parts[0] in EXCLUDE_DIRS or rel.name == "404.html" or rel.name.startswith("_"):
            continue
        head = f.read_text(encoding="utf-8", errors="ignore")[:6000]
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', head, re.I):
            continue
        url = rel.as_posix()
        url = url[: -len("index.html")] if url.endswith("index.html") else url
        yield url, f


def alternates():
    """url -> [(lang, url)] from docs/data/hreflang.json (optional)."""
    import json
    f = DOCS / "data" / "hreflang.json"
    out = {}
    if not f.exists():
        return out
    for p in json.loads(f.read_text(encoding="utf-8")).get("pairs", []):
        alts = [("he", p["he"]), ("en", p["en"]), ("x-default", p["he"])]
        out[p["he"]] = out[p["en"]] = alts
    return out


def build(base=DEFAULT_BASE):
    base = base.rstrip("/") + "/"
    rows = []
    alts = alternates()
    for url, f in pages():
        segs = url.split("/")
        if segs[0] == "en":  # English section mirrors the Hebrew priorities
            segs = segs[1:]
        top = segs[0] if segs else ""
        pr = PRIORITY.get(top, "0.6")
        if top == "tools" and len(segs) > 2:
            pr = "0.8"
        links = "".join(f'<xhtml:link rel="alternate" hreflang="{lang}" href="{base}{u}"/>' for lang, u in alts.get(url, []))
        rows.append(f"  <url><loc>{base}{url}</loc>{links}<lastmod>{lastmod(f)}</lastmod><priority>{pr}</priority></url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")
    (DOCS / "sitemap.xml").write_text(xml, encoding="utf-8")
    from urllib.parse import urlparse
    prefix = urlparse(base).path  # "/" at the domain root
    robots = (f"User-agent: *\nAllow: /\nDisallow: {prefix}thanks/\nDisallow: {prefix}en/thanks/\nDisallow: {prefix}dl/\n\n"
              f"Sitemap: {base}sitemap.xml\n")
    (DOCS / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"sitemap.xml: {len(rows)} urls; robots.txt written (base {base})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=DEFAULT_BASE)
    build(ap.parse_args().base)
