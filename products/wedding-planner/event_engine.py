"""Shared spreadsheet engine for the event planners (wedding, bar/bat mitzvah).

build_workbook(cfg, demo=False) -> openpyxl.Workbook
All numbers on the dashboard are live formulas; input cells are yellow.
"""
import datetime as dt
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import FormulaRule, CellIsRule, DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

FONT = "Arial"
C_HEAD = "6B2E4F"      # deep plum
C_HEAD2 = "B5838D"
C_INPUT = "FFF4CC"     # input = soft yellow
C_CALC = "F2F2F2"      # formula = light grey
C_TITLE = "3D1A2E"
C_OK = "D8F0DC"
C_WARN = "FFE0B2"
C_BAD = "F8D0D0"
thin = Side(style="thin", color="D9D9D9")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
NIS = '#,##0 "₪";[Red]-#,##0 "₪";"-"'
DATE = "dd/mm/yyyy"
PCT = "0%"

# sheet names
S_HELP, S_SET, S_DASH, S_BUD, S_GST, S_VEN, S_PAY, S_TODO, S_SEAT = (
    "הוראות", "הגדרות", "דשבורד", "תקציב", "מוזמנים", "ספקים", "תשלומים", "צ'קליסט", "הושבה")

FIRST = 5           # first data row on list sheets
N_GUESTS = 400
N_VENDORS = 80
N_PAY = 150
N_TODO = 90
N_TABLES = 60
N_CATS = 20


def q(sheet):
    return "'" + sheet.replace("'", "''") + "'"


def rng(sheet, col, n):
    return f"{q(sheet)}!${col}${FIRST}:${col}${FIRST + n - 1}"


def style_cell(c, kind=None, fmt=None, bold=False, size=11, color="000000", align="right"):
    c.font = Font(name=FONT, bold=bold, size=size, color=color)
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True, readingOrder=2)
    if kind == "input":
        c.fill = PatternFill("solid", fgColor=C_INPUT)
        c.border = BORDER
    elif kind == "calc":
        c.fill = PatternFill("solid", fgColor=C_CALC)
        c.border = BORDER
    elif kind == "head":
        c.fill = PatternFill("solid", fgColor=C_HEAD)
        c.font = Font(name=FONT, bold=True, size=11, color="FFFFFF")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True, readingOrder=2)
        c.border = BORDER
    if fmt:
        c.number_format = fmt


def new_sheet(wb, name, title, subtitle, widths, tab=None):
    ws = wb.create_sheet(name)
    ws.sheet_view.rightToLeft = True
    ws.sheet_view.showGridLines = False
    if tab:
        ws.sheet_properties.tabColor = tab
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    last = get_column_letter(max(len(widths), 2))
    ws.merge_cells(f"A1:{last}1")
    ws["A1"] = title
    style_cell(ws["A1"], bold=True, size=18, color=C_TITLE)
    ws.row_dimensions[1].height = 32
    ws.merge_cells(f"A2:{last}2")
    ws["A2"] = subtitle
    style_cell(ws["A2"], size=10, color="666666")
    ws.row_dimensions[2].height = 30
    return ws


def headers(ws, row, names):
    for i, h in enumerate(names, start=1):
        c = ws.cell(row=row, column=i, value=h)
        style_cell(c, "head")
    ws.row_dimensions[row].height = 30


def add_list_validation(ws, formula, cells, prompt=None):
    dv = DataValidation(type="list", formula1=formula, allow_blank=True, showDropDown=False)
    dv.error = "יש לבחור ערך מהרשימה (אפשר לערוך את הרשימות בגיליון הגדרות)"
    dv.errorTitle = "ערך לא ברשימה"
    dv.errorStyle = "warning"
    if prompt:
        dv.prompt = prompt
        dv.showInputMessage = True
    ws.add_data_validation(dv)
    dv.add(cells)


def define(wb, name, ref):
    wb.defined_names[name] = DefinedName(name, attr_text=ref)


