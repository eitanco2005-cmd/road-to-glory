"""Rendering for the wedding vendor price guides (docs/chatuna/mechirim/). Content lives in build_price_pages.py.

Every price row carries source ids; the page prints them as numbered references that jump to the dated source list.
The "fits your budget" box uses the same vendor lines as docs/tools/wedding-cost/calc.js (parsed from that file), so
the share-of-budget figures match what the calculator shows.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(DOCS, "chatuna", "mechirim")
SITE = "https://tichnun.netlify.app"
OG = f"{SITE}/assets/og/wedding-prices.png"
e = html.escape


# ---------------------------------------------------------------- calculator model (read from calc.js)
def calc_model():
    js = open(os.path.join(DOCS, "tools", "wedding-cost", "calc.js"), encoding="utf-8").read()
    lines = re.findall(r'\["(\w+)", "([^"]+)", (\d+), (\d+), (\d+), (true|false)\]', js)
    plate = dict(re.findall(r"(summer|winter): (\d+)", re.search(r"var PLATE = \{[^}]+\}", js).group(0)))
    kid = float(re.search(r"var KID = ([\d.]+)", js).group(1))
    return {
        "lines": {k: dict(label=l, lo=int(a), mid=int(b), hi=int(c), on=on == "true") for k, l, a, b, c, on in lines},
        "plate_summer": int(plate["summer"]), "kid": kid,
    }


def default_total(model):
    """The calculator's default scenario: 250 adults + 20 kids, center, summer, weekday, regular venue, mid tier, 7%."""
    food = model["plate_summer"] * (250 + 20 * model["kid"])
    vend = sum(L["mid"] for L in model["lines"].values() if L["on"])
    return (food + vend) * 1.07, food


# ---------------------------------------------------------------- helpers
def ils(v):
    if isinstance(v, str):
        return v
    return "₪" + f"{int(v):,}"


