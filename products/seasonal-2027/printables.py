#!/usr/bin/env python3
"""Free printables (Hebrew, A4 PDF, printed by Chromium from HTML):
  out/pesach-cleaning-checklist-2027.pdf  – ניקיון לפסח חדר אחר חדר + לוח זמנים לערב פסח
  out/savings-challenge-2027.pdf          – אתגר חיסכון 2027: 52 שבועות + 12 חודשים
Content lists (CLEAN, MONTH_TIPS) are also imported by site.py so the web pages and the PDFs say the same thing.
    python3 printables.py"""
import datetime
import html
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
FONTS = (HERE.parent / "hanukkah" / "fonts").as_uri()
e = html.escape

# room, [tasks]
CLEAN = [
    ("מטבח: מקרר ומקפיא", ["מוציאים הכול, זורקים או אורזים חמץ", "שוטפים מדפים, מגירות וגומיות הדלת", "מנגבים ידיות ודופן עליונה",
                          "מקפיא: מסיימים או מוכרים חמץ קפוא לפני", "מכסים מדפים (אם זה המנהג שלכם)"]),
    ("מטבח: תנור, כיריים ומיקרוגל", ["תנור: ניקוי יסודי ואחריו הכשרה לפי המנהג", "כיריים: מנקים סביב המבערים והרשתות",
                                   "מיקרוגל: ניקוי ובדיקה, או סגירה לחג", "טוסטר וטוסטר-אובן: אורזים ומסלקים לחג"]),
    ("מטבח: ארונות ומשטחים", ["מרוקנים ארונות חמץ, מנגבים פירורים", "סוגרים ומסמנים ארון חמץ שנמכר", "משטחי עבודה: ניקוי וכיסוי או הכשרה",
                             "כיור וברזים: ניקוי יסודי", "מגירת סכו״ם ומגירת «הכול»", "פח אשפה: שוטפים ומחליפים שקית"]),
    ("מטבח: מכשירים וכלים", ["מיקסר, מעבד מזון, מטחנה: מנקים או אורזים", "קומקום ומכונת קפה: בודקים לפי המנהג", "מוציאים כלי פסח ומדיחים",
                            "מדיח כלים: לפי המנהג (הכשרה או אי-שימוש)"]),
    ("פינת אוכל וסלון", ["שולחן, כיסאות ופינות", "ספות: מתחת לכריות ובין המושבים", "כיסא תינוק ועגלה", "מדפים שאכלו לידם ושולחן קפה"]),
    ("חדרי ילדים", ["תיקי בית ספר וילקוטים", "מגירות ושולחן כתיבה", "מתחת למיטה ובין הצעצועים", "מחביאים של ממתקים וחטיפים",
                   "קופסאות אוכל ובקבוקים"]),
    ("חדרי שינה וארונות", ["כיסי מעילים, ז׳קטים ומכנסיים", "שידות לילה", "תיקים, ארנקים ותיקי גב"]),
    ("רכב", ["מושבי ילדים ובין הכיסאות", "תא כפפות ותאי דלת", "תא מטען ושטיחונים", "שואב אבק יסודי"]),
    ("עבודה, מרפסת ומחסן", ["מגירה במשרד ובעבודה", "מרפסת ופינת ישיבה בחוץ", "מחסן: אוכל לבעלי חיים, שקיות ישנות", "מזון לחיות מחמד: לבדוק מה מותר בפסח"]),
]
TIMELINE = [("4 שבועות לפני", "מחלקים חדרים ותפקידים. מתחילים מהחדרים שאין בהם אוכל"),
            ("3 שבועות לפני", "ארונות בגדים, חדרי ילדים, סלון ורכב"),
            ("שבועיים לפני", "מכינים רשימת קניות לפסח. מזמינים מצות שמורות"),
            ("שבוע לפני", "מוכרים חמץ (דרך הרב או בטופס מקוון של רבנות). מסיימים חמץ במקפיא"),
            ("3 ימים לפני", "המטבח: מקרר, ארונות, תנור, כיריים ומשטחים. מוציאים כלי פסח"),
            ("שלישי 20.4.2027 בערב", "בדיקת חמץ לאור נר, אחרי צאת הכוכבים, ואמירת «כל חמירא»"),
            ("רביעי 21.4.2027 בבוקר", "אוכלים חמץ ושורפים אותו עד השעה שמתפרסמת בעירכם. ביטול חמץ"),
            ("רביעי 21.4.2027 בערב", "ליל הסדר. חג שמח!")]

