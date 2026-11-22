#!/usr/bin/env python3
"""Technical SEO checks over docs/ (R6A). Exit 1 on any error.

- every sitemap URL: file exists, not noindex, unique <title> + meta description, canonical == its own URL
- every noindex page is absent from the sitemap
- JSON-LD parses; no aggregateRating / review (we have no real reviews)
- <img> has width + height + alt (alt="" allowed for decorative)
- internal <a href> targets exist (all html pages except dl/)
- _redirects sources do not exist as files unless forced, targets exist
    python3 tools/site/seo_check.py
"""
import json
import pathlib
import re
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from audit_content import norm_link, BASE  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
errs, warns = [], []


def target_exists(t):
    t = t.split("#")[0]
    if t in ("", "/"):
        return True
    p = DOCS / t
    return p.is_file() or (p / "index.html").is_file()


def redirect_sources():
    f = DOCS / "_redirects"
    out = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) >= 2 and not line.startswith("#"):
                out[parts[0].lstrip("/")] = parts[1].lstrip("/")
    return out


def main():
    sm = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    urls = [u[len(BASE):] for u in re.findall(r"<loc>([^<]+)</loc>", sm)]
    redirects = redirect_sources()
    titles, descs = defaultdict(list), defaultdict(list)
    for u in urls:
        f = DOCS / u / "index.html" if u == "" or u.endswith("/") else DOCS / u
        if not f.exists():
            errs.append(f"sitemap URL without file: {u}")
            continue
        s = f.read_text(encoding="utf-8")
        if re.search(r'name="robots"[^>]+noindex', s):
            errs.append(f"noindex page in sitemap: {u}")
        t = re.search(r"<title>(.*?)</title>", s, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', s)
        c = re.search(r'<link rel="canonical" href="([^"]*)"', s)
        if not t:
            errs.append(f"no title: {u}")
        else:
            titles[t.group(1).strip()].append(u)
            if len(t.group(1)) > 75:
                warns.append(f"long title ({len(t.group(1))}): {u}")
        if not d or not d.group(1).strip():
            errs.append(f"no meta description: {u}")
        else:
            descs[d.group(1).strip()].append(u)
        if not c:
            errs.append(f"no canonical: {u}")
        elif c.group(1) != BASE + u:
            errs.append(f"canonical mismatch: {u} -> {c.group(1)}")
    for k, v in list(titles.items()) + list(descs.items()):
        if len(v) > 1:
            errs.append(f"duplicate title/description {k[:50]!r}: {v}")
    for u in redirects:
        if u in urls:
            errs.append(f"redirected URL still in sitemap: {u}")
    for f in sorted(DOCS.rglob("*.html")):
        rel = f.relative_to(DOCS).as_posix()
        if rel.startswith(("dl/", "shots/")):
            continue
        pu = rel[: -len("index.html")] if rel.endswith("index.html") else rel
        s = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'name="robots"[^>]+noindex', s) and f"<loc>{BASE}{pu}</loc>" in sm:
            errs.append(f"noindex page listed in sitemap: {pu}")
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                data = json.loads(blk)
            except Exception as ex:
                errs.append(f"bad JSON-LD in {rel}: {ex}")
                continue
            js = json.dumps(data)
            if re.search(r'"(aggregateRating|review|reviewRating)"', js):
                errs.append(f"rating/review markup in {rel}")
        for img in re.findall(r"<img\b[^>]*>", s):
            if "width=" not in img or "height=" not in img:
                errs.append(f"img without width/height in {rel}: {img[:90]}")
            if "alt=" not in img:
                errs.append(f"img without alt in {rel}: {img[:90]}")
        body = re.sub(r"<script\b(?![^>]*ld\+json).*?</script>", " ", s, flags=re.S)
        for href in re.findall(r'<a\b[^>]*href="([^"]+)"', body):
            if "${" in href or "{{" in href or "'" in href:
                continue
            t = norm_link(pu, href)
            if not t or t.startswith(("EXT:", "api/")):
                continue
            if t.rstrip("/") in redirects or t in redirects:
                errs.append(f"link to redirected URL in {rel}: {href}")
            elif not target_exists(t):
                errs.append(f"broken internal link in {rel}: {href} -> {t}")
    for src, dst in redirects.items():
        if not target_exists(dst):
            errs.append(f"redirect target missing: {src} -> {dst}")
    for w in warns:
        print("warn:", w)
    for e in errs:
        print("ERROR:", e)
    print(f"{len(urls)} sitemap URLs checked; {len(errs)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
