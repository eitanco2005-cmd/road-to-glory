"""Passover Seder Planner: guests, menu, shopping list scaled by head count, prep timeline, haggadah assignments."""
import datetime as dt
from xl import *  # noqa: F401,F403

D = dt.date
S_SET, S_DASH, S_GST, S_SHOP, S_MENU, S_HAG, S_TIME, S_PLATE = (
    "Settings", "Dashboard", "Guests", "Shopping List", "Menu", "Haggadah Parts", "Prep Timeline", "Seder Plate")
N_GST, N_SHOP, N_MENU, N_HAG, N_TIME = 80, 90, 50, 50, 60

# item, category, per adult per seder, per child per seder, per seder plate/table, unit, pack size, pack label, example price/pack
# Ritual quantities follow the guidance published by Chabad.org (see Start Here); meal quantities are common catering rules of thumb.
SHOP = [
    ("Matzah: shmurah, handmade (for the mitzvah)", "Matzah", 2, 1.5, 3, "matzot", 7, "1 lb (~7 matzot)", 32),
    ("Matzah: machine (for the meal & extra)", "Matzah", 2, 1, 0, "sheets", 10, "1 lb box (~10 sheets)", 6),
    ("Wine (four cups)", "Wine & juice", 0.75, 0, 0, "bottles", 1, "750 ml bottle", 14),
    ("Grape juice (four cups)", "Wine & juice", 0.1, 0.5, 0, "bottles", 1, "64 oz bottle (~8 cups)", 6),
    ("Elijah's cup wine", "Wine & juice", 0, 0, 0.2, "bottles", 1, "750 ml bottle", 0),
    ("Maror: romaine lettuce", "Seder plate", 0.15, 0.1, 0.5, "heads", 1, "head", 2.5),
    ("Maror: fresh horseradish root", "Seder plate", 0.05, 0, 0.25, "lb", 1, "lb", 6),
    ("Karpas: parsley / celery / potato", "Seder plate", 0.05, 0.05, 0.5, "bunches", 1, "bunch", 2),
    ("Charoset: apples", "Seder plate", 0.25, 0.25, 0, "apples", 1, "apple", 0.8),
    ("Charoset: walnuts", "Seder plate", 0.03, 0.03, 0, "lb", 1, "lb", 9),
    ("Charoset: sweet red wine", "Seder plate", 0, 0, 0.1, "bottles", 1, "bottle", 0),
    ("Eggs (seder plate + egg in salt water)", "Seder plate", 1, 1, 1, "eggs", 12, "dozen", 4.5),
    ("Shank bone / roasted chicken neck (zeroa)", "Seder plate", 0, 0, 1, "pieces", 1, "piece", 3),
    ("Salt (for salt water)", "Seder plate", 0, 0, 0.05, "boxes", 1, "box", 2),
    ("Gefilte fish", "Meal", 1, 0.5, 0, "pieces", 8, "jar (~8 pieces)", 9),
    ("Chicken soup: whole chicken / parts", "Meal", 0.2, 0.15, 0, "lb", 1, "lb", 3.5),
    ("Matzo meal (matzo balls ~2 per person)", "Meal", 0.12, 0.12, 0, "cans", 1, "can (~16 balls)", 4.5),
    ("Brisket (raw weight)", "Meal", 0.5, 0.25, 0, "lb", 1, "lb", 11),
    ("Roast chicken (raw, bone-in)", "Meal", 0.4, 0.25, 0, "lb", 1, "lb", 3.5),
    ("Potatoes (kugel / roasted)", "Meal", 0.4, 0.3, 0, "lb", 5, "5 lb bag", 5),
    ("Green vegetables / salad", "Meal", 0.3, 0.2, 0, "lb", 1, "lb", 3),
    ("Macaroons / Passover dessert", "Dessert", 0.15, 0.15, 0, "cans", 1, "can", 5),
    ("Fresh fruit", "Dessert", 0.3, 0.3, 0, "lb", 1, "lb", 2.5),
    ("Haggadot (one per guest)", "Table", 0, 0, 0, "copies", 1, "copy", 0),
    ("Candles (yom tov)", "Table", 0, 0, 2, "candles", 12, "pack of 12", 4),
    ("Napkins, plates, cups (if disposable)", "Table", 1, 1, 0, "place settings", 20, "pack of 20", 8),
]
MENU = [("Seder plate & ritual", "Charoset", "", 3), ("Seder plate & ritual", "Hard-boiled eggs & salt water", "", 1),
        ("Starter", "Gefilte fish with horseradish", "", 2), ("Soup", "Chicken soup with matzo balls", "", 3),
        ("Main", "Brisket", "", 2), ("Main", "Roast chicken (or a vegetarian main)", "", 1),
        ("Side", "Potato kugel", "", 1), ("Side", "Roasted vegetables / green salad", "", 0),
        ("Dessert", "Flourless chocolate cake", "", 2), ("Dessert", "Macaroons & fruit", "", 0)]
