#!/usr/bin/env python3
"""Pesach 2027 (Hebrew): hub docs/pesach/ (hreflang/links to the English Passover pages), free cleaning checklist page + PDF,
product p/seder-planner/ (₪19), Purim+Pesach bundle (₪29), free calculator tools/matza-wine-calculator/, 3 guides.
    python3 pages_pesach.py"""
from site_common2027 import *  # noqa: F401,F403
from printables import CLEAN as ROOMS, TIMELINE as CLEAN_TL

SEDER = D["pesach"]            # 15 Nisan; the seder is the evening before
EREV, SHVII, CHUL, BEDIKA = D["erev_pesach"], D["shvii"], D["acharon_chul"], D["bedika"]
SIMG = S_PROD + "img/"
SEDER_TXT = f"ליל הסדר בשנת 2027 (תשפ״ז) הוא ב<strong>{hd(SEDER, evening=True)}</strong>"
SRC_SHIUR = "https://www.etzion.org.il/he/halakha/orach-chaim/prayer-and-blessings/%D7%A9%D7%99%D7%A2%D7%95%D7%A8-%D7%9B%D7%91%D7%99%D7%A6%D7%94-%D7%95%D7%9B%D7%96%D7%99%D7%AA-%D7%91%D7%99%D7%9E%D7%99%D7%A0%D7%95-%D7%9C%D7%A2%D7%A0%D7%99%D7%99%D7%9F-%D7%91%D7%A8%D7%9B%D7%95%D7%AA"


def dates_table():
    import datetime as dt
    chm0, chm1 = SEDER + dt.timedelta(days=1), SHVII - dt.timedelta(days=1)
    rows = [("בדיקת חמץ (ליל י״ד בניסן)", hd(BEDIKA) + " בערב"), ("ערב פסח: סוף אכילת חמץ וביעור חמץ", hd(EREV) + " בבוקר"),
            ("<strong>ליל הסדר</strong>", f"<strong>{hd(SEDER, evening=True)}</strong>"), ("פסח, יום טוב ראשון (ט״ו בניסן)", hd(SEDER)),
            ("חול המועד (בארץ)", f"{hd(chm0, weekday=False)} – {hd(chm1, weekday=False)}"), ("שביעי של פסח (כ״א בניסן)", f"{hd(SHVII)} (מתחיל בערב הקודם)"),
            ("מימונה / צאת החג בארץ", hd(SHVII) + " בערב"), ("חו״ל: סדר שני", hd(SEDER) + " בערב"), ("חו״ל: אחרון של פסח (כ״ב בניסן)", hd(CHUL))]
    return ('<div class="table-wrap"><table class="s27-table"><caption class="sr-only">תאריכי פסח 2027</caption><tr><th>מה</th><th>מתי</th></tr>'
            + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows) + "</table></div>")


def clean_box():
    return (f'<div class="s27-dl mt-2"><img src="{{up}}pesach/img/checklist-1.webp" alt="צ׳קליסט ניקיון לפסח חדר אחר חדר להדפסה" width="662" height="935" loading="lazy">'
            f'<div><h3 class="mt-0">צ׳קליסט ניקיון לפסח 2027: PDF חינם</h3><p>{len(ROOMS)} אזורים בבית, {sum(len(t) for _, t in ROOMS)} משימות לסימון, לוח זמנים עד ליל הסדר וטבלת «מי אחראי על מה». A4, 2 עמודים, בלי הרשמה.</p>'
            f'<a class="btn" href="{{up}}{PDF_CLEAN}" download>הורדת הצ׳קליסט</a> <a class="btn secondary" href="{{up}}{CLEAN}">הרשימה המלאה באתר</a></div></div>')


# ------------------------------------------------------------------ product
def product():
    faq = [("באיזו תוכנה זה עובד?", "Excel (2010 ומעלה, גם בנייד), Google Sheets ו-LibreOffice. אין מאקרו."),
           ("איך הקובץ מחשב כמה מצות ויין?", "לפי מספר המבוגרים והילדים שאישרו הגעה, מספר הסדרים (1 בארץ, 2 בחו״ל), שיעור הרביעית שבחרתם (86 או 150 מ״ל), כמה מהמבוגרים שותים יין, וכמה כזיתים מצה לכל מבוגר. את כל אלה קובעים בגיליון ההגדרות."),
           ("הכמויות לארוחה מדויקות?", "הן כללי אצבע מקובלים לאירוח (למשל 300 גרם בשר לפני בישול למבוגר) ונועדו כנקודת פתיחה. כל מספר בתא צהוב ניתן לשינוי."),
           ("יש בקובץ פסיקה הלכתית?", "לא. הקובץ מציג את השיעורים המקובלים עם מקורות, ומשאיר לכם לבחור לפי המנהג. לשאלות הלכה פנו לרב."),
           ("המחירים אמיתיים?", "לא. אלה מחירים לדוגמה כדי שהחישוב יעבוד מיד. מעדכנים לפי המחירים אצלכם."),
           ("איך מקבלים את הקובץ?", "מיד אחרי התשלום ב-PayPal (אפשר בכרטיס אשראי, בלי חשבון) נפתח דף הורדה עם קובץ ריק וקובץ דוגמה מלא.")]
    body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<div class="split"><div>
