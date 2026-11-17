"""Build the עוסק פטור 2026 tracker (.xlsx).

Usage:  python3 build.py            -> osek-patur-tracker-2026.xlsx (empty) + -example.xlsx (demo data)
All numbers are formulas; input cells are yellow. No macros.
Official figures (checked 2026-11-17):
  * VAT-exempt dealer ceiling 2026: 122,833 ILS (2025: 120,000) - Kol Zchut "עוסק פטור", Tax Authority publications.
"""
import datetime as dt
import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, DoughnutChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.series import DataPoint
from openpyxl.formatting.rule import CellIsRule, DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

HERE = Path(__file__).parent
YEAR = 2026
CEILING = 122833
CHECKED = "17.11.2026"
SOURCE = "כל זכות – 'עוסק פטור' (kolzchut.org.il) ופרסומי רשות המסים"
ROWS = 500  # log rows
FIRST = 5   # first data row in logs
LAST = FIRST + ROWS - 1

# palette
TEAL = "0F766E"
TEAL_L = "CCFBF1"
INPUT = "FFF7D6"
CALC = "F1F5F9"
WHITE = "FFFFFF"
GREY = "64748B"

thin = Side(style="thin", color="CBD5E1")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
F_TITLE = Font(name="Arial", size=18, bold=True, color=TEAL)
F_SUB = Font(name="Arial", size=10, color=GREY)
F_HEAD = Font(name="Arial", size=11, bold=True, color=WHITE)
F_BOLD = Font(name="Arial", size=11, bold=True)
F_BODY = Font(name="Arial", size=11)
F_KPI = Font(name="Arial", size=20, bold=True, color=TEAL)
FILL_HEAD = PatternFill("solid", fgColor=TEAL)
FILL_IN = PatternFill("solid", fgColor=INPUT)
FILL_CALC = PatternFill("solid", fgColor=CALC)
FILL_L = PatternFill("solid", fgColor=TEAL_L)
RIGHT = Alignment(horizontal="right", vertical="center", wrap_text=True, readingOrder=2)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True, readingOrder=2)
ILS = '#,##0 ₪;[Red]-#,##0 ₪;"–"'
PCT = '0.0%'
DATE = 'DD/MM/YYYY'

MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט",
          "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
CATEGORIES = ["ציוד ומחשבים", "תוכנות ומנויים", "פרסום ושיווק", "רכב ונסיעות",
              "טלפון ואינטרנט", "שכירות / משרד", "השתלמויות וספרות מקצועית",
              "הנהלת חשבונות וייעוץ", "ביטוחים", "חומרי גלם וקניות לעסק", "אחר"]
PAYMENTS = ["העברה בנקאית", "ביט / פייבוקס", "אשראי", "מזומן", "צ'ק", "PayPal", "אחר"]


def rtl(ws, tab=None):
    ws.sheet_view.rightToLeft = True
    ws.sheet_view.showGridLines = False
    if tab:
        ws.sheet_properties.tabColor = tab


def cell(ws, ref, value=None, font=F_BODY, fill=None, fmt=None, align=RIGHT, border=True):
    c = ws[ref]
    if value is not None:
        c.value = value
    c.font = font
    c.alignment = align
    if fill:
        c.fill = fill
    if fmt:
        c.number_format = fmt
    if border:
        c.border = BORDER
    return c


def title(ws, text, sub):
    ws["A1"].value = text
    ws["A1"].font = F_TITLE
    ws["A1"].alignment = Alignment(horizontal="right", readingOrder=2)
    ws["A2"].value = sub
    ws["A2"].font = F_SUB
    ws["A2"].alignment = Alignment(horizontal="right", readingOrder=2)
    ws.row_dimensions[1].height = 30


