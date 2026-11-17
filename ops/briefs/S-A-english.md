# Stream A: English Jewish-life planners (branch ws/en)
Read ops/PLAN.md (§12) and ops/briefs/CONTRACT.md. Site: https://tichnun.netlify.app/ (Netlify, docs/ at root). Build an English
section under `docs/en/` (lang="en" dir="ltr", reuse the design system; header/footer must work in LTR; add an
English/Hebrew switch link). Products priced in **USD** (checkout.js must support per-product currency: add `currency`
to product JSON, default ILS; PayPal SDK must be loaded with the matching currency — if mixed currencies on one page are
hard, keep one currency per page). Build 4 products (xlsx, English, formulas, dashboard, instructions; adapt existing
Hebrew engines in products/wedding-planner & bar-mitzvah where possible):
1. Bar/Bat Mitzvah Planner ($19) 2. Jewish Wedding Planner ($24) 3. Passover Seder Planner (guests, menu, shopping list
scaled by guests, timeline, haggadah assignments) ($15) 4. Jewish Holiday Hosting Planner (Rosh Hashana, Sukkot,
Hanukkah, Purim, Shabbat menus/guest lists) ($15) + "Jewish Life Bundle" ($49).
Free tools for traffic: bar mitzvah budget calculator (USD), Passover seder shopping calculator (by number of guests),
"how much to give as a bar mitzvah gift" guide/calculator (US norms, cite sources, chai multiples).
6+ helpful English guides. JSON-LD, sitemap via build_site.py, hreflang between he/en where pages correspond.
Research US search phrases first (research/en-keywords.md). Test with e2e + Playwright 375/1280. Push ws/en. No PR.
Report ops/reports/S-A-english.md, then send_message the manager (@parent) a summary.