<h1>מתכנן ליל הסדר 2027 באקסל: אורחים, תפריט, כמויות, קניות ותפקידים בהגדה</h1>
<p class="lead">רושמים מי מגיע, והקובץ מחשב כמה מצות, יין, מרור וכל מצרכי הארוחה צריך, בונה רשימת קניות עם עלות, מחלק את קטעי ההגדה ומסדר לוח הכנות לפי התאריך.</p>
</div>
<div id="buy" class="buy" data-product="seder-planner" data-compact="1"></div>
<ul class="hero-points"><li>Excel ו-Google Sheets</li><li>מצות ויין לפי השיעור שתבחרו</li><li>27 מצרכים מוכנים + שורות שלכם</li><li>תפקידים בהגדה</li><li>הורדה מיידית</li></ul>
</div>
<p class="hk-note mt-2">רוצים קודם חישוב מהיר? <a href="{{up}}{S_TOOL}">מחשבון מצות ויין</a> החינמי. מארחים גם בפורים? <a href="{{up}}{PES}#{BUNDLE}">פורים + פסח ב-₪29</a>.</p>
<img class="hk-hero-img mt-3" src="img/dashboard.webp" width="1228" height="560" alt="דשבורד מתכנן ליל הסדר: אורחים, מצות, יין ועלות קניות" fetchpriority="high">
</div></section>
<section class="section"><div class="container">
<div class="section-head"><h2>מה יש בקובץ</h2><p class="muted">8 גיליונות מחוברים. מקלידים רק בתאים הצהובים.</p></div>
<div class="grid cols-3">
<div class="card feature"><span class="ic" aria-hidden="true">👨‍👩‍👧‍👦</span><div><h3>אורחים</h3><p>מבוגרים וילדים לכל משפחה, אישור הגעה, רגישויות ומה כל אחד מביא.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🍷</span><div><h3>מצות ויין לפי השיעור</h3><p>רביעית 86 או 150 מ״ל, כזיתים לכל מבוגר, מי שותה יין ומי מיץ ענבים.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🛒</span><div><h3>כמויות וקניות</h3><p>כמה לקנות מכל מצרך, באריזות שלמות, עם עלות משוערת וסימון מה נקנה.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">📖</span><div><h3>תפקידים בהגדה</h3><p>סימני הסדר וקטעי המגיד, ומי מוביל כל קטע: מה נשתנה, ארבעה בנים, עשר המכות.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">🗓️</span><div><h3>לוח הכנות</h3><p>16 משימות מ-6 שבועות לפני, עם תאריך יעד שמחושב לבד ומה שעבר מסומן באדום.</p></div></div>
<div class="card feature"><span class="ic" aria-hidden="true">📊</span><div><h3>דשבורד</h3><p>ימים לסדר, מצות, בקבוקי יין, עלות לסועד ועלות לפי קטגוריה מול התקציב.</p></div></div>
</div></div></section>
<section class="section alt"><div class="container">
<div class="section-head"><h2>ככה זה נראה</h2><p class="muted">מקובץ הדוגמה המצורף (17 סועדים). המספרים להמחשה.</p></div>
<div class="screens">
<figure><img src="img/shopping.webp" loading="lazy" width="1257" height="532" alt="גיליון כמויות וקניות לליל הסדר"><figcaption>כמויות וקניות</figcaption></figure>
<figure><img src="img/haggadah.webp" loading="lazy" width="1264" height="635" alt="חלוקת תפקידים בהגדה"><figcaption>תפקידים בהגדה</figcaption></figure>
<figure><img src="img/guests.webp" loading="lazy" width="1264" height="248" alt="רשימת אורחים לליל הסדר"><figcaption>אורחים</figcaption></figure>
</div></div></section>
<section class="section"><div class="container narrow">
<h2>שאלות נפוצות</h2>{faq_html(faq)}
<h2 class="mt-4">עוד לפסח 2027</h2>
{links([("צ׳קליסט ניקיון לפסח (PDF חינם)", CLEAN), ("איך מארגנים ליל סדר", S_G1), ("פסח 2027: תאריכים", S_G2), ("כל מה שצריך לפסח", PES),
        ("Passover Seder Planner (English, USD)", EN_SEDER)])}
