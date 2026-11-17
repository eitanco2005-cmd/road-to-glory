"""Shared openpyxl helpers for the English (LTR, USD) Jewish-life planners.

Conventions: yellow = input, grey = formula, navy header row. Data rows start at FIRST.
Only functions that work in Excel 2016+, Excel 365, Google Sheets and LibreOffice (SUMIFS, COUNTIFS, IFERROR,
INDEX/MATCH, ROUNDUP). No macros, no dynamic arrays.
"""
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

FONT = "Calibri"
C_HEAD = "1F3A5F"
C_TITLE = "1F3A5F"
C_INPUT = "FFF4CC"
C_CALC = "EEF1F5"
C_OK = "D8F0DC"
C_WARN = "FFE0B2"
C_BAD = "F8D0D0"
C_GOLD = "C9A227"
thin = Side(style="thin", color="D0D5DD")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
USD = '"$"#,##0;[Red]-"$"#,##0;"-"'
USD2 = '"$"#,##0.00;[Red]-"$"#,##0.00;"-"'
DATE = "ddd, mmm d, yyyy"
PCT = "0%"
NUM = "#,##0;-#,##0;\"-\""
NUM1 = "#,##0.0;-#,##0.0;\"-\""
FIRST = 5
BRAND = "Tichnun Plus"
SITE = "https://tichnun.netlify.app/en/"


def q(sheet):
    return "'" + sheet.replace("'", "''") + "'"


def col(sheet, letter, n):
    """Absolute data-column range on a list sheet."""
    return f"{q(sheet)}!${letter}${FIRST}:${letter}${FIRST + n - 1}"


def style(c, kind=None, fmt=None, bold=False, size=11, color="1D2A2E", align="left", wrap=True, italic=False):
    c.font = Font(name=FONT, bold=bold, size=size, color=color, italic=italic)
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if kind == "input":
        c.fill = PatternFill("solid", fgColor=C_INPUT)
        c.border = BORDER
    elif kind == "calc":
        c.fill = PatternFill("solid", fgColor=C_CALC)
        c.border = BORDER
    elif kind == "head":
        c.fill = PatternFill("solid", fgColor=C_HEAD)
        c.font = Font(name=FONT, bold=True, size=11, color="FFFFFF")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
    elif kind == "total":
        c.fill = PatternFill("solid", fgColor="DCE3EC")
        c.font = Font(name=FONT, bold=True, size=11, color=C_TITLE)
        c.border = BORDER
    if fmt:
        c.number_format = fmt
    return c


def put(ws, ref, value, kind=None, fmt=None, **kw):
    c = ws[ref]
    c.value = value
    return style(c, kind, fmt, **kw)


def new_book():
    wb = Workbook()
    wb.remove(wb.active)
    return wb


def sheet(wb, name, title, subtitle, widths, tab=None):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 100
    if tab:
        ws.sheet_properties.tabColor = tab
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    last = get_column_letter(max(len(widths), 2))
    ws.merge_cells(f"A1:{last}1")
    put(ws, "A1", title, bold=True, size=18, color=C_TITLE)
    ws.row_dimensions[1].height = 30
    ws.merge_cells(f"A2:{last}2")
    put(ws, "A2", subtitle, size=10, color="5B6770")
    ws.row_dimensions[2].height = 30
    return ws


def headers(ws, row, names, height=32):
    for i, h in enumerate(names, start=1):
        style(ws.cell(row=row, column=i, value=h), "head")
    ws.row_dimensions[row].height = height
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def blank_rows(ws, first, n, kinds, fmts=None):
    """Paint n empty rows: kinds[i] in {'input','calc',None}."""
    fmts = fmts or {}
    for r in range(first, first + n):
        for i, k in enumerate(kinds, start=1):
            c = ws.cell(row=r, column=i)
            style(c, k, fmts.get(i))


def dv_list(ws, formula, cells, prompt=None, strict=False):
    dv = DataValidation(type="list", formula1=formula, allow_blank=True, showDropDown=False)
    dv.error = "Pick a value from the list (you can edit the lists on the Settings sheet)."
    dv.errorTitle = "Not in the list"
    dv.errorStyle = "stop" if strict else "warning"
    if prompt:
        dv.prompt = prompt
        dv.showInputMessage = True
    ws.add_data_validation(dv)
    dv.add(cells)


def dv_number(ws, cells, minimum=0):
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1=str(minimum), allow_blank=True)
    dv.error = f"Enter a number (≥ {minimum})."
    dv.errorStyle = "warning"
    ws.add_data_validation(dv)
    dv.add(cells)


def define(wb, name, ref):
    wb.defined_names[name] = DefinedName(name, attr_text=ref)


