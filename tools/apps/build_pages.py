#!/usr/bin/env python3
"""Build the Stream B product pages and guides (static HTML) for the web apps.

    python3 tools/apps/build_pages.py

Writes docs/p/seating-chart/index.html, docs/p/cv-builder/index.html and two guides under each
docs/p/<slug>/guides/<guide>/index.html. Screenshots come from tools/apps/screenshots.js.
"""
import html
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
sys.path.insert(0, str(REPO / "tools" / "site"))
from site_config import BASE_URL, BRAND  # noqa: E402

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731


def head(title, desc, path, depth, image, ld, og_type="website"):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | {BRAND}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{BASE_URL}{path}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)} | {BRAND}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:image" content="{BASE_URL}{image}">
<meta name="twitter:card" content="summary_large_image">
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
"""


def foot(depth, checkout=False, extra=""):
    up = "../" * depth
    return (f"""
</main>
<footer id="site-footer"></footer>
<script src="{up}assets/site.js"></script>
""" + (f'<script src="{up}assets/checkout.js"></script>\n' if checkout else "") + extra + "</body>\n</html>\n")


def crumbs(items):
    out = []
    for i, (label, href) in enumerate(items):
        if href:
            out.append(f'<a href="{href}">{E(label)}</a>')
        else:
            out.append(f'<span aria-current="page">{E(label)}</span>')
    return '<nav class="breadcrumbs" aria-label="פירורי לחם">' + ' <span aria-hidden="true">›</span> '.join(out) + "</nav>"


def breadcrumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE_URL + u} for i, (n, u) in enumerate(items)]}


def faq_ld(faq):
    import re
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}


ICON = {
    "drag": '<path d="M5 9l-3 3 3 3M9 5l3-3 3 3M15 19l-3 3-3-3M19 9l3 3-3 3M2 12h20M12 2v20"/>',
    "auto": '<path d="M12 3l1.9 4.6L18.5 9l-4.6 1.9L12 15.5l-1.9-4.6L5.5 9l4.6-1.4z"/><path d="M19 14l.8 2 2.2.8-2.2.8L19 20l-.8-2.4L16 17l2.2-.8z"/>',
    "warn": '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0zM12 9v4M12 17h.01"/>',
    "import": '<path d="M12 3v12M7 10l5 5 5-5"/><path d="M5 21h14"/>',
    "print": '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "table": '<circle cx="12" cy="12" r="5"/><circle cx="12" cy="3" r="1.5"/><circle cx="12" cy="21" r="1.5"/><circle cx="3" cy="12" r="1.5"/><circle cx="21" cy="12" r="1.5"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8"/>',
    "lang": '<path d="M5 8l6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    "check": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
}


def feature(icon, title, text):
    return (f'<div class="feature"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[icon]}</svg></div><div><h3>{E(title)}</h3><p>{text}</p></div></div>')


def screens(slug, items):
    out = []
    for i, (cap, w, h) in enumerate(items, 1):
        out.append(f'<figure><a href="img/screen-{i}.webp" target="_blank" rel="noopener"><img src="img/screen-{i}.webp" alt="{E(cap)}" '
                   f'loading="lazy" width="{w}" height="{h}"></a><figcaption>{E(cap)}</figcaption></figure>')
    return "\n".join(out)


def compare_table(rows):
    body = "".join(f"<tr><td>{E(a)}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return ('<div class="table-wrap"><table><thead><tr><th scope="col">מה</th><th scope="col">חינם</th><th scope="col">גרסה מלאה</th></tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


Y, N = '<span aria-label="כן">✓</span>', '<span class="muted" aria-label="לא">—</span>'


def product_page(p):
    slug, path = p["slug"], f"p/{p['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": p["name"], "description": p["desc"], "sku": slug, "brand": {"@type": "Brand", "name": BRAND},
         "category": "כלי אונליין", "image": [f"{BASE_URL}{path}img/screen-{i}.png" for i in range(1, len(p["screens"]) + 1)],
         "offers": {"@type": "Offer", "price": str(p["price"]), "priceCurrency": "ILS", "availability": "https://schema.org/InStock",
                    "url": BASE_URL + path, "priceValidUntil": "2027-12-31"}},
        {"@type": "SoftwareApplication", "name": p["app_name"], "applicationCategory": p["app_cat"], "operatingSystem": "Web",
         "url": BASE_URL + p["app"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ILS"}},
        breadcrumb_ld([("דף הבית", ""), ("מוצרים", "products/"), (p["short"], path)]),
        faq_ld(p["faq"])]}
    h = head(p["title"], p["desc"], path, 2, f"{path}img/screen-1.png", ld, "product")
    h += f"""
<section class="hero">
 <div class="container">
  {crumbs([("דף הבית", "../../"), ("מוצרים", "../../products/"), (p["short"], None)])}
  <div class="split">
   <div>
    <h1>{p["h1"]}</h1>
    <p class="lead">{p["lead"]}</p>
    <p class="btn-row mt-2"><a class="btn accent" href="../../{p["app"]}">{E(p["cta"])}</a><a class="btn secondary" href="#free-vs-full">מה חינם ומה בתשלום?</a></p>
    <ul class="hero-points">{"".join(f"<li>{E(x)}</li>" for x in p["points"])}</ul>
   </div>
   <div>
    <div id="buy" class="buy" data-product="{slug}" data-label="{E(p["buy_label"])}"></div>
    <p class="small muted mt-1">{p["buy_note"]}</p>
   </div>
  </div>
 </div>
</section>

<section class="section alt" id="screens">
 <div class="container">
  <div class="section-head"><h2>ככה זה נראה</h2><p class="muted">צילומי מסך מהכלי עצמו, עם נתוני דוגמה בדויים.</p></div>
  <div class="screens">
{screens(slug, p["screens"])}
  </div>
 </div>
</section>

<section class="section">
 <div class="container">
  <div class="section-head"><h2>מה אפשר לעשות</h2></div>
  <div class="grid cols-2">
{"".join(feature(*f) for f in p["features"])}
  </div>
 </div>
</section>

<section class="section alt" id="free-vs-full">
 <div class="container narrow">
  <h2>חינם מול גרסה מלאה</h2>
  {compare_table(p["compare"])}
  <p class="small muted mt-2">{p["honest"]}</p>
 </div>
</section>

<section class="section">
 <div class="container">
  <div class="section-head"><h2>איך זה עובד</h2></div>
  <ol class="steps">{"".join(f"<li><h3>{E(a)}</h3><p>{b}</p></li>" for a, b in p["steps"])}</ol>
 </div>
</section>

<section class="section alt">
 <div class="container narrow">
  <h2>שאלות נפוצות</h2>
  <div class="faq">
{"".join(f"<details><summary>{E(q)}</summary><p>{a}</p></details>" for q, a in p["faq"])}
  </div>
 </div>
</section>

<section class="section">
 <div class="container narrow">
  {p["related"]}
 </div>
</section>