<div class="mt-3"><div class="buy" data-product="seder-planner" data-compact="1"></div></div>
</div></section>
<div class="buy-bar"><span><strong>מתכנן ליל הסדר</strong> · <span class="price">₪19</span></span><a class="btn small" href="#buy">לרכישה</a></div>
"""
    t = "מתכנן ליל הסדר 2027 באקסל – כמויות מצות ויין, קניות והגדה | תכנון פלוס"
    d = "קובץ אקסל לפסח 2027: אורחים, תפריט, כמה מצות ויין צריך לפי השיעור שתבחרו, רשימת קניות עם עלות, תפקידים בהגדה ולוח הכנות. Excel ו-Google Sheets, ₪19."
    page(S_PROD, t, d, body, [product_ld("מתכנן ליל הסדר – פסח 2027", d, S_PROD, 19, [SIMG + "dashboard.webp", SIMG + "shopping.webp", SIMG + "haggadah.webp"]), faq_ld(faq)],
         og_image=SIMG + "dashboard.webp", crumbs=[("פסח 2027", PES), ("מתכנן ליל הסדר", S_PROD)], buy=True, alt=EN_SEDER)


# ------------------------------------------------------------------ calculator
CALC_JS = r"""
<script>
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  function n(id) { var v = parseFloat($(id).value); return isFinite(v) && v > 0 ? v : 0; }
  function r(name) { var x = document.querySelector('input[name="' + name + '"]:checked'); return x ? parseFloat(x.value) : 0; }
  function up(x, s) { s = s || 1; return Math.ceil(x / s - 1e-9) * s; }
  function f(x, d) { return Number(x).toLocaleString("he-IL", { maximumFractionDigits: d || 0 }); }
  function calc() {
    var A = n("adults"), K = n("kids"), S = r("seders") || 1, ml = r("reviit") || 86, share = Math.min(100, n("wine")) / 100;
    var kz = r("kz") || 3, kzm = n("kzm") || 2, days = n("days"), mpd = n("mpd"), box = n("box") || 30, M = 1.1;
    if (!A && !K) { $("out").hidden = true; $("empty").hidden = false; return; }
    var hand = up((A * kz + K * kz / 2) / kzm * S * M);
    var mach = up((A + K) * mpd * days), boxes = up(mach / box);
    var wine = up((A * share * 4 * ml + ml) * S * M / 750);
    var juice = up((A * (1 - share) + K) * 4 * ml * S * M / 1000, 0.5);
    $("k-hand").textContent = f(hand); $("k-wine").textContent = f(wine); $("k-juice").textContent = f(juice, 1); $("k-box").textContent = f(boxes);
    var rows = [["מצה שמורה עבודת יד (למצווה)", f(hand) + " מצות"], ["מצת מכונה לכל החג", f(mach) + " מצות ≈ " + f(boxes) + " חבילות"],
      ["יין לארבע כוסות + כוס של אליהו", f(wine) + " בקבוקי 750 מ״ל"], ["מיץ ענבים", f(juice, 1) + " ליטר"],
      ["חסה למרור", f(up((A * .15 + K * .1 + .5) * S)) + " ראשים"], ["ביצים (קערה + ביצה במי מלח)", f((A + K + 1) * S)],
      ["תפוחים לחרוסת", f(up((A + K) * .05 * S, .1), 1) + " ק״ג"], ["הגדות", f(A + K)]];
    $("list").innerHTML = rows.map(function (x) { return "<tr><td>" + x[0] + '</td><td class="num">' + x[1] + "</td></tr>"; }).join("");
    $("out").hidden = false; $("empty").hidden = true;
  }
  var fm = $("seder-form");
  fm.addEventListener("input", calc); fm.addEventListener("change", calc);
  calc();
})();
</script>"""


def calculator():
    faq = [("כמה מצות שמורות צריך לאדם בליל הסדר?", "בסדר אוכלים לפחות שלושה כזיתים: מוציא מצה, כורך ואפיקומן (שולחן ערוך, אורח חיים תע״ה, תע״ז), ויש נוהגים להוסיף. כמה כזיתים יש במצה תלוי בגודל המצה ובשיטה, ולכן המחשבון מאפשר לבחור. ברירת המחדל, חצי מצת יד לכזית, היא הערכה זהירה. לשאלה מעשית פנו לרב."),
           ("מה זה רביעית ולמה יש שתי אפשרויות?", "כל אחת מארבע הכוסות צריכה להכיל לפחות רביעית (שולחן ערוך, אורח חיים תע״ב, ט). לשיטת הגר״ח נאה רביעית היא כ-86 מ״ל, ולשיטת החזון איש כ-150 מ״ל. בוחרים לפי המנהג שלכם."),
           ("כמה בקבוקי יין צריך לליל הסדר?", "לפי 86 מ״ל לכוס, מבוגר ששותה יין צריך כ-344 מ״ל לארבע כוסות, כלומר כחצי בקבוק. לפי 150 מ״ל זה 600 מ״ל. המחשבון מוסיף כוס של אליהו לכל סדר ו-10% רזרבה."),
           ("כמה חבילות מצה לקנות לכל החג?", "תלוי כמה מצה אוכלים ביום. ברירת המחדל: 2 מצות לאדם ליום, 7 ימים, וכ-30 מצות בחבילת קילו. משנים לפי המשפחה ולפי מה שכתוב על האריזה."),
           ("הנתונים נשמרים?", "לא. החישוב רץ בדפדפן. קישור לשיתוף כולל רק את המספרים שהזנתם.")]
    body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<h1>כמה מצות ויין צריך לליל הסדר? מחשבון לפסח 2027</h1>
<p class="lead">מכניסים כמה מבוגרים וילדים, בוחרים שיעור רביעית ומספר כזיתים, ומקבלים כמה מצות שמורות, חבילות מצה, בקבוקי יין ומיץ ענבים לקנות. {SEDER_TXT}.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
<div class="split">
<form class="tool-panel" id="seder-form" onsubmit="return false" novalidate>
<div class="fields cols-2">
<div class="field"><label for="adults">מבוגרים</label><input id="adults" name="adults" type="number" inputmode="numeric" min="0" step="1" value="10"></div>
<div class="field"><label for="kids">ילדים</label><input id="kids" name="kids" type="number" inputmode="numeric" min="0" step="1" value="4"></div>
</div>
<div class="field"><span class="label" id="sd-l">כמה סדרים</span><div class="choices" role="radiogroup" aria-labelledby="sd-l">
<label><input type="radio" name="seders" value="1" checked> סדר אחד (בארץ)</label><label><input type="radio" name="seders" value="2"> שני סדרים (בחו״ל)</label></div></div>
<div class="field"><span class="label" id="rv-l">שיעור רביעית לכוס</span><div class="choices" role="radiogroup" aria-labelledby="rv-l">
<label><input type="radio" name="reviit" value="86" checked> 86 מ״ל (הגר״ח נאה)</label><label><input type="radio" name="reviit" value="150"> 150 מ״ל (החזון איש)</label></div></div>
<div class="field"><span class="label" id="kz-l">כזיתים מצה לכל מבוגר</span><div class="choices" role="radiogroup" aria-labelledby="kz-l">
<label><input type="radio" name="kz" value="3" checked> 3 (מוציא, כורך, אפיקומן)</label><label><input type="radio" name="kz" value="5"> 5 (יש המהדרים)</label></div></div>
<details class="mt-1"><summary>הגדרות נוספות</summary>
<div class="fields cols-2 mt-1">
<div class="field"><label for="wine">אחוז המבוגרים ששותים יין</label><input id="wine" name="wine" type="number" inputmode="numeric" min="0" max="100" step="5" value="70"></div>
<div class="field"><label for="kzm">כזיתים במצת יד אחת</label><input id="kzm" name="kzm" type="number" inputmode="decimal" min="1" max="6" step="0.5" value="2"></div>
<div class="field"><label for="days">ימים עם מצת מכונה</label><input id="days" name="days" type="number" inputmode="numeric" min="0" max="8" step="1" value="7"></div>
<div class="field"><label for="mpd">מצות מכונה לאדם ליום</label><input id="mpd" name="mpd" type="number" inputmode="decimal" min="0" max="10" step="0.5" value="2"></div>
<div class="field"><label for="box">מצות בחבילת 1 ק״ג</label><input id="box" name="box" type="number" inputmode="numeric" min="1" max="80" step="1" value="30"></div>
</div></details>
</form>
<div aria-live="polite">
<div id="empty" class="result" hidden><div class="label">התוצאה תופיע כאן</div><p class="mb-0">הכניסו מספר סועדים.</p></div>
<div id="out" class="result">
<div class="hk-tiles">
<div class="hk-tile"><div class="k">מצות יד שמורות</div><div class="v" id="k-hand"></div></div>
<div class="hk-tile"><div class="k">בקבוקי יין</div><div class="v" id="k-wine"></div><div class="s">750 מ״ל</div></div>
<div class="hk-tile"><div class="k">מיץ ענבים</div><div class="v" id="k-juice"></div><div class="s">ליטר</div></div>
<div class="hk-tile"><div class="k">חבילות מצה</div><div class="v" id="k-box"></div><div class="s">לכל החג</div></div>
</div>
<div class="card mt-2"><h2 class="h3">רשימת קניות לסדר</h2><table class="hk-ing"><tbody id="list"></tbody></table>
<p class="hk-note mt-1 mb-0">כולל 10% רזרבה למצות השמורות, ליין ולמיץ, וכוס של אליהו בכל סדר.</p></div>
</div>
<div data-share data-share-scope="#seder-form" data-share-result="#k-hand,#k-wine" data-share-msg="לליל הסדר שלנו צריך {{result}} מצות שמורות ו-{{result2}} בקבוקי יין. חשבו לסדר שלכם במחשבון החינמי של תכנון פלוס:"></div>
</div></div>
<script src="{{up}}assets/share.js"></script>
{cta("כל הסדר בקובץ אחד", "«מתכנן ליל הסדר 2027»: אורחים, תפריט, 27 מצרכים לפי מספר הסועדים, רשימת קניות עם עלות, תפקידים בהגדה ולוח הכנות. ₪19.", S_PROD, "למתכנן ליל הסדר")}
</div></section>
<section class="section alt"><div class="container narrow prose">
<h2>לפי מה המחשבון מחשב?</h2>
<ul><li><strong>מצה שמורה:</strong> (מבוגרים × כזיתים + ילדים × חצי מזה) ÷ כזיתים במצה × מספר סדרים, ועוד 10%.</li>
<li><strong>יין:</strong> 4 כוסות × רביעית לכל מבוגר ששותה יין, ועוד כוס של אליהו לכל סדר ו-10%, מחולק לבקבוקי 750 מ״ל.</li>
<li><strong>מיץ ענבים:</strong> 4 כוסות × רביעית לכל ילד ולכל מבוגר שלא שותה יין.</li>
<li><strong>מצת מכונה:</strong> סועדים × מצות ליום × ימים, מחולק למספר המצות בחבילה.</li></ul>
<p>מקורות לשיעורים: שולחן ערוך, אורח חיים, סימנים תע״ב (ארבע כוסות), תע״ה ותע״ז (מצה). לשיעורי רביעית לפי השיטות: <a href="{SRC_SHIUR}" rel="noopener" target="_blank">ישיבת הר עציון, «שיעור כביצה וכזית בימינו»</a>. המחשבון הוא כלי תכנון ולא פסק הלכה.</p>
<h2>שאלות נפוצות</h2>{faq_html(faq)}
<p class="mt-3"><a href="{{up}}{S_G1}">איך מארגנים ליל סדר</a> · <a href="{{up}}{PES}">פסח 2027</a> · <a href="{{up}}{EN_SCALC}" hreflang="en" lang="en">Seder shopping calculator (English)</a></p>
</div></section>
{CALC_JS}
"""
    t = "כמה מצות ויין צריך לליל הסדר? מחשבון לפסח 2027 | תכנון פלוס"
    d = "מחשבון חינמי לפסח 2027: כמה מצות שמורות, חבילות מצה, בקבוקי יין ומיץ ענבים צריך לפי מספר האורחים, שיעור הרביעית ומספר הכזיתים. עם מקורות."
    page(S_TOOL, t, d, body, [app_ld("מחשבון מצות ויין לליל הסדר", d, S_TOOL), faq_ld(faq)],
         og_image=SIMG + "shopping.webp", crumbs=[("פסח 2027", PES), ("מחשבון מצות ויין", S_TOOL)], alt=EN_SCALC)