HAG = [("1. Kadesh", "Kiddush over the first cup"), ("2. Urchatz", "Wash hands (no blessing)"),
       ("3. Karpas", "Vegetable dipped in salt water"), ("4. Yachatz", "Break the middle matzah; hide the afikoman"),
       ("5. Maggid: Ha Lachma Anya", "\"This is the bread of affliction\""),
       ("5. Maggid: Ma Nishtana (Four Questions)", "Traditionally the youngest child"),
       ("5. Maggid: Avadim Hayinu", "\"We were slaves\""), ("5. Maggid: The Four Children", "Wise, wicked, simple, unable to ask"),
       ("5. Maggid: The story", "Arami oved avi / the Exodus narrative"),
       ("5. Maggid: Ten Plagues", "Spill a drop of wine for each plague"), ("5. Maggid: Dayenu", "Song"),
       ("5. Maggid: Pesach, Matzah, Maror", "Rabban Gamliel's three things"), ("5. Maggid: Second cup", "Blessing and drink"),
       ("6. Rachtzah", "Wash hands with a blessing"), ("7–8. Motzi Matzah", "Blessings over the matzah"),
       ("9. Maror", "Bitter herbs dipped in charoset"), ("10. Korech", "Hillel sandwich"),
       ("11. Shulchan Orech", "The festive meal"), ("12. Tzafun", "Find and eat the afikoman (prize for the finder?)"),
       ("13. Barech", "Grace after meals; third cup"), ("Elijah's cup / opening the door", ""),
       ("Miriam's cup (if your family uses one)", ""), ("14. Hallel", "Psalms of praise; fourth cup"),
       ("15. Nirtzah", "\"Next year in Jerusalem!\""), ("Songs: Echad Mi Yodea", ""), ("Songs: Chad Gadya", "")]
TIMELINE = [(42, "Decide on one or two seders; invite guests (and ask about dietary needs)"),
            (35, "Order shmurah matzah and specialty items early (they sell out)"),
            (30, "Plan the menu; assign dishes guests will bring"),
            (28, "Start cleaning for Passover, room by room"),
            (21, "Buy haggadot (same edition for everyone makes page-calling easier)"),
            (21, "Plan haggadah parts and kids' activities (plague props, afikoman prize)"),
            (14, "Big shopping trip for non-perishables, wine and grape juice"),
            (10, "Cook and freeze make-ahead dishes (soup, matzo balls, kugel)"),
            (7, "Confirm final head count for each night"),
            (5, "Arrange to sell chametz (through your rabbi or online form)"),
            (4, "Kasher / switch kitchen to Passover dishes"),
            (3, "Shop for fresh produce, fish and meat"),
            (2, "Cook brisket (it slices better the day after); make charoset"),
            (1, "Bedikat chametz: search for chametz in the evening (dates vary, e.g. when the seder is Saturday night)"),
            (1, "Set the table, prepare the seder plate(s), salt water, pillows for reclining"),
            (0, "Burn / dispose of chametz by the morning deadline (check your local times)"),
            (0, "Light candles; enjoy the seder!")]


