"""Jewish Holiday Hosting Planner: one file for a year of hosting (Rosh Hashanah to Shavuot, plus Shabbat)."""
import datetime as dt
from xl import *  # noqa: F401,F403

D = dt.date
S_SET, S_DASH, S_HOL, S_GST, S_MENU, S_SHOP, S_TRAD, S_MM = (
    "Settings", "Dashboard", "Holidays", "Guests", "Menus", "Shopping", "Traditions", "Mishloach Manot")
N_HOL, N_GST, N_MENU, N_SHOP, N_TRAD, N_MM = 10, 120, 150, 200, 120, 60
GUEST_COL0 = 4  # column D = first holiday column on Guests

HOLIDAYS = [  # name, example date (5787/5788 examples), example budget
    ("Rosh Hashanah dinner", D(2027, 10, 1), 450), ("Rosh Hashanah lunch", D(2027, 10, 2), 250),
    ("Yom Kippur break-fast", D(2027, 10, 11), 300), ("Sukkot meal in the sukkah", D(2027, 10, 16), 300),
    ("Hanukkah party", D(2026, 12, 6), 250), ("Purim seudah", D(2027, 3, 23), 200),
    ("Shavuot dairy meal", D(2027, 6, 11), 200), ("Shabbat dinner", None, 150), ("Other gathering", None, None)]

TRADITIONS = [
    ("Rosh Hashanah dinner", "Round challah (often with raisins)", "For the cycle of the year"),
    ("Rosh Hashanah dinner", "Apples & honey", "For a sweet new year"),
    ("Rosh Hashanah dinner", "Simanim (symbolic foods): pomegranate, dates, leek, beet, gourd, fish head…", "Customs vary by family"),
    ("Rosh Hashanah dinner", "New fruit for the second night (shehecheyanu)", "Often pomegranate or another fruit not yet eaten this season"),
    ("Rosh Hashanah dinner", "Candles and kiddush", ""),
    ("Rosh Hashanah lunch", "Plan around services / shofar times", "Check your synagogue's schedule"),
    ("Rosh Hashanah lunch", "Tashlich after lunch (first afternoon, or second if the first is Shabbat)", ""),
    ("Yom Kippur break-fast", "Pre-fast meal (seudah mafseket) the afternoon before", "Light, not too salty, lots of water"),
    ("Yom Kippur break-fast", "Set the break-fast table before going to synagogue", "Many families serve a dairy brunch: bagels, lox, kugel, eggs"),
    ("Yom Kippur break-fast", "Drinks ready: water, juice, coffee", ""),
    ("Sukkot meal in the sukkah", "Build and decorate the sukkah", "Often started right after Yom Kippur"),
    ("Sukkot meal in the sukkah", "Schach (covering) in place", ""),
    ("Sukkot meal in the sukkah", "Order lulav & etrog", "Order early from your synagogue or a Judaica shop"),
    ("Sukkot meal in the sukkah", "Warm layers, lights and bug spray for the sukkah", ""),
    ("Hanukkah party", "Menorah (hanukkiah) for each household that lights", ""),
    ("Hanukkah party", "Candles: 44 for all eight nights per menorah (incl. the shamash)", "2+3+4+…+9 = 44"),
    ("Hanukkah party", "Latkes (potatoes, onions, eggs, oil) + applesauce & sour cream", ""),
    ("Hanukkah party", "Sufganiyot (jelly donuts)", ""),
    ("Hanukkah party", "Dreidels and gelt", ""),
    ("Hanukkah party", "Gifts / gift exchange plan", ""),
    ("Purim seudah", "Hear the Megillah (evening and morning)", "Check your synagogue's times"),
    ("Purim seudah", "Mishloach manot: at least two ready-to-eat foods to at least one friend", "Use the Mishloach Manot sheet"),
    ("Purim seudah", "Matanot la'evyonim: gifts to at least two people in need", "Many give through their synagogue"),
    ("Purim seudah", "Hamantaschen", ""), ("Purim seudah", "Costumes", ""),
    ("Shavuot dairy meal", "Dairy dishes: cheesecake, blintzes, lasagna", ""),
    ("Shavuot dairy meal", "Flowers and greenery", ""),
    ("Shabbat dinner", "Candles lit 18 minutes before sunset (check local times)", ""),
    ("Shabbat dinner", "Two challot and a cover", ""), ("Shabbat dinner", "Kiddush cup and wine / grape juice", ""),
    ("Shabbat dinner", "Hand-washing cup", ""), ("Shabbat dinner", "Food kept warm without cooking (if observing): hot plate / blech", "")]

