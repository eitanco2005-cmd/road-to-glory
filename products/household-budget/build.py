#!/usr/bin/env python3
"""Build the Hebrew household budget Pro workbook (Excel, RTL, formulas only).

Usage:  python3 products/household-budget/build.py
Writes, for each year in YEARS: a blank workbook and an example workbook with demo data.
"""
import random
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import CellIsRule, DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parent
YEARS = [2027, 2026]

# ---------- style ----------
FONT = "Arial"
C_PRIMARY = "1F4E79"
C_ACCENT = "2E8B57"
C_INPUT = "FFF4CC"     # yellow = you type here
C_FORMULA = "EAF1FB"   # light blue = calculated
C_HEAD = "1F4E79"
C_GROUP = "DDE7F3"
thin = Side(style="thin", color="C9D3DF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
ILS = '"₪"#,##0;[Red]-"₪"#,##0;"–"'
ILS0 = '"₪"#,##0;[Red]-"₪"#,##0;"₪"0'
PCT = '0%;[Red]-0%;"–"'
MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]

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
    return c

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
    c.alignment = Alignment(vertical="center", horizontal="right" if not fmt else "center")
    return c

def title(ws, text, sub=None, span=8):
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
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = ws.page_margins.right = 0.4

# ---------- categories (Israeli household) ----------
# (group, category, type, 50/30/20 class, default monthly)
INC, EXP = "הכנסה", "הוצאה"
NEED, WANT, SAVE = "צורך (50%)", "רצון (30%)", "חיסכון וחובות (20%)"
CATS = [
    ("הכנסות", "משכורת נטו – בן/בת זוג 1", INC, "", 12500),
    ("הכנסות", "משכורת נטו – בן/בת זוג 2", INC, "", 9500),
    ("הכנסות", "קצבת ילדים (ביטוח לאומי)", INC, "", 340),
    ("הכנסות", "הכנסה מעסק / עבודה נוספת", INC, "", 0),
    ("הכנסות", "שכר דירה שמתקבל", INC, "", 0),
    ("הכנסות", "החזרי מס / מענקים", INC, "", 0),
    ("הכנסות", "הכנסה אחרת", INC, "", 0),
    ("דיור", "משכנתא / שכר דירה", EXP, NEED, 5200),
    ("דיור", "ארנונה", EXP, NEED, 520),
    ("דיור", "ועד בית", EXP, NEED, 180),
    ("דיור", "חשמל", EXP, NEED, 450),
    ("דיור", "מים וביוב", EXP, NEED, 180),
    ("דיור", "גז", EXP, NEED, 70),
    ("דיור", "אחזקה ותיקונים בבית", EXP, NEED, 150),
    ("תקשורת", "אינטרנט וטלוויזיה", EXP, NEED, 180),
    ("תקשורת", "טלפונים ניידים", EXP, NEED, 120),
    ("ביטוחים ובריאות", "קופת חולים – ביטוח משלים", EXP, NEED, 160),
    ("ביטוחים ובריאות", "ביטוח בריאות פרטי", EXP, NEED, 150),
    ("ביטוחים ובריאות", "ביטוח חיים / משכנתא", EXP, NEED, 120),
    ("ביטוחים ובריאות", "ביטוח דירה ומבנה", EXP, NEED, 70),
    ("ביטוחים ובריאות", "ביטוח לאומי (עצמאי / לא עובד)", EXP, NEED, 0),
    ("ביטוחים ובריאות", "תרופות ורופאים", EXP, NEED, 150),
    ("ביטוחים ובריאות", "רופא שיניים ואופטיקה", EXP, NEED, 120),
    ("רכב ותחבורה", "דלק / טעינה", EXP, NEED, 700),
    ("רכב ותחבורה", "ביטוח רכב (חובה + מקיף)", EXP, NEED, 400),
    ("רכב ותחבורה", "טיפולים ותיקונים", EXP, NEED, 250),
    ("רכב ותחבורה", "רישיון רכב (אגרה) וטסט", EXP, NEED, 120),
    ("רכב ותחבורה", "חניה וכבישי אגרה", EXP, WANT, 100),
    ("רכב ותחבורה", "תחבורה ציבורית / רב-קו", EXP, NEED, 100),
    ("מזון ובית", "סופרמרקט", EXP, NEED, 3200),
    ("מזון ובית", "שוק, ירקות ומאפייה", EXP, NEED, 400),
    ("מזון ובית", "פארם וטואלטיקה", EXP, NEED, 250),
    ("מזון ובית", "אוכל בחוץ ומשלוחים", EXP, WANT, 600),
    ("ילדים", "גן / מעון / צהרון", EXP, NEED, 1800),
    ("ילדים", "חוגים ותנועות נוער", EXP, WANT, 400),
    ("ילדים", "תשלומי הורים וציוד לבית הספר", EXP, NEED, 150),
    ("ילדים", "ביגוד והנעלה לילדים", EXP, NEED, 200),
    ("ילדים", "בייביסיטר ודמי כיס", EXP, WANT, 150),
    ("פנאי ואישי", "בילויים ותרבות", EXP, WANT, 300),
    ("פנאי ואישי", "מנויים (סטרימינג, אפליקציות, חדר כושר)", EXP, WANT, 200),
    ("פנאי ואישי", "ביגוד והנעלה למבוגרים", EXP, WANT, 300),
    ("פנאי ואישי", "טיפוח ומספרה", EXP, WANT, 150),
    ("פנאי ואישי", "חופשות וטיולים", EXP, WANT, 700),
    ("פנאי ואישי", "חיות מחמד", EXP, WANT, 0),
    ("חגים ואירועים", "מתנות לשמחות (חתונות, בר/בת מצווה)", EXP, WANT, 350),
    ("חגים ואירועים", "חגים ומתנות למשפחה", EXP, WANT, 250),
    ("חגים ואירועים", "תרומות", EXP, WANT, 50),
    ("בנק ופיננסים", "עמלות בנק ודמי כרטיס", EXP, NEED, 30),
    ("חיסכון", "קרן חירום", EXP, SAVE, 800),
    ("חיסכון", "חיסכון לכל ילד / חיסכון לילדים", EXP, SAVE, 100),
    ("חיסכון", "השקעות / קרן השתלמות עצמאית", EXP, SAVE, 500),
    ("חיסכון", "חיסכון למטרה (רכב, חופשה, שיפוץ)", EXP, SAVE, 400),
    ("חובות", "החזר הלוואה", EXP, SAVE, 0),
    ("חובות", "החזר כרטיס אשראי / מינוס", EXP, SAVE, 0),
    ("שונות", "הוצאות לא צפויות", EXP, NEED, 300),
    ("שונות", "אחר", EXP, WANT, 0),
]
GROUPS = []
for g, *_ in CATS:
    if g not in GROUPS:
        GROUPS.append(g)