def header_row(ws, row, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        col = ws.cell(row=row, column=i)
        col.value = h
        col.font = F_HEAD
        col.fill = FILL_HEAD
        col.alignment = CENTER
        col.border = BORDER
        ws.column_dimensions[col.column_letter].width = w
    ws.row_dimensions[row].height = 32


# ---------------------------------------------------------------- sheets
def sheet_instructions(wb):
    ws = wb.active
    ws.title = "הוראות"
    rtl(ws, TEAL)
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 110
    ws["B1"].value = f"מעקב עוסק פטור {YEAR} – הוראות שימוש"
    ws["B1"].font = F_TITLE
    lines = [
        ("איך מתחילים (3 דקות)", True),
        ("1. בגיליון 'הגדרות' ממלאים שם עסק ובודקים את שנת המס והתקרה. התאים הצהובים הם התאים היחידים שממלאים.", False),
        ("2. בכל פעם שמתקבל תשלום – שורה חדשה בגיליון 'הכנסות' (תאריך, מס' קבלה, לקוח, סכום).", False),
        ("3. בכל הוצאה לעסק – שורה בגיליון 'הוצאות'. בוחרים קטגוריה מהרשימה. אם רק חלק מההוצאה מוכר (למשל טלפון), רושמים אחוז בעמודה '% מוכר'.", False),
        ("4. 'לוח בקרה' מראה כמה ניצלתם מהתקרה, כמה נשאר, ומתי בקצב הנוכחי צפוי לעבור אותה.", False),
        ("5. 'סיכום חודשי' מציג הכנסות, הוצאות ורווח לפי חודש ולפי רבעון.", False),
        ("6. 'עזר לדוח שנתי' מרכז את המספרים שיבקשו מכם בסוף השנה, ורשימת מסמכים לבדיקה.", False),
        ("", False),
        ("חשוב לדעת", True),
        (f"• תקרת עוסק פטור לשנת {YEAR}: {CEILING:,} ₪ (בשנת 2025: 120,000 ₪). מקור: {SOURCE}. נבדק לאחרונה: {CHECKED}.", False),
        ("• התקרה נמדדת לפי מחזור העסקאות (סך ההכנסות ברוטו), לא לפי הרווח. הוצאות לא מקטינות את המחזור לצורך התקרה.", False),
        ("• התקרה מתעדכנת בדרך כלל בינואר. בתחילת שנה חדשה עדכנו בגיליון 'הגדרות' את השנה ואת התקרה לפי הפרסום הרשמי.", False),
        ("• הקובץ נועד לסדר ומעקב בלבד. הוא אינו ייעוץ מס או ייעוץ משפטי ואינו מחליף רואה חשבון או יועץ מס.", False),
        ("• עוסק פטור מוציא קבלות (לא חשבוניות מס). הקובץ אינו מנפיק מסמכים – רק מתעד אותם.", False),
        ("", False),
        ("טיפים", True),
        ("• אל תמחקו שורות באמצע הטבלה – פשוט נקו את התוכן. יש מקום ל-500 הכנסות ו-500 הוצאות.", False),
        ("• תאריך חייב להיות תאריך אמיתי (למשל 15/03/2026), אחרת השורה לא תיספר בסיכומים.", False),
        ("• רק תשלומים שהתאריך שלהם בשנת המס שבהגדרות נספרים בסיכומים ובתקרה.", False),
        ("• Google Sheets: מעלים את הקובץ ל-Google Drive ← לחיצה ימנית ← 'פתיחה באמצעות Google Sheets'. כל הנוסחאות עובדות; ייתכנו הבדלים קטנים בעיצוב הגרפים.", False),
        ("• גרסה עם נתוני דוגמה מצורפת בנפרד (example), כדי לראות איך הכול נראה מלא.", False),
    ]
    r = 3
    for text, bold in lines:
        c = ws.cell(row=r, column=2, value=text)
        c.font = Font(name="Arial", size=13 if bold else 11, bold=bold, color=TEAL if bold else "000000")
        c.alignment = RIGHT
        ws.row_dimensions[r].height = 22 if bold else 30
        r += 1
    legend = [("תא צהוב = ממלאים", FILL_IN), ("תא אפור = מחושב אוטומטית, לא לגעת", FILL_CALC)]
    r += 1
    for text, fill in legend:
        cell(ws, f"B{r}", text, fill=fill)
        r += 1


def sheet_settings(wb):
    ws = wb.create_sheet("הגדרות")
    rtl(ws, "F59E0B")
    title(ws, "הגדרות", "ממלאים פעם אחת בתחילת השנה")
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 70
    rows = [
        ("שם העסק", "", INPUT, None, "יופיע בכותרות"),
        ("שנת מס", YEAR, INPUT, "0", "רק הכנסות והוצאות מהשנה הזו נספרות"),
        ("תקרת עוסק פטור (₪)", CEILING, INPUT, ILS, f"{YEAR}: {CEILING:,} ₪ · מקור: {SOURCE} · נבדק {CHECKED}"),
        ("חודש נוכחי (אוטומטי)", "=IF(YEAR(TODAY())=B4,MONTH(TODAY()),IF(YEAR(TODAY())>B4,12,1))", CALC, "0", "לפי תאריך המחשב"),
        ("חודש לחישוב (ידני, לא חובה)", None, INPUT, "0", "השאירו ריק. מלאו 1–12 רק אם רוצים לחשב קצב עד חודש אחר"),
        ("חודש פתיחת העסק בשנה זו", 1, INPUT, "0", "אם פתחתם את העסק באמצע השנה – רשמו את החודש (1–12), כדי שהקצב החודשי יחושב נכון"),
        ("חודש לחישוב בפועל", "=IF(B7<>\"\",B7,B6)", CALC, "0", ""),
        ("חודשי פעילות שנספרים", "=MAX(1,B9-B8+1)", CALC, "0", ""),
    ]
    for i, (label, val, fill, fmt, note) in enumerate(rows, start=3):
        cell(ws, f"A{i}", label, font=F_BOLD)
        c = cell(ws, f"B{i}", val, fill=PatternFill("solid", fgColor=fill), fmt=fmt)
        cell(ws, f"C{i}", note, font=F_SUB, border=False)
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="12", allow_blank=True,
                        error="מספר חודש בין 1 ל-12", errorTitle="חודש לא תקין")
    ws.add_data_validation(dv)
    dv.add("B7")
    dv.add("B8")
    dvy = DataValidation(type="whole", operator="between", formula1="2024", formula2="2040")
    ws.add_data_validation(dvy)
    dvy.add("B4")

    # lists for dropdowns
    cell(ws, "E2", "קטגוריות הוצאה (אפשר לשנות)", font=F_HEAD, fill=FILL_HEAD, align=CENTER)
    cell(ws, "G2", "אמצעי תשלום", font=F_HEAD, fill=FILL_HEAD, align=CENTER)
    ws.column_dimensions["E"].width = 32
    ws.column_dimensions["G"].width = 22
    for i in range(15):
        cell(ws, f"E{3+i}", CATEGORIES[i] if i < len(CATEGORIES) else None, fill=FILL_IN)
    for i in range(10):
        cell(ws, f"G{3+i}", PAYMENTS[i] if i < len(PAYMENTS) else None, fill=FILL_IN)
    return ws


