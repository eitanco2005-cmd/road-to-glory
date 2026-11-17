"""Build both event planners and publish them into docs/:
- docs/dl/<secret>/...       downloadable files (ASCII names)
- docs/p/<slug>/img/*.png    screenshots of the filled demo
- docs/data/products/<slug>.json (+ event-bundle.json)
Run from anywhere:  python3 products/wedding-planner/publish.py
"""
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DOCS = os.path.join(REPO, "docs")
sys.path.insert(0, HERE)
from docx_engine import build_docx  # noqa: E402
from event_engine import build_workbook  # noqa: E402
from shots import render  # noqa: E402


def load_cfg(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(os.path.dirname(path)).replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CFG


PRODUCTS = [
    dict(slug="wedding-planner", cfg=os.path.join(HERE, "build.py"), secret="lje2wikbyyh1goea",
         base="wedding-planner", tool="wedding-gift", price=49,
         title="מתכנן חתונה באקסל ו-Google Sheets",
         subtitle="תקציב, מוזמנים ואישורי הגעה, מתנות, ספקים, לוח תשלומים, צ'קליסט והושבה – בקובץ אחד",
         labels=("מתכנן החתונה (Excel, ריק – להתחיל לעבוד)", "קובץ דוגמה ממולא (להתרשמות)",
                 "נוסחים מוכנים, לוח זמנים וצ'קליסט להדפסה (Word)")),
    dict(slug="bar-mitzvah-planner", cfg=os.path.join(HERE, "..", "bar-mitzvah-planner", "build.py"),
         secret="3lvcpz0f1kr21brs", base="bar-bat-mitzvah-planner", tool="bar-mitzvah-cost", price=39,
         title="מתכנן בר / בת מצווה באקסל ו-Google Sheets",
         subtitle="תקציב, מוזמנים ואישורי הגעה, מתנות, ספקים, תשלומים, צ'קליסט כולל עלייה לתורה, והושבה",
         labels=("מתכנן בר/בת המצווה (Excel, ריק – להתחיל לעבוד)", "קובץ דוגמה ממולא (להתרשמות)",
                 "נוסחים מוכנים, לוח זמנים וצ'קליסט להדפסה (Word)")),
]


def main(shots=True):
    os.makedirs(os.path.join(DOCS, "data", "products"), exist_ok=True)
    for p in PRODUCTS:
        cfg = load_cfg(p["cfg"])
        dl = os.path.join(DOCS, "dl", p["secret"])
        os.makedirs(dl, exist_ok=True)
        names = [f"{p['base']}.xlsx", f"{p['base']}-example.xlsx", f"{p['base']}-messages.docx"]
        build_workbook(cfg, demo=False).save(os.path.join(dl, names[0]))
        build_workbook(cfg, demo=True).save(os.path.join(dl, names[1]))
        build_docx(cfg, os.path.join(dl, names[2]))
        if shots:
            img = os.path.join(DOCS, "p", p["slug"], "img")
            os.makedirs(img, exist_ok=True)
            render(cfg, img, "screen")
        data = {
            "slug": p["slug"], "title": p["title"], "subtitle": p["subtitle"], "price_ils": p["price"],
            "bundle_of": [],
            "files": [{"label": lab, "path": f"dl/{p['secret']}/{n}"} for lab, n in zip(p["labels"], names)],
            "sheets_copy_url": None, "tool": p["tool"],
        }
        with open(os.path.join(DOCS, "data", "products", p["slug"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    bundle = {"slug": "event-bundle", "title": "חבילת אירועים: חתונה + בר/בת מצווה",
              "subtitle": "שני המתכננים המלאים במחיר אחד – ₪69 במקום ₪88",
              "price_ils": 69, "bundle_of": ["wedding-planner", "bar-mitzvah-planner"], "files": [],
              "sheets_copy_url": None, "tool": None}
    with open(os.path.join(DOCS, "data", "products", "event-bundle.json"), "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print("published")


if __name__ == "__main__":
    main(shots="--no-shots" not in sys.argv)
