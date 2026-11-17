"""Build the Hebrew price-quote template pack (הצעת מחיר): 1 x .xlsx (5 designs, auto VAT) + 5 x .docx.

Usage: python3 build.py  [--example]   (example fills demo values for screenshots)
VAT rate: 18% from 1.1.2025 (צו מס ערך מוסף, raised from 17%); still 18% when checked 17.11.2026.
A price quote is NOT a tax invoice / receipt. Stated in every design.
"""
import datetime as dt
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

HERE = Path(__file__).parent
VAT = 0.18
CHECKED = "17.11.2026"
VAT_SOURCE = "שיעור המע\"מ 18% בתוקף מ-1.1.2025 (צו מס ערך מוסף, רשות המסים)"
NOT_INVOICE = "מסמך זה הוא הצעת מחיר בלבד ואינו חשבונית מס או קבלה."
LINES = 12

THEMES = [
    # name, main color, light color, font, style
    dict(key="classic", name="קלאסי", main="1E3A5F", light="E8EEF5", font="David", band=True),
    dict(key="modern", name="מודרני", main="0F766E", light="E6F6F4", font="Arial", band=True),
    dict(key="minimal", name="מינימליסטי", main="111827", light="F3F4F6", font="Arial", band=False),
    dict(key="colorful", name="צבעוני", main="C2410C", light="FFF1E6", font="Arial", band=True),
    dict(key="pricelist", name="לפי מחירון", main="6D28D9", light="F1ECFD", font="Arial", band=True),
]

ILS = '#,##0.00 ₪;[Red]-#,##0.00 ₪;""'
RIGHT = Alignment(horizontal="right", vertical="center", wrap_text=True, readingOrder=2)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True, readingOrder=2)
LEFT = Alignment(horizontal="left", vertical="center", readingOrder=2)
INPUT = PatternFill("solid", fgColor="FFF7D6")
thin = Side(style="thin", color="CBD5E1")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
BOTTOM = Border(bottom=thin)

B = "'פרטי העסק'"
DEMO_ITEMS = [("עיצוב לוגו – 3 סקיצות + 2 סבבי תיקונים", 1, "פרויקט", 1800),
              ("עיצוב כרטיס ביקור דו-צדדי", 1, "פרויקט", 450),
              ("דף נחיתה – עיצוב ובנייה", 1, "פרויקט", 3200),
              ("שעת ייעוץ שיווקי", 3, "שעה", 280)]
PRICELIST = [("שעת עבודה", "שעה", 250), ("שעת ייעוץ", "שעה", 280), ("עיצוב לוגו", "פרויקט", 1800),
             ("כרטיס ביקור", "פרויקט", 450), ("דף נחיתה", "פרויקט", 3200), ("ניהול רשתות – חודש", "חודש", 1500),
             ("צילום מוצר (לתמונה)", "יחידה", 60), ("נסיעה (לק\"מ)", "ק\"מ", 2.5)]


def c(ws, ref, value=None, font=None, fill=None, fmt=None, align=RIGHT, border=None):
    x = ws[ref]
    if value is not None:
        x.value = value
    if font:
        x.font = font
    if fill:
        x.fill = fill
    if fmt:
        x.number_format = fmt
    x.alignment = align
    if border:
        x.border = border
    return x


