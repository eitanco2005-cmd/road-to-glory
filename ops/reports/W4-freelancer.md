# Report W4: Freelancer products (branch `ws/freelancer`)

*2026-11-17*

## What's built

| Item | Path |
|---|---|
| עוסק פטור 2026 tracker (₪39) .xlsx: empty + example | `products/osek-patur-tracker/` (builder `build.py`) |
| Price-quote pack (₪29): 1 .xlsx with 5 designs + example, and 5 .docx | `products/quote-pack/` (builder `build.py`) |
| Download copies (unguessable folders) | `docs/dl/rtxv604h87l232v3/` (osek), `docs/dl/95861t10412vl3f9/` (quotes; the Word files ship as one ZIP) |
| Product JSON | `docs/data/products/osek-patur-tracker.json`, `price-quote-pack.json` |
| Sales pages | `docs/p/osek-patur-tracker/`, `docs/p/price-quote-pack/` (with screenshots in `img/`) |
| Free tools | `docs/tools/osek-patur-ceiling/`, `docs/tools/vat-calculator/` |
| Guides (2 per product) | `docs/p/osek-patur-tracker/guides/{osek-patur-ceiling-2026,income-expense-tracking}/`, `docs/p/price-quote-pack/guides/{how-to-write-a-quote,quote-vs-invoice}/` |
| Page generator (re-run after edits) | `products/osek-patur-tracker/build_pages.py`: writes all 8 W4 pages |

### Tracker contents
Sheets: הוראות, לוח בקרה, הגדרות, הכנסות, הוצאות, סיכום חודשי, עזר לדוח שנתי.

- **Logs:** 500-row income and expense logs. Dates and amounts are validated, and payment methods and categories are dropdowns.
- **Expense "% מוכר" column:** covers mixed-use expenses such as a phone or car. Rows marked "document missing" are flagged.
- **Year filter:** only rows dated in the tax year set in הגדרות are counted.
- **Dashboard:** a ceiling gauge (half-doughnut chart plus a data bar), a status that turns yellow at 70% and red at 90%, and these figures:
  - average monthly pace
  - projected year-end turnover
  - the month the ceiling is likely to be crossed
  - how much can still be earned per month
- **Pace calculation:** it handles a business that opened mid-year (start month) and lets you override the month manually.
- **Monthly and quarterly summary:** with an income-vs-expenses chart and a cumulative-vs-ceiling chart.
- **Annual report helper:** turnover, expenses by category with a pie chart, profit, receipt count, and an end-of-year checklist.

### Quote pack contents
- **Business details:** entered once in הגדרות and shown in all 5 designs: קלאסי, מודרני, מינימליסטי, צבעוני, לפי מחירון.
- **Price list:** design 5 picks items from a dropdown that reads the price list.
- **Automatic sums:** line totals, subtotal, % discount, VAT, and grand total.
- **Dealer type:** עוסק מורשה or חברה adds 18% VAT. עוסק פטור shows "ללא מע״מ" and adds no VAT. Both cases are verified.
- **Dates:** "בתוקף עד" = date + validity days.
- **Print:** each design fits on one A4 page.
- **Yellow input cells:** a "highlight input cells" switch turns the yellow fill off so it doesn't print.
- **Word versions:** same layouts, RTL, totals typed by hand. The pages say this honestly.
- **Disclaimer on every design:** "not a tax invoice/receipt".

## Update after merging W1 (claude/epic-heisenberg-h552gc)
- **Merge:** merged into `ws/freelancer`. On the two product JSONs I kept **mine** (no `placeholder`).
- **Product pages:** rebuilt to W1's template order. H1 → one sentence → compact buy box → points → everything else.
  - At 375×667 the first pay button ends at about 564px (osek) and 497px (quotes), so it is above the fold.
  - The lower sections now link to `#buy` instead of rendering a second buy box.
- **URLs:** canonical, `og:url`, absolute `og:image` and Product `offers.url` now use `https://eitanco2005-cmd.github.io/road-to-glory/`.
- **Test purchases (`?test=1`):** both products reach the thanks page, and every download link returns 200.
- **Freelancer bundle:** both of its members are now deliverable, so it should be buyable.
- **W1 e2e:** `node tools/site/e2e_test.js` reports **ALL PASSED**. I installed fastapi and uvicorn locally to run it.

## Testing
- **Formulas:** recalculated with LibreOffice headless. No error cells in either workbook.
  - Tracker example: turnover ₪80,600, 65.6% of the ceiling.
  - Quote example: 6,290 − 5% = 5,975.50, + 18% = 7,051.09. With עוסק פטור the total is 5,975.50 and VAT is 0.
- **Pages:** tested with Playwright at 375px and 1280px against W1's `ws/platform` assets.
  - No JS errors and no horizontal scroll on any of the 8 pages.
  - In `?test=1` mode, the buy box renders from my JSON.
  - Both calculators were checked by hand. Ceiling: ₪80k by August → 65.1%, ₪42,833 left, at ₪15k/month crosses in November. VAT: 1,180 ÷ 1.18 = 1,000 + 180.
- **404 links:** the only ones are pages not yet on my branch (W1 `legal/*`, `products/`, other workers' pages).

## Decisions
- **Official figures:** checked on 17.11.2026 by web search. Direct fetch of kolzchut/greeninvoice was blocked by the sandbox network.
  - Osek patur ceiling 2026 = **₪122,833** (2025: ₪120,000). Source: Kol Zchut, plus Tax Authority publications.
  - VAT = **18%** since 1.1.2025.
  - Both are cited with that date in the files and on the pages. Both are single cells in the workbooks: update them every January.
- **"Crossing the ceiling":** the copy says the switch to עוסק מורשה applies from the transaction that crosses it, attributed to Kol Zchut. Deadlines are deliberately left vague ("usually by end of January"), with a referral to the Tax Authority or an accountant. No tax advice wording.
- **Allocation-number threshold (guide "quote-vs-invoice"):** stated as ₪5,000 from June 2026, per R's research. It links to gov.il to check the current threshold.
- **Product JSON:** `files[].path` is relative to `docs/` (`dl/<folder>/<file>`), matching checkout.js's ROOT-relative fetch convention. I also added optional `page` and `image` keys. **Merge note:** W1 created placeholder versions of these two JSONs with `"placeholder": true`. Keep **mine**, otherwise checkout shows "בקרוב".
- **Bundle:** I did not touch the `freelancer-bundle.json` placeholder (W1 owns it). My pages link to `products/` for the bundle.
- **Example copies:** each product also ships a filled example file, used for the screenshots. They're honest: the pages say the screenshots come from the example copy.

## Left / for the manager
1. **Google Sheets copy link:** `sheets_copy_url` is null. Owner or manager steps:
   1. Upload each `.xlsx` to Drive and open it with Google Sheets.
   2. Share it as "anyone with link: viewer".
   3. Put `https://docs.google.com/spreadsheets/d/<ID>/copy` into the JSON.
   - Instructions inside the files already explain how a buyer can open the file in Sheets on their own.
2. ~~Absolute `og:image` URLs~~: done.
3. **Sitemap (W1):** add the 8 W4 URLs.
4. **January refresh:** update the ceiling for 2027 (in both `build.py` files and `build_pages.py`), rebuild, and recopy to `docs/dl/`. This is a natural "2027 edition" for repeat sales.
