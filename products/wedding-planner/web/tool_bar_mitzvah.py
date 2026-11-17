from common import BASE, UPDATED, UPDATED_HE, breadcrumb_ld, breadcrumbs, faq_html, faq_ld, page

PATH = "tools/bar-mitzvah-cost"
TITLE = "כמה עולה בר מצווה 2026? מחשבון עלות בר / בת מצווה | Glory"
DESC = ("מחשבון חינם לעלות בר או בת מצווה: אולם או צהריים או קידוש, מספר אורחים, צלם, DJ, תפילין ועוד. "
        "רואים סכום כולל, עלות לאורח וכמה יישאר מהכיס אחרי המתנות.")

LINES = [  # id, label, default, checked
    ("photo", "צילום סטילס", 3500, True), ("video", "וידאו / מגנטים משולב", 3000, False),
    ("dj", "DJ / הגברה / הפעלה", 4000, True), ("decor", "עיצוב ופרחים", 3000, True),
    ("invite", "הזמנות ואישורי הגעה", 600, True), ("clothes", "בגדים לכל המשפחה", 2500, True),
    ("tefillin", "תפילין וטלית", 3000, True), ("teacher", "מורה / הכנה לעלייה לתורה או לדרשה", 2000, True),
    ("kiddush", "קידוש בבית הכנסת", 1500, False), ("magnets", "עמדת מגנטים / אטרקציה", 2500, False),
]

FAQS = [
    ("כמה עולה בר מצווה בממוצע?",
     "אין נתון רשמי. בכתבות צרכנות מופיעים סכומים של עד כ-18,000 ₪ לאירוע צנוע בבית הכנסת, והטווח עצום: קידוש ומסיבה קטנה יכולים לעלות כמה אלפי שקלים, ואירוע ערב באולם ל-150 אורחים עולה בקלות 50,000–70,000 ₪. המחשבון נותן הערכה לפי הבחירות שלכם."),
    ("כמה עולה מנה באירוע בר מצווה?",
     "המחשבון מציע כברירת מחדל כ-280 ₪ למנה באירוע ערב, כ-190 ₪ בצהריים או במסעדה וכ-75 ₪ לאורח בקידוש. אלה הערכות כלליות שלנו – הזינו את המחיר מהצעת המחיר שקיבלתם."),
    ("כמה לשים בבר מצווה?",
     "אין מספר רשמי. נפוץ לתת סכום בכפולות של 18. לפי הערכה שלנו: חברים של חתן/כלת השמחה כ-100–180 ₪, משפחה של מכרים כ-250–400 ₪, ומשפחה קרובה 500 ₪ ומעלה. באירוע צנוע (קידוש) – פחות."),
    ("האם המתנות מכסות את בר המצווה?",
     "לפעמים חלקית. המחשבון מחשב את המתנות הצפויות לפי ממוצע לאורח (אפשר לשנות) ומראה כמה צפוי לצאת מהכיס. ילדים נותנים בדרך כלל פחות ממבוגרים."),
    ("מתי כדאי להתחיל לתכנן?",
     "כ-8 עד 12 חודשים מראש: אולמות, צלמים ומורים לבר מצווה נתפסים מוקדם, ותפילין בהזמנה אישית לוקחות זמן. ראו את <a href=\"../../p/bar-mitzvah-planner/guides/bar-mitzvah-timeline/\">לוח הזמנים המלא</a>."),
    ("האם הנתונים נשמרים?",
     "לא. הכל מחושב בדפדפן שלכם בלבד."),
]


