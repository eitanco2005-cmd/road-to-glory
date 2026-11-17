#!/usr/bin/env python3
"""Generate the English (LTR, USD) section of the site under docs/en/.

    python3 products/en-jewish-life/site_en.py

Pages: en/ (home), en/planners/, en/p/<slug>/ (4 products), en/tools/ (+3 tools), en/guides/ (+guides from
guides/*.json), en/thanks/, en/legal/{terms,refund,privacy}/. Also writes docs/data/hreflang.json (he<->en pairs,
used by tools/site/build_sitemap.py). Tool page bodies live in tools/<slug>.html (+ .js).
"""
import html
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
DOCS = REPO / "docs"
sys.path.insert(0, str(REPO / "tools" / "site"))
from site_config import BASE_URL  # noqa: E402

BRAND = "Tichnun Plus"
UPDATED = "2026-11-17"
E = lambda s: html.escape("" if s is None else str(s), quote=True)  # noqa: E731

# English page path -> Hebrew counterpart (hreflang + language switch)
HREFLANG = {
    "en/": "",
    "en/planners/": "products/",
    "en/tools/": "tools/",
    "en/guides/": "guides/",
    "en/p/bar-mitzvah-planner/": "p/bar-mitzvah-planner/",
    "en/p/jewish-wedding-planner/": "p/wedding-planner/",
    "en/tools/bar-mitzvah-budget/": "tools/bar-mitzvah-cost/",
    "en/guides/jewish-wedding-checklist/": "guides/wedding-checklist/",
}

ICON = {
    "chart": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/>',
    "people": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "gift": '<path d="M20 12v10H4V12M2 7h20v5H2zM12 22V7M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "check": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "table": '<circle cx="12" cy="12" r="5"/><circle cx="12" cy="3" r="1.5"/><circle cx="12" cy="21" r="1.5"/><circle cx="3" cy="12" r="1.5"/><circle cx="21" cy="12" r="1.5"/>',
    "star": '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "cart": '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15z"/><path d="M8 7h8M8 11h6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8"/>',
}


