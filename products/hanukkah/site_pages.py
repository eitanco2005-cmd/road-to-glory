#!/usr/bin/env python3
"""Generate all Hanukkah pages (he + en).  Run: python3 site_pages.py"""
import json

from site_common import page, faq_html, faq_ld, product_ld, app_ld, article_ld, BASE
import pack

# ------------------------------------------------------------------ paths
HE_PACK, HE_PLAN, HE_HUB, HE_TOOL = "p/hanukkah-activity-pack/", "p/hanukkah-party-planner/", "hanukkah/", "tools/sufganiyot-calculator/"
HE_G1, HE_G2, HE_G3 = "hanukkah/hanukkah-2026-dates/", "hanukkah/kids-activities/", "hanukkah/hanukkah-party/"
EN = "en/hanukkah/"
EN_PACK, EN_PLAN, EN_TOOL = EN + "activity-pack/", EN + "party-planner/", EN + "latke-calculator/"
EN_G1, EN_G2, EN_THANKS, EN_TERMS = EN + "when-is-hanukkah-2026/", EN + "how-to-play-dreidel/", EN + "thanks/", EN + "terms/"
PIMG, LIMG, EIMG = HE_PACK + "img/", HE_PLAN + "img/", EN + "img/"

HE_DATES_TABLE = ('<div class="table-wrap"><table class="hk-dates"><caption class="sr-only">הדלקת נרות חנוכה 2026</caption>'
                  '<tr><th>נר</th><th>ערב</th><th>תאריך</th><th>תאריך עברי</th><th>נרות + שמש</th></tr>'
                  + "".join(f"<tr><td>{n}</td><td>{d}</td><td>{g}</td><td>{h}</td><td>{n} + 1</td></tr>" for n, d, g, h in pack.NIGHTS_HE)
                  + "</table></div>")
EN_DATES_TABLE = ('<div class="table-wrap"><table class="hk-dates"><caption class="sr-only">Hanukkah 2026 candle lighting</caption>'
                  '<tr><th>Night</th><th>Evening of</th><th>Candles + shamash</th></tr>'
                  + "".join(f"<tr><td>{n}</td><td>{d}, {g}, 2026</td><td>{n} + 1</td></tr>" for n, d, g in pack.NIGHTS_EN)
                  + "</table></div>")
BRACHOT_HE_HTML = "".join(f'<p class="hk-bracha" lang="he" dir="rtl">{b}</p>' for b in pack.BRACHOT_HE)


def pages_grid(items, base):
    return '<div class="hk-pages">' + "".join(
        f'<figure><img src="{base}{f}.webp" loading="lazy" width="579" height="{h}" alt="{alt}"><figcaption>{cap}</figcaption></figure>'
        for f, h, alt, cap in items) + "</div>"


# ================================================================== HEBREW
# ---------------------------------------------------------------- activity pack
faq_pack = [
    ("לאיזה גיל זה מתאים?", "לילדים בגילאי 4 עד 10. יש דפי צביעה פשוטים לקטנים, מבוך קל ומבוך מאתגר, תפזורת ודף «כמה נרות?» לתרגול ספירה."),
    ("כמה פעמים אפשר להדפיס?", "כמה שרוצים, לשימוש אישי, משפחתי וכיתתי (גננות ומורות מוזמנות להדפיס לכל הכיתה). לא למכירה חוזרת או להפצה ברשת."),
    ("באיזה גודל הדפים?", "קובץ PDF אחד בגודל A4, 20 עמודים, באיכות וקטורית — הקווים חדים גם בהדפסה ביתית רגילה."),
    ("הברכות כתובות בניקוד?", "כן. שלוש ברכות הדלקת הנרות בניקוד מלא, בגופן גדול וברור. את השם כתבנו בקיצור (ה׳) כדי שאפשר יהיה להשתמש בדף בלי חשש."),
    ("התאריכים נכונים ל-2026?", "כן. נר ראשון ביום שישי 4.12.2026 בערב, ונר שמיני בשישי 11.12.2026. לוח ההדלקה כולל תאריך לועזי ועברי לכל ערב."),
    ("איך מקבלים את הקובץ?", "מיד אחרי התשלום ב-PayPal (אפשר גם בכרטיס אשראי, בלי חשבון) נפתח דף הורדה עם הקובץ."),
]
body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<div class="split"><div>
<h1>חבילת פעילויות לחנוכה 2026 – דפי צביעה ומשחקים להדפסה</h1>
<p class="lead">20 עמודים מוכנים להדפסה לילדים: דפי צביעה לחנוכה, מבוכים, תפזורת, משחק סביבון עם דף ניקוד, סביבון לגזירה, לוח הדלקת נרות לחנוכה 2026 וברכות בניקוד.</p>
</div>
<div id="buy" class="buy" data-product="hanukkah-activity-pack" data-compact="1"></div>
<ul class="hero-points"><li>20 עמודים, PDF בגודל A4</li><li>איורים מקוריים, קווים עבים ונקיים</li><li>גילאי 4–10</li><li>מדפיסים כמה שרוצים</li><li>הורדה מיידית</li></ul>
</div>
<p class="hk-note mt-2">רוצים גם לתכנן את המסיבה? <a href="{{up}}hanukkah/">בחבילת החנוכה</a> מקבלים את הפעילויות + מתכנן המסיבה ב-₪29 במקום ₪38.</p>
</div></section>
<section class="section alt"><div class="container">
<div class="section-head"><h2>הצצה לעמודים</h2><p class="muted">צילומים מהקובץ עצמו.</p></div>
{pages_grid([("cover", 842, "עמוד השער של חבילת הפעילויות לחנוכה", "שער"),
             ("coloring", 842, "דף צביעה של חנוכייה", "דף צביעה: חנוכייה"),
             ("maze", 842, "מבוך חנוכה לילדים", "מבוך קל"),
             ("wordsearch", 842, "תפזורת חנוכה בעברית", "תפזורת חנוכה"),
             ("dreidel-rules", 842, "חוקי משחק הסביבון", "משחק הסביבון"),
             ("diy", 842, "סביבון לגזירה והדבקה", "סביבון לגזירה"),
             ("chart", 842, "לוח הדלקת נרות חנוכה 2026", "לוח הדלקת נרות 2026"),
             ("blessings", 842, "ברכות הדלקת נרות חנוכה בניקוד", "ברכות בניקוד")], "img/")}
