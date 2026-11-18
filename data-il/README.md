# Israeli open data: holidays 2025–2030, VAT, osek patur, minimum wage, Bituach Leumi

[עברית למטה](#עברית) · Live page with downloads: **https://tichnun.netlify.app/data-il/**

Small, carefully sourced datasets for developers, journalists and anyone building a form, calendar or calculator for Israel.
**Data: CC0 1.0 (public domain). Code: MIT.** Every rate carries a source URL, a check date and how it was verified.

| Dataset | Rows | JSON | CSV |
|---|---|---|---|
| Israeli holidays 2025–2030 (Hebrew + English names, Hebrew dates, rest days) | 144 | [json](data/israel-holidays-2025-2030.json) | [csv](data/israel-holidays-2025-2030.csv) |
| VAT (מע״מ) rate history since 1976 | 18 | [json](data/israel-vat-history.json) | [csv](data/israel-vat-history.csv) |
| Osek patur (exempt dealer) turnover ceiling 2016–2026 | 11 | [json](data/israel-osek-patur-ceiling.json) | [csv](data/israel-osek-patur-ceiling.csv) |
| Minimum wage (monthly + hourly) since 2015 | 8 | [json](data/israel-minimum-wage.json) | [csv](data/israel-minimum-wage.csv) |
| Bituach Leumi (National Insurance) 2026 basics | 9 | [json](data/israel-bituach-leumi-2026.json) | [csv](data/israel-bituach-leumi-2026.csv) |

CSV files are UTF-8 with a BOM, so Excel shows the Hebrew correctly.

## Holidays: how the dates are made

* Computed with the arithmetic Hebrew calendar (Dershowitz & Reingold, *Calendrical Calculations*): [`tools/hebrew_calendar.py`](tools/hebrew_calendar.py), no dependencies.
* Israeli rules: one-day Yom Tov, 7-day Pesach, Yom HaShoah / Yom HaZikaron / Yom HaAtzmaut moved away from Shabbat,
  fasts that fall on Shabbat postponed (Ta'anit Esther moved back to Thursday).
* **Verified:** all 144 dates were cross-checked against two independent libraries, [hdate](https://github.com/py-libhdate/py-libhdate)
  (every holiday, including the modern days) and [pyluach](https://github.com/simlist/pyluach) (religious holidays and fasts), plus
  published anchor dates. 249 checks, 0 mismatches: [`tools/verify_holidays.py`](tools/verify_holidays.py).
* Fields: `start` / `end` are the daytime dates; `begins` is `sunset_previous_day` (then `eve` is the evening it starts) or
  `dawn` (minor fasts); `rest_day` is a statutory day of rest in Israel; `type` is `major`, `minor`, `chol-hamoed`, `fast` or `modern`.

## JavaScript (zero dependencies, browser or Node)

Not on npm. Use the file from the site, from jsDelivr, or copy [`js/israel-data.js`](js/israel-data.js) into your project.

```html
<script src="https://tichnun.netlify.app/data-il/israel-data.js"></script>
<!-- or: https://cdn.jsdelivr.net/gh/eitanco2005-cmd/road-to-glory@main/data-il/js/israel-data.js -->
<script>
  IsraelData.isIsraeliHoliday("2026-04-22");   // [{id:"yom-haatzmaut", name_he:"יום העצמאות", name_en:"Yom HaAtzmaut (Independence Day)", …}]
  IsraelData.isRestDay("2026-09-21");          // true (Yom Kippur);  isRestDay(d, {shabbat:true}) also counts Saturdays
  IsraelData.nextHoliday("2026-11-18").start;  // "2026-12-05" (Hanukkah)
  IsraelData.addVat(1000);                     // {net:1000, vat:180, gross:1180, rate:0.18}
  IsraelData.removeVat(1180);                  // {net:1000, vat:180, gross:1180, rate:0.18}
  IsraelData.vatRate("2024-06-01");            // 0.17
  IsraelData.osekPaturCeiling(2026);           // 122833
  IsraelData.minimumWage("2026-11-18");        // {monthly:6443.85, hourly:35.4, from:"2026-04-01", source:"…"}
</script>
```

```js
// Node
const IL = require("./israel-data.js");
```

## Python (zero dependencies)

Not on PyPI. Install straight from GitHub:

```bash
pip install "git+https://github.com/eitanco2005-cmd/road-to-glory.git#subdirectory=data-il/python"
```

```python
import israel_data as il
il.is_israeli_holiday("2026-04-22")       # [{'id': 'yom-haatzmaut', 'name_he': 'יום העצמאות', ...}]
il.is_rest_day("2026-09-21")              # True
il.next_holiday("2026-11-18")["name_en"]  # 'Hanukkah'
il.add_vat(1000)                          # {'net': 1000.0, 'vat': 180.0, 'gross': 1180.0, 'rate': 0.18}
il.remove_vat(1180, date="2024-06-01")    # uses the 17% rate in force then
il.osek_patur_ceiling(2026)               # 122833
il.minimum_wage("2026-11-18")["monthly"]  # 6443.85
```

Or no install at all: `requests.get("https://tichnun.netlify.app/data-il/israel-holidays-2025-2030.json").json()`.

## Sources and corrections

Rates live in [`tools/rates_sources.py`](tools/rates_sources.py), one source per row, with `verification` = `2+ sources` or
`1 source`. Rows we could not confirm are left out. Rebuild everything with `python3 data-il/tools/build.py`.
Found a mistake or a new rate? Open an issue.

## Free calculators that use this data

[VAT calculator 18%](https://tichnun.netlify.app/tools/vat-calculator/) ·
[Osek patur ceiling](https://tichnun.netlify.app/tools/osek-patur-ceiling/) ·
[Budget by net salary](https://tichnun.netlify.app/tools/net-salary-budget/) ·
[50/30/20 budget](https://tichnun.netlify.app/tools/budget-503020/) ·
[Wedding gift calculator](https://tichnun.netlify.app/tools/wedding-gift/) ·
[Embed any of them on your site](https://tichnun.netlify.app/embed/)

---

## עברית

**נתונים פתוחים על ישראל** – מאגר קטן ומדויק: תאריכי החגים בישראל 2025–2030 בעברית ובאנגלית, היסטוריית שיעורי המע״מ, תקרת
עוסק פטור לפי שנה, שכר המינימום ונתוני הבסיס של ביטוח לאומי 2026. לכל ערך יש קישור למקור ותאריך בדיקה.
**הנתונים בנחלת הכלל (CC0), הקוד ברישיון MIT** – מותר להשתמש בכל מקום, גם מסחרי, בלי לבקש רשות.

* **הורדה:** JSON ו-CSV בטבלה למעלה, או מהאתר: https://tichnun.netlify.app/data-il/ (ה-CSV נפתח באקסל בעברית תקינה).
* **החגים** חושבו בחישוב אריתמטי של הלוח העברי לפי המנהג בישראל (יום טוב אחד, דחיית יום הזיכרון ויום העצמאות, צומות שחלים
  בשבת), והושוו לשתי ספריות עצמאיות: 249 בדיקות, אפס אי-התאמות.
* **JavaScript:** `<script src="https://tichnun.netlify.app/data-il/israel-data.js"></script>` ואז
  `IsraelData.isIsraeliHoliday("2026-04-22")`, `IsraelData.addVat(1000)`, `IsraelData.osekPaturCeiling(2026)`.
* **Python:** `pip install "git+https://github.com/eitanco2005-cmd/road-to-glory.git#subdirectory=data-il/python"` ואז
  `import israel_data as il; il.add_vat(1000)`.
* **מחשבונים חינם:** [מחשבון מע״מ](https://tichnun.netlify.app/tools/vat-calculator/) ·
  [תקרת עוסק פטור](https://tichnun.netlify.app/tools/osek-patur-ceiling/) ·
  [תקציב לפי נטו](https://tichnun.netlify.app/tools/net-salary-budget/) ·
  [כמה לשים בחתונה](https://tichnun.netlify.app/tools/wedding-gift/) ·
  [הטמעת מחשבון באתר שלכם](https://tichnun.netlify.app/embed/)

מצאתם טעות? פתחו issue במאגר.