MENUS = [("Rosh Hashanah dinner", "Starter", "Gefilte fish or salmon"), ("Rosh Hashanah dinner", "Soup", "Chicken soup with matzo balls"),
         ("Rosh Hashanah dinner", "Main", "Brisket with carrots (tzimmes)"), ("Rosh Hashanah dinner", "Side", "Honey-roasted carrots"),
         ("Rosh Hashanah dinner", "Dessert", "Honey cake"), ("Yom Kippur break-fast", "Main", "Bagels, lox & cream cheese"),
         ("Yom Kippur break-fast", "Main", "Noodle kugel"), ("Yom Kippur break-fast", "Side", "Egg salad & tuna salad"),
         ("Sukkot meal in the sukkah", "Main", "Stuffed peppers"), ("Sukkot meal in the sukkah", "Dessert", "Apple crumble"),
         ("Hanukkah party", "Main", "Latkes"), ("Hanukkah party", "Dessert", "Sufganiyot"),
         ("Purim seudah", "Main", "Roast chicken"), ("Purim seudah", "Dessert", "Hamantaschen"),
         ("Shavuot dairy meal", "Main", "Cheese blintzes"), ("Shavuot dairy meal", "Dessert", "Cheesecake")]


def hol_name_ref(i):
    return f"{q(S_HOL)}!$A${FIRST + i}"


def build_settings(wb, demo):
    ws = sheet(wb, S_SET, "Settings", "Your household and the drop-down lists. Holidays themselves are listed on the Holidays sheet.",
               [36, 26, 3, 22, 22], tab="FFC000")
    rows = [("Household name", "The Shapiros" if demo else "", None, "household"),
            ("Year (e.g. 5787–5788 / 2026–27)", "2026–27" if demo else "", None, "year_label"),
            ("Overall hosting budget for the year", 2400 if demo else None, USD, "year_budget")]
    for i, (label, val, fmt, name) in enumerate(rows):
        put(ws, f"A{4 + i}", label, bold=True)
        put(ws, f"B{4 + i}", val, "input", fmt)
        define(wb, name, f"{q(S_SET)}!$B${4 + i}")
    lists = [("D", "Courses", ["Starter", "Soup", "Main", "Side", "Salad", "Dessert", "Drinks", "Kids"], 12, "lst_course"),
             ("E", "Shopping categories", ["Meat & fish", "Dairy", "Produce", "Bakery", "Pantry", "Drinks & wine",
                                           "Paper goods", "Ritual items", "Other"], 12, "lst_scat")]
    for letter, title, items, n, name in lists:
        put(ws, f"{letter}3", title, "head")
        for i in range(n):
            put(ws, f"{letter}{4 + i}", items[i] if i < len(items) else None, "input")
        define(wb, name, f"{q(S_SET)}!${letter}$4:${letter}${3 + n}")
    put(ws, "A9", "Holiday dates move every year on the Gregorian calendar. Check a Jewish calendar (e.g. your "
                  "synagogue's, Chabad.org or Hebcal) and type them on the Holidays sheet.", size=9, color="6B7780", italic=True)
    ws.merge_cells("A9:B11")
    return ws


