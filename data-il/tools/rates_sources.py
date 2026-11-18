"""Hand-curated Israeli rate tables for data-il, one source URL per row.

`verification` says how each value was checked on CHECKED:
  "2+ sources"   the same value and date appear in at least two independent sources
  "1 source"     only one source found; treat with care
Values were confirmed from the sources' published text (search-indexed copies of the pages listed). Official pages
(gov.il, btl.gov.il) are cited where they publish the figure. Found an error? Open an issue on GitHub.
Rows that could not be confirmed are left out on purpose (e.g. minimum wage before April 2015, VAT 1976–1985 variants
that only one site lists).
"""
CHECKED = "2026-11-18"

WIKI_VAT = "https://he.wikipedia.org/wiki/תבנית:מס_ערך_מוסף_בישראל"
CAP_VAT = "https://info.cap.co.il/vat-rates/"
WIKI_VAT_ARTICLE = "https://he.wikipedia.org/wiki/מס_ערך_מוסף"

HOLIDAY_SOURCES = [
    {"title": "Dershowitz & Reingold, Calendrical Calculations (arithmetic Hebrew calendar)", "url": "https://www.cambridge.org/9781107057623"},
    {"title": "hdate (py-libhdate), used to cross-check every date", "url": "https://github.com/py-libhdate/py-libhdate"},
    {"title": "pyluach, used to cross-check religious holidays and fasts", "url": "https://github.com/simlist/pyluach"},
]


def _vat(frm, to, rate, url, title, ver, note=None):
    return {"from": frm, "to": to, "rate_percent": rate, "source_url": url, "source_title": title,
            "verification": ver, "checked": CHECKED, "note": note}