def svg(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')


def up(path):
    """Relative prefix from docs/<path> (a directory URL like 'en/p/x/') back to docs/."""
    return "../" * path.count("/")


def page(path, title, desc, body, *, crumbs=None, jsonld=None, og_image=None, checkout=False, noindex=False,
         extra_scripts="", og_type="website"):
    u = up(path)
    url = BASE_URL + path
    full_title = title if BRAND in title else f"{title} | {BRAND}"
    alts = ""
    if path in HREFLANG:
        alts = (f'<link rel="alternate" hreflang="en" href="{url}">\n'
                f'<link rel="alternate" hreflang="he" href="{BASE_URL}{HREFLANG[path]}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}{HREFLANG[path]}">\n')
    graph = list(jsonld or [])
    if crumbs:
        items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE_URL + p}
                 for i, (n, p) in enumerate([("Home", "en/")] + crumbs)]
        graph.append({"@type": "BreadcrumbList", "itemListElement": items})
    ld = ""
    if graph:
        ld = ('<script type="application/ld+json">\n' +
              json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1) + "\n</script>\n")
    crumb_html = ""
    if crumbs:
        parts = [f'<a href="{u}en/">Home</a>']
        for n, p in crumbs[:-1]:
            parts.append(f'<a href="{u}{p}">{E(n)}</a>')
        parts.append(f'<span aria-current="page">{E(crumbs[-1][0])}</span>')
        crumb_html = ('<nav class="breadcrumbs" aria-label="Breadcrumb">' + ' <span aria-hidden="true">›</span> '.join(parts)
                      + "</nav>")
    body = body.replace("{{CRUMBS}}", crumb_html).replace("{{UP}}", u)
    og = og_image or "assets/og-default.png"
    robots = '<meta name="robots" content="noindex, nofollow">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
{robots}<link rel="canonical" href="{url}">
{alts}<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e6b63">
<link rel="icon" type="image/svg+xml" href="{u}assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="{u}assets/site.css">
{ld}</head>
<body>
<header id="site-header"></header>
<main id="main">
{body}
</main>
<footer id="site-footer"></footer>
<script src="{u}assets/site.js"></script>
{f'<script src="{u}assets/checkout.js"></script>' + chr(10) if checkout else ""}{extra_scripts}</body>
</html>
"""


def write(path, text):
    f = DOCS / path / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")
    print("wrote", f.relative_to(REPO))


def faq_html(faq):
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{a}</p></details>" for q, a in faq) + "</div>"


def faq_ld(faq):
    import re
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
        for q, a in faq]}


# --------------------------------------------------------------------------- products
COMMON_FAQ = [
    ("Does it work in Google Sheets?",
     "Yes. The file uses only standard formulas (no macros, no add-ins), so it works in Google Sheets: upload it to Google "
     "Drive and open it with Google Sheets. Formatting and charts can look slightly different. That way you can share it "
     "with your partner or family and edit together from any phone."),
    ("What versions of Excel does it need?",
     "Excel 2016 or newer, Excel 365, Excel for Mac and Excel on phones and tablets. It also opens in LibreOffice and Apple "
     "Numbers (some charts may look different in Numbers)."),
    ("How do I get the file?",
     "Right after you pay you land on a download page with the blank planner and a filled-in example. Bookmark that page "
     "to download again later. PayPal also emails you a receipt."),
    ("Do I need a PayPal account?",
     "No. You can pay with any debit or credit card through PayPal's guest checkout, or use your PayPal account if you have one."),
    ("Can I get a refund?",
     "These are instant digital downloads, so we don't refund simply because you changed your mind. But if the file doesn't "
     "open or doesn't work as described and we can't fix it, you get your money back. See the <a href=\"{{UP}}en/legal/refund/\">refund policy</a>."),
]

PRODUCTS = {
    "bar-mitzvah-planner": dict(
        json_slug="bar-mitzvah-planner-en", price=19, short="Bar/Bat Mitzvah Planner",
        title="Bar Mitzvah Planner Spreadsheet: Budget, Guest List & Checklist",
        desc="Bar & bat mitzvah planner for Excel and Google Sheets: budget, vendors, payments, guest list & RSVPs, gifts, "
             "aliyot & candle-lighting, seating, checklist. $19.",
        h1='Bar &amp; Bat Mitzvah Planner: <span class="hl">the whole simcha in one spreadsheet</span>',
        lead="Budget, vendors, guest list, gifts, honors and a timed checklist, in one Excel / Google Sheets file built for "
             "American b'nai mitzvah.",
        points=["Bar and bat mitzvah", "Works in Google Sheets", "No macros", "Filled-in example included"],
        blurb="Track the budget against signed contracts and payments, RSVPs and kids' meals, gifts and thank-you notes, "
              "aliyot and the candle-lighting ceremony, and seating. The dashboard shows where you stand at a glance.",
        shots=["Dashboard: days to go, budget, payments due, RSVPs, gifts and thank-you notes",
               "Budget: suggested split vs planned vs committed vs paid, by category",
               "Guest list: RSVPs, kids, meals, tables, gifts and thank-you tracking",
               "Payments: deposits and installments; overdue in red, due soon in orange",
               "Checklist: 34 tasks with due dates counted back from the date",
               "Honors & candle-lighting: aliyot, ark, hagbah/gelilah and 14 candles"],
        features=[("chart", "Live dashboard", "Days to go, budget vs contracts, what's paid and what's due, RSVPs, gifts received and thank-yous still to write."),
                  ("money", "Budget in 14 categories", "Party venue & catering, kiddush luncheon, DJ/MC & dancers, photo, décor, tutor & synagogue fees, tallit, favors, tzedakah and more, with a suggested split."),
                  ("calendar", "Vendors & payments", "Contracts, deposits and installments with due dates. Overdue payments turn red."),
                  ("people", "Guest list & RSVPs", "Households, sides, groups (school, camp, synagogue), invited vs attending, kids, meals and dietary needs."),
                  ("gift", "Gifts & thank-you notes", "Amount and type (check, cash, Zelle/Venmo, Israel Bond…) and whether the thank-you note went out."),
                  ("star", "Aliyot & candle-lighting", "Who gets each honor at the service and who lights each of the 13 (+1) candles at the party."),
                  ("check", "34-task checklist", "From getting the date and the Torah portion to thank-you notes, with automatic due dates."),
                  ("table", "Seating & day-of schedule", "Table capacity filled from the guest list, plus a run-of-show for service, kiddush and party.")],
        inbox="The planner (blank, ready to fill) and a filled-in example so you can see how everything connects.",
        who="Parents planning a bar or bat mitzvah: a Shabbat service and kiddush, an evening party, a Sunday brunch, or a small "
            "family celebration. Use only the sheets you need and rename any category.",
        faq=[("Does it work for a bat mitzvah too?", "Yes. Every sheet is written for both. Rename or delete anything that doesn't apply, for example the tallit line."),
             ("We're only doing a kiddush luncheon. Is it overkill?", "Not at all. Leave the party categories empty and use the guest list, gifts and checklist. The totals simply ignore empty rows."),
             ("Does it tell me how much to spend?", "No. The suggested % split is a common rule of thumb to start from; real prices depend on your area, guest count and vendors. Our free <a href=\"{{UP}}en/tools/bar-mitzvah-budget/\">budget calculator</a> helps you build a first estimate.")] + COMMON_FAQ,
        related=[("en/tools/bar-mitzvah-budget/", "Free bar mitzvah budget calculator"),
                 ("en/tools/bar-mitzvah-gift/", "How much to give for a bar mitzvah (calculator)"),
                 ("en/guides/bar-mitzvah-planning-timeline/", "Bar mitzvah planning timeline"),
                 ("en/guides/bar-mitzvah-cost/", "How much does a bar mitzvah cost?")]),
    "jewish-wedding-planner": dict(
        json_slug="jewish-wedding-planner", price=24, short="Jewish Wedding Planner",
        title="Jewish Wedding Planner Spreadsheet: Budget, Guests, Ketubah & Chuppah",
        desc="Jewish wedding planner for Excel & Google Sheets: budget, vendors, payments, guest list, ketubah witnesses, "
             "chuppah & sheva brachot honors, checklist, day-of timeline. $24.",
        h1='Jewish Wedding Planner: <span class="hl">from the ketubah to the hora</span>',
        lead="A wedding planning spreadsheet that knows what a Jewish wedding needs: ketubah, witnesses, chuppah, sheva "
             "brachot, tisch, bedeken and yichud, alongside the budget and guest list.",
        points=["Built for Jewish weddings", "Works in Google Sheets", "No macros", "Filled-in example included"],
        blurb="Budget vs contracts vs payments, a guest list with RSVPs, meals and gifts, the ceremony honors (kibbudim), a "
              "36-task checklist and a day-of schedule you can hand to your vendors.",
        shots=["Dashboard: days to go, budget, payments due, RSVPs, honors, gifts",
               "Budget: 14 categories including ketubah, chuppah and officiant",
               "Guest list: sides, RSVPs, meals, tables, gifts and thank-yous",
               "Payments: deposits and installments; overdue in red",
               "Checklist: 36 Jewish wedding tasks with automatic due dates",
               "Ceremony honors: witnesses, ketubah reader, chuppah holders, sheva brachot"],
        features=[("chart", "Live dashboard", "Days to go, budget vs contracts, payments due, RSVPs, honors confirmed and thank-you notes to write."),
                  ("money", "Budget in 14 categories", "Venue & catering, photo, music, flowers & chuppah, ketubah, rings, officiant, aufruf kiddush, sheva brachot meals, tips."),
                  ("calendar", "Vendors & payments", "Deposits and installments with due dates; overdue in red, due soon in orange."),
                  ("people", "Guest list & RSVPs", "Both sides, groups, invited vs attending, meal choices including sealed kosher meals, tables."),
                  ("star", "Ceremony honors", "Ketubah witnesses, kiddushin witnesses, ketubah reader, 4 chuppah holders, 7 sheva brachot, escorts, tisch speakers."),
                  ("check", "36-task Jewish wedding checklist", "Rabbi, date (with a reminder about dates to avoid), ketubah artist, mikveh, license, yichud room."),
                  ("clock", "Day-of schedule", "Tisch, ketubah signing, bedeken, processional, chuppah, glass, yichud, hora, birkat hamazon."),
                  ("gift", "Gifts & thank-you notes", "Registry, checks, honeymoon fund or donations, and who still needs a note.")],
        inbox="The planner (blank, ready to fill) and a filled-in example wedding so you can see how everything connects.",
        who="Couples (and parents) planning a Jewish wedding of any size or movement, including interfaith couples who want "
            "Jewish elements. Every list and category is editable.",
        faq=[("We're not Orthodox. Will it fit us?", "Yes. The honors and checklist cover the common traditions; delete what you don't do and add your own. Your rabbi or officiant decides the details."),
             ("Does it include the ketubah text?", "No. It tracks the ketubah (artist, text choice, witnesses, signing) but the text itself comes from your officiant or ketubah artist."),
             ("Is there a seating chart?", "Yes, a seating helper: type a table number for each guest and it counts seats per table and flags tables over capacity.")] + COMMON_FAQ,
        related=[("en/guides/jewish-wedding-checklist/", "Jewish wedding checklist"),
                 ("en/p/jewish-holiday-planner/", "Jewish Holiday Hosting Planner"),
                 ("en/planners/", "All planners and the Jewish Life Bundle")]),
    "passover-seder-planner": dict(
        json_slug="passover-seder-planner", price=15, short="Passover Seder Planner",
        title="Passover Seder Planner: Shopping List by Guest Count, Menu & Haggadah",
        desc="Passover seder planner for Excel & Google Sheets: guest list for 1 or 2 seders, shopping list that scales with "
             "your head count, menu, haggadah parts, prep timeline. $15.",
        h1='Passover Seder Planner: <span class="hl">a calm seder, enough matzah</span>',
        lead="Guests for one or two seders, a shopping list that scales with your head count, a menu and cooking plan, haggadah "
             "parts for everyone, and a prep timeline counted back from the seder.",
        points=["One or two seders", "Shopping list scales by guests", "Works in Google Sheets", "No macros"],
        blurb="Type who's coming each night and the shopping list recalculates: shmurah and machine matzah, wine and grape "
              "juice, maror, eggs, brisket, soup, dessert, haggadot. Adjust any rate to your family's custom.",
        shots=["Dashboard: people per night, shopping cost, what's left to buy",
               "Shopping list: quantities scale with adults, kids and seder plates",
               "Guests: households, night, RSVP, dietary needs, what they bring",
               "Haggadah parts: the 15 steps plus songs, assigned for each night",
               "Prep timeline: from invitations to burning chametz, with dates"],
        features=[("cart", "Shopping list that scales", "26 items with per-adult, per-child and per-seder-plate rates; packs to buy, on hand and estimated cost."),
                  ("people", "Guests for each night", "Adults and kids, 1st seder, 2nd seder or both, RSVP (count 'maybe' or not), allergies and what they're bringing."),
                  ("book", "Haggadah parts", "Kadesh to Nirtzah plus Ma Nishtana, the Four Children, the plagues, Dayenu and the songs, per night."),
                  ("doc", "Menu & cooking plan", "Dishes, who makes them and how many days ahead; prep dates calculated from the seder date."),
                  ("calendar", "Prep timeline", "17 dated tasks: ordering shmurah matzah, cleaning, selling and burning chametz, cooking ahead."),
                  ("check", "Seder plate checklist", "Every item on the plate and table with what it means, ready to tick off.")],
        inbox="The planner (blank, ready to fill) and a filled-in example with two seders.",
        who="Anyone hosting a seder, from a first-time host with 6 guests to a family hosting 30 across two nights.",
        faq=[("Where do the quantities come from?", "Ritual items start from the per-person guidance Chabad.org publishes (for example 3 matzot per seder plate plus about 2 per other participant per seder). Meal amounts are common catering rules of thumb. Every rate is a yellow cell you can change."),
             ("We only do one seder.", "Set 'Number of seders' to 1 on the Settings sheet and every quantity halves automatically."),
             ("Can I try the numbers first?", "Yes. Our free <a href=\"{{UP}}en/tools/seder-shopping-calculator/\">seder shopping calculator</a> uses the same rates.")] + COMMON_FAQ,
        related=[("en/tools/seder-shopping-calculator/", "Free seder shopping calculator"),
                 ("en/guides/how-to-host-a-passover-seder/", "How to host a Passover seder"),
                 ("en/p/jewish-holiday-planner/", "Jewish Holiday Hosting Planner")]),
    "jewish-holiday-planner": dict(
        json_slug="jewish-holiday-planner", price=15, short="Holiday Hosting Planner",
        title="Jewish Holiday Hosting Planner: Menus, Guests & Shopping for the Year",
        desc="Jewish holiday hosting planner for Excel & Google Sheets: Rosh Hashanah, break-fast, Sukkot, Hanukkah, Purim, "
             "Shavuot & Shabbat guests, menus, shopping, budgets. $15.",
        h1='Jewish Holiday Hosting Planner: <span class="hl">a whole year of hosting, organized</span>',
        lead="Rosh Hashanah dinner, the Yom Kippur break-fast, a meal in the sukkah, the Hanukkah party, the Purim seudah, "
             "Shavuot and Shabbat: guests, menus, shopping and budgets in one file you reuse every year.",
        points=["Rosh Hashanah to Shavuot", "Mishloach manot tracker", "Works in Google Sheets", "No macros"],
        blurb="Plan each holiday meal with its own guest list, menu, shopping list and budget, tick off the traditions "
              "(simanim, sukkah, 44 Hanukkah candles, megillah) and track Purim baskets.",
        shots=["Dashboard: next hosted meal, budget vs shopping, guests per holiday",
               "Holidays: date, hosting, budget, guests, shopping, dishes, traditions done",
               "Guests: who's coming to which holiday, with dietary needs",
               "Traditions: what each holiday needs, ready to tick off",
               "Shopping: items per holiday with quantity × price"],
        features=[("calendar", "Every holiday in one place", "Nine meals out of the box (renameable): Rosh Hashanah ×2, break-fast, Sukkot, Hanukkah, Purim, Shavuot, Shabbat, other."),
                  ("people", "Guests per holiday", "One row per household, a Yes under each holiday they're coming to; counts and servings update."),
                  ("doc", "Menus & cooking plan", "Dishes per holiday, who brings what, make-ahead days and prep dates."),
                  ("cart", "Shopping & budget", "Quantity × price per item and holiday; budget left per meal and for the year."),
                  ("check", "Traditions checklist", "32 essentials: round challah, simanim, lulav & etrog, menorah and candles, megillah times, Shabbat blech."),
                  ("gift", "Mishloach manot tracker", "Purim baskets: who gets one, what's inside, who delivers, plus matanot la'evyonim.")],
        inbox="The planner (blank, ready to fill) and a filled-in example year.",
        who="Families who host holiday meals and want one place for guest lists, menus and shopping, year after year.",
        faq=[("Are the holiday dates included?", "Dates change every year, so you type them in (from your synagogue, Chabad.org or Hebcal). The example file shows dates for 2026–27."),
             ("Can I add other occasions?", "Yes: rename 'Other gathering' or any row on the Holidays sheet, and the guest columns, menus and shopping follow."),
             ("Does it cover Passover?", "Passover has its own, more detailed <a href=\"{{UP}}en/p/passover-seder-planner/\">Seder Planner</a>, included in the Jewish Life Bundle.")] + COMMON_FAQ,
        related=[("en/guides/hosting-rosh-hashanah-dinner/", "Hosting Rosh Hashanah dinner"),
                 ("en/guides/hanukkah-party-planning/", "Hanukkah party planning"),
                 ("en/p/passover-seder-planner/", "Passover Seder Planner")]),
}
ORDER = ["bar-mitzvah-planner", "jewish-wedding-planner", "passover-seder-planner", "jewish-holiday-planner"]
BUNDLE_PRICE, BUNDLE_SUM = 49, sum(PRODUCTS[k]["price"] for k in ORDER)


def shots_html(slug, captions):
    img = DOCS / "en" / "p" / slug / "img"
    figs = []
    for i, cap in enumerate(captions, start=1):
        if not (img / f"screen-{i}.webp").exists():
            continue
        from PIL import Image
        w, h = Image.open(img / f"screen-{i}.png").size
        figs.append(f'<figure><a href="img/screen-{i}.png" target="_blank" rel="noopener"><img src="img/screen-{i}.webp" '
                    f'alt="{E(cap)}" loading="lazy" width="{w}" height="{h}"></a><figcaption>{E(cap)}</figcaption></figure>')
    return "\n".join(figs)


def product_page(slug):
    p = PRODUCTS[slug]
    path = f"en/p/{slug}/"
    feats = "\n".join(f'<div class="feature"><div class="ic">{svg(i)}</div><div><h3>{E(h)}</h3><p>{E(t)}</p></div></div>'
                      for i, h, t in p["features"])
    related = "".join(f'<li><a href="{{{{UP}}}}{u}">{E(t)}</a></li>' for u, t in p["related"])
    body = f"""
