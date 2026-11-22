#!/usr/bin/env python3
"""R6B conversion readiness for the wedding products (idempotent; also run by tools/site/build_site.py).

    python3 tools/convert/build_convert.py

* Product pages (p/wedding-planner, p/seating-chart, p/invitation-maker): a "before you buy" block right after the
  hero, between <!-- convert:trust --> markers: what you get, who it fits / doesn't, a free sample ("נסו בחינם"),
  a 3-step "how it works" strip and the payment / delivery / refund lines.
* New pages written whole: p/rsvp-tracker/ (landing for the RSVP app) and p/wedding-bundle/ (compare table + one buy box).
* chatuna/ hub: free samples section (<!-- convert:samples -->) before the bundle section.
* tools/wedding-gift/: gentle "מתחתנים בעצמכם?" box after the result (<!-- convert:funnel -->).
Free samples live in docs/samples/ (make_mini_budget.py + samples.js). No reviews, no scarcity, no countdowns.
"""
import html
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
sys.path.insert(0, str(REPO / "tools" / "site"))
from site_config import BASE_URL, BRAND  # noqa: E402

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731


def load(slug):
    return json.loads((DOCS / "data" / "products" / f"{slug}.json").read_text(encoding="utf-8"))


def ils(n):
    n = float(n)
    return "₪" + (f"{int(n):,}" if n.is_integer() else f"{n:,.2f}")


SAMPLES = {
    "budget": dict(file="samples/mini-wedding-budget.xlsx", img="samples/img/mini-wedding-budget.webp", kind="Excel",
                   title="מיני תקציב חתונה (Excel)",
                   text="גיליון אחד עם נוסחאות אמיתיות: מוזמנים × מחיר מנה, 10 קטגוריות, התחייבויות, תשלומים והערכת מתנות. עובד גם ב-Google Sheets.",
                   alt="מיני תקציב חתונה באקסל – תצוגה של הקובץ החינמי"),
    "seating": dict(file="samples/seating-chart-sample.pdf", img="samples/img/seating-chart-sample.webp", kind="PDF",
                    title="דוגמת סידור הושבה (PDF)",
                    text="PDF נקי כמו שיוצא מהגרסה המלאה: מפת שולחנות ורשימת כניסה לפי א-ב, עם 77 מוזמנים בדויים.",
                    alt="דוגמת PDF של סידור הושבה לחתונה עם שמות בדויים"),
    "invite": dict(file="samples/invitation-sample.png", img="samples/img/invitation-sample.webp", kind="PNG",
                   title="דוגמת הזמנה לחתונה (PNG)",
                   text="הזמנה בעיצוב \"ענפי זית\" עם תאריך עברי, באיכות ההורדה הנקייה. השמות בדויים.",
                   alt="דוגמת הזמנה לחתונה בעיצוב ענפי זית"),
}

STEPS = {
    "file": [("בוחרים ומשלמים", "PayPal או כרטיס אשראי, בלי לפתוח חשבון ובלי הרשמה."),
             ("מורידים מיד", "אחרי התשלום עוברים לדף הורדה עם כל הקבצים. שמרו את הקישור כדי להוריד שוב."),
             ("ממלאים ומתכננים", "פותחים באקסל או ב-Google Sheets וממלאים רק את התאים הצבועים.")],
    "app": [("משתמשים בחינם", "הכלי פתוח לכולם בדפדפן, בלי הרשמה. בודקים שהוא מתאים לכם."),
            ("פותחים את הגרסה המלאה", "תשלום חד-פעמי ב-PayPal או בכרטיס, בתוך הכלי או בעמוד הזה."),
            ("מייצאים מיד", "ההורדות הנקיות נפתחות מיד בדפדפן שבו שילמתם. מקבלים גם קישור לדף אישור.")],
}

