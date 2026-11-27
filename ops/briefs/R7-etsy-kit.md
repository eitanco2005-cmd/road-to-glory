# Round 7: Etsy launch kit (branch ws/etsy)
Owner said "etsy" (2026-11-27). Owner will spend ~1 hour ONCE to open the shop and paste listings, then only answer rare buyer
messages. Everything must be copy-paste ready and dead simple. Israel is an Etsy Payments country (payout to Israeli bank).
Read ops/STATUS.md, reports/Realistic paths to 1000 dollars.md, products/en-jewish-life/, products/hanukkah/, products/seasonal-2027/.

Deliver folder etsy/ (committed) with:
1. etsy/GUIDE-he.md — the owner's step-by-step guide IN HEBREW, short numbered steps, exact button names (Etsy UI in English):
   sign up at etsy.com/sell, shop language English, country Israel, currency USD, shop name (give 3 available-looking options,
   recommend one; English brand, e.g. "TichnunPlus"/similar — check availability is impossible, so give backups), how Etsy's
   onboarding forces the FIRST listing (paste listing #1), payments/bank setup (Israeli bank, ID verification), billing card,
   2FA, then paste remaining listings. Include: how to upload digital files (Etsy limit: 5 files per listing, 20MB each — verify),
   where to answer messages, and what to do if Etsy asks for ID or holds the shop for review.
2. etsy/shop/ — shop title, announcement, About section, shop policies text (digital downloads, no refunds except broken files
   policy consistent with our site's legal/refund, contact), FAQ, and 5 ready reply templates for common buyer messages.
3. etsy/listings/NN-slug/ for 10–12 listings, priority by seasonality NOW: (1) Hanukkah Activity Pack (Hanukkah starts Dec 4 —
   listing #1, make it the onboarding listing), (2) Hanukkah Party Planner, (3) Hanukkah bundle, (4) Bar/Bat Mitzvah Planner,
   (5) Jewish Wedding Planner, (6) Wedding Budget Planner (English — create from the Hebrew wedding planner engine if no English
   version exists), (7) Printable Wedding Seating Chart template (English xlsx + printable PDF; create if needed), (8) Passover
   Seder Planner, (9) Jewish Holiday Hosting Planner, (10) Jewish Life Bundle, (+ optional 11–12 if strong).
   Each listing folder: listing.md with Title (≤140 chars, front-load keywords), 13 tags (each ≤20 chars), description (clear
   "what you get", "how it works", "instant download", file formats, compatible with Excel/Google Sheets/print, no physical item),
   price in USD (research Etsy competitor prices; typical $5–15 single, bundles more; price to sell, not to max margin),
   category + attributes suggestion, "Who made it / AI disclosure" answer (designed by us; AI-assisted — disclose per Etsy policy),
   and files/ (the digital download files, ≤20MB each, ≤5) + images/ (7–10 images, 3000x2250 px 4:3 JPG: hero mockup with title
   text, what's inside, 3–4 real screenshots of pages/sheets, how-it-works, compatibility). Render with Playwright/PIL.
   IMPORTANT Etsy rules: files and images must NOT contain links/ads pointing to our website or PayPal (no off-Etsy selling);
   remove site links/footers from the Etsy versions of files. No fake reviews/claims.
4. etsy/CHECKLIST.md — one-page checklist the owner ticks while pasting.
5. Verify: every file opens (LibreOffice recalc 0 errors for xlsx, PDFs render), images exact size, titles/tags within limits
   (write a validator etsy/validate.py and run it). Push ws/etsy. No PR. Report ops/reports/R7.md, then send_message the manager (@parent).