<section class="hero">
 <div class="container">
  {{{{CRUMBS}}}}
  <div class="split">
   <div>
    <h1>{p['h1']}</h1>
    <p class="lead">{E(p['lead'])}</p>
   </div>
   <div id="buy" class="buy" data-product="{p['json_slug']}" data-compact="1"></div>
   <div>
    <ul class="hero-points">{''.join(f'<li>{E(x)}</li>' for x in p['points'])}</ul>
    <p class="mt-2">{E(p['blurb'])}</p>
    <p class="small muted">Excel + Google Sheets · ${p['price']} one-time · instant download · <a href="#screens">screenshots ↓</a> · <a href="#inside">what's inside ↓</a></p>
   </div>
  </div>
 </div>
</section>

<section class="section alt" id="screens">
 <div class="container">
  <div class="section-head"><h2>See it in action</h2><p class="muted">Screenshots from the filled-in example file that comes with the planner (names and numbers are made up).</p></div>
  <div class="screens">
{shots_html(slug, p['shots'])}
  </div>
 </div>
</section>

<section class="section" id="inside">
 <div class="container">
  <div class="section-head"><h2>What's inside</h2></div>
  <div class="grid cols-2">
{feats}
  </div>
  <div class="callout mt-3"><strong>You download:</strong> {E(p['inbox'])} One .xlsx file per planner, no macros, US dollars and US date format.</div>
 </div>
