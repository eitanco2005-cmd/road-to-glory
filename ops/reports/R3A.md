# R3A: Seasonal pre-positioning (ws/seasonal)

Pages for three upcoming peaks, built 6–20 weeks early so they have time to rank: **תקציב 2027** (late Dec–Jan), **Purim 2027** (23.3.2027) and **Pesach 2027** (seder 21.4.2027). The build adds 16 new URLs (the sitemap goes from 112 to 128), 2 paid products and 1 bundle, 2 free calculators with WhatsApp share, and 2 free printable PDFs.

## What's built

| Area | URL | What |
|---|---|---|
| Budget 2027 | `budget-2027/` | Hub and main guide. It has 7 steps (HowTo JSON-LD), a 2027 seasonal-expense table computed from the Hebrew calendar, and a "what changes in 2027" table with sources. It links to the 50/30/20, net-salary and savings-goal calculators and to the household-budget 2027 product. |
| | `budget-2027/what-changes-2027/` | Each item is tagged ידוע, צפוי or עוד לא ידוע, with a source per row (see Facts). |
| | `budget-2027/savings-challenge/` + `files/savings-challenge-2027.pdf` | Free PDF, A4, 2 pages: a 52-week challenge with 2027 week dates (total ₪13,780) and a monthly challenge with one money habit per month. |
| Purim | `purim/` | Hub with the dates table and the bundle buy box. |
| | `p/purim-planner/` | **מתכנן משלוחי מנות 2027, ₪19**, xlsx with 7 sheets: recipients (150 rows), package types (8, cost per package computed from the items, "שני מינים" check), shopping list scaled by package counts, delivery route sorted by stop number, מתנות לאביונים + מחצית השקל, and a dashboard with 2 charts. Comes as a blank file and an example file. |
| | `tools/mishloach-manot-budget/` | Free calculator: count and price per group, class kids, matanot l'evyonim, and a budget check. Has the share bar and the tip jar. |
| | 3 guides | `purim/mishloach-manot-ideas/` (ideas by budget), `purim/purim-halacha/` (the 4 mitzvot with שו״ע/רמב״ם sources), `purim/class-mishloach-manot/` (gifts for kindergarten and school classes). |
| Pesach | `pesach/` | Hub with the dates table, the cleaning-checklist download, the bundle, and links to the 4 English Passover pages. |
| | `pesach/cleaning-checklist/` + `files/pesach-cleaning-checklist-2027.pdf` | **Free lead magnet.** 9 areas and 39 tasks, a timeline back from the seder, and a "who does what" table. The page carries the same list as the PDF. |
| | `p/seder-planner/` | **מתכנן ליל הסדר 2027, ₪19**, xlsx with 8 sheets: settings (number of seders, רביעית 86/150 ml, כזיתים, wine share, safety margin), guests, menu, 27 shopping items scaled by head count (formulas for wine, juice and shmurah matzah), haggadah roles, a prep timeline dated from the seder, and a dashboard. Blank file and example file. |
| | `tools/matza-wine-calculator/` | Free calculator: hand matzot, machine-matzah boxes, wine bottles, grape juice and seder shopping lines. Has share and the tip jar, and cites its sources. |
| | 3 guides | `pesach/seder-night-guide/` (hreflang to `en/guides/how-to-host-a-passover-seder/`), `pesach/pesach-2027-dates/`, `pesach/pesach-budget/`. |
| Bundle | `spring-holidays-bundle` | **₪29 for Purim + Pesach planners** (₪38 separately). Buy boxes on both hubs and in the products catalog. |

hreflang pairs added to `docs/data/hreflang.json` (sitemap) and to the Hebrew `<head>`: seder planner ↔ `en/p/passover-seder-planner/`, matza calculator ↔ `en/tools/seder-shopping-calculator/`, seder guide ↔ `en/guides/how-to-host-a-passover-seder/`. English page heads were not edited; the sitemap carries the reciprocal links, as in R2.

## Dates (verified)
`products/seasonal-2027/verify_dates.py` uses the Hanukkah approach (Dershowitz & Reingold arithmetic calendar). It checks itself against RH 5787 = 12.9.2026, Pesach 5786 = 2.4.2026 and Purim 5786 = 3.3.2026, all OK, and it exits non-zero if any page date disagrees.
- 5787 is a leap year, so Purim falls in Adar II. Purim Katan is Sun 21.2.2027.
- Fast of Esther: Mon 22.3. **Purim: Tue 23.3.2027**. Shushan Purim (Jerusalem): Wed 24.3.
- Bedikat chametz: Tue 20.4 evening. Erev Pesach: Wed 21.4. **Seder: Wed 21.4.2027 evening**. First day: Thu 22.4. Shvi'i shel Pesach: Wed 28.4. Last day in the diaspora: Thu 29.4. These match the existing English Passover pages.
- For the budget seasonal table: Shavuot 11.6, Rosh Hashana 2.10 (eve 1.10), Sukkot 16.10, Hanukkah 5788 25.12 (first candle 24.12).

