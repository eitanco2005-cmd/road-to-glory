# R3B: Earn links without outreach (branch `ws/linkbait`)

All four items in `ops/briefs/R3-links.md` are done. Nobody was contacted and nothing was published to npm or PyPI. The sitemap grew from 112 to 115 URLs: `embed/`, `en/embed/` and `data-il/`. The embed pages themselves are noindex.

## 1. Embeddable calculators

- **10 embeds.** Six are Hebrew under `docs/embed/<slug>/`: wedding-gift, vat-calculator, osek-patur-ceiling, net-salary-budget, budget-503020 and sufganiyot-calculator. Four are English under `docs/en/embed/<slug>/`: bar-mitzvah-gift, bar-mitzvah-budget, seder-shopping-calculator and latke-calculator.
- **Size:** each embed is 14–21 KB, under the 40 KB limit. They load no site header or footer, no site.js and no web font.
- **Layout:** RTL for Hebrew and LTR for English. Each one works at 375 px with no horizontal scroll.
- **Generator:** `tools/site/build_embeds.py`. It lifts the calculator's own markup and script from the live page, so an embed always computes exactly like the page. It prunes `site.css` down to the rules the embed uses and turns relative links into absolute links that open in a new tab.
- **Rebuilds:** `build_site.py` now calls the embed generator, so embeds can't drift from their pages.
- **Auto-height:** the embed posts `{type:"tichnun:embed-height", slug, height}` to the parent page. The posts fire on load, from a ResizeObserver, and on input, change and toggle events. The snippet's listener checks the message origin and matches the right iframe by `e.source`.
- **Attribution, in two places:**
  - Inside the iframe: «מחשבון: תכנון פלוס» (English: "Calculator by תכנון פלוס"). It is a normal followed link that opens the full calculator.
  - Under the iframe, in the copy-paste snippet: a plain `<a>` to the calculator page. This is the one that can count as a backlink, because a link inside an iframe belongs to our domain, not the host's.
- **Hubs:** `docs/embed/` ("הוסיפו מחשבון חינם לאתר שלכם") and `docs/en/embed/`. Each card has the copy-paste code, a copy button and a live preview that loads when opened. The hubs have:
  - how-to steps for WordPress, Wix and Squarespace
  - simple terms: free for any site, keep the credit line
  - an FAQ, plus ItemList and FAQPage JSON-LD
  - hreflang between the two hubs, with the pair added to `hreflang.json`
- **Theme:** embeds default to a light theme, so they don't turn dark on a light host page when the visitor's device is in dark mode. Host sites can add `?theme=dark` or `?theme=auto` to the URL.
- **Embed links on the site:**
  - Each of the 10 calculator pages has a «הטמיעו את המחשבון הזה באתר שלכם» / "Embed this calculator" link right after the calculator, between `<!-- embed-link -->` markers.
  - The Hebrew and English tools index pages link to the hubs and to the data page.

## 2. Open data (`data-il/`, data CC0, code MIT)

- **Holidays 2025–2030.** 144 rows with Hebrew and English names, Hebrew dates, sunset/dawn start, eve date and statutory rest day.
  - Computed by `data-il/tools/hebrew_calendar.py` (arithmetic calendar, no dependencies) with the Israeli rules for one-day Yom Tov, the moved memorial and Independence days, and fasts that fall on Shabbat.
  - **Verified** by `data-il/tools/verify_holidays.py` against two independent libraries, hdate and pyluach, plus fixed anchor dates: 249 checks, 0 mismatches.
- **Rates, one source URL per row, plus `checked` and `verification` fields** (`2+ sources` or `1 source`). The values live in `data-il/tools/rates_sources.py`:
  - VAT history since 1976 (18 rows; 18% since 2025-01-01).
  - Osek patur ceiling 2016–2026 (122,833 ₪ for 2026).
  - Minimum wage since April 2015 (6,443.85 ₪ and 35.40 ₪/hour from 2026-04-01).
  - Bituach Leumi 2026 basics: average wage 13,769 ₪, threshold 7,703 ₪, maximum insurable income 51,910 ₪, and employee, employer and self-employed rates.