def settings_sheet(wb, example):
    ws = wb.create_sheet("פרטי העסק")
    ws.sheet_view.rightToLeft = True
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = "F59E0B"
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 44
    ws.column_dimensions["C"].width = 60
    c(ws, "A1", "פרטי העסק – ממלאים פעם אחת, מופיעים בכל העיצובים", Font(name="Arial", size=16, bold=True, color="0F766E"))
    rows = [
        ("שם העסק", "סטודיו לדוגמה" if example else "", ""),
        ("סוג עוסק", "עוסק מורשה", "עוסק מורשה / חברה = מוסיפים מע\"מ. עוסק פטור = בלי מע\"מ"),
        ("מספר עוסק / ח.פ.", "012345678" if example else "", ""),
        ("כתובת", "רחוב הדוגמה 1, תל אביב" if example else "", ""),
        ("טלפון", "050-0000000" if example else "", ""),
        ("אימייל", "studio@example.com" if example else "", ""),
        ("אתר / אינסטגרם", "", ""),
        ("פרטי בנק להעברה", "", "לא חובה"),
        ("שיעור מע\"מ", VAT, f"{VAT_SOURCE}. נבדק {CHECKED}. אם השיעור ישתנה – מעדכנים רק כאן"),
        ("תוקף ההצעה (ימים)", 30, ""),
        ("שם החותם/ת", "ישראל ישראלי" if example else "", ""),
        ("להדגיש תאים למילוי בצהוב?", "כן", "לפני שמירה כ-PDF / הדפסה – שנו ל'לא' כדי שהצהוב לא יודפס"),
        ("תנאי ברירת מחדל", "50% מקדמה עם אישור ההצעה, היתרה עם המסירה. המחירים בשקלים. עבודה נוספת מעבר למפורט תתומחר בנפרד.", "מופיע בכל הצעה, אפשר לשנות"),
    ]
    for i, (lab, val, note) in enumerate(rows, start=3):
        c(ws, f"A{i}", lab, Font(name="Arial", bold=True), border=BOX)
        x = c(ws, f"B{i}", val, Font(name="Arial"), INPUT, border=BOX)
        c(ws, f"C{i}", note, Font(name="Arial", size=9, color="64748B"))
        ws.row_dimensions[i].height = 22
    ws["B11"].number_format = "0%"
    ws.row_dimensions[15].height = 48
    dv = DataValidation(type="list", formula1='"עוסק מורשה,עוסק פטור,חברה בע״מ"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add("B4")
    dvh = DataValidation(type="list", formula1='"כן,לא"', allow_blank=False)
    ws.add_data_validation(dvh)
    dvh.add("B14")
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="1")
    ws.add_data_validation(dvp)
    dvp.add("B11")

    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    # price list
    c(ws, "A18", "מחירון (לעיצוב 5 – 'לפי מחירון')", Font(name="Arial", size=14, bold=True, color="6D28D9"))
    for j, h in enumerate(["פריט", "יחידה", "מחיר ליחידה לפני מע\"מ"]):
        x = ws.cell(row=19, column=1 + j, value=h)
        x.font = Font(name="Arial", bold=True, color="FFFFFF")
        x.fill = PatternFill("solid", fgColor="6D28D9")
        x.alignment = CENTER
    for k in range(40):
        r = 20 + k
        item = PRICELIST[k] if k < len(PRICELIST) else (None, None, None)
        for j, v in enumerate(item):
            x = ws.cell(row=r, column=1 + j, value=v)
            x.fill = INPUT
            x.border = BOX
            x.alignment = RIGHT
            x.font = Font(name="Arial")
        ws.cell(row=r, column=3).number_format = ILS
    return ws


