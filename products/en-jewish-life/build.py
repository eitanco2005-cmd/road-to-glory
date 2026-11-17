#!/usr/bin/env python3
"""Build + publish the English Jewish-life planners.

    python3 products/en-jewish-life/build.py [--no-shots]

Writes blank + example .xlsx into docs/dl/<folder>/, screenshots into docs/en/p/<slug>/img/, and
docs/data/products/<slug>.json (currency USD, lang en) for each product and the bundle.
"""
import argparse
import json
import os
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
DOCS = REPO / "docs"
sys.path.insert(0, str(HERE))

import event  # noqa: E402
import holidays  # noqa: E402
import seder  # noqa: E402
from event_configs import BAR_MITZVAH, WEDDING  # noqa: E402

PRODUCTS = [
    dict(slug="bar-mitzvah-planner-en", key="bar-mitzvah-planner", folder="l9e1t1e7ryqmfim5", price=19,
         title="Bar / Bat Mitzvah Planner (Excel & Google Sheets)",
         subtitle="Budget, vendors & payments, guest list & RSVPs, gifts & thank-yous, aliyot & candle-lighting, seating, checklist",
         file="bar-bat-mitzvah-planner", tool="bar-mitzvah-budget",
         build=lambda demo: event.build(BAR_MITZVAH, demo)),
    dict(slug="jewish-wedding-planner", key="jewish-wedding-planner", folder="m8gvkisyw6as1zfi", price=24,
         title="Jewish Wedding Planner (Excel & Google Sheets)",
         subtitle="Budget, vendors & payments, guests & RSVPs, ketubah & chuppah honors, seating, checklist, day-of timeline",
         file="jewish-wedding-planner", tool=None,
         build=lambda demo: event.build(WEDDING, demo)),
    dict(slug="passover-seder-planner", key="passover-seder-planner", folder="2zw7zvvwvjwjx5ut", price=15,
         title="Passover Seder Planner (Excel & Google Sheets)",
         subtitle="Guests for one or two seders, shopping list scaled by head count, menu, haggadah parts, prep timeline",
         file="passover-seder-planner", tool="seder-shopping-calculator",
         build=seder.build),
    dict(slug="jewish-holiday-planner", key="jewish-holiday-planner", folder="i1rkd4uhly4erf8l", price=15,
         title="Jewish Holiday Hosting Planner (Excel & Google Sheets)",
         subtitle="Rosh Hashanah to Shavuot plus Shabbat: guests, menus, shopping & budget, traditions, mishloach manot",
         file="jewish-holiday-planner", tool=None,
         build=holidays.build),
]
BUNDLE = dict(slug="jewish-life-bundle", price=49, title="Jewish Life Bundle: all 4 planners",
              subtitle="Bar/Bat Mitzvah, Jewish Wedding, Passover Seder and Holiday Hosting planners: $49 instead of $73")


def page_slug(p):
    """URL slug of the English page (the bar mitzvah JSON slug carries -en to avoid clashing with the Hebrew one)."""
    return p["key"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-shots", action="store_true")
    a = ap.parse_args()
    import shots
    for p in PRODUCTS:
        d = DOCS / "dl" / p["folder"]
        d.mkdir(parents=True, exist_ok=True)
        blank, demo = d / f"{p['file']}.xlsx", d / f"{p['file']}-example.xlsx"
        p["build"](False).save(blank)
        p["build"](True).save(demo)
        print("wrote", blank.relative_to(REPO), demo.relative_to(REPO))
        img = DOCS / "en" / "p" / page_slug(p) / "img"
        if not a.no_shots:
            shutil.rmtree(img, ignore_errors=True)
            shots.render("bar-mitzvah-planner" if p["key"] == "bar-mitzvah-planner" else p["key"], str(img))
            print("shots ->", img.relative_to(REPO))
        data = {
            "slug": p["slug"], "lang": "en", "currency": "USD", "price": p["price"],
            "title": p["title"], "subtitle": p["subtitle"], "bundle_of": [],
            "files": [{"label": "The planner (Excel, blank: start here)", "path": f"dl/{p['folder']}/{blank.name}"},
                      {"label": "Filled-in example (to see how it works)", "path": f"dl/{p['folder']}/{demo.name}"}],
            "sheets_copy_url": None, "tool": p["tool"], "page": f"en/p/{page_slug(p)}/",
            "image": f"en/p/{page_slug(p)}/img/screen-1.webp",
        }
        (DOCS / "data" / "products" / f"{p['slug']}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    b = {"slug": BUNDLE["slug"], "lang": "en", "currency": "USD", "price": BUNDLE["price"], "title": BUNDLE["title"],
         "subtitle": BUNDLE["subtitle"], "bundle_of": [p["slug"] for p in PRODUCTS], "files": [], "sheets_copy_url": None,
         "tool": None, "page": "en/planners/"}
    (DOCS / "data" / "products" / "jewish-life-bundle.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
    idx = {"_note": "English catalogue (Stream A). Prices in USD. Not part of the Hebrew index.json.",
           "products": [{"slug": p["slug"], "page": f"en/p/{page_slug(p)}/"} for p in PRODUCTS],
           "bundles": [BUNDLE["slug"]]}
    (DOCS / "data" / "products" / "index-en.json").write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")
    print("product JSON written")


if __name__ == "__main__":
    main()
