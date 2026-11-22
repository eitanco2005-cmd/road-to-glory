# Status board

**Restarted 2026-11-17** (owner paused Nov 6–17) · Phase 2 (Get found) — live at https://tichnun.netlify.app/ (brand: תכנון פלוס) · 103 pages: Hebrew + English shop, 3 pay-to-export apps, Hanukkah, RTL dev kit

| Workstream | Worker session | Branch | State |
|---|---|---|---|
| R. Product research | session_01WwXrbNKGphm4dNn1Fu2Vqx | `ws/research` | done (merged) |
| W1 Platform | session_01WwXrbP2QqkhxopJnxwcVdC | `ws/platform` | done (merged) |
| W2 Event products | session_01WwXrbNB3jJnkLxJLxXpun9 | `ws/events` | done (merged) |
| W3 Money products | session_01WwXrbPbD4hErXvpu5XCHNa | `ws/money` | done (merged) |
| W4 Freelancer products | session_01WwXrbP9gQM5pgpiJPV3pjH | `ws/freelancer` | done (merged) |

| A. English Jewish planners | session_01WwXrbPq1XLRrnmchxqUaHS | `ws/en` | done (merged) |
| B. Pay-to-export apps | session_01WwXrbRBox2nqBk9W4FzQz7 | `ws/apps` | done (merged) |
| C+D. Tips/upsells + RTL kit | session_01WwXrbR2nUUh11PJf4AM8EV | `ws/tipskit` | done (merged) |
| E. Hanukkah pack | session_01WwXrbQhAm2zpZGSQCbvZty | `ws/hanukkah` | done (merged) |
| F. Kids worksheets | session_01WwXrbQ7yV2Qg4zc5wLVvth | `ws/worksheets` | DROPPED (research: free Ministry competition) |
| G. Invitation maker | session_01WwXrbPGbcrZijkXQqMQfy3 | `ws/invites` | done (merged) |
| H. Speech writer | session_01WwXrbNU6eoXkk2izTax4LB | `ws/speeches` | CANCELLED by owner |

**Money:** Revenue ₪0 · Fees ₪0 · Profit ₪0 / ₪3,600

