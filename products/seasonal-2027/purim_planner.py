#!/usr/bin/env python3
"""מתכנן משלוחי מנות – פורים 2027 (.xlsx, Hebrew RTL). Recipients, package types (cost per package from its items),
shopping list scaled by how many of each package, delivery route by stop number, מתנות לאביונים, dashboard with charts.
    python3 purim_planner.py   -> out/purim-planner-2027.xlsx, out/purim-planner-2027-example.xlsx
Prices are examples only (stated in the file)."""
import datetime
import pathlib

from xlhe import *  # noqa: F401,F403

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
SH = ["הוראות", "הגדרות", "חבילות", "נמענים", "רשימת קניות", "מסלול חלוקה", "דשבורד"]
S_SET, S_PKG, S_REC, S_SHOP, S_ROUTE, S_DASH = (q(x) for x in SH[1:])
N_PKG, N_ITEM, N_REC = 8, 60, 150
P0 = 5                      # package table first row (rows 5..12)
I0 = 17                     # item table first row (rows 17..76)
R0 = 7                      # recipients first row
CAT0 = 16                   # categories in settings A16:A23
TYPES = ["מאכל", "משקה", "אריזה", "קישוט", "אחר"]
STATUS = ["טרם", "מוכן", "✓ נמסר"]
WHO = ["אני", "בן/בת הזוג", "הילדים", "שליח", "בדואר/איסוף"]
CATS = ["משפחה", "שכנים", "חברים", "גן / כיתה", "עבודה", "בית כנסת / קהילה", "צוות (מורים, מטפלים)", "אחר"]

# package name, description, [(item, type, qty, unit, price)]
PKGS = [
    ("בסיסית", "לשכנים ולחברים", [("אוזני המן", "מאכל", 3, "יח׳", 1.5), ("שוקולד קטן", "מאכל", 1, "יח׳", 3.5),
                                    ("מיץ / שתייה קטנה", "משקה", 1, "יח׳", 2.5), ("שקית צלופן + סרט", "אריזה", 1, "יח׳", 1)]),
    ("משפחתית", "למשפחה הקרובה", [("עוגה ביתית / מאפה", "מאכל", 1, "יח׳", 12), ("בקבוק יין", "משקה", 1, "בקבוק", 30),
                                  ("פירות יבשים / פיצוחים", "מאכל", 1, "שקית", 8), ("סלסלה", "אריזה", 1, "יח׳", 6)]),
    ("לגן ולכיתה", "חבילה קטנה לילד", [("סוכריות / ממתק", "מאכל", 2, "יח׳", 1), ("חטיף קטן", "מאכל", 1, "יח׳", 1.5),
                                       ("שקית + מדבקה", "אריזה", 1, "יח׳", 0.5)]),
]
EX_PKGS = PKGS + [("לצוות", "לגננת, למורה ולמטפלת", [("מארז פרלינים", "מאכל", 1, "מארז", 18), ("קפה / תה מיוחד", "משקה", 1, "יח׳", 12),
                                                     ("כרטיס תודה", "קישוט", 1, "יח׳", 2), ("שקית מתנה", "אריזה", 1, "יח׳", 3)])]
