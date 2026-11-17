# Stream B report: pay-to-export web tools (branch `ws/apps`)

Date: 2026-11-17. Status: **built, tested end-to-end in `?test=1`, pushed to `ws/apps`**. Not merged.

## What's built

| Path | What |
|---|---|
| `docs/apps/seating/` | Seating-chart planner (Hebrew RTL, mobile). Free: everything on screen + watermarked print/PDF. Paid ₪29 (`seating-chart`): clean PDF, XLSX export, printable table cards. |
| `docs/apps/cv/` | Hebrew/English CV builder. Free: form, live A4 preview, 4 templates, 5 accent colours, watermarked print/PDF. Paid ₪19 (`cv-builder`): clean PDF + DOCX. |
| `docs/apps/shared/` | `zip.js` (dependency-free ZIP writer/reader, XLSX writer, XLSX first-sheet reader, download helper), `unlock.js` (unlock state + purchase dialog), `apps.css`. |
| `docs/p/seating-chart/`, `docs/p/cv-builder/` | Product pages: unique title/description, OG, JSON-LD Product + SoftwareApplication + Breadcrumb + FAQPage, screenshots (PNG + WebP), "free vs full" table, buy box, FAQ, related links. |
| Guides (2 each) | `p/seating-chart/guides/how-to-seat-guests/`, `.../tables-and-seats/` (includes a tables calculator), `p/cv-builder/guides/how-to-write-cv/`, `.../cv-in-english/` (includes ATS section). Article + FAQ JSON-LD. |
| `docs/data/products/seating-chart.json`, `cv-builder.json` | `"unlock": true`, `"files": []`, plus `app`, `app_name`, `badge`, `image`. |
| `tools/apps/` | `e2e_apps.js` (Playwright E2E), `screenshots.js` (regenerates product screenshots), `build_pages.py` (regenerates product pages + guides). |

### Seating app features
Add guest (name, people count, side, group); paste a list (tabs/commas, header row detected, "משפחת כהן (4)" parsed);
import CSV (UTF-8 or windows-1255, quoted fields, `,`/`;`/tab) or XLSX (via `DecompressionStream`); round/rect tables
with seat drawing and occupancy; drag & drop with mouse and touch (long-press) plus tap-to-edit fallback; sides/groups
with colours and filters; search highlights guests on tables; "keep apart" pairs; conflicts (over capacity, keep-apart
violated) shown in red; auto-seat (keeps side+group clusters together, best fit, splits only when needed, respects
keep-apart); undo (Ctrl+Z); backup/restore JSON; demo data; printable view = table map + alphabetical entrance list.
Exported XLSX re-imports (tables are recreated).

### CV app features
Personal details, summary, experience, military/national service, education, skills, languages, custom sections;
add/remove/reorder items; separate Hebrew and English content with "copy Hebrew as a base"; templates
classic/modern/minimal/executive, single column with standard headings (ATS friendly); print/PDF keeps real text;
DOCX is real Word paragraphs (bidi for Hebrew, Heading 2 style for section titles), checked with python-docx and
LibreOffice.

## Unlock flow (as briefed)
- `docs/assets/checkout.js` (shared, minimal + backward compatible): a product with `"unlock": true` counts as
  deliverable; after capture (or the TEST button) it stores `localStorage["tp-unlocks"][slug] = {o, t, test}`, records
  the sale as before, shows "paid" with a link to the thanks page, and dispatches `window` event `site:unlocked`.
  **No redirect** for unlock products. File products are unchanged (E2E regression check: wedding-planner still
  redirects to the thanks page with downloads).