<div class="buy-bar"><span><strong>{E(p["short"])}</strong> · <span class="price">₪{p["price"]}</span></span><a class="btn small" href="../../{p["app"]}">לכלי</a></div>
"""
    h += foot(2, checkout=True)
    out = DOCS / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(h, encoding="utf-8")
    print("wrote", out.relative_to(REPO))


def guide_page(g):
    path = f"p/{g['slug']}/guides/{g['id']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": g["h1"], "description": g["desc"], "inLanguage": "he", "datePublished": "2026-11-17", "dateModified": "2026-11-17",
         "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND},
         "image": f"{BASE_URL}p/{g['slug']}/img/screen-1.png", "mainEntityOfPage": BASE_URL + path},
        breadcrumb_ld([("דף הבית", ""), (g["product_short"], f"p/{g['slug']}/"), (g["crumb"], path)])]
        + ([faq_ld(g["faq"])] if g.get("faq") else [])}
    h = head(g["title"], g["desc"], path, 4, f"p/{g['slug']}/img/screen-1.png", ld, "article")
    faq = ""
    if g.get("faq"):
        faq = '<h2>שאלות נפוצות</h2><div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{a}</p></details>" for q, a in g["faq"]) + "</div>"
    h += f"""
<section class="section">
 <div class="container narrow">
  {crumbs([("דף הבית", "../../../../"), (g["product_short"], "../../"), ("מדריכים", None), (g["crumb"], None)])}
  <article class="prose">
   <h1>{E(g["h1"])}</h1>
   <p class="updated">עודכן: נובמבר 2026 · זמן קריאה: כ-{g["minutes"]} דקות</p>
{g["body"]}
{faq}
  </article>
  <div class="cta-box mt-4">
   <div><h2 style="font-size:1.2rem">{E(g["cta_title"])}</h2><p>{g["cta_text"]}</p></div>
   <a class="btn accent" href="../../../../{g["app"]}">{E(g["cta_btn"])}</a>
  </div>
  <p class="small muted mt-3">עוד: {g["more"]}</p>
 </div>