S = "הגדרות"
YR = f"'{S}'!$B$4"
CEIL = f"'{S}'!$B$5"
MNOW = f"'{S}'!$B$9"
MACTIVE = f"'{S}'!$B$10"
Y_START = f"DATE({YR},1,1)"
Y_END = f"DATE({YR},12,31)"


def sheet_income(wb):
    ws = wb.create_sheet("הכנסות")
    rtl(ws, "16A34A")
    title(ws, "יומן הכנסות", "כל תשלום שהתקבל = שורה. רק שורות עם תאריך בשנת המס נספרות.")
    cell(ws, "E2", "סה\"כ בשנת המס:", font=F_BOLD, border=False)
    cell(ws, "F2", f"=SUMIFS(F{FIRST}:F{LAST},A{FIRST}:A{LAST},\">=\"&{Y_START},A{FIRST}:A{LAST},\"<=\"&{Y_END})",
         font=F_BOLD, fill=FILL_L, fmt=ILS)
    header_row(ws, 4, ["תאריך קבלת התשלום", "מס' קבלה", "לקוח", "תיאור העבודה", "אמצעי תשלום", "סכום (₪)", "חודש"],
               [16, 12, 24, 36, 16, 14, 10])
    for r in range(FIRST, LAST + 1):
        for col in "ABCDEF":
            c = ws[f"{col}{r}"]
            c.fill = FILL_IN
            c.border = BORDER
            c.alignment = RIGHT
            c.font = F_BODY
        ws[f"A{r}"].number_format = DATE
        ws[f"F{r}"].number_format = ILS
        g = ws[f"G{r}"]
        g.value = f'=IF(ISNUMBER(A{r}),MONTH(A{r}),"")'
        g.fill = FILL_CALC
        g.border = BORDER
        g.alignment = CENTER
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:G{LAST}"
    dv_date = DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True,
                             error="הקלידו תאריך, למשל 15/03/2026", errorTitle="תאריך לא תקין")
    dv_amt = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                            error="סכום חייב להיות מספר חיובי", errorTitle="סכום לא תקין")
    dv_pay = DataValidation(type="list", formula1=f"='{S}'!$G$3:$G$12", allow_blank=True)
    for dv in (dv_date, dv_amt, dv_pay):
        ws.add_data_validation(dv)
    dv_date.add(f"A{FIRST}:A{LAST}")
    dv_amt.add(f"F{FIRST}:F{LAST}")
    dv_pay.add(f"E{FIRST}:E{LAST}")
    return ws


