#!/usr/bin/env python3
"""Rebuild the whole seasonal-2027 stream and publish into docs/:
dates check -> workbooks -> printables -> copy deliverables (dl_folders.json + free PDFs) -> product JSONs -> previews -> pages.
    python3 release.py          (then: python3 tools/site/build_site.py)"""
import json
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DOCS = HERE.parents[1] / "docs"
run = lambda s: subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)  # noqa: E731
for step in ("verify_dates.py", "purim_planner.py", "seder_planner.py", "printables.py"):
    run(step)
folders = json.loads((HERE / "dl_folders.json").read_text(encoding="utf-8"))
for slug, d in folders.items():
    for f in d["files"]:
        (DOCS / f["path"]).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(HERE / "out" / f["src"], DOCS / f["path"])
        print("published", f["path"])
for name, dest in (("pesach-cleaning-checklist-2027.pdf", "pesach/files/"), ("savings-challenge-2027.pdf", "budget-2027/files/")):
    (DOCS / dest).mkdir(parents=True, exist_ok=True)
    shutil.copy(HERE / "out" / name, DOCS / dest / name)
    print("published", dest + name)

PRODUCTS = {
    "purim-planner": dict(title="מתכנן משלוחי מנות 2027 – אקסל", price_ils=19, tool="mishloach-manot-budget", url="p/purim-planner/",
                          subtitle="נמענים, סוגי חבילות עם עלות, רשימת קניות אוטומטית, מסלול חלוקה ותקציב כולל מתנות לאביונים",
                          image="p/purim-planner/img/dashboard.webp"),
    "seder-planner": dict(title="מתכנן ליל הסדר 2027 – אקסל", price_ils=19, tool="matza-wine-calculator", url="p/seder-planner/",
                          subtitle="אורחים, תפריט, כמויות מצות ויין לפי השיעור, רשימת קניות, תפקידים בהגדה ולוח הכנות",
                          image="p/seder-planner/img/dashboard.webp"),
}
for slug, p in PRODUCTS.items():
    obj = {"slug": slug, "title": p["title"], "subtitle": p["subtitle"], "price_ils": p["price_ils"], "bundle_of": [],
           "files": [{"label": f["label"], "path": f["path"]} for f in folders[slug]["files"]], "sheets_copy_url": None,
           "tool": p["tool"], "url": p["url"], "image": p["image"]}
    (DOCS / "data/products" / f"{slug}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
bundle = {"slug": "spring-holidays-bundle", "title": "חבילת פורים + פסח: משלוחי מנות + ליל הסדר",
          "subtitle": "מתכנן משלוחי המנות ומתכנן ליל הסדר יחד – ₪29 במקום ₪38", "price_ils": 29,
          "bundle_of": ["purim-planner", "seder-planner"], "files": [], "sheets_copy_url": None, "tool": None, "url": "pesach/"}
(DOCS / "data/products/spring-holidays-bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("product JSONs written")
for step in ("previews.py", "pages_budget.py", "pages_purim.py", "pages_pesach.py"):
    run(step)