</div></section>
<section class="section"><div class="container">
<div class="section-head"><h2>מה יש בחבילה</h2></div>
<div class="grid cols-3">
<div class="card feature"><span class="ic" aria-hidden="true">🖍️</span><div><h3>5 דפי צביעה</h3><p>חנוכייה, סביבונים, סופגנייה ולביבות, חנוכייה בחלון ופך השמן — עם משפט קצר על החג בכל דף.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🧩</span><div><h3>משחקי חשיבה</h3><p>מבוך קל ומבוך מאתגר, תפזורת עם 13 מילים, צביעה לפי מספרים ודף «כמה נרות?» לספירה.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🎲</span><div><h3>משחק הסביבון</h3><p>חוקים פשוטים עם איור לכל אות (נ, ג, ה, פ), דף ניקוד ל-5 שחקנים וסביבון נייר לגזירה.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🕎</span><div><h3>לוח הדלקה 2026</h3><p>שמונה הלילות עם תאריך לועזי ועברי, כמה נרות בכל ערב, והערות לשישי ולמוצאי שבת.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">📜</span><div><h3>ברכות בניקוד</h3><p>שלוש ברכות ההדלקה באותיות גדולות, להניח ליד החנוכייה.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">💌</span><div><h3>מעשים טובים וברכות</h3><p>לוח «8 לילות של מעשים טובים», שתי ברכות לחג לגזירה, ודף פתרונות להורים.</p></div></div>
</div></div></section>
<section class="section alt"><div class="container narrow">
<h2>שאלות נפוצות</h2>{faq_html(faq_pack)}
<h2 class="mt-4">עוד לחנוכה</h2>
<ul class="hk-list"><li><a href="{{up}}{HE_G2}">פעילויות לחנוכה לילדים: רעיונות לבית ולגן</a></li>
<li><a href="{{up}}{HE_G1}">חנוכה 2026: מתי מדליקים, ברכות וסדר ההדלקה</a></li>
<li><a href="{{up}}{HE_TOOL}">מחשבון: כמה סופגניות ולביבות צריך?</a></li>
<li><a href="{{up}}{HE_PLAN}">מתכנן מסיבת חנוכה באקסל</a></li></ul>
<div class="mt-3"><div class="buy" data-product="hanukkah-activity-pack" data-compact="1"></div></div>
</div></section>
<div class="buy-bar"><span><strong>פעילויות לחנוכה</strong> · <span class="price">₪19</span></span><a class="btn small" href="#buy">לרכישה</a></div>
"""
t = "חבילת פעילויות לחנוכה 2026 – דפי צביעה, מבוכים ותפזורת להדפסה | תכנון פלוס"
d = "20 דפי פעילות לחנוכה להדפסה: דפי צביעה, מבוכים, תפזורת, משחק סביבון, סביבון לגזירה, לוח הדלקת נרות 2026 וברכות בניקוד. PDF בגודל A4, ₪19."
page(HE_PACK, t, d, body, [product_ld("חבילת פעילויות לחנוכה 2026", d, HE_PACK, 19, [PIMG + "cover.webp", PIMG + "coloring.webp", PIMG + "maze.webp"]), faq_ld(faq_pack)],
     og_image=PIMG + "cover.webp", crumbs=[("חנוכה 2026", HE_HUB), ("חבילת פעילויות", HE_PACK)], buy=True, alt=EN_PACK)

# ---------------------------------------------------------------- party planner
faq_plan = [
    ("באיזו תוכנה זה עובד?", "Excel (2010 ומעלה, גם בנייד), Google Sheets ו-LibreOffice. ב-Google Sheets: מעלים ל-Drive ובוחרים «פתיחה באמצעות Google Sheets». אין מאקרו."),
    ("איך הקובץ יודע כמה סופגניות צריך?", "הוא סופר את מי שאישר הגעה בגיליון האורחים (ואפשר לבחור לספור גם את ה«אולי»), ומכפיל בכמות לאדם: 1.5 סופגניות למבוגר ו-1 לילד כברירת מחדל. אפשר לשנות כל הנחה."),
    ("ואם אני מכינה סופגניות בבית?", "בוחרים «מכינים» והקובץ מחשב כמה מנות בצק צריך (מנה של 500 גרם קמח ≈ 16 סופגניות) וכמה קמח, שמרים, סוכר, ביצים, חלב, חמאה, ריבה ושמן לקנות."),
    ("מה זה מעקב מתנות ל-8 לילות?", "טבלה שבה רושמים לכל ערב של חנוכה למי, איזו מתנה, תקציב ועלות בפועל. רואים סיכום לפי ערב ואת התקציב מול ההוצאה בגרף."),
    ("המחירים בקובץ אמיתיים?", "לא. אלה מחירים לדוגמה כדי שהחישוב יעבוד מהרגע הראשון. מעדכנים אותם לפי המחירים אצלכם."),
    ("איך מקבלים את הקובץ?", "מיד אחרי התשלום ב-PayPal (אפשר בכרטיס אשראי, בלי חשבון) נפתח דף הורדה עם קובץ ריק וקובץ דוגמה מלא."),
]
body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<div class="split"><div>
<h1>מתכנן מסיבת חנוכה באקסל: אורחים, כמויות, קניות ומתנות</h1>
<p class="lead">מכניסים את רשימת האורחים, והקובץ מחשב כמה סופגניות ולביבות צריך, בונה רשימת קניות עם עלות משוערת ועוזר לעקוב אחרי המתנות לכל שמונת הלילות.</p>
</div>
<div id="buy" class="buy" data-product="hanukkah-party-planner" data-compact="1"></div>
<ul class="hero-points"><li>Excel ו-Google Sheets</li><li>כמויות מחושבות לפי האורחים</li><li>רשימת קניות אוטומטית</li><li>מעקב מתנות ל-8 לילות</li><li>הורדה מיידית</li></ul>
</div>
<p class="hk-note mt-2">רוצים קודם לנסות? <a href="{{up}}{HE_TOOL}">המחשבון החינמי</a> אומר בתוך שנייה כמה סופגניות ולביבות צריך.</p>
<img class="hk-hero-img mt-3" src="img/dashboard.webp" width="857" height="577" alt="דשבורד מתכנן מסיבת חנוכה: אורחים, כמויות, עלות קניות ותקציב מתנות" fetchpriority="high">
</div></section>
<section class="section"><div class="container">
<div class="section-head"><h2>מה יש בקובץ</h2><p class="muted">7 גיליונות מחוברים. מקלידים רק בתאים הצהובים.</p></div>
<div class="grid cols-3">
<div class="card feature"><span class="ic" aria-hidden="true">👨‍👩‍👧</span><div><h3>אורחים ואישורי הגעה</h3><p>מבוגרים וילדים, מגיע / אולי / לא, באיזה ערב, מי מביא מה, ואלרגיות.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🍩</span><div><h3>כמויות סופגניות ולביבות</h3><p>לפי האורחים ומקדם תיאבון: כמה סופגניות, כמה לביבות, כמה ק״ג תפוחי אדמה, ביצים, קמח ושמן.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🛒</span><div><h3>רשימת קניות</h3><p>נבנית לבד מהכמויות, עם מחיר ליחידה, עלות משוערת וסימון מה כבר נקנה.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🎁</span><div><h3>מתנות ל-8 לילות</h3><p>למי, מה, תקציב, עלות בפועל וסטטוס — עם סיכום לכל ערב.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">✅</span><div><h3>צ'קליסט הכנות</h3><p>16 משימות מוכנות עם תאריך יעד לפי מועד המסיבה.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">📊</span><div><h3>דשבורד</h3><p>הכול במבט אחד, עם גרף מתנות לפי ערב ועלות הקניות לפי קטגוריה.</p></div></div>
</div></div></section>
<section class="section alt"><div class="container">
<div class="section-head"><h2>ככה זה נראה</h2><p class="muted">מקובץ הדוגמה המצורף. המספרים להמחשה.</p></div>
<div class="screens">
<figure><img src="img/quantities.webp" loading="lazy" width="903" height="682" alt="גיליון כמויות: סופגניות, לביבות ומצרכים"><figcaption>כמויות: מה צריך לפי מספר האורחים</figcaption></figure>
<figure><img src="img/shopping.webp" loading="lazy" width="900" height="700" alt="רשימת קניות אוטומטית לחנוכה"><figcaption>רשימת קניות עם עלות משוערת</figcaption></figure>
<figure><img src="img/gifts.webp" loading="lazy" width="1300" height="400" alt="מעקב מתנות לשמונת לילות חנוכה"><figcaption>מתנות ל-8 לילות</figcaption></figure>
<figure><img src="img/guests.webp" loading="lazy" width="1300" height="400" alt="רשימת אורחים ואישורי הגעה"><figcaption>אורחים ואישורי הגעה</figcaption></figure>
</div></div></section>
<section class="section"><div class="container narrow">
<h2>שאלות נפוצות</h2>{faq_html(faq_plan)}
<h2 class="mt-4">מדריכים</h2>
<ul class="hk-list"><li><a href="{{up}}{HE_G3}">איך מארגנים מסיבת חנוכה: כמויות, תפריט ורשימת קניות</a></li>
<li><a href="{{up}}{HE_TOOL}">מחשבון כמה סופגניות ולביבות צריך</a></li><li><a href="{{up}}{HE_G1}">תאריכי חנוכה 2026</a></li></ul>
<div class="mt-3"><div class="buy" data-product="hanukkah-party-planner" data-compact="1"></div></div>
</div></section>
<div class="buy-bar"><span><strong>מתכנן מסיבת חנוכה</strong> · <span class="price">₪19</span></span><a class="btn small" href="#buy">לרכישה</a></div>
"""
t = "מתכנן מסיבת חנוכה באקסל – כמויות סופגניות, קניות ומתנות | תכנון פלוס"
d = "קובץ אקסל לאירוח בחנוכה: רשימת אורחים, חישוב כמה סופגניות ולביבות צריך, רשימת קניות אוטומטית ומעקב מתנות ל-8 לילות. Excel ו-Google Sheets, ₪19."
page(HE_PLAN, t, d, body, [product_ld("מתכנן מסיבת חנוכה – אקסל", d, HE_PLAN, 19, [LIMG + "dashboard.webp", LIMG + "quantities.webp", LIMG + "shopping.webp"]), faq_ld(faq_plan)],
     og_image=LIMG + "dashboard.webp", crumbs=[("חנוכה 2026", HE_HUB), ("מתכנן מסיבה", HE_PLAN)], buy=True, alt=EN_PLAN)

# ---------------------------------------------------------------- calculator (shared JS, both languages)
CALC_JS = r"""
<script>
(function () {
  "use strict";
  var C = window.HK_CALC;
  var $ = function (id) { return document.getElementById(id); };
  function num(id) { var v = parseFloat($(id).value); return isFinite(v) && v > 0 ? v : 0; }
  function radio(n) { var r = document.querySelector('input[name="' + n + '"]:checked'); return r ? r.value : ""; }
  function up(x, step) { step = step || 1; return Math.ceil(x / step - 1e-9) * step; }
  function fmt(x, d) { return Number(x).toLocaleString(C.locale, { maximumFractionDigits: d || 0 }); }
  function calc() {
    var a = num("adults"), k = num("kids"), f = { light: .75, normal: 1, hungry: 1.3 }[radio("appetite")] || 1;
    var make = radio("mode") === "make", men = num("menorahs");
    if (!a && !k) { $("out").hidden = true; $("empty").hidden = false; return; }
    var R = C.rates;
    var latkes = up((a * R.l_ad + k * R.l_kid) * f), pot = up(latkes / R.l_per, 0.1);
    var suf = up((a * R.s_ad + k * R.s_kid) * f), b = up(suf / R.batch);
    $("v-suf").textContent = fmt(suf); $("v-lat").textContent = fmt(latkes);
    $("v-pot").textContent = fmt(pot, 1); $("v-oil").textContent = fmt(up(pot * R.oil, 0.1) + (make ? Math.max(R.s_oil_min, up(b * R.s_oil, 0.1)) : 0), 1);
    var rows = [
      [C.t.potatoes, fmt(pot, 1) + " " + C.u.pot], [C.t.onions, fmt(up(pot * R.on))], [C.t.eggs, fmt(up(pot * R.egg) + (make ? b * 2 : 0))],
      [C.t.flour_l, fmt(up(pot * R.flour, C.u.flour_step)) + " " + C.u.flour], [C.t.oil_l, fmt(up(pot * R.oil, 0.1), 1) + " " + C.u.oil]
    ];
    if (make) rows = rows.concat(C.dough.map(function (d) { return [d[0], fmt(d[1] === "jam" ? suf * R.jam : b * d[1], 2) + " " + d[2]]; }))
      .concat([[C.t.oil_s, fmt(Math.max(R.s_oil_min, up(b * R.s_oil, 0.1)), 1) + " " + C.u.oil]]);
    rows = rows.concat([[C.t.drinks, fmt(up((a + k) * R.drink, C.u.drink_step), 1) + " " + C.u.drink], [C.t.gelt, fmt(k * 5)], [C.t.candles, fmt(men * 44)]]);
    $("list").innerHTML = rows.map(function (r) { return "<tr><td>" + r[0] + '</td><td class="num">' + r[1] + "</td></tr>"; }).join("");
    $("batches").textContent = make ? C.t.batches.replace("{b}", b).replace("{s}", suf) : C.t.buy;
    $("out").hidden = false; $("empty").hidden = true;
    try { history.replaceState(null, "", "?a=" + a + "&k=" + k + "&f=" + radio("appetite") + "&m=" + radio("mode") + "&h=" + men); } catch (e) {}
  }
  var q = new URLSearchParams(location.search);
  if (q.get("a")) $("adults").value = q.get("a");
  if (q.get("k")) $("kids").value = q.get("k");
  if (q.get("h")) $("menorahs").value = q.get("h");
  ["f:appetite", "m:mode"].forEach(function (p) { var s = p.split(":"), v = q.get(s[0]); if (v) { var el = document.querySelector('input[name="' + s[1] + '"][value="' + v + '"]'); if (el) el.checked = true; } });
  document.getElementById("calc").addEventListener("input", calc);
  document.getElementById("calc").addEventListener("change", calc);
  calc();
})();
</script>"""