def sheet_expenses(wb):
    ws = wb.create_sheet("הוצאות")
    rtl(ws, "DC2626")
    title(ws, "יומן הוצאות", "עוסק פטור לא מקזז מע\"מ – רושמים את הסכום המלא ששולם, כולל מע\"מ.")
    cell(ws, "G2", "סה\"כ מוכר בשנה:", font=F_BOLD, border=False)
    cell(ws, "H2", f"=SUMIFS(H{FIRST}:H{LAST},A{FIRST}:A{LAST},\">=\"&{Y_START},A{FIRST}:A{LAST},\"<=\"&{Y_END})",
         font=F_BOLD, fill=FILL_L, fmt=ILS)
    header_row(ws, 4, ["תאריך", "ספק", "קטגוריה", "תיאור", "מס' מסמך", "סכום ששולם (₪)", "% מוכר (ריק = 100%)",
                       "סכום מוכר (₪)", "מסמך שמור?"],
               [14, 22, 26, 30, 12, 15, 14, 15, 12])
    for r in range(FIRST, LAST + 1):
        for col in "ABCDEFGI":
            c = ws[f"{col}{r}"]
            c.fill = FILL_IN
            c.border = BORDER
            c.alignment = RIGHT
            c.font = F_BODY
        ws[f"A{r}"].number_format = DATE
        ws[f"F{r}"].number_format = ILS
        ws[f"G{r}"].number_format = "0%"
        h = ws[f"H{r}"]
        h.value = f'=IF(F{r}="","",F{r}*IF(G{r}="",1,G{r}))'
        h.number_format = ILS
        h.fill = FILL_CALC
        h.border = BORDER
        h.alignment = RIGHT
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:I{LAST}"
    dv_date = DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True,
                             error="הקלידו תאריך, למשל 15/03/2026", errorTitle="תאריך לא תקין")
    dv_amt = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True)
    dv_pct = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                            error="אחוז בין 0% ל-100% (למשל 50%)", errorTitle="אחוז לא תקין")
    dv_cat = DataValidation(type="list", formula1=f"='{S}'!$E$3:$E$17", allow_blank=True)
    dv_yes = DataValidation(type="list", formula1='"כן,לא"', allow_blank=True)
    for dv in (dv_date, dv_amt, dv_pct, dv_cat, dv_yes):
        ws.add_data_validation(dv)
    dv_date.add(f"A{FIRST}:A{LAST}")
    dv_amt.add(f"F{FIRST}:F{LAST}")
    dv_pct.add(f"G{FIRST}:G{LAST}")
    dv_cat.add(f"C{FIRST}:C{LAST}")
    dv_yes.add(f"I{FIRST}:I{LAST}")
    ws.conditional_formatting.add(f"I{FIRST}:I{LAST}",
                                  CellIsRule(operator="equal", formula=['"לא"'], fill=PatternFill("solid", fgColor="FECACA")))
    return ws


INC = f"'הכנסות'!$F${FIRST}:$F${LAST}"
INC_D = f"'הכנסות'!$A${FIRST}:$A${LAST}"
EXP = f"'הוצאות'!$H${FIRST}:$H${LAST}"
EXP_D = f"'הוצאות'!$A${FIRST}:$A${LAST}"
EXP_C = f"'הוצאות'!$C${FIRST}:$C${LAST}"


