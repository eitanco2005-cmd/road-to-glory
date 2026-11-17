"""Page shell for the Hanukkah pages (he RTL under docs/p, docs/tools, docs/hanukkah; en LTR under docs/en/hanukkah).
Uses the shared design system (assets/site.css, site.js, checkout.js). English pages carry their own static
header/footer (site.js only injects into #site-header/#site-footer, which English pages don't have)."""
import json
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "site"))
from site_config import BASE_URL as BASE, BRAND, BRAND_LATIN  # noqa: E402

UPDATED = "2026-11-17"

EXTRA_CSS = """
.hk-hero-img{border-radius:var(--radius);border:1px solid var(--border);box-shadow:var(--shadow-lg);background:#fff;width:100%;height:auto}
.hk-list{padding-inline-start:1.2rem}.hk-list li{margin:.3rem 0}
.hk-pages{display:grid;gap:1rem;grid-template-columns:repeat(2,1fr)}@media(min-width:760px){.hk-pages{grid-template-columns:repeat(4,1fr)}}
.hk-pages figure{margin:0}.hk-pages img{width:100%;height:auto;border:1px solid var(--border);border-radius:var(--radius-sm);box-shadow:var(--shadow);background:#fff}
.hk-pages figcaption{font-size:.9rem;color:var(--muted);text-align:center;margin-top:.35rem}
.hk-dates{width:100%;border-collapse:collapse;font-size:.98rem}.hk-dates th,.hk-dates td{border:1px solid var(--border);padding:.45rem .6rem;text-align:center}
.hk-dates th{background:var(--surface-2)}
.hk-tiles{display:grid;gap:.75rem;grid-template-columns:repeat(2,1fr)}@media(min-width:640px){.hk-tiles{grid-template-columns:repeat(4,1fr)}}
.hk-tile{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:.9rem}
.hk-tile .k{font-weight:700;color:var(--muted);font-size:.92rem}.hk-tile .v{font-size:1.7rem;font-weight:800;font-variant-numeric:tabular-nums;color:var(--primary)}
.hk-tile .s{font-size:.85rem;color:var(--muted)}
.hk-ing{width:100%;border-collapse:collapse}.hk-ing td{border-bottom:1px solid var(--border);padding:.35rem .25rem}.hk-ing td.num{text-align:end;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.hk-note{font-size:.9rem;color:var(--muted)}
.hk-bracha{font-family:'Noto Sans Hebrew','Assistant',sans-serif;font-size:1.3rem;line-height:1.9;background:var(--surface-2);border-radius:var(--radius-sm);padding:.6rem 1rem;margin:.5rem 0}
.prose img{max-width:100%;height:auto;border-radius:var(--radius-sm);border:1px solid var(--border)}
.en-header .brand small{display:none}
@media(max-width:480px){.en-header .brand span{display:none}.en-header .nav a{padding:.4rem .4rem}}
.lang-switch{font-weight:700;font-size:.92rem}
"""

EN_LOGO = ('<svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#0e6b63"/>'
           '<path d="M32 12l5.6 12.4 13.4 1.4-10 9.1 2.8 13.2L32 41.4l-11.8 6.7 2.8-13.2-10-9.1 13.4-1.4z" fill="#f0b44c"/></svg>')


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def strip(s):
    return re.sub(r"<[^>]+>", "", s)


def en_header(up, he_alt=None):
    sw = f'<a class="lang-switch" href="{up}{he_alt}" hreflang="he" lang="he">עברית</a>' if he_alt else ""
    return (f'<header class="site-header en-header"><a class="skip-link" href="#main">Skip to content</a><div class="container bar">'
            f'<a class="brand" href="{up}en/hanukkah/" aria-label="{BRAND_LATIN} — Hanukkah">{EN_LOGO}<span>{BRAND_LATIN}</span></a>'
            f'<nav class="nav" aria-label="Main"><a href="{up}en/hanukkah/">Hanukkah</a><a href="{up}en/hanukkah/latke-calculator/">Calculator</a>{sw}</nav>'
            f'</div></header>')


def en_footer(up):
    return (f'<footer class="site-footer"><div class="container"><div class="cols">'
            f'<div><a class="brand" href="{up}en/hanukkah/">{EN_LOGO}<span>{BRAND_LATIN}</span></a>'
            f'<p class="muted small mt-1">Printable Hanukkah activities and planners. Secure checkout with PayPal, instant download.</p></div>'
            f'<div><h2 class="footer-h">Hanukkah 2026</h2><ul><li><a href="{up}en/hanukkah/activity-pack/">Activity Pack</a></li>'
            f'<li><a href="{up}en/hanukkah/party-planner/">Party Planner</a></li><li><a href="{up}en/hanukkah/latke-calculator/">Latke &amp; doughnut calculator</a></li>'
            f'<li><a href="{up}en/hanukkah/when-is-hanukkah-2026/">When is Hanukkah 2026?</a></li><li><a href="{up}en/hanukkah/how-to-play-dreidel/">How to play dreidel</a></li></ul></div>'
            f'<div><h2 class="footer-h">Info</h2><ul><li><a href="{up}en/hanukkah/terms/">Terms &amp; refunds</a></li>'
            f'<li><a href="{up}legal/privacy/" hreflang="he">Privacy (Hebrew)</a></li><li><a href="{up}" hreflang="he">{BRAND} (Hebrew site)</a></li></ul></div>'
            f'</div><p class="fine">© 2026 {BRAND_LATIN}. Payments are processed by PayPal; we never see or store card details.</p></div></footer>')


