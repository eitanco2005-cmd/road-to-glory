"""Hebrew RTL Word companion: ready-to-send messages + printable checklist + day-of timeline."""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

PLUM = RGBColor(0x6B, 0x2E, 0x4F)


def _rtl_par(p):
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:bidi")
    b.set(qn("w:val"), "1")
    pPr.append(b)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def _run(p, text, bold=False, size=11, color=None):
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = "Arial"
    rPr = r._r.get_or_add_rPr()
    rtl = OxmlElement("w:rtl")
    rtl.set(qn("w:val"), "1")
    rPr.append(rtl)
    fonts = rPr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rPr.append(fonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        fonts.set(qn(a), "Arial")
    if bold:
        bcs = OxmlElement("w:bCs")
        rPr.append(bcs)
    szcs = OxmlElement("w:szCs")
    szcs.set(qn("w:val"), str(size * 2))
    rPr.append(szcs)
    if color:
        r.font.color.rgb = color
    return r


def para(doc, text, bold=False, size=11, color=None, space=6):
    p = doc.add_paragraph()
    _rtl_par(p)
    p.paragraph_format.space_after = Pt(space)
    _run(p, text, bold, size, color)
    return p


def heading(doc, text, size=16):
    return para(doc, text, bold=True, size=size, color=PLUM, space=8)


def message_box(doc, text):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    cell = t.rows[0].cells[0]
    tblPr = t._tbl.tblPr
    bv = OxmlElement("w:bidiVisual")
    tblPr.append(bv)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "F7EEF2")
    cell._tc.get_or_add_tcPr().append(shd)
    cell.paragraphs[0].text = ""
    for i, line in enumerate(text.split("\n")):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        _rtl_par(p)
        _run(p, line, size=11)
    doc.add_paragraph()


def checklist_table(doc, tasks):
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    t._tbl.tblPr.append(OxmlElement("w:bidiVisual"))
    for c, h in zip(t.rows[0].cells, ["✓", "משימה", "שלב", "תאריך יעד"]):
        c.paragraphs[0].text = ""
        _rtl_par(c.paragraphs[0])
        _run(c.paragraphs[0], h, bold=True)
    for phase, _w, text in tasks:
        row = t.add_row().cells
        for c, v in zip(row, ["☐", text, phase, "____/____"]):
            c.paragraphs[0].text = ""
            _rtl_par(c.paragraphs[0])
            _run(c.paragraphs[0], v, size=10)
    widths = [Cm(1), Cm(10), Cm(3.2), Cm(2.8)]
    t.autofit = False
    for col, w in zip(t.columns, widths):
        col.width = w
    for row in t.rows:
        for c, w in zip(row.cells, widths):
            c.width = w


def build_docx(cfg, path):
    doc = Document()
    sec = doc.sections[0]
    sec.right_margin = sec.left_margin = Cm(2)
    sectPr = sec._sectPr
    bidi = OxmlElement("w:bidi")
    sectPr.append(bidi)
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    heading(doc, cfg["docx_title"], 20)
    para(doc, cfg["docx_intro"], size=11, color=RGBColor(0x55, 0x55, 0x55))
    for title, msgs in cfg["docx_messages"]:
        heading(doc, title, 14)
        for m in msgs:
            message_box(doc, m)
    heading(doc, "לוח זמנים ליום האירוע (למלא ולשלוח לספקים)", 14)
    t = doc.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    t._tbl.tblPr.append(OxmlElement("w:bidiVisual"))
    for c, h in zip(t.rows[0].cells, ["שעה", "מה קורה", "אחראי/ת / ספק"]):
        c.paragraphs[0].text = ""
        _rtl_par(c.paragraphs[0])
        _run(c.paragraphs[0], h, bold=True)
    for hour, what in cfg["docx_timeline"]:
        row = t.add_row().cells
        for c, v in zip(row, [hour, what, ""]):
            c.paragraphs[0].text = ""
            _rtl_par(c.paragraphs[0])
            _run(c.paragraphs[0], v, size=10)
    doc.add_page_break()
    heading(doc, "צ'קליסט להדפסה", 14)
    para(doc, "אותן משימות כמו בקובץ האקסל. תאריכי היעד המדויקים מחושבים בגיליון \"צ'קליסט\".", size=10)
    checklist_table(doc, cfg["tasks"])
    para(doc, "")
    para(doc, "Glory – כלים חכמים לתכנון · לשימוש אישי של הרוכשים", size=9, color=RGBColor(0x88, 0x88, 0x88))
    doc.core_properties.title = cfg["docx_title"]
    doc.core_properties.author = "Glory"
    doc.save(path)