def design_sheet(wb, idx, t, example):
    ws = wb.create_sheet(f"{idx} {t['name']}")
    ws.sheet_view.rightToLeft = True
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = t["main"]
    fn = t["font"]
    main = t["main"]
    light = PatternFill("solid", fgColor=t["light"])
    band = PatternFill("solid", fgColor=main)
    widths = {"A": 2, "B": 11, "C": 36, "D": 9, "E": 11, "F": 15, "G": 16, "H": 2}
    for k, w in widths.items():
        ws.column_dimensions[k].width = w
    white_big = Font(name=fn, size=22, bold=True, color="FFFFFF")
    col_big = Font(name=fn, size=22, bold=True, color=main)
    f = Font(name=fn, size=11)
    fb = Font(name=fn, size=11, bold=True)
    fs = Font(name=fn, size=9, color="64748B")

    # header
    for r in (2, 3, 4):
        for col in "BCDEFG":
            if t["band"]:
                ws[f"{col}{r}"].fill = band
    ws.merge_cells("B2:E3")
    c(ws, "B2", f"={B}!B3", white_big if t["band"] else col_big)
    ws.merge_cells("F2:G3")
    c(ws, "F2", "הצעת מחיר", Font(name=fn, size=20, bold=True, color="FFFFFF" if t["band"] else main), align=LEFT)
    ws.merge_cells("B4:G4")
    hdr_small = Font(name=fn, size=10, color="FFFFFF" if t["band"] else "475569")
    # skip the "·" separator for empty business fields so a half-filled header has no dangling dots
    c(ws, "B4", f'=TRIM({B}!B4&" "&{B}!B5&IF({B}!B6="","","  ·  "&{B}!B6)&IF({B}!B7="","","  ·  "&{B}!B7)&IF({B}!B8="","","  ·  "&{B}!B8))', hdr_small)
    ws.row_dimensions[2].height = 26
    ws.row_dimensions[3].height = 26
    ws.row_dimensions[4].height = 20
    if not t["band"]:
        for col in "BCDEFG":
            ws[f"{col}4"].border = Border(bottom=Side(style="medium", color=main))

    # quote meta + client
    c(ws, "B6", "לכבוד:", fb)
    ws.merge_cells("C6:D6")
    c(ws, "C6", "כרמל שיווק בע\"מ" if example else None, f, INPUT)
    c(ws, "B7", "איש קשר:", fs)
    ws.merge_cells("C7:D7")
    c(ws, "C7", "נועה" if example else None, f, INPUT)
    c(ws, "B8", "טלפון/מייל:", fs)
    ws.merge_cells("C8:D8")
    c(ws, "C8", "noa@example.com" if example else None, f, INPUT)
    c(ws, "F6", "מס' הצעה:", fb)
    c(ws, "G6", 1024 if example else None, f, INPUT, "0")
    c(ws, "F7", "תאריך:", fb)
    c(ws, "G7", dt.date(2026, 11, 17) if example else "=TODAY()", f, INPUT, "DD/MM/YYYY")
    c(ws, "F8", "בתוקף עד:", fb)
    c(ws, "G8", f'=IF(G7="","",G7+{B}!B12)', f, None, "DD/MM/YYYY")
    c(ws, "B10", "נושא:", fb)
    ws.merge_cells("C10:G10")
    c(ws, "C10", "מיתוג לעסק חדש" if example else None, f, INPUT)

    # items
    heads = ["#", "תיאור", "כמות", "יחידה", "מחיר ליחידה", "סה\"כ"]
    for j, h in enumerate(heads):
        x = ws.cell(row=12, column=2 + j, value=h)
        x.font = Font(name=fn, bold=True, color="FFFFFF" if t["band"] or t["key"] != "minimal" else main)
        x.fill = band
        x.alignment = CENTER
        if t["key"] == "minimal":
            x.fill = PatternFill(fill_type=None)
            x.font = Font(name=fn, bold=True, color=main)
            x.border = Border(bottom=Side(style="medium", color=main))
    ws.row_dimensions[12].height = 22
    first, last = 13, 12 + LINES
    is_pl = t["key"] == "pricelist"
    for k in range(LINES):
        r = first + k
        stripe = light if (k % 2 == 1 and t["key"] != "minimal") else None
        c(ws, f"B{r}", f'=IF(OR(C{r}<>"",F{r}<>""),{k+1},"")', f, stripe, align=CENTER, border=BOTTOM)
        c(ws, f"C{r}", None, f, INPUT, border=BOTTOM)
        c(ws, f"D{r}", None, f, INPUT, "#,##0.##", CENTER, BOTTOM)
        if is_pl:
            c(ws, f"E{r}", f"=IFERROR(INDEX({B}!$B$20:$B$59,MATCH(C{r},{B}!$A$20:$A$59,0)),\"\")", f, stripe, align=CENTER, border=BOTTOM)
            c(ws, f"F{r}", f"=IFERROR(INDEX({B}!$C$20:$C$59,MATCH(C{r},{B}!$A$20:$A$59,0)),\"\")", f, stripe, ILS, border=BOTTOM)
        else:
            c(ws, f"E{r}", None, f, INPUT, align=CENTER, border=BOTTOM)
            c(ws, f"F{r}", None, f, INPUT, ILS, border=BOTTOM)
        c(ws, f"G{r}", f'=IF(OR(D{r}="",F{r}=""),"",D{r}*F{r})', fb, stripe, ILS, border=BOTTOM)
        ws.row_dimensions[r].height = 20
    if is_pl:
        dv = DataValidation(type="list", formula1=f"={B}!$A$20:$A$59", allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"C{first}:C{last}")
    dvq = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                         error="כמות חייבת להיות מספר", errorTitle="כמות")
    ws.add_data_validation(dvq)
    dvq.add(f"D{first}:D{last}")
    if example:
        rows = [(n, q, u, p) for n, q, u, p in DEMO_ITEMS]
        if is_pl:
            rows = [("עיצוב לוגו", 1, None, None), ("כרטיס ביקור", 1, None, None), ("דף נחיתה", 1, None, None),
                    ("שעת ייעוץ", 3, None, None)]
        for k, (n, q, u, p) in enumerate(rows):
            r = first + k
            ws[f"C{r}"] = n
            ws[f"D{r}"] = q
            if not is_pl:
                ws[f"E{r}"] = u
                ws[f"F{r}"] = p

    # totals
    t0 = last + 2
    vat_on = f'{B}!$B$4<>"עוסק פטור"'
    totals = [
        ("סכום לפני הנחה", f"=SUM(G{first}:G{last})", None),
        ("הנחה (%)", 0.05 if example else None, "pct"),
        ("סכום ההנחה", f"=-ROUND(G{t0}*IF(G{t0+1}=\"\",0,G{t0+1}),2)", None),
        ("סה\"כ לפני מע\"מ", f"=G{t0}+G{t0+2}", None),
        (f'=IF({vat_on},"מע\"\"מ "&TEXT({B}!$B$11,"0%"),"עוסק פטור – ללא מע\"\"מ")',
         f"=IF({vat_on},ROUND(G{t0+3}*{B}!$B$11,2),0)", None),
        ("סה\"כ לתשלום", f"=G{t0+3}+G{t0+4}", "total"),
    ]
    for k, (lab, val, kind) in enumerate(totals):
        r = t0 + k
        ws.merge_cells(f"E{r}:F{r}")
        c(ws, f"E{r}", lab, fb if kind == "total" else f, align=RIGHT)
        if kind == "pct":
            c(ws, f"G{r}", val, f, INPUT, "0%")
            dvd = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True)
            ws.add_data_validation(dvd)
            dvd.add(f"G{r}")
        elif kind == "total":
            for col in "EFG":
                ws[f"{col}{r}"].fill = band
            c(ws, f"E{r}", lab, Font(name=fn, size=13, bold=True, color="FFFFFF"))
            c(ws, f"G{r}", val, Font(name=fn, size=13, bold=True, color="FFFFFF"), band, ILS)
            ws.row_dimensions[r].height = 26
        else:
            c(ws, f"G{r}", val, f, light, ILS)

    # terms + signature
    tr = t0 + 8
    ws.merge_cells(f"B{tr}:D{tr}")
    c(ws, f"B{tr}", "תנאים והערות", Font(name=fn, size=12, bold=True, color=main))
    ws.merge_cells(f"B{tr+1}:G{tr+3}")
    c(ws, f"B{tr+1}", f"={B}!B15", f, INPUT, align=Alignment(horizontal="right", vertical="top", wrap_text=True, readingOrder=2))
    ws.row_dimensions[tr + 1].height = 22
    sr = tr + 5
    c(ws, f"C{sr}", "אישור הלקוח (שם, תאריך וחתימה):", fb)
    ws.merge_cells(f"F{sr}:G{sr}")
    c(ws, f"F{sr}", f'="בברכה, "&{B}!B13', fb)
    ws[f"C{sr+2}"].border = Border(bottom=Side(style="thin", color="000000"))
    ws.merge_cells(f"F{sr+2}:G{sr+2}")
    ws[f"F{sr+2}"].border = Border(bottom=Side(style="thin", color="000000"))
    ws[f"G{sr+2}"].border = Border(bottom=Side(style="thin", color="000000"))
    ws.merge_cells(f"B{sr+4}:G{sr+4}")
    c(ws, f"B{sr+4}", NOT_INVOICE + " המחירים בשקלים חדשים.", fs, align=CENTER)

    # input highlight only when toggle in settings = "כן" (so it never prints by accident)
    ws["J1"] = f"={B}!$B$14"
    ws["J1"].font = Font(color="FFFFFF")
    ws.column_dimensions["J"].hidden = True
    refs = []
    for row in ws.iter_rows(min_row=1, max_row=sr + 4, max_col=8):
        for x in row:
            if x.fill is not None and x.fill.fgColor is not None and x.fill.fgColor.rgb in ("00FFF7D6", "FFFFF7D6"):
                x.fill = PatternFill(fill_type=None)
                refs.append(x.coordinate)
    ws.conditional_formatting.add(" ".join(refs), FormulaRule(formula=['$J$1="כן"'], fill=INPUT))
    ws.print_area = f"A1:H{sr+4}"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.print_options.horizontalCentered = True
    return ws


