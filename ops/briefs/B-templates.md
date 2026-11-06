# Brief B — Sellable template pack (branch `ws/templates`)

Context: read `ops/STRATEGY.md`. Product: "Local Business Landing Page Pack" sold on
Gumroad for ~$24. Target buyers: freelancers and small business owners.

Deliver in `product/`:
1. 6 one-page HTML/CSS templates (restaurant, salon/beauty, trades, clinic/dental,
   fitness/gym, real estate agent). Mobile-first, accessible, easy-to-edit (clear
   comments + CSS variables for brand colours/fonts), no build step, no paid assets.
2. `product/README.md` — buyer-facing quick start (edit, deploy free to Netlify/GitHub
   Pages, connect domain) and license (personal + client use, no resale).
3. `product/listing.md` — Gumroad listing copy: title, tagline, description, bullet
   features, 3 price-point suggestions, cover/thumbnail description.
4. `product/build_zip.sh` — packs templates + README into `dist/pack.zip`.
Verify each template with Playwright screenshots at 375px and 1280px; save preview
images in `product/previews/` (these become listing images). Commit + push to
`ws/templates`. Summarise in `ops/reports/B-templates.md`.
