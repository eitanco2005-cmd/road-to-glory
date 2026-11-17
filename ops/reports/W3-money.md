# W3 Money products: report

Branch `ws/money`. Status: **done, ready to merge**. Written 2026-11-17.

## What's built

### 1. Household budget Pro (`household-budget`, ₪39)
- **Generator:** `products/household-budget/build.py` (openpyxl). It builds 2027 and 2026 versions, each as a blank workbook and an example with a full year of demo data.
- **Sheets:** הוראות, דשבורד, הגדרות, תקציב, תנועות, חודשי, שנתי, יעדי חיסכון, חובות. All sheets are RTL. Input cells are yellow and formula cells light blue. There are no macros.
  - **Categories:** 56 Israeli categories (ארנונה, ועד בית, קופת חולים משלים, ביטוח לאומי, גן/צהרון, טסט ואגרה, מתנות לשמחות…), each tagged הכנסה/הוצאה and צורך/רצון/חיסכון. There are 34 empty rows for the buyer's own categories.
  - **Data entry:** a monthly plan auto-fills 12 months and can be overridden per month. The transaction log has 2,000 rows, with dropdowns for category, payment method and date validation. Rows dated in another year are flagged and not counted.
  - **Views:** the monthly view has a month picker, red over-budget flags and a chart. The annual sheet is SUMIFS by category × month, with a running bank balance. The dashboard shows KPIs, group table, 50/30/20 actual vs target, and 5 charts.
  - **Savings goals:** monthly amount needed to reach each goal, with progress bars.
  - **Debts:** NPER months to payoff, CUMIPMT remaining interest, and an avalanche payoff order.
- **2027 version (January campaign):** the year is one cell (`הגדרות!B4`, defined name `BudgetYear`). The download ships 2027 as the main file and includes 2026. Guide 1 targets "תקציב משפחתי 2027".