PRODUCTS = {
    "wedding-planner": dict(
        page="p/wedding-planner/index.html", kind="file", sample="budget", app=None,
        get=["קובץ Excel עם 9 גיליונות מחוברים: דשבורד, תקציב, ספקים, תשלומים, מוזמנים, מתנות, צ'קליסט והושבה",
             "קובץ דוגמה ממולא, כדי לראות איך זה נראה כשהכל מלא",
             "מסמך Word: נוסחים מוכנים, לוח זמנים ליום החתונה וצ'קליסט להדפסה",
             "עובד ב-Excel, ב-Google Sheets ובטלפון. בלי מאקרו, בלי מנוי",
             "הקבצים שלכם לתמיד, אפשר להוריד שוב מדף ההורדה"],
        fit=["זוגות שרוצים את כל המספרים במקום אחד ולשתף עם בן/בת הזוג וההורים",
             "מי שרוצה לעקוב אחרי מקדמות, יתרות לספקים וצ'קים מהחתונה",
             "חתונות של 80 עד 400 אורחים, באולם, בגן או באירוע צנוע"],
        notfit=["מי שמחפש אפליקציה ששולחת הודעות ותזכורות לבד: כאן מעדכנים ידנית",
                "מי שממש לא אוהב טבלאות (אז עדיף להתחיל מהכלים האונליין שלנו)",
                "מי שמפיקה מנהלת עבורו את התקציב והספקים"],
        delivery="מיד אחרי התשלום עוברים לדף הורדה עם 3 הקבצים. הקישור לדף נשמר אצלכם, ואפשר להוריד שוב בכל זמן."),
    "seating-chart": dict(
        page="p/seating-chart/index.html", kind="app", sample="seating", app="apps/seating/",
        get=["PDF נקי בלי סימן מים: מפת שולחנות + רשימת כניסה לפי א-ב לדלפק הכניסה",
             "ייצוא לאקסל: הושבה לפי שולחן, רשימת מוזמנים ושולחנות (לאולם ולמארחות)",
             "כרטיסי שולחן מוכנים להדפסה",
             "תשלום חד-פעמי, לכל האירועים שתתכננו בדפדפן הזה",
             "בחינם כבר עכשיו: שימוש מלא על המסך, הושבה אוטומטית ו-PDF עם סימן מים"],
        fit=["חתונות ואירועים של 50 עד 600 מוזמנים",
             "מי שרוצה להושיב בגרירה ולראות מיד התנגשויות (\"לא להושיב ליד…\")",
             "מי שקיבל רשימה מאקסל או מכלי אישורי ההגעה ורוצה לסדר שולחנות מהר"],
        notfit=["מי שצריך שרטוט של האולם בקנה מידה: הכלי מסדר שולחנות ושמות, לא מיקום פיזי באולם",
                "עבודה משותפת בזמן אמת מכמה טלפונים: הנתונים נשמרים בדפדפן אחד (מעבירים עם קובץ גיבוי)"],
        delivery="אין קובץ לחכות לו: הייצוא הנקי נפתח מיד בדפדפן שבו שילמתם, בלי הרשמה. מקבלים גם קישור לדף אישור שפותח את הגרסה המלאה גם במכשיר אחר."),
    "invitation-maker": dict(
        page="p/invitation-maker/index.html", kind="app", sample="invite", app="apps/invite/",
        get=["PNG נקי באיכות גבוהה (2000×2828) לוואטסאפ, בלי סימן מים",
             "PDF לבית דפוס (A5 או A6 עם בליד, 300 DPI) או דף A4 עם 2/4 הזמנות להדפסה בבית",
             "תיקונים והורדות חוזרות בלי הגבלה, גם בעיצובים אחרים",
             "בחינם כבר עכשיו: כל 12 העיצובים, תאריך עברי אוטומטי ותצוגה מקדימה עם סימן מים"],
        fit=["הזמנה דיגיטלית לוואטסאפ, או קובץ מוכן לבית דפוס",
             "מי שרוצה תאריך עברי נכון בלי לחשב לבד",
             "מי שרוצה לראות את ההזמנה מוכנה לפני שמשלמים"],
        notfit=["מי שרוצה להעלות תמונה או לוגו: כרגע אין אפשרות כזו",
                "מי שמחפש עיצוב אישי בהזמנה ממעצב/ת גרפי/ת"],
        delivery="ההורדות הנקיות נפתחות מיד בדפדפן שבו שילמתם, בלי לצאת מהמעצב. מקבלים גם קישור לדף אישור לשימוש במכשיר אחר."),
    "rsvp-tracker": dict(
        page="p/rsvp-tracker/index.html", kind="app", sample=None, app="apps/rsvp/",
        get=["מספר הזמנות בלי הגבלה (בחינם: עד 80 הזמנות, וכל הזמנה יכולה להיות משפחה שלמה)",
             "ייצוא לאקסל: כל הרשימה, סיכום מנות לפי צד, ורשימת מי שעוד לא ענה עם טלפונים",
             "תשלום חד-פעמי, בלי מנוי ובלי הרשמה",
             "הנתונים נשארים רק אצלכם בדפדפן",
             "בחינם כבר עכשיו: ייבוא אנשי קשר ואקסל, סטטוס הגעה, מנות, תזכורת בוואטסאפ והעברה להושבה"],
        fit=["זוגות שמנהלים את אישורי ההגעה בעצמם, בלי מוקד טלפוני",
             "מי שרוצה לדעת בכל רגע כמה מנות להזמין ומי עוד לא ענה",
             "מי שירצה אחר כך להושיב את המאשרים בכלי סידורי ההושבה"],
        notfit=["מי שרוצה שמישהו אחר יתקשר לאורחים: זה כלי לניהול עצמי, לא שירות אישורי הגעה",
                "שליחת הודעות המונית אוטומטית: כאן שולחים תזכורת בוואטסאפ בלחיצה לכל אורח"],
        delivery="ההגבלה נפתחת מיד בדפדפן שבו שילמתם, בלי הרשמה. מקבלים גם קישור לדף אישור שפותח את הגרסה המלאה במכשיר אחר."),
}


