#!/usr/bin/env python3
"""Hanukkah party / hosting planner (.xlsx, he RTL + en). Built with openpyxl: formulas, coloured input cells,
dropdowns, instructions sheet, dashboard with charts. No macros.
    python3 planner.py      -> out/hanukkah-party-planner-{he,en}{,-example}.xlsx

Quantity assumptions (all editable in the Quantities sheet, shown to the user as assumptions, not facts):
  latkes: 4 per adult / 2 per child; ~20 medium latkes per kg potatoes (≈9 per lb)
  per kg potatoes: 1 onion, 2 eggs, 40 g flour, 250 ml frying oil
  sufganiyot: 1.5 per adult / 1 per child; homemade batch = 500 g flour -> 16 doughnuts
  appetite factor: light 0.75 / normal 1 / hungry 1.3
"""
import datetime
import pathlib

from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"

INPUT = PatternFill("solid", fgColor="FFF4C2")
HEAD = PatternFill("solid", fgColor="173A66")
SUB = PatternFill("solid", fgColor="DCE8F6")
CALC = PatternFill("solid", fgColor="F3F6FA")
GOLD = PatternFill("solid", fgColor="F2B632")
THIN = Side(style="thin", color="B8C4D2")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WHITE_B = Font(bold=True, color="FFFFFF", size=12)
TITLE = Font(bold=True, size=18, color="173A66")
BOLD = Font(bold=True)

GUEST_ROWS = 120
GIFT_ROWS = 80
SHOP_MANUAL = 25
TASK_ROWS = 40