# name, category, package, qty, address, stop, who, status, got-from-them, note
EX_REC = [
    ("סבא וסבתא כהן", "משפחה", "משפחתית", 1, "רח׳ הזית 4", 6, "אני", "מוכן", "כן", ""),
    ("דודה רונית", "משפחה", "משפחתית", 1, "רח׳ הגפן 12", 7, "אני", "טרם", "", ""),
    ("משפחת לוי (קומה 2)", "שכנים", "בסיסית", 1, "בבניין", 1, "הילדים", "✓ נמסר", "כן", ""),
    ("משפחת אברהם (קומה 3)", "שכנים", "בסיסית", 1, "בבניין", 2, "הילדים", "✓ נמסר", "", ""),
    ("משפחת מזרחי (קומה 4)", "שכנים", "בסיסית", 1, "בבניין", 3, "הילדים", "מוכן", "", "אלרגיה לבוטנים"),
    ("יעל ודני", "חברים", "בסיסית", 1, "רח׳ הרימון 8", 4, "אני", "מוכן", "כן", ""),
    ("משפחת פרץ", "חברים", "בסיסית", 1, "רח׳ התאנה 3", 5, "אני", "טרם", "", ""),
    ("גן החצב – כל הילדים", "גן / כיתה", "לגן ולכיתה", 28, "גן החצב", 8, "בן/בת הזוג", "טרם", "", "בלי בוטנים (גן נקי)"),
    ("כיתה ב׳2 – כל הילדים", "גן / כיתה", "לגן ולכיתה", 32, "בית הספר", 9, "הילדים", "טרם", "", "לפי הנחיות המחנכת"),
    ("הגננת והסייעת", "צוות (מורים, מטפלים)", "לצוות", 2, "גן החצב", 8, "בן/בת הזוג", "טרם", "", ""),
    ("המחנכת", "צוות (מורים, מטפלים)", "לצוות", 1, "בית הספר", 9, "הילדים", "טרם", "", ""),
    ("צוות המשרד", "עבודה", "בסיסית", 6, "", None, "אני", "טרם", "", "מביאים ביום ב׳"),
    ("הרב והרבנית", "בית כנסת / קהילה", "משפחתית", 1, "בית הכנסת", 10, "אני", "טרם", "", ""),
    ("השכנה מהבית ממול", "שכנים", "בסיסית", 1, "רח׳ הזית 5", None, "", "טרם", "", ""),
]


