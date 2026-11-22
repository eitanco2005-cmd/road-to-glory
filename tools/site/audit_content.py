#!/usr/bin/env python3
"""Content audit of every sitemap URL (R6A). Writes research/content-audit.json (raw metrics).

Per page: title, meta description, h1, main-text word count, max near-duplicate similarity vs any other page
(Jaccard on 5-word shingles of main text), sources (external links in a sources box / outbound links),
interactive tool / checkout presence, internal links in/out, robots noindex, canonical.
    python3 tools/site/audit_content.py [--urls-from-dirs]   (default: URLs from docs/sitemap.xml)
"""
import html
import json
import pathlib
import re
import sys
from collections import defaultdict

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
BASE = "https://tichnun.netlify.app/"


def page_file(url):
    p = DOCS / url
    return p / "index.html" if url == "" or url.endswith("/") else p


def text_of(s):
    m = re.search(r"<main[^>]*>(.*)</main>", s, re.S)
    b = m.group(1) if m else s
    b = re.sub(r"<(script|style|svg|noscript)\b.*?</\1>", " ", b, flags=re.S)
    b = re.sub(r"<!--.*?-->", " ", b, flags=re.S)
    b = re.sub(r"<[^>]+>", " ", b)
    return html.unescape(re.sub(r"\s+", " ", b)).strip()


def shingles(t, k=5):
    w = re.findall(r"[\w֐-׿₪%.,'-]+", t.lower())
    return {" ".join(w[i:i + k]) for i in range(max(0, len(w) - k + 1))}


def norm_link(page_url, href):
    href = href.split("#")[0].split("?")[0]
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:", "whatsapp:")):
        return None
    if href.startswith(BASE):
        return href[len(BASE):]
    if href.startswith(("http://", "https://", "//")):
        return "EXT:" + href
    if href.startswith("/"):
        target = href[1:]
    else:
        base = page_url if page_url.endswith("/") or page_url == "" else (page_url.rsplit("/", 1)[0] + "/" if "/" in page_url else "")
        parts = [x for x in base.split("/") if x]
        for seg in href.split("/"):
            if seg == "..":
                parts = parts[:-1]
            elif seg in (".", ""):
                continue
            else:
                parts.append(seg)
        target = "/".join(parts) + ("/" if parts and (href.endswith("/") or href.endswith(".")) else "")
    if target.endswith("index.html"):
        target = target[: -len("index.html")]
    return target


def main():
    sm = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    urls = [u[len(BASE):] for u in re.findall(r"<loc>([^<]+)</loc>", sm)]
    rows, sh = {}, {}
    inbound = defaultdict(set)
    allhtml = [f for f in DOCS.rglob("*.html") if "/dl/" not in f.as_posix()]
    for f in allhtml:  # inbound links counted from every page (indexable or not)
        rel = f.relative_to(DOCS).as_posix()
        pu = rel[: -len("index.html")] if rel.endswith("index.html") else rel
        s = f.read_text(encoding="utf-8", errors="ignore")
        for href in re.findall(r'<a\b[^>]*href="([^"]+)"', s):
            t = norm_link(pu, href)
            if t is not None and not t.startswith("EXT:") and t != pu:
                inbound[t].add(pu)
    for u in urls:
        f = page_file(u)
        s = f.read_text(encoding="utf-8", errors="ignore")
        t = text_of(s)
        links = [norm_link(u, h) for h in re.findall(r'<a\b[^>]*href="([^"]+)"', s)]
        links = [x for x in links if x]
        ext = sorted({x[4:] for x in links if x.startswith("EXT:") and "wa.me" not in x and "whatsapp" not in x
                      and "fonts.g" not in x and "paypal" not in x})
        out_int = sorted({x for x in links if not x.startswith("EXT:") and x != u})
        g = lambda rx: (re.search(rx, s, re.S | re.I).group(1).strip() if re.search(rx, s, re.S | re.I) else "")
        rows[u] = {
            "url": u,
            "title": html.unescape(g(r"<title>(.*?)</title>")),
            "desc": html.unescape(g(r'<meta name="description" content="([^"]*)"')),
            "h1": html.unescape(re.sub(r"<[^>]+>", "", g(r"<h1[^>]*>(.*?)</h1>"))),
            "canonical": g(r'<link rel="canonical" href="([^"]*)"'),
            "words": len(t.split()),
            "ext_links": ext,
            "has_sources": bool(re.search(r"מקורות|Sources|sources-box|class=\"sources", s)) and bool(ext),
            "has_tool": bool(re.search(r"<form|<input|calc\.js|data-calc|<select", s)),
            "has_checkout": 'data-product=' in s or 'class="buy' in s,
            "out_internal": len(out_int),
            "in_internal": len(inbound.get(u, set())),
            "noindex": bool(re.search(r'name="robots"[^>]+noindex', s)),
        }
        sh[u] = shingles(t)
    for u in urls:
        best, bu = 0.0, ""
        for v in urls:
            if v == u or not sh[u] or not sh[v]:
                continue
            j = len(sh[u] & sh[v]) / len(sh[u] | sh[v])
            if j > best:
                best, bu = j, v
        rows[u]["dup"] = round(best, 3)
        rows[u]["dup_with"] = bu
    out = REPO / "research" / "content-audit.json"
    out.write_text(json.dumps(list(rows.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    # duplicate titles/descriptions
    for key in ("title", "desc"):
        seen = defaultdict(list)
        for r in rows.values():
            seen[r[key]].append(r["url"])
        for k, v in seen.items():
            if len(v) > 1:
                print(f"DUP {key}: {k!r} -> {v}")
    print(f"{len(rows)} pages -> {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