def sheet_summary(wb):
    ws = wb.create_sheet("סיכום חודשי")
    rtl(ws, "2563EB")
    title(ws, "סיכום חודשי ורבעוני", "מחושב אוטומטית מיומני ההכנסות וההוצאות")
    header_row(ws, 4, ["חודש", "הכנסות", "הוצאות מוכרות", "רווח", "הכנסות מצטבר", "% מהתקרה", "נותר עד התקרה", "תקרה"],
               [14, 15, 16, 15, 17, 12, 17, 14])
    for m in range(1, 13):
        r = 4 + m
        start = f"DATE({YR},{m},1)"
        end = f"DATE({YR},{m + 1},1)"
        cell(ws, f"A{r}", MONTHS[m - 1], font=F_BOLD, fill=FILL_CALC)
        cell(ws, f"B{r}", f'=SUMIFS({INC},{INC_D},">="&{start},{INC_D},"<"&{end})', fill=FILL_CALC, fmt=ILS)
        cell(ws, f"C{r}", f'=SUMIFS({EXP},{EXP_D},">="&{start},{EXP_D},"<"&{end})', fill=FILL_CALC, fmt=ILS)
        cell(ws, f"D{r}", f"=B{r}-C{r}", fill=FILL_CALC, fmt=ILS)
        cell(ws, f"E{r}", f"=SUM($B$5:B{r})", fill=FILL_CALC, fmt=ILS)
        cell(ws, f"F{r}", f"=E{r}/{CEIL}", fill=FILL_CALC, fmt=PCT)
        cell(ws, f"G{r}", f"=MAX(0,{CEIL}-E{r})", fill=FILL_CALC, fmt=ILS)
        cell(ws, f"H{r}", f"={CEIL}", fill=FILL_CALC, fmt=ILS)
    cell(ws, "A17", "סה\"כ שנה", font=F_HEAD, fill=FILL_HEAD)
    for col in "BCD":
        cell(ws, f"{col}17", f"=SUM({col}5:{col}16)", font=F_BOLD, fill=FILL_L, fmt=ILS)
    cell(ws, "E17", "=E16", font=F_BOLD, fill=FILL_L, fmt=ILS)
    cell(ws, "F17", "=F16", font=F_BOLD, fill=FILL_L, fmt=PCT)
    cell(ws, "G17", "=G16", font=F_BOLD, fill=FILL_L, fmt=ILS)
    ws.conditional_formatting.add("F5:F16", DataBarRule(start_type="num", start_value=0, end_type="num",
                                                        end_value=1, color="14B8A6"))
    ws.conditional_formatting.add("F5:F17", CellIsRule(operator="greaterThan", formula=["1"],
                                                       font=Font(color="DC2626", bold=True)))

    # quarters
    header_row(ws, 20, ["רבעון", "הכנסות", "הוצאות מוכרות", "רווח", "% מהתקרה (מצטבר)"], [14, 15, 16, 15, 17])
    for q in range(1, 5):
        r = 20 + q
        a, b = 5 + (q - 1) * 3, 7 + (q - 1) * 3
        cell(ws, f"A{r}", f"רבעון {q} ({MONTHS[(q-1)*3]}–{MONTHS[(q-1)*3+2]})", font=F_BOLD, fill=FILL_CALC)
        cell(ws, f"B{r}", f"=SUM(B{a}:B{b})", fill=FILL_CALC, fmt=ILS)
        cell(ws, f"C{r}", f"=SUM(C{a}:C{b})", fill=FILL_CALC, fmt=ILS)
        cell(ws, f"D{r}", f"=B{r}-C{r}", fill=FILL_CALC, fmt=ILS)
        cell(ws, f"E{r}", f"=F{b}", fill=FILL_CALC, fmt=PCT)
    ws.column_dimensions["A"].width = 26
    ws.freeze_panes = "B5"

    # charts
    bar = BarChart()
    bar.type = "col"
    bar.title = "הכנסות מול הוצאות לפי חודש"
    bar.y_axis.title = "₪"
    data = Reference(ws, min_col=2, max_col=3, min_row=4, max_row=16)
    cats = Reference(ws, min_col=1, min_row=5, max_row=16)
    bar.add_data(data, titles_from_data=True)
    bar.set_categories(cats)
    bar.series[0].graphicalProperties.solidFill = "14B8A6"
    bar.series[1].graphicalProperties.solidFill = "F87171"
    bar.height, bar.width = 8, 17
    ws.add_chart(bar, "J4")

    line = LineChart()
    line.title = "הכנסות מצטברות מול התקרה"
    line.add_data(Reference(ws, min_col=5, min_row=4, max_row=16), titles_from_data=True)
    line.add_data(Reference(ws, min_col=8, min_row=4, max_row=16), titles_from_data=True)
    line.set_categories(cats)
    line.series[0].graphicalProperties.line.solidFill = "0F766E"
    line.series[0].graphicalProperties.line.width = 32000
    line.series[1].graphicalProperties.line.solidFill = "DC2626"
    line.series[1].graphicalProperties.line.dashStyle = "dash"
    line.height, line.width = 8, 17
    ws.add_chart(line, "J21")
    return ws