HE_CALC_CFG = {
    "locale": "he-IL",
    "rates": {"l_ad": 4, "l_kid": 2, "l_per": 20, "on": 1, "egg": 2, "flour": 40, "oil": 0.25, "s_ad": 1.5, "s_kid": 1, "batch": 16,
              "s_oil": 0.5, "s_oil_min": 1, "jam": 15, "drink": 0.5},
    "u": {"pot": "ק״ג", "flour": "גרם", "flour_step": 10, "oil": "ליטר", "drink": "ליטר", "drink_step": 0.5},
    "t": {"potatoes": "תפוחי אדמה", "onions": "בצלים", "eggs": "ביצים (לביבות + בצק)", "flour_l": "קמח / מצה טחונה ללביבות",
          "oil_l": "שמן לטיגון לביבות", "oil_s": "שמן לטיגון סופגניות", "drinks": "שתייה", "gelt": "מטבעות שוקולד (5 לילד)",
          "candles": "נרות חנוכה (44 לחנוכייה)", "batches": "מכינים בבית: {b} מנות בצק (כל מנה = 500 גרם קמח ≈ 16 סופגניות) ל-{s} סופגניות.",
          "buy": "קונים במאפייה: הזמינו את מספר הסופגניות שלמעלה."},
    "dough": [["קמח לסופגניות", 500, "גרם"], ["שמרים יבשים", 10, "גרם"], ["סוכר", 60, "גרם"], ["חלב", 250, "מ״ל"], ["חמאה", 50, "גרם"], ["ריבה", "jam", "גרם"]],
}
EN_CALC_CFG = {
    "locale": "en-US",
    "rates": {"l_ad": 4, "l_kid": 2, "l_per": 9, "on": 0.5, "egg": 1, "flour": 2, "oil": 0.5, "s_ad": 1.5, "s_kid": 1, "batch": 16,
              "s_oil": 2, "s_oil_min": 4, "jam": 1, "drink": 16},
    "u": {"pot": "lb", "flour": "tbsp", "flour_step": 1, "oil": "cups", "drink": "fl oz", "drink_step": 8},
    "t": {"potatoes": "Potatoes", "onions": "Onions", "eggs": "Eggs (latkes + dough)", "flour_l": "Flour or matzo meal for latkes",
          "oil_l": "Oil for frying latkes", "oil_s": "Oil for frying doughnuts", "drinks": "Drinks", "gelt": "Chocolate gelt (5 per kid)",
          "candles": "Hanukkah candles (44 per menorah)", "batches": "Making them at home: {b} batches of dough (each = 4 cups flour ≈ 16 doughnuts) for {s} doughnuts.",
          "buy": "Buying them: order the number of doughnuts shown above from your bakery."},
    "dough": [["Flour for doughnuts", 4, "cups"], ["Active dry yeast", 1, "packets"], ["Sugar", 0.25, "cups"], ["Milk", 1, "cups"],
              ["Butter", 4, "tbsp"], ["Jelly / jam", "jam", "tbsp"]],
}


def calc_panel(lang):
    he = lang == "he"
    L = (lambda a, b: a if he else b)
    return f"""
<div class="split">
<form class="tool-panel" id="calc" onsubmit="return false" novalidate>
<div class="fields cols-2">
<div class="field"><label for="adults">{L("מבוגרים", "Adults")}</label><input id="adults" type="number" inputmode="numeric" min="0" step="1" value="8"></div>
<div class="field"><label for="kids">{L("ילדים", "Kids")}</label><input id="kids" type="number" inputmode="numeric" min="0" step="1" value="6"></div>
</div>
<div class="field"><span class="label" id="ap-l">{L("תיאבון", "Appetite")}</span>
<div class="choices" role="radiogroup" aria-labelledby="ap-l">
<label><input type="radio" name="appetite" value="light"> {L("קל (יש עוד אוכל)", "Light (other food too)")}</label>
<label><input type="radio" name="appetite" value="normal" checked> {L("רגיל", "Normal")}</label>
<label><input type="radio" name="appetite" value="hungry"> {L("רעבים (הלביבות הן הארוחה)", "Hungry (latkes are dinner)")}</label></div></div>
<div class="field"><span class="label" id="md-l">{L("סופגניות", "Jelly doughnuts (sufganiyot)")}</span>
<div class="choices" role="radiogroup" aria-labelledby="md-l">
<label><input type="radio" name="mode" value="buy" checked> {L("קונים", "Buying")}</label>
<label><input type="radio" name="mode" value="make"> {L("מכינים בבית", "Making at home")}</label></div></div>
<div class="field"><label for="menorahs">{L("כמה חנוכיות מדליקים בבית?", "How many menorahs do you light?")}</label><input id="menorahs" type="number" inputmode="numeric" min="0" step="1" value="1"></div>
</form>
<div aria-live="polite">
<div id="empty" class="result" hidden><div class="label">{L("התוצאה תופיע כאן", "Your result will show here")}</div><p class="mb-0">{L("הכניסו מספר אורחים.", "Enter the number of guests.")}</p></div>
<div id="out">
<div class="hk-tiles">
<div class="hk-tile"><div class="k">{L("סופגניות", "Doughnuts")}</div><div class="v" id="v-suf"></div></div>
<div class="hk-tile"><div class="k">{L("לביבות", "Latkes")}</div><div class="v" id="v-lat"></div></div>
<div class="hk-tile"><div class="k">{L("תפוחי אדמה", "Potatoes")}</div><div class="v" id="v-pot"></div><div class="s">{L("ק״ג", "lb")}</div></div>
<div class="hk-tile"><div class="k">{L("שמן לטיגון", "Frying oil")}</div><div class="v" id="v-oil"></div><div class="s">{L("ליטר", "cups")}</div></div>
</div>
<div class="card mt-2"><h2 class="h3">{L("רשימת קניות", "Shopping list")}</h2><table class="hk-ing"><tbody id="list"></tbody></table>
<p class="hk-note mt-1 mb-0" id="batches"></p></div>
</div></div></div>"""


