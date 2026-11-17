# W1 Platform (branch ws/platform)
Read `ops/briefs/CONTRACT.md`. Build:
1. Design system: `docs/assets/site.css` (clean, trustworthy, warm; RTL; mobile-first; light+dark), `site.js`
   (shared header/nav/footer injected into `<header id="site-header">`/`<footer id="site-footer">`).
2. Home page `docs/index.html` ("Glory" brand, Hebrew tagline about smart planning tools), product grid from
   `docs/data/products/*.json` (keep a static index `docs/data/products/index.json` listing slugs; product workers'
   files may not exist yet — create placeholder JSONs for the 6 products + 4 bundles from PLAN.md section 3).
   Also `docs/products/index.html` (catalogue) and a tools index `docs/tools/index.html`.
3. `docs/assets/checkout.js`: PayPal JS SDK (client id from config, currency ILS, intent capture),
   createOrder with product title/price from JSON, onApprove → capture → record sale → redirect to thanks page.
   Handle bundles. Include a TEST mode (`?test=1`) that skips PayPal and simulates success for QA.
4. `docs/thanks/index.html`: shows the order's download links + Sheets copy link, receipt-like summary, support note.
5. Sales log: `docs/assets/sales.js` with `recordSale({orderId, slug, amount, currency})` that POSTs JSON to a URL in
   `docs/assets/config.js` (`SALES_ENDPOINT`, may be empty → no-op). Also `recordVisit(path)` to `VISITS_ENDPOINT`.
   The manager will host the endpoint; also write `tools/site/sales_endpoint/` — a tiny FastAPI app (Dockerfile,
   suitable for a Hugging Face Docker Space) that appends sales/visits to a JSON-lines file and exposes
   GET /summary protected by a token from env var. Document deploy steps in its README.
6. Legal pages in Hebrew (`docs/legal/`): terms of sale, digital-goods cancellation/refund policy per Israeli
   Consumer Protection law, privacy policy, accessibility statement. Seller name placeholder `SELLER_NAME`,
   contact placeholder `SELLER_EMAIL` (manager fills).
7. `docs/sitemap.xml` generator script `tools/site/build_sitemap.py`, `robots.txt`, `404.html`, favicon (SVG).
Verify checkout in TEST mode end to end with Playwright; screenshot home at 375/1280. Push to ws/platform.
