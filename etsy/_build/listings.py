"""Single source for every Etsy listing: text (-> listing.md) and image specs (-> images/)."""
import pathlib

L = pathlib.Path(__file__).resolve().parents[1] / "listings"

AI_NOTE = ("Designed by our shop. The illustrations, layouts and spreadsheet formulas were created with the help of AI "
           "tools, then checked and tested by us (every formula recalculated, every page test-printed to PDF).")
DIGITAL = ("This is a DIGITAL DOWNLOAD. No physical item will be shipped. After payment, Etsy gives you the files "
           "right away (Purchases page + email link).")
XLSX_HOW = [
    "Buy, then download the .xlsx files from Etsy (You > Purchases and reviews > Download files).",
    "Excel: double-click the file. Google Sheets: go to drive.google.com > New > File upload, then open the file with Google Sheets (or in Sheets: File > Import > Upload).",
    "Start with the Instructions / Start Here sheet. Type only in the yellow cells; grey cells calculate by themselves.",
    "Look at the EXAMPLE file to see a finished version, then fill in the blank file with your own details.",
]
XLSX_COMPAT = ("Works in Microsoft Excel (2016 or newer, Excel 365, Excel for Mac), Google Sheets (free), Apple Numbers "
               "(basic use; charts may look different) and LibreOffice. No macros, no add-ins, nothing to install.")
LICENSE = ("Personal use only. Please do not resell, share or post the files publicly. You may print as many copies "
           "as you need for your own family, event or classroom.")

LISTINGS = []


def add(**kw):
    LISTINGS.append(kw)
    return kw


def by_slug(slug):
    return next(x for x in LISTINGS if x["slug"] == slug)


def files_of(slug):
    return sorted((L / slug / "files").iterdir())


# =============================================================================== 01 Hanukkah Activity Pack
PACK = "01-hanukkah-activity-pack"
add(
    slug=PACK, n=1, theme="hanukkah", onboarding=True,
    title="Hanukkah Activity Pack for Kids, Printable Hanukkah Coloring Pages, Mazes, Word Search, Dreidel Game, Candle Chart 2026, PDF",
    price=6.00,
    tags=["hanukkah printable", "hanukkah coloring", "hanukkah for kids", "chanukah activities", "dreidel game",
          "hanukkah worksheets", "jewish kids crafts", "menorah coloring", "hanukkah 2026", "chanukah printable",
          "hebrew school", "hanukkah party game", "hanukkah gift kids"],
    category="Type \"coloring\" in the Category box and pick: Books, Movies & Music > Books > Coloring Books (or Paper & Party Supplies > Paper > Stationery if it is not offered).",
    attributes={"Type": "Digital download", "Occasion": "Hanukkah", "Holiday": "Hanukkah", "Subject / theme": "Holidays",
                "Recipient": "Children / Unisex kids", "Craft type (if asked)": "Coloring, Paper crafts"},
    intro="20 printable Hanukkah pages to keep kids busy and happy for all eight nights. Print at home or in class: "
          "coloring pages, mazes, a word search, the dreidel game with a score sheet, a cut-and-fold paper dreidel, a 2026 "
          "candle-lighting chart, blessings, kindness challenge and greeting cards. Ages about 4–10.",
    inside=["Cover + contents + the Hanukkah story in a nutshell + printing tips",
            "5 coloring pages: menorah, dreidels, latkes & jelly doughnuts, menorah in the window, the jug of oil",
            "Color-by-number menorah",
            "Count the candles (8 nights)",
            "2 mazes: easy and tricky",
            "Hanukkah word search (14 words) + answer key",
            "How to play dreidel (נ ג ה ש, with rules) + dreidel score sheet",
            "Make your own dreidel: real-size cut-and-fold template",
            "Candle-lighting chart for Hanukkah 2026 (Dec 4–11, Friday-night notes)",
            "Candle blessings in Hebrew, transliteration and English",
            "8 Nights of Kindness tracker",
            "2 Hanukkah cards to color, cut out and give"],
    formats=["2 PDF files: US Letter (8.5 x 11 in) and A4 — the same 20 pages, choose your paper size",
             "Vector art: crisp at any print size; black & white friendly coloring pages"],
    how=["Buy and download the PDF from Etsy (You > Purchases and reviews > Download files).",
         "Open it with any PDF reader (Adobe Acrobat Reader, Preview on Mac, your phone or browser).",
         "Print at 100% / \"Actual size\". Plain paper is fine; card stock is best for the paper dreidel and the cards.",
         "Print again as often as you like for your own family or class."],
    compat="Any PDF reader on computer, tablet or phone. Prints on home printers (Letter or A4).",
    faq=[("Is this a physical product?", "No. It is a printable PDF you download and print yourself."),
         ("Which dates are on the chart?", "Hanukkah 2026: first candle Friday evening Dec 4, eighth candle Friday evening Dec 11."),
         ("Can I use it with my class?", "Yes, print as many copies as you need for your own class or Hebrew school group. Please don't share the file itself.")],
)