faq_tool = [
    ("כמה סופגניות לקנות לאורח?", "הערכה מקובלת היא סופגנייה וחצי למבוגר וסופגנייה אחת לילד, כשיש גם אוכל אחר. אם הסופגניות הן הקינוח היחיד, או שהן קטנות (מיני), כדאי לבחור «רעבים» או להוסיף כ-30%."),
    ("כמה לביבות לאדם?", "בערך 4 לביבות בגודל בינוני למבוגר ו-2 לילד, כשהלביבות הן מנה אחת מתוך כמה. אם הן הארוחה עצמה, בחרו «רעבים»."),
    ("כמה לביבות יוצאות מקילו תפוחי אדמה?", "בערך 20 לביבות בינוניות (כף גדושה כל אחת) מקילו תפוחי אדמה, יחד עם בצל, 2 ביצים וכ-4 כפות קמח או מצה טחונה."),
    ("כמה סופגניות יוצאות מ-500 גרם קמח?", "בערך 16 סופגניות בגודל רגיל. המחשבון מעגל למעלה למספר מנות שלמות."),
    ("כמה שמן צריך לטיגון?", "ללביבות בטיגון רדוד: כרבע ליטר לכל קילו תפוחי אדמה. לסופגניות בטיגון עמוק צריך סיר עם לפחות ליטר שמן, שמספיק לכמה סבבים."),
    ("הנתונים נשמרים?", "לא. החישוב רץ בדפדפן ושום מספר לא נשלח לשרת."),
]
body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<h1>כמה סופגניות ולביבות צריך? מחשבון לחנוכה</h1>
<p class="lead">מכניסים כמה מבוגרים וילדים מגיעים ומקבלים מיד כמה סופגניות ולביבות להכין או לקנות, וכמה תפוחי אדמה, ביצים, קמח ושמן לקנות.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
{calc_panel("he")}
<div class="cta-box mt-4"><div><h2 class="h3">רוצים שהקובץ יעשה את זה לבד?</h2><p>«מתכנן מסיבת חנוכה» מחשב את הכמויות ישר מרשימת האורחים, בונה רשימת קניות עם עלות ועוקב אחרי המתנות לשמונת הלילות. ₪19.</p></div>
<a class="btn accent" href="{{up}}{HE_PLAN}">למתכנן המסיבה</a></div>
</div></section>
<section class="section alt"><div class="container narrow prose">
<h2>לפי מה המחשבון מחשב?</h2>
<ul><li>לביבות: 4 למבוגר, 2 לילד; כ-20 לביבות מקילו תפוחי אדמה.</li><li>לכל קילו תפוחי אדמה: בצל, 2 ביצים, כ-40 גרם קמח ורבע ליטר שמן.</li>
<li>סופגניות: 1.5 למבוגר, 1 לילד; מנת בצק של 500 גרם קמח ≈ 16 סופגניות.</li><li>תיאבון «קל» = 75% מהכמויות, «רעבים» = 130%.</li></ul>
<p>אלה הערכות לבית ממוצע, לא כלל. כדאי לעגל למעלה אם יש בני נוער רעבים, ולמטה אם יש גם ארוחה מלאה.</p>
<h2>שאלות נפוצות</h2>{faq_html(faq_tool)}
<p class="mt-3"><a href="{{up}}{HE_G3}">המדריך המלא לאירוח בחנוכה</a> · <a href="{{up}}{HE_HUB}">כל מה שצריך לחנוכה 2026</a></p>
</div></section>
<script>window.HK_CALC = {json.dumps(HE_CALC_CFG, ensure_ascii=False)};</script>{CALC_JS}
"""
t = "כמה סופגניות ולביבות צריך? מחשבון כמויות לחנוכה | תכנון פלוס"
d = "מחשבון חינמי לחנוכה: כמה סופגניות ולביבות להכין לפי מספר המבוגרים והילדים, וכמה תפוחי אדמה, ביצים, קמח ושמן לקנות. תוצאה מיידית."
page(HE_TOOL, t, d, body, [app_ld("מחשבון סופגניות ולביבות", d, HE_TOOL), faq_ld(faq_tool)],
     og_image=LIMG + "quantities.webp", crumbs=[("חנוכה 2026", HE_HUB), ("מחשבון סופגניות", HE_TOOL)], alt=EN_TOOL)

# ---------------------------------------------------------------- hub
body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<h1>חנוכה 2026: פעילויות לילדים, אירוח ותאריכי הדלקה</h1>
<p class="lead">חנוכה תשפ״ז מתחיל ביום שישי 4 בדצמבר 2026 בערב ונמשך עד שבת 12 בדצמבר. כאן תמצאו דפי פעילות להדפסה, מתכנן מסיבה, מחשבון סופגניות ומדריכים.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
<div class="grid cols-2">
<article class="card pad-lg"><h2 class="h3"><a href="{{up}}{HE_PACK}">חבילת פעילויות לחנוכה</a></h2><img src="{{up}}{PIMG}cover.webp" alt="שער חבילת הפעילויות" width="579" height="842" loading="lazy" style="max-width:200px;height:auto;float:inline-end;margin-inline-start:1rem;border:1px solid var(--border);border-radius:8px">
<p>20 דפים להדפסה: צביעה, מבוכים, תפזורת, משחק סביבון, לוח הדלקה וברכות בניקוד.</p><p><strong>₪19</strong></p><a class="btn" href="{{up}}{HE_PACK}">לפרטים</a></article>
<article class="card pad-lg"><h2 class="h3"><a href="{{up}}{HE_PLAN}">מתכנן מסיבת חנוכה באקסל</a></h2>
<img src="{{up}}{LIMG}dashboard.webp" alt="דשבורד מתכנן המסיבה" width="857" height="577" loading="lazy" style="width:100%;height:auto;border:1px solid var(--border);border-radius:8px">
<p>אורחים, כמויות סופגניות ולביבות, רשימת קניות ומעקב מתנות ל-8 לילות.</p><p><strong>₪19</strong></p><a class="btn" href="{{up}}{HE_PLAN}">לפרטים</a></article>
</div>
<article class="card pad-lg mt-3" id="hanukkah-bundle"><div class="split"><div><h2 class="h3">חבילת חנוכה: שניהם יחד</h2><p>חבילת הפעילויות + מתכנן המסיבה. ₪29 במקום ₪38.</p><span class="badge success">חוסכים ₪9</span></div>
<div class="buy" data-product="hanukkah-bundle" data-compact="1"></div></div></article>
</div></section>
<section class="section alt"><div class="container narrow">
<h2>מתי מדליקים נרות חנוכה 2026?</h2>{HE_DATES_TABLE}
<p class="hk-note mt-1">מדליקים בערב. בשישי מדליקים לפני נרות שבת, ובמוצאי שבת אחרי צאת השבת. <a href="{{up}}{HE_G1}">כל הפרטים והברכות</a>.</p>
<h2 class="mt-4">כלים ומדריכים</h2>
<ul class="hk-list"><li><a href="{{up}}{HE_TOOL}">מחשבון: כמה סופגניות ולביבות צריך?</a></li>
<li><a href="{{up}}{HE_G1}">חנוכה 2026: תאריכים, ברכות וסדר ההדלקה</a></li>
<li><a href="{{up}}{HE_G2}">פעילויות לחנוכה לילדים: רעיונות לבית ולגן</a></li>
<li><a href="{{up}}{HE_G3}">איך מארגנים מסיבת חנוכה</a></li>
<li><a href="{{up}}{EN}" hreflang="en" lang="en">Hanukkah 2026 in English</a></li></ul>
</div></section>
"""
t = "חנוכה 2026 – תאריכים, פעילויות לילדים ומסיבת חנוכה | תכנון פלוס"
d = "חנוכה 2026 מתחיל ב-4.12 בערב: לוח הדלקת נרות, דפי פעילות לחנוכה להדפסה, מתכנן מסיבה באקסל ומחשבון כמה סופגניות ולביבות צריך."
page(HE_HUB, t, d, body, [{"@context": "https://schema.org", "@type": "CollectionPage", "name": t, "description": d, "url": BASE + HE_HUB, "inLanguage": "he-IL"}],
     og_image=PIMG + "cover.webp", crumbs=[("חנוכה 2026", HE_HUB)], buy=True, alt=EN)

# ---------------------------------------------------------------- he guides
def guide(path, title, desc, h1, html, faq, crumbs, lang="he", alt=None, img=None):
    upd = "עודכן: 17 בנובמבר 2026" if lang == "he" else "Updated: November 17, 2026"
    body = (f'<article class="section"><div class="container narrow prose">{{CRUMBS}}<h1>{h1}</h1><p class="updated muted">{upd}</p>'
            f'{html}' + (("<h2>" + ("שאלות נפוצות" if lang == "he" else "FAQ") + "</h2>" + faq_html(faq)) if faq else "") + "</div></article>")
    lds = [article_ld(h1, desc, path, lang, img)] + ([faq_ld(faq)] if faq else [])
    page(path, title, desc, body, lds, og_image=img, crumbs=crumbs, lang=lang, alt=alt, og_type="article")


g1 = f"""
<p>חנוכה תשפ״ז נופל השנה על <strong>4–12 בדצמבר 2026</strong>. את הנר הראשון מדליקים ביום שישי, 4 בדצמבר, בערב (כ״ה בכסלו), ואת הנר השמיני ביום שישי, 11 בדצמבר. היום האחרון של החג הוא שבת, 12 בדצמבר.</p>
<h2>לוח הדלקת נרות חנוכה 2026</h2>{HE_DATES_TABLE}
<p>בסך הכול צריך 44 נרות לחנוכייה אחת לכל החג: 36 נרות ועוד שמש בכל ערב. זה בדיוק מה שיש בקופסת נרות חנוכה רגילה.</p>
<h2>השנה יש שני ערבי שבת בחנוכה</h2>
<p>הנר הראשון והנר השמיני חלים ביום שישי. בערבים האלה מדליקים את נרות החנוכה <strong>לפני</strong> הדלקת נרות שבת, ומשתמשים בנרות גדולים יותר או בשמן שיספיקו לדלוק לפחות חצי שעה אחרי צאת הכוכבים. במוצאי שבת (5.12) מדליקים אחרי צאת השבת. אם מבדילים קודם או מדליקים קודם — לפי מנהג הבית.</p>
<h2>סדר ההדלקה</h2>
<ol><li>מניחים את הנרות מימין לשמאל: בערב הראשון נר אחד בצד ימין, ובכל ערב מוסיפים נר משמאלו.</li>
<li>מדליקים את השמש ומברכים.</li><li>מדליקים בעזרת השמש משמאל לימין — קודם את הנר החדש של אותו ערב.</li>
<li>מניחים את השמש במקומו ואומרים «הנרות הללו» ושרים «מעוז צור».</li></ol>
<h2>ברכות הדלקת נרות חנוכה</h2>
<p>בכל ערב מברכים את שתי הברכות הראשונות. בערב הראשון מוסיפים את ברכת «שהחיינו».</p>{BRACHOT_HE_HTML}
<p class="hk-note">יש הנוהגים לומר «לְהַדְלִיק נֵר שֶׁל חֲנֻכָּה». שם ה׳ כתוב כאן בקיצור; בברכה אומרים אותו כרגיל.</p>
<p>רוצים את הלוח והברכות מודפסים ליד החנוכייה? הם חלק מ<a href="{{up}}{HE_PACK}">חבילת הפעילויות לחנוכה</a>, יחד עם דפי צביעה ומשחקים לילדים.</p>
"""
faq_g1 = [("מתי חנוכה 2026?", "מערב יום שישי 4.12.2026 (כ״ה בכסלו תשפ״ז) ועד שבת 12.12.2026. הנר השמיני מודלק ביום שישי 11.12.2026."),
          ("מתי מתחיל חופש חנוכה 2026 בבתי הספר?", "חופשת חנוכה נקבעת בלוח החופשות של משרד החינוך ומשתנה בין מסגרות. בדקו בלוח החופשות הרשמי ובהודעות בית הספר או הגן."),
          ("כמה נרות צריך לכל החג?", "44 נרות לחנוכייה אחת: 1+2+...+8 = 36 נרות, ועוד שמש בכל אחד משמונת הערבים."),
          ("באיזה צד מתחילים?", "את הנרות מניחים מימין לשמאל, ומדליקים משמאל לימין — קודם את הנר שנוסף באותו ערב.")]
guide(HE_G1, "חנוכה 2026: מתי מדליקים נרות? תאריכים, ברכות וסדר הדלקה | תכנון פלוס",
      "חנוכה 2026 מתחיל ביום שישי 4.12 בערב ועד 12.12. לוח הדלקת נרות לכל ערב, ברכות בניקוד, מה עושים בערב שבת ובמוצאי שבת וכמה נרות צריך.",
      "חנוכה 2026: מתי מדליקים נרות, ברכות וסדר ההדלקה", g1, faq_g1, [("חנוכה 2026", HE_HUB), ("תאריכי חנוכה 2026", HE_G1)], alt=EN_G1, img=PIMG + "chart.webp")