def rel_up(page):
    return "../" * (len(pathlib.PurePosixPath(page).parts) - 1)


def sample_card(key, up, heading="נסו בחינם"):
    s = SAMPLES[key]
    return (f'<div class="cv-card sample-card" data-sample="{key}"><h3>{E(heading)}</h3>'
            f'<img src="{up}{s["img"]}" alt="{E(s["alt"])}" loading="lazy" width="900" height="600">'
            f'<p class="mb-0"><strong>{E(s["title"])}</strong><br><span class="small muted">{E(s["text"])}</span></p>'
            f'<a class="btn secondary small" href="{up}{s["file"]}" download data-sample-dl="{key}">הורדה חינם ({s["kind"]}) ↓</a>'
            '<p class="small muted mt-1 mb-0">בלי תשלום, בלי מייל ובלי הרשמה.</p></div>')


def trust_row(up, delivery):
    return ('<div class="trust-row">'
            '<div><span class="ic" aria-hidden="true">🔒</span><span><strong>תשלום מאובטח</strong>'
            'PayPal או כרטיס אשראי/חיוב דרך PayPal. לא צריך חשבון PayPal, ואנחנו לא רואים את פרטי הכרטיס.</span></div>'
            f'<div><span class="ic" aria-hidden="true">⚡</span><span><strong>מסירה מיידית</strong>{E(delivery)}</span></div>'
            '<div><span class="ic" aria-hidden="true">↩</span><span><strong>החזר כספי הוגן</strong>'
            'מוצר דיגיטלי, לכן אין ביטול רק כי השתנתה התוכנית. אבל אם משהו לא עובד או שונה מהתיאור ולא תיקנו – מחזירים את מלוא הסכום. '
            f'<a href="{up}legal/refund/">מדיניות הביטולים</a></span></div>'
            "</div>")


def steps_strip(kind, title="איך זה עובד"):
    lis = "".join(f"<li><h3>{E(h)}</h3><p>{E(t)}</p></li>" for h, t in STEPS[kind])
    return f'<h2 class="mt-3" style="font-size:1.25rem">{E(title)}</h2><ol class="steps compact">{lis}</ol>'


def trust_block(slug, cfg, up, *, inner_only=False):
    p = load(slug)
    get = "".join(f"<li>{E(x)}</li>" for x in cfg["get"])
    fit = "".join(f"<li>{E(x)}</li>" for x in cfg["fit"])
    nofit = "".join(f"<li>{E(x)}</li>" for x in cfg["notfit"])
    if cfg["sample"]:
        third = sample_card(cfg["sample"], up)
    else:  # app with no sample file: the app itself is the free trial
        third = (f'<div class="cv-card"><h3>נסו בחינם</h3><p>הכלי עצמו חינם לשימוש עד 80 הזמנות, בלי הרשמה. '
                 'אפשר לטעון רשימת דוגמה ולראות הכל לפני שמחליטים.</p>'
                 f'<a class="btn secondary small" href="{up}{cfg["app"]}?demo=1">לפתוח עם רשימת דוגמה ←</a></div>')
    tail = ""
    if cfg["app"] and cfg["sample"]:
        tail = (f'<p class="small muted mt-2 mb-0">ועוד יותר טוב מדוגמה: <a href="{up}{cfg["app"]}">הכלי עצמו פתוח לשימוש חינם</a>, '
                f'ומשלמים {ils(p["price_ils"])} רק כשרוצים את הייצוא הנקי.</p>')
    body = ('<div class="cv-grid">'
            f'<div class="cv-card"><h2>מה מקבלים ב-{ils(p["price_ils"])}</h2><ul class="ticks">{get}</ul></div>'
            f'<div class="cv-card"><h2>למי זה מתאים</h2><ul class="ticks">{fit}</ul><h4>ולמי פחות</h4><ul class="crosses">{nofit}</ul></div>'
            f"{third}</div>{tail}"
            + steps_strip(cfg["kind"]) + trust_row(up, cfg["delivery"]))
    if inner_only:
        return body
    return ('<!-- convert:trust --><section class="section convert-trust" id="before-buy" aria-label="לפני שקונים">'
            f'<div class="container">{body}</div></section><!-- /convert:trust -->\n')


