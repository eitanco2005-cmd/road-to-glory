"""Generate W4's static pages (product pages, free tools, guides) into docs/.

python3 products/osek-patur-tracker/build_pages.py
Uses W1's shared design system (docs/assets/site.css, site.js, checkout.js) via relative paths.
Official figures used (checked 17.11.2026):
  * osek patur ceiling 2026 = 122,833 ILS (2025: 120,000) - Kol Zchut / Tax Authority
  * VAT 18% since 1.1.2025
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
CHECKED = "17.11.2026"
CEILING = 122833
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "site"))
from site_config import BASE_URL as BASE, BRAND  # noqa: E402

SRC_CEIL = ('<a href="https://www.kolzchut.org.il/he/%D7%A2%D7%95%D7%A1%D7%A7_%D7%A4%D7%98%D7%95%D7%A8" '
            'rel="noopener" target="_blank">כל זכות – עוסק פטור</a> ופרסומי '
            '<a href="https://www.gov.il/he/departments/israel_tax_authority/govil-landing-page" rel="noopener" target="_blank">רשות המסים</a>')
SRC_VAT = ('<a href="https://www.gov.il/he/departments/israel_tax_authority/govil-landing-page" rel="noopener" '
           'target="_blank">רשות המסים</a> – צו מס ערך מוסף (שיעור המס), בתוקף מ-1.1.2025')


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def page(path, *, title, desc, h1, body, crumbs, jsonld, og_image=None, depth, checkout=False, extra_head="",
         scripts="", crumbs_in_body=False):
    """depth = number of dirs below docs/ (p/slug = 2)."""
    up = "../" * depth
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in jsonld)
    crumb_html = ' <span aria-hidden="true">›</span> '.join(
        f'<a href="{up}{href}">{esc(name)}</a>' if href is not None else f"<span>{esc(name)}</span>"
        for name, href in crumbs)
    og = f'<meta property="og:image" content="{BASE}{og_image}">' if og_image else f'<meta property="og:image" content="{BASE}assets/og-default.png">'
    canon = f"{BASE}{path}/"
    html = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0e6b63">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
{og}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
{extra_head}
{ld}
</head>
<body>
<a class="skip-link" href="#main">דלג לתוכן</a>
<header id="site-header"></header>
<main id="main">
{"" if crumbs_in_body else f'<div class="container"><nav class="breadcrumbs mt-2" aria-label="פירורי לחם">{crumb_html}</nav></div>'}
{body.replace("%%CRUMBS%%", f'<nav class="breadcrumbs" aria-label="פירורי לחם">{crumb_html}</nav>')}
</main>
<footer id="site-footer"></footer>
<script src="{up}assets/site.js" defer></script>
{f'<script src="{up}assets/checkout.js" defer></script>' if checkout else ""}
{scripts}
</body>
</html>
"""
    out = DOCS / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n} for i, n in enumerate(items)]}


def faq_html(qas):
    return '<div class="faq">' + "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in qas) + "</div>"


