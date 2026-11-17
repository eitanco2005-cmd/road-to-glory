# P2 QA reviewer (branch ws/qa)
The site is LIVE at https://eitanco2005-cmd.github.io/road-to-glory/ (source: docs/ on main). Read ops/PLAN.md and ops/briefs/CONTRACT.md.
Audit like a picky Israeli customer and a Google reviewer, then FIX what you find (in docs/ and products/):
1. Every page at 375 and 1280: Hebrew spelling/grammar, RTL glitches, broken links, slow assets, accessibility (contrast, alt text, labels).
2. Every spreadsheet: open, recalc with LibreOffice, try realistic inputs, check formulas, charts, RTL, instructions sheet. Fix bugs.
3. Facts: re-check every cited figure (VAT 18%, osek patur ceiling, wedding gift norms, prices) against the cited sources; correct or soften claims.
4. Copy honesty: remove any claim we can't back (e.g. "Google Sheets" copy links don't exist yet — say "works in Excel and Google Sheets (upload)" instead).
5. Checkout in ?test=1 for every product + bundle; never complete a real payment.
Run `node tools/site/e2e_test.js` (needs `pip install fastapi uvicorn`) and keep it passing. Write ops/reports/P2-qa.md (found / fixed / left). Push to ws/qa. No PR.
