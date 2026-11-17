# P2 Rebrand report: "Glory" → "תכנון פלוס" (branch ws/rebrand)

## Result
- Brand is **תכנון פלוס** on every user-visible surface: titles, meta descriptions, `og:site_name`, `og:title`,
  JSON-LD (Organization / Brand / publisher / author), header + footer logo text (docs/assets/site.js), footer ©,
  legal pages, thanks page, 404, all guides, tools and product pages, OG image, workbook/docx text and metadata.
- **Base URL is centralised and set to `https://tichnun.netlify.app/`** (site at the domain root). All 47 indexable
  pages have a canonical equal to `BASE_URL + path` (scripted check: 0 mismatches); sitemap and robots point there.
- Final grep `grep -ri glory docs products tools | grep -v road-to-glory` → **empty**. `road-to-glory` itself also no
  longer appears anywhere in docs/, products/ or tools/.

## Where the base URL / brand live now
| What | File |
|---|---|
| `BASE_URL`, `BRAND`, `BRAND_LATIN`, `TAGLINE` (Python) | `tools/site/site_config.py` |
| `SITE_URL`, `BRAND`, `BRAND_LATIN` (browser) | `docs/assets/config.js` |
| Consumers of `BASE_URL` | `build_sitemap.py` (sitemap + robots), `build_site.py` (via build_sitemap), `build_legal.py`, `indexnow.py` (host derived from BASE_URL), `products/household-budget/site_common.py` (household + renovation pages), `products/wedding-planner/web/common.py` (wedding/bar-mitzvah pages, tools, guides), `products/osek-patur-tracker/build_pages.py` (osek + quote pages, VAT/ceiling tools) |
| **Host change in one command** | `python3 tools/site/set_base_url.py https://new-host/` — rewrites site_config.py, config.js `SITE_URL`, every absolute URL baked into docs/ (incl. the 20 hand-written pages), templates and README, then rebuilds sitemap/robots. Tested on a throwaway copy (netlify → tichnun.co.il → regenerating pages afterwards produced no extra diff). |

