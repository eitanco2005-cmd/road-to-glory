# Round 6B: Conversion readiness for wedding products (branch ws/convert)
Context: Google will start sending visitors soon. A new, unknown shop needs trust + try-before-you-buy. Focus on wedding products:
p/wedding-planner, p/seating-chart (apps/seating), p/rsvp-tracker (apps/rsvp), p/invitation-maker (apps/invite), wedding-bundle (₪79).
Read ops/PLAN.md §13, ops/STATUS.md, ops/briefs/CONTRACT.md.

1. Free samples (no payment, direct download): "mini wedding budget" xlsx (1 sheet, real formulas, branded, links to full planner);
   sample seating-chart PDF export (realistic fake names); sample invitation PNG. Put on product pages ("נסו בחינם") and in the chatuna hub.
2. Product pages: real screenshots/previews (render with Playwright at 2x), a clear "מה מקבלים" checklist, "למי זה מתאים / לא מתאים",
   honest refund line linking legal/refund, secure-payment line (PayPal or card, no account), instant delivery explanation, and a short
   "איך זה עובד" 3-step strip. No fake reviews, no fake scarcity, no countdowns.
3. Funnel: after the guest gift calculator result, a gentle "מתחתנים בעצמכם?" box linking to the chatuna couple path; after the free
   RSVP 80-guest limit or seating watermark export, a clear upgrade message with the bundle as the best-value option.
4. Bundle page: compare table (separate vs bundle price), what's included, single buy box.
5. Checkout copy check: product names/descriptions passed to PayPal are clear in Hebrew; thanks page has next steps + how to get help.
6. python3 tools/site/build_site.py; run ALL e2e suites (list in ops/briefs/R4-wedding-focus.md + tools/site/e2e_wedding.js, apps suite);
   add checks for samples downloading and the new upgrade prompts. Push ws/convert. No PR. Report ops/reports/R6B.md, then send_message
   the manager (@parent). Another worker (ws/quality) edits page text/SEO in parallel: keep your changes to buy areas, samples, funnel
   boxes; minimal, mergeable edits.