def page(path, title, desc, body, jsonld=(), og_image=None, crumbs=(), lang="he", buy=False, scripts=(), alt=None,
         noindex=False, og_type=None):
    """path like 'p/x/' relative to docs. crumbs: [(name, path)]. alt: path of the other-language equivalent (hreflang)."""
    depth = path.strip("/").count("/") + 1 if path.strip("/") else 0
    up = "../" * depth
    url = BASE + path
    og = BASE + (og_image or "assets/og-default.png")
    home = ("ראשי", "") if lang == "he" else ("Hanukkah 2026", "en/hanukkah/")
    trail = [home] + [c for c in crumbs if c[1] != home[1]]
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(trail)]}
    lds = "\n".join(f'<script type="application/ld+json">\n{json.dumps(j, ensure_ascii=False)}\n</script>' for j in [*jsonld, bc])
    crumb = f'<nav class="breadcrumbs" aria-label="{"פירורי לחם" if lang == "he" else "Breadcrumbs"}">'
    for i, (n, p) in enumerate(trail):
        if i:
            crumb += '<span aria-hidden="true">›</span>'
        crumb += n if p == path else f'<a href="{up}{p}">{n}</a>'
    crumb += "</nav>"
    hreflang = ""
    if alt:
        he_url, en_url = (url, BASE + alt) if lang == "he" else (BASE + alt, url)
        hreflang = (f'<link rel="alternate" hreflang="he" href="{he_url}">\n<link rel="alternate" hreflang="en" href="{en_url}">\n'
                    f'<link rel="alternate" hreflang="x-default" href="{he_url if lang == "he" else en_url}">\n')
    js = [f'<script src="{up}assets/site.js"></script>']
    if buy:
        js.append(f'<script src="{up}assets/checkout.js"></script>')
    js += [s.replace("{up}", up) for s in scripts]
    if lang == "he":
        head_html, foot_html = '<header id="site-header"></header>', '<footer id="site-footer"></footer>'
    else:
        head_html, foot_html = en_header(up, alt), en_footer(up)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    html = f"""<!doctype html>
<html lang="{lang}" dir="{"rtl" if lang == "he" else "ltr"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{url}">
{hreflang}<meta property="og:type" content="{og_type or ('product' if buy else 'website')}">
<meta property="og:locale" content="{"he_IL" if lang == "he" else "en_US"}">
<meta property="og:site_name" content="{BRAND if lang == "he" else BRAND_LATIN}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e6b63">
<link rel="icon" type="image/svg+xml" href="{up}assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Noto+Sans+Hebrew:wght@400;700&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
<style>{EXTRA_CSS}</style>
{lds}
</head>
<body>
{head_html}
<main id="main">
{body.replace("{CRUMBS}", crumb).replace("{up}", up)}
</main>
{foot_html}
{chr(10).join(js)}
</body>
</html>
"""
    out = DOCS / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = fix_img_sizes(html, out.parent)
    out.write_text(html, encoding="utf-8")
    return out


def fix_img_sizes(html, page_dir):
    """Set width/height of local <img> tags from the real image files (avoids layout shift)."""
    from PIL import Image

    def rep(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if not src or src.group(1).startswith("http"):
            return tag
        f = (page_dir / src.group(1)).resolve()
        if not f.exists():
            raise FileNotFoundError(f"{f} (in {page_dir})")
        w, h = Image.open(f).size
        tag = re.sub(r'\swidth="\d+"', f' width="{w}"', tag)
        tag = re.sub(r'\sheight="\d+"', f' height="{h}"', tag)
        return tag
    return re.sub(r"<img\b[^>]*>", rep, html)


def faq_html(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}


def article_ld(title, desc, path, lang="he", image=None):
    org = BRAND if lang == "he" else BRAND_LATIN
    return {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
            "inLanguage": "he-IL" if lang == "he" else "en-US", "datePublished": UPDATED, "dateModified": UPDATED,
            "mainEntityOfPage": BASE + path, **({"image": BASE + image} if image else {}),
            "author": {"@type": "Organization", "name": org}, "publisher": {"@type": "Organization", "name": org}}


def product_ld(name, desc, path, price, images, currency="ILS", lang="he"):
    return {"@context": "https://schema.org", "@type": "Product", "name": name, "description": desc,
            "image": [BASE + i for i in images], "brand": {"@type": "Brand", "name": BRAND if lang == "he" else BRAND_LATIN},
            "offers": {"@type": "Offer", "price": str(price), "priceCurrency": currency, "availability": "https://schema.org/InStock",
                       "url": BASE + path}}


def app_ld(name, desc, path, lang="he", currency="ILS"):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "description": desc, "url": BASE + path,
            "applicationCategory": "LifestyleApplication", "operatingSystem": "Any", "inLanguage": "he-IL" if lang == "he" else "en-US",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": currency}}