def instructions(wb):
    ws = wb.active
    ws.title = "הוראות"
    ws.sheet_view.rightToLeft = True
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 110
    lines = [
        ("ערכת הצעות מחיר – הוראות", 18, True),
        ("1. בגיליון 'פרטי העסק' ממלאים פעם אחת: שם, סוג עוסק, טלפון, תנאים. הם יופיעו אוטומטית בכל 5 העיצובים.", 11, False),
        ("2. בוחרים עיצוב (גיליונות 1–5), ממלאים פרטי לקוח ושורות פריטים בתאים הצהובים. הסכומים, ההנחה והמע\"מ מחושבים לבד.", 11, False),
        ("   תאריך ההצעה מתמלא אוטומטית בתאריך של היום ומתעדכן בכל פתיחה של הקובץ. כדי לקבע אותו – הקלידו את התאריך בתא (Ctrl+;).", 11, False),
        ("3. 'סוג עוסק' קובע את המע\"מ: עוסק מורשה / חברה – מתווסף מע\"מ; עוסק פטור – ללא מע\"מ.", 11, False),
        ("4. מחירים ליחידה נרשמים לפני מע\"מ.", 11, False),
        ("5. עיצוב 5 ('לפי מחירון'): בוחרים פריט מרשימה, והמחיר והיחידה נמשכים מהמחירון שבגיליון 'פרטי העסק'.", 11, False),
        ("6. שמירה כ-PDF: קובץ ← שמירה בשם / הדפסה ← PDF. כל עיצוב מוגדר לעמוד A4 אחד.", 11, False),
        ("7. לוגו: הוספה ← תמונה, וגוררים לפינת הכותרת.", 11, False),
        ("8. להצעה חדשה: מעתיקים את הגיליון (לחיצה ימנית על הלשונית ← העבר/העתק) או שומרים עותק של הקובץ.", 11, False),
        ("", 11, False),
        ("חשוב", 14, True),
        (f"• {NOT_INVOICE} חשבונית מס / קבלה מפיקים בתוכנה או בפנקס מאושרים.", 11, False),
        (f"• {VAT_SOURCE}. נבדק לאחרונה: {CHECKED}.", 11, False),
        ("• הקובץ אינו ייעוץ משפטי או ייעוץ מס. התנאים המוצעים הם דוגמה – התאימו אותם לעסק שלכם.", 11, False),
        ("• Google Sheets: מעלים ל-Google Drive ← פתיחה באמצעות Google Sheets. הנוסחאות עובדות כרגיל.", 11, False),
        ("• קבצי ה-Word בחבילה זהים בעיצוב, אבל בהם הסכומים מוקלדים ידנית. לחישוב אוטומטי – השתמשו בקובץ האקסל.", 11, False),
    ]
    for i, (t, size, bold) in enumerate(lines, start=1):
        x = ws.cell(row=i, column=2, value=t)
        x.font = Font(name="Arial", size=size, bold=bold, color="0F766E" if bold else "000000")
        x.alignment = RIGHT
        ws.row_dimensions[i].height = 30 if size > 11 else 26