# --------------------------------------------------------------------------- settings
def build_settings(wb, cfg, demo):
    ws = new_sheet(wb, S_SET, "הגדרות האירוע",
                   "ממלאים פעם אחת. התאים הצהובים הם קלט. אפשר לערוך את הרשימות שבטבלה למטה, והן יופיעו ברשימות הנפתחות בכל הקובץ.",
                   [30, 22, 4, 24, 22, 24, 16, 14, 16, 10, 14, 16], tab="FFC000")
    rows = [
        ("שם האירוע", cfg["demo_name"] if demo else "", None, "event_name"),
        ("תאריך האירוע", cfg["demo_date"] if demo else None, DATE, "event_date"),
        ("מקום האירוע / אולם", cfg["demo_venue"] if demo else "", None, "event_venue"),
        ("מחיר מנה (₪, כולל מע\"מ)", cfg["demo_plate"] if demo else None, NIS, "plate_price"),
        ("מינימום מנות בחוזה", cfg["demo_min"] if demo else None, "#,##0", "plate_min"),
        ("תקרת תקציב כוללת (₪)", cfg["demo_cap"] if demo else None, NIS, "budget_cap"),
        ("מתנה ממוצעת צפויה לאורח מגיע (₪)", cfg["demo_gift"] if demo else None, NIS, "gift_avg"),
    ]
    for i, (label, val, fmt, name) in enumerate(rows):
        r = 4 + i
        c = ws.cell(row=r, column=1, value=label)
        style_cell(c, bold=True)
        v = ws.cell(row=r, column=2, value=val)
        style_cell(v, "input", fmt)
        define(wb, name, f"{q(S_SET)}!$B${r}")
    ws["A11"] = "טיפ: את המתנה הממוצעת אפשר להעריך עם המחשבון החינמי שלנו באתר (" + cfg["tool_name"] + ")."
    style_cell(ws["A11"], size=9, color="666666")
    ws.merge_cells("A11:B12")

    # lists
    lists = [
        ("D", "קטגוריות תקציב", [c[0] for c in cfg["categories"]], N_CATS, "lst_cat"),
        ("E", "צדדים", cfg["sides"], 10, "lst_side"),
        ("F", "קבוצות מוזמנים", cfg["groups"], 20, "lst_group"),
        ("G", "סטטוס הגעה", ["מגיעים", "לא מגיעים", "אולי", "טרם ענו"], 4, "lst_rsvp"),
        ("H", "סוג מתנה", ["צ'ק", "מזומן", "העברה בנקאית", "ביט / פייבוקס", "מתנה", "אחר"], 8, "lst_gift"),
        ("I", "סטטוס ספק", ["בבירור", "התקבלה הצעה", "נסגר", "בוטל"], 4, "lst_vstat"),
        ("J", "כן / לא", ["כן", "לא"], 2, "lst_yes"),
        ("K", "אמצעי תשלום", ["העברה בנקאית", "אשראי", "צ'ק", "מזומן", "ביט / פייבוקס"], 8, "lst_paym"),
        ("L", "שלבים", [p for p in cfg["phases"]], 10, "lst_phase"),
    ]
    ws["D3"] = "רשימות (אפשר לערוך ולהוסיף בשורות הריקות)"
    style_cell(ws["D3"], bold=True, color=C_TITLE)
    for col, title, items, size, name in lists:
        h = ws[f"{col}14"]
        h.value = title
        style_cell(h, "head")
        for k in range(size):
            c = ws[f"{col}{15 + k}"]
            c.value = items[k] if k < len(items) else None
            style_cell(c, "input")
        define(wb, name, f"{q(S_SET)}!${col}$15:${col}${15 + size - 1}")
    ws["D13"] = "⚠ שינוי שם של ערך ברשימה לא מעדכן ערכים שכבר נבחרו בגיליונות האחרים."
    style_cell(ws["D13"], size=9, color="996600")
    ws.freeze_panes = "A4"
    return ws


# --------------------------------------------------------------------------- budget
def build_budget(wb, cfg, demo):
    ws = new_sheet(wb, S_BUD, "תקציב לפי קטגוריות",
                   "תכנון (צהוב) מול התחייבות בפועל (נלקח אוטומטית מגיליון ספקים) ומול מה ששולם (מגיליון תשלומים). "
                   "האחוז המקובל הוא כלל אצבע בלבד; ערכו אותו כרצונכם.",
                   [26, 13, 15, 16, 16, 15, 16, 16, 12], tab="70AD47")
    headers(ws, 4, ["קטגוריה", "% מקובל", "הצעה לפי תקרה", "תכנון (₪)", "התחייבות בפועל",
                    "שולם", "יתרה לתשלום", "הפרש מהתכנון", "% מהתכנון"])
    shares = {c[0]: c[1] for c in cfg["categories"]}
    demo_plan = cfg.get("demo_plan", {})
    for k in range(N_CATS):
        r = FIRST + k
        name = cfg["categories"][k][0] if k < len(cfg["categories"]) else None
        ws[f"A{r}"] = f'=IF({q(S_SET)}!D{15 + k}="","",{q(S_SET)}!D{15 + k})'
        ws[f"B{r}"] = shares.get(name) if name else None
        ws[f"C{r}"] = f'=IF(OR(A{r}="",B{r}="",budget_cap=""),"",B{r}*budget_cap)'
        ws[f"D{r}"] = demo_plan.get(name) if (demo and name) else None
        ws[f"E{r}"] = (f'=IF(A{r}="","",SUMIFS({rng(S_VEN,"F",N_VENDORS)},{rng(S_VEN,"B",N_VENDORS)},A{r},'
                       f'{rng(S_VEN,"G",N_VENDORS)},"<>בוטל"))')
        ws[f"F{r}"] = (f'=IF(A{r}="","",SUMIFS({rng(S_PAY,"E",N_PAY)},{rng(S_PAY,"B",N_PAY)},A{r},'
                       f'{rng(S_PAY,"F",N_PAY)},"כן"))')
        ws[f"G{r}"] = f'=IF(A{r}="","",E{r}-F{r})'
        ws[f"H{r}"] = f'=IF(OR(A{r}="",D{r}=""),"",D{r}-E{r})'
        ws[f"I{r}"] = f'=IF(OR(A{r}="",D{r}="",D{r}=0),"",E{r}/D{r})'
        style_cell(ws[f"A{r}"], "calc", bold=True)
        style_cell(ws[f"B{r}"], "input", PCT)
        style_cell(ws[f"C{r}"], "calc", NIS)
        style_cell(ws[f"D{r}"], "input", NIS)
        for col in "EFGH":
            style_cell(ws[f"{col}{r}"], "calc", NIS)
        style_cell(ws[f"I{r}"], "calc", PCT)
    t = FIRST + N_CATS
    ws[f"A{t}"] = "סה\"כ"
    ws[f"B{t}"] = f"=SUM(B{FIRST}:B{t-1})"
    for col in "CDEFG":
        ws[f"{col}{t}"] = f"=SUM({col}{FIRST}:{col}{t-1})"
    ws[f"H{t}"] = f"=D{t}-E{t}"
    ws[f"I{t}"] = f'=IF(D{t}=0,"",E{t}/D{t})'
    for col in "ABCDEFGHI":
        c = ws[f"{col}{t}"]
        style_cell(c, "head", PCT if col in "BI" else (NIS if col != "A" else None))
    define(wb, "bud_total_row", f"{q(S_BUD)}!$A${t}")
    ws.conditional_formatting.add(f"H{FIRST}:H{t}", CellIsRule(operator="lessThan", formula=["0"],
                                  fill=PatternFill("solid", fgColor=C_BAD)))
    ws.conditional_formatting.add(f"I{FIRST}:I{t-1}", DataBarRule(start_type="num", start_value=0,
                                  end_type="num", end_value=1, color="B5838D"))
    ws[f"A{t+2}"] = ("הסבר: \"התחייבות בפועל\" = סכום המחיר הסופי של ספקים בקטגוריה (לא כולל ספקים בסטטוס בוטל). "
                     "ספק בלי מחיר סופי לא נספר עדיין. הפרש שלילי (באדום) = חריגה מהתכנון.")
    ws.merge_cells(f"A{t+2}:I{t+3}")
    style_cell(ws[f"A{t+2}"], size=9, color="666666")
    ws.freeze_panes = "B5"
    return ws, t


