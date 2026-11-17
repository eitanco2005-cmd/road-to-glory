"""Event planner engine (Bar/Bat Mitzvah, Jewish Wedding): English, LTR, USD.

build(cfg, demo=False) -> Workbook. Every number on the Dashboard is a live formula.
Sheets: Start Here · Settings · Dashboard · Budget · Vendors · Payments · Guests · Seating · Checklist · <Honors> · Day-of
"""
import datetime as dt
from xl import *  # noqa: F401,F403

S_SET, S_DASH, S_BUD, S_VEN, S_PAY, S_GST, S_SEAT, S_TODO, S_DAY = (
    "Settings", "Dashboard", "Budget", "Vendors", "Payments", "Guests", "Seating", "Checklist", "Day-of Schedule")
N_CATS, N_VEN, N_PAY, N_GST, N_TAB, N_TODO, N_HON, N_DAY = 20, 60, 120, 300, 40, 80, 40, 40
RSVP = ["Attending", "Declined", "No reply yet", "Not invited yet"]


def build_settings(wb, cfg, demo):
    ws = sheet(wb, S_SET, f"{cfg['short']} settings",
               "Fill in once. Yellow cells are inputs. The lists on the right feed the drop-downs everywhere in the file: "
               "rename, delete or add items freely.",
               [34, 24, 3, 30, 22, 22, 18, 18, 22], tab="FFC000")
    d = cfg["demo"]
    rows = [
        ("Event name", d["name"] if demo else "", None, "event_name"),
        ("Event date", d["date"] if demo else None, DATE, "event_date"),
        ("Venue / location", d["venue"] if demo else "", None, "event_venue"),
        ("Total budget (cap)", d["cap"] if demo else None, USD, "budget_cap"),
        ("Catering cost per guest (incl. tax & tip)", d["pp"] if demo else None, USD, "cost_pp"),
        ("Guaranteed minimum guests (contract)", d["min"] if demo else None, NUM, "min_guests"),
    ]
    for i, (label, val, fmt, name) in enumerate(rows):
        r = 4 + i
        put(ws, f"A{r}", label, bold=True)
        put(ws, f"B{r}", val, "input", fmt)
        define(wb, name, f"{q(S_SET)}!$B${r}")
    put(ws, "A11", "Tip: not sure about the budget? Try the free calculator at " + SITE + cfg["tool_path"], size=9,
        color="6B7780", italic=True)
    ws.merge_cells("A11:B12")

    lists = [("D", "Budget categories", [c[0] for c in cfg["categories"]], N_CATS, "lst_cat"),
             ("E", "Guest sides", cfg["sides"], 10, "lst_side"),
             ("F", "Guest groups", cfg["groups"], 15, "lst_group"),
             ("G", "RSVP status", RSVP, 4, "lst_rsvp"),
             ("H", "Gift types", cfg["gift_types"], 10, "lst_gift"),
             ("I", "Meal / dietary", cfg["meals"], 10, "lst_meal")]
    for letter, title, items, n, name in lists:
        put(ws, f"{letter}3", title, "head")
        for i in range(n):
            c = ws[f"{letter}{4 + i}"]
            c.value = items[i] if i < len(items) else None
            style(c, "input")
        define(wb, name, f"{q(S_SET)}!${letter}$4:${letter}${3 + n}")
    put(ws, "D25", "Suggested split of the budget (edit on the Budget sheet)", size=9, color="6B7780", italic=True)
    ws.merge_cells("D25:I25")
    dv_number(ws, "B7:B9")
    return ws


