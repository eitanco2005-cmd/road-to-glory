# Streams C + D: tips/upsells and RTL developer kit (branch ws/tipskit)
Read ops/PLAN.md (§12), ops/briefs/CONTRACT.md. Site: https://tichnun.netlify.app/.
C. Tips + upsells:
 - Reusable "tip jar" component (docs/assets/tip.js): small, tasteful box at the bottom of every free tool result
   ("עזר לכם? אפשר להזמין אותנו לקפה ☕") with ₪10 / ₪20 / custom amount via PayPal (product slug "tip", amount
   chosen by buyer, min ₪5), thank-you message inline. Must not annoy: shown after the user gets a result.
 - Upsell: on product pages show the matching bundle with savings ("חוסכים ₪X"); on thanks page offer the
   complementary product at a one-time 20% discount (honest, no countdown timers).
D. RTL developer kit (English):
 - `devkit/` folder: "RTL Landing Kit" — open-source (MIT) free version: 3 responsive RTL landing-page templates
   (Hebrew/Arabic ready, logical CSS properties, no framework + a Tailwind variant), good README with screenshots,
   live demos under docs/devkit/demos/.
 - Pro pack ($24, sold via our PayPal at docs/devkit/): 12 more templates + components (RTL navbars, forms, pricing,
   dashboards), Figma-free; deliver as zip in docs/dl/<random>/.
 - Landing page docs/devkit/index.html (English, LTR) with demos, free download link (GitHub), Pro buy box.
 - Update repo README.md with a "RTL Landing Kit" section (GitHub discovery), keeping the existing site links.
Test (e2e + Playwright). Push ws/tipskit. No PR. Report ops/reports/S-CD.md, then send_message the manager (@parent).