- **Rows left out on purpose:** rows that couldn't be confirmed, such as minimum wage before April 2015.
- **Sourcing caveat:** gov.il, Wikipedia and Kolzchut can't be reached from this container, by shell or by fetch. The rate values come from the sources' published text as returned by web search, not from full page reads.
  - Most rows agree across two or more sources. Rows with a single source say so (VAT 1977 and 1982; osek patur 2016, 2017 and 2021).
  - Known conflicts are written in each row's `note`: the 2005 VAT date (1 vs 15 September), and one site showing 122,400 for the 2026 osek patur ceiling.
- **Helpers, no dependencies:**
  - JS: `data-il/js/israel-data.js`, which works in the browser or in Node. Functions: `isIsraeliHoliday`, `isRestDay`, `nextHoliday`, `vatRate`, `addVat`, `removeVat`, `osekPaturCeiling`, `minimumWage`.
  - Python: the `israel_data` package, with the same functions and doctests. Installed with `pip install "git+…#subdirectory=data-il/python"`, which I tested in a clean virtual environment. Its data block is generated.
- **README and license:** `data-il/README.md` in English and Hebrew covers install-from-GitHub, the jsDelivr CDN, usage and links to the live calculators. The license file is `data-il/LICENSE`.
- **Site page:** `docs/data-il/` shows the downloads (JSON + CSV, served from the site), upcoming holidays, the rate tables with sources, code examples and an English section.
  - It carries DataCatalog JSON-LD plus five **Dataset** JSON-LD blocks (license, creator, distribution, coverage) and FAQPage JSON-LD.
  - The CSV files are UTF-8 with a BOM so Excel shows the Hebrew correctly.
- **Rebuild:** `python3 data-il/tools/build.py` regenerates everything; `build_site.py` runs it too.

## 3. README

The root README has two new sections, "Israeli open data" and "Embeddable calculators". Both sit above the RTL kit section.

## 4. Build and tests

- `python3 tools/site/build_site.py` runs clean (115 URLs).
- **New test, `tools/site/e2e_embed.js` (152 checks, ALL PASSED).** For each of the 10 embeds:
  - the size limit and noindex
  - it renders in an iframe on a foreign host page using the hub's exact snippet
  - the attribution link is present inside the iframe and in the snippet, with no nofollow
  - the postMessage height matches the content, and still matches after the content grows
  - the same inputs give the same results as the full page
  - no JS errors
  - no horizontal scroll at 375 px
  - the calculator page links to its embed card

  It also checks the hubs (cards, copy button, live preview, JSON-LD) and the data page (10 downloads parse, 5 Dataset JSON-LD blocks, the JS helpers work in the page).
- Existing suites all pass: e2e_test, e2e_apps, e2e_tipskit, e2e_en, hanukkah test_e2e and e2e_share.
- e2e_en crawls every `en/` page and expects site chrome, so at first it failed on the four chrome-less `en/embed/<slug>/` widgets. It now skips those widget pages, which e2e_embed covers. It still tests the `en/embed/` hub, and that passes.

## Shared files touched (small, backward compatible)

- `tools/site/build_site.py`: a guarded call to build_embeds and data-il/tools/build.py.
- `docs/data/hreflang.json`: one pair added, placed after the guides pair.
- The 10 calculator pages: one marked line each.
- `docs/tools/index.html` and `docs/en/tools/index.html`: one line each.
- `README.md`.
- `products/en-jewish-life/e2e_en.js`: skips the iframe widget pages.

If ws/seasonal adds calculators, they can be added to `EMBEDS` in `build_embeds.py` and the test `CASES`.

## Notes for the manager

- Links earned this way are passive. They only appear if site owners find the hub or dataset pages through search or GitHub, so expect slow or zero uptake.
- The best next step is a GitHub Release and topics for `data-il`, because GitHub is our fastest crawl path.
- The repo must stay public for the `pip install git+…` command and the jsDelivr link to work.