def build_budget(wb, cfg, demo):
    ws = sheet(wb, S_BUD, "Budget",
               "Planned = what you want to spend. Committed = signed contracts on the Vendors sheet. Paid = payments marked Paid. "
               "Suggested % is a common rule of thumb; change it to suit you.",
               [32, 12, 15, 15, 15, 15, 15, 16], tab="2E7D32")
    headers(ws, 4, ["Category", "Suggested %", "Suggested $", "Planned", "Committed", "Paid", "Still to pay",
                    "Planned − committed"])
    pcts = [c[1] for c in cfg["categories"]]
    planned = cfg["demo"].get("planned", {})
    for i in range(N_CATS):
        r = FIRST + i
        put(ws, f"A{r}", f"=IF({q(S_SET)}!D{4 + i}=\"\",\"\",{q(S_SET)}!D{4 + i})", "calc", bold=True)
        put(ws, f"B{r}", pcts[i] if i < len(pcts) else None, "input", PCT)
        put(ws, f"C{r}", f"=IF(OR(A{r}=\"\",B{r}=\"\",budget_cap=\"\"),\"\",budget_cap*B{r})", "calc", USD)
        cat = cfg["categories"][i][0] if i < len(cfg["categories"]) else None
        put(ws, f"D{r}", planned.get(cat) if demo and cat else None, "input", USD)
        put(ws, f"E{r}", f"=IF(A{r}=\"\",\"\",SUMIFS({col(S_VEN, 'G', N_VEN)},{col(S_VEN, 'A', N_VEN)},A{r}))", "calc", USD)
        put(ws, f"F{r}", f"=IF(A{r}=\"\",\"\",SUMIFS({col(S_PAY, 'E', N_PAY)},{col(S_PAY, 'B', N_PAY)},A{r},"
                         f"{col(S_PAY, 'F', N_PAY)},\"Paid\"))", "calc", USD)
        put(ws, f"G{r}", f"=IF(A{r}=\"\",\"\",E{r}-F{r})", "calc", USD)
        put(ws, f"H{r}", f"=IF(OR(A{r}=\"\",D{r}=\"\"),\"\",D{r}-E{r})", "calc", USD)
    t = FIRST + N_CATS
    last = t - 1
    put(ws, f"A{t}", "Total", "total")
    for L in "BCDEFGH":
        put(ws, f"{L}{t}", f"=SUM({L}{FIRST}:{L}{last})", "total", PCT if L == "B" else USD)
    define(wb, "tot_planned", f"{q(S_BUD)}!$D${t}")
    define(wb, "tot_committed", f"{q(S_BUD)}!$E${t}")
    define(wb, "tot_paid", f"{q(S_BUD)}!$F${t}")
    cf(ws, f"H{FIRST}:H{last}", f"AND(ISNUMBER(H{FIRST}),H{FIRST}<0)", C_BAD)
    cf(ws, f"B{t}", f"ROUND(B{t},2)<>1", C_WARN)
    put(ws, f"A{t + 2}", "Suggested % should add up to 100% (the total turns orange if it doesn't). "
                         "Red in the last column = contracts above what you planned.", size=9, color="6B7780", italic=True)
    ws.merge_cells(f"A{t + 2}:H{t + 2}")
    return ws


def build_vendors(wb, cfg, demo):
    ws = sheet(wb, S_VEN, "Vendors",
               "One row per vendor. Enter the full contract total once it's signed; record each deposit and installment on the "
               "Payments sheet and the paid and balance columns update.",
               [26, 26, 20, 18, 26, 14, 15, 15, 15, 30], tab="1565C0")
    headers(ws, 4, ["Category", "Vendor", "Contact person", "Phone", "Email / website", "Status", "Contract total",
                    "Paid so far", "Balance", "Notes"])
    blank_rows(ws, FIRST, N_VEN, ["input"] * 7 + ["calc", "calc", "input"], {7: USD, 8: USD, 9: USD})
    for i in range(N_VEN):
        r = FIRST + i
        ws[f"H{r}"] = f"=IF(B{r}=\"\",\"\",SUMIFS({col(S_PAY, 'E', N_PAY)},{col(S_PAY, 'A', N_PAY)},B{r},{col(S_PAY, 'F', N_PAY)},\"Paid\"))"
        ws[f"I{r}"] = f"=IF(OR(B{r}=\"\",G{r}=\"\"),\"\",G{r}-H{r})"
    last = FIRST + N_VEN - 1
    dv_list(ws, "lst_cat", f"A{FIRST}:A{last}")
    dv_list(ws, '"Researching,Quote received,Booked,Not chosen"', f"F{FIRST}:F{last}")
    dv_number(ws, f"G{FIRST}:G{last}")
    cf(ws, f"F{FIRST}:F{last}", f'F{FIRST}="Booked"', C_OK)
    if demo:
        for i, row in enumerate(cfg["demo"]["vendors"]):
            for j, v in enumerate(row):
                ws.cell(row=FIRST + i, column=[1, 2, 3, 6, 7][j], value=v)
    return ws


