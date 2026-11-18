#!/usr/bin/env python3
"""Verify Purim 2027 and Passover 2027 dates with the arithmetic Hebrew calendar
(Dershowitz & Reingold, Calendrical Calculations; same code as products/hanukkah/verify_dates.py).
Sanity checks against known dates: Rosh Hashana 5787 = 2026-09-12, Pesach 5786 (15 Nisan) = 2026-04-02, Purim 5786 = 2026-03-03.
Run: python3 verify_dates.py   (exits non-zero if a check or an expected 2027 date fails)"""
import datetime
import sys

EPOCH = -1373427  # R.D. of 1 Tishri AM 1
def leap(y): return (7*y+1) % 19 < 7
def months(y): return 13 if leap(y) else 12
def elapsed(y):
    m = (235*y-234)//19
    parts = 12084 + 13753*m
    day = m*29 + parts//25920
    return day+1 if (3*(day+1)) % 7 < 3 else day
def delay2(y):
    ny0, ny1, ny2 = elapsed(y-1), elapsed(y), elapsed(y+1)
    if ny2-ny1 == 356: return 2
    if ny1-ny0 == 382: return 1
    return 0
def new_year(y): return EPOCH + elapsed(y) + delay2(y)
def days_in_year(y): return new_year(y+1)-new_year(y)
def long_heshvan(y): return days_in_year(y) % 10 == 5
def short_kislev(y): return days_in_year(y) % 10 == 3
def last_day(y, m):
    if m in (2, 4, 6, 10, 13): return 29
    if m == 12 and not leap(y): return 29
    if m == 8 and not long_heshvan(y): return 29
    if m == 9 and short_kislev(y): return 29
    return 30
def fixed(y, m, d):  # m: 1=Nisan ... 6=Elul, 7=Tishri ... 12=Adar (Adar I in leap years), 13=Adar II
    r = new_year(y) + d - 1
    if m < 7:
        for mm in range(7, months(y)+1): r += last_day(y, mm)
        for mm in range(1, m): r += last_day(y, mm)
    else:
        for mm in range(7, m): r += last_day(y, mm)
    return r
def greg(rd): return datetime.date.fromordinal(rd)
def adar(y): return 13 if leap(y) else 12

DAYS_HE = ["שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת", "ראשון"]
def he_day(d): return DAYS_HE[d.weekday()]

Y = 5787
DATES = {  # key: (label, hebrew month, day)
    "purim_katan": ("פורים קטן (י״ד באדר א׳)", 12, 14),
    "taanit_esther": ("תענית אסתר (י״ג באדר ב׳)", adar(Y), 13),
    "purim": ("פורים (י״ד באדר ב׳)", adar(Y), 14),
    "shushan_purim": ("שושן פורים – ירושלים (ט״ו באדר ב׳)", adar(Y), 15),
    "bedika": ("ליל בדיקת חמץ (ערב י״ד בניסן)", 1, 13),   # evening of 13 Nisan = night of 14 Nisan
    "erev_pesach": ("ערב פסח (י״ד בניסן)", 1, 14),
    "pesach": ("פסח – יום טוב ראשון (ט״ו בניסן)", 1, 15),
    "shvii": ("שביעי של פסח (כ״א בניסן)", 1, 21),
    "acharon_chul": ("אחרון של פסח בחו״ל (כ״ב בניסן)", 1, 22),
    "shavuot": ("שבועות (ו׳ בסיוון)", 3, 6),
}
LATER = {"rosh_hashana_5788": (5788, 7, 1), "yom_kippur_5788": (5788, 7, 10), "sukkot_5788": (5788, 7, 15), "hanukkah_5788": (5788, 9, 25)}
EXPECTED = {"purim": datetime.date(2027, 3, 23), "pesach": datetime.date(2027, 4, 22), "erev_pesach": datetime.date(2027, 4, 21),
            "shvii": datetime.date(2027, 4, 28), "taanit_esther": datetime.date(2027, 3, 22), "shushan_purim": datetime.date(2027, 3, 24)}

def compute():
    out = {k: greg(fixed(Y, m, d)) for k, (_, m, d) in DATES.items()}
    out.update({k: greg(fixed(y, m, d)) for k, (y, m, d) in LATER.items()})
    return out

if __name__ == "__main__":
    ok = True
    for label, got, want in (("RH 5787", greg(fixed(5787, 7, 1)), datetime.date(2026, 9, 12)),
                             ("Pesach 5786", greg(fixed(5786, 1, 15)), datetime.date(2026, 4, 2)),
                             ("Purim 5786", greg(fixed(5786, adar(5786), 14)), datetime.date(2026, 3, 3))):
        print(f"sanity {label}: {got} {'OK' if got == want else 'FAIL (want ' + str(want) + ')'}"); ok &= got == want
    print("5787 leap year:", leap(Y))
    c = compute()
    for k, (label, _, _) in DATES.items():
        d = c[k]
        flag = "" if k not in EXPECTED else (" OK" if EXPECTED[k] == d else f" FAIL (page says {EXPECTED[k]})")
        ok &= k not in EXPECTED or EXPECTED[k] == d
        print(f"{label}: {d} יום {he_day(d)} / {d.strftime('%A')}{flag}")
    for k in LATER:
        print(f"{k}: {c[k]} ({c[k].strftime('%A')}; the holiday starts the evening before)")
    sys.exit(0 if ok else 1)