</section>

<section class="section alt">
 <div class="container">
  <div class="section-head"><h2>How it works</h2></div>
  <ol class="steps">
   <li><h3>Buy &amp; download</h3><p>Pay with PayPal or any card. Your download page opens right away.</p></li>
   <li><h3>Fill in Settings</h3><p>Date, budget and a few basics. Five minutes, and every sheet connects.</p></li>
   <li><h3>Update as you go</h3><p>Vendors, RSVPs, gifts, tasks. The dashboard keeps itself current.</p></li>
  </ol>
 </div>
</section>

<section class="section">
 <div class="container narrow">
  <h2>Who it's for</h2>
  <p>{E(p['who'])}</p>
  <h2 class="mt-3">Questions</h2>
  {faq_html(p['faq'])}
 </div>
</section>

<section class="section alt">
 <div class="container narrow">
  <div class="cta-box">
   <div><h2 style="font-size:1.25rem">Jewish Life Bundle: all 4 planners</h2>
   <p>Bar/Bat Mitzvah, Jewish Wedding, Passover Seder and Holiday Hosting for ${BUNDLE_PRICE} instead of ${BUNDLE_SUM}.</p></div>
   <div><a class="btn accent" href="{{{{UP}}}}en/planners/#bundle">See the bundle</a></div>
  </div>
  <h2 class="mt-4" style="font-size:1.3rem">Free tools &amp; guides</h2>
  <ul>{related}</ul>
 </div>
