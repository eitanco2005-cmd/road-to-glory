#!/usr/bin/env python3
"""Generate listing.md + images/ for listings.   python3 etsy/_build/gen.py [slug-prefix ...]"""
import shutil
import sys

import images as I
import listings as LS
from renders import pdf_page, xlsx_sheet

L = LS.L
XLSX_STEPS = [("Download", "Buy, then download the files from your Etsy Purchases page. Instant, no waiting."),
              ("Open", "Excel: double-click. Google Sheets: upload to Google Drive and open with Sheets."),
              ("Fill in", "Type in the yellow cells. Totals, lists and charts update by themselves.")]
XLSX_COMPAT = [("Opens in", ["Microsoft Excel (Windows & Mac)", "Google Sheets (free)", "LibreOffice", "Excel / Sheets phone apps"]),
               ("You get", ["Blank planner (.xlsx)", "Filled-in EXAMPLE file", "No macros, nothing to install", "Instant digital download"])]
NOT_PHYSICAL = "Digital download · no physical item is shipped"


def f(slug, name):
    return L / slug / "files" / name


# ------------------------------------------------------------------ per-listing image specs
def spec_pack(x):
    pdf = f(x["slug"], "Hanukkah-Activity-Pack-2026-US-Letter.pdf")
    P = lambda n: pdf_page(pdf, n)  # noqa: E731
    t = "hanukkah"
    return [
        I.hero(t, "Hanukkah Activity Pack", "20 printable pages for kids: color, play, cut & fold, light the candles",
               ["20 pages", "Ages 4–10", "Letter + A4", "Instant download"], [P(3), P(13), P(1)], kicker="Printable · 2026"),
        I.grid(t, "What's inside: 20 pages", "Coloring, puzzles, games, crafts, candle chart & blessings",
               [(P(n), l) for n, l in [(1, "Cover"), (3, "Color the menorah"), (4, "Dreidels"), (5, "Treats"), (6, "Window"),
                                       (7, "Jug of oil"), (8, "Color by number"), (9, "Count candles"), (10, "Easy maze"),
                                       (11, "Tricky maze"), (12, "Word search"), (13, "Dreidel rules"), (14, "Score sheet"),
                                       (15, "Paper dreidel"), (16, "Candle chart"), (17, "Blessings"), (18, "Kindness"),
                                       (19, "Cards"), (20, "Answer key"), (2, "Contents")]], cols=7),
        I.shot(t, "Big, bold coloring pages", "Simple outlines that little hands can color", [P(3), P(5)]),
        I.shot(t, "Puzzles and the dreidel game", "Mazes, word search, rules and a score sheet", [P(11), P(12), P(13)]),
        I.shot(t, "Make your own dreidel", "Real-size cut-and-fold template — best on card stock", [P(15)],
               bullets=["Cut, fold, glue", "Push a pencil through the middle", "Spin and play with the rules page"]),
        I.shot(t, "Hanukkah 2026 candle chart", "Dates for all 8 nights + blessings in Hebrew, transliteration & English",
               [P(16), P(17)]),
        I.steps(t, "How it works", [("Buy", "Checkout on Etsy. The PDF is ready right away."),
                                    ("Download", "Get it from your Etsy Purchases page or the email link."),
                                    ("Print", "Print at 100% on Letter or A4. Print again any time.")], footer=NOT_PHYSICAL),
        I.checklist(t, "Good to know", "One PDF in two paper sizes",
                    [("Formats", ["US Letter 8.5 x 11 in", "A4 (Europe, Israel, UK)", "Crisp vector art", "Black & white friendly"]),
                     ("Great for", ["Family Hanukkah nights", "Parties & kids' tables", "Hebrew school & classrooms", "Grandparents' visits"])]),
    ]


def party_shots(slug, prefix="Hanukkah-Party-Planner-EXAMPLE.xlsx"):
    xl = f(slug, prefix)
    return dict(dash=xlsx_sheet(xl, "Hanukkah Party Planner 2026", nth=-1), qty=xlsx_sheet(xl, "Quantities", crop=(0, .55)),
                shop=xlsx_sheet(xl, "Shopping List", crop=(0, .6)), gifts=xlsx_sheet(xl, "8 Nights Gifts", crop=(0, .4), xcrop=(0, .64)),
                todo=xlsx_sheet(xl, "To-Do", crop=(0, .45)), guests=xlsx_sheet(xl, "Guests", crop=(0, .4), xcrop=(0, .7)))


def spec_party(x):
    t = "hanukkah"
    s = party_shots(x["slug"])
    return [
        I.hero(t, "Hanukkah Party Planner", "Latkes, doughnuts, shopping, guests and 8 nights of gifts — in one spreadsheet",
               ["Excel", "Google Sheets", "Blank + example", "Instant download"], [s["shop"], s["gifts"], s["dash"]],
               landscape=True, kicker="Spreadsheet · 2026"),
        I.shot(t, "Dashboard", "Everything at a glance: guests, quantities, costs, gifts by night", [s["dash"]]),
        I.shot(t, "How many latkes do we need?", "Type adults + kids. Quantities calculate themselves.", [s["qty"]],
               bullets=["Latkes, doughnuts, potatoes, oil", "Make or buy doughnuts", "20 editable assumptions"]),
        I.shot(t, "Shopping list with costs", "Auto rows from your head count + your own items", [s["shop"]]),
        I.shot(t, "8 Nights gift tracker", "Who gets what on which night, budget vs actual", [s["gifts"]]),
        I.shot(t, "Countdown to-do list", "16 tasks with due dates counted back from your party date", [s["todo"]],
               bullets=["Overdue tasks turn red", "Tick ✓ when done", "Guest list with RSVPs too"]),
        I.steps(t, "How it works", XLSX_STEPS, footer=NOT_PHYSICAL),
        I.checklist(t, "Works where you work", "No macros, no add-ins", XLSX_COMPAT),
    ]