</section>
"""
    h += foot(4, extra=g.get("script", ""))
    out = DOCS / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(h, encoding="utf-8")
    print("wrote", out.relative_to(REPO))


# ---------------------------------------------------------------- seating
SEATING = {
    "slug": "seating-chart", "short": "סידורי הושבה", "price": 29, "app": "apps/seating/", "app_cat": "LifestyleApplication",
    "name": "סידורי הושבה אונליין – גרסה מלאה", "app_name": "סידורי הושבה – תכנון פלוס",
    "title": "תוכנה לסידורי הושבה לחתונה – אונליין, בעברית, בלי הרשמה",
    "desc": "כלי אונליין לסידורי הושבה לחתונה, בר מצווה ואירועים: ייבוא מוזמנים מאקסל, שולחנות עגולים ומלבניים, גרירה, הושבה אוטומטית לפי צד וקבוצה והתראה על מי שלא יושב יחד. חינם לשימוש; PDF נקי, אקסל וכרטיסי שולחן ב-₪29.",
    "h1": 'סידורי הושבה לחתונה: <span class="hl">גוררים, מושיבים, מדפיסים</span>',
    "lead": "כלי אונליין בעברית שמסדר את ההושבה בשבילכם: מדביקים את רשימת המוזמנים, מוסיפים שולחנות, ולוחצים \"הושבה אוטומטית\". אחר כך מתקנים בגרירה. בלי הרשמה ובלי להוריד כלום.",
    "cta": "פתחו את הכלי – חינם",
    "points": ["חינם לשימוש מלא במסך", "ייבוא מאקסל / CSV", "עובד בטלפון", "הנתונים נשארים אצלכם"],
    "buy_label": "גרסה מלאה: PDF נקי + אקסל + כרטיסי שולחן",
    "buy_note": "אפשר לשלם גם מתוך הכלי, ברגע שתרצו לייצא. אחרי התשלום הייצוא נפתח מיד, בלי הרשמה.",
    "screens": [("מסך הכלי: מוזמנים בלי שולחן מימין, שולחנות עם תפוסה ומקומות פנויים", 1280, 860),
                ("עריכת מוזמן: שולחן, צד, קבוצה ו\"לא להושיב יחד\" – והתנגשות מסומנת באדום", 1280, 860),
                ("הדפסה / PDF: מפת שולחנות ורשימת כניסה לפי א-ב", 820, 1100),
                ("כרטיסי שולחן להדפסה (בגרסה המלאה)", 820, 1100),
                ("בטלפון: לשוניות מוזמנים / שולחנות, גרירה בלחיצה ארוכה", 390, 844)],
    "features": [
        ("import", "ייבוא רשימה בשניות", "הדבקה מאקסל או מ-Google Sheets, או ייבוא קובץ CSV / XLSX. שורה לכל הזמנה, עם מספר אנשים, צד וקבוצה."),
        ("table", "שולחנות עגולים ומלבניים", "כל שולחן עם מספר מקומות משלו, ציור של המקומות התפוסים ושם חופשי (שולחן אבירים, משפחה, ילדים)."),
        ("drag", "גרירה ושחרור", "גוררים הזמנה לשולחן, או לוחצים עליה ובוחרים שולחן. בטלפון: לחיצה ארוכה ואז גרירה."),
        ("auto", "הושבה אוטומטית", "מושיבה קבוצות יחד (חברים מהצבא, עבודה, משפחה), שומרת על צד ועל המקום בשולחן, ומשאירה לכם רק תיקונים."),
        ("warn", "התנגשויות וחריגות", "סימון \"לא להושיב יחד\" בין שתי הזמנות, והתראה באדום על שולחן בחריגה או על בקשה שהופרה."),
        ("print", "הדפסה, PDF ואקסל", "מפת שולחנות ורשימת כניסה לפי א-ב לדלפק הקבלה, קובץ אקסל לאולם, וכרטיסי שולחן גדולים."),
    ],
    "compare": [("שימוש מלא במסך: מוזמנים, שולחנות, גרירה", Y, Y), ("הושבה אוטומטית והתנגשויות", Y, Y), ("ייבוא מאקסל / CSV וגיבוי", Y, Y),
                ("הדפסה / PDF", "עם סימן מים", "נקי"), ("ייצוא לאקסל (לאולם ולמארחות)", N, Y), ("כרטיסי שולחן להדפסה", N, Y),
                ("מחיר", "₪0", "₪29 חד-פעמי")],
    "honest": "כנות: הכלי רץ כולו בדפדפן שלכם, ולכן הנעילה של הייצוא היא פשוטה ולא \"מוגנת\". אם הכלי חסך לכם ערב של אקסל, הגרסה המלאה היא הדרך לתמוך בו.",
    "steps": [("מוסיפים מוזמנים ושולחנות", "מדביקים רשימה או מייבאים קובץ, ובוחרים כמה שולחנות ומקומות."),
              ("מושיבים", "\"הושבה אוטומטית\" ואז תיקונים בגרירה. הכל נשמר בדפדפן אוטומטית."),
              ("מדפיסים ושולחים לאולם", "PDF עם סימן מים בחינם, או PDF נקי, אקסל וכרטיסי שולחן בגרסה המלאה.")],
    "faq": [
        ("זה באמת חינם?", "כן. כל הכלי עובד בחינם במסך, בלי הגבלת מוזמנים או שולחנות, כולל הדפסה / PDF עם סימן מים. משלמים ₪29 פעם אחת רק אם רוצים PDF נקי, אקסל וכרטיסי שולחן."),
        ("איפה נשמרים הנתונים? מישהו רואה את רשימת המוזמנים?", "הרשימה נשמרת רק בדפדפן במכשיר שלכם (localStorage) ולא נשלחת אלינו. כדי לעבור למחשב אחר או לשמור עותק, בתפריט ⋯ יש \"שמירת גיבוי\" ו\"שחזור מגיבוי\"."),
        ("אפשר לעבוד מהטלפון?", "כן. בטלפון יש לשונית מוזמנים ולשונית שולחנות. גוררים בלחיצה ארוכה, או לוחצים על שם ובוחרים שולחן מהרשימה."),
        ("מה קורה אחרי התשלום?", "הייצוא הנקי נפתח מיד בדפדפן שבו שילמתם, בלי הרשמה ובלי מעבר לדף אחר. מקבלים גם קישור לדף אישור הזמנה: פתיחה שלו בדפדפן אחר פותחת שם את הגרסה המלאה."),
        ("איך מייבאים מאקסל?", "שומרים את רשימת המוזמנים כקובץ XLSX או CSV, או פשוט מעתיקים את העמודות ומדביקים. הכלי מזהה כותרות כמו שם, כמות, צד, קבוצה ושולחן."),
        ("זה מתאים גם לבר מצווה או לאירוע חברה?", "כן. הצדדים והקבוצות הם טקסט חופשי: אפשר לכתוב \"משפחת אבא\", \"כיתה\", \"מחלקת מכירות\" וכל מה שמתאים."),
        ("אפשר לקבל החזר?", 'זה מוצר דיגיטלי שנפתח מיד, ולכן כדאי לנסות את כל הכלי בחינם לפני הרכישה. פרטים ב<a href="../../legal/refund/">מדיניות הביטולים</a>. אם משהו לא עובד – כתבו לנו ונתקן.'),
    ],
    "related": """<div class="cta-box">
   <div><h2 style="font-size:1.25rem">מתכננים את כל החתונה?</h2>
   <p><a href="../wedding-planner/">מתכנן החתונה באקסל</a> (₪49) מחבר תקציב, ספקים, תשלומים, אישורי הגעה ורישום צ'קים, ואת רשימת המוזמנים שלו אפשר להדביק ישר לכלי ההושבה. להזמנה עצמה: <a href="../invitation-maker/">מעצב ההזמנות</a>.</p></div>
   <a class="btn" href="../wedding-planner/">למתכנן החתונה</a>
  </div>
  <h2 class="mt-4" style="font-size:1.3rem">מדריכים</h2>
  <ul>
   <li><a href="../invitation-maker/">מעצב הזמנות לחתונה ולבר מצווה אונליין</a> – הזמנה מעוצבת לשליחה בוואטסאפ ולהדפסה</li>
   <li><a href="guides/how-to-seat-guests/">סידורי הושבה לחתונה: איך עושים את זה נכון, שלב אחר שלב</a></li>
   <li><a href="guides/tables-and-seats/">כמה שולחנות צריך? מחשבון וכללי אצבע לשולחן עגול ומלבני</a></li>
   <li><a href="../wedding-planner/guides/rsvp-seating-gifts/">אישורי הגעה, הושבה ורישום צ'קים – שיטה מסודרת</a></li>
   <li><a href="../../tools/wedding-gift/">מחשבון: כמה לשים בחתונה 2026</a></li>
  </ul>""",
}

CV = {
    "slug": "cv-builder", "short": "בונה קורות חיים", "price": 19, "app": "apps/cv/", "app_cat": "BusinessApplication",
    "name": "בונה קורות חיים בעברית – גרסה מלאה", "app_name": "בונה קורות חיים – תכנון פלוס",
    "title": "בניית קורות חיים בעברית ובאנגלית – 4 תבניות, מתאים ל-ATS",
    "desc": "בונה קורות חיים אונליין בעברית ובאנגלית: טופס פשוט, תצוגה חיה ו-4 תבניות נקיות שמערכות סינון (ATS) קוראות, כולל שירות צבאי. חינם לשימוש; PDF נקי ו-Word ב-₪19.",
    "h1": 'קורות חיים בעברית ובאנגלית: <span class="hl">ממלאים, רואים, מורידים</span>',
    "lead": "ממלאים טופס פשוט ורואים את קורות החיים נבנים בזמן אמת, בעמוד A4 אמיתי. 4 תבניות נקיות, עברית מימין לשמאל ואנגלית משמאל לימין, בלי הרשמה.",
    "cta": "פתחו את הכלי – חינם",
    "points": ["PDF בעברית שיוצא נכון: מימין לשמאל, בלי סימני פיסוק הפוכים", "4 תבניות נקיות", "עברית + אנגלית", "מתאים למערכות סינון (ATS)"],
    "buy_label": "גרסה מלאה: PDF נקי + Word",
    "buy_note": "אפשר לשלם גם מתוך הכלי, כשקורות החיים מוכנים. אחרי התשלום ההורדה הנקייה נפתחת מיד.",
    "screens": [("הכלי: טופס מצד אחד, קורות החיים מתעדכנים בזמן אמת מהצד השני", 1280, 860),
                ("4 התבניות: קלאסי, מודרני, מינימלי ובכיר", 1640, 680),
                ("גרסה באנגלית, משמאל לימין, בתבנית מודרני", 535, 756),
                ("בטלפון: לשוניות עריכה ותצוגה", 390, 844)],
    "features": [
        ("eye", "תצוגה חיה בעמוד A4", "כל שינוי בטופס מופיע מיד בעמוד, כולל קו שמראה איפה נגמר העמוד הראשון."),
        ("doc", "4 תבניות נקיות", "קלאסי, מודרני, מינימלי ובכיר, עם 5 צבעי הדגשה. כולן בטור אחד וכותרות רגילות: מה שמערכות סינון קוראות הכי טוב."),
        ("lang", "עברית ואנגלית", "שתי גרסאות נפרדות של אותם קורות חיים. אפשר להעתיק את העברית כבסיס ולתרגם שדה-שדה."),
        ("check", "מבנה ישראלי", "מדור שירות צבאי / לאומי, תמצית מקצועית, שפות ומדורים חופשיים (התנדבות, קורסים, פרסומים)."),
        ("shield", "פרטיות", "מה שאתם כותבים נשמר רק בדפדפן שלכם. לא נשלח אלינו ולא לאף אחד."),
        ("print", "PDF ו-Word", "PDF עם טקסט אמיתי (לא תמונה), וקובץ Word למשרות שמבקשות DOCX או למי שרוצה להמשיך לערוך."),
    ],
    "compare": [("טופס מלא ו-4 תבניות", Y, Y), ("עברית + אנגלית", Y, Y), ("תצוגה חיה וגיבוי", Y, Y),
                ("PDF", "עם סימן מים", "נקי"), ("קובץ Word (DOCX)", N, Y), ("מחיר", "₪0", "₪19 חד-פעמי")],
    "honest": "כנות: הכלי רץ כולו בדפדפן, ולכן הנעילה פשוטה ולא \"מוגנת\". גרסת ה-PDF החינמית כוללת סימן מים, שגם נקרא כטקסט על ידי מערכות סינון – לשליחה למשרות כדאי PDF נקי.",
    "steps": [("ממלאים", "פרטים, תמצית, ניסיון, צבא, השכלה וכישורים. אפשר להתחיל מדוגמה."),
              ("בוחרים עיצוב ושפה", "4 תבניות, 5 צבעים, ועברית או אנגלית בלחיצה."),
              ("מורידים", "PDF עם סימן מים בחינם, או PDF נקי + Word בגרסה המלאה.")],
    "faq": [
        ("למה לא פשוט Word או ממיר PDF חינמי?", "בעברית הרבה כלים מייצרים PDF עם מספרים, תאריכים וסוגריים במקום הלא נכון, או טקסט שנשמר כתמונה. כאן העמוד נבנה מראש מימין לשמאל, תאריכים ומילים באנגלית (Excel, B.A.) מסודרים נכון, וה-PDF שומר על טקסט אמיתי שאפשר לסמן ולחפש."),
        ("קורות החיים יעברו מערכות סינון (ATS)?", "התבניות בנויות כדי לעזור לזה: טור אחד, כותרות רגילות (ניסיון תעסוקתי, השכלה…), טקסט אמיתי ולא תמונה, בלי טבלאות ובלי תיבות טקסט. אף אחד לא יכול להבטיח מעבר סינון: הכי חשוב שהתוכן יכלול את המילים מתוך מודעת המשרה."),
        ("איך יוצא ה-PDF?", "לוחצים \"הורדה\" ובוחרים PDF: נפתח חלון ההדפסה של הדפדפן, ושם בוחרים \"שמירה כ-PDF\". כך הטקסט נשאר טקסט אמיתי וחד. בטלפון זה עובד דרך תפריט השיתוף / ההדפסה."),
        ("אפשר להוסיף תמונה?", "לא, ובכוונה: רוב המגייסים בישראל לא מצפים לתמונה, ומערכות סינון לא קוראות אותה. אותו דבר לגבי תעודת זהות, מצב משפחתי וכתובת מלאה."),
        ("איך כותבים שירות צבאי?", 'יש מדור נפרד. כתבו תפקיד ויחידה במילים שאדם מבחוץ מבין, ומה עשיתם במספרים. יש על זה פרק ב<a href="guides/how-to-write-cv/">מדריך לכתיבת קורות חיים</a>.'),
        ("איפה נשמר מה שכתבתי?", "רק בדפדפן במכשיר שלכם. כדי לעבור מחשב, השתמשו ב\"שמירת גיבוי\" בתפריט ⋯ ואז \"שחזור מגיבוי\" במחשב השני."),
        ("מה קורה אחרי התשלום?", "ה-PDF הנקי וה-Word נפתחים מיד בדפדפן שבו שילמתם, לכל הגרסאות שתייצאו בו. מקבלים גם קישור לדף אישור: פתיחה שלו בדפדפן אחר פותחת שם את הגרסה המלאה."),
        ("אפשר לקבל החזר?", 'זה מוצר דיגיטלי שנפתח מיד, ולכן כדאי לנסות את הכלי בחינם לפני הרכישה. פרטים ב<a href="../../legal/refund/">מדיניות הביטולים</a>. אם משהו לא עובד – כתבו לנו ונתקן.'),
    ],
    "related": """<h2 style="font-size:1.3rem">מדריכים</h2>
  <ul>
   <li><a href="guides/how-to-write-cv/">איך כותבים קורות חיים בעברית: מבנה, דוגמאות וטעויות נפוצות</a></li>
   <li><a href="guides/cv-in-english/">קורות חיים באנגלית לישראלים + איך לעבור מערכות ATS</a></li>
  </ul>
  <div class="cta-box mt-3">
   <div><h2 style="font-size:1.2rem">עובדים כעצמאים?</h2><p><a href="../price-quote-pack/">ערכת תבניות הצעת מחיר</a> ו<a href="../osek-patur-tracker/">מעקב עוסק פטור</a> לצד הפרילנס.</p></div>
   <a class="btn secondary" href="../../products/">לכל המוצרים</a>
  </div>""",
}

# ---------------------------------------------------------------- guides
G_SEAT_1 = {
    "slug": "seating-chart", "id": "how-to-seat-guests", "product_short": "סידורי הושבה", "crumb": "איך עושים סידורי הושבה", "app": "apps/seating/",
    "title": "סידורי הושבה לחתונה: איך עושים את זה נכון, שלב אחר שלב",
    "desc": "מדריך מעשי לסידורי הושבה לחתונה ולאירועים: מתי מתחילים, איך מחלקים לפי קבוצות, שולחנות מיוחדים, מי לא יושב ליד מי, שינויים של הרגע האחרון ורשימת כניסה לקבלה.",
    "h1": "סידורי הושבה לחתונה: איך עושים את זה נכון, שלב אחר שלב", "minutes": 6,
    "body": """<p class="lead">סידורי הושבה נשמעים כמו משימה של ערב אחד, ובפועל הם נמשכים שבועות: אישורי הגעה משתנים, מישהו מבקש לשבת עם החברים, ומישהו אחר בדיוק לא. הנה שיטה שעובדת.</p>

