#!/usr/bin/env python3
"""Generate W3 renovation pages: product page, renovation cost tool, 2 guides.  Run: python3 site_pages.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "household-budget"))
from site_common import page, faq_html, faq_ld, product_ld, app_ld, article_ld, UPDATED_HE  # noqa: E402

P = "p/renovation-budget/"
TOOL = "tools/renovation-cost/"
G1 = P + "guides/renovation-cost-2027/"
G2 = P + "guides/compare-quotes/"
IMG = P + "img/"

SOURCES = [
    ("סוגרים דירה – מחירון שיפוצים 2026", "https://www.sogrimdira.co.il/renovation-prices-2026/",
     "ריצוף, צבע, החלפת חשמל ואינסטלציה, חדר רחצה, שיפוץ דירת 3 חדרים"),
    ("experts.co.il – מחירון מטבחים 2026", "https://experts.co.il/%D7%A0%D7%92%D7%A8-%D7%9C%D7%9E%D7%98%D7%91%D7%97%D7%99%D7%9D/%D7%9E%D7%97%D7%99%D7%A8%D7%95%D7%9F-%D7%9E%D7%98%D7%91%D7%97%D7%99%D7%9D",
     "מטבח בסיסי / סטנדרטי / פרימיום והתקנה"),
    ("מדריך מחירי מזגן מיני מרכזי 2026", "https://xn--5dbilbmjk5btdz.xn--4dbrk0ce/blog/mazgan-mini-merkazi-mehir",
     "מערכת מיני מרכזי לדירת 3–4 חדרים כולל התקנה"),
    ("שיפוצים ישראל – מחירון 2026", "https://shipozimil.co.il/%F0%9F%92%B0-%D7%9E%D7%97%D7%99%D7%A8%D7%95%D7%9F-%D7%A9%D7%99%D7%A4%D7%95%D7%A6%D7%99%D7%9D-%D7%9E%D7%A2%D7%95%D7%93%D7%9B%D7%9F-%D7%9C-2026-%D7%9B%D7%9E%D7%94-%D7%A2%D7%95%D7%9C%D7%94-%D7%9C%D7%A9/",
     "נקודת חשמל חדשה"),
]
SRC_HTML = "<ul>" + "".join(f'<li><a href="{u}" rel="nofollow noopener" target="_blank">{n}</a>: {w}</li>' for n, u, w in SOURCES) + "</ul>"

# ---------------------------------------------------------------- product page
faq = [
    ("באיזו תוכנה זה עובד?", "Excel (2010 ומעלה, כולל Microsoft 365 ו-Excel לנייד) ו-Google Sheets: מעלים ל-Drive ובוחרים «פתיחה באמצעות Google Sheets». גם LibreOffice עובד. אין מאקרו."),
    ("איך הקובץ משווה הצעות מחיר?", "רושמים כל הצעה עם מספר העבודה ומסמנים אם המחיר כולל מע\"מ. הקובץ מוסיף 18% כשצריך, כדי שכל ההצעות יושוו באותו בסיס, מסמן את הזולה ומראה את הפער של כל הצעה ממנה. ליד המחיר רואים אחריות, משך עבודה ותנאי תשלום."),
    ("מה זה בלת\"מ ולמה הקובץ מתריע עליו?", "בלת\"מ (בלתי צפוי מראש) הוא סכום שמשאירים בצד לדברים שמתגלים תוך כדי עבודה. קובעים אחוז (ברירת המחדל 15%), והדשבורד מראה כמה ממנו כבר נאכל ומתריע באדום כשמתקרבים לחריגה."),
    ("זה מתאים גם לבנייה או לשיפוץ חדר אחד?", "כן. רשימת החדרים והתחומים ניתנת לעריכה, ויש 100 שורות עבודה. מתאים משיפוץ אמבטיה ועד שיפוץ דירה מלאה. לבניית בית מאפס הקובץ יעבוד, אבל לא מכסה שלבי היתר ובנייה הנדסיים."),
    ("מה זה קובץ ה-Word?", "רשימת בדיקה להדפסה: מה חייב להופיע בהצעת מחיר, מה לבדוק על הקבלן, לוח תשלומים הוגן, שאלות לפגישה וטבלה להשוואה מהירה בין 3 קבלנים."),
    ("איך מקבלים את הקבצים?", "מיד אחרי התשלום ב-PayPal נפתח עמוד הורדה. אפשר לשלם בכרטיס אשראי דרך PayPal גם בלי חשבון."),
    ("זה ייעוץ הנדסי או משפטי?", "לא. זה כלי תכנון ומעקב. בעבודות מבניות, חשמל וגז עבדו רק עם בעלי רישיון, ובהסכם גדול כדאי להתייעץ עם עורך דין."),
]
body = """
<section class="hero">
  <div class="container">
    {CRUMBS}
    <div class="split">
      <div>
        <h1>אקסל תקציב שיפוץ: מתכנן שיפוץ דירה בעברית</h1>
        <p class="lead">כל השיפוץ בקובץ אחד: עבודות, הצעות מחיר, תשלומים ובלת"מ, עם דשבורד שמראה כמה נשאר.</p>
      </div>
      <div id="buy" class="buy" data-product="renovation-budget" data-compact="1"></div>
      <ul class="hero-points">
        <li>השוואת הצעות כולל מע"מ 18%</li>
        <li>בלת"מ עם התראה</li>
        <li>תזרים תשלומים לפי חודש</li>
        <li>רשימת בדיקה לקבלן (Word)</li>
      </ul>
    </div>
    <p class="w3-note mt-2">עוד לא יודעים כמה זה יעלה? נסו את <a href="{up}tools/renovation-cost/">מחשבון עלות השיפוץ החינמי</a>.</p>
    <img class="w3-hero-img mt-3" src="img/dashboard.webp" width="1400" height="820" alt="דשבורד שיפוץ: מצב התקציב, בלת&quot;מ, לפי חדר ולפי תחום" fetchpriority="high">
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><h2>מה יש בקובץ</h2><p class="muted">7 גיליונות מחוברים. מקלידים בתאים הצהובים, וכל השאר מחושב לבד.</p></div>
    <div class="grid cols-3">
      <div class="card feature"><span class="ic" aria-hidden="true">🏠</span><div><h3>עבודות לפי חדר ותחום</h3><p>100 שורות: חדר, תחום (חשמל, ריצוף, מטבח…), תיאור, אומדן, סטטוס. התקציב מתעדכן לבד כשבוחרים הצעה.</p></div></div>
      <div class="card feature"><span class="ic" aria-hidden="true">⚖️</span><div><h3>השוואת הצעות מחיר</h3><p>כל ההצעות מומרות למחיר כולל מע"מ. הזולה מסומנת, ורואים פער, אחריות, משך ותנאי תשלום.</p></div></div>
      <div class="card feature"><span class="ic" aria-hidden="true">💸</span><div><h3>תשלומים ותזרים</h3><p>תשלומים ששולמו ותשלומים מתוכננים לפי ההסכם, ותזרים לפי חודש כדי לדעת כמה כסף צריך ומתי.</p></div></div>
      <div class="card feature"><span class="ic" aria-hidden="true">🛟</span><div><h3>בלת"מ</h3><p>קובעים אחוז לבלתי צפוי, והדשבורד מראה כמה ממנו נשאר ומתריע כשנוגעים בו.</p></div></div>
      <div class="card feature"><span class="ic" aria-hidden="true">🧾</span><div><h3>מעקב חשבוניות</h3><p>כל תשלום בלי חשבונית או קבלה מסומן, כדי שבסוף השיפוץ יהיו לכם כל המסמכים לאחריות.</p></div></div>
      <div class="card feature"><span class="ic" aria-hidden="true">📇</span><div><h3>אנשי מקצוע</h3><p>טלפונים, מספרי רישום, ביטוח והמלצות במקום אחד. בנוסף: רשימת בדיקה להדפסה לפני חתימה עם קבלן.</p></div></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="section-head"><h2>ככה זה נראה</h2><p class="muted">צילומי מסך מקובץ הדוגמה המצורף, שיפוץ דירת 3 חדרים. המחירים בדוגמה הם להמחשה ואינם הצעת מחיר.</p></div>
    <div class="screens">
      <figure><img src="img/dashboard.webp" loading="lazy" width="1400" height="820" alt="דשבורד שיפוץ"><figcaption>דשבורד: תקציב, בלת"מ, חדרים, תחומים ותזרים</figcaption></figure>
      <figure><img src="img/quotes.webp" loading="lazy" width="1400" height="560" alt="השוואת הצעות מחיר"><figcaption>השוואת הצעות מחיר באותו בסיס של מע"מ</figcaption></figure>
      <figure><img src="img/works.webp" loading="lazy" width="1400" height="560" alt="עבודות ותקציב לפי חדר"><figcaption>עבודות: אומדן, הצעה שנבחרה, שולם ונותר</figcaption></figure>
      <figure><img src="img/payments.webp" loading="lazy" width="1400" height="560" alt="לוח תשלומים"><figcaption>תשלומים: שולם, מתוכנן וחשבוניות</figcaption></figure>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><h2>איך עובדים עם הקובץ</h2></div>
    <ol class="steps">
      <li><h3>רושמים עבודות ואומדן</h3><p>מה עושים בכל חדר והערכה ראשונית. כבר עכשיו רואים אם זה בתוך התקציב.</p></li>
      <li><h3>משווים הצעות</h3><p>רושמים את ההצעות מהקבלנים, משווים כולל מע"מ ובוחרים. התקציב מתעדכן לפי הבחירה.</p></li>
      <li><h3>עוקבים אחרי תשלומים</h3><p>כל תשלום נרשם, והדשבורד מראה כמה נשאר ואם הבלת"מ עדיין שלם.</p></li>
    </ol>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="split">
      <div>
        <h2>מה מקבלים בהורדה</h2>
        <ul class="w3-list">
          <li><strong>מתכנן תקציב שיפוץ</strong>: קובץ אקסל ריק ומוכן לעבודה</li>
          <li><strong>קובץ דוגמה מלא</strong>: שיפוץ דירת 3 חדרים עם הצעות ותשלומים</li>
          <li><strong>רשימת בדיקה לפני חתימה עם קבלן</strong>: קובץ Word להדפסה</li>
        </ul>
        <p class="muted">‎.xlsx ו-‎.docx, בלי מאקרו. רכישה חד-פעמית.</p>
      </div>
      <div><div class="buy" data-product="renovation-budget" data-compact="1"></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    <h2>שאלות נפוצות</h2>
    FAQ
    <h2 class="mt-4">מדריכים</h2>
    <ul class="w3-list w3-guides">
      <li><a href="guides/renovation-cost-2027/">כמה עולה שיפוץ דירה ב-2027? טווחי מחירים לפי עבודה</a></li>
      <li><a href="guides/compare-quotes/">איך משווים הצעות מחיר לשיפוץ (ולמה הזולה לא תמיד זולה)</a></li>
      <li><a href="{up}tools/renovation-cost/">מחשבון עלות שיפוץ (חינם)</a></li>
    </ul>
  </div>