# --------------------------------------------------------------------------- guests
def build_guests(wb, cfg, demo):
    ws = new_sheet(wb, S_GST, "רשימת מוזמנים, אישורי הגעה ומתנות",
                   "שורה אחת לכל הזמנה (משפחה / זוג / יחיד). \"מוזמנים\" = כמה אנשים בהזמנה. כשמגיעים פחות, רשמו ב\"מאשרים\" את המספר; "
                   "אם ריק, נספר מספר המוזמנים. העמודות האפורות מחושבות.",
                   [6, 24, 14, 16, 10, 13, 10, 10, 14, 9, 12, 14, 11, 22], tab="4472C4")
    headers(ws, 4, ["#", "שם / משפחה", "צד", "קבוצה", "מוזמנים", "סטטוס הגעה", "מאשרים",
                    "נספרים", "טלפון", "שולחן", "סכום מתנה", "סוג מתנה", "תודה נשלחה", "הערות"])
    demo_rows = cfg["demo_guests"] if demo else []
    for k in range(N_GUESTS):
        r = FIRST + k
        ws[f"A{r}"] = f'=IF(B{r}="","",ROW()-{FIRST - 1})'
        ws[f"H{r}"] = f'=IF(B{r}="","",IF(F{r}="מגיעים",IF(G{r}="",E{r},G{r}),0))'
        if k < len(demo_rows):
            name, side, group, inv, st, conf, table, gift, gtype, thx = demo_rows[k]
            for col, v in zip("BCDEFGJKLM", (name, side, group, inv, st, conf, table, gift, gtype, thx)):
                ws[f"{col}{r}"] = v
        for col in "BCDEFGIJKLMN":
            style_cell(ws[f"{col}{r}"], "input", NIS if col == "K" else None,
                       align="center" if col in "EGJ" else "right")
        style_cell(ws[f"A{r}"], "calc", align="center")
        style_cell(ws[f"H{r}"], "calc", align="center")
    last = FIRST + N_GUESTS - 1
    add_list_validation(ws, "=lst_side", f"C{FIRST}:C{last}")
    add_list_validation(ws, "=lst_group", f"D{FIRST}:D{last}")
    add_list_validation(ws, "=lst_rsvp", f"F{FIRST}:F{last}")
    add_list_validation(ws, "=lst_gift", f"L{FIRST}:L{last}")
    add_list_validation(ws, "=lst_yes", f"M{FIRST}:M{last}")
    num = DataValidation(type="whole", operator="between", formula1="0", formula2="50", allow_blank=True)
    num.error = "מספר שלם בין 0 ל-50"
    ws.add_data_validation(num)
    num.add(f"E{FIRST}:E{last}")
    num.add(f"G{FIRST}:G{last}")
    fill = lambda c: PatternFill("solid", fgColor=c)
    ws.conditional_formatting.add(f"F{FIRST}:F{last}", CellIsRule(operator="equal", formula=['"מגיעים"'], fill=fill(C_OK)))
    ws.conditional_formatting.add(f"F{FIRST}:F{last}", CellIsRule(operator="equal", formula=['"לא מגיעים"'], fill=fill(C_BAD)))
    ws.conditional_formatting.add(f"F{FIRST}:F{last}", CellIsRule(operator="equal", formula=['"אולי"'], fill=fill(C_WARN)))
    ws.conditional_formatting.add(f"M{FIRST}:M{last}",
                                  FormulaRule(formula=[f'AND(K{FIRST}>0,M{FIRST}<>"כן")'], fill=fill(C_WARN)))
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = f"A4:N{last}"
    return ws