<h2>1. מתי מתחילים</h2>
<p>את השלד (אילו קבוצות יושבות יחד וכמה שולחנות צריך) אפשר לבנות כבר כשרשימת המוזמנים סגורה. את ההושבה הסופית עושים אחרי סבב אישורי ההגעה האחרון, בדרך כלל <strong>7–10 ימים לפני האירוע</strong>, וזה גם המועד שבו הרבה אולמות מבקשים את מספר המנות ואת מפת השולחנות. בדקו מה כתוב אצלכם בחוזה.</p>

<h2>2. רשימה אחת, שורה לכל הזמנה</h2>
<p>עובדים עם שורה לכל <strong>הזמנה</strong> (משפחה, זוג או יחיד), עם מספר האנשים שמגיעים בפועל. לכל שורה מוסיפים:</p>
<ul>
 <li><strong>צד</strong> – כלה / חתן / משותף (בבר מצווה: אמא / אבא).</li>
 <li><strong>קבוצה</strong> – משפחה קרובה, משפחה מורחבת, חברים מהצבא, עבודה, שכנים. הקבוצות הן כמעט השולחנות עצמם.</li>
</ul>
<p>טיפ: אם הרשימה כבר באקסל או ב-Google Sheets, אפשר להעתיק את העמודות ולהדביק אותן ישירות ל<a href="../../../../apps/seating/">כלי סידורי ההושבה</a>.</p>

