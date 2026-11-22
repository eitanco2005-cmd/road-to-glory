# Round 6A: Quality audit before Google indexes us (branch ws/quality)
Context: Google Search Console verified and sitemap (157 URLs) submitted on 2026-11-22. Research (reports/Realistic paths to 1000 dollars.md)
warns: new sites with many AI-written pages often rank briefly then get dropped (~3 months) under Google's scaled-content-abuse /
helpful-content systems. Goal: make every indexable page clearly worth indexing, BEFORE Google evaluates the site.
Read ops/PLAN.md §13 (focus = Israeli weddings), ops/STATUS.md.

1. Inventory all 157 URLs (docs/sitemap.xml) into research/content-audit.md with: topic, target query, word count, uniqueness vs other
   pages (near-duplicate check, e.g. shingle/Jaccard on text), has sources?, has original data/tool?, internal links in/out.
2. Decide per page: KEEP / IMPROVE / MERGE (301 via Netlify _redirects in docs/_redirects) / NOINDEX (meta robots noindex,follow +
   drop from sitemap). Be decisive: thin, templated, overlapping or off-focus pages with no unique value should be merged or noindexed.
   Never delete a page that has a product checkout; noindex is fine for weak supporting pages.
3. IMPROVE the top ~15 wedding pages (chatuna hub, kama-lasim pages, wedding-gift, wedding-cost, mechirim pages, seating/RSVP/invite
   product pages): specific numbers, worked examples, clear author/"updated on" date + methodology/sources box, remove generic filler,
   strong first paragraph answering the query, FAQ only where genuinely useful.
4. Technical: unique <title>/meta description everywhere (find duplicates), canonical tags correct, valid JSON-LD (no fake reviews/ratings),
   images with width/height + alt, mobile Lighthouse performance ≥ 90 on top 10 pages (run Lighthouse via Chromium at
   /opt/pw-browsers/chromium if available, else Playwright metrics), no broken internal links, sitemap only lists indexable canonical URLs.
5. Add an "About / מי אנחנו" page (honest: small Israeli project, how calculators work, sources policy, contact email from config).
6. python3 tools/site/build_site.py; run ALL e2e suites (list in ops/briefs/R4-wedding-focus.md + tools/site/e2e_wedding.js); update
   tests if pages were merged. Push ws/quality. No PR. Report ops/reports/R6A.md (counts per decision + reasoning), then send_message
   the manager (@parent). Another worker (ws/convert) edits product pages' buy areas in parallel: keep your product-page edits to text
   above/below the buy box and coordinate via minimal, mergeable changes.
