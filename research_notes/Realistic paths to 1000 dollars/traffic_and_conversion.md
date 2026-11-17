# Traffic and Conversion Realities for a New Zero-Audience Site (tichnun.netlify.app)

Research method note: Research ran 2026-11-17. The session's network blocked direct page fetches from most hosts, including searchenginejournal.com, seroundtable.com, ahrefs.com, seranking.com, developers.google.com, dev.to, indiehackers.com and metehan.ai. Most figures below therefore come from search-result snippets and summaries, not full-page reads. They are marked "(snippet)" where the exact wording or methodology could not be checked. One fact was checked directly: the Public Suffix List file on GitHub.

## Q1. How long do new sites, especially on free subdomains, take to get indexed and get meaningful Google traffic? Are free subdomains treated differently?

### Takeaway
Being indexed within days to weeks is plausible. Meaningful Google traffic for a new site with no links usually takes months, and many new pages never rank at all. A *.netlify.app subdomain counts as its own "site" technically, but Google's John Mueller said in January 2026 that free subdomain hosts make SEO harder, because they share neighbourhood signals with spam.

### Cited Findings
- **Ahrefs study (May 2025, about 1M random URLs first crawled in September 2023):** reportedly only **1.74% of newly published pages reach the top 10 within one year**, down from 5.7% in its 2017 version (snippet; the page could not be fetched to confirm the numbers). — [Ahrefs via search summary](https://www.authorityhacker.com/how-long-to-rank-on-google/); see also [crowdo.net summary](https://crowdo.net/blog/how-long-to-rank-in-google-2025/)
- A "SEMrush 2025" figure of about **3.5 months for new domains to reach page 1** is repeated on blogs. I could not trace it to Semrush's own publication, so treat it as unverified. — [tryanalyze.ai](https://www.tryanalyze.ai/blog/how-long-does-it-take-to-rank-in-google-and-how-old-are-top-ranking-pages)
- Vendor estimates for indexing time conflict: "3–14 days", "about a month for <500 pages" and "a few days to a couple of weeks". None cites primary data. — [expertbeacon](https://expertbeacon.com/how-much-time-does-google-take-to-index-a-new-website/), [aiad.com.au](https://aiad.com.au/how-long-does-it-take-google-to-index-a-page)
- Older data (2013 poll): 54% of webmasters said Google indexed new sites within a week. — [SERoundtable](https://www.seroundtable.com/google-new-sites-index-16555.html)
- **Mueller, January 2026 (Reddit, reported by SEJ and SERoundtable):** "A free subdomain hosting service attracts a lot of spam & low-effort content." Free subdomain hosting makes SEO harder even when the site does everything else right, because search engines struggle to separate quality from the surrounding noise. He extended the caution to very cheap TLDs (snippet). — [Search Engine Journal](https://www.searchenginejournal.com/googles-mueller-free-subdomain-hosting-makes-seo-harder/565249/), [SERoundtable](https://www.seroundtable.com/google-warns-free-subdomain-hosts-40783.html), [Techwyse](https://www.techwyse.com/news/search-news/free-subdomain-hosting-seo-challenges)
- **netlify.app, github.io, vercel.app and pages.dev are all in the PRIVATE section of the Public Suffix List.** I checked this directly against raw.githubusercontent.com/publicsuffix/list (netlify.app is at line 15082). This lets search engines treat each subdomain as a separate site, but per Mueller the ecosystem still affects quality signals. — [Public Suffix List](https://github.com/publicsuffix/list), [Techwyse](https://www.techwyse.com/news/search-news/free-subdomain-hosting-seo-challenges)
- A DEV post claims Google applies "stringent crawl budget limitations and aggressive quality filters" to pages.dev, vercel.app and github.io. It gives no source, so treat it as unverified. — [DEV](https://dev.to/kpripper/the-technical-seo-implications-of-backlinks-originating-from-cloudflare-pages-pagesdev-go)
- A Netlify forum thread confirms *.netlify.app sites can be indexed. A later reply says Search Console can be used on netlify.app subdomains (verified through an HTML file or meta tag). — [Netlify Answers](https://answers.netlify.com/t/will-seo-work-for-xyz-netlify-app/72336)
- **Anecdotes on new sites (self-reported, 2025–2026):**
  - An Indie Hackers post title: "I built 140 SEO pages in 3 weeks, Google sent me one click". It was a rebuilt dead domain with static free tools. — [Indie Hackers](https://www.indiehackers.com/post/i-built-140-seo-pages-in-3-weeks-google-sent-me-one-click-Tpte8rPKC2689FwnsOvQ)
  - The "Thicket" project ran 25 AI-managed Next.js sites. Over 30 days it logged 382 total sessions across all 25 sites, about 7 organic sessions a week, $0 revenue, and reportedly only one page indexed by Google at that point. A 100-day follow-up still showed $0 revenue, and daily Google impressions crashed from about 2,600 to 34 within two days in early May. — [DEV (30 days)](https://dev.to/yonatan_naor_5642e43447ea/i-let-ai-agents-run-my-website-portfolio-for-30-days-heres-what-actually-happened-2ib4), [DEV (100 days)](https://dev.to/yonatan_naor_5642e43447ea/an-ai-ran-a-web-business-for-100-days-revenue-0-herex27s-the-full-audit-483i)
  - A PTO calculator suite reported 750 daily impressions within 10 days, with one page at position 8 and 755 impressions in its first week. This is impressions, not clicks. — [DEV](https://dev.to/john_3e45dd3f305a91bf327d/i-built-a-pto-calculator-suite-that-gets-750-daily-search-impressions-in-10-days-ch4)
  - An age/date calculator hub claimed 1,500 visits a week within 2 weeks. It is self-reported, and the domain history is unknown. — [DEV](https://dev.to/roxana_dinu_4a99c745e097c/-how-i-built-a-free-age-date-calculator-hub-from-zero-to-1500-visitsweek-in-2-weeks-4i26)
  - A developer launched in January 2026 and got "exactly zero visitors" from Google for 3 months. — [DEV](https://dev.to/tzhkai/i-spent-3-months-getting-zero-organic-traffic-then-one-fix-brought-40-users-in-24-hours-5a2)
  - Another site went "from 0 to 72 indexed pages in 2 months". The author says what mattered in months 1–3 was static rendering, internal links, content depth and schema, not backlinks. — [DEV](https://dev.to/serhii_kalyna_730b636889c/from-0-to-72-indexed-pages-in-2-months-what-google-actually-does-with-new-sites-3kca)
  - technologychecker.io (domain registered August 2025) reached 26,498 sessions a month, 13,334 of them from Google, about 12 months after launch. — [Seomator](https://seomator.com/customers/technologychecker)
- A small-business SEO guide says Search Console impressions often appear around months 3–4 and clicks begin around months 6–9. This is a practitioner heuristic. — [search summary, behindrankings.com](https://behindrankings.com/seo-for-a-new-website/)
- An oft-quoted stat (older Ahrefs, around 2017–2020): 96.55% of pages get zero Google traffic. — [behindrankings.com](https://behindrankings.com/seo-for-a-new-website/)

### Inferences
- Base case for tichnun.netlify.app with Google: some pages indexed within 1–4 weeks if Googlebot finds a link, and close to zero clicks (0–50 a month) for the first 30–60 days. By day 90, a few long-tail calculator pages *may* bring tens to low hundreds of visits a month. Case studies that claim fast results usually involve aged domains, Search Console submission or promotion, and they are survivorship-biased.
- The free subdomain is a real but unquantified headwind. No study puts a number on how much it penalizes ranking.

### Gaps
- No controlled experiment compares the same content on *.netlify.app and on a custom domain.
- The Ahrefs and Semrush time-to-rank figures could not be confirmed from the original pages because of network blocks.

## Q2. Is there a Google "sandbox" now? How do the 2024–2026 helpful-content, scaled-content-abuse and spam updates affect new AI-assisted sites?

### Takeaway
Google has never confirmed a "sandbox", but practitioners keep seeing a 3–6 month lag for new sites. The bigger 2024–2026 risk is the scaled content abuse policy. SE Ranking's experiment showed AI-written sites on brand-new domains ranking briefly and then vanishing within about 3 months.

### Cited Findings
- On 5 March 2024 Google introduced three spam policies: **scaled content abuse**, **expired domain abuse** and **site reputation abuse**. Scaled content abuse covers pages "generated for the primary purpose of manipulating Search rankings and not helping users", however they were produced (AI, human or mixed). — [Beyond Indigo summary](https://www.beyondindigopets.com/blog/how-google-is-cracking-down-on-scaled-content-abuse/), [PPC Land](https://ppc.land/scaled-content-abuse/)
- The August 2025 spam update tightened enforcement against scaled content abuse and site reputation abuse using SpamBrain improvements (secondary sources). — [Seeders](https://seeders.com/blog/august-2025-google-spam-update/), [DesignRush](https://news.designrush.com/google-2025-spam-update-complete-seo-penalties)
- An August 2026 spam update case study: a site with more than 1.5M indexed URLs dropped and was hit for "scaled content abuse". — [GSQi (Glenn Gabe)](https://gsqi.com/marketing-blog/august-2026-google-spam-update-case-studies/)
- One analyst's monitoring sample found 837 of 49,345 sites (about 1.7%) deindexed within days of a spam action. This is a third-party sample, not Google data. — [PPC Land](https://ppc.land/scaled-content-abuse/)
- **SE Ranking experiment:** 2,000 AI-generated articles on 20 brand-new domains. They ranked at first, then "completely disappeared from Google search results after three months". The articles produced 555,000 impressions and 2,300 clicks over the measurement period (snippet; one summary gives the dates as November 2024 to February 2025, another as June 2024 to July 2025, so the period is unclear). — [PPC Land](https://ppc.land/se-ranking-study-shows-ai-content-disappears-from-search-after-3-months/), [SE Ranking](https://seranking.com/blog/ai-content-experiment/)
- The "sandbox" is described as an unconfirmed filter, a term dating from about 2004. Claims that "80%+ of new sites" are affected trace to one unsupported vendor blog. — [webscraft](https://webscraft.org/blog/pisochnitsya-google-yak-zrozumiti-scho-sayt-prohodit-testuvannya?lang=en), [wisp.blog](https://www.wisp.blog/blog/the-google-sandbox-effect-why-your-search-traffic-drops-after-3-6-months)
- HackerNoon: "I launched two similar job boards: Google indexed one and rejected the other". This is an anecdote of quality and novelty filtering at the indexing stage. — [HackerNoon](https://hackernoon.com/i-launched-two-similar-job-boards-google-indexed-one-and-rejected-the-other)

### Inferences
- A pattern of initial impressions followed by a sharp drop (the Thicket 2,600→34 crash, SE Ranking's 3-month disappearance) is a realistic risk for many templated or AI-written pages. Forecasts should not extrapolate early impressions.
- Interactive calculators and spreadsheets with genuine utility are less likely to look like scaled content than mass-produced text guides. Bilingual near-duplicate pages should each carry real, distinct value.

### Gaps
- No official Google data exists on new-domain trust timelines.

## Q3. Bing, DuckDuckGo and IndexNow: how fast do URLs get indexed and bring traffic? What is Bing's share in Israel and the US?

### Takeaway
IndexNow can get pages into Bing within hours for known domains, but brand-new domains have sat unindexed for days. Bing's share in Israel is about 1% overall (about 3.5% on desktop), so Bing traffic to Hebrew pages will be tiny. In the US, Bing is about 7.5–8.4% of all-device search.

### Cited Findings
- **Israel (StatCounter, 2026 snapshots):** Google about 98%, Bing about 1.1–1.2% overall, Yandex 0.33% and DuckDuckGo 0.1%. Bing is about 3.4–3.6% on desktop and about 0.11% on mobile (July 2026). — [StatCounter Israel](https://gs.statcounter.com/search-engine-market-share/all/israel), [StatCounter Israel desktop](https://gs.statcounter.com/search-engine-market-share/desktop/israel), [StatCounter Israel mobile](https://gs.statcounter.com/search-engine-market-share/mobile/israel)
- **US:** Bing had 7.5% of all-device search in April 2025 (StatCounter via Statista). StatCounter's page showed 8.41% for desktop plus mobile through mid-2026. Desktop-only figures conflict widely between secondary sources (17%, 27.6%, 29%), and a claimed "54.68%" in one secondary source looks wrong. — [Statista](https://statista.com/statistics/1383614/bing-search-engine-market-share-united-states), [StatCounter US](https://gs.statcounter.com/search-engine-market-share/desktop-mobile/united-states-of-america/2025), [Search Engine Land](https://searchengineland.com/guide/bing-users), [Backlinko](https://backlinko.com/bing-users)
- **IndexNow tests:**
  - Tygart Media (server logs, June 2026): IndexNow got content into Bing "within hours". Without it, Bing discovery would take 24–72 hours. GPTBot found new content faster than Bing even without IndexNow. — [Tygart Media](https://tygartmedia.com/indexnow-speed-test-bing-gpt-google-crawl-comparison/)
  - Metehan Yesilyurt (2024): a **new domain** submitted via IndexNow was still unindexed on Bing after 3 days, while an already-indexed domain's URL was picked up in about 2 minutes. He suggests Bing treats new sites differently. — [metehan.ai](https://metehan.ai/blog/how-to-submit-index-your-page-on-searchgpt-an-experiement-results), [metehan.ai AI-citation test](https://metehan.ai/blog/what-happens-when-you-launch-a-website-without-google-or-bing-ai-citation-test/)
  - A Yoast-attributed retailer case: products indexed in 48 hours instead of 10 days (unverified). — [nicenic.com](https://nicenic.com/news/Google-vs-Bing-Which-Indexing-System-Truly-Delivers-Instant-Discovery-40704)
  - A Microsoft forum thread reports IndexNow returning "success" while Bing did not show the URLs. Accepting a submission does not mean the page is indexed. — [Microsoft Tech Community](https://techcommunity.microsoft.com/discussions/bing/rank-math-indexnow-returns-success-but-bing-doesnt-reflect-url-submissions/4532990)
- IndexNow accepts up to 10,000 URLs per POST. Google does not use IndexNow. — [blckalpaca](https://blckalpaca.at/fr/base-de-connaissances/seo-geo/seo-technique/indexnow-35-milliards-durl-par-jour-sans-google.md), [trysight.ai](https://www.trysight.ai/blog/indexnow-vs-traditional-indexing)

### Inferences
- IndexNow costs nothing to use (a key file plus one POST, with no account needed) and is worth doing. It also feeds Bing-backed AI answers such as Copilot and partly ChatGPT. Expected traffic: Bing plus DDG plus Yandex together are about 1.5% of Israeli search, so Hebrew Bing traffic is close to zero. For English pages aimed at the US, Bing is roughly 8% of search, and Bing results are reportedly less competitive for long-tail queries, but expect single to low double-digit visits a month in the first 90 days.

### Gaps
- No large-scale 2025–2026 controlled study of IndexNow latency for brand-new domains exists. No data shows DuckDuckGo traffic specifically for new sites (DDG largely uses Bing's index).

## Q4. How do pages get cited by AI search (ChatGPT, Perplexity, Copilot, Google AI Overviews)? What does AI referral traffic look like for small new sites?

### Takeaway
AI referrals are tiny: about 0.24% of all website traffic in 2025 and 0.32% in 2026. To be cited, a page generally has to be in a search index first (Bing or Google for ChatGPT and Copilot; ranking in Google's top 10 for AI Overviews). A new, unindexed, unlinked site should expect almost no AI referral traffic in 90 days.

### Cited Findings
- **SE Ranking:** AI referrals were 0.02% of total website traffic in 2024, 0.24% in 2025 and 0.32% in 2026. ChatGPT's share of AI referrals was 79.74% in 2025 and 74.78% in 2026. In 2026 Gemini had 11.56% and Perplexity 7.23%. — [SE Ranking](https://seranking.com/blog/ai-traffic-research-study/)
- **Ahrefs (about 35K sites, 2025):** AI sent about 0.1% of total referral traffic. ChatGPT accounted for 50% of it, Perplexity 30.7% and Gemini 17.6%. — [Ahrefs](https://ahrefs.com/blog/ai-traffic-research/)
- **Similarweb (June 2025, 1,000 domains):** ChatGPT sent 396.8M referral visits, 81.7% of the AI referrals to those sites. — [Digiday](https://digiday.com/media/in-graphic-detail-ai-platforms-are-driving-more-traffic-but-not-enough-to-offset-zero-click-search)
- **Ahrefs (August 2025):** only about 12% of URLs cited by ChatGPT, Gemini, Copilot or Perplexity rank in Google or Bing's top 10 for the same prompt. Perplexity had the highest overlap at 28.6%. **Google AI Overviews: 76% of cited URLs came from the top 10.** The explanation offered is "query fan-out". — [Ahrefs](https://ahrefs.com/blog/ai-search-overlap/)
- ChatGPT search reportedly relies mainly on Bing's index, with Google as a fallback (Aleyda Solís). Other testers found its citations resemble Google results, so this is not settled. — [Ahrefs](https://ahrefs.com/blog/ai-search-overlap/)
- Metehan test: a site outside both Google and Bing (IndexNow only) had 0 pages indexed after 3 days. In a separate test Perplexity retrieved his test page while ChatGPT "looked for search index". — [metehan.ai](https://metehan.ai/blog/what-happens-when-you-launch-a-website-without-google-or-bing-ai-citation-test/)
- GPTBot crawled new content faster than Bingbot in one 2026 server-log test. — [Tygart Media](https://tygartmedia.com/indexnow-speed-test-bing-gpt-google-crawl-comparison/)
- An agency claims a blank domain reached 265K impressions and 39 AI citations in 6 months. This is a marketing case study with an unclear amount of effort behind it. — [rsla.io](https://rsla.io/work/rsla-organic-growth)

### Inferences
- If a site gets 1,000 total visits, 0.3% AI share implies about 3 AI-referred visits. Even if AI referrals were 10 times the average for a utility site, they would not move the 90-day forecast. Being indexed in Bing (via IndexNow) is the main lever for ChatGPT and Copilot. Not blocking GPTBot, OAI-SearchBot and PerplexityBot in robots.txt costs nothing.

### Gaps
- No data on AI citations specifically for *.netlify.app or for brand-new sites. No data on AI referrals to Hebrew-language pages.

## Q5. Hebrew-language SEO: competition, market size, and whether Hebrew queries are easier

### Takeaway
No independent data shows Hebrew keywords are easier. Vendor sources call the Israeli market competitive, especially in commercial niches. The likely openings are long-tail, utility-type Hebrew queries where fewer purpose-built tools exist. Google holds about 98% of the market, so Hebrew SEO is Google SEO.

### Cited Findings
- Google holds about 98% of Israeli search share (StatCounter), and other guides cite ">95%". — [StatCounter Israel](https://gs.statcounter.com/search-engine-market-share/all/israel), [Ranktracker](https://www.ranktracker.com/blog/a-complete-guide-for-doing-seo-in-israel)
- Vendor guides describe "fierce" competition with high CPCs in tech and a "highly competitive" local market. Long-tail terms face less competition. Users often mix Hebrew and English in queries. — [Ranktracker Hebrew SEO](https://ranktracker.com/blog/a-complete-guide-for-doing-seo-in-hebrew), [Ranktracker local Israel](https://www.ranktracker.com/blog/a-complete-guide-for-doing-local-seo-in-israel), [Argos Multilingual](https://www.argosmultilingual.com/blog/hebrew-seo)
- Semrush's extended Israeli keyword database is available only through a premium partner (AdActive), which suggests Hebrew keyword data is thin in mainstream tools. — [Semrush News](https://www.semrush.com/news/249357-an-extended-keyword-database-for-israel-is-available-only-via-our-premium-partner-adactive/)

### Inferences
- Israel has about 10M people, so Hebrew search volumes per query are small (often tens to hundreds a month for long-tail terms). Lower competition does not translate into high traffic. An empty niche × small volume × a new free subdomain points to a low ceiling in the first 90 days.

### Gaps
- No Hebrew keyword-difficulty benchmarks. I found no data on the absolute volume of Israeli search queries.

## Q6. Realistic conversion rates (digital downloads, freemium tools with a one-time unlock, tip boxes) and typical first-month traffic

### Takeaway
Cold-traffic purchase conversion for digital products is roughly 0.5–3% of product-page visitors, and lower measured against all site visitors. Freemium "free to paid" benchmarks (3–8%) are measured on *signed-up users*, not visitors. Tip jars convert a tiny fraction of visitors, and about 21% of creators with tip links reportedly get even one tip a month. With tens to low hundreds of visitors in the first 90 days, expect $0 to a few sales.

### Cited Findings
- **Gumroad (InsightRaider, methodology unverified):** average sales-page conversion 3.2%, top pages 8–12%, underperformers 0.5–1%. Cold traffic 1.9%, email-list audiences 3.2%. The source itself says some figures are "planning assumption[s], not a measured average". — [InsightRaider](https://insightraider.com/en/data/gumroad-statistics-2026), [DEV / InsightRaider](https://dev.to/insightraider/how-to-sell-digital-products-on-gumroad-in-2026-146k-products-analyzed-4ddp)
- **Shopify (Littledata, about 2,800 stores; dated 2023 or 2025 depending on the source):** average 1.4%, top 20% at 3.2%, top 10% at 4.7%. Add-to-cart 4.6% and checkout completion 45%. Global e-commerce averages 1.4–2.7% (Statista, Dynamic Yield, Smart Insights Q3 2025 at 2.5%). Agency claims of 5–8% for digital products are unverified. — [Nudgify](https://www.nudgify.com/shopify-conversion-rate-benchmarks/), [Blend Commerce](https://blendcommerce.com/en-gb/blogs/shopify/ecommerce-conversion-rate-benchmarks-2025), [Thunderbit](https://thunderbit.com/blog/shopify-conversion-rate-statistics)
- **Freemium SaaS (per signup, not per visitor):**
  - ChartMogul: median free-to-paid 8%, but bimodal. 25% of products are below 2.5% and another quarter are at 10–15%. 3–5% is "good" and 8–12% "great". — [ChartMogul](https://chartmogul.com/reports/saas-conversion-report/)
  - First Page Sage (80+ SaaS clients, 2021–2025): freemium averages 3.7%, ranging from 2.6% to 5.8% by industry. — [CrazyEgg summary](https://www.crazyegg.com/blog/free-to-paid-conversion-rate/)
  - Lenny Rachitsky: self-serve freemium converts at 6–8%. — [Userpilot](https://userpilot.com/blog/freemium-to-premium)
- **Tips:** an unverified blog claims only 21% of creators with active tip-jar links receive at least one tip a month. Buy Me a Coffee charges a 5% fee plus card processing. — [voxbooster](https://voxbooster.com/blog/digital-tipping-creator-statistics-2026), [buycoffee.to](https://buycoffee.to/en/blog/how-much-do-you-actually-keep-from-a-donation)
- **First-month traffic examples:** the Thicket portfolio had 382 sessions across 25 sites in 30 days (about 15 per site) and $0 revenue over 100 days. The Indie Hackers 140-page tools site got 1 Google click in 3 weeks. — [DEV](https://dev.to/yonatan_naor_5642e43447ea/i-let-ai-agents-run-my-website-portfolio-for-30-days-heres-what-actually-happened-2ib4), [Indie Hackers](https://www.indiehackers.com/post/i-built-140-seo-pages-in-3-weeks-google-sent-me-one-click-Tpte8rPKC2689FwnsOvQ)

### Inferences
- A rough forecasting chain for a site with no promotion:
  - Visitors: 30 days about 0–100, 60 days about 20–300, 90 days about 50–1,000 (wide, right-skewed).
  - Share of visitors who reach a paid offer: perhaps 10–30%.
  - Purchase rate on cold traffic: about 1–2%.
  - Overall visitor→sale: about 0.1–0.5%.
  - Result: about 0–5 sales by day 90 in the base case. A $1,000 target would need on the order of 50–100+ sales at $10–20, which means roughly 10k–100k visitors. That is not plausible from organic search alone on this timeline.
- A one-time unlock inside a tool the visitor is already using may beat the download benchmark, because intent is shown at the moment of use. No data quantifies this.

### Gaps
- No credible benchmark for visitor→purchase on a "pay-to-unlock web tool" or a one-time unlock. No reliable tip-jar conversion per visitor. Gumroad figures come from a single unverified source.

## Q7. Without Search Console, how can Google still discover the site?

### Takeaway
Google discovers URLs mainly by following links and reading sitemaps. Without Search Console, the levers are: a `Sitemap:` line in robots.txt, links from pages Google already crawls (GitHub repos and READMEs, profiles, forums), and accurate `lastmod` dates. The sitemap "ping" endpoint no longer works. Note that netlify.app subdomains *can* be verified in Search Console with an HTML tag or file if that constraint is ever relaxed.

### Cited Findings
- Google deprecated the sitemaps ping endpoint in June 2023 because pings were "not very useful" and "the vast majority of the submissions lead to spam". Pings now return 404. Sitemaps can still be submitted "through robots.txt and Search Console", and Google asks for an accurate `lastmod`. — [Google Search Central Blog](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping), [SERoundtable](https://www.seroundtable.com/google-to-drop-support-for-sitemaps-ping-endpoints-35617.html)
- Search Console works for github.io project sites through HTML-tag verification. Netlify forum replies say the same for netlify.app subdomains. — [simplearyan.github.io](https://simplearyan.github.io/blog/indexing-github-pages-subdomain), [Netlify Answers](https://answers.netlify.com/t/will-seo-work-for-xyz-netlify-app/72336)
- Netlify serves duplicate URLs on deploy-preview and branch subdomains, which can create duplicate-content noise. Use canonical tags. — [Netlify Answers](https://answers.netlify.com/t/netlify-com-netlify-app-potential-duplicate-content-seo-issue/22726.md), [codesections](https://www.codesections.com/blog/netlify/)
- A practitioner says launching with 50+ pages would have sped up indexing. — [DEV QuickAgeCalc](https://dev.to/roxana_dinu_4a99c745e097c/-how-i-built-a-free-age-date-calculator-hub-from-zero-to-1500-visitsweek-in-2-weeks-4i26)

### Inferences
- The practical no-Search-Console checklist:
  - robots.txt with `Sitemap: https://tichnun.netlify.app/sitemap.xml`.
  - Correct `hreflang` between the he and en pages, plus self-canonicals.
  - IndexNow for Bing and Yandex, which also feeds ChatGPT and Copilot.
  - Links to the site from a public GitHub repo README and its "website" field (GitHub is crawled heavily).
  - Do not block AI crawlers.
- Link-based discovery without any external link could take weeks. One crawled inbound link is probably the single most important thing to get Google's first crawl.

### Gaps
- No measured data on how fast Googlebot follows a link from a new GitHub README. Practitioner consensus says days to weeks, but I found no source with numbers.