def strip(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def refs(ids, order):
    return "".join(f'<a class="ref" href="#src-{order.index(i) + 1}" aria-label="מקור {order.index(i) + 1}">[{order.index(i) + 1}]</a>' for i in ids)


def collect_sources(p):
    order = []
    for r in p["rows"]:
        for i in r.get("src", []):
            if i not in order:
                order.append(i)
    for i in p.get("extra_src", []):
        if i not in order:
            order.append(i)
    return order


def price_table(p, order):
    head = '<thead><tr><th>מה</th><th class="num">זול</th><th class="num">טיפוסי</th><th class="num">יקר</th><th>מקור</th></tr></thead>'
    body = []
    for r in p["rows"]:
        note = f'<span class="row-note">{r["note"]}</span>' if r.get("note") else ""
        body.append(f'<tr><td><strong>{r["label"]}</strong>{note}</td><td class="num">{ils(r["lo"])}</td>'
                    f'<td class="num"><strong>{ils(r["mid"])}</strong></td><td class="num">{ils(r["hi"])}</td>'
                    f'<td class="refs">{refs(r.get("src", []), order)}</td></tr>')
    return (f'<div class="table-wrap"><table class="price-table"><caption>{p["caption"]}</caption>{head}<tbody>\n'
            + "\n".join(body) + "\n</tbody></table></div>")


def budget_box(p, model, up):
    b = p.get("budget")
    if not b:
        return ""
    total, food = default_total(model)
    if b.get("line") == "food":
        share = round(food / total * 100)
        part = f"באותה חתונה המנות לבדן הן כ-{share}% מהעלות (כ-{ils(round(food, -3))})."
    else:
        L = model["lines"][b["line"]]
        share = L["mid"] / total * 100
        sh = f"{share:.0f}%" if share >= 1.5 else f"{share:.1f}%"
        part = (f'במחשבון, השורה "{e(L["label"])}" היא {ils(L["lo"])} ברמה חסכונית, {ils(L["mid"])} ברמה ממוצעת ו-{ils(L["hi"])} בפרימיום, '
                f"כלומר כ-{sh} מהעלות הכוללת" + ("" if L["on"] else " (השורה כבויה כברירת מחדל: מסמנים אותה אם צריך)") + ".")
    calc = f"{up}tools/wedding-cost/" + (b.get("preset") or "")
    return f"""
  <div class="cta-box budget-fit mt-3">
   <div>
    <h2 class="h3" style="font-size:1.2rem">איך זה משתלב בתקציב שלכם</h2>
    <p>חתונה טיפוסית במחשבון שלנו (250 מוזמנים, מרכז, קיץ, אמצע שבוע, ספקים ברמה ממוצעת) עולה כ-{ils(round(total, -3))}. {part} {b.get("text", "")}</p>
    <p class="small mb-0">קיבלתם הצעת מחיר? הקלידו אותה במחשבון במקום ההערכה. את כל ההצעות, המקדמות והתשלומים מנהלים ב<a href="{up}p/wedding-planner/">מתכנן החתונה</a> (₪49, או ב<a href="{up}chatuna/#bundle">חבילת החתונה</a> ₪79).</p>
   </div>
   <a class="btn accent" href="{calc}">{b.get("cta", "בדקו במחשבון עלות החתונה")}</a>
  </div>"""


def source_list(order, SOURCES):
    out = []
    for n, i in enumerate(order, 1):
        s = SOURCES[i]
        date = s["date"]
        out.append(f'<li id="src-{n}"><span class="num">[{n}]</span> <a href="{e(s["url"])}" rel="noopener" target="_blank">{s["title"]}</a> – {s["pub"]}. '
                   f'{date}. {s.get("note", "")}</li>')
    return "\n".join(out)


STYLE = """<style>
.price-table caption{caption-side:top;text-align:start;font-weight:700;padding-bottom:.4rem}
.price-table td,.price-table th{vertical-align:top}
.price-table .row-note{display:block;font-size:.85rem;color:var(--muted);font-weight:400}
.price-table .refs{white-space:nowrap}
a.ref{font-size:.8rem;text-decoration:none;margin-inline-end:.15rem}
.data-note{border-inline-start:4px solid var(--accent,#f0b44c)}
ol.src-list{padding-inline-start:0;list-style:none}
ol.src-list li{margin-bottom:.5rem}
.price-hub-grid{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));padding:0;list-style:none}
.price-hub-grid a{display:block;height:100%;padding:1rem;border:1px solid var(--border);border-radius:12px;text-decoration:none;background:var(--surface)}
.price-hub-grid strong{display:block;font-size:1.05rem}
.price-hub-grid span{color:var(--muted);font-size:.92rem}
@media (max-width:480px){.price-table .refs{white-space:normal}.price-table td,.price-table th{padding:.45rem .35rem;font-size:.9rem}}
</style>"""


def head(title, desc, url, ld, up, og_type="article"):
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="תכנון פלוס">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG}">
<meta name="theme-color" content="#0e6b63">
<link rel="icon" type="image/svg+xml" href="{up}assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<header id="site-header"></header>
<main id="main">
{STYLE}"""


def foot(up):
    return f"""</main>