def build_holidays(wb, demo):
    ws = sheet(wb, S_HOL, "Holidays you're hosting",
               "Rename or add meals in column A; the Guests sheet uses these as its columns. Guests, shopping and dishes are "
               "counted automatically.",
               [30, 18, 10, 13, 10, 14, 13, 9, 13, 14], tab="1565C0")
    headers(ws, 4, ["Holiday / meal", "Date", "Hosting?", "Budget", "Guests", "Shopping est.", "Budget left", "Dishes",
                    "Traditions done", "Days to go"])
    blank_rows(ws, FIRST, N_HOL, ["input", "input", "input", "input", "calc", "calc", "calc", "calc", "calc", "calc"],
               {2: DATE, 4: USD, 5: NUM, 6: USD, 7: USD, 8: NUM, 9: PCT, 10: NUM})
    for i in range(N_HOL):
        r = FIRST + i
        if i < len(HOLIDAYS):
            name, date, budget = HOLIDAYS[i]
            ws[f"A{r}"] = name
            if demo:
                ws[f"B{r}"], ws[f"D{r}"] = date, budget
                ws[f"C{r}"] = "Yes" if i not in (6, 8) else "No"
        gcol = get_column_letter(GUEST_COL0 + i)
        ws[f"E{r}"] = f"=IF(A{r}=\"\",\"\",SUMIFS({col(S_GST, 'B', N_GST)},{col(S_GST, gcol, N_GST)},\"Yes\"))"
        ws[f"F{r}"] = f"=IF(A{r}=\"\",\"\",SUMIFS({col(S_SHOP, 'G', N_SHOP)},{col(S_SHOP, 'A', N_SHOP)},A{r}))"
        ws[f"G{r}"] = f"=IF(OR(A{r}=\"\",D{r}=\"\"),\"\",D{r}-F{r})"
        ws[f"H{r}"] = f"=IF(A{r}=\"\",\"\",COUNTIFS({col(S_MENU, 'A', N_MENU)},A{r},{col(S_MENU, 'C', N_MENU)},\"<>\"))"
        ws[f"I{r}"] = (f"=IF(COUNTIFS({col(S_TRAD, 'A', N_TRAD)},A{r})=0,\"\",COUNTIFS({col(S_TRAD, 'A', N_TRAD)},A{r},"
                       f"{col(S_TRAD, 'D', N_TRAD)},\"Yes\")/COUNTIFS({col(S_TRAD, 'A', N_TRAD)},A{r}))")
        ws[f"J{r}"] = f"=IF(OR(B{r}=\"\",C{r}=\"No\"),\"\",IF(B{r}<TODAY(),\"Done\",B{r}-TODAY()))"
    last = FIRST + N_HOL - 1
    t = last + 1
    put(ws, f"A{t}", "Total", "total")
    for L, fmt in (("D", USD), ("E", NUM), ("F", USD), ("G", USD), ("H", NUM)):
        put(ws, f"{L}{t}", f"=SUM({L}{FIRST}:{L}{last})", "total", fmt)
    for L in "BCIJ":
        put(ws, f"{L}{t}", "", "total")
    define(wb, "hol_names", f"{q(S_HOL)}!$A${FIRST}:$A${last}")
    define(wb, "hol_shop_total", f"{q(S_HOL)}!$F${t}")
    dv_list(ws, '"Yes,No,Maybe"', f"C{FIRST}:C{last}")
    cf(ws, f"G{FIRST}:G{last}", f"AND(ISNUMBER(G{FIRST}),G{FIRST}<0)", C_BAD)
    cf(ws, f"A{FIRST}:J{last}", f'$C{FIRST}="No"', "EEEEEE")
    return ws