def build_settings(wb, demo):
    ws = sheet(wb, S_SET, "Seder settings",
               "Fill in once. The head counts below come from the Guests sheet and drive every quantity on the Shopping List.",
               [44, 20, 4, 40], tab="FFC000")
    rows = [("Family / host name", "The Goldbergs" if demo else "", None, "host"),
            ("Date of the first seder (evening)", D(2027, 4, 21) if demo else None, DATE, "seder_date"),
            ("Number of seders you're hosting (1 or 2)", 2 if demo else 1, NUM, "n_seders"),
            ("Seder plates on the table (usually 1 per ~10–12 people)", 2 if demo else 1, NUM, "plates"),
            ("Plan for 'Maybe' guests too? (Yes / No)", "Yes", None, "count_maybe"),
            ("Budget for food & supplies", 1100 if demo else None, USD, "seder_budget")]
    for i, (label, val, fmt, name) in enumerate(rows):
        r = 4 + i
        put(ws, f"A{r}", label, bold=True)
        put(ws, f"B{r}", val, "input", fmt)
        define(wb, name, f"{q(S_SET)}!$B${r}")
    dv_list(ws, '"1,2"', "B6", strict=True)
    dv_list(ws, '"Yes,No"', "B8", strict=True)
    put(ws, "A11", "Head count (from the Guests sheet)", bold=True, size=13, color=C_TITLE)
    g = N_GST
    yes = '"Yes"'

    def seats(col_letter, night_filter):
        # adults/kids attending a given night: RSVP Yes (+ Maybe if chosen)
        base = (f"SUMIFS({col(S_GST, col_letter, g)},{col(S_GST, 'D', g)},\"{{n}}\",{col(S_GST, 'E', g)},{{s}})")
        parts = []
        for n in night_filter:
            parts.append(base.format(n=n, s=yes))
            parts.append(f"IF(count_maybe=\"Yes\",{base.format(n=n, s='\"Maybe\"')},0)")
        return "=" + "+".join(parts)

    labels = [("Adults: 1st seder", seats("B", ["1st seder", "Both"]), "adults1"),
              ("Kids: 1st seder", seats("C", ["1st seder", "Both"]), "kids1"),
              ("Adults: 2nd seder", f"=IF(n_seders=2,{seats('B', ['2nd seder', 'Both'])[1:]},0)", "adults2"),
              ("Kids: 2nd seder", f"=IF(n_seders=2,{seats('C', ['2nd seder', 'Both'])[1:]},0)", "kids2")]
    for i, (label, f, name) in enumerate(labels):
        r = 12 + i
        put(ws, f"A{r}", label, bold=True)
        put(ws, f"B{r}", f, "calc", NUM)
        define(wb, name, f"{q(S_SET)}!$B${r}")
    put(ws, "A16", "Adult seats across all seders", bold=True)
    put(ws, "B16", "=adults1+adults2", "calc", NUM)
    define(wb, "adult_seats", f"{q(S_SET)}!$B$16")
    put(ws, "A17", "Child seats across all seders", bold=True)
    put(ws, "B17", "=kids1+kids2", "calc", NUM)
    define(wb, "kid_seats", f"{q(S_SET)}!$B$17")
    put(ws, "A18", "Seder plates across all seders", bold=True)
    put(ws, "B18", "=IF(plates=\"\",1,plates)*IF(n_seders=2,2,1)", "calc", NUM)
    define(wb, "plate_seders", f"{q(S_SET)}!$B$18")
    put(ws, "A19", "Biggest table (most people at one seder)", bold=True)
    put(ws, "B19", "=MAX(adults1+kids1,adults2+kids2)", "calc", NUM)
    define(wb, "max_table", f"{q(S_SET)}!$B$19")
    put(ws, "D4", "Night options for the Guests sheet", "head")
    for i, v in enumerate(["1st seder", "2nd seder", "Both"]):
        put(ws, f"D{5 + i}", v, "calc")
    define(wb, "lst_night", f"{q(S_SET)}!$D$5:$D$7")
    put(ws, "D9", "Tip: in Israel there is one seder; outside Israel most communities hold two.", size=9, color="6B7780", italic=True)
    ws.merge_cells("D9:D11")
    return ws