# ------------------------------------------------------------------ texts
TX = {
    "he": {
        "rtl": True, "font": "Arial", "cur": '"₪"#,##0', "cur2": '"₪"#,##0.00',
        "sheets": ["הוראות", "אורחים", "כמויות", "רשימת קניות", "מתנות 8 לילות", "משימות", "דשבורד"],
        "title": "מתכנן מסיבת חנוכה 2026",
        "instr": [
            ("מה יש בקובץ", None),
            ("אורחים", "רשימת מוזמנים: מבוגרים, ילדים, אישור הגעה, באיזה ערב, מה כל אחד מביא והערות (אלרגיות, צמחוני)."),
            ("כמויות", "מחשבון שמחשב לבד כמה סופגניות ולביבות צריך, וכמה תפוחי אדמה, ביצים, קמח ושמן לקנות — לפי מספר האורחים שאישרו."),
            ("רשימת קניות", "נבנית אוטומטית מהכמויות. מוסיפים מחיר משוער ליחידה ומסמנים מה נקנה. יש שורות ריקות לפריטים נוספים."),
            ("מתנות 8 לילות", "מעקב מתנות לכל אחד משמונת הלילות: למי, מה, תקציב, כמה עלה בפועל וסטטוס (רעיון / נקנה / נעטף / ניתן)."),
            ("משימות", "צ'קליסט הכנות עם תאריך יעד שמחושב לפי תאריך המסיבה."),
            ("דשבורד", "סיכום: אורחים, כמויות, עלות קניות משוערת, תקציב מתנות מול ביצוע וגרפים."),
            ("איך עובדים", None),
            ("1", "מקלידים רק בתאים הצהובים. כל השאר מחושב בנוסחאות — לא צריך לגעת בהם."),
            ("2", "בגיליון «כמויות» קובעים את תאריך המסיבה, אם לספור גם את מי שענה «אולי», ואם מכינים סופגניות בבית או קונים."),
            ("3", "כל ההנחות (כמה לביבות לאדם, כמה לביבות יוצאות מקילו תפוחי אדמה וכו') מופיעות בטבלת «הנחות» ואפשר לשנות אותן."),
            ("4", "המחירים בקובץ הם דוגמה בלבד. עדכנו לפי המחירים אצלכם."),
            ("תאריכי חנוכה 2026", None),
            ("", "נר ראשון: יום שישי 4.12.2026 בערב (כ״ה בכסלו תשפ״ז). נר שמיני: שישי 11.12.2026. היום האחרון של החג: שבת 12.12.2026."),
            ("עובד ב-", "Excel 2010 ומעלה, Excel לנייד, Google Sheets (העלאה ל-Drive ← פתיחה באמצעות Google Sheets) ו-LibreOffice. בלי מאקרו."),
        ],
        "g_head": ["#", "שם / משפחה", "מבוגרים", "ילדים", "אישור הגעה", "ערב (נר)", "מביאים", "טלפון", "הערות / אלרגיות"],
        "rsvp": ["מגיע/ה", "אולי", "לא מגיע/ה", "טרם ענה"],
        "g_sum": ["אישרו – מבוגרים", "אישרו – ילדים", "אולי – מבוגרים", "אולי – ילדים", "סה״כ הזמנות"],
        "q_inputs": [("תאריך המסיבה", "date"), ("לספור גם «אולי»?", "yn"), ("תיאבון", "appetite"),
                     ("סופגניות: מכינים או קונים?", "make"), ("מספר חנוכיות בבית", "int"),
                     ("מבוגרים (ידני, לא חובה)", "int"), ("ילדים (ידני, לא חובה)", "int")],
        "yes": "כן", "no": "לא", "appetite": ["קל", "רגיל", "רעב"], "make": ["קונים", "מכינים"],
        "q_used": ["מבוגרים בחישוב", "ילדים בחישוב", "מקדם תיאבון", "ערב המסיבה (נר)"],
        "assump_h": "הנחות (אפשר לשנות)",
        "assump": [
            ("לביבות למבוגר", 4, "יח'"), ("לביבות לילד", 2, "יח'"), ("לביבות מקילו תפוחי אדמה", 20, "יח'"),
            ("בצל לקילו תפוחי אדמה", 1, "יח'"), ("ביצים לקילו תפוחי אדמה", 2, "יח'"), ("קמח לקילו תפוחי אדמה", 40, "גרם"),
            ("שמן טיגון לקילו תפוחי אדמה", 0.25, "ליטר"), ("סופגניות למבוגר", 1.5, "יח'"), ("סופגניות לילד", 1, "יח'"),
            ("סופגניות ממנה (500 גרם קמח)", 16, "יח'"), ("שמן טיגון למנה של סופגניות", 0.5, "ליטר"), ("ריבה לסופגנייה", 15, "גרם"),
            ("שמנת / יוגורט לאדם", 50, "גרם"), ("רסק תפוחים לאדם", 50, "גרם"), ("שתייה לאדם", 0.5, "ליטר"),
            ("מטבעות שוקולד לילד", 5, "יח'"), ("צלחות לאדם", 2, "יח'"), ("מפיות לאדם", 3, "יח'"), ("כוסות לאדם", 2, "יח'"),
            ("נרות לחנוכייה לכל החג", 44, "יח'"),
        ],
        "res_h": "התוצאה: מה צריך",
        "res_cols": ["פריט", "כמות", "יחידה", "קטגוריה", "מחיר לדוגמה ליח'"],
        "cats": ["לביבות", "סופגניות", "תוספות", "שתייה", "כיבוד", "חד-פעמי", "חנוכה"],
        "items": [  # key, label, unit, category, example price
            ("latkes", "לביבות (סה״כ)", "יח'", 0, None), ("potatoes", "תפוחי אדמה", "ק״ג", 0, 5),
            ("onions", "בצל", "יח'", 0, 1), ("eggs_l", "ביצים ללביבות", "יח'", 0, 1.2), ("flour_l", "קמח ללביבות", "גרם", 0, 0.006),
            ("oil_l", "שמן לטיגון לביבות", "ליטר", 0, 12), ("suf", "סופגניות (סה״כ)", "יח'", 1, 7),
            ("suf_flour", "קמח לסופגניות", "גרם", 1, 0.006), ("suf_yeast", "שמרים יבשים", "גרם", 1, 0.3),
            ("suf_sugar", "סוכר", "גרם", 1, 0.006), ("suf_eggs", "ביצים לסופגניות", "יח'", 1, 1.2),
            ("suf_milk", "חלב", "מ״ל", 1, 0.007), ("suf_butter", "חמאה", "גרם", 1, 0.04),
            ("suf_jam", "ריבה", "גרם", 1, 0.03), ("suf_oil", "שמן לטיגון סופגניות", "ליטר", 1, 12),
            ("cream", "שמנת חמוצה / יוגורט", "גרם", 2, 0.03), ("apple", "רסק תפוחים", "גרם", 2, 0.02),
            ("drinks", "שתייה", "ליטר", 3, 6), ("gelt", "מטבעות שוקולד", "יח'", 4, 1),
            ("plates", "צלחות חד-פעמיות", "יח'", 5, 0.3), ("napkins", "מפיות", "יח'", 5, 0.1), ("cups", "כוסות", "יח'", 5, 0.2),
            ("candles", "נרות חנוכה", "יח'", 6, 0.35),
        ],
        "batch_note": "במצב «קונים» שורות הבצק של הסופגניות מתאפסות ונשארת רק כמות הסופגניות לקנייה.",
        "s_head": ["פריט", "כמות", "יחידה", "קטגוריה", "מחיר ליח'", "סה״כ משוער", "נקנה?"],
        "s_manual": "פריטים נוספים (מקלידים חופשי)", "bought": ["✓", "✗"],
        "s_total": "סה״כ קניות משוער",
        "gf_head": ["ערב (נר)", "תאריך", "למי", "מתנה / רעיון", "תקציב", "עלות בפועל", "סטטוס", "איפה קונים / הערות"],
        "gf_status": ["רעיון", "נקנה", "נעטף", "ניתן"],
        "gf_sum_h": ["ערב (נר)", "תאריך", "מתנות", "תקציב", "בפועל"],
        "t_head": ["משימה", "כמה ימים לפני", "תאריך יעד", "אחראי/ת", "בוצע?"],
        "tasks": [("לקבוע תאריך ושעה למסיבה", 21), ("לשלוח הזמנות לאורחים", 14), ("לבדוק אלרגיות ומגבלות אוכל", 10),
                  ("לקנות נרות חנוכה (44 לחנוכייה)", 10), ("לבדוק שיש שמן, פתילים / נרות וחנוכייה תקינה", 10),
                  ("להחליט: מכינים סופגניות או מזמינים", 10), ("להזמין סופגניות מהמאפייה (אם קונים)", 5),
                  ("לקנות מתנות לשמונת הלילות", 7), ("לעטוף מתנות", 3), ("לקנות סביבונים ומטבעות שוקולד", 5),
                  ("קניות יבשות: קמח, שמן, סוכר, חד-פעמי", 3), ("קניות טריות: תפוחי אדמה, בצל, ביצים, שמנת", 1),
                  ("להכין דף שירים / ברכות הדלקה", 2), ("לקלף ולגרר תפוחי אדמה", 0), ("לטגן לביבות", 0), ("להדליק נרות ולהנות!", 0)],
        "done": ["✓", "✗"],
        "d_kpi": ["אורחים מבוגרים", "אורחים ילדים", "סופגניות", "לביבות", "תפוחי אדמה (ק״ג)", "קניות משוערות",
                  "תקציב מתנות", "הוצאה בפועל על מתנות", "משימות שבוצעו"],
        "d_chart1": "מתנות: תקציב מול בפועל לפי ערב", "d_chart2": "עלות קניות משוערת לפי קטגוריה",
        "d_cat_h": ["קטגוריה", "עלות משוערת"],
        "night": "נר", "date_fmt": "dd/mm/yyyy",
    },
    "en": {
        "rtl": False, "font": "Calibri", "cur": '"$"#,##0', "cur2": '"$"#,##0.00',
        "sheets": ["Instructions", "Guests", "Quantities", "Shopping List", "8 Nights Gifts", "To-Do", "Dashboard"],
        "title": "Hanukkah Party Planner 2026",
        "instr": [
            ("What’s inside", None),
            ("Guests", "Guest list: adults, kids, RSVP, which night, what each guest brings and notes (allergies, vegetarian)."),
            ("Quantities", "Works out how many latkes and jelly doughnuts (sufganiyot) you need, and how many potatoes, eggs, flour and oil to buy, from your confirmed guests."),
            ("Shopping List", "Built automatically from the quantities. Add an estimated price per unit and tick what you bought. Extra blank rows for anything else."),
            ("8 Nights Gifts", "Gift tracker for all eight nights: who, what, budget, actual cost and status (idea / bought / wrapped / given)."),
            ("To-Do", "Prep checklist with due dates calculated from your party date."),
            ("Dashboard", "Summary: guests, quantities, estimated shopping cost, gift budget vs. spent, and charts."),
            ("How to use it", None),
            ("1", "Type only in the yellow cells. Everything else is a formula — no need to touch it."),
            ("2", "On the Quantities sheet set your party date, whether to count “maybe” guests, and whether you make or buy the doughnuts."),
            ("3", "Every assumption (latkes per person, latkes per lb of potatoes, etc.) is in the Assumptions table and can be changed."),
            ("4", "Prices in the file are examples only. Update them to your local prices."),
            ("Hanukkah 2026 dates", None),
            ("", "First candle: Friday evening, December 4, 2026 (25 Kislev 5787). Eighth candle: Friday, December 11. Last day of Hanukkah: Saturday, December 12, 2026."),
            ("Works in", "Excel 2010+, Excel mobile, Google Sheets (upload to Drive → Open with Google Sheets), Numbers and LibreOffice. No macros."),
        ],
        "g_head": ["#", "Name / family", "Adults", "Kids", "RSVP", "Night", "Bringing", "Phone", "Notes / allergies"],
        "rsvp": ["Yes", "Maybe", "No", "No reply"],
        "g_sum": ["Confirmed adults", "Confirmed kids", "Maybe – adults", "Maybe – kids", "Invitations"],
        "q_inputs": [("Party date", "date"), ("Count “maybe” guests too?", "yn"), ("Appetite", "appetite"),
                     ("Doughnuts: make or buy?", "make"), ("Menorahs in the house", "int"),
                     ("Adults (manual, optional)", "int"), ("Kids (manual, optional)", "int")],
        "yes": "Yes", "no": "No", "appetite": ["Light", "Normal", "Hungry"], "make": ["Buy", "Make"],
        "q_used": ["Adults used", "Kids used", "Appetite factor", "Party night (candle)"],
        "assump_h": "Assumptions (editable)",
        "assump": [
            ("Latkes per adult", 4, "pcs"), ("Latkes per kid", 2, "pcs"), ("Latkes per lb of potatoes", 9, "pcs"),
            ("Onions per lb of potatoes", 0.5, "pcs"), ("Eggs per lb of potatoes", 1, "pcs"), ("Flour / matzo meal per lb of potatoes", 2, "tbsp"),
            ("Frying oil per lb of potatoes", 0.5, "cups"), ("Doughnuts per adult", 1.5, "pcs"), ("Doughnuts per kid", 1, "pcs"),
            ("Doughnuts per batch (4 cups flour)", 16, "pcs"), ("Frying oil per doughnut batch", 2, "cups"), ("Jelly per doughnut", 1, "tbsp"),
            ("Sour cream per person", 2, "tbsp"), ("Applesauce per person", 2, "tbsp"), ("Drinks per person", 16, "fl oz"),
            ("Chocolate gelt per kid", 5, "pcs"), ("Plates per person", 2, "pcs"), ("Napkins per person", 3, "pcs"), ("Cups per person", 2, "pcs"),
            ("Candles per menorah (all 8 nights)", 44, "pcs"),
        ],
        "res_h": "Result: what you need",
        "res_cols": ["Item", "Qty", "Unit", "Category", "Example price / unit"],
        "cats": ["Latkes", "Doughnuts", "Toppings", "Drinks", "Treats", "Disposables", "Hanukkah"],
        "items": [
            ("latkes", "Latkes (total)", "pcs", 0, None), ("potatoes", "Potatoes", "lb", 0, 1),
            ("onions", "Onions", "pcs", 0, 0.6), ("eggs_l", "Eggs for latkes", "pcs", 0, 0.35), ("flour_l", "Flour / matzo meal for latkes", "tbsp", 0, 0.03),
            ("oil_l", "Oil for frying latkes", "cups", 0, 0.6), ("suf", "Jelly doughnuts (total)", "pcs", 1, 1.75),
            ("suf_flour", "Flour for doughnuts", "cups", 1, 0.15), ("suf_yeast", "Active dry yeast", "packets", 1, 0.8),
            ("suf_sugar", "Sugar", "cups", 1, 0.4), ("suf_eggs", "Eggs for doughnuts", "pcs", 1, 0.35),
            ("suf_milk", "Milk", "cups", 1, 0.25), ("suf_butter", "Butter", "tbsp", 1, 0.2),
            ("suf_jam", "Jelly / jam", "tbsp", 1, 0.15), ("suf_oil", "Oil for frying doughnuts", "cups", 1, 0.6),
            ("cream", "Sour cream", "tbsp", 2, 0.12), ("apple", "Applesauce", "tbsp", 2, 0.08),
            ("drinks", "Drinks", "fl oz", 3, 0.04), ("gelt", "Chocolate gelt", "pcs", 4, 0.25),
            ("plates", "Disposable plates", "pcs", 5, 0.15), ("napkins", "Napkins", "pcs", 5, 0.03), ("cups", "Cups", "pcs", 5, 0.1),
            ("candles", "Hanukkah candles", "pcs", 6, 0.12),
        ],
        "batch_note": "In “Buy” mode the doughnut dough rows drop to zero and only the number of doughnuts to buy remains.",
        "s_head": ["Item", "Qty", "Unit", "Category", "Price / unit", "Est. total", "Bought?"],
        "s_manual": "Anything else (type freely)", "bought": ["✓", "✗"],
        "s_total": "Estimated shopping total",
        "gf_head": ["Night", "Date", "For", "Gift / idea", "Budget", "Actual cost", "Status", "Where to buy / notes"],
        "gf_status": ["Idea", "Bought", "Wrapped", "Given"],
        "gf_sum_h": ["Night", "Date", "Gifts", "Budget", "Actual"],
        "t_head": ["Task", "Days before", "Due date", "Who", "Done?"],
        "tasks": [("Pick the party date and time", 21), ("Send invitations", 14), ("Ask about allergies and food needs", 10),
                  ("Buy Hanukkah candles (44 per menorah)", 10), ("Check the menorah, candles / oil and wicks", 10),
                  ("Decide: make or buy the jelly doughnuts", 10), ("Order doughnuts from the bakery (if buying)", 5),
                  ("Buy gifts for the eight nights", 7), ("Wrap the gifts", 3), ("Buy dreidels and chocolate gelt", 5),
                  ("Pantry shopping: flour, oil, sugar, disposables", 3), ("Fresh shopping: potatoes, onions, eggs, sour cream", 1),
                  ("Print song sheets / candle blessings", 2), ("Peel and grate potatoes", 0), ("Fry the latkes", 0), ("Light the candles and enjoy!", 0)],
        "done": ["✓", "✗"],
        "d_kpi": ["Adult guests", "Kid guests", "Jelly doughnuts", "Latkes", "Potatoes (lb)", "Est. shopping",
                  "Gift budget", "Spent on gifts", "Tasks done"],
        "d_chart1": "Gifts: budget vs. actual by night", "d_chart2": "Estimated shopping cost by category",
        "d_cat_h": ["Category", "Est. cost"],
        "night": "Night", "date_fmt": "mm/dd/yyyy",
    },
}