## Log
- 2026-11-06: Strategy set (service-first, template pack second). Workers launched.
- 2026-11-06: Owner rule: no outreach. Pivoted to inbound-only self-serve digital products. A → storefront, C → marketplace research.
- 2026-11-17: Owner finished PayPal Business upgrade + Live app "Glory Store". Client ID saved in config/paypal.json. Worker R (session_01WwXrbNKGphm4dNn1Fu2Vqx, ws/research) researching Hebrew products. Workers A/B/C archived.
- 2026-11-17: Master plan written (ops/PLAN.md). Research merged.
- 2026-11-17: Phase 1 started: W1–W4 launched (contract in ops/briefs/CONTRACT.md).
- 2026-11-17: W1 platform merged: Hebrew site, PayPal + guest card checkout verified with live client id (no payment made), 33/33 e2e checks. Open: seller name/email for legal pages, sales-log hosting, GitHub Pages.
- 2026-11-17: W4 merged: עוסק פטור tracker + quote pack, ceiling + VAT calculators, 4 guides. Sitemap 16 URLs. Open: Google Sheets copy links.
- 2026-11-17: W2 merged: wedding + bar mitzvah planners, event bundle, 2 calculators, 4 guides.
- 2026-11-17: W3 merged. **Phase 1 build complete**: 6 products + 4 bundles, 6 free tools, 12 guides, 32-URL sitemap, full e2e ALL PASSED. Waiting on owner: repo public + Pages + push-to-main OK, seller name/email.
- 2026-11-17: Seller details filled (owner approved name + email for the site). Pushed to main for GitHub Pages.
- 2026-11-17: 🚀 SITE LIVE https://eitanco2005-cmd.github.io/road-to-glory/ — PayPal buttons render on live pages, legal pages show seller. Phase 2 started (QA + SEO workers).
- 2026-11-17: Owner decisions: no social media, no Grow for now, no HF token, no public sales tracking. Sales log endpoints stay empty (no-op). Profit tracking = PayPal emails; manager asks owner weekly (optional).
- 2026-11-17: Owner: never ask about sales; just report progress.
- 2026-11-17 21:00: P2 QA (facts fixed, honest copy, a11y, spreadsheet bug fixes) + P2 SEO (12 guides, 2 tools: net-salary budget, savings goal) merged and published. e2e ALL PASSED. Sitemap 47 URLs.
- 2026-11-17: Exposure: README links to site from GitHub; IndexNow key + tools/site/indexnow.py (Bing/DDG/ChatGPT search). Owner told: domain + Search Console are optional speed-ups, offered once, not pushed.
- 2026-11-17: Moved to Netlify https://tichnun.netlify.app/ (deploys from main/docs). Rebranded to תכנון פלוס (all pages + downloads). Old github.io URLs auto-forward via site.js.
- 2026-11-17: Owner: diversify. Launched streams A (English Jewish planners), B (pay-to-export apps), C+D (tips/upsells + RTL dev kit). See PLAN §12.
- 2026-11-17: Wave 2 launched: E (Hanukkah pack, urgent), F (kids/teacher worksheets), G (invitation maker).
- 2026-11-17: Wave 3 launched: H (speech & greeting writer, non-spreadsheet).
- 2026-11-17: Stream H cancelled by owner ("bad idea"); worker stopped and archived.
- 2026-11-17: Deep research done (reports/Realistic paths to 1000 dollars.md). Verdict: distribution is the binding constraint; $1k odds ≈1–2% (30d), 2–4% (60d), 5–8% (90d) under current rules. Portfolio: double down on seating-chart pay-to-export (he+en, WhatsApp share) + English USD planners; keep CV builder (differentiate), spreadsheets/calculators, RTL kit, tips cheap; invitation maker folded into wedding tools; Hanukkah = 2027 asset; DROP worksheets, mass AI pages, bounties, awesome-list PR campaigns. Next: WhatsApp share on all calculators, per-query English pages, IndexNow each deploy, GitHub repo polish, day-45 review (~Jan 1).
- 2026-11-17: Merged A (English /en/: 4 USD planners + bundle, 3 calculators, 7 guides) and G (invitation maker ₪19, 12 templates, WhatsApp share). 73 URLs. Risk noted: PayPal may hold USD payments for manual acceptance if the account is set to "ask" for unheld currencies.
- 2026-11-17: Merged E (Hanukkah: 6 products he/en, 2 calculators, hubs, guides) + home banners until Dec 12. checkout.js gained thanks_path. 87 URLs.
- 2026-11-17: Merged B (seating chart ₪29/$9 + CV builder ₪19, WhatsApp share) and C+D (tip jar on free tools, bundle upsells, RTL Landing Kit free MIT + Pro $24). All 5 e2e suites pass. 103 URLs. Wave 1–2 build complete.
- 2026-11-18: Round 2 launched (session_01WwXrbNG1skZriyvNmiH98U, ws/round2): WhatsApp share on all calculators + 8 English per-query pages (seating + planners).
- 2026-11-18: Merged round 2: WhatsApp share on 13 calculators (links reopen same result), 8 English per-query pages, og images. 6 e2e suites pass. 112 URLs. Guarded stale products/en-jewish-life/site_en.py main().
- 2026-11-18: Round 3 launched: 3A seasonal pre-positioning (budget 2027, Purim, Pesach 2027) + 3B link-earning (embeddable calculators, Israeli open data on GitHub).
- 2026-11-18: Merged 3B: 10 embeddable calculators (/embed/, /en/embed/) with attribution links + data-il/ open dataset (holidays 2025–30, VAT, osek patur ceiling, min wage, BL) with JS/Python helpers. 7 e2e suites pass. 115 URLs.
- TODO (from R3A, ws/seasonal): from 2026-12-20 add a home-page banner for docs/budget-2027/ (תקציב 2027, peak late Dec–Jan), replacing the Hanukkah banner that ends Dec 12. Later: Purim banner (docs/purim/) from ~2027-02-01, Pesach banner (docs/pesach/) from ~2027-03-01. Not added yet on purpose.
- 2026-11-18: Merged 3A seasonal: budget-2027 hub + savings challenge, Purim (planner ₪19, mishloach manot calculator, 3 guides), Pesach (seder planner ₪19, matza/wine calculator, cleaning checklist, 3 guides), spring bundle ₪29. Added Purim/Pesach calculators as embeds (12 total). All 8 e2e suites pass. 131 URLs. TODO Dec 20: budget-2027 home banner; after Dec 12: remove Hanukkah banners.
- 2026-11-18: FOCUS: single audience = Israeli weddings (PLAN §13). Round 4 launched (ws/wedding): wedding hub, cost calculator, gift sub-pages, RSVP app, timeline generator, ₪79 wedding bundle. Other sections frozen.
- 2026-11-18: Merged R4 wedding focus: chatuna/ hub (guest + couple paths), wedding-cost calculator, 8 kama-lasim pages, 3 guest guides, RSVP app (free 80, ₪29 unlock), timeline generator (+ICS), wedding bundle ₪79, wedding-first nav/home. 9 suites pass. 146 URLs.
- 2026-11-18: Private counter live: netlify/functions/hit.mjs (POST /api/hit → Netlify Blobs; bots + test sales skipped) + stats.mjs (GET /api/stats?days=N, header X-Stats-Token checked against a SHA-256 hash in code). Token held only in the owner-approved secure credential for tichnun.netlify.app.
- 2026-11-21: Check-in (delayed from Nov 19). Stats 7d: 5 visits, all Nov 18 22:35–22:46 UTC, home page, direct, US/DE/CA (likely bots/scanners or GitHub viewers), 0 since; 0 sales. Site healthy. Launched R5 wedding vendor price guides (ws/prices).
- 2026-11-21: Merged R5: chatuna/mechirim/ hub + 10 vendor price guides (sourced ranges; 27/69 rows rely on search extracts — spot-check later). 9 suites pass. 157 URLs. Env allowlist gained 14 Israeli research hosts (approved).
- 2026-11-22: Check-in. Stats 7d: 6 visits total, all home page/direct; Nov 21 11:59 UTC visit came minutes after a deploy (likely Netlify screenshot bot, like Nov 18 18:14). Real visitors ≈ 0, sales 0. Site healthy (157 URLs). Decision: no new worker this round — zero traffic signal means more pages add little now; conserve usage until search engines start sending visits. Next: Dec 13 banner removal, Dec 20 budget banner, Jan 1 review.
- 2026-11-22: Owner started Google Search Console (URL-prefix property https://tichnun.netlify.app/); HTML verification meta tag added to docs/index.html.
- 2026-11-22: Google Search Console VERIFIED (HTML tag in docs/index.html — never remove it) and sitemap.xml submitted (157 URLs). Expect Google indexing within days; first impressions in 1–3 weeks.
- 2026-11-22: Round 6 launched: 6A quality audit/pruning before Google indexing (ws/quality), 6B conversion readiness for wedding products (ws/convert).
- 2026-11-22: Merged R6B conversion: free samples (docs/samples/), before-you-buy blocks, p/rsvp-tracker + p/wedding-bundle (₪126→₪79 compare), funnel boxes after gift calculator/RSVP limit/seating watermark, clearer PayPal descriptions, thanks next steps. 10 suites pass. 159 URLs.