g2 = f"""
<p>שמונה ימים של חופש, ערבים ארוכים ונרות — חנוכה הוא זמן מצוין לפעילויות עם ילדים. ריכזנו רעיונות שלא דורשים ציוד מיוחד, מתאימים לבית ולגן, ורובם לוקחים פחות מחצי שעה.</p>
<h2>1. דפי צביעה לחנוכה</h2><p>חנוכייה, סביבון, סופגנייה ופך שמן הם הנושאים הקלאסיים. לקטנים בחרו דפים עם קווים עבים ומעט פרטים. שווה לשלב משפט קצר על הנס בכל דף, כדי שהצביעה תהיה גם הזדמנות לספר את הסיפור.</p>
<h2>2. משחק סביבון אמיתי</h2><p>מחלקים לכל ילד 10 פריטים (סוכריות, אגוזים, קוביות לגו). כל אחד שם פריט בקופה, ומסובבים בתורות: <strong>נ</strong> – כלום, <strong>ג</strong> – לוקחים הכול, <strong>ה</strong> – לוקחים חצי, <strong>פ</strong> – מוסיפים אחד. דף ניקוד עוזר לילדים בגיל בית ספר לתרגל חיבור וחיסור בלי לשים לב.</p>
<h2>3. סביבון מנייר</h2><p>מדפיסים תבנית של קובייה עם האותיות נ, ג, ה, פ, גוזרים, מקפלים ומדביקים, ומכניסים עיפרון קצר דרך המרכז. פעילות יצירה שנגמרת במשחק.</p>
<h2>4. מבוכים ותפזורת</h2><p>מבוך שבו פך השמן צריך להגיע לחנוכייה, ותפזורת עם מילים כמו סביבון, לביבות, מכבים ושמש — מעולים לרגעים השקטים אחרי ההדלקה, ולילדים שכבר קוראים.</p>
<h2>5. «כמה נרות?»</h2><p>לגילאי גן: מציגים חנוכיות עם מספר נרות שונה ומבקשים לספור ולכתוב את המספר. אפשר לעשות את אותו הדבר עם החנוכייה האמיתית בכל ערב.</p>
<h2>6. לוח הדלקה עם ✓</h2><p>לוח עם שמונה הערבים שבו הילדים מסמנים כל ערב שהדלקתם. זה נותן תחושת התקדמות, ועוזר לזכור כמה נרות לשים.</p>
<h2>7. שמונה לילות של מעשים טובים</h2><p>במקום (או בנוסף) למתנה בכל ערב, כל ילד רושם או מצייר מעשה טוב אחד שעשה באותו יום. בערב האחרון קוראים את כל הרשימה יחד.</p>
<h2>8. כרטיסי ברכה לחג</h2><p>מדפיסים כרטיס עם איור לצביעה, הילדים כותבים «חג אורים שמח» ונותנים לסבא וסבתא, לגננת או לשכנים.</p>
<h2>9. מטבח קטן: לביבות וסופגניות</h2><p>ילדים יכולים לשטוף ולגרר (בעזרת מבוגר), לערבב בצק או למלא ריבה. את הטיגון משאירים למבוגרים. כמה צריך? <a href="{{up}}{HE_TOOL}">המחשבון שלנו</a> מחשב לפי מספר האנשים.</p>
<h2>10. חנוכייה בחלון</h2><p>מדליקים ליד החלון כדי «לפרסם את הנס». אפשר לצאת לטיול ערב קצר ולספור חנוכיות בחלונות השכונה.</p>
<div class="cta-box mt-4"><div><h2 class="h3">כל הדפים במקום אחד</h2><p>חבילת הפעילויות לחנוכה כוללת 20 דפים מוכנים להדפסה: צביעה, מבוכים, תפזורת, משחק סביבון ודף ניקוד, סביבון לגזירה, «כמה נרות?», לוח הדלקה 2026, ברכות בניקוד, מעשים טובים וכרטיסי ברכה. ₪19.</p></div>
<a class="btn accent" href="{{up}}{HE_PACK}">לחבילת הפעילויות</a></div>
<p><img src="{{up}}{PIMG}maze.webp" alt="מבוך חנוכה מתוך החבילה" width="579" height="842" loading="lazy" style="max-width:280px;height:auto"></p>
"""
faq_g2 = [("מאיזה גיל אפשר לשחק בסביבון?", "כבר מגיל 3–4 אפשר לסובב ולזהות אותיות. מגיל 6 בערך ילדים מבינים את החוקים לבד, כולל «חצי קופה»."),
          ("מה עושים בחנוכה עם ילדים כשיורד גשם?", "יצירה (סביבון מנייר, כרטיסי ברכה), דפי צביעה, מבוכים, אפייה משותפת ומשחק סביבון משפחתי.")]
guide(HE_G2, "פעילויות לחנוכה לילדים: 10 רעיונות לבית ולגן + דפים להדפסה | תכנון פלוס",
      "רעיונות לפעילויות חנוכה עם ילדים: דפי צביעה, משחק סביבון, סביבון מנייר, מבוכים ותפזורת, לוח הדלקה, מעשים טובים וכרטיסי ברכה. מתאים לבית ולגן.",
      "פעילויות לחנוכה לילדים: 10 רעיונות לבית ולגן", g2, faq_g2, [("חנוכה 2026", HE_HUB), ("פעילויות לילדים", HE_G2)], img=PIMG + "cover.webp")

g3 = f"""
<p>מסיבת חנוכה טובה צריכה שלושה דברים: לדעת מי מגיע, לדעת כמה אוכל להכין, ולא לשכוח את הנרות. הנה הדרך לעשות את זה בלי לחץ.</p>
<h2>שבועיים לפני: מי מגיע</h2><p>קבעו ערב (בחנוכה 2026 יש שני ערבי שבת — 4.12 ו-11.12 — ושש הזדמנויות באמצע השבוע). שלחו הזמנה ובקשו אישור הגעה עם מספר מבוגרים וילדים, ושאלו על אלרגיות. ספירה מדויקת של מבוגרים וילדים בנפרד חשובה, כי ילדים אוכלים בערך חצי.</p>
<h2>כמה אוכל צריך</h2>
<ul><li><strong>לביבות:</strong> כ-4 למבוגר ו-2 לילד כשיש עוד אוכל. מקילו תפוחי אדמה יוצאות כ-20 לביבות בינוניות.</li>
<li><strong>סופגניות:</strong> כ-1.5 למבוגר ו-1 לילד. מ-500 גרם קמח יוצאות כ-16 סופגניות.</li>
<li><strong>תוספות:</strong> שמנת חמוצה או יוגורט ורסק תפוחים, כ-50 גרם מכל אחד לאדם.</li>
<li><strong>שתייה:</strong> כחצי ליטר לאדם לערב של שלוש שעות.</li></ul>
<p>לחישוב מהיר לפי מספר האורחים שלכם: <a href="{{up}}{HE_TOOL}">מחשבון סופגניות ולביבות</a>.</p>
<h2>תפריט פשוט לערב חנוכה</h2>
<ul><li>לביבות תפוחי אדמה (ואם רוצים גם לביבות גבינה או ירקות לגיוון)</li><li>סלט גדול ולחם, למי שלא רוצה רק טיגון</li>
<li>סופגניות — קונים או מכינים</li><li>פירות, מטבעות שוקולד לילדים, תה וקפה</li></ul>
<h2>רשימת קניות</h2>
<p>חלקו את הקניות לשתיים: <strong>יבשים</strong> (קמח, שמן, סוכר, שמרים, חד-פעמי, נרות) כמה ימים לפני, ו<strong>טריים</strong> (תפוחי אדמה, בצל, ביצים, שמנת) יום לפני. אל תשכחו 44 נרות לכל חנוכייה, ושמן בכמות שמספיקה גם לטיגון עמוק (לפחות ליטר לסיר סופגניות).</p>
<h2>ביום המסיבה</h2>
<ol><li>מגררים תפוחי אדמה וסוחטים היטב את הנוזלים — זה הסוד ללביבות פריכות.</li><li>מטגנים בשמן חם בסבבים קטנים, ומניחים על נייר סופג.</li>
<li>שומרים חמים בתנור על חום נמוך עד שכולם מגיעים.</li><li>מדליקים נרות יחד, שרים ומחלקים סביבונים.</li></ol>
<h2>מתנות לשמונה לילות</h2><p>אם נותנים מתנה בכל ערב, רשמו מראש למי, מה ומה התקציב. כך לא נתקעים ביום השביעי בלי רעיון, ורואים כמה כבר הוצאתם.</p>
<div class="cta-box mt-4"><div><h2 class="h3">כל זה בקובץ אחד</h2><p>«מתכנן מסיבת חנוכה» באקסל: רשימת אורחים, חישוב סופגניות ולביבות, רשימת קניות אוטומטית עם עלות, צ'קליסט ומעקב מתנות ל-8 לילות. ₪19.</p></div>
<a class="btn accent" href="{{up}}{HE_PLAN}">למתכנן המסיבה</a></div>
"""
faq_g3 = [("כמה זמן לפני לטגן לביבות?", "הכי טעים לטגן סמוך להגשה. אפשר לטגן עד שעתיים לפני ולחמם בתנור (180 מעלות, כ-10 דקות) על תבנית, בלי לכסות."),
          ("כמה סופגניות להזמין למסיבה של 20 איש?", "לפי 1.5 למבוגר ו-1 לילד: ל-12 מבוגרים ו-8 ילדים צריך כ-26 סופגניות. במחשבון אפשר לשנות לפי התיאבון.")]
guide(HE_G3, "איך מארגנים מסיבת חנוכה: כמויות, תפריט ורשימת קניות | תכנון פלוס",
      "מדריך לאירוח בחנוכה: כמה לביבות וסופגניות לאדם, תפריט פשוט, רשימת קניות, סדר עבודה ביום המסיבה ומעקב מתנות לשמונה לילות.",
      "איך מארגנים מסיבת חנוכה: כמויות, תפריט ורשימת קניות", g3, faq_g3, [("חנוכה 2026", HE_HUB), ("מסיבת חנוכה", HE_G3)], img=LIMG + "quantities.webp")

# ================================================================== ENGLISH
EN_TERMS_NOTE = f'<p class="hk-note">Prices in USD. See our <a href="{{up}}{EN_TERMS}">terms &amp; refund policy</a>.</p>'