EXAMPLE = {
    "he": {
        "guests": [("משפחת כהן", 2, 3, "מגיע/ה", 3, "סלט", "", "ילד אלרגי לבוטנים"), ("סבא וסבתא", 2, 0, "מגיע/ה", 3, "עוגה", "", ""),
                   ("דנה ויואב", 2, 1, "אולי", 3, "", "", "צמחונים"), ("משפחת לוי", 2, 2, "מגיע/ה", 3, "שתייה", "", ""),
                   ("נועה", 1, 0, "לא מגיע/ה", 3, "", "", ""), ("משפחת מזרחי", 2, 4, "טרם ענה", 3, "", "", "")],
        "gifts": [(1, "נועם", "ספר קומיקס", 60, 55, "נעטף"), (1, "מאיה", "ערכת יצירה", 70, 0, "נקנה"),
                  (2, "נועם", "כדור כדורגל", 80, 0, "רעיון"), (2, "מאיה", "ספר", 50, 0, "רעיון"),
                  (3, "כל המשפחה", "משחק קופסה", 120, 110, "נקנה"), (8, "סבתא", "צעיף", 90, 0, "רעיון")],
        "date": datetime.date(2026, 12, 6),
    },
    "en": {
        "guests": [("The Cohens", 2, 3, "Yes", 3, "Salad", "", "Peanut allergy (kid)"), ("Grandma & Grandpa", 2, 0, "Yes", 3, "Dessert", "", ""),
                   ("Dana & Josh", 2, 1, "Maybe", 3, "", "", "Vegetarian"), ("The Levys", 2, 2, "Yes", 3, "Drinks", "", ""),
                   ("Noa", 1, 0, "No", 3, "", "", ""), ("The Friedmans", 2, 4, "No reply", 3, "", "", "")],
        "gifts": [(1, "Sam", "Comic book", 15, 13, "Wrapped"), (1, "Maya", "Craft kit", 20, 0, "Bought"),
                  (2, "Sam", "Soccer ball", 25, 0, "Idea"), (2, "Maya", "Book", 12, 0, "Idea"),
                  (3, "Whole family", "Board game", 35, 32, "Bought"), (8, "Grandma", "Scarf", 30, 0, "Idea")],
        "date": datetime.date(2026, 12, 6),
    },
}


