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
