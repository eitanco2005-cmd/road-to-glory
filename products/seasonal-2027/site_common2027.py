"""Shared bits for the seasonal 2027 pages: reuses the Hanukkah page shell (products/hanukkah/site_common.py, unchanged)
with today's date, plus paths, the verified dates and a few page-part helpers."""
import datetime
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
from verify_dates import compute  # noqa: E402  (ours; import before the Hanukkah dir joins sys.path)
sys.path.insert(1, str(HERE.parent / "hanukkah"))
import site_common as sc  # noqa: E402

sc.UPDATED = "2026-11-18"
sc.EXTRA_CSS += """
.s27-table{width:100%;border-collapse:collapse;font-size:.97rem}.s27-table th,.s27-table td{border:1px solid var(--border);padding:.5rem .6rem;text-align:start;vertical-align:top}
.s27-table th{background:var(--surface-2)}
.s27-tag{display:inline-block;font-size:.8rem;font-weight:700;border-radius:999px;padding:.05rem .55rem;white-space:nowrap}
.s27-tag.ok{background:#dff3e4;color:#14532d}.s27-tag.exp{background:#fff4c2;color:#6b4e00}.s27-tag.unk{background:#fbe3e1;color:#7f1d1d}
.s27-dl{display:flex;gap:1rem;align-items:center;flex-wrap:wrap;background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius);padding:1rem}
.s27-dl img{width:150px;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff}
.s27-groups{display:grid;gap:.5rem}.s27-grow{display:grid;grid-template-columns:1fr 6.5rem 6.5rem;gap:.5rem;align-items:end}
.s27-grow .field{margin:0}.s27-grow .gl{font-weight:700;padding-bottom:.55rem}
.s27-check{list-style:none;padding-inline-start:0}.s27-check li::before{content:"☐ ";color:var(--primary)}
@media(max-width:420px){.s27-grow{grid-template-columns:1fr 5.2rem 5.2rem}}
"""
page, faq_html, faq_ld, product_ld, app_ld, article_ld, BASE = (sc.page, sc.faq_html, sc.faq_ld, sc.product_ld, sc.app_ld,
                                                                 sc.article_ld, sc.BASE)
D = compute()
MONTHS_HE = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
DAYS_HE = ["שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת", "ראשון"]


def hd(d, evening=False, weekday=True):
    """'יום רביעי, 21 באפריל 2027' (evening=True -> the evening before, as Jewish holidays start)."""
    if evening:
        d = d - datetime.timedelta(days=1)
    s = f"{d.day} ב{MONTHS_HE[d.month - 1]} {d.year}"
    return (f"יום {DAYS_HE[d.weekday()]}{' בערב' if evening else ''}, " + s) if weekday else s


def short(d):
    return f"{d.day}.{d.month}.{d.year}"


# ------------------------------------------------------------------ paths
BUD, BUD_WC, BUD_CH = "budget-2027/", "budget-2027/what-changes-2027/", "budget-2027/savings-challenge/"
PUR, P_PROD, P_TOOL = "purim/", "p/purim-planner/", "tools/mishloach-manot-budget/"
P_G1, P_G2, P_G3 = "purim/mishloach-manot-ideas/", "purim/purim-halacha/", "purim/class-mishloach-manot/"
PES, S_PROD, S_TOOL, CLEAN = "pesach/", "p/seder-planner/", "tools/matza-wine-calculator/", "pesach/cleaning-checklist/"
S_G1, S_G2, S_G3 = "pesach/seder-night-guide/", "pesach/pesach-2027-dates/", "pesach/pesach-budget/"
EN_SEDER, EN_SCALC, EN_HOST, EN_CHECK = ("en/p/passover-seder-planner/", "en/tools/seder-shopping-calculator/",
                                         "en/guides/how-to-host-a-passover-seder/", "en/guides/passover-seder-checklist/")
HB = "p/household-budget/"
PDF_CLEAN = "pesach/files/pesach-cleaning-checklist-2027.pdf"
PDF_SAVE = "budget-2027/files/savings-challenge-2027.pdf"
BUNDLE = "spring-holidays-bundle"


def guide(path, title, desc, h1, body_html, faq, crumbs, alt=None, img=None, minutes=None, buy=False, scripts=()):
    upd = "עודכן: 18 בנובמבר 2026" + (f" · זמן קריאה: {minutes} דקות" if minutes else "")
    body = (f'<article class="section"><div class="container narrow prose">{{CRUMBS}}<h1>{h1}</h1><p class="updated muted">{upd}</p>'
            f'{body_html}' + (("<h2>שאלות נפוצות</h2>" + faq_html(faq)) if faq else "") + "</div></article>")
    lds = [article_ld(h1, desc, path, "he", img)] + ([faq_ld(faq)] if faq else [])
    return page(path, title, desc, body, lds, og_image=img, crumbs=crumbs, alt=alt, og_type="article", buy=buy, scripts=scripts)


def cta(title, text, href, btn):
    return (f'<div class="cta-box mt-4"><div><h2 class="h3">{title}</h2><p>{text}</p></div>'
            f'<a class="btn accent" href="{{up}}{href}">{btn}</a></div>')


def links(items):
    return '<ul class="hk-list">' + "".join(
        f'<li><a href="{{up}}{h}"{(" hreflang=" + chr(34) + "en" + chr(34) + " lang=" + chr(34) + "en" + chr(34)) if h.startswith("en/") else ""}>{t}</a></li>'
        for t, h in items) + "</ul>"


def collection_ld(t, d, path):
    return {"@context": "https://schema.org", "@type": "CollectionPage", "name": t, "description": d, "url": BASE + path, "inLanguage": "he-IL"}


def howto_ld(name, steps, path):
    return {"@context": "https://schema.org", "@type": "HowTo", "name": name, "inLanguage": "he-IL", "url": BASE + path,
            "step": [{"@type": "HowToStep", "position": i + 1, "name": s} for i, s in enumerate(steps)]}


def write_json(path, obj):
    p = sc.DOCS / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