### 2. Renovation budget planner (`renovation-budget`, ₪39)
- **Generator:** `products/renovation-budget/build.py` builds a blank workbook and a 3-room-apartment example.
- **Sheets:** הוראות, דשבורד, פרויקט, עבודות, הצעות מחיר, תשלומים, קבלנים.
  - **Works:** 100 work lines with room, trade and status dropdowns. The governing budget is the chosen quote if one exists, otherwise the estimate.
  - **Quotes:** converted to an incl.-VAT basis (VAT 18% is a setting cell). The sheet flags the cheapest quote per work item (MINIFS) and shows each quote's gap from it.
  - **Payments:** paid vs planned, with an invoice flag.
  - **Dashboard:** contingency (בלת"מ) status with an alert, breakdown by room and by trade, a 12-month cash flow and 3 charts.
- **Contractor checklist:** `products/renovation-budget/build_checklist.py` builds an RTL Word file covering what a quote must contain, contractor checks, a fair payment schedule, questions to ask, and a 3-contractor comparison table.

### 3. Free tools
- **`docs/tools/budget-503020/`**
  - Income → needs/wants/savings, monthly and yearly. Three split models: 50/30/20, 60/20/20 and 70/20/10.
  - Emergency fund range of 3–6 months of needs, and how many months it takes to reach it.
  - Optional "your actual" comparison with meters and plain-language advice, including a housing-cost share warning.
  - The calculation can be shared as a URL.
- **`docs/tools/renovation-cost/`**
  - Inputs: area, finish level, works (flooring, paint, electrical, plumbing, kitchen, bathrooms, mini-central A/C, extra) and contingency.
  - Output: a price range per item and in total, plus price per m² compared with a benchmark.
  - **Every price range cites its source on the page, checked 17 Nov 2026:** sogrimdira.co.il 2026 price list, experts.co.il kitchens 2026, a mini-central A/C 2026 guide, and shipozimil.co.il.
  - These are commercial price guides, not official data, and the page says so.

### 4. Pages
- **Sales pages:** `docs/p/household-budget/` and `docs/p/renovation-budget/`. Each has a hero, buy box (`.buy` + checkout.js), features, 4 real screenshots rendered from the example workbooks, steps, what's included, FAQ, guide links and a mobile `.buy-bar`.
- **Guides, 2 per product:**
  - `p/household-budget/guides/family-budget-2027/`: תקציב משפחתי 2027 ב-6 צעדים
  - `p/household-budget/guides/fixed-expenses-list/`: רשימת הוצאות קבועות
  - `p/renovation-budget/guides/renovation-cost-2027/`: מחירון with sources
  - `p/renovation-budget/guides/compare-quotes/`: worked VAT example
- **On every page:** a unique Hebrew title and description, canonical, Open Graph, JSON-LD (Product+Offer / WebApplication / Article, FAQPage, BreadcrumbList) and no ratings.
- **Generators:** `products/household-budget/site_pages.py`, `products/renovation-budget/site_pages.py` and the shared shell `site_common.py`. Re-run them after edits.

### 5. Data and downloads
- `docs/data/products/household-budget.json` and `renovation-budget.json` follow the contract schema, plus extra `url` and `image` fields. `files[].path` is relative to the docs root (`dl/...`), which is the form W1's thanks page resolves.
- Download folders:
  - `docs/dl/356eeeed31d1ee5e/` (household): 2027 blank, 2027 example, 2026 blank
  - `docs/dl/1c9ed6b2319083a3/` (renovation): blank, example, checklist .docx
- `products/*/release.sh` rebuilds the files, runs the LibreOffice QA and copies them into the download folders.

## Testing
- **Formulas:** every workbook was recalculated with LibreOffice headless (`products/household-budget/qa_recalc.py`). The result is **0 formula errors** in all 5 workbooks. I spot-checked key values by hand:
  - Dashboard totals match the transactions.
  - Quote gaps are correct: 16,500 + 18% = 19,470, and its gap from the 17,200 quote is 2,270.
  - NPER/CUMIPMT give sensible results.
  - The avalanche order puts the 11% overdraft first.
- **Pages:** tested with Playwright at 375 px and 1280 px, with W1's `ws/platform` assets overlaid.
  - All 8 pages have no console errors, no failed requests and no horizontal overflow, and the header and footer are injected.
  - The tools compute correctly. For example, ₪18,000 income gives 9,000 / 5,400 / 3,600 and an emergency fund of 27,000–54,000.
  - Test-mode checkout (`?test=1`) reaches `thanks/` for both products, and all 6 download links return 200.

## Decisions
- **Blank file plus example file.** The blank workbook has no pre-filled amounts, so buyers start clean. The example workbook shows a full year so buyers can see how it works, and the screenshots come from it.
- **2027 is the main year.** January is the selling season. 2026 is included at no extra cost.
- **Excel features.** I used only functions that Excel 2010+, Google Sheets and LibreOffice all support. MINIFS is written with the `_xlfn.` prefix, and there are no dynamic arrays or macros.
- **No tax or legal advice.** The only official figure is VAT 18% (Israel Tax Authority, since 1.1.2025), which is cited in the workbook and on the pages. Where the ביטוח לאומי and ארנונה text mentions amounts and discounts, it points readers to the official bodies instead of quoting figures.
- **Renovation estimator method.** The level mapping uses part of each range: basic = bottom 40%, standard = middle 30–70%, high = top 40%. Electrical and plumbing scale with area relative to 90 m², clamped to 0.6–2×. All of this is written on the page.
- **Page styles.** The small set of extra CSS lives inline in each page (`.w3-*` classes), so I didn't touch W1's `assets/`.

## For the manager / left to do
1. **Merge conflict:** W1 created placeholder `docs/data/products/household-budget.json` and `renovation-budget.json` on `ws/platform`. **Keep W3's versions.** They have files, so they're purchasable.
2. **Sitemap (W1-owned):** add these 8 URLs:
   - `p/household-budget/`, `p/renovation-budget/`
   - `tools/budget-503020/`, `tools/renovation-cost/`
   - `p/household-budget/guides/family-budget-2027/`, `p/household-budget/guides/fixed-expenses-list/`
   - `p/renovation-budget/guides/renovation-cost-2027/`, `p/renovation-budget/guides/compare-quotes/`
3. **Tools index:** W1's tools index shows both tools as "בקרוב". Flip them to live.
4. **Google Sheets copy link:** `sheets_copy_url` is null. To offer one:
   - Upload `household-budget-2027.xlsx` and `renovation-budget.xlsx` to the owner's Google Drive.
   - Open each with Google Sheets and "Save as Google Sheets".
   - Share as "Anyone with the link: Viewer".
   - Put `https://docs.google.com/spreadsheets/d/<ID>/copy` into the JSON.
   - Check the charts after conversion: Sheets re-renders openpyxl charts and may change their colours.
5. **Money bundle (₪59):** W1's `money-bundle.json` should have `bundle_of: ["household-budget","renovation-budget"]`.
6. **Guide link to W2:** the fixed-expenses guide links to `tools/wedding-gift/`, which is W2's page.
7. **Every January:** change `YEARS` in `household-budget/build.py`, run `release.sh`, and update the year in the page and guide titles.
8. **Recheck renovation prices** about every 6 months. The ranges live in `docs/tools/renovation-cost/calc.js` and on the tool and guide pages.
