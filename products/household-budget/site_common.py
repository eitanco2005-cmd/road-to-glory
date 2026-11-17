"""Shared page shell for W3 pages (household budget + renovation). Uses W1's design system (assets/site.css)."""
import json
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "site"))
from site_config import BASE_URL as BASE, BRAND  # noqa: E402
UPDATED = "2026-11-17"
UPDATED_HE = "17 בנובמבר 2026"


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def page(path, title, desc, body, jsonld, og_image=None, crumbs=(), extra_scripts=(), buy=False):
    """path: site path like 'p/household-budget/' (relative to docs). crumbs: [(name, path or None)]."""
    depth = path.strip("/").count("/") + 1 if path.strip("/") else 0
    up = "../" * depth
    url = BASE + path
    og = BASE + (og_image or "assets/og-default.png")
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": BASE + p} if p is not None else {"item": url})}
        for i, (n, p) in enumerate([("ראשי", "")] + list(crumbs))]}
    lds = "\n".join(f'<script type="application/ld+json">\n{json.dumps(j, ensure_ascii=False)}\n</script>' for j in [*jsonld, bc])
    crumb_html = '<nav class="breadcrumbs" aria-label="פירורי לחם"><a href="' + up + '">ראשי</a>'
    for n, p in crumbs:
        crumb_html += '<span aria-hidden="true">›</span>'
        crumb_html += f'<a href="{up}{p}">{n}</a>' if p is not None and p != path else n
    crumb_html += "</nav>"
    scripts = [f'<script src="{up}assets/site.js"></script>']
    if buy:
        scripts.append(f'<script src="{up}assets/checkout.js"></script>')
    scripts += [s.replace("{up}", up) for s in extra_scripts]
    html = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'product' if buy else 'website'}">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e6b63">
<link rel="icon" type="image/svg+xml" href="{up}assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
<style>
/* W3 page extras (only used where W1's design system has no equivalent) */
.w3-hero-img{{border-radius:var(--radius);border:1px solid var(--border);box-shadow:var(--shadow-lg);background:#fff;width:100%;height:auto}}
.w3-list{{padding-inline-start:1.2rem}} .w3-list li{{margin:.3rem 0}}
.w3-guides a{{font-weight:700}}
.w3-tiles{{display:grid;gap:.75rem;grid-template-columns:1fr}} @media(min-width:640px){{.w3-tiles{{grid-template-columns:repeat(3,1fr)}}}}
.w3-tile{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem}}
.w3-tile .k{{font-weight:700;color:var(--muted);font-size:.95rem}} .w3-tile .v{{font-size:1.8rem;font-weight:800;font-variant-numeric:tabular-nums;color:var(--primary)}}
.w3-tile .s{{font-size:.9rem;color:var(--muted)}}
.w3-row{{display:flex;justify-content:space-between;gap:.75rem;align-items:baseline;margin:.6rem 0 .25rem}}
.w3-note{{font-size:.9rem;color:var(--muted)}}
.prose img{{max-width:100%;height:auto;border-radius:var(--radius-sm);border:1px solid var(--border)}}
</style>
{lds}
</head>
<body>
<header id="site-header"></header>
<main id="main">
{body.replace("{CRUMBS}", crumb_html).replace("{up}", up)}
</main>
<footer id="site-footer"></footer>
{chr(10).join(scripts)}
</body>
</html>
"""
    out = DOCS / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


def faq_html(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


def faq_ld(items):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}


def article_ld(title, desc, path, image=None):
    return {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
            "inLanguage": "he-IL", "datePublished": UPDATED, "dateModified": UPDATED, "mainEntityOfPage": BASE + path,
            **({"image": BASE + image} if image else {}), "author": {"@type": "Organization", "name": BRAND},
            "publisher": {"@type": "Organization", "name": BRAND}}


def product_ld(name, desc, path, price, images):
    return {"@context": "https://schema.org", "@type": "Product", "name": name, "description": desc,
            "image": [BASE + i for i in images], "brand": {"@type": "Brand", "name": BRAND},
            "offers": {"@type": "Offer", "price": str(price), "priceCurrency": "ILS", "availability": "https://schema.org/InStock",
                       "url": BASE + path}}


def app_ld(name, desc, path):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "description": desc, "url": BASE + path,
            "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "inLanguage": "he-IL",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ILS"}}
