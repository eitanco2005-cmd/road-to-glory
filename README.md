# תכנון פלוס (Tichnun Plus) — Hebrew planning spreadsheets & free calculators

🌐 **Live site: https://tichnun.netlify.app/**

Hebrew Excel / Google Sheets planners and free online calculators for Israeli households and freelancers:

- [מתכנן חתונה באקסל](https://tichnun.netlify.app/p/wedding-planner/) · [מחשבון כמה לשים בחתונה](https://tichnun.netlify.app/tools/wedding-gift/)
- [אקסל תקציב משק בית 2027](https://tichnun.netlify.app/p/household-budget/) · [מחשבון תקציב 50/30/20](https://tichnun.netlify.app/tools/budget-503020/)
- [אקסל לעוסק פטור 2026](https://tichnun.netlify.app/p/osek-patur-tracker/) · [מחשבון תקרת עוסק פטור](https://tichnun.netlify.app/tools/osek-patur-ceiling/) · [מחשבון מע״מ](https://tichnun.netlify.app/tools/vat-calculator/)
- [מתכנן בר/בת מצווה](https://tichnun.netlify.app/p/bar-mitzvah-planner/) · [מחשבון עלות בר מצווה](https://tichnun.netlify.app/tools/bar-mitzvah-cost/)
- [תבניות הצעת מחיר](https://tichnun.netlify.app/p/price-quote-pack/) · [מתכנן תקציב שיפוץ](https://tichnun.netlify.app/p/renovation-budget/) · [מחשבון עלות שיפוץ](https://tichnun.netlify.app/tools/renovation-cost/)
- [כל המדריכים](https://tichnun.netlify.app/guides/)

---
Project docs: `ops/PLAN.md` (master plan), `ops/STATUS.md` (status), `docs/` (site source).
Site base URL and brand live in `tools/site/site_config.py` (`BASE_URL`, `BRAND`) and `docs/assets/config.js` (`SITE_URL`).
To move hosts: `python3 tools/site/set_base_url.py https://new-host/`. Netlify publishes `docs/` at the domain root.