</section>
<div class="buy-bar"><span><strong>מתכנן תקציב שיפוץ</strong> · <span class="price">₪39</span></span><a class="btn small" href="#buy">לרכישה</a></div>
""".replace("FAQ", faq_html(faq))
title = "אקסל תקציב שיפוץ – מתכנן שיפוץ דירה והשוואת הצעות מחיר | תכנון פלוס"
desc = "קובץ אקסל בעברית לניהול שיפוץ: עבודות לפי חדר, השוואת הצעות מחיר כולל מע\"מ, לוח תשלומים, בלת\"מ ודשבורד + רשימת בדיקה לקבלן. ₪39, הורדה מיידית."
page(P, title, desc, body,
     [product_ld("מתכנן תקציב שיפוץ", desc, P, 39, [IMG + "dashboard.webp", IMG + "quotes.webp", IMG + "works.webp"]), faq_ld(faq)],
     og_image=IMG + "dashboard.webp", crumbs=[("מוצרים", "products/"), ("מתכנן תקציב שיפוץ", P)], buy=True)

# ---------------------------------------------------------------- tool
tfaq = [
    ("כמה מדויק המחשבון?", "זה אומדן ראשוני בלבד, לפי טווחי מחירים שפורסמו באתרי מחירונים ישראליים ב-2026 (המקורות למטה). המחיר האמיתי תלוי במצב הדירה, בחומרים, באזור ובקבלן. השתמשו בו כדי לדעת סדר גודל, ובקשו לפחות 3 הצעות מחיר כתובות."),
    ("האם המחירים כוללים מע\"מ?", "המקורות לא תמיד מציינים זאת במפורש. כשמשווים הצעות, ודאו שכולן באותו בסיס: מחיר + 18% מע\"מ."),
    ("למה להוסיף בלת\"מ?", "כמעט בכל שיפוץ מתגלים דברים אחרי שפותחים קירות ורצפות, כמו צנרת ישנה, רטיבות או חשמל שלא עומד בתקן. מקובל לשמור 10%–20% מהתקציב בצד, ובבית ישן כדאי יותר."),
    ("מה לא כלול באומדן?", "דלתות, חלונות ואלומיניום, נגרות וארונות, גופי תאורה, ריהוט, תכנון ופיקוח, היתרים, דיור חלופי והובלה. אפשר להוסיף אותם בשדה «עבודות נוספות»."),
    ("הנתונים שלי נשמרים?", "לא. החישוב רץ בדפדפן ושום מספר לא נשלח לשרת."),
]
tbody = """
<section class="hero">
  <div class="container">
    {CRUMBS}
    <h1>מחשבון עלות שיפוץ דירה 2026</h1>
    <p class="lead">בחרו גודל דירה, רמת גימור ואילו עבודות אתם מתכננים, וקבלו טווח מחירים לכל עבודה ולכל השיפוץ, כולל בלת"מ. מבוסס על מחירונים ישראליים שפורסמו ב-2026.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="split">
      <form class="tool-panel" id="calc" onsubmit="return false" novalidate>
        <div class="fields cols-2">
          <div class="field">
            <label for="area">שטח הדירה</label>
            <div class="input-affix"><input id="area" type="number" inputmode="numeric" min="20" max="400" step="5" value="85"><span class="affix">מ"ר</span></div>
          </div>
          <div class="field">
            <label for="cont">בלת"מ</label>
            <select id="cont"><option value="0.1">10%</option><option value="0.15" selected>15% (מומלץ)</option><option value="0.2">20% (בית ישן)</option></select>
          </div>
        </div>
        <div class="field">
          <span class="label" id="lvl-l">רמת גימור</span>
          <div class="choices" role="radiogroup" aria-labelledby="lvl-l">
            <label><input type="radio" name="level" value="0"> בסיסית</label>
            <label><input type="radio" name="level" value="1" checked> בינונית</label>
            <label><input type="radio" name="level" value="2"> גבוהה</label>
          </div>
        </div>
        <div class="field">
          <span class="label">מה משפצים?</span>
          <div class="choices">
            <label><input type="checkbox" name="w" value="floor" checked> ריצוף</label>
            <label><input type="checkbox" name="w" value="paint" checked> צבע</label>
            <label><input type="checkbox" name="w" value="elec"> החלפת חשמל</label>
            <label><input type="checkbox" name="w" value="plumb"> החלפת אינסטלציה</label>
            <label><input type="checkbox" name="w" value="kitchen" checked> מטבח חדש</label>
            <label><input type="checkbox" name="w" value="ac"> מזגן מיני מרכזי</label>
          </div>
        </div>
        <div class="fields cols-2">
          <div class="field">
            <label for="baths">חדרי רחצה לשיפוץ מלא</label>
            <select id="baths"><option value="0">0</option><option value="1" selected>1</option><option value="2">2</option><option value="3">3</option></select>
          </div>
          <div class="field">
            <label for="extra">עבודות נוספות (הערכה שלכם)</label>
            <div class="input-affix"><input id="extra" type="number" inputmode="numeric" min="0" step="500" placeholder="דלתות, חלונות, נגרות…"><span class="affix">₪</span></div>
          </div>
        </div>
      </form>
      <div aria-live="polite">
        <div class="result">
          <div class="label">אומדן לשיפוץ כולל בלת"מ</div>
          <div class="big" id="total">–</div>
          <p class="mb-0" id="sub"></p>
        </div>
        <div class="table-wrap mt-2">
          <table><thead><tr><th>עבודה</th><th class="num">טווח משוער</th></tr></thead><tbody id="rows"></tbody></table>
        </div>
        <p class="w3-note mt-1" id="bench"></p>
      </div>
    </div>
    <div class="cta-box mt-4">
      <div><h2 class="h3">מתחילים לקבל הצעות מחיר?</h2><p>ב«מתכנן תקציב שיפוץ» מעבירים את האומדן לטבלת עבודות, משווים הצעות כולל מע"מ, עוקבים אחרי תשלומים ורואים בכל רגע כמה בלת"מ נשאר. ₪39, כולל רשימת בדיקה לפני חתימה עם קבלן.</p></div>
      <a class="btn accent" href="{up}p/renovation-budget/">לקובץ המלא</a>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container narrow prose">
    <h2>איך המחשבון מחשב</h2>
    <ul>
      <li><strong>ריצוף:</strong> 180–350 ₪ למ"ר, כולל פירוק, יישור והתקנה, כפול שטח הדירה.</li>
      <li><strong>צבע:</strong> 4,500–7,000 ₪ לדירת 4 חדרים כולל תקרות. הנחנו דירה של כ-100 מ"ר, כלומר 45–70 ₪ למ"ר רצפה.</li>
      <li><strong>החלפת חשמל:</strong> 18,000–45,000 ₪ לדירה. <strong>החלפת אינסטלציה:</strong> 15,000–35,000 ₪ לדירה. שני הטווחים מותאמים לגודל הדירה ביחס ל-90 מ"ר.</li>
      <li><strong>חדר רחצה קומפלט:</strong> 35,000–75,000 ₪ לחדר.</li>
      <li><strong>מטבח:</strong> בסיסי 15–22 אלף, סטנדרטי 25–40 אלף, פרימיום 45–70 אלף ₪, ועוד 2,500–5,000 ₪ להתקנה.</li>
      <li><strong>מזגן מיני מרכזי:</strong> 15,000–40,000 ₪ לדירת 3–4 חדרים, כולל התקנה.</li>
      <li><strong>רמת גימור:</strong> בסיסית לוקחת את החלק התחתון של כל טווח, בינונית את האמצע, וגבוהה את החלק העליון.</li>
    </ul>
    <p>להשוואה: שיפוץ מלא של דירת 3 חדרים (כ-75 מ"ר) מוערך ב-120,000–200,000 ₪.</p>
    <h3>מקורות (נבדקו ב-UPD)</h3>
    SRC
    <p>המחירים נאספו מאתרי מחירונים מסחריים, ולא ממקור רשמי. הם משתנים לפי אזור, מצב הדירה וחומרים. המחשבון נותן סדר גודל ואינו הצעת מחיר.</p>
    <p>מדריכים: <a href="{up}p/renovation-budget/guides/renovation-cost-2027/">כמה עולה שיפוץ דירה ב-2027</a> · <a href="{up}p/renovation-budget/guides/compare-quotes/">איך משווים הצעות מחיר לשיפוץ</a></p>
    <h2>שאלות נפוצות</h2>
    TFAQ
  </div>
</section>
""".replace("TFAQ", faq_html(tfaq)).replace("SRC", SRC_HTML).replace("UPD", UPDATED_HE)
ttitle = "מחשבון עלות שיפוץ דירה 2026 – כמה עולה לשפץ? | תכנון פלוס"
tdesc = "מחשבון עלות שיפוץ בעברית: גודל דירה, רמת גימור ועבודות (ריצוף, צבע, חשמל, אינסטלציה, מטבח, אמבטיה, מזגן) וקבלו טווח מחירים עם בלת\"מ. לפי מחירונים מ-2026."
page(TOOL, ttitle, tdesc, tbody, [app_ld("מחשבון עלות שיפוץ דירה", tdesc, TOOL), faq_ld(tfaq)],
     og_image=IMG + "dashboard.webp", crumbs=[("כלים חינם", "tools/"), ("מחשבון עלות שיפוץ", TOOL)],
     extra_scripts=['<script src="calc.js"></script>'])

# ---------------------------------------------------------------- guide 1: cost
rows = [
    ("ריצוף (כולל פירוק והתקנה)", "180–350 ₪ למ\"ר", 0),
    ("צביעת דירת 4 חדרים כולל תקרות", "4,500–7,000 ₪", 0),
    ("החלפת תשתית חשמל לדירה", "18,000–45,000 ₪", 0),
    ("נקודת חשמל חדשה כולל חיווט", "350–550 ₪ לנקודה", 3),
    ("החלפת אינסטלציה לדירה", "15,000–35,000 ₪", 0),
    ("שיפוץ חדר רחצה קומפלט", "35,000–75,000 ₪", 0),
    ("מטבח בסיסי / סטנדרטי / פרימיום", "15–22 / 25–40 / 45–70 אלף ₪", 1),
    ("התקנת מטבח", "2,500–5,000 ₪", 1),
    ("מזגן מיני מרכזי לדירת 3–4 חדרים", "15,000–40,000 ₪", 2),
    ("שיפוץ מלא, דירת 3 חדרים (~75 מ\"ר)", "120,000–200,000 ₪", 0),
]
table = '<div class="table-wrap"><table><thead><tr><th>עבודה</th><th class="num">טווח מחירים</th><th>מקור</th></tr></thead><tbody>' + \
    "".join(f'<tr><td>{a}</td><td class="num">{b}</td><td><a href="{SOURCES[s][1]}" rel="nofollow noopener" target="_blank">{SOURCES[s][0].split(" – ")[0]}</a></td></tr>' for a, b, s in rows) + \
    "</tbody></table></div>"
g1 = """
<article class="section">
  <div class="container narrow prose">
    {CRUMBS}
    <h1>כמה עולה שיפוץ דירה ב-2027? טווחי מחירים לפי עבודה</h1>
    <p class="updated muted">עודכן: UPD · זמן קריאה: 6 דקות</p>
    <p><strong>בקצרה:</strong> שיפוץ מלא של דירת 3 חדרים מוערך ב-120–200 אלף ₪. שיפוץ חדר רחצה לבדו עולה 35–75 אלף, ומטבח חדש 15–70 אלף לפי הרמה. לכל אומדן הוסיפו 10%–20% בלת"מ. המחירים כאן מבוססים על מחירונים שפורסמו ב-2026, וב-2027 כדאי לצפות לעליות קלות.</p>
    <h2>טבלת מחירים לפי עבודה</h2>
    TABLE
    <p class="source">המחירים נאספו מאתרי מחירונים מסחריים בנובמבר 2026. אלה לא מחירים רשמיים, והם משתנים לפי אזור, מצב הדירה וחומרים.</p>
    <p>רוצים חישוב לדירה שלכם? <a href="{up}tools/renovation-cost/">מחשבון עלות השיפוץ</a> מחבר את הטווחים לפי השטח, רמת הגימור והעבודות שבחרתם.</p>

    <h2>מה מייקר שיפוץ</h2>
    <ul>
      <li><strong>תשתיות ישנות.</strong> בבניין משנות ה-70 וה-80 הרבה פעמים צריך להחליף צנרת וחשמל, וזה מוסיף עשרות אלפי שקלים שלא רואים בסוף.</li>
      <li><strong>הזזת קירות, מטבח או נקודות מים.</strong> כל העברה של ניקוז או נקודת מים מוסיפה עבודת אינסטלציה, איטום וריצוף.</li>
      <li><strong>רמת הגימור.</strong> אריח פורצלן גדול, ברזים מעוצבים ומשטח קוורץ יכולים להכפיל את עלות החומרים.</li>
      <li><strong>לוח זמנים לחוץ.</strong> קבלן שצריך לעבוד מהר או בסופי שבוע יגבה יותר.</li>
      <li><strong>קומה גבוהה בלי מעלית משא.</strong> הובלת חומרים ופינוי פסולת עולים יותר.</li>
    </ul>

    <h2>הוצאות שרוב האנשים שוכחים</h2>
    <ul>
      <li>פינוי פסולת ומכולה.</li>
      <li>תכנון: אדריכל או מעצב, ולפעמים מהנדס לקירות נושאים.</li>
      <li>היתר מהעירייה ואישור מהוועד או מהנציגות, כשנדרש.</li>
      <li>דיור חלופי או אחסון רהיטים בזמן העבודה.</li>
      <li>גופי תאורה, ידיות, אביזרי אמבטיה, וילונות.</li>
      <li>ניקיון סוף שיפוץ.</li>
    </ul>

    <h2>כמה בלת"מ להשאיר?</h2>
    <p>כלל אצבע: 10% בדירה חדשה יחסית, 15% בשיפוץ רגיל ו-20% בבית ישן או כשפותחים תשתיות. הבלת"מ הוא לא "כסף נוסף לשדרוגים". הוא נועד לדברים שמתגלים בדרך. כדאי לעקוב כמה ממנו כבר נוצל, כדי לא לגלות את החריגה בתשלום האחרון.</p>

    <div class="cta-box mt-3">
      <div><h2 class="h3">מאומדן לתקציב שמחזיק</h2><p>«מתכנן תקציב שיפוץ» מחבר עבודות, הצעות מחיר ותשלומים, ומראה בדשבורד כמה התחייבתם, כמה שולם וכמה בלת"מ נשאר. ₪39.</p></div>
      <a class="btn accent" href="{up}p/renovation-budget/">לפרטים על הקובץ</a>
    </div>
    <p class="mt-3">הצעד הבא: <a href="../compare-quotes/">איך משווים הצעות מחיר לשיפוץ</a>.</p>
    <p class="source">המדריך הוא מידע כללי ואינו הצעת מחיר או ייעוץ הנדסי.</p>
  </div>
</article>
""".replace("TABLE", table).replace("UPD", UPDATED_HE)
t1 = "כמה עולה שיפוץ דירה ב-2027? מחירון לפי עבודה | תכנון פלוס"
d1 = "טווחי מחירים לשיפוץ דירה: ריצוף, צבע, חשמל, אינסטלציה, חדר רחצה, מטבח ומזגן, עם מקורות. מה מייקר שיפוץ, מה שוכחים לתקצב וכמה בלת\"מ להשאיר."
page(G1, t1, d1, g1, [article_ld(t1.split(" | ")[0], d1, G1, IMG + "dashboard.webp")], og_image=IMG + "dashboard.webp",
     crumbs=[("מתכנן תקציב שיפוץ", P), ("כמה עולה שיפוץ", G1)])

# ---------------------------------------------------------------- guide 2: compare quotes
ex = """<div class="table-wrap"><table><thead><tr><th>קבלן</th><th class="num">המחיר בהצעה</th><th>כולל מע"מ?</th><th>חומרים</th><th class="num">אחריות</th><th class="num">מחיר להשוואה</th></tr></thead><tbody>
<tr><td>קבלן א'</td><td class="num">₪16,500</td><td>לא</td><td>כלולים</td><td class="num">12 חודשים</td><td class="num"><strong>₪19,470</strong></td></tr>
<tr><td>קבלן ב'</td><td class="num">₪21,000</td><td>כן</td><td>כלולים</td><td class="num">24 חודשים</td><td class="num"><strong>₪21,000</strong></td></tr>
<tr><td>קבלן ג'</td><td class="num">₪17,200</td><td>כן</td><td>לא כלולים</td><td class="num">12 חודשים</td><td class="num"><strong>₪17,200 + חומרים</strong></td></tr>
</tbody></table></div>"""
g2 = """
<article class="section">
  <div class="container narrow prose">
    {CRUMBS}
    <h1>איך משווים הצעות מחיר לשיפוץ (ולמה הזולה לא תמיד זולה)</h1>
    <p class="updated muted">עודכן: UPD · זמן קריאה: 5 דקות</p>
    <p><strong>בקצרה:</strong> לפני שמשווים, מביאים את כל ההצעות לאותו בסיס: מחיר כולל מע"מ, אותה רשימת עבודות ואותם חומרים. רק אחרי זה משווים מחיר, ולצדו אחריות, לוח זמנים ותנאי תשלום.</p>
    <h2>דוגמה: שלוש הצעות לעבודת חשמל</h2>
    <p>על הנייר קבלן א' הכי זול, ב-16,500 ₪. אבל המחיר שלו לא כולל מע"מ, ואחרי תוספת 18% הוא עולה 19,470 ₪. קבלן ג' נראה זול יותר, אבל החומרים לא כלולים בהצעה שלו.</p>
    EX
    <p>אחרי ההשוואה ההחלטה כבר לא מובנת מאליה: קבלן ב' יקר ב-1,530 ₪ מקבלן א', אבל נותן אחריות כפולה. לגבי קבלן ג', צריך לבקש הערכה למחיר החומרים לפני שאפשר להשוות.</p>

    <h2>5 כללים להשוואה הוגנת</h2>
    <ol>
      <li><strong>אותו כתב כמויות לכולם.</strong> שלחו לכל הקבלנים את אותה רשימה: מה עושים, באיזו כמות (מ"ר, נקודות, יחידות) ובאיזה חומר. בלי זה כל אחד מתמחר שיפוץ אחר.</li>
      <li><strong>הכול כולל מע"מ.</strong> מע"מ בישראל הוא 18% (מאז 1 בינואר 2025, לפי רשות המסים). הצעה "לפני מע"מ" תמיד נראית זולה יותר.</li>
      <li><strong>מה כלול ומה לא.</strong> חומרים, פינוי פסולת, הגנה על הבית, ניקיון. כל "לא כלול" הוא תוספת שתשלמו בהמשך.</li>
      <li><strong>אחריות ולוח זמנים.</strong> 12 חודשי אחריות לעומת 24 שווים כסף. גם קבלן שמתחיל עוד חודשיים עולה לכם, למשל בשכר דירה נוסף.</li>
      <li><strong>לוח תשלומים לפי שלבים.</strong> העדיפו קבלן שמקבל תשלום על שלבים שהסתיימו ומשאיר סכום אחרון למסירה, על פני קבלן שמבקש את רוב הכסף מראש.</li>
    </ol>

    <h2>סימנים שכדאי לעצור ולבדוק</h2>
    <ul>
      <li>הצעה זולה ב-30% ויותר מכל השאר. בדרך כלל משהו חסר בה.</li>
      <li>סכום כולל בלי פירוט סעיפים.</li>
      <li>דרישה למקדמה גבוהה במזומן.</li>
      <li>אין שם מלא, מספר עוסק או רישום. קבלן רשום אפשר לבדוק בפנקס הקבלנים של רשם הקבלנים ב-gov.il.</li>
      <li>"נסגור את הפרטים תוך כדי". כל מה שלא כתוב יהפוך לוויכוח.</li>
    </ul>

    <div class="cta-box mt-3">
      <div><h2 class="h3">השוואה אוטומטית באקסל</h2><p>ב«מתכנן תקציב שיפוץ» רושמים כל הצעה ומסמנים אם היא כוללת מע"מ. הקובץ ממיר הכול לאותו בסיס, מסמן את הזולה ומראה את הפער של כל הצעה. מגיע עם רשימת בדיקה להדפסה לפני חתימה. ₪39.</p></div>
      <a class="btn accent" href="{up}p/renovation-budget/">לפרטים על הקובץ</a>
    </div>
    <p class="mt-3">עוד לא יודעים כמה השיפוץ אמור לעלות? <a href="{up}tools/renovation-cost/">מחשבון עלות שיפוץ</a> · <a href="../renovation-cost-2027/">מחירון שיפוצים לפי עבודה</a></p>
    <p class="source">המדריך הוא מידע כללי ואינו ייעוץ משפטי. בהסכם גדול כדאי להתייעץ עם עורך דין.</p>
  </div>
</article>
""".replace("EX", ex).replace("UPD", UPDATED_HE)
t2 = "איך משווים הצעות מחיר לשיפוץ – מדריך עם דוגמה | תכנון פלוס"
d2 = "איך להשוות הצעות מחיר של קבלני שיפוצים: מע\"מ 18%, מה כלול, חומרים, אחריות ולוח תשלומים. דוגמה מספרית שמראה למה ההצעה הזולה לא תמיד זולה."
page(G2, t2, d2, g2, [article_ld(t2.split(" | ")[0], d2, G2, IMG + "quotes.webp")], og_image=IMG + "quotes.webp",
     crumbs=[("מתכנן תקציב שיפוץ", P), ("השוואת הצעות מחיר", G2)])
print("renovation pages written")
