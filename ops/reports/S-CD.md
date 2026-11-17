# Streams C + D report (branch `ws/tipskit`)

Both streams are built and tested. Testing used TEST mode only: no real payments were made, and nothing was posted outside the repo.

## C. Tips + upsells

| What | Where | Behaviour |
|---|---|---|
| Tip jar ("עזר לכם? אפשר להזמין אותנו לקפה ☕") | `docs/assets/tip.js` | Shows on every free tool page in `tools/<slug>/`. It stays **hidden until the visitor has a result**: they typed or clicked in the tool, a `.result`/`aria-live` area holds numbers, and 1.8 s have passed. Amounts are ₪10, ₪20 or a custom amount from ₪5 to ₪500. Payment goes through PayPal with slug `tip`. The thank-you appears inline. Closing it with × hides it for 14 days; after a tip it stays hidden for 90 days. |
| Bundle upsell on product pages | `docs/assets/upsell.js` | Under the main buy box it shows the smallest bundle that contains the product, with the real saving ("חוסכים ₪X"), plus a line for the "everything" bundle. Bundles come from `products/index.json`, so new bundles appear automatically. It links to the bundle's buy box if the page already has one, otherwise to `products/#<bundle>`. |
| One-time offer on the thanks page | `docs/assets/upsell.js` + `docs/data/upsell.json` | Offers the complementary product at **20% off, rounded to whole shekels** (₪39 → ₪31, ₪29 → ₪23). It is paid right there and redirects to that product's normal thanks page. It is shown **once per browser** and never for a product the buyer already owns, either directly or through a bundle. It has no timer and the copy says "you can simply skip it". TEST orders use a separate flag, so testing doesn't use up the real offer. |
| Shared payment primitive | `docs/assets/paykit.js` | Renders PayPal for an amount decided on the page, in any currency, with TEST mode and `recordSale()`. Tips, the thanks-page offer and the USD devkit all use it. **`checkout.js` is unchanged.** |

**Shared-file change (minimal, backward compatible):** `docs/assets/site.js` gained a `features()` function of about 8 lines. It loads `tip.js` on `tools/<slug>/` and `upsell.js` on `p/<slug>/` and `thanks/`, and only on Hebrew pages (`<html lang="he">`), so `/en/` and the devkit are not affected.
- To keep these off a page, use `<html data-tip="off">` (for example on ws/apps pay-to-export tools) or `data-upsell="off"`.
- `site.css` is untouched: the components inject their own small styles, which use the site's CSS variables.

**Complement map** (`docs/data/upsell.json`, editable):
- wedding → household budget
- bar mitzvah → household budget
- household ↔ renovation
- osek patur ↔ quote pack
- event-bundle → household
- money-bundle → osek patur
- freelancer-bundle → household
- everything-bundle → nothing

## D. RTL Landing Kit

- **`devkit/`, free and MIT-licensed:**
  - 3 templates (`launch` SaaS, `studio` agency, `pocket` mobile app), each as plain CSS (`index.html`) and Tailwind (`tailwind.html`).
  - Full Hebrew, Arabic and English copy with a language switcher (`?lang=ar`).
  - `css/rtl-kit.css` uses logical properties only; there is no left/right anywhere.
  - `js/rtl-kit.js` is about 2 KB.
  - The Tailwind variant is compiled to `css/tailwind.css` (Tailwind 3.4.16, `npm run build:tw`). It does not use the CDN, which is blocked here and isn't meant for production anyway.
  - Includes a README with 9 screenshots (3 templates × he/ar/en), a LICENSE, and generator scripts (`tools/build_free.py`, `content.py`).
