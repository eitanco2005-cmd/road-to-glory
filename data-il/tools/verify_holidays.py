#!/usr/bin/env python3
"""Cross-check the zero-dependency holiday computation against two independent libraries.

    python3 -m venv /tmp/v && /tmp/v/bin/pip install hdate pyluach
    /tmp/v/bin/python data-il/tools/verify_holidays.py        # exits 1 on any mismatch

* hdate (py-libhdate, Israel mode): every holiday incl. the modern days and their postponement rules
* pyluach (Israel mode): the religious holidays and fasts
Plus fixed anchor dates from published calendars (Rosh Hashanah, Pesach, Hanukkah) as a third check.
"""
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import hebrew_calendar as hc  # noqa: E402

FROM, TO = 2025, 2030
ours = hc.israeli_holidays(FROM, TO)

# id -> names used by each library (first day only)
HDATE = {
    "rosh-hashanah": "rosh_hashana_i", "tzom-gedaliah": "tzom_gedaliah", "yom-kippur": "yom_kippur", "sukkot": "sukkot",
    "shemini-atzeret": "shmini_atzeret", "hanukkah": "chanukah", "asara-btevet": "asara_btevet", "tu-bishvat": "tu_bshvat",
    "taanit-esther": "taanit_esther", "purim": "purim", "shushan-purim": "shushan_purim", "pesach": "pesach",
    "shvii-shel-pesach": "pesach_vii", "yom-hashoah": "yom_hashoah", "yom-hazikaron": "yom_hazikaron",
    "yom-haatzmaut": "yom_haatzmaut", "lag-baomer": "lag_bomer", "yom-yerushalayim": "yom_yerushalayim",
    "shavuot": "shavuot", "shiva-asar-btammuz": "tzom_tammuz", "tisha-bav": "tisha_bav", "tu-bav": "tu_bav",
}
PYLUACH = {
    "rosh-hashanah": "1 Rosh Hashana", "tzom-gedaliah": "Tzom Gedalia", "yom-kippur": "Yom Kippur", "sukkot": "1 Succos",
    "shemini-atzeret": "Shmini Atzeres", "hanukkah": "1 Chanuka", "asara-btevet": "10 of Teves", "tu-bishvat": "Tu B'shvat",
    "taanit-esther": "Taanis Esther", "purim": "Purim", "shushan-purim": "Shushan Purim", "pesach": "1 Pesach",
    "shvii-shel-pesach": "7 Pesach", "lag-baomer": "Lag Ba'omer", "shavuot": "Shavuos", "shiva-asar-btammuz": "17 of Tamuz",
    "tisha-bav": "9 of Av", "tu-bav": "Tu B'av",
}
# Published anchors (well-known dates)
ANCHORS = {("rosh-hashanah", 2025): "2025-09-23", ("rosh-hashanah", 2026): "2026-09-12", ("pesach", 2025): "2025-04-13",
           ("pesach", 2026): "2026-04-02", ("hanukkah", 2025): "2025-12-15", ("hanukkah", 2026): "2026-12-05",
           ("yom-haatzmaut", 2025): "2025-05-01", ("yom-haatzmaut", 2026): "2026-04-22", ("yom-kippur", 2025): "2025-10-02"}


def hdate_days():
    from hdate import HDateInfo
    out = {}
    d = datetime.date(FROM, 1, 1)
    while d <= datetime.date(TO, 12, 31):
        for h in HDateInfo(d, diaspora=False).holidays:
            out.setdefault((h.name, d.year), []).append(d)
        d += datetime.timedelta(days=1)
    return out


def pyluach_days():
    from pyluach import dates
    out = {}
    d = datetime.date(FROM, 1, 1)
    while d <= datetime.date(TO, 12, 31):
        name = dates.GregorianDate(d.year, d.month, d.day).holiday(israel=True, prefix_day=True)
        if name:
            out.setdefault((name, d.year), []).append(d)
        d += datetime.timedelta(days=1)
    return out


def main():
    bad = checked = 0
    try:
        hd = hdate_days()
    except ImportError:
        hd = None
        print("hdate not installed: skipped")
    try:
        pl = pyluach_days()
    except ImportError:
        pl = None
        print("pyluach not installed: skipped")
    for r in ours:
        start = datetime.date.fromisoformat(r["start"])
        y = start.year
        for lib, table, names in (("hdate", hd, HDATE), ("pyluach", pl, PYLUACH)):
            if table is None or r["id"] not in names:
                continue
            got = table.get((names[r["id"]], y), [])
            # the first day in that Gregorian year that is not a continuation from the previous one
            firsts = [d for d in got if d - datetime.timedelta(days=1) not in got]
            checked += 1
            if start not in firsts:
                bad += 1
                print(f"MISMATCH {lib}: {r['id']} {r['start']} vs {[d.isoformat() for d in firsts]}")
        if (r["id"], y) in ANCHORS:
            checked += 1
            if ANCHORS[(r["id"], y)] != r["start"]:
                bad += 1
                print(f"MISMATCH anchor: {r['id']} {r['start']} vs {ANCHORS[(r['id'], y)]}")
    print(f"{len(ours)} holidays {FROM}-{TO}, {checked} cross-checks, {bad} mismatches")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
