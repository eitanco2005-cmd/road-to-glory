from common import BASE, UPDATED, breadcrumb_ld, breadcrumbs, esc, faq_html, faq_ld, page

SHOT_CAPTIONS = ["דשבורד: ימים לאירוע, תקציב, תשלומים, אישורי הגעה ומאזן מתנות",
                 "תקציב: חלוקה מקובלת, תכנון מול התחייבות בפועל ומה שולם",
                 "מוזמנים: אישורי הגעה, שולחן, סכום וסוג מתנה ומעקב תודות",
                 "לוח תשלומים: איחורים באדום, תשלומים קרובים בכתום",
                 "צ'קליסט עם תאריכי יעד שמחושבים מתאריך האירוע",
                 "עוזר הושבה: תפוסה לכל שולחן וחריגות"]

ICONS = {
    "money": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12v10H4V12M2 7h20v5H2zM12 22V7M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
    "table": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><circle cx="12" cy="3" r="1.5"/><circle cx="12" cy="21" r="1.5"/><circle cx="3" cy="12" r="1.5"/><circle cx="21" cy="12" r="1.5"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/></svg>',
}


def feature(icon, h, p):
    return f'<div class="feature"><div class="ic">{ICONS[icon]}</div><div><h3>{h}</h3><p>{p}</p></div></div>'


def build_product(c):
    path = f"p/{c['slug']}"
    bc = breadcrumbs([("דף הבית", "../../"), ("מוצרים", "../../products/"), (c["crumb"], None)])
    shots = "\n".join(
        f'<figure><a href="img/screen-{i}.webp" target="_blank" rel="noopener"><img src="img/screen-{i}.webp" '
        f'alt="{esc(c["shot_alt"])} – {esc(cap)}" loading="lazy" width="1100" height="650"></a>'
        f'<figcaption>{esc(cap)}</figcaption></figure>'
        for i, cap in enumerate(SHOT_CAPTIONS, start=1))
    feats = "\n".join(feature(*f) for f in c["features"])
    points = "".join(f"<li>{p}</li>" for p in c["points"])
    guides = "".join(f'<li><a href="guides/{g}/">{esc(t)}</a></li>' for g, t in c["guides"])
    body = f"""
<section class="hero">
 <div class="container">
  {bc}
  <div class="split">
   <div>
    <h1>{c['h1']}</h1>
    <p class="lead">{c['one_liner']}</p>
   </div>
   <div id="buy" class="buy" data-product="{c['slug']}" data-compact="1"></div>
   <div>
    <ul class="hero-points">{points}</ul>
    <p class="mt-2">{c['lead']}</p>
    <p class="small muted">{c['eyebrow']} · <a href="#screens">צילומי מסך ↓</a> · <a href="#inside">מה בפנים ↓</a></p>
   </div>
  </div>
 </div>
</section>

<section class="section alt" id="screens">
 <div class="container">
  <div class="section-head"><h2>ככה זה נראה</h2><p class="muted">צילומי מסך מקובץ הדוגמה הממולא שמגיע עם המוצר (שמות ונתונים בדויים).</p></div>
  <div class="screens">
{shots}
  </div>
 </div>
</section>

<section class="section" id="inside">
 <div class="container">
  <div class="section-head"><h2>מה מקבלים</h2><p class="muted">{c['inside_intro']}</p></div>
  <div class="grid cols-2">
{feats}
  </div>
  <div class="callout mt-3">
   <strong>בחבילה להורדה:</strong> {c['files_text']}
  </div>
 </div>
</section>

<section class="section alt">
 <div class="container">
  <div class="section-head"><h2>איך זה עובד</h2></div>
  <ol class="steps">
   <li><h3>קונים ומורידים</h3><p>תשלום ב-PayPal, ומיד אחריו עמוד הורדה עם כל הקבצים.</p></li>
   <li><h3>ממלאים הגדרות</h3><p>תאריך, מחיר מנה ותקציב – 5 דקות, והכל מתחבר.</p></li>
   <li><h3>מעדכנים תוך כדי</h3><p>ספקים, תשלומים, אישורי הגעה ומתנות. הדשבורד מתעדכן לבד.</p></li>
  </ol>
 </div>
</section>

<section class="section">
 <div class="container narrow">
  <h2>למי זה מתאים?</h2>
  {c['who']}
  <h2 class="mt-3">שאלות נפוצות</h2>
  {faq_html(c['faqs'])}
 </div>
</section>

<section class="section alt">
 <div class="container narrow">
  <div class="cta-box">
   <div><h2 style="font-size:1.25rem">חבילת אירועים: חתונה + בר/בת מצווה</h2>
   <p>שני המתכננים המלאים ב-₪69 במקום ₪88. מתאים למשפחות עם כמה שמחות בדרך.</p></div>
   <div style="min-width:min(100%,320px)"><div class="buy" data-product="event-bundle" data-compact="1"></div></div>
  </div>
  <h2 class="mt-4" style="font-size:1.3rem">מדריכים ומחשבונים חינם</h2>
  <ul>
   <li><a href="../../tools/{c['tool']}/">{c['tool_label']}</a></li>
   {guides}
   <li><a href="../{c['other_slug']}/">{c['other_label']}</a></li>
  </ul>
 </div>
</section>

<div class="buy-bar"><span><strong>{c['crumb']}</strong> · <span class="price">₪{c['price']}</span></span><a class="btn small" href="#buy">לרכישה</a></div>
"""
    ld = [
        {"@type": "Product", "name": c["ld_name"], "description": c["desc"], "sku": c["slug"],
         "brand": {"@type": "Brand", "name": "Glory"}, "category": "תבניות אקסל / Google Sheets",
         "image": [BASE + f"{path}/img/screen-{i}.png" for i in range(1, 5)],
         "offers": {"@type": "Offer", "price": str(c["price"]), "priceCurrency": "ILS",
                    "availability": "https://schema.org/InStock", "url": BASE + path + "/",
                    "priceValidUntil": "2027-12-31"}},
        breadcrumb_ld([("דף הבית", ""), ("מוצרים", "products/"), (c["crumb"], path + "/")]),
        faq_ld(c["faqs"]),
    ]
    scripts = '<script src="../../assets/checkout.js"></script>\n'
    return page(path, c["title"], c["desc"], body, ld, og_image=BASE + f"{path}/img/screen-1.png", scripts=scripts)