def build():
    bc = breadcrumbs([("דף הבית", "../../"), ("מחשבונים", "../"), ("עלות בר / בת מצווה", None)])
    rows = []
    for lid, label, dflt, chk in LINES:
        extra = ' id="row-tefillin"' if lid == "tefillin" else ""
        rows.append(f"""<div class="line"{extra} data-label="{label}">
     <label class="lchk"><input type="checkbox" name="use_{lid}"{" checked" if chk else ""}> {label}</label>
     <div class="input-affix"><input type="number" name="amt_{lid}" value="{dflt}" min="0" step="100" inputmode="numeric" aria-label="סכום עבור {label}"><span class="affix">₪</span></div>
    </div>""")
    lines_html = "\n    ".join(rows)
    body = f"""
<style>
.line{{display:grid;grid-template-columns:1fr 9.5rem;gap:.6rem;align-items:center;padding:.35rem 0;border-bottom:1px dashed var(--border)}}
.line .lchk{{display:flex;gap:.5rem;align-items:center;font-weight:600}}
.line input[type=number]{{min-height:42px;padding-block:.4rem}}
.line input:disabled{{opacity:.45}}
#r-lines{{list-style:none;padding:0;margin:.75rem 0 0;display:grid;gap:.35rem;font-size:.95rem}}
#r-lines li{{display:grid;grid-template-columns:minmax(7rem,1.3fr) 1fr auto;gap:.6rem;align-items:center}}
#r-lines .lb{{height:10px;background:var(--surface-2);border-radius:99px;overflow:hidden}}
#r-lines .lb span{{display:block;height:100%;background:var(--primary);border-radius:99px}}
@media (max-width:480px){{.line{{grid-template-columns:1fr 7.5rem}} #r-lines li{{grid-template-columns:1fr auto}} #r-lines .lb{{display:none}}}}
</style>
<section class="hero">
 <div class="container narrow">
  {bc}
  <span class="eyebrow">מחשבון חינם · עודכן {UPDATED_HE}</span>
  <h1>כמה עולה בר מצווה? <span class="hl">מחשבון עלות לבר ובת מצווה</span></h1>
  <p class="lead">בוחרים סוג אירוע ומספר אורחים, מסמנים מה צריך – ורואים עלות כוללת, עלות לאורח וכמה צפוי לצאת מהכיס אחרי המתנות.
  כל הסכומים ניתנים לעריכה, כך שאפשר להזין את הצעות המחיר שקיבלתם.</p>
 </div>
</section>

<section class="section" style="padding-top:0">
 <div class="container narrow">
  <form id="bm-form" class="tool-panel" novalidate>
   <div class="fields cols-2">
    <div class="field">
     <span class="label" id="l-who">למי האירוע?</span>
     <div class="choices" role="radiogroup" aria-labelledby="l-who">
      <label><input type="radio" name="who" value="bar" checked> בר מצווה</label>
      <label><input type="radio" name="who" value="bat"> בת מצווה</label>
     </div>
    </div>
    <div class="field">
     <span class="label" id="l-type">סוג האירוע</span>
     <div class="choices" role="radiogroup" aria-labelledby="l-type">
      <label><input type="radio" name="type" value="evening" checked> ערב באולם</label>
      <label><input type="radio" name="type" value="lunch"> צהריים / מסעדה</label>
      <label><input type="radio" name="type" value="kiddush"> קידוש ומסיבה</label>
     </div>
    </div>
   </div>
   <div class="fields cols-3">
    <div class="field"><label for="adults">מבוגרים</label><input type="number" id="adults" name="adults" value="120" min="0" inputmode="numeric"></div>
    <div class="field"><label for="kids">ילדים ונוער</label><input type="number" id="kids" name="kids" value="30" min="0" inputmode="numeric"><span class="hint">ילד ≈ 60% ממנה</span></div>
    <div class="field"><label for="plate">מחיר מנה / לאורח</label><div class="input-affix"><input type="number" id="plate" name="plate" value="280" min="0" inputmode="numeric"><span class="affix">₪</span></div></div>
   </div>
   <h2 style="font-size:1.1rem" class="mt-1">מה עוד בתקציב?</h2>
   <div>
    {lines_html}
   </div>
   <div class="fields cols-3 mt-2">
    <div class="field"><label for="reserve">רזרבה (%)</label><input type="number" id="reserve" name="reserve" value="7" min="0" max="30" inputmode="numeric"></div>
    <div class="field"><label for="giftAdult">מתנה ממוצעת למבוגר</label><div class="input-affix"><input type="number" id="giftAdult" name="giftAdult" value="180" min="0" inputmode="numeric"><span class="affix">₪</span></div></div>
    <div class="field"><label for="giftKid">מתנה ממוצעת לילד/ה</label><div class="input-affix"><input type="number" id="giftKid" name="giftKid" value="100" min="0" inputmode="numeric"><span class="affix">₪</span></div></div>
   </div>
   <div class="result" aria-live="polite">
    <div class="label">עלות משוערת כוללת</div>
    <div class="big" id="r-total">₪0</div>
    <div class="kpis mt-1">
     <div class="kpi"><div class="k">לאורח</div><div class="v" id="r-per"></div></div>
     <div class="kpi"><div class="k">מתנות צפויות</div><div class="v" id="r-gifts"></div></div>
     <div class="kpi" style="grid-column:span 2"><div class="k" id="r-net-label">מהכיס אחרי מתנות</div><div class="v" id="r-net"></div></div>
    </div>
    <ul id="r-lines"></ul>
   </div>
   <noscript><p class="noscript">המחשבון צריך JavaScript.</p></noscript>
  </form>

  <div class="cta-box mt-3">
   <div>
    <h2 style="font-size:1.2rem">רוצים לנהל את כל זה בקובץ אחד?</h2>
    <p>מתכנן בר/בת המצווה של Glory: תקציב מול הצעות מחיר, מוזמנים ואישורי הגעה, מתנות ותודות, תשלומים וצ'קליסט עם עלייה לתורה. ₪39.</p>
   </div>
   <a class="btn accent" href="../../p/bar-mitzvah-planner/">למתכנן בר/בת המצווה</a>
  </div>
 </div>
</section>

<section class="section alt">
 <div class="container narrow prose">
  <h2>ממה מורכבת עלות בר מצווה?</h2>
  <p>ברוב האירועים <strong>המקום והאוכל</strong> הם יותר ממחצית העלות, ולכן שתי ההחלטות הגדולות הן סוג האירוע ומספר המוזמנים.
  אחריהם באים צילום, מוזיקה ועיצוב, ובבר מצווה גם תפילין וטלית – שעלותן תלויה מאוד ברמת ההידור.</p>
  <h2>שלושה סוגי אירועים, שלושה תקציבים</h2>
  <div class="table-wrap"><table>
   <thead><tr><th>סוג אירוע</th><th>ברירת מחדל במחשבון</th><th>מתאים ל…</th></tr></thead>
   <tbody>
    <tr><td>ערב באולם</td><td>כ-280 ₪ למנה</td><td>אירוע גדול עם DJ, רחבה ומשפחה מורחבת</td></tr>
    <tr><td>צהריים / מסעדה</td><td>כ-190 ₪ למנה</td><td>אירוע משפחתי מכובד בתקציב בינוני</td></tr>
    <tr><td>קידוש ומסיבה</td><td>כ-75 ₪ לאורח</td><td>עלייה לתורה וקידוש, ומסיבה קטנה לחברים</td></tr>
   </tbody></table></div>
  <p class="small muted">ברירות המחדל הן הערכות כלליות שלנו נכון ל{UPDATED_HE}, לא מחירון רשמי. המחירים משתנים מאוד לפי אזור, יום ועונה – תמיד בקשו 2–3 הצעות מחיר.</p>
  <h2>מקורות</h2>
  <ul class="source">
   <li>סכומים של עד כ-18,000 ₪ לאירוע צנוע וטווחי מחירים לצלמים (מכ-1,500 ₪ לחבילה בסיסית ועד 10,000 ₪ ומעלה): <a href="https://www.ice.co.il/consumerism/news/article/837555" target="_blank" rel="noopener">ice – כסף וצרכנות</a>,
   <a href="https://www.karamel.co.il/כך_תתכננו_נכון_את_בר_בת_המצווה.asp" target="_blank" rel="noopener">קרמל</a>,
   <a href="https://financa.co.il/איך-לתכנן-תקציב-לבת-מצווה-בתל-אביב-בלי-ה/" target="_blank" rel="noopener">פיננקה</a> (כפי שסוכם בסקר השוק שלנו, נבדק {UPDATED_HE}).</li>
   <li>מנהג הכפולות של 18 במתנות: מקובל במסורת היהודית ("חי").</li>
   <li>שאר ברירות המחדל: הערכת Glory, {UPDATED_HE}. ניתן לעריכה.</li>
  </ul>
 </div>
</section>

<section class="section">
 <div class="container narrow">
  <h2>שאלות נפוצות</h2>
  {faq_html(FAQS)}
  <p class="mt-3">עוד: <a href="../../p/bar-mitzvah-planner/guides/bar-mitzvah-cost-2026/">כמה עולה בר מצווה – מדריך מלא</a> ·
  <a href="../../p/bar-mitzvah-planner/guides/bar-mitzvah-timeline/">לוח זמנים להכנה</a> ·
  <a href="../wedding-gift/">כמה לשים בחתונה</a></p>
 </div>
</section>
"""
    ld = [
        {"@type": "WebApplication", "name": "מחשבון עלות בר / בת מצווה", "url": BASE + PATH + "/",
         "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "inLanguage": "he-IL",
         "isAccessibleForFree": True, "dateModified": UPDATED, "description": DESC,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ILS"}},
        breadcrumb_ld([("דף הבית", ""), ("מחשבונים", "tools/"), ("עלות בר / בת מצווה", PATH + "/")]),
        faq_ld(FAQS),
    ]
    return page(PATH, TITLE, DESC, body, ld, og_image=BASE + "p/bar-mitzvah-planner/img/screen-1.png",
                scripts='<script src="calc.js" defer></script>\n')
