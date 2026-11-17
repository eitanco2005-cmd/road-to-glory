#!/usr/bin/env python3
"""Build the Hebrew renovation budget planner (Excel, RTL, formulas only).

Usage:  python3 products/renovation-budget/build.py
Writes renovation-budget.xlsx (blank) and renovation-budget-example.xlsx (demo data).
"""
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import CellIsRule, DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parent
FONT = "Arial"
C_PRIMARY, C_ACCENT, C_INPUT, C_FORMULA, C_HEAD = "1F4E79", "2E8B57", "FFF4CC", "EAF1FB", "1F4E79"
thin = Side(style="thin", color="C9D3DF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
ILS = '"₪"#,##0;[Red]-"₪"#,##0;"–"'
ILS0 = '"₪"#,##0;[Red]-"₪"#,##0;"₪"0'
PCT = '0%;[Red]-0%;"–"'
VAT = 0.18  # Israel standard VAT rate since 1 Jan 2025 (Israel Tax Authority)

def f(bold=False, size=11, color="222222", italic=False):
    return Font(name=FONT, bold=bold, size=size, color=color, italic=italic)

def fill(c):
    return PatternFill("solid", start_color=c, end_color=c)

def head(ws, row, col, text, width=None):
    c = ws.cell(row=row, column=col, value=text)
    c.font = f(True, 11, "FFFFFF")
    c.fill = fill(C_HEAD)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BORDER
    if width:
        ws.column_dimensions[L(col)].width = width

def cell(ws, row, col, value=None, kind="formula", fmt=None, bold=False):
    c = ws.cell(row=row, column=col, value=value)
    c.border = BORDER
    c.font = f(bold)
    if kind == "input":
        c.fill = fill(C_INPUT)
    elif kind == "formula":
        c.fill = fill(C_FORMULA)
    if fmt:
        c.number_format = fmt
    c.alignment = Alignment(vertical="center", horizontal="center" if fmt else "right")
    return c

def title(ws, text, sub=None):
    ws.sheet_view.rightToLeft = True
    ws.sheet_view.showGridLines = False
    ws["A1"] = text
    ws["A1"].font = f(True, 18, C_PRIMARY)
    ws.row_dimensions[1].height = 30
    if sub:
        ws["A2"] = sub
        ws["A2"].font = f(False, 10, "5A6B7D", italic=True)

def setup_print(ws, landscape=True):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

ROOMS = ["כל הדירה", "סלון", "מטבח", "חדר שינה הורים", "חדר ילדים 1", "חדר ילדים 2", "חדר עבודה / ממ\"ד",
         "חדר רחצה", "שירותי אורחים", "מרפסת", "מסדרון וכניסה", "מרפסת שירות", "אחר"]
TRADES = ["הריסה ופינוי", "בנייה וגבס", "אינסטלציה", "חשמל", "ריצוף וחיפוי", "איטום", "טיח ושפכטל", "צבע",
          "מטבח", "נגרות וארונות", "אלומיניום וחלונות", "דלתות", "מיזוג אוויר", "כלים סניטריים וברזים",
          "תאורה", "חומרים (קנייה עצמית)", "אדריכל / מעצב / פיקוח", "היתרים ואגרות", "הובלה ואחסון",
          "דיור חלופי", "ניקיון", "אחר"]
STATUS = ["טרם התחיל", "ממתין להצעות", "נבחר קבלן", "בביצוע", "הסתיים"]
YESNO = ["כן", "לא"]
PAYST = ["שולם", "מתוכנן"]

W_FIRST, W_N = 5, 100
W_LAST = W_FIRST + W_N - 1
Q_FIRST, Q_LAST = 5, 204
P_FIRST, P_LAST = 5, 254
S, W, Q, P = "'פרויקט'", "'עבודות'", "'הצעות מחיר'", "'תשלומים'"

DEMO_WORKS = [  # room, trade, description, estimate (incl. VAT), status
    ("כל הדירה", "הריסה ופינוי", "פירוק ריצוף ישן, קירות במטבח, פינוי פסולת", 9000, "הסתיים"),
    ("כל הדירה", "חשמל", "החלפת לוח חשמל + 12 נקודות חדשות", 18000, "בביצוע"),
    ("כל הדירה", "אינסטלציה", "החלפת צנרת מים ראשית", 15000, "הסתיים"),
    ("כל הדירה", "ריצוף וחיפוי", "ריצוף 75 מ\"ר פורצלן 80×80 כולל עבודה", 22000, "בביצוע"),
    ("כל הדירה", "צבע", "צביעת הדירה כולל תקרות", 6500, "טרם התחיל"),
    ("מטבח", "מטבח", "מטבח חדש 4.2 מ' + אי, משטח קוורץ", 45000, "נבחר קבלן"),
    ("מטבח", "כלים סניטריים וברזים", "כיור, ברז נשלף", 2500, "טרם התחיל"),
    ("חדר רחצה", "איטום", "איטום רצפה וקירות מקלחת", 3500, "הסתיים"),
    ("חדר רחצה", "ריצוף וחיפוי", "חיפוי קירות עד התקרה", 9000, "בביצוע"),
    ("חדר רחצה", "כלים סניטריים וברזים", "אסלה תלויה, ארון אמבטיה, מקלחון", 9500, "טרם התחיל"),
    ("סלון", "אלומיניום וחלונות", "חלון ויטרינה ליציאה למרפסת", 14000, "ממתין להצעות"),
    ("כל הדירה", "דלתות", "4 דלתות פנים", 8000, "ממתין להצעות"),
    ("כל הדירה", "מיזוג אוויר", "מיני מרכזי 3 כ\"ס", 16000, "נבחר קבלן"),
    ("כל הדירה", "תאורה", "גופי תאורה ותאורה שקועה", 6000, "טרם התחיל"),
    ("חדר שינה הורים", "נגרות וארונות", "ארון קיר 2.8 מ'", 11000, "ממתין להצעות"),
    ("כל הדירה", "אדריכל / מעצב / פיקוח", "מעצבת פנים – תוכנית ופיקוח עליון", 12000, "בביצוע"),
    ("כל הדירה", "ניקיון", "ניקיון סוף שיפוץ", 1500, "טרם התחיל"),
]
DEMO_QUOTES = [  # work no, contractor, price, incl VAT?, materials?, warranty, days, terms, chosen
    (2, "אבי חשמל בע\"מ", 16500, "לא", "כן", 12, 6, "30/40/30", "כן"),
    (2, "חשמלאי השרון", 21000, "כן", "כן", 24, 5, "50/50", "לא"),
    (2, "י.ש. חשמל", 17200, "כן", "לא", 12, 8, "שוטף", "לא"),
    (3, "שלום אינסטלציה", 14000, "כן", "כן", 24, 4, "50/50", "כן"),
    (3, "מים זורמים", 12900, "לא", "כן", 12, 5, "30/70", "לא"),
    (4, "רצפות הצפון", 19500, "כן", "לא", 12, 9, "שלבים", "כן"),
    (4, "קרמיקה פלוס", 23500, "כן", "כן", 24, 10, "שלבים", "לא"),
    (6, "מטבחי הגליל", 42000, "כן", "כן", 60, 21, "40/40/20", "כן"),
    (6, "קיטשן דיזיין", 48900, "כן", "כן", 60, 30, "30/60/10", "לא"),
    (6, "נגריית עמית", 39000, "לא", "כן", 24, 35, "50/50", "לא"),
    (13, "קור אוויר", 14500, "לא", "כן", 36, 2, "מלא בהתקנה", "כן"),
    (13, "אקלים פלוס", 16800, "כן", "כן", 36, 2, "מלא בהתקנה", "לא"),
    (16, "סטודיו נוי", 12000, "כן", "", 0, 0, "חודשי", "כן"),
    (1, "פינוי מהיר", 8200, "כן", "", 0, 3, "בסיום", "כן"),
    (8, "איטום ישיר", 3200, "כן", "כן", 84, 2, "בסיום", "כן"),
    (9, "רצפות הצפון", 8500, "כן", "לא", 12, 4, "שלבים", "כן"),
]
DEMO_PAYS = [  # date, work, to, amount, method, status, invoice
    (date(2027, 1, 12), 16, "סטודיו נוי", 4000, "העברה בנקאית", "שולם", "כן"),
    (date(2027, 1, 20), 1, "פינוי מהיר", 8200, "העברה בנקאית", "שולם", "כן"),
    (date(2027, 1, 22), 2, "אבי חשמל בע\"מ", 5841, "העברה בנקאית", "שולם", "כן"),
    (date(2027, 1, 25), 3, "שלום אינסטלציה", 7000, "צ'ק", "שולם", "כן"),
    (date(2027, 2, 3), 3, "שלום אינסטלציה", 7000, "צ'ק", "שולם", "כן"),
    (date(2027, 2, 5), 8, "איטום ישיר", 3200, "העברה בנקאית", "שולם", "לא"),
    (date(2027, 2, 6), 4, "ספק אריחים", 7800, "כרטיס אשראי", "שולם", "כן"),
    (date(2027, 2, 10), 6, "מטבחי הגליל", 16800, "העברה בנקאית", "שולם", "כן"),
    (date(2027, 2, 12), 16, "סטודיו נוי", 4000, "העברה בנקאית", "שולם", "כן"),
    (date(2027, 2, 18), 4, "רצפות הצפון", 9750, "העברה בנקאית", "שולם", "כן"),
    (date(2027, 2, 25), 2, "אבי חשמל בע\"מ", 7788, "העברה בנקאית", "מתוכנן", "לא"),
    (date(2027, 3, 5), 6, "מטבחי הגליל", 16800, "העברה בנקאית", "מתוכנן", "לא"),
    (date(2027, 3, 8), 13, "קור אוויר", 17110, "כרטיס אשראי", "מתוכנן", "לא"),
    (date(2027, 3, 10), 4, "רצפות הצפון", 9750, "העברה בנקאית", "מתוכנן", "לא"),
    (date(2027, 3, 12), 16, "סטודיו נוי", 4000, "העברה בנקאית", "מתוכנן", "לא"),
    (date(2027, 3, 20), 6, "מטבחי הגליל", 8400, "העברה בנקאית", "מתוכנן", "לא"),
]


def build(demo: bool, path: Path):
    wb = Workbook()
    wb.remove(wb.active)

    # ================= הוראות =================
    ws = wb.create_sheet("הוראות")
    title(ws, "מתכנן תקציב שיפוץ", "Glory · אקסל בעברית לניהול שיפוץ: עבודות, השוואת הצעות מחיר, תשלומים ובלת\"מ")
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 112
    lines = [
        ("איך מתחילים", True),
        ("1. «פרויקט»: שם, תאריך התחלה, התקציב המקסימלי שלכם ואחוז הבלת\"מ (ברירת מחדל 15%).", False),
        ("2. «עבודות»: שורה לכל עבודה – חדר, תחום, תיאור ואומדן ראשוני (כולל מע\"מ). כל עבודה מקבלת מספר קבוע (עמודה א').", False),
        ("3. «הצעות מחיר»: לכל עבודה רשמו את ההצעות שקיבלתם, עם מספר העבודה. סמנו אם המחיר כולל מע\"מ – הקובץ מוסיף 18% כשצריך,", False),
        ("   מסמן את ההצעה הזולה ביותר ומראה את הפער. כשבוחרים קבלן, כתבו «כן» בעמודה «נבחרה?».", False),
        ("4. «תשלומים»: כל תשלום (לקבלן, לספק, בחנות) עם מספר העבודה. «מתוכנן» = תשלום עתידי לפי הסכם, «שולם» = יצא מהחשבון.", False),
        ("5. «דשבורד»: כמה התחייבתם, כמה שולם, כמה נשאר, מה מצב הבלת\"מ ותזרים התשלומים לפי חודש.", False),
        ("", False),
        ("איך מחושב התקציב של כל עבודה", True),
        ("אם נבחרה הצעת מחיר – התקציב הוא סכום ההצעה כולל מע\"מ. אם עדיין לא – האומדן הראשוני שלכם. כך התמונה מתעדכנת ככל שמתקדמים.", False),
        ("", False),
        ("למה בלת\"מ (בלתי צפוי מראש)?", True),
        ("כמעט בכל שיפוץ מתגלים דברים אחרי שפותחים קירות ורצפות: צנרת רקובה, חשמל ישן, רטיבות. מקובל לשמור 10%–20% מהתקציב בצד.", False),
        ("הקובץ מחשב כמה בלת\"מ נשאר אחרי ההתחייבויות, ומתריע באדום כשנגעתם בו.", False),
        ("", False),
        ("צבעים", True),
        ("צהוב = מקלידים.   כחול בהיר = נוסחה.   אדום = חריגה / תשומת לב.", False),
        ("", False),
        ("לפני שחותמים עם קבלן", True),
        ("השתמשו ברשימת הבדיקה (קובץ ה-Word המצורף): הצעה כתובה ומפורטת, מה כלול ומה לא, לוח תשלומים לפי שלבים, אחריות ותאריכים.", False),
        ("Google Sheets: העלו את הקובץ ל-Google Drive ← «פתיחה באמצעות Google Sheets». הנוסחאות, הרשימות והגרפים עוברים.", False),
        ("", False),
        ("הבהרה", True),
        ("הקובץ הוא כלי תכנון בלבד. המחירים בדוגמה הם להמחשה ואינם הצעת מחיר. מע\"מ 18% – שיעור המע\"מ בישראל מ-1.1.2025 (רשות המסים).", False),
        ("אין בקובץ ייעוץ משפטי, הנדסי או מס. בעבודות מבניות, גז וחשמל ראשי – עבדו רק עם בעלי רישיון מתאים.", False),
    ]
    for i, (t, bold) in enumerate(lines, start=4):
        c = ws.cell(row=i, column=2, value=t)
        c.font = f(bold, 13 if bold else 11, C_PRIMARY if bold else "222222")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    setup_print(ws, False)

    # ================= פרויקט =================
    ws = wb.create_sheet("פרויקט")
    title(ws, "פרטי הפרויקט", "ממלאים פעם אחת")
    for col, w in zip("ABCD", [34, 22, 4, 60]):
        ws.column_dimensions[col].width = w
    rows = [
        ("שם הפרויקט", "שיפוץ דירה – רח' הגפן" if demo else "", None, ""),
        ("תאריך התחלה", date(2027, 1, 10) if demo else None, "dd/mm/yyyy", "משמש לתזרים התשלומים בדשבורד."),
        ("תאריך סיום מתוכנן", date(2027, 4, 30) if demo else None, "dd/mm/yyyy", ""),
        ("תקציב מקסימלי (כולל מע\"מ)", 230000 if demo else 0, ILS0, "הסכום שאתם לא רוצים לעבור בשום מקרה."),
        ("בלת\"מ – אחוז מהתקציב", 0.15, "0%", "מקובל 10%–20%. בבית ישן – כדאי יותר."),
        ("שיעור מע\"מ", VAT, "0%", "18% מ-1.1.2025 (רשות המסים). אם ישתנה – עדכנו כאן."),
    ]
    for i, (k, v, fmt, note) in enumerate(rows, start=4):
        ws.cell(row=i, column=1, value=k).font = f(True)
        cell(ws, i, 2, v, "input", fmt)
        ws.cell(row=i, column=4, value=note).font = f(False, 10, "5A6B7D")
    ws.cell(row=11, column=1, value="סכום הבלת\"מ").font = f(True)
    cell(ws, 11, 2, "=B7*B8", "formula", ILS0, True)
    ws.cell(row=12, column=1, value="תקציב לעבודות (בלי בלת\"מ)").font = f(True)
    cell(ws, 12, 2, "=B7-B11", "formula", ILS0, True)
    lists = [("חדרים", ROOMS, 1), ("תחומי עבודה", TRADES, 2), ("סטטוס", STATUS, 4), ("כן/לא", YESNO, 5), ("מצב תשלום", PAYST, 6)]
    base = 15
    ws.cell(row=base - 1, column=1, value="רשימות (אפשר לשנות ולהוסיף בשורות הריקות)").font = f(True, 12, C_PRIMARY)
    for j, (name, items, col) in enumerate(lists):
        colL = ["A", "B", "D", "E", "F"][j]
        c = ws[f"{colL}{base}"]
        c.value = name
        c.font = f(True, 11, "FFFFFF")
        c.fill = fill(C_HEAD)
        for i in range(30):
            cc = ws[f"{colL}{base + 1 + i}"]
            cc.value = items[i] if i < len(items) else None
            cc.fill = fill(C_INPUT)
            cc.border = BORDER
    ws.column_dimensions["E"].width = 12
    ws.column_dimensions["F"].width = 12
    ws.column_dimensions["D"].width = 60
    LR = (base + 1, base + 30)
    wb.defined_names["VAT"] = DefinedName("VAT", attr_text=f"{S}!$B$9")
    setup_print(ws, False)

    def dv_list(ws, colL, rng):
        dv = DataValidation(type="list", formula1=f"={S}!${colL}${LR[0]}:${colL}${LR[1]}", allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(rng)
        return dv

    # ================= עבודות =================
    ws = wb.create_sheet("עבודות")
    title(ws, "עבודות ותקציב לפי חדר", "שורה לכל עבודה. המספר בעמודה א' משמש לקישור הצעות מחיר ותשלומים.")
    hdr = [("מס'", 6), ("חדר", 16), ("תחום", 20), ("תיאור העבודה", 40), ("אומדן ראשוני (כולל מע\"מ)", 15),
           ("הצעה שנבחרה (כולל מע\"מ)", 15), ("תקציב קובע", 14), ("שולם", 13), ("נותר לשלם", 13),
           ("% שולם", 10), ("סטטוס", 14), ("הצעות שהתקבלו", 10), ("הערות", 30)]
    for j, (h, w) in enumerate(hdr, start=1):
        head(ws, 4, j, h, w)
    ws.row_dimensions[4].height = 34
    for i in range(W_N):
        r = W_FIRST + i
        d = DEMO_WORKS[i] if (demo and i < len(DEMO_WORKS)) else (None,) * 5
        cell(ws, r, 1, i + 1, "formula", "0", True)
        cell(ws, r, 2, d[0], "input")
        cell(ws, r, 3, d[1], "input")
        cell(ws, r, 4, d[2], "input")
        cell(ws, r, 5, d[3], "input", ILS)
        cell(ws, r, 6, f"=SUMIFS({Q}!$G${Q_FIRST}:$G${Q_LAST},{Q}!$A${Q_FIRST}:$A${Q_LAST},A{r},{Q}!$K${Q_FIRST}:$K${Q_LAST},\"כן\")", "formula", ILS)
        cell(ws, r, 7, f"=IF(N(F{r})>0,F{r},N(E{r}))", "formula", ILS, True)
        cell(ws, r, 8, f"=SUMIFS({P}!$E${P_FIRST}:$E${P_LAST},{P}!$B${P_FIRST}:$B${P_LAST},A{r},{P}!$G${P_FIRST}:$G${P_LAST},\"שולם\")", "formula", ILS)
        cell(ws, r, 9, f"=G{r}-H{r}", "formula", ILS)
        cell(ws, r, 10, f"=IF(N(G{r})=0,\"\",H{r}/G{r})", "formula", "0%")
        cell(ws, r, 11, d[4], "input")
        cell(ws, r, 12, f"=IF(D{r}&B{r}=\"\",\"\",COUNTIF({Q}!$A${Q_FIRST}:$A${Q_LAST},A{r}))", "formula", "0")
        cell(ws, r, 13, None, "input")
    dv_list(ws, "A", f"B{W_FIRST}:B{W_LAST}")
    dv_list(ws, "B", f"C{W_FIRST}:C{W_LAST}")
    dv_list(ws, "D", f"K{W_FIRST}:K{W_LAST}")
    ws.conditional_formatting.add(f"I{W_FIRST}:I{W_LAST}", CellIsRule(operator="lessThan", formula=["0"], fill=fill("F8D7DA")))
    ws.conditional_formatting.add(f"J{W_FIRST}:J{W_LAST}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="2E8B57"))
    ws.conditional_formatting.add(f"F{W_FIRST}:F{W_LAST}", FormulaRule(formula=[f"AND(N(F{W_FIRST})>0,N(E{W_FIRST})>0,F{W_FIRST}>E{W_FIRST}*1.1)"], fill=fill("FCE4D6")))
    tr = W_LAST + 2
    ws.cell(row=tr, column=4, value="סה\"כ").font = f(True)
    for col in (5, 6, 7, 8, 9):
        cl = L(col)
        cell(ws, tr, col, f"=SUM({cl}{W_FIRST}:{cl}{W_LAST})", "formula", ILS, True)
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = f"A4:M{W_LAST}"
    setup_print(ws)

    # ================= הצעות מחיר =================
    ws = wb.create_sheet("הצעות מחיר")
    title(ws, "השוואת הצעות מחיר", "כל הצעה בשורה, עם מספר העבודה מגיליון «עבודות». הזולה ביותר לכל עבודה מסומנת בירוק.")
    hdr = [("מס' עבודה", 9), ("העבודה", 34), ("קבלן / ספק", 22), ("מחיר בהצעה", 13), ("המחיר כולל מע\"מ?", 10),
           ("כולל חומרים?", 10), ("מחיר כולל מע\"מ", 14), ("אחריות (חודשים)", 10), ("משך (ימי עבודה)", 10),
           ("תנאי תשלום", 14), ("נבחרה?", 9), ("פער מהזולה", 13), ("הערות", 28)]
    for j, (h, w) in enumerate(hdr, start=1):
        head(ws, 4, j, h, w)
    ws.row_dimensions[4].height = 34
    for i, r in enumerate(range(Q_FIRST, Q_LAST + 1)):
        d = DEMO_QUOTES[i] if (demo and i < len(DEMO_QUOTES)) else (None,) * 9
        cell(ws, r, 1, d[0], "input", "0")
        cell(ws, r, 2, f"=IF(A{r}=\"\",\"\",IFERROR(INDEX({W}!$C${W_FIRST}:$C${W_LAST},A{r})&\" – \"&INDEX({W}!$D${W_FIRST}:$D${W_LAST},A{r}),\"מספר עבודה לא קיים\"))", "formula")
        cell(ws, r, 3, d[1], "input")
        cell(ws, r, 4, d[2], "input", ILS)
        cell(ws, r, 5, d[3], "input")
        cell(ws, r, 6, d[4] or None, "input")
        cell(ws, r, 7, f"=IF(N(D{r})=0,\"\",IF(E{r}=\"לא\",D{r}*(1+VAT),D{r}))", "formula", ILS, True)
        cell(ws, r, 8, d[5] if d[5] else None, "input", "0")
        cell(ws, r, 9, d[6] if d[6] else None, "input", "0")
        cell(ws, r, 10, d[7], "input")
        cell(ws, r, 11, d[8], "input")
        cell(ws, r, 12, f"=IF(G{r}=\"\",\"\",G{r}-_xlfn.MINIFS($G${Q_FIRST}:$G${Q_LAST},$A${Q_FIRST}:$A${Q_LAST},A{r}))", "formula", ILS)
        cell(ws, r, 13, None, "input")
    dv_yn = DataValidation(type="list", formula1=f"={S}!$E${LR[0]}:$E${LR[1]}", allow_blank=True)
    ws.add_data_validation(dv_yn)
    for colL in "EFK":
        dv_yn.add(f"{colL}{Q_FIRST}:{colL}{Q_LAST}")
    dv_id = DataValidation(type="whole", operator="between", formula1="1", formula2=str(W_N), allow_blank=True,
                           error="רשמו את מספר העבודה מגיליון «עבודות» (1–100)", errorTitle="מספר עבודה")
    ws.add_data_validation(dv_id)
    dv_id.add(f"A{Q_FIRST}:A{Q_LAST}")
    ws.conditional_formatting.add(f"A{Q_FIRST}:M{Q_LAST}", FormulaRule(formula=[f'$K{Q_FIRST}="כן"'], fill=fill("D9EAD3"), font=Font(bold=True)))
    ws.conditional_formatting.add(f"L{Q_FIRST}:L{Q_LAST}", FormulaRule(formula=[f'AND($G{Q_FIRST}<>"",$L{Q_FIRST}=0)'], fill=fill("B6D7A8")))
    ws.conditional_formatting.add(f"B{Q_FIRST}:B{Q_LAST}", FormulaRule(formula=[f'$B{Q_FIRST}="מספר עבודה לא קיים"'], fill=fill("F8D7DA")))
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = f"A4:M{Q_LAST}"
    ws.cell(row=Q_LAST + 2, column=2, value="פער מהזולה = 0 → זו ההצעה הזולה לעבודה הזאת. זול יותר לא תמיד עדיף: השוו גם אחריות, חומרים ולוח זמנים.").font = f(False, 10, "5A6B7D", True)
    setup_print(ws)

    # ================= תשלומים =================
    ws = wb.create_sheet("תשלומים")
    title(ws, "תשלומים", "כל תשלום עם מספר העבודה. «מתוכנן» = לפי לוח התשלומים בהסכם, «שולם» = כבר יצא.")
    hdr = [("תאריך", 12), ("מס' עבודה", 9), ("העבודה", 34), ("שולם ל-", 22), ("סכום (כולל מע\"מ)", 14),
           ("אמצעי תשלום", 15), ("מצב", 10), ("חשבונית/קבלה התקבלה?", 12), ("הערות", 28)]
    for j, (h, w) in enumerate(hdr, start=1):
        head(ws, 4, j, h, w)
    ws.row_dimensions[4].height = 34
    for i, r in enumerate(range(P_FIRST, P_LAST + 1)):
        d = DEMO_PAYS[i] if (demo and i < len(DEMO_PAYS)) else (None,) * 7
        cell(ws, r, 1, d[0], "input", "dd/mm/yyyy")
        cell(ws, r, 2, d[1], "input", "0")
        cell(ws, r, 3, f"=IF(B{r}=\"\",\"\",IFERROR(INDEX({W}!$C${W_FIRST}:$C${W_LAST},B{r})&\" – \"&INDEX({W}!$D${W_FIRST}:$D${W_LAST},B{r}),\"מספר עבודה לא קיים\"))", "formula")
        cell(ws, r, 4, d[2], "input")
        cell(ws, r, 5, d[3], "input", ILS)
        cell(ws, r, 6, d[4], "input")
        cell(ws, r, 7, d[5], "input")
        cell(ws, r, 8, d[6], "input")
        cell(ws, r, 9, None, "input")
    dv_ps = DataValidation(type="list", formula1=f"={S}!$F${LR[0]}:$F${LR[1]}", allow_blank=True)
    dv_yn2 = DataValidation(type="list", formula1=f"={S}!$E${LR[0]}:$E${LR[1]}", allow_blank=True)
    dv_pm = DataValidation(type="list", formula1='"העברה בנקאית,צ\'ק,כרטיס אשראי,מזומן,ביט / פייבוקס"', allow_blank=True, showErrorMessage=False)
    dv_id2 = DataValidation(type="whole", operator="between", formula1="1", formula2=str(W_N), allow_blank=True,
                            error="רשמו את מספר העבודה מגיליון «עבודות» (1–100)", errorTitle="מספר עבודה")
    for dv in (dv_ps, dv_yn2, dv_pm, dv_id2):
        ws.add_data_validation(dv)
    dv_ps.add(f"G{P_FIRST}:G{P_LAST}")
    dv_yn2.add(f"H{P_FIRST}:H{P_LAST}")
    dv_pm.add(f"F{P_FIRST}:F{P_LAST}")
    dv_id2.add(f"B{P_FIRST}:B{P_LAST}")
    ws.conditional_formatting.add(f"A{P_FIRST}:I{P_LAST}", FormulaRule(formula=[f'$G{P_FIRST}="מתוכנן"'], font=Font(color="7F7F7F", italic=True)))
    ws.conditional_formatting.add(f"H{P_FIRST}:H{P_LAST}", FormulaRule(formula=[f'AND($G{P_FIRST}="שולם",$H{P_FIRST}<>"כן")'], fill=fill("FCE4D6")))
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:I{P_LAST}"
    setup_print(ws)

    # ================= דשבורד =================
    ws = wb.create_sheet("דשבורד", 1)
    title(ws, "דשבורד שיפוץ")
    ws["A1"] = f"=\"דשבורד שיפוץ\"&IF({S}!B4=\"\",\"\",\" · \"&{S}!B4)"
    for col, w in zip("ABCDEFGHIJ", [38, 30, 14, 22, 14, 14, 14, 4, 16, 14]):
        ws.column_dimensions[col].width = w
    head(ws, 3, 1, "מצב התקציב")
    head(ws, 3, 2, "סכום")
    k = [
        ("תקציב מקסימלי", f"={S}!B7"),
        ("מתוכנן לעבודות (תקציב קובע)", f"={W}!G{tr}"),
        ("מתוכו: התחייבויות (הצעות שנבחרו)", f"={W}!F{tr}"),
        ("שולם עד היום", f"={W}!H{tr}"),
        ("נותר לשלם על עבודות", f"=B5-B7"),
        ("בלת\"מ שהוגדר", f"={S}!B11"),
        ("מרווח שנשאר (תקציב פחות מתוכנן)", "=B4-B5"),
        ("מצב הבלת\"מ", "=IF(B10>=B9,\"הבלת\"\"מ שלם ✓\",IF(B10>=0,\"נגעתם בבלת\"\"מ – נשאר \"&TEXT(B10,\"#,##0\")&\" ₪\",\"חריגה מהתקציב!\"))"),
        ("% מהעבודות שהסתיימו", f"=IFERROR(COUNTIF({W}!K{W_FIRST}:K{W_LAST},\"הסתיים\")/COUNTIF({W}!D{W_FIRST}:D{W_LAST},\"?*\"),\"\")"),
        ("תשלומים מתוכננים שטרם שולמו", f"=SUMIFS({P}!E{P_FIRST}:E{P_LAST},{P}!G{P_FIRST}:G{P_LAST},\"מתוכנן\")"),
        ("תשלומים בלי חשבונית/קבלה", f"=COUNTIFS({P}!G{P_FIRST}:G{P_LAST},\"שולם\",{P}!H{P_FIRST}:H{P_LAST},\"<>כן\")"),
    ]
    for i, (lab, frm) in enumerate(k):
        r = 4 + i
        cell(ws, r, 1, lab, None).font = f(True)
        fmt = PCT if "%" in lab else ("0" if "בלי חשבונית" in lab else (None if "מצב" in lab else ILS))
        cell(ws, r, 2, frm, "formula", fmt, True)
    ws.conditional_formatting.add("B10", CellIsRule(operator="lessThan", formula=["B9"], fill=fill("F8D7DA")))
    ws.conditional_formatting.add("B11", FormulaRule(formula=['NOT(ISNUMBER(SEARCH("שלם",B11)))'], fill=fill("F8D7DA")))
    ws.conditional_formatting.add("B12", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="2E8B57"))

    # by room
    head(ws, 3, 4, "חדר")
    head(ws, 3, 5, "מתוכנן")
    head(ws, 3, 6, "שולם")
    head(ws, 3, 7, "נותר")
    for i in range(len(ROOMS)):
        r = 4 + i
        cell(ws, r, 4, f"=IF({S}!A{LR[0] + i}=\"\",\"\",{S}!A{LR[0] + i})", None).font = f(True)
        cell(ws, r, 5, f"=IF(D{r}=\"\",\"\",SUMIFS({W}!$G${W_FIRST}:$G${W_LAST},{W}!$B${W_FIRST}:$B${W_LAST},D{r}))", "formula", ILS)
        cell(ws, r, 6, f"=IF(D{r}=\"\",\"\",SUMIFS({W}!$H${W_FIRST}:$H${W_LAST},{W}!$B${W_FIRST}:$B${W_LAST},D{r}))", "formula", ILS)
        cell(ws, r, 7, f"=IF(D{r}=\"\",\"\",E{r}-F{r})", "formula", ILS)
    room_last = 4 + len(ROOMS) - 1

    # by trade
    t0 = 20
    head(ws, t0, 4, "תחום")
    head(ws, t0, 5, "מתוכנן")
    head(ws, t0, 6, "שולם")
    head(ws, t0, 7, "% מהתקציב")
    for i in range(len(TRADES)):
        r = t0 + 1 + i
        cell(ws, r, 4, f"=IF({S}!B{LR[0] + i}=\"\",\"\",{S}!B{LR[0] + i})", None).font = f(True)
        cell(ws, r, 5, f"=IF(D{r}=\"\",\"\",SUMIFS({W}!$G${W_FIRST}:$G${W_LAST},{W}!$C${W_FIRST}:$C${W_LAST},D{r}))", "formula", ILS)
        cell(ws, r, 6, f"=IF(D{r}=\"\",\"\",SUMIFS({W}!$H${W_FIRST}:$H${W_LAST},{W}!$C${W_FIRST}:$C${W_LAST},D{r}))", "formula", ILS)
        cell(ws, r, 7, f"=IF(OR(D{r}=\"\",N($B$5)=0),\"\",E{r}/$B$5)", "formula", PCT)
    trade_last = t0 + len(TRADES)

    # cash flow by month (12 months from start)
    c0 = 17
    head(ws, c0, 1, "חודש")
    head(ws, c0, 2, "שולם")
    head(ws, c0, 3, "מתוכנן")
    for m in range(12):
        r = c0 + 1 + m
        cell(ws, r, 1, f"=IF({S}!$B$5=\"\",\"\",EDATE(DATE(YEAR({S}!$B$5),MONTH({S}!$B$5),1),{m}))", "formula", "mm/yyyy")
        rng = (f"{P}!$E${P_FIRST}:$E${P_LAST},{P}!$A${P_FIRST}:$A${P_LAST},\">=\"&A{r},{P}!$A${P_FIRST}:$A${P_LAST},\"<\"&EDATE(A{r},1)")
        cell(ws, r, 2, f"=IF(A{r}=\"\",0,SUMIFS({rng},{P}!$G${P_FIRST}:$G${P_LAST},\"שולם\"))", "formula", ILS)
        cell(ws, r, 3, f"=IF(A{r}=\"\",0,SUMIFS({rng},{P}!$G${P_FIRST}:$G${P_LAST},\"מתוכנן\"))", "formula", ILS)
    ws.cell(row=c0 - 1, column=1, value="תזרים תשלומים (12 חודשים מתאריך ההתחלה)").font = f(True, 12, C_PRIMARY)

    ch = PieChart()
    ch.title = "התקציב לפי תחום"
    ch.add_data(Reference(ws, min_col=5, min_row=t0, max_row=trade_last), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=4, min_row=t0 + 1, max_row=trade_last))
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showPercent = True
    for a in ("showVal", "showCatName", "showSerName", "showLegendKey", "showLeaderLines"):
        setattr(ch.dataLabels, a, False)
    ch.height, ch.width = 10, 14
    ws.add_chart(ch, "K20")

    c2 = BarChart()
    c2.type = "col"
    c2.title = "לפי חדר: מתוכנן מול שולם"
    c2.add_data(Reference(ws, min_col=5, max_col=6, min_row=3, max_row=room_last), titles_from_data=True)
    c2.set_categories(Reference(ws, min_col=4, min_row=4, max_row=room_last))
    c2.height, c2.width = 9, 18
    ws.add_chart(c2, "K2")

    c3 = BarChart()
    c3.type = "col"
    c3.grouping = "stacked"
    c3.overlap = 100
    c3.title = "תזרים: שולם ומתוכנן לפי חודש"
    c3.add_data(Reference(ws, min_col=2, min_row=c0, max_row=c0 + 12), titles_from_data=True)
    c3.add_data(Reference(ws, min_col=3, min_row=c0, max_row=c0 + 12), titles_from_data=True)
    c3.set_categories(Reference(ws, min_col=1, min_row=c0 + 1, max_row=c0 + 12))
    c3.height, c3.width = 8, 16
    ws.add_chart(c3, "K40")
    setup_print(ws)

    # ================= קבלנים =================
    ws = wb.create_sheet("קבלנים")
    title(ws, "אנשי מקצוע וספקים", "טלפונים, רישיונות וביטוח – הכול במקום אחד")
    hdr = [("שם", 22), ("תחום", 18), ("טלפון", 14), ("אימייל", 24), ("מס' רישום / רישיון", 16),
           ("ביטוח צד ג' בתוקף?", 12), ("מי המליץ", 16), ("הערות", 34)]
    for j, (h, w) in enumerate(hdr, start=1):
        head(ws, 4, j, h, w)
    for r in range(5, 45):
        for c in range(1, 9):
            cell(ws, r, c, None, "input")
    dv_list(ws, "B", "B5:B44")
    dv_yn3 = DataValidation(type="list", formula1=f"={S}!$E${LR[0]}:$E${LR[1]}", allow_blank=True)
    ws.add_data_validation(dv_yn3)
    dv_yn3.add("F5:F44")
    ws.cell(row=46, column=1, value="קבלן רשום אפשר לבדוק באתר פנקס הקבלנים של רשם הקבלנים (gov.il). חשמלאי – רישיון חשמלאי ממשרד האנרגיה.").font = f(False, 10, "5A6B7D", True)
    setup_print(ws)

    order = ["הוראות", "דשבורד", "פרויקט", "עבודות", "הצעות מחיר", "תשלומים", "קבלנים"]
    wb._sheets = [wb[n] for n in order]
    for n, c in zip(order, ["7F7F7F", C_ACCENT, "C9A227", "C9A227", "C9A227", "C9A227", C_PRIMARY]):
        wb[n].sheet_properties.tabColor = c
    wb.active = 1 if demo else 0
    wb.properties.title = "מתכנן תקציב שיפוץ"
    wb.properties.creator = "Glory"
    wb.calculation.fullCalcOnLoad = True
    wb.save(path)


if __name__ == "__main__":
    build(False, OUT / "renovation-budget.xlsx")
    build(True, OUT / "renovation-budget-example.xlsx")
    print("built")