def build_guests(wb, demo):
    ws = sheet(wb, S_GST, "Guests",
               "One row per household. Choose which night they come and their RSVP. 'Maybe' is counted if Settings says so.",
               [28, 9, 9, 13, 11, 30, 30, 26], tab="6A1B9A")
    headers(ws, 4, ["Name / household", "Adults", "Kids", "Which night", "RSVP", "Dietary needs / allergies",
                    "Bringing", "Haggadah part / notes"])
    blank_rows(ws, FIRST, N_GST, ["input"] * 8, {2: NUM, 3: NUM})
    last = FIRST + N_GST - 1
    dv_list(ws, "lst_night", f"D{FIRST}:D{last}", strict=True)
    dv_list(ws, '"Yes,Maybe,No,Not asked yet"', f"E{FIRST}:E{last}", strict=True)
    dv_number(ws, f"B{FIRST}:C{last}")
    cf(ws, f"E{FIRST}:E{last}", f'E{FIRST}="Yes"', C_OK)
    cf(ws, f"E{FIRST}:E{last}", f'E{FIRST}="Maybe"', C_WARN)
    if demo:
        rows = [("Us (the Goldbergs)", 2, 3, "Both", "Yes", "", "", "Leader"),
                ("Grandma Ruth & Grandpa Joe", 2, 0, "Both", "Yes", "Low salt", "Charoset", "Dayenu"),
                ("The Katz family", 2, 2, "1st seder", "Yes", "Nut allergy (child)", "Flourless cake", "Four Children"),
                ("Aunt Debbie", 1, 0, "1st seder", "Yes", "Vegetarian", "Salad", "Ten Plagues"),
                ("Sam & Leah Rosen", 2, 1, "2nd seder", "Yes", "", "Wine", ""),
                ("Maya (college friend)", 1, 0, "1st seder", "Maybe", "Gluten-free", "", ""),
                ("The Patels (neighbors, first seder!)", 2, 2, "2nd seder", "Yes", "Vegetarian", "", "Ma Nishtana (kids)"),
                ("Uncle Mike", 1, 0, "Both", "Maybe", "", "Gefilte fish", "")]
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                if v != "":
                    ws.cell(row=FIRST + i, column=j + 1, value=v)
    return ws