COMMON_FAQ_TAIL = [
    ("זה עובד ב-Google Sheets?",
     "כן. הקובץ נבנה כך שכל הנוסחאות, הרשימות הנפתחות והעיצוב המותנה עובדים גם ב-Google Sheets: מעלים ל-Google Drive ופותחים עם Google Sheets. "
     "כך אפשר לעבוד עליו יחד מכמה טלפונים."),
    ("יש פקודות מאקרו? צריך להתקין משהו?",
     "לא. רק נוסחאות רגילות של Excel, בלי מאקרו ובלי תוספים. עובד ב-Excel 2016 ומעלה, Excel 365, Excel לטלפון, Google Sheets ו-LibreOffice."),
    ("אפשר לקבל החזר?",
     "מדובר במוצר דיגיטלי שמועבר מיד להורדה. פרטים מלאים ב<a href=\"../../legal/refund/\">מדיניות הביטולים</a>. אם משהו בקובץ לא עובד – נתקן."),
    ("זה כולל ייעוץ או המלצה פיננסית?",
     "לא. אחוזי החלוקה וסכומי הדוגמה הם כללי אצבע להתמצאות. המחירים בפועל תלויים בספקים, באזור ובעונה."),
]

WEDDING = dict(
    slug="wedding-planner", price=49, crumb="מתכנן חתונה", other_slug="bar-mitzvah-planner",
    other_label="מתכנן בר / בת מצווה (₪39)", tool="wedding-gift", tool_label="מחשבון: כמה לשים בחתונה 2026",
    title="מתכנן חתונה באקסל ו-Google Sheets – תקציב, מוזמנים וצ'קים | Glory",
    desc="קובץ אקסל לתכנון חתונה בעברית: תקציב מול ספקים, רשימת מוזמנים ואישורי הגעה, רישום צ'קים ותודות, לוח תשלומים, צ'קליסט והושבה. עובד גם ב-Google Sheets. ₪49, הורדה מיידית.",
    ld_name="מתכנן חתונה באקסל ו-Google Sheets", shot_alt="מתכנן חתונה באקסל",
    eyebrow="אקסל + Google Sheets · ₪49 · הורדה מיידית",
    one_liner="תקציב, מוזמנים, צ'קים, ספקים ותשלומים – קובץ אקסל / Google Sheets אחד בעברית שמסדר את כל החתונה.",
    h1="מתכנן חתונה באקסל: <span class=\"hl\">כל החתונה בקובץ אחד</span>",
    lead="תקציב, ספקים ותשלומים, רשימת מוזמנים עם אישורי הגעה, רישום צ'קים ותודות, צ'קליסט והושבה. "
         "ממלאים פעם אחת, והדשבורד מראה בכל רגע כמה התחייבתם, כמה שילמתם, מי עוד לא אישר הגעה – והאם המתנות יכסו את האירוע.",
    points=["עברית מלאה, מימין לשמאל", "עובד גם ב-Google Sheets", "בלי מאקרו", "קובץ דוגמה ממולא"],
    inside_intro="9 גיליונות מחוברים זה לזה: מה שמעדכנים במקום אחד מתעדכן בכל השאר.",
    features=[
        ("chart", "דשבורד חי", "ימים לחתונה, תקציב מתוכנן מול התחייבויות, שולם ויתרה, תשלומים באיחור ובשבועיים הקרובים, שיעור אישורי הגעה ומאזן מתנות."),
        ("money", "תקציב לפי 13 קטגוריות", "עם חלוקה מקובלת לפי תקרת התקציב שלכם, תכנון מול התחייבות בפועל, והתראה באדום על חריגה."),
        ("users", "מוזמנים ואישורי הגעה", "שורה לכל הזמנה, לפי צד וקבוצה, סטטוס הגעה ומספר מאשרים. עד 400 הזמנות, עם סינון."),
        ("gift", "רישום צ'קים ומתנות", "סכום וסוג המתנה (צ'ק, ביט, העברה), וסימון כתום עד ששולחים תודה. ממוצע מתנה לאורח מחושב לבד."),
        ("cal", "ספקים ולוח תשלומים", "הצעות מחיר, מחיר סופי, מקדמות ויתרות עם תאריכי יעד. איחורים נצבעים באדום."),
        ("check", "צ'קליסט של 38 משימות", "מכ-14 חודשים לפני ועד אחרי החתונה, עם תאריכי יעד שמחושבים אוטומטית מתאריך האירוע."),
        ("table", "עוזר הושבה", "מספר שולחן לכל הזמנה, ותמונת תפוסה לכל שולחן כולל חריגות ומי עוד לא שובץ."),
        ("doc", "נוסחים מוכנים (Word)", "שמרו את התאריך, בקשת אישור הגעה, תזכורת יום לפני והודעות תודה, לוח זמנים ליום החתונה וצ'קליסט להדפסה."),
    ],
    files_text="מתכנן החתונה (Excel ריק להתחלה), קובץ דוגמה ממולא להתרשמות, ומסמך Word עם נוסחים מוכנים, לוח זמנים ליום החתונה וצ'קליסט להדפסה.",
    who="<p>לזוגות שמתחתנים ב-2026–2027 ורוצים סדר בלי אפליקציה ובלי מנוי: קובץ אחד שאפשר לשתף עם בן/בת הזוג וההורים. "
        "מתאים לחתונה של 80 אורחים וגם של 400, באולם, בגן או באירוע צנוע.</p>",
    guides=[("wedding-budget-2026", "תקציב חתונה 2026: איך מחלקים ומה באמת עולה"),
            ("rsvp-seating-gifts", "אישורי הגעה, הושבה ורישום צ'קים – שיטה מסודרת")],
    faqs=[
        ("מה ההבדל בין זה לבין טבלה שאני בונה לבד?",
         "הכל כבר מחובר: ספק שסוגרים נכנס לתקציב, תשלום שמסמנים מעדכן את היתרה, אישור הגעה משנה את מספר המנות וההושבה, ומתנה שנרשמת מעדכנת את המאזן. "
         "בנוסף יש צ'קליסט עם תאריכים אוטומטיים ונוסחים מוכנים."),
        ("אפשר לשנות את הקטגוריות והרשימות?",
         "כן. בגיליון \"הגדרות\" אפשר לערוך ולהוסיף קטגוריות תקציב, צדדים, קבוצות מוזמנים ואמצעי תשלום, והם מופיעים בכל הרשימות הנפתחות."),
        ("כמה מוזמנים הקובץ תומך?",
         "עד 400 שורות הזמנה (כל שורה יכולה להיות משפחה שלמה), 80 ספקים, 150 תשלומים ו-60 שולחנות."),
    ] + COMMON_FAQ_TAIL,
)