</section>

<div class="buy-bar"><span><strong>{E(p['short'])}</strong> · <span class="price">${p['price']}</span></span><a class="btn small" href="#buy">Buy now</a></div>
"""
    imgs = [BASE_URL + f"en/p/{slug}/img/screen-{i}.png" for i in range(1, len(p["shots"]) + 1)
            if (DOCS / "en" / "p" / slug / "img" / f"screen-{i}.png").exists()]
    ld = [{"@type": "Product", "name": p["short"], "description": p["desc"], "sku": p["json_slug"],
           "brand": {"@type": "Brand", "name": BRAND}, "category": "Spreadsheet templates (Excel / Google Sheets)",
           "image": imgs,
           "offers": {"@type": "Offer", "price": str(p["price"]), "priceCurrency": "USD",
                      "availability": "https://schema.org/InStock", "url": BASE_URL + path, "priceValidUntil": "2027-12-31"}},
          faq_ld(p["faq"])]
    write(path, page(path, p["title"], p["desc"], body, crumbs=[("Planners", "en/planners/"), (p["short"], path)],
                     jsonld=ld, og_image=f"en/p/{slug}/img/screen-1.png", checkout=True))


def product_cards(prefix):
    out = []
    for k in ORDER:
        p = PRODUCTS[k]
        out.append(f'<article class="card product-card" data-slug="{p["json_slug"]}"><div class="thumb events">'
                   f'<img src="{prefix}en/p/{k}/img/screen-1.webp" alt="" loading="lazy" width="640" height="360"></div>'
                   f'<div class="body"><h3><a href="{prefix}en/p/{k}/">{E(p["short"])}</a></h3><p class="sub">{E(p["lead"])}</p>'
                   f'<div class="meta"><span class="price">${p["price"]}</span><span class="badge accent">Excel + Google Sheets</span>'
                   f'</div></div></article>')
    return "\n".join(out)


def bundle_box():
    items = "".join(f'<li>{E(PRODUCTS[k]["short"])} <span class="muted num">(${PRODUCTS[k]["price"]})</span></li>' for k in ORDER)
    return f"""<article class="card pad-lg" id="bundle" data-slug="jewish-life-bundle">
 <div class="btn-row" style="justify-content:space-between;align-items:center"><h3 class="mb-0">Jewish Life Bundle: all 4 planners</h3><span class="badge success">Save ${BUNDLE_SUM - BUNDLE_PRICE}</span></div>
 <p class="muted mt-1">Every simcha and every holiday, one purchase. Instant download of all four planners with their examples.</p>
 <ul class="small">{items}</ul>
 <p class="small muted">Instead of <s class="num">${BUNDLE_SUM}</s> separately</p>
 <div class="buy" data-product="jewish-life-bundle" data-compact="1"></div>
