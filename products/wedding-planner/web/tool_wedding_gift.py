from common import BASE, UPDATED, UPDATED_HE, breadcrumb_ld, breadcrumbs, faq_html, faq_ld, page

PATH = "tools/wedding-gift"
TITLE = "כמה לשים בחתונה 2026? מחשבון מעודכן לפי מחיר מנה | תכנון פלוס"
DESC = ("מחשבון חינם: כמה לשים בחתונה ב-2026 לפי קרבה, עונה, אזור, יום בשבוע וסוג האולם. "
        "לבד, בזוג או עם ילדים – כולל טווח מקובל וטבלה לכל רמת קרבה.")

SOURCES = """
<ul class="source">
<li>מחירי מנה 2026 (תל אביב והמרכז: קיץ כ-420–550 ₪, חורף כ-340–430 ₪, תוספת של כ-40–70 ₪ ביום חמישי) – לפי מחירון Attending לשנת 2026 כפי שצוטט בעיתונות הכלכלית,
 למשל <a href="https://www.bizportal.co.il/financialconsumerism/news/article/20043776" rel="noopener" target="_blank">Bizportal</a> ו<a href="https://finance.walla.co.il/item/3807201" rel="noopener" target="_blank">וואלה כסף</a>. נבדק {u}.</li>
<li>עלות חתונה טיפוסית – נתוני zap מתחתנים 2025 כפי שפורסמו ב-<a href="https://www.mako.co.il/news-specials/data_n12/Article-d63f6b035bc1791026.htm" rel="noopener" target="_blank">N12</a>.</li>
<li>טווחים מסורתיים לפי קרבה (מכרים, חברים, חברים קרובים) – <a href="https://www.israelhayom.co.il/article/389413?amp=1" rel="noopener" target="_blank">ישראל היום: כמה כסף שמים לחתונה</a>; וגם <a href="https://www.kipa.co.il/יחסים/חתונה/1153162-0" rel="noopener" target="_blank">כיפה</a>. חלק מהנתונים שם ישנים, ולכן המחשבון מתבסס על מחיר המנה העדכני.</li>
<li>מקדמי הקרבה, ההנחה לזוג, יום שישי בצהריים ואולם צנוע/יוקרתי – הכיול שלנו, לא נתון רשמי. אין "סכום נכון" אחד: זו נקודת התחלה.</li>
</ul>""".format(u=UPDATED_HE)

FAQS = [
    ("כמה לשים בחתונה כזוג ב-2026?",
     "לזוג חברים באולם במרכז בקיץ המחשבון ממליץ על כ-750 ₪ (טווח 650–850 ₪). לזוג חברים קרובים כ-1,000 ₪, ולמכרים כ-550 ₪. בחורף ומחוץ למרכז הסכומים נמוכים בכ-10%–20%."),
    ("כמה לשים בחתונה אם מגיעים לבד?",
     "חבר/ה שמגיע/ה לבד: כ-400 ₪ באולם רגיל במרכז בקיץ, וכ-350 ₪ בחורף. מכר/ה: כ-300 ₪. חבר/ה קרוב/ה: כ-550 ₪."),
    ("כמה לשים בחתונה אם לא מגיעים?",
     "מי שלא מגיע לא צורך מנה, ולכן יש שנוהגים לתת כמחצית מהסכום הרגיל: לחבר/ה כ-200–250 ₪. סמנו \"לא מגיעים\" במחשבון."),
    ("כמה לשים לבן דוד או לאח?",
     "למשפחה מורחבת (בני דודים) המחשבון מתחיל בכ-600 ₪ לאדם, ולמשפחה קרובה (אחים, דודים) בכ-950 ₪ לאדם ומעלה. במשפחות רבות יש מנהג משפחתי – הוא גובר על כל מחשבון."),
    ("האם חתונה ביום שישי בצהריים זולה יותר?",
     "בדרך כלל כן: אירועי צהריים ויום שישי מתומחרים נמוך יותר מערב באמצע השבוע, ולכן גם הסכום המקובל נמוך מעט. ביום חמישי המנה יקרה יותר."),
    ("מה זה \"לעגל לכפולה של 18\"?",
     "יש שנוהגים לתת סכום שמתחלק ב-18 (\"חי\"), כמו 360, 540 או 720 ₪. סמנו את האפשרות והמחשבון יעגל בהתאם."),
    ("האם המחשבון שומר את הנתונים שלי?",
     "לא. החישוב מתבצע כולו בדפדפן שלכם, ושום נתון לא נשלח לשרת."),
]