def sheet_dashboard(wb):
    ws = wb.create_sheet("לוח בקרה", 1)
    rtl(ws, "0F766E")
    ws["A1"].value = f'="לוח בקרה – עוסק פטור "&{YR}&IF(\'{S}\'!$B$3<>"",\" · \"&\'{S}\'!$B$3,"")'
    ws["A1"].font = F_TITLE
    ws["A1"].alignment = Alignment(horizontal="right", readingOrder=2)
    ws["A2"].value = f'="התקרה לשנת "&{YR}&": "&TEXT({CEIL},"#,##0")&" ₪ · מקור: {SOURCE} · נבדק {CHECKED}"'
    ws["A2"].font = F_SUB
    for col, w in zip("ABCDEFGH", [30, 20, 4, 36, 24, 4, 14, 14]):
        ws.column_dimensions[col].width = w

    kpis = [
        ("A4", "B4", "הכנסות מתחילת השנה", "='סיכום חודשי'!E16", ILS),
        ("A5", "B5", "נותר עד התקרה", f"=MAX(0,{CEIL}-B4)", ILS),
        ("A6", "B6", "ניצול התקרה", f"=B4/{CEIL}", PCT),
        ("A7", "B7", "הוצאות מוכרות מתחילת השנה", "='סיכום חודשי'!C17", ILS),
        ("A8", "B8", "רווח מתחילת השנה", "=B4-B7", ILS),
        ("D4", "E4", "קצב הכנסה חודשי ממוצע", f"=SUMIFS({INC},{INC_D},\">=\"&{Y_START},{INC_D},\"<\"&DATE({YR},{MNOW}+1,1))/{MACTIVE}", ILS),
        ("D5", "E5", "תחזית מחזור לסוף השנה", f"=SUMIFS({INC},{INC_D},\">=\"&{Y_START},{INC_D},\"<\"&DATE({YR},{MNOW}+1,1))+E4*(12-{MNOW})", ILS),
        ("D6", "E6", "מתי צפוי לעבור את התקרה", f'=IF(B4>{CEIL},"כבר עברתם",IF(E4<=0,"אין עדיין נתונים",IF(E5<={CEIL},"לא בקצב הנוכחי",INDEX(\'סיכום חודשי\'!$A$5:$A$16,MIN(12,{MNOW}+ROUNDUP(({CEIL}-SUMIFS({INC},{INC_D},">="&{Y_START},{INC_D},"<"&DATE({YR},{MNOW}+1,1)))/E4,0))))))', None),
        ("D7", "E7", "אפשר להכניס בחודש עד סוף השנה (כולל החודש)", f"=MAX(0,{CEIL}-B4)/(13-{MNOW})", ILS),
        ("D8", "E8", "מצב", f'=IF(B6>1,"עברתם את התקרה – כדאי לפנות לרו״ח / למע״מ",IF(B6>=0.9,"קרוב מאוד לתקרה",IF(B6>=0.7,"לשים לב – מעל 70%","בטוח – מתחת ל-70%")))', None),
    ]
    for lref, vref, label, formula, fmt in kpis:
        cell(ws, lref, label, font=F_BOLD, fill=FILL_L)
        c = cell(ws, vref, formula, font=Font(name="Arial", size=14, bold=True, color=TEAL), fill=FILL_CALC, fmt=fmt)
        ws.row_dimensions[c.row].height = 30
    ws.conditional_formatting.add("B6", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1,
                                                    color="14B8A6"))
    for rng in ("B6", "E8"):
        ws.conditional_formatting.add(rng, FormulaRule(formula=["$B$6>=0.9"], fill=PatternFill("solid", fgColor="FECACA")))
        ws.conditional_formatting.add(rng, FormulaRule(formula=["AND($B$6>=0.7,$B$6<0.9)"],
                                                       fill=PatternFill("solid", fgColor="FEF3C7")))
    ws["E6"].alignment = CENTER
    ws["E8"].alignment = CENTER
    ws["E8"].font = Font(name="Arial", size=12, bold=True)

    # gauge data (hidden helper in G/H)
    cell(ws, "G3", "מד", font=F_SUB, border=False)
    cell(ws, "G4", "נוצל", font=F_SUB, border=False)
    cell(ws, "H4", f"=MIN(B4,{CEIL})", font=F_SUB, border=False, fmt=ILS)
    cell(ws, "G5", "נותר", font=F_SUB, border=False)
    cell(ws, "H5", f"=MAX(0,{CEIL}-B4)", font=F_SUB, border=False, fmt=ILS)
    cell(ws, "G6", "חצי תחתון", font=F_SUB, border=False)
    cell(ws, "H6", f"={CEIL}", font=F_SUB, border=False, fmt=ILS)
    ws.column_dimensions["G"].hidden = True
    ws.column_dimensions["H"].hidden = True

    g = DoughnutChart(holeSize=55)
    g.title = "מד תקרה"
    g.add_data(Reference(ws, min_col=8, min_row=4, max_row=6), titles_from_data=False)
    g.set_categories(Reference(ws, min_col=7, min_row=4, max_row=6))
    g.firstSliceAng = 270
    s = g.series[0]
    colors = ["0F766E", "E2E8F0", None]
    for i, col in enumerate(colors):
        pt = DataPoint(idx=i)
        if col:
            pt.graphicalProperties.solidFill = col
        else:
            pt.graphicalProperties.noFill = True
            pt.graphicalProperties.line.noFill = True
        s.dPt.append(pt)
    g.legend = None
    g.visible_cells_only = False
    g.height, g.width = 8, 12
    ws.add_chart(g, "A11")

    bar = BarChart()
    bar.type = "col"
    bar.title = "הכנסות לפי חודש"
    sm = wb["סיכום חודשי"]
    bar.add_data(Reference(sm, min_col=2, min_row=4, max_row=16), titles_from_data=True)
    bar.set_categories(Reference(sm, min_col=1, min_row=5, max_row=16))
    bar.series[0].graphicalProperties.solidFill = "14B8A6"
    bar.legend = None
    bar.height, bar.width = 8, 14
    ws.add_chart(bar, "D11")

    pie = PieChart()
    pie.title = "הוצאות לפי קטגוריה"
    rep = wb["עזר לדוח שנתי"]
    pie.add_data(Reference(rep, min_col=2, min_row=11, max_row=21), titles_from_data=False)
    pie.set_categories(Reference(rep, min_col=1, min_row=11, max_row=21))
    pie.dataLabels = DataLabelList()
    pie.dataLabels.showPercent = True
    pie.height, pie.width = 9, 14
    ws.add_chart(pie, "A28")
    ws.merge_cells("A9:E9")
    cell(ws, "A9", "הקובץ לתיעוד ומעקב בלבד ואינו ייעוץ מס. בכל החלטה – רואה חשבון / יועץ מס.", font=F_SUB, border=False)
    return ws


