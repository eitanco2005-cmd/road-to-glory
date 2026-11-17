# Stream A report: English Jewish-life planners (branch ws/en)

Status: **built, tested, pushed to `ws/en`** (no PR). Ready to merge; after merging run
`python3 tools/site/build_site.py` (rebuilds sitemap with hreflang).

## What's live on the branch
- **`/en/` section** (lang="en" dir="ltr", same design system): home, `/en/planners/`, 4 product pages, `/en/tools/` + 3 free
  calculators, `/en/guides/` + 7 guides, `/en/thanks/` (noindex), `/en/legal/{terms,refund,privacy}/`. 22 pages.
- **Products (USD)**, each = blank .xlsx + filled example, Start Here sheet, Settings, live Dashboard with charts,
  yellow inputs / grey formulas, drop-downs, conditional formatting, no macros:
  | Product | JSON slug | Price | Sheets |
  |---|---|---|---|
  | Bar/Bat Mitzvah Planner | `bar-mitzvah-planner-en` | $19 | Budget (14 cats), Vendors, Payments, Guests+gifts+thank-yous, Seating, Checklist (34), Honors & Candles (aliyot + 13+1 candles), Day-of |
  | Jewish Wedding Planner | `jewish-wedding-planner` | $24 | same engine + Ceremony Honors (witnesses, chuppah holders, sheva brachot, tisch), 36-task Jewish checklist, tisch→sheva brachot day-of |
  | Passover Seder Planner | `passover-seder-planner` | $15 | Guests per night (1/2 seders, maybe-toggle), Shopping List scaled by adult/child seats & seder plates (26 items, packs + cost), Menu, Haggadah Parts, Prep Timeline, Seder Plate |
  | Jewish Holiday Hosting Planner | `jewish-holiday-planner` | $15 | Holidays (9 meals), Guests×holidays grid, Menus, Shopping, Traditions (32), Mishloach Manot, Dashboard |
  | Jewish Life Bundle | `jewish-life-bundle` | $49 (vs $73) | all four |
  All 8 files recalculated in LibreOffice with **0 formula errors**. Files in `docs/dl/{l9e1…,m8gv…,2zw7…,i1rk…}/`.
  Built from scratch (new English LTR engine, `products/en-jewish-life/`), not by translating the Hebrew engine: its labels
  are hard-coded Hebrew/RTL/ILS, a clean engine was faster and safer. Rebuild: `python3 products/en-jewish-life/build.py`
  (xlsx + screenshots + JSON), then `python3 products/en-jewish-life/site_en.py` (pages).
- **Free tools**: bar mitzvah gift calculator (chai multiples, relationship/giver/attending/area, cites ReformJudaism.org,
  JewishBoston, Your Teen), bar mitzvah budget calculator (USD, itemized, every assumption editable, cites The Bash +
  Inquirer 2025), seder shopping calculator (same rates as the spreadsheet, injected at build; cites Chabad.org; printable).
- **Guides (7)**: multiples of 18, bar mitzvah timeline, bar mitzvah cost, how to host a seder, Jewish wedding checklist,
  hosting Rosh Hashanah dinner, Hanukkah party planning (Hanukkah 2026 starts Fri Dec 4: most time-sensitive page).
  Each has FAQ + sources + Article/FAQPage JSON-LD. Written by a sub-agent from search results; source pages themselves could
  not be opened (chabad.org etc. blocked in this sandbox), so facts rest on search summaries. Unsourced general-knowledge
  points are flagged softly in text ("customs vary, ask your rabbi").
- **SEO**: unique titles/descriptions, canonical, OG, JSON-LD (Product+Offer USD, SoftwareApplication, BreadcrumbList,
  FAQPage, Article). **hreflang**: in-page on English pages + reciprocal `xhtml:link` alternates in `sitemap.xml` for 7
  he↔en pairs (`docs/data/hreflang.json`); x-default = Hebrew. robots disallows `/en/thanks/`.
- Keyword research: `research/en-keywords.md` (relative volumes from SERP inspection; no paid tool available).

## Shared files touched (minimal, backward compatible)
- `docs/assets/checkout.js`: per-product `currency` (default ILS) + `price` (falls back to `price_ils`); SDK loaded once
  per page with that currency (a second currency on the same page shows a clear error, never a wrong charge); English UI
  strings + `en_US` locale + `en/legal/` links + redirect to `en/thanks/` when `<html lang="en">` or product `"lang":"en"`;
  PayPal brand_name = BRAND_LATIN on English pages. Hebrew behaviour unchanged (e2e regression check passes).
- `docs/assets/site.js`: English header/footer when lang=en; **language switch** in every header (follows
  `<link rel=alternate hreflang>` if present, else the other home). Fixed a `G` ordering slip during dev.
- `docs/assets/site.css`: `.lang-switch` styles; ≤520px shows short label (EN/עב), ≤440px header shows logo without brand
  text so nav + switch fit at 320–375px (Hebrew header too).
- `tools/site/build_sitemap.py`: hreflang alternates from `docs/data/hreflang.json`; `en/` priorities mirror Hebrew;
  robots `Disallow: /en/thanks/`.
- New product JSONs only; Hebrew `index.json` untouched (English catalogue in `docs/data/products/index-en.json`).

## Tests
`node products/en-jewish-life/e2e_en.js` → **ALL PASSED**: 22 pages × 375/1280 (lang/dir, English header+switch+footer,
no overflow, no JS errors, 1 h1, meta, canonical, USD only); test purchase of a planner (2 downloads, 200) and the bundle
(8 downloads, 200) → `/en/thanks/` with USD receipt; calculator sanity; Hebrew page still ₪39 + Hebrew, header fits at
320/375; **live PayPal SDK loaded with currency=USD&locale=en_US and buttons rendered**. Screenshots in `ops/reports/S-A/`.

## Decisions
- Bar mitzvah JSON slug is `bar-mitzvah-planner-en` (Hebrew already owns `bar-mitzvah-planner`); URL stays `/en/p/bar-mitzvah-planner/`.
- One currency per page (English pages USD only); English pages never show ILS products.
- English refund policy mirrors the Hebrew one (14 days, refund if faulty/not as described) without citing Israeli law.
- Seller line on English legal pages uses the seller name as in config (Hebrew script) + email; transliteration left to owner.
- Example prices in the seder shopping list are placeholders, labelled as such in the file.

## Owner actions / risks
1. **PayPal must accept USD.** SDK renders USD buttons, but an Israeli PayPal account may hold USD payments as "pending –
   accept/deny" if it has no USD balance. Owner: PayPal → Settings → Payments → "Block payments… / Allow payments sent to me
   in a currency I don't hold" → set to accept and keep/convert. One real $ test purchase recommended.
2. US buyers may see a foreign-transaction fee (mentioned in terms).
3. Google Sheets copy links (`sheets_copy_url`) not created (needs an owner Google account; contract forbids new accounts).

## Left / next
- Guides could be extended (bat mitzvah specific, break-fast menu, sheva brachot); Passover pages should be refreshed in
  February before the season. Re-check search phrases in Search Console after 3–4 weeks.