TRUST_RE = re.compile(r"<!-- convert:trust -->.*?<!-- /convert:trust -->\n?", re.S)


def inject_after_hero(src, block):
    if "<!-- convert:trust -->" in src:
        return TRUST_RE.sub(lambda m: block, src)
    i = src.find('<section class="hero">')
    j = src.find("</section>", i)
    if i < 0 or j < 0:
        raise SystemExit("hero section not found")
    j += len("</section>\n")
    return src[:j] + "\n" + block + src[j:]


# ---------------------------------------------------------------- whole pages (new)
def head(title, desc, path, image, ld):
    up = rel_up(path + "index.html")
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | {BRAND}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{BASE_URL}{path}">
<meta property="og:type" content="website">
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


def foot(up):
    return (f'\n</main>\n<footer id="site-footer"></footer>\n<script src="{up}assets/site.js"></script>\n'
            f'<script src="{up}assets/checkout.js"></script>\n</body>\n</html>\n')


def ld_graph(name, desc, path, price, images, crumb, faq):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": name, "description": desc, "sku": path.strip("/").split("/")[-1],
         "brand": {"@type": "Brand", "name": BRAND}, "image": [BASE_URL + i for i in images],
         "offers": {"@type": "Offer", "price": str(price), "priceCurrency": "ILS", "availability": "https://schema.org/InStock",
                    "url": BASE_URL + path, "priceValidUntil": "2027-12-31"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "דף הבית", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "הכל לחתונה", "item": BASE_URL + "chatuna/"},
            {"@type": "ListItem", "position": 3, "name": crumb, "item": BASE_URL + path}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faq]},
    ]}


def faq_html(faq):
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{a}</p></details>" for q, a in faq) + "</div>"


def crumbs(up, label):
    return (f'<nav class="breadcrumbs" aria-label="פירורי לחם"><a href="{up}">דף הבית</a> <span aria-hidden="true">›</span> '
            f'<a href="{up}chatuna/">הכל לחתונה</a> <span aria-hidden="true">›</span> <span aria-current="page">{E(label)}</span></nav>')