def build_shopping(wb, demo):
    ws = sheet(wb, S_SHOP, "Shopping list (scales with your guest count)",
               "Quantities = per adult × adult seats + per child × child seats + per seder plate × plates, over all seders. "
               "Edit the yellow rates, pack sizes and prices to suit your family and your store. Type a number in "
               "'Override' to replace the calculation.",
               [40, 13, 9, 9, 9, 11, 12, 10, 18, 9, 9, 11, 11, 10], tab="2E7D32")
    headers(ws, 4, ["Item", "Category", "Per adult", "Per child", "Per plate", "Unit", "Needed", "Override", "Pack size",
                    "Units / pack", "On hand", "Packs to buy", "Price / pack", "Bought"])
    put(ws, "A3", "Rates are per person per seder. Example prices are placeholders; edit to your store's.", size=9,
        color="6B7780", italic=True)
    blank_rows(ws, FIRST, N_SHOP, ["input", "input", "input", "input", "input", "input", "calc", "input", "input", "input",
                                   "input", "calc", "input", "input"],
               {3: "0.00", 4: "0.00", 5: "0.00", 7: NUM1, 8: NUM1, 10: NUM1, 11: NUM1, 12: NUM, 13: USD2})
    for i in range(N_SHOP):
        r = FIRST + i
        if i < len(SHOP):
            it, cat, pa, pc, pp, unit, size, label, price = SHOP[i]
            ws[f"A{r}"], ws[f"B{r}"], ws[f"C{r}"], ws[f"D{r}"], ws[f"E{r}"] = it, cat, pa, pc, pp
            ws[f"F{r}"], ws[f"I{r}"], ws[f"J{r}"], ws[f"M{r}"] = unit, label, size, price
            if it.startswith("Haggadot"):
                ws[f"H{r}"] = "=max_table"
                style(ws[f"H{r}"], "calc", NUM1)
        ws[f"G{r}"] = (f"=IF(A{r}=\"\",\"\",IF(H{r}<>\"\",H{r},N(C{r})*adult_seats+N(D{r})*kid_seats+N(E{r})*plate_seders))")
        ws[f"L{r}"] = f"=IF(OR(A{r}=\"\",G{r}=\"\"),\"\",ROUNDUP(MAX(0,G{r}-N(K{r}))/IF(N(J{r})=0,1,J{r}),0))"
    last = FIRST + N_SHOP - 1
    t = last + 1
    put(ws, f"A{t}", "Estimated total", "total")
    ws.column_dimensions["O"].width = 12
    put(ws, "O4", "Cost", "head")
    for i in range(N_SHOP):
        r = FIRST + i
        put(ws, f"O{r}", f"=IF(OR(L{r}=\"\",M{r}=\"\"),0,L{r}*M{r})", "calc", USD2)
    put(ws, f"O{t}", f"=SUM(O{FIRST}:O{last})", "total", USD)
    put(ws, f"N{t}", "", "total")
    define(wb, "shop_total", f"{q(S_SHOP)}!$O${t}")
    define(wb, "shop_left", f"{q(S_SHOP)}!$O${t + 1}")
    put(ws, f"N{t + 1}", "Still to buy:", bold=True, align="right")
    put(ws, f"O{t + 1}", f"=SUMIFS(O{FIRST}:O{last},N{FIRST}:N{last},\"<>Yes\")", "calc", USD)
    dv_list(ws, '"Matzah,Wine & juice,Seder plate,Meal,Dessert,Drinks,Table,Other"', f"B{FIRST}:B{last}")
    dv_list(ws, '"Yes,No"', f"N{FIRST}:N{last}")
    cf(ws, f"A{FIRST}:O{last}", f'$N{FIRST}="Yes"', C_OK)
    ws.freeze_panes = "B5"
    return ws


def build_menu(wb, demo):
    ws = sheet(wb, S_MENU, "Menu & cooking plan",
               "List each dish, who makes it and how many days ahead. The prep date and the servings (biggest table) "
               "fill in automatically.",
               [22, 34, 22, 12, 18, 10, 12, 30], tab="EF6C00")
    headers(ws, 4, ["Course", "Dish", "Made / brought by", "Days ahead", "Prep date", "Servings", "Done", "Recipe / notes"])
    blank_rows(ws, FIRST, N_MENU, ["input", "input", "input", "input", "calc", "calc", "input", "input"], {4: NUM, 5: DATE, 6: NUM})
    for i in range(N_MENU):
        r = FIRST + i
        if i < len(MENU):
            c, d, by, days = MENU[i]
            ws[f"A{r}"], ws[f"B{r}"], ws[f"D{r}"] = c, d, days
            if demo:
                ws[f"C{r}"] = ["Us", "Us", "Uncle Mike", "Us", "Us", "Us", "Us", "Aunt Debbie", "Katz family", "Us"][i]
        ws[f"E{r}"] = f"=IF(OR(B{r}=\"\",D{r}=\"\",seder_date=\"\"),\"\",seder_date-D{r})"
        ws[f"F{r}"] = f"=IF(B{r}=\"\",\"\",max_table)"
    last = FIRST + N_MENU - 1
    dv_list(ws, '"Seder plate & ritual,Starter,Soup,Main,Side,Dessert,Drinks,Kids"', f"A{FIRST}:A{last}")
    dv_list(ws, '"Yes,No"', f"G{FIRST}:G{last}")
    cf(ws, f"A{FIRST}:H{last}", f'$G{FIRST}="Yes"', C_OK)
    return ws