</article>"""


TOOLS = [
    ("bar-mitzvah-gift", "🎁", "How much to give for a bar mitzvah", "A suggested gift in multiples of $18 (chai), by how close you are and who's giving"),
    ("bar-mitzvah-budget", "💵", "Bar mitzvah budget calculator", "Estimate the total cost of a bar or bat mitzvah by guests, style and choices"),
    ("seder-shopping-calculator", "🍷", "Passover seder shopping calculator", "How much matzah, wine, maror, eggs, brisket and more for your guest count"),
]


def tool_cards(prefix):
    return "\n".join(f'<a class="card tool-card" href="{prefix}en/tools/{s}/"><span class="ic" aria-hidden="true">{i}</span>'
                     f'<div><h3>{E(t)}</h3><p>{E(d)}</p></div></a>' for s, i, t, d in TOOLS)


def load_guides():
    out = []
    gdir = HERE / "guides"
    for f in sorted(gdir.glob("*.json")) if gdir.exists() else []:
        out.append(json.loads(f.read_text(encoding="utf-8")))
    return out


def guide_cards(prefix, guides):
    return "\n".join(f'<a class="card tool-card" href="{prefix}en/guides/{g["slug"]}/"><span class="ic" aria-hidden="true">📖</span>'
                     f'<div><h3>{E(g["h1"])}</h3><p>{E(short(g["lead"]))}</p></div></a>' for g in guides)


def short(t, n=140):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def home(guides):
    path = "en/"
    body = f"""
<section class="hero">
 <div class="container">
  <span class="eyebrow">Excel &amp; Google Sheets planners</span>
  <h1>Plan the simcha. <span class="hl">Enjoy the simcha.</span></h1>
  <p class="lead">Ready-made spreadsheets for bar and bat mitzvahs, Jewish weddings, the Passover seder and holiday hosting, plus free calculators. Budgets, guest lists, gifts, honors and checklists that do the math for you.</p>
  <div class="btn-row mt-2"><a class="btn" href="planners/">See the planners</a><a class="btn secondary" href="tools/">Free calculators</a></div>
  <ul class="hero-points"><li>Works in Excel &amp; Google Sheets</li><li>No macros, no sign-up</li><li>Instant download</li><li>Secure PayPal or card checkout</li></ul>
 </div>
</section>
<section class="section alt" id="planners">
 <div class="container">
  <div class="section-head"><h2>The planners</h2><p class="muted">Each one comes with a blank planner and a filled-in example.</p></div>
  <div class="grid cols-4">
{product_cards(up(path))}
  </div>
  <div class="mt-3">{bundle_box()}</div>
 </div>
</section>
<section class="section">
 <div class="container">
  <div class="section-head"><h2>Free calculators</h2><p class="muted">Instant answers, nothing to sign up for. Everything runs in your browser.</p></div>
  <div class="grid cols-3">
{tool_cards(up(path))}
  </div>
 </div>
</section>
<section class="section alt">
 <div class="container">
  <div class="section-head"><h2>Guides</h2></div>
  <div class="grid cols-2">
{guide_cards(up(path), guides)}
  </div>
 </div>
</section>
<section class="section">
 <div class="container narrow">
  <h2>Why a spreadsheet?</h2>
  <p>Apps come and go, and most event apps want a subscription. A spreadsheet is yours: it works offline, you can share it with your partner, parents or planner in Google Sheets, and it's still there for the next simcha. Our planners do the math (totals, balances, due dates, RSVP counts) so you only type what you know.</p>
  <p class="muted small">Tichnun Plus is a small independent shop. We also publish Hebrew planners for Israeli families on our <a href="{up(path)}" lang="he" hreflang="he">Hebrew site</a>.</p>
 </div>