# --------------------------------------------------------------------------- vendors
def build_vendors(wb, cfg, demo):
    ws = new_sheet(wb, S_VEN, "ספקים והצעות מחיר",
                   "רושמים כל ספק שבודקים. כשסוגרים, מעדכנים \"מחיר סופי\" ו\"נסגר\" – הסכום נכנס לתקציב. "
                   "\"שולם\" מחושב מגיליון תשלומים (שורות שסומנו \"כן\").",
                   [24, 20, 16, 14, 14, 14, 14, 14, 14, 26], tab="ED7D31")
    headers(ws, 4, ["ספק", "קטגוריה", "איש קשר", "טלפון", "הצעת מחיר", "מחיר סופי",
                    "סטטוס", "שולם", "יתרה", "הערות"])
    demo_rows = cfg["demo_vendors"] if demo else []
    for k in range(N_VENDORS):
        r = FIRST + k
        if k < len(demo_rows):
            for col, v in zip("ABCDEFG", demo_rows[k]):
                ws[f"{col}{r}"] = v
        ws[f"H{r}"] = (f'=IF(A{r}="","",SUMIFS({rng(S_PAY,"E",N_PAY)},{rng(S_PAY,"A",N_PAY)},A{r},'
                       f'{rng(S_PAY,"F",N_PAY)},"כן"))')
        ws[f"I{r}"] = f'=IF(OR(A{r}="",F{r}="",G{r}="בוטל"),"",F{r}-H{r})'
        for col in "ABCDGJ":
            style_cell(ws[f"{col}{r}"], "input")
        for col in "EF":
            style_cell(ws[f"{col}{r}"], "input", NIS)
        for col in "HI":
            style_cell(ws[f"{col}{r}"], "calc", NIS)
    last = FIRST + N_VENDORS - 1
    add_list_validation(ws, "=lst_cat", f"B{FIRST}:B{last}")
    add_list_validation(ws, "=lst_vstat", f"G{FIRST}:G{last}")
    ws.conditional_formatting.add(f"G{FIRST}:G{last}", CellIsRule(operator="equal", formula=['"נסגר"'],
                                  fill=PatternFill("solid", fgColor=C_OK)))
    ws.conditional_formatting.add(f"A{FIRST}:J{last}", FormulaRule(formula=[f'$G{FIRST}="בוטל"'],
                                  font=Font(color="999999", strike=True)))
    define(wb, "lst_vendor", rng(S_VEN, "A", N_VENDORS))
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = f"A4:J{last}"
    return ws


# --------------------------------------------------------------------------- payments
def build_payments(wb, cfg, demo):
    ws = new_sheet(wb, S_PAY, "לוח תשלומים",
                   "כל מקדמה ותשלום בשורה נפרדת. בוחרים ספק מהרשימה (הקטגוריה מתמלאת לבד). "
                   "מסמנים \"כן\" כששולם. שורות באיחור נצבעות באדום, ושורות בשבועיים הקרובים בכתום.",
                   [24, 18, 24, 13, 13, 9, 13, 16, 11, 12], tab="A5A5A5")
    headers(ws, 4, ["ספק", "קטגוריה", "תיאור (מקדמה / תשלום)", "תאריך יעד", "סכום", "שולם?",
                    "תאריך תשלום", "אמצעי תשלום", "ימים ליעד", "מצב"])
    demo_rows = cfg["demo_payments"] if demo else []
    for k in range(N_PAY):
        r = FIRST + k
        if k < len(demo_rows):
            vend, desc, due, amt, paid, pdate, meth = demo_rows[k]
            ws[f"A{r}"], ws[f"C{r}"], ws[f"D{r}"], ws[f"E{r}"] = vend, desc, due, amt
            ws[f"F{r}"], ws[f"G{r}"], ws[f"H{r}"] = paid, pdate, meth
        ws[f"B{r}"] = (f'=IF(A{r}="","",IFERROR(INDEX({rng(S_VEN,"B",N_VENDORS)},'
                       f'MATCH(A{r},{rng(S_VEN,"A",N_VENDORS)},0)),"ספק לא ברשימה"))')
        ws[f"I{r}"] = f'=IF(OR(D{r}="",F{r}="כן"),"",D{r}-TODAY())'
        ws[f"J{r}"] = (f'=IF(A{r}&E{r}="","",IF(F{r}="כן","שולם",IF(D{r}="","ללא תאריך",'
                       f'IF(D{r}<TODAY(),"באיחור",IF(D{r}-TODAY()<=14,"בקרוב","מתוכנן")))))')
        for col in "ACFH":
            style_cell(ws[f"{col}{r}"], "input")
        for col in "DG":
            style_cell(ws[f"{col}{r}"], "input", DATE, align="center")
        style_cell(ws[f"E{r}"], "input", NIS)
        style_cell(ws[f"B{r}"], "calc")
        style_cell(ws[f"I{r}"], "calc", "0", align="center")
        style_cell(ws[f"J{r}"], "calc", align="center")
    last = FIRST + N_PAY - 1
    add_list_validation(ws, "=lst_vendor", f"A{FIRST}:A{last}", "בחרו ספק מגיליון ספקים")
    add_list_validation(ws, "=lst_yes", f"F{FIRST}:F{last}")
    add_list_validation(ws, "=lst_paym", f"H{FIRST}:H{last}")
    dv = DataValidation(type="date", operator="greaterThan", formula1="36526", allow_blank=True)
    dv.error = "יש להזין תאריך (למשל 15/03/2027)"
    ws.add_data_validation(dv)
    dv.add(f"D{FIRST}:D{last}")
    dv.add(f"G{FIRST}:G{last}")
    ws.conditional_formatting.add(f"A{FIRST}:J{last}", FormulaRule(formula=[f'$J{FIRST}="באיחור"'],
                                  fill=PatternFill("solid", fgColor=C_BAD)))
    ws.conditional_formatting.add(f"A{FIRST}:J{last}", FormulaRule(formula=[f'$J{FIRST}="בקרוב"'],
                                  fill=PatternFill("solid", fgColor=C_WARN)))
    ws.conditional_formatting.add(f"J{FIRST}:J{last}", FormulaRule(formula=[f'$J{FIRST}="שולם"'],
                                  fill=PatternFill("solid", fgColor=C_OK)))
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = f"A4:J{last}"
    return ws