# 12 months, one money habit each (general, not financial advice)
MONTH_TIPS = ["עוברים על דפי הבנק והאשראי של דצמבר ובונים תקציב לשנה", "מבטלים מנוי אחד שלא משתמשים בו", "משווים מחירי ביטוח רכב ודירה לפני חידוש",
              "מתכננים את קניות פסח מראש, עם רשימה ותקציב", "שבוע «בלי לקנות בחוץ»: אוכל מהבית", "בודקים את דמי הניהול בקרן הפנסיה ובקרן ההשתלמות",
              "קובעים תקציב לחופש הגדול לפני שמזמינים", "מפרישים כבר עכשיו לציוד בית הספר ולחגי תשרי", "בודקים מסלול סלולר ואינטרנט מול מה שיש בשוק",
              "מוכרים בגדים וחפצים שלא בשימוש", "בודקים זכאות להחזר מס על השנים האחרונות", "סיכום שנה: כמה חסכנו, ומה היעד ל-2028"]
MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]

CSS = """
@font-face{font-family:Assistant;src:url(FONTS/Assistant-400.ttf);font-weight:400}
@font-face{font-family:Assistant;src:url(FONTS/Assistant-700.ttf);font-weight:700}
@font-face{font-family:Assistant;src:url(FONTS/Assistant-800.ttf);font-weight:800}
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box}html,body{margin:0}
body{font-family:Assistant,sans-serif;color:#1d2a2e;-webkit-print-color-adjust:exact;print-color-adjust:exact;direction:rtl}
.page{width:210mm;height:297mm;padding:12mm 13mm 9mm;display:flex;flex-direction:column;break-after:page;overflow:hidden}
.top{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2mm solid ACC;padding-bottom:2mm;margin-bottom:3mm}
h1{font-size:25pt;font-weight:800;margin:0;color:#173a66;line-height:1.1}.top p{margin:1mm 0 0;font-size:11pt;color:#4b5a66}
.brand{font-weight:800;color:ACC;font-size:11pt;white-space:nowrap}
.grid{columns:2;column-gap:7mm;flex:1}
.room{break-inside:avoid;margin:0 0 3.2mm;border:.4mm solid #d5dde5;border-radius:3mm;padding:2mm 3mm}
.room h2{font-size:12.5pt;margin:0 0 1mm;color:#173a66}
.room ul{list-style:none;margin:0;padding:0}.room li{font-size:10.6pt;padding:.7mm 0;display:flex;gap:2mm;align-items:baseline}
.cb{flex:none;width:3.8mm;height:3.8mm;border:.4mm solid #1d2a2e;border-radius:.8mm;display:inline-block;transform:translateY(.6mm)}
table{width:100%;border-collapse:collapse;font-size:10.5pt}th,td{border:.3mm solid #c8d2dc;padding:1.3mm 2mm;text-align:center}
th{background:#eef3f8;color:#173a66}td.l{text-align:right}
.note{font-size:9pt;color:#5b6b7c;margin-top:2mm}.foot{display:flex;justify-content:space-between;font-size:8.5pt;color:#6b7a88;margin-top:2mm}
.wk{display:grid;grid-template-columns:1fr 1fr;gap:0 6mm;flex:1}
.wk table td{padding:.75mm 1.5mm;font-size:9.6pt}
.big{font-size:13pt;font-weight:800;color:ACC}
.tl td{font-size:10.5pt}
.mo td{height:15mm}
"""


def doc(pages, acc):
    return (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{CSS.replace("FONTS", FONTS).replace("ACC", acc)}</style>'
            f'</head><body>{"".join(pages)}</body></html>')


def top(h, sub):
    return f'<div class="top"><div><h1>{e(h)}</h1><p>{e(sub)}</p></div><div class="brand">תכנון פלוס</div></div>'


def foot(n, total, url):
    return f'<div class="foot"><span>{e(url)} · חינם לשימוש אישי ולהדפסה</span><span>עמוד {n} מתוך {total}</span></div>'