FIRST = 5
NROWS = 90                      # category rows 5..94 (room to add your own)
LAST = FIRST + NROWS - 1
TX_FIRST, TX_LAST = 5, 2004     # 2,000 transaction rows
B = "'תקציב'"
T = "'תנועות'"
Y = "'שנתי'"
S = "'הגדרות'"


def build(year: int, demo: bool, path: Path):
    wb = Workbook()
    wb.remove(wb.active)
    random.seed(year)

    # ================= הוראות =================
    ws = wb.create_sheet("הוראות")
    title(ws, f"תקציב משק בית Pro {year}", "Glory · קובץ אקסל בעברית לתכנון ומעקב אחרי ההוצאות וההכנסות של הבית")
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 110
    lines = [
        ("איך מתחילים (10 דקות)", True),
        ("1. בגיליון «הגדרות» רשמו את שנת התקציב, שם המשפחה ויתרת הפתיחה בחשבון העו\"ש.", False),
        ("2. בגיליון «תקציב» עברו על הקטגוריות ורשמו בעמודה הצהובה «סכום חודשי מתוכנן» כמה אתם מתכננים להכניס/להוציא בכל חודש.", False),
        ("   הסכום מועתק אוטומטית לכל 12 החודשים. חודש חריג (למשל ארנונה דו-חודשית או חופשה בקיץ)? פשוט כתבו סכום אחר בחודש הזה.", False),
        ("   אפשר לשנות שמות קטגוריות ולהוסיף שורות חדשות בשורות הריקות בתחתית הטבלה. הקפידו לבחור «סוג» (הכנסה/הוצאה) וסיווג 50/30/20.", False),
        ("3. בגיליון «תנועות» רשמו כל הוצאה או הכנסה: תאריך, קטגוריה (מתוך רשימה נפתחת), סכום. אפשר גם שורה אחת לכל קטגוריה בסוף החודש מתוך דף האשראי.", False),
        ("4. זהו. הגיליונות «חודשי», «שנתי» ו«דשבורד» מתעדכנים לבד.", False),
        ("", False),
        ("מה יש בכל גיליון", True),
        ("הגדרות – שנה, שם, יתרת פתיחה ויעד חיסכון חודשי.", False),
        ("תקציב – כל הקטגוריות הישראליות (ארנונה, ועד בית, קופת חולים, ביטוח לאומי, גן/צהרון ועוד) עם תכנון לכל חודש.", False),
        ("תנועות – יומן ההוצאות וההכנסות (2,000 שורות). העמודות הכחולות מחושבות אוטומטית.", False),
        ("חודשי – בוחרים חודש מהרשימה ורואים מתוכנן מול בפועל לכל קטגוריה, כולל התראה באדום על חריגה.", False),
        ("שנתי – כל הקטגוריות × 12 חודשים, סה\"כ הכנסות, הוצאות, חיסכון ויתרה מצטברת.", False),
        ("דשבורד – תמונת מצב: גרפים של הכנסות מול הוצאות, התפלגות לפי קבוצות, ובדיקת 50/30/20.", False),
        ("יעדי חיסכון – כמה צריך לשים בצד כל חודש כדי להגיע ליעד בזמן.", False),
        ("חובות – הלוואות וכרטיסי אשראי: מתי כל חוב ייגמר וכמה ריבית הוא עולה, עם סדר פירעון מומלץ (הריבית הגבוהה קודם).", False),
        ("", False),
        ("צבעים", True),
        ("צהוב = כאן מקלידים.   כחול בהיר = נוסחה, לא צריך לגעת.   כל הסכומים בשקלים.", False),
        ("", False),
        ("טיפים", True),
        ("• הוצאה שמגיעה פעם בשנה (ביטוח רכב, אגרת רישוי, חגים) – כדאי לתכנן כסכום חודשי (סכום שנתי ÷ 12) כדי שלא תפתיע.", False),
        ("• כלל 50/30/20 הוא נקודת התחלה ולא חוק: בישראל הדיור לבד לוקח לרוב חלק גדול מההכנסה. המטרה היא לראות את המגמה ולשפר.", False),
        ("• להעתקה ל-Google Sheets: העלו את הקובץ ל-Google Drive ← פתחו באמצעות Google Sheets. הנוסחאות, הרשימות והגרפים עוברים.", False),
        ("", False),
        ("הבהרה", True),
        ("הקובץ הוא כלי לתכנון ומעקב אישי בלבד ואינו ייעוץ פיננסי, השקעות או מס. בדקו החלטות מהותיות מול איש מקצוע מוסמך.", False),
        ("שאלות או תקלה בקובץ? פרטי יצירת קשר מופיעים בעמוד ההורדה ובאתר.", False),
    ]
    for i, (t, bold) in enumerate(lines, start=4):
        c = ws.cell(row=i, column=2, value=t)
        c.font = f(bold, 13 if bold else 11, C_PRIMARY if bold else "222222")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    setup_print(ws, landscape=False)

    # ================= הגדרות =================
    ws = wb.create_sheet("הגדרות")
    title(ws, "הגדרות", "ממלאים פעם אחת")
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 60
    rows = [
        ("שנת התקציב", year, "0", "השנה שעליה הקובץ מסכם. תנועות משנים אחרות לא נספרות."),
        ("שם המשפחה", "משפחת ישראלי" if demo else "", None, "מופיע בכותרת הדשבורד."),
        ("יתרת פתיחה בעו\"ש (1 בינואר)", 4500 if demo else 0, ILS0, "כמה כסף יש בחשבון בתחילת השנה (במינוס? רשמו סכום שלילי)."),
        ("יעד חיסכון חודשי", 1800 if demo else 0, ILS0, "כמה תרצו שיישאר בסוף כל חודש (כולל הפקדות לחיסכון)."),
    ]
    for i, (k, v, fmt, note) in enumerate(rows, start=4):
        ws.cell(row=i, column=1, value=k).font = f(True)
        cell(ws, i, 2, v, "input", fmt)
        ws.cell(row=i, column=3, value=note).font = f(False, 10, "5A6B7D")
    ws["A10"] = "חודשים (לרשימות)"
    ws["A10"].font = f(True)
    for i, m in enumerate(MONTHS):
        ws.cell(row=11 + i, column=1, value=m)
        ws.cell(row=11 + i, column=2, value=i + 1)
    ws["A24"] = "אמצעי תשלום (לרשימות)"
    ws["A24"].font = f(True)
    for i, m in enumerate(["כרטיס אשראי", "הוראת קבע", "העברה בנקאית", "מזומן", "ביט / פייבוקס", "צ'ק", "אחר"]):
        ws.cell(row=25 + i, column=1, value=m)
    ws["A34"] = "סיווג 50/30/20 (לרשימות)"
    ws["A34"].font = f(True)
    for i, m in enumerate([NEED, WANT, SAVE]):
        ws.cell(row=35 + i, column=1, value=m)
    ws["A40"] = "סוג (לרשימות)"
    ws["A40"].font = f(True)
    ws["A41"], ws["A42"] = INC, EXP
    wb.defined_names["BudgetYear"] = DefinedName("BudgetYear", attr_text=f"{S}!$B$4")

    # ================= תקציב =================
    ws = wb.create_sheet("תקציב")
    title(ws, f"תכנון תקציב {year}", "צהוב = מקלידים. הסכום החודשי מועתק לכל החודשים – אפשר לשנות כל חודש בנפרד.")
    hdr = ["קבוצה", "קטגוריה", "סוג", "סיווג 50/30/20", "סכום חודשי מתוכנן"] + MONTHS + ["סה\"כ שנתי"]
    widths = [16, 38, 9, 19, 14] + [10.5] * 12 + [13]
    for j, (h, w) in enumerate(zip(hdr, widths), start=1):
        head(ws, 4, j, h, w)
    ws.row_dimensions[4].height = 32
    for i in range(NROWS):
        r = FIRST + i
        if i < len(CATS):
            g, name, typ, cls, amt = CATS[i]
        else:
            g, name, typ, cls, amt = None, None, None, None, None
        cell(ws, r, 1, g, "input")
        cell(ws, r, 2, name, "input")
        cell(ws, r, 3, typ, "input")
        cell(ws, r, 4, cls or None, "input")
        cell(ws, r, 5, amt, "input", ILS)
        for m in range(12):
            cell(ws, r, 6 + m, f"=IF($E{r}=\"\",\"\",$E{r})", "input", ILS)
        cell(ws, r, 18, f"=IF($B{r}=\"\",\"\",SUM(F{r}:Q{r}))", "formula", ILS, bold=True)
    tr = LAST + 2
    for lab, typ, rr in (("סה\"כ הכנסות מתוכננות", INC, tr), ("סה\"כ הוצאות מתוכננות (כולל חיסכון)", EXP, tr + 1)):
        ws.cell(row=rr, column=2, value=lab).font = f(True)
        for m in range(13):
            col = 6 + m
            cl = L(col)
            cell(ws, rr, col, f"=SUMIFS({cl}${FIRST}:{cl}${LAST},$C${FIRST}:$C${LAST},\"{typ}\")", "formula", ILS, True)
    ws.cell(row=tr + 2, column=2, value="מאזן מתוכנן (הכנסות פחות הוצאות)").font = f(True)
    for m in range(13):
        cl = L(6 + m)
        cell(ws, tr + 2, 6 + m, f"={cl}{tr}-{cl}{tr + 1}", "formula", ILS, True)
    ws.conditional_formatting.add(f"F{tr + 2}:R{tr + 2}", CellIsRule(operator="lessThan", formula=["0"], fill=fill("F8D7DA")))
    dv_type = DataValidation(type="list", formula1=f"={S}!$A$41:$A$42", allow_blank=True)
    dv_cls = DataValidation(type="list", formula1=f"={S}!$A$35:$A$37", allow_blank=True)
    dv_amt = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                            error="רשמו סכום חיובי בשקלים", errorTitle="סכום לא תקין")
    for dv in (dv_type, dv_cls, dv_amt):
        ws.add_data_validation(dv)
    dv_type.add(f"C{FIRST}:C{LAST}")
    dv_cls.add(f"D{FIRST}:D{LAST}")
    dv_amt.add(f"E{FIRST}:Q{LAST}")
    ws.freeze_panes = "C5"
    setup_print(ws)

    # ================= תנועות =================
    ws = wb.create_sheet("תנועות")
    title(ws, "יומן תנועות", "שורה לכל הוצאה או הכנסה. הקטגוריה נבחרת מרשימה (מתוך גיליון «תקציב»).")
    hdr = [("תאריך", 12), ("קטגוריה", 38), ("סכום", 12), ("אמצעי תשלום", 16), ("הערה", 34), ("סוג", 10), ("חודש", 8)]
    for j, (h, w) in enumerate(hdr, start=1):
        head(ws, 4, j, h, w)
    for r in range(TX_FIRST, TX_LAST + 1):
        for col, kind, fmt in ((1, "input", "dd/mm/yyyy"), (2, "input", None), (3, "input", ILS),
                               (4, "input", None), (5, "input", None)):
            c = ws.cell(row=r, column=col)
            c.fill = fill(C_INPUT)
            c.border = BORDER
            if fmt:
                c.number_format = fmt
        ws.cell(row=r, column=6, value=f"=IF(B{r}=\"\",\"\",IFERROR(INDEX({B}!$C${FIRST}:$C${LAST},MATCH(B{r},{B}!$B${FIRST}:$B${LAST},0)),\"?\"))").fill = fill(C_FORMULA)
        ws.cell(row=r, column=7, value=f"=IF(A{r}=\"\",\"\",IF(YEAR(A{r})=BudgetYear,MONTH(A{r}),\"שנה אחרת\"))").fill = fill(C_FORMULA)
    dv_cat = DataValidation(type="list", formula1=f"={B}!$B${FIRST}:$B${LAST}", allow_blank=True,
                            error="בחרו קטגוריה מהרשימה (אפשר להוסיף קטגוריות בגיליון «תקציב»)", errorTitle="קטגוריה לא מוכרת")
    dv_pay = DataValidation(type="list", formula1=f"={S}!$A$25:$A$31", allow_blank=True)
    dv_date = DataValidation(type="date", operator="between", formula1="DATE(2000,1,1)", formula2="DATE(2100,12,31)",
                             allow_blank=True, error="רשמו תאריך, למשל 15/01/" + str(year), errorTitle="תאריך לא תקין")
    for dv in (dv_cat, dv_pay, dv_date):
        ws.add_data_validation(dv)
    dv_cat.add(f"B{TX_FIRST}:B{TX_LAST}")
    dv_pay.add(f"D{TX_FIRST}:D{TX_LAST}")
    dv_date.add(f"A{TX_FIRST}:A{TX_LAST}")
    ws.conditional_formatting.add(f"F{TX_FIRST}:G{TX_LAST}", FormulaRule(formula=[f'OR($F{TX_FIRST}="?",$G{TX_FIRST}="שנה אחרת")'], fill=fill("F8D7DA")))
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:G{TX_LAST}"
    setup_print(ws, landscape=False)
    if demo:
        fill_demo(ws, year)

    # ================= שנתי =================
    ws = wb.create_sheet("שנתי")
    title(ws, f"סיכום שנתי {year} – בפועל", "מחושב אוטומטית מתוך «תנועות». אין צורך להקליד כאן.")
    hdr = ["קבוצה", "קטגוריה", "סוג"] + MONTHS + ["סה\"כ בפועל", "מתוכנן", "הפרש (מתוכנן פחות בפועל)"]
    widths = [16, 38, 9] + [10.5] * 12 + [13, 13, 15]
    for j, (h, w) in enumerate(zip(hdr, widths), start=1):
        head(ws, 4, j, h, w)
    ws.row_dimensions[4].height = 32
    for m in range(12):           # hidden helper row with month numbers
        ws.cell(row=3, column=4 + m, value=m + 1).font = f(False, 8, "FFFFFF")
    for i in range(NROWS):
        r = FIRST + i
        cell(ws, r, 1, f"=IF({B}!A{r}=\"\",\"\",{B}!A{r})")
        cell(ws, r, 2, f"=IF({B}!B{r}=\"\",\"\",{B}!B{r})")
        cell(ws, r, 3, f"=IF({B}!C{r}=\"\",\"\",{B}!C{r})")
        for m in range(12):
            cl = L(4 + m)
            cell(ws, r, 4 + m,
                 f"=IF($B{r}=\"\",\"\",SUMIFS({T}!$C${TX_FIRST}:$C${TX_LAST},{T}!$B${TX_FIRST}:$B${TX_LAST},$B{r},{T}!$G${TX_FIRST}:$G${TX_LAST},{cl}$3))",
                 "formula", ILS)
        cell(ws, r, 16, f"=IF($B{r}=\"\",\"\",SUM(D{r}:O{r}))", "formula", ILS, True)
        cell(ws, r, 17, f"=IF($B{r}=\"\",\"\",{B}!R{r})", "formula", ILS)
        cell(ws, r, 18, f"=IF($B{r}=\"\",\"\",IF($C{r}=\"{INC}\",P{r}-Q{r},Q{r}-P{r}))", "formula", ILS)
    ws.conditional_formatting.add(f"R{FIRST}:R{LAST}", CellIsRule(operator="lessThan", formula=["0"], fill=fill("F8D7DA")))
    s0 = LAST + 2
    summary = [
        ("סה\"כ הכנסות", lambda cl: f"=SUMIFS({cl}${FIRST}:{cl}${LAST},$C${FIRST}:$C${LAST},\"{INC}\")"),
        ("סה\"כ הוצאות", lambda cl: f"=SUMIFS({cl}${FIRST}:{cl}${LAST},$C${FIRST}:$C${LAST},\"{EXP}\")"),
        ("נשאר בחודש (הכנסות פחות הוצאות)", lambda cl: f"={cl}{s0}-{cl}{s0 + 1}"),
    ]
    for k, (lab, fn) in enumerate(summary):
        rr = s0 + k
        ws.cell(row=rr, column=2, value=lab).font = f(True)
        for m in range(14):
            col = 4 + m
            cell(ws, rr, col, fn(L(col)), "formula", ILS, True)
    rr = s0 + 3
    ws.cell(row=rr, column=2, value="יתרה מצטברת בעו\"ש (משוערת)").font = f(True)
    for m in range(12):
        cl = L(4 + m)
        prev = f"{S}!$B$6" if m == 0 else f"{L(3 + m)}{rr}"
        cell(ws, rr, 4 + m, f"={prev}+{cl}{s0 + 2}", "formula", ILS, True)
    rr = s0 + 4
    ws.cell(row=rr, column=2, value="יעד חיסכון חודשי").font = f(True)
    for m in range(12):
        cell(ws, rr, 4 + m, f"={S}!$B$7", "formula", ILS)
    ws.conditional_formatting.add(f"D{s0 + 2}:O{s0 + 3}", CellIsRule(operator="lessThan", formula=["0"], fill=fill("F8D7DA")))
    ws.freeze_panes = "D5"
    setup_print(ws)
    YS = s0  # summary rows on שנתי

    # ================= חודשי =================
    ws = wb.create_sheet("חודשי")
    title(ws, "מבט חודשי: מתוכנן מול בפועל", "בחרו חודש בתא הצהוב")
    ws["A3"] = "חודש:"
    ws["A3"].font = f(True, 12)
    cell(ws, 3, 2, MONTHS[2] if demo else MONTHS[0], "input")
    ws["B3"].font = f(True, 12)
    ws["C3"] = f"=MATCH(B3,{S}!$A$11:$A$22,0)"
    ws["C3"].font = f(False, 8, "FFFFFF")
    dv_m = DataValidation(type="list", formula1=f"={S}!$A$11:$A$22", allow_blank=False)
    ws.add_data_validation(dv_m)
    dv_m.add("B3")
    hdr = [("קטגוריה", 38), ("סוג", 9), ("מתוכנן", 13), ("בפועל", 13), ("נשאר / חריגה", 14), ("% ניצול", 10)]
    for j, (h, w) in enumerate(hdr, start=1):
        head(ws, 5, j, h, w)
    for i in range(NROWS):
        r = 6 + i
        src = FIRST + i
        cell(ws, r, 1, f"=IF({B}!B{src}=\"\",\"\",{B}!B{src})")
        cell(ws, r, 2, f"=IF({B}!C{src}=\"\",\"\",{B}!C{src})")
        cell(ws, r, 3, f"=IF(A{r}=\"\",\"\",N(INDEX({B}!$F{src}:$Q{src},1,$C$3)))", "formula", ILS)
        cell(ws, r, 4, f"=IF(A{r}=\"\",\"\",N(INDEX({Y}!$D{src}:$O{src},1,$C$3)))", "formula", ILS)
        cell(ws, r, 5, f"=IF(A{r}=\"\",\"\",IF(B{r}=\"{INC}\",D{r}-C{r},C{r}-D{r}))", "formula", ILS)
        cell(ws, r, 6, f"=IF(OR(A{r}=\"\",N(C{r})=0),\"\",D{r}/C{r})", "formula", PCT)
    end = 6 + NROWS - 1
    ws.conditional_formatting.add(f"E6:E{end}", CellIsRule(operator="lessThan", formula=["0"], fill=fill("F8D7DA"), font=Font(color="9C0006", bold=True)))
    ws.conditional_formatting.add(f"F6:F{end}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1.5, color="5B9BD5"))
    # month summary box
    ws.column_dimensions["H"].width = 30
    ws.column_dimensions["I"].width = 14
    ws.column_dimensions["J"].width = 14
    head(ws, 5, 8, "סיכום החודש")
    head(ws, 5, 9, "מתוכנן")
    head(ws, 5, 10, "בפועל")
    for k, (lab, typ) in enumerate((("הכנסות", INC), ("הוצאות", EXP))):
        rr = 6 + k
        cell(ws, rr, 8, lab, None).font = f(True)
        cell(ws, rr, 9, f"=SUMIFS(C$6:C${end},B$6:B${end},\"{typ}\")", "formula", ILS, True)
        cell(ws, rr, 10, f"=SUMIFS(D$6:D${end},B$6:B${end},\"{typ}\")", "formula", ILS, True)
    cell(ws, 8, 8, "נשאר בסוף החודש", None).font = f(True)
    cell(ws, 8, 9, "=I6-I7", "formula", ILS, True)
    cell(ws, 8, 10, "=J6-J7", "formula", ILS, True)
    cell(ws, 9, 8, "קטגוריות בחריגה", None).font = f(True)
    cell(ws, 9, 10, f"=COUNTIFS(E6:E{end},\"<0\",B6:B{end},\"{EXP}\")", "formula", "0", True)
    ws.conditional_formatting.add("I8:J8", CellIsRule(operator="lessThan", formula=["0"], fill=fill("F8D7DA")))
    ch = BarChart()
    ch.type = "col"
    ch.title = "החודש: מתוכנן מול בפועל"
    ch.add_data(Reference(ws, min_col=9, min_row=5, max_row=7), titles_from_data=True)
    ch.add_data(Reference(ws, min_col=10, min_row=5, max_row=7), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=8, min_row=6, max_row=7))
    ch.height, ch.width = 7.5, 13
    ws.add_chart(ch, "H11")
    ws.freeze_panes = "A6"
    setup_print(ws, landscape=False)

    # ================= דשבורד =================
    ws = wb.create_sheet("דשבורד", 1)
    title(ws, f"דשבורד {year}")
    ws["A1"] = f"=\"דשבורד {year}\"&IF({S}!$B$5=\"\",\"\",\" · \"&{S}!$B$5)"
    for col, w in zip("ABCDEFGHIJ", [24, 15, 15, 15, 4, 26, 14, 14, 14, 14]):
        ws.column_dimensions[col].width = w
    # KPI block
    head(ws, 3, 1, "מדד")
    head(ws, 3, 2, "בפועל עד היום")
    head(ws, 3, 3, "מתוכנן לשנה")
    head(ws, 3, 4, "% מהתכנון")
    kpis = [
        ("הכנסות", f"={Y}!P{YS}", f"={B}!R{LAST + 2}"),
        ("הוצאות (כולל חיסכון)", f"={Y}!P{YS + 1}", f"={B}!R{LAST + 3}"),
        ("נשאר (הכנסות פחות הוצאות)", f"={Y}!P{YS + 2}", f"={B}!R{LAST + 4}"),
        ("הופרש לחיסכון ולהחזר חובות", f"=SUMIFS({Y}!$P${FIRST}:$P${LAST},{B}!$D${FIRST}:$D${LAST},\"{SAVE}\")",
         f"=SUMIFS({B}!$R${FIRST}:$R${LAST},{B}!$D${FIRST}:$D${LAST},\"{SAVE}\")"),
    ]
    for k, (lab, a, p) in enumerate(kpis):
        r = 4 + k
        cell(ws, r, 1, lab, None).font = f(True)
        cell(ws, r, 2, a, "formula", ILS, True)
        cell(ws, r, 3, p, "formula", ILS)
        cell(ws, r, 4, f"=IF(N(C{r})=0,\"\",B{r}/C{r})", "formula", PCT)
    cell(ws, 8, 1, "שיעור חיסכון (מהכנסות)", None).font = f(True)
    cell(ws, 8, 2, "=IF(N(B4)=0,\"\",(B6+B7)/B4)", "formula", PCT, True)
    cell(ws, 9, 1, "חודשים עם נתונים", None).font = f(True)
    cell(ws, 9, 2, f"=SUMPRODUCT(--({Y}!D{YS + 1}:O{YS + 1}>0))", "formula", "0", True)
    cell(ws, 10, 1, "יתרה משוערת בעו\"ש היום", None).font = f(True)
    cell(ws, 10, 2, f"=IF(B9=0,{S}!B6,INDEX({Y}!D{YS + 3}:O{YS + 3},1,B9))", "formula", ILS, True)
    ws.conditional_formatting.add("B6", CellIsRule(operator="lessThan", formula=["0"], fill=fill("F8D7DA")))

    # groups table (for charts)
    head(ws, 3, 6, "קבוצת הוצאות")
    head(ws, 3, 7, "מתוכנן לשנה")
    head(ws, 3, 8, "בפועל")
    head(ws, 3, 9, "% ניצול")
    exp_groups = [g for g in GROUPS if g != "הכנסות"]
    for k, g in enumerate(exp_groups):
        r = 4 + k
        cell(ws, r, 6, g, None).font = f(True)
        cell(ws, r, 7, f"=SUMIFS({B}!$R${FIRST}:$R${LAST},{B}!$A${FIRST}:$A${LAST},F{r},{B}!$C${FIRST}:$C${LAST},\"{EXP}\")", "formula", ILS)
        cell(ws, r, 8, f"=SUMIFS({Y}!$P${FIRST}:$P${LAST},{Y}!$A${FIRST}:$A${LAST},F{r},{Y}!$C${FIRST}:$C${LAST},\"{EXP}\")", "formula", ILS)
        cell(ws, r, 9, f"=IF(N(G{r})=0,\"\",H{r}/G{r})", "formula", PCT)
    gl = 4 + len(exp_groups) - 1
    r = gl + 1
    cell(ws, r, 6, "קבוצות אחרות (שהוספתם)", None).font = f(True)
    cell(ws, r, 7, f"={B}!R{LAST + 3}-SUM(G4:G{gl})", "formula", ILS)
    cell(ws, r, 8, f"={Y}!P{YS + 1}-SUM(H4:H{gl})", "formula", ILS)
    gl = r
    ws.conditional_formatting.add(f"I4:I{gl}", CellIsRule(operator="greaterThan", formula=["1"], fill=fill("F8D7DA")))

    # 50/30/20
    r0 = 13
    head(ws, r0, 1, "בדיקת 50/30/20")
    head(ws, r0, 2, "יעד")
    head(ws, r0, 3, "בפועל ₪")
    head(ws, r0, 4, "בפועל %")
    for k, (cls, tgt) in enumerate(((NEED, 0.5), (WANT, 0.3), (SAVE, 0.2))):
        r = r0 + 1 + k
        cell(ws, r, 1, cls, None).font = f(True)
        cell(ws, r, 2, tgt, "formula", "0%")
        cell(ws, r, 3, f"=SUMIFS({Y}!$P${FIRST}:$P${LAST},{B}!$D${FIRST}:$D${LAST},A{r})", "formula", ILS)
        cell(ws, r, 4, f"=IF(N($B$4)=0,\"\",C{r}/$B$4)", "formula", PCT)
    ws.cell(row=r0 + 4, column=1, value="האחוזים הם מתוך סך ההכנסות נטו בפועל.").font = f(False, 9, "5A6B7D", True)

    # monthly helper table (for line/bar chart)
    r1 = 20
    head(ws, r1, 1, "חודש")
    head(ws, r1, 2, "הכנסות")
    head(ws, r1, 3, "הוצאות")
    head(ws, r1, 4, "יתרה מצטברת")
    for m in range(12):
        r = r1 + 1 + m
        cl = L(4 + m)
        cell(ws, r, 1, MONTHS[m], None)
        cell(ws, r, 2, f"={Y}!{cl}{YS}", "formula", ILS)
        cell(ws, r, 3, f"={Y}!{cl}{YS + 1}", "formula", ILS)
        cell(ws, r, 4, f"={Y}!{cl}{YS + 3}", "formula", ILS)

    c1 = BarChart()
    c1.type = "col"
    c1.title = "הכנסות מול הוצאות לפי חודש"
    c1.add_data(Reference(ws, min_col=2, max_col=3, min_row=r1, max_row=r1 + 12), titles_from_data=True)
    c1.set_categories(Reference(ws, min_col=1, min_row=r1 + 1, max_row=r1 + 12))
    c1.height, c1.width = 8, 17
    c1.y_axis.numFmt = '#,##0'
    c1.y_axis.majorGridlines = None
    ws.add_chart(c1, "K22")

    c2 = PieChart()
    c2.title = "לאן הולך הכסף (בפועל)"
    c2.add_data(Reference(ws, min_col=8, min_row=3, max_row=gl), titles_from_data=True)
    c2.set_categories(Reference(ws, min_col=6, min_row=4, max_row=gl))
    c2.dataLabels = DataLabelList()
    c2.dataLabels.showPercent = True
    for a in ("showVal", "showCatName", "showSerName", "showLegendKey", "showLeaderLines"):
        setattr(c2.dataLabels, a, False)
    c2.height, c2.width = 9, 13
    ws.add_chart(c2, "K3")

    c3 = BarChart()
    c3.type = "bar"
    c3.title = "מתוכנן מול בפועל לפי קבוצה"
    c3.add_data(Reference(ws, min_col=7, max_col=8, min_row=3, max_row=gl), titles_from_data=True)
    c3.set_categories(Reference(ws, min_col=6, min_row=4, max_row=gl))
    c3.height, c3.width = 9, 17
    ws.add_chart(c3, "S3")

    c4 = LineChart()
    c4.title = "יתרה מצטברת בעו\"ש"
    c4.add_data(Reference(ws, min_col=4, min_row=r1, max_row=r1 + 12), titles_from_data=True)
    c4.set_categories(Reference(ws, min_col=1, min_row=r1 + 1, max_row=r1 + 12))
    c4.height, c4.width = 8, 13
    c4.legend = None
    ws.add_chart(c4, "U22")

    c5 = BarChart()
    c5.type = "col"
    c5.title = "50/30/20: יעד מול בפועל"
    c5.add_data(Reference(ws, min_col=2, min_row=r0, max_row=r0 + 3), titles_from_data=True)
    c5.add_data(Reference(ws, min_col=4, min_row=r0, max_row=r0 + 3), titles_from_data=True)
    c5.set_categories(Reference(ws, min_col=1, min_row=r0 + 1, max_row=r0 + 3))
    c5.height, c5.width = 8, 13
    c5.y_axis.numFmt = '0%'
    ws.add_chart(c5, "K40")
    setup_print(ws)

    # ================= יעדי חיסכון =================
    ws = wb.create_sheet("יעדי חיסכון")
    title(ws, "יעדי חיסכון", "כמה לשים בצד כל חודש כדי להגיע ליעד בזמן")
    hdr = [("יעד", 30), ("סכום היעד", 14), ("תאריך יעד", 13), ("נחסך עד היום", 14), ("חסר", 13),
           ("חודשים שנותרו", 12), ("להפריש בחודש", 14), ("התקדמות", 16)]
    for j, (h, w) in enumerate(hdr, start=1):
        head(ws, 4, j, h, w)
    demo_goals = [("קרן חירום (3 חודשי הוצאות)", 45000, date(year, 12, 31), 18000),
                  ("חופשה משפחתית בקיץ", 12000, date(year, 7, 1), 4000),
                  ("החלפת רכב", 30000, date(year + 2, 6, 30), 6000)]
    for i in range(15):
        r = 5 + i
        g = demo_goals[i] if (demo and i < len(demo_goals)) else (None, None, None, None)
        cell(ws, r, 1, g[0], "input")
        cell(ws, r, 2, g[1], "input", ILS)
        cell(ws, r, 3, g[2], "input", "dd/mm/yyyy")
        cell(ws, r, 4, g[3], "input", ILS)
        cell(ws, r, 5, f"=IF(B{r}=\"\",\"\",MAX(0,B{r}-N(D{r})))", "formula", ILS)
        cell(ws, r, 6, f"=IF(OR(B{r}=\"\",C{r}=\"\"),\"\",MAX(1,(YEAR(C{r})-YEAR(TODAY()))*12+MONTH(C{r})-MONTH(TODAY())))", "formula", "0")
        cell(ws, r, 7, f"=IF(F{r}=\"\",\"\",E{r}/F{r})", "formula", ILS, True)
        cell(ws, r, 8, f"=IF(N(B{r})=0,\"\",MIN(1,N(D{r})/B{r}))", "formula", "0%")
    cell(ws, 21, 6, "סה\"כ לחודש:", None).font = f(True)
    cell(ws, 21, 7, "=SUM(G5:G19)", "formula", ILS, True)
    ws.conditional_formatting.add("H5:H19", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="2E8B57"))
    ws.cell(row=23, column=1, value="טיפ: רשמו את ההפקדה החודשית כקטגוריה בקבוצת «חיסכון» בגיליון «תקציב», כדי שתופיע בתכנון.").font = f(False, 10, "5A6B7D", True)
    setup_print(ws)

    # ================= חובות =================
    ws = wb.create_sheet("חובות")
    title(ws, "הלוואות וחובות", "מתי כל חוב ייגמר וכמה ריבית הוא עולה")
    hdr = [("שם החוב", 30), ("יתרה היום", 14), ("ריבית שנתית", 12), ("תשלום חודשי", 14), ("חודשים לסיום", 13),
           ("תאריך סיום משוער", 15), ("ריבית שעוד תשלמו (משוער)", 17), ("סדר פירעון מומלץ", 13)]
    for j, (h, w) in enumerate(hdr, start=1):
        head(ws, 4, j, h, w)
    ws.row_dimensions[4].height = 32
    demo_debts = [("הלוואה לרכב", 38000, 0.065, 1200), ("מינוס בעו\"ש", 6000, 0.11, 600), ("הלוואה מקרן השתלמות", 15000, 0.045, 500)]
    for i in range(12):
        r = 5 + i
        d = demo_debts[i] if (demo and i < len(demo_debts)) else (None, None, None, None)
        cell(ws, r, 1, d[0], "input")
        cell(ws, r, 2, d[1], "input", ILS)
        cell(ws, r, 3, d[2], "input", "0.0%")
        cell(ws, r, 4, d[3], "input", ILS)
        cell(ws, r, 5, f"=IF(OR(B{r}=\"\",N(D{r})=0),\"\",IF(B{r}*N(C{r})/12>=D{r},\"התשלום לא מכסה ריבית\",ROUNDUP(NPER(N(C{r})/12,-D{r},B{r}),0)))", "formula", "0")
        cell(ws, r, 6, f"=IF(ISNUMBER(E{r}),EDATE(TODAY(),E{r}),\"\")", "formula", "mm/yyyy")
        cell(ws, r, 7, f"=IF(ISNUMBER(E{r}),MAX(0,-CUMIPMT(N(C{r})/12+1E-12,E{r},B{r},1,E{r},0)),\"\")", "formula", ILS)
        cell(ws, r, 8, f"=IF(B{r}=\"\",\"\",COUNTIFS($C$5:$C$16,\">\"&N(C{r}),$B$5:$B$16,\"<>\")+1)", "formula", "0")
    cell(ws, 18, 1, "סה\"כ", None).font = f(True)
    cell(ws, 18, 2, "=SUM(B5:B16)", "formula", ILS, True)
    cell(ws, 18, 4, "=SUM(D5:D16)", "formula", ILS, True)
    cell(ws, 18, 7, "=SUM(G5:G16)", "formula", ILS, True)
    ws.conditional_formatting.add("E5:E16", FormulaRule(formula=['ISTEXT(E5)'], fill=fill("F8D7DA")))
    notes = [
        "סדר הפירעון המומלץ (1 = ראשון): שיטת «מפולת» – כל שקל נוסף הולך לחוב עם הריבית הגבוהה ביותר, וכך משלמים הכי פחות ריבית בסך הכול.",
        "את הריבית השנתית אפשר למצוא בדוח הבנק, באפליקציה או בהסכם ההלוואה. החישוב מניח ריבית קבועה ותשלומים שווים (שפיצר).",
        "המספרים הם הערכה לתכנון בלבד. לפני מחזור או פירעון מוקדם בדקו מול הבנק עמלות ותנאים.",
    ]
    for i, n in enumerate(notes):
        ws.cell(row=20 + i, column=1, value=n).font = f(False, 10, "5A6B7D", True)
    setup_print(ws)

    # sheet order & tab colors
    order = ["הוראות", "דשבורד", "הגדרות", "תקציב", "תנועות", "חודשי", "שנתי", "יעדי חיסכון", "חובות"]
    wb._sheets = [wb[n] for n in order]
    colors = ["7F7F7F", C_ACCENT, "7F7F7F", "C9A227", "C9A227", C_PRIMARY, C_PRIMARY, C_ACCENT, C_ACCENT]
    for n, c in zip(order, colors):
        wb[n].sheet_properties.tabColor = c
    wb.active = 0 if not demo else 1
    wb.properties.title = f"תקציב משק בית Pro {year}"
    wb.properties.creator = "Glory"
    wb.calculation.fullCalcOnLoad = True
    wb.save(path)