# --------------------------------------------------------------------------- checklist
def build_todo(wb, cfg, demo):
    ws = new_sheet(wb, S_TODO, "צ'קליסט ולוח זמנים",
                   "תאריך היעד מחושב לפי תאריך האירוע (גיליון הגדרות) ומספר השבועות לפני. "
                   "אפשר לשנות כל משימה, למחוק או להוסיף בשורות הריקות.",
                   [44, 16, 11, 13, 9, 14, 16, 26], tab="7030A0")
    headers(ws, 4, ["משימה", "שלב", "שבועות לפני", "תאריך יעד", "בוצע", "אחראי/ת", "מצב", "הערות"])
    tasks = cfg["tasks"]
    done_n = cfg.get("demo_done", 0) if demo else 0
    for k in range(N_TODO):
        r = FIRST + k
        if k < len(tasks):
            phase, weeks, text = tasks[k]
            ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"] = text, phase, weeks
            if k < done_n:
                ws[f"E{r}"] = "כן"
        ws[f"D{r}"] = f'=IF(OR(A{r}="",C{r}="",event_date=""),"",event_date-C{r}*7)'
        ws[f"G{r}"] = (f'=IF(A{r}="","",IF(E{r}="כן","✔ בוצע",IF(D{r}="","",IF(D{r}<TODAY(),"באיחור",'
                       f'IF(D{r}-TODAY()<=14,"השבועיים הקרובים","")))))')
        for col in "ABEFH":
            style_cell(ws[f"{col}{r}"], "input")
        style_cell(ws[f"C{r}"], "input", "0", align="center")
        style_cell(ws[f"D{r}"], "calc", DATE, align="center")
        style_cell(ws[f"G{r}"], "calc", align="center")
    last = FIRST + N_TODO - 1
    add_list_validation(ws, "=lst_yes", f"E{FIRST}:E{last}")
    add_list_validation(ws, "=lst_phase", f"B{FIRST}:B{last}")
    ws.conditional_formatting.add(f"A{FIRST}:H{last}", FormulaRule(formula=[f'$E{FIRST}="כן"'],
                                  font=Font(color="7F7F7F"), fill=PatternFill("solid", fgColor=C_OK)))
    ws.conditional_formatting.add(f"G{FIRST}:G{last}", CellIsRule(operator="equal", formula=['"באיחור"'],
                                  fill=PatternFill("solid", fgColor=C_BAD)))
    ws.conditional_formatting.add(f"G{FIRST}:G{last}", CellIsRule(operator="equal", formula=['"השבועיים הקרובים"'],
                                  fill=PatternFill("solid", fgColor=C_WARN)))
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = f"A4:H{last}"
    return ws


# --------------------------------------------------------------------------- seating
def build_seating(wb, cfg, demo):
    ws = new_sheet(wb, S_SEAT, "עוזר הושבה",
                   "בגיליון מוזמנים רושמים מספר שולחן לכל הזמנה. כאן רואים כמה אנשים (נספרים) משובצים בכל שולחן ומתי יש חריגה.",
                   [10, 26, 11, 12, 10, 14, 4, 30, 14], tab="00B0F0")
    headers(ws, 4, ["שולחן", "שם / תיאור", "קיבולת", "משובצים", "פנוי", "מצב"])
    demo_names = cfg.get("demo_tables", {}) if demo else {}
    for k in range(N_TABLES):
        r = FIRST + k
        ws[f"A{r}"] = k + 1
        ws[f"B{r}"] = demo_names.get(k + 1)
        ws[f"C{r}"] = cfg["table_size"]
        ws[f"D{r}"] = f'=SUMIFS({rng(S_GST,"H",N_GUESTS)},{rng(S_GST,"J",N_GUESTS)},A{r})'
        ws[f"E{r}"] = f'=IF(C{r}="","",C{r}-D{r})'
        ws[f"F{r}"] = f'=IF(OR(C{r}="",D{r}=0),"",IF(D{r}>C{r},"חריגה!",IF(D{r}=C{r},"מלא","")))'
        for col in "ABC":
            style_cell(ws[f"{col}{r}"], "input", align="center" if col != "B" else "right")
        for col in "DEF":
            style_cell(ws[f"{col}{r}"], "calc", align="center")
    last = FIRST + N_TABLES - 1
    ws.conditional_formatting.add(f"F{FIRST}:F{last}", CellIsRule(operator="equal", formula=['"חריגה!"'],
                                  fill=PatternFill("solid", fgColor=C_BAD)))
    ws.conditional_formatting.add(f"F{FIRST}:F{last}", CellIsRule(operator="equal", formula=['"מלא"'],
                                  fill=PatternFill("solid", fgColor=C_OK)))
    ws.conditional_formatting.add(f"D{FIRST}:D{last}", DataBarRule(start_type="num", start_value=0,
                                  end_type="num", end_value=cfg["table_size"], color="00B0F0"))
    summary = [
        ("סה\"כ מקומות בשולחנות", f"=SUM(C{FIRST}:C{last})"),
        ("משובצים בשולחנות", f"=SUM(D{FIRST}:D{last})"),
        ("נספרים (מגיעים) בסה\"כ", f"=SUM({rng(S_GST,'H',N_GUESTS)})"),
        ("מגיעים שעוד לא שובצו", f"=I7-I6"),
        ("שולחנות בשימוש", f'=COUNTIF(D{FIRST}:D{last},">0")'),
        ("שולחנות בחריגה", f'=COUNTIF(F{FIRST}:F{last},"חריגה!")'),
    ]
    ws["H4"] = "סיכום"
    style_cell(ws["H4"], "head")
    ws["I4"] = ""
    style_cell(ws["I4"], "head")
    for i, (lab, f) in enumerate(summary):
        r = 5 + i
        ws[f"H{r}"] = lab
        style_cell(ws[f"H{r}"], bold=True)
        ws[f"I{r}"] = f
        style_cell(ws[f"I{r}"], "calc", "#,##0", bold=True, align="center")
    ws["H12"] = "מגיעים שהמספר שלהם לא נמצא ברשימת השולחנות לא נספרים כמשובצים. קיבולת ברירת מחדל: " + str(cfg["table_size"]) + "."
    ws.merge_cells("H12:I14")
    style_cell(ws["H12"], size=9, color="666666")
    ws.freeze_panes = "A5"
    return ws


