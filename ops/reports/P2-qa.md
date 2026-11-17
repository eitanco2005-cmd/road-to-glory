# P2 QA report (branch ws/qa)

*2026-11-17. Base: main @ 45683cf. No real payment was made; all checkouts used `?test=1`.*

## Result in one line
Site, files and checkout all pass. Fixed 4 spreadsheet bugs, 2 wrong tax claims, ~20 overstated claims, the false "Google Sheets copy link" promise, contrast and a11y issues, and halved the heaviest images. `node tools/site/e2e_test.js`: **ALL PASSED**.

## How it was checked
- **Pages:** Playwright crawl of all 34 html pages at 375 and 1280 px (68 runs): horizontal overflow, JS/console errors, 4xx assets, internal links, image alt/size, axe-core 4.10 a11y scan. Visual review of screenshots.
- **Checkout:** every product (6) and bundle (4) at 375 and 1280: test pay button → price matches JSON → thanks page → every download link returns the real file (200). 20/20 passed.
- **Spreadsheets:** all 13 xlsx recalculated in LibreOffice, blank and filled with realistic Israeli data (incl. last row of every table). Independently re-verified: 0 error cells, no functions newer than Excel 2016.
- **Facts:** every cited figure checked against the cited/official sources (gov.il, Kol Zchut, Bizportal, Walla, N12, Green Invoice etc.). Note: the proxy blocked kolzchut, mako and sogrimdira directly, so those were verified via search snippets / secondary sources.

## Found → fixed

### Spreadsheets (generators fixed and rebuilt; same file paths in docs/dl)
| File | Bug | Fix |
|---|---|---|
| Household budget (3 files) | Dashboard "יתרה משוערת בעו"ש היום" picked the wrong month when data didn't start in January (showed 25,780 instead of 57,240) | Uses last month with any income/expense |
| Household budget | "% ניצול" missing for "קבוצות אחרות" row | Added |
| Renovation (2 files) | Dashboard room/trade tables and charts ignored rooms/trades the buyer adds (a 9,000 ₪ job vanished) | Catch-all rows; charts include them |
| Renovation | `MINIFS` = #NAME? in Excel 2010/2016, but page promises "Excel 2010 ומעלה" | Replaced with SUMPRODUCT/MIN, same results everywhere |
| Renovation | Two quotes marked "כן" for one job silently double-counted | Cell turns red + instruction note |
| Quote pack | Header showed dangling "· · ·" when contact fields empty | Fixed; also instructions explain TODAY() date fixing (Ctrl+;) |
| Wedding + bar mitzvah | Instructions promised a "יצירת עותק" link that doesn't exist | Honest "upload to Drive / File → Import" text |
Osek patur tracker: no bugs (tested to 97% of the ceiling, crossing month, quarterly, annual sheet).

### Facts
- **Wrong (fixed):** osek patur guide said the "עסק זעיר" track has its own ceiling (it uses the same 122,833 ₪); said the ceiling updates every year (it was frozen at 120,000 ₪ in 2024–2025).
- **Softened (unsupported or overstated):** bar mitzvah "average 18,000 ₪" (no such average; now a range with context); photographer range 3–10k → 1.5k–10k+; bar mitzvah gift ranges marked as our estimate; wedding "typical 100–120k" → zap's 117k mid-budget + 100–150k range; unverifiable "two-thirds / a fifth" split and "regions 10% cheaper" removed; wedding-gift summary now framed as our calculator's estimate, "רוב האנשים" → "נוהג נפוץ", "half if not attending" → "יש שנוהגים"; 30–60k season saving → 25–55k (matches cited plate prices); contract tips hedged; "15–20 fixed expenses", "רובנו" softened; deposit/validity "common practice"; "תוכנה מאושרת" → "תוכנה הרשומה ברשות המסים"; cancellation FAQ now cites §14ג(ד) and is less absolute.
- **Verified OK:** VAT 18% (from 1.1.2025) and all VAT math; osek patur ceiling 122,833 ₪ (2026) and the calculator constant; turnover is gross; ineligible professions; allocation-number thresholds; 2026 wedding plate prices and calculator defaults; every calculator output quoted in tables/FAQs; quote and contractor-comparison examples; bundle prices.
- Every fix applied to both the html and its generator script (so regeneration keeps it). All JSON-LD still parses.

### Copy honesty
- Removed every promise of a Google Sheets "copy link" (home ×3, products ×2, thanks instructions, terms ×2, privacy). Now: "works in Excel and in Google Sheets by uploading to Drive". Generator `tools/site/build_legal.py` updated too.
- Wedding/bar mitzvah FAQ claimed dropdowns + conditional formatting all work in Sheets (untested; dropdowns use named ranges) → softened.
- "Excel 2010 ומעלה" (household, renovation) is now true (MINIFS removed).

### Pages / accessibility / speed
- Accent text colour #c98410 failed contrast (2.7–2.9:1) on 34 page runs → #8f5a00 (≥5.1:1).
- Heading order: footer h3 → h2 (styled same), osek calculator CTA h3 → h2, hidden h2 on tools index.
- Scrollable tables now keyboard-focusable with unique labels (site.js).
- Wedding + bar mitzvah screenshots PNG → WebP: 1.25 MB → 0.57 MB; PNGs kept for og:image; `shots.py` now writes both.
- After fixes: **0 axe violations, 0 overflow, 0 broken internal links, 0 JS errors** on 68 runs.
- Hebrew text: scanned all pages for duplicated words / spacing errors (none real) and read home + main tool copy; no spelling issues found.
- Housekeeping: untracked committed `__pycache__/*.pyc`, added `.gitignore`.

## Left (decisions / owner actions)
1. **Real Google Sheets copy links:** someone with a Google account must upload each blank file, convert to Sheets, share as viewer, and set `sheets_copy_url` to `https://docs.google.com/spreadsheets/d/<id>/copy`. Until then the site says "upload to Drive". Worth also testing the event planners' dropdowns there once.
2. Event planner dashboard charts cover only the default category/side rows (buyer-added rows show in tables, not charts). Left: extending would draw empty bars.
3. Event planner "סטטוס הגעה" pie counts invited, the headline counts confirmed — definitional, left.
4. Renovation price ranges come from commercial price lists we couldn't fetch independently; pages already say they are not official.
5. The legal pages are templates, not lawyer-reviewed (as W1 noted).
6. The badge "אקסל + Google Sheets" on product cards kept: the files do work in Sheets via upload.
7. Merge note: P2-SEO works on docs/ in parallel; my edits are targeted string changes, conflicts should be small (most likely `docs/index.html`, `docs/assets/site.js`).

## Re-run
- `node tools/site/e2e_test.js` → ALL PASSED (after all changes).
- Crawl/checkout scripts used are QA-only (not committed); checkout test: 20/20 pass.