<footer id="site-footer"></footer>
<script src="{up}assets/site.js"></script>
<script src="{up}assets/share.js"></script>
</body>
</html>
"""


def share_box(msg):
    return (f'<div data-share data-share-scope="#price-summary" data-share-msg="{e(msg)}" '
            'data-share-note="שלחו לבן/בת הזוג או להורים לפני הפגישה עם הספק."></div>')


def article_ld(url, headline, desc, date, crumbs, faq):
    g = [
        {"@type": "Article", "headline": headline, "description": desc, "inLanguage": "he-IL",
         "datePublished": date, "dateModified": date, "mainEntityOfPage": url, "image": OG,
         "author": {"@type": "Organization", "name": "תכנון פלוס", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "name": "תכנון פלוס", "url": SITE + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": n, "name": name, "item": item} for n, (name, item) in enumerate(crumbs, 1)]},
    ]
    if faq:
        g.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]})
    return {"@context": "https://schema.org", "@graph": g}


def faq_html(faq):
    return "\n".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in faq)


def render_page(p, pages, SOURCES, model, date, updated_label):
    up = "../../../"
    url = f"{SITE}/chatuna/mechirim/{p['slug']}/"
    order = collect_sources(p)
    crumbs = [("דף הבית", SITE + "/"), ("הכל לחתונה", SITE + "/chatuna/"), ("מחירי ספקים לחתונה", SITE + "/chatuna/mechirim/"), (p["crumb"], url)]
    ld = article_ld(url, strip(p["h1"]), p["desc"], date, crumbs, p["faq"])
    ul = lambda items: "<ul>\n" + "\n".join(f"<li>{x}</li>" for x in items) + "\n</ul>"
    ol = lambda items: "<ol>\n" + "\n".join(f"<li>{x}</li>" for x in items) + "\n</ol>"
    thin = f'<div class="callout data-note mt-2"><strong>כמה הנתונים חזקים:</strong> {p["thin"]}</div>' if p.get("thin") else ""
    others = "\n".join(f'<li><a href="../{o["slug"]}/">{o["menu"]}</a></li>' for o in pages if o["slug"] != p["slug"])
    related = "\n".join(f'<li><a href="{up}{u}">{t}</a></li>' for u, t in p.get("related", []))
    return head(p["title"], p["desc"], url, ld, up) + f"""
<section class="hero">
 <div class="container narrow">
  <nav class="breadcrumbs" aria-label="פירורי לחם"><a href="{up}">דף הבית</a> <span aria-hidden="true">›</span> <a href="../../">הכל לחתונה</a> <span aria-hidden="true">›</span> <a href="../">מחירי ספקים</a> <span aria-hidden="true">›</span> <span aria-current="page">{e(p['crumb'])}</span></nav>
  <span class="eyebrow">מחירון עם מקורות · {updated_label}</span>
  <h1>{p['h1']}</h1>
  <p class="lead">{p['lead']}</p>
 </div>
</section>

<section class="section" style="padding-top:0">
 <div class="container narrow prose" id="price-summary">
  <h2>{p['table_h']}</h2>
  {p.get('table_intro', '')}
  {price_table(p, order)}
  <p class="small muted">{p.get('table_note', 'טווחים מעוגלים, כולל מע"מ אלא אם צוין אחרת. "טיפוסי" הוא אמצע הטווח שהמקורות מדווחים, לא ממוצע סטטיסטי. המספרים בסוגריים מפנים לרשימת המקורות בתחתית העמוד.')}</p>
  {thin}
  {share_box(p['share_msg'])}

  <h2>מה קובע את המחיר</h2>
  {ol(p['drivers'])}
  {p.get('extra', '')}
  <h2>שאלות לשאול את הספק לפני שסוגרים</h2>
  {ul(p['ask'])}
  <h2>איך לחסוך בלי להתחרט</h2>
  {ul(p['save'])}
{budget_box(p, model, up)}
 </div>
</section>

<section class="section alt">
 <div class="container narrow">
  <h2>שאלות נפוצות</h2>
  <div class="faq">
{faq_html(p['faq'])}
  </div>
 </div>
</section>

<section class="section">
 <div class="container narrow prose">
  <h2>מחירים של ספקים נוספים</h2>
  <ul>
{others}
  </ul>
  <p>כל הספקים בטבלה אחת: <a href="../">מחירון ספקים לחתונה 2026</a> · <a href="{up}tools/wedding-cost/">מחשבון עלות חתונה</a> · <a href="../../">הכל לחתונה</a></p>
  {('<h2>מדריכים קשורים</h2><ul>' + related + '</ul>') if related else ''}
  <h2>מקורות</h2>
  <ol class="source src-list">
{source_list(order, SOURCES)}
  </ol>
  <p class="small muted">נבדק {updated_label.replace('עודכן ', '')}. המחירים הם מחירונים, כתבות ונתוני אתרי השוואה, לא מחירון רשמי, והם משתנים לפי ספק, תאריך ואזור. הצעת מחיר כתובה מהספק גוברת על כל טבלה. מצאתם מחיר שנראה לכם לא מעודכן? זה קורה, ונשמח לתקן.</p>
 </div>
</section>

""" + foot(up)