def q(name):
    return "'" + name + "'"


def style_head(ws, row, cols, fill=HEAD, font=WHITE_B):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BOX


def box(cell, fill=None, fmt=None, bold=False):
    cell.border = BOX
    if fill:
        cell.fill = fill
    if fmt:
        cell.number_format = fmt
    if bold:
        cell.font = BOLD


def dv_list(ws, items, rng, allow_blank=True):
    dv = DataValidation(type="list", formula1='"' + ",".join(items) + '"', allow_blank=allow_blank, showDropDown=False)
    dv.error = "בחרו מהרשימה / pick from the list"
    dv.add(rng)
    ws.add_data_validation(dv)


def build(lang, example=False):
    t = TX[lang]
    ex = EXAMPLE[lang] if example else None
    SH = t["sheets"]
    wb = Workbook()
    wss = [wb.active] + [wb.create_sheet() for _ in SH[1:]]
    for ws, name in zip(wss, SH):
        ws.title = name
        ws.sheet_view.rightToLeft = t["rtl"]
        ws.sheet_view.showGridLines = False
    wI, wG, wQ, wS, wF, wT, wD = wss
    gN, qN, sN, fN, tN = (q(x) for x in SH[1:6])

    # ---------------------------------------------------------- instructions
    wI["A1"] = t["title"]
    wI["A1"].font = TITLE
    wI.column_dimensions["A"].width = 22
    wI.column_dimensions["B"].width = 110
    r = 3
    for k, v in t["instr"]:
        if v is None:
            r += 1
            wI.cell(row=r, column=1, value=k).font = Font(bold=True, size=13, color="FFFFFF")
            wI.cell(row=r, column=1).fill = HEAD
            wI.cell(row=r, column=2).fill = HEAD
        else:
            wI.cell(row=r, column=1, value=k).font = BOLD
            c = wI.cell(row=r, column=2, value=v)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    r += 1
    wI.cell(row=r, column=1, value="■").font = Font(color="F2B632", size=14)
    wI.cell(row=r, column=1).fill = INPUT
    wI.cell(row=r, column=2, value=("תא להקלדה" if lang == "he" else "input cell (type here)"))
    wI.cell(row=r + 1, column=1).fill = CALC
    wI.cell(row=r + 1, column=2, value=("נוסחה – מחושב אוטומטית" if lang == "he" else "formula – calculated for you"))
    wI.cell(row=r + 3, column=2, value=("© 2026 תכנון פלוס · tichnun.netlify.app · לשימוש אישי" if lang == "he"
                                        else "© 2026 Tichnun Plus · tichnun.netlify.app/en/hanukkah/ · for personal use")).font = Font(color="777777", size=9)

    # ---------------------------------------------------------- guests
    wG["A1"] = SH[1]
    wG["A1"].font = TITLE
    sums = t["g_sum"]
    # summary row 3/4
    for i, lbl in enumerate(sums):
        c = wG.cell(row=3, column=2 + i, value=lbl)
        c.fill = SUB
        c.font = BOLD
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        c.border = BOX
    H0, R0 = 6, 7
    R1 = R0 + GUEST_ROWS - 1
    yes, maybe = t["rsvp"][0], t["rsvp"][1]
    f_sum = [f'=SUMIFS(C{R0}:C{R1},E{R0}:E{R1},"{yes}")', f'=SUMIFS(D{R0}:D{R1},E{R0}:E{R1},"{yes}")',
             f'=SUMIFS(C{R0}:C{R1},E{R0}:E{R1},"{maybe}")', f'=SUMIFS(D{R0}:D{R1},E{R0}:E{R1},"{maybe}")',
             f'=COUNTA(B{R0}:B{R1})']
    for i, f in enumerate(f_sum):
        c = wG.cell(row=4, column=2 + i, value=f)
        box(c, CALC, "0", True)
        c.alignment = Alignment(horizontal="center")
    for i, h in enumerate(t["g_head"], start=1):
        wG.cell(row=H0, column=i, value=h)
    style_head(wG, H0, len(t["g_head"]))
    for rr in range(R0, R1 + 1):
        wG.cell(row=rr, column=1, value=f'=IF(B{rr}="","",ROW()-{R0 - 1})').fill = CALC
        for cc in range(2, 10):
            box(wG.cell(row=rr, column=cc), INPUT)
        wG.cell(row=rr, column=1).border = BOX
    if ex:
        for i, row in enumerate(ex["guests"]):
            for j, v in enumerate(row):
                wG.cell(row=R0 + i, column=2 + j, value=v if v != "" else None)
    dv_list(wG, t["rsvp"], f"E{R0}:E{R1}")
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="8", allow_blank=True)
    dv.add(f"F{R0}:F{R1}")
    wG.add_data_validation(dv)
    dvn = DataValidation(type="whole", operator="between", formula1="0", formula2="99", allow_blank=True)
    dvn.add(f"C{R0}:D{R1}")
    wG.add_data_validation(dvn)
    for col, w in zip("ABCDEFGHI", [5, 26, 10, 10, 14, 10, 18, 14, 34]):
        wG.column_dimensions[col].width = w
    wG.row_dimensions[3].height = 32
    wG.freeze_panes = f"A{R0}"
    green = PatternFill("solid", fgColor="D9F2E1")
    red = PatternFill("solid", fgColor="FBE0E0")
    wG.conditional_formatting.add(f"E{R0}:E{R1}", CellIsRule(operator="equal", formula=[f'"{yes}"'], fill=green))
    wG.conditional_formatting.add(f"E{R0}:E{R1}", CellIsRule(operator="equal", formula=[f'"{t["rsvp"][2]}"'], fill=red))

    # ---------------------------------------------------------- quantities
    wQ["A1"] = SH[2]
    wQ["A1"].font = TITLE
    for col, w in zip("ABCDEFGH", [34, 14, 10, 16, 18, 3, 40, 12]):
        wQ.column_dimensions[col].width = w
    r = 3
    inp = {}
    for lbl, kind in t["q_inputs"]:
        wQ.cell(row=r, column=1, value=lbl).font = BOLD
        c = wQ.cell(row=r, column=2)
        box(c, INPUT)
        if kind == "date":
            c.value = ex["date"] if ex else datetime.date(2026, 12, 6)
            c.number_format = t["date_fmt"]
            d = DataValidation(type="date", operator="between", formula1="DATE(2026,11,1)", formula2="DATE(2027,1,31)", allow_blank=False)
            d.add(c.coordinate)
            wQ.add_data_validation(d)
        elif kind == "yn":
            c.value = t["no"]
            dv_list(wQ, [t["yes"], t["no"]], c.coordinate, False)
        elif kind == "appetite":
            c.value = t["appetite"][1]
            dv_list(wQ, t["appetite"], c.coordinate, False)
        elif kind == "make":
            c.value = t["make"][0]
            dv_list(wQ, t["make"], c.coordinate, False)
        elif kind == "int":
            c.value = 1 if "חנוכיות" in lbl or "Menorah" in lbl else None
            d = DataValidation(type="whole", operator="between", formula1="0", formula2="999", allow_blank=True)
            d.add(c.coordinate)
            wQ.add_data_validation(d)
        inp[kind if kind not in ("int",) else lbl] = c.coordinate
        r += 1
    keys = [k for k, _ in t["q_inputs"]]
    DATE, YN, APP, MAKE = "B3", "B4", "B5", "B6"
    MEN, MAD, MKID = "B7", "B8", "B9"
    r += 1  # used values
    used_r = r
    used = [
        f'=IF({MAD}<>"",{MAD},{gN}!B4+IF({YN}="{t["yes"]}",{gN}!D4,0))',
        f'=IF({MKID}<>"",{MKID},{gN}!C4+IF({YN}="{t["yes"]}",{gN}!E4,0))',
        f'=IF({APP}="{t["appetite"][0]}",0.75,IF({APP}="{t["appetite"][2]}",1.3,1))',
        f'=IF({DATE}-DATE(2026,12,3)>=1,IF({DATE}-DATE(2026,12,3)<=8,{DATE}-DATE(2026,12,3),"—"),"—")',
    ]
    for i, (lbl, f) in enumerate(zip(t["q_used"], used)):
        wQ.cell(row=r + i, column=1, value=lbl)
        c = wQ.cell(row=r + i, column=2, value=f)
        box(c, CALC, "0.00" if i == 2 else "0", True)
    AD, KD, FAC = f"B{used_r}", f"B{used_r + 1}", f"B{used_r + 2}"
    # assumptions in G:H
    wQ.cell(row=3, column=7, value=t["assump_h"]).font = Font(bold=True, color="FFFFFF")
    wQ.cell(row=3, column=7).fill = HEAD
    wQ.cell(row=3, column=8).fill = HEAD
    wQ.cell(row=3, column=9).fill = HEAD
    A = {}
    akeys = ["l_ad", "l_kid", "l_perkg", "on", "egg", "flour", "oil", "s_ad", "s_kid", "s_batch", "s_oil", "s_jam",
             "cream", "apple", "drink", "gelt", "plates", "napkins", "cups", "candles"]
    for i, ((lbl, val, unit), k) in enumerate(zip(t["assump"], akeys)):
        rr = 4 + i
        wQ.cell(row=rr, column=7, value=lbl).border = BOX
        c = wQ.cell(row=rr, column=8, value=val)
        box(c, INPUT)
        wQ.cell(row=rr, column=9, value=unit).border = BOX
        A[k] = f"$H${rr}"
    wQ.column_dimensions["I"].width = 8
    # results
    r = used_r + 6
    wQ.cell(row=r - 1, column=1, value=t["res_h"]).font = Font(bold=True, size=13, color="173A66")
    for i, h in enumerate(t["res_cols"], start=1):
        wQ.cell(row=r, column=i, value=h)
    style_head(wQ, r, 5)
    res0 = r + 1
    make = f'{MAKE}="{t["make"][1]}"'
    batches = f'ROUNDUP(B{{suf}}/{A["s_batch"]},0)'
    if lang == "he":
        F = {
            "latkes": f'=ROUNDUP(({AD}*{A["l_ad"]}+{KD}*{A["l_kid"]})*{FAC},0)',
            "potatoes": f'=ROUNDUP(B{{latkes}}/{A["l_perkg"]},1)',
            "onions": f'=ROUNDUP(B{{potatoes}}*{A["on"]},0)',
            "eggs_l": f'=ROUNDUP(B{{potatoes}}*{A["egg"]},0)',
            "flour_l": f'=ROUNDUP(B{{potatoes}}*{A["flour"]},-1)',
            "oil_l": f'=ROUNDUP(B{{potatoes}}*{A["oil"]},1)',
            "suf": f'=ROUNDUP(({AD}*{A["s_ad"]}+{KD}*{A["s_kid"]})*{FAC},0)',
            "suf_flour": f'=IF({make},{batches}*500,0)',
            "suf_yeast": f'=IF({make},{batches}*10,0)',
            "suf_sugar": f'=IF({make},{batches}*60,0)',
            "suf_eggs": f'=IF({make},{batches}*2,0)',
            "suf_milk": f'=IF({make},{batches}*250,0)',
            "suf_butter": f'=IF({make},{batches}*50,0)',
            "suf_jam": f'=IF({make},B{{suf}}*{A["s_jam"]},0)',
            "suf_oil": f'=IF({make},ROUNDUP({batches}*{A["s_oil"]},1),0)',
        }
    else:
        F = {
            "latkes": f'=ROUNDUP(({AD}*{A["l_ad"]}+{KD}*{A["l_kid"]})*{FAC},0)',
            "potatoes": f'=ROUNDUP(B{{latkes}}/{A["l_perkg"]},1)',
            "onions": f'=ROUNDUP(B{{potatoes}}*{A["on"]},0)',
            "eggs_l": f'=ROUNDUP(B{{potatoes}}*{A["egg"]},0)',
            "flour_l": f'=ROUNDUP(B{{potatoes}}*{A["flour"]},0)',
            "oil_l": f'=ROUNDUP(B{{potatoes}}*{A["oil"]},1)',
            "suf": f'=ROUNDUP(({AD}*{A["s_ad"]}+{KD}*{A["s_kid"]})*{FAC},0)',
            "suf_flour": f'=IF({make},{batches}*4,0)',
            "suf_yeast": f'=IF({make},{batches}*1,0)',
            "suf_sugar": f'=IF({make},{batches}*0.25,0)',
            "suf_eggs": f'=IF({make},{batches}*2,0)',
            "suf_milk": f'=IF({make},{batches}*1,0)',
            "suf_butter": f'=IF({make},{batches}*4,0)',
            "suf_jam": f'=IF({make},B{{suf}}*{A["s_jam"]},0)',
            "suf_oil": f'=IF({make},ROUNDUP({batches}*{A["s_oil"]},1),0)',
        }
    ppl = f"({AD}+{KD})"
    F.update({
        "cream": f'=ROUNDUP({ppl}*{A["cream"]}*{FAC},0)', "apple": f'=ROUNDUP({ppl}*{A["apple"]}*{FAC},0)',
        "drinks": f'=ROUNDUP({ppl}*{A["drink"]},{1 if lang == "he" else 0})', "gelt": f'={KD}*{A["gelt"]}',
        "plates": f'={ppl}*{A["plates"]}', "napkins": f'={ppl}*{A["napkins"]}', "cups": f'={ppl}*{A["cups"]}',
        "candles": f'={MEN}*{A["candles"]}',
    })
    rowof = {}
    for i, (k, *_rest) in enumerate(t["items"]):
        rowof[k] = res0 + i
    for i, (k, lbl, unit, cat, price) in enumerate(t["items"]):
        rr = res0 + i
        f = F[k].replace("{latkes}", str(rowof["latkes"])).replace("{potatoes}", str(rowof["potatoes"])).replace("{suf}", str(rowof["suf"]))
        wQ.cell(row=rr, column=1, value=lbl).border = BOX
        c = wQ.cell(row=rr, column=2, value=f)
        box(c, CALC, "#,##0.0" if k in ("potatoes", "oil_l", "suf_oil", "drinks") else "#,##0", True)
        wQ.cell(row=rr, column=3, value=unit).border = BOX
        wQ.cell(row=rr, column=4, value=t["cats"][cat]).border = BOX
        pc = wQ.cell(row=rr, column=5, value=price)
        box(pc, INPUT if price is not None else CALC, t["cur2"])
    res1 = res0 + len(t["items"]) - 1
    note_r = res1 + 2
    wQ.cell(row=note_r, column=1, value=t["batch_note"]).font = Font(italic=True, color="555555")
    wQ.freeze_panes = "A3"

    # ---------------------------------------------------------- shopping list
    wS["A1"] = SH[3]
    wS["A1"].font = TITLE
    for col, w in zip("ABCDEFG", [32, 11, 10, 16, 13, 15, 10]):
        wS.column_dimensions[col].width = w
    wS["A3"] = t["s_total"]
    wS["A3"].font = Font(bold=True, size=13)
    S0 = 6
    for i, h in enumerate(t["s_head"], start=1):
        wS.cell(row=S0 - 1, column=i, value=h)
    style_head(wS, S0 - 1, 7)
    n_auto = len([it for it in t["items"] if it[4] is not None])
    rr = S0
    for (k, lbl, unit, cat, price) in t["items"]:
        if price is None:
            continue
        src = rowof[k]
        wS.cell(row=rr, column=1, value=f"={qN}!A{src}")
        wS.cell(row=rr, column=2, value=f"={qN}!B{src}").number_format = "#,##0.0"
        wS.cell(row=rr, column=3, value=f"={qN}!C{src}")
        wS.cell(row=rr, column=4, value=f"={qN}!D{src}")
        wS.cell(row=rr, column=5, value=f"={qN}!E{src}").number_format = t["cur2"]
        for cc in range(1, 6):
            box(wS.cell(row=rr, column=cc), CALC)
        # doughnuts bought only in buy mode; in make mode the dough rows carry the cost
        if k == "suf":
            wS.cell(row=rr, column=6, value=f'=IF({qN}!{MAKE}="{t["make"][1]}",0,B{rr}*E{rr})')
        else:
            wS.cell(row=rr, column=6, value=f"=B{rr}*E{rr}")
        box(wS.cell(row=rr, column=6), CALC, t["cur2"])
        box(wS.cell(row=rr, column=7), INPUT)
        rr += 1
    auto_end = rr - 1
    wS.cell(row=rr + 1, column=1, value=t["s_manual"]).font = Font(bold=True, color="173A66")
    m0 = rr + 2
    for r2 in range(m0, m0 + SHOP_MANUAL):
        for cc in (1, 2, 3, 4, 5, 7):
            box(wS.cell(row=r2, column=cc), INPUT)
        wS.cell(row=r2, column=5).number_format = t["cur2"]
        c = wS.cell(row=r2, column=6, value=f'=IF(OR(B{r2}="",E{r2}=""),0,B{r2}*E{r2})')
        box(c, CALC, t["cur2"])
    m1 = m0 + SHOP_MANUAL - 1
    dv_list(wS, t["cats"], f"D{m0}:D{m1}")
    dv_list(wS, t["bought"], f"G{S0}:G{m1}")
    wS["B3"] = f"=SUM(F{S0}:F{m1})"
    box(wS["B3"], GOLD, t["cur"], True)
    wS.merge_cells("B3:C3")
    wS.freeze_panes = f"A{S0}"
    grey = Font(color="999999", strike=True)
    wS.conditional_formatting.add(f"A{S0}:F{m1}", FormulaRule(formula=[f'$G{S0}="✓"'], font=grey))
    wS.conditional_formatting.add(f"A{S0}:F{auto_end}", FormulaRule(formula=[f"$B{S0}=0"], font=Font(color="BBBBBB")))

    # ---------------------------------------------------------- gifts
    wF["A1"] = SH[4]
    wF["A1"].font = TITLE
    F0 = 4
    for i, h in enumerate(t["gf_head"], start=1):
        wF.cell(row=F0 - 1, column=i, value=h)
    style_head(wF, F0 - 1, 8)
    F1 = F0 + GIFT_ROWS - 1
    for r2 in range(F0, F1 + 1):
        for cc in (1, 3, 4, 5, 6, 7, 8):
            box(wF.cell(row=r2, column=cc), INPUT)
        c = wF.cell(row=r2, column=2, value=f'=IF(A{r2}="","",DATE(2026,12,3)+A{r2})')
        box(c, CALC, t["date_fmt"])
        wF.cell(row=r2, column=5).number_format = t["cur"]
        wF.cell(row=r2, column=6).number_format = t["cur"]
    if ex:
        for i, (n, who, g, b, a, st) in enumerate(ex["gifts"]):
            rr2 = F0 + i
            wF.cell(row=rr2, column=1, value=n)
            wF.cell(row=rr2, column=3, value=who)
            wF.cell(row=rr2, column=4, value=g)
            wF.cell(row=rr2, column=5, value=b)
            wF.cell(row=rr2, column=6, value=a or None)
            wF.cell(row=rr2, column=7, value=st)
    dvn8 = DataValidation(type="whole", operator="between", formula1="1", formula2="8", allow_blank=True)
    dvn8.add(f"A{F0}:A{F1}")
    wF.add_data_validation(dvn8)
    dv_list(wF, t["gf_status"], f"G{F0}:G{F1}")
    for col, w in zip("ABCDEFGHIJKLMNO", [9, 12, 18, 28, 11, 12, 11, 30, 3, 9, 12, 9, 11, 11, 3]):
        wF.column_dimensions[col].width = w
    # per-night summary in J:N
    wF.cell(row=F0 - 1, column=10, value=t["gf_sum_h"][0])
    for i, h in enumerate(t["gf_sum_h"], start=10):
        c = wF.cell(row=F0 - 1, column=i, value=h)
        c.fill = HEAD
        c.font = WHITE_B
        c.alignment = Alignment(horizontal="center")
    for n in range(1, 9):
        rr2 = F0 + n - 1
        wF.cell(row=rr2, column=10, value=n).border = BOX
        box(wF.cell(row=rr2, column=11, value=f"=DATE(2026,12,3)+J{rr2}"), CALC, t["date_fmt"])
        box(wF.cell(row=rr2, column=12, value=f"=COUNTIFS(A${F0}:A${F1},J{rr2},D${F0}:D${F1},\"<>\")"), CALC, "0")
        box(wF.cell(row=rr2, column=13, value=f"=SUMIFS(E${F0}:E${F1},A${F0}:A${F1},J{rr2})"), CALC, t["cur"])
        box(wF.cell(row=rr2, column=14, value=f"=SUMIFS(F${F0}:F${F1},A${F0}:A${F1},J{rr2})"), CALC, t["cur"])
    tr = F0 + 8
    wF.cell(row=tr, column=10, value="Σ").font = BOLD
    for col in (12, 13, 14):
        c = wF.cell(row=tr, column=col, value=f"=SUM({L(col)}{F0}:{L(col)}{F0 + 7})")
        box(c, GOLD, "0" if col == 12 else t["cur"], True)
    # status counts
    for i, st in enumerate(t["gf_status"]):
        rr2 = tr + 2 + i
        wF.cell(row=rr2, column=10, value=st).border = BOX
        box(wF.cell(row=rr2, column=12, value=f'=COUNTIF(G${F0}:G${F1},J{rr2})'), CALC, "0")
    wF.freeze_panes = f"A{F0}"
    colors = {0: "FFF4C2", 1: "DCE8F6", 2: "E7DDF7", 3: "D9F2E1"}
    for i, st in enumerate(t["gf_status"]):
        wF.conditional_formatting.add(f"G{F0}:G{F1}", CellIsRule(operator="equal", formula=[f'"{st}"'], fill=PatternFill("solid", fgColor=colors[i])))
    wF.conditional_formatting.add(f"F{F0}:F{F1}", FormulaRule(formula=[f'AND(F{F0}<>"",E{F0}<>"",F{F0}>E{F0})'], font=Font(color="C0392B", bold=True)))

    # ---------------------------------------------------------- tasks
    wT["A1"] = SH[5]
    wT["A1"].font = TITLE
    for i, h in enumerate(t["t_head"], start=1):
        wT.cell(row=3, column=i, value=h)
    style_head(wT, 3, 5)
    T0 = 4
    T1 = T0 + TASK_ROWS - 1
    for i in range(TASK_ROWS):
        rr2 = T0 + i
        if i < len(t["tasks"]):
            wT.cell(row=rr2, column=1, value=t["tasks"][i][0])
            wT.cell(row=rr2, column=2, value=t["tasks"][i][1])
        for cc in (1, 2, 4, 5):
            box(wT.cell(row=rr2, column=cc), INPUT)
        box(wT.cell(row=rr2, column=3, value=f'=IF(B{rr2}="","",{qN}!$B$3-B{rr2})'), CALC, t["date_fmt"])
    if ex:
        for i in range(4):
            wT.cell(row=T0 + i, column=5, value="✓")
    dv_list(wT, t["done"], f"E{T0}:E{T1}")
    for col, w in zip("ABCDE", [48, 14, 14, 16, 10]):
        wT.column_dimensions[col].width = w
    wT.conditional_formatting.add(f"A{T0}:D{T1}", FormulaRule(formula=[f'$E{T0}="✓"'], font=Font(color="999999", strike=True)))
    wT.conditional_formatting.add(f"C{T0}:C{T1}", FormulaRule(formula=[f'AND($C{T0}<>"",$E{T0}<>"✓",$C{T0}<TODAY())'], font=Font(color="C0392B", bold=True)))
    wT.freeze_panes = f"A{T0}"

    # ---------------------------------------------------------- dashboard
    wD["A1"] = t["title"]
    wD["A1"].font = TITLE
    wD.column_dimensions["A"].width = 26
    wD.column_dimensions["B"].width = 16
    for col in "CDEFGHIJK":
        wD.column_dimensions[col].width = 12
    kf = [f"={qN}!{AD}", f"={qN}!{KD}", f"={qN}!B{rowof['suf']}", f"={qN}!B{rowof['latkes']}", f"={qN}!B{rowof['potatoes']}",
          f"={sN}!B3", f"={fN}!M{tr}", f"={fN}!N{tr}",
          f'=COUNTIF({tN}!E{T0}:E{T1},"✓")&" / "&COUNTA({tN}!A{T0}:A{T1})']
    fmts = ["0", "0", "#,##0", "#,##0", "#,##0.0", t["cur"], t["cur"], t["cur"], "@"]
    for i, (lbl, f, fm) in enumerate(zip(t["d_kpi"], kf, fmts)):
        rr2 = 3 + i
        c1 = wD.cell(row=rr2, column=1, value=lbl)
        c1.fill = SUB
        c1.font = BOLD
        c1.border = BOX
        c2 = wD.cell(row=rr2, column=2, value=f)
        box(c2, CALC, fm, True)
        c2.font = Font(bold=True, size=13, color="173A66")
        c2.alignment = Alignment(horizontal="center")
    # category cost table for pie (A14:B20)
    c0 = 14
    wD.cell(row=c0, column=1, value=t["d_cat_h"][0])
    wD.cell(row=c0, column=2, value=t["d_cat_h"][1])
    style_head(wD, c0, 2)
    for i, cat in enumerate(t["cats"]):
        rr2 = c0 + 1 + i
        wD.cell(row=rr2, column=1, value=cat).border = BOX
        box(wD.cell(row=rr2, column=2, value=f"=SUMIFS({sN}!F{S0}:F{m1},{sN}!D{S0}:D{m1},A{rr2})"), CALC, t["cur"])
    ch1 = BarChart()
    ch1.type = "col"
    ch1.title = t["d_chart1"]
    ch1.y_axis.title = None
    data = Reference(wF, min_col=13, max_col=14, min_row=F0 - 1, max_row=F0 + 7)
    cats = Reference(wF, min_col=10, min_row=F0, max_row=F0 + 7)
    ch1.add_data(data, titles_from_data=True)
    ch1.set_categories(cats)
    ch1.height, ch1.width = 7.5, 15
    ch1.series[0].graphicalProperties.solidFill = "F2B632"
    ch1.series[1].graphicalProperties.solidFill = "2F6DB5"
    wD.add_chart(ch1, "D3")
    ch2 = PieChart()
    ch2.title = t["d_chart2"]
    ch2.add_data(Reference(wD, min_col=2, min_row=c0 + 1, max_row=c0 + len(t["cats"])), titles_from_data=False)
    ch2.set_categories(Reference(wD, min_col=1, min_row=c0 + 1, max_row=c0 + len(t["cats"])))
    ch2.dataLabels = DataLabelList()
    ch2.dataLabels.showPercent = True
    ch2.dataLabels.showVal = False
    ch2.dataLabels.showCatName = False
    ch2.dataLabels.showSerName = False
    ch2.dataLabels.showLeaderLines = False
    ch2.height, ch2.width = 7.5, 15
    wD.add_chart(ch2, "D19")

    # fonts + print setup
    for ws in wss:
        for row in ws.iter_rows():
            for c in row:
                if c.font and c.font.name != t["font"]:
                    f = c.font
                    c.font = Font(name=t["font"], bold=f.bold, italic=f.italic, size=f.size, color=f.color, strike=f.strike)
        ws.page_setup.orientation = "landscape" if ws in (wG, wF) else "portrait"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4 if lang == "he" else ws.PAPERSIZE_LETTER
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.active = 0
    wb.properties.title = t["title"]
    wb.properties.creator = "Tichnun Plus"
    name = f"hanukkah-party-planner-{lang}{'-example' if example else ''}.xlsx"
    OUT.mkdir(exist_ok=True)
    wb.save(OUT / name)
    return OUT / name


if __name__ == "__main__":
    for lang in ("he", "en"):
        for exm in (False, True):
            print(build(lang, exm))