def sheet_report(wb):
    ws = wb.create_sheet("עזר לדוח שנתי")
    rtl(ws, "7C3AED")
    title(ws, "עזר לדוח השנתי", "המספרים המרכזיים לסוף השנה + רשימת בדיקה. לתיאום מול רואה החשבון.")
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 14
    ws.column_dimensions["D"].width = 60
    cell(ws, "A4", "מחזור עסקאות שנתי (סך ההכנסות)", font=F_BOLD, fill=FILL_L)
    cell(ws, "B4", "='סיכום חודשי'!B17", font=F_BOLD, fill=FILL_CALC, fmt=ILS)
    cell(ws, "D4", "זה הסכום שמדווחים בהצהרת המחזור השנתית לעוסק פטור", font=F_SUB, border=False)
    cell(ws, "A5", "סך הוצאות מוכרות", font=F_BOLD, fill=FILL_L)
    cell(ws, "B5", "='סיכום חודשי'!C17", font=F_BOLD, fill=FILL_CALC, fmt=ILS)
    cell(ws, "A6", "רווח לפני מס (הכנסות פחות הוצאות)", font=F_BOLD, fill=FILL_L)
    cell(ws, "B6", "=B4-B5", font=F_BOLD, fill=FILL_CALC, fmt=ILS)
    cell(ws, "A7", "מספר קבלות שנרשמו", font=F_BOLD, fill=FILL_L)
    cell(ws, "B7", f'=COUNTIFS({INC_D},">="&{Y_START},{INC_D},"<="&{Y_END})', font=F_BOLD, fill=FILL_CALC, fmt="0")

    header_row(ws, 10, ["קטגוריית הוצאה", "סכום מוכר", "% מההוצאות"], [44, 18, 14])
    for i in range(11):
        r = 11 + i
        cell(ws, f"A{r}", f"='{S}'!E{3+i}", fill=FILL_CALC)
        cell(ws, f"B{r}", f'=IF(A{r}="",0,SUMIFS({EXP},{EXP_C},A{r},{EXP_D},">="&{Y_START},{EXP_D},"<="&{Y_END}))',
             fill=FILL_CALC, fmt=ILS)
        cell(ws, f"C{r}", f"=IF($B$5=0,0,B{r}/$B$5)", fill=FILL_CALC, fmt=PCT)
    cell(ws, "A22", "קטגוריות נוספות / ללא קטגוריה", fill=FILL_CALC)
    cell(ws, "B22", "=B5-SUM(B11:B21)", fill=FILL_CALC, fmt=ILS)
    cell(ws, "C22", "=IF($B$5=0,0,B22/$B$5)", fill=FILL_CALC, fmt=PCT)

    header_row(ws, 25, ["רשימת בדיקה לסוף השנה", "בוצע?", "", "הערה"], [44, 18, 14, 60])
    checks = [
        ("הצהרה שנתית על מחזור העסקאות למע\"מ (עוסק פטור)", "בדרך כלל עד סוף ינואר של השנה הבאה. בודקים את המועד המדויק באתר רשות המסים"),
        ("דוח שנתי למס הכנסה – לבדוק אם חייבים להגיש", "עם רואה חשבון / באזור האישי באתר רשות המסים"),
        ("כל הקבלות שהוצאו תואמות ליומן ההכנסות", "השוו את 'מספר קבלות שנרשמו' לפנקס / לתוכנה"),
        ("מסמכים לכל ההוצאות שמורים (סרוקים)", "בגיליון 'הוצאות' – עמודה 'מסמך שמור?'"),
        ("אישורי הפקדה לפנסיה / קרן השתלמות לשנה", "מבקשים מהקרן או מהאזור האישי"),
        ("אישור ניכוי מס במקור (אם לקוחות ניכו)", ""),
        ("טופס 867 מהבנק (ריבית/רווחי הון, אם יש)", ""),
        ("תשלומי מקדמות לביטוח לאומי ולמס הכנסה – סיכום", ""),
        ("עדכון התקרה והשנה בגיליון 'הגדרות' לשנה הבאה", "התקרה מתעדכנת בדרך כלל בינואר"),
    ]
    dv = DataValidation(type="list", formula1='"כן,לא,לא רלוונטי"', allow_blank=True)
    ws.add_data_validation(dv)
    for i, (t, note) in enumerate(checks):
        r = 26 + i
        cell(ws, f"A{r}", t)
        cell(ws, f"B{r}", None, fill=FILL_IN, align=CENTER)
        dv.add(f"B{r}")
        cell(ws, f"D{r}", note, font=F_SUB)
        ws.row_dimensions[r].height = 28
    ws.conditional_formatting.add("B26:B34", CellIsRule(operator="equal", formula=['"כן"'],
                                                        fill=PatternFill("solid", fgColor="BBF7D0")))
    cell(ws, "A37", "אין בקובץ ייעוץ מס. המועדים והחובות משתנים – יש לאמת מול רשות המסים / רואה חשבון.",
         font=F_SUB, border=False)
    return ws


