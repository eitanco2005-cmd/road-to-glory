# Content audit (R6A, 2026-11-22)

All 157 URLs that were in `docs/sitemap.xml` when Google Search Console got the sitemap. I measured them first, then gave each one a decision.
The raw metrics are in `research/content-audit-baseline.json`. Re-run `python3 tools/site/audit_content.py` for the current state. It writes `research/content-audit.json`.

## How it was measured
- **words**: the text inside `<main>` (scripts, svg and comments stripped).
- **dup**: the highest Jaccard similarity of 5-word shingles against any other page, plus that page. A score of 0.15 or more is shown; 0.5 or more counts as a near-duplicate.
- **src**: the number of outbound links to sources (WhatsApp, fonts and PayPal links excluded).
- **tool/checkout**: the page has a form or calculator, or a PayPal buy box.
- **in/out**: internal links in, counted from every docs page, and internal links out.
- **Target query**: the main part of the `<title>`.

## Decision rules
1. **Wedding focus (PLAN §13)**: wedding pages are kept, and the ones that bring in traffic or money are IMPROVEd.
2. **Product pages with a checkout and free calculators are kept indexable.** A tool or a product is unique value no matter the topic.
3. **NOINDEX** (`noindex, follow`, which also drops the page from the sitemap) applies to:
   - pages outside the wedding focus with no tool, data or sources;
   - thin link hubs under about 250 words;
   - near-duplicates;
   - app UI pages that compete with their own landing page for the same query.

   Nothing was deleted except the MERGE pages.
4. **MERGE** (forced 301 in `docs/_redirects`) applies when two of our pages target the same query and one of them clearly wins (it has the calculator). I folded in the content from the merged page that the target was missing. For the wedding budget guide, that was the budget-split table and the "set a ceiling first" steps, which now sit in the cost calculator's `#budget-split` section. The other four targets already covered their guides' content.
5. Substantive pages outside the focus stay KEEP and frozen: the money guides (1,250–1,350 words, 4–5 sources each), the English guides (950–1,450 words, 3–6 sources) and data-il (27 sources).

## Result
| Decision | Pages |
|---|---|
| KEEP | 75 |
| IMPROVE | 39 |
| MERGE (301) | 5 |
| NOINDEX | 38 |
| **Indexable after the audit** | **115** (114 kept or improved + new `about/`) |

How the decisions are enforced: `docs/data/seo.json` holds the noindex list and the redirects. `tools/site/seo_rules.py` applies them on every `build_site.py` run. It adds the meta tag, writes `_redirects` and rewrites internal links that point at merged URLs. `tools/site/seo_check.py` fails the build check if a noindex or redirected page is in the sitemap, or if it finds duplicate titles or descriptions, a wrong canonical, bad JSON-LD, rating markup, images without size or alt, or broken internal links.

What IMPROVE means:
- Every IMPROVE page got a "מי כתב ואיך בדקנו" box (tools/wedding/trust_box.py). It has the date the page was reviewed, a method note written for that page type, the sources policy and a link to `about/`.
- Four pages also got content edits:
  - tools/wedding-gift: all calculator coefficients published, plus a worked example. A couple of friends on a Thursday in the center in summer: 480 × 1.12 × 85% × 2 × 90% ≈ ₪823, which rounds to ₪800. e2e asserts that the calculator gives the same answer.
  - tools/wedding-cost: the budget split merged in from the old guide.
  - chatuna/: a first paragraph that answers both core queries with numbers.
  - guides/wedding-save-money: a stale "60%" claim corrected to 68% from our worked split.

Most wedding pages were already specific (numbers, dated sources, tables), so I didn't rewrite them. I removed no FAQ blocks: each wedding FAQ answers a distinct question, and none repeats the body text word for word.

