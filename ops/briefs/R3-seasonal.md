# Round 3A: Seasonal pre-positioning (branch ws/seasonal)
Read reports/Realistic paths to 1000 dollars.md, ops/STATUS.md, ops/briefs/CONTRACT.md. Site https://tichnun.netlify.app/ (Netlify, docs/ root).
Research note: seasonal pages must be live 6–14 weeks before the peak to rank. Build NOW for upcoming peaks. Verify all dates with a
Hebrew-calendar computation (reuse products/hanukkah/verify_dates.py approach): Purim 2027, Passover 2027.

1. January "תקציב 2027" campaign (peak late Dec–Jan): hub docs/budget-2027/ — genuinely useful: step-by-step "how to build a family
   budget for 2027", what changed in 2027 for Israeli households (only facts you can cite: VAT, tax brackets/credit points if published,
   ביטוח לאומי changes; mark unknowns), monthly savings challenge printable (free), links to the household-budget product (2027 edition),
   50/30/20 and net-salary calculators. Add home-page placement from Dec 20 (leave a TODO note in ops/STATUS.md, don't add yet).
2. Purim 2027 (Hebrew): mishloach manot planner (xlsx: recipients, what to give, budget, shopping list, delivery route) ₪19; free
   "תקציב משלוחי מנות" calculator; 3 guides (ideas by budget, rules/halachic basics with sources, kids' class gifts). Hub docs/purim/.
3. Passover 2027 (Hebrew): "ניקיון לפסח" room-by-room checklist printable (free lead magnet) + Hebrew seder planner xlsx (guests,
   menu, quantities by guests, shopping, haggadah roles) ₪19 + bundle ₪29; free "כמות מצות/יין לפי מספר אורחים" calculator; 3 guides.
   Hub docs/pesach/, hreflang to the English Passover pages.
4. WhatsApp share (docs/assets/share.js) on all new calculators. Catalog/tools.json/sitemap via python3 tools/site/build_site.py.
Run ALL e2e suites (tools/site/e2e_test.js [pip install fastapi uvicorn], tools/apps/e2e_apps.js, tools/site/e2e_tipskit.js,
products/en-jewish-life/e2e_en.js, products/hanukkah/test_e2e.js, tools/site/e2e_share.js) + LibreOffice recalc of new workbooks.
Push ws/seasonal. No PR. Report ops/reports/R3A.md, then send_message the manager (@parent).