# ---------------------------------------------------------------- demo data
def demo(wb):
    rnd = random.Random(7)
    inc = wb["הכנסות"]
    clients = ["סטודיו נוף", "דנה לוי", "מכולת השכונה", "עמותת אור", "רון כהן", "קפה מרפסת", "משרד גל ושות'"]
    jobs = ["עיצוב לוגו", "ניהול רשתות – חודשי", "צילום אירוע", "בניית דף נחיתה", "שיעור פרטי", "ייעוץ", "עריכת וידאו"]
    r = FIRST
    n = 1001
    for m in range(1, 11):
        for _ in range(rnd.randint(3, 5)):
            d = dt.date(YEAR, m, rnd.randint(1, 28))
            inc[f"A{r}"] = d
            inc[f"B{r}"] = n
            inc[f"C{r}"] = rnd.choice(clients)
            inc[f"D{r}"] = rnd.choice(jobs)
            inc[f"E{r}"] = rnd.choice(PAYMENTS[:4])
            inc[f"F{r}"] = rnd.choice([800, 1200, 1500, 2200, 2800, 3500, 4200])
            r += 1
            n += 1
    ex = wb["הוצאות"]
    items = [("מחשב נייד", "ציוד ומחשבים", 4200, None), ("Adobe", "תוכנות ומנויים", 230, None),
             ("פרסום ממומן", "פרסום ושיווק", 600, None), ("סלולר", "טלפון ואינטרנט", 120, 0.5),
             ("דלק", "רכב ונסיעות", 350, 0.45), ("קורס מקצועי", "השתלמויות וספרות מקצועית", 1500, None),
             ("רואה חשבון", "הנהלת חשבונות וייעוץ", 400, None)]
    r = FIRST
    for m in range(1, 11):
        for name, cat, amt, pct in rnd.sample(items, 3):
            ex[f"A{r}"] = dt.date(YEAR, m, rnd.randint(1, 28))
            ex[f"B{r}"] = name
            ex[f"C{r}"] = cat
            ex[f"F{r}"] = amt
            if pct:
                ex[f"G{r}"] = pct
            ex[f"I{r}"] = "כן" if rnd.random() > 0.1 else "לא"
            r += 1
    wb["הגדרות"]["B3"] = "סטודיו לדוגמה"
    wb["הגדרות"]["B7"] = 10  # freeze 'today' at October for stable screenshots


def build(example=False):
    wb = Workbook()
    sheet_instructions(wb)
    sheet_settings(wb)
    sheet_income(wb)
    sheet_expenses(wb)
    sheet_summary(wb)
    sheet_report(wb)
    sheet_dashboard(wb)
    if example:
        demo(wb)
    wb.active = 1
    for ws in wb.worksheets:
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.properties.title = f"מעקב עוסק פטור {YEAR}"
    wb.properties.creator = "Glory"
    name = f"osek-patur-tracker-{YEAR}{'-example' if example else ''}.xlsx"
    out = HERE / name
    wb.save(out)
    print("wrote", out)
    return out


if __name__ == "__main__":
    build(False)
    build(True)
