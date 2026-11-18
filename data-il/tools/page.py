"""Render docs/data-il/index.html (Hebrew page with an English section) for data-il/tools/build.py."""
import html
import json


def e(s):
    return html.escape("" if s is None else str(s), quote=True)


def ils(n):
    return "₪" + (f"{n:,.2f}" if isinstance(n, float) and not float(n).is_integer() else f"{int(n):,}")


def dataset_ld(key, doc, site, gh, version):
    return {
        "@context": "https://schema.org", "@type": "Dataset",
        "name": doc["title"], "alternateName": doc.get("title_he"),
        "description": doc["description"][:4900] if len(doc["description"]) >= 50 else doc["description"] + " Open data with a source URL for every value.",
        "url": f"{site}data-il/#{key}", "sameAs": f"{gh}/data/{key}.json",
        "license": "https://creativecommons.org/publicdomain/zero/1.0/", "isAccessibleForFree": True,
        "creator": {"@type": "Organization", "name": "תכנון פלוס (Tichnun Plus)", "url": site},
        "inLanguage": ["he", "en"], "spatialCoverage": {"@type": "Place", "name": "Israel"},
        "temporalCoverage": doc.get("temporal", "2025/2030"), "dateModified": version,
        "keywords": doc.get("keywords", ["Israel", "open data"]),
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{site}data-il/{key}.json"},
            {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": f"{site}data-il/{key}.csv"}],
    }


def src_link(r):
    return f'<a href="{e(r["source_url"])}" rel="noopener" target="_blank">{e(r.get("source_title") or "מקור")}</a>'


def render(datasets, hol, version, site, gh, raw):
    docs = dict(datasets)
    lds = [dataset_ld(k, d, site, gh, version) for k, d in datasets]
    catalog = {"@context": "https://schema.org", "@type": "DataCatalog", "name": "Israeli open data by תכנון פלוס",
               "url": f"{site}data-il/", "license": "https://creativecommons.org/publicdomain/zero/1.0/",
               "dataset": [{"@type": "Dataset", "name": d["title"], "url": f"{site}data-il/#{k}"} for k, d in datasets]}

    # downloads table
    dl = "".join(
        f'<tr id="{e(k)}"><td><strong>{e(d.get("title_he") or d["title"])}</strong><br><span class="small muted" lang="en" dir="ltr">{e(d["title"])}</span></td>'
        f'<td class="num">{len(d["rows"])}</td>'
        f'<td><a href="{e(k)}.json" download>JSON</a> · <a href="{e(k)}.csv" download>CSV</a> · <a href="{gh}/data/{e(k)}.json" rel="noopener">GitHub</a></td></tr>'
        for k, d in datasets)

    # upcoming holidays (next ~14 months from the dataset's build date)
    up = [h for h in hol if version <= h["start"] <= f"{int(version[:4]) + 1}-12-31" and h["type"] != "chol-hamoed"][:40]
    hol_rows = "".join(
        f'<tr><td>{e(h["name_he"])}<br><span class="small muted" lang="en" dir="ltr">{e(h["name_en"])}</span></td>'
        f'<td class="num">{e(h["start"])}{"–" + e(h["end"][5:]) if h["end"] != h["start"] else ""}</td>'
        f'<td>{e(h["hebrew_date_he"])}</td><td>{"✔" if h["rest_day"] else ""}</td></tr>' for h in up)

    vat = docs["israel-vat-history"]["rows"]
    vat_rows = "".join(f'<tr><td class="num">{e(r["from"])}</td><td class="num">{e(r["rate_percent"])}%</td><td class="small">{src_link(r)}</td></tr>'
                       for r in reversed(vat))
    osek = docs["israel-osek-patur-ceiling"]["rows"]
    osek_rows = "".join(f'<tr><td class="num">{r["year"]}</td><td class="num">{ils(r["ceiling_ils"])}</td><td class="small">{src_link(r)}{(" · " + e(r["note"])) if r.get("note") else ""}</td></tr>'
                        for r in reversed(osek))
    mw = docs["israel-minimum-wage"]["rows"]
    mw_rows = "".join(f'<tr><td class="num">{e(r["from"])}</td><td class="num">{ils(r["monthly_ils"])}</td><td class="num">{ils(r["hourly_ils"]) if r.get("hourly_ils") else "–"}</td><td class="small">{src_link(r)}</td></tr>'
                      for r in reversed(mw))
    bl = docs.get("israel-bituach-leumi-2026")
    bl_html = ""
    if bl:
        bl_rows = "".join(f'<tr><td>{e(r["name_he"])}<br><span class="small muted" lang="en" dir="ltr">{e(r["name_en"])}</span></td><td class="num">{e(r["display"])}</td><td class="small">{src_link(r)}</td></tr>'
                          for r in bl["rows"])
        bl_html = f'''<h3 id="bl-table">ביטוח לאומי – נתוני בסיס {e(bl.get("year", ""))}</h3>
  <div class="table-wrap"><table><thead><tr><th>נתון</th><th>ערך</th><th>מקור</th></tr></thead><tbody>{bl_rows}</tbody></table></div>'''

    faq = [
        ("מה הרישיון?", "הנתונים משוחררים לנחלת הכלל (CC0 1.0) והקוד ברישיון MIT. מותר להשתמש בהם בכל מקום, גם מסחרי, בלי לבקש רשות. קרדיט עם קישור יתקבל בברכה."),
        ("איך חושבו תאריכי החגים?", "בחישוב אריתמטי של הלוח העברי (Dershowitz & Reingold), עם כללי הדחייה הנהוגים בישראל: יום טוב אחד, פסח של 7 ימים, הקדמת ודחיית יום הזיכרון ויום העצמאות, יום השואה וצומות שחלים בשבת. כל 144 התאריכים הושוו לשתי ספריות עצמאיות (hdate, pyluach) בלי אף אי-התאמה."),
        ("מתי חג מתחיל?", "שדה start הוא היום הראשון (באור יום). חגים עם begins=sunset_previous_day נכנסים בשקיעה של הערב הקודם (שדה eve). צומות קלים (גדליה, עשרה בטבת, אסתר, י״ז בתמוז) מתחילים בעלות השחר."),
        ("איך מעדכנים?", "הנתונים נבדקים מול המקורות המצוינים בכל שורה. מצאתם טעות? פתחו issue במאגר ב-GitHub."),
    ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in [catalog] + lds + [faq_ld])

    title = "נתונים פתוחים על ישראל: חגים 2025–2030, מע״מ, תקרת עוסק פטור ושכר מינימום (JSON/CSV) | תכנון פלוס"
    desc = "מאגר נתונים פתוח וחינמי (CC0): תאריכי חגים בישראל 2025–2030 בעברית ובאנגלית, היסטוריית שיעורי מע״מ, תקרת עוסק פטור, שכר מינימום וביטוח לאומי, עם מקור לכל ערך. JSON, CSV, ספריית JS ו-Python."
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{site}data-il/">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="תכנון פלוס">
<meta property="og:title" content="נתונים פתוחים על ישראל: חגים, מע״מ, עוסק פטור, שכר מינימום">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{site}data-il/">
<meta property="og:image" content="{site}assets/og-default.png">
<meta name="theme-color" content="#0e6b63">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="../assets/site.css">
<style>
.code{{direction:ltr;text-align:left;unicode-bidi:isolate;background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:.8rem 1rem;overflow:auto;font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;white-space:pre}}
.en-block{{direction:ltr;text-align:left}}
</style>
{ld}</head>
<body>
<a class="skip-link" href="#main">דלג לתוכן</a>
<header id="site-header"></header>
<main id="main">
<!-- Generated by data-il/tools/build.py, do not edit by hand. -->
<div class="container"><nav class="breadcrumbs mt-2" aria-label="פירורי לחם"><a href="../">ראשי</a> <span aria-hidden="true">›</span> <a href="../tools/">כלים חינם</a> <span aria-hidden="true">›</span> <span>נתונים פתוחים</span></nav></div>
<section class="section mt-0" style="padding-top:.5rem">
 <div class="container narrow">
  <h1>נתונים פתוחים על ישראל: חגים, מע״מ, עוסק פטור ושכר מינימום</h1>
  <p class="lead muted">מאגר קטן ומדויק למפתחים, לעיתונאים ולכל מי שבונה טופס, לוח שנה או מחשבון: תאריכי החגים בישראל 2025–2030 בעברית ובאנגלית, ושיעורים רשמיים עם קישור למקור ותאריך בדיקה לכל ערך. JSON ו-CSV, בחינם, ברישיון CC0 (נחלת הכלל).</p>
  <p class="small muted">עודכן: {e(version)} · <a href="{gh}" rel="noopener">המאגר ב-GitHub</a> · <a href="#en" hreflang="en">English below</a></p>

  <h2>הורדה</h2>
  <div class="table-wrap"><table><thead><tr><th>מאגר</th><th class="num">שורות</th><th>קבצים</th></tr></thead><tbody>{dl}</tbody></table></div>
  <p class="small muted">קובצי ה-CSV שמורים ב-UTF-8 עם BOM, כך שאקסל פותח את העברית נכון. ספריית JavaScript בקובץ אחד: <a href="israel-data.js">israel-data.js</a>.</p>

  <h2 id="holidays">חגים ומועדים בישראל – הקרובים</h2>
  <p>הטבלה המלאה (2025–2030, {len(hol)} שורות) בקבצים. ✔ = יום שבתון על פי חוק.</p>
  <div class="table-wrap"><table><thead><tr><th>חג</th><th class="num">תאריך</th><th>תאריך עברי</th><th>שבתון</th></tr></thead><tbody>{hol_rows}</tbody></table></div>

  <h2 id="rates">שיעורים והיסטוריה</h2>
  <h3 id="vat-table">שיעור מע״מ בישראל לאורך השנים</h3>
  <div class="table-wrap"><table><thead><tr><th class="num">מתאריך</th><th class="num">שיעור</th><th>מקור</th></tr></thead><tbody>{vat_rows}</tbody></table></div>
  <p class="small">חישוב מהיר: <a href="../tools/vat-calculator/">מחשבון מע״מ 18%</a></p>
  <h3 id="osek-table">תקרת עוסק פטור לפי שנה</h3>
  <div class="table-wrap"><table><thead><tr><th class="num">שנה</th><th class="num">תקרה שנתית</th><th>מקור</th></tr></thead><tbody>{osek_rows}</tbody></table></div>
  <p class="small">כמה נשאר לכם? <a href="../tools/osek-patur-ceiling/">מחשבון תקרת עוסק פטור</a></p>
  <h3 id="mw-table">שכר מינימום בישראל (לעובד בגיר)</h3>
  <div class="table-wrap"><table><thead><tr><th class="num">מתאריך</th><th class="num">חודשי</th><th class="num">לשעה</th><th>מקור</th></tr></thead><tbody>{mw_rows}</tbody></table></div>
  <p class="small">תכנון תקציב לפי ההכנסה: <a href="../tools/net-salary-budget/">מחשבון תקציב לפי משכורת נטו</a></p>
  {bl_html}

  <h2 id="use">שימוש בקוד</h2>
  <p>JavaScript (דפדפן או Node, בלי תלויות):</p>
<pre class="code">&lt;script src="{site}data-il/israel-data.js"&gt;&lt;/script&gt;
&lt;script&gt;
  IsraelData.isIsraeliHoliday("2026-04-22");  // [{{id:"yom-haatzmaut", name_he:"יום העצמאות", ...}}]
  IsraelData.isRestDay("2026-09-21");         // true (Yom Kippur)
  IsraelData.addVat(1000);                    // {{net:1000, vat:180, gross:1180, rate:0.18}}
  IsraelData.removeVat(1180);                 // {{net:1000, vat:180, gross:1180, rate:0.18}}
  IsraelData.osekPaturCeiling(2026);          // 122833
&lt;/script&gt;</pre>
  <p>Python (התקנה ישירה מ-GitHub):</p>
<pre class="code">pip install "git+https://github.com/eitanco2005-cmd/road-to-glory.git#subdirectory=data-il/python"

import israel_data as il
il.next_holiday("2026-11-18")["name_he"]   # 'חנוכה'
il.add_vat(1000)                          # {{'net': 1000.0, 'vat': 180.0, 'gross': 1180.0, 'rate': 0.18}}</pre>
  <p>או בלי שום התקנה: <code dir="ltr">fetch("{site}data-il/israel-holidays-2025-2030.json")</code>.</p>

  <h2>שאלות נפוצות</h2>
  <div class="faq">{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)}</div>
  <p class="mt-2">עוד: <a href="../embed/">מחשבונים חינם להטמעה באתר שלכם</a> · <a href="../tools/">כל המחשבונים</a></p>
 </div>