# =============================================================================== 02 Hanukkah Party Planner
PARTY = "02-hanukkah-party-planner"
add(
    slug=PARTY, n=2, theme="hanukkah",
    title="Hanukkah Party Planner Spreadsheet, Latke & Jelly Doughnut Calculator, Guest List, Shopping List, 8 Nights Gift Tracker, Excel Google Sheets",
    price=7.00,
    tags=["hanukkah planner", "hanukkah party", "chanukah party", "latke party", "hanukkah gifts list",
          "gift tracker", "party planner excel", "google sheets party", "holiday spreadsheet", "jewish holiday",
          "hanukkah 2026", "party shopping list", "8 nights of gifts"],
    category="Type \"planner\" in the Category box and pick: Paper & Party Supplies > Paper > Calendars & Planners.",
    attributes={"Type": "Digital download", "Occasion": "Hanukkah", "Holiday": "Hanukkah", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="Hosting latkes night? Type the number of adults and kids and this spreadsheet tells you how many latkes, "
          "jelly doughnuts and pounds of potatoes you need, builds the shopping list with costs, and keeps the 8-nights "
          "gift list, RSVPs and to-dos in one place.",
    inside=["Instructions sheet (start here)",
            "Guests: adults, kids, RSVP drop-downs, which night, food notes, automatic totals",
            "Quantities: latkes, jelly doughnuts, potatoes, oil, eggs, flour, drinks, gelt, candles — from your head count (20 editable assumptions, make or buy doughnuts)",
            "Shopping List: automatic rows + 25 of your own, estimated cost, bought ✓",
            "8 Nights Gifts: who gets what on which night, budget vs actual, status (idea / bought / wrapped / given)",
            "To-Do: 16 tasks with due dates counted back from your party date, overdue turns red",
            "Dashboard: guest totals, quantities, costs + 2 charts"],
    formats=["2 .xlsx files: a BLANK planner and a filled-in EXAMPLE party",
             "US units (lb, cups) and US dollars; currency format is easy to change"],
    how=XLSX_HOW, compat=XLSX_COMPAT,
    faq=[("Do I need Excel?", "No. It also works in free Google Sheets (upload the file to Google Drive and open it with Google Sheets)."),
         ("Are the prices real?", "The prices in the example are only sample numbers. Type the prices from your own store.")],
)

# =============================================================================== 03 Hanukkah Bundle
add(
    slug="03-hanukkah-bundle", n=3, theme="hanukkah", bundle_of=[PACK, PARTY],
    title="Hanukkah Bundle: Kids Activity Pack Printable + Hanukkah Party Planner Spreadsheet, Coloring Pages, Dreidel Game, Latke Calculator",
    price=10.00,
    tags=["hanukkah bundle", "hanukkah printable", "hanukkah planner", "hanukkah for kids", "hanukkah coloring",
          "chanukah party", "dreidel game", "latke party", "hanukkah 2026", "jewish holiday", "hanukkah worksheets",
          "gift tracker", "chanukah printable"],
    category="Same as the Activity Pack: type \"coloring\" or \"planner\" and pick Paper & Party Supplies > Paper > Calendars & Planners.",
    attributes={"Type": "Digital download", "Occasion": "Hanukkah", "Holiday": "Hanukkah"},
    intro="Everything for Hanukkah at home in one download: the 20-page kids' activity pack (print-and-play) plus the "
          "Hanukkah party planner spreadsheet (latkes, doughnuts, shopping list, 8 nights of gifts). Save vs buying "
          "them separately ($6 + $7).",
    inside=["Hanukkah Activity Pack (20 pages, PDF in US Letter and A4): coloring pages, mazes, word search, dreidel game + score sheet, cut-and-fold dreidel, 2026 candle chart, blessings, kindness tracker, cards",
            "Hanukkah Party Planner (.xlsx blank + example): guests, latke & doughnut quantities, shopping list with costs, 8-nights gift tracker, to-do list, dashboard"],
    formats=["2 PDF files (Letter + A4) and 2 .xlsx files (blank + example)"],
    how=["Download the 4 files from Etsy (You > Purchases and reviews > Download files).",
         "Print the PDF at 100% (Letter or A4).",
         "Open the .xlsx in Excel, or upload it to Google Drive and open with Google Sheets. Type in the yellow cells."],
    compat="PDF: any PDF reader. Spreadsheet: " + XLSX_COMPAT,
    faq=[("What's the difference from buying separately?", "Same files, lower price ($10 instead of $13).")],
)


def description(x):
    out = [x["intro"], "", "★ WHAT YOU GET"]
    out += [f"• {i}" for i in x["inside"]]
    out += ["", "★ FILE FORMAT"] + [f"• {f}" for f in x["formats"]]
    out += ["", "★ HOW IT WORKS"] + [f"{i + 1}. {s}" for i, s in enumerate(x["how"])]
    out += ["", "★ COMPATIBILITY", x["compat"]]
    out += ["", "★ INSTANT DOWNLOAD", DIGITAL]
    if x.get("faq"):
        out += ["", "★ QUESTIONS"]
        for q, a in x["faq"]:
            out += [f"Q: {q}", f"A: {a}"]
    out += ["", "★ LICENSE", LICENSE, "", "★ WHO MADE IT", AI_NOTE, "",
            "Questions or a file that won't open? Send us a message on Etsy and we'll help."]
    return "\n".join(out)

# =============================================================================== 04 Bar/Bat Mitzvah
BM = "04-bar-bat-mitzvah-planner"
add(
    slug=BM, n=4, theme="mitzvah",
    title="Bar Mitzvah Planner Spreadsheet, Bat Mitzvah Budget, Guest List & RSVP Tracker, Aliyot, Candle Lighting, Checklist, Excel Google Sheets",
    price=12.00,
    tags=["bar mitzvah", "bat mitzvah", "bar mitzvah planner", "bat mitzvah planner", "mitzvah budget",
          "rsvp tracker", "guest list template", "candle lighting", "jewish celebration", "event planner excel",
          "party budget sheet", "sheets planner", "mitzvah checklist"],
    category="Type \"planner\" in the Category box and pick: Paper & Party Supplies > Paper > Calendars & Planners.",
    attributes={"Type": "Digital download", "Occasion": "Bar & Bat Mitzvah (or Religious celebration)", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="Plan the whole bar or bat mitzvah in one spreadsheet: budget, vendors and payments, guest list with RSVPs, "
          "gifts and thank-you notes, aliyot and candle-lighting honors, seating, a full checklist and a day-of schedule. "
          "Everything adds up by itself.",
    inside=["Start Here + Settings (event name, date, budget, price per guest, your drop-down lists)",
            "Dashboard: days to go, budget vs committed vs paid, RSVPs, gifts, honors and checklist progress, charts",
            "Budget: 14 categories (kiddush, party, DJ, photo, invitations, tallit, tutor…) planned vs committed vs paid",
            "Vendors + Payments: contracts, deposits and installments with due dates; overdue turns red",
            "Guest list: households, RSVP, adults/kids, meal, table, gift received, thank-you sent",
            "Seating helper: tables, seats, who's still unseated",
            "Checklist: 34 tasks with due dates counted back from the date",
            "Honors & Candle-lighting: aliyot, ark opening, 13+1 candle-lighting honors",
            "Day-of schedule: service, kiddush and party run-of-show"],
    formats=["2 .xlsx files: BLANK planner + filled-in EXAMPLE", "US dollars; easy to change the currency format"],
    how=XLSX_HOW, compat=XLSX_COMPAT,
    faq=[("Does it work for a bat mitzvah / b'nai mitzvah?", "Yes. Every label is editable and the lists live on the Settings sheet."),
         ("Do I need Excel?", "No, free Google Sheets works too.")],
)

# =============================================================================== 05 Jewish Wedding Planner
JW = "05-jewish-wedding-planner"
add(
    slug=JW, n=5, theme="wedding",
    title="Jewish Wedding Planner Spreadsheet, Wedding Budget, Guest List RSVP, Ketubah & Chuppah Honors, Checklist, Seating, Excel Google Sheets",
    price=14.00,
    tags=["jewish wedding", "wedding planner", "wedding spreadsheet", "chuppah", "ketubah", "wedding budget",
          "wedding checklist", "guest list tracker", "rsvp tracker", "wedding google sheet", "interfaith wedding",
          "jewish bride", "engagement gift"],
    category="Type \"wedding planner\" in the Category box and pick: Paper & Party Supplies > Paper > Calendars & Planners (or Weddings > … > Wedding Planners if offered).",
    attributes={"Type": "Digital download", "Occasion": "Wedding", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="A complete wedding planner built for Jewish weddings: budget and payments, vendors, guest list with RSVPs and "
          "gifts, ceremony honors (witnesses, chuppah holders, sheva brachot), seating, a 36-task checklist and a day-of "
          "timeline from tisch to hora. Type in the yellow cells; everything else updates itself.",
    inside=["Start Here + Settings (names, date, budget, price per guest, drop-down lists)",
            "Dashboard: days to go, budget, payments, RSVPs, gifts, honors, checklist progress + charts",
            "Budget: 14 categories incl. ketubah, chuppah & officiant; planned vs committed vs paid",
            "Vendors + Payments: contracts, deposits and installments with due dates; overdue in red",
            "Guest list: households, side, RSVP, meal, table, gift, thank-you sent",
            "Seating: tables and seats filled from the guest list",
            "Checklist: 36 Jewish-wedding tasks with automatic due dates",
            "Ceremony Honors: witnesses, ketubah reader, chuppah holders, sheva brachot, escorts, tisch",
            "Day-of schedule: tisch, ketubah signing, bedeken, chuppah, yichud, hora, sheva brachot"],
    formats=["2 .xlsx files: BLANK planner + filled-in EXAMPLE wedding", "US dollars; easy to change the currency format"],
    how=XLSX_HOW, compat=XLSX_COMPAT,
    faq=[("Can we use it for an interfaith or non-religious wedding?", "Yes. Rename or delete any task, honor or category."),
         ("Is the checklist religious advice?", "No. It is a practical planning list. Customs vary, so follow your rabbi or officiant.")],
)

# =============================================================================== 06 Wedding Budget Planner
WB = "06-wedding-budget-planner"
add(
    slug=WB, n=6, theme="wedding",
    title="Wedding Budget Planner Spreadsheet, Wedding Budget Tracker, Vendor Quote Comparison, Payment Schedule, Excel & Google Sheets Template",
    price=7.00,
    tags=["wedding budget", "budget tracker", "wedding spreadsheet", "wedding planner", "budget template",
          "wedding expenses", "vendor comparison", "payment tracker", "wedding google sheet", "engaged gift",
          "bride to be", "wedding planning", "excel template"],
    category="Type \"wedding planner\" in the Category box and pick: Paper & Party Supplies > Paper > Calendars & Planners.",
    attributes={"Type": "Digital download", "Occasion": "Wedding", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="Know exactly where your wedding money goes. Set the total budget, plan each category, log every deposit and "
          "payment, compare vendor quotes and see what's paid, what's due next and how much is left — automatically.",
    inside=["Start Here sheet with quick-start steps",
            "Settings: names, date, total budget, guest count, 20 editable categories with suggested % split",
            "Budget: suggested vs your estimate vs committed vs paid per category; overspending turns red",
            "Expenses & Payments: 120 rows for deposits, installments and balances with due dates; overdue / due-soon alerts",
            "Vendor Quotes: compare up to 60 quotes; the cheapest per category is highlighted",
            "Dashboard: budget left, paid, still to pay, due in the next 30 days, cost per guest, days to go + 2 charts"],
    formats=["2 .xlsx files: BLANK planner + filled-in EXAMPLE", "US dollars; works with any currency (change the cell format)"],
    how=XLSX_HOW, compat=XLSX_COMPAT,
    faq=[("Is this the full wedding planner?", "This one is budget-focused. For guests, honors, checklist and seating see our Jewish Wedding Planner or the Wedding Planning Bundle."),
         ("Can I change the categories?", "Yes, rename or add them on the Settings sheet and they flow everywhere.")],
)

# =============================================================================== 07 Seating chart
SC = "07-wedding-seating-chart"
add(
    slug=SC, n=7, theme="wedding",
    title="Wedding Seating Chart Template, Printable Table Plan + Excel Google Sheets Guest Seating Planner, Table Numbers 1-30, Find Your Seat",
    price=6.00,
    tags=["seating chart", "wedding seating", "seating plan", "table plan", "table numbers", "find your seat",
          "seating template", "guest seating", "reception seating", "printable wedding", "wedding table plan",
          "seating spreadsheet", "event seating"],
    category="Type \"seating chart\" in the Category box and pick: Weddings > Decorations > Seating Charts (or Paper & Party Supplies > Paper > Calendars & Planners).",
    attributes={"Type": "Digital download", "Occasion": "Wedding", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="Two ways to plan who sits where: a smart spreadsheet that turns your guest list into a table-by-table seating "
          "plan (with over-capacity warnings), and a printable kit with round and long table planners, a floor-plan grid, "
          "a Find Your Seat board and table numbers 1–30.",
    inside=["Spreadsheet (.xlsx): Guests (400 rows: side, group, meal, table #, notes) → Seating Plan fills itself, seat by seat",
            "Tables sheet: 40 tables, names, seats per table, seated / free, 'Over by 2' warnings, guests without a table",
            "Printable PDF kit (26 pages): round table planners for 8, 10 and 12 seats",
            "Long / head table planner (up to 20 seats) + notes",
            "Floor-plan dot grid to sketch the room",
            "Find Your Seat A–Z guest board (2 pages)",
            "Table number cards 1–30 (2 per page)"],
    formats=["2 .xlsx files (BLANK + EXAMPLE) and 2 PDF files (US Letter + A4)", "PDF printables are not editable; write by hand or use the spreadsheet"],
    how=["Download the 4 files from Etsy (You > Purchases and reviews > Download files).",
         "Spreadsheet: open in Excel, or upload to Google Drive and open with Google Sheets. Type guests, pick table numbers.",
         "Seating Plan updates by itself. Print it or share it with your venue.",
         "Printables: print the PDF at 100% on Letter or A4 (card stock for table numbers)."],
    compat="Spreadsheet: " + XLSX_COMPAT + " PDF: any PDF reader.",
    faq=[("Is this a large printed seating board?", "No. It's a planning kit (letter/A4 pages) and a spreadsheet. Nothing is shipped."),
         ("Works for bar mitzvahs, galas, parties?", "Yes, any seated event.")],
)

# =============================================================================== 08 Passover
PS = "08-passover-seder-planner"
add(
    slug=PS, n=8, theme="passover",
    title="Passover Seder Planner Spreadsheet, Pesach Shopping List Calculator, Seder Guest List, Menu, Haggadah Reading Parts, Excel Google Sheets",
    price=8.00,
    tags=["passover", "passover seder", "seder planner", "pesach", "passover printable", "seder plate",
          "haggadah", "passover menu", "jewish holiday", "pesach planner", "shopping list", "holiday hosting",
          "passover 2027"],
    category="Type \"planner\" in the Category box and pick: Paper & Party Supplies > Paper > Calendars & Planners.",
    attributes={"Type": "Digital download", "Occasion": "Passover", "Holiday": "Passover", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="Hosting the seder? Enter your guests for one or two nights and the planner scales the shopping list (matzah, "
          "wine, eggs, seder plate items…) to your head count, keeps the menu, assigns Haggadah reading parts and gives "
          "you a prep timeline.",
    inside=["Start Here + Settings",
            "Guests per night: 1st and 2nd seder, adults / kids, 'maybe' toggle",
            "Shopping List: 26 items scaled by adults, kids and seder plates, with packs to buy and cost",
            "Menu planner",
            "Haggadah Parts: who reads what",
            "Prep Timeline: what to do when, counted back from the seder",
            "Seder Plate guide",
            "Dashboard with totals and charts"],
    formats=["2 .xlsx files: BLANK planner + filled-in EXAMPLE seder", "US units and dollars; example prices are samples"],
    how=XLSX_HOW, compat=XLSX_COMPAT,
    faq=[("Which year?", "Any year: type your own seder date. Passover 2027 begins the evening of April 21, 2027."),
         ("Is the quantity guide religious advice?", "No. It's a practical estimate. Follow your family's and rabbi's customs.")],
)

# =============================================================================== 09 Holiday hosting
HH = "09-jewish-holiday-hosting-planner"
add(
    slug=HH, n=9, theme="holiday",
    title="Jewish Holiday Hosting Planner Spreadsheet, Rosh Hashanah, Sukkot, Hanukkah, Purim, Passover & Shabbat Menus, Guests, Shopping",
    price=8.00,
    tags=["jewish holiday", "rosh hashanah", "shabbat dinner", "holiday planner", "sukkot", "purim",
          "mishloach manot", "jewish hostess gift", "holiday menu", "hosting planner", "jewish calendar",
          "yom tov", "shavuot"],
    category="Type \"planner\" in the Category box and pick: Paper & Party Supplies > Paper > Calendars & Planners.",
    attributes={"Type": "Digital download", "Occasion": "Religious holiday", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="One planner for every holiday meal of the year: Rosh Hashanah, Yom Kippur break-fast, Sukkot, Hanukkah, "
          "Purim, Passover, Shavuot and Shabbat. Guests per holiday, menus, shopping and budget, traditions, and a "
          "mishloach manot list.",
    inside=["Start Here + Settings",
            "Holidays: 9 meals with dates, guest counts and budget",
            "Guests × holidays grid: who comes to which meal",
            "Menus per holiday",
            "Shopping & budget",
            "Traditions: 32 customs and foods to remember",
            "Mishloach Manot list for Purim",
            "Dashboard with totals and charts"],
    formats=["2 .xlsx files: BLANK planner + filled-in EXAMPLE year", "US dollars"],
    how=XLSX_HOW, compat=XLSX_COMPAT,
    faq=[("Is it dated?", "No: type your own dates each year, and reuse it."),
         ("Is it a gift?", "A digital download makes an easy last-minute gift: use Etsy's 'This order is a gift' option and send the files to them.")],
)

# =============================================================================== 10 Jewish Life Bundle
add(
    slug="10-jewish-life-bundle", n=10, theme="mitzvah", bundle_of=[BM, JW, PS, HH],
    title="Jewish Life Planner Bundle: Bar Bat Mitzvah, Jewish Wedding, Passover Seder & Holiday Hosting Spreadsheets, Excel Google Sheets",
    price=29.00,
    tags=["jewish planner", "bar mitzvah", "bat mitzvah", "jewish wedding", "passover seder", "jewish holiday",
          "planner bundle", "rosh hashanah", "chuppah", "jewish gift", "family planner", "google sheets bundle",
          "hosting planner"],
    category="Type \"planner\" in the Category box and pick: Paper & Party Supplies > Paper > Calendars & Planners.",
    attributes={"Type": "Digital download", "Occasion": "Religious celebration", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="All four of our Jewish-life planners in one download: Bar/Bat Mitzvah, Jewish Wedding, Passover Seder and "
          "Holiday Hosting. $29 instead of $42 if bought separately. Each comes as a blank planner + a filled-in example.",
    inside=["Bar/Bat Mitzvah Planner: budget, vendors & payments, guests & gifts, aliyot & candle-lighting, seating, checklist, day-of",
            "Jewish Wedding Planner: budget, vendors & payments, guests, ketubah & chuppah honors, seating, 36-task checklist, day-of",
            "Passover Seder Planner: guests per night, scaled shopping list, menu, Haggadah parts, prep timeline",
            "Jewish Holiday Hosting Planner: 9 holiday meals, guests, menus, shopping, traditions, mishloach manot"],
    formats=["4 ZIP files (one per planner), each with a BLANK and an EXAMPLE .xlsx",
             "Unzip: double-click on Mac / right-click > Extract All on Windows"],
    how=["Download the 4 ZIP files from Etsy (You > Purchases and reviews > Download files).",
         "Unzip each one (double-click on Mac; right-click > Extract All on Windows).",
         "Open the .xlsx in Excel, or upload it to Google Drive and open with Google Sheets.",
         "Start with the Start Here sheet; type in the yellow cells."],
    compat=XLSX_COMPAT,
    faq=[("Can I buy the planners separately?", "Yes, each one has its own listing in the shop.")],
)

# =============================================================================== 11 Wedding bundle
add(
    slug="11-wedding-planning-bundle", n=11, theme="wedding", bundle_of=[JW, WB, SC],
    title="Wedding Planning Bundle: Jewish Wedding Planner, Wedding Budget Tracker & Seating Chart Template, Excel Google Sheets + Printables",
    price=19.00,
    tags=["wedding bundle", "wedding planner", "wedding budget", "seating chart", "jewish wedding",
          "wedding spreadsheet", "table numbers", "guest list tracker", "wedding checklist", "engagement gift",
          "bride to be", "chuppah", "wedding printable"],
    category="Type \"wedding planner\" in the Category box and pick: Paper & Party Supplies > Paper > Calendars & Planners.",
    attributes={"Type": "Digital download", "Occasion": "Wedding", "Software (if asked)": "Microsoft Excel, Google Sheets"},
    intro="Three wedding tools in one download: the full Jewish Wedding Planner, the Wedding Budget Planner and the "
          "Wedding Seating Chart (spreadsheet + printable kit). $19 instead of $27 if bought separately.",
    inside=["Jewish Wedding Planner (.xlsx blank + example): budget, vendors & payments, guests & RSVPs, ceremony honors, 36-task checklist, seating, day-of timeline",
            "Wedding Budget Planner (.xlsx blank + example): category budget, payments with due dates, vendor quote comparison, dashboard",
            "Wedding Seating Chart (.xlsx blank + example + 26-page printable PDF in Letter and A4): seating plan, round/long table planners, Find Your Seat board, table numbers 1–30"],
    formats=["3 ZIP files (one per product), each with the blank + example files (and the seating PDFs)",
             "Unzip: double-click on Mac / right-click > Extract All on Windows"],
    how=["Download the files from Etsy (You > Purchases and reviews > Download files).",
         "Unzip each ZIP.",
         "Open the .xlsx in Excel, or upload to Google Drive and open with Google Sheets. Print the PDFs at 100%."],
    compat="Spreadsheets: " + XLSX_COMPAT + " PDFs: any PDF reader.",
    faq=[("Is the budget planner also inside the wedding planner?", "The wedding planner has a budget sheet; the Budget Planner adds a deeper payment schedule and vendor quote comparison. Use whichever you like.")],
)