def build_payments(wb, cfg, demo):
    ws = sheet(wb, S_PAY, "Payments",
               "Every deposit and installment. Pick the vendor, enter the due date and amount, and switch Status to Paid when it's "
               "done. Overdue rows turn red, rows due within 14 days turn orange.",
               [26, 24, 26, 18, 14, 12, 18, 16, 12], tab="1565C0")
    headers(ws, 4, ["Vendor", "Category", "What for", "Due date", "Amount", "Status", "Date paid", "Method", "Days left"])
    blank_rows(ws, FIRST, N_PAY, ["input", "calc", "input", "input", "input", "input", "input", "input", "calc"],
               {4: DATE, 5: USD, 7: DATE, 9: NUM})
    for i in range(N_PAY):
        r = FIRST + i
        ws[f"B{r}"] = f"=IF(A{r}=\"\",\"\",IFERROR(INDEX({col(S_VEN, 'A', N_VEN)},MATCH(A{r},{col(S_VEN, 'B', N_VEN)},0)),\"\"))"
        ws[f"I{r}"] = f"=IF(OR(D{r}=\"\",F{r}=\"Paid\"),\"\",D{r}-TODAY())"
    last = FIRST + N_PAY - 1
    dv_list(ws, f"{col(S_VEN, 'B', N_VEN)}", f"A{FIRST}:A{last}", prompt="Pick a vendor from the Vendors sheet")
    dv_list(ws, '"Due,Paid"', f"F{FIRST}:F{last}")
    dv_list(ws, '"Check,Credit card,Bank transfer,Zelle,Venmo,Cash,Other"', f"H{FIRST}:H{last}")
    cf(ws, f"A{FIRST}:I{last}", f'AND($D{FIRST}<>"",$F{FIRST}<>"Paid",$D{FIRST}<TODAY())', C_BAD)
    cf(ws, f"A{FIRST}:I{last}", f'AND($D{FIRST}<>"",$F{FIRST}<>"Paid",$D{FIRST}-TODAY()<=14)', C_WARN)
    cf(ws, f"F{FIRST}:F{last}", f'F{FIRST}="Paid"', C_OK)
    if demo:
        for i, (v, what, due, amt, st) in enumerate(cfg["demo"]["payments"]):
            r = FIRST + i
            ws[f"A{r}"], ws[f"C{r}"], ws[f"D{r}"], ws[f"E{r}"], ws[f"F{r}"] = v, what, due, amt, st
            if st == "Paid":
                ws[f"G{r}"] = due
                ws[f"H{r}"] = "Credit card" if i % 2 else "Check"
    return ws


