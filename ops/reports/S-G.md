# Stream G report: Hebrew invitation maker (branch ws/invites)

## Built
- **App** `docs/apps/invite/` (client-side, no backend, mobile-first, Hebrew RTL)
  - `templates.js`: 12 original designs drawn with Canvas 2D (no images, no third-party art): wedding ×5 (קלאסי זהב,
    ענפי זית, קשת בוהו, לילה מוזהב, אקוורל ורוד), bar/bat mitzvah ×4 (פסי טלית, אבן ירושלמית, פרחים בפסטל, מודרני),
    birthday/brit ×3 (בלונים, ברית/בריתה, יום הולדת חגיגי). 3 palettes each + free accent colour. Auto-fit text layout.
  - 12 free OFL Hebrew Google Fonts (Frank Ruhl Libre, David Libre, Bellefair, Noto Rashi Hebrew, Suez One, Secular One,
    Karantina, Amatic SC, Varela Round, Rubik, Heebo, Assistant), selectable for headings/body.
  - `hebdate.js`: Hebrew date in letters from the Gregorian date via Intl Hebrew calendar ("ביום חמישי, ה׳ בסיוון התשפ״ז"),
    toggles for weekday / Hebrew / Gregorian, and "אור ל…" (after sunset → next Hebrew day).
  - Form: opening line, title, names (+ size slider), wording (with ready-made wordings per category), date, hours,
    venue, address, two parents columns, footer. Text per category kept separately; autosaved in localStorage.
  - Free: watermarked on-screen preview + 600px watermarked PNG download.
  - Paid ₪19 (unlocked): clean PNG 2000×2828, Web Share button (phones), PDF: A5 or A6 with 3 mm bleed at 300 DPI,
    A4 home sheet 2-up or 4-up with crop marks. PDF is written by our own tiny writer (`pdf.js`, JPEG/DCTDecode) — no
    jsPDF/CDN dependency (cdnjs was also unreachable from this sandbox).
- **Unlock**: `docs/assets/unlock.js` did not exist on main, so I wrote `docs/apps/invite/unlock.js` (TPUnlock.get/has/set/clear,
  key `tp-unlock:<slug>` = `{o, t, test}`). Test-mode unlocks only count on pages opened with `?test=1`.
- **Product** `docs/data/products/invitation-maker.json` (`"unlock": true`, `"app": "apps/invite/"`, `"badge"`), added to
  `data/products/index.json` (category events). Product page `docs/p/invitation-maker/` (SoftwareApplication + FAQ +
  Breadcrumb JSON-LD, OG, 4 screenshots in `img/`).
- **Guides** under `docs/p/invitation-maker/guides/`: `wedding-invitation-wording` (נוסח הזמנה לחתונה),
  `bar-mitzvah-invitation-wording` (נוסח הזמנה לבר/בת מצווה), `print-invitations` (הדפסת הזמנות).
- Links added from wedding-planner and bar-mitzvah-planner product pages. Ran `tools/site/build_site.py` (sitemap now 52 URLs,
  catalog pre-render refreshed in index.html / products/index.html).

## Shared-file changes (small, backward compatible)
- `assets/checkout.js`: `isDeliverable` also true for `unlock: true`; `finish(..., product)` — for unlock products it stores
  `tp-unlock:<slug>` in localStorage, dispatches `tp:unlocked` on window, records the sale, and **stays on the page**
  (shows "ההורדות נפתחו" + link to the thanks page). Normal products unchanged. Same key format as unlock.js, so the
  ws/apps worker (seating/CV) can use the same mechanism — the manager may want to keep one copy of this hunk when merging.
- `assets/catalog.js` + `tools/site/build_site.py`: card badge uses optional `p.badge` (default "אקסל + Google Sheets");
  catalog `deliverable()` accepts `unlock: true`.
- `thanks/index.html`: product with `unlock` + `app` and no files shows "חזרה למעצב ולהורדות" instead of "files in preparation".

## Tested (Playwright, local server, ?test=1)
- 375 and 1280 px: no horizontal scroll on app, product page, guides, products, wedding page; no broken internal links; no JS errors.
- App: template switch, form edits, Hebrew date, free PNG download, TEST purchase → unlock without redirect, clean PNG,
  all 4 PDFs (validated with pdfinfo: A5+bleed 154×216 mm, A6+bleed 111×154 mm, A4 landscape/portrait), unlock persists
  on reload; test unlock not honoured without ?test=1; product-page purchase → thanks page → app unlocked.

## Decisions / notes
- Client-side unlock is bypassable by design (as the brief accepts); unlock is per browser. FAQ says so honestly and tells
  buyers to write with the order number if they change device.
- Download file names are ASCII (`invitation-<template>-<date>.png`): Chromium dropped Hebrew names for blob downloads.
- No photo/logo upload (FAQ says "not yet"). Possible next steps: photo upload, parasha auto-fill, RSVP QR code.
- og:image uses `p/invitation-maker/img/screen-1.png` (template collage).