def build_rsvp_page():
    path = "p/rsvp-tracker/"
    up = rel_up(path + "index.html")
    p = load("rsvp-tracker")
    title = "רשימת מוזמנים ואישורי הגעה לחתונה – כלי אונליין חינם עד 80 הזמנות"
    desc = ("כלי אונליין בעברית לניהול רשימת מוזמנים ואישורי הגעה: ייבוא אנשי קשר ואקסל, סטטוס הגעה, מנות, תזכורת בוואטסאפ "
            "והעברה לסידורי הושבה. חינם עד 80 הזמנות; ₪29 חד-פעמי לבלי הגבלה + אקסל.")
    faq = [
        ("מה ההבדל בין החינמי למלא?", "בחינם אפשר לנהל עד 80 הזמנות (כל הזמנה יכולה להיות משפחה שלמה) עם כל הפעולות: ייבוא, סטטוס, מנות, תזכורות והעברה להושבה. "
         "הגרסה המלאה (₪29 חד-פעמי) מסירה את ההגבלה ומוסיפה ייצוא לאקסל."),
        ("איפה נשמרים הנתונים?", "רק בדפדפן שלכם (localStorage). הרשימה לא נשלחת אלינו. כדי לעבור מכשיר מורידים קובץ גיבוי ומעלים אותו במכשיר השני."),
        ("זה שולח הודעות לאורחים לבד?", "לא. לכל אורח יש כפתור שפותח וואטסאפ עם נוסח תזכורת מוכן, ואתם לוחצים שליחה. אין שליחה המונית אוטומטית."),
        ("מה קורה כשמגיעים ל-80 הזמנות?", "כל מה שכבר הוזן נשמר ונשאר זמין. פשוט אי אפשר להוסיף עוד הזמנות עד שפותחים את הגרסה המלאה."),
        ("אפשר לקבל החזר?", f'אפשר לבדוק הכל בחינם לפני התשלום. אם משהו לא עובד כמתואר ולא הצלחנו לתקן – מחזירים את מלוא הסכום. פרטים ב<a href="{up}legal/refund/">מדיניות הביטולים</a>.'),
    ]
    imgs = ["p/rsvp-tracker/img/screen-1.png", "p/rsvp-tracker/img/screen-2.png"]
    ld = ld_graph(p["title"], desc, path, p["price_ils"], imgs, "רשימת מוזמנים ואישורי הגעה", faq)
    out = head(title, desc, path, imgs[0], ld)
    out += f"""
<section class="hero">
 <div class="container">
  {crumbs(up, "רשימת מוזמנים ואישורי הגעה")}
  <div class="split">
   <div>
    <h1>רשימת מוזמנים ואישורי הגעה: <span class="hl">מי מגיע, כמה מנות, מי עוד לא ענה</span></h1>
    <p class="lead">כלי אונליין בעברית שעובד בדפדפן: מייבאים אנשי קשר או אקסל, מסמנים מי אישר, שולחים תזכורת בוואטסאפ בלחיצה ומעבירים את המאשרים לסידורי ההושבה.</p>
    <p class="btn-row"><a class="btn" href="{up}apps/rsvp/">לפתוח את הכלי (חינם)</a> <a class="btn secondary" href="{up}apps/rsvp/?demo=1">לראות עם רשימת דוגמה</a></p>
    <p class="small muted">חינם עד 80 הזמנות · {ils(p["price_ils"])} חד-פעמי לבלי הגבלה + אקסל · בלי הרשמה</p>
   </div>
   <div id="buy" class="buy" data-product="rsvp-tracker" data-label="גרסה מלאה: בלי הגבלה + ייצוא לאקסל"></div>
  </div>
 </div>
</section>

<section class="section alt" id="screens">
 <div class="container">
  <div class="section-head"><h2>ככה זה נראה</h2><p class="muted">צילומי מסך מהכלי עצמו עם רשימת הדוגמה (שמות בדויים).</p></div>
  <div class="screens">
<figure><a href="img/screen-1.webp" target="_blank" rel="noopener"><img src="img/screen-1.webp" alt="רשימת מוזמנים ואישורי הגעה – מסך ראשי עם סיכום מאשרים, מנות ורשימה לפי צד" loading="lazy" width="1280" height="860"></a><figcaption>מסך ראשי: סיכום מאשרים ומנות, ורשימה לפי צד וקבוצה</figcaption></figure>
<figure><a href="img/screen-2.webp" target="_blank" rel="noopener"><img src="img/screen-2.webp" alt="רשימת מוזמנים ואישורי הגעה בטלפון" loading="lazy" width="390" height="844" style="max-height:520px;object-fit:contain;background:#fff"></a><figcaption>עובד גם בטלפון, שם הכי נוח לסמן תשובות</figcaption></figure>
  </div>
 </div>
</section>
"""
    out += ('<!-- convert:trust --><section class="section convert-trust" id="before-buy" aria-label="לפני שקונים"><div class="container">'
            + trust_block("rsvp-tracker", PRODUCTS["rsvp-tracker"], up, inner_only=True) + "</div></section><!-- /convert:trust -->\n")
    out += f"""
<section class="section alt">
 <div class="container narrow">
  <div class="cta-box">
   <div><h2 style="font-size:1.25rem">מתכננים את כל החתונה?</h2>
   <p>חבילת החתונה: רשימת המוזמנים המלאה + סידורי הושבה + מעצב הזמנות + מתכנן באקסל ב-₪79 במקום ₪126.</p></div>
   <div><a class="btn" href="../wedding-bundle/">להשוואה ולחבילה ←</a></div>
  </div>
  <h2 class="mt-3">שאלות נפוצות</h2>
  {faq_html(faq)}
 </div>
</section>

<div class="buy-bar"><span><strong>אישורי הגעה</strong> · <span class="price">חינם עד 80</span></span><a class="btn small" href="{up}apps/rsvp/">לכלי</a></div>
"""
    out += foot(up)
    write(path, out)


