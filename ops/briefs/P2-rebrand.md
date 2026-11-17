# P2 Rebrand: "Glory" → "תכנון פלוס" (branch ws/rebrand)

Owner chose the brand **תכנון פלוס** (Latin/English contexts: "Tichnun Plus"). The site is moving from GitHub Pages
to Netlify (publish dir `docs/`, served at the domain ROOT, e.g. https://tichnun.netlify.app/ — exact host TBD by manager).

Do:
1. Replace the brand everywhere user-visible: page titles/meta/og:site_name, JSON-LD (Organization/Brand), header logo
   text (docs/assets/site.js), footer, legal pages (tools/site/build_legal.py, then regenerate with
   `--name "איתן כהן" --email "eitanco2005@gmail.com"`), favicon/og image if they contain text, thanks page, guides.
   Fix Hebrew grammar around the name (e.g. "ב-Glory" → "באתר תכנון פלוס", "של Glory" → "של תכנון פלוס").
2. Update every generator in products/** and tools/** that writes "Glory", regenerate all .xlsx/.docx downloads,
   and rename files containing "glory" (e.g. wedding-planner-glory.xlsx → wedding-planner.xlsx). Update product JSON
   `files[].path` accordingly. Keep the same docs/dl/<random> folders. Remove old files.
3. Centralise the site base URL: one constant (e.g. tools/site/site_config.py `BASE_URL` + `docs/assets/config.js SITE_URL`)
   used by build_sitemap.py, build_legal.py, canonical/og:url generation, guides, product page builders, indexnow.py.
   Set it to `https://tichnun.netlify.app/` for now; manager will adjust if the host differs. Canonicals must point there.
   Do NOT add redirects from github.io yet (manager does that).
4. Grep must end clean: `grep -ri glory docs products tools --include=* | grep -v "road-to-glory"` should only show
   things that genuinely can't change (e.g. the GitHub repo name in README), listed in your report.
5. Run `python3 tools/site/build_site.py`, `node tools/site/e2e_test.js` (pip install fastapi uvicorn), LibreOffice
   recalc of regenerated workbooks (0 errors). Report in ops/reports/P2-rebrand.md. Push to ws/rebrand. No PR.