# --------------------------------------------------------------------------- dashboard
def build_dashboard(wb, cfg, bud_total):
    ws = new_sheet(wb, S_DASH, "דשבורד " + cfg["event_label"],
                   "הכל מחושב אוטומטית מהגיליונות האחרים. אין צורך להקליד כאן.",
                   [30, 18, 4, 30, 18, 4, 22, 14, 14], tab=C_HEAD)
    G, V, P, T = S_GST, S_VEN, S_PAY, S_TODO
    gH, gE, gF, gK, gM, gC = (rng(G, c, N_GUESTS) for c in "HEFKMC")
    kpis_left = [
        ("📅 ימים לאירוע", '=IF(event_date="","הזינו תאריך בהגדרות",event_date-TODAY())', "#,##0"),
        ("💰 תקציב מתוכנן", f"={q(S_BUD)}!D{bud_total}", NIS),
        ("🤝 התחייבויות לספקים", f"={q(S_BUD)}!E{bud_total}", NIS),
        ("✅ שולם עד היום", f"={q(S_BUD)}!F{bud_total}", NIS),
        ("⏳ יתרה לתשלום", f"={q(S_BUD)}!G{bud_total}", NIS),
        ("📊 נותר בתקציב (תכנון − התחייבות)", f"={q(S_BUD)}!H{bud_total}", NIS),
        ("🚨 תשלומים באיחור", f'=COUNTIF({rng(P,"J",N_PAY)},"באיחור")', "#,##0"),
        ("🔔 תשלומים בשבועיים הקרובים (₪)", f'=SUMIFS({rng(P,"E",N_PAY)},{rng(P,"J",N_PAY)},"בקרוב")', NIS),
    ]
    kpis_right = [
        ("✉️ הזמנות (שורות)", f'=COUNTIF({rng(G,"B",N_GUESTS)},"?*")', "#,##0"),
        ("👥 סה\"כ מוזמנים (אנשים)", f"=SUM({gE})", "#,##0"),
        ("🎉 מגיעים (נספרים)", f"=SUM({gH})", "#,##0"),
        ("❔ טרם ענו (אנשים)", f'=SUMIFS({gE},{gF},"טרם ענו")+SUMIFS({gE},{gF},"",{rng(G,"B",N_GUESTS)},"?*")', "#,##0"),
        ("📈 שיעור אישור", f'=IF(SUM({gE})=0,"",SUM({gH})/SUM({gE}))', PCT),
        ("🍽 עלות מנות משוערת", f'=IF(plate_price="","",MAX(SUM({gH}),N(plate_min))*plate_price)', NIS),
        ("🎁 מתנות שהתקבלו", f"=SUM({gK})", NIS),
        ("💌 תודות שטרם נשלחו", f'=COUNTIFS({gK},">0",{gM},"<>כן")', "#,##0"),
    ]
    for col_l, col_v, items in (("A", "B", kpis_left), ("D", "E", kpis_right)):
        for i, (lab, f, fmt) in enumerate(items):
            r = 4 + i
            ws[f"{col_l}{r}"] = lab
            style_cell(ws[f"{col_l}{r}"], bold=True, size=12)
            ws[f"{col_l}{r}"].fill = PatternFill("solid", fgColor="F7EEF2")
            ws[f"{col_l}{r}"].border = BORDER
            ws[f"{col_v}{r}"] = f
            style_cell(ws[f"{col_v}{r}"], "calc", fmt, bold=True, size=13, color=C_TITLE, align="center")
            ws.row_dimensions[r].height = 24
    ws.conditional_formatting.add("B10", CellIsRule(operator="greaterThan", formula=["0"],
                                  fill=PatternFill("solid", fgColor=C_BAD)))
    ws.conditional_formatting.add("B9", CellIsRule(operator="lessThan", formula=["0"],
                                  fill=PatternFill("solid", fgColor=C_BAD)))

    # gifts vs cost box
    ws["G4"] = "מאזן מתנות מול עלות"
    ws.merge_cells("G4:H4")
    style_cell(ws["G4"], "head")
    style_cell(ws["H4"], "head")
    box = [
        ("מתנות צפויות (מגיעים × ממוצע)", f'=IF(gift_avg="","",SUM({gH})*gift_avg)', NIS),
        ("מתנות שהתקבלו בפועל", f"=SUM({gK})", NIS),
        ("התחייבויות לספקים", f"={q(S_BUD)}!E{bud_total}", NIS),
        ("מאזן צפוי (צפויות − התחייבויות)", '=IF(H5="","",H5-H7)', NIS),
        ("מאזן בפועל (התקבלו − התחייבויות)", "=H6-H7", NIS),
        ("ממוצע מתנה לאורח (מי שנרשמה מתנה)", f'=IF(SUMIFS({gH},{gK},">0")=0,"",SUM({gK})/SUMIFS({gH},{gK},">0"))', NIS),
    ]
    for i, (lab, f, fmt) in enumerate(box):
        r = 5 + i
        ws[f"G{r}"] = lab
        style_cell(ws[f"G{r}"], bold=True, size=10)
        ws[f"G{r}"].border = BORDER
        ws[f"H{r}"] = f
        style_cell(ws[f"H{r}"], "calc", fmt, bold=True, align="center")
    ws.conditional_formatting.add("H8:H9", CellIsRule(operator="lessThan", formula=["0"],
                                  fill=PatternFill("solid", fgColor=C_BAD)))
    ws.conditional_formatting.add("H8:H9", CellIsRule(operator="greaterThanOrEqual", formula=["0"],
                                  fill=PatternFill("solid", fgColor=C_OK)))
    ws["G11"] = "✔ משימות שבוצעו"
    style_cell(ws["G11"], bold=True)
    ws["H11"] = (f'=IF(COUNTIF({rng(T,"A",N_TODO)},"?*")=0,"",COUNTIFS({rng(T,"A",N_TODO)},"?*",'
                 f'{rng(T,"E",N_TODO)},"כן")/COUNTIF({rng(T,"A",N_TODO)},"?*"))')
    style_cell(ws["H11"], "calc", PCT, bold=True, align="center")
    ws["G12"] = "⚠ משימות באיחור"
    style_cell(ws["G12"], bold=True)
    ws["H12"] = f'=COUNTIF({rng(T,"G",N_TODO)},"באיחור")'
    style_cell(ws["H12"], "calc", "#,##0", bold=True, align="center")

    # helper tables for charts (row 40+)
    h = 40
    ws[f"A{h-1}"] = "טבלאות עזר לגרפים (מחושבות)"
    style_cell(ws[f"A{h-1}"], bold=True, color="999999")
    headers_row = [("A", "סטטוס הגעה"), ("B", "אנשים")]
    for col, t in headers_row:
        ws[f"{col}{h}"] = t
        style_cell(ws[f"{col}{h}"], "head")
    statuses = ["מגיעים", "לא מגיעים", "אולי", "טרם ענו"]
    for i, s in enumerate(statuses):
        r = h + 1 + i
        ws[f"A{r}"] = s
        style_cell(ws[f"A{r}"], "calc")
        if s == "טרם ענו":
            ws[f"B{r}"] = f'=SUMIFS({gE},{gF},"טרם ענו")+SUMIFS({gE},{gF},"",{rng(G,"B",N_GUESTS)},"?*")'
        else:
            ws[f"B{r}"] = f'=SUMIFS({gE},{gF},"{s}")'
        style_cell(ws[f"B{r}"], "calc", "#,##0")
    for col, t in (("D", "צד"), ("E", "מוזמנים"), ("F", "מגיעים")):
        ws[f"{col}{h}"] = t
        style_cell(ws[f"{col}{h}"], "head")
    n_sides = 10
    for i in range(n_sides):
        r = h + 1 + i
        ws[f"D{r}"] = f'=IF({q(S_SET)}!E{15+i}="","",{q(S_SET)}!E{15+i})'
        ws[f"E{r}"] = f'=IF(D{r}="","",SUMIFS({gE},{gC},D{r}))'
        ws[f"F{r}"] = f'=IF(D{r}="","",SUMIFS({gH},{gC},D{r}))'
        for col in "DEF":
            style_cell(ws[f"{col}{r}"], "calc", "#,##0" if col != "D" else None)
    n_side_rows = len(cfg["sides"])

    # charts
    bar = BarChart()
    bar.type = "bar"
    bar.style = 10
    bar.title = "תכנון מול התחייבות לפי קטגוריה"
    bar.y_axis.title = "₪"
    bar.y_axis.numFmt = '#,##0'
    n_c = len(cfg["categories"])
    data = Reference(wb[S_BUD], min_col=4, max_col=5, min_row=4, max_row=4 + n_c)
    cats = Reference(wb[S_BUD], min_col=1, min_row=5, max_row=4 + n_c)
    bar.add_data(data, titles_from_data=True)
    bar.set_categories(cats)
    bar.height, bar.width = 11, 17
    bar.series[0].graphicalProperties.solidFill = "D9C2CC"
    bar.series[1].graphicalProperties.solidFill = C_HEAD
    bar.x_axis.delete = False
    bar.y_axis.delete = False
    bar.legend.position = "b"
    ws.add_chart(bar, "A14")

    pie = PieChart()
    pie.title = "אישורי הגעה (אנשים)"
    pie.add_data(Reference(ws, min_col=2, min_row=h, max_row=h + 4), titles_from_data=True)
    pie.set_categories(Reference(ws, min_col=1, min_row=h + 1, max_row=h + 4))
    pie.height, pie.width = 7.2, 10
    pie.dataLabels = DataLabelList()
    pie.dataLabels.showVal = False
    pie.dataLabels.showPercent = True
    pie.dataLabels.showCatName = False
    pie.dataLabels.showSerName = False
    pie.dataLabels.showLegendKey = False
    from openpyxl.chart.series import DataPoint
    for idx, colr in enumerate(["70AD47", "E06666", "FFC000", "BFBFBF"]):
        pt = DataPoint(idx=idx)
        pt.graphicalProperties.solidFill = colr
        pie.series[0].dPt.append(pt)
    ws.add_chart(pie, "G14")

    sides = BarChart()
    sides.type = "col"
    sides.title = "מוזמנים ומגיעים לפי צד"
    sides.add_data(Reference(ws, min_col=5, max_col=6, min_row=h, max_row=h + n_side_rows), titles_from_data=True)
    sides.set_categories(Reference(ws, min_col=4, min_row=h + 1, max_row=h + n_side_rows))
    sides.height, sides.width = 8, 10
    sides.series[0].graphicalProperties.solidFill = "D9C2CC"
    sides.series[1].graphicalProperties.solidFill = C_HEAD
    sides.x_axis.delete = False
    sides.y_axis.delete = False
    sides.legend.position = "b"
    ws.add_chart(sides, "G29")
    return ws