def build():
    bc = breadcrumbs([("דף הבית", "../../"), ("מחשבונים", "../"), ("כמה לשים בחתונה", None)])
    body = f"""
<section class="hero">
 <div class="container narrow">
  {bc}
  <span class="eyebrow">מחשבון חינם · עודכן {UPDATED_HE}</span>
  <h1>כמה לשים בחתונה 2026? <span class="hl">מחשבון מעודכן</span></h1>
  <p class="lead">בקצרה: ב-2026 מנה באולם במרכז עולה כ-340–550 ₪ לאדם (חורף עד קיץ). לפי המחשבון שלנו (על בסיס מחיר המנה העדכני), חבר/ה שמגיע/ה לבד שם/ה כ-350–450 ₪,
  זוג חברים כ-650–850 ₪, ומשפחה קרובה 1,000 ₪ ומעלה. המחשבון מתאים את הסכום בדיוק למצב שלכם.</p>
 </div>
</section>

<section class="section" style="padding-top:0">
 <div class="container narrow">
  <form id="gift-form" class="tool-panel" novalidate>
   <div class="field">
    <span class="label" id="l-close">מה הקרבה שלכם לזוג?</span>
    <div class="choices" role="radiogroup" aria-labelledby="l-close">
     <label><input type="radio" name="closeness" value="acquaintance"> מכר/ה</label>
     <label><input type="radio" name="closeness" value="work"> מהעבודה</label>
     <label><input type="radio" name="closeness" value="friend" checked> חבר/ה</label>
     <label><input type="radio" name="closeness" value="close"> חבר/ה קרוב/ה</label>
     <label><input type="radio" name="closeness" value="family"> משפחה מורחבת</label>
     <label><input type="radio" name="closeness" value="nuclear"> משפחה קרובה</label>
    </div>
   </div>
   <div class="fields cols-2">
    <div class="field">
     <span class="label" id="l-adults">כמה מבוגרים?</span>
     <div class="choices" role="radiogroup" aria-labelledby="l-adults">
      <label><input type="radio" name="adults" value="1"> לבד</label>
      <label><input type="radio" name="adults" value="2" checked> זוג</label>
      <label><input type="radio" name="adults" value="3"> 3</label>
      <label><input type="radio" name="adults" value="4"> 4</label>
     </div>
    </div>
    <div class="field">
     <label for="kids">ילדים שמגיעים</label>
     <input type="number" id="kids" name="kids" min="0" max="10" value="0" inputmode="numeric">
     <span class="hint">ילד נספר כחצי מנה</span>
    </div>
   </div>
   <div class="fields cols-2">
    <div class="field">
     <span class="label" id="l-att">מגיעים לחתונה?</span>
     <div class="choices" role="radiogroup" aria-labelledby="l-att">
      <label><input type="radio" name="attend" value="yes" checked> מגיעים</label>
      <label><input type="radio" name="attend" value="no"> לא מגיעים</label>
     </div>
    </div>
    <div class="field">
     <span class="label" id="l-season">עונה</span>
     <div class="choices" role="radiogroup" aria-labelledby="l-season">
      <label><input type="radio" name="season" value="summer" checked> קיץ (אפריל–אוקטובר)</label>
      <label><input type="radio" name="season" value="winter"> חורף</label>
     </div>
    </div>
   </div>
   <div class="fields cols-3">
    <div class="field">
     <label for="region">אזור</label>
     <select id="region" name="region">
      <option value="center">תל אביב והמרכז / שרון</option>
      <option value="other">צפון / דרום / ירושלים</option>
     </select>
    </div>
    <div class="field">
     <label for="day">יום</label>
     <select id="day" name="day">
      <option value="weekday">ראשון–רביעי בערב</option>
      <option value="thursday">חמישי בערב</option>
      <option value="friday">שישי / צהריים</option>
     </select>
    </div>
    <div class="field">
     <label for="venue">סוג המקום</label>
     <select id="venue" name="venue">
      <option value="regular">אולם / גן אירועים רגיל</option>
      <option value="luxury">מקום יוקרתי</option>
      <option value="modest">אירוע צנוע / מסעדה</option>
     </select>
    </div>
   </div>
   <details class="mb-2">
    <summary class="small" style="cursor:pointer;font-weight:700">יודעים את מחיר המנה? (אופציונלי)</summary>
    <div class="field mt-1">
     <label for="plate">מחיר מנה לאדם</label>
     <div class="input-affix"><input type="number" id="plate" name="plate" min="0" placeholder="למשל 450" inputmode="numeric"><span class="affix">₪</span></div>
     <span class="hint">אם תזינו מחיר, הוא יחליף את ההערכה לפי עונה, אזור ויום</span>
    </div>
   </details>
   <label class="small" style="display:flex;gap:.5rem;align-items:center"><input type="checkbox" name="chai"> לעגל לכפולה של 18 (חי)</label>

   <div class="result mt-2" aria-live="polite">
    <div class="label">סכום מומלץ · <span id="r-who"></span></div>
    <div class="big" id="r-amount">₪0</div>
    <div>טווח מקובל: <strong id="r-range" class="num"></strong></div>
    <div class="small muted mt-1"><span id="r-plate"></span>. <span id="r-note"></span></div>
   </div>
   <div class="table-wrap mt-2">
    <table><caption class="sr-only">סכום לפי רמת קרבה באותם תנאים</caption>
     <thead><tr><th>אותם תנאים, לפי קרבה</th><th class="num">סכום</th></tr></thead>
     <tbody id="r-table"></tbody></table>
   </div>
   <noscript><p class="noscript">המחשבון צריך JavaScript. בינתיים: חבר/ה לבד כ-400 ₪, זוג חברים כ-750 ₪, משפחה קרובה 1,000 ₪ ומעלה.</p></noscript>
  </form>
  <style>#r-table tr.sel td{{background:var(--accent-soft);font-weight:700}}</style>

  <div class="cta-box mt-3">
   <div>
    <h2 class="h3" style="font-size:1.2rem">מתחתנים בעצמכם?</h2>
    <p>מתכנן החתונה של תכנון פלוס מסדר תקציב, מוזמנים ואישורי הגעה, ספקים ותשלומים, ורושם כל צ'ק עם מעקב תודות. אקסל ו-Google Sheets, ₪49.</p>
   </div>
   <a class="btn accent" href="../../p/wedding-planner/">למתכנן החתונה</a>
  </div>
 </div>
</section>

<section class="section alt">
 <div class="container narrow prose">
  <h2>איך המחשבון קובע כמה לשים?</h2>
  <p>הנקודה המרכזית היא <strong>מחיר המנה</strong>: נוהג נפוץ בישראל הוא לנסות לפחות "לכסות את המנה". לכן המחשבון מתחיל ממחיר מנה משוער לפי עונה, אזור, יום וסוג המקום,
  ומכפיל במקדם לפי הקרבה: מכר/ה רחוק/ה מכסה כשני שלישים מהמנה, חבר/ה קצת פחות ממנה מלאה, וחבר/ה קרוב/ה או משפחה – יותר מהמנה.</p>
  <h2>כמה לשים בחתונה כזוג?</h2>
  <p>זוג נותן בדרך כלל קצת פחות מכפול מאדם שמגיע לבד, ולכן המחשבון מחשב 90% לכל מבוגר. דוגמה (קיץ, מרכז, אולם רגיל, ראשון–רביעי):</p>
  <div class="table-wrap"><table>
   <thead><tr><th>קרבה</th><th class="num">לבד</th><th class="num">זוג</th></tr></thead>
   <tbody>
    <tr><td>מכר/ה</td><td class="num">₪300</td><td class="num">₪550</td></tr>
    <tr><td>מהעבודה</td><td class="num">₪350</td><td class="num">₪650</td></tr>
    <tr><td>חבר/ה</td><td class="num">₪400</td><td class="num">₪750</td></tr>
    <tr><td>חבר/ה קרוב/ה</td><td class="num">₪550</td><td class="num">₪1,000</td></tr>
    <tr><td>משפחה מורחבת</td><td class="num">₪600</td><td class="num">₪1,100</td></tr>
    <tr><td>משפחה קרובה</td><td class="num">₪950</td><td class="num">₪1,750</td></tr>
   </tbody></table></div>
  <p class="small muted">בחורף ומחוץ למרכז הסכומים נמוכים בכ-10%–20%. באירוע צהריים או ביום שישי – נמוכים יותר; ביום חמישי ובמקום יוקרתי – גבוהים יותר.</p>
  <h2>כמה לשים בחתונה אם לא מגיעים?</h2>
  <p>אין מנה לכסות, ולכן יש שנוהגים לתת כמחצית מהסכום הרגיל לפי הקרבה. אם אתם קרובים מאוד לזוג, אפשר כמובן לתת כאילו הגעתם.</p>
  <h2>צ'ק, ביט או העברה?</h2>
  <p>כל האפשרויות מקובלות היום. עם צ'ק כדאי לכתוב את השם המלא על המעטפה; בביט או בהעברה – לצרף ברכה קצרה עם השם, כדי שהזוג יוכל לרשום ולהודות.</p>
  <h2>מקורות ושיטה</h2>
  {SOURCES}
  <p class="small muted">המחשבון נותן הערכה כללית בלבד. מתנה היא החלטה אישית, ומנהגים משפחתיים או קהילתיים גוברים על כל טבלה.</p>
 </div>
</section>

<section class="section">
 <div class="container narrow">
  <h2>שאלות נפוצות</h2>
  {faq_html(FAQS)}
  <p class="mt-3">עוד: <a href="../../p/wedding-planner/guides/wedding-budget-2026/">תקציב חתונה 2026 – איך מחלקים</a> ·
  <a href="../../p/wedding-planner/guides/rsvp-seating-gifts/">אישורי הגעה, הושבה ורישום צ'קים</a> ·
  <a href="../bar-mitzvah-cost/">מחשבון עלות בר מצווה</a></p>
 </div>
</section>
"""
    ld = [
        {"@type": "WebApplication", "name": "מחשבון כמה לשים בחתונה 2026", "url": BASE + PATH + "/",
         "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "inLanguage": "he-IL",
         "isAccessibleForFree": True, "dateModified": UPDATED, "description": DESC,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ILS"}},
        breadcrumb_ld([("דף הבית", ""), ("מחשבונים", "tools/"), ("כמה לשים בחתונה", PATH + "/")]),
        faq_ld(FAQS),
    ]
    return page(PATH, TITLE, DESC, body, ld, og_image=BASE + "p/wedding-planner/img/screen-1.png",
                scripts='<script src="calc.js" defer></script>\n')
