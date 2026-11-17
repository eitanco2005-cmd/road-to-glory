# P2 SEO content (branch ws/seo)
Site is LIVE at https://eitanco2005-cmd.github.io/road-to-glory/. Read ops/PLAN.md, research/products.md, ops/briefs/CONTRACT.md.
Goal: Google traffic without any promotion. Build:
1. Keyword map (research/keywords.md): for each product cluster, 10 Hebrew search phrases people really use (check Google autocomplete/"people also ask" via web search), grouped by intent.
2. 12 new genuinely useful Hebrew guide articles (1,000+ words, original, practical, no fluff, cite sources) under a new `docs/guides/<slug>/` section with a guides index page, internal links to the matching free tool and product. Prioritise the January "תקציב 2027" cluster and wedding cluster.
3. 2 new free tools that match high-intent searches (e.g. net salary → monthly budget, savings goal calculator) under `docs/tools/<slug>/`, added to docs/data/tools.json.
4. Technical SEO: JSON-LD (Article, FAQPage only where valid, BreadcrumbList), unique titles/descriptions, internal links from home, run `python3 tools/site/build_site.py` so sitemap updates.
No fake reviews, no keyword stuffing, no AI-spam patterns. Run e2e test before pushing. Report in ops/reports/P2-seo.md. Push to ws/seo. No PR.
