#!/usr/bin/env python3
"""Free sample: "mini wedding budget" (1 sheet, real formulas, RTL, branded, links to the full planner).

    python3 tools/convert/make_mini_budget.py   -> docs/samples/mini-wedding-budget.xlsx
"""
import pathlib
import sys

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "site"))
from site_config import BASE_URL, BRAND, BRAND_LATIN  # noqa: E402

OUT = REPO / "docs" / "samples" / "mini-wedding-budget.xlsx"
TEAL, TEAL_L, INPUT, GREY = "0E6B63", "E3F2F0", "FFF6D6", "F4F5F7"
thin = Side(style="thin", color="D0D5DB")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
ILS = '#,##0 "₪";[Red]-#,##0 "₪"'
FONT = "Arial"

# (category, planned formula or default, committed example, paid example)
ROWS = [
    ("אולם וקייטרינג (מוזמנים × מחיר מנה)", "=$C$5*$C$6", 0, 0),
    ("צילום ווידאו", 9000, 0, 0),
    ("DJ / מוזיקה", 6500, 0, 0),
    ("שמלה, חליפה ואביזרים", 8000, 0, 0),
    ("איפור ושיער", 3000, 0, 0),
    ("עיצוב ופרחים (מעבר לחבילת האולם)", 5000, 0, 0),
    ("רב / עורך טקס ורבנות", 2500, 0, 0),
    ("הזמנות, אישורי הגעה והסעות", 3000, 0, 0),
    ("טבעות", 4000, 0, 0),
    ("שונות ובלת\"מ (כ-5%)", "=ROUND(SUM(C10:C18)*0.05,-2)", 0, 0),
]


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "תקציב חתונה"
    ws.sheet_view.rightToLeft = True
    ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (3, 38, 16, 16, 16, 16, 18)):
        ws.column_dimensions[col].width = w

    def cell(ref, value, bold=False, size=11, color="1F2937", fill=None, fmt=None, align="right", wrap=False, border=False):
        c = ws[ref]
        c.value = value
        c.font = Font(name=FONT, bold=bold, size=size, color=color)
        c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap, readingOrder=2)
        if fill:
            c.fill = PatternFill("solid", fgColor=fill)
        if fmt:
            c.number_format = fmt
        if border:
            c.border = BOX
        return c

    # header band
    for r in (1, 2):
        for col in "BCDEFG":
            ws[f"{col}{r}"].fill = PatternFill("solid", fgColor=TEAL)
    cell("B1", "תקציב חתונה מקוצר – דוגמה חינם", bold=True, size=16, color="FFFFFF", fill=TEAL)
    cell("B2", f"{BRAND} · {BASE_URL.replace('https://', '').rstrip('/')} · ממלאים רק את התאים הצהובים", size=10, color="FFFFFF", fill=TEAL)
    ws.row_dimensions[1].height = 30

    # inputs
    cell("B4", "הנתונים שלכם", bold=True, size=12, color=TEAL)
    inputs = [("מספר מוזמנים (מבוגרים)", 250, "#,##0"), ("מחיר מנה (₪, כולל מע\"מ)", 380, ILS),
              ("תקציב יעד כולל (₪)", 160000, ILS), ("מתנה ממוצעת לאורח (₪) – הערכה", 400, ILS)]
    for i, (label, val, fmt) in enumerate(inputs):
        r = 5 + i
        cell(f"B{r}", label, border=True)
        cell(f"C{r}", val, fill=INPUT, fmt=fmt, align="center", border=True, bold=True)
    dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="100000000", allow_blank=True,
                        showErrorMessage=True, errorTitle="מספר בלבד", error="הזינו מספר חיובי (בלי טקסט).")
    ws.add_data_validation(dv)
    dv.add("C5:C8")

    # table
    hdr = ["קטגוריה", "מתוכנן", "התחייבות בפועל", "שולם", "יתרה לתשלום", "מעל / מתחת לתכנון"]
    for col, h in zip("BCDEFG", hdr):
        cell(f"{col}9", h, bold=True, color="FFFFFF", fill=TEAL, align="center", border=True, wrap=True)
    ws.row_dimensions[9].height = 32
    first, last = 10, 9 + len(ROWS)
    for i, (name, planned, committed, paid) in enumerate(ROWS):
        r = first + i
        band = GREY if i % 2 else None
        cell(f"B{r}", name, fill=band, border=True)
        cell(f"C{r}", planned, fill=INPUT, fmt=ILS, align="center", border=True)
        cell(f"D{r}", committed or None, fill=INPUT, fmt=ILS, align="center", border=True)
        cell(f"E{r}", paid or None, fill=INPUT, fmt=ILS, align="center", border=True)
        cell(f"F{r}", f"=MAX(0,D{r}-E{r})", fill=band, fmt=ILS, align="center", border=True)
        cell(f"G{r}", f'=IF(D{r}="","",D{r}-C{r})', fill=band, fmt=ILS, align="center", border=True)
    dv.add(f"C{first}:E{last}")
    t = last + 1
    cell(f"B{t}", "סה\"כ", bold=True, fill=TEAL_L, border=True)
    for col in "CDEF":
        cell(f"{col}{t}", f"=SUM({col}{first}:{col}{last})", bold=True, fill=TEAL_L, fmt=ILS, align="center", border=True)
    cell(f"G{t}", f"=SUM(G{first}:G{last})", bold=True, fill=TEAL_L, fmt=ILS, align="center", border=True)

    # summary
    s = t + 2
    cell(f"B{s}", "סיכום", bold=True, size=12, color=TEAL)
    summary = [
        ("תכנון מול תקציב היעד", f"=$C$7-C{t}", "חיובי = נשאר מרווח; שלילי (אדום) = התכנון חורג מהיעד"),
        ("עלות למוזמן (לפי התכנון)", f"=IF($C$5>0,C{t}/$C$5,0)", ""),
        ("הערכת מתנות (מוזמנים × מתנה ממוצעת)", "=$C$5*$C$8", "הערכה בלבד; בפועל תלוי בכמה מגיעים ובמתנה"),
        ("עלות נטו אחרי מתנות (הערכה)", f"=C{t}-C{s + 3}", ""),
        ("שולם עד עכשיו מתוך ההתחייבויות", f'=IF(D{t}>0,E{t}/D{t},0)', ""),
    ]
    for i, (label, f, note) in enumerate(summary):
        r = s + 1 + i
        cell(f"B{r}", label, border=True)
        cell(f"C{r}", f, bold=True, fmt="0%" if i == 4 else ILS, align="center", border=True)
        if note:
            cell(f"D{r}", note, size=9, color="6B7280")
    end = s + 1 + len(summary)

    red = Font(name=FONT, color="B42318", bold=True)
    ws.conditional_formatting.add(f"G{first}:G{t}", CellIsRule(operator="greaterThan", formula=["0"], font=red,
                                                                 fill=PatternFill("solid", fgColor="FDECEC")))
    ws.conditional_formatting.add(f"C{s + 1}", CellIsRule(operator="lessThan", formula=["0"], font=red,
                                                           fill=PatternFill("solid", fgColor="FDECEC")))
    ws.conditional_formatting.add(f"C{t}", FormulaRule(formula=[f"C{t}>$C$7"], font=red))

    # how-to + upsell
    h = end + 1
    cell(f"B{h}", "איך משתמשים", bold=True, size=12, color=TEAL)
    tips = ["1. משנים את 4 הנתונים למעלה: מספר המוזמנים ומחיר המנה מחשבים לבד את שורת האולם.",
            "2. מעדכנים \"מתוכנן\" לכל קטגוריה. כשסוגרים ספק כותבים את הסכום ב\"התחייבות בפועל\", וכל תשלום ב\"שולם\".",
            "3. אדום = חריגה מהתכנון. המספרים הם דוגמה ונקודת פתיחה בלבד, לא הצעת מחיר או ייעוץ.",
            "מחירים מקובלים לפי ספק: " + BASE_URL + "chatuna/mechirim/"]
    for i, tip in enumerate(tips):
        cell(f"B{h + 1 + i}", tip, size=10)
        ws.merge_cells(f"B{h + 1 + i}:G{h + 1 + i}")
    u = h + len(tips) + 2
    for col in "BCDEFG":
        ws[f"{col}{u}"].fill = PatternFill("solid", fgColor=TEAL_L)
        ws[f"{col}{u + 1}"].fill = PatternFill("solid", fgColor=TEAL_L)
    cell(f"B{u}", "רוצים את כל החתונה בקובץ אחד?", bold=True, size=12, color=TEAL, fill=TEAL_L)
    cell(f"B{u + 1}", "המתכנן המלא (₪49): 13 קטגוריות, ספקים ולוח תשלומים, מוזמנים ואישורי הגעה, צ'קים ומתנות, צ'קליסט והושבה ←",
         size=10, fill=TEAL_L)
    ws.merge_cells(f"B{u + 1}:G{u + 1}")
    link = ws[f"B{u + 1}"]
    link.hyperlink = BASE_URL + "p/wedding-planner/?utm_source=sample&utm_medium=xlsx"
    link.font = Font(name=FONT, size=10, color="0B57D0", underline="single")

    ws.freeze_panes = "A4"
    ws.print_area = f"A1:G{u + 1}"
    ws.page_setup.orientation = "portrait"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.properties.creator = BRAND_LATIN
    wb.properties.title = "Mini wedding budget (sample)"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print("wrote", OUT.relative_to(REPO))


if __name__ == "__main__":
    main()