No github.io redirects were added (manager's job).

## What was done
1. **Generators first, then regenerate.** Every page generator now imports `BASE_URL`/`BRAND` from site_config.
   Before rebranding I verified that the generators reproduce the committed pages; they did, except for hand-added
   cross-links from P2-SEO (household → 4 site guides, osek → open-osek-patur guide, wedding → 4 wedding guides).
   I back-ported those links into the generators (`site_pages.py`, `build_pages.py`, `product_pages.py` `site_guides`),
   so **regenerating all 29 generated pages now gives byte-identical output to what is committed.**
2. **Hand-written pages** (home, products, tools index, guides index + 12 guides, net-salary/savings-goal tools,
   thanks, 404): same replacement rules applied directly.
3. **Hebrew grammar rules used**: "ב-Glory" → "באתר תכנון פלוס"; "של Glory" → "של תכנון פלוס"; "אתר Glory" → "אתר תכנון פלוס";
   "איזה מידע Glory אוסף" → "איזה מידע אתר תכנון פלוס אוסף"; "קטלוג Glory:" → "הקטלוג של תכנון פלוס:";
   "הערכות/הערכת Glory" → "הערכות של / הערכה של תכנון פלוס"; "הכיול שלנו (Glory)" → "הכיול שלנו";
   legal "(להלן "Glory", "אנחנו")" → "(להלן "תכנון פלוס", "אנחנו")"; title suffix "| Glory" → "| תכנון פלוס".
4. **Legal pages** regenerated with `--name "איתן כהן" --email "eitanco2005@gmail.com"` (brand passed into the template).
5. **Downloads regenerated** from the generators (all products), file renames:
   - `dl/lje2wikbyyh1goea/wedding-planner-glory{,-example}.xlsx, -messages.docx` → `wedding-planner{,-example}.xlsx`, `wedding-planner-messages.docx`
   - `dl/3lvcpz0f1kr21brs/bar-bat-mitzvah-planner-glory*` → `bar-bat-mitzvah-planner{,-example}.xlsx`, `bar-bat-mitzvah-planner-messages.docx`
   - `products/{wedding,bar-mitzvah}-planner/out/*-Glory*` → same Hebrew names without "-Glory".
   - Same dl/<secret> folders kept, old files removed (git rm), product JSON `files[].path` updated by publish.py.
   - Household (3), renovation (2 + checklist docx), osek (2), quote pack (2 xlsx + 5 docx re-zipped) rebuilt and
     copied to their existing dl folders. A scan of every xlsx/docx in docs/dl and products finds no "Glory".
6. **Screenshots**: wedding + bar-mitzvah screenshots were re-rendered by publish.py (they come from the build; the
   only visible change is the date-based "days to event" figure). Household/renovation/osek/quote screenshots were
   **not** re-rendered: the brand appears only on the instructions sheet, which is not in any screenshot (checked).
7. **OG image** `docs/assets/og-default.png` re-rendered from `tools/site/templates/og.html` with the new name.
   Favicon has no text (unchanged).
8. **JS identifiers renamed** so the grep is clean: `window.GLORY` → `window.SITE`, `GLORY_CONFIG` → `SITE_CONFIG`,
   `GloryCheckout` → `SiteCheckout`, `data-glory` → `data-site-sdk`, localStorage keys `glory-*` → `tp-*`
   (theme, orders, pending sales, visit dedupe). The move to a new origin resets browser storage anyway, so nothing is lost.
9. **404 page**: removed the `/road-to-glory/` sub-path detection; it now uses `<base href="/">` (Netlify serves
   404.html at the root for any missing path).
10. **e2e test** now serves docs/ at the root (`http://127.0.0.1:8765/`) like Netlify.
11. **Header on mobile**: "תכנון פלוס" is wider than "Glory" and wrapped onto two lines at 375px. Added
    `white-space: nowrap` and tighter spacing at ≤420px / ≤350px; no horizontal overflow at 320px or 375px (checked).
12. Sales-endpoint docs: suggested Space names `glory-sales-log*` → `tichnun-sales-log*`, example
    `ALLOWED_ORIGINS=https://tichnun.netlify.app` (the endpoint is not deployed yet, so nothing live changes).
13. README: new title, links on tichnun.netlify.app, note on how to change the host.

## Decisions (for the manager to override if needed)
- **Tagline**: header small text was "כלים חכמים לתכנון", which repeats "תכנון" next to the new name. Changed to
  **"קבצים ומחשבונים חכמים"** (header), and the workbook/docx footer line to "תכנון פלוס – קבצים ומחשבונים חכמים בעברית".
  Home-page hero copy and the OG image headline ("כלים חכמים לתכנון / חתונה · תקציב · עסק") left as is.
- **PayPal `brand_name`** = `cfg.BRAND` = "תכנון פלוס" (Hebrew, shown on the PayPal page). `BRAND_LATIN` "Tichnun Plus"
  is available in config.js if PayPal renders Hebrew badly; switch in checkout.js line ~186.
- Brand in workbook/docx metadata (creator/author) is the Hebrew name.
- Content strings in generators carry the brand as literal Hebrew text; structural places (og:site_name, JSON-LD,
  legal head) use the `BRAND` constant.
- `ops/` documents (PLAN, STATUS, briefs, older reports) still say "Glory": they are history, outside the grep scope.

## What still says road-to-glory / Glory (cannot change here)
- The GitHub repository name `eitanco2005-cmd/road-to-glory` (git remote; not referenced in docs/products/tools any more).
- ops/ history files.

## Checks run
| Check | Result |
|---|---|
| `python3 tools/site/build_site.py` | 0 catalog regions changed; sitemap 47 URLs + robots on https://tichnun.netlify.app/ |
| Regenerate all page generators + build_legal | byte-identical to committed docs |
| `node tools/site/e2e_test.js` (fastapi + uvicorn installed) | **ALL PASSED** (incl. live PayPal SDK buttons, guest card, test purchase → thanks → download, bundles, legal pages, no JS errors) |
| `pytest tools/site/sales_endpoint/test_app.py` | 1 passed |
| LibreOffice recalc (`qa_recalc.py`) on all 13 xlsx in docs/dl | **0 errors in every file** |
| Canonical == BASE_URL + path, og:site_name == תכנון פלוס on all indexable pages | 0 mismatches |
| `grep -ri glory docs products tools \| grep -v road-to-glory` | empty |
| Visual: home at 375/1280px, header at 320/375px, OG image | OK |