</section>
"""
    ld = [{"@type": "WebSite", "name": BRAND, "url": BASE_URL + path, "inLanguage": "en-US"},
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE_URL + f"en/p/{k}/",
                                                     "name": PRODUCTS[k]["short"]} for i, k in enumerate(ORDER)]}]
    write(path, page(path, "Jewish Life Planners for Excel & Google Sheets | Tichnun Plus",
                     "Bar & bat mitzvah, Jewish wedding, Passover seder and holiday hosting planners for Excel and Google "
                     "Sheets, plus free calculators. Instant download, from $15.", body, jsonld=ld, checkout=True))


def planners():
    path = "en/planners/"
    body = f"""
<section class="section">
 <div class="container">
  {{{{CRUMBS}}}}
  <div class="section-head"><h1>Planners</h1><p class="lead muted">Excel and Google Sheets planners for Jewish life. One-time payment in US dollars, instant download, no subscription.</p></div>
  <div class="grid cols-2">
{product_cards(up(path))}
  </div>
  <h2 class="mt-4">Save with the bundle</h2>
  {bundle_box()}
  <div class="callout mt-3"><strong>Every planner includes</strong> a blank file to start from and a filled-in example, works in Excel 2016+ / 365 / Mac / mobile and Google Sheets, and uses only standard formulas (no macros).</div>
 </div>
</section>
"""
    write(path, page(path, "Jewish Life Planners: Bar Mitzvah, Wedding, Seder & Holidays",
                     "All Tichnun Plus planners for Excel & Google Sheets: bar/bat mitzvah ($19), Jewish wedding ($24), "
                     "Passover seder ($15), holiday hosting ($15), or all 4 for $49.", body,
                     crumbs=[("Planners", path)], checkout=True))


def tools_index():
    path = "en/tools/"
    body = f"""
<section class="section">
 <div class="container">
  {{{{CRUMBS}}}}
  <div class="section-head"><h1>Free calculators</h1><p class="lead muted">Quick, private (nothing leaves your browser) and free.</p></div>
  <div class="grid cols-3">
{tool_cards(up(path))}
  </div>
 </div>
</section>"""
    write(path, page(path, "Free Bar Mitzvah & Passover Calculators",
                     "Free calculators: how much to give for a bar mitzvah (chai multiples), bar mitzvah budget, and a "
                     "Passover seder shopping list by number of guests.", body, crumbs=[("Free tools", path)]))


TOOL_META = {
    "bar-mitzvah-gift": dict(
        title="How Much to Give for a Bar Mitzvah? Gift Calculator (Chai)",
        desc="How much money to give for a bar or bat mitzvah: a quick calculator that suggests an amount in multiples of "
             "$18 (chai) based on your relationship and who's giving.",
        name="Bar mitzvah gift calculator", product="bar-mitzvah-planner"),
    "bar-mitzvah-budget": dict(
        title="Bar Mitzvah Budget Calculator: Estimate the Cost",
        desc="Free bar & bat mitzvah budget calculator: estimate the total cost by guest count, kiddush or party, catering "
             "per person, DJ, photo, décor and more. Instant breakdown.",
        name="Bar mitzvah budget calculator", product="bar-mitzvah-planner"),
    "seder-shopping-calculator": dict(
        title="Passover Seder Shopping Calculator: Matzah & Wine per Guest",
        desc="How much matzah, wine, grape juice, maror, eggs, brisket and more to buy for your seder. Enter adults, kids "
             "and seders and get a printable shopping list.",
        name="Passover seder shopping calculator", product="passover-seder-planner"),
}


def tool_page(slug):
    m = TOOL_META[slug]
    path = f"en/tools/{slug}/"
    body_src = (HERE / "tools" / f"{slug}.html").read_text(encoding="utf-8")
    js = (HERE / "tools" / f"{slug}.js").read_text(encoding="utf-8")
    if "__SHOP__" in js:  # seder calculator uses the same rates as the spreadsheet
        sys.path.insert(0, str(HERE))
        import seder
        js = js.replace("__SHOP__", json.dumps([list(r) for r in seder.SHOP]))
    faq = json.loads((HERE / "tools" / f"{slug}.faq.json").read_text(encoding="utf-8"))
    faq = [(x["q"], x["a"]) for x in faq]
    p = PRODUCTS[m["product"]]
    body = body_src.replace("{{FAQ}}", faq_html(faq)).replace(
        "{{CTA}}",
        f'<div class="cta-box"><div><h2 style="font-size:1.2rem">Planning it for real?</h2>'
        f'<p>The {E(p["short"])} turns this into a full plan: {E(p["blurb"][0].lower() + p["blurb"][1:])}</p></div>'
        f'<div><a class="btn accent" href="{{{{UP}}}}en/p/{m["product"]}/">See the planner (${p["price"]})</a></div></div>')
    ld = [{"@type": "SoftwareApplication", "name": m["name"], "applicationCategory": "FinanceApplication"
           if slug != "seder-shopping-calculator" else "LifestyleApplication", "operatingSystem": "Web browser",
           "url": BASE_URL + path, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "inLanguage": "en-US"},
          faq_ld(faq)]
    write(path, page(path, m["title"], m["desc"], body, crumbs=[("Free tools", "en/tools/"), (m["name"], path)], jsonld=ld,
                     extra_scripts=f"<script>\n{js}\n</script>\n"))


def guides_index(guides):
    path = "en/guides/"
    body = f"""