# ------------------------------------------------------------------ cleaning checklist (free lead magnet)
def cleaning():
    rooms = "".join(f"<h3>{r}</h3><ul class='s27-check'>" + "".join(f"<li>{t}</li>" for t in ts) + "</ul>" for r, ts in ROOMS)
    tl = "".join(f"<tr><th scope='row'>{a}</th><td>{b}</td></tr>" for a, b in CLEAN_TL)
    faq = [("מאיפה מתחילים לנקות לפסח?", "מהחדרים שאין בהם אוכל (חדרי שינה, ארונות, סלון), ומשאירים את המטבח לימים האחרונים. כך החמץ נשאר במקום אחד והבית «סגור» בהדרגה."),
           ("צריך לנקות את כל הבית?", "ההלכה דורשת לבדוק ולנקות מחמץ מקומות שאולי הוכנס אליהם חמץ. מקום שלא מכניסים אליו חמץ לא צריך בדיקה (שולחן ערוך, אורח חיים, סימן תל״ג, סעיף ג). ניקיון אביב הוא בחירה, לא חובה."),
           ("מתי בודקים חמץ ב-2027?", f"ב{hd(BEDIKA)} בערב, אחרי צאת הכוכבים. למחרת בבוקר ({hd(EREV)}) מסיימים לאכול חמץ ושורפים אותו עד השעה שמתפרסמת בעירכם."),
           ("הצ׳קליסט באמת חינם?", "כן. PDF להורדה בלי מייל ובלי הרשמה, להדפסה ולשימוש אישי.")]
    body = f"""
<p><strong>בקצרה:</strong> רשימת ניקיון לפסח מחולקת ל-{len(ROOMS)} אזורים בבית, עם לוח זמנים לאחור מליל הסדר ({hd(SEDER, evening=True)}). אפשר להוריד כ-PDF להדפסה ולתלות על המקרר.</p>
{clean_box()}
<h2>העיקרון: חמץ, לא אבק</h2>
<p>ניקיון לפסח נועד להוציא חמץ מהמקומות שאולי נכנס אליהם חמץ. «כל מקום שאין מכניסין בו חמץ אין צריך בדיקה» (שולחן ערוך, אורח חיים, סימן תל״ג, סעיף ג). לכן מתחילים מהמקומות שבאמת אוכלים בהם, ולא מהחלונות. שאלות של כשרות כלים ומנהגים: פנו לרב.</p>
<h2>הרשימה חדר אחר חדר</h2>
{rooms}
<h2>לוח זמנים</h2>
<div class="table-wrap"><table class="s27-table"><tr><th>מתי</th><th>מה עושים</th></tr>{tl}</table></div>
<p class="small muted">שעות סוף אכילת חמץ ושריפתו משתנות בין ערים. בדקו בלוח הזמנים המקומי.</p>
{cta("אחרי הניקיון: ליל הסדר", "«מתכנן ליל הסדר 2027» מחשב מצות, יין ומצרכים לפי מספר האורחים, בונה רשימת קניות ומחלק את ההגדה. ₪19.", S_PROD, "למתכנן ליל הסדר")}"""
    guide(CLEAN, "ניקיון לפסח 2027 – צ׳קליסט חדר אחר חדר להדפסה (PDF חינם) | תכנון פלוס",
          "רשימת ניקיון לפסח 2027 חדר אחר חדר: מטבח, סלון, חדרי ילדים, ארונות ורכב, עם לוח זמנים עד ליל הסדר. PDF חינם להדפסה, בלי הרשמה.",
          "ניקיון לפסח 2027: צ׳קליסט חדר אחר חדר", body, faq, [("פסח 2027", PES), ("צ׳קליסט ניקיון לפסח", CLEAN)],
          img="pesach/img/checklist-1.webp", minutes=5)


