# W2 Event products: report

Branch `ws/events`, 2026-11-17. Everything in the W2 brief is built and tested. Only the Google Sheets copy links are still open (they need the owner's Google account, see "Left to do").

## What's built

| Item | Path |
|---|---|
| Shared spreadsheet engine (9 linked RTL sheets) | `products/wedding-planner/event_engine.py` |
| Word companion engine (messages, day-of timeline, printable checklist) | `products/wedding-planner/docx_engine.py` |
| Wedding planner config/build (₪49) | `products/wedding-planner/build.py` → `out/` |
| Bar/bat mitzvah planner config/build (₪39) | `products/bar-mitzvah-planner/build.py` → `out/` |
| Publish (files to `docs/dl/`, screenshots, product JSON) | `products/wedding-planner/publish.py` |
| Screenshot renderer (LibreOffice → PDF → PNG) | `products/wedding-planner/shots.py` |
| HTML page generator (all 8 pages) | `products/wedding-planner/web/build_pages.py` |
| Downloads (wedding) | `docs/dl/lje2wikbyyh1goea/` (blank xlsx, filled example xlsx, docx) |
| Downloads (bar mitzvah) | `docs/dl/3lvcpz0f1kr21brs/` (same three files) |
| Product JSON | `docs/data/products/wedding-planner.json`, `bar-mitzvah-planner.json`, `event-bundle.json` |
| Sales pages | `docs/p/wedding-planner/`, `docs/p/bar-mitzvah-planner/` (6 screenshots each in `img/`) |
| Free tools | `docs/tools/wedding-gift/` ("כמה לשים בחתונה 2026"), `docs/tools/bar-mitzvah-cost/` |
| Guides (2 per product) | `docs/p/wedding-planner/guides/{wedding-budget-2026,rsvp-seating-gifts}/`, `docs/p/bar-mitzvah-planner/guides/{bar-mitzvah-cost-2026,bar-mitzvah-timeline}/` |

To rebuild everything: `python3 products/wedding-planner/build.py && python3 products/bar-mitzvah-planner/build.py && python3 products/wedding-planner/publish.py && python3 products/wedding-planner/web/build_pages.py`

### Workbook contents (both planners)
The workbook has these sheets: הוראות, הגדרות, דשבורד, תקציב, מוזמנים, ספקים, תשלומים, צ'קליסט, הושבה.
- **Formulas, not values.** The budget's "actual" column comes from vendors (final price, cancelled vendors excluded). "Paid" comes from payments marked "כן".
- **Payments.** Status is computed from TODAY(): overdue rows are red, rows due within 14 days are orange.
- **Checklist.** Due dates are calculated as event date − weeks.
- **Seating.** Uses SUMIFS of confirmed guests per table, and flags overflow and confirmed guests not yet seated.
- **Dashboard.** Shows 16 KPIs, a "gifts vs cost" balance box, and three charts (budget by category, RSVP pie, guests by side).
- **Dropdowns.** They read from editable lists in הגדרות through defined names (`lst_*`).
- **Inputs and protection.** Input cells are yellow and formula cells are grey. There are no macros. Capacity is 400 invitation rows, 80 vendors, 150 payments and 60 tables.
- **Two xlsx files per product.** One is blank, ready to use. The other is a filled demo with fictional names, which is also the source of the screenshots.
- **Word file.** Ready-to-send WhatsApp-style messages (save the date, RSVP, reminder, thank-you), a day-of timeline table and a printable checklist.

## Testing done
- **Formulas.** I recalculated all four xlsx files with LibreOffice headless and scanned every cell: there are 0 formula errors. I spot-checked the demo by hand (budget totals, paid/remaining, overdue detection, seating totals, RSVP sums).
- **Pages.** I tested all 8 pages with Playwright at 375px and 1280px against W1's `ws/platform` assets. There are no console errors, no failed requests and no horizontal scroll.
- **Links.** Every internal link resolves. The only 404s are other workers' pages linked from W1's footer.
- **Checkout (TEST mode, `?test=1`).** The wedding, bar mitzvah and event-bundle purchases each redirect to `thanks/`. The page lists the correct download links (the bundle shows all six), and every file returns 200.
- **Calculators.**
  - Wedding: the example table on the page matches the calculator's output.
  - Bar mitzvah: the default scenario gives ₪61,247 total. The cost-guide table (₪61k / ₪48k / ₪31k) was computed with the same logic.

## Update after W1 merge
- I merged `origin/claude/epic-heisenberg-h552gc` into `ws/events`. The product JSON conflicts were resolved in favour of W2's versions, so none of them carries `placeholder` any more.
- The product page heroes now follow the manager's order: H1 → one sentence → compact buy box → the rest. At 375×667 the pay button's bottom edge is at 526px (wedding) and 497px (bar mitzvah), so it is above the fold.
- `node tools/site/e2e_test.js` → **ALL PASSED** (it needed `pip install fastapi uvicorn` here). My own suite passes too: 8 pages × 2 widths, links, and test purchases for both products and the bundle.

## Decisions
1. **One engine, two configs.** The bar mitzvah build imports the engine from `products/wedding-planner/`, which keeps everything within W2's owned paths.
2. **Blank file plus filled example file.** Users who are short on time don't have to delete sample rows, and the screenshots stay honest because they come from a real file.
3. **Screenshots come from the actual workbook** (LibreOffice PDF export), not mock-ups.
4. **Wedding-gift model.** It starts from the 2026 price per plate, then applies closeness factors (0.65–2.0 of a plate), 90% per adult for couples, half a plate per child, and about 50% when not attending.
   - Plate prices are the midpoints of the Attending 2026 ranges as quoted in the press (center summer 420–550, winter 340–430), with Thursday +12%.
   - "Other regions −10%" comes from zap 2025 via N12.
   - The closeness, Friday and venue factors are our own calibration, and the page says so plainly.
5. **Bar mitzvah prices are editable estimates.** Default plate prices and line items are labelled as our estimates as of Nov 2026, and every field can be edited. I found no reliable 2026 source for plate prices.
6. **Sources.** I could not open the Israeli news sites from this sandbox (DNS blocked). Figures come from search-result snippets of those articles and from `research/products.md`. Every page cites the outlet with a link and the check date (נובמבר 2026). **QA should open the cited links once and confirm the figures.**
7. **Product JSON conflict.** W1 created placeholder JSONs on `ws/platform` for `wedding-planner`, `bar-mitzvah-planner` and `event-bundle`. **When merging, take W2's versions**: they have real `files`, no `placeholder` flag, and a better bundle subtitle. Slugs and the tool slug (`wedding-gift`) match W1's `tools.json`. The bar mitzvah tool slug is `bar-mitzvah-cost`, per the contract.
8. **Absolute URLs.** Canonical and OG URLs use `https://eitanco2005-cmd.github.io/road-to-glory/`, the same as W1's home page. If a custom domain is added, run one search-and-replace in `products/wedding-planner/web/common.py` (`BASE`) and rebuild.
9. **No FAQ rich-result expectations.** FAQPage JSON-LD is included because it is harmless. The pages also carry Product + Offer, WebApplication and Article schema, plus BreadcrumbList. There are no ratings or reviews.

## Left to do (manager / owner)
- **Google Sheets copy links.** `sheets_copy_url` is `null` in both JSONs.
  1. Upload each blank xlsx to the owner's Google Drive and open it with Google Sheets.
  2. Check that the dropdowns and conditional formats came through. Named-range validations sometimes need re-pointing to the `הגדרות` ranges.
  3. Share it as "anyone with the link: viewer".
  4. Put `https://docs.google.com/spreadsheets/d/<ID>/copy` into the JSON.
  5. Until then, the pages say "upload to Drive and open with Google Sheets", which works today.
- Add `tools/bar-mitzvah-cost` to W1's `docs/data/tools.json` (W1 owns that file), and add all 8 W2 pages to the sitemap.
- Optional: open the four xlsx files in real Excel and Google Sheets once. They were verified in LibreOffice only.