## Facts and sources ("what changes in 2027")
- Tax brackets and credit points: **צפוי**. Indexation is frozen 2025–2027 and resumes in 2028 (Goldfarb Gross Seligman summary of the 2025 law; Tax Authority). The credit point stays at ₪242 a month while the freeze holds; the page says to verify in January.
- VAT: **ידוע**. 18% since 1.1.2025. No change for 2027 had been published as of 18.11.2026.
- Arnona: **צפוי**. +3.05% in January 2027 under the automatic formula (ynet). Councils can request exceptional increases.
- Bituach Leumi / health tax: **לא ידוע**. 2027 thresholds are normally published in January. The page cites the BTL 2026 rates circular.
- Benefits indexation: **לא ידוע**.
- State budget 2027: **לא ידוע**. 2026 is an election year, so a continuing budget is likely and new measures are possible.
- Halachic figures are always given with sources and a "not a ruling, ask a rabbi" line:
  - רביעית 86 ml (R. Chaim Naeh) or 150 ml (Chazon Ish), via the Etzion VBM article.
  - שו״ע או״ח 472 (four cups), 475/477 (matzah), 433:3 (cleaning only where chametz may have been), 687, 689, 694, 695, 697.
  - Rambam, Megillah 2:17.
- Meal quantities and all prices are labeled as rules of thumb or examples.
- Caveat: the source URLs come from web search. The sandbox blocks outbound curl, so I could not open the pages to re-check them.

## Shared files touched (append-only, small)
- `docs/data/products/index.json`: +2 products (events category), +1 bundle.
- `docs/data/tools.json`: +2 tools.
- `docs/data/hreflang.json`: +3 pairs.
- `docs/data/upsell.json`: purim ↔ seder complements.
- `docs/guides/index.html`: new section "חגים ושנה חדשה 2027" with 6 cards.
- `tools/site/e2e_share.js`: +2 cases.
- `tools/site/e2e_test.js`: the hard-coded "home lists 8 tools" check now reads the count from tools.json. It would have broken for any worker adding a tool, including ws/linkbait.
- `ops/STATUS.md`: one TODO line, as the brief asked (see below).
- `python3 tools/site/build_site.py` re-rendered the catalog sections in docs/index.html, docs/products/index.html and docs/tools/index.html.

Everything else lives in new paths: `products/seasonal-2027/**`, `docs/budget-2027/**`, `docs/purim/**`, `docs/pesach/**`, `docs/p/{purim,seder}-planner/**`, `docs/tools/{mishloach-manot-budget,matza-wine-calculator}/**`, `docs/dl/{l9xg51dmh2y8mjd2,h47k3jyddtezfhsk}/`, and `docs/data/products/{purim-planner,seder-planner,spring-holidays-bundle}.json`.

## Decisions
1. **Bundle = Purim + Pesach planners, ₪29.** The brief says "seder planner ₪19 + bundle ₪29" without naming the bundle's contents. Pairing the seder planner with the other spring planner gives the same ₪38→₪29 shape as the Hanukkah bundle. The cleaning checklist stays free as the lead magnet.
2. **The lead magnet is an open download.** There is no email gate, because the site has no list or email infrastructure and the owner rules out outreach. Its job is to bring in traffic and link to the paid planner.
3. **New products appear in the regular catalog now** (index.json, events category), so the home page catalog cards list them. The seasonal home **banner** is deliberately not added. A TODO in ops/STATUS.md says: budget-2027 banner from 2026-12-20, then Purim from about 1.2.2027 and Pesach from about 1.3.2027.
4. **A separate budget-2027 hub instead of editing W3's existing `family-budget-2027` guide.** They overlap, so the hub takes different angles: what changes, the seasonal calendar and the challenge. It links to the W3 guide and does not edit W3's generated pages.
5. **Page shell reused, not forked.** `products/hanukkah/site_common.py` is imported unchanged and its date and CSS are overridden at runtime. Hanukkah's `previews.py` is loaded via importlib.
6. **Halachic quantities are user-chosen settings, not a ruling.** These are the רביעית size, the number of כזיתים, and how many כזיתים fit in one matzah. I found no reliable gram figure for a כזית of matzah, so I didn't publish one.

## Build and tests
- Rebuild everything: `python3 products/seasonal-2027/release.py`, then `python3 tools/site/build_site.py` (sitemap: 128 URLs).
- LibreOffice recalculation (`products/seasonal-2027/qa_recalc.py`) found **0 formula errors** in all 4 workbooks. Checked values:
  - Purim example: 14 recipients, 78 packages, ₪651 + ₪260 matanot and mahatzit = ₪911; route order correct.
  - Seder example: 9 adults + 8 kids gives 21.45 hand matzot, 4 wine bottles and 5 L of juice; shopping total ₪1,931.
- e2e results are below (all at 375px and 1280px where relevant).

| Suite | Checks | Result |
|---|---|---|
| tools/site/e2e_test.js (fastapi + uvicorn installed) | 32 | ALL PASSED (after the tools-count fix above) |
| tools/apps/e2e_apps.js | 111 | ALL PASSED |
| tools/site/e2e_tipskit.js (tip jar now also covers the 2 new calculators) | 94 | ALL PASSED |
| products/en-jewish-life/e2e_en.js | 108 | ALL PASSED |
| products/hanukkah/test_e2e.js | 78 | ALL PASSED |
| tools/site/e2e_share.js (+2 cases) | 171 | ALL PASSED |
| **new** products/seasonal-2027/e2e_seasonal.js | 67 | ALL PASSED |

## Follow-ups (not done)
- After merging to main: run IndexNow (`tools/site/indexnow.py`) for the 16 new URLs.
- 2026-12-20: add the home banner for budget-2027.
- January 2027: update `what-changes-2027` once the BTL 2027 rates and the Tax Authority 2027 tables are published. Each row says when it was last checked.
- Optional: English Purim page; Google Sheets copy links (`sheets_copy_url` is null, the same as the other products).