## Pages
| URL | Target query | Words | Dup (max) | Src | Tool | In/Out | Decision | Why |
|---|---|---|---|---|---|---|---|---|
| `/` | תכנון פלוס | 1108 | 0.18 ↔ `products/` | 0 |  | 114/38 | **KEEP** | hub / unique page |
| `apps/cv/` | בניית קורות חיים בעברית אונליין | 243 | 0.04 | 0 | tool | 3/3 | **NOINDEX** | app UI page (~250–360 words of labels) competes with its own landing page for the same query; landing page stays indexed |
| `apps/invite/` | עיצוב הזמנה אונליין בעברית | 358 | 0.04 | 0 | tool checkout | 7/10 | **NOINDEX** | app UI page (~250–360 words of labels) competes with its own landing page for the same query; landing page stays indexed |
| `apps/rsvp/` | רשימת מוזמנים ואישורי הגעה לחתונה | 466 | 0.01 | 0 | tool | 18/6 | **IMPROVE** | focus page: author/updated/method box |
| `apps/seating/` | סידורי הושבה לחתונה אונליין | 276 | 0.04 | 0 | tool | 11/7 | **NOINDEX** | app UI page (~250–360 words of labels) competes with its own landing page for the same query; landing page stays indexed |
| `budget-2027/` | תקציב 2027 | 950 | 0.22 ↔ `budget-2027/what-changes-2027/` | 6 |  | 3/11 | **KEEP** | substantive (950 words, 6 sources) |
| `budget-2027/savings-challenge/` | אתגר חיסכון 2027 | 391 | 0.02 | 0 |  | 1/5 | **KEEP** | free tool / original asset |
| `budget-2027/what-changes-2027/` | מה משתנה ב-2027 | 547 | 0.22 ↔ `budget-2027/` | 6 |  | 1/1 | **KEEP** | hub / unique page |
| `chatuna/` | הכל לחתונה | 662 | 0.03 | 0 |  checkout | 42/33 | **IMPROVE** | focus page: author/updated/method box; first paragraph now answers both core queries with numbers |
| `chatuna/haavarat-kesef/` | איך לתת כסף בחתונה | 1091 | 0.02 | 4 |  | 13/8 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/kama-lasim/ben-dod/` | כמה לשים בחתונה לבן דוד או בת דודה | 808 | 0.16 ↔ `chatuna/kama-lasim/zug/` | 3 |  | 11/12 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/kama-lasim/chatuna-ktana/` | כמה לשים בחתונה קטנה, בוטיק או במסעדה | 765 | 0.15 ↔ `chatuna/kama-lasim/makom-yukrati/` | 3 |  | 9/12 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/kama-lasim/gan-eruim/` | כמה לשים בחתונה בגן אירועים | 845 | 0.15 ↔ `chatuna/kama-lasim/chatuna-ktana/` | 3 |  | 10/12 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/kama-lasim/lo-magiim/` | כמה לשים בחתונה אם לא מגיעים | 796 | 0.15 ↔ `chatuna/kama-lasim/tzafon-darom/` | 3 |  | 10/12 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/kama-lasim/makom-yukrati/` | כמה לשים בחתונה במקום יוקרתי | 763 | 0.16 ↔ `chatuna/kama-lasim/yom-shishi/` | 3 |  | 9/12 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/kama-lasim/tzafon-darom/` | כמה לשים בחתונה בצפון, בדרום ובירושלים | 738 | 0.16 ↔ `chatuna/kama-lasim/yom-shishi/` | 3 |  | 9/12 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/kama-lasim/yom-shishi/` | כמה לשים בחתונה ביום שישי | 734 | 0.16 ↔ `chatuna/kama-lasim/tzafon-darom/` | 3 |  | 10/12 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/kama-lasim/zug/` | כמה לשים בחתונה בזוג | 756 | 0.16 ↔ `chatuna/kama-lasim/ben-dod/` | 3 |  | 12/12 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/ma-lilbosh/` | מה ללבוש לחתונה | 899 | 0.03 | 0 |  | 13/6 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/` | מחירון ספקים לחתונה 2026 | 769 | 0.03 | 0 |  | 18/16 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/chalifat-chatan/` | מחיר חליפת חתן 2026 | 523 | 0.20 ↔ `chatuna/mechirim/ipur-kala/` | 2 |  | 10/14 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/dj/` | מחיר DJ לחתונה 2026 | 789 | 0.17 ↔ `chatuna/mechirim/chalifat-chatan/` | 8 |  | 12/15 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/hasaot/` | מחיר הסעות לחתונה 2026 | 761 | 0.13 | 5 |  | 10/15 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/ipur-kala/` | מחיר איפור ושיער לכלה 2026 | 676 | 0.20 ↔ `chatuna/mechirim/chalifat-chatan/` | 4 |  | 10/15 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/itzuv-prachim/` | מחיר עיצוב ופרחים לחתונה 2026 | 736 | 0.17 ↔ `chatuna/mechirim/chalifat-chatan/` | 6 |  | 10/16 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/magnetim/` | מחיר צלם מגנטים לחתונה 2026 | 646 | 0.19 ↔ `chatuna/mechirim/chalifat-chatan/` | 3 |  | 10/15 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/rav/` | מחיר רב לחתונה 2026 | 749 | 0.12 | 3 |  | 11/15 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/simlat-kala/` | מחיר שמלת כלה 2026 | 822 | 0.18 ↔ `chatuna/mechirim/ipur-kala/` | 9 |  | 12/15 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/tzalam/` | מחיר צלם לחתונה 2026 | 843 | 0.17 ↔ `chatuna/mechirim/chalifat-chatan/` | 7 |  | 12/16 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/mechirim/ulam/` | מחיר מנה באולם וגן אירועים 2026 | 1063 | 0.13 | 4 |  | 12/16 | **IMPROVE** | focus page: author/updated/method box |
| `chatuna/rayonot-matana/` | רעיונות למתנה לחתונה | 832 | 0.03 | 0 |  | 11/6 | **IMPROVE** | focus page: author/updated/method box |
| `data-il/` | נתונים פתוחים על ישראל | 1322 | 0.00 | 27 |  | 4/17 | **KEEP** | substantive (1322 words, 27 sources) |
| `devkit/` | RTL Landing Kit | 567 | 0.00 | 1 |  checkout | 1/10 | **KEEP** | product page with checkout |
| `devkit/demos/templates/launch/` | Mivne | 249 | 0.89 ↔ `devkit/demos/templates/launch/tailwind.html` | 0 | tool | 1/0 | **NOINDEX** | demo template of the RTL kit (fictional brand copy); tailwind twin is 80–100% identical |
| `devkit/demos/templates/launch/tailwind.html` | Mivne | 264 | 0.89 ↔ `devkit/demos/templates/launch/` | 0 | tool | 1/0 | **NOINDEX** | demo template of the RTL kit (fictional brand copy); tailwind twin is 80–100% identical |
| `devkit/demos/templates/pocket/` | כיס | 162 | 1.00 ↔ `devkit/demos/templates/pocket/tailwind.html` | 0 | tool | 1/0 | **NOINDEX** | demo template of the RTL kit (fictional brand copy); tailwind twin is 80–100% identical |
| `devkit/demos/templates/pocket/tailwind.html` | כיס | 165 | 1.00 ↔ `devkit/demos/templates/pocket/` | 0 | tool | 1/0 | **NOINDEX** | demo template of the RTL kit (fictional brand copy); tailwind twin is 80–100% identical |
| `devkit/demos/templates/studio/` | סטודיו גלים | 162 | 0.80 ↔ `devkit/demos/templates/studio/tailwind.html` | 0 | tool | 1/0 | **NOINDEX** | demo template of the RTL kit (fictional brand copy); tailwind twin is 80–100% identical |
| `devkit/demos/templates/studio/tailwind.html` | סטודיו גלים | 166 | 0.80 ↔ `devkit/demos/templates/studio/` | 0 | tool | 1/0 | **NOINDEX** | demo template of the RTL kit (fictional brand copy); tailwind twin is 80–100% identical |
| `embed/` | מחשבונים להטמעה באתר | 676 | 0.04 | 0 |  | 12/12 | **KEEP** | hub / unique page |
| `en/` | Jewish Life Planners for Excel & Google Sheets | 672 | 0.27 ↔ `en/guides/` | 0 |  checkout | 32/17 | **KEEP** | hub / unique page |
| `en/apps/seating/` | Free Wedding Seating Chart Maker | 577 | 0.01 | 0 | tool | 6/6 | **KEEP** | hub / unique page |
| `en/embed/` | Free embeddable Jewish holiday & simcha calculators | 463 | 0.04 | 0 |  | 7/8 | **KEEP** | hub / unique page |
| `en/guides/` | Guides | 384 | 0.27 ↔ `en/` | 0 |  | 11/13 | **KEEP** | hub / unique page |
| `en/guides/bar-mitzvah-cost/` | How Much Does a Bar Mitzvah Cost | 1372 | 0.07 | 4 |  | 13/14 | **KEEP** | substantive (1372 words, 4 sources) |
| `en/guides/bar-mitzvah-planning-checklist/` | Bar Mitzvah Planning Checklist (Printable) | 957 | 0.08 | 3 |  | 12/15 | **KEEP** | substantive (957 words, 3 sources) |
| `en/guides/bar-mitzvah-planning-timeline/` | Bar Mitzvah Planning Timeline | 1315 | 0.07 | 4 |  | 14/13 | **KEEP** | substantive (1315 words, 4 sources) |
| `en/guides/bat-mitzvah-budget-breakdown/` | Bat Mitzvah Budget Breakdown | 1078 | 0.08 | 5 |  | 12/15 | **KEEP** | substantive (1078 words, 5 sources) |
| `en/guides/hanukkah-party-planning/` | Hanukkah Party Planning | 1298 | 0.05 | 5 |  | 13/13 | **KEEP** | substantive (1298 words, 5 sources) |
| `en/guides/hosting-rosh-hashanah-dinner/` | Hosting Rosh Hashanah Dinner | 1353 | 0.05 | 6 |  | 13/13 | **KEEP** | substantive (1353 words, 6 sources) |
| `en/guides/how-to-host-a-passover-seder/` | How to Host a Passover Seder | 1449 | 0.07 | 6 |  | 14/14 | **KEEP** | substantive (1449 words, 6 sources) |
| `en/guides/jewish-wedding-checklist/` | Jewish Wedding Checklist | 1424 | 0.06 | 6 |  | 16/13 | **KEEP** | substantive (1424 words, 6 sources) |
| `en/guides/jewish-wedding-processional-order/` | Jewish Wedding Processional Order | 1004 | 0.06 | 4 |  | 13/16 | **KEEP** | substantive (1004 words, 4 sources) |
| `en/guides/passover-seder-checklist/` | Passover Seder Checklist (Printable) | 954 | 0.07 | 4 |  | 12/14 | **KEEP** | substantive (954 words, 4 sources) |
| `en/guides/why-gifts-in-multiples-of-18/` | Why Jews Give Gifts in Multiples of 18 (Chai) | 1466 | 0.04 | 6 |  | 12/13 | **KEEP** | substantive (1466 words, 6 sources) |
| `en/hanukkah/` | Hanukkah 2026 | 233 | 0.09 | 0 |  checkout | 8/7 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `en/hanukkah/activity-pack/` | Hanukkah Activity Pack 2026 | 433 | 0.01 | 0 |  checkout | 3/6 | **KEEP** | product page with checkout |
| `en/hanukkah/how-to-play-dreidel/` | How to Play Dreidel | 362 | 0.01 | 0 |  | 2/2 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `en/hanukkah/latke-calculator/` | How Many Latkes Per Person | 365 | 0.02 | 0 | tool | 5/4 | **KEEP** | hub / unique page |
| `en/hanukkah/party-planner/` | Hanukkah Party Planner Spreadsheet | 403 | 0.02 | 0 |  checkout | 3/3 | **KEEP** | product page with checkout |
| `en/hanukkah/terms/` | Terms of Sale & Refund Policy | 209 | 0.01 | 0 |  | 3/2 | **NOINDEX** | duplicate of en/legal/terms |
| `en/hanukkah/when-is-hanukkah-2026/` | When Is Hanukkah 2026 | 599 | 0.09 | 0 |  | 3/2 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `en/legal/privacy/` | Privacy policy | 346 | 0.03 | 0 |  | 1/1 | **KEEP** | legal/trust page |
| `en/legal/refund/` | Refund policy | 232 | 0.03 | 0 |  | 7/1 | **KEEP** | legal/trust page |
| `en/legal/terms/` | Terms of sale | 302 | 0.03 | 0 |  | 0/3 | **KEEP** | legal/trust page |
| `en/p/bar-mitzvah-planner/` | Bar Mitzvah Planner Spreadsheet | 828 | 0.29 ↔ `en/p/jewish-wedding-planner/` | 0 |  checkout | 9/13 | **KEEP** | product page with checkout |
| `en/p/jewish-holiday-planner/` | Jewish Holiday Hosting Planner | 697 | 0.30 ↔ `en/p/passover-seder-planner/` | 0 |  checkout | 6/11 | **KEEP** | product page with checkout |
| `en/p/jewish-wedding-planner/` | Jewish Wedding Planner Spreadsheet | 763 | 0.29 ↔ `en/p/bar-mitzvah-planner/` | 0 |  checkout | 7/11 | **KEEP** | product page with checkout |
| `en/p/passover-seder-planner/` | Passover Seder Planner | 733 | 0.30 ↔ `en/p/jewish-holiday-planner/` | 0 |  checkout | 8/11 | **KEEP** | product page with checkout |
| `en/planners/` | Jewish Life Planners | 248 | 0.25 ↔ `en/` | 0 |  checkout | 5/5 | **NOINDEX** | thin hub (96–248 words) that only lists links; children stay indexed |
| `en/seating/` | Seating Chart Guides | 188 | 0.04 | 0 |  | 5/6 | **NOINDEX** | thin hub (96–248 words) that only lists links; children stay indexed |
| `en/seating/bar-mitzvah-seating-chart/` | Bar Mitzvah Seating Chart | 1061 | 0.04 | 5 |  | 7/10 | **KEEP** | substantive (1061 words, 5 sources) |
| `en/seating/how-to-make-a-wedding-seating-chart/` | How to Make a Wedding Seating Chart | 1164 | 0.06 | 6 |  | 6/9 | **KEEP** | substantive (1164 words, 6 sources) |
| `en/seating/seating-chart-for-round-tables/` | Seating Chart for Round Tables | 1072 | 0.06 | 4 |  | 5/8 | **KEEP** | substantive (1072 words, 4 sources) |
| `en/seating/wedding-seating-chart-template/` | Wedding Seating Chart Template (Free) | 1279 | 0.06 | 4 |  | 6/9 | **KEEP** | substantive (1279 words, 4 sources) |
| `en/tools/` | Free Bar Mitzvah & Passover Calculators | 96 | 0.08 | 0 |  | 5/6 | **NOINDEX** | thin hub (96–248 words) that only lists links; children stay indexed |
| `en/tools/bar-mitzvah-budget/` | Bar Mitzvah Budget Calculator | 685 | 0.04 | 2 | tool | 8/4 | **KEEP** | free tool / original asset |
| `en/tools/bar-mitzvah-gift/` | How Much to Give for a Bar Mitzvah | 735 | 0.04 | 3 | tool | 6/4 | **KEEP** | free tool / original asset |
| `en/tools/seder-shopping-calculator/` | Passover Seder Shopping Calculator | 599 | 0.02 | 2 | tool | 9/4 | **KEEP** | free tool / original asset |
| `guides/` | מדריכים | 586 | 0.02 | 0 |  | 13/29 | **KEEP** | hub / unique page |
| `guides/budget-by-net-salary/` | תקציב לפי משכורת נטו | 1265 | 0.02 | 4 |  | 9/9 | **KEEP** | substantive (1265 words, 4 sources) |
| `guides/couple-money/` | ניהול כסף בזוגיות | 1280 | 0.02 | 4 |  | 3/7 | **KEEP** | substantive (1280 words, 4 sources) |
| `guides/emergency-fund/` | קרן חירום | 1277 | 0.02 | 5 |  | 7/8 | **KEEP** | substantive (1277 words, 5 sources) |
| `guides/expense-tracking/` | מעקב הוצאות | 1248 | 0.02 | 4 |  | 5/9 | **KEEP** | substantive (1248 words, 4 sources) |
| `guides/get-out-of-overdraft/` | איך לצאת מהמינוס | 1245 | 0.02 | 5 |  | 6/7 | **KEEP** | substantive (1245 words, 5 sources) |
| `guides/how-to-save-money/` | איך לחסוך כסף ב-2027 | 1347 | 0.02 | 5 |  | 8/7 | **KEEP** | substantive (1347 words, 5 sources) |
| `guides/open-osek-patur/` | איך פותחים עוסק פטור ב-2026 | 1281 | 0.02 | 5 |  | 2/7 | **KEEP** | substantive (1281 words, 5 sources) |
| `guides/savings-goal-plan/` | איך לחסוך למטרה | 1258 | 0.02 | 4 |  | 7/7 | **KEEP** | substantive (1258 words, 4 sources) |
| `guides/wedding-checklist/` | צ'קליסט חתונה | 1386 | 0.04 | 4 |  | 10/13 | **IMPROVE** | focus page: author/updated/method box |
| `guides/wedding-guest-list/` | רשימת מוזמנים לחתונה | 1360 | 0.03 | 4 |  | 10/10 | **IMPROVE** | focus page: author/updated/method box |
| `guides/wedding-save-money/` | איך לחסוך בחתונה | 1301 | 0.04 | 5 |  | 15/12 | **IMPROVE** | focus page: author/updated/method box; fixed stale 60% claim → 68% from our worked split, linked |
| `guides/wedding-vendor-contracts/` | חוזה עם אולם אירועים | 1346 | 0.04 | 5 |  | 14/10 | **IMPROVE** | focus page: author/updated/method box |
| `hanukkah/` | חנוכה 2026 | 207 | 0.12 | 0 |  checkout | 8/7 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `hanukkah/hanukkah-2026-dates/` | חנוכה 2026 | 434 | 0.12 | 0 |  | 3/2 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `hanukkah/hanukkah-party/` | איך מארגנים מסיבת חנוכה | 361 | 0.01 | 0 |  | 3/3 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `hanukkah/kids-activities/` | פעילויות לחנוכה לילדים | 410 | 0.00 | 0 |  | 2/3 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `legal/` | מידע משפטי | 28 | 0.00 | 0 |  | 4/4 | **NOINDEX** | 28-word link hub |
| `legal/accessibility/` | הצהרת נגישות | 234 | 0.00 | 0 |  | 1/1 | **KEEP** | legal/trust page |
| `legal/privacy/` | מדיניות פרטיות | 341 | 0.03 | 0 |  | 3/1 | **KEEP** | legal/trust page |
| `legal/refund/` | מדיניות ביטולים והחזרים | 313 | 0.03 | 0 |  | 11/1 | **KEEP** | legal/trust page |
| `legal/terms/` | תקנון ותנאי מכירה | 453 | 0.02 | 0 |  | 3/3 | **KEEP** | legal/trust page |
| `p/bar-mitzvah-planner/` | מתכנן בר מצווה / בת מצווה באקסל | 635 | 0.23 ↔ `p/wedding-planner/` | 0 |  checkout | 8/15 | **KEEP** | product page with checkout |
| `p/bar-mitzvah-planner/guides/bar-mitzvah-cost-2026/` | כמה עולה בר מצווה ב-2026 | 429 | 0.04 | 2 |  | 7/5 | **MERGE** | same intent as tools/bar-mitzvah-cost/ (which has the calculator/fuller page); 301 |
| `p/bar-mitzvah-planner/guides/bar-mitzvah-timeline/` | לוח זמנים להכנת בר / בת מצווה | 342 | 0.04 | 0 |  | 7/4 | **NOINDEX** | off-focus short guide (<570 words, no/thin sources) with no tool or data |
| `p/cv-builder/` | בניית קורות חיים בעברית ובאנגלית | 620 | 0.04 | 0 |  checkout | 5/11 | **KEEP** | product page with checkout |
| `p/cv-builder/guides/cv-in-english/` | קורות חיים באנגלית לישראלים | 626 | 0.01 | 0 |  | 4/3 | **NOINDEX** | generic CV advice, no sources, off-focus, saturated query |
| `p/cv-builder/guides/how-to-write-cv/` | איך כותבים קורות חיים בעברית (2026) | 615 | 0.01 | 0 |  | 4/3 | **NOINDEX** | generic CV advice, no sources, off-focus, saturated query |
| `p/hanukkah-activity-pack/` | חבילת פעילויות לחנוכה 2026 | 365 | 0.01 | 0 |  checkout | 3/5 | **KEEP** | product page with checkout |
| `p/hanukkah-party-planner/` | מתכנן מסיבת חנוכה באקסל | 373 | 0.09 | 0 |  checkout | 4/4 | **KEEP** | product page with checkout |
| `p/household-budget/` | אקסל תקציב משק בית 2027 | 547 | 0.02 | 0 |  checkout | 17/8 | **KEEP** | product page with checkout |
| `p/household-budget/guides/family-budget-2027/` | תקציב משפחתי 2027 | 458 | 0.01 | 0 |  | 7/3 | **MERGE** | same intent as budget-2027/ (which has the calculator/fuller page); 301 |
| `p/household-budget/guides/fixed-expenses-list/` | רשימת הוצאות קבועות של משק בית בישראל | 564 | 0.01 | 0 |  | 8/4 | **NOINDEX** | off-focus short guide (<570 words, no/thin sources) with no tool or data |
| `p/invitation-maker/` | עיצוב הזמנה לחתונה ולבר מצווה אונליין | 687 | 0.02 | 0 |  checkout | 13/18 | **IMPROVE** | focus page: author/updated/method box |
| `p/invitation-maker/guides/bar-mitzvah-invitation-wording/` | נוסח הזמנה לבר מצווה ובת מצווה | 547 | 0.02 | 0 |  | 5/7 | **KEEP** | hub / unique page |
| `p/invitation-maker/guides/print-invitations/` | הדפסת הזמנות לחתונה ולאירועים | 594 | 0.04 | 0 |  | 4/7 | **IMPROVE** | focus page: author/updated/method box |
| `p/invitation-maker/guides/wedding-invitation-wording/` | נוסח הזמנה לחתונה | 733 | 0.04 | 0 |  | 5/9 | **IMPROVE** | focus page: author/updated/method box |
| `p/osek-patur-tracker/` | אקסל לעוסק פטור 2026 | 553 | 0.01 | 2 |  checkout | 7/6 | **KEEP** | product page with checkout |
| `p/osek-patur-tracker/guides/income-expense-tracking/` | איך לנהל הכנסות והוצאות כעוסק פטור | 477 | 0.01 | 0 |  | 3/1 | **NOINDEX** | off-focus short guide (<570 words, no/thin sources) with no tool or data |
| `p/osek-patur-tracker/guides/osek-patur-ceiling-2026/` | תקרת עוסק פטור 2026 | 577 | 0.02 | 2 |  | 4/2 | **MERGE** | same intent as tools/osek-patur-ceiling/ (which has the calculator/fuller page); 301 |
| `p/price-quote-pack/` | תבנית הצעת מחיר בעברית | 445 | 0.01 | 1 |  checkout | 6/4 | **KEEP** | product page with checkout |
| `p/price-quote-pack/guides/how-to-write-a-quote/` | איך לכתוב הצעת מחיר | 437 | 0.01 | 0 |  | 4/3 | **NOINDEX** | off-focus short guide (<570 words, no/thin sources) with no tool or data |
| `p/price-quote-pack/guides/quote-vs-invoice/` | הצעת מחיר, חשבון עסקה, קבלה וחשבונית מס | 451 | 0.01 | 2 |  | 4/3 | **NOINDEX** | off-focus short guide (<570 words, no/thin sources) with no tool or data |
| `p/purim-planner/` | מתכנן משלוחי מנות 2027 באקסל | 410 | 0.09 | 0 |  checkout | 8/5 | **KEEP** | product page with checkout |
| `p/renovation-budget/` | אקסל תקציב שיפוץ | 552 | 0.02 | 0 |  checkout | 5/4 | **KEEP** | product page with checkout |
| `p/renovation-budget/guides/compare-quotes/` | איך משווים הצעות מחיר לשיפוץ | 391 | 0.01 | 0 |  | 4/3 | **NOINDEX** | off-focus short guide (<570 words, no/thin sources) with no tool or data |
| `p/renovation-budget/guides/renovation-cost-2027/` | כמה עולה שיפוץ דירה ב-2027 | 406 | 0.01 | 4 |  | 4/3 | **MERGE** | same intent as tools/renovation-cost/ (which has the calculator/fuller page); 301 |
| `p/seating-chart/` | תוכנה לסידורי הושבה לחתונה | 679 | 0.04 | 0 |  checkout | 8/17 | **IMPROVE** | focus page: author/updated/method box |
| `p/seating-chart/guides/how-to-seat-guests/` | סידורי הושבה לחתונה | 619 | 0.04 | 0 |  | 4/7 | **IMPROVE** | focus page: author/updated/method box |
| `p/seating-chart/guides/tables-and-seats/` | כמה שולחנות צריך לחתונה | 406 | 0.04 | 0 | tool | 6/7 | **IMPROVE** | focus page: author/updated/method box |
| `p/seder-planner/` | מתכנן ליל הסדר 2027 באקסל | 367 | 0.06 | 0 |  checkout | 8/6 | **KEEP** | product page with checkout |
| `p/wedding-planner/` | מתכנן חתונה באקסל ו-Google Sheets | 737 | 0.23 ↔ `p/bar-mitzvah-planner/` | 0 |  checkout | 28/21 | **IMPROVE** | focus page: author/updated/method box |
| `p/wedding-planner/guides/rsvp-seating-gifts/` | אישורי הגעה, הושבה ורישום צ'קים לחתונה | 534 | 0.04 | 0 |  | 13/8 | **IMPROVE** | focus page: author/updated/method box |
| `p/wedding-planner/guides/wedding-budget-2026/` | תקציב חתונה 2026 | 654 | 0.03 | 2 |  | 10/9 | **MERGE** | same intent as tools/wedding-cost/ (which has the calculator/fuller page); 301 |
| `pesach/` | פסח 2027 | 298 | 0.20 ↔ `pesach/pesach-2027-dates/` | 0 |  checkout | 7/13 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `pesach/cleaning-checklist/` | ניקיון לפסח 2027 | 576 | 0.04 | 0 |  | 3/3 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `pesach/pesach-2027-dates/` | פסח 2027 מתי | 343 | 0.20 ↔ `pesach/` | 0 |  | 2/4 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `pesach/pesach-budget/` | תקציב לפסח 2027 | 336 | 0.02 | 0 |  | 1/4 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `pesach/seder-night-guide/` | איך מארגנים ליל סדר 2027 | 382 | 0.02 | 0 |  | 4/3 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `products/` | כל המוצרים | 667 | 0.18 ↔ `` | 0 |  checkout | 12/12 | **KEEP** | hub / unique page |
| `purim/` | פורים 2027 | 206 | 0.09 | 0 |  checkout | 6/8 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `purim/class-mishloach-manot/` | משלוחי מנות לגן ולכיתה | 351 | 0.01 | 0 |  | 3/3 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `purim/mishloach-manot-ideas/` | רעיונות למשלוחי מנות לפי תקציב | 394 | 0.01 | 0 |  | 3/3 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `purim/purim-halacha/` | הלכות פורים בקצרה | 479 | 0.07 | 0 |  | 3/3 | **NOINDEX** | off-focus seasonal page, <600 words, no sources, generic topic (dates/ideas/halacha) we cannot win; products + calculators stay indexed; revisit before the season |
| `tools/` | מחשבונים חינם | 240 | 0.15 ↔ `` | 0 |  | 11/15 | **KEEP** | free tool / original asset |
| `tools/bar-mitzvah-cost/` | כמה עולה בר מצווה 2026 | 546 | 0.03 | 3 | tool | 5/5 | **KEEP** | free tool / original asset |
| `tools/budget-503020/` | מחשבון תקציב 50/30/20 בשקלים | 429 | 0.02 | 0 | tool | 16/5 | **KEEP** | free tool / original asset |
| `tools/matza-wine-calculator/` | כמה מצות ויין צריך לליל הסדר | 455 | 0.02 | 1 | tool | 9/5 | **KEEP** | free tool / original asset |
| `tools/mishloach-manot-budget/` | מחשבון תקציב משלוחי מנות 2027 | 326 | 0.09 | 0 | tool | 9/6 | **KEEP** | free tool / original asset |
| `tools/net-salary-budget/` | מחשבון תקציב לפי משכורת נטו | 634 | 0.02 | 0 | tool | 9/7 | **KEEP** | free tool / original asset |
| `tools/osek-patur-ceiling/` | מחשבון תקרת עוסק פטור 2026 | 372 | 0.02 | 2 | tool | 10/4 | **KEEP** | free tool / original asset |
| `tools/renovation-cost/` | מחשבון עלות שיפוץ דירה 2026 | 450 | 0.01 | 4 | tool | 5/4 | **KEEP** | free tool / original asset |
| `tools/savings-goal/` | מחשבון יעד חיסכון | 558 | 0.01 | 0 | tool | 9/6 | **KEEP** | free tool / original asset |
| `tools/sufganiyot-calculator/` | כמה סופגניות ולביבות צריך | 322 | 0.01 | 0 | tool | 7/4 | **KEEP** | free tool / original asset |
| `tools/vat-calculator/` | מחשבון מע"מ 18% | 362 | 0.01 | 1 | tool | 9/6 | **KEEP** | free tool / original asset |
| `tools/wedding-cost/` | כמה עולה חתונה ב-2026 | 1096 | 0.01 | 8 | tool | 22/13 | **IMPROVE** | focus page: author/updated/method box; merged budget-split section (worked ₪184.9k split) from wedding-budget-2026 |
| `tools/wedding-gift/` | כמה לשים בחתונה 2026 | 784 | 0.03 | 5 | tool | 31/17 | **IMPROVE** | focus page: author/updated/method box; worked example (Thursday couple = ₪800) + full coefficient table |
| `tools/wedding-timeline/` | לוח זמנים לחתונה לפי תאריך | 470 | 0.01 | 1 | tool | 16/5 | **IMPROVE** | focus page: author/updated/method box |
