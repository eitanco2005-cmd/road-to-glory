#!/usr/bin/env python3
"""R6A: "who wrote this and how we checked" box on the main wedding pages (called by tools/site/build_site.py).

Idempotent: replaces <!-- trust -->…<!-- /trust --> or inserts it right before </main>. One short, honest box per
page type: who we are (link to about/), when the page was last reviewed, how the numbers are produced, sources policy.
To mark a page as re-reviewed, change REVIEWED (or a per-page "reviewed") and rebuild.
"""
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
REVIEWED = "22 בנובמבר 2026"

METHOD = {
    "calc": "החישוב רץ בדפדפן שלכם ושום נתון לא נשלח. כל המקדמים והנוסחה מפורטים בעמוד, והמחירים הבסיסיים לקוחים ממחירונים ומכתבות מתוארכים (קישורים בסעיף המקורות). כשאין נתון רשמי, כתוב במפורש שזו הערכה שלנו.",
    "gift": "הסכומים בטבלאות מחושבים באותו מודל של מחשבון כמה לשים בחתונה: מחיר מנה מדווח ל-2026 × חלק מהמנה לפי קרבה, ומעוגלים ל-50 ₪. מחירי המנה מגיעים ממחירונים מתוארכים; מקדמי הקרבה הם כיול שלנו ולא נתון רשמי, ומנהג משפחתי גובר עליהם.",
    "prices": "כל טווח מחירים בעמוד מגיע ממקור מתוארך שמקושר ליד השורה. איפה שהמקורות סותרים, הצגנו את הטווח הרחב וציינו זאת. לא קיבלנו תשלום מאף ספק ואין כאן קישורי שותפים.",
    "guide": "המדריך נכתב מתוך מקורות ציבוריים שמקושרים בעמוד (מחירונים, כל זכות, אתרי רשויות) ומניסיון מעשי בתכנון. במקום שבו אנחנו ממליצים ולא מצטטים, זה כתוב כך.",
    "product": "המוצר נבנה ונבדק על ידינו: הכלים רצים בדפדפן והרשימות שלכם לא נשלחות אלינו. צילומי המסך בעמוד הם מהכלי עצמו עם נתונים בדויים. אין כאן ביקורות או דירוגים מפוברקים.",
    "hub": "העמוד מרכז את הכלים והמדריכים שלנו לחתונה. הסכומים בו מחושבים במחשבונים שבאתר, ולכל עמוד משנה יש סעיף מקורות משלו.",
}

PAGES = {
    "chatuna/": "hub", "chatuna/mechirim/": "prices",
    "tools/wedding-gift/": "calc", "tools/wedding-cost/": "calc", "tools/wedding-timeline/": "calc",
    "chatuna/haavarat-kesef/": "guide", "chatuna/ma-lilbosh/": "guide", "chatuna/rayonot-matana/": "guide",
    "guides/wedding-checklist/": "guide", "guides/wedding-guest-list/": "guide", "guides/wedding-save-money/": "guide",
    "guides/wedding-vendor-contracts/": "guide", "p/wedding-planner/guides/rsvp-seating-gifts/": "guide",
    "p/seating-chart/guides/how-to-seat-guests/": "guide", "p/seating-chart/guides/tables-and-seats/": "guide",
    "p/invitation-maker/guides/wedding-invitation-wording/": "guide", "p/invitation-maker/guides/print-invitations/": "guide",
    "p/wedding-planner/": "product", "p/seating-chart/": "product", "apps/rsvp/": "product", "p/invitation-maker/": "product",
}
for d in sorted((DOCS / "chatuna" / "kama-lasim").iterdir()):
    if (d / "index.html").exists():
        PAGES[f"chatuna/kama-lasim/{d.name}/"] = "gift"
for d in sorted((DOCS / "chatuna" / "mechirim").iterdir()):
    if (d / "index.html").exists():
        PAGES[f"chatuna/mechirim/{d.name}/"] = "prices"

MARK = re.compile(r"<!-- trust -->.*?<!-- /trust -->\n?", re.S)


def box(url, kind):
    up = "../" * url.count("/")
    return ('<!-- trust --><section class="section" style="padding-top:0" aria-label="מי אנחנו ואיך בדקנו"><div class="container narrow">'
            '<aside class="callout small trust-box"><p class="mb-1"><strong>מי כתב ואיך בדקנו</strong> · '
            f'נסקר ועודכן: <time datetime="2026-11-22">{REVIEWED}</time></p>'
            f'<p class="mb-1">{METHOD[kind]}</p>'
            f'<p class="mb-0">תכנון פלוס הוא פרויקט ישראלי קטן. <a href="{up}about/">מי אנחנו, איך המחשבונים עובדים ומדיניות המקורות</a> · '
            f'מצאתם טעות? <a href="mailto:eitanco2005@gmail.com">כתבו לנו</a> ונתקן.</p></aside></div></section><!-- /trust -->\n')


def main():
    n = 0
    for url, kind in PAGES.items():
        f = DOCS / url / "index.html"
        if not f.exists():
            print("trust_box: missing", url)
            continue
        s = f.read_text(encoding="utf-8")
        b = box(url, kind)
        new = MARK.sub(lambda m: b, s) if MARK.search(s) else s.replace("</main>", b + "</main>", 1)
        if new != s:
            f.write_text(new, encoding="utf-8")
            n += 1
    print(f"trust_box: {len(PAGES)} pages, {n} updated")


if __name__ == "__main__":
    main()
