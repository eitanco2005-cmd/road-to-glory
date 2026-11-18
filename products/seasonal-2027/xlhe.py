"""Small openpyxl helpers for the Hebrew RTL seasonal workbooks (Purim / Pesach 2027).
Conventions (same as the rest of the shop): yellow = input, grey-blue = formula, navy headers, RTL sheets, no macros."""
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

INPUT = PatternFill("solid", fgColor="FFF4C2")
HEAD = PatternFill("solid", fgColor="173A66")
SUB = PatternFill("solid", fgColor="DCE8F6")
CALC = PatternFill("solid", fgColor="F3F6FA")
OKF = PatternFill("solid", fgColor="DFF3E4")
WARN = PatternFill("solid", fgColor="FBE3E1")
THIN = Side(style="thin", color="B8C4D2")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WHITE_B = Font(name="Arial", bold=True, color="FFFFFF", size=11)
TITLE = Font(name="Arial", bold=True, size=18, color="173A66")
BOLD = Font(name="Arial", bold=True)
BASE = Font(name="Arial", size=11)
MUTED = Font(name="Arial", size=10, color="5B6B7C", italic=True)
CUR = '"₪"#,##0'
CUR2 = '"₪"#,##0.00'
DATE = "dd/mm/yyyy"
FOOT = "© 2026 תכנון פלוס · tichnun.netlify.app · לשימוש אישי ומשפחתי"


def q(name):
    return "'" + name + "'"


def book(names):
    wb = Workbook()
    wss = [wb.active] + [wb.create_sheet() for _ in names[1:]]
    for ws, n in zip(wss, names):
        ws.title = n
        ws.sheet_view.rightToLeft = True
        ws.sheet_view.showGridLines = False
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.page_setup.orientation = "landscape"
    return wb, wss


def widths(ws, ws_widths):
    for col, w in ws_widths.items():
        ws.column_dimensions[col].width = w


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = TITLE
    ws.row_dimensions[1].height = 30
    if sub:
        ws["A2"] = sub
        ws["A2"].font = MUTED


def cell(ws, ref, value=None, kind=None, fmt=None, bold=False, align=None, wrap=False):
    c = ws[ref]
    if value is not None:
        c.value = value
    c.border = BOX
    c.font = BOLD if bold else BASE
    if kind == "in":
        c.fill = INPUT
    elif kind == "calc":
        c.fill = CALC
    elif kind == "sub":
        c.fill = SUB
        c.font = BOLD
    if fmt:
        c.number_format = fmt
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    return c


def head(ws, row, names, col0=1, height=30):
    for i, n in enumerate(names):
        c = ws.cell(row=row, column=col0 + i, value=n)
        c.fill, c.font, c.border = HEAD, WHITE_B, BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = height


def dv_list(ws, src, rng, prompt=None):
    """src: list of strings or a formula like =$A$1:$A$9"""
    f = src if isinstance(src, str) else '"' + ",".join(src) + '"'
    dv = DataValidation(type="list", formula1=f, allow_blank=True, showDropDown=False)
    dv.error = "בחרו ערך מהרשימה"
    dv.errorTitle = "ערך לא ברשימה"
    if prompt:
        dv.prompt = prompt
    dv.add(rng)
    ws.add_data_validation(dv)


def dv_num(ws, rng, lo=0, hi=100000, whole=False):
    dv = DataValidation(type="whole" if whole else "decimal", operator="between", formula1=str(lo), formula2=str(hi), allow_blank=True)
    dv.error = f"מספר בין {lo} ל-{hi}"
    dv.add(rng)
    ws.add_data_validation(dv)


def dv_date(ws, rng):
    dv = DataValidation(type="date", operator="greaterThan", formula1="36526", allow_blank=True)
    dv.error = "הקלידו תאריך, למשל 23/03/2027"
    dv.add(rng)
    ws.add_data_validation(dv)


def cf_fill(ws, rng, formula, fill):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[formula], fill=fill))


def instructions(ws, heading, intro, blocks):
    """blocks: [(section title, [(key, text)…])]"""
    title(ws, heading)
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 100
    ws["A3"] = intro
    ws["A3"].font = BASE
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:B3")
    ws.row_dimensions[3].height = 48
    r = 5
    for sec, rows in blocks:
        for col in (1, 2):
            ws.cell(row=r, column=col).fill = HEAD
        ws.cell(row=r, column=1, value=sec).font = WHITE_B
        r += 1
        for k, v in rows:
            ws.cell(row=r, column=1, value=k).font = BOLD
            c = ws.cell(row=r, column=2, value=v)
            c.font = BASE
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r].height = max(18, 16 * (1 + len(v) // 95))
            r += 1
        r += 1
    ws.cell(row=r, column=1).fill = INPUT
    ws.cell(row=r, column=2, value="תא צהוב: כאן מקלידים").font = BASE
    ws.cell(row=r + 1, column=1).fill = CALC
    ws.cell(row=r + 1, column=2, value="תא אפור-כחלחל: נוסחה, מחושב לבד (לא צריך לגעת)").font = BASE
    ws.cell(row=r + 3, column=2, value=FOOT).font = MUTED
    return r + 3


def kpi(ws, row, label, formula, fmt=None, note=None):
    cell(ws, f"A{row}", label, "sub")
    cell(ws, f"B{row}", formula, "calc", fmt, bold=True, align="center")
    if note:
        ws[f"C{row}"] = note
        ws[f"C{row}"].font = MUTED


def bar(ws, anchor, ttl, data_ws, cats, vals, col_title=True, w=16, h=8, horizontal=True, number_format=None):
    ch = BarChart()
    ch.type = "bar" if horizontal else "col"
    ch.title = ttl
    ch.style = 10
    ch.legend = None
    ch.add_data(vals, titles_from_data=col_title)
    ch.set_categories(cats)
    ch.width, ch.height = w, h
    ch.dataLabels = DataLabelList(showVal=True, showCatName=False, showSerName=False, showLegendKey=False, showPercent=False)
    if number_format:
        ch.dataLabels.numFmt = number_format
    ws.add_chart(ch, anchor)
    return ch


def pie(ws, anchor, ttl, cats, vals, w=11, h=8):
    ch = PieChart()
    ch.title = ttl
    ch.add_data(vals, titles_from_data=True)
    ch.set_categories(cats)
    ch.width, ch.height = w, h
    ch.legend = None
    ch.dataLabels = DataLabelList(showPercent=True, showCatName=True, showVal=False, showSerName=False, showLegendKey=False)
    ws.add_chart(ch, anchor)
    return ch


def props(wb, ttl, subject):
    wb.properties.title = ttl
    wb.properties.subject = subject
    wb.properties.creator = "תכנון פלוס"
    wb.properties.keywords = "tichnun.netlify.app"


__all__ = [n for n in dir() if not n.startswith("_")] + ["Reference", "Alignment", "Font"]