- `docs/thanks/index.html` (shared, minimal): for unlock products it stores the unlock too, says "the full version is
  open in this browser", hides the Excel how-to box and links back to the app. Opening the thanks link in another
  browser/device restores the unlock there (that's the "restore purchase" path).
- `apps/shared/unlock.js`: locked exports open a dialog with the buy box (`SiteCheckout.render()`), close-and-continue
  after payment. **Test-mode unlocks only count while the page runs with `?test=1`**, so a `?test=1` "purchase" does
  not unlock the normal site.
- Honest copy on the pages: the client-side lock is simple and bypassable; data never leaves the browser.

## Decisions
1. **No CDN libraries.** cdnjs/jsdelivr are blocked from this environment, and the apps are more robust without them:
   XLSX/DOCX are generated with a ~150-line ZIP writer (stored entries), XLSX import uses the browser's
   `DecompressionStream` (Chrome 80+, Safari 16.4+, Firefox 113+; older browsers get "save as CSV" message).
2. **PDF via print CSS**, not jsPDF/html2canvas: Hebrew shaping and RTL are correct, the CV PDF has selectable text
   (ATS), files are small. The user picks "Save as PDF" in the print dialog (copy says so). Watermark = fixed,
   repeated diagonal text + footer line on every printed page.
3. New catalogue category **`apps` ("כלים אונליין")** for both tools, with an optional product field **`badge`**
   (catalog.js + build_site.py fall back to "אקסל + Google Sheets"). `products/index.html` got an `apps` section.
4. Apps are **not added to bundles** (bundle thanks page lists files; unlock products have none).
5. Sitemap: `apps/` priority 0.9 (`tools/site/build_sitemap.py`). Ran `tools/site/build_site.py`, which re-rendered
   `docs/index.html`, `docs/products/index.html` and `docs/sitemap.xml` (generated; re-run after merging other streams).
6. Cross-links added: wedding-planner and bar-mitzvah-planner pages, the wedding RSVP/seating guide, guides index →
   seating tool / new guides.

## Shared files touched (all minimal)
`docs/assets/checkout.js`, `docs/assets/catalog.js` (badge + unlock deliverable), `docs/thanks/index.html`,
`docs/data/products/index.json`, `docs/products/index.html`, `docs/index.html` + `docs/sitemap.xml` (generated),
`tools/site/build_site.py` (badge), `tools/site/build_sitemap.py` (apps priority), `docs/guides/index.html`,
`docs/p/wedding-planner/index.html`, `docs/p/bar-mitzvah-planner/index.html`,
`docs/p/wedding-planner/guides/rsvp-seating-gifts/index.html` (one link each).
Expect a trivial merge on `index.json`, `sitemap.xml` and the pre-rendered catalog blocks if ws/en or ws/tipskit also
touched them: keep both sides, then re-run `python3 tools/site/build_site.py`.

## Tests
`node tools/apps/e2e_apps.js` → **ALL PASSED** (≈70 checks): manual add, paste with header, CSV with quoted comma,
tables, auto-seat, mouse drag & drop, undo, keep-apart conflict, free watermarked PDF (pdftotext), locked export →
dialog → TEST payment → no redirect → token stored → full badge, XLSX opened with openpyxl (3 RTL sheets), clean PDF
without watermark, table cards, XLSX re-import, thanks page for unlock product, test unlock ignored without `?test=1`,
real unlock restored via thanks link in a fresh browser; CV live preview, 4 templates, English LTR, watermark,
TEST purchase, DOCX via python-docx + LibreOffice render, clean PDF with real text; all new pages + home/products
return 200 with no `<main>` overflow and no JS errors at 375px and 1280px; product page purchase; file-product
regression; products page shows both apps live.
`tools/site/e2e_test.js` (W1) could not run here: it needs fastapi/uvicorn for the sales endpoint (pre-existing).

## What's left / notes for the manager
- Merge `ws/apps`, re-run `tools/site/build_site.py`, deploy, then a real ₪ purchase check on the live site (PayPal
  live flow is the same code path as other products; only the post-capture step differs).
- Offline the shared header overflows 375px slightly because Google Fonts can't load (fallback font is wider); with
  Assistant loaded it fits. Not changed (W1's file).
- Possible later: free tools list (`data/tools.json`) only links to `tools/<slug>/`, so the apps are not in the
  "כלים חינם" grid; could add a link field there if wanted.
- IndexNow: submit the 8 new URLs after deploy (`tools/site/indexnow.py`).

## Update 2 (manager: seating is the priority)
- **English seating tool**: `docs/en/apps/seating/` (LTR, hreflang ↔ `apps/seating/`), product `seating-chart-en`,
  **$9 USD** (my pick: ≈ ₪29, low-friction for a US "free seating chart maker" search). Same `app.js` as the Hebrew
  tool, language chosen by `<html lang>`; each language keeps its own saved chart and its own unlock. Page has
  SEO copy, how-to, FAQ + FAQPage/SoftwareApplication JSON-LD, og image `en/apps/seating/img/screen-1.png`.
  Listed in `docs/data/products/index-en.json` (Stream A's catalogue) with `page: en/apps/seating/`.
- **WhatsApp share + "chart ready" banner**: when everyone is seated with no conflicts, a banner offers the paid export
  (one click → purchase dialog), the free watermarked PDF, and "Share on WhatsApp" (`https://wa.me/?text=` prefilled
  with event name, guest/table counts and the tool link with utm tags; never guest names).
- **CV**: kept modest; product page now leads with clean RTL PDF (hero point + FAQ "why not Word / a free PDF
  converter").
- **Merged `origin/ws/en` into `ws/apps`** to build on Stream A's per-product currency/language checkout. Conflict in
  `checkout.js` resolved keeping both (unlock path now passes `en` → English messages, `en/thanks/` link).
  **Fixed a ws/en bug in `docs/assets/site.js`**: `G.lang` was set before `var G` was defined, which threw on every
  page (header/footer/catalog missing). One-line reorder; Stream A should take the same fix.
- **Needs Stream A** (not in ws/en yet): `docs/en/thanks/` must handle `"unlock": true` products like
  `docs/thanks/index.html` does (store `tp-unlocks[slug]`, link to `p.app`); `docs/en/legal/refund/` and `docs/en/`
  home are linked from the English tool page and don't exist yet in ws/en.
- Tests: `node tools/apps/e2e_apps.js` → 108 PASS (adds English USD flow, unlock isolation between products, LTR XLSX,
  English watermark/escort list, WhatsApp link content, Hebrew banner).