def build_haggadah(wb, demo):
    ws = sheet(wb, S_HAG, "Haggadah parts",
               "Share the reading around the table. Assign each part for each night; add songs, discussion questions or "
               "your family's additions in the empty rows.",
               [40, 40, 24, 24, 26], tab="AD1457")
    headers(ws, 4, ["Part of the seder", "What happens", "1st seder: who", "2nd seder: who", "Notes / page"])
    blank_rows(ws, FIRST, N_HAG, ["input"] * 5)
    for i, (part, what) in enumerate(HAG):
        ws[f"A{FIRST + i}"], ws[f"B{FIRST + i}"] = part, what
    if demo:
        who = {0: "Dad", 5: "Ella (youngest)", 7: "Katz kids", 9: "Aunt Debbie", 10: "Grandma Ruth", 18: "Afikoman hunt: all kids"}
        for k, v in who.items():
            ws[f"C{FIRST + k}"] = v
        ws[f"D{FIRST + 5}"] = "Patel kids"
    t = FIRST + N_HAG + 1
    put(ws, f"A{t}", "Parts assigned (1st seder)", bold=True)
    put(ws, f"B{t}", f"=COUNTIFS(C{FIRST}:C{t - 2},\"<>\")&\" of \"&COUNTA(A{FIRST}:A{t - 2})", "calc")
    define(wb, "hag_assigned", f"{q(S_HAG)}!$B${t}")
    return ws


def build_timeline(wb, demo):
    ws = sheet(wb, S_TIME, "Prep timeline",
               "Dates count back from the first seder. Customs and local times vary (e.g. for selling and burning chametz). "
               "Check with your rabbi or community calendar.",
               [12, 64, 18, 14, 9, 14], tab="00838F")
    headers(ws, 4, ["Days before", "Task", "Date", "Who", "Done", "Status"])
    blank_rows(ws, FIRST, N_TIME, ["input", "input", "calc", "input", "input", "calc"], {1: NUM, 3: DATE})
    for i in range(N_TIME):
        r = FIRST + i
        if i < len(TIMELINE):
            ws[f"A{r}"], ws[f"B{r}"] = TIMELINE[i]
            if demo and i < 4:
                ws[f"E{r}"] = "Yes"
        ws[f"C{r}"] = f"=IF(OR(B{r}=\"\",A{r}=\"\",seder_date=\"\"),\"\",seder_date-A{r})"
        ws[f"F{r}"] = (f"=IF(B{r}=\"\",\"\",IF(E{r}=\"Yes\",\"Done\",IF(C{r}=\"\",\"\",IF(C{r}<TODAY(),\"Overdue\","
                       f"IF(C{r}-TODAY()<=7,\"This week\",\"Upcoming\")))))")
    last = FIRST + N_TIME - 1
    dv_list(ws, '"Yes,No"', f"E{FIRST}:E{last}")
    cf(ws, f"A{FIRST}:F{last}", f'$F{FIRST}="Done"', C_OK)
    cf(ws, f"A{FIRST}:F{last}", f'$F{FIRST}="Overdue"', C_BAD)
    cf(ws, f"A{FIRST}:F{last}", f'$F{FIRST}="This week"', C_WARN)
    return ws