def build_bundle_page():
    path = "p/wedding-bundle/"
    up = rel_up(path + "index.html")
    b = load("wedding-bundle")
    members = [load(s) for s in b["bundle_of"]]
    total = sum(float(m["price_ils"]) for m in members)
    save = total - float(b["price_ils"])
    title = "חבילת חתונה: מתכנן באקסל + סידורי הושבה + אישורי הגעה + הזמנה – ₪79"
    desc = (f"ארבעת כלי החתונה המלאים בתשלום אחד: מתכנן חתונה באקסל, סידורי הושבה, רשימת מוזמנים ואישורי הגעה ומעצב הזמנות. "
            f"{ils(b['price_ils'])} במקום {ils(total)}, תשלום חד-פעמי, בלי מנוי.")
    links = {"wedding-planner": "p/wedding-planner/", "seating-chart": "p/seating-chart/", "rsvp-tracker": "p/rsvp-tracker/",
             "invitation-maker": "p/invitation-maker/"}
    what = {"wedding-planner": "קובץ Excel / Google Sheets: תקציב, ספקים ותשלומים, מוזמנים, צ'קים, צ'קליסט + Word עם נוסחים",
            "seating-chart": "PDF נקי, ייצוא לאקסל וכרטיסי שולחן מכלי ההושבה",
            "rsvp-tracker": "בלי הגבלת 80 הזמנות + ייצוא לאקסל של המאשרים, המנות ומי שלא ענה",
            "invitation-maker": "PNG נקי לוואטסאפ ו-PDF לדפוס מכל 12 העיצובים"}
    delivery = {"wedding-planner": "הורדה מיידית", "seating-chart": "נפתח מיד בדפדפן", "rsvp-tracker": "נפתח מיד בדפדפן",
                "invitation-maker": "נפתח מיד בדפדפן"}
    rows = "".join(
        f'<tr><td><a href="{up}{links[m["slug"]]}"><strong>{E(m["title"])}</strong></a><br><span class="small muted">{E(what[m["slug"]])}</span></td>'
        f'<td class="small">{delivery[m["slug"]]}</td><td class="num">{ils(m["price_ils"])}</td><td class="num">✓</td></tr>'
        for m in members)
    faq = [
        ("איך מקבלים את ארבעת הכלים אחרי התשלום?", "מיד אחרי התשלום עוברים לדף אחד: שם מורידים את קבצי המתכנן, ובאותו רגע נפתחות בדפדפן הזה הגרסאות המלאות של כלי ההושבה, אישורי ההגעה ומעצב ההזמנות, עם כפתור לכל כלי. שמרו את הקישור לדף כדי לפתוח שוב או במכשיר אחר."),
        ("כבר קניתי אחד הכלים. כדאי לי החבילה?", "רק אם אתם צריכים לפחות עוד שניים מהשלושה האחרים. אין זיכוי אוטומטי על רכישה קודמת, אז השוו לפי הטבלה."),
        ("הכלים האונליין עובדים בלי אינטרנט ובכמה מכשירים?", "הכלים רצים בדפדפן והנתונים נשמרים במכשיר שלכם. כדי לעבור מכשיר משתמשים בקובץ הגיבוי, ופותחים שם את הקישור לדף האישור כדי לפתוח את הגרסה המלאה."),
        ("יש מנוי או חיוב חוזר?", "לא. תשלום אחד, ומה שקיבלתם נשאר שלכם."),
        ("אפשר לקבל החזר?", f'אם משהו לא עובד כמתואר ולא הצלחנו לתקן – מחזירים את מלוא הסכום. פרטים ב<a href="{up}legal/refund/">מדיניות הביטולים</a>.'),
    ]
    imgs = ["p/wedding-planner/img/screen-1.png", "p/seating-chart/img/screen-1.png", "p/rsvp-tracker/img/screen-1.png", "p/invitation-maker/img/screen-1.png"]
    ld = ld_graph(b["title"], desc, path, b["price_ils"], imgs, "חבילת חתונה", faq)
    out = head(title, desc, path, imgs[0], ld)
    shots = [("p/wedding-planner/img/screen-1.webp", "מתכנן החתונה: דשבורד"), ("p/seating-chart/img/screen-1.webp", "סידורי הושבה"),
             ("p/rsvp-tracker/img/screen-1.webp", "רשימת מוזמנים ואישורי הגעה"), ("p/invitation-maker/img/screen-1.webp", "מעצב ההזמנות")]
    figs = "".join(f'<figure><img src="{up}{s}" alt="{E(c)}" loading="lazy" width="1280" height="800"><figcaption>{E(c)}</figcaption></figure>' for s, c in shots)
    samples = "".join(sample_card(k, up, heading=SAMPLES[k]["title"].split(" (")[0]) for k in ("budget", "seating", "invite"))
    out += f"""
<section class="hero">
 <div class="container">
  {crumbs(up, "חבילת חתונה")}
  <div class="split">
   <div>
    <h1>חבילת חתונה: <span class="hl">ארבעת הכלים המלאים ב-{ils(b["price_ils"])}</span></h1>
    <p class="lead">מתכנן החתונה באקסל, סידורי הושבה, רשימת מוזמנים ואישורי הגעה ומעצב הזמנות – בתשלום אחד, במקום {ils(total)} בנפרד.</p>
    <ul class="hero-points"><li>חוסכים {ils(save)}</li><li>תשלום חד-פעמי, בלי מנוי</li><li>הכל בעברית</li><li>מתחילים מיד</li></ul>
   </div>
   <div id="buy" class="buy" data-product="wedding-bundle" data-label="חבילת חתונה – 4 כלים"></div>
  </div>
 </div>
</section>

<section class="section" id="compare">
 <div class="container narrow">
  <h2>בנפרד מול חבילה</h2>
  <div class="table-wrap"><table class="cmp-table">
   <thead><tr><th>מה כלול</th><th>איך מקבלים</th><th class="num">בנפרד</th><th class="num">בחבילה</th></tr></thead>
   <tbody>{rows}</tbody>
   <tfoot><tr><td>סה"כ</td><td></td><td class="num"><s>{ils(total)}</s></td><td class="num">{ils(b["price_ils"])}</td></tr>
   <tr><td colspan="4" class="small">חיסכון: {ils(save)} ({round(save / total * 100)}%) לעומת קנייה נפרדת</td></tr></tfoot>
  </table></div>
  <p class="small muted">המחירים הם המחירים הרגילים באתר. אין כאן מבצע מוגבל בזמן: החבילה תמיד במחיר הזה.</p>
 </div>
</section>

<section class="section alt" id="screens">
 <div class="container">
  <div class="section-head"><h2>מה בפנים</h2><p class="muted">צילומי מסך מהכלים עצמם (נתונים בדויים). כל אחד מהכלים האונליין פתוח לשימוש חינם לפני הקנייה.</p></div>
  <div class="screens">{figs}</div>
 </div>
</section>

<section class="section" id="before-buy">
 <div class="container">
  <div class="section-head"><h2>נסו לפני שקונים</h2><p class="muted">שלוש דוגמאות להורדה חינם, בלי מייל ובלי הרשמה.</p></div>
  <div class="samples-grid">{samples}</div>
  <h2 class="mt-3" style="font-size:1.25rem">למי החבילה מתאימה</h2>
  <div class="cv-grid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">
   <div class="cv-card"><h3>מתאימה</h3><ul class="ticks"><li>זוגות בתחילת התכנון שרוצים סדר מהתקציב ועד ההושבה</li><li>מי שצריך לפחות שלושה מהכלים</li><li>מי שמעדיף לעשות לבד, בלי אפליקציה במנוי</li></ul></div>
   <div class="cv-card"><h3>פחות מתאימה</h3><ul class="crosses"><li>מי שצריך רק כלי אחד: עדיף לקנות אותו לבד</li><li>מי שמפיקה מנהלת עבורו את כל התכנון</li><li>מי שמחפש שירות אישורי הגעה טלפוני</li></ul></div>
  </div>
  {steps_strip("file", "איך זה עובד")}
  {trust_row(up, "מיד אחרי התשלום: דף אחד עם קבצי המתכנן להורדה, והגרסאות המלאות של שלושת הכלים האונליין נפתחות בדפדפן הזה.")}
 </div>
</section>

<section class="section alt">
 <div class="container narrow">
  <h2>שאלות נפוצות</h2>
  {faq_html(faq)}
  <p class="mt-3"><a href="#buy" class="btn">לרכישת החבילה · {ils(b["price_ils"])}</a></p>
  <p class="small muted">צריכים רק חלק? <a href="{up}p/wedding-planner/">מתכנן</a> · <a href="{up}p/seating-chart/">הושבה</a> · <a href="{up}p/rsvp-tracker/">אישורי הגעה</a> · <a href="{up}p/invitation-maker/">הזמנות</a> · <a href="{up}chatuna/">הכל לחתונה</a></p>
 </div>
</section>

<div class="buy-bar"><span><strong>חבילת חתונה</strong> · <span class="price">{ils(b["price_ils"])}</span></span><a class="btn small" href="#buy">לרכישה</a></div>
"""
    out += foot(up)
    write(path, out)