BAR = dict(
    slug="bar-mitzvah-planner", price=39, crumb="מתכנן בר / בת מצווה", other_slug="wedding-planner",
    other_label="מתכנן חתונה (₪49)", tool="bar-mitzvah-cost", tool_label="מחשבון: כמה עולה בר מצווה",
    title="מתכנן בר מצווה / בת מצווה באקסל – תקציב, מוזמנים וצ'קליסט | Glory",
    desc="קובץ אקסל לתכנון בר או בת מצווה בעברית: תקציב מול ספקים, מוזמנים ואישורי הגעה, רישום מתנות, תשלומים, צ'קליסט כולל עלייה לתורה והושבה. גם ב-Google Sheets. ₪39.",
    ld_name="מתכנן בר / בת מצווה באקסל ו-Google Sheets", shot_alt="מתכנן בר מצווה באקסל",
    eyebrow="אקסל + Google Sheets · ₪39 · הורדה מיידית",
    one_liner="תקציב, מוזמנים, מתנות, ספקים וצ'קליסט עם עלייה לתורה – קובץ אקסל / Google Sheets אחד בעברית.",
    h1="מתכנן בר / בת מצווה: <span class=\"hl\">שמחה מסודרת, בלי לחץ</span>",
    lead="תקציב, ספקים ותשלומים, מוזמנים ואישורי הגעה (כולל החברים של חתן/כלת השמחה), מתנות ותודות, צ'קליסט עם עלייה לתורה ותפילין, והושבה. "
         "דשבורד אחד מראה איפה אתם עומדים.",
    points=["בר מצווה וגם בת מצווה", "עובד גם ב-Google Sheets", "בלי מאקרו", "קובץ דוגמה ממולא"],
    inside_intro="אותו מנוע מוכח של מתכנן החתונה שלנו, מותאם לבר ובת מצווה.",
    features=[
        ("chart", "דשבורד חי", "ימים לאירוע, תקציב מול התחייבויות, תשלומים קרובים ובאיחור, אישורי הגעה ומאזן מתנות."),
        ("money", "תקציב לפי 11 קטגוריות", "אולם וקייטרינג, צילום, DJ, תפילין וטלית, מורה לבר מצווה, קידוש ועוד – עם חלוקה מקובלת לפי התקרה."),
        ("users", "מוזמנים ואישורי הגעה", "משפחת אמא, משפחת אבא, חברים של הילד/ה וחברים של ההורים, עם סטטוס הגעה ומספר מאשרים."),
        ("gift", "מתנות ותודות", "סכום וסוג (צ'ק, ביט, מזומן, מתנה), ומעקב תודות – גם כשהילד/ה כותבים אותן בעצמם."),
        ("cal", "ספקים ותשלומים", "הצעות מחיר ומקדמות עם תאריכי יעד, כולל תשלומים חודשיים למורה."),
        ("check", "צ'קליסט של 28 משימות", "מבחירת סוג האירוע, דרך תפילין ובית הכנסת, ועד ההודעות תודה – עם תאריכים אוטומטיים."),
        ("table", "עוזר הושבה", "כולל שולחנות ילדים, תפוסה וחריגות."),
        ("doc", "נוסחים מוכנים (Word)", "הזמנה ובקשת אישור הגעה, הזמנה לעלייה לתורה וקידוש, הודעות תודה, לוח זמנים לאירוע וצ'קליסט להדפסה."),
    ],
    files_text="מתכנן בר/בת המצווה (Excel ריק להתחלה), קובץ דוגמה ממולא, ומסמך Word עם נוסחים מוכנים, לוח זמנים לאירוע וצ'קליסט להדפסה.",
    who="<p>להורים שמתכננים בר או בת מצווה – אירוע ערב באולם, צהריים, קידוש ומסיבה או חגיגה משפחתית. "
        "הקובץ גמיש: מחיר מנה אפשר להשאיר ריק, ואת הקטגוריות אפשר לשנות.</p>",
    guides=[("bar-mitzvah-cost-2026", "כמה עולה בר מצווה ב-2026? השוואה בין סוגי אירועים"),
            ("bar-mitzvah-timeline", "לוח זמנים להכנת בר / בת מצווה: מה עושים ומתי")],
    faqs=[
        ("זה מתאים גם לבת מצווה?",
         "כן. הקובץ כתוב לשניהם. קטגוריה כמו \"תפילין / טלית\" אפשר למחוק או לשנות בגיליון הגדרות."),
        ("ומה אם עושים רק קידוש ומסיבה קטנה?",
         "מצוין. משאירים את מחיר המנה ריק או מזינים עלות לאורח, ומשתמשים רק במה שצריך. הצ'קליסט כולל גם את התיאום עם בית הכנסת."),
        ("מה ההבדל ממתכנן החתונה?",
         "אותו מנוע, אבל קטגוריות, צדדים, קבוצות מוזמנים, צ'קליסט ונוסחים שמותאמים לבר/בת מצווה. שניהם יחד בחבילת האירועים ב-₪69."),
    ] + COMMON_FAQ_TAIL,
)


def build():
    return [build_product(WEDDING), build_product(BAR)]