def build_guests(wb, cfg, demo):
    ws = sheet(wb, S_GST, "Guest list, RSVPs & gifts",
               "One row per household/invitation. Invited = how many people the invitation is for; Attending = how many said yes. "
               "Log gifts as they arrive and tick off thank-you notes.",
               [28, 18, 20, 28, 10, 15, 11, 8, 18, 8, 12, 14, 12, 24], tab="6A1B9A")
    headers(ws, 4, ["Name / household", "Side", "Group", "Address or email", "Invited", "RSVP", "Attending", "Kids",
                    "Meal / dietary", "Table", "Gift amount", "Gift type", "Thank-you sent", "Notes"])
    blank_rows(ws, FIRST, N_GST, ["input"] * 14, {5: NUM, 7: NUM, 8: NUM, 11: USD})
    last = FIRST + N_GST - 1
    dv_list(ws, "lst_side", f"B{FIRST}:B{last}")
    dv_list(ws, "lst_group", f"C{FIRST}:C{last}")
    dv_list(ws, "lst_rsvp", f"F{FIRST}:F{last}", strict=True)
    dv_list(ws, "lst_meal", f"I{FIRST}:I{last}")
    dv_list(ws, "lst_gift", f"L{FIRST}:L{last}")
    dv_list(ws, '"Yes,No"', f"M{FIRST}:M{last}")
    dv_number(ws, f"E{FIRST}:H{last}")
    cf(ws, f"F{FIRST}:F{last}", f'F{FIRST}="Attending"', C_OK)
    cf(ws, f"F{FIRST}:F{last}", f'F{FIRST}="Declined"', "E0E0E0")
    cf(ws, f"M{FIRST}:M{last}", f'AND(K{FIRST}<>"",M{FIRST}<>"Yes")', C_WARN)
    cf(ws, f"G{FIRST}:G{last}", f'AND(ISNUMBER(G{FIRST}),ISNUMBER(E{FIRST}),G{FIRST}>E{FIRST})', C_BAD)
    if demo:
        for i, g in enumerate(cfg["demo"]["guests"]):
            for j, v in enumerate(g):
                if v is not None:
                    ws.cell(row=FIRST + i, column=j + 1, value=v)
    return ws


def build_seating(wb, cfg, demo):
    ws = sheet(wb, S_SEAT, "Seating helper",
               "List your tables and seats. Type the table number in the Guests sheet (Table column) and this sheet counts who is "
               "seated where. Red = over capacity.",
               [10, 26, 10, 12, 10, 16], tab="6A1B9A")
    headers(ws, 4, ["Table", "Name / theme", "Seats", "Seated", "Free", "Status"])
    blank_rows(ws, FIRST, N_TAB, ["input", "input", "input", "calc", "calc", "calc"], {3: NUM, 4: NUM, 5: NUM})
    for i in range(N_TAB):
        r = FIRST + i
        ws[f"D{r}"] = f"=IF(A{r}=\"\",\"\",SUMIFS({col(S_GST, 'G', N_GST)},{col(S_GST, 'J', N_GST)},A{r}))"
        ws[f"E{r}"] = f"=IF(OR(A{r}=\"\",C{r}=\"\"),\"\",C{r}-D{r})"
        ws[f"F{r}"] = f"=IF(E{r}=\"\",\"\",IF(E{r}<0,\"Over capacity\",IF(E{r}=0,\"Full\",\"Has room\")))"
    last = FIRST + N_TAB - 1
    cf(ws, f"A{FIRST}:F{last}", f'AND(ISNUMBER($E{FIRST}),$E{FIRST}<0)', C_BAD)
    cf(ws, f"F{FIRST}:F{last}", f'F{FIRST}="Full"', C_OK)
    t = last + 1
    put(ws, f"A{t}", "Total", "total")
    put(ws, f"B{t}", "", "total")
    for L in "CDE":
        put(ws, f"{L}{t}", f"=SUM({L}{FIRST}:{L}{last})", "total", NUM)
    put(ws, f"F{t}", f"=SUMIFS({col(S_GST, 'G', N_GST)},{col(S_GST, 'J', N_GST)},\"\")", "total", NUM)
    put(ws, f"F{t + 1}", "↑ attending guests without a table", size=9, color="6B7780", italic=True)
    if demo:
        for i, (name, seats) in enumerate(cfg["demo"]["tables"]):
            ws[f"A{FIRST + i}"], ws[f"B{FIRST + i}"], ws[f"C{FIRST + i}"] = i + 1, name, seats
    return ws


