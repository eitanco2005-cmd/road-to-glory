# Shared build contract (all workers read this)

Read `ops/PLAN.md` first. Site = static Hebrew RTL site in `docs/` (GitHub Pages), no build step.

## Ownership (only edit your own paths, to avoid merge conflicts)
- **W1 Platform** owns: `docs/index.html`, `docs/assets/**`, `docs/legal/**`, `docs/thanks/**`,
  `docs/products/index.html`, `docs/sitemap.xml`, `docs/robots.txt`, `docs/404.html`, `tools/site/**`.
- **W2 Events** owns: `docs/p/wedding-planner/**`, `docs/p/bar-mitzvah-planner/**`,
  `docs/tools/wedding-gift/**`, `docs/tools/bar-mitzvah-cost/**`, `products/wedding*/**`, `products/bar-mitzvah*/**`
- **W3 Money** owns: `docs/p/household-budget/**`, `docs/p/renovation-budget/**`,
  `docs/tools/budget-503020/**`, `docs/tools/renovation-cost/**`, `products/household*/**`, `products/renovation*/**`
- **W4 Freelancer** owns: `docs/p/osek-patur-tracker/**`, `docs/p/price-quote-pack/**`,
  `docs/tools/osek-patur-ceiling/**`, `docs/tools/vat-calculator/**`, `products/osek*/**`, `products/quote*/**`
- Each product worker also writes `docs/data/products/<slug>.json` for each of its products.

## Shared interfaces (W1 builds them; others just use them)
- Every page: `<html lang="he" dir="rtl">`, link `/assets/site.css`, load `/assets/site.js` (header/footer injection,
  visit counter), Hebrew font Assistant/Heebo via Google Fonts.
- Paths are root-relative in markup as `/road-to-glory/...` is NOT assumed: use **relative** paths
  (e.g. `../../assets/site.css`) so the site works on any host.
- Buy button: `<div class="buy" data-product="<slug>"></div>` + `<script src="../../assets/checkout.js"></script>`.
  checkout.js reads `docs/data/products/<slug>.json` and `/config` client id, renders PayPal buttons (ILS),
  on capture records the sale (see W1 brief) and redirects to `thanks/?p=<slug>&o=<orderId>`.
- Product JSON schema:
  `{"slug","title","subtitle","price_ils","bundle_of":[],"files":[{"label","path"}],"sheets_copy_url":null,"tool":"<tool slug>"}`
  `files[].path` points into `docs/dl/<random-16-char-folder>/...` (unguessable folder, not linked anywhere but thanks page).
- PayPal Live client id: `config/paypal.json` (W1 copies it into `docs/assets/config.js`).

## Product quality bar
- Spreadsheets: real .xlsx built with Python (openpyxl), Hebrew RTL sheets (`sheet_view.rightToLeft=True`),
  formulas not hard-coded values, input cells clearly coloured, a "הוראות" sheet, dashboard with charts,
  data validation/dropdowns, no macros. Also note what must be done to offer a Google Sheets copy.
- Any tax/legal figure: cite official source + date in the file and the page. No tax advice wording.
- Free tool pages: work fully client-side, instant results, useful on their own, with a clear soft link to the paid product.
- Product + tool pages: unique `<title>` and meta description in Hebrew targeting the search phrase, FAQ section,
  JSON-LD (Product / SoftwareApplication), Open Graph, 2–4 screenshots of the product (Playwright/rendered) in the page.
- Test on 375px and 1280px with Playwright. Honest copy: no fake reviews, no fake scarcity.

## Git
Commit often, push to your own branch only. No pull requests. Don't edit `ops/STATUS.md` or `ops/PLAN.md`.
Write a short report at `ops/reports/<worker>.md` when done (what's built, what's left, any decisions).