def build_guests(wb, demo):
    widths = [26, 9, 26] + [11] * N_HOL + [26]
    ws = sheet(wb, S_GST, "Guests (who's coming to what)",
               "One row per household. Type Yes under each holiday they're coming to. Column titles come from the Holidays sheet.",
               widths, tab="6A1B9A")
    names = ["Name / household", "People", "Dietary needs / allergies"] + [""] * N_HOL + ["Notes / bringing"]
    headers(ws, 4, names, height=60)
    for i in range(N_HOL):
        c = ws.cell(row=4, column=GUEST_COL0 + i)
        c.value = f"=IF({hol_name_ref(i)}=\"\",\"(spare)\",{hol_name_ref(i)})"
    kinds = ["input", "input", "input"] + ["input"] * N_HOL + ["input"]
    blank_rows(ws, FIRST, N_GST, kinds, {2: NUM})
    last = FIRST + N_GST - 1
    first_h, last_h = get_column_letter(GUEST_COL0), get_column_letter(GUEST_COL0 + N_HOL - 1)
    dv_list(ws, '"Yes,Maybe,No"', f"{first_h}{FIRST}:{last_h}{last}")
    dv_number(ws, f"B{FIRST}:B{last}")
    cf(ws, f"{first_h}{FIRST}:{last_h}{last}", f'{first_h}{FIRST}="Yes"', C_OK)
    cf(ws, f"{first_h}{FIRST}:{last_h}{last}", f'{first_h}{FIRST}="Maybe"', C_WARN)
    if demo:
        rows = [("Us (the Shapiros)", 4, "", "YYYYYYY.Y"), ("Grandma Ruth", 1, "Low sugar", "YY.YY.Y.."),
                ("The Kleins", 4, "Nut allergy", "Y..Y.Y..."), ("Uncle Mike & Dana", 2, "", "Y.Y.Y...."),
                ("The Bermans", 5, "Vegetarian (2)", "...YY.Y.."), ("Rabbi & Mrs. Stern", 2, "Strictly kosher", ".Y......."),
                ("Josh & Talia", 2, "", "..Y.YY.Y."), ("Neighbors: the Garcias", 3, "", "....Y...."),
                ("Leah (college friend)", 1, "Vegan", "Y....Y..."), ("The Novaks", 4, "", "....Y.Y..")]
        for i, (n, ppl, diet, pat) in enumerate(rows):
            r = FIRST + i
            ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"] = n, ppl, diet or None
            for j, ch in enumerate(pat):
                if ch == "Y":
                    ws.cell(row=r, column=GUEST_COL0 + j, value="Yes")
    return ws


def build_menus(wb, demo):
    ws = sheet(wb, S_MENU, "Menus", "Plan dishes per holiday. Servings = that holiday's guest count.",
               [28, 14, 34, 20, 11, 18, 10, 9, 28], tab="EF6C00")
    headers(ws, 4, ["Holiday / meal", "Course", "Dish", "Made / brought by", "Days ahead", "Prep date", "Servings", "Done",
                    "Recipe / notes"])
    blank_rows(ws, FIRST, N_MENU, ["input", "input", "input", "input", "input", "calc", "calc", "input", "input"],
               {5: NUM, 6: DATE, 7: NUM})
    for i in range(N_MENU):
        r = FIRST + i
        if i < len(MENUS):
            ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"] = MENUS[i]
            if demo:
                ws[f"D{r}"] = "Grandma Ruth" if "cake" in MENUS[i][2] else "Us"
                ws[f"E{r}"] = 2 if MENUS[i][1] in ("Main", "Soup") else 1
        hd = f"IFERROR(INDEX({q(S_HOL)}!$B${FIRST}:$B${FIRST + N_HOL - 1},MATCH(A{r},hol_names,0)),\"\")"
        ws[f"F{r}"] = f"=IF(OR(C{r}=\"\",E{r}=\"\"),\"\",IF({hd}=\"\",\"\",{hd}-E{r}))"
        ws[f"G{r}"] = f"=IF(C{r}=\"\",\"\",IFERROR(INDEX({q(S_HOL)}!$E${FIRST}:$E${FIRST + N_HOL - 1},MATCH(A{r},hol_names,0)),\"\"))"
    last = FIRST + N_MENU - 1
    dv_list(ws, "hol_names", f"A{FIRST}:A{last}")
    dv_list(ws, "lst_course", f"B{FIRST}:B{last}")
    dv_list(ws, '"Yes,No"', f"H{FIRST}:H{last}")
    cf(ws, f"A{FIRST}:I{last}", f'$H{FIRST}="Yes"', C_OK)
    return ws


