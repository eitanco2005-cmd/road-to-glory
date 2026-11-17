#!/usr/bin/env python3
"""Build the Hebrew contractor checklist (.docx, RTL) shipped with the renovation planner."""
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

OUT = Path(__file__).resolve().parent / "renovation-contractor-checklist.docx"


def rtl(p):
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:bidi")
    ps = pPr.find(qn("w:pStyle"))
    pPr.insert(1 if ps is not None else 0, b)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for r in p.runs:
        rPr = r._r.get_or_add_rPr()
        rt = OxmlElement("w:rtl")
        rPr.append(rt)
        r.font.name = "Arial"
        rPr.rFonts.set(qn("w:cs"), "Arial")
        r.font.size = r.font.size or Pt(11)
        r.font.size_cs = None
        szcs = OxmlElement("w:szCs")
        szcs.set(qn("w:val"), str(int((r.font.size.pt if r.font.size else 11) * 2)))
        rPr.append(szcs)
    return p


def para(doc, text, bold=False, size=11, color=None, style=None):
    p = doc.add_paragraph(style=style)
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    if bold:
        rPr = r._r.get_or_add_rPr()
        rPr.append(OxmlElement("w:bCs"))
    return rtl(p)


def box(doc, text):
    return para(doc, "☐  " + text)


SECTIONS = [
    ("לפני שמבקשים הצעות מחיר", [
        "כתבתי רשימת עבודות מפורטת לכל חדר (אפשר להעתיק מגיליון «עבודות» בקובץ האקסל).",
        "החלטתי מה אני קונה בעצמי (אריחים, כלים סניטריים, גופי תאורה) ומה הקבלן מספק.",
        "יש לי תוכנית או סקיצה עם מידות, ולפחות 3 קבלנים לכל עבודה גדולה.",
        "בדקתי אם העבודה דורשת היתר או אישור מהעירייה או מהוועד/נציגות הבית (למשל שינוי קירות, מרפסת, חלונות בחזית).",
    ]),
    ("מה חייב להופיע בהצעת המחיר", [
        "פירוט סעיף-סעיף: כמויות (מ\"ר, נקודות, יחידות) ומחיר לכל סעיף – לא רק סכום כולל.",
        "האם המחיר כולל מע\"מ (18%) – כתוב במפורש.",
        "מה כלול ומה לא: חומרים, פינוי פסולת, הובלה, הגנה על רצפות ורהיטים, ניקיון בסיום.",
        "סוג ודגם החומרים (מותג, עובי, סוג צנרת/כבלים) – כדי להשוות תפוחים לתפוחים.",
        "לוח זמנים: תאריך התחלה, משך העבודה, ומה קורה באיחור.",
        "אחריות: כמה זמן ועל מה (עבודה, חומרים, איטום, רטיבות).",
        "תוקף ההצעה ומה קורה לתוספות – איך מתמחרים עבודה נוספת שלא הייתה בהצעה.",
    ]),
    ("בדיקות על הקבלן", [
        "שם מלא, מספר עוסק/ח.פ. וכתובת – לא רק שם פרטי וטלפון.",
        "רישום בפנקס הקבלנים (באתר רשם הקבלנים ב-gov.il) – רלוונטי במיוחד לעבודות בנייה גדולות.",
        "חשמלאי: רישיון חשמלאי בתוקף, בהתאם לסוג העבודה. גז: טכנאי גז מוסמך.",
        "ביטוח צד ג' וביטוח עבודות קבלניות בתוקף – ביקשתי עותק.",
        "דיברתי עם 2 לקוחות קודמים וראיתי תמונות או עבודה שבוצעה.",
    ]),
    ("לוח תשלומים הוגן", [
        "המקדמה סבירה ולא רוב הסכום מראש.",
        "תשלומים לפי שלבים שהושלמו (למשל: סיום הריסה, סיום צנרת וחשמל, סיום ריצוף, מסירה) – לא לפי תאריכים בלבד.",
        "השארתי סכום אחרון (למשל 10%) לתשלום אחרי מסירה ותיקון ליקויים.",
        "על כל תשלום מקבלים חשבונית/קבלה – ורושמים אותה בגיליון «תשלומים».",
    ]),
    ("לפני החתימה", [
        "יש הסכם כתוב שמפנה להצעת המחיר המפורטת, חתום על ידי שני הצדדים.",
        "כל שינוי או תוספת נעשים בכתב (גם הודעת וואטסאפ מסודרת עדיפה על שיחה), עם מחיר לפני הביצוע.",
        "ידוע מי אחראי על פינוי פסולת, שעות עבודה מותרות בבניין ותיאום עם השכנים.",
        "שמרתי בלת\"מ של 10%–20% מהתקציב לדברים שיתגלו תוך כדי עבודה.",
    ]),
    ("במסירה", [
        "עברתי חדר-חדר עם רשימת ליקויים ותאריך לתיקון.",
        "בדקתי לחץ מים, ניקוז, כל שקע ומפסק, פתיחה וסגירה של חלונות ודלתות, שיפועים במקלחת.",
        "קיבלתי תעודות אחריות, הוראות שימוש, ואישור בודק חשמל אם נדרש.",
        "שילמתי את התשלום האחרון רק אחרי התיקונים.",
    ]),
]