- **Pro pack, $24:** the source is in `products/rtl-kit-pro/` and the build output in `products/rtl-kit-pro/build.py`.
  - 12 templates: restaurant, real estate, clinic with 3-step booking, law firm, online course, conference, product store, nonprofit with donations, waitlist, portfolio, fitness studio with monthly/yearly toggle, SaaS dashboard app shell.
  - A components gallery:
    - navbars: simple, mega dropdown, centred with announcement bar, dark with side drawer
    - forms: contact with +972 prefix, login with error state, multi-step signup, Israeli checkout
    - pricing: 3 tiers, toggle, comparison table
    - dashboard: KPIs, SVG chart, table
    - also tabs, timeline, modal, toast and breadcrumbs
  - Also included: `pro.css`, `pro.js` (about 4 KB), the free kit, a README and a commercial license.
  - Zip: `docs/dl/zvc8s5ykj4hwzgxz/rtl-landing-kit-pro-v1.0.zip` (109 KB). Product data: `docs/data/products/rtl-kit-pro.json`, which is **not** in `index.json`, so the Hebrew catalogue is unaffected.
- **`docs/devkit/index.html`:** an English LTR landing page built with the kit's own CSS. It has hero, live demos (he/ar/en/Tailwind links), how it works, a Pro gallery with 14 screenshots, a sticky Pro buy box in USD via paykit, an FAQ, and JSON-LD for SoftwareSourceCode and Product. It is mobile-OK with no overflow and records a visit through sales.js.
- **`docs/devkit/thanks/`:** an English download page (noindex) that reads the product JSON.
- **Downloads and demos:** the free zip is `docs/devkit/rtl-landing-kit-free.zip` and the live demos are in `docs/devkit/demos/`. Rebuild everything with `python3 products/rtl-kit-pro/build.py`; it also takes the screenshots.
- **Repo `README.md`:** added a "RTL Landing Kit" section with a screenshot. The existing site links are kept.

## Tests

- `node tools/site/e2e_tipskit.js`: **86/86 pass** at 375 and 1280 px. It covers:
  - the tip jar on all 8 tools: hidden before use and shown after a result
  - the ₪5 minimum
  - a test tip and the thank-you
  - not reappearing after × or after a tip
  - upsell savings on 3 product pages
  - the thanks-page offer price, no timer, test payment → redirect, and not shown twice
  - devkit landing, all 6 demos (RTL by default, `?lang=en` gives LTR) with no overflow
  - Pro TEST purchase → thanks page → zip download (200)
  - no page errors
- `node tools/site/e2e_test.js` (the existing platform e2e): **all pass** after the site.js change.

## Decisions / notes for the manager

1. **Pro templates are not published as live pages**, only as screenshots, so the zip is what buyers pay for. As with the existing products, the zip sits in an unguessable `docs/dl/` folder in a public repo, and so does the generator under `products/rtl-kit-pro/src/`. That is the same accepted trade-off as the Hebrew products.
2. Pro templates ship with **Hebrew placeholder copy** and built-in Arabic typography (`lang="ar"` switches fonts and line height). The landing page and FAQ say this honestly. The free templates carry the full he/ar/en copy and the switcher.
3. **Links to the GitHub repo point to `main`** (`/tree/main/devkit`), so they work once this branch is merged.
4. I did **not** rebuild `docs/sitemap.xml`, because it is W1-owned and would cause merge conflicts. After merging, run `python3 tools/site/build_sitemap.py` to add `/devkit/` and the demos. The devkit thanks page is noindex.
5. The tip has no product JSON (`tip` is only the PayPal sku and the sales-log slug). The sales endpoint already accepts any slug and the currency is USD for the devkit, so the summary shows ILS and USD separately.
6. **Pre-existing issue, not mine:** at 375 px, when Google Fonts fail to load, the fallback font makes the site header about 18 px wider than the screen (the theme toggle is pushed off-screen). With the fonts loaded there is no overflow. This could be fixed in `site.css` by letting `.nav`/`.brand small` wrap or shrink. It belongs to W1/platform.
7. The PayPal SDK only allows one currency per page. That is why the devkit (USD) has its own page and never loads `checkout.js` (ILS).