def build_xlsx(example=False):
    wb = Workbook()
    instructions(wb)
    settings_sheet(wb, example)
    for i, t in enumerate(THEMES, start=1):
        design_sheet(wb, i, t, example)
    wb.active = 2
    wb.properties.title = "ערכת הצעות מחיר"
    wb.properties.creator = "Glory"
    out = HERE / f"hatzaat-mechir-templates{'-example' if example else ''}.xlsx"
    wb.save(out)
    print("wrote", out)
    return out


# ------------------------------------------------------------------ docx
def set_rtl_par(p, align=WD_ALIGN_PARAGRAPH.RIGHT):
    if align == WD_ALIGN_PARAGRAPH.LEFT:  # physical left: leave paragraph LTR so every app agrees
        p.alignment = align
        return p
    pPr = p._p.get_or_add_pPr()
    bidi = OxmlElement("w:bidi")
    pPr.insert(0, bidi)
    p.alignment = align
    return p


def run(p, text, size=11, bold=False, color=None, font="Arial"):
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = font
    rPr = r._r.get_or_add_rPr()
    rfonts = rPr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rPr.insert(0, rfonts)
    rfonts.set(qn("w:cs"), font)
    rfonts.set(qn("w:ascii"), font)
    rfonts.set(qn("w:hAnsi"), font)
    rtl = OxmlElement("w:rtl")
    rPr.append(rtl)
    szcs = OxmlElement("w:szCs")
    szcs.set(qn("w:val"), str(int(size * 2)))
    rPr.append(szcs)
    if bold:
        rPr.append(OxmlElement("w:bCs"))
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    return r


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def table_rtl(tbl):
    tblPr = tbl._tbl.tblPr
    tblPr.append(OxmlElement("w:bidiVisual"))


