# Stream B: Pay-to-export web tools (branch ws/apps)
Read ops/PLAN.md (§12), ops/briefs/CONTRACT.md. Site: https://tichnun.netlify.app/ (static, docs/ at root).
Build two client-side apps (no backend; data stays in the browser/localStorage; Hebrew RTL; mobile-friendly):
1. `docs/apps/seating/` — wedding/event seating-chart planner: add guests (paste list / import CSV/XLSX), tables
   (round/rect, seats), drag-and-drop, groups/sides, conflicts ("keep apart"), auto-seat suggestion, printable view.
   Free: full use on screen + watermarked PDF. Paid ₪29: clean PDF + XLSX export + table cards for printing.
2. `docs/apps/cv/` — Hebrew CV builder: form → live preview, 4 clean RTL templates, Hebrew/English toggle,
   ATS-friendly. Free: preview + watermarked PDF. Paid ₪19: clean PDF + DOCX.
Unlock flow: PayPal checkout via checkout.js (product JSON with "unlock": true); on capture, store an unlock token
for that product in localStorage and enable clean exports immediately (no redirect needed; also offer the thanks page).
Accept that client-side unlock is bypassable; keep it simple and honest. PDF via jsPDF/html2canvas or print CSS
(pinned versions from cdnjs/jsdelivr). Product pages under docs/p/<slug>/ + 2 guides each, link from related products
(seating ↔ wedding planner). Add to catalog + sitemap. Test end-to-end in ?test=1 with Playwright. Push ws/apps. No PR.
Report ops/reports/S-B-tools.md, then send_message the manager (@parent) a summary.