VAT_ROWS = [
    _vat("1976-07-01", "1977-10-31", 8, CAP_VAT, "CAP – היסטוריית שיעורי מע״מ בישראל", "2+ sources",
         "VAT introduced in Israel on 1 July 1976 (also he.wikipedia: מס ערך מוסף)"),
    _vat("1977-11-01", "1982-07-31", 12, CAP_VAT, "CAP – היסטוריית שיעורי מע״מ בישראל", "1 source",
         "he.wikipedia says 12% came with the October 1977 economic reform; exact start date varies by source"),
    _vat("1982-08-01", "1985-05-31", 15, CAP_VAT, "CAP – היסטוריית שיעורי מע״מ בישראל", "1 source",
         "one calculator site gives 1982-07-27"),
    _vat("1985-06-01", "1985-09-30", 17, WIKI_VAT, "ויקיפדיה – תבנית:מס ערך מוסף בישראל", "2+ sources"),
    _vat("1985-10-01", "1990-02-28", 15, WIKI_VAT, "ויקיפדיה – תבנית:מס ערך מוסף בישראל", "2+ sources"),
    _vat("1990-03-01", "1990-12-31", 16, WIKI_VAT, "ויקיפדיה – תבנית:מס ערך מוסף בישראל", "2+ sources"),
    _vat("1991-01-01", "1992-12-31", 18, WIKI_VAT, "ויקיפדיה – תבנית:מס ערך מוסף בישראל", "2+ sources"),
    _vat("1993-01-01", "2002-06-14", 17, WIKI_VAT, "ויקיפדיה – תבנית:מס ערך מוסף בישראל", "2+ sources"),
    _vat("2002-06-15", "2004-02-29", 18, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources"),
    _vat("2004-03-01", "2005-08-31", 17, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources"),
    _vat("2005-09-01", "2006-06-30", 16.5, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources",
         "one source gives 2005-09-15"),
    _vat("2006-07-01", "2009-06-30", 15.5, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources"),
    _vat("2009-07-01", "2009-12-31", 16.5, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources"),
    _vat("2010-01-01", "2012-08-31", 16, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources"),
    _vat("2012-09-01", "2013-06-01", 17, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources"),
    _vat("2013-06-02", "2015-09-30", 18, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources"),
    _vat("2015-10-01", "2024-12-31", 17, WIKI_VAT_ARTICLE, "ויקיפדיה – מס ערך מוסף", "2+ sources"),
    _vat("2025-01-01", None, 18, "https://www.vatupdate.com/2024/12/30/israels-vat-rate-to-increase-to-18-starting-january-2025/",
         "VATupdate – Israel's VAT rate to increase to 18% starting January 2025", "2+ sources",
         "Israel Tax Authority, צו מס ערך מוסף (שיעור המס); current rate"),
]


def _osek(year, ceiling, url, title, ver, note=None):
    return {"year": year, "ceiling_ils": ceiling, "source_url": url, "source_title": title, "verification": ver,
            "checked": CHECKED, "note": note}


EFRATY = "https://www.efraty.com/"
OSEK_ROWS = [
    _osek(2016, 99006, EFRATY, "אפרתי – תקרת עוסק פטור לפי שנים", "1 source"),
    _osek(2017, 98707, EFRATY, "אפרתי – תקרת עוסק פטור לפי שנים", "1 source", "CPI-linked; fell with the index"),
    _osek(2018, 99003, "https://www.protocol.co.il/exempt-dealer/", "פרוטוקול – עוסק פטור", "2+ sources"),
    _osek(2019, 100187, EFRATY, "אפרתי – תקרת עוסק פטור לפי שנים", "2+ sources"),
    _osek(2020, 100491, "https://www.taxman.co.il/", "Taxman – תקרת עוסק פטור 2020", "2+ sources"),
    _osek(2021, 99893, "https://www.taxman.co.il/2020/12/עסק-פטור-2021/", "Taxman – עוסק פטור 2021", "1 source",
          "CPI-linked; fell with the index"),
    _osek(2022, 102292, "https://www.greeninvoice.co.il/magazine/תקרת-עוסק-פטור/", "חשבונית ירוקה – תקרת עוסק פטור", "2+ sources"),
    _osek(2023, 107692, "https://alonsave.co.il/תקרת-עוסק-פטור", "אלון סייב – תקרת עוסק פטור לפי שנים", "2+ sources"),
    _osek(2024, 120000, "https://www.bizportal.co.il/guides/news/article/20045314", "ביזפורטל – תקרת עוסק פטור", "2+ sources",
          "raised to a round 120,000"),
    _osek(2025, 120000, "https://alonsave.co.il/תקרת-עוסק-פטור", "אלון סייב – תקרת עוסק פטור לפי שנים", "2+ sources",
          "frozen (not indexed)"),
    _osek(2026, 122833, "https://www.kolzchut.org.il/he/עוסק_פטור", "כל זכות – עוסק פטור", "2+ sources",
          "also greeninvoice, gmcpa; one site shows 122,400"),
]


def _mw(frm, to, monthly, hourly, url, title, ver, note=None):
    return {"from": frm, "to": to, "monthly_ils": monthly, "hourly_ils": hourly, "source_url": url, "source_title": title,
            "verification": ver, "checked": CHECKED, "note": note}


LAW = "https://www.chamber.org.il/serviceslobby/legal/1856/1861/"
MW_ROWS = [
    _mw("2015-04-01", "2016-06-30", 4650, None, LAW, "לשכת המסחר – חוק שכר מינימום (הוראת שעה)", "2+ sources"),
    _mw("2016-07-01", "2016-12-31", 4825, 25.94, LAW, "לשכת המסחר – חוק שכר מינימום (הוראת שעה)", "2+ sources"),
    _mw("2017-01-01", "2017-11-30", 5000, 26.88, LAW, "לשכת המסחר – חוק שכר מינימום (הוראת שעה)", "2+ sources"),
    _mw("2017-12-01", "2023-03-31", 5300, 29.12, "https://www.chamber.org.il/serviceslobby/legal/1856/81476/",
        "לשכת המסחר – שכר מינימום 5,300", "2+ sources",
        "hourly 28.49 until 2018-03-31 (÷186), 29.12 from 2018-04-01 (÷182)"),
    _mw("2023-04-01", "2024-03-31", 5571.75, 30.61, "https://www.timewatch.co.il/", "TimeWatch – עדכון שכר מינימום 1.4.2023", "2+ sources"),
    _mw("2024-04-01", "2025-03-31", 5880.02, 32.30, "https://www.malam-payroll.com/עדכון-שכר-מינימום-מיום-1-4-2024/",
        "מלם שכר – עדכון שכר מינימום 1.4.2024", "2+ sources"),
    _mw("2025-04-01", "2026-03-31", 6247.67, 34.32, "https://www.ynet.co.il/economy/article/rjcptaa2jl",
        "ynet – שכר המינימום עולה ל-6,247.67 ש״ח", "2+ sources"),
    _mw("2026-04-01", None, 6443.85, 35.40, "https://www.btl.gov.il/Mediniyut/GeneralData/Pages/שכר%20מינימום.aspx",
        "ביטוח לאומי – שכר מינימום", "2+ sources", "also kolzchut; current rate"),
]

BTL_LETTER = "https://www.btl.gov.il/Insurance/HozrimBituah/Hozrim/אגרת%20למעסיק%20לשנת%202026.pdf"
BTL_AVG = "https://www.btl.gov.il/Mediniyut/GeneralData/Pages/שכר%20ממוצע.aspx"
SELF_2026 = "https://naama-tax.co.il/blog/2026-04-08-national-insurance-self-employed-2026/"


def _bl(id_, he, en, value, unit, display, url, title, ver="2+ sources", note=None):
    return {"id": id_, "year": 2026, "name_he": he, "name_en": en, "value": value, "unit": unit, "display": display,
            "from": "2026-01-01", "source_url": url, "source_title": title, "verification": ver, "checked": CHECKED, "note": note}


BL_ROWS = [
    _bl("average-wage-s2", "השכר הממוצע (סעיף 2 לחוק הביטוח הלאומי)", "Average wage (NI Law section 2)", 13769, "ILS/month",
        "₪13,769", BTL_AVG, "ביטוח לאומי – שכר ממוצע לפי סעיפים 1 ו-2", note="was 13,316 until 12/2025"),
    _bl("reduced-rate-threshold", "מדרגת הכנסה מופחתת (גבייה)", "Reduced-rate income threshold", 7703, "ILS/month", "₪7,703",
        BTL_LETTER, "ביטוח לאומי – איגרת למעסיק לשנת 2026"),
    _bl("max-insurable-income", "הכנסה מרבית לתשלום דמי ביטוח", "Maximum insurable income", 51910, "ILS/month", "₪51,910",
        BTL_LETTER, "ביטוח לאומי – איגרת למעסיק לשנת 2026", note="622,920 per year"),
    _bl("employee-rate-low", "שכיר: ביטוח לאומי + בריאות עד המדרגה", "Employee: NI + health up to the threshold", 4.27, "percent",
        "1.04% + 3.23% = 4.27%", BTL_LETTER, "ביטוח לאומי – איגרת למעסיק לשנת 2026"),
    _bl("employee-rate-high", "שכיר: ביטוח לאומי + בריאות מעל המדרגה", "Employee: NI + health above the threshold", 12.17, "percent",
        "7.00% + 5.17% = 12.17%", BTL_LETTER, "ביטוח לאומי – איגרת למעסיק לשנת 2026"),
    _bl("employer-rate-low", "מעסיק: דמי ביטוח עד המדרגה", "Employer: NI up to the threshold", 4.51, "percent", "4.51%",
        BTL_LETTER, "ביטוח לאומי – איגרת למעסיק לשנת 2026"),
    _bl("employer-rate-high", "מעסיק: דמי ביטוח מעל המדרגה", "Employer: NI above the threshold", 7.60, "percent", "7.60%",
        BTL_LETTER, "ביטוח לאומי – איגרת למעסיק לשנת 2026"),
    _bl("self-employed-rate-low", "עצמאי: ביטוח לאומי + בריאות עד המדרגה", "Self-employed: NI + health up to the threshold", 7.70,
        "percent", "4.47% + 3.23% = 7.70%", SELF_2026, "נעמה – דמי ביטוח לאומי לעצמאים 2026"),
    _bl("self-employed-rate-high", "עצמאי: ביטוח לאומי + בריאות מעל המדרגה", "Self-employed: NI + health above the threshold", 18.00,
        "percent", "12.83% + 5.17% = 18.00%", SELF_2026, "נעמה – דמי ביטוח לאומי לעצמאים 2026"),
]

RATE_FIELDS_SRC = ["source_url", "source_title", "verification", "checked", "note"]
DATASETS = {
    "israel-vat-history": dict(
        meta=dict(title="Israel VAT rate history (1976–today)", title_he="היסטוריית שיעור המע״מ בישראל",
                  description="Standard VAT (מע״מ) rate in Israel by effective date since VAT was introduced on 1 July 1976, with a source URL for every row. to=null means the current rate.",
                  temporal="1976-07-01/..", keywords=["Israel", "VAT", "מע\"מ", "tax rates"]),
        rows=VAT_ROWS, fields=["from", "to", "rate_percent"] + RATE_FIELDS_SRC),
    "israel-osek-patur-ceiling": dict(
        meta=dict(title="Israel osek patur (exempt dealer) turnover ceiling by year", title_he="תקרת עוסק פטור לפי שנה",
                  description="Annual turnover ceiling (ILS, calendar year) under which an Israeli business may register as osek patur (VAT-exempt dealer), 2016–2026, with sources.",
                  temporal="2016/2026", keywords=["Israel", "osek patur", "עוסק פטור", "VAT exemption"]),
        rows=OSEK_ROWS, fields=["year", "ceiling_ils"] + RATE_FIELDS_SRC),
    "israel-minimum-wage": dict(
        meta=dict(title="Israel minimum wage history (adult, monthly and hourly)", title_he="היסטוריית שכר המינימום בישראל",
                  description="Monthly minimum wage for an adult full-time employee in Israel since April 2015, and the hourly rate (monthly ÷ 182 since April 2018), with sources.",
                  temporal="2015-04-01/..", keywords=["Israel", "minimum wage", "שכר מינימום"]),
        rows=MW_ROWS, fields=["from", "to", "monthly_ils", "hourly_ils"] + RATE_FIELDS_SRC),
    "israel-bituach-leumi-2026": dict(
        meta=dict(title="Bituach Leumi (National Insurance) basic figures 2026", title_he="ביטוח לאומי – נתוני בסיס 2026", year=2026,
                  description="Israel National Insurance 2026: average wage, reduced-rate threshold, maximum insurable income and contribution rates (employee, employer, self-employed, incl. health tax), with sources.",
                  temporal="2026", keywords=["Israel", "Bituach Leumi", "ביטוח לאומי", "national insurance"]),
        rows=BL_ROWS, fields=["id", "year", "name_he", "name_en", "value", "unit", "display", "from"] + RATE_FIELDS_SRC),
}