faq_pack_en = [
    ("What ages is it for?", "Kids about 4 to 10. There are simple coloring pages for little ones, an easy and a tricky maze, a word search and a counting page."),
    ("Can I print it for my class?", "Yes. Print as many copies as you need for your family, classroom or Hebrew school. Please don’t resell or share the file online."),
    ("What paper size?", "You get two PDFs: US Letter and A4. 20 pages each, vector art, so lines stay crisp on any home printer."),
    ("Are the blessings included?", "Yes: the three candle blessings in Hebrew with vowels, transliteration and English translation, plus a 2026 lighting chart with dates."),
    ("Which dreidel letters do you use?", "Nun, Gimel, Hei, Shin (“a great miracle happened there”), with a note that Israeli dreidels have Pe instead of Shin."),
    ("How do I get it?", "Right after paying with PayPal (or a debit/credit card, no PayPal account needed) you’re taken to your download page."),
]
body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<div class="split"><div>
<h1>Hanukkah Activity Pack 2026 – Printable Coloring Pages, Mazes &amp; Games</h1>
<p class="lead">20 print-ready pages for kids: Hanukkah coloring pages, mazes, a word search, the dreidel game with a score sheet, a cut-and-fold dreidel, a 2026 candle-lighting chart and the blessings.</p>
</div>
<div id="buy" class="buy" data-product="hanukkah-activity-pack-en" data-compact="1"></div>
<ul class="hero-points"><li>20 pages, US Letter + A4 PDF</li><li>Original, clean line art</li><li>Ages 4–10</li><li>Print as often as you like</li><li>Instant download</li></ul>
</div>
<p class="hk-note mt-2">Hosting too? Get the activity pack and the party planner together in the <a href="{{up}}{EN}#bundle">Hanukkah bundle</a> for $19 instead of $24.</p>
</div></section>
<section class="section alt"><div class="container">
<div class="section-head"><h2>Peek inside</h2><p class="muted">Pages from the actual PDF.</p></div>
{pages_grid([("pack-cover", 750, "Cover of the Hanukkah Activity Pack", "Cover"), ("pack-coloring", 750, "Menorah coloring page", "Menorah coloring page"),
             ("pack-maze", 750, "Hanukkah maze for kids", "Easy maze"), ("pack-wordsearch", 750, "Hanukkah word search", "Word search"),
             ("pack-dreidel-rules", 750, "How to play dreidel page", "Dreidel game rules"), ("pack-diy", 750, "Cut and fold paper dreidel", "Make your own dreidel"),
             ("pack-chart", 750, "Hanukkah 2026 candle lighting chart", "2026 lighting chart"), ("pack-blessings", 750, "Hanukkah candle blessings with transliteration", "Blessings")], "{up}" + EIMG)}
</div></section>
<section class="section"><div class="container">
<div class="section-head"><h2>What’s inside</h2></div>
<div class="grid cols-3">
<div class="card feature"><span class="ic" aria-hidden="true">🖍️</span><div><h3>5 coloring pages</h3><p>Menorah, dreidels, latkes and a jelly doughnut, a menorah in the window and the little jug of oil.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🧩</span><div><h3>Puzzles</h3><p>Easy and tricky mazes, a 14-word search, color-by-number and “Count the Candles”.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🎲</span><div><h3>Dreidel game</h3><p>Illustrated rules for Nun, Gimel, Hei, Shin, a 5-player score sheet and a paper dreidel to build.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🕎</span><div><h3>2026 lighting chart</h3><p>All eight nights with dates, candle counts and notes for the two Friday nights and Saturday night.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">📜</span><div><h3>The blessings</h3><p>Hebrew with vowels, transliteration and English, in large print to keep by the menorah.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">💌</span><div><h3>Kindness &amp; cards</h3><p>“8 Nights of Kindness” chart, two cards to color and cut out, and an answer key.</p></div></div>
</div></div></section>
<section class="section alt"><div class="container narrow">
<h2>FAQ</h2>{faq_html(faq_pack_en)}
<h2 class="mt-4">More for Hanukkah</h2>
<ul class="hk-list"><li><a href="{{up}}{EN_G1}">When is Hanukkah 2026? Dates, lighting order and blessings</a></li>
<li><a href="{{up}}{EN_G2}">How to play dreidel (rules for kids)</a></li><li><a href="{{up}}{EN_TOOL}">How many latkes per person? Free calculator</a></li>
<li><a href="{{up}}{EN_PLAN}">Hanukkah Party Planner</a></li></ul>
<div class="mt-3"><div class="buy" data-product="hanukkah-activity-pack-en" data-compact="1"></div></div>{EN_TERMS_NOTE}
</div></section>
<div class="buy-bar"><span><strong>Hanukkah Activity Pack</strong> · <span class="price">$12</span></span><a class="btn small" href="#buy">Buy</a></div>
"""
t = "Hanukkah Activity Pack 2026 – Printable Coloring Pages, Mazes & Word Search"
d = "20 printable Hanukkah activities for kids: coloring pages, mazes, word search, dreidel game & score sheet, paper dreidel, 2026 candle chart and blessings. Letter + A4 PDF, $12."
page(EN_PACK, t, d, body, [product_ld("Hanukkah Activity Pack 2026", d, EN_PACK, 12, [EIMG + "pack-cover.webp", EIMG + "pack-coloring.webp", EIMG + "pack-maze.webp"], "USD", "en"), faq_ld(faq_pack_en)],
     og_image=EIMG + "pack-cover.webp", crumbs=[("Activity Pack", EN_PACK)], lang="en", buy=True, alt=HE_PACK)

faq_plan_en = [
    ("Does it work in Google Sheets?", "Yes. It’s a regular .xlsx with formulas only (no macros): upload it to Google Drive and choose Open with Google Sheets. It also works in Excel (desktop, web and mobile), Numbers and LibreOffice."),
    ("How does it know how many latkes I need?", "It counts confirmed guests on the Guests sheet (optionally “maybe” too) and multiplies by editable per-person amounts: 4 latkes per adult and 2 per kid, about 9 latkes per pound of potatoes."),
    ("I make my own sufganiyot. Does it help?", "Choose “Make” and it works out batches of dough (4 cups flour ≈ 16 doughnuts) and how much flour, yeast, sugar, eggs, milk, butter, jelly and oil to buy."),
    ("What’s the 8-night gift tracker?", "One row per gift: night, who it’s for, the gift, budget, actual cost and status. You see totals per night and budget vs. spent on a chart."),
    ("Are the prices real?", "No, they are example prices so the totals work from the start. Replace them with your local prices."),
]
body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<div class="split"><div>
<h1>Hanukkah Party Planner – Guests, Latke Quantities, Shopping &amp; Gifts</h1>
<p class="lead">Enter your guest list and the spreadsheet works out how many latkes and jelly doughnuts to make, builds a shopping list with an estimated cost and tracks gifts for all eight nights.</p>
</div>
<div id="buy" class="buy" data-product="hanukkah-party-planner-en" data-compact="1"></div>
<ul class="hero-points"><li>Excel + Google Sheets</li><li>Quantities from your RSVPs</li><li>Automatic shopping list</li><li>8-night gift tracker</li><li>Instant download</li></ul>
</div>
<p class="hk-note mt-2">Just need numbers? Try the free <a href="{{up}}{EN_TOOL}">latke &amp; doughnut calculator</a>.</p>
<img class="hk-hero-img mt-3" src="{{up}}{EIMG}planner-dashboard.webp" width="857" height="577" alt="Hanukkah party planner dashboard with guests, quantities, shopping cost and gift budget" fetchpriority="high">
</div></section>
<section class="section"><div class="container">
<div class="section-head"><h2>What’s in the workbook</h2><p class="muted">7 linked sheets. Type only in the yellow cells.</p></div>
<div class="grid cols-3">
<div class="card feature"><span class="ic" aria-hidden="true">👨‍👩‍👧</span><div><h3>Guests &amp; RSVPs</h3><p>Adults and kids, yes / maybe / no, which night, who brings what, allergies.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🥔</span><div><h3>Latke &amp; doughnut math</h3><p>From your guests and an appetite setting: latkes, doughnuts, pounds of potatoes, eggs, flour and oil.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🛒</span><div><h3>Shopping list</h3><p>Built from the quantities, with price per unit, estimated total and a bought checkbox.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🎁</span><div><h3>Gifts for 8 nights</h3><p>Who, what, budget, actual cost and status — with totals per night.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">✅</span><div><h3>Prep checklist</h3><p>16 ready tasks with due dates counted back from your party date.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">📊</span><div><h3>Dashboard</h3><p>Everything at a glance, with charts for gift spending and shopping cost.</p></div></div>
</div></div></section>
<section class="section alt"><div class="container">
<div class="section-head"><h2>Screenshots</h2><p class="muted">From the included example workbook. Numbers are for illustration.</p></div>
<div class="screens">
<figure><img src="{{up}}{EIMG}planner-quantities.webp" loading="lazy" width="934" height="670" alt="Quantities sheet: latkes, doughnuts and ingredients"><figcaption>Quantities from your guest count</figcaption></figure>
<figure><img src="{{up}}{EIMG}planner-shopping.webp" loading="lazy" width="900" height="700" alt="Automatic Hanukkah shopping list"><figcaption>Shopping list with estimated cost</figcaption></figure>
<figure><img src="{{up}}{EIMG}planner-gifts.webp" loading="lazy" width="1264" height="380" alt="Gift tracker for the eight nights of Hanukkah"><figcaption>8-night gift tracker</figcaption></figure>
<figure><img src="{{up}}{EIMG}planner-guests.webp" loading="lazy" width="1300" height="400" alt="Guest list with RSVPs"><figcaption>Guests and RSVPs</figcaption></figure>
</div></div></section>
<section class="section"><div class="container narrow">
<h2>FAQ</h2>{faq_html(faq_plan_en)}
<div class="mt-3"><div class="buy" data-product="hanukkah-party-planner-en" data-compact="1"></div></div>{EN_TERMS_NOTE}
</div></section>
<div class="buy-bar"><span><strong>Hanukkah Party Planner</strong> · <span class="price">$12</span></span><a class="btn small" href="#buy">Buy</a></div>
"""
t = "Hanukkah Party Planner Spreadsheet – Latke Quantities, Shopping List & Gift Tracker"
d = "Hanukkah party planner for Excel and Google Sheets: guest list, how many latkes and doughnuts to make, automatic shopping list and an 8-night gift tracker. $12, instant download."
page(EN_PLAN, t, d, body, [product_ld("Hanukkah Party Planner", d, EN_PLAN, 12, [EIMG + "planner-dashboard.webp", EIMG + "planner-quantities.webp"], "USD", "en"), faq_ld(faq_plan_en)],
     og_image=EIMG + "planner-dashboard.webp", crumbs=[("Party Planner", EN_PLAN)], lang="en", buy=True, alt=HE_PLAN)

