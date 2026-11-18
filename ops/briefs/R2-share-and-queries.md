# Round 2: WhatsApp sharing + per-query English pages (branch ws/round2)
Read reports/Realistic paths to 1000 dollars.md (the research) and ops/STATUS.md. Site https://tichnun.netlify.app/ (Netlify, docs/ at root).

1. WhatsApp share everywhere it helps (Hebrew + English):
   - Every free calculator under docs/tools/** and docs/en/**/(calculators): after a result, a "שתפו בוואטסאפ" / "Share on WhatsApp"
     button (https://wa.me/?text=...) with a short natural message + a link that REOPENS THE SAME CALCULATION (encode inputs in the
     URL query/hash; the page must read them on load and compute). Never include personal names/data.
   - Small shared helper docs/assets/share.js (also a native navigator.share fallback on mobile, copy-link fallback on desktop).
   - Per-page og:image (Hebrew text preview) for the top 4 calculators so WhatsApp previews look good (generate PNGs 1200x630).
2. English per-query landing pages (US search intent), each genuinely useful on its own (not thin, not templated filler):
   - Seating cluster: "wedding seating chart template", "how to make a wedding seating chart", "seating chart for round tables",
     "bar mitzvah seating chart" → pages under docs/en/seating/ linking to the English seating tool (docs/en/apps/seating/).
   - Planner cluster: "bar mitzvah planning checklist" (printable timeline 12 months → day of), "bat mitzvah budget breakdown",
     "jewish wedding checklist", "passover seder checklist" → under docs/en/guides/ linking to the matching USD planner.
   - 8 pages total, 800–1500 words each, practical (checklists, tables, examples), cite sources where facts are stated.
   - JSON-LD (Article/HowTo where valid, BreadcrumbList), unique titles/descriptions, internal links, hreflang if a Hebrew twin exists.
3. Run python3 tools/site/build_site.py and ALL e2e suites: tools/site/e2e_test.js (pip install fastapi uvicorn), tools/apps/e2e_apps.js,
   tools/site/e2e_tipskit.js, products/en-jewish-life/e2e_en.js, products/hanukkah/test_e2e.js. Add a small test for share links reopening
   the same result. Push to ws/round2. No PR. Report ops/reports/R2.md, then send_message the manager (@parent) a summary.