</section>

<section class="section alt" id="en" lang="en" dir="ltr">
 <div class="container narrow en-block">
  <h2>Israeli open data (English)</h2>
  <p>A small, carefully sourced dataset for developers and journalists: Israeli holiday dates 2025–2030 with Hebrew and English names
  (computed with the arithmetic Hebrew calendar, Israeli rules, cross-checked against two independent libraries), plus VAT rate history,
  the osek patur (exempt dealer) turnover ceiling, minimum wage and Bituach Leumi basics, each value with a source URL and a check date.
  Data is CC0 (public domain), code is MIT. Downloads are in the table above (JSON + CSV), the zero-dependency JavaScript helper is
  <a href="israel-data.js">israel-data.js</a> and the Python package installs straight from GitHub:</p>
<pre class="code">pip install "git+https://github.com/eitanco2005-cmd/road-to-glory.git#subdirectory=data-il/python"
npm: not published; use the CDN or copy the file:
&lt;script src="https://cdn.jsdelivr.net/gh/eitanco2005-cmd/road-to-glory@main/data-il/js/israel-data.js"&gt;&lt;/script&gt;</pre>
  <p>Source, docs and issues: <a href="{gh}" rel="noopener">github.com/eitanco2005-cmd/road-to-glory/data-il</a> ·
  Free calculators you can embed: <a href="../en/embed/">tichnun.netlify.app/en/embed/</a></p>
 </div>
</section>
</main>
<footer id="site-footer"></footer>
<script src="../assets/site.js" defer></script>
</body>
</html>
"""
