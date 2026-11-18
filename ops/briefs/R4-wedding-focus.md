# Round 4: FOCUS — become the best Hebrew site for Israeli weddings (branch ws/wedding)
Owner feedback: "what is your audience? who will buy all that?" — correct: we are scattered. Decision: ONE audience = Israeli weddings
(guests + couples). Everything else stays online but frozen. Read reports/Realistic paths to 1000 dollars.md, ops/STATUS.md,
ops/briefs/CONTRACT.md. Site https://tichnun.netlify.app/ (Netlify, docs/ root). Existing wedding assets: tools/wedding-gift
(guest calculator), p/wedding-planner (₪49 xlsx), apps/seating (₪29), apps/invite (₪19), event bundle, guides.

1. Wedding hub docs/chatuna/ ("הכל לחתונה"): the single best entry point. Two clear paths: "אני אורח" (gift calculator, what to wear,
   how to transfer money/Bit/check etiquette, gift ideas) and "אנחנו מתחתנים" (timeline, budget, guests, seating, invitations).
2. New free tools (high-intent searches, each with WhatsApp share via docs/assets/share.js and an embed via tools/site/build_embeds.py):
   a) Venue/wedding cost calculator by guests, region, day of week, season, venue type (cite price sources; ranges, not fake precision).
   b) "כמה לשים בחתונה" deepening: per venue tier + per region quick-answer pages (e.g. "כמה לשים בחתונה בגן אירועים", "...ביום שישי",
      "...בזוג", "...לבן דוד") — 8 genuinely distinct pages that each answer one question well with a table, then link to the calculator.
      Avoid thin/duplicate content: each page needs its own reasoning/data.
   c) Guest-list & RSVP tracker app docs/apps/rsvp/ (client-side, localStorage, import contacts CSV/XLSX, sides/groups, RSVP status,
      meal choices, export to the seating app in one click). Free up to 80 guests; ₪29 unlocks unlimited + Excel export
      (reuse checkout unlock: product JSON "unlock": true). Bundle "חבילת חתונה": planner + seating + RSVP + invitation = ₪79.
   d) Wedding timeline generator: enter wedding date → personalised month-by-month checklist (printable, free).
3. Internal linking: every wedding page links the hub and the next step; home page gets a prominent wedding section first; footer
   "חתונה" column. Keep other sections reachable but de-emphasised.
4. Technical: JSON-LD (FAQ/HowTo/Article where valid), unique titles, build_site.py, sitemap, WhatsApp og images for hub + top tools.
5. Run ALL e2e suites (tools/site/e2e_test.js [pip install fastapi uvicorn], tools/apps/e2e_apps.js, tools/site/e2e_tipskit.js,
   products/en-jewish-life/e2e_en.js, products/hanukkah/test_e2e.js, tools/site/e2e_share.js, tools/site/e2e_embed.js,
   products/seasonal-2027/e2e_seasonal.js) + new tests for the RSVP app and new tools. Push ws/wedding. No PR.
   Report ops/reports/R4.md, then send_message the manager (@parent).