def build_shopping(wb, demo):
    ws = sheet(wb, S_SHOP, "Shopping", "Per holiday. Estimated cost = quantity × price. Mark Bought as you shop.",
               [28, 32, 16, 9, 12, 12, 13, 9], tab="2E7D32")
    headers(ws, 4, ["Holiday / meal", "Item", "Category", "Qty", "Unit", "Price / unit", "Est. cost", "Bought"])
    blank_rows(ws, FIRST, N_SHOP, ["input"] * 6 + ["calc", "input"], {4: NUM1, 6: USD2, 7: USD2})
    for i in range(N_SHOP):
        r = FIRST + i
        ws[f"G{r}"] = f"=IF(OR(D{r}=\"\",F{r}=\"\"),\"\",D{r}*F{r})"
    if demo:
        items = [("Rosh Hashanah dinner", "Brisket (raw)", "Meat & fish", 7, "lb", 11), ("Rosh Hashanah dinner", "Round challot", "Bakery", 3, "each", 7),
                 ("Rosh Hashanah dinner", "Honey", "Pantry", 1, "jar", 8), ("Rosh Hashanah dinner", "Apples", "Produce", 8, "each", .8),
                 ("Rosh Hashanah dinner", "Pomegranates", "Produce", 3, "each", 3), ("Rosh Hashanah dinner", "Wine", "Drinks & wine", 4, "bottle", 14),
                 ("Yom Kippur break-fast", "Bagels", "Bakery", 3, "dozen", 14), ("Yom Kippur break-fast", "Lox", "Meat & fish", 2, "lb", 30),
                 ("Yom Kippur break-fast", "Cream cheese", "Dairy", 3, "tub", 5), ("Hanukkah party", "Potatoes", "Produce", 10, "lb", 1),
                 ("Hanukkah party", "Frying oil", "Pantry", 2, "bottle", 9), ("Hanukkah party", "Sufganiyot", "Bakery", 3, "dozen", 18),
                 ("Hanukkah party", "Hanukkah candles", "Ritual items", 2, "box of 44", 5), ("Hanukkah party", "Chocolate gelt", "Pantry", 4, "bag", 4),
                 ("Purim seudah", "Mishloach manot baskets", "Other", 12, "each", 6), ("Sukkot meal in the sukkah", "String lights", "Other", 2, "set", 15)]
        for i, row in enumerate(items):
            for j, v in enumerate(row):
                ws.cell(row=FIRST + i, column=j + 1, value=v)
            if i < 6:
                ws[f"H{FIRST + i}"] = "Yes"
    last = FIRST + N_SHOP - 1
    dv_list(ws, "hol_names", f"A{FIRST}:A{last}")
    dv_list(ws, "lst_scat", f"C{FIRST}:C{last}")
    dv_list(ws, '"Yes,No"', f"H{FIRST}:H{last}")
    cf(ws, f"A{FIRST}:H{last}", f'$H{FIRST}="Yes"', C_OK)
    return ws


def build_traditions(wb, demo):
    ws = sheet(wb, S_TRAD, "Traditions & to-do checklist",
               "What each holiday needs, so nothing is forgotten. Customs differ between communities: edit freely.",
               [28, 62, 44, 9], tab="AD1457")
    headers(ws, 4, ["Holiday / meal", "Item", "Notes", "Done"])
    blank_rows(ws, FIRST, N_TRAD, ["input"] * 4)
    for i, (h, it, note) in enumerate(TRADITIONS):
        r = FIRST + i
        ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"] = h, it, note or None
        if demo and h.startswith("Hanukkah") and i % 2 == 0:
            ws[f"D{r}"] = "Yes"
    last = FIRST + N_TRAD - 1
    dv_list(ws, "hol_names", f"A{FIRST}:A{last}")
    dv_list(ws, '"Yes,No"', f"D{FIRST}:D{last}")
    cf(ws, f"A{FIRST}:D{last}", f'$D{FIRST}="Yes"', C_OK)
    return ws