def write(path, text):
    f = DOCS / path / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    if not f.exists() or f.read_text(encoding="utf-8") != text:
        f.write_text(text, encoding="utf-8")
        print("wrote", f.relative_to(REPO))


# ---------------------------------------------------------------- hub + calculator
def region(src, name, block, anchor, before=True):
    pat = re.compile(rf"<!-- convert:{name} -->.*?<!-- /convert:{name} -->\n?", re.S)
    block = f"<!-- convert:{name} -->{block}<!-- /convert:{name} -->\n"
    if pat.search(src):
        return pat.sub(lambda m: block, src)
    i = src.find(anchor)
    if i < 0:
        raise SystemExit(f"anchor for {name} not found")
    if not before:
        i += len(anchor) + 1
    return src[:i] + block + src[i:]


def hub_samples():
    up = "../"
    cards = "".join(sample_card(k, up, heading=SAMPLES[k]["title"].split(" (")[0]) for k in ("budget", "seating", "invite"))
    return ('<section class="section" id="dugmaot" aria-labelledby="s-h"><div class="container">'
            '<div class="section-head"><span class="eyebrow">נסו בחינם</span><h2 id="s-h">שלוש דוגמאות להורדה, בלי מייל ובלי הרשמה</h2>'
            '<p class="muted">רוצים לראות איך זה נראה לפני שמחליטים? קחו את הקבצים, פתחו, ותחליטו בעצמכם.</p></div>'
            f'<div class="samples-grid">{cards}</div>'
            '<p class="small muted mt-2">רוצים את כל ארבעת הכלים המלאים? <a href="../p/wedding-bundle/">השוואה: בנפרד מול חבילה ←</a></p>'
            "</div></section>")