def borders(tbl, color="CBD5E1", inside=True):
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right") + (("insideH", "insideV") if inside else ()):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), color)
        b.append(e)
    tblPr.append(b)


def set_widths(tbl, widths):
    tbl.autofit = False
    grid = tbl._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w.twips if hasattr(w, "twips") else w / 635)))
    for row in tbl.rows:
        for cc, w in zip(row.cells, widths):
            cc.width = w
    tblPr = tbl._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)


def cell_text(cell, text, size=10, bold=False, color=None, font="Arial", align=WD_ALIGN_PARAGRAPH.RIGHT):
    p = cell.paragraphs[0]
    set_rtl_par(p, align)
    run(p, text, size, bold, color, font)


def build_docx(t):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(1.8)
    sec.top_margin = sec.bottom_margin = Cm(1.5)
    sectPr = sec._sectPr
    sectPr.append(OxmlElement("w:bidi"))
    fn = t["font"]
    main, light = t["main"], t["light"]
    st = doc.styles["Normal"]
    st.font.name = fn
    st.font.size = Pt(11)
    st.paragraph_format.space_after = Pt(2)
    st.paragraph_format.space_before = Pt(0)

    # header block
    head = doc.add_table(rows=1, cols=2)
    table_rtl(head)
    head.alignment = WD_TABLE_ALIGNMENT.CENTER
    a, b = head.rows[0].cells
    txtc = "FFFFFF" if t["band"] else main
    if t["band"]:
        shade(a, main)
        shade(b, main)
    cell_text(a, "[שם העסק]", 20, True, txtc, fn)
    p = a.add_paragraph()
    set_rtl_par(p)
    run(p, "[סוג עוסק ומספר] · [כתובת] · [טלפון] · [אימייל]", 9, False, "FFFFFF" if t["band"] else "475569", fn)
    cell_text(b, "הצעת מחיר", 20, True, txtc, fn, WD_ALIGN_PARAGRAPH.LEFT)
    set_widths(head, [Cm(11.4), Cm(6)])
    if not t["band"]:
        borders(head, main, inside=False)

    doc.add_paragraph()
    meta = doc.add_table(rows=4, cols=4)
    table_rtl(meta)
    vals = [("לכבוד:", "[שם הלקוח / החברה]", "מס' הצעה:", "[0000]"),
            ("איש קשר:", "[שם]", "תאריך:", "[__/__/____]"),
            ("טלפון/מייל:", "[...]", "בתוקף עד:", "[__/__/____]"),
            ("נושא:", "[נושא ההצעה]", "", "")]
    for i, row in enumerate(vals):
        for j, v in enumerate(row):
            cell_text(meta.rows[i].cells[j], v, 10, j % 2 == 0, None if j % 2 else main, fn)
    set_widths(meta, [Cm(2.6), Cm(7), Cm(2.6), Cm(5.2)])

    doc.add_paragraph()
    items = doc.add_table(rows=1 + 8, cols=6)
    table_rtl(items)
    borders(items, "CBD5E1")
    heads = ["#", "תיאור", "כמות", "יחידה", "מחיר ליחידה", "סה\"כ"]
    widths = [Cm(1), Cm(7.6), Cm(1.6), Cm(1.8), Cm(2.6), Cm(2.8)]
    for j, h in enumerate(heads):
        cc = items.rows[0].cells[j]
        if t["key"] == "minimal":
            cell_text(cc, h, 10, True, main, fn, WD_ALIGN_PARAGRAPH.CENTER)
        else:
            shade(cc, main)
            cell_text(cc, h, 10, True, "FFFFFF", fn, WD_ALIGN_PARAGRAPH.CENTER)
    for i in range(1, 9):
        for j in range(6):
            cc = items.rows[i].cells[j]
            cell_text(cc, str(i) if j == 0 else "", 10, False, None, fn,
                      WD_ALIGN_PARAGRAPH.CENTER if j in (0, 2, 3) else WD_ALIGN_PARAGRAPH.RIGHT)
            if i % 2 == 0 and t["key"] != "minimal":
                shade(cc, light)
    set_widths(items, widths)

    doc.add_paragraph()
    tot = doc.add_table(rows=5, cols=2)
    table_rtl(tot)
    tot.alignment = WD_TABLE_ALIGNMENT.LEFT
    trows = [("סכום לפני הנחה", "₪"), ("הנחה", "₪"), ("סה\"כ לפני מע\"מ", "₪"),
             ("מע\"מ 18% (עוסק פטור: ללא מע\"מ)", "₪"), ("סה\"כ לתשלום", "₪")]
    for i, (l, v) in enumerate(trows):
        last = i == len(trows) - 1
        lc, vc = tot.rows[i].cells
        if last:
            shade(lc, main)
            shade(vc, main)
        else:
            shade(vc, light)
        cell_text(lc, l, 11 if last else 10, last, "FFFFFF" if last else None, fn)
        cell_text(vc, v, 11 if last else 10, last, "FFFFFF" if last else None, fn, WD_ALIGN_PARAGRAPH.LEFT)
    set_widths(tot, [Cm(6), Cm(3.5)])

    p = set_rtl_par(doc.add_paragraph())
    run(p, "חישוב מהיר: מע\"מ = סה\"כ לפני מע\"מ × 0.18. לחישוב אוטומטי השתמשו בקובץ האקסל המצורף.", 8, False, "64748B", fn)

    p = set_rtl_par(doc.add_paragraph())
    run(p, "תנאים והערות", 12, True, main, fn)
    for line in ["תנאי תשלום: [למשל 50% מקדמה, היתרה במסירה].", "לוח זמנים: [מועד התחלה ומסירה].",
                 "כולל: [מה כלול בהצעה]. לא כולל: [מה לא כלול].", "עבודה נוספת מעבר למפורט תתומחר בנפרד."]:
        p = set_rtl_par(doc.add_paragraph())
        run(p, "• " + line, 10, False, None, fn)

    doc.add_paragraph()
    sig = doc.add_table(rows=2, cols=2)
    table_rtl(sig)
    cell_text(sig.rows[0].cells[0], "אישור הלקוח (שם, תאריך וחתימה):", 10, True, None, fn)
    cell_text(sig.rows[0].cells[1], "בברכה, [שם וחתימה]", 10, True, None, fn)
    cell_text(sig.rows[1].cells[0], "\n_________________________", 10, False, None, fn)
    cell_text(sig.rows[1].cells[1], "\n_________________________", 10, False, None, fn)
    set_widths(sig, [Cm(9.2), Cm(8.2)])

    doc.add_paragraph()
    p = set_rtl_par(doc.add_paragraph(), WD_ALIGN_PARAGRAPH.CENTER)
    run(p, NOT_INVOICE + " המחירים בשקלים חדשים.", 8, False, "64748B", fn)

    doc.core_properties.title = f"הצעת מחיר – {t['name']}"
    doc.core_properties.author = "Glory"
    out = HERE / f"hatzaat-mechir-{THEMES.index(t)+1}-{t['key']}.docx"
    doc.save(out)
    print("wrote", out)
    return out


if __name__ == "__main__":
    build_xlsx(False)
    build_xlsx(True)
    for t in THEMES:
        build_docx(t)
