"""Zero-dependency Hebrew calendar + Israeli holiday rules (public domain / CC0).

Arithmetic Hebrew calendar from Dershowitz & Reingold, "Calendrical Calculations" (molad of Tishri + the four
dehiyyot). Holiday rules are those used in Israel (one-day Yom Tov, 7-day Pesach, Israeli postponement rules for
the modern days). Cross-checked against two independent libraries by data-il/tools/verify_holidays.py.

Months: 1=Nisan 2=Iyar 3=Sivan 4=Tammuz 5=Av 6=Elul 7=Tishri 8=Cheshvan 9=Kislev 10=Tevet 11=Shevat
        12=Adar (Adar I in a leap year) 13=Adar II
"""
import datetime

EPOCH = -1373427  # R.D. (proleptic Gregorian ordinal) of 1 Tishri AM 1


def is_leap(y):
    return (7 * y + 1) % 19 < 7


def months_in_year(y):
    return 13 if is_leap(y) else 12


def _elapsed(y):
    m = (235 * y - 234) // 19
    parts = 12084 + 13753 * m
    day = m * 29 + parts // 25920
    return day + 1 if (3 * (day + 1)) % 7 < 3 else day


def _delay2(y):
    ny0, ny1, ny2 = _elapsed(y - 1), _elapsed(y), _elapsed(y + 1)
    if ny2 - ny1 == 356:
        return 2
    if ny1 - ny0 == 382:
        return 1
    return 0


def new_year(y):
    return EPOCH + _elapsed(y) + _delay2(y)


def days_in_year(y):
    return new_year(y + 1) - new_year(y)


def last_day(y, m):
    if m in (2, 4, 6, 10, 13):
        return 29
    if m == 12 and not is_leap(y):
        return 29
    if m == 8 and days_in_year(y) % 10 != 5:  # Cheshvan is long only in a "complete" year
        return 29
    if m == 9 and days_in_year(y) % 10 == 3:  # Kislev is short in a "deficient" year
        return 29
    return 30


def to_ordinal(y, m, d):
    r = new_year(y) + d - 1
    if m < 7:
        for mm in range(7, months_in_year(y) + 1):
            r += last_day(y, mm)
        for mm in range(1, m):
            r += last_day(y, mm)
    else:
        for mm in range(7, m):
            r += last_day(y, mm)
    return r


def to_gregorian(y, m, d):
    return datetime.date.fromordinal(to_ordinal(y, m, d))


def adar(y):
    """The Adar in which Purim falls (Adar II in a leap year)."""
    return 13 if is_leap(y) else 12


MONTH_EN = {1: "Nisan", 2: "Iyar", 3: "Sivan", 4: "Tammuz", 5: "Av", 6: "Elul", 7: "Tishrei", 8: "Cheshvan",
            9: "Kislev", 10: "Tevet", 11: "Shevat", 12: "Adar", 13: "Adar II"}
MONTH_HE = {1: "ניסן", 2: "אייר", 3: "סיוון", 4: "תמוז", 5: "אב", 6: "אלול", 7: "תשרי", 8: "חשוון", 9: "כסלו",
            10: "טבת", 11: "שבט", 12: "אדר", 13: "אדר ב׳"}


def month_en(y, m):
    return "Adar I" if (m == 12 and is_leap(y)) else MONTH_EN[m]


def month_he(y, m):
    return "אדר א׳" if (m == 12 and is_leap(y)) else MONTH_HE[m]


_ONES = "אבגדהוזחט"
_TENS = "יכלמנסעפצ"
_HUNDREDS = "קרשת"