def gift_funnel():
    # wrapped in embed-link markers so tools/site/build_embeds.py leaves it out of the third-party embed
    return ('<!-- embed-link --><aside class="funnel-box" aria-label="לזוגות שמתחתנים"><strong>מתחתנים בעצמכם?</strong>'
            '<p class="small">אותו חשבון מהצד השני: כמה תעלה החתונה וכמה יחזור במתנות, מי מאשר הגעה ואיך מושיבים. '
            'הכלים החינמיים לזוגות מחכים כאן: <a href="../../chatuna/#mitchatnim">מסלול "אנחנו מתחתנים" ←</a></p></aside>''<!-- /embed-link -->')


def main():
    for slug, cfg in PRODUCTS.items():
        if slug == "rsvp-tracker":
            continue
        f = DOCS / cfg["page"]
        src = f.read_text(encoding="utf-8")
        new = inject_after_hero(src, trust_block(slug, cfg, rel_up(cfg["page"])))
        if new != src:
            f.write_text(new, encoding="utf-8")
            print("updated", f.relative_to(REPO))
    build_rsvp_page()
    build_bundle_page()
    hub = DOCS / "chatuna/index.html"
    src = hub.read_text(encoding="utf-8")
    new = region(src, "samples", hub_samples(), '<section class="section" id="bundle"')
    if new != src:
        hub.write_text(new, encoding="utf-8")
        print("updated", hub.relative_to(REPO))
    gift = DOCS / "tools/wedding-gift/index.html"
    src = gift.read_text(encoding="utf-8")
    new = region(src, "funnel", gift_funnel(), '<script src="../../assets/share.js"></script>', before=False)
    if new != src:
        gift.write_text(new, encoding="utf-8")
        print("updated", gift.relative_to(REPO))


if __name__ == "__main__":
    main()
