# Brief A — Portfolio site + demo sites (branch `ws/portfolio`)

Context: read `ops/STRATEGY.md`. We sell fixed-price landing pages to small local
businesses ($149 Starter / $299 Standard, delivered in 48h). Buyers need proof.

Deliver in `docs/` (served by GitHub Pages):
1. `docs/index.html` — the agency's own sales page: offer, two price tiers, what's
   included, 48h turnaround, process (3 steps), FAQ, contact section (a mailto
   placeholder `CONTACT_EMAIL` the owner will replace). Fast, responsive, no build step.
   Brand name placeholder: "Glory Sites".
2. Three demo client sites for fictional businesses (clearly fictional names, no real
   brands): `docs/demos/cafe/`, `docs/demos/salon/`, `docs/demos/plumber/`. Each
   realistic, mobile-first, with hero, services, hours/location block, testimonials
   marked as sample text, contact/booking CTA.
3. Linked from the sales page as a portfolio grid.
Rules: plain HTML/CSS (minimal JS), no external assets except Google Fonts; images via
CSS/SVG or royalty-free placeholders only. Check every page at 375px and 1280px with
Playwright screenshots. Commit + push to `ws/portfolio`. Finish with a short summary in
`ops/reports/A-portfolio.md`.