# ------------------------------------------------------------------ hub
def hub():
    body = f"""
<section class="hero"><div class="container">{{CRUMBS}}
<h1>פסח 2027: ניקיון, ליל הסדר, תאריכים ותקציב</h1>
<p class="lead">{SEDER_TXT}, ושביעי של פסח ב{hd(SHVII)}. כאן תמצאו צ׳קליסט ניקיון חינמי, מחשבון מצות ויין, מתכנן ליל סדר ומדריכים.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
{clean_box()}
<div class="grid cols-2 mt-3">
<article class="card pad-lg"><h2 class="h3"><a href="{{up}}{S_PROD}">מתכנן ליל הסדר באקסל</a></h2>
<img src="{{up}}{SIMG}dashboard.webp" alt="דשבורד מתכנן ליל הסדר" width="1228" height="560" loading="lazy" style="width:100%;height:auto;border:1px solid var(--border);border-radius:8px">
<p>אורחים, תפריט, כמויות לפי מספר הסועדים, רשימת קניות, תפקידים בהגדה ולוח הכנות.</p><p><strong>₪19</strong></p><a class="btn" href="{{up}}{S_PROD}">לפרטים</a></article>
<article class="card pad-lg"><h2 class="h3"><a href="{{up}}{S_TOOL}">מחשבון מצות ויין</a></h2>
<p>כמה מצות שמורות, חבילות מצה, בקבוקי יין ומיץ ענבים, לפי מספר האורחים ושיעור הרביעית שלכם. חינם.</p><a class="btn secondary" href="{{up}}{S_TOOL}">למחשבון</a></article>
</div>
<article class="card pad-lg mt-3" id="{BUNDLE}"><div class="split"><div><h2 class="h3">פורים + פסח יחד</h2>
<p>מתכנן ליל הסדר + <a href="{{up}}{P_PROD}">מתכנן משלוחי המנות</a>. ₪29 במקום ₪38.</p><span class="badge success">חוסכים ₪9</span></div>
<div class="buy" data-product="{BUNDLE}" data-compact="1"></div></div></article>
</div></section>
<section class="section alt"><div class="container narrow">
<h2>תאריכי פסח 2027</h2>{dates_table()}
<p class="hk-note mt-1">התאריכים חושבו לפי הלוח העברי. זמני הדלקת נרות, סוף אכילת חמץ ושריפתו משתנים לפי העיר.</p>
<h2 class="mt-4">מדריכים</h2>
{links([("ניקיון לפסח: צ׳קליסט חדר אחר חדר", CLEAN), ("איך מארגנים ליל סדר: לוח זמנים, כמויות ותפקידים", S_G1),
        ("פסח 2027: כל התאריכים", S_G2), ("תקציב לפסח: איך מתכננים את ההוצאות של החג", S_G3), ("פורים 2027", PUR)])}
<h2 class="mt-4">In English</h2>
{links([("How to host a Passover seder", EN_HOST), ("Passover seder checklist", EN_CHECK), ("Seder shopping calculator", EN_SCALC), ("Passover Seder Planner", EN_SEDER)])}
</div></section>"""
    t = "פסח 2027 – ניקיון, ליל הסדר, תאריכים ומחשבון מצות | תכנון פלוס"
    d = f"פסח 2027: ליל הסדר ב-{short(EREV)} בערב. צ׳קליסט ניקיון לפסח חינם להדפסה, מחשבון מצות ויין, מתכנן ליל סדר באקסל, תאריכים ומדריכים."
    page(PES, t, d, body, [collection_ld(t, d, PES)], og_image="pesach/img/checklist-1.webp", crumbs=[("פסח 2027", PES)], buy=True)


