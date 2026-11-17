"""Shared HTML helpers for W2 pages (static output into docs/)."""
import html
import json
import os

BASE = "https://eitanco2005-cmd.github.io/road-to-glory/"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DOCS = os.path.join(REPO, "docs")
UPDATED = "2026-11-17"
UPDATED_HE = "נובמבר 2026"


def esc(s):
    return html.escape(s, quote=True)


def rel(path):
    """relative prefix from docs/<path>/index.html back to docs/"""
    depth = len([p for p in path.strip("/").split("/") if p])
    return "../" * depth


def page(path, title, desc, body, jsonld, og_image=None, extra_head="", scripts=""):
    r = rel(path)
    url = BASE + path.strip("/") + "/"
    og = og_image or (BASE + "assets/og-default.png")
    ld = json.dumps({"@context": "https://schema.org", "@graph": jsonld}, ensure_ascii=False, indent=1)
    out = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="Glory">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e6b63">
<link rel="icon" type="image/svg+xml" href="{r}assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="{r}assets/site.css">
{extra_head}<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<header id="site-header"></header>
<main id="main">
{body}
</main>
<footer id="site-footer"></footer>
<script src="{r}assets/site.js"></script>
{scripts}</body>
</html>
"""
    dst = os.path.join(DOCS, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    return dst


def breadcrumbs(items):
    """items: list of (label, href or None). Returns (html, jsonld)."""
    parts = []
    for i, (lab, href) in enumerate(items):
        if href:
            parts.append(f'<a href="{href}">{esc(lab)}</a>')
        else:
            parts.append(f'<span aria-current="page">{esc(lab)}</span>')
    sep = ' <span aria-hidden="true">›</span> '
    h = f'<nav class="breadcrumbs" aria-label="פירורי לחם">{sep.join(parts)}</nav>'
    return h


def breadcrumb_ld(items):
    """items: list of (label, absolute path under BASE or '')"""
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": lab, "item": BASE + p} for i, (lab, p) in enumerate(items)]}


def faq_html(faqs):
    out = ['<div class="faq">']
    for q_, a in faqs:
        out.append(f"<details><summary>{esc(q_)}</summary><p>{a}</p></details>")
    out.append("</div>")
    return "\n".join(out)


def faq_ld(faqs):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q_, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q_, a in faqs]}
