#!/usr/bin/env python3
"""Add a "next step" strip + link to the wedding hub (docs/chatuna/) to every older wedding page.

    python3 tools/wedding/link_wedding.py      (idempotent; also run by tools/site/build_site.py)

The strip sits right before </main>, between <!-- wedding-next --> and <!-- /wedding-next --> markers.
Pages built in round 4 (hub, gift sub-pages, guest guides, cost/timeline tools, RSVP app) carry their own links.
"""
import pathlib
import re

DOCS = pathlib.Path(__file__).resolve().parents[2] / "docs"
HUB = "chatuna/"
GIFT_QUICK = [("chatuna/kama-lasim/zug/", "בזוג"), ("chatuna/kama-lasim/ben-dod/", "לבן דוד"), ("chatuna/kama-lasim/lo-magiim/", "אם לא מגיעים"),
              ("chatuna/kama-lasim/yom-shishi/", "ביום שישי"), ("chatuna/kama-lasim/gan-eruim/", "בגן אירועים"), ("chatuna/kama-lasim/makom-yukrati/", "במקום יוקרתי"),
              ("chatuna/kama-lasim/chatuna-ktana/", "בחתונה קטנה"), ("chatuna/kama-lasim/tzafon-darom/", "בצפון ובדרום")]
RSVP = ("apps/rsvp/", "רשימת מוזמנים ואישורי הגעה", "ייבוא אנשי קשר, תזכורת בוואטסאפ בלחיצה והעברה להושבה. חינם עד 80 הזמנות")
COST = ("tools/wedding-cost/", "מחשבון עלות חתונה", "כמה תעלה החתונה לפי מוזמנים, אזור, עונה ויום, וכמה יחזור במתנות")
TIMELINE = ("tools/wedding-timeline/", "לוח זמנים אישי לחתונה", "מזינים תאריך ומקבלים מה לסגור בכל חודש")
SEATING = ("apps/seating/", "סידורי הושבה", "מעבירים את המאשרים ומושיבים אוטומטית לפי צד וקבוצה")
INVITE = ("apps/invite/", "מעצב ההזמנות", "הזמנה לחתונה לוואטסאפ ולדפוס")
BUNDLE = ("p/wedding-bundle/", "חבילת החתונה ב-₪79", "מתכנן, אישורי הגעה, הושבה והזמנה במקום ₪126")
PRICES = ("chatuna/mechirim/", "מחירון ספקים לחתונה 2026", "כמה עולה צלם, DJ, שמלה, איפור, רב והסעות, עם מקורות")
GIVE = ("chatuna/haavarat-kesef/", "איך לתת כסף בחתונה", "צ'ק, ביט, פייבוקס או העברה, ומה לכתוב")
WEAR = ("chatuna/ma-lilbosh/", "מה ללבוש לחתונה", "לפי סוג המקום והשעה")

PAGES = {
    "tools/wedding-gift/index.html": dict(steps=[GIVE, WEAR], quick=True),
    "guides/wedding-checklist/index.html": dict(steps=[TIMELINE, COST, PRICES]),
    "guides/wedding-guest-list/index.html": dict(steps=[RSVP, SEATING]),
    "guides/wedding-save-money/index.html": dict(steps=[PRICES, COST, BUNDLE]),
    "guides/wedding-vendor-contracts/index.html": dict(steps=[PRICES, COST, TIMELINE]),
    "p/wedding-planner/index.html": dict(steps=[RSVP, BUNDLE]),
    "p/wedding-planner/guides/rsvp-seating-gifts/index.html": dict(steps=[RSVP, SEATING]),
    "p/seating-chart/index.html": dict(steps=[RSVP, INVITE]),
    "p/seating-chart/guides/how-to-seat-guests/index.html": dict(steps=[RSVP, SEATING]),
    "p/seating-chart/guides/tables-and-seats/index.html": dict(steps=[RSVP, SEATING]),
    "apps/seating/index.html": dict(steps=[RSVP, BUNDLE]),
    "p/invitation-maker/index.html": dict(steps=[RSVP, TIMELINE]),
    "p/invitation-maker/guides/wedding-invitation-wording/index.html": dict(steps=[INVITE, RSVP]),
    "p/invitation-maker/guides/print-invitations/index.html": dict(steps=[INVITE, RSVP]),
    "apps/invite/index.html": dict(steps=[RSVP, SEATING]),
}
MARK = re.compile(r"<!-- wedding-next -->.*?<!-- /wedding-next -->\n?", re.S)


def strip(page: str, cfg) -> str:
    up = "../" * (len(pathlib.PurePosixPath(page).parts) - 1)
    items = "".join(f'<li><a href="{up}{u}"><strong>{t}</strong></a> – {d}</li>' for u, t, d in cfg["steps"])
    quick = ""
    if cfg.get("quick"):
        quick = '<p class="small mb-0">תשובה מהירה: כמה לשים ' + " · ".join(f'<a href="{up}{u}">{t}</a>' for u, t in GIFT_QUICK) + "</p>"
    return ('<!-- wedding-next --><section class="section wedding-next" style="padding-top:0" aria-label="הצעד הבא"><div class="container narrow">'
            f'<div class="callout"><strong>הצעד הבא</strong><ul class="mb-1">{items}</ul>{quick}'
            f'<p class="small mb-0">כל הכלים והמדריכים לחתונה, לאורחים ולזוגות: <a href="{up}{HUB}">הכל לחתונה ←</a></p></div>'
            "</div></section><!-- /wedding-next -->\n")


def main():
    n = 0
    for page, cfg in PAGES.items():
        f = DOCS / page
        if not f.exists():
            print("missing", page)
            continue
        src = f.read_text(encoding="utf-8")
        new = MARK.sub("", src).replace("</main>", strip(page, cfg) + "</main>", 1)
        if new != src:
            f.write_text(new, encoding="utf-8")
            n += 1
    print(f"wedding-next: {n} page(s) updated")


if __name__ == "__main__":
    main()
