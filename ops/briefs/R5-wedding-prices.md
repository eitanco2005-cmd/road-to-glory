# Round 5: Wedding vendor price guides (branch ws/prices)
Read ops/PLAN.md §13, ops/STATUS.md, reports/Realistic paths to 1000 dollars.md. Site https://tichnun.netlify.app/ (docs/ root).
Couples constantly search vendor prices. Build the best Hebrew answers, under docs/chatuna/mechirim/ (hub + pages):
מחיר אולם/גן אירועים למנה 2026 (by region/day/season), מחיר צלם לחתונה, מחיר DJ לחתונה, מחיר שמלת כלה, מחיר איפור ושיער לכלה,
מחיר רב/עורך חופה, מחיר הסעות לחתונה, מחיר מגנטים/צלם מגנטים, מחיר עיצוב/פרחים לחתונה, מחיר חליפת חתן.
Each page: price table with ranges (low/typical/high) + what drives price + questions to ask the vendor + how to save + a mini
"how this fits your total budget" box linking to tools/wedding-cost/ (preset if possible) and the wedding planner/bundle.
Every number must cite at least one dated source (articles, vendor price lists, mit4mit/price guides); never invent precision —
use ranges and say when data is thin. Add these items to the wedding-cost calculator model only if consistent.
JSON-LD (Article + FAQ where valid + BreadcrumbList), WhatsApp share, link from chatuna/ hub and relevant guides.
python3 tools/site/build_site.py; run ALL e2e suites listed in ops/briefs/R4-wedding-focus.md plus tools/site/e2e_wedding.js;
add checks for the new pages. Push ws/prices. No PR. Report ops/reports/R5.md, then send_message the manager (@parent).