def faq_ld(qas):
    import re
    strip = lambda s: re.sub("<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q),
                            "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qas]}


def product_ld(name, desc, price, image, sku):
    return {"@context": "https://schema.org", "@type": "Product", "name": name, "description": desc,
            "image": image, "sku": sku, "brand": {"@type": "Brand", "name": BRAND},
            "offers": {"@type": "Offer", "price": f"{price:.2f}", "priceCurrency": "ILS",
                       "availability": "https://schema.org/InStock", "url": BASE + "p/" + sku + "/", "itemCondition": "https://schema.org/NewCondition"}}


def tool_ld(name, desc):
    return {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": name, "description": desc,
            "applicationCategory": "FinanceApplication", "operatingSystem": "Web", "inLanguage": "he",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ILS"}}


def article_ld(headline, desc):
    return {"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc,
            "inLanguage": "he", "dateModified": "2026-11-17", "author": {"@type": "Organization", "name": BRAND}}


def screens(items):
    return '<div class="screens">' + "".join(
        f'<figure><img src="{src}" alt="{esc(alt)}" loading="lazy" width="1200" height="700"><figcaption>{cap}</figcaption></figure>'
        for src, alt, cap in items) + "</div>"


BAR_PAD = "<style>@media (max-width:899px){body{padding-bottom:72px}}</style>"


def buybar(price, label):
    return (f'<div class="buy-bar"><div><strong>{label}</strong> · <span class="price">₪{price}</span></div>'
            f'<a class="btn small" href="#buy">לרכישה</a></div>')


# =============================================================== product: osek patur tracker
def osek_product():
    faqs = [
        ("למי הקובץ מתאים?", "לכל מי שרשום כעוסק פטור (או עומד להירשם) ורוצה לדעת בכל רגע כמה הכניס, כמה הוציא וכמה נשאר עד התקרה – פרילנסרים, מורים פרטיים, מעצבים, צלמים, מטפלים ובעלי עסקים קטנים."),
        ("האם זה מחליף פנקס קבלות או תוכנת הנהלת חשבונות?", "לא. עוסק פטור צריך להוציא קבלות בפנקס קבלות ממוספר או בתוכנה הרשומה ברשות המסים. הקובץ מתעד את הקבלות וההוצאות ומרכז את המספרים, כדי שתדעו איפה אתם עומדים ויהיה לכם קל בסוף השנה."),
        ("מה קורה בשנה הבאה, כשהתקרה מתעדכנת?", "בגיליון 'הגדרות' משנים את שנת המס ואת סכום התקרה (שני תאים), וכל החישובים מתעדכנים. התקרה מתעדכנת בדרך כלל בינואר."),
        ("זה עובד ב-Google Sheets?", "כן. מעלים את הקובץ ל-Google Drive ופותחים באמצעות Google Sheets. כל הנוסחאות עובדות; ייתכנו הבדלים קטנים בעיצוב הגרפים. עובד גם ב-Excel למחשב, ב-Excel Online וב-LibreOffice."),
        ("יש בקובץ מאקרו או משהו שצריך להתקין?", "לא. זה קובץ אקסל רגיל עם נוסחאות בלבד, בלי מאקרו ובלי תוספים."),
        ("איך מקבלים את הקובץ?", "מיד אחרי התשלום ב-PayPal נפתח עמוד הורדה עם הקובץ הריק ועם עותק עם נתוני דוגמה."),
        ("האם הקובץ נותן ייעוץ מס?", "לא. הוא כלי לסדר ומעקב. בשאלות על חובות דיווח, מעבר לעוסק מורשה או ניכוי הוצאות – פנו לרואה חשבון או ליועץ מס."),
        ("אפשר לבטל ולקבל החזר?", 'זה מוצר דיגיטלי שנמסר מיד להורדה. פרטים מלאים ב<a href="../../legal/refund/">תנאי הרכישה ומדיניות הביטולים</a>.'),
    ]
    title = "אקסל לעוסק פטור 2026 – מעקב הכנסות, הוצאות ותקרה | תכנון פלוס"
    desc = "קובץ אקסל לעוסק פטור 2026: יומן הכנסות והוצאות, מד תקרה חי מול 122,833 ₪, תחזית מתי תעברו את התקרה, סיכום רבעוני ועזר לדוח השנתי. ₪39, הורדה מיידית."
    body = f"""
<section class="hero">
 <div class="container">
  %%CRUMBS%%
  <div class="split">
   <div>
    <h1>אקסל לעוסק פטור <span class="hl">2026</span>: הכנסות, הוצאות ומד תקרה חי</h1>
    <p class="lead">רושמים כל תשלום בשורה אחת, והקובץ מראה כמה ניצלתם מתקרת {CEILING:,} ₪, כמה נשאר ומתי תעברו אותה.</p>
   </div>
   <div class="buy" id="buy" data-product="osek-patur-tracker" data-compact="1"></div>
   <ul class="hero-points"><li>Excel + Google Sheets</li><li>בלי מאקרו</li><li>הורדה מיידית</li></ul>
  </div>
  <p class="mt-2"><a href="../../tools/osek-patur-ceiling/">או נסו קודם את מחשבון התקרה החינמי ←</a></p>
  <figure class="card mt-2" style="margin-inline:0;padding:.5rem"><img src="img/dashboard.webp" alt="לוח הבקרה של קובץ מעקב עוסק פטור: הכנסות מתחילת השנה, נותר עד התקרה ומד תקרה" width="1200" height="700"></figure>
 </div>
</section>

<section class="section alt">
 <div class="container">
  <div class="section-head"><h2>מה מקבלים בקובץ</h2></div>
  <div class="grid cols-3">
   <div class="feature"><div class="ic">📈</div><div><h3>מד תקרה חי</h3><p>אחוז הניצול מתוך {CEILING:,} ₪, כמה נשאר, וסימון בצהוב מ-70% ובאדום מ-90%.</p></div></div>
   <div class="feature"><div class="ic">🔮</div><div><h3>תחזית לסוף השנה</h3><p>לפי הקצב החודשי שלכם: מחזור צפוי, החודש שבו צפוי לעבור את התקרה, וכמה אפשר להכניס בחודש בלי לעבור.</p></div></div>
   <div class="feature"><div class="ic">🧾</div><div><h3>יומן הכנסות</h3><p>תאריך, מספר קבלה, לקוח ואמצעי תשלום. מקום ל-500 תשלומים, עם בדיקת תאריכים וסכומים.</p></div></div>
   <div class="feature"><div class="ic">💳</div><div><h3>יומן הוצאות</h3><p>11 קטגוריות (אפשר לשנות), אחוז מוכר להוצאות מעורבות כמו טלפון ורכב, וסימון מסמכים חסרים.</p></div></div>
   <div class="feature"><div class="ic">🗓️</div><div><h3>סיכום חודשי ורבעוני</h3><p>הכנסות, הוצאות ורווח לכל חודש ולכל רבעון, עם גרפים של הכנסות מול הוצאות ומצטבר מול התקרה.</p></div></div>
   <div class="feature"><div class="ic">📋</div><div><h3>עזר לדוח השנתי</h3><p>מחזור שנתי, הוצאות לפי קטגוריה, רווח, מספר קבלות ורשימת בדיקה של מסמכים לסוף השנה.</p></div></div>
  </div>
 </div>
</section>

<section class="section">
 <div class="container">
  <div class="section-head"><h2>ככה זה נראה</h2><p class="muted">צילומי מסך מהעותק עם נתוני הדוגמה שמצורף לקובץ.</p></div>
  {screens([("img/dashboard.webp", "לוח בקרה עם מד תקרה", "לוח הבקרה: ניצול התקרה, תחזית ומצב"),
            ("img/income-log.webp", "יומן הכנסות בעברית", "יומן הכנסות: שורה לכל תשלום"),
            ("img/monthly-summary.webp", "סיכום חודשי עם גרפים", "סיכום חודשי ורבעוני עם גרפים"),
            ("img/annual-report.webp", "עזר לדוח השנתי", "עזר לדוח השנתי ורשימת בדיקה")])}
 </div>
</section>

<section class="section alt">
 <div class="container">
  <div class="section-head"><h2>איך זה עובד</h2></div>
  <ol class="steps">
   <li><h3>ממלאים הגדרות</h3><p>שם העסק, שנת המס והתקרה (כבר מעודכנת ל-{CEILING:,} ₪). פעם אחת.</p></li>
   <li><h3>רושמים תשלומים והוצאות</h3><p>שורה לכל קבלה ולכל הוצאה. התאים הצהובים הם היחידים שממלאים.</p></li>
   <li><h3>מסתכלים על לוח הבקרה</h3><p>כל השאר מחושב לבד: תקרה, תחזית, סיכומים ודוח שנתי.</p></li>
  </ol>
 </div>
</section>

<section class="section">
 <div class="container narrow">
  <div class="section-head center"><h2>מעקב עוסק פטור 2026 – ₪39</h2><p class="muted">תשלום מאובטח ב-PayPal (גם בכרטיס אשראי בלי חשבון PayPal). ההורדה נפתחת מיד אחרי התשלום.</p></div>
  <p class="center"><a class="btn" href="#buy">לרכישה – ₪39</a></p>
  <p class="small muted center mt-2">משתלם יותר יחד: <a href="../../products/">חבילת עצמאים</a> – מעקב עוסק פטור + תבניות הצעת מחיר.</p>
  <div class="callout mt-2"><strong>שקיפות:</strong> הקובץ הוא כלי מעקב ואינו ייעוץ מס. נתון התקרה ({CEILING:,} ₪ לשנת 2026) נלקח מ{SRC_CEIL}, נבדק ב-{CHECKED}.</div>
 </div>
</section>

<section class="section alt">
 <div class="container narrow">
  <h2>שאלות נפוצות</h2>
  {faq_html(faqs)}
  <h2 class="mt-4">מדריכים שיכולים לעזור</h2>
  <ul>
   <li><a href="guides/osek-patur-ceiling-2026/">תקרת עוסק פטור 2026: כמה היא, איך מחשבים ומה קורה כשעוברים</a></li>
   <li><a href="guides/income-expense-tracking/">איך לנהל הכנסות והוצאות כעוסק פטור – מדריך מעשי</a></li>
   <li><a href="../../guides/open-osek-patur/">איך פותחים עוסק פטור ב-2026</a></li>
   <li><a href="../../tools/osek-patur-ceiling/">מחשבון תקרת עוסק פטור 2026 (חינם)</a></li>
  </ul>
 </div>
</section>
{buybar(39, "מעקב עוסק פטור")}
"""
    page("p/osek-patur-tracker", title=title, desc=desc, h1="", body=body, depth=2, checkout=True, extra_head=BAR_PAD, crumbs_in_body=True,
         crumbs=[("ראשי", ""), ("מוצרים", "products/"), ("מעקב עוסק פטור 2026", None)],
         og_image="p/osek-patur-tracker/img/dashboard.webp",
         jsonld=[product_ld("מעקב עוסק פטור 2026 – קובץ אקסל", desc, 39, BASE + "p/osek-patur-tracker/img/dashboard.webp", "osek-patur-tracker"),
                 breadcrumb_ld(["ראשי", "מוצרים", "מעקב עוסק פטור 2026"]), faq_ld(faqs)])


# =============================================================== product: quote pack
def quote_product():
    faqs = [
        ("מה ההבדל בין הצעת מחיר לחשבונית?", 'הצעת מחיר היא הצעה ללקוח לפני העבודה, ואינה מסמך מס. חשבונית מס או קבלה מפיקים בתוכנה או בפנקס מאושרים אחרי העסקה. הסבר מלא <a href="guides/quote-vs-invoice/">במדריך הזה</a>.'),
        ("המע\"מ מחושב לבד?", 'כן, בקובץ האקסל. בוחרים פעם אחת "עוסק מורשה", "חברה" או "עוסק פטור": לעוסק מורשה ולחברה מתווסף מע"מ 18%, לעוסק פטור – לא. אם השיעור ישתנה, מעדכנים תא אחד.'),
        ("מה יש בקבצי ה-Word?", "אותם 5 עיצובים, מוכנים להקלדה. ב-Word הסכומים מוקלדים ידנית (Word לא מחשב כמו אקסל), לכן מומלץ לחשב באקסל או ב<a href=\"../../tools/vat-calculator/\">מחשבון המע\"מ</a>."),
        ("אפשר להוסיף לוגו?", "כן. ב-Excel וב-Word: הוספה ← תמונה, וגוררים לכותרת."),
        ("איך שולחים ללקוח?", "שומרים כ-PDF (קובץ ← שמירה בשם / הדפסה ← PDF). כל עיצוב מוגדר לעמוד A4 אחד. לפני השמירה מכבים את הצהוב של תאי המילוי בתא אחד בהגדרות."),
        ("זה עובד ב-Google Sheets / Google Docs?", "כן. מעלים ל-Google Drive ופותחים ב-Google Sheets או ב-Google Docs."),
        ("התנאים בתבנית הם ייעוץ משפטי?", "לא. נוסח התנאים הוא דוגמה שאפשר לערוך. לעסקאות גדולות או מורכבות כדאי להתייעץ עם עורך דין."),
    ]
    title = "תבנית הצעת מחיר בעברית – Excel + Word, 5 עיצובים | תכנון פלוס"
    desc = "ערכת תבניות הצעת מחיר בעברית: 5 עיצובים ב-Excel עם חישוב מע\"מ 18% אוטומטי, הנחה ותוקף, וגרסאות Word. מתאים לעוסק מורשה ולעוסק פטור. ₪29, הורדה מיידית."
    body = f"""
<section class="hero">
 <div class="container">
  %%CRUMBS%%
  <div class="split">
   <div>
    <h1>תבנית <span class="hl">הצעת מחיר</span> בעברית – 5 עיצובים, Excel + Word</h1>
    <p class="lead">ממלאים פרטי עסק פעם אחת ומוסיפים שורות – הסכום, ההנחה, מע"מ 18% והתוקף מחושבים לבד.</p>
   </div>
   <div class="buy" id="buy" data-product="price-quote-pack" data-compact="1"></div>
   <ul class="hero-points"><li>עוסק מורשה, חברה או עוסק פטור</li><li>עמוד A4 אחד, שמירה כ-PDF</li><li>הורדה מיידית</li></ul>
  </div>
  <p class="mt-2"><a href="../../tools/vat-calculator/">או נסו קודם את מחשבון המע"מ החינמי ←</a></p>
  <figure class="card mt-2" style="margin-inline:0;padding:.5rem;overflow-x:auto"><img src="img/all-designs.webp" alt="חמשת עיצובי הצעת המחיר זה לצד זה" width="2073" height="524"></figure>
 </div>
</section>

<section class="section alt">
 <div class="container">
  <div class="section-head"><h2>מה בחבילה</h2></div>
  <div class="grid cols-3">
   <div class="feature"><div class="ic">🎨</div><div><h3>5 עיצובים</h3><p>קלאסי, מודרני, מינימליסטי, צבעוני, ועיצוב שמושך מחירים ממחירון.</p></div></div>
   <div class="feature"><div class="ic">🧮</div><div><h3>חישוב אוטומטי</h3><p>סה"כ לשורה, סכום ביניים, הנחה באחוזים, מע"מ 18% וסה"כ לתשלום.</p></div></div>
   <div class="feature"><div class="ic">🏷️</div><div><h3>מחירון</h3><p>רושמים את השירותים פעם אחת, ובעיצוב 5 בוחרים מרשימה – המחיר והיחידה נכנסים לבד.</p></div></div>
   <div class="feature"><div class="ic">📅</div><div><h3>תוקף ומספור</h3><p>תאריך ההצעה ו"בתוקף עד" מחושב לפי מספר הימים שבחרתם.</p></div></div>
   <div class="feature"><div class="ic">✍️</div><div><h3>תנאים וחתימה</h3><p>תנאי תשלום לדוגמה (אפשר לערוך) ושורות חתימה לאישור הלקוח.</p></div></div>
   <div class="feature"><div class="ic">📄</div><div><h3>גם ב-Word</h3><p>אותם 5 עיצובים כקבצי Word בעברית מימין לשמאל, להקלדה חופשית.</p></div></div>
  </div>
 </div>
</section>

<section class="section">
 <div class="container">
  <div class="section-head"><h2>5 העיצובים</h2><p class="muted">צילומי מסך מקובץ הדוגמה המצורף (פרטי עסק ולקוח לדוגמה).</p></div>
  {screens([("img/design-modern.webp", "הצעת מחיר בעיצוב מודרני עם חישוב מע\"מ", "עיצוב 2 – מודרני"),
            ("img/design-classic.webp", "הצעת מחיר בעיצוב קלאסי", "עיצוב 1 – קלאסי"),
            ("img/design-minimal.webp", "הצעת מחיר בעיצוב מינימליסטי", "עיצוב 3 – מינימליסטי"),
            ("img/design-pricelist.webp", "הצעת מחיר לפי מחירון", "עיצוב 5 – לפי מחירון"),
            ("img/word-modern.webp", "תבנית הצעת מחיר ב-Word", "גרסת Word – עיצוב מודרני")])}
 </div>
</section>

<section class="section alt">
 <div class="container narrow">
  <div class="section-head center"><h2>ערכת הצעות מחיר – ₪29</h2><p class="muted">תשלום מאובטח ב-PayPal (גם בכרטיס אשראי). ההורדה נפתחת מיד: Excel, Excel עם דוגמה, ו-ZIP עם 5 קבצי Word.</p></div>
  <p class="center"><a class="btn" href="#buy">לרכישה – ₪29</a></p>
  <p class="small muted center mt-2">משתלם יותר יחד: <a href="../../products/">חבילת עצמאים</a> – תבניות הצעת מחיר + מעקב עוסק פטור 2026.</p>
  <div class="callout warn mt-2"><strong>חשוב:</strong> הצעת מחיר <strong>אינה</strong> חשבונית מס או קבלה, וכך כתוב בתחתית כל עיצוב. מסמכי מס מפיקים בתוכנה או בפנקס מאושרים. שיעור המע"מ (18%) לפי {SRC_VAT}; נבדק ב-{CHECKED}.</div>
 </div>
</section>

<section class="section">
 <div class="container narrow">
  <h2>שאלות נפוצות</h2>
  {faq_html(faqs)}
  <h2 class="mt-4">מדריכים</h2>
  <ul>
   <li><a href="guides/how-to-write-a-quote/">איך לכתוב הצעת מחיר שסוגרת עסקה – מבנה, דוגמה וטעויות נפוצות</a></li>
   <li><a href="guides/quote-vs-invoice/">הצעת מחיר, חשבון עסקה, קבלה וחשבונית מס – מה ההבדל?</a></li>
   <li><a href="../../tools/vat-calculator/">מחשבון מע"מ 18% (חינם)</a></li>
  </ul>
 </div>
</section>
{buybar(29, "ערכת הצעות מחיר")}
"""
    page("p/price-quote-pack", title=title, desc=desc, h1="", body=body, depth=2, checkout=True, extra_head=BAR_PAD, crumbs_in_body=True,
         crumbs=[("ראשי", ""), ("מוצרים", "products/"), ("תבניות הצעת מחיר", None)],
         og_image="p/price-quote-pack/img/all-designs.webp",
         jsonld=[product_ld("ערכת תבניות הצעת מחיר בעברית – Excel + Word", desc, 29, BASE + "p/price-quote-pack/img/all-designs.webp", "price-quote-pack"),
                 breadcrumb_ld(["ראשי", "מוצרים", "תבניות הצעת מחיר"]), faq_ld(faqs)])


# =============================================================== tool: ceiling calculator
CEIL_JS = """
<script>
(function(){
  var C = %d;
  var MONTHS = ["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"];
  var $ = function(id){ return document.getElementById(id); };
  var fmt = function(n){ return "₪" + Math.round(n).toLocaleString("he-IL"); };
  var now = new Date();
  var defMonth = now.getFullYear() === 2026 ? now.getMonth() + 1 : (now.getFullYear() > 2026 ? 12 : 1);
  ["month","start"].forEach(function(id){
    var s = $(id);
    MONTHS.forEach(function(m,i){ var o=document.createElement("option"); o.value=i+1; o.textContent=m; s.appendChild(o); });
  });
  $("month").value = defMonth; $("start").value = 1;
  function num(id){ var v = parseFloat(String($(id).value).replace(/[,₪\\s]/g,"")); return isNaN(v) ? null : v; }
  function calc(){
    var inc = num("income"), m = +$("month").value, st = +$("start").value, plan = num("plan");
    if (st > m) { st = m; $("start").value = m; }
    var out = $("out");
    if (inc === null || inc < 0) { out.hidden = true; return; }
    out.hidden = false;
    var active = Math.max(1, m - st + 1);
    var pace = inc / active;
    var monthly = plan !== null && plan >= 0 ? plan : pace;
    var proj = inc + monthly * (12 - m);
    var used = inc / C, left = Math.max(0, C - inc);
    var perMonth = left / (13 - m);
    $("r-used").textContent = (used*100).toFixed(1) + "%%";
    $("r-left").textContent = fmt(left);
    $("r-pace").textContent = fmt(pace);
    $("r-proj").textContent = fmt(proj);
    $("r-per").textContent = fmt(perMonth);
    var bar = $("bar"); bar.style.width = Math.min(100, used*100) + "%%";
    var meter = $("meter"); meter.className = "meter" + (used >= .9 ? " danger" : used >= .7 ? " warn" : "");
    meter.setAttribute("aria-valuenow", Math.round(used*100));
    var cross;
    if (inc > C) cross = "כבר עברתם את התקרה של " + fmt(C) + ". כדאי לפנות לרואה חשבון או למשרד מע\\"מ בהקדם.";
    else if (monthly <= 0) cross = "בלי הכנסות נוספות לא תגיעו לתקרה השנה.";
    else if (proj <= C) cross = "בקצב של " + fmt(monthly) + " לחודש, צפוי לסיים את השנה בכ-" + fmt(proj) + " – מתחת לתקרה, עם מרווח של " + fmt(C - proj) + ".";
    else {
      var k = Math.ceil((C - inc) / monthly);
      var mm = Math.min(12, m + k);
      cross = "בקצב של " + fmt(monthly) + " לחודש, צפוי לעבור את התקרה בערך ב" + MONTHS[mm-1] + " 2026. מומלץ לתכנן מראש עם רואה חשבון.";
    }
    $("r-cross").textContent = cross;
    var st2 = $("status");
    var lvl = (inc > C || used >= .9) ? "danger" : (proj > C || used >= .7) ? "warn" : "success";
    st2.className = "callout " + lvl;
  }
  ["income","month","start","plan"].forEach(function(id){ $(id).addEventListener("input", calc); });
  calc();
})();
</script>
""" % CEILING


def ceiling_tool():
    faqs = [
        ("מה תקרת עוסק פטור לשנת 2026?", f"{CEILING:,} ₪ מחזור עסקאות שנתי (בשנת 2025: 120,000 ₪). מקור: {SRC_CEIL}. נבדק ב-{CHECKED}."),
        ("התקרה נמדדת לפי הכנסות או לפי רווח?", "לפי מחזור העסקאות – סך ההכנסות ברוטו מהעסק. הוצאות לא מורידות מהמחזור לצורך התקרה."),
        ("מה קורה כשעוברים את התקרה?", 'צריך לעבור למעמד עוסק מורשה ולהתחיל לגבות מע"מ. לפי המידע ב<a href="https://www.kolzchut.org.il/he/%D7%A2%D7%95%D7%A1%D7%A7_%D7%A4%D7%98%D7%95%D7%A8" rel="noopener" target="_blank">כל זכות</a>, השינוי חל כבר מהעסקה שבה נחצתה התקרה – ולכן כדאי לזהות את זה מראש ולא בדיעבד. את הפרטים המדויקים לבדוק מול רשות המסים או רואה חשבון.'),
        ("פתחתי את העסק באמצע השנה. איך המחשבון מחשב?", "בוחרים את חודש הפתיחה, והקצב החודשי מחושב רק לפי החודשים שבהם העסק פעל. את השאלה איך התקרה חלה על שנת פתיחה חלקית כדאי לבדוק עם רואה חשבון."),
        ("המחשבון שומר את המספרים שלי?", "לא. החישוב נעשה בדפדפן שלכם בלבד, ושום נתון לא נשלח לשום מקום."),
    ]
    title = "מחשבון תקרת עוסק פטור 2026 – כמה נשאר לי עד התקרה? | תכנון פלוס"
    desc = f"מחשבון חינם: מכניסים הכנסות מתחילת השנה ומקבלים כמה נשאר עד תקרת עוסק פטור 2026 ({CEILING:,} ₪), תחזית לסוף השנה ומתי צפוי לעבור אותה."
    body = f"""
<section class="section mt-0" style="padding-top:.5rem">
 <div class="container narrow">
  <h1>מחשבון תקרת עוסק פטור 2026</h1>
  <p class="lead muted">התקרה לשנת 2026 היא <strong>{CEILING:,} ₪</strong> מחזור שנתי (הכנסות ברוטו, לא רווח). הכניסו כמה הכנסתם מתחילת השנה, ותראו כמה נשאר ומתי בקצב הנוכחי תגיעו לתקרה.</p>
  <div class="tool-panel">
   <div class="fields cols-2">
    <div class="field"><label for="income">הכנסות מתחילת 2026 (₪)</label>
     <div class="input-affix"><input id="income" type="number" inputmode="decimal" min="0" step="100" placeholder="למשל 64000"><span class="affix">₪</span></div>
     <span class="hint">סך התשלומים שקיבלתם (כל הקבלות), לפני הוצאות</span></div>
    <div class="field"><label for="month">עד איזה חודש (כולל)?</label><select id="month"></select></div>
    <div class="field"><label for="start">חודש פתיחת העסק ב-2026</label><select id="start"></select><span class="hint">אם העסק פעל כל השנה – ינואר</span></div>
    <div class="field"><label for="plan">הכנסה חודשית צפויה מעכשיו (לא חובה)</label>
     <div class="input-affix"><input id="plan" type="number" inputmode="decimal" min="0" step="100" placeholder="ריק = לפי הקצב עד היום"><span class="affix">₪</span></div></div>
   </div>
   <div id="out" class="result" hidden aria-live="polite">
    <div class="label">ניצלתם מהתקרה</div>
    <div class="big" id="r-used">0%</div>
    <div class="meter mt-1" id="meter" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="ניצול התקרה"><span id="bar" style="width:0"></span></div>
    <div class="kpis mt-2">
     <div class="kpi"><div class="v" id="r-left">–</div><div class="k">נותר עד התקרה</div></div>
     <div class="kpi"><div class="v" id="r-pace">–</div><div class="k">קצב חודשי עד היום</div></div>
     <div class="kpi"><div class="v" id="r-proj">–</div><div class="k">מחזור צפוי לסוף השנה</div></div>
     <div class="kpi"><div class="v" id="r-per">–</div><div class="k">אפשר להכניס בחודש (כולל החודש)</div></div>
    </div>
    <div class="callout success" id="status"><span id="r-cross"></span></div>
   </div>
   <p class="source mt-2">מקור התקרה: {SRC_CEIL}. נבדק ב-{CHECKED}. המחשבון לצורכי מידע בלבד ואינו ייעוץ מס. החישוב מתבצע בדפדפן בלבד.</p>
  </div>

  <div class="cta-box mt-3">
   <div><h2 class="h3">רוצים את זה מתעדכן לבד כל השנה?</h2><p>קובץ האקסל לעוסק פטור 2026 עושה את החישוב הזה מכל קבלה שאתם רושמים – יחד עם יומן הוצאות, סיכום רבעוני ועזר לדוח השנתי.</p></div>
   <a class="btn accent" href="../../p/osek-patur-tracker/">לקובץ המלא – ₪39</a>
  </div>
 </div>
</section>

<section class="section alt">
 <div class="container narrow prose">
  <h2>איך המחשבון עובד</h2>
  <ul>
   <li><strong>ניצול:</strong> ההכנסות מתחילת השנה חלקי {CEILING:,} ₪.</li>
   <li><strong>קצב חודשי:</strong> ההכנסות חלקי מספר החודשים שהעסק פעל השנה (מחודש הפתיחה ועד החודש שבחרתם).</li>
   <li><strong>תחזית:</strong> ההכנסות עד היום + הקצב החודשי (או ההכנסה הצפויה שהזנתם) × החודשים שנשארו.</li>
   <li><strong>כמה אפשר להכניס בחודש:</strong> מה שנשאר עד התקרה, מחולק בחודשים שנותרו כולל החודש הנוכחי.</li>
  </ul>
  <p>רוצים להבין לעומק? קראו את <a href="../../p/osek-patur-tracker/guides/osek-patur-ceiling-2026/">המדריך לתקרת עוסק פטור 2026</a>.</p>
  <h2>שאלות נפוצות</h2>
  {faq_html(faqs)}
 </div>
</section>
"""
    page("tools/osek-patur-ceiling", title=title, desc=desc, h1="", body=body, depth=2,
         crumbs=[("ראשי", ""), ("כלים חינם", "tools/"), ("מחשבון תקרת עוסק פטור", None)],
         og_image="p/osek-patur-tracker/img/dashboard.webp", scripts=CEIL_JS,
         jsonld=[tool_ld("מחשבון תקרת עוסק פטור 2026", desc),
                 breadcrumb_ld(["ראשי", "כלים חינם", "מחשבון תקרת עוסק פטור 2026"]), faq_ld(faqs)])


# =============================================================== tool: VAT calculator
VAT_JS = """
<script>
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var r2 = function(n){ return Math.round((n + Number.EPSILON) * 100) / 100; };
  var fmt = function(n){ return "₪" + r2(n).toLocaleString("he-IL",{minimumFractionDigits:2,maximumFractionDigits:2}); };
  function num(v){ v = parseFloat(String(v).replace(/[,₪\\s]/g,"")); return isNaN(v) ? null : v; }
  function rate(){ var r = num($("rate").value); return r === null || r < 0 ? 18 : r; }
  function mode(){ return document.querySelector('input[name=mode]:checked').value; }
  function calc(){
    var a = num($("amount").value), R = rate()/100, out = $("vout");
    $("rate-label").textContent = rate() + "%";
    if (a === null) { out.hidden = true; return; }
    out.hidden = false;
    var before, vat, total;
    if (mode() === "add") { before = a; vat = r2(a * R); total = r2(before + vat); }
    else { total = a; before = r2(a / (1 + R)); vat = r2(total - before); }
    $("v-before").textContent = fmt(before); $("v-vat").textContent = fmt(vat); $("v-total").textContent = fmt(total);
    $("v-big").textContent = mode() === "add" ? fmt(total) : fmt(before);
    $("v-biglabel").textContent = mode() === "add" ? "סה\\"כ כולל מע\\"מ" : "סכום לפני מע\\"מ";
    $("v-formula").textContent = mode() === "add"
      ? a.toLocaleString("he-IL") + " × " + (1+R).toFixed(2) + " = " + total.toLocaleString("he-IL")
      : a.toLocaleString("he-IL") + " ÷ " + (1+R).toFixed(2) + " = " + before.toLocaleString("he-IL");
  }
  ["amount","rate"].forEach(function(id){ $(id).addEventListener("input", calc); });
  document.querySelectorAll("input[name=mode]").forEach(function(x){ x.addEventListener("change", calc); });
  calc();

  // quick quote
  var tbody = $("q-rows");
  function addRow(){
    var tr = document.createElement("tr");
    tr.innerHTML = '<td><input type="text" aria-label="תיאור" placeholder="תיאור"></td>' +
      '<td><input type="number" aria-label="כמות" min="0" step="any" value="1" inputmode="decimal"></td>' +
      '<td><input type="number" aria-label="מחיר ליחידה לפני מע\\"מ" min="0" step="any" placeholder="0" inputmode="decimal"></td>' +
      '<td class="num" data-sum>–</td>';
    tbody.appendChild(tr);
    tr.querySelectorAll("input").forEach(function(i){ i.addEventListener("input", quote); });
  }
  for (var i = 0; i < 3; i++) addRow();
  $("q-add").addEventListener("click", function(){ addRow(); });
  function quote(){
    var R = rate()/100, sub = 0, lines = [];
    tbody.querySelectorAll("tr").forEach(function(tr){
      var ins = tr.querySelectorAll("input"), q = num(ins[1].value), p = num(ins[2].value);
      var s = (q !== null && p !== null) ? r2(q*p) : null;
      tr.querySelector("[data-sum]").textContent = s === null ? "–" : fmt(s);
      if (s !== null) { sub += s; lines.push((ins[0].value || "פריט") + ": " + q + " × " + fmt(p) + " = " + fmt(s)); }
    });
    var d = num($("q-disc").value) || 0; var disc = r2(sub * d/100); var net = r2(sub - disc);
    var patur = $("q-patur").checked; var vat = patur ? 0 : r2(net * R); var tot = r2(net + vat);
    $("q-sub").textContent = fmt(sub); $("q-dsum").textContent = disc ? "-" + fmt(disc) : fmt(0);
    $("q-net").textContent = fmt(net); $("q-vat").textContent = patur ? "ללא (עוסק פטור)" : fmt(vat);
    $("q-tot").textContent = fmt(tot);
    $("q-copy").dataset.text = lines.join("\\n") + "\\n" + "סה\\"כ לפני מע\\"מ: " + fmt(net) + "\\n" +
      (patur ? "עוסק פטור – ללא מע\\"מ" : "מע\\"מ " + rate() + "%: " + fmt(vat)) + "\\nסה\\"כ לתשלום: " + fmt(tot);
  }
  ["q-disc","q-patur","rate"].forEach(function(id){ $(id).addEventListener("input", quote); });
  $("q-patur").addEventListener("change", quote);
  $("q-copy").addEventListener("click", function(){
    var t = this.dataset.text || "", btn = this;
    (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function(){
      btn.textContent = "הועתק ✓"; setTimeout(function(){ btn.textContent = "העתקת הסיכום"; }, 1800);
    }).catch(function(){ window.prompt("העתיקו את הסיכום:", t); });
  });
  quote();
})();
</script>
"""


VSTYLE = """<style>
.vat-kpis{grid-template-columns:1fr}
.vat-kpis .kpi{display:flex;justify-content:space-between;align-items:center;gap:.5rem}
@media (min-width:600px){.vat-kpis{grid-template-columns:repeat(3,minmax(0,1fr))}.vat-kpis .kpi{display:block}}
#q-table input[type=number]{-moz-appearance:textfield;appearance:textfield}
#q-table input::-webkit-outer-spin-button,#q-table input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
#q-table td.num{font-size:.92rem;overflow-wrap:anywhere}
#q-table{table-layout:fixed;min-width:0}
#q-table th,#q-table td{padding:.45rem .4rem}
#q-table input{min-height:42px;padding:.4rem .45rem;font-size:1rem;min-width:0}
@media (max-width:480px){#q-table th{font-size:.85rem}}
</style>"""


def vat_tool():
    faqs = [
        ("מה שיעור המע\"מ בישראל ב-2026?", f'18%. השיעור עלה מ-17% ל-18% ב-1 בינואר 2025. מקור: {SRC_VAT}. נבדק ב-{CHECKED}.'),
        ("איך מוסיפים מע\"מ למחיר?", "מכפילים ב-1.18. לדוגמה: 1,000 ₪ לפני מע\"מ × 1.18 = 1,180 ₪ כולל מע\"מ (מתוכם 180 ₪ מע\"מ)."),
        ("איך מורידים מע\"מ ממחיר כולל?", "מחלקים ב-1.18 (לא מורידים 18%!). לדוגמה: 1,180 ₪ ÷ 1.18 = 1,000 ₪. חלק המע\"מ בסכום כולל הוא 18/118 ממנו – בערך 15.25%."),
        ("למה הורדת 18% מהסכום נותנת תוצאה שגויה?", "כי ה-18% מחושבים על הסכום לפני מע\"מ ולא על הסכום הכולל. 1,180 פחות 18% זה 967.60 ₪ – כ-32 ₪ פחות מהנכון."),
        ("עוסק פטור גובה מע\"מ?", 'לא. עוסק פטור לא מוסיף מע"מ להצעות ולקבלות. לכן במחשבון הצעת המחיר יש תיבה "עוסק פטור".'),
        ("המחשבון שומר את הנתונים?", "לא. הכול מחושב בדפדפן שלכם ולא נשלח לשום מקום."),
    ]
    title = "מחשבון מע\"מ 18% – הוספה והורדה של מע\"מ בקליק | תכנון פלוס"
    desc = "מחשבון מע\"מ 18% מעודכן ל-2026: הוספת מע\"מ למחיר, הורדת מע\"מ מסכום כולל, ומחשבון הצעת מחיר מהיר עם הנחה. חינם, בלי הרשמה."
    body = f"""
<section class="section mt-0" style="padding-top:.5rem">
 <div class="container narrow">
  <h1>מחשבון מע"מ 18%</h1>
  <p class="lead muted">להוסיף מע"מ: <strong>× 1.18</strong>. להוריד מע"מ: <strong>÷ 1.18</strong>. או פשוט מקלידים סכום:</p>
  <div class="tool-panel">
   <div class="field"><span class="label">מה רוצים לחשב?</span>
    <div class="choices" role="radiogroup">
     <label><input type="radio" name="mode" value="add" checked> להוסיף מע"מ (יש לי מחיר לפני מע"מ)</label>
     <label><input type="radio" name="mode" value="remove"> להוריד מע"מ (יש לי מחיר כולל)</label>
    </div></div>
   <div class="fields cols-2">
    <div class="field"><label for="amount">סכום (₪)</label>
     <div class="input-affix"><input id="amount" type="number" inputmode="decimal" min="0" step="any" placeholder="למשל 1000"><span class="affix">₪</span></div></div>
    <div class="field"><label for="rate">שיעור מע"מ (%)</label><input id="rate" type="number" inputmode="decimal" min="0" max="100" step="0.5" value="18"><span class="hint">ברירת מחדל: 18% (בתוקף מ-1.1.2025)</span></div>
   </div>
   <div id="vout" class="result" hidden aria-live="polite">
    <div class="label" id="v-biglabel"></div>
    <div class="big" id="v-big"></div>
    <div class="kpis vat-kpis mt-2">
     <div class="kpi"><div class="v" id="v-before">–</div><div class="k">לפני מע"מ</div></div>
     <div class="kpi"><div class="v" id="v-vat">–</div><div class="k">מע"מ <span id="rate-label">18%</span></div></div>
     <div class="kpi"><div class="v" id="v-total">–</div><div class="k">כולל מע"מ</div></div>
    </div>
    <p class="small muted mt-1" id="v-formula" dir="ltr" style="direction:ltr;unicode-bidi:isolate;text-align:right"></p>
   </div>
  </div>

  <h2 class="mt-4">מחשבון הצעת מחיר מהיר</h2>
  <p class="muted">כמה שורות, הנחה, מע"מ – וסיכום שאפשר להעתיק להודעה ללקוח.</p>
  <div class="tool-panel">
   <div class="table-wrap">
    <table id="q-table"><thead><tr><th style="width:32%">תיאור</th><th style="width:14%">כמות</th><th style="width:26%">מחיר ליחידה<br><span class="small muted">לפני מע"מ</span></th><th class="num" style="width:28%">סה"כ</th></tr></thead>
    <tbody id="q-rows"></tbody></table>
   </div>
   <button class="btn secondary small mt-1" id="q-add" type="button">+ שורה</button>
   <div class="fields cols-2 mt-2">
    <div class="field"><label for="q-disc">הנחה (%)</label><input id="q-disc" type="number" min="0" max="100" step="any" value="0" inputmode="decimal"></div>
    <div class="field"><span class="label">סוג עוסק</span><div class="choices"><label><input type="checkbox" id="q-patur"> אני עוסק פטור (בלי מע"מ)</label></div></div>
   </div>
   <div class="table-wrap"><table>
    <tr><td>סכום ביניים</td><td class="num" id="q-sub">₪0.00</td></tr>
    <tr><td>הנחה</td><td class="num" id="q-dsum">₪0.00</td></tr>
    <tr><td>סה"כ לפני מע"מ</td><td class="num" id="q-net">₪0.00</td></tr>
    <tr><td>מע"מ</td><td class="num" id="q-vat">₪0.00</td></tr>
    <tr><td><strong>סה"כ לתשלום</strong></td><td class="num"><strong id="q-tot">₪0.00</strong></td></tr>
   </table></div>
   <button class="btn small mt-2" id="q-copy" type="button">העתקת הסיכום</button>
   <p class="source mt-2">שיעור המע"מ: {SRC_VAT}. נבדק ב-{CHECKED}. כלי עזר לחישוב בלבד; אינו מפיק מסמך מס. החישוב מתבצע בדפדפן בלבד.</p>
  </div>

  <div class="cta-box mt-3">
   <div><h3>צריכים הצעת מחיר מעוצבת ללקוח?</h3><p>5 תבניות הצעת מחיר בעברית (Excel + Word) שמחשבות את כל זה לבד – עם הלוגו, התנאים והחתימה שלכם, ושמירה כ-PDF.</p></div>
   <a class="btn accent" href="../../p/price-quote-pack/">לתבניות – ₪29</a>
  </div>
 </div>
</section>

<section class="section alt">
 <div class="container narrow prose">
  <h2>טבלת מע"מ מהירה (18%)</h2>
  <div class="table-wrap"><table>
   <thead><tr><th>לפני מע"מ</th><th>מע"מ</th><th>כולל מע"מ</th></tr></thead>
   <tbody>
   {"".join(f'<tr><td class="num">₪{b:,}</td><td class="num">₪{b*0.18:,.2f}</td><td class="num">₪{b*1.18:,.2f}</td></tr>' for b in (100, 250, 500, 1000, 2500, 5000, 10000))}
   </tbody></table></div>
  <h2>שאלות נפוצות</h2>
  {faq_html(faqs)}
  <p class="mt-2">עוד בנושא: <a href="../../p/price-quote-pack/guides/how-to-write-a-quote/">איך לכתוב הצעת מחיר שסוגרת עסקה</a> · <a href="../../p/price-quote-pack/guides/quote-vs-invoice/">הצעת מחיר מול חשבונית מס</a> · <a href="../osek-patur-ceiling/">מחשבון תקרת עוסק פטור</a></p>
 </div>
</section>
"""
    page("tools/vat-calculator", title=title, desc=desc, h1="", body=body, depth=2, extra_head=VSTYLE,
         crumbs=[("ראשי", ""), ("כלים חינם", "tools/"), ("מחשבון מע\"מ", None)],
         og_image="p/price-quote-pack/img/all-designs.webp", scripts=VAT_JS,
         jsonld=[tool_ld("מחשבון מע\"מ 18%", desc), breadcrumb_ld(["ראשי", "כלים חינם", "מחשבון מע\"מ"]), faq_ld(faqs)])


# =============================================================== guides
def guide(path, slug_name, crumbs, title, desc, h1, content, cta_href, cta_title, cta_text, cta_btn):
    body = f"""
<article class="section mt-0" style="padding-top:.5rem">
 <div class="container narrow prose">
  <h1>{h1}</h1>
  <p class="updated">עודכן: {CHECKED} · מדריך כללי, אינו ייעוץ מס או ייעוץ משפטי</p>
  {content}
  <div class="cta-box mt-4">
   <div><h3>{cta_title}</h3><p>{cta_text}</p></div>
   <a class="btn accent" href="{cta_href}">{cta_btn}</a>
  </div>
 </div>
</article>
"""
    page(path, title=title, desc=desc, h1=h1, body=body, depth=4, crumbs=crumbs,
         jsonld=[article_ld(h1, desc), breadcrumb_ld([c[0] for c in crumbs])])


def guides():
    oc = [("ראשי", ""), ("מעקב עוסק פטור 2026", "p/osek-patur-tracker/")]
    guide("p/osek-patur-tracker/guides/osek-patur-ceiling-2026", "", oc + [("תקרת עוסק פטור 2026", None)],
          "תקרת עוסק פטור 2026: 122,833 ₪ – איך מחשבים ומה קורה כשעוברים | תכנון פלוס",
          "תקרת עוסק פטור לשנת 2026 היא 122,833 ₪. מה נכלל במחזור, איך לעקוב במהלך השנה, מה קורה כשעוברים את התקרה ואיך לתכנן מראש.",
          "תקרת עוסק פטור 2026: כמה היא, איך מחשבים ומה קורה כשעוברים",
          f"""
<div class="callout"><strong>בקצרה:</strong> בשנת 2026 עוסק פטור יכול להגיע למחזור עסקאות של עד <strong>{CEILING:,} ₪</strong> בשנה (בשנת 2025 התקרה הייתה 120,000 ₪). המחזור נמדד לפי סך ההכנסות ברוטו – לא לפי הרווח.<br><span class="source">מקור: {SRC_CEIL}. נבדק ב-{CHECKED}.</span></div>

<h2>מה זה בעצם "התקרה"?</h2>
<p>עוסק פטור הוא עסק קטן שפטור מגביית מע"מ מהלקוחות. הפטור הזה מוגבל בגודל: כל עוד מחזור העסקאות השנתי שלכם נמוך מהתקרה, אתם יכולים להישאר עוסק פטור. התקרה מתעדכנת בדרך כלל בינואר לפי המדד, אבל לא בכל שנה (ב-2024 וב-2025 היא נשארה 120,000 ₪), ולכן חשוב לבדוק את הסכום המעודכן בכל שנה מחדש.</p>

<h2>מה נספר במחזור – ומה לא</h2>
<ul>
 <li><strong>נספר:</strong> כל ההכנסות מהעסק – כל תשלום שקיבלתם על עבודה, שירות או מוצר, בכל אמצעי תשלום (העברה, ביט, אשראי, מזומן, צ'ק, PayPal).</li>
 <li><strong>לא מקטין את המחזור:</strong> הוצאות. גם אם הוצאתם 40,000 ₪ על ציוד ושיווק, המחזור לצורך התקרה הוא עדיין סך ההכנסות.</li>
 <li><strong>שווה לבדוק עם רו"ח:</strong> מקרים מיוחדים כמו מכירת ציוד של העסק, הכנסות מכמה עיסוקים שונים או תקבולים מחו"ל.</li>
</ul>

<h2>דוגמה: האם אני בדרך לעבור?</h2>
<p>נניח שעד סוף אוגוסט הכנסתם 80,000 ₪. זה קצב של 10,000 ₪ לחודש. אם הקצב נשמר, בסוף דצמבר תגיעו ל-120,000 ₪ – מתחת ל-{CEILING:,} ₪, אבל עם מרווח של פחות מ-3,000 ₪. מספיק פרויקט אחד גדול בדצמבר כדי לעבור. את החישוב הזה עושה בשבילכם <a href="../../../../tools/osek-patur-ceiling/">מחשבון תקרת עוסק פטור</a>.</p>

<h2>מה קורה כשעוברים את התקרה</h2>
<p>מי שעובר את התקרה צריך לעבור למעמד <strong>עוסק מורשה</strong>: להתחיל לגבות מע"מ מהלקוחות, להוציא חשבוניות מס ולהגיש דיווחי מע"מ תקופתיים. לפי המידע באתר כל זכות, המעבר חל כבר <strong>מהעסקה שבה נחצתה התקרה</strong> – כלומר זה לא משהו שמטפלים בו "בשנה הבאה". על החובה להודיע למשרד מע"מ ועל המועדים המדויקים כדאי לבדוק מול רשות המסים או עם רואה חשבון.</p>
<p>שימו לב גם ש<strong>יש מקצועות שלא יכולים להיות עוסק פטור בכלל</strong>, בלי קשר להיקף ההכנסות (למשל חלק מבעלי המקצועות החופשיים כמו עורכי דין, רואי חשבון, יועצי מס, אדריכלים ומהנדסים). אם אתם לא בטוחים – בדקו לפני הרישום.</p>

<h2>איך לא להיתפס לא מוכנים</h2>
<ol>
 <li><strong>רשמו כל קבלה בזמן אמת</strong> – לא בסוף השנה. כך תמיד תדעו את המחזור המצטבר.</li>
 <li><strong>הסתכלו על הקצב, לא רק על הסכום.</strong> 60% מהתקרה ביוני זה מצב אחר לגמרי מ-60% בנובמבר.</li>
 <li><strong>הגדירו "קו אזהרה"</strong> – למשל 70% מהתקרה – ותכננו מראש מה עושים כשמגיעים אליו.</li>
 <li><strong>שקלו מעבר מתוכנן.</strong> לפעמים עדיף לעבור לעוסק מורשה מראש, בתחילת שנה או בתחילת התקשרות עם לקוח גדול. זו החלטה שכדאי לקבל עם רואה חשבון.</li>
 <li><strong>בסוף השנה</strong> – עוסק פטור מגיש הצהרה שנתית על מחזור העסקאות למע"מ (בדרך כלל עד סוף ינואר של השנה שאחרי). את המועד המדויק בודקים באתר רשות המסים.</li>
</ol>

<h2>שאלות קצרות</h2>
<p><strong>התקרה היא לשנה קלנדרית?</strong> כן, מינואר עד דצמבר.<br>
<strong>מע"מ על הוצאות – אפשר לקזז?</strong> לא. עוסק פטור לא גובה מע"מ ולכן גם לא מקזז מע"מ תשומות. ההוצאה נרשמת בסכום המלא ששילמתם.<br>
<strong>יש עוד תקרות שצריך להכיר?</strong> כן – למשל מסלול «בעל עסק זעיר» במס הכנסה (ניכוי נורמטיבי של 30% מהמחזור ודוח מקוצר). הוא משתמש באותה תקרת מחזור (122,833 ₪ ב-2026), אבל זה מסלול של מס הכנסה ולא של מע"מ, וההצטרפות אליו נפרדת.</p>
<p class="source">המידע במדריך כללי ועשוי להשתנות. הוא אינו ייעוץ מס. לכל החלטה – רואה חשבון או יועץ מס, ואתר רשות המסים.</p>
""",
          "../../", "מד תקרה שמתעדכן מכל קבלה", "קובץ האקסל לעוסק פטור 2026 מראה בכל רגע כמה ניצלתם מהתקרה, מתי בקצב הנוכחי תעברו אותה, וכמה אפשר להכניס בחודש.", "לקובץ – ₪39")

    guide("p/osek-patur-tracker/guides/income-expense-tracking", "", oc + [("ניהול הכנסות והוצאות", None)],
          "איך לנהל הכנסות והוצאות כעוסק פטור – מדריך מעשי | תכנון פלוס",
          "מדריך מעשי לעוסק פטור: איך לרשום הכנסות והוצאות, אילו פרטים לשמור, איך לטפל בהוצאות מעורבות ומה להכין לסוף השנה. כולל רשימת בדיקה.",
          "איך לנהל הכנסות והוצאות כעוסק פטור – מדריך מעשי",
          f"""
<p>רוב העצמאים הקטנים לא נכשלים בגלל חוסר ידע, אלא בגלל חוסר סדר: קבלות בפנקס, העברות בבנק, הוצאות בתמונות בטלפון – ובסוף השנה מנסים לחבר הכול. המדריך הזה מציע שיטה פשוטה של 10 דקות בשבוע.</p>

<h2>1. יומן הכנסות: שורה לכל קבלה</h2>
<p>כל תשלום שמתקבל = קבלה (בפנקס קבלות ממוספר או בתוכנה הרשומה ברשות המסים) = שורה ביומן. מספיקות 6 עמודות:</p>
<div class="table-wrap"><table>
 <thead><tr><th>עמודה</th><th>למה צריך אותה</th></tr></thead>
 <tbody>
  <tr><td>תאריך קבלת התשלום</td><td>לסיכום חודשי ולמעקב תקרה</td></tr>
  <tr><td>מספר קבלה</td><td>להתאמה מול הפנקס / התוכנה בסוף השנה</td></tr>
  <tr><td>לקוח</td><td>לדעת מי הלקוחות הגדולים</td></tr>
  <tr><td>תיאור העבודה</td><td>לזכור על מה התשלום</td></tr>
  <tr><td>אמצעי תשלום</td><td>להתאמה מול דפי הבנק והאשראי</td></tr>
  <tr><td>סכום</td><td>מחזור, תקרה, רווח</td></tr>
 </tbody></table></div>
<p>טיפ: רשמו לפי <strong>תאריך קבלת הכסף</strong>, וכשקיבלתם צ'ק דחוי – בדקו עם רו"ח איך לרשום אותו.</p>

<h2>2. יומן הוצאות: גם ההוצאות הקטנות</h2>
<p>הוצאות לא מקטינות את המחזור לצורך תקרת עוסק פטור, אבל הן כן משפיעות על הרווח שעליו משלמים מס הכנסה וביטוח לאומי. לכל הוצאה רשמו תאריך, ספק, קטגוריה, סכום ששולם (כולל מע"מ – עוסק פטור לא מקזז מע"מ) – ו<strong>שמרו את המסמך</strong>. צילום ברור בטלפון שמגובה בענן הוא התחלה טובה.</p>
<p>קטגוריות נפוצות: ציוד ומחשבים, תוכנות ומנויים, פרסום ושיווק, רכב ונסיעות, טלפון ואינטרנט, שכירות/משרד, השתלמויות, הנהלת חשבונות, ביטוחים.</p>

<h2>3. הוצאות מעורבות: טלפון, רכב, חדר בבית</h2>
<p>יש הוצאות שמשמשות גם את העסק וגם אתכם באופן פרטי. במקרים כאלה רק <strong>חלק</strong> מההוצאה מוכר. השיעורים תלויים בכללים של רשות המסים ובנסיבות שלכם – אל תנחשו, שאלו את רואה החשבון פעם אחת ורשמו את האחוז ביומן. בקובץ שלנו יש עמודת "% מוכר" בדיוק בשביל זה.</p>

<h2>4. השגרה השבועית (10 דקות)</h2>
<ol>
 <li>עוברים על דף הבנק / האפליקציה ומוודאים שלכל תשלום שנכנס יש קבלה ושורה ביומן.</li>
 <li>מעלים צילומי חשבוניות של הוצאות השבוע ורושמים אותן.</li>
 <li>מציצים במעקב התקרה: כמה ניצלתם, ומה הקצב.</li>
</ol>

<h2>5. סוף רבעון וסוף שנה</h2>
<p>בסוף כל רבעון כדאי לראות הכנסות, הוצאות ורווח – זה עוזר להבין אם המקדמות למס הכנסה ולביטוח לאומי מתאימות. בסוף השנה מכינים:</p>
<ul>
 <li>מחזור שנתי – להצהרה השנתית למע"מ (בדרך כלל עד סוף ינואר; בודקים מועד מדויק באתר רשות המסים).</li>
 <li>סיכום הוצאות לפי קטגוריה ורווח – לדוח השנתי למס הכנסה, אם אתם חייבים בהגשה.</li>
 <li>אישורים שנתיים: הפקדות לפנסיה וקרן השתלמות, ניכוי מס במקור מלקוחות, טופס 867 מהבנק אם רלוונטי.</li>
 <li>התאמה: מספר הקבלות ביומן מול הפנקס או התוכנה.</li>
</ul>

<h2>Excel או אפליקציה?</h2>
<p>אפליקציות להפקת קבלות נוחות, אבל לא תמיד נותנות תמונה של תקרה, קצב ורווח. גיליון מסודר שנותן את התמונה הזו – בלי מנוי חודשי – הוא השלמה טובה. אם אתם כבר עובדים עם תוכנה, אפשר לייצא ממנה את רשימת הקבלות ולהדביק ליומן.</p>
<p class="source">המדריך כללי ואינו ייעוץ מס. חובות הדיווח והמועדים משתנים – בדקו מול רשות המסים או רואה חשבון.</p>
""",
          "../../", "כל זה כבר בנוי בקובץ אחד", "יומן הכנסות והוצאות, אחוז מוכר, סיכום רבעוני, מד תקרה ועזר לדוח השנתי – בקובץ אקסל אחד בעברית.", "לקובץ – ₪39")

    qc = [("ראשי", ""), ("תבניות הצעת מחיר", "p/price-quote-pack/")]
    guide("p/price-quote-pack/guides/how-to-write-a-quote", "", qc + [("איך לכתוב הצעת מחיר", None)],
          "איך לכתוב הצעת מחיר: מבנה, דוגמה וטעויות נפוצות | תכנון פלוס",
          "איך לכתוב הצעת מחיר מקצועית בעברית: 9 החלקים שחייבים להופיע, דוגמה מלאה עם מע\"מ 18%, תנאי תשלום, תוקף וטעויות שעולות כסף.",
          "איך לכתוב הצעת מחיר שסוגרת עסקה – מבנה, דוגמה וטעויות נפוצות",
          """
<p>הצעת מחיר טובה עושה שני דברים: עוזרת ללקוח להגיד "כן" מהר, ומגינה עליכם כשמשהו לא ברור בהמשך. הנה המבנה שעובד.</p>

<h2>9 החלקים של הצעת מחיר</h2>
<ol>
 <li><strong>פרטי העסק:</strong> שם, סוג עוסק ומספר, טלפון ומייל. לוגו אם יש.</li>
 <li><strong>פרטי הלקוח:</strong> שם החברה/הלקוח ואיש הקשר.</li>
 <li><strong>מספר הצעה ותאריך:</strong> כדי שתוכלו להפנות אליה ("לפי הצעה 1024").</li>
 <li><strong>תוקף:</strong> "בתוקף עד" – רבים קובעים 14–30 יום. זה מגן עליכם משינויי מחירים.</li>
 <li><strong>נושא:</strong> משפט אחד שמסכם את העבודה.</li>
 <li><strong>פירוט שורות:</strong> תיאור, כמות, יחידה, מחיר ליחידה וסה"כ. פירוט ברור מונע ויכוחים.</li>
 <li><strong>סיכום:</strong> סכום ביניים, הנחה (אם יש), סה"כ לפני מע"מ, מע"מ וסה"כ לתשלום.</li>
 <li><strong>תנאים:</strong> תנאי תשלום, לוח זמנים, מה כלול ומה לא, כמה סבבי תיקונים.</li>
 <li><strong>אישור וחתימה:</strong> מקום לחתימת הלקוח – אישור כתוב הוא הבסיס לעבודה.</li>
</ol>

<h2>דוגמה מלאה</h2>
<div class="table-wrap"><table>
 <thead><tr><th>תיאור</th><th>כמות</th><th>מחיר ליחידה</th><th class="num">סה"כ</th></tr></thead>
 <tbody>
  <tr><td>עיצוב לוגו – 3 סקיצות + 2 סבבי תיקונים</td><td>1</td><td>1,800 ₪</td><td class="num">1,800.00 ₪</td></tr>
  <tr><td>עיצוב כרטיס ביקור דו-צדדי</td><td>1</td><td>450 ₪</td><td class="num">450.00 ₪</td></tr>
  <tr><td>דף נחיתה – עיצוב ובנייה</td><td>1</td><td>3,200 ₪</td><td class="num">3,200.00 ₪</td></tr>
  <tr><td>שעת ייעוץ שיווקי</td><td>3</td><td>280 ₪</td><td class="num">840.00 ₪</td></tr>
  <tr><td colspan="3">סכום ביניים</td><td class="num">6,290.00 ₪</td></tr>
  <tr><td colspan="3">הנחה 5%</td><td class="num">-314.50 ₪</td></tr>
  <tr><td colspan="3">סה"כ לפני מע"מ</td><td class="num">5,975.50 ₪</td></tr>
  <tr><td colspan="3">מע"מ 18%</td><td class="num">1,075.59 ₪</td></tr>
  <tr><td colspan="3"><strong>סה"כ לתשלום</strong></td><td class="num"><strong>7,051.09 ₪</strong></td></tr>
 </tbody></table></div>
<p>עוסק פטור? אז אין שורת מע"מ, וכדאי לכתוב במפורש "עוסק פטור – ללא מע"מ" כדי שהלקוח לא יחשוב ששכחתם. רוצים לבדוק חישוב? <a href="../../../../tools/vat-calculator/">מחשבון המע"מ</a> כולל מחשבון הצעת מחיר מהיר.</p>

<h2>תנאי תשלום שכדאי לשקול</h2>
<ul>
 <li>מקדמה עם אישור ההצעה (מקובל אצל רבים: 30%–50%) והיתרה במסירה.</li>
 <li>לפרויקטים ארוכים: תשלום לפי אבני דרך.</li>
 <li>"עבודה נוספת מעבר למפורט תתומחר בנפרד" – המשפט שחוסך הכי הרבה ויכוחים.</li>
 <li>המחירים בשקלים, ומצוין אם הם כוללים מע"מ או לא.</li>
</ul>
<p>אלה דוגמאות נפוצות ולא ייעוץ משפטי. בעסקאות גדולות או מורכבות כדאי שעורך דין יעבור על התנאים.</p>

<h2>7 טעויות שעולות כסף</h2>
<ol>
 <li><strong>לא לציין אם המחיר כולל מע"מ.</strong> 18% זה הבדל גדול מדי בשביל "הבנתי אחרת".</li>
 <li><strong>"עיצוב לוגו" בלי מספר סקיצות ותיקונים.</strong> בלי גבול – יש סבב עשירי.</li>
 <li><strong>בלי תוקף.</strong> לקוח שחוזר אחרי חצי שנה מצפה לאותו מחיר.</li>
 <li><strong>הורדת מע"מ בטעות.</strong> כדי לחלץ מחיר לפני מע"מ מסכום כולל מחלקים ב-1.18, לא מורידים 18%.</li>
 <li><strong>הנחה בלי לפרט.</strong> הראו את המחיר המלא ואת ההנחה – זה מראה ללקוח מה הוא מקבל.</li>
 <li><strong>שליחה כקובץ עריכה.</strong> שלחו PDF, לא Word/Excel שאפשר לשנות.</li>
 <li><strong>להתייחס להצעה כאל חשבונית.</strong> הצעת מחיר אינה מסמך מס. אחרי העסקה מפיקים קבלה או חשבונית מס כחוק – <a href="../quote-vs-invoice/">כאן ההסבר המלא</a>.</li>
</ol>
""",
          "../../", "5 תבניות מוכנות עם חישוב אוטומטי", "כל המבנה הזה כבר בנוי: פרטי עסק פעם אחת, שורות, הנחה, מע\"מ 18%, תוקף וחתימה. Excel + Word, עמוד A4 אחד.", "לתבניות – ₪29")

    guide("p/price-quote-pack/guides/quote-vs-invoice", "", qc + [("הצעת מחיר מול חשבונית", None)],
          "הצעת מחיר, חשבון עסקה, קבלה וחשבונית מס – מה ההבדל? | תכנון פלוס",
          "מה ההבדל בין הצעת מחיר, חשבון עסקה, קבלה וחשבונית מס? מי מוציא מה (עוסק פטור / מורשה), מתי, ומה זה מספר הקצאה. הסבר פשוט עם טבלה.",
          "הצעת מחיר, חשבון עסקה, קבלה וחשבונית מס – מה ההבדל?",
          f"""
<p>ארבעה מסמכים שנראים דומים, אבל רק לחלק מהם יש משמעות מבחינת מס. ההבדל חשוב במיוחד אם אתם משתמשים בתבניות.</p>

<h2>הטבלה בקצרה</h2>
<div class="table-wrap"><table>
 <thead><tr><th>מסמך</th><th>מתי</th><th>מסמך מס?</th><th>מי מוציא</th></tr></thead>
 <tbody>
  <tr><td><strong>הצעת מחיר</strong></td><td>לפני העבודה – מה תעשו ובכמה</td><td>לא</td><td>כל עסק</td></tr>
  <tr><td><strong>חשבון עסקה</strong></td><td>דרישת תשלום, לפני שהכסף התקבל</td><td>לא</td><td>בעיקר עוסק מורשה</td></tr>
  <tr><td><strong>קבלה</strong></td><td>אחרי שהתקבל תשלום</td><td>כן</td><td>כל עסק (עוסק פטור מוציא קבלות)</td></tr>
  <tr><td><strong>חשבונית מס</strong></td><td>על עסקה חייבת במע"מ</td><td>כן</td><td>עוסק מורשה / חברה בלבד</td></tr>
 </tbody></table></div>

<h2>הצעת מחיר</h2>
<p>הצעה ללקוח: מה תעשו, באיזה מחיר, באילו תנאים ועד מתי ההצעה בתוקף. אין לה משמעות מבחינת מס, ולכן אפשר להכין אותה בכל כלי – Excel, Word או Google Docs. היא כן יכולה להיות חשובה מבחינה עסקית ומשפטית, במיוחד אם הלקוח חתם עליה. לכן כדאי לכתוב אותה ברור – <a href="../how-to-write-a-quote/">איך כותבים הצעת מחיר טובה</a>.</p>

<h2>חשבון עסקה</h2>
<p>"דרישת תשלום" שעוסק מורשה שולח לפני שהלקוח שילם. היא לא חשבונית מס, ולכן הלקוח לא יכול לקזז לפיה מע"מ. כשהתשלום מתקבל, מוציאים חשבונית מס (או חשבונית מס/קבלה).</p>

<h2>קבלה</h2>
<p>אישור שקיבלתם כסף. <strong>עוסק פטור</strong> מוציא קבלות על כל תשלום שמתקבל – זה המסמך העיקרי שלו. את הקבלות מפיקים בפנקס או בתוכנה שעומדים בדרישות רשות המסים, לא בתבנית חופשית.</p>

<h2>חשבונית מס</h2>
<p>המסמך שמאפשר ללקוח שהוא עוסק מורשה לקזז את המע"מ ששילם. רק עוסק מורשה או חברה מוציאים חשבונית מס – עוסק פטור לא. גם אותה מפיקים בתוכנה או בפנקס מאושרים.</p>
<div class="callout warn"><strong>מספר הקצאה:</strong> חשבוניות מס בין עוסקים מעל סכום מסוים חייבות "מספר הקצאה" מרשות המסים, כדי שהלקוח יוכל לקזז את המע"מ. הסף ירד בהדרגה – ולפי הפרסומים, מיוני 2026 הוא חל על חשבוניות מעל 5,000 ₪ לפני מע"מ. זו עוד סיבה להפיק חשבוניות בתוכנה שמחוברת למערכת. בדקו את הסף העדכני ב<a href="https://www.gov.il/he/service/request-assignment-number-for-tax-invoice" rel="noopener" target="_blank">אתר רשות המסים</a>.</div>

<h2>אז מה מותר לעשות עם תבנית?</h2>
<ul>
 <li>✅ הצעות מחיר – בדיוק בשביל זה יש תבניות.</li>
 <li>✅ סיכום עבודה / פירוט שעות ללקוח, כנספח.</li>
 <li>❌ קבלות וחשבוניות מס – רק בתוכנה או בפנקס מאושרים.</li>
</ul>
<p>בכל התבניות שלנו כתוב בתחתית: "מסמך זה הוא הצעת מחיר בלבד ואינו חשבונית מס או קבלה".</p>

<h2>ומה עם מע"מ בהצעת המחיר?</h2>
<p>עוסק מורשה או חברה – מציינים את המחיר לפני מע"מ, את המע"מ (18% מאז 1.1.2025) ואת הסה"כ. עוסק פטור – לא מוסיף מע"מ, וכדאי לכתוב זאת במפורש. לחישוב מהיר: <a href="../../../../tools/vat-calculator/">מחשבון מע"מ 18%</a>.</p>
<p class="source">שיעור המע"מ: {SRC_VAT}. המדריך כללי ואינו ייעוץ מס או ייעוץ משפטי; הכללים משתנים – בדקו מול רשות המסים או רואה חשבון. עודכן {CHECKED}.</p>
""",
          "../../", "תבניות הצעת מחיר בעברית – בלי לבלבל עם חשבונית", "5 עיצובים, מע\"מ 18% אוטומטי (או בלי מע\"מ לעוסק פטור), תוקף, תנאים וחתימה. Excel + Word.", "לתבניות – ₪29")


if __name__ == "__main__":
    osek_product()
    quote_product()
    ceiling_tool()
    vat_tool()
    guides()
