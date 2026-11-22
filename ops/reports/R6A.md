# R6A: Quality audit before Google indexing (branch ws/quality)

**Bottom line:** the sitemap went from 157 to 115 URLs. 38 weak pages are now noindex,follow and 5 are 301-merged into stronger pages; I deleted nothing else. 39 wedding pages got a "who wrote this / how we checked" box, and 4 got real content fixes. There is a new About page (`about/`). All 12 top pages now score 91–100 on mobile Lighthouse performance, up from 70–95. Every page-level decision is in `research/content-audit.md`.

## Decisions (157 baseline URLs)
| Decision | Count | What |
|---|---|---|
| KEEP | 75 | Product pages with checkout, free calculators, substantive guides outside the focus (money guides 1,250–1,350 words with 4–5 sources, English guides 950–1,450 words with 3–6 sources), data-il, legal |
| IMPROVE | 39 | Wedding focus pages: hub, gift calculator + 8 kama-lasim pages, cost calculator, timeline, price hub + 10 vendor pages, 3 guest guides, 9 couple guides, 4 wedding product pages |
| MERGE (301) | 5 | wedding-budget-2026 → tools/wedding-cost/ (I moved its budget-split content there); bar-mitzvah-cost-2026, osek-patur-ceiling-2026, renovation-cost-2027 → their calculators; family-budget-2027 → budget-2027/ |
| NOINDEX | 38 | 6 devkit demo templates (fake brand copy, html/tailwind twins 80–100% identical), 4 thin hubs (legal/, en/tools/, en/seating/, en/planners/), en/hanukkah/terms (duplicates en/legal/terms), 3 app UI pages that compete with their own landing pages (apps/seating, apps/invite, apps/cv), 15 seasonal Hanukkah/Purim/Pesach hubs + articles (<600 words, no sources, generic), 9 short guides outside the focus (CV, quotes, renovation quotes, fixed expenses, income tracking, bar-mitzvah timeline) |

Reasoning: Google judges the whole site. Weak pages outside the focus with no tool, data or sources add the most risk of a "scaled content" verdict, and they had almost no chance of ranking anyway. The seasonal products and calculators themselves stay indexed; only the thin articles and hubs around them are out. To bring a page back: improve it, remove it from `docs/data/seo.json` → `noindex`, then rebuild.

## What changed
- **Rules applied on every build:**
  - `docs/data/seo.json` + `tools/site/seo_rules.py`, called from `build_site.py`, apply the noindex tag (the sitemap then skips the page) and write `docs/_redirects` as forced 301s.
  - The same step rewrites internal links that point at merged URLs, strips hreflang links that point at noindexed pages (the sitemap skips those pairs too), and switches the site font to a non-blocking `display=optional` load.
  - A merged page that an old generator recreates gets noindexed automatically and stays shadowed by the 301.
- **New tools:**
  - `tools/site/audit_content.py` writes the per-page metrics.
  - `tools/site/seo_check.py` is the technical gate: unique titles and descriptions, canonical equals the page's own URL, JSON-LD parses, no rating/review markup, every img has size and alt, no broken internal links, no noindexed or redirected URL in the sitemap. It now reports 0 errors on 115 URLs. The only warnings are 19 long English or off-focus titles, which I left alone.
  - The one duplicate-title case was the devkit demo pairs, which are now noindexed.
- **Content:**
  - `tools/wedding/trust_box.py` adds the box to 39 pages: who wrote it, the review date, a method note by page type, sources policy, a link to about/ and a "found a mistake? write to us" mailto.
  - Gift calculator: all coefficients are now published, plus a worked example (Thursday couple = ₪800, mid-week ₪750, Friday ₪600).
  - Cost calculator: new `#budget-split` worked split (₪184.9k, 68% food) and the "set a ceiling first" steps from the merged guide.
  - Hub: the first paragraph now answers both core queries with numbers.
  - wedding-save-money: a stale 60% claim fixed to 68%, with a link.
  - Most wedding pages were already specific and sourced (from R4/R5), so I didn't rewrite them. I removed no FAQs: they answer distinct questions.
- **About page** (`about/`, "מי אנחנו"): states that this is a small Israeli project run by איתן כהן, explains how the calculators work, gives the sources policy (including an honest note that AI is used for drafting while numbers stay sourced), says there are no affiliates and no fake reviews, and gives the contact email from config. It is linked from the footer (site.js) and from every trust box.
- **Performance (mobile Lighthouse 12.2.1, local server):**

  | Page | Before | After |
  |---|---|---|
  | home | 94 | 100 |
  | chatuna/ | 93 | 99 |
  | wedding-gift | 79 | 100 |
  | wedding-cost | 95 | 98 |
  | kama-lasim/zug | 79 | 100 |
  | mechirim/ | 91 | 100 |
  | mechirim/ulam | 75 | 100 |
  | apps/rsvp | 81 | 95 |
  | p/seating-chart | 84 | 98 |
  | p/wedding-planner | 71 | 91 |
  | wedding-timeline | 93 | 100 |
  | p/invitation-maker | 70 | 99 |

  CLS had three causes:
  - The header injected by JS. Fixed by reserving its height: `#site-header:empty`.
  - The hero buy box filled by checkout.js. Fixed by reserving its height: `.hero .buy:empty{min-height:370px}`.
  - The Google Font swap. Fixed with a non-blocking font CSS load plus `display=optional`.

  apps/invite keeps the blocking fonts because it needs them for canvas drawing.
- **Tests:** e2e_wedding gained an R6A block. It checks that the worked examples equal what the calculators output (that is what makes the About page's claim true), plus the about page and footer link, trust boxes, the 301 and sitemap removal, and that no noindexed page is in the sitemap.

## Coordination with ws/convert
- I did not touch the buy boxes. On the product pages my only edits are the trust box appended right before `</main>` and the font `<link>` in `<head>`.
- One shared-CSS rule touches their area: `.hero .buy:empty { min-height: 370px }` in site.css, which stops the hero jumping while checkout.js renders. If ws/convert changes the buy box height a lot, adjust that number.
- apps/seating and apps/invite are now noindex,follow. Users still reach them from the landing pages, and only the landing pages compete in search.

## Caveats / follow-ups
- Some old page generators were run once and are not part of build_site.py. Several of them still link the merged URLs; seo_rules rewrites those links at build time. The generators of the kama-lasim pages (`tools/wedding/build_gift_pages.py`), of tools/wedding-gift, and of wedding-cost do not contain my content edits, so re-running them would drop those edits. Treat the `docs/` HTML of those pages as the source of truth.
- Before each season, consider re-indexing improved Hanukkah 2027, Purim and Pesach articles. They would need sources and a tool tie-in first.
- In Search Console, expect "Excluded by noindex" for 38 URLs and "Page with redirect" for 5. Both are intended.

## Verification
- `python3 tools/site/build_site.py` produces a 115-URL sitemap. `python3 tools/site/seo_check.py` reports 0 errors.
- All 9 e2e suites pass on the final build (number of passed checks in brackets): e2e_test (32), e2e_apps (111), e2e_tipskit (102), e2e_en (110), hanukkah test_e2e (78), e2e_share (195), e2e_embed (152), e2e_seasonal (67), e2e_wedding (303).
- I updated two tests on purpose:
  - e2e_seasonal now expects the noindexed seasonal pages to be absent from the sitemap.
  - e2e_wedding has the new R6A block.