faq_tool_en = [
    ("How many latkes per person?", "Plan on about 4 medium latkes per adult and 2 per child when there are other dishes. If latkes are the main course, choose “Hungry” (about 30% more)."),
    ("How many latkes from a pound of potatoes?", "Roughly 8–10 medium latkes (a heaping tablespoon each). The calculator uses 9, with half an onion, one egg and 2 tablespoons of flour or matzo meal per pound."),
    ("How many sufganiyot (jelly doughnuts) per person?", "About 1.5 per adult and 1 per child. A batch made with 4 cups of flour gives about 16 doughnuts."),
    ("How much oil do I need?", "For shallow-frying latkes, about ½ cup per pound of potatoes. For deep-frying doughnuts, at least 4 cups in the pot; it’s reused for every batch."),
    ("Is my data saved?", "No. Everything is calculated in your browser."),
]
body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<h1>How Many Latkes Per Person? Latke &amp; Sufganiyot Calculator</h1>
<p class="lead">Enter how many adults and kids are coming and instantly see how many latkes and jelly doughnuts to make or buy — and how many pounds of potatoes, eggs, flour and oil to get.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
{calc_panel("en")}
<div class="cta-box mt-4"><div><h2 class="h3">Let the spreadsheet do it from your RSVPs</h2><p>The Hanukkah Party Planner calculates quantities straight from your guest list, builds a priced shopping list and tracks gifts for all eight nights. $12.</p></div>
<a class="btn accent" href="{{up}}{EN_PLAN}">See the planner</a></div>
</div></section>
<section class="section alt"><div class="container narrow prose">
<h2>How the calculator works</h2>
<ul><li>Latkes: 4 per adult, 2 per kid; about 9 latkes per pound of potatoes.</li><li>Per pound of potatoes: ½ onion, 1 egg, 2 tbsp flour or matzo meal, ½ cup oil.</li>
<li>Doughnuts: 1.5 per adult, 1 per kid; 4 cups of flour ≈ 16 doughnuts.</li><li>“Light” appetite = 75% of the amounts, “Hungry” = 130%.</li></ul>
<p>These are estimates for a typical home party, not rules. Round up for hungry teenagers and down if there’s a full dinner too.</p>
<h2>FAQ</h2>{faq_html(faq_tool_en)}
<p class="mt-3"><a href="{{up}}{EN_G1}">When is Hanukkah 2026?</a> · <a href="{{up}}{EN}">All Hanukkah 2026 printables</a></p>
</div></section>
<script>window.HK_CALC = {json.dumps(EN_CALC_CFG)};</script>{CALC_JS}
"""
t = "How Many Latkes Per Person? Free Latke & Sufganiyot Calculator (Hanukkah 2026)"
d = "Free Hanukkah calculator: how many latkes and jelly doughnuts to make for your guests, plus pounds of potatoes, eggs, flour and oil to buy. Instant results."
page(EN_TOOL, t, d, body, [app_ld("Latke & Sufganiyot Calculator", d, EN_TOOL, "en", "USD"), faq_ld(faq_tool_en)],
     og_image=EIMG + "planner-quantities.webp", crumbs=[("Latke calculator", EN_TOOL)], lang="en", alt=HE_TOOL)

# ---------------------------------------------------------------- en hub
body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<h1>Hanukkah 2026: Printable Activities, Party Planner &amp; Dates</h1>
<p class="lead">Hanukkah 2026 begins at sundown on Friday, December 4, and ends at nightfall on Saturday, December 12. Here are printable kids’ activities, a party planner, a free latke calculator and guides.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
<div class="grid cols-2">
<article class="card pad-lg"><h2 class="h3"><a href="{{up}}{EN_PACK}">Hanukkah Activity Pack</a></h2>
<img src="{{up}}{EIMG}pack-cover.webp" alt="Hanukkah Activity Pack cover" width="595" height="770" loading="lazy" style="max-width:200px;height:auto;float:inline-end;margin-inline-start:1rem;border:1px solid var(--border);border-radius:8px">
<p>20 printable pages: coloring, mazes, word search, dreidel game, 2026 candle chart and blessings. US Letter + A4.</p><p><strong>$12</strong></p><a class="btn" href="{{up}}{EN_PACK}">Details</a></article>
<article class="card pad-lg"><h2 class="h3"><a href="{{up}}{EN_PLAN}">Hanukkah Party Planner</a></h2>
<img src="{{up}}{EIMG}planner-dashboard.webp" alt="Party planner dashboard" width="857" height="577" loading="lazy" style="width:100%;height:auto;border:1px solid var(--border);border-radius:8px">
<p>Guests, latke and doughnut quantities, shopping list and an 8-night gift tracker. Excel + Google Sheets.</p><p><strong>$12</strong></p><a class="btn" href="{{up}}{EN_PLAN}">Details</a></article>
</div>
<article class="card pad-lg mt-3" id="bundle"><div class="split"><div><h2 class="h3">Hanukkah Bundle: both for $19</h2><p>The Activity Pack + the Party Planner. $19 instead of $24.</p><span class="badge success">Save $5</span></div>
<div class="buy" data-product="hanukkah-bundle-en" data-compact="1"></div></div></article>
{EN_TERMS_NOTE}
</div></section>
<section class="section alt"><div class="container narrow">
<h2>Hanukkah 2026 candle lighting dates</h2>{EN_DATES_TABLE}
<p class="hk-note mt-1">On the two Fridays, light before the Shabbat candles; on Saturday night, after Shabbat ends. <a href="{{up}}{EN_G1}">Full guide with blessings</a>.</p>
<h2 class="mt-4">Free tools &amp; guides</h2>
<ul class="hk-list"><li><a href="{{up}}{EN_TOOL}">How many latkes per person? Calculator</a></li><li><a href="{{up}}{EN_G1}">When is Hanukkah 2026?</a></li>
<li><a href="{{up}}{EN_G2}">How to play dreidel</a></li><li><a href="{{up}}{HE_HUB}" hreflang="he" lang="he">חנוכה 2026 בעברית</a></li></ul>
</div></section>
"""
t = "Hanukkah 2026 – Printable Activities for Kids, Party Planner & Candle Lighting Dates"
d = "Hanukkah 2026 starts Friday, December 4 at sundown. Printable Hanukkah activity pack, party planner spreadsheet, free latke calculator and candle lighting chart."
page(EN, t, d, body, [{"@context": "https://schema.org", "@type": "CollectionPage", "name": t, "description": d, "url": BASE + EN, "inLanguage": "en-US"}],
     og_image=EIMG + "pack-cover.webp", crumbs=[], lang="en", buy=True, alt=HE_HUB)

# ---------------------------------------------------------------- en guides
bl_en = "".join(f'<h3>{lbl}</h3><p class="hk-bracha" lang="he" dir="rtl">{he}</p><p><em>{tr}</em></p><p>{en}</p>'
                for lbl, he, (tr, en) in zip(["Blessing 1 (every night)", "Blessing 2 (every night)", "Blessing 3 (first night only)"], pack.BRACHOT_HE, pack.BRACHOT_EN))
g1e = f"""
<p>In 2026 Hanukkah runs from <strong>sundown on Friday, December 4, to nightfall on Saturday, December 12</strong>. You light the first candle on Friday evening, December 4 (25 Kislev 5787), and the eighth candle on Friday, December 11.</p>
<h2>Hanukkah 2026 candle lighting chart</h2>{EN_DATES_TABLE}
<p>For one menorah you need 44 candles in total: 36 candles plus a shamash each night — exactly one standard box.</p>
<h2>Two Friday nights this year</h2>
<p>Both the first and the eighth nights fall on Friday. On those evenings, light the Hanukkah candles <strong>before</strong> the Shabbat candles, and use candles big enough to burn until at least 30 minutes after nightfall (standard small Hanukkah candles often don’t last that long). On Saturday night, December 5, light after Shabbat ends; families differ on whether Havdalah or Hanukkah candles come first.</p>
<h2>How to light the menorah</h2>
<ol><li>Place the candles from right to left: night one has a single candle on the far right, and each night you add one to its left.</li>
<li>Light the shamash (helper candle) and say the blessings.</li><li>Use the shamash to light the candles from left to right — newest candle first.</li>
<li>Put the shamash back in its place and sing Maoz Tzur.</li></ol>
<h2>The Hanukkah blessings</h2>{bl_en}
<p class="hk-note">Some say “l’hadlik ner Hanukkah” in the first blessing. In the Hebrew above the Divine Name is abbreviated (ה׳); say it as usual when reciting.</p>
<p>Want this chart and the blessings printed next to your menorah, plus 18 pages of activities for the kids? It’s all in the <a href="{{up}}{EN_PACK}">Hanukkah Activity Pack</a>.</p>
"""
faq_g1e = [("When does Hanukkah start in 2026?", "At sundown on Friday, December 4, 2026. The eighth and last candle is lit on Friday, December 11, and Hanukkah ends at nightfall on Saturday, December 12."),
           ("Is Hanukkah on the same date every year?", "It always starts on 25 Kislev in the Hebrew calendar, which moves against the regular calendar. In 2025 it started December 14; in 2026 it starts December 4."),
           ("How many candles do I need for Hanukkah?", "44 per menorah: 1+2+…+8 = 36 candles, plus a shamash on each of the eight nights.")]
guide(EN_G1, "When Is Hanukkah 2026? Dates, Candle Lighting Chart & Blessings",
      "Hanukkah 2026 begins at sundown Friday, December 4 and ends Saturday, December 12. Candle lighting chart, how to light the menorah, Friday-night rules and the blessings.",
      "When Is Hanukkah 2026? Dates, Lighting Order and Blessings", g1e, faq_g1e, [("When is Hanukkah 2026?", EN_G1)], lang="en", alt=HE_G1, img=EIMG + "pack-chart.webp")

