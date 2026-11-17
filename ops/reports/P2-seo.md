# P2 SEO content: report (branch ws/seo)

*2026-11-17. Brief: ops/briefs/P2-seo.md.*

## What was built

### 1. Keyword map: `research/keywords.md`
- 7 clusters, each with 10 Hebrew phrases grouped by intent. Each phrase is mapped to the page that targets it.
- The gaps found become the next content candidates, listed at the end of the file.
- **Limitation:** Google autocomplete (suggestqueries.google.com) is blocked by this environment's proxy (HTTP 403). Phrases were validated by live web search instead: Israeli publishers build pages for these exact queries. There are no volume numbers. Re-rank with Search Console data after 2–3 weeks.

### 2. Twelve new guides: `docs/guides/<slug>/` plus the index `docs/guides/`
Each guide is 1,070–1,180 words (body + FAQ), original Hebrew, 4–6 cited sources, and at least one table or worked example. The worked examples were recomputed in Python.

| Cluster | Guide | Free tool | Product |
|---|---|---|---|
| Budget 2027 | budget-by-net-salary | net-salary-budget (new) | household-budget |
| Budget 2027 | how-to-save-money | budget-503020 | household-budget |
| Budget 2027 | get-out-of-overdraft | net-salary-budget | household-budget |
| Budget 2027 | emergency-fund | savings-goal (new) | household-budget |
| Budget 2027 | savings-goal-plan | savings-goal | household-budget |
| Budget 2027 | couple-money | budget-503020 | household-budget |
| Budget 2027 | expense-tracking | budget-503020 | household-budget |
| Wedding | wedding-checklist | wedding-gift | wedding-planner |
| Wedding | wedding-guest-list | wedding-gift | wedding-planner |
| Wedding | wedding-save-money | wedding-gift | wedding-planner |
| Wedding | wedding-vendor-contracts | wedding-gift | wedding-planner |
| Freelancer | open-osek-patur | osek-patur-ceiling | osek-patur-tracker |

What every guide page has:
- A unique title (≤ 56 characters including " | Glory") and a 139–154 character description.
- Canonical URL and Open Graph tags.
- JSON-LD:
  - `Article`
  - `BreadcrumbList` (ראשי › מדריכים › page)
  - `FAQPage`, used only because each page shows the same Q&A visibly. Per research/products.md, Google no longer shows FAQ rich results, so this is understanding only, not a rich-result play.
- A tool callout, one calm product CTA, related-guide links and a disclaimer.

The guides index has `CollectionPage`/`ItemList` and `BreadcrumbList` JSON-LD. It links all 12 new guides plus the 12 existing product guides.

### 3. Two new free tools (in `docs/data/tools.json`)
- **`tools/net-salary-budget/`: מחשבון תקציב לפי משכורת נטו**
  - Inputs: net income, housing, loan repayments, adults, kids, car, savings %.
  - Output: a monthly and yearly budget across 11 Israeli categories. Every row can be edited; the remaining rows rebalance and the rounding remainder goes to the buffer row, so the total matches income exactly.
  - Warnings: housing above 30% / 40% of income, debt above 20%, money left over or a deficit.
  - The share link stores the inputs in the URL.
- **`tools/savings-goal/`: מחשבון יעד חיסכון**
  - Two modes: "monthly amount needed by date" and "when will I reach the goal".
  - Uses monthly compounding, with presets, a yearly table and honest tips (high-return warning, standing-order tip).
- Both tools:
  - run fully client-side;
  - have `WebApplication`, `FAQPage` and `BreadcrumbList` JSON-LD;
  - have 400+ words of explanation;
  - link to the household-budget product.
- Tested with Playwright at 375 and 1280 px: correct numbers, no horizontal scroll, no JS errors. Checked by hand: 30,000 target, 6,000 saved, 24 months at 3% gives ₪958 a month.

### 4. Internal links and technical
- **Home** (`docs/index.html`): new section "מתכננים את 2027? מתחילים כאן" with 6 guides and a "לכל המדריכים" button. Static HTML, so crawlers see it without JS.
- **Header nav and footer** (`docs/assets/site.js`): added a "מדריכים" link (+2 lines). Checked at 375 px: three nav items plus the theme toggle fit.
- **Product pages** household-budget, wedding-planner and osek-patur-tracker: new guides appended to their existing guide lists.
- Ran `python3 tools/site/build_site.py`: the sitemap now has 47 URLs, including all guides and the two new tools.
- **e2e:** `node tools/site/e2e_test.js` reports ALL PASSED. One assertion changed from "home lists 6 tools" to 8, because the two new tools appear in the home catalog.
- Automated checks: all JSON-LD parses, no broken internal links on any new or touched page, no duplicate titles, no horizontal overflow at 375 px on any guide.

## Decisions
- **Guides live under `docs/guides/`, not under each product.** The brief asked for a new section, and some guides (overdraft, emergency fund) serve more than one product.
- **The guide HTML was generated** from plain-text sources by a small script in the session scratchpad, so all 12 pages share identical head, schema and structure. Only the HTML is committed. To edit a guide later, edit its HTML directly, or ask me to recreate the generator.
- **No salary gross→net tool.** The research flagged that field as crowded and high-maintenance because the 2026 tax brackets changed mid-year. The net-salary tool starts from net pay, which needs no tax tables.
- **The tool's category split is presented as a starting point, not as statistics**, and the page says so. No invented "average family spends X" figures.
- **Wedding gets 4 guides, budget 7, osek patur 1**, following the brief's January-budget and wedding priority.

## Facts to keep an eye on (all hedged in the text)
- **Osek patur ceiling ₪122,833 (2026)** comes from Kol Zchut / gov.il summaries. Update the open-osek-patur guide in January when the 2027 figure is published.
- **Overdraft interest of about 10.7–12.7% (2025)** comes from TheMarker's comparison page, which quotes Bank of Israel data.
- **Wedding price per plate** (centre ₪420–550 in summer, ₪340–430 in winter): from Bizportal quoting Attending's 2026 price list.
- **Rabbinate registration timing** (about 3 months to 45 days before): secondary sources only. The text tells couples to check with their registration office.
- **"14-day cancellation does not apply to venues"** comes from a single consumer article and is written as "according to consumer guides".
- **Some sources could not be fetched from this environment**, because the proxy blocks direct page fetches. These were accepted from search results; Kol Zchut page names were built from the standard titles: הסכם_ממון, הרשאה_לחיוב_חשבון, קצבת_ילדים. Two links point to the boi.org.il homepage rather than a deep page. Worth a click-check by QA.

## Left / next
- Click-check the external source links (see above).
- Next guides from the keyword gaps:
  - כמה לשים בבר מצווה
  - חוזה עם קבלן שיפוצים
  - סדר עבודות בשיפוץ
  - עוסק פטור או מורשה
  - a "what changes in 2027" piece once official figures are out (late Dec)
- Once Search Console is verified: re-rank the keyword map and rewrite titles toward the queries that get impressions.
- **Possible conflict with QA (ws/qa):** I touched `docs/assets/site.js` (nav/footer, 2 lines), `docs/index.html` (one new section), the three product pages (link lines only) and `tools/site/e2e_test.js` (one assertion).