<h2>3. כמה שולחנות ואיזה</h2>
<p>מחלקים את מספר המאשרים במספר המקומות בשולחן ומוסיפים שולחן אחד רזרבי. איך מחשבים בדיוק ומה ההבדל בין עגול למלבני – ב<a href="../tables-and-seats/">מדריך כמה שולחנות צריך</a>.</p>

<h2>4. קודם השולחנות המיוחדים</h2>
<ol>
 <li><strong>משפחה קרובה</strong> – קרוב לרחבה ולחופה. הורים, אחים וסבים.</li>
 <li><strong>מבוגרים</strong> – רחוק מהרמקולים, קרוב לשירותים וליציאה, עם גישה נוחה לכיסא גלגלים.</li>
 <li><strong>שולחן אבירים / צעירים</strong> – החברים הקרובים ליד הרחבה.</li>
 <li><strong>ילדים</strong> – אם יש: שולחן נפרד ליד ההורים, או ילדים עם ההורים.</li>
</ol>

<h2>5. אחר כך קבוצה-קבוצה</h2>
<p>עוברים על כל קבוצה ומנסים להושיב אותה בשולחן אחד. קבוצה גדולה מדי? מפצלים לשני שולחנות סמוכים לפי היכרות (למשל &quot;צוות&quot; ו&quot;הנהלה&quot;). קבוצה קטנה? מצרפים אותה לקבוצה מאותו צד עם מכנה משותף. מי שמגיע לבד – ליד מישהו שהוא מכיר.</p>
<p>ב<a href="../../../../apps/seating/">כלי ההושבה</a> כפתור &quot;הושבה אוטומטית&quot; עושה בדיוק את זה: מושיב קבוצות יחד לפי צד, ומפצל רק כשאין ברירה. אחר כך מתקנים בגרירה.</p>

<h2>6. מי לא יושב ליד מי</h2>
<p>הורים גרושים, בני דודים מסוכסכים, אקס שהוזמן בכל זאת. כתבו את זה <strong>מראש</strong> ולא מהזיכרון. בכלי שלנו מסמנים &quot;לא להושיב באותו שולחן עם&quot;, וכל שולחן שמפר את הבקשה נצבע באדום. חשוב לא פחות: לא להושיב אותם בשולחנות צמודים שגב אל גב.</p>

<h2>7. ביטולים ותוספות של הרגע האחרון</h2>
<ul>
 <li>השאירו <strong>שולחן אחד גמיש</strong> או 1–2 מקומות פנויים בכמה שולחנות.</li>
 <li>ביטול? אל תשאירו שולחן עם 4 אנשים: אחדו שני שולחנות חלקיים.</li>
 <li>עדכנו את האולם בכל שינוי שמשנה את מספר המנות.</li>
</ul>

<h2>8. מה מעבירים לאולם ולקבלה</h2>
<ul>
 <li><strong>מפת שולחנות</strong> – מי יושב בכל שולחן, לאולם ולמנהלת האירוע.</li>
 <li><strong>רשימת כניסה לפי א-ב</strong> – שם ← מספר שולחן, לדלפק הקבלה. זה מה שחוסך תור בכניסה.</li>
 <li><strong>כרטיסי שולחן</strong> – מספר גדול על כל שולחן.</li>
</ul>
<p>את שלושתם מפיקים מהכלי: הדפסה / PDF בחינם (עם סימן מים), או PDF נקי, אקסל וכרטיסי שולחן בגרסה המלאה.</p>

<h2>טעויות נפוצות</h2>
<ul>
 <li>להושיב לפי מי &quot;צריך&quot; לשבת קרוב, ולא לפי מי יהנה יחד.</li>
 <li>לשכוח את הצלם, הזמר או המלווים – גם הם צריכים מקום (ולפעמים מנה).</li>
 <li>לעבוד על כמה עותקים של הרשימה במקביל. רשימה אחת, אדם אחד שאחראי עליה.</li>
</ul>""",
    "faq": [("מתי שולחים לאולם את סידורי ההושבה?", "ברוב האולמות כשבוע עד עשרה ימים לפני האירוע, יחד עם מספר המנות הסופי. המועד המדויק כתוב בחוזה או אצל מנהלת האירוע."),
            ("כמה אנשים בשולחן בחתונה?", "בדרך כלל 10–12 בשולחן עגול, ותלוי בגודל השולחן ובאולם. פירוט במדריך כמה שולחנות צריך.")],
    "cta_title": "כלי סידורי ההושבה של תכנון פלוס", "cta_text": "גרירה, הושבה אוטומטית, התנגשויות ורשימת כניסה. חינם לשימוש, בלי הרשמה.", "cta_btn": "לכלי ההושבה",
    "more": '<a href="../tables-and-seats/">כמה שולחנות צריך</a> · <a href="../../../wedding-planner/guides/rsvp-seating-gifts/">אישורי הגעה, הושבה וצ\'קים</a> · <a href="../../../wedding-planner/">מתכנן החתונה באקסל</a>',
}

TABLE_CALC = """
<div class="tool-panel mt-2" id="tcalc">
 <div class="fields cols-3">
  <div class="field"><label for="tc-guests">מאשרי הגעה</label><input id="tc-guests" type="number" min="1" value="250" inputmode="numeric"></div>
  <div class="field"><label for="tc-seats">מקומות בשולחן</label><input id="tc-seats" type="number" min="2" value="10" inputmode="numeric"></div>
  <div class="field"><label for="tc-special">שולחנות מיוחדים (אבירים, משפחה)</label><input id="tc-special" type="number" min="0" value="1" inputmode="numeric"></div>
 </div>
 <div class="field"><label for="tc-special-seats">מקומות בכל שולחן מיוחד</label><input id="tc-special-seats" type="number" min="2" value="14" inputmode="numeric"></div>
 <div class="result" aria-live="polite"><p class="mb-0" id="tc-out"></p></div>
</div>
"""
TABLE_SCRIPT = """<script>
(function () {
  var $ = function (id) { return document.getElementById(id); };
  function n(id, d) { var v = parseInt($(id).value, 10); return isFinite(v) && v >= 0 ? v : d; }
  function calc() {
    var g = n("tc-guests", 0), s = Math.max(2, n("tc-seats", 10)), sp = n("tc-special", 0), ss = Math.max(2, n("tc-special-seats", 14));
    var rest = Math.max(0, g - sp * ss), t = Math.ceil(rest / s), total = t + sp, seats = t * s + sp * ss;
    $("tc-out").innerHTML = "צריך <strong>" + total + " שולחנות</strong>: " + (sp ? sp + " מיוחדים + " : "") + t + " רגילים של " + s +
      " (" + seats + " מקומות ל-" + g + " אורחים, " + (seats - g) + " פנויים). מומלץ להוסיף שולחן אחד רזרבי למי שמאשר ברגע האחרון.";
  }
  ["tc-guests", "tc-seats", "tc-special", "tc-special-seats"].forEach(function (id) { $(id).addEventListener("input", calc); });
  calc();
})();
</script>
"""
G_SEAT_2 = {
    "slug": "seating-chart", "id": "tables-and-seats", "product_short": "סידורי הושבה", "crumb": "כמה שולחנות צריך", "app": "apps/seating/",
    "title": "כמה שולחנות צריך לחתונה? מחשבון + כמה יושבים בשולחן עגול ומלבני",
    "desc": "מחשבון כמה שולחנות צריך לחתונה או לאירוע לפי מספר המאשרים, וכללי אצבע לכמה אנשים יושבים בשולחן עגול, מלבני ושולחן אבירים.",
    "h1": "כמה שולחנות צריך? מחשבון וכללי אצבע לשולחן עגול ומלבני", "minutes": 4,
    "body": """<p class="lead">החשבון הבסיסי פשוט: מאשרים חלקי מקומות בשולחן. אבל שולחנות מיוחדים, ילדים ושינויים של הרגע האחרון משנים את התמונה. המחשבון כאן עושה את זה בשבילכם.</p>