def fill_demo(ws, year):
    """Realistic-looking demo transactions for the example workbook."""
    rows = []
    def add(d, cat, amt, pay, note=""):
        rows.append((d, cat, round(amt), pay, note))
    for m in range(1, 13):
        d1 = date(year, m, 1)
        add(date(year, m, 10), "משכורת נטו – בן/בת זוג 1", 12500 + random.choice([0, 0, 300]), "העברה בנקאית")
        add(date(year, m, 10), "משכורת נטו – בן/בת זוג 2", 9500, "העברה בנקאית")
        add(date(year, m, 20), "קצבת ילדים (ביטוח לאומי)", 340, "העברה בנקאית")
        if m in (3, 9):
            add(date(year, m, 25), "החזרי מס / מענקים", 1800, "העברה בנקאית", "החזר מס")
        add(date(year, m, 2), "משכנתא / שכר דירה", 5200, "הוראת קבע")
        if m % 2 == 1:
            add(date(year, m, 5), "ארנונה", 1040, "הוראת קבע", "תשלום דו-חודשי")
            add(date(year, m, 18), "חשמל", random.randint(700, 1150), "הוראת קבע")
            add(date(year, m, 22), "מים וביוב", random.randint(300, 420), "הוראת קבע")
        add(date(year, m, 1), "ועד בית", 180, "הוראת קבע")
        add(date(year, m, 12), "גז", random.randint(50, 90), "כרטיס אשראי")
        add(date(year, m, 3), "אינטרנט וטלוויזיה", 179, "כרטיס אשראי")
        add(date(year, m, 3), "טלפונים ניידים", 118, "כרטיס אשראי")
        add(date(year, m, 1), "קופת חולים – ביטוח משלים", 162, "הוראת קבע")
        add(date(year, m, 1), "ביטוח בריאות פרטי", 148, "הוראת קבע")
        add(date(year, m, 1), "ביטוח חיים / משכנתא", 121, "הוראת קבע")
        add(date(year, m, 1), "ביטוח דירה ומבנה", 68, "הוראת קבע")
        for _ in range(4):
            add(d1 + timedelta(days=random.randint(0, 26)), "דלק / טעינה", random.randint(150, 220), "כרטיס אשראי")
        if m == 2:
            add(date(year, m, 14), "ביטוח רכב (חובה + מקיף)", 4600, "כרטיס אשראי", "חידוש שנתי")
            add(date(year, m, 14), "רישיון רכב (אגרה) וטסט", 1450, "כרטיס אשראי")
        if m in (4, 10):
            add(date(year, m, 8), "טיפולים ותיקונים", random.randint(900, 1600), "כרטיס אשראי")
        for _ in range(5):
            add(d1 + timedelta(days=random.randint(0, 27)), "סופרמרקט", random.randint(480, 820), "כרטיס אשראי")
        add(d1 + timedelta(days=random.randint(0, 27)), "שוק, ירקות ומאפייה", random.randint(300, 480), "מזומן")
        add(d1 + timedelta(days=random.randint(0, 27)), "פארם וטואלטיקה", random.randint(150, 320), "כרטיס אשראי")
        for _ in range(3):
            add(d1 + timedelta(days=random.randint(0, 27)), "אוכל בחוץ ומשלוחים", random.randint(140, 330), "כרטיס אשראי")
        if m not in (7, 8):
            add(date(year, m, 1), "גן / מעון / צהרון", 1800, "הוראת קבע")
            add(date(year, m, 5), "חוגים ותנועות נוער", 420, "כרטיס אשראי")
        else:
            add(date(year, m, 1), "גן / מעון / צהרון", 2400, "העברה בנקאית", "קייטנה")
        if m == 8:
            add(date(year, m, 25), "תשלומי הורים וציוד לבית הספר", 1600, "כרטיס אשראי")
        add(d1 + timedelta(days=random.randint(0, 27)), "בילויים ותרבות", random.randint(150, 450), "כרטיס אשראי")
        add(date(year, m, 4), "מנויים (סטרימינג, אפליקציות, חדר כושר)", 215, "כרטיס אשראי")
        if m in (3, 4, 9, 11):
            add(d1 + timedelta(days=random.randint(0, 27)), "ביגוד והנעלה למבוגרים", random.randint(400, 900), "כרטיס אשראי")
            add(d1 + timedelta(days=random.randint(0, 27)), "ביגוד והנעלה לילדים", random.randint(300, 700), "כרטיס אשראי")
        if m in (5, 6, 8, 10):
            add(d1 + timedelta(days=random.randint(0, 27)), "מתנות לשמחות (חתונות, בר/בת מצווה)", random.choice([500, 600, 800]), "ביט / פייבוקס", "חתונה")
        if m in (4, 9):
            add(date(year, m, 10), "חגים ומתנות למשפחה", random.randint(900, 1500), "כרטיס אשראי", "פסח" if m == 4 else "ראש השנה")
        if m == 7:
            add(date(year, m, 15), "חופשות וטיולים", 7800, "כרטיס אשראי", "צימר בגליל")
        add(date(year, m, 11), "קרן חירום", 800, "העברה בנקאית")
        add(date(year, m, 11), "השקעות / קרן השתלמות עצמאית", 500, "הוראת קבע")
        add(date(year, m, 11), "חיסכון למטרה (רכב, חופשה, שיפוץ)", 400, "הוראת קבע")
        add(date(year, m, 15), "החזר הלוואה", 1200, "הוראת קבע", "הלוואה לרכב")
        add(date(year, m, 28), "עמלות בנק ודמי כרטיס", random.randint(18, 40), "הוראת קבע")
        if random.random() < 0.5:
            add(d1 + timedelta(days=random.randint(0, 27)), "הוצאות לא צפויות", random.randint(200, 1200), "כרטיס אשראי", "תיקון מכונת כביסה")
    rows.sort(key=lambda x: x[0])
    for i, (d, cat, amt, pay, note) in enumerate(rows):
        r = TX_FIRST + i
        ws.cell(row=r, column=1, value=d)
        ws.cell(row=r, column=2, value=cat)
        ws.cell(row=r, column=3, value=amt)
        ws.cell(row=r, column=4, value=pay)
        ws.cell(row=r, column=5, value=note or None)
    assert TX_FIRST + len(rows) < TX_LAST


if __name__ == "__main__":
    for y in YEARS:
        build(y, False, OUT / f"household-budget-{y}.xlsx")
        build(y, True, OUT / f"household-budget-{y}-example.xlsx")
        print("built", y)
