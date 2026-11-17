# Stream E – Hanukkah pack (branch `ws/hanukkah`)

Status: **built, tested, pushed. Ready to merge and go live before Nov 22.**

## Dates checked
Hanukkah 5787 = **evening Fri 4 Dec 2026 → Sat 12 Dec 2026** (8th candle Fri 11 Dec). Computed with the arithmetic Hebrew
calendar (`products/hanukkah/verify_dates.py`, sanity-checked against Rosh Hashana 5787 = 12 Sep 2026 and Hanukkah 2025 = 14 Dec
evening). Kislev 5787 has 30 days → night 6 = ל׳ כסלו, nights 7–8 = א׳–ב׳ טבת. Two Friday nights (1 and 8) + motzei Shabbat (night 2):
lighting notes on the chart cover all three.

## Brachot
Standard text with full niqqud: (1) …לְהַדְלִיק נֵר חֲנֻכָּה (note: some say נֵר שֶׁל חֲנֻכָּה), (2) שֶׁעָשָׂה נִסִּים…,
(3) שֶׁהֶחֱיָנוּ – first night only. The Name is written ה׳ (so the sheet can be discarded; note tells readers to say it as usual).
English pack adds transliteration + translation. Rendered/visually checked in the PDF (Noto Sans Hebrew, niqqud correct).

## Products (all with files in `docs/dl/<random>/`, see `products/hanukkah/dl_folders.json`)
| slug | price | files |
|---|---|---|
| `hanukkah-activity-pack` | ₪19 | 20-page A4 PDF (he) |
| `hanukkah-party-planner` | ₪19 | xlsx blank + example (he, RTL) |
| `hanukkah-bundle` | ₪29 | both of the above |
| `hanukkah-activity-pack-en` | $12 | 20-page PDF, US Letter + A4 |
| `hanukkah-party-planner-en` | $12 | xlsx blank + example |
| `hanukkah-bundle-en` | $19 | both English products |

**Activity pack (20 pp, vector, original art drawn as SVG in `art.py`, printed by Chromium):** cover, contents + story + print tips,
5 coloring pages (hanukkiah, dreidels, sufganiyah + latkes, window scene, oil jug), color-by-number, "count the candles",
easy + hard maze (seeded generator, mirrored for RTL), word search (13 he / 14 en words, unique placement verified), dreidel rules,
score sheet, cut-and-fold cube dreidel (real size), 2026 lighting chart, blessings page, 8 nights of kindness, 2 greeting cards,
answer key. Fonts embedded: Fredoka, Assistant, Noto Sans Hebrew, Nunito (all OFL, `products/hanukkah/fonts/`).

**Party planner xlsx (openpyxl, no macros, recalculated in LibreOffice: 0 formula errors):** Instructions, Guests (RSVP dropdowns,
SUMIFS totals), Quantities (party date, count-maybes, appetite, make/buy; 20 editable assumptions; latkes, sufganiyot, potatoes,
dough ingredients, oil, drinks, gelt, disposables, candles), Shopping List (auto rows + 25 manual rows, est. cost, bought ✓),
8 Nights Gifts (per-night summary, status, over-budget highlight), To-Do (16 tasks, due dates from party date, overdue highlight),
Dashboard (KPIs, bar chart budget vs actual per night, pie of cost by category). Hebrew sheets RTL, A4; English US units, Letter.
Prices in the file are labelled examples.

## Pages
Hebrew (RTL, shared header/footer): `p/hanukkah-activity-pack/`, `p/hanukkah-party-planner/`, hub `hanukkah/` (bundle buy box +
dates table), tool `tools/sufganiyot-calculator/`, guides `hanukkah/hanukkah-2026-dates/`, `hanukkah/kids-activities/`,
`hanukkah/hanukkah-party/`.
English (`docs/en/` doesn't exist on main → standalone LTR under `docs/en/hanukkah/`, own static header/footer, only files under that
folder so it can't collide with ws/en): hub (bundle), `activity-pack/`, `party-planner/`, `latke-calculator/`,
`when-is-hanukkah-2026/`, `how-to-play-dreidel/`, `terms/` (EN terms + refund), `thanks/` (noindex, EN download page).
All pages: unique title/description, canonical, OG, JSON-LD (Product / WebApplication / Article / FAQPage / BreadcrumbList),
hreflang he↔en pairs, FAQ, real previews (WebP rendered from the PDFs / LibreOffice renders of the example workbooks).
Generators: `products/hanukkah/site_pages.py`; full rebuild: `python3 products/hanukkah/release.py`.

## Shared-file changes (minimal, backward compatible)
- `docs/assets/checkout.js`: optional product fields `currency` (default ILS), `price` (default `price_ils`), `thanks_path`
  (default `thanks/`). SDK loads with the product's currency (one currency per page; a second currency on the same page shows an error
  instead of charging in the wrong currency). Box texts in English when `<html lang="en">` (locale en_US). ILS products unchanged.
  USD product JSONs set both `price` and `price_ils` (same USD number) so either reader works — if ws/en chose a different field for the
  amount, reconcile at merge. Field name `currency` as agreed.
- Nothing else shared touched: **not** edited `data/products/index.json`, `data/tools.json`, `sitemap.xml`, home/products pages
  (W1-owned, and ws/worksheets edits the same catalog).

## Tests
- `node products/hanukkah/test_e2e.js` → **78 PASS / 0 FAIL**: 14 pages × 375/1280 (no h-scroll, 1 h1, canonical, JSON-LD, no
  broken images, lang/dir, no JS errors); TEST purchases for all 6 products land on the right thanks page (he → `thanks/`,
  en → `en/hanukkah/thanks/`) and every download returns a real PDF/xlsx; both calculators (10 adults + 4 kids → 19 doughnuts,
  48 latkes, 2.4 kg / 5.4 lb potatoes); live PayPal SDK loads with `currency=ILS` on he pages and `currency=USD` on en pages.
- `tools/site/e2e_test.js` (platform) → ALL PASSED with the new checkout.js (run with a stub sales endpoint since fastapi isn't
  installable in this container).

## Manager to-do at merge
1. Run `python3 tools/site/build_site.py` (sitemap picks up the 15 new indexable pages automatically; thanks is excluded).
2. Optional catalog entries (W1 files) — suggested:
   - `data/products/index.json`: category `"holidays": "חגים"`, products `hanukkah-activity-pack`, `hanukkah-party-planner`
     (category holidays), bundles + `hanukkah-bundle`. Note catalog cards hard-code the badge "אקסל + Google Sheets" (wrong for the
     PDF) and the platform e2e counts 6 products — adjust both if you add them.
   - `data/tools.json`: `{"slug":"sufganiyot-calculator","title":"כמה סופגניות ולביבות צריך?","description":"מחשבון כמויות לחנוכה לפי מספר האורחים","product":"hanukkah-party-planner","icon":"🍩"}`
   - A home-page link to `hanukkah/` until Dec 12 would help most.
3. After Dec 12: keep pages live (evergreen for 2027 with a date refresh) or noindex — your call.

## Decisions
- Dreidel letters: Hebrew pack נ ג ה פ, English pack נ ג ה ש with a note about פ in Israel.
- Quantity assumptions (latkes 4/2, sufganiyot 1.5/1, 20 latkes per kg / 9 per lb, 500 g flour ≈ 16 doughnuts, min 1 L / 4 cups
  deep-frying oil) are presented as editable estimates, not facts.
- No school-vacation dates claimed (we point to the Ministry of Education calendar).
- `products/hanukkah/out/` (intermediate HTML/PDF) is git-ignored; deliverables live only in `docs/dl/`.