def build_checklist(wb, cfg, demo):
    ws = sheet(wb, S_TODO, "Planning checklist",
               "Due dates are counted back from the event date on the Settings sheet. Mark Done = Yes when finished. "
               "Add your own tasks in the empty rows.",
               [20, 10, 58, 18, 14, 9, 14], tab="EF6C00")
    headers(ws, 4, ["Phase", "Weeks before", "Task", "Due date", "Who", "Done", "Status"])
    blank_rows(ws, FIRST, N_TODO, ["input", "input", "input", "calc", "input", "input", "calc"], {2: NUM, 4: DATE})
    for i in range(N_TODO):
        r = FIRST + i
        if i < len(cfg["tasks"]):
            ph, wk, task = cfg["tasks"][i]
            ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"] = ph, wk, task
        ws[f"D{r}"] = f"=IF(OR(C{r}=\"\",B{r}=\"\",event_date=\"\"),\"\",event_date-7*B{r})"
        ws[f"G{r}"] = (f"=IF(C{r}=\"\",\"\",IF(F{r}=\"Yes\",\"Done\",IF(D{r}=\"\",\"\",IF(D{r}<TODAY(),\"Overdue\","
                       f"IF(D{r}-TODAY()<=14,\"Due soon\",\"Upcoming\")))))")
    last = FIRST + N_TODO - 1
    dv_list(ws, '"Yes,No"', f"F{FIRST}:F{last}")
    cf(ws, f"A{FIRST}:G{last}", f'$G{FIRST}="Done"', C_OK)
    cf(ws, f"A{FIRST}:G{last}", f'$G{FIRST}="Overdue"', C_BAD)
    cf(ws, f"A{FIRST}:G{last}", f'$G{FIRST}="Due soon"', C_WARN)
    if demo:
        today = cfg["demo"]["today"]
        for i in range(len(cfg["tasks"])):
            r = FIRST + i
            due = cfg["demo"]["date"] - dt.timedelta(weeks=cfg["tasks"][i][1])
            if due < today:
                ws[f"F{r}"] = "Yes"
    return ws


def build_honors(wb, cfg, demo):
    h = cfg["honors"]
    ws = sheet(wb, h["sheet"], h["title"], h["subtitle"], [32, 44, 26, 26, 11, 11, 26], tab="AD1457")
    headers(ws, 4, ["Honor / role", "What it involves", "Person", "Hebrew name (if needed)", "Asked", "Confirmed", "Notes"])
    blank_rows(ws, FIRST, N_HON, ["input"] * 7)
    for i, (role, what) in enumerate(h["rows"]):
        ws[f"A{FIRST + i}"], ws[f"B{FIRST + i}"] = role, what
    last = FIRST + N_HON - 1
    dv_list(ws, '"Yes,No"', f"E{FIRST}:F{last}")
    cf(ws, f"A{FIRST}:G{last}", f'$F{FIRST}="Yes"', C_OK)
    if demo:
        for i, (person, ok) in enumerate(cfg["demo"]["honors"]):
            ws[f"C{FIRST + i}"], ws[f"E{FIRST + i}"], ws[f"F{FIRST + i}"] = person, "Yes", ok
    t = last + 2
    put(ws, f"A{t}", "Filled", bold=True)
    put(ws, f"B{t}", f"=COUNTIFS(F{FIRST}:F{last},\"Yes\")&\" of \"&COUNTA(A{FIRST}:A{last})&\" confirmed\"", "calc")
    define(wb, "honors_confirmed", f"{q(h['sheet'])}!$B${t}")
    return ws


def build_dayof(wb, cfg, demo):
    ws = sheet(wb, S_DAY, "Day-of schedule",
               "A run-of-show to share with your planner, DJ/band, photographer and family. Edit the times and add rows.",
               [12, 46, 24, 40], tab="00838F")
    headers(ws, 4, ["Time", "What happens", "Who's responsible", "Notes"])
    blank_rows(ws, FIRST, N_DAY, ["input"] * 4, {1: "h:mm AM/PM"})
    for i, (t, what, who) in enumerate(cfg["dayof"]):
        r = FIRST + i
        hh, mm = t
        ws[f"A{r}"] = dt.time(hh, mm)
        ws[f"B{r}"], ws[f"C{r}"] = what, who
    return ws