def build_mm(wb, demo):
    ws = sheet(wb, S_MM, "Purim: mishloach manot & matanot la'evyonim",
               "Who gets a basket, what's in it, who delivers it and whether it's done. Gifts to the needy at the bottom.",
               [28, 30, 30, 12, 18, 9], tab="AD1457")
    headers(ws, 4, ["Recipient", "Address / notes", "What's inside", "Cost", "Delivered by", "Done"])
    blank_rows(ws, FIRST, N_MM, ["input", "input", "input", "input", "input", "input"], {4: USD2})
    last = FIRST + N_MM - 1
    dv_list(ws, '"Yes,No"', f"F{FIRST}:F{last}")
    cf(ws, f"A{FIRST}:F{last}", f'$F{FIRST}="Yes"', C_OK)
    if demo:
        for i, n in enumerate(["The Kleins", "Rabbi & Mrs. Stern", "Grandma Ruth", "Kids' teachers (3)", "The Garcias"]):
            r = FIRST + i
            ws[f"A{r}"], ws[f"C{r}"], ws[f"D{r}"], ws[f"E{r}"] = n, "Hamantaschen + juice box", 6, "Kids"
            ws[f"F{r}"] = "Yes" if i < 2 else None
    t = last + 2
    put(ws, f"A{t}", "Matanot la'evyonim (gifts to the needy)", bold=True, size=13, color=C_TITLE)
    put(ws, f"A{t + 1}", "Given through", bold=True)
    put(ws, f"B{t + 1}", "Synagogue fund" if demo else None, "input")
    put(ws, f"A{t + 2}", "Amount", bold=True)
    put(ws, f"B{t + 2}", 54 if demo else None, "input", USD)
    put(ws, f"A{t + 3}", "Done", bold=True)
    put(ws, f"B{t + 3}", None, "input")
    dv_list(ws, '"Yes,No"', f"B{t + 3}")
    put(ws, f"A{t + 5}", "Baskets: total / delivered", bold=True)
    put(ws, f"B{t + 5}", f"=COUNTA(A{FIRST}:A{last})&\" / \"&COUNTIFS(F{FIRST}:F{last},\"Yes\")", "calc")
    define(wb, "mm_status", f"{q(S_MM)}!$B${t + 5}")
    return ws


def build_dashboard(wb, demo):
    ws = sheet(wb, S_DASH, "Holiday hosting dashboard", "Updates by itself from the other sheets.",
               [34, 16, 4, 34, 16], tab="C9A227")
    h0, h1 = FIRST, FIRST + N_HOL - 1
    H = q(S_HOL)
    kpi(ws, 4, "Household", "=IF(household=\"\",\"(set on Settings)\",household)")
    kpi(ws, 5, "Year", "=year_label")
    kpi(ws, 6, "Meals you're hosting", f"=COUNTIFS({H}!$C${h0}:$C${h1},\"Yes\")", NUM)
    kpi(ws, 7, "Next hosted meal",
        f"=IFERROR(INDEX({H}!$A${h0}:$A${h1},MATCH(SMALL({H}!$J${h0}:$J${h1},1),{H}!$J${h0}:$J${h1},0)),\"\")")
    kpi(ws, 8, "…days to go", f"=IFERROR(SMALL({H}!$J${h0}:$J${h1},1),\"\")", NUM)
    kpi(ws, 4, "Total hosting budget", f"=IF(year_budget=\"\",SUM({H}!$D${h0}:$D${h1}),year_budget)", USD, "D", "E")
    kpi(ws, 5, "Shopping planned", "=hol_shop_total", USD, "D", "E")
    kpi(ws, 6, "Bought so far", f"=SUMIFS({col(S_SHOP, 'G', N_SHOP)},{col(S_SHOP, 'H', N_SHOP)},\"Yes\")", USD, "D", "E")
    kpi(ws, 7, "Budget left", "=E4-E5", USD, "D", "E")
    kpi(ws, 8, "Mishloach manot (total / delivered)", "=mm_status", None, "D", "E")
    cf(ws, "E7", "AND(ISNUMBER(E7),E7<0)", C_BAD, bold=True)
    put(ws, "A10", "Per holiday", bold=True, size=13, color=C_TITLE)
    heads = ["Holiday / meal", "Guests", "", "Budget", "Shopping est."]
    for i, h in enumerate(heads):
        if h:
            style(ws.cell(row=11, column=i + 1, value=h), "head")
    for i in range(N_HOL):
        r = 12 + i
        src = FIRST + i
        put(ws, f"A{r}", f"=IF({H}!A{src}=\"\",\"\",{H}!A{src})", "calc")
        put(ws, f"B{r}", f"=IF({H}!A{src}=\"\",\"\",{H}!E{src})", "calc", NUM)
        put(ws, f"D{r}", f"=IF({H}!A{src}=\"\",\"\",N({H}!D{src}))", "calc", USD)
        put(ws, f"E{r}", f"=IF({H}!A{src}=\"\",\"\",{H}!F{src})", "calc", USD)
    n = len(HOLIDAYS)
    bar_chart(ws, "A24", "Guests per holiday", Reference(ws, min_col=1, min_row=12, max_row=11 + n),
              [Reference(ws, min_col=2, min_row=11, max_row=11 + n)], width=20, height=9, money=False)
    bar_chart(ws, "A43", "Budget vs shopping estimate", Reference(ws, min_col=1, min_row=12, max_row=11 + n),
              [Reference(ws, min_col=4, max_col=5, min_row=11, max_row=11 + n)], width=20, height=10)
    return ws