def cleaning():
    rooms = "".join(f'<div class="room"><h2>{e(r)}</h2><ul>' + "".join(f'<li><span class="cb"></span>{e(t)}</li>' for t in ts) + "</ul></div>"
                    for r, ts in CLEAN)
    p1 = (f'<section class="page">{top("ניקיון לפסח 2027: חדר אחר חדר", "צ׳קליסט להדפסה. מסמנים ✓ ומחלקים בין בני הבית.")}'
          f'<div class="grid">{rooms}</div>'
          '<p class="note">העיקרון: מנקים מחמץ את המקומות שאולי נכנס אליהם חמץ. מקום שלא מכניסים אליו חמץ לא צריך בדיקה '
          '(שולחן ערוך, אורח חיים, סימן תל״ג סעיף ג׳). ניקיון אביב הוא בונוס, לא חובה. בשאלות הלכה פנו לרב.</p>'
          f'{foot(1, 2, "tichnun.netlify.app/pesach/")}</section>')
    rows = "".join(f'<tr><td class="l"><b>{e(a)}</b></td><td class="l">{e(b)}</td><td><span class="cb"></span></td></tr>' for a, b in TIMELINE)
    who = "".join(f'<tr><td class="l">{e(r)}</td><td></td><td></td><td><span class="cb"></span></td></tr>' for r, _ in CLEAN)
    p2 = (f'<section class="page">{top("לוח זמנים לניקיון ולערב פסח", "פסח 2027: ליל הסדר ביום רביעי, 21 באפריל 2027")}'
          f'<table class="tl"><tr><th style="width:30%">מתי</th><th>מה עושים</th><th style="width:10%">✓</th></tr>{rows}</table>'
          '<h2 style="font-size:14pt;color:#173a66;margin:6mm 0 2mm">מי אחראי על מה</h2>'
          f'<table><tr><th style="width:38%">חדר</th><th>אחראי</th><th style="width:22%">עד תאריך</th><th style="width:10%">✓</th></tr>{who}</table>'
          '<p class="note">את שעת סוף אכילת חמץ ושעת שריפת החמץ בודקים בלוח הזמנים של העיר שלכם (משתנה בין ערים). '
          'לתכנון הסדר עצמו: מחשבון המצות והיין החינמי ומתכנן ליל הסדר באתר.</p><div style="flex:1"></div>'
          f'{foot(2, 2, "tichnun.netlify.app/pesach/")}</section>')
    return doc([p1, p2], "#0e6b63")


def savings():
    first = datetime.date(2027, 1, 3)  # first Sunday of 2027
    def half(a, b):
        rows = ""
        for w in range(a, b + 1):
            d = first + datetime.timedelta(weeks=w - 1)
            rows += (f'<tr><td>{w}</td><td>{d.day}.{d.month}</td><td>₪{w * 10:,}</td><td>₪{10 * w * (w + 1) // 2:,}</td>'
                     f'<td><span class="cb"></span></td></tr>')
        return f'<table><tr><th>שבוע</th><th>מתחיל</th><th>לחסוך</th><th>מצטבר</th><th>✓</th></tr>{rows}</table>'
    p1 = (f'<section class="page">{top("אתגר 52 השבועות 2027", "בשבוע 1 חוסכים ₪10, בשבוע 2 ₪20, וכך הלאה. בסוף השנה: ₪13,780.")}'
          f'<div class="wk">{half(1, 26)}{half(27, 52)}</div>'
          '<p class="note">קשה בסוף השנה? אפשר להפוך את הסדר: להתחיל מ-₪520 בינואר, כשהמוטיבציה גבוהה, ולרדת. גרסה קלה: חצי מכל סכום (סה״כ ₪6,890). '
          'כדאי להעביר את הסכום לחשבון חיסכון נפרד באותו יום.</p>'
          f'{foot(1, 2, "tichnun.netlify.app/budget-2027/")}</section>')
    rows = "".join(f'<tr><td><b>{m}</b></td><td class="l">{e(t)}</td><td></td><td></td><td><span class="cb"></span></td></tr>'
                   for m, t in zip(MONTHS, MONTH_TIPS))
    p2 = (f'<section class="page">{top("אתגר חיסכון חודשי 2027", "יעד לכל חודש, הרגל כסף אחד לכל חודש, ומקום לרשום כמה נחסך בפועל.")}'
          '<p style="font-size:12pt;margin:1mm 0 3mm">היעד שלי ל-2027: ₪__________ · בשביל: ______________________ · כל חודש: ₪__________</p>'
          f'<table class="mo"><tr><th style="width:12%">חודש</th><th>משימת החודש</th><th style="width:14%">יעד</th><th style="width:14%">נחסך</th><th style="width:7%">✓</th></tr>{rows}'
          '<tr><td><b>סה״כ</b></td><td></td><td></td><td></td><td></td></tr></table>'
          '<p class="note">רוצים שהמספרים יתחשבו לבד? מחשבון יעד החיסכון ומחשבון 50/30/20 באתר חינמיים. '
          'המשימות הן רעיונות כלליים לתכנון אישי, לא ייעוץ פיננסי.</p><div style="flex:1"></div>'
          f'{foot(2, 2, "tichnun.netlify.app/budget-2027/")}</section>')
    return doc([p1, p2], "#b7791f")


def main():
    OUT.mkdir(exist_ok=True)
    jobs = []
    for name, fn in (("pesach-cleaning-checklist-2027", cleaning), ("savings-challenge-2027", savings)):
        src = OUT / f"{name}.html"
        src.write_text(fn(), encoding="utf-8")
        jobs.append(f"{src}={OUT / (name + '.pdf')}")
    subprocess.run(["node", str(HERE.parent / "hanukkah" / "print_pdf.js"), *jobs], check=True)


if __name__ == "__main__":
    main()