""" + TABLE_CALC + """
<h2>כמה אנשים יושבים בשולחן?</h2>
<p>אלה כללי אצבע מקובלים. בכל אולם המידות והמנהגים קצת שונים, אז <strong>תמיד בדקו עם האולם</strong> כמה הוא מושיב בפועל ואם יש לו שולחנות בכמה גדלים.</p>
<div class="table-wrap"><table>
<thead><tr><th scope="col">סוג שולחן</th><th scope="col">בנוחות</th><th scope="col">צפוף</th></tr></thead>
<tbody>
<tr><td>עגול, קוטר כ-150 ס&quot;מ</td><td>8–10</td><td>11</td></tr>
<tr><td>עגול, קוטר כ-180 ס&quot;מ</td><td>10–12</td><td>13–14</td></tr>
<tr><td>מלבני כ-180×75 ס&quot;מ</td><td>6 (3 בכל צד)</td><td>8 (גם בראשים)</td></tr>
<tr><td>שולחן אבירים (כמה מלבניים ברצף)</td><td>כ-2 אנשים לכל מטר אורך</td><td>—</td></tr>
</tbody></table></div>
<p class="small muted">כלל אצבע: לכל סועד צריך כ-60 ס&quot;מ לאורך היקף השולחן, ו-70 ס&quot;מ אם יש כיסאות עם ידיות או כיסאות תינוק.</p>

<h2>עגול או מלבני?</h2>
<ul>
 <li><strong>עגול</strong> – כולם רואים את כולם, נוח לשיחה. הסטנדרט ברוב האולמות.</li>
 <li><strong>מלבני / אבירים</strong> – מכניס יותר אנשים לאותו שטח, ונראה טוב בגן ובאירוע בסגנון &quot;שולחן ארוך&quot;. פחות נוח לשיחה עם מי שבקצה השני.</li>
</ul>

<h2>אל תמלאו כל שולחן עד הסוף</h2>
<p>שולחן מלא בדיוק נראה טוב על הנייר, אבל אם מגיעים עוד 2 אנשים מאותה משפחה אין לאן להוסיף אותם. השאירו מקום פנוי פה ושם, או שולחן רזרבי אחד, ותאמו עם האולם כמה כיסאות נוספים יש בהישג יד.</p>

<h2>ילדים</h2>
<p>תינוקות בעגלה לא תופסים מקום, אבל ילד שאוכל – כן (ולפעמים במנת ילד). ספרו אותם ברשימה כדי שהחשבון יהיה נכון.</p>

<h2>מהמספר לסידור</h2>
<p>אחרי שיודעים כמה שולחנות, אפשר להושיב. ב<a href="../../../../apps/seating/">כלי סידורי ההושבה</a> מוסיפים את מספר השולחנות שיצא כאן בלחיצה אחת, והכלי מראה כל הזמן כמה מקומות פנויים נשארו וכמה חסרים. השלבים המלאים ב<a href="../how-to-seat-guests/">מדריך סידורי ההושבה</a>.</p>""",
    "faq": [("כמה שולחנות צריך ל-300 אורחים?", "בשולחנות של 10 – 30 שולחנות, ועוד שולחן רזרבי אחד. בשולחנות של 12 – 25. הכניסו את המספרים שלכם במחשבון למעלה."),
            ("כמה יושבים בשולחן אבירים?", "בערך 2 אנשים לכל מטר אורך, משני הצדדים יחד. שולחן אבירים של 6 מטר מושיב כ-12–14 אנשים.")],
    "cta_title": "מהמספר לסידור – בכלי אחד", "cta_text": "מוסיפים שולחנות, מדביקים את רשימת המוזמנים ולוחצים \"הושבה אוטומטית\". חינם.", "cta_btn": "לכלי ההושבה",
    "more": '<a href="../how-to-seat-guests/">איך עושים סידורי הושבה</a> · <a href="../../../wedding-planner/guides/wedding-budget-2026/">תקציב חתונה 2026</a> · <a href="../../../../tools/wedding-gift/">כמה לשים בחתונה</a>',
    "script": TABLE_SCRIPT,
}

G_CV_1 = {
    "slug": "cv-builder", "id": "how-to-write-cv", "product_short": "בונה קורות חיים", "crumb": "איך כותבים קורות חיים", "app": "apps/cv/",
    "title": "איך כותבים קורות חיים בעברית (2026): מבנה, דוגמאות וטעויות נפוצות",
    "desc": "מדריך לכתיבת קורות חיים בעברית: מה מכניסים ובאיזה סדר, איך כותבים תמצית והישגים, איך מציגים שירות צבאי, ומה לא לכתוב. עם דוגמאות.",
    "h1": "איך כותבים קורות חיים בעברית: מבנה, דוגמאות וטעויות נפוצות", "minutes": 7,
    "body": """<p class="lead">מגייסים מקדישים לקורות חיים שניות ספורות בסינון הראשון, ולפעמים לפניהם עוברת מערכת סינון אוטומטית. המטרה פשוטה: שבקריאה מהירה יהיה ברור מה אתם יודעים לעשות ולמה אתם מתאימים <em>למשרה הזאת</em>.</p>

<h2>האורך: עמוד אחד, לפעמים שניים</h2>
<p>לרוב המשרות עמוד אחד מספיק. עם 10+ שנות ניסיון רלוונטי – עד שני עמודים. מה שלא נכנס כנראה לא מספיק חשוב.</p>

<h2>המבנה המקובל</h2>
<ol>
 <li><strong>פרטים אישיים</strong> – שם, טלפון, אימייל, עיר. קישור ללינקדאין או לתיק עבודות אם יש.</li>
 <li><strong>תמצית מקצועית</strong> – 2–4 שורות.</li>
 <li><strong>ניסיון תעסוקתי</strong> – מהחדש לישן.</li>
 <li><strong>שירות צבאי / לאומי</strong> – בתחילת הקריירה לפני ההשכלה או אחריה; עם ניסיון רב – בקצרה, בסוף.</li>
 <li><strong>השכלה</strong> – תואר, מוסד, שנים. ממוצע רק אם הוא גבוה ורלוונטי.</li>
 <li><strong>כישורים ושפות</strong>.</li>
 <li><strong>מדורים נוספים</strong> – התנדבות, קורסים, פרסומים, פרויקטים.</li>
