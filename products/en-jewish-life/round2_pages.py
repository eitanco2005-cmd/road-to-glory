#!/usr/bin/env python3
"""Round 2 per-query English pages (source of truth). Writes guides/*.json and seating/*.json, which site_en.py renders.
    python3 products/en-jewish-life/round2_pages.py
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
UPD = "2026-11-18"
PRINT = '<p class="print-btn"><button type="button" class="btn secondary small" onclick="window.print()">Print this checklist</button></p>'
APP = "{{UP}}en/apps/seating/"


def cl(*items):
    return '<ul class="checklist">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def table(head, rows, caption=None):
    cap = f'<caption class="sr-only">{caption}</caption>' if caption else ""
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table>{cap}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def a(url, text):
    return f'<a href="{url}" rel="noopener" target="_blank">{text}</a>'


SRC = {
    "chiavari": ("Chiavari Chair Sales: Pro table seating guide", "https://chiavarisales.com/pro-table-seating-guide"),
    "prl": ("Party Rental Ltd.: How many people can sit at a table?", "https://help.partyrentalltd.com/how-many-people-can-sit-at-a-table"),
    "designing": ("Designing Idea: Banquet table sizes", "https://designingidea.com/banquet-table-sizes"),
    "efavor": ("Efavormart: Round table sizes and seating", "https://www.efavormart.com/blogs/home/round-table-size-choosing-the-perfect-tablecloth-size-and-seating-for-any-event"),
    "ww": ("WeddingWire: How to create your wedding seating chart", "https://www.weddingwire.com/wedding-ideas/how-to-create-your-wedding-seating-chart"),
    "greenvelope": ("Greenvelope: Wedding seating chart guide", "https://www.greenvelope.com/blog/wedding-seating-chart/"),
    "bridebook": ("Bridebook: How to create a wedding seating chart", "https://bridebook.com/au-en/article/wedding-seating-chart"),
    "paperlust": ("Paperlust: How to make a wedding seating chart", "https://paperlust.co/blog/how-to-make-a-wedding-seating-chart/"),
    "knotmistakes": ("The Knot: Reception seating mistakes to avoid", "https://www.theknot.com/content/reception-seating-mistakes-to-avoid"),
    "prismm": ("Prismm: Bar and bat mitzvah seating ideas", "https://prismm.com/blog/mitzvah-seating-ideas"),
    "pleasantdale": ("Pleasantdale Chateau: Kids' table tips", "https://pleasantdale.com/blog/kids-table-tips/"),
    "mjl_bm": ("My Jewish Learning: Bar/Bat Mitzvah planning", "https://www.myjewishlearning.com/article/barbat-mitzvah-planning/"),
    "mjl_guest": ("My Jewish Learning: What a bar/bat mitzvah guest needs to know", "https://www.myjewishlearning.com/article/what-a-barbat-mitzvah-guest-needs-to-know/"),
    "bash": ("The Bash: Bar/bat mitzvah planning checklist", "https://thebash.com/articles/bar-bat-mitzvah-planning-checklist"),
    "bash_budget": ("The Bash: How much does a bar/bat mitzvah cost?", "https://thebash.com/articles/bar-bat-mitzvah-budget-planner"),
    "nyfamily": ("New York Family: A step-by-step guide to planning a bar or bat mitzvah", "https://www.newyorkfamily.com/a-step-by-step-guide-to-planning-a-bar-or-bat-mitzvah/"),
    "inquirer": ("Philadelphia Inquirer: Bar and bat mitzvah planning, costs and savings (2025)", "https://www.inquirer.com/consumer/bar-bat-mitzvah-planning-cost-budget-savings-philadelphia-20250305.html"),
    "ritualwell": ("Ritualwell: Candle-lighting ceremony for a bat mitzvah", "https://ritualwell.org/ritual/candle-lighting-ceremony-bat-mitzvah/"),
    "chabad_bat": ("Chabad.org: What is a bat mitzvah?", "https://www.chabad.org/1918218"),
    "knot_jw": ("The Knot: Jewish wedding ceremony seating, entrances and exits", "https://www.theknot.com/content/jewish-wedding-ceremony-seating"),
    "chabad_proc": ("Chabad.org: The Jewish wedding processional", "https://www.chabad.org/library/article_cdo/aid/313720/jewish/The-Jewish-Wedding-Processional.htm"),
    "mjl_wed": ("My Jewish Learning: Liturgy, rituals and customs of Jewish weddings", "https://www.myjewishlearning.com/article/liturgy-rituals-customs-of-jewish-weddings/"),
    "rj_wed": ("ReformJudaism.org: 12 things you may see at a Jewish wedding", "https://reformjudaism.org/practice/lifecycle-and-rituals/weddings/12-things-you-may-see-jewish-wedding"),
    "chabad_shop": ("Chabad.org: Seder shopping list", "https://www.chabad.org/holidays/passover/pesach_cdo/aid/867329/jewish/Seder-Shopping-List.htm"),
    "chabad_prep": ("Chabad.org: Seder preparations", "https://www.chabad.org/library/article_cdo/aid/645207/jewish/Seder-Preparations.htm"),
    "rj_seder": ("ReformJudaism.org: Hosting a Passover seder? Use this checklist", "https://www.reformjudaism.org/jewish-holidays/passover/hosting-passover-seder-use-checklist-prepare"),
    "ej_pesach": ("Exploring Judaism: The Passover preparation checklist", "https://www.exploringjudaism.org/?p=14063"),
}


def sources(*keys):
    return [{"label": SRC[k][0], "url": SRC[k][1]} for k in keys]


PAGES = []

# ---------------------------------------------------------------- seating 1: template
PAGES.append(("seating", {
    "slug": "wedding-seating-chart-template",
    "title": "Wedding Seating Chart Template (Free): Guest List, Table Plan & Escort List",
    "description": "A free wedding seating chart template you can copy: the guest-list columns, a filled-in table plan for 120 guests, an A–Z escort list and the checks to run before you print.",
    "h1": "Wedding seating chart template: the three lists you actually need",
    "lead": "A seating chart is really three lists: a guest list with the right columns, a table plan, and an alphabetical escort list for the welcome table. Here is a template for each, with a worked example you can copy.",
    "updated": UPD,
    "related_app": "seating",
    "related_product": "jewish-wedding-planner",
    "more": ["en/guides/jewish-wedding-checklist/", "en/guides/jewish-wedding-processional-order/"],
    "body_html": (
        "<p>Most &ldquo;seating chart templates&rdquo; online are a pretty poster with empty circles. The poster is the last step. What saves you the evening is the data behind it: who is coming, how many seats each invitation takes, and which group they belong to. Get that right and the circles fill themselves in.</p>"
        "<h2>Part 1: the guest list (one row per invitation)</h2>"
        "<p>Start from your RSVP list, not your invitation list. Put one row per invitation (a couple or family is one row) and count seats, so a family of four never gets split by accident.</p>"
        + table(["Column", "What to put in it", "Why it matters"], [
            ["Name", "How the invitation was addressed: &ldquo;Dana &amp; Mike Levi&rdquo;", "This is what goes on the escort card"],
            ["Seats", "Confirmed number of people, including kids", "Table capacity is counted in seats, not names"],
            ["Side", "Partner A / Partner B / Both", "Keeps families near their own side of the room"],
            ["Group", "College friends, Mom&rsquo;s cousins, Work (Partner A)&hellip;", "Groups become tables; this is the single most useful column"],
            ["Needs", "Wheelchair, high chair, near exit, hard of hearing", "Decides which table, not just who sits together"],
            ["Keep apart", "Names of anyone they should not share a table with", "Divorced parents, an ex, a family feud"],
            ["Meal", "Meat / fish / vegan / kids", "Your caterer will ask for counts per table"],
            ["Table", "Leave empty until Part 2", "Filled in when you seat them"],
        ], "Guest list columns") +
        "<p>Tip: write the group as specifically as you can. &ldquo;Friends&rdquo; is useless when you have 60 of them; &ldquo;Partner A&rsquo;s soccer team&rdquo; is a table.</p>"
        "<h2>Part 2: the table plan</h2>"
        "<p>Before you seat anyone, get the floor plan and the table sizes from your venue. As a rule of thumb, rental companies list a 60-inch round at 8&ndash;10 guests and a 72-inch round at 10&ndash;12; most planners treat 8 and 10 as the comfortable numbers (see " + a(SRC["chiavari"][1], "Chiavari Chair Sales") + " and " + a(SRC["prl"][1], "Party Rental Ltd.") + "). Then work table by table:</p>"
        + table(["Table", "Seats", "Who", "Notes"], [
            ["1 (sweetheart or head table)", "2&ndash;12", "The couple, or the couple and the wedding party", "Facing the room, near the dance floor"],
            ["2", "10", "Partner A&rsquo;s parents, siblings, grandparents", "Close to the front; easy path for grandparents"],
            ["3", "10", "Partner B&rsquo;s parents, siblings, grandparents", "Mirror image of table 2"],
            ["4&ndash;5", "10 each", "Aunts, uncles, cousins (by side)", "Seat each branch of the family together"],
            ["6&ndash;9", "10 each", "Friend groups (college, work, childhood)", "One group per table where possible"],
            ["10&ndash;11", "10 each", "Parents&rsquo; friends", "Further from the speakers"],
            ["12", "10", "&ldquo;Mixer&rdquo; table: the people left over", "Put outgoing guests here; it is often the most fun table"],
            ["13 (spare)", "8&ndash;10", "Empty", "For late RSVPs and the plus-one nobody mentioned"],
        ], "Example table plan for 120 guests at 60-inch rounds") +
        "<p>That example seats 120 guests at twelve tables of ten plus a spare. If your venue uses 60-inch rounds and you want room to breathe, plan 15 tables of 8 instead. The math is simple: guests &divide; seats per table, round up, add one.</p>"
        "<h2>Part 3: the escort list (A&ndash;Z)</h2>"
        "<p>Guests look for their own name, not for a table. So the list at the entrance is sorted by last name, one line per invitation, with the table number. This is the list your stationer prints on escort cards or a big display board, and the one the venue coordinator keeps in their pocket.</p>"
        + table(["Name (by last name)", "Table"], [
            ["Abrams, Ruth &amp; David", "4"], ["Cohen, Noa", "7"], ["Friedman family (4)", "5"], ["Levi, Dana &amp; Mike", "8"], ["Shapiro, Grandma Esther", "2"],
        ], "Example escort list") +
        "<p><strong>Escort cards vs. place cards:</strong> escort cards tell guests which <em>table</em>; place cards tell them which <em>seat</em>. Most weddings only need escort cards. Use place cards if you are serving plated meals with different choices, or at the head table.</p>"
        "<h2>Before you print: a 10-minute check</h2>"
        + cl("Every confirmed guest has a table (no one left in &ldquo;unseated&rdquo;).",
             "No table is over capacity, counting kids and high chairs.",
             "Nobody is at a table with someone on their keep-apart list.",
             "Older guests and anyone using a wheelchair are near an aisle and not next to the speakers.",
             "Each table has at least one person who knows most of the others.",
             "Meal counts per table match what you sent the caterer.",
             "The spare table exists and is on the floor plan.",
             "The escort list is alphabetical by last name and matches the table plan.") +
        "<h2>Doing it in a spreadsheet vs. a seating tool</h2>"
        "<p>A spreadsheet is fine for the guest list. It gets painful at the table plan: you are dragging rows around, recounting seats and checking conflicts by eye. Our <a href=\"" + APP + "\">free seating chart maker</a> takes the same columns (paste them from Excel or Google Sheets, or import a CSV or XLSX; headers like Name, Count, Side, Group and Table are detected), lets you drag parties onto round or long tables, auto-seats by group and warns about keep-apart pairs. It runs in your browser and never uploads your guest list. Using it on screen is free; a clean PDF, Excel export and printable table cards are a one-time $9.</p>"
        "<p>Prefer paper? Print this page, use Part 1 as your RSVP sheet, and sketch the table plan on the venue&rsquo;s floor plan. The method is the same.</p>"
    ),
    "faq": [
        {"q": "What should a wedding seating chart template include?", "a": "A guest list with one row per invitation (name, number of seats, side, group, needs, keep-apart, meal), a table plan with capacity per table, and an alphabetical escort list with each party's table number."},
        {"q": "How many guests fit at a round wedding table?", "a": "Rental companies typically list a 60-inch round at 8-10 guests and a 72-inch round at 10-12. Many planners use 8 and 10 as the comfortable numbers. Confirm with your venue, because chair and charger sizes change the answer."},
        {"q": "Should the escort list be sorted by table or by name?", "a": "By last name. Guests look for their own name, so an alphabetical list (name, then table number) is much faster at the entrance. Keep a by-table version for the venue and caterer."},
        {"q": "When should I make the seating chart?", "a": "Draft it once most RSVPs are in, usually 3 to 5 weeks before the wedding, and finalize it after your RSVP deadline so you can give the caterer final counts."},
    ],
    "sources": sources("chiavari", "prl", "greenvelope", "ww"),
}))

# ---------------------------------------------------------------- seating 2: how to
PAGES.append(("seating", {
    "slug": "how-to-make-a-wedding-seating-chart",
    "title": "How to Make a Wedding Seating Chart: 9 Steps (With Examples)",
    "description": "How to make a wedding seating chart step by step: when to start, how to group guests into tables, where family and the wedding party sit, kids, conflicts and the final check.",
    "h1": "How to make a wedding seating chart, step by step",
    "lead": "Seating feels like a puzzle with 150 pieces. It gets much easier when you do it in the right order: the room first, then groups, then the tricky people, then the details.",
    "updated": UPD,
    "related_app": "seating",
    "related_product": "jewish-wedding-planner",
    "more": ["en/guides/jewish-wedding-checklist/", "en/guides/jewish-wedding-processional-order/"],
    "howto": {"name": "How to make a wedding seating chart", "totalTime": "PT3H", "tools": ["Final RSVP list", "Venue floor plan", "Seating chart tool or spreadsheet"],
              "steps": [
                  {"name": "Get the floor plan and table sizes", "text": "Ask the venue for the floor plan, table shapes and how many seats each table really takes.", "anchor": "step-1"},
                  {"name": "Turn RSVPs into parties", "text": "One row per invitation with the number of seats, side and group.", "anchor": "step-2"},
                  {"name": "Seat the couple and the head table", "text": "Decide between a sweetheart table and a head table, and place it first.", "anchor": "step-3"},
                  {"name": "Place the families", "text": "Parents, grandparents and siblings go closest to the couple.", "anchor": "step-4"},
                  {"name": "Fill tables by group", "text": "Turn each friend or family group into a table; split big groups along natural lines.", "anchor": "step-5"},
                  {"name": "Handle the leftovers", "text": "Build mixer tables from guests who don't fit a group, seating each next to someone they know.", "anchor": "step-6"},
                  {"name": "Solve conflicts and special needs", "text": "Separate keep-apart pairs, seat older guests near aisles and away from speakers, decide on kids.", "anchor": "step-7"},
                  {"name": "Check the numbers", "text": "No table over capacity, everyone seated, meal counts match the caterer.", "anchor": "step-8"},
                  {"name": "Make the escort list and send it out", "text": "Print an A-Z list (name to table), send the table plan to the venue and caterer.", "anchor": "step-9"},
              ]},
    "body_html": (
        "<p><strong>When to start:</strong> sketch the room as soon as you have a venue, but do the real chart after most RSVPs are in. Guides differ a little on timing: " + a(SRC["paperlust"][1], "Paperlust") + " suggests a first draft about 5&ndash;6 weeks out, while others wait until the RSVP deadline, 3&ndash;4 weeks before the date. Either way, leave a week before the caterer&rsquo;s final-count deadline.</p>"
        "<h2 id=\"step-1\">1. Get the floor plan and real table sizes</h2>"
        "<p>Ask the venue for a floor plan with the dance floor, bars, buffet, exits and speakers marked, and for the exact table sizes. A 60-inch round is usually listed at 8&ndash;10 guests and a 72-inch round at 10&ndash;12 (" + a(SRC["prl"][1], "Party Rental Ltd.") + "). Ask what <em>they</em> recommend: chargers, chair widths and centerpieces change the answer. See our <a href=\"{{UP}}en/seating/seating-chart-for-round-tables/\">round-table guide</a> for the arithmetic.</p>"
        "<h2 id=\"step-2\">2. Turn your RSVPs into parties</h2>"
        "<p>Make one row per invitation with the number of confirmed seats, the side (yours, theirs, both) and a specific group label. &ldquo;Mom&rsquo;s book club&rdquo; beats &ldquo;friends&rdquo;. If you keep a <a href=\"{{UP}}en/seating/wedding-seating-chart-template/\">guest list in this format</a>, the next steps take minutes.</p>"
        "<h2 id=\"step-3\">3. Place the couple first</h2>"
        "<p>Decide between a <strong>sweetheart table</strong> (just the two of you, both families feel equal) and a <strong>head table</strong> (you plus the wedding party, often with their partners). Put it where everyone can see you and close to the dance floor.</p>"
        "<h2 id=\"step-4\">4. Seat the families closest to you</h2>"
        "<p>Parents, grandparents and siblings get the tables nearest the couple. Many couples give each set of parents their own table so they can host their own relatives and friends. If parents are divorced, two tables at the same distance from you avoid any sense of rank.</p>"
        "<h2 id=\"step-5\">5. Fill tables group by group</h2>"
        "<p>Now the bulk of the work: each group becomes a table. A group of 10 is a table. A group of 14 becomes one table of 8 and one of 6 that you top up with a related group (college friends + their partners, work friends + the plus-ones). Split big groups along lines that already exist, like class year or department, rather than at random.</p>"
        + table(["Group size", "What to do"], [
            ["Fits one table exactly", "Seat it as is"],
            ["A few too many", "Move the couple with the loosest tie to the group to a neighboring, related table"],
            ["A few too few", "Fill with guests who know at least one person there"],
            ["Twice a table or more", "Split along existing lines; place the two tables side by side"],
        ], "Fitting groups to tables") +
        "<h2 id=\"step-6\">6. Build mixer tables from the leftovers</h2>"
        "<p>Every wedding has guests who don&rsquo;t belong to any group: a neighbor, a mentor, a far-flung cousin. Put them together at a mixer table and make sure each has at least one person they know. Seat your most outgoing friends there as hosts.</p>"
        "<h2 id=\"step-7\">7. Solve conflicts and special needs</h2>"
        "<ul><li><strong>Keep-apart pairs:</strong> exes, feuding relatives. Different tables, and not in each other&rsquo;s line of sight if you can help it.</li>"
        "<li><strong>Older guests:</strong> near an aisle and the restrooms, away from the speakers. This is one of the most common seating complaints (" + a(SRC["knotmistakes"][1], "The Knot") + ").</li>"
        "<li><strong>Accessibility:</strong> a wheelchair needs an open spot at the table, not a chair squeezed out.</li>"
        "<li><strong>Kids:</strong> young children usually sit with their parents; a kids&rsquo; table works for older children with a supervising adult nearby (" + a(SRC["bridebook"][1], "Bridebook") + ").</li>"
        "<li><strong>Singles:</strong> don&rsquo;t build a &ldquo;singles table&rdquo;; seat people with friends.</li></ul>"
        "<h2 id=\"step-8\">8. Check the numbers</h2>"
        + cl("Every confirmed guest is seated.", "No table is over capacity (count high chairs).", "Meal choices per table are totaled for the caterer.", "There is one spare table or a few spare seats for surprises.") +
        "<h2 id=\"step-9\">9. Make the escort list and send everything out</h2>"
        "<p>Print an alphabetical list (last name, then table) for escort cards or the display board. Send the table plan with table numbers and meal counts to the venue and caterer, and keep a copy for the day-of coordinator.</p>"
        "<h2>Doing this without index cards on the floor</h2>"
        "<p>The classic method is sticky notes on a poster. It works, but every change means recounting. Our <a href=\"" + APP + "\">free seating chart maker</a> does steps 5&ndash;8 for you: paste the guest list, add round or long tables, press Auto-seat (it keeps groups together and respects keep-apart pairs), then drag to adjust. It runs in your browser and your list is never uploaded. A clean PDF with the table map and A&ndash;Z escort list, Excel export and table cards are a one-time $9; everything else is free.</p>"
        "<div class=\"callout\"><strong>Jewish wedding note:</strong> if you&rsquo;re seating a Jewish wedding, remember the honorees: chuppah pole holders, witnesses and the guests reciting the sheva brachot are often seated near the front so they can step forward quickly. See our <a href=\"{{UP}}en/guides/jewish-wedding-checklist/\">Jewish wedding checklist</a>.</div>"
    ),
    "faq": [
        {"q": "How far in advance should you do a wedding seating chart?", "a": "Draft it when most RSVPs are in, about 3 to 6 weeks before the wedding depending on your RSVP deadline, and finalize it at least a week before the caterer needs final numbers."},
        {"q": "Who sits closest to the couple?", "a": "Parents, grandparents and siblings, then close family and the wedding party's partners. Divorced parents can each host a table at the same distance from the couple."},
        {"q": "Should couples be split up at the wedding?", "a": "No. Keep couples and families together; split groups of friends instead, along natural lines like class year or team."},
        {"q": "What is the fastest way to make a seating chart?", "a": "Group guests by a specific label first, then turn each group into a table. A seating tool with auto-seat and drag-and-drop does most of the arithmetic for you."},
    ],
    "sources": sources("ww", "greenvelope", "bridebook", "paperlust", "knotmistakes", "prl"),
}))

# ---------------------------------------------------------------- seating 3: round tables
PAGES.append(("seating", {
    "slug": "seating-chart-for-round-tables",
    "title": "Seating Chart for Round Tables: How Many Fit + How Many Tables You Need",
    "description": "How many people fit at 48, 60 and 72-inch round tables, how many tables you need for 50 to 250 guests, room space per table, and how to seat round tables without splitting families.",
    "h1": "Seating chart for round tables: capacity, table count and layout",
    "lead": "Round tables are the default at weddings and b'nai mitzvah because everyone can talk to everyone. The catch is the math: how many people actually fit, and how many tables you need.",
    "updated": UPD,
    "related_app": "seating",
    "related_product": "jewish-wedding-planner",
    "more": ["en/guides/jewish-wedding-checklist/"],
    "howto": {"name": "How to plan a seating chart for round tables", "steps": [
        {"name": "Pick the table size", "text": "Choose 60-inch rounds (8-10 guests) or 72-inch rounds (10-12) with your venue.", "anchor": "capacity"},
        {"name": "Count the tables", "text": "Divide confirmed guests by comfortable seats per table, round up and add one spare.", "anchor": "how-many"},
        {"name": "Check the room", "text": "Allow roughly a 10-12 foot square per 60-inch table including chairs and aisles, and confirm with the venue's floor plan.", "anchor": "space"},
        {"name": "Seat parties, not people", "text": "Fill tables with whole couples and families, using 9 or 11 seats where a group doesn't divide evenly.", "anchor": "seating"},
    ]},
    "body_html": (
        "<h2 id=\"capacity\">How many people fit at a round table?</h2>"
        "<p>Published capacity charts agree on the range, and differ on how tight is acceptable. These are the figures rental companies and planners typically use:</p>"
        + table(["Table", "Comfortable", "Maximum (tight)", "Good for"], [
            ["48-inch (4 ft) round", "6", "8", "Small rooms, kids&rsquo; tables, cocktail areas"],
            ["60-inch (5 ft) round", "8", "10", "The standard wedding table"],
            ["66-inch round", "9", "11", "Venues that want 10 without crowding"],
            ["72-inch (6 ft) round", "10", "12", "Big families, fewer tables to fill"],
        ], "Round table capacity") +
        "<p>Sources: " + a(SRC["chiavari"][1], "Chiavari Chair Sales") + " (60-inch comfortably seats 8; 72-inch 10&ndash;12), " + a(SRC["prl"][1], "Party Rental Ltd.") + " (60-inch 8&ndash;10; 72-inch 10&ndash;12) and " + a(SRC["designing"][1], "Designing Idea") + ". Chiavari chairs are narrower than banquet chairs, so venues using them often fit the higher number; big centerpieces and chargers push you toward the lower one. Always ask the venue what they set.</p>"
        "<h2 id=\"how-many\">How many round tables do you need?</h2>"
        "<p><strong>Tables = guests &divide; comfortable seats per table, rounded up, plus one spare.</strong> The spare absorbs late RSVPs and groups that don&rsquo;t divide neatly. Don&rsquo;t count the head or sweetheart table in the division.</p>"
        + table(["Guests", "60&Prime; at 8", "60&Prime; at 10", "72&Prime; at 10", "72&Prime; at 12"], [
            ["50", "7 + 1", "5 + 1", "5 + 1", "5 + 1"],
            ["80", "10 + 1", "8 + 1", "8 + 1", "7 + 1"],
            ["120", "15 + 1", "12 + 1", "12 + 1", "10 + 1"],
            ["150", "19 + 1", "15 + 1", "15 + 1", "13 + 1"],
            ["200", "25 + 1", "20 + 1", "20 + 1", "17 + 1"],
            ["250", "32 + 1", "25 + 1", "25 + 1", "21 + 1"],
        ], "Number of round tables by guest count") +
        "<p>Notice the trade-off: 72-inch tables at 12 save tables (and centerpieces, linens and floor space), but conversation across a 6-foot table is harder. Many couples mix sizes: 72-inch rounds for big family tables, 60-inch for friend groups.</p>"
        "<h2 id=\"space\">How much room do round tables take?</h2>"
        "<p>A seated guest needs roughly 18&ndash;24 inches behind the table edge for the chair and to stand up, and servers need an aisle on top of that. A practical planning figure is a square of about 10&ndash;12 feet per 60-inch table and 11&ndash;13 feet per 72-inch table, including chairs and walkways. That is a rule of thumb only: the venue&rsquo;s floor plan and fire-code capacity are what count, along with the dance floor, the buffet or bar lines and any accessible routes.</p>"
        "<h2 id=\"seating\">Seating round tables without splitting families</h2>"
        "<p>Round tables punish odd numbers. A family of 5 and a couple make 7, which leaves one awkward seat at a table of 8. Some fixes that work:</p>"
        "<ul><li><strong>Seat parties, not people.</strong> Work in invitations (a couple, a family of four) and fill tables with whole parties. Never split a couple to make the numbers work.</li>"
        "<li><strong>Allow 9 or 11.</strong> A 60-inch round set for 9 or a 72-inch set for 11 looks normal and solves most leftovers. Tell the venue the per-table count in advance.</li>"
        "<li><strong>Use the spare table for overflow.</strong> Three couples who know each other loosely make a better table than six seats scattered across the room.</li>"
        "<li><strong>Keep the empty seat away from the dance floor.</strong> If a table has one empty seat, put it where it faces the couple, so nobody sits with their back to the action.</li>"
        "<li><strong>Kids&rsquo; tables can be smaller.</strong> A 48-inch round with 6 kids plus booster seats is easier than squeezing 10 children around a 60-inch table.</li></ul>"
        "<h2>Example: 130 guests on 60-inch rounds</h2>"
        "<p>130 guests &divide; 10 = 13 tables, plus one spare = 14 rounds, and a sweetheart table. In practice, groups won&rsquo;t divide into exact tens, so a typical result looks like: 9 tables of 10, 3 tables of 9, 1 table of 8 and a spare with 5 late RSVPs. That&rsquo;s still 14 rounds, and nobody is split from their partner.</p>"
        "<h2>Round tables vs. long tables</h2>"
        "<p>Long (banquet or farm) tables seat more people in the same floor area and look great for a family-style dinner, but you can only talk to the three or four people near you. Rounds are more social and easier to assign by group. Many venues mix both: a long head table and rounds for everyone else. Our <a href=\"" + APP + "\">seating chart maker</a> supports both round and long tables, shows seats used per table, and auto-seats guests by group so you can try both layouts in a few minutes.</p>"
    ),
    "faq": [
        {"q": "How many people can sit at a 60-inch round table?", "a": "Usually 8 comfortably and up to 10. Rental companies list it at 8-10; venues using slim Chiavari chairs often seat 10."},
        {"q": "How many people fit at a 72-inch round table?", "a": "Usually 10 comfortably and up to 12."},
        {"q": "How many round tables do I need for 150 guests?", "a": "At 10 per 60-inch table, 15 tables plus one spare. At 8 per table, 19 plus a spare. At 12 per 72-inch table, 13 plus a spare."},
        {"q": "Is it OK to have 9 people at a table?", "a": "Yes. Odd counts like 9 or 11 are common and are better than splitting a couple or family. Tell the venue the count per table so place settings match."},
    ],
    "sources": sources("chiavari", "prl", "designing", "efavor"),
}))

# ---------------------------------------------------------------- seating 4: bar mitzvah
PAGES.append(("seating", {
    "slug": "bar-mitzvah-seating-chart",
    "title": "Bar Mitzvah Seating Chart: Kids' Tables, Adults & Candle-Lighting Honorees",
    "description": "How to make a bar or bat mitzvah seating chart: the mitzvah kids' section, younger children, teens and young adults, family tables, candle-lighting honorees, and a sample layout for 150 guests.",
    "h1": "Bar and bat mitzvah seating chart: how to seat kids, teens and adults",
    "lead": "A bar or bat mitzvah party seats two very different crowds: a pack of 13-year-olds who will barely sit down, and adults who came to talk. A good chart plans for both.",
    "updated": UPD,
    "related_app": "seating",
    "related_product": "bar-mitzvah-planner",
    "more": ["en/guides/bar-mitzvah-planning-checklist/", "en/guides/bat-mitzvah-budget-breakdown/", "en/guides/bar-mitzvah-planning-timeline/"],
    "body_html": (
        "<p>The service itself usually needs no chart: synagogue seating is open, and a kiddush lunch after services is often buffet-style. The seating chart is for the party, whether that&rsquo;s Saturday night, Sunday brunch or a luncheon. Here&rsquo;s how to divide the room.</p>"
        "<h2>1. The mitzvah kids&rsquo; section</h2>"
        "<p>The b&rsquo;nai mitzvah&rsquo;s friends are the heart of the party, and they spend most of it on the dance floor. Common set-ups (" + a(SRC["prismm"][1], "Prismm") + "):</p>"
        "<ul><li><strong>A long, U- or E-shaped table</strong> near the dance floor, where the guest of honor sits with friends.</li>"
        "<li><strong>A kids&rsquo; lounge</strong> with open seating: high tables, stools or couches. Many parties skip assigned seats for this group entirely.</li>"
        "<li><strong>Several round tables</strong> grouped together, with friend groups (school, camp, team) at separate tables.</li></ul>"
        "<p>Whichever you choose, keep it close to the DJ and away from the grandparents. Budget kid-friendly food and a kids&rsquo; meal count separately for the caterer.</p>"
        "<h2>2. Younger children</h2>"
        "<p>Children under about 8 usually sit with their parents. If you have many young cousins, a supervised kids&rsquo; table with activity packs works, but put it near the parents&rsquo; tables, not across the room (" + a(SRC["pleasantdale"][1], "Pleasantdale Chateau") + ").</p>"
        "<h2>3. Older teens and young adults</h2>"
        "<p>High-schoolers and college-age cousins rarely want to sit with 13-year-olds, or with their parents. Give them their own table between the kids&rsquo; section and the dance floor. If most of them are cousins, a combined cousins&rsquo; table often works best.</p>"
        "<h2>4. Family and honorees</h2>"
        "<p>Seat grandparents and the immediate family nearest the front, with a clear path to the dance floor and the candle-lighting spot. If you&rsquo;re holding a candle-lighting ceremony (a party custom, typically about 13 candles honoring relatives and friends; see " + a(SRC["ritualwell"][1], "Ritualwell") + "), seat the honorees close enough to come up quickly when called. Keep a list of honorees next to the seating chart so you can check every one of them has a seat near the front.</p>"
        "<h2>5. Adults&rsquo; tables</h2>"
        "<p>The rest is like a wedding: one table per group (synagogue friends, work, neighbors, parents of the mitzvah kids who stay), seated by how well they know each other rather than by importance. Put adults who want to talk furthest from the speakers. For table sizes and counts, see <a href=\"{{UP}}en/seating/seating-chart-for-round-tables/\">round tables</a>.</p>"
        "<h2>Sample layout: 150 guests</h2>"
        + table(["Section", "Guests", "Tables", "Placement"], [
            ["Mitzvah kids (friends)", "45", "1 long E-table or 5 rounds of 9", "Next to the dance floor"],
            ["Teens / young adults / cousins", "12", "1 &times; 72&Prime; round", "Between kids and dance floor"],
            ["Immediate family + grandparents", "20", "2 &times; 60&Prime; rounds", "Front, near the candle-lighting spot"],
            ["Extended family", "30", "3 &times; 60&Prime; rounds", "Front half of the room"],
            ["Family friends, synagogue, work", "40", "4 &times; 60&Prime; rounds", "Back half, away from speakers"],
            ["Young children with parents", "3", "(at their parents&rsquo; tables)", "&mdash;"],
            ["Spare", "&mdash;", "1 &times; 60&Prime; round", "For late RSVPs"],
        ], "Sample bar mitzvah seating layout for 150 guests") +
        "<h2>Seating chart checklist</h2>"
        + cl("Kids&rsquo; RSVPs confirmed separately (they change late).",
             "Kids&rsquo; meal count and any allergies sent to the caterer.",
             "Every candle-lighting honoree has a seat near the front.",
             "Grandparents near an aisle and away from the speakers.",
             "Divorced or separated family members at tables of equal standing.",
             "A chaperone or two seated with or next to the kids&rsquo; section.",
             "Escort cards sorted A&ndash;Z by last name; kids&rsquo; cards in their own section.",
             "Table plan and counts sent to the venue and the DJ (for the candle-lighting order).") +
        "<div class=\"callout warn\"><strong>Shabbat note:</strong> if the party is on Shabbat or the event follows Shabbat customs, prepare everything printed (escort cards, the honorees list) before Shabbat begins, and ask the venue to set them out.</div>"
        "<h2>Build the chart</h2>"
        "<p>Our <a href=\"" + APP + "\">free seating chart maker</a> handles mixed layouts: long tables for the kids, rounds for adults. Paste your guest list with a Group column (Kids &ndash; school, Kids &ndash; camp, Family &ndash; Mom&rsquo;s side&hellip;), press Auto-seat, then drag to adjust and mark keep-apart pairs. Your list stays in your browser. Planning the whole event? The <a href=\"{{UP}}en/p/bar-mitzvah-planner/\">Bar/Bat Mitzvah Planner</a> tracks the guest list, honors, budget and gifts in one spreadsheet.</p>"
    ),
    "faq": [
        {"q": "Do the bar mitzvah kids need assigned seats?", "a": "Often not. Many parties give the mitzvah kids a long table or lounge with open seating near the dance floor, since they spend most of the party dancing. Assign seats if you need to manage friend groups or allergies."},
        {"q": "Where should young children sit at a bar mitzvah?", "a": "Children under about 8 usually sit with their parents. A supervised kids' table near the parents can work if there are many young cousins."},
        {"q": "Where do candle-lighting honorees sit?", "a": "Near the front, close to where the candles are lit, so they can come up quickly when the DJ or emcee calls them."},
        {"q": "How many kids' tables do I need?", "a": "Count kids separately from adults: one long table for the mitzvah kids or rounds of 8-10, plus a table for teens and young adults if you have more than a handful."},
    ],
    "sources": sources("prismm", "pleasantdale", "ritualwell", "mjl_bm", "nyfamily"),
}))

# ---------------------------------------------------------------- guide 5: bar mitzvah planning checklist
PAGES.append(("guides", {
    "slug": "bar-mitzvah-planning-checklist",
    "title": "Bar Mitzvah Planning Checklist (Printable): 12 Months to the Day Of",
    "description": "A printable bar and bat mitzvah planning checklist with tick boxes: 12 months out to the day of, plus the Shabbat-morning and party run sheets and the after-party list.",
    "h1": "Bar and bat mitzvah planning checklist (printable)",
    "lead": "Tick-box checklist from twelve months out to the last thank-you note. Print it, stick it on the fridge, and cross things off. For the reasoning behind each step, see our month-by-month planning timeline.",
    "updated": UPD,
    "related_product": "bar-mitzvah-planner",
    "related_tool": "bar-mitzvah-budget",
    "more": ["en/seating/bar-mitzvah-seating-chart/"],
    "body_html": (
        PRINT +
        "<p>Every synagogue runs its own b&rsquo;nai mitzvah program. Where your synagogue&rsquo;s dates differ from this list, follow the synagogue. Sequences here follow common guidance from " + a(SRC["mjl_bm"][1], "My Jewish Learning") + ", " + a(SRC["bash"][1], "The Bash") + " and " + a(SRC["nyfamily"][1], "New York Family") + "; for the why behind each step, read the <a href=\"{{UP}}en/guides/bar-mitzvah-planning-timeline/\">planning timeline</a>.</p>"
        "<h2>12+ months before</h2>"
        + cl("Date confirmed in writing by the synagogue (Torah portion noted).",
             "B&rsquo;nai mitzvah program requirements, classes and fees understood.",
             "Celebration format chosen: kiddush, evening party, brunch, trip or a mix.",
             "Budget set (try our <a href=\"{{UP}}en/tools/bar-mitzvah-budget/\">budget calculator</a>).",
             "Draft guest list with separate counts for adults and kids.",
             "Venue and caterer booked (if holding a party); kosher requirements checked.",
             "Hotel block considered for out-of-town guests.") +
        "<h2>9&ndash;12 months before</h2>"
        + cl("Tutoring started (per synagogue schedule).",
             "Mitzvah project chosen.",
             "Photographer / videographer booked.",
             "DJ, band or entertainment booked.",
             "Save-the-dates sent to travelers.") +
        "<h2>6&ndash;9 months before</h2>"
        + cl("Decor, florist and theme decided.",
             "Invitation design chosen (print or digital).",
             "Tallit, kippah and other ritual items ordered.",
             "Kippot, favors or swag ordered.",
             "Photo montage: start collecting photos.") +
        "<h2>3&ndash;6 months before</h2>"
        + cl("Honors list: aliyot, ark opening, other synagogue honors (ask who is eligible).",
             "Candle-lighting list drafted (often about 13 candles).",
             "Outfits chosen; fittings booked.",
             "Kiddush or oneg sponsorship arranged with the synagogue.",
             "Transportation for guests or kids arranged, if needed.") +
        "<h2>6&ndash;8 weeks before</h2>"
        + cl("Invitations mailed (earlier for travelers).",
             "RSVP deadline set 3&ndash;4 weeks before the event.",
             "D&rsquo;var Torah draft reviewed with the rabbi or tutor.",
             "Menu tasting and final menu.") +
        "<h2>3&ndash;4 weeks before</h2>"
        + cl("Missing RSVPs chased.",
             "Final headcount (adults / kids) sent to the caterer.",
             "Seating chart done (see <a href=\"{{UP}}en/seating/bar-mitzvah-seating-chart/\">bar mitzvah seating</a>).",
             "Hebrew names of aliyah honorees collected for the rabbi.",
             "Candle-lighting order and music sent to the DJ.") +
        "<h2>1&ndash;2 weeks before</h2>"
        + cl("Rehearsal in the sanctuary.",
             "Vendors confirmed: arrival times, contacts, final payments.",
             "Tip envelopes prepared.",
             "Escort cards and table numbers printed.",
             "Welcome bags for hotel guests packed.") +
        "<h2>The day before</h2>"
        + cl("Speech printed (two copies).",
             "Tallit, kippah, clothes laid out.",
             "Day-of kit: safety pins, stain remover, snacks, phone chargers, pen for the guest book.",
             "Decor and printed items delivered to the venue (before Shabbat, if relevant).") +
        "<h2>The day of: service</h2>"
        + cl("Arrive early; check in with the rabbi and gabbai.",
             "Honorees know their cue and have the blessings text.",
             "Someone assigned to greet guests and hand out kippot.",
             "Photos per synagogue rules (many don&rsquo;t allow photography on Shabbat).") +
        "<h2>The day of: party</h2>"
        + cl("One person (not a parent) is the vendor contact.",
             "Candle-lighting honorees seated near the front.",
             "Gift box or table watched by a trusted person.",
             "Final payments and tips handed out.") +
        "<h2>After</h2>"
        + cl("Every gift logged (name, gift, address).",
             "Thank-you notes written within a few weeks.",
             "Tzedakah from gift money decided with your child.",
             "Thank-yous to the tutor, rabbi and synagogue staff.",
             "Photos backed up; reviews left for vendors.") +
        "<h2>Who owns what</h2>"
        "<p>Checklists stall when everything sits with one parent. A split that works for many families:</p>"
        + table(["Who", "Owns"], [
            ["Bar/bat mitzvah", "Torah and haftarah study, d&rsquo;var Torah, mitzvah project, thank-you notes, candle-lighting rhymes (with help)"],
            ["Parent 1", "Synagogue contact, honors list, Hebrew names, tutor schedule, invitations and RSVPs"],
            ["Parent 2", "Venue, caterer, vendors, budget and payments, seating chart"],
            ["A grandparent or friend", "Out-of-town guests: hotel block, welcome bags, rides"],
            ["Day-of point person (not a parent)", "Vendor arrivals, timeline, tips, gift table"],
        ], "Who owns which tasks") +
        "<p>Put names next to each tick box on your printed copy, and review the list together once a month; ten minutes is enough.</p>"
        "<div class=\"callout\"><strong>Want this as a living list?</strong> The <a href=\"{{UP}}en/p/bar-mitzvah-planner/\">Bar/Bat Mitzvah Planner</a> spreadsheet has a dated checklist that recalculates from your event date, plus budget, guest list, honors and gift tracker.</div>"
    ),
    "faq": [
        {"q": "When should I start planning a bar mitzvah?", "a": "About 12 to 18 months before, once the synagogue confirms the date. Busy venues and vendors in big cities can book out a year or more ahead."},
        {"q": "When do bar mitzvah invitations go out?", "a": "Commonly 6 to 8 weeks before, with save-the-dates months earlier for guests who travel. Set the RSVP deadline 3 to 4 weeks before the event."},
        {"q": "What goes in a day-of kit?", "a": "Two copies of the speech, the tallit and kippah, safety pins, stain remover, snacks, phone chargers, tip envelopes and a pen for the guest book."},
        {"q": "What is the difference between this checklist and the planning timeline?", "a": "The timeline explains each step; this page is the short tick-box version designed to print and carry around."},
    ],
    "sources": sources("mjl_bm", "bash", "nyfamily"),
}))

# ---------------------------------------------------------------- guide 6: bat mitzvah budget breakdown
PAGES.append(("guides", {
    "slug": "bat-mitzvah-budget-breakdown",
    "title": "Bat Mitzvah Budget Breakdown: 3 Sample Budgets With Percentages",
    "description": "A bat mitzvah budget breakdown by category with three worked examples (kiddush lunch, kiddush plus party, big evening party), the percentage each line takes and bat-mitzvah-specific costs to plan for.",
    "h1": "Bat mitzvah budget breakdown: three sample budgets",
    "lead": "Where does the money actually go? Here are three worked bat mitzvah budgets, from a kiddush lunch to a big evening party, with the share each category takes, so you can see what moves the total.",
    "updated": UPD,
    "related_product": "bar-mitzvah-planner",
    "related_tool": "bar-mitzvah-budget",
    "more": ["en/seating/bar-mitzvah-seating-chart/"],
    "body_html": (
        "<p><strong>A word on numbers first.</strong> There is no national survey of bar and bat mitzvah spending. Published &ldquo;averages&rdquo; come from planners and vendors; a 2025 " + a(SRC["inquirer"][1], "Philadelphia Inquirer") + " report quoted a local planner putting even low-key celebrations at roughly $10,000&ndash;$50,000, and vendor sites like " + a(SRC["bash_budget"][1], "The Bash") + " quote similar ranges. The examples below are not averages. They are worked examples built with the starting assumptions of our free <a href=\"{{UP}}en/tools/bar-mitzvah-budget/\">bar/bat mitzvah budget calculator</a> (average-cost US area unless noted), so you can reproduce them and swap in your own quotes.</p>"
        "<h2>Example 1: kiddush luncheon after services, 100 guests</h2>"
        "<p>80 adults and 20 kids, a kiddush lunch at about $25 a head, a photographer (half-day), simple flowers, $900 for outfits.</p>"
        + table(["Category", "Cost", "Share"], [
            ["Kiddush luncheon", "$2,500", "32%"], ["Tutor &amp; synagogue fees", "$1,500", "19%"], ["Kiddush d&eacute;cor &amp; flowers", "$1,000", "13%"],
            ["Photography", "$1,000", "13%"], ["Clothing (family)", "$900", "12%"], ["Contingency (10%)", "$706", "9%"], ["Invitations &amp; postage", "$160", "2%"],
            ["<strong>Total</strong>", "<strong>$7,766</strong>", "about $78 per guest"],
        ], "Kiddush luncheon budget") +
        "<p>With no party, the fixed costs (synagogue fees, clothes, photos) are half the budget. That&rsquo;s why the kiddush format is so much cheaper: there&rsquo;s no venue, bar or entertainment line at all.</p>"
        "<h2>Example 2: kiddush plus Saturday-night party, 120 guests</h2>"
        "<p>85 adults and 35 kids, party catering and bar around $95 per adult (kids at under half), venue rental $2,500, DJ with MC and dancers, photo and video, moderate decor, one attraction, $1,200 for outfits.</p>"
        + table(["Category", "Cost", "Share"], [
            ["Party catering &amp; bar", "$9,571", "30%"], ["Photo &amp; video", "$3,800", "12%"], ["Music &amp; entertainment", "$3,500", "11%"],
            ["Kiddush luncheon", "$3,000", "10%"], ["Contingency (10%)", "$2,860", "9%"], ["Venue rental", "$2,500", "8%"],
            ["D&eacute;cor, flowers &amp; centerpieces", "$2,160", "7%"], ["Tutor &amp; synagogue fees", "$1,500", "5%"], ["Clothing (family)", "$1,200", "4%"],
            ["Extras (photo booth, games)", "$900", "3%"], ["Favors / swag", "$280", "1%"], ["Invitations &amp; postage", "$192", "1%"],
            ["<strong>Total</strong>", "<strong>$31,464</strong>", "about $262 per guest"],
        ], "Kiddush plus party budget") +
        "<h2>Example 3: big evening party in a high-cost city, 175 guests</h2>"
        "<p>120 adults and 55 kids, high-cost metro pricing (about $135 per adult for catering and bar, $5,000 venue), DJ with MC and dancers, photo and video, moderate decor, several attractions, $1,500 for outfits.</p>"
        + table(["Category", "Cost", "Share"], [
            ["Party catering &amp; bar", "$19,541", "39%"], ["Photo &amp; video", "$5,130", "10%"], ["Venue rental", "$5,000", "10%"],
            ["Music &amp; entertainment", "$4,725", "9%"], ["Contingency (10%)", "$4,534", "9%"], ["D&eacute;cor, flowers &amp; centerpieces", "$4,252", "9%"],
            ["Extras (photo booth, games)", "$2,970", "6%"], ["Clothing (family)", "$1,500", "3%"], ["Tutor &amp; synagogue fees", "$1,500", "3%"],
            ["Favors / swag", "$440", "1%"], ["Invitations &amp; postage", "$280", "1%"],
            ["<strong>Total</strong>", "<strong>$49,873</strong>", "about $285 per guest"],
        ], "Evening party budget") +
        "<h2>What the three budgets show</h2>"
        "<ul><li><strong>Food is the biggest line once there&rsquo;s a party</strong> (30&ndash;40%), and it scales with every guest. Cutting 20 adults from Example 3 saves more than dropping the photo booth.</li>"
        "<li><strong>The format matters more than the details.</strong> Going from kiddush to kiddush-plus-party quadruples the budget in these examples.</li>"
        "<li><strong>Region is a multiplier.</strong> The same party in a high-cost metro runs roughly a third more in our assumptions.</li>"
        "<li><strong>Keep a contingency.</strong> Around 10% covers overtime, extra guests and the things nobody budgets for.</li></ul>"
        "<h2>Bat-mitzvah-specific lines to plan for</h2>"
        "<p>Most of a bat mitzvah budget is the same as a bar mitzvah. These are the lines families say they underestimated:</p>"
        + cl("Outfits: many girls have two (service and party), plus alterations.",
             "Hair and makeup for the bat mitzvah girl (and sometimes family) on the day.",
             "Candle-lighting ceremony: candles, a stand or cake, printed rhymes, the DJ&rsquo;s time.",
             "Photo montage or video if not included in the photo/video package.",
             "Shabbat candlesticks or a meaningful gift from the family, a custom in some communities (" + a(SRC["chabad_bat"][1], "Chabad.org") + ").",
             "Tallit, if your community&rsquo;s custom is for girls to wear one.") +
        "<h2>How to build your own breakdown</h2>"
        "<ol><li>Decide the format (kiddush, party or both); it sets 70% of the total.</li>"
        "<li>Count adults and kids separately; kids&rsquo; meals usually cost less.</li>"
        "<li>Get two or three written per-person quotes from caterers, including tax, service charge and kosher supervision if needed.</li>"
        "<li>Plug the quotes into the <a href=\"{{UP}}en/tools/bar-mitzvah-budget/\">budget calculator</a> and adjust each line.</li>"
        "<li>Track actual spending against the plan as deposits go out.</li></ol>"
    ),
    "faq": [
        {"q": "How much does a bat mitzvah cost?", "a": "It ranges from a few thousand dollars for a kiddush lunch to tens of thousands for an evening party. Our worked examples come to about $7,800 for a 100-guest kiddush, $31,500 for a kiddush plus party for 120, and $50,000 for a 175-guest party in a high-cost city."},
        {"q": "What is the biggest expense of a bat mitzvah?", "a": "Food and drink, once there is a party: about 30-40% of the total in our examples. With a kiddush only, synagogue fees, photos and clothing take a larger share."},
        {"q": "How can I cut a bat mitzvah budget?", "a": "Reduce the guest count, choose a kiddush or daytime event instead of an evening party, pick a Sunday or off-peak date, and get competing per-person catering quotes."},
        {"q": "Is a bat mitzvah budget different from a bar mitzvah budget?", "a": "Mostly no. The extra lines families mention are a second outfit, hair and makeup, and the candle-lighting ceremony."},
    ],
    "sources": sources("inquirer", "bash_budget", "mjl_bm", "ritualwell", "chabad_bat"),
}))

# ---------------------------------------------------------------- guide 7: jewish wedding processional order
PAGES.append(("guides", {
    "slug": "jewish-wedding-processional-order",
    "title": "Jewish Wedding Processional Order: Who Walks When, Who Stands Under the Chuppah",
    "description": "The Jewish wedding processional order step by step: who walks first, how both sets of parents escort the couple, who stands under the chuppah, which side guests sit on, and the recessional.",
    "h1": "Jewish wedding processional order: who walks, who stands where",
    "lead": "A Jewish processional looks different from the one most American guests know: both partners are escorted, usually by both parents, and the parents stay under the chuppah. Here is the common order, the variations, and a printable line-up sheet.",
    "updated": UPD,
    "related_product": "jewish-wedding-planner",
    "more": ["en/seating/wedding-seating-chart-template/", "en/seating/how-to-make-a-wedding-seating-chart/"],
    "body_html": (
        "<p>There is no single required order: customs vary between Ashkenazi and Sephardi families, between Orthodox, Conservative and Reform communities, and between families. The order below is the one most American Jewish weddings use, as described by " + a(SRC["knot_jw"][1], "The Knot") + " and " + a(SRC["mjl_wed"][1], "My Jewish Learning") + ". Confirm it with your rabbi, who usually runs the rehearsal.</p>"
        "<h2>Before the processional</h2>"
        "<p>Many couples hold a <em>ketubah</em> signing with the witnesses and a <em>bedeken</em> (veiling), and in more traditional weddings a <em>tisch</em> for the groom, before the ceremony. Guests are seated by then. In many Jewish weddings, the bride&rsquo;s family and friends sit on the <strong>right</strong> side (facing the chuppah) and the groom&rsquo;s on the <strong>left</strong>, the reverse of a typical Christian ceremony (" + a(SRC["knot_jw"][1], "The Knot") + "). Plenty of couples skip sides altogether.</p>"
        "<h2>The processional, in order</h2>"
        "<ol>"
        "<li><strong>Rabbi and/or cantor</strong> take their places under the chuppah (or walk in first).</li>"
        "<li><strong>Grandparents of the bride</strong>, then <strong>grandparents of the groom</strong>; they are seated in the front row. Some families reverse this order so the groom&rsquo;s side goes first throughout.</li>"
        "<li><strong>Groomsmen</strong>, singly or in pairs, then the <strong>best man</strong>.</li>"
        "<li><strong>The groom, escorted by his parents</strong>, one on each side. They walk to the chuppah and the parents stand under or beside it.</li>"
        "<li><strong>Bridesmaids</strong>, then the <strong>maid or matron of honor</strong>.</li>"
        "<li><strong>Ring bearer and flower girl</strong>.</li>"
        "<li><strong>The bride, escorted by her parents</strong>, one on each side. The groom may step forward to meet her before she enters the chuppah.</li>"
        "</ol>"
        "<p>For two grooms or two brides, the same pattern works: each partner is escorted by their parents, and the couple decides who walks first.</p>"
        "<h2>Common variations</h2>"
        + table(["Custom", "What changes"], [
            ["Traditional / Orthodox", "The groom is often escorted by the two fathers and the bride by the two mothers, sometimes carrying candles (" + a(SRC["chabad_proc"][1], "Chabad.org") + "). Men and women may be seated separately."],
            ["Circling", "Under the chuppah the bride may circle the groom seven times (some do three, some circle each other, many skip it)."],
            ["Divorced or remarried parents", "Each partner can walk with one parent at a time, with both parents and a step-parent, or alone; there is no wrong answer."],
            ["Small wedding", "Skip the wedding party; parents escort the couple and everyone else is seated."],
            ["Late parent", "Some couples walk with another close relative, or carry or display something meaningful."],
        ], "Processional variations") +
        "<h2>Who stands under the chuppah?</h2>"
        "<p>Under the canopy: the couple, the officiant(s) and, in most families, both sets of parents. In the most common arrangement the bride stands to the groom&rsquo;s right, with each set of parents on their child&rsquo;s side. Grandparents usually sit in the front row. The wedding party stands beside or behind the chuppah, or sits. Four friends or relatives may hold the poles if the chuppah is hand-held, which is a lovely honor to give (" + a(SRC["rj_wed"][1], "ReformJudaism.org") + ").</p>"
        "<h2>The recessional</h2>"
        "<p>After the glass is broken and the guests shout &ldquo;mazal tov&rdquo;, the order reverses:</p>"
        "<ol><li>The couple (often straight to <em>yichud</em>, a few minutes alone together).</li><li>The bride&rsquo;s parents, then the groom&rsquo;s parents.</li><li>Grandparents.</li><li>Flower girl and ring bearer.</li><li>Wedding party, in pairs.</li><li>Rabbi and/or cantor.</li></ol>"
        "<h2>Printable line-up sheet</h2>"
        + PRINT +
        "<p>Fill in the names, print three copies (coordinator, rabbi, DJ or musicians) and bring one to the rehearsal.</p>"
        + cl("Officiant(s): ____________________",
             "Bride&rsquo;s grandparents: ____________________",
             "Groom&rsquo;s grandparents: ____________________",
             "Groomsmen (in order): ____________________",
             "Best man: ____________________",
             "Groom + escorts: ____________________",
             "Bridesmaids (in order): ____________________",
             "Maid / matron of honor: ____________________",
             "Ring bearer / flower girl: ____________________",
             "Bride + escorts: ____________________",
             "Chuppah pole holders (4): ____________________",
             "Music cue for each entrance: ____________________") +
        "<p>Seating the reception next? Our <a href=\"{{UP}}en/seating/how-to-make-a-wedding-seating-chart/\">step-by-step seating guide</a> and free <a href=\"" + APP + "\">seating chart maker</a> handle the rest, and the <a href=\"{{UP}}en/guides/jewish-wedding-checklist/\">Jewish wedding checklist</a> covers the ketubah, witnesses and honors.</p>"
    ),
    "faq": [
        {"q": "Who walks first in a Jewish wedding processional?", "a": "Usually the rabbi and/or cantor, followed by the grandparents, the wedding party, the groom with his parents, the bridesmaids and flower children, and finally the bride with her parents."},
        {"q": "Do both parents walk the bride down the aisle at a Jewish wedding?", "a": "In most Jewish weddings, yes: each partner is escorted by both parents, who then stand under the chuppah. In some traditional weddings the two fathers escort the groom and the two mothers escort the bride."},
        {"q": "Which side does the bride's family sit on at a Jewish wedding?", "a": "Often the right side facing the chuppah, the reverse of a typical Christian ceremony. Many couples don't assign sides at all."},
        {"q": "Who stands under the chuppah?", "a": "The couple, the officiant and usually both sets of parents. Grandparents sit in the front row and the wedding party stands nearby."},
    ],
    "sources": sources("knot_jw", "chabad_proc", "mjl_wed", "rj_wed"),
}))

# ---------------------------------------------------------------- guide 8: passover seder checklist
PAGES.append(("guides", {
    "slug": "passover-seder-checklist",
    "title": "Passover Seder Checklist (Printable): Seder Plate, Table, Shopping & Timeline",
    "description": "A printable Passover seder checklist: what goes on the seder plate, what to put on the table, a shopping list and a countdown from four weeks out to seder night (Passover 2027 begins April 21).",
    "h1": "Passover seder checklist (printable)",
    "lead": "Everything to tick off before the first seder: the countdown, the seder plate, the table and the shopping list. Passover 2027 begins at sundown on Wednesday, April 21, 2027.",
    "updated": UPD,
    "related_product": "passover-seder-planner",
    "related_tool": "seder-shopping-calculator",
    "more": [],
    "body_html": (
        PRINT +
        "<p>This is the short, printable version. If it&rsquo;s your first seder, read <a href=\"{{UP}}en/guides/how-to-host-a-passover-seder/\">how to host a Passover seder</a> first. Ritual items follow the lists published by " + a(SRC["chabad_shop"][1], "Chabad.org") + "; customs differ between families and communities, so adapt freely and ask your rabbi about anything halachic.</p>"
        "<h2>4&ndash;6 weeks before</h2>"
        + cl("Guest list for each seder (adults / kids), and who brings what.",
             "Haggadot: one per guest, ideally the same edition.",
             "Shmurah matzah ordered (it can sell out close to the holiday).",
             "Menu planned, including any guests&rsquo; dietary needs.",
             "Kosher-for-Passover wine and grape juice listed (see quantities below).",
             "Plan for chametz: what to use up, store or give away.") +
        "<h2>1&ndash;2 weeks before</h2>"
        + cl("Non-perishable shopping done (matzah, wine, matzo meal, canned goods).",
             "Kitchen cleaning plan and dates; kashering plan if you kasher.",
             "Extra chairs, table and pillows (for leaning) borrowed.",
             "Seder roles assigned: Four Questions, readings, afikoman hunt.",
             "Afikoman prize bought.") +
        "<h2>2&ndash;3 days before</h2>"
        + cl("Fresh shopping: romaine, horseradish, parsley, apples, eggs, produce.",
             "Make-ahead cooking: soup, brisket, charoset.",
             "Table linens washed; dishes and glasses counted.") +
        "<h2>The night before</h2>"
        + cl("Search for chametz (<em>bedikat chametz</em>), if you observe it.",
             "Eggs hard-boiled; horseradish grated (keep covered).",
             "Shank bone or chicken neck roasted.",
             "Salt water mixed (about 1&ndash;2 tablespoons of salt in 2 cups of water, per " + a(SRC["chabad_prep"][1], "Chabad.org") + ").") +
        "<h2>The seder plate</h2>"
        + cl("<strong>Zeroa</strong>: roasted shank bone or chicken neck.",
             "<strong>Beitzah</strong>: hard-boiled (often roasted) egg.",
             "<strong>Maror</strong>: bitter herbs, usually horseradish and/or romaine.",
             "<strong>Charoset</strong>: apples, nuts and wine, or your family recipe.",
             "<strong>Karpas</strong>: parsley, celery, onion or boiled potato, by custom.",
             "<strong>Chazeret</strong>: second bitter herb (often romaine).") +
        "<h2>The table</h2>"
        + cl("Three whole matzot, covered, at the leader&rsquo;s place (plus matzah for everyone).",
             "Wine or grape juice for four cups each.",
             "Elijah&rsquo;s cup (and Miriam&rsquo;s cup, if your family uses one).",
             "Salt water bowls within reach of everyone.",
             "A haggadah at every seat.",
             "Pillows for leaning at the leader&rsquo;s seat (or every seat).",
             "Candles lit before the holiday begins.",
             "Bowl, pitcher and towel for hand-washing.",
             "Afikoman wrapped and ready to hide.") +
        "<h2>How much to buy</h2>"
        "<p>Rules of thumb used in our planner (ritual quantities follow Chabad.org&rsquo;s guidance; meal quantities are catering rules of thumb):</p>"
        + table(["Item", "Per adult, per seder", "Notes"], [
            ["Shmurah matzah", "about 2 matzot", "Plus 3 whole matzot per seder plate"],
            ["Wine", "about &frac34; bottle", "Four cups; grape juice for kids and anyone who prefers it"],
            ["Eggs", "1", "Plus one per seder plate"],
            ["Romaine (maror)", "a few leaves", "About one head for 6&ndash;7 adults"],
            ["Brisket (raw)", "about &frac12; lb", "Shrinks a lot in cooking"],
        ], "Passover seder quantities") +
        "<p>For your exact guest count, use the free <a href=\"{{UP}}en/tools/seder-shopping-calculator/\">seder shopping calculator</a>; it turns adults, kids and number of seders into a shopping list you can print.</p>"
        "<h2>Seder night run sheet</h2>"
        + table(["When", "What"], [
            ["Afternoon", "Table set; seder plate assembled; wine and juice chilled; afikoman wrapped"],
            ["1 hour before", "Soup and mains in a low oven; haggadot at each seat; salt water poured"],
            ["Before sundown", "Candles lit at the correct time for your location"],
            ["Arrival", "Guests seated; roles reminded (Four Questions, readings)"],
            ["Kadesh to Maggid", "First cup, karpas, breaking the middle matzah, the story; this is the longest part"],
            ["Motzi-Matzah to Korech", "Matzah, maror, the Hillel sandwich; then serve the meal (Shulchan Orech)"],
            ["After the meal", "Afikoman found and ransomed, grace after meals, third and fourth cups, songs"],
        ], "Seder night run sheet") +
        "<p>Put the soup on the table as soon as Shulchan Orech starts: after an hour of storytelling, hungry guests appreciate speed more than plating.</p>"
        "<h2>After the seder</h2>"
        + cl("Leftover matzah and wine stored for the second seder.",
             "Note what ran out and what was left, for next year.",
             "Haggadot and seder plate packed together.") +
        "<p class=\"small muted\">Also see: " + a(SRC["rj_seder"][1], "ReformJudaism.org&rsquo;s hosting checklist") + " and " + a(SRC["ej_pesach"][1], "Exploring Judaism&rsquo;s preparation checklist") + ".</p>"
    ),
    "faq": [
        {"q": "What goes on a seder plate?", "a": "Zeroa (shank bone or chicken neck), beitzah (egg), maror (bitter herbs), charoset, karpas (a vegetable such as parsley or potato) and, in many families, chazeret (a second bitter herb). Customs vary."},
        {"q": "When is Passover 2027?", "a": "Passover 2027 begins at sundown on Wednesday, April 21, 2027, so the first seder is that evening."},
        {"q": "How much matzah do I need for a seder?", "a": "Chabad.org's guidance is three whole matzot per seder plate plus about two for each other participant, per seder. Buy extra machine matzah for the meal."},
        {"q": "How many bottles of wine for a seder?", "a": "Plan roughly three-quarters of a bottle per adult for the four cups, per seder, plus grape juice for kids."},
    ],
    "sources": sources("chabad_shop", "chabad_prep", "rj_seder", "ej_pesach"),
}))


def main():
    for folder, g in PAGES:
        d = HERE / folder
        d.mkdir(exist_ok=True)
        (d / f"{g['slug']}.json").write_text(json.dumps(g, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("wrote", folder, g["slug"])


if __name__ == "__main__":
    main()
