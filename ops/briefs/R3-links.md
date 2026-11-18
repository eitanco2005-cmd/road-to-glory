# Round 3B: Earn links without outreach — embeddable widgets + open data (branch ws/linkbait)
Read reports/Realistic paths to 1000 dollars.md, ops/STATUS.md. Site https://tichnun.netlify.app/. Goal: give other sites a reason to
link to us on their own (no contacting anyone, no PRs to other repos).

1. Embeddable calculators: for the 6 strongest calculators (wedding-gift, vat-calculator, osek-patur-ceiling, net-salary budget,
   budget-503020, sufganiyot/latke if present), make a lightweight embed version docs/embed/<slug>/ (no site header/footer, responsive,
   ~<40KB, works in an iframe, RTL, auto-height via postMessage) with a small visible attribution link "מחשבון: תכנון פלוס" (normal link,
   not nofollow). A page docs/embed/ ("הוסיפו מחשבון חינם לאתר שלכם") listing each with copy-paste iframe code + live preview, plus an
   "Embed" link on each calculator page. Also English versions for the English calculators.
2. Open data on GitHub (in THIS repo, folder data-il/, MIT/CC0): JSON + CSV for Israeli holidays 2025–2030 (Hebrew + English names,
   dates computed + verified), VAT rate history (with source links), osek patur ceiling history, minimum wage history, ביטוח לאומי
   basic rates if sourceable — every value with a source URL and date. A tiny zero-dependency JS + Python helper (e.g. isIsraeliHoliday,
   addVat), README in English + Hebrew with usage examples and links to the live calculators. Also a docs/data-il/ page on the site
   explaining the dataset with download links. Do not publish to npm/PyPI (no accounts) — show install-from-GitHub instructions.
3. Update the root README.md with an "Israeli open data" and "Embeddable calculators" section. Add JSON-LD Dataset markup on docs/data-il/.
4. python3 tools/site/build_site.py; run ALL e2e suites (see list in ops/briefs/R3-seasonal.md) + a new test for embed pages (render in an
   iframe, attribution link present, postMessage height works). Push ws/linkbait. No PR. Report ops/reports/R3B.md, then send_message the manager (@parent).