def build_plate(wb, demo):
    ws = sheet(wb, S_PLATE, "Seder plate & table checklist",
               "Tick each item off as you set the table. Arrangements differ by tradition (e.g. Ashkenazi / Sephardi customs).",
               [34, 60, 10], tab="C9A227")
    headers(ws, 4, ["Item", "Meaning", "Ready"])
    items = [("Zeroa (shank bone / roasted neck)", "The Passover offering; vegetarians often use a roasted beet"),
             ("Beitzah (roasted / hard-boiled egg)", "The festival offering; mourning and renewal"),
             ("Maror (bitter herbs)", "The bitterness of slavery"),
             ("Chazeret (second bitter herb, often romaine)", "Used for Korech in many traditions"),
             ("Charoset", "Mortar the Israelites used to build"),
             ("Karpas (vegetable)", "Spring; dipped in salt water"),
             ("Salt water", "Tears"), ("Three matzot under a cover", "Yachatz: the middle one is broken"),
             ("Kiddush cups / wine glasses", "Four cups"), ("Elijah's cup", "Filled before opening the door"),
             ("Miriam's cup (optional)", "Water; a newer custom in many homes"),
             ("Pillows for reclining", "A sign of freedom"), ("Haggadot for everyone", "Same edition makes it easy"),
             ("Afikoman bag & prize", "For the children who find it"), ("Hand-washing cup & towel", "Urchatz & Rachtzah"),
             ("Candles & candlesticks", "Yom tov candles")]
    for i, (a, b) in enumerate(items):
        put(ws, f"A{FIRST + i}", a, "input", bold=True)
        put(ws, f"B{FIRST + i}", b, "input")
        put(ws, f"C{FIRST + i}", "Yes" if demo and i < 6 else None, "input", align="center")
    last = FIRST + len(items) + 9
    blank_rows(ws, FIRST + len(items), 10, ["input"] * 3)
    dv_list(ws, '"Yes,No"', f"C{FIRST}:C{last}")
    cf(ws, f"A{FIRST}:C{last}", f'$C{FIRST}="Yes"', C_OK)
    return ws


def build_dashboard(wb, demo):
    ws = sheet(wb, S_DASH, "Seder dashboard", "Updates by itself. Nothing to type here.",
               [36, 20, 4, 34, 16, 4, 16, 12], tab="C9A227")
    kpi(ws, 4, "Host", "=IF(host=\"\",\"(set on Settings)\",host)")
    kpi(ws, 5, "First seder", "=IF(seder_date=\"\",\"\",seder_date)", "mmm d, yyyy")
    kpi(ws, 6, "Days to go", "=IF(seder_date=\"\",\"\",MAX(0,seder_date-TODAY()))", NUM)
    put(ws, "A8", "People", bold=True, size=13, color=C_TITLE)
    kpi(ws, 9, "1st seder: adults", "=adults1", NUM)
    kpi(ws, 10, "1st seder: kids", "=kids1", NUM)
    kpi(ws, 11, "2nd seder: adults", "=adults2", NUM)
    kpi(ws, 12, "2nd seder: kids", "=kids2", NUM)
    kpi(ws, 13, "Chairs needed (biggest table)", "=max_table", NUM)
    g = N_GST
    kpi(ws, 14, "Households still to answer", f"=COUNTIFS({col(S_GST, 'E', g)},\"Not asked yet\")+COUNTIFS({col(S_GST, 'E', g)},\"Maybe\")", NUM)
    kpi(ws, 15, "Guests with dietary needs", f"=COUNTIFS({col(S_GST, 'F', g)},\"<>\",{col(S_GST, 'E', g)},\"<>No\")", NUM)
    put(ws, "D8", "Shopping & prep", bold=True, size=13, color=C_TITLE)
    kpi(ws, 9, "Estimated shopping cost", "=shop_total", USD, "D", "E")
    kpi(ws, 10, "Still to buy", "=shop_left", USD, "D", "E")
    kpi(ws, 11, "Budget left", "=IF(seder_budget=\"\",\"\",seder_budget-shop_total)", USD, "D", "E")
    kpi(ws, 12, "Shmurah matzot needed", f"=IFERROR(INDEX({col(S_SHOP, 'G', N_SHOP)},1),\"\")", NUM, "D", "E")
    kpi(ws, 13, "Bottles of wine", f"=IFERROR(INDEX({col(S_SHOP, 'L', N_SHOP)},3),\"\")", NUM, "D", "E")
    kpi(ws, 14, "Prep tasks overdue", f"=COUNTIFS({col(S_TIME, 'F', N_TIME)},\"Overdue\")", NUM, "D", "E")
    kpi(ws, 15, "Haggadah parts assigned (night 1)", "=hag_assigned", None, "D", "E")
    cf(ws, "E11", "AND(ISNUMBER(E11),E11<0)", C_BAD, bold=True)
    cf(ws, "E14", "AND(ISNUMBER(E14),E14>0)", C_BAD, bold=True)
    # chart tables
    put(ws, "G4", "Category", "head")
    put(ws, "H4", "Cost", "head")
    for i, c in enumerate(["Matzah", "Wine & juice", "Seder plate", "Meal", "Dessert", "Table"]):
        put(ws, f"G{5 + i}", c, "calc")
        put(ws, f"H{5 + i}", f"=SUMIFS({col(S_SHOP, 'O', N_SHOP)},{col(S_SHOP, 'B', N_SHOP)},G{5 + i})", "calc", USD)
    put(ws, "G13", "Night", "head")
    put(ws, "H13", "Adults", "head")
    put(ws, "I13", "Kids", "head")
    ws.column_dimensions["I"].width = 10
    put(ws, "G14", "1st seder", "calc")
    put(ws, "H14", "=adults1", "calc", NUM)
    put(ws, "I14", "=kids1", "calc", NUM)
    put(ws, "G15", "2nd seder", "calc")
    put(ws, "H15", "=adults2", "calc", NUM)
    put(ws, "I15", "=kids2", "calc", NUM)
    bar_chart(ws, "A18", "Shopping cost by category", Reference(ws, min_col=7, min_row=5, max_row=10),
              [Reference(ws, min_col=8, min_row=4, max_row=10)], width=20, height=8)
    bar_chart(ws, "A35", "Who's coming", Reference(ws, min_col=7, min_row=14, max_row=15),
              [Reference(ws, min_col=8, max_col=9, min_row=13, max_row=15)], width=13, height=8, horizontal=False,
              stacked=True, money=False)
    return ws


