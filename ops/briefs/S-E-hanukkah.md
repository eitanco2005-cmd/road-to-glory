# Stream E: Hanukkah pack — URGENT, must be live by Nov 22 (branch ws/hanukkah)
Read ops/PLAN.md §12 and ops/briefs/CONTRACT.md. Site https://tichnun.netlify.app/ (docs/ at root). Hanukkah 2026: verify dates (≈ Dec 4–12).
Build print-ready PDFs (A4 for Hebrew, US Letter + A4 for English) with clean original vector art (SVG → PDF; no
copyrighted characters, no AI-looking clutter):
1. Hebrew "חבילת פעילויות לחנוכה" ₪19: coloring pages, mazes, dreidel game rules + score sheet, word search, candle
   lighting chart with brachot (verify text), 15+ pages. 2. English "Hanukkah Activity Pack" $12 (same, English).
3. Hanukkah party/hosting planner (Hebrew xlsx ₪19 + English $12): guests, latke/sufganiyot quantities by guests,
   shopping list, gift tracker for 8 nights. 4. Bundle ₪29 / $19.
Free tool: "how many sufganiyot/latkes" quantity calculator (he + en). 3 guides (he) + 2 (en). Product pages per
contract (en pages under docs/en/ if that section exists on main, else docs/en/hanukkah/ standalone LTR), previews
(rendered PNG/WebP of pages). If per-product USD currency isn't supported in checkout.js yet, add `currency` support
minimally and backward compatibly (another worker may also add it on ws/en — keep the same field name `currency`).
Test e2e + Playwright. Push ws/hanukkah. No PR. Report ops/reports/S-E.md, then send_message the manager (@parent).