g2e = f"""
<p>Dreidel is the classic Hanukkah game: a four-sided spinning top and a pot of treats. It takes a minute to learn and works for ages 4 to 94.</p>
<h2>What you need</h2><ul><li>A dreidel (or <a href="{{up}}{EN_PACK}">print one and fold it</a>)</li><li>10–15 small pieces per player: chocolate gelt, pennies, raisins, nuts or candy</li><li>2 or more players</li></ul>
<h2>The letters</h2>
<p>Each side has a Hebrew letter. Together they stand for <em>Nes Gadol Hayah Sham</em>, “a great miracle happened there”. In Israel the last letter is Pe (<em>Poh</em>, “here”) instead of Shin.</p>
<div class="table-wrap"><table class="hk-dates"><tr><th>Letter</th><th>Name</th><th>What you do</th></tr>
<tr><td lang="he">נ</td><td>Nun</td><td>Nothing. Next player.</td></tr><tr><td lang="he">ג</td><td>Gimel</td><td>Take the whole pot!</td></tr>
<tr><td lang="he">ה</td><td>Hei</td><td>Take half the pot (round down).</td></tr><tr><td lang="he">ש / פ</td><td>Shin / Pe</td><td>Put one piece in the pot.</td></tr></table></div>
<h2>How to play</h2>
<ol><li>Everyone starts with the same number of pieces.</li><li>Each player puts one piece in the pot.</li><li>Take turns spinning; do what the letter says.</li>
<li>Whenever the pot is empty (after a Gimel), everyone puts in one piece again.</li><li>If you run out of pieces you’re out — or agree on a “loan” so little ones can keep playing.</li>
<li>Play until one person has everything, or set a timer and whoever has the most wins.</li></ol>
<h2>Tips for playing with kids</h2>
<ul><li>Keep score on paper for school-age kids — it’s sneaky addition and subtraction practice.</li><li>For preschoolers skip the “half” rule: Hei = take two.</li>
<li>Spin on a hard, flat surface like a tray or table, not a tablecloth.</li></ul>
<div class="cta-box mt-4"><div><h2 class="h3">Printable dreidel rules, score sheet &amp; paper dreidel</h2><p>The Hanukkah Activity Pack includes an illustrated rules page, a 5-player score sheet and a cut-and-fold dreidel, plus 17 more pages. $12.</p></div>
<a class="btn accent" href="{{up}}{EN_PACK}">See the pack</a></div>
<p><img src="{{up}}{EIMG}pack-dreidel-rules.webp" alt="Printable dreidel rules page" width="595" height="770" loading="lazy" style="max-width:280px;height:auto"></p>
"""
faq_g2e = [("What do the letters on a dreidel mean?", "Nun, Gimel, Hei, Shin stand for “Nes Gadol Hayah Sham” — a great miracle happened there. Israeli dreidels use Pe for “Poh” — here."),
           ("What does Hei mean in dreidel?", "Take half of the pot. If there’s an odd number of pieces, round down (some families round up — agree before you start).")]
guide(EN_G2, "How to Play Dreidel: Simple Rules for Kids (Printable Score Sheet)",
      "How to play dreidel: what Nun, Gimel, Hei and Shin mean, step-by-step rules, tips for playing with young kids and a printable score sheet.",
      "How to Play Dreidel: Simple Rules for Kids", g2e, faq_g2e, [("How to play dreidel", EN_G2)], lang="en", img=EIMG + "pack-dreidel-rules.webp")

# ---------------------------------------------------------------- en thanks (noindex) + terms
body = """
<section class="section"><div class="container narrow">
<h1>Thank you! Your downloads</h1>
<div id="loading" class="result"><p class="mb-0">Loading your order…</p></div>
<noscript><p>Please enable JavaScript to show your download links.</p></noscript>
<div id="error" class="callout warn" hidden><p class="mb-0">We couldn’t find this order link. If you paid, email us with your PayPal receipt and we’ll send your files right away.</p></div>
<div id="ok" hidden>
<p id="test-flag" class="callout warn" hidden>TEST MODE — no payment was taken.</p>
<p>Your files are ready. <strong>Bookmark this page</strong> or copy its link to download again later.</p>
<div id="downloads"></div>
<div class="card mt-3"><h2 class="h3">Receipt</h2><dl class="small"><dt>Product</dt><dd id="r-title"></dd><dt>Amount</dt><dd id="r-price"></dd><dt>Order</dt><dd id="r-order"></dd><dt>Date</dt><dd id="r-date"></dd></dl>
<button type="button" class="btn secondary small" id="copy-link">Copy this page’s link</button></div>
<p class="small mt-2" id="support"></p>
</div></div></section>
"""
THANKS_JS = r"""<script>
(function () {
  "use strict";
  var G = window.SITE, esc = G.escape, $ = function (id) { return document.getElementById(id); };
  var q = new URLSearchParams(location.search), slug = q.get("p") || "", order = q.get("o") || "", test = q.get("test") === "1";
  function fail() { $("loading").hidden = true; $("error").hidden = false; }
  function money(p) { var c = (p.currency || "ILS").toUpperCase(), v = p.price != null ? p.price : p.price_ils; return ({ USD: "$", ILS: "₪" }[c] || c + " ") + v; }
  function list(p) {
    var items = (p.files || []).map(function (f) {
      var ext = (/\.([a-z0-9]+)$/i.exec(f.path) || [, ""])[1].toUpperCase();
      return '<li><a class="dl" href="' + esc(G.url(f.path)) + '" download><span>' + esc(f.label) + '</span><span class="ext">' + ext + "</span></a></li>";
    });
    return items.length ? '<ul class="downloads">' + items.join("") + "</ul>" : '<p class="callout warn">Files are being prepared. Email us your order number and we’ll send them.</p>';
  }
  if (!/^[a-z0-9-]+$/.test(slug) || !order || order.length > 64) return fail();
  Promise.all([G.getJSON("data/products/" + slug + ".json"), G.config()]).then(function (r) {
    var p = r[0], cfg = r[1];
    return Promise.all((p.bundle_of || []).map(function (s) { return G.getJSON("data/products/" + s + ".json").catch(function () { return null; }); }))
      .then(function (ms) { return { p: p, ms: ms.filter(Boolean), cfg: cfg }; });
  }).then(function (d) {
    var p = d.p;
    document.title = "Thank you! Download " + p.title;
    $("downloads").innerHTML = d.ms.length ? d.ms.map(function (m) { return '<h2 class="h3 mt-2">' + esc(m.title) + "</h2>" + list(m); }).join("") : list(p);
    $("r-title").textContent = p.title; $("r-price").textContent = money(p); $("r-order").textContent = order;
    $("r-date").textContent = new Date().toLocaleDateString("en-US"); $("test-flag").hidden = !test;
    var email = d.cfg.SELLER_EMAIL && d.cfg.SELLER_EMAIL !== "SELLER_EMAIL" ? d.cfg.SELLER_EMAIL : "";
    if (email) $("support").innerHTML = 'File won’t open or something unclear? Email <a href="mailto:' + esc(email) + "?subject=" + encodeURIComponent("Order " + order) + '">' + esc(email) + "</a> with your order number.";
    $("loading").hidden = true; $("ok").hidden = false;
    try { var k = "tp-orders", arr = JSON.parse(localStorage.getItem(k) || "[]"); if (!arr.some(function (x) { return x.o === order; })) { arr.push({ p: slug, o: order, t: Date.now(), test: test }); localStorage.setItem(k, JSON.stringify(arr.slice(-30))); } } catch (e) {}
  }).catch(fail);
  $("copy-link").addEventListener("click", function () { var b = this; if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () { b.textContent = "Link copied ✓"; }); else prompt("Copy this link:", location.href); });
})();
</script>"""
page(EN_THANKS, "Thank you – your Hanukkah downloads", "Your download page.", body, [], crumbs=[("Thank you", EN_THANKS)], lang="en", noindex=True,
     scripts=[THANKS_JS])

body = """
<article class="section"><div class="container narrow prose">{CRUMBS}
<h1>Terms of sale &amp; refund policy</h1>
<p class="updated muted">Updated: November 17, 2026</p>
<h2>What you buy</h2><p>Digital files (PDF and Excel/.xlsx) delivered by download immediately after payment. Nothing is shipped. Prices are in US dollars and include any fees we charge; your bank or PayPal may apply currency conversion.</p>
<h2>License</h2><p>For personal, family and classroom use: print as many copies as you need for your own household, class or school group. You may not resell, share or upload the files, or claim them as your own.</p>
<h2>Payment</h2><p>Payments are processed by PayPal (PayPal account or debit/credit card as a guest). We never see or store your card details.</p>
<h2>Refunds</h2><p>Because files are delivered instantly, sales are final. If a file is faulty or won’t open and we can’t fix it, or you were charged twice, email us within 14 days with your order number and we’ll fix it or refund you in full.</p>
<h2>Accuracy</h2><p>Dates and blessing texts were checked carefully; quantity estimates in the planner and calculator are guidelines only. Customs vary between communities — follow your own.</p>
<h2>Contact</h2><p id="contact">Questions: see the email on your download page, or the contact link on our <a href="{up}legal/terms/" hreflang="he">Hebrew terms page</a> (the full legal terms of the seller, in Hebrew, also apply).</p>
</div></article>
<script>document.addEventListener("DOMContentLoaded", function(){ if (!window.SITE) return; SITE.config().then(function (c) { if (c.SELLER_EMAIL && c.SELLER_EMAIL !== "SELLER_EMAIL") document.getElementById("contact").innerHTML = 'Questions or problems: <a href="mailto:' + SITE.escape(c.SELLER_EMAIL) + '">' + SITE.escape(c.SELLER_EMAIL) + "</a>."; }); });</script>"""
page(EN_TERMS, "Terms of Sale & Refund Policy – Tichnun Plus Hanukkah", "Terms of sale, license and refund policy for Hanukkah printables and planners.", body, [],
     crumbs=[("Terms", EN_TERMS)], lang="en")
print("pages written")
