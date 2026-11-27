#!/usr/bin/env python3
"""Wedding Budget Planner (English, USD, general audience) -> etsy/listings/06-wedding-budget-planner/files/."""
import datetime as dt
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "products" / "en-jewish-life"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from xl import *  # noqa: F401,F403,E402
import xl  # noqa: E402
from clean import clean_xlsx  # noqa: E402

xl.SITE = "https://tichnun.netlify.app/en/"  # removed by clean_xlsx
D = dt.date
SD = "mmm d, yyyy"
S_SET, S_BUD, S_EXP, S_VEN, S_DASH = "Settings", "Budget", "Expenses & Payments", "Vendor Quotes", "Dashboard"
N_CATS, N_EXP, N_VEN = 20, 120, 60
CATS = [("Venue & rentals", .20), ("Catering, cake & bar", .25), ("Photography & video", .11), ("Music / DJ / band", .06),
        ("Flowers & decor", .08), ("Attire & accessories", .06), ("Hair & makeup", .02), ("Rings", .03),
        ("Officiant & ceremony", .01), ("Invitations & stationery", .02), ("Transportation", .02),
        ("Favors & gifts", .015), ("Wedding planner / coordinator", .03), ("Rehearsal dinner & other events", .025),
        ("Tips & gratuities", .02), ("Unexpected / buffer", .05)]
DEMO_EST = [9000, 13000, 4800, 2200, 3200, 2400, 700, 1500, 400, 700, 600, 500, 0, 1200, 800, 2000]
DEMO_EXP = [  # date, cat, vendor, desc, amount, paid, due
    (D(2026, 6, 3), "Venue & rentals", "Oak Hill Barn", "Venue deposit", 3000, "Yes", None),
    (None, "Venue & rentals", "Oak Hill Barn", "Venue balance", 6200, "No", D(2027, 5, 1)),
    (D(2026, 7, 10), "Catering, cake & bar", "Fresh Table Catering", "Catering deposit (120 guests)", 4000, "Yes", None),
    (None, "Catering, cake & bar", "Fresh Table Catering", "Catering balance", 9200, "No", D(2027, 5, 20)),
    (D(2026, 8, 2), "Photography & video", "Lightbox Studio", "Retainer", 1500, "Yes", None),
    (None, "Photography & video", "Lightbox Studio", "Balance", 3300, "No", D(2027, 5, 29)),
    (D(2026, 9, 14), "Attire & accessories", "Bella Bridal", "Dress", 1650, "Yes", None),
    (None, "Attire & accessories", "Menswear Co.", "Suit rental", 280, "No", D(2027, 4, 15)),
    (D(2026, 10, 1), "Rings", "Main St Jewelers", "Two bands", 1350, "Yes", None),
    (D(2026, 10, 20), "Invitations & stationery", "Paper Lane", "Save the dates + postage", 260, "Yes", None),
    (None, "Music / DJ / band", "DJ Marcus", "DJ deposit", 600, "No", D(2026, 11, 20)),
    (None, "Flowers & decor", "Wildflower Co.", "Florist deposit", 900, "No", D(2027, 1, 15)),
]
DEMO_VEN = [("Photography & video", "Lightbox Studio", 4800, "8 hrs, 2 shooters, album", 5, "Yes"),
            ("Photography & video", "Sunny Days Photo", 4200, "6 hrs, 1 shooter", 4, "No"),
            ("Photography & video", "Ever After Films", 5600, "Photo + video", 4, "No"),
            ("Music / DJ / band", "DJ Marcus", 2100, "5 hrs, ceremony sound", 5, "Yes"),
            ("Music / DJ / band", "The Groove Band", 5200, "4-piece band", 5, "No"),
            ("Flowers & decor", "Wildflower Co.", 3100, "Bouquets, centerpieces, arch", 4, "Yes"),
            ("Flowers & decor", "Bloom Room", 3600, "Full service", 3, "No")]