def gematria(n):
    """Hebrew numerals with geresh/gershayim: 15 -> ט״ו, 786 -> תשפ״ו."""
    s = ""
    while n >= 400:
        s += "ת"
        n -= 400
    if n >= 100:
        s += _HUNDREDS[n // 100 - 1]
        n %= 100
    if n == 15:
        s += "טו"
        n = 0
    elif n == 16:
        s += "טז"
        n = 0
    if n >= 10:
        s += _TENS[n // 10 - 1]
        n %= 10
    if n:
        s += _ONES[n - 1]
    return s[:-1] + "״" + s[-1] if len(s) > 1 else s + "׳"


def hebrew_date_he(y, m, d):
    return f"{gematria(d)} ב{month_he(y, m)} {gematria(y % 1000)}"


def hebrew_date_en(y, m, d):
    return f"{d} {month_en(y, m)} {y}"


# weekday helpers (Python: Monday=0 … Sunday=6)
SUN, MON, TUE, WED, THU, FRI, SAT = 6, 0, 1, 2, 3, 4, 5


def _dow(y, m, d):
    return to_gregorian(y, m, d).weekday()


def holidays_for_hebrew_year(y):
    """Israeli holidays of Hebrew year y (Tishri y … Elul y). Each: dict(id, he, en, type, rest_day, h=(y,m,d), days)."""
    H = []

    def add(id_, he, en, typ, m, d, days=1, rest=False, note=None):
        H.append(dict(id=id_, he=he, en=en, type=typ, h=(y, m, d), days=days, rest_day=rest, note=note))

    add("rosh-hashanah", "ראש השנה", "Rosh Hashanah", "major", 7, 1, 2, True)
    g = 4 if _dow(y, 7, 3) == SAT else 3
    add("tzom-gedaliah", "צום גדליה", "Fast of Gedaliah", "fast", 7, g, note="postponed to 4 Tishrei when 3 Tishrei is Shabbat" if g == 4 else None)
    add("yom-kippur", "יום כיפור", "Yom Kippur", "major", 7, 10, 1, True)
    add("sukkot", "סוכות", "Sukkot", "major", 7, 15, 1, True)
    add("sukkot-chol-hamoed", "חול המועד סוכות (כולל הושענא רבה)", "Sukkot intermediate days (incl. Hoshana Raba)", "chol-hamoed", 7, 16, 6)
    add("shemini-atzeret", "שמיני עצרת / שמחת תורה", "Shemini Atzeret / Simchat Torah", "major", 7, 22, 1, True)
    add("hanukkah", "חנוכה", "Hanukkah", "minor", 9, 25, 8)
    add("asara-btevet", "צום עשרה בטבת", "Fast of 10 Tevet", "fast", 10, 10)
    add("tu-bishvat", "ט״ו בשבט", "Tu BiShvat", "minor", 11, 15)
    a = adar(y)
    te = 11 if _dow(y, a, 13) == SAT else 13
    add("taanit-esther", "תענית אסתר", "Fast of Esther", "fast", a, te,
        note="moved back to Thursday 11 Adar because 13 Adar is Shabbat" if te == 11 else None)
    add("purim", "פורים", "Purim", "minor", a, 14)
    add("shushan-purim", "שושן פורים", "Shushan Purim", "minor", a, 15,
        note="Jerusalem. 15 Adar is Shabbat: 'Purim Meshulash' (megillah read Friday 14 Adar)" if _dow(y, a, 15) == SAT else "Jerusalem and other walled cities")
    add("pesach", "פסח", "Passover (Pesach)", "major", 1, 15, 1, True)
    add("pesach-chol-hamoed", "חול המועד פסח", "Passover intermediate days", "chol-hamoed", 1, 16, 5)
    add("shvii-shel-pesach", "שביעי של פסח", "Seventh day of Passover", "major", 1, 21, 1, True)
    # Yom HaShoah: 27 Nisan; Friday -> Thursday 26, Sunday -> Monday 28
    w = _dow(y, 1, 27)
    sh = 26 if w == FRI else 28 if w == SUN else 27
    if y > 5718:
        add("yom-hashoah", "יום הזיכרון לשואה ולגבורה", "Yom HaShoah (Holocaust Remembrance Day)", "modern", 1, sh,
            note=None if sh == 27 else "moved from 27 Nisan (would fall next to Shabbat)")
    # Yom HaZikaron / Yom HaAtzmaut: 5 Iyar is Sat/Mon/Wed/Fri
    w = _dow(y, 2, 5)
    at = {SAT: 3, FRI: 4, MON: 6}.get(w, 5)
    moved = at != 5
    add("yom-hazikaron", "יום הזיכרון לחללי מערכות ישראל ונפגעי פעולות האיבה", "Yom HaZikaron (Memorial Day)", "modern", 2, at - 1,
        note="moved from 4 Iyar" if moved else None)
    add("yom-haatzmaut", "יום העצמאות", "Yom HaAtzmaut (Independence Day)", "modern", 2, at, 1, True,
        note="moved from 5 Iyar (Sabbath-adjacent rules)" if moved else None)
    add("lag-baomer", "ל״ג בעומר", "Lag BaOmer", "minor", 2, 18)
    add("yom-yerushalayim", "יום ירושלים", "Jerusalem Day", "modern", 2, 28)
    add("shavuot", "שבועות", "Shavuot", "major", 3, 6, 1, True)
    t = 18 if _dow(y, 4, 17) == SAT else 17
    add("shiva-asar-btammuz", "צום י״ז בתמוז", "Fast of 17 Tammuz", "fast", 4, t,
        note="postponed to 18 Tammuz because 17 Tammuz is Shabbat" if t == 18 else None)
    b = 10 if _dow(y, 5, 9) == SAT else 9
    add("tisha-bav", "תשעה באב", "Tisha B'Av", "fast", 5, b,
        note="postponed to 10 Av because 9 Av is Shabbat" if b == 10 else None)
    add("tu-bav", "ט״ו באב", "Tu B'Av", "minor", 5, 15)
    return H


EVENING_START = {"major", "minor", "chol-hamoed", "modern"}  # these begin at sundown the evening before
DAYTIME_FASTS = {"tzom-gedaliah", "asara-btevet", "taanit-esther", "shiva-asar-btammuz"}  # dawn to nightfall


def israeli_holidays(g_from, g_to):
    """All holidays whose first day is within [g_from, g_to] (Gregorian years, inclusive), sorted by date."""
    out = []
    for y in range(g_from + 3759, g_to + 3762):
        for h in holidays_for_hebrew_year(y):
            hy, hm, hd = h["h"]
            start = to_gregorian(hy, hm, hd)
            if not (g_from <= start.year <= g_to):
                continue
            end = start + datetime.timedelta(days=h["days"] - 1)
            begins = "sunset_previous_day"
            if h["id"] in DAYTIME_FASTS:
                begins = "dawn"
            out.append(dict(
                id=h["id"], name_he=h["he"], name_en=h["en"], type=h["type"],
                start=start.isoformat(), end=end.isoformat(), days=h["days"],
                begins=begins,
                eve=(start - datetime.timedelta(days=1)).isoformat() if begins == "sunset_previous_day" else None,
                weekday_en=start.strftime("%A"),
                hebrew_date_en=hebrew_date_en(hy, hm, hd), hebrew_date_he=hebrew_date_he(hy, hm, hd),
                hebrew_year=hy, rest_day=h["rest_day"], note=h["note"]))
    out.sort(key=lambda r: (r["start"], r["id"]))
    return out