<section class="section">
 <div class="container">
  {{{{CRUMBS}}}}
  <div class="section-head"><h1>Guides</h1><p class="lead muted">Practical, sourced guides for planning Jewish life events and holidays.</p></div>
  <div class="grid cols-2">
{guide_cards(up(path), guides)}
  </div>
 </div>
</section>"""
    write(path, page(path, "Guides: Bar Mitzvah, Jewish Wedding, Passover & Holidays",
                     "Practical guides for planning a bar or bat mitzvah, a Jewish wedding, a Passover seder and holiday "
                     "meals, with sources.", body, crumbs=[("Guides", path)]))


def guide_page(g):
    path = f"en/guides/{g['slug']}/"
    faq = [(x["q"], E(x["a"])) for x in g.get("faq", [])]
    src = "".join(f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["label"])}</a></li>' for s in g.get("sources", []))
    cta = ""
    if g.get("related_product") in PRODUCTS:
        p = PRODUCTS[g["related_product"]]
        cta += (f'<div class="cta-box mt-3"><div><h2 style="font-size:1.2rem">{E(p["short"])}</h2><p>{E(p["lead"])}</p></div>'
                f'<div><a class="btn accent" href="{{{{UP}}}}en/p/{g["related_product"]}/">See the planner (${p["price"]})</a></div></div>')
    tool = next((t for t in TOOLS if t[0] == g.get("related_tool")), None)
    if tool:
        cta += (f'<div class="callout mt-3"><strong>Free tool:</strong> <a href="{{{{UP}}}}en/tools/{tool[0]}/">{E(tool[2])}</a>: '
                f'{E(tool[3])}.</div>')
    others = "".join(f'<li><a href="{{{{UP}}}}en/guides/{o["slug"]}/">{E(o["h1"])}</a></li>' for o in load_guides() if o["slug"] != g["slug"])
    body = f"""
<section class="section">
 <div class="container">
  {{{{CRUMBS}}}}
  <article class="prose">
   <h1>{E(g['h1'])}</h1>
   <p class="updated">Updated {E(g.get('updated', UPDATED))}</p>
   <p class="lead">{E(g['lead'])}</p>
   {g['body_html']}
   {cta}
   {'<h2>Questions</h2>' + faq_html(faq) if faq else ''}
   {'<h2>Sources</h2><ul class="source">' + src + '</ul>' if src else ''}
   <p class="small muted mt-3">General information, not religious, legal or financial advice. Customs vary between communities; ask your rabbi.</p>
   <h2>More guides</h2>
   <ul>{others}</ul>
  </article>
 </div>
</section>"""
    ld = [{"@type": "Article", "headline": g["h1"], "description": g["description"], "inLanguage": "en-US",
           "datePublished": g.get("updated", UPDATED), "dateModified": g.get("updated", UPDATED),
           "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND},
           "mainEntityOfPage": BASE_URL + path}]
    if faq:
        ld.append(faq_ld(faq))
    write(path, page(path, g["title"], g["description"], body, crumbs=[("Guides", "en/guides/"), (g["h1"], path)], jsonld=ld,
                     og_type="article"))


def thanks():
    src = (HERE / "thanks.html").read_text(encoding="utf-8")
    write("en/thanks/", page("en/thanks/", "Thank you: your download", "Your Tichnun Plus download page.", src,
                             noindex=True, extra_scripts=(HERE / "thanks.js").read_text(encoding="utf-8")))


def legal():
    data = json.loads((HERE / "legal.json").read_text(encoding="utf-8"))
    for slug, d in data.items():
        path = f"en/legal/{slug}/"
        body = f"""
<section class="section">
 <div class="container">
  {{{{CRUMBS}}}}
  <article class="prose">
   <h1>{E(d['title'])}</h1>
   <p class="updated">Last updated: November 17, 2026</p>
   {d['body']}
  </article>
 </div>
</section>"""
        write(path, page(path, d["title"], d["desc"], body, crumbs=[(d["title"], path)]))


def main():
    guides = load_guides()
    home(guides)
    planners()
    for k in ORDER:
        product_page(k)
    tools_index()
    for s, *_ in TOOLS:
        tool_page(s)
    guides_index(guides)
    for g in guides:
        guide_page(g)
    thanks()
    legal()
    pairs = [{"en": k, "he": v} for k, v in HREFLANG.items()
             if (DOCS / k / "index.html").exists() and (DOCS / v / "index.html").exists()]
    (DOCS / "data" / "hreflang.json").write_text(json.dumps({"_note": "he<->en page pairs (Stream A). Read by build_sitemap.py.",
                                                             "pairs": pairs}, indent=1) + "\n")
    print(f"hreflang pairs: {len(pairs)}")


if __name__ == "__main__":
    main()