def build(demo=False):
    wb = new_book()
    build_settings(wb, demo)
    build_holidays(wb, demo)
    build_guests(wb, demo)
    build_menus(wb, demo)
    build_shopping(wb, demo)
    build_traditions(wb, demo)
    build_mm(wb, demo)
    d = build_dashboard(wb, demo)
    wb.move_sheet(d, offset=-(len(wb.sheetnames) - 2))
    instructions(
        wb, "Jewish Holiday Hosting Planner",
        "One file for a year of hosting: Rosh Hashanah, Yom Kippur break-fast, Sukkot, Hanukkah, Purim, Shavuot and "
        "Shabbat. Guest lists per holiday, menus, shopping and budgets, a traditions checklist and a mishloach manot tracker.",
        ["Holidays: type this year's dates, whether you're hosting, and a budget per meal. Rename or add meals in column A.",
         "Guests: one row per household; type Yes under each holiday they're coming to.",
         "Menus: plan dishes and who brings them. Prep dates and servings fill in automatically.",
         "Shopping: list what to buy per holiday with quantities and prices; mark Bought as you go.",
         "Traditions: tick off the holiday essentials (simanim, sukkah, candles, megillah…).",
         "Dashboard: next meal, guests per holiday, budget vs shopping, mishloach manot progress."],
        ["Holiday dates change every year. Take them from a Jewish calendar (your synagogue, Chabad.org or Hebcal).",
         "Hanukkah needs 44 candles per menorah for all eight nights, counting the shamash (2+3+…+9).",
         "The example file uses illustrative dates and prices only."],
        [("Settings", "Household, year, overall budget, course and shopping lists."),
         ("Dashboard", "Next hosted meal, budget vs spending, guests per holiday, charts."),
         ("Holidays", "Dates, hosting yes/no, budget, guests, shopping, dishes and traditions progress per meal."),
         ("Guests", "Households × holidays grid with dietary needs."),
         ("Menus", "Dishes, cooks, make-ahead days, prep dates and servings."),
         ("Shopping", "Items per holiday with quantity × price and Bought tick."),
         ("Traditions", "32 holiday essentials from round challah to the Shabbat blech."),
         ("Mishloach Manot", "Purim baskets and gifts to the needy.")])
    wb.active = 0
    props(wb, "Jewish Holiday Hosting Planner", "Jewish holiday hosting spreadsheet")
    return wb