def build_dashboard(wb, cfg, demo):
    ws = sheet(wb, S_DASH, f"{cfg['short']} dashboard",
               "Everything updates by itself from the other sheets. Nothing to type here.",
               [34, 22, 4, 34, 18, 4, 16, 12, 12], tab="C9A227")
    g, p = N_GST, N_PAY
    kpi(ws, 4, "Event", "=IF(event_name=\"\",\"(set on Settings)\",event_name)")
    kpi(ws, 5, "Date", "=IF(event_date=\"\",\"\",event_date)", "mmm d, yyyy")
    kpi(ws, 6, "Days to go", "=IF(event_date=\"\",\"\",MAX(0,event_date-TODAY()))", NUM)
    put(ws, "A8", "Money", bold=True, size=13, color=C_TITLE)
    kpi(ws, 9, "Budget cap", "=IF(budget_cap=\"\",0,budget_cap)", USD)
    kpi(ws, 10, "Planned (Budget sheet)", "=tot_planned", USD)
    kpi(ws, 11, "Committed (signed contracts)", "=tot_committed", USD)
    kpi(ws, 12, "Paid so far", "=tot_paid", USD)
    kpi(ws, 13, "Still to pay", "=tot_committed-tot_paid", USD)
    kpi(ws, 14, "Left in budget after contracts", "=IF(budget_cap=\"\",\"\",budget_cap-tot_committed)", USD)
    kpi(ws, 15, "Overdue payments", f"=SUMIFS({col(S_PAY, 'E', p)},{col(S_PAY, 'F', p)},\"<>Paid\",{col(S_PAY, 'D', p)},\"<\"&TODAY())", USD)
    kpi(ws, 16, "Due in the next 30 days", f"=SUMIFS({col(S_PAY, 'E', p)},{col(S_PAY, 'F', p)},\"<>Paid\",{col(S_PAY, 'D', p)},\">=\"&TODAY(),{col(S_PAY, 'D', p)},\"<=\"&(TODAY()+30))", USD)
    put(ws, "D8", "Guests", bold=True, size=13, color=C_TITLE)
    kpi(ws, 9, "Invitations (households)", f"=COUNTA({col(S_GST, 'A', g)})", NUM, "D", "E")
    kpi(ws, 10, "People invited", f"=SUM({col(S_GST, 'E', g)})", NUM, "D", "E")
    kpi(ws, 11, "Attending", f"=SUMIFS({col(S_GST, 'G', g)},{col(S_GST, 'F', g)},\"Attending\")", NUM, "D", "E")
    kpi(ws, 12, "…of them kids", f"=SUMIFS({col(S_GST, 'H', g)},{col(S_GST, 'F', g)},\"Attending\")", NUM, "D", "E")
    kpi(ws, 13, "Still waiting to hear from (people)", f"=SUMIFS({col(S_GST, 'E', g)},{col(S_GST, 'F', g)},\"No reply yet\")", NUM, "D", "E")
    kpi(ws, 14, "Catering estimate (attending × cost)", "=IF(cost_pp=\"\",\"\",MAX(E11,IF(min_guests=\"\",0,min_guests))*cost_pp)", USD, "D", "E")
    kpi(ws, 15, "Gifts received", f"=SUM({col(S_GST, 'K', g)})", USD, "D", "E")
    kpi(ws, 16, "Thank-you notes to write", f"=COUNTIFS({col(S_GST, 'K', g)},\"<>\",{col(S_GST, 'M', g)},\"<>Yes\")", NUM, "D", "E")
    put(ws, "A18", "Planning", bold=True, size=13, color=C_TITLE)
    t = N_TODO
    kpi(ws, 19, "Checklist done", f"=IFERROR(COUNTIFS({col(S_TODO, 'G', t)},\"Done\")/COUNTIFS({col(S_TODO, 'C', t)},\"<>\"),0)", PCT)
    kpi(ws, 20, "Overdue tasks", f"=COUNTIFS({col(S_TODO, 'G', t)},\"Overdue\")", NUM)
    kpi(ws, 21, "Tasks due in the next 2 weeks", f"=COUNTIFS({col(S_TODO, 'G', t)},\"Due soon\")", NUM)
    kpi(ws, 19, cfg["honors"]["kpi"], "=honors_confirmed", None, "D", "E")
    kpi(ws, 20, "Vendors booked", f"=COUNTIFS({col(S_VEN, 'F', N_VEN)},\"Booked\")", NUM, "D", "E")
    kpi(ws, 21, "Attending guests without a table", f"=SUMIFS({col(S_GST, 'G', g)},{col(S_GST, 'F', g)},\"Attending\",{col(S_GST, 'J', g)},\"\")", NUM, "D", "E")
    cf(ws, "B15", "AND(ISNUMBER(B15),B15>0)", C_BAD, bold=True)
    cf(ws, "B14", "AND(ISNUMBER(B14),B14<0)", C_BAD, bold=True)
    cf(ws, "B20", "AND(ISNUMBER(B20),B20>0)", C_BAD, bold=True)

    # chart helper tables (G:I)
    put(ws, "G4", "RSVP", "head")
    put(ws, "H4", "People", "head")
    for i, (lab, f) in enumerate([
        ("Attending", f"=SUMIFS({col(S_GST, 'G', g)},{col(S_GST, 'F', g)},\"Attending\")"),
        ("Declined", f"=SUMIFS({col(S_GST, 'E', g)},{col(S_GST, 'F', g)},\"Declined\")"),
        ("No reply yet", f"=SUMIFS({col(S_GST, 'E', g)},{col(S_GST, 'F', g)},\"No reply yet\")"),
        ("Not invited yet", f"=SUMIFS({col(S_GST, 'E', g)},{col(S_GST, 'F', g)},\"Not invited yet\")"),
    ]):
        put(ws, f"G{5 + i}", lab, "calc")
        put(ws, f"H{5 + i}", f, "calc", NUM)
    put(ws, "G11", "Money", "head")
    put(ws, "H11", "Amount", "head")
    for i, (lab, f) in enumerate([("Paid", "=tot_paid"), ("Still to pay", "=tot_committed-tot_paid"),
                                  ("Not yet committed", "=MAX(0,IF(budget_cap=\"\",0,budget_cap)-tot_committed)")]):
        put(ws, f"G{12 + i}", lab, "calc")
        put(ws, f"H{12 + i}", f, "calc", USD)

    bar_chart(ws, "A24", "Budget by category: planned vs committed",
              Reference(wb[S_BUD], min_col=1, min_row=FIRST, max_row=FIRST + len(cfg["categories"]) - 1),
              [Reference(wb[S_BUD], min_col=4, max_col=5, min_row=4, max_row=FIRST + len(cfg["categories"]) - 1)],
              width=24, height=11)
    pie_chart(ws, "A47", "Where the budget stands", Reference(ws, min_col=7, min_row=12, max_row=14),
              Reference(ws, min_col=8, min_row=12, max_row=14), width=12, height=8)
    pie_chart(ws, "D47", "Guests by RSVP", Reference(ws, min_col=7, min_row=5, max_row=8),
              Reference(ws, min_col=8, min_row=5, max_row=8), width=13, height=8)
    return ws


def build(cfg, demo=False):
    wb = new_book()
    build_settings(wb, cfg, demo)
    dash = wb.create_sheet("_dash")  # placeholder to fix sheet order
    build_budget(wb, cfg, demo)
    build_vendors(wb, cfg, demo)
    build_payments(wb, cfg, demo)
    build_guests(wb, cfg, demo)
    build_seating(wb, cfg, demo)
    build_checklist(wb, cfg, demo)
    build_honors(wb, cfg, demo)
    build_dayof(wb, cfg, demo)
    wb.remove(dash)
    d = build_dashboard(wb, cfg, demo)
    wb.move_sheet(d, offset=-(len(wb.sheetnames) - 2))
    instructions(wb, cfg["title"], cfg["intro"], cfg["steps"], cfg["notes"], cfg["sheets"])
    wb.active = 0
    props(wb, cfg["title"], cfg["short"] + " planner")
    return wb