QUESTIONS = [
    "מי בפועל יעבוד אצלי – אתה או צוות? מי מנהל העבודה באתר?",
    "כמה פרויקטים אתה מנהל במקביל? באיזה ימים ושעות תעבדו?",
    "מה קורה אם מתגלה בעיה (צנרת רקובה, רטיבות)? איך מתמחרים את זה?",
    "איזה חומרים אתה ממליץ ולמה? אפשר לבחור מותג אחר?",
    "מה האחריות בפועל – ומה קורה אם מופיעה רטיבות אחרי חצי שנה?",
    "אפשר לקבל טלפון של שני לקוחות אחרונים?",
]


def build():
    doc = Document()
    sec = doc.sections[0]
    sectPr = sec._sectPr
    sectPr.append(OxmlElement("w:bidi"))
    style = doc.styles["Normal"]
    style.font.name = "Arial"
    style.element.rPr.rFonts.set(qn("w:cs"), "Arial")
    para(doc, "רשימת בדיקה: לפני שחותמים עם קבלן שיפוצים", True, 18, "1F4E79")
    para(doc, "נלווה ל«מתכנן תקציב שיפוץ» של Glory · הדפיסו וסמנו ✓", False, 10, "5A6B7D")
    for head, items in SECTIONS:
        para(doc, head, True, 14, "1F4E79")
        for it in items:
            box(doc, it)
    para(doc, "שאלות לשאול כל קבלן בפגישה", True, 14, "1F4E79")
    for q in QUESTIONS:
        para(doc, "•  " + q)
    para(doc, "השוואה מהירה בין 3 הצעות", True, 14, "1F4E79")
    t = doc.add_table(rows=8, cols=4)
    t.style = "Table Grid"
    tblPr = t._tbl.tblPr
    tblPr.append(OxmlElement("w:bidiVisual"))
    rows = ["", "קבלן א'", "קבלן ב'", "קבלן ג'"], ["מחיר כולל מע\"מ", "", "", ""], ["כולל חומרים?", "", "", ""], \
        ["פינוי פסולת כלול?", "", "", ""], ["משך העבודה", "", "", ""], ["אחריות", "", "", ""], \
        ["לוח תשלומים", "", "", ""], ["תחושה כללית / המלצות", "", "", ""]
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j)
            c.text = v
            for p in c.paragraphs:
                rtl(p)
                for r in p.runs:
                    r.bold = (i == 0 or j == 0)
    para(doc, "")
    para(doc, "המסמך הוא רשימת תזכורות כללית לתכנון ואינו ייעוץ משפטי או הנדסי. בהסכמים גדולים מומלץ להתייעץ עם עורך דין או מהנדס.", False, 9, "5A6B7D")
    doc.core_properties.title = "רשימת בדיקה לפני חתימה עם קבלן שיפוצים"
    doc.core_properties.author = "Glory"
    doc.save(OUT)
    print("built", OUT.name)


if __name__ == "__main__":
    build()