def build(example=False):
    wb, (wI, wS, wP, wR, wSh, wRt, wD) = book(SH)
    props(wb, "מתכנן משלוחי מנות – פורים 2027", "משלוחי מנות: נמענים, חבילות, קניות, מסלול חלוקה ותקציב")
    pk = EX_PKGS if example else PKGS
    P1, I1, R1 = P0 + N_PKG - 1, I0 + N_ITEM - 1, R0 + N_REC - 1
    pkg_names = f"={S_PKG}!$A${P0}:$A${P1}"
    pkg_tbl = f"{S_PKG}!$A${P0}:$E${P1}"
    it_pkg, it_type, it_cost = (f"{S_PKG}!${c}${I0}:${c}${I1}" for c in "ACG")
    rec_cat, rec_pkg, rec_cnt, rec_cost, rec_stop, rec_st = (f"{S_REC}!${c}${R0}:${c}${R1}" for c in "CDLMGI")

    # ------------------------------------------------------------ instructions
    instructions(wI, "מתכנן משלוחי מנות – פורים 2027",
                 "פורים תשפ״ז חל ביום שלישי, 23 במרץ 2027 (י״ד באדר ב׳). בירושלים חוגגים שושן פורים ביום רביעי, 24 במרץ. "
                 "הקובץ עוזר לתכנן למי שולחים, מה שמים בכל חבילה, כמה זה עולה ומה לקנות, ולחלק הכול בסבב אחד מסודר.",
                 [("מה יש בקובץ", [
                     ("הגדרות", "שם המשפחה, תאריך פורים, תקציב כולל, מתנות לאביונים, ורשימת הקבוצות (משפחה, שכנים, גן…) שאפשר לשנות."),
                     ("חבילות", "עד 8 סוגי חבילות. לכל חבילה רושמים את הפריטים שבה, והקובץ מחשב עלות לחבילה, כמה חבילות מכל סוג צריך, "
                                "ובודק שיש בה לפחות שני מיני מאכל או משקה."),
                     ("נמענים", "עד 150 שורות: שם, קבוצה, איזו חבילה, כמה (לגן או לכיתה רושמים את מספר הילדים), כתובת, מספר עצירה בסבב, "
                                "מי מוסר, סטטוס ואם קיבלתם מהם."),
                     ("רשימת קניות", "נבנית לבד: כל פריט כפול מספר החבילות שצריך, עם עלות ועמודת «נקנה»."),
                     ("מסלול חלוקה", "מסדר את הנמענים לפי מספר העצירה שנתתם להם, כדי לחלק הכול בסבב אחד בלי לחזור על עצמכם."),
                     ("דשבורד", "כמה נמענים וחבילות, עלות כוללת מול התקציב, כמה כבר נמסרו, וגרפים לפי קבוצה ולפי סוג חבילה.")]),
                  ("איך עובדים", [
                      ("1", "מקלידים רק בתאים הצהובים. כל השאר מחושב בנוסחאות."),
                      ("2", "מתחילים ב«חבילות»: נותנים שם לכל סוג חבילה ומוסיפים לה פריטים בטבלת הרכיבים. המחירים שבקובץ הם דוגמה בלבד, עדכנו לפי החנות שלכם."),
                      ("3", "ב«נמענים» בוחרים לכל שורה קבוצה וסוג חבילה מהרשימה. אם משאירים «כמות» ריקה, נספרת חבילה אחת."),
                      ("4", "רוצים מסלול? תנו לכל נמען מספר עצירה (1, 2, 3…) לפי הסדר שבו תעברו. נמען בלי מספר לא יופיע במסלול."),
                      ("5", "ביום פורים מעדכנים סטטוס «✓ נמסר», והדשבורד מראה כמה נשארו.")]),
                  ("כמה מילים על המצווה", [
                      ("משלוח מנות", "לפחות שתי מנות (שני סוגי מאכל או משקה) לאדם אחד לפחות, ביום פורים. מקור: מגילת אסתר ט, יט–כב; "
                                     "שולחן ערוך אורח חיים סימן תרצ״ה סעיף ד׳. הבדיקה «שני מינים» בגיליון החבילות היא תזכורת בלבד."),
                      ("מתנות לאביונים", "לפחות שתי מתנות לשני אביונים (מתנה לכל אחד) ביום פורים. מקור: שו״ע או״ח סימן תרצ״ד סעיף א׳. "
                                         "את הסכום לכל מתנה קובעים בגיליון ההגדרות. לשאלות הלכתיות פנו לרב."),
                      ("הערה", "הקובץ הוא כלי תכנון, לא פסק הלכה. הסכומים והמחירים לדוגמה בלבד.")])])

    # ------------------------------------------------------------ settings
    title(wS, "הגדרות", "ממלאים פעם אחת. התאריך והתקציב משמשים את הדשבורד.")
    widths(wS, {"A": 34, "B": 22, "C": 60})
    rows = [("שם המשפחה", "משפחת ישראלי" if example else None, "in", None, ""),
            ("תאריך פורים", datetime.date(2027, 3, 23), "in", DATE, "י״ד באדר ב׳ תשפ״ז. בירושלים: 24/03/2027 (שושן פורים)."),
            ("תקציב כולל למשלוחי מנות", 1500 if example else 800, "in", CUR, "כמה אתם מוכנים להוציא על כל החבילות יחד"),
            ("מתנות לאביונים: מספר מתנות", 4 if example else 2, "in", "0", "לפחות 2 (מתנה אחת לכל אחד משני אביונים)"),
            ("מתנות לאביונים: סכום לכל מתנה", 50 if example else None, "in", CUR, "הסכום שאתם בוחרים. לשאלות הלכתיות פנו לרב."),
            ("סה״כ מתנות לאביונים", "=B7*B8", "calc", CUR, ""),
            ("מחצית השקל: מספר אנשים", 4 if example else None, "in", "0", "אופציונלי. נוהגים לתת לפני פורים."),
            ("מחצית השקל: סכום לאדם", 15 if example else None, "in", CUR2, "הסכום מתפרסם מדי שנה. בדקו מול בית הכנסת או הרבנות."),
            ("סה״כ מחצית השקל", "=B10*B11", "calc", CUR, "")]
    for i, (lbl, v, kind, fmt, note) in enumerate(rows):
        r = 4 + i
        cell(wS, f"A{r}", lbl, "sub")
        cell(wS, f"B{r}", v, kind, fmt, align="center")
        wS[f"C{r}"] = note
        wS[f"C{r}"].font = MUTED
    dv_date(wS, "B5")
    dv_num(wS, "B6:B11", 0, 1000000)
    head(wS, CAT0 - 1, ["קבוצות נמענים (אפשר לשנות)"])
    for i in range(8):
        cell(wS, f"A{CAT0 + i}", CATS[i], "in")

    # ------------------------------------------------------------ packages
    title(wP, "חבילות", "טבלה עליונה: סוגי החבילות. טבלה תחתונה: מה יש בכל חבילה. העלות וכמות החבילות מחושבות לבד.")
    widths(wP, {"A": 20, "B": 30, "C": 14, "D": 12, "E": 14, "F": 14, "G": 14, "H": 26})
    head(wP, P0 - 1, ["סוג חבילה", "למי / תיאור", "עלות לחבילה", "כמה צריך", "עלות כוללת", "שני מינים?"])
    for i in range(N_PKG):
        r = P0 + i
        name, desc = (pk[i][0], pk[i][1]) if i < len(pk) else (None, None)
        cell(wP, f"A{r}", name, "in", bold=True)
        cell(wP, f"B{r}", desc, "in")
        cell(wP, f"C{r}", f'=IF(A{r}="","",SUMIF({it_pkg},A{r},{it_cost}))', "calc", CUR2, align="center")
        cell(wP, f"D{r}", f'=IF(A{r}="","",SUMIF({rec_pkg},A{r},{rec_cnt}))', "calc", "0", align="center")
        cell(wP, f"E{r}", f'=IF(A{r}="","",C{r}*D{r})', "calc", CUR, align="center")
        cell(wP, f"F{r}", f'=IF(A{r}="","",IF(COUNTIFS({it_pkg},A{r},{it_type},"מאכל")+COUNTIFS({it_pkg},A{r},{it_type},"משקה")>=2,'
                          f'"✓ שני מינים","⚠ הוסיפו מין"))', "calc", align="center")
    cf_fill(wP, f"F{P0}:F{P1}", f'LEFT(F{P0},1)="⚠"', WARN)
    cf_fill(wP, f"F{P0}:F{P1}", f'LEFT(F{P0},1)="✓"', OKF)
    cell(wP, f"D{P1 + 1}", f"=SUM(D{P0}:D{P1})", "sub", "0", align="center")
    cell(wP, f"E{P1 + 1}", f"=SUM(E{P0}:E{P1})", "sub", CUR, align="center")
    cell(wP, f"C{P1 + 1}", "סה״כ", "sub", align="center")
    wP[f"A{I0 - 2}"] = "רכיבי החבילות"
    wP[f"A{I0 - 2}"].font = Font(name="Arial", bold=True, size=14, color="173A66")
    head(wP, I0 - 1, ["חבילה", "פריט", "סוג", "כמות לחבילה", "יחידה", "מחיר ליחידה", "עלות לחבילה", "הערה"])
    items = [(p[0], *it) for p in pk for it in p[2]]
    for i in range(N_ITEM):
        r = I0 + i
        v = items[i] if i < len(items) else [None] * 6
        cell(wP, f"A{r}", v[0], "in")
        cell(wP, f"B{r}", v[1], "in")
        cell(wP, f"C{r}", v[2], "in", align="center")
        cell(wP, f"D{r}", v[3], "in", "0.##", align="center")
        cell(wP, f"E{r}", v[4], "in", align="center")
        cell(wP, f"F{r}", v[5], "in", CUR2, align="center")
        cell(wP, f"G{r}", f'=IF(OR(A{r}="",B{r}=""),"",N(D{r})*N(F{r}))', "calc", CUR2, align="center")
        cell(wP, f"H{r}", None, "in")
    dv_list(wP, pkg_names, f"A{I0}:A{I1}", "בחרו חבילה מהטבלה העליונה")
    dv_list(wP, TYPES, f"C{I0}:C{I1}")
    dv_num(wP, f"D{I0}:D{I1}", 0, 10000)
    dv_num(wP, f"F{I0}:F{I1}", 0, 100000)
    wP.freeze_panes = "A5"

    # ------------------------------------------------------------ recipients
    title(wR, "נמענים", "לגן או לכיתה: שורה אחת עם מספר הילדים בעמודת «כמות». «כמות» ריקה = חבילה אחת.")
    widths(wR, {"A": 5, "B": 28, "C": 18, "D": 16, "E": 8, "F": 22, "G": 9, "H": 13, "I": 11, "J": 11, "K": 28, "L": 9, "M": 12})
    for i, (lbl, f, fmt) in enumerate([("נמענים", f'=COUNTA(B{R0}:B{R0 + N_REC - 1})', "0"),
                                       ("חבילות", f"=SUM(L{R0}:L{R0 + N_REC - 1})", "0"),
                                       ("נמסרו", f'=SUMIF(I{R0}:I{R0 + N_REC - 1},"✓ נמסר",L{R0}:L{R0 + N_REC - 1})', "0"),
                                       ("עלות", f"=SUM(M{R0}:M{R0 + N_REC - 1})", CUR)]):
        cell(wR, f"{'BCDE'[i]}3", lbl, "sub", align="center")
        cell(wR, f"{'BCDE'[i]}4", f, "calc", fmt, bold=True, align="center")
    head(wR, R0 - 1, ["#", "שם", "קבוצה", "חבילה", "כמות", "כתובת / מקום", "עצירה בסבב", "מי מוסר", "סטטוס", "קיבלנו מהם?", "הערות (אלרגיות…)",
                      "נספר", "עלות"])
    ex = EX_REC if example else []
    for i in range(N_REC):
        r = R0 + i
        v = ex[i] if i < len(ex) else [None] * 10
        cell(wR, f"A{r}", f'=IF(B{r}="","",ROW()-{R0 - 1})', "calc", align="center")
        for col, val, fmt in zip("BCDEFGHIJK", v, [None, None, None, "0", None, "0", None, None, None, None]):
            cell(wR, f"{col}{r}", val if val != "" else None, "in", fmt, align="center" if col in "EGIJ" else None)
        cell(wR, f"L{r}", f'=IF(OR(B{r}="",D{r}=""),0,IF(E{r}="",1,E{r}))', "calc", "0", align="center")
        cell(wR, f"M{r}", f'=IF(L{r}=0,0,L{r}*IFERROR(VLOOKUP(D{r},{pkg_tbl},3,FALSE),0))', "calc", CUR, align="center")
        # route key: stop number + row/10000 (stable order when several recipients share a stop); blank when no stop
        wR[f"N{r}"] = f'=IF(OR(B{r}="",G{r}=""),"",G{r}+ROW()/10000)'
        wR[f"N{r}"].font = Font(name="Arial", size=8, color="BBBBBB")
    dv_list(wR, f"={S_SET}!$A${CAT0}:$A${CAT0 + 7}", f"C{R0}:C{R1}")
    dv_list(wR, pkg_names, f"D{R0}:D{R1}")
    dv_list(wR, WHO, f"H{R0}:H{R1}")
    dv_list(wR, STATUS, f"I{R0}:I{R1}")
    dv_list(wR, ["כן", "לא"], f"J{R0}:J{R1}")
    dv_num(wR, f"E{R0}:E{R1}", 0, 1000, True)
    dv_num(wR, f"G{R0}:G{R1}", 1, N_REC, True)
    cf_fill(wR, f"B{R0}:K{R1}", f'$I{R0}="✓ נמסר"', OKF)
    wR.column_dimensions["N"].hidden = True
    wR.freeze_panes = f"C{R0}"
    wR.auto_filter.ref = f"A{R0 - 1}:M{R1}"

    # ------------------------------------------------------------ shopping list
    title(wSh, "רשימת קניות", "נבנית לבד מהחבילות ומכמות הנמענים. עמודת «סה״כ מהפריט» מחברת פריט שמופיע בכמה חבילות.")
    widths(wSh, {"A": 28, "B": 16, "C": 12, "D": 10, "E": 13, "F": 13, "G": 16, "H": 12})
    cell(wSh, "A3", "עלות קניות משוערת", "sub")
    cell(wSh, "B3", f"=SUM(F6:F{5 + N_ITEM})", "calc", CUR, bold=True, align="center")
    cell(wSh, "C3", "נקנה", "sub", align="center")
    cell(wSh, "D3", f'=COUNTIF(H6:H{5 + N_ITEM},"✓")&" / "&COUNTIF(A6:A{5 + N_ITEM},"?*")', "calc", align="center")
    head(wSh, 5, ["פריט", "לחבילה", "כמות לקנות", "יחידה", "מחיר ליחידה", "עלות", "סה״כ מהפריט (כל החבילות)", "נקנה?"])
    for i in range(N_ITEM):
        r, s = 6 + i, I0 + i
        cell(wSh, f"A{r}", f'=IF(OR({S_PKG}!B{s}="",{S_PKG}!A{s}=""),"",{S_PKG}!B{s})', "calc")
        cell(wSh, f"B{r}", f'=IF(A{r}="","",{S_PKG}!A{s})', "calc")
        cell(wSh, f"C{r}", f'=IF(A{r}="","",N({S_PKG}!D{s})*N(IFERROR(VLOOKUP(B{r},{pkg_tbl},4,FALSE),0)))', "calc", "0.##", align="center")
        cell(wSh, f"D{r}", f'=IF(A{r}="","",{S_PKG}!E{s}&"")', "calc", align="center")
        cell(wSh, f"E{r}", f'=IF(A{r}="","",N({S_PKG}!F{s}))', "calc", CUR2, align="center")
        cell(wSh, f"F{r}", f'=IF(A{r}="",0,C{r}*E{r})', "calc", CUR, align="center")
        cell(wSh, f"G{r}", f'=IF(A{r}="","",SUMIF($A$6:$A${5 + N_ITEM},A{r},$C$6:$C${5 + N_ITEM}))', "calc", "0.##", align="center")
        cell(wSh, f"H{r}", "✓" if example and i in (0, 1, 4) else None, "in", align="center")
    dv_list(wSh, ["✓"], f"H6:H{5 + N_ITEM}")
    cf_fill(wSh, f"A6:G{5 + N_ITEM}", '$H6="✓"', OKF)
    wSh.freeze_panes = "A6"

    # ------------------------------------------------------------ route
    title(wRt, "מסלול חלוקה", "מסודר לפי «עצירה בסבב» שבגיליון הנמענים. כמה נמענים באותה עצירה (למשל גן) מופיעים זה אחרי זה.")
    widths(wRt, {"A": 9, "B": 28, "C": 22, "D": 16, "E": 8, "F": 13, "G": 11, "H": 28})
    head(wRt, 4, ["עצירה", "שם", "כתובת / מקום", "חבילה", "כמות", "מי מוסר", "סטטוס", "הערות"])
    rec_key = f"{S_REC}!$N${R0}:$N${R1}"
    for i in range(N_REC):
        r = 5 + i
        wRt[f"J{r}"] = f'=IF(COUNT({rec_key})<{i + 1},"",SMALL({rec_key},{i + 1}))'
        wRt[f"J{r}"].number_format = "0.0000"
        wRt[f"J{r}"].font = Font(name="Arial", size=8, color="BBBBBB")
        cell(wRt, f"A{r}", f'=IF(J{r}="","",INT(J{r}))', "calc", "0", align="center")
        rowx = f"ROUND(MOD(J{r},1)*10000,0)-{R0 - 1}"
        for col, src in zip("BCDEFGH", "BFDLHIK"):
            cell(wRt, f"{col}{r}", f'=IF($A{r}="","",INDEX({S_REC}!${src}${R0}:${src}${R1},{rowx})&"")' if col != "E" else
                 f'=IF($A{r}="","",INDEX({S_REC}!$L${R0}:$L${R1},{rowx}))', "calc", align="center" if col in "AEG" else None)
    wRt.column_dimensions["J"].hidden = True
    cf_fill(wRt, f"A5:H{4 + N_REC}", '$G5="✓ נמסר"', OKF)
    wRt.freeze_panes = "A5"

    # ------------------------------------------------------------ dashboard
    title(wD, "דשבורד פורים 2027", "הכול במבט אחד. מתעדכן לבד.")
    widths(wD, {"A": 30, "B": 16, "C": 34, "E": 22, "F": 12, "G": 13})
    kpi(wD, 4, "ימים עד פורים", f"=MAX(0,{S_SET}!B5-TODAY())", "0", "נכון להיום")
    kpi(wD, 5, "נמענים", f"={S_REC}!B4", "0")
    kpi(wD, 6, "חבילות להכין", f"={S_REC}!C4", "0")
    kpi(wD, 7, "נמסרו", f"={S_REC}!D4", "0", "חבילות שסומנו «✓ נמסר»")
    kpi(wD, 8, "עלות משלוחי מנות", f"={S_REC}!E4", CUR)
    kpi(wD, 9, "תקציב למשלוחי מנות", f"={S_SET}!B6", CUR)
    kpi(wD, 10, "נותר בתקציב", "=B9-B8", CUR, "מספר שלילי = חריגה")
    kpi(wD, 11, "עלות ממוצעת לחבילה", '=IF(B6=0,0,B8/B6)', CUR2)
    kpi(wD, 12, "מתנות לאביונים + מחצית השקל", f"={S_SET}!B9+{S_SET}!B12", CUR)
    kpi(wD, 13, "סה״כ הוצאות פורים", "=B8+B12", CUR)
    cf_fill(wD, "B10", "B10<0", WARN)
    head(wD, 3, ["לפי קבוצה", "חבילות", "עלות"], col0=5)
    for i in range(8):
        r = 4 + i
        cell(wD, f"E{r}", f"={S_SET}!A{CAT0 + i}&\"\"", "calc")
        cell(wD, f"F{r}", f'=IF(E{r}="",0,SUMIF({rec_cat},E{r},{rec_cnt}))', "calc", "0", align="center")
        cell(wD, f"G{r}", f'=IF(E{r}="",0,SUMIF({rec_cat},E{r},{rec_cost}))', "calc", CUR, align="center")
    head(wD, 14, ["לפי סוג חבילה", "חבילות", "עלות"], col0=5)
    for i in range(N_PKG):
        r = 15 + i
        cell(wD, f"E{r}", f"={S_PKG}!A{P0 + i}&\"\"", "calc")
        cell(wD, f"F{r}", f'=IF(E{r}="",0,N({S_PKG}!D{P0 + i}))', "calc", "0", align="center")
        cell(wD, f"G{r}", f'=IF(E{r}="",0,N({S_PKG}!E{P0 + i}))', "calc", CUR, align="center")
    bar(wD, "A16", "עלות לפי קבוצה (₪)", wD, Reference(wD, min_col=5, min_row=4, max_row=11),
        Reference(wD, min_col=7, min_row=3, max_row=11), number_format="#,##0")
    pie(wD, "I3", "חבילות לפי סוג", Reference(wD, min_col=5, min_row=15, max_row=14 + N_PKG),
        Reference(wD, min_col=6, min_row=14, max_row=14 + N_PKG))
    wb.active = 6 if example else 0
    return wb


def main():
    OUT.mkdir(exist_ok=True)
    for ex, name in ((False, "purim-planner-2027.xlsx"), (True, "purim-planner-2027-example.xlsx")):
        build(ex).save(OUT / name)
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
