# Stream G: Online Hebrew invitation maker (branch ws/invites)
Read ops/PLAN.md §12, ops/briefs/CONTRACT.md. Site https://tichnun.netlify.app/. Client-side app at docs/apps/invite/:
pick a template (12 original designs: wedding ×5, bar/bat mitzvah ×4, birthday/brit ×3), edit Hebrew text fields
(names, date — auto Hebrew date, venue, hours), colours/fonts (free OFL Hebrew fonts), live preview, mobile-first.
Free: watermarked low-res PNG preview. Paid ₪19: clean high-res PNG (for WhatsApp) + print PDF (A5/A6 with bleed).
Unlock via checkout.js (product JSON "unlock": true; on capture store unlock in localStorage). Another worker builds
similar unlock apps on ws/apps — if docs/assets/unlock.js exists on main, reuse it; otherwise write a tiny one at
docs/apps/invite/unlock.js. Product page docs/p/invitation-maker/ + 3 guides ("נוסח הזמנה לחתונה", etc.), link from
wedding/bar mitzvah products. Add to catalog/sitemap. Test in ?test=1 with Playwright. Push ws/invites. No PR.
Report ops/reports/S-G.md, then send_message the manager (@parent).