</ol>

<h2>מה <u>לא</u> לכתוב</h2>
<ul>
 <li>מספר תעודת זהות, כתובת מלאה, מצב משפחתי, גיל ותמונה – לא נדרשים ולא עוזרים.</li>
 <li>&quot;קורות חיים&quot; בכותרת – ברור מהמסמך. בכותרת שמים את השם.</li>
 <li>&quot;ממליצים יינתנו לפי בקשה&quot; – זה מובן מאליו.</li>
 <li>תחביבים, אלא אם הם באמת קשורים למשרה.</li>
</ul>

<h2>תמצית מקצועית שעובדת</h2>
<p>מי אתם, במה אתם חזקים (עם מספר אחד אם אפשר), ומה אתם מחפשים. בלי סיסמאות כמו &quot;יחסי אנוש מצוינים&quot;.</p>
<div class="callout"><strong>דוגמה:</strong> &quot;מנהלת חשבונות עם 5 שנות ניסיון בהנהלת חשבונות סוג 3, בחברות של 50–200 עובדים. אחראית על סגירות חודשיות, התאמות בנקים ודיווחי מע&quot;מ. מחפשת תפקיד של חשבת שכר או מנהלת כספים בחברה צומחת.&quot;</div>

<h2>ניסיון: הישגים, לא רק תחומי אחריות</h2>
<p>במקום לתאר מה התפקיד &quot;כלל&quot;, תארו מה <strong>עשיתם ומה יצא מזה</strong>. מתחילים בפועל, ומוסיפים מספר כשאפשר.</p>
<div class="table-wrap"><table>
<thead><tr><th scope="col">במקום</th><th scope="col">עדיף</th></tr></thead>
<tbody>
<tr><td>אחריות על שירות לקוחות</td><td>טיפלתי בכ-60 פניות ביום ושמרתי על ציון שביעות רצון של 4.7 מתוך 5</td></tr>
<tr><td>ניהול קמפיינים</td><td>הורדתי את העלות לליד ב-30% תוך חצי שנה</td></tr>
<tr><td>עבודה מול ספקים</td><td>ניהלתי מו&quot;מ מול 12 ספקים וחסכתי כ-80 אלף ₪ בשנה</td></tr>
</tbody></table></div>
<p>פעלים שעובדים טוב: הובלתי, הקמתי, שיפרתי, קיצרתי, חסכתי, הטמעתי, ניהלתי, בניתי, הדרכתי.</p>

<h2>איך כותבים שירות צבאי</h2>
<p>מי שקורא את קורות החיים לא תמיד מכיר את שמות היחידות והקורסים. תרגמו את השירות לכישורים:</p>
<ul>
 <li><strong>תפקיד ויחידה במילים פשוטות</strong> – &quot;מש&quot;קית הדרכה, חיל המודיעין&quot; ולא רק ראשי תיבות.</li>
 <li><strong>מה עשיתם, בהיקף</strong> – &quot;הדרכתי מחזורים של 30 חיילים&quot;, &quot;אחראי על ציוד בשווי כמיליון ₪&quot;.</li>
 <li><strong>פיקוד וניהול</strong> – כמה אנשים היו תחתיכם.</li>
 <li>אם השירות מסווג – כתבו את התחום הכללי בלבד (&quot;תפקיד טכנולוגי ביחידה מבצעית&quot;).</li>
</ul>

<h2>כישורים</h2>
<p>רשימה קצרה של כלים וכישורים שבאמת שולטים בהם, עם המילים שמופיעות במודעת המשרה: Excel, SAP, Python, Salesforce, הנהלת חשבונות סוג 3. כישורים רכים עדיף להראות דרך ההישגים ולא לכתוב כרשימה.</p>

<h2>שפות</h2>
<p>שפה ורמה, בשורה אחת: &quot;עברית – שפת אם · אנגלית – ברמה גבוהה מאוד · רוסית – שיחה&quot;.</p>

<h2>התאמה לכל משרה</h2>
<p>לא צריך לכתוב קורות חיים חדשים לכל משרה, אבל כן כדאי: לעדכן את התמצית, להקדים את ההישגים הכי רלוונטיים, ולוודא שהמילים המרכזיות מהמודעה מופיעות. זה גם מה שעוזר לעבור <a href="../cv-in-english/">מערכות סינון (ATS)</a>.</p>

<h2>הקובץ עצמו</h2>
<ul>
 <li><strong>PDF</strong> כברירת מחדל – נראה אותו דבר בכל מחשב. <strong>Word</strong> רק כשמבקשים.</li>
 <li>שם קובץ ברור: &quot;קורות חיים - שם מלא.pdf&quot;, לא &quot;cv_final_3.pdf&quot;.</li>
 <li>PDF עם טקסט אמיתי, לא סריקה ולא תמונה.</li>
</ul>""",
    "faq": [("כמה עמודים צריכים להיות קורות חיים?", "עמוד אחד לרוב המשרות, ועד שני עמודים למי שיש לו ניסיון רלוונטי של 10 שנים ומעלה."),
            ("צריך לשים תמונה בקורות חיים?", "בישראל זה לא נדרש ברוב המשרות, ומערכות סינון לא קוראות תמונות. עדיף בלי, אלא אם המעסיק ביקש."),
            ("לכתוב שירות צבאי לפני או אחרי השכלה?", "בתחילת הקריירה השירות הוא לרוב הניסיון המשמעותי, ולכן אפשר לשים אותו לפני ההשכלה. עם כמה שנות ניסיון – בקצרה, אחרי הניסיון התעסוקתי.")],
    "cta_title": "בונה קורות החיים של תכנון פלוס", "cta_text": "טופס פשוט, תצוגה חיה ו-4 תבניות נקיות, בעברית ובאנגלית. חינם לשימוש.", "cta_btn": "לבניית קורות חיים",
    "more": '<a href="../cv-in-english/">קורות חיים באנגלית ומערכות ATS</a> · <a href="../../">בונה קורות החיים</a>',
}

G_CV_2 = {
    "slug": "cv-builder", "id": "cv-in-english", "product_short": "בונה קורות חיים", "crumb": "קורות חיים באנגלית ו-ATS", "app": "apps/cv/",
    "title": "קורות חיים באנגלית לישראלים: מבנה, תרגום שירות צבאי ומעבר מערכות ATS",
    "desc": "איך כותבים קורות חיים באנגלית כשהמקור בעברית: מבנה, תאריכים, איך לתרגם שירות צבאי ותארים, טעויות נפוצות, ומה עושים כדי שמערכות סינון (ATS) יקראו את הקובץ.",
    "h1": "קורות חיים באנגלית לישראלים: מבנה, תרגום ומערכות ATS", "minutes": 7,
    "body": """<p class="lead">הרבה משרות בישראל, בעיקר בהייטק ובחברות בינלאומיות, מבקשות קורות חיים באנגלית. זה לא תרגום מילה-במילה של הגרסה העברית: יש הבדלים במבנה, בניסוח ובמה שמשמיטים.</p>

