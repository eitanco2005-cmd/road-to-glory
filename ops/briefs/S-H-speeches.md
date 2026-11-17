# Stream H: Personal speech & greeting writer (branch ws/speeches)
Read ops/PLAN.md §12, ops/briefs/CONTRACT.md. Site https://tichnun.netlify.app/ (static, docs/ at root, Netlify).
Goal: a genuinely good, warm, personal speech in minutes — the product people would happily pay ₪29 for. No LLM, no API:
a client-side template engine over a LARGE library of original, well-written modular passages.
1. Research first (research/speeches.md): Hebrew search phrases & what people want (נאום לבר מצווה, נאום הורים בבת
   מצווה, דרשה לבר מצווה לפי פרשה, ברכה לחתונה, נאום אבא של הכלה/חתן, נאום לחבר הכי טוב, ברכה ליום הולדת 50/70...),
   typical length, structure, tone; English equivalents (bar mitzvah parent speech, father of the bride speech).
2. App at docs/apps/speech/ (Hebrew RTL + English mode under docs/en/apps/speech/ if docs/en exists, else docs/apps/speech-en/):
   choose occasion + speaker role → short friendly form (names, ages, 2–4 personal stories/traits as free text, shared
   memories, tone: מרגש/מצחיק/מכובד, length 2/4/6 min, religious level, gender-correct Hebrew forms) → speech assembled
   from passages (opening, personal story weaving the user's own text, values/blessing, parsha hook for drasha — build
   a parsha table for all 54 parshiyot with 2–3 accurate themes each, verify), closing. Shuffle/regenerate per section,
   inline editing, read-time estimate.
   Free: see opening + outline + 2 lines blurred. Paid ₪29 / $19: full speech, unlimited regenerations for that occasion,
   copy, DOCX + nicely formatted PDF (large font for reading at the podium). Unlock via checkout.js ("unlock": true) +
   localStorage; reuse docs/assets/unlock.js if present on main.
   Quality bar: Hebrew must read naturally with correct gender/number agreement; at least 8 variants per section per
   occasion; no clichés overload; respectful for religious and secular families.
3. Product pages per occasion (docs/p/speech-bar-mitzvah/, speech-wedding/, ...) + 6 Hebrew guides (how to write X,
   with a free short example) + 3 English guides. Link from wedding & bar mitzvah products. Catalog + sitemap.
Test: Playwright flows for 3 occasions × both genders in ?test=1, PDF/DOCX output opens. e2e passes. Push ws/speeches.
No PR. Report ops/reports/S-H.md, then send_message the manager (@parent).