# --------------------------------------------------------------------------- help
def build_help(wb, cfg):
    ws = new_sheet(wb, S_HELP, cfg["product_title"],
                   cfg["product_subtitle"], [4, 100], tab="C00000")
    lines = cfg["help"] + [
        "",
        "## מקרא צבעים",
        "▮ צהוב = תא קלט: כאן מקלידים.",
        "▮ אפור = תא מחושב: לא צריך לגעת (נוסחה).",
        "▮ ירוק / כתום / אדום בטבלאות = בוצע / בקרוב / באיחור או חריגה.",
        "",
        "## Google Sheets",
        "הקובץ עובד ב-Excel וגם ב-Google Sheets: מעלים את הקובץ ל-Google Drive ‏← לחיצה ימנית ‏← \"פתיחה באמצעות Google Sheets\" "
        "(או ב-Sheets: קובץ ‏← ייבוא). הנוסחאות והרשימות עובדות; ייתכנו הבדלים קטנים בעיצוב הגרפים.",
        "",
        "## חשוב לדעת",
        "הסכומים המקובלים והאחוזים בקובץ הם כללי אצבע להתמצאות בלבד. מחירים בפועל משתנים לפי ספק, אזור ועונה – "
        "תמיד בקשו הצעות מחיר כתובות.",
        "הקובץ לשימוש אישי של הרוכשים. אין בו פקודות מאקרו.",
        "גרסה " + cfg["version"] + " · תכנון פלוס – קבצים ומחשבונים חכמים בעברית",
    ]
    r = 4
    for line in lines:
        c = ws.cell(row=r, column=2)
        if line.startswith("## "):
            c.value = line[3:]
            style_cell(c, bold=True, size=13, color=C_HEAD)
            ws.row_dimensions[r].height = 24
        else:
            c.value = line
            style_cell(c, size=11)
            if len(line) > 95:
                ws.row_dimensions[r].height = 15 * (len(line) // 95 + 1)
        r += 1
    # colour swatches next to legend lines
    for row in ws.iter_rows(min_row=4, max_row=r, min_col=2, max_col=2):
        cell = row[0]
        if isinstance(cell.value, str) and cell.value.startswith("▮ צהוב"):
            ws.cell(row=cell.row, column=1).fill = PatternFill("solid", fgColor=C_INPUT)
        if isinstance(cell.value, str) and cell.value.startswith("▮ אפור"):
            ws.cell(row=cell.row, column=1).fill = PatternFill("solid", fgColor=C_CALC)
    return ws


def build_workbook(cfg, demo=False):
    wb = Workbook()
    wb.remove(wb.active)
    build_help(wb, cfg)
    build_settings(wb, cfg, demo)
    # dashboard placeholder position: create later but move to index 2
    _, bud_total = build_budget(wb, cfg, demo)
    build_guests(wb, cfg, demo)
    build_vendors(wb, cfg, demo)
    build_payments(wb, cfg, demo)
    build_todo(wb, cfg, demo)
    build_seating(wb, cfg, demo)
    dash = build_dashboard(wb, cfg, bud_total)
    wb.move_sheet(dash, offset=-(len(wb.sheetnames) - 2))
    wb.active = wb.sheetnames.index(S_DASH if demo else S_HELP)
    for ws in wb.worksheets:
        ws.sheet_view.tabSelected = (ws.title == wb.active.title)
        ws.page_setup.orientation = "landscape"
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.properties.title = cfg["product_title"]
    wb.properties.creator = "תכנון פלוס"
    wb.calculation.fullCalcOnLoad = True
    return wb