# ------------------------------------------------------------------ guides
def g_seder():
    steps = ["שישה שבועות לפני: מחליטים מי מארח ומזמינים", "חודש לפני: תפריט ומי מביא מה", "שלושה שבועות לפני: הגדות ותפקידים",
             "שבועיים לפני: קנייה גדולה של יבשים ויין", "שבוע לפני: מאשרים מספר סועדים ומוכרים חמץ", "יומיים לפני: טריים, בישול וחרוסת",
             "ערב החג: עורכים שולחן וקערות"]
    faq = [("כמה זמן נמשך ליל הסדר?", "תלוי במשפחה. סדר עם ילדים צעירים נמשך לרוב 3–4 שעות כולל הסעודה. חלוקת תפקידים מראש מקצרת את ההמתנה ומשאירה את הילדים מעורבים."),
           ("כמה אוכל להכין לליל הסדר?", "האורחים כבר אכלו מצה, מרור וחרוסת לפני הסעודה, אז מנות קטנות מספיקות. כלל אצבע: כ-300 גרם בשר (לפני בישול) למבוגר אם יש עיקרית אחת, ופחות אם יש שתיים."),
           ("איך שומרים על הילדים ערניים?", "נותנים לכל ילד תפקיד (מה נשתנה, ארבעה בנים, עשר המכות עם אביזרים), שואלים שאלות לאורך המגיד, ומבטיחים פרס על האפיקומן.")]
    body = f"""
<p><strong>בקצרה:</strong> {SEDER_TXT}. ליל סדר רגוע מתחיל שישה שבועות קודם: רשימת אורחים, תפריט, כמויות, תפקידים בהגדה, ואז קניות ובישול לפי לוח זמנים.</p>
<h2>לוח זמנים לאחור מליל הסדר</h2>
<ol>{"".join(f"<li>{s}</li>" for s in steps)}</ol>
<h2>כמה מצות ויין?</h2>
<p>כל אחת מארבע הכוסות צריכה רביעית: כ-86 מ״ל לשיטת הגר״ח נאה או כ-150 מ״ל לשיטת החזון איש (שולחן ערוך, אורח חיים תע״ב, ט). מבוגר ששותה יין צריך כחצי בקבוק עד כמעט בקבוק שלם. מצה שמורה: לפחות שלושה כזיתים למבוגר. החישוב המדויק לפי מספר האורחים: <a href="{{up}}{S_TOOL}">מחשבון מצות ויין</a>.</p>
<h2>קערת הסדר</h2>
<ul><li><strong>זרוע:</strong> כנף או צוואר עוף צלויים.</li><li><strong>ביצה:</strong> ביצה קשה (צלויה קלות לפי חלק מהמנהגים).</li>
<li><strong>מרור וחזרת:</strong> חסה, ולפי המנהג גם חזרת.</li><li><strong>חרוסת:</strong> תפוחים, תמרים או סילאן, אגוזים ויין.</li><li><strong>כרפס:</strong> סלרי, פטרוזיליה או תפוח אדמה, עם מי מלח.</li></ul>
<p>סדר הפריטים על הקערה משתנה בין מנהגים. בשולחן גדול כדאי קערה לכל 8–10 סועדים.</p>
<h2>תפקידים בהגדה</h2>
<p>חלקו מראש: מי עושה קידוש, מי שואל «מה נשתנה», ארבעה בנים לארבעה ילדים, מי מוביל את «דיינו» ומי מחביא את האפיקומן. שולחן שבו כל אחד יודע מתי תורו זורם יותר.</p>
<h2>טעויות נפוצות</h2>
<ul><li>מבשלים יותר מדי. אחרי ארבע כוסות ומצה, רוב האורחים אוכלים פחות ממה שנדמה.</li>
<li>מגלים בערב החג שחסרות הגדות או כוסות.</li><li>לא שואלים מראש על רגישויות (אגוזים בחרוסת, צמחונים).</li></ul>
{cta("הכול מוכן בקובץ אחד", "אורחים, תפריט, 27 מצרכים מחושבים, רשימת קניות, תפקידים בהגדה ולוח ההכנות הזה עם תאריכים. ₪19.", S_PROD, "למתכנן ליל הסדר")}"""
    guide(S_G1, "איך מארגנים ליל סדר 2027 – לוח זמנים, כמויות ותפקידים בהגדה | תכנון פלוס",
          "מדריך לאירוח ליל הסדר 2027: לוח הכנות מ-6 שבועות לפני, כמה מצות ויין צריך לפי השיעורים, קערת הסדר, חלוקת תפקידים בהגדה וטעויות נפוצות.",
          "איך מארגנים ליל סדר: לוח זמנים, כמויות ותפקידים", body, faq, [("פסח 2027", PES), ("איך מארגנים ליל סדר", S_G1)],
          alt=EN_HOST, img=SIMG + "dashboard.webp", minutes=5)
    # HowTo markup lives on the same page via an extra JSON-LD script
    p = sc.DOCS / S_G1 / "index.html"
    s = p.read_text(encoding="utf-8")
    s = s.replace("</head>", f'<script type="application/ld+json">\n{json.dumps(howto_ld("איך מארגנים ליל סדר", steps, S_G1), ensure_ascii=False)}\n</script>\n</head>', 1)
    p.write_text(s, encoding="utf-8")