def build(demo=False):
    wb = new_book()
    # ---------------- Settings
    ws = sheet(wb, S_SET, "Settings", "Your names, date, total budget and guest count. Category names live here too: rename them freely.",
               [30, 22, 4, 34, 13], tab="C9A227")
    rows = [("Couple", "Emma & James" if demo else None, None), ("Wedding date", D(2027, 6, 5) if demo else None, DATE),
            ("Total budget", 45000 if demo else None, USD), ("Expected guests", 120 if demo else None, NUM),
            ("Today (leave empty = today)", D(2026, 11, 17) if demo else None, DATE)]
    for i, (lbl, v, f) in enumerate(rows):
        r = 4 + i
        put(ws, f"A{r}", lbl, bold=True)
        put(ws, f"B{r}", v, "input", f)
    define(wb, "w_date", f"{q(S_SET)}!$B$5")
    define(wb, "budget_cap", f"{q(S_SET)}!$B$6")
    define(wb, "guests_n", f"{q(S_SET)}!$B$7")
    put(ws, "A10", "Today used", bold=True)
    put(ws, "B10", "=IF(B8=\"\",TODAY(),B8)", "calc", DATE)
    define(wb, "today_", f"{q(S_SET)}!$B$10")
    put(ws, "D3", "Budget categories (rename / add)", "head")
    put(ws, "E3", "Suggested %", "head")
    for i in range(N_CATS):
        r = 4 + i
        put(ws, f"D{r}", CATS[i][0] if i < len(CATS) else None, "input")
        put(ws, f"E{r}", CATS[i][1] if i < len(CATS) else None, "input", PCT)
    define(wb, "cat_list", f"{q(S_SET)}!$D$4:$D${3 + N_CATS}")
    put(ws, "D25", "Suggested % are common rules of thumb, not advice. Change them to fit your plans.", size=9, italic=True, color="6B7780")

    # ---------------- Budget
    ws = sheet(wb, S_BUD, "Budget by category",
               "Estimate = what you plan to spend. Committed = everything entered on Expenses & Payments. Paid = rows marked Paid.",
               [32, 12, 14, 14, 14, 14, 14, 16], tab="2E7D32")
    headers(ws, 4, ["Category", "Suggested %", "Suggested $", "Your estimate", "Committed", "Paid", "Still to pay", "Estimate − committed"])
    E = lambda c: col(S_EXP, c, N_EXP)  # noqa: E731
    for i in range(N_CATS):
        r = FIRST + i
        put(ws, f"A{r}", f"=IF({q(S_SET)}!D{4 + i}=\"\",\"\",{q(S_SET)}!D{4 + i})", "calc", bold=True)
        put(ws, f"B{r}", f"=IF({q(S_SET)}!E{4 + i}=\"\",\"\",{q(S_SET)}!E{4 + i})", "calc", PCT)
        put(ws, f"C{r}", f"=IF(OR(A{r}=\"\",B{r}=\"\",budget_cap=\"\"),\"\",budget_cap*B{r})", "calc", USD)
        put(ws, f"D{r}", DEMO_EST[i] if demo and i < len(DEMO_EST) else None, "input", USD)
        put(ws, f"E{r}", f"=IF(A{r}=\"\",\"\",SUMIFS({E('E')},{E('B')},A{r}))", "calc", USD)
        put(ws, f"F{r}", f"=IF(A{r}=\"\",\"\",SUMIFS({E('E')},{E('B')},A{r},{E('F')},\"Yes\"))", "calc", USD)
        put(ws, f"G{r}", f"=IF(A{r}=\"\",\"\",E{r}-F{r})", "calc", USD)
        put(ws, f"H{r}", f"=IF(OR(A{r}=\"\",D{r}=\"\"),\"\",D{r}-E{r})", "calc", USD)
    t = FIRST + N_CATS
    put(ws, f"A{t}", "Total", "total")
    for L_ in "BCDEFGH":
        put(ws, f"{L_}{t}", f"=SUM({L_}{FIRST}:{L_}{t - 1})", "total", PCT if L_ == "B" else USD)
    define(wb, "tot_est", f"{q(S_BUD)}!$D${t}")
    define(wb, "tot_com", f"{q(S_BUD)}!$E${t}")
    define(wb, "tot_paid", f"{q(S_BUD)}!$F${t}")
    cf(ws, f"H{FIRST}:H{t - 1}", f"AND(ISNUMBER(H{FIRST}),H{FIRST}<0)", C_BAD)
    put(ws, f"A{t + 2}", "Red in the last column = you committed more than your estimate for that category.", size=9, italic=True, color="6B7780")

    # ---------------- Expenses & Payments
    ws = sheet(wb, S_EXP, "Expenses & payments",
               "One row per payment or bill (deposit, installment, balance). Paid? = Yes when paid. Unpaid rows past their due date turn red.",
               [15, 30, 24, 32, 13, 9, 15, 14, 24], tab="1565C0")
    headers(ws, 4, ["Date paid", "Category", "Vendor", "What for", "Amount", "Paid?", "Due date", "Status", "Notes"])
    blank_rows(ws, FIRST, N_EXP, ["input"] * 7 + ["calc", "input"], {1: SD, 5: USD, 7: SD})
    for r in range(FIRST, FIRST + N_EXP):
        ws[f"H{r}"] = (f"=IF(E{r}=\"\",\"\",IF(F{r}=\"Yes\",\"Paid\",IF(G{r}=\"\",\"To pay\","
                       f"IF(G{r}<today_,\"OVERDUE\",IF(G{r}-today_<=30,\"Due soon\",\"Upcoming\")))))")
    if demo:
        for i, row in enumerate(DEMO_EXP):
            for j, v in enumerate(row):
                ws.cell(row=FIRST + i, column=j + 1, value=v)
    last = FIRST + N_EXP - 1
    dv_list(ws, "=cat_list", f"B{FIRST}:B{last}")
    dv_list(ws, '"Yes,No"', f"F{FIRST}:F{last}")
    dv_number(ws, f"E{FIRST}:E{last}")
    cf(ws, f"H{FIRST}:H{last}", f'H{FIRST}="OVERDUE"', C_BAD, bold=True)
    cf(ws, f"H{FIRST}:H{last}", f'H{FIRST}="Due soon"', C_WARN)
    cf(ws, f"H{FIRST}:H{last}", f'H{FIRST}="Paid"', C_OK)

    # ---------------- Vendor quotes
    ws = sheet(wb, S_VEN, "Vendor quotes",
               "Compare quotes before you book. Mark the one you choose; the cheapest quote per category is highlighted.",
               [30, 26, 13, 40, 10, 10, 24], tab="8E24AA")
    headers(ws, 4, ["Category", "Vendor", "Quote", "What's included", "Rating 1–5", "Chosen?", "Contact / notes"])
    blank_rows(ws, FIRST, N_VEN, ["input"] * 7, {3: USD})
    if demo:
        for i, row in enumerate(DEMO_VEN):
            for j, v in enumerate(row):
                ws.cell(row=FIRST + i, column=j + 1, value=v)
    lv = FIRST + N_VEN - 1
    dv_list(ws, "=cat_list", f"A{FIRST}:A{lv}")
    dv_list(ws, '"Yes,No,Maybe"', f"F{FIRST}:F{lv}")
    dv_list(ws, '"1,2,3,4,5"', f"E{FIRST}:E{lv}")
    cf(ws, f"F{FIRST}:F{lv}", f'F{FIRST}="Yes"', C_OK, bold=True)
    cf(ws, f"C{FIRST}:C{lv}", f'AND(ISNUMBER(C{FIRST}),C{FIRST}>0,COUNTIFS($A${FIRST}:$A${lv},A{FIRST},$C${FIRST}:$C${lv},"<"&C{FIRST},$C${FIRST}:$C${lv},">0")=0,'
                               f'COUNTIFS($A${FIRST}:$A${lv},A{FIRST},$C${FIRST}:$C${lv},">0")>1)', "D8EBFB", bold=True)

    # ---------------- Dashboard
    ws = sheet(wb, S_DASH, "Wedding budget dashboard", "Everything updates by itself. Nothing to type here.",
               [30, 16, 34, 4, 4, 4, 4, 4], tab="C62828")
    ws.freeze_panes = None
    kp = [("Total budget", "=IF(budget_cap=\"\",\"\",budget_cap)", USD, None),
          ("Your estimates (all categories)", "=tot_est", USD, None),
          ("Committed so far", "=tot_com", USD, None),
          ("Paid so far", "=tot_paid", USD, None),
          ("Still to pay", "=tot_com-tot_paid", USD, None),
          ("Budget left (budget − committed)", "=IF(budget_cap=\"\",\"\",budget_cap-tot_com)", USD, "red = over budget"),
          ("Estimate vs budget", "=IF(budget_cap=\"\",\"\",budget_cap-tot_est)", USD, "negative = estimates above budget"),
          ("Cost per guest (committed)", "=IF(OR(guests_n=\"\",guests_n=0),\"\",tot_com/guests_n)", USD, None),
          ("% of budget paid", "=IF(OR(budget_cap=\"\",budget_cap=0),\"\",tot_paid/budget_cap)", PCT, None),
          ("Payments overdue", f"=COUNTIF({col(S_EXP, 'H', N_EXP)},\"OVERDUE\")", NUM, None),
          ("Due in the next 30 days", f"=SUMIFS({col(S_EXP, 'E', N_EXP)},{col(S_EXP, 'H', N_EXP)},\"Due soon\")", USD, None),
          ("Days to the wedding", "=IF(w_date=\"\",\"\",w_date-today_)", NUM, None)]
    for i, (lbl, fml, f, note) in enumerate(kp):
        kpi(ws, 4 + i, lbl, fml, f, note=note)
    cf(ws, "B9", "AND(ISNUMBER(B9),B9<0)", C_BAD, bold=True)
    cf(ws, "B13", "AND(ISNUMBER(B13),B13>0)", C_BAD, bold=True)
    bar_chart(ws, "A18", "Estimate vs committed by category",
              Reference(wb[S_BUD], min_col=1, min_row=FIRST, max_row=FIRST + len(CATS) - 1),
              [Reference(wb[S_BUD], min_col=4, min_row=4, max_row=FIRST + len(CATS) - 1),
               Reference(wb[S_BUD], min_col=5, min_row=4, max_row=FIRST + len(CATS) - 1)], width=22, height=12)
    put(ws, "A44", "Paid vs still to pay", bold=True)
    put(ws, "A45", "Paid")
    put(ws, "B45", "=tot_paid", "calc", USD)
    put(ws, "A46", "Still to pay")
    put(ws, "B46", "=tot_com-tot_paid", "calc", USD)
    put(ws, "A47", "Not yet committed")
    put(ws, "B47", "=MAX(0,IF(budget_cap=\"\",0,budget_cap)-tot_com)", "calc", USD)
    pie_chart(ws, "C44", "Where the budget stands", Reference(ws, min_col=1, min_row=45, max_row=47),
              Reference(ws, min_col=2, min_row=45, max_row=47), width=13, height=8)
    for w in wb.worksheets:
        w.page_setup.orientation = "landscape" if w.title in (S_EXP, S_VEN, S_BUD) else "portrait"
        w.page_setup.paperSize = w.PAPERSIZE_LETTER
        w.page_setup.fitToWidth = 1
        w.page_setup.fitToHeight = 0
        w.sheet_properties.pageSetUpPr.fitToPage = True
    wb.move_sheet(S_DASH, offset=-(len(wb.sheetnames) - 2))
    instructions(wb, "Wedding Budget Planner",
                 "Set your total budget, plan each category, log every deposit and payment, compare vendor quotes and "
                 "see at a glance what's paid, what's due and how much is left.",
                 ["Settings: type your names, wedding date, total budget and guest count.",
                  "Budget: type your estimate per category (the Suggested $ column helps).",
                  "Vendor Quotes: compare quotes; the cheapest per category turns blue. Mark the one you choose.",
                  "Expenses & Payments: one row per deposit or bill, with a due date. Set Paid? = Yes when paid.",
                  "Dashboard: check it weekly: budget left, overdue payments, what's due in the next 30 days."],
                 ["Rename or add categories on the Settings sheet; they flow into every drop-down."],
                 [("Settings", "Names, date, total budget, guests, 20 editable categories with suggested %."),
                  ("Dashboard", "Budget left, paid, still to pay, overdue, next 30 days, cost per guest, 2 charts."),
                  ("Budget", "Suggested vs estimate vs committed vs paid per category; overspend in red."),
                  ("Expenses & Payments", "120 rows: deposits, installments, balances, due dates, overdue alerts."),
                  ("Vendor Quotes", "60 rows to compare vendors side by side, cheapest highlighted.")])
    # The template mentions religious advice in a generic note; replace for this general product.
    st = wb["Start Here"]
    for row in st.iter_rows():
        for c in row:
            if isinstance(c.value, str) and "rabbi" in c.value:
                c.value = "• Example figures and suggested percentages are rough guides only, not financial advice."
    wb.active = 0
    props(wb, "Wedding Budget Planner", "Wedding budget spreadsheet")
    wb.properties.keywords = "wedding budget, planner, spreadsheet, Excel, Google Sheets"
    return wb


if __name__ == "__main__":
    out = REPO / "etsy" / "listings" / "06-wedding-budget-planner" / "files"
    out.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(__file__).resolve().parent / "_cache"
    tmp.mkdir(exist_ok=True)
    for demo, name in [(False, "Wedding-Budget-Planner.xlsx"), (True, "Wedding-Budget-Planner-EXAMPLE.xlsx")]:
        build(demo).save(tmp / name)
        clean_xlsx(tmp / name, out / name)
        print(out / name)