<h2>המבנה באנגלית</h2>
<ol>
 <li><strong>Name + contact</strong> – שם, טלפון בפורמט בינלאומי (+972-50-...), אימייל, עיר ומדינה (Tel Aviv, Israel), לינקדאין.</li>
 <li><strong>Summary</strong> – 2–3 שורות.</li>
 <li><strong>Experience</strong> – מהחדש לישן, עם 2–5 נקודות לכל תפקיד.</li>
 <li><strong>Military Service</strong> – בקצרה (ראו בהמשך).</li>
 <li><strong>Education</strong>, <strong>Skills</strong>, <strong>Languages</strong>.</li>
</ol>
<p>בבונה קורות החיים יש גרסה עברית וגרסה אנגלית נפרדות, והכותרות מתחלפות לבד. אפשר להעתיק את העברית כבסיס ולתרגם שדה-שדה.</p>

<h2>ניסוח: פועל בעבר + תוצאה</h2>
<p>כל נקודה מתחילה בפועל, בלי &quot;I&quot;: <em>Led, Built, Reduced, Increased, Launched, Managed, Automated</em>. ואחריו מספר:</p>
<div class="callout"><em>Reduced monthly closing time from 10 to 6 working days by automating bank reconciliations in Excel.</em></div>
<p>בתפקיד הנוכחי – זמן הווה (<em>Lead, Manage</em>), בתפקידים קודמים – עבר.</p>

<h2>תאריכים</h2>
<p>פורמט אחיד בכל המסמך: <em>2021 – Present</em> או <em>Mar 2021 – Jan 2024</em>. לא לערבב 03/2021 עם 2021.</p>

<h2>איך מתרגמים שירות צבאי</h2>
<ul>
 <li>כתבו <strong>IDF</strong> ואת החיל באנגלית: <em>IDF Intelligence Corps</em>, <em>IDF Armored Corps</em>.</li>
 <li>תרגמו את <strong>התפקיד</strong>, לא את הראשי תיבות: &quot;מש&quot;קית הדרכה&quot; ← <em>Training NCO</em>; &quot;קצין&quot; ← <em>Officer (Lieutenant)</em>; &quot;מפקד צוות&quot; ← <em>Team Commander</em>.</li>
 <li>תארו את ההיקף: <em>Commanded a team of 12 soldiers</em>, <em>Trained cohorts of 30</em>.</li>
 <li>למשרות בחו&quot;ל – שורה אחת מספיקה, אלא אם התפקיד רלוונטי ישירות.</li>
</ul>

<h2>השכלה</h2>
<p><em>B.A. in Economics, Tel Aviv University, 2019</em>. ציון ממוצע רק אם הוא גבוה; באנגלית מקובל <em>GPA 92/100</em> או <em>Cum Laude / Magna Cum Laude</em>. &quot;הנדסאי&quot; – <em>Practical Engineer</em>; &quot;בגרות מלאה&quot; בדרך כלל לא כותבים.</p>

<h2>טעויות נפוצות של ישראלים</h2>
<ul>
 <li><em>Responsible for…</em> בכל שורה – מתארים מה עשיתם, לא על מה הייתם אחראים.</li>
 <li>תרגום מילולי: &quot;Excellent human relations&quot;, &quot;Fast learner&quot; – עדיף להראות בהישג.</li>
 <li>פרטים אישיים כמו גיל, מצב משפחתי ות&quot;ז – לא כותבים, ובמשרות בארה&quot;ב זה אפילו לא רצוי.</li>
 <li>מסמך מיושר לימין או עם סימני פיסוק הפוכים – בגרסה האנגלית הכל משמאל לימין.</li>
</ul>

<h2>מה זה ATS ואיך עוברים אותו</h2>
<p>ATS (Applicant Tracking System) היא מערכת שקולטת קורות חיים, מפרקת אותם לשדות ומדרגת אותם לפי התאמה למשרה. הרבה חברות בינוניות וגדולות בישראל משתמשות בה. מה שעוזר לה לקרוא נכון:</p>
<ul>
 <li><strong>טור אחד</strong>, בלי טבלאות, תיבות טקסט או עמודות צד.</li>
 <li><strong>כותרות רגילות</strong>: Experience, Education, Skills – לא &quot;My Journey&quot;.</li>
 <li><strong>טקסט אמיתי</strong>: PDF שנוצר מהמסמך (לא סריקה, לא תמונה), או Word.</li>
 <li><strong>מילים מהמודעה</strong>: אם כתוב &quot;Salesforce&quot; ו&quot;stakeholder management&quot; – והם נכונים לגביכם – שיופיעו כלשונם.</li>
 <li>פרטי קשר בגוף המסמך, לא בכותרת עליונה של Word.</li>
 <li>בלי אייקונים במקום מילים (טלפון 📞), בלי גרפים של &quot;רמת שליטה&quot;.</li>
</ul>
<p>כל ארבע התבניות ב<a href="../../../../apps/cv/">בונה קורות החיים</a> בנויות כך: טור אחד, כותרות סטנדרטיות, וה-PDF והקובץ ב-Word הם טקסט אמיתי. שום כלי לא יכול להבטיח מעבר סינון – התוכן וההתאמה למשרה הם העיקר.</p>

<h2>צ'קליסט לפני שליחה</h2>
<ul>
 <li>☐ עמוד אחד (או שניים עם ניסיון רב).</li>
 <li>☐ כל נקודה מתחילה בפועל ויש בה תוצאה.</li>
 <li>☐ תאריכים בפורמט אחיד.</li>
 <li>☐ בדיקת איות (גם שמות חברות וכלים).</li>
 <li>☐ שם קובץ: <em>FirstName-LastName-CV.pdf</em>.</li>
</ul>""",
    "faq": [("CV או Resume – מה ההבדל?", "בישראל ובאירופה אומרים CV, בארה\"ב Resume, ובפועל מדובר באותו מסמך של עמוד-שניים. (בארה\"ב CV הוא לרוב מסמך אקדמי ארוך.)"),
            ("להגיש PDF או Word?", "PDF כברירת מחדל, כל עוד הוא נוצר מהמסמך ולא נסרק. אם המודעה או מערכת ההגשה מבקשות DOCX – שולחים Word."),
            ("צריך לתרגם את כל קורות החיים או לכתוב מחדש?", "עדיף לכתוב מחדש בעזרת הגרסה העברית: אותו תוכן, אבל ניסוח באנגלית טבעית, פעלים בהתחלה ובלי ביטויים שמתורגמים מילולית.")],
    "cta_title": "קורות חיים בעברית ובאנגלית, באותו מקום", "cta_text": "שתי גרסאות נפרדות, 4 תבניות שמתאימות ל-ATS, תצוגה חיה. חינם לשימוש.", "cta_btn": "לבניית קורות חיים",
    "more": '<a href="../how-to-write-cv/">איך כותבים קורות חיים בעברית</a> · <a href="../../">בונה קורות החיים</a>',
}


def main():
    product_page(SEATING)
    product_page(CV)
    for g in (G_SEAT_1, G_SEAT_2, G_CV_1, G_CV_2):
        guide_page(g)


if __name__ == "__main__":
    main()