def g_dates():
    faq = [("מתי פסח 2027?", f"ליל הסדר ב{hd(SEDER, evening=True)}. היום הראשון של החג: {hd(SEDER)}. שביעי של פסח: {hd(SHVII)}."),
           ("מתי בודקים חמץ ב-2027?", f"ב{hd(BEDIKA)} בערב, אחרי צאת הכוכבים."),
           ("כמה ימים פסח בארץ ובחו״ל?", "בארץ שבעה ימים: יום טוב ראשון, חמישה ימי חול המועד ושביעי של פסח. בחו״ל שמונה ימים, עם שני ימים טובים בהתחלה ושניים בסוף."),
           ("מתי פורים 2027?", f"{hd(D['purim'])}. בירושלים: {hd(D['shushan_purim'])}.")]
    body = f"""
<p><strong>בקצרה:</strong> {SEDER_TXT}. פסח נמשך בארץ עד {hd(SHVII)} (שביעי של פסח), ובחו״ל עד {hd(CHUL)}.</p>
{dates_table()}
<h2>הימים שלפני</h2>
<p>בדיקת חמץ: {hd(BEDIKA)} בערב. ערב פסח: {hd(EREV)}. בבוקר מסיימים לאכול חמץ, שורפים אותו ומבטלים. מכירת חמץ נעשית בימים שלפני, דרך רב או בטופס מקוון של הרבנות. השעות המדויקות משתנות בין ערים.</p>
<h2>חופשת פסח</h2>
<p>תאריכי החופשה בבתי הספר ובגנים מתפרסמים בלוח החופשות של משרד החינוך לשנת הלימודים תשפ״ז. בדקו שם לפני שמזמינים חופשה.</p>
<h2>איך חישבנו</h2>
<p>התאריכים חושבו לפי האלגוריתם של הלוח העברי (Dershowitz & Reingold, Calendrical Calculations), ונבדקו מול תאריכים ידועים: ראש השנה תשפ״ז = 12.9.2026, פסח תשפ״ו = 2.4.2026.</p>
<p>{" · ".join(f'<a href="{{up}}{h}">{t}</a>' for t, h in [("צ׳קליסט ניקיון לפסח", CLEAN), ("מחשבון מצות ויין", S_TOOL), ("איך מארגנים ליל סדר", S_G1)])}</p>"""
    guide(S_G2, f"פסח 2027 מתי? ליל הסדר {short(EREV)}, שביעי של פסח ובדיקת חמץ | תכנון פלוס",
          f"כל תאריכי פסח 2027: בדיקת חמץ {short(BEDIKA)} בערב, ליל הסדר {short(EREV)}, חול המועד ושביעי של פסח {short(SHVII)}. בארץ ובחו״ל, עם תאריך עברי.",
          "פסח 2027: כל התאריכים", body, faq, [("פסח 2027", PES), ("תאריכי פסח 2027", S_G2)], minutes=2)