def cf(ws, rng, formula, fill, bold=False):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[formula], fill=PatternFill("solid", fgColor=fill),
                                                   font=Font(bold=bold) if bold else None))


def instructions(wb, title, intro, steps, notes, sheets):
    ws = wb.create_sheet("Start Here", 0)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = C_GOLD
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 92
    ws.merge_cells("B1:C1")
    put(ws, "B1", title, bold=True, size=20, color=C_TITLE)
    ws.row_dimensions[1].height = 36
    ws.merge_cells("B2:C2")
    put(ws, "B2", intro, size=11, color="333333")
    ws.row_dimensions[2].height = 48
    r = 4
    put(ws, f"B{r}", "Quick start", bold=True, size=14, color=C_TITLE)
    r += 1
    for i, s in enumerate(steps, start=1):
        put(ws, f"B{r}", f"Step {i}", bold=True)
        put(ws, f"C{r}", s)
        ws.row_dimensions[r].height = 34
        r += 1
    r += 1
    put(ws, f"B{r}", "Colour key", bold=True, size=14, color=C_TITLE)
    r += 1
    put(ws, f"B{r}", "Yellow cells", "input", bold=True)
    put(ws, f"C{r}", "Type here. Drop-down lists come from the Settings sheet, where you can rename or add options.")
    r += 1
    put(ws, f"B{r}", "Grey cells", "calc", bold=True)
    put(ws, f"C{r}", "Calculated for you. Please don't type over them (if you do by mistake, press Ctrl+Z / Cmd+Z).")
    r += 2
    put(ws, f"B{r}", "What's inside", bold=True, size=14, color=C_TITLE)
    r += 1
    for name, desc in sheets:
        put(ws, f"B{r}", name, bold=True)
        put(ws, f"C{r}", desc)
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1
    put(ws, f"B{r}", "Good to know", bold=True, size=14, color=C_TITLE)
    r += 1
    for n in notes + [
        "Works in Excel 2016 or newer, Excel 365, Excel for Mac/phone, Google Sheets (File → Import, or upload to "
        "Drive and open with Google Sheets) and LibreOffice. No macros, no add-ins.",
        "Amounts are in US dollars. Change the currency format with Format Cells if you need another currency.",
        "Example figures are rough guides only, not financial or religious advice. Follow your family's and your "
        "rabbi's customs.",
        f"Made by {BRAND} · {SITE} · Personal use licence: please don't resell or share the file publicly.",
    ]:
        ws.merge_cells(f"B{r}:C{r}")
        put(ws, f"B{r}", "• " + n)
        ws.row_dimensions[r].height = 32
        r += 1
    return ws


def kpi(ws, row, label, formula, fmt=None, col_label="A", col_val="B", note=None):
    put(ws, f"{col_label}{row}", label, bold=True)
    put(ws, f"{col_val}{row}", formula, "calc", fmt, bold=True, size=12, align="right")
    if note:
        nc = chr(ord(col_val) + 1)
        put(ws, f"{nc}{row}", note, size=9, color="6B7780", italic=True)
    ws.row_dimensions[row].height = 22


def bar_chart(ws, anchor, title, cats_ref, data_refs, titles_from_data=True, width=17, height=8.5, horizontal=True,
              y_title=None, stacked=False, money=True):
    ch = BarChart()
    ch.type = "bar" if horizontal else "col"
    ch.style = 10
    ch.title = title
    for d in data_refs:
        ch.add_data(d, titles_from_data=titles_from_data)
    ch.set_categories(cats_ref)
    ch.width, ch.height = width, height
    if money:
        ch.y_axis.number_format = '"$"#,##0'
    if y_title:
        ch.y_axis.title = y_title
    if stacked:
        ch.grouping = "stacked"
        ch.overlap = 100
    ch.legend.position = "b"
    ws.add_chart(ch, anchor)
    return ch


def pie_chart(ws, anchor, title, cats_ref, data_ref, width=11, height=8.5):
    ch = PieChart()
    ch.title = title
    ch.add_data(data_ref, titles_from_data=False)
    ch.set_categories(cats_ref)
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.dataLabels.showPercent = False
    ch.dataLabels.showSerName = False
    ch.dataLabels.showCatName = False
    ch.dataLabels.showLegendKey = False
    ch.width, ch.height = width, height
    ch.legend.position = "r"
    ws.add_chart(ch, anchor)
    return ch


def props(wb, title, subject):
    wb.properties.title = title
    wb.properties.subject = subject
    wb.properties.creator = BRAND
    wb.properties.keywords = "planner, spreadsheet, Excel, Google Sheets, Jewish"


__all__ = [n for n in dir() if not n.startswith("_")] + ["Reference", "get_column_letter"]