def spec_hbundle(x):
    t = "hanukkah"
    pdf = f(x["slug"], "Hanukkah-Activity-Pack-2026-US-Letter.pdf")
    P = lambda n: pdf_page(pdf, n)  # noqa: E731
    s = party_shots(x["slug"])
    return [
        I.hero(t, "Hanukkah Bundle", "Kids' activity pack + party planner spreadsheet. Save vs buying separately.",
               ["20-page PDF", "Excel + Sheets", "4 files", "Instant download"], [P(13), P(3), P(1)], kicker="2 products · 1 price"),
        I.checklist(t, "What's in the bundle", "Two products, one download",
                    [("Activity Pack (PDF)", ["20 pages, Letter + A4", "Coloring & color-by-number", "Mazes & word search",
                                              "Dreidel game + paper dreidel", "2026 candle chart & blessings"]),
                     ("Party Planner (.xlsx)", ["Latke & doughnut calculator", "Shopping list with costs", "Guest list & RSVPs",
                                                "8 nights gift tracker", "To-do list + dashboard"])]),
        I.grid(t, "Activity pack pages", "Print at home or in class", [(P(n), l) for n, l in
               [(3, "Coloring"), (8, "Color by number"), (10, "Maze"), (12, "Word search"), (15, "Paper dreidel"),
                (16, "Candle chart"), (17, "Blessings"), (19, "Cards")]], cols=4),
        I.shot(t, "Party planner dashboard", "Guests, quantities, costs and gifts at a glance", [s["dash"]]),
        I.shot(t, "Quantities + shopping list", "From head count to shopping list in seconds", [s["qty"], s["shop"]]),
        I.shot(t, "8 Nights gift tracker", "Budget vs actual for every night", [s["gifts"]]),
        I.steps(t, "How it works", [("Download", "All 4 files from your Etsy Purchases page."), ("Print", "The activity pack at 100%, Letter or A4."),
                                    ("Plan", "Open the planner in Excel or Google Sheets.")], footer=NOT_PHYSICAL),
    ]


SPECS = {"01": spec_pack, "02": spec_party, "03": spec_hbundle}


def listing_md(x):
    files = [p.name for p in LS.files_of(x["slug"])]
    imgs = sorted(p.name for p in (L / x["slug"] / "images").glob("*.jpg"))
    lines = [f"# Listing {x['n']:02d}: {x['slug'][3:]}", ""]
    if x.get("onboarding"):
        lines += ["> **This is the FIRST listing** — paste it during Etsy's shop-setup (\"Stock your shop\") step.", ""]
    lines += ["## Title", "```", x["title"], "```", f"({len(x['title'])}/140 characters)", "",
              "## Price (USD)", "```", f"{x['price']:.2f}", "```", "Quantity: 999 (digital — Etsy suggests this).", "",
              "## Tags (13 — paste one at a time, press Enter after each)", "```"] + x["tags"] + ["```", "",
              "## Description", "```", LS.description(x), "```", "",
              "## Category", x["category"], "", "## Attributes (fill what Etsy shows; skip the rest)"]
    lines += [f"- **{k}:** {v}" for k, v in x["attributes"].items()]
    lines += ["", "## About this listing (Etsy's questions)",
              "- **Who made it?** I did",
              "- **What is it?** A finished product",
              "- **When was it made?** Made to order → choose **2020–2026** (or the newest range shown)",
              "- **Type:** Digital files",
              "- **AI disclosure:** Etsy asks sellers to be transparent about AI use. If the form asks whether AI/generative tools were used, answer **Yes** — designed by us, AI-assisted. The description already says so (\"WHO MADE IT\").",
              "- **Renewal:** Automatic", "",
              "## Upload these files (Digital files section, in this order)"]
    lines += [f"{i + 1}. `files/{n}`" for i, n in enumerate(files)]
    lines += ["", "## Upload these photos (Photos section, in this order; #1 is the thumbnail)"]
    lines += [f"{i + 1}. `images/{n}`" for i, n in enumerate(imgs)]
    lines += ["", "Shipping: none (digital). Personalization: off. Variations: none."]
    (L / x["slug"] / "listing.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(prefixes):
    jobs_all = []
    todo = [x for x in LS.LISTINGS if not prefixes or any(x["slug"].startswith(p) for p in prefixes)]
    for x in todo:
        spec = SPECS[x["slug"][:2]]
        d = L / x["slug"] / "images"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        htmls = spec(x)
        jobs_all += [(h, d / f"{i + 1:02d}-{x['slug'][3:]}.jpg") for i, h in enumerate(htmls)]
    I.render_all(jobs_all)
    for x in todo:
        listing_md(x)
        print("built", x["slug"], len(list((L / x["slug"] / "images").glob("*.jpg"))), "images")


if __name__ == "__main__":
    main(sys.argv[1:])