def g_budget():
    cats = [("מצות, יין וקערת הסדר", "לפי מספר הסועדים. מצה שמורה יקרה בהרבה ממצת מכונה, לכן כדאי לחשב בדיוק."),
            ("הסעודה", "בשר, דגים, ירקות וקינוח. בדרך כלל הסעיף הגדול ביותר אם מארחים."),
            ("מוצרי פסח לכל השבוע", "לא רק הסדר: מצות, ממרחים, קמח תפו״א ומוצרים כשרים לפסח לשבוע שלם."),
            ("ניקיון והכשרה", "חומרי ניקוי, נייר כסף, כיסויים, ואולי ניקוי תנור או שטיחים."),
            ("כלים", "כלי פסח חדשים או חד פעמיים."),
            ("ביגוד ומתנות", "בגדי חג לילדים, מתנות למארחים, «אפיקומן»."),
            ("חול המועד", "טיולים, אטרקציות, אוכל בחוץ. כדאי לקבוע תקציב לכל יום.")]
    faq = [("כמה עולה פסח למשפחה?", "אין מספר אחד. זה תלוי בעיקר אם מארחים את הסדר, בכמה סועדים ובתוכניות לחול המועד. במקום ממוצע, עדיף לחשב את המשפחה שלכם לפי הקטגוריות שבמדריך."),
           ("איך חוסכים בקניות לפסח?", "קונים לפי רשימה מחושבת (לא «ליתר ביטחון»), משווים מחירי מצות ויין בין רשתות, מחלקים מנות בין המשפחה, ומתכננים את חול המועד מראש עם תקציב יומי.")]
    body = f"""
<p><strong>בקצרה:</strong> פסח הוא אחד החודשים היקרים בשנה למשפחות בישראל: אירוח, מוצרים מיוחדים לשבוע שלם, ניקיון וחופשה. השנה {SEDER_TXT}. כדאי להפריש כבר מינואר ולחלק את ההוצאה לקטגוריות.</p>
<h2>שבע הקטגוריות של תקציב פסח</h2>
<div class="table-wrap"><table class="s27-table"><tr><th>קטגוריה</th><th>מה לכלול</th></tr>{"".join(f"<tr><th scope='row'>{a}</th><td>{b}</td></tr>" for a, b in cats)}</table></div>
<h2>איך מחשבים</h2>
<ol><li>מתחילים מהסדר: <a href="{{up}}{S_TOOL}">מחשבון המצות והיין</a> נותן כמויות, ו<a href="{{up}}{S_PROD}">מתכנן ליל הסדר</a> מכפיל במחירים ומראה עלות לסועד.</li>
<li>מוסיפים את שאר השבוע: כמה ארוחות בבית, כמה בחוץ.</li><li>חול המועד: תקציב יומי × מספר ימי הטיול.</li>
<li>מחלקים את הסכום ב-3 ומפרישים מינואר עד מרץ. כך פסח לא נופל על חודש אחד.</li></ol>
<h2>טיפים לחיסכון</h2>
<ul><li>מוצרים «כשר לפסח» יקרים יותר. קנו רק מה שבאמת צריך לשבוע.</li><li>מארחים? בקשו מכל משפחה להביא מנה אחת.</li>
<li>הזמינו מצות שמורות מוקדם: לפעמים יש הנחה, ותמיד יש זמינות.</li><li>אטרקציות בחול המועד: בדקו הטבות של מועדוני אשראי וכרטיסי עובדים.</li></ul>
{cta("לשלב את פסח בתקציב השנתי", "«תקציב משק בית Pro 2027» כולל קטגוריית חגים ויעדי חיסכון חודשיים, כך שפסח לא מפתיע. ₪39.", HB, "לקובץ התקציב 2027")}
<p class="small muted mt-3">מידע כללי לתכנון אישי, לא ייעוץ פיננסי.</p>"""
    guide(S_G3, "תקציב לפסח 2027 – כמה עולה החג ואיך מתכננים | תכנון פלוס",
          "איך מתכננים תקציב לפסח 2027: שבע קטגוריות ההוצאה (סדר, מצות, מוצרי פסח, ניקיון, חול המועד), איך מחשבים את המשפחה שלכם, וטיפים לחיסכון.",
          "תקציב לפסח 2027: איך מתכננים את ההוצאות של החג", body, faq, [("פסח 2027", PES), ("תקציב לפסח", S_G3)], minutes=4)


if __name__ == "__main__":
    product()
    calculator()
    cleaning()
    hub()
    g_seder()
    g_dates()
    g_budget()
    print("pesach pages written")