def build(demo=False):
    wb = new_book()
    build_settings(wb, demo)
    build_guests(wb, demo)
    build_shopping(wb, demo)
    build_menu(wb, demo)
    build_haggadah(wb, demo)
    build_timeline(wb, demo)
    build_plate(wb, demo)
    d = build_dashboard(wb, demo)
    wb.move_sheet(d, offset=-(len(wb.sheetnames) - 2))
    instructions(
        wb, "Passover Seder Planner",
        "Guest list for one or two seders, a shopping list that scales with your head count, a menu and cooking plan, "
        "haggadah reading parts, a prep timeline counted back from the seder, and a seder-plate checklist.",
        ["Settings: enter the date of the first seder, how many seders you host and how many seder plates.",
         "Guests: one row per household, with adults, kids, which night and RSVP.",
         "Shopping List: quantities update automatically. Adjust the yellow per-person rates, pack sizes and your "
         "store's prices; mark items Bought as you shop.",
         "Menu: list dishes, who brings them and how many days ahead to cook.",
         "Haggadah Parts: give everyone a part, from the Four Questions to Chad Gadya.",
         "Dashboard: head counts, shopping cost, what's left to buy and overdue prep tasks."],
        ["Ritual quantities (matzah, wine, maror, eggs) start from the per-person guidance published by Chabad.org "
         "(e.g. 3 shmurah matzot per seder plate, plus about 2 per other participant, per seder; about 2 oz of maror "
         "per person per night; roughly 6–8 handmade shmurah matzot per pound). Meal quantities are common catering "
         "rules of thumb. Halachic minimums and family customs vary: adjust the rates and ask your rabbi.",
         "Kids are counted separately so you can plan grape juice instead of wine and smaller portions."],
        [("Settings", "Seder date, number of seders and plates; head counts."),
         ("Dashboard", "People per night, shopping cost, what's left to buy, overdue tasks, charts."),
         ("Guests", "Households, adults, kids, night, RSVP, dietary needs, what they bring."),
         ("Shopping List", "26 items scaled by guests and seders; packs to buy and estimated cost."),
         ("Menu", "Dishes, cooks, make-ahead days and prep dates."),
         ("Haggadah Parts", "The 15 steps of the seder plus favourites, assigned per night."),
         ("Prep Timeline", "17 tasks from invitations to burning chametz, dated automatically."),
         ("Seder Plate", "Seder plate and table checklist with the meaning of each item.")])
    wb.active = 0
    props(wb, "Passover Seder Planner", "Passover seder planning spreadsheet")
    return wb
