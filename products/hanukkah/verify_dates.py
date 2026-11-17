#!/usr/bin/env python3
"""Verify Hanukkah 2026 dates with the arithmetic Hebrew calendar (Dershowitz & Reingold, Calendrical Calculations).
Sanity checks: Rosh Hashana 5787 = 2026-09-12, 25 Kislev 5786 = 2025-12-15.  Run: python3 verify_dates.py"""
import datetime
EPOCH = -1373427  # R.D. of 1 Tishri AM 1
def leap(y): return (7*y+1)%19 < 7
def months(y): return 13 if leap(y) else 12
def elapsed(y):
    m = (235*y-234)//19
    parts = 12084 + 13753*m
    day = m*29 + parts//25920
    return day+1 if (3*(day+1))%7 < 3 else day
def delay2(y):
    ny0, ny1, ny2 = elapsed(y-1), elapsed(y), elapsed(y+1)
    if ny2-ny1 == 356: return 2
    if ny1-ny0 == 382: return 1
    return 0
def new_year(y): return EPOCH + elapsed(y) + delay2(y)
def days_in_year(y): return new_year(y+1)-new_year(y)
def long_heshvan(y): return days_in_year(y)%10 == 5
def short_kislev(y): return days_in_year(y)%10 == 3
def last_day(y,m):
    if m in (2,4,6,10,13): return 29
    if m==12 and not leap(y): return 29
    if m==8 and not long_heshvan(y): return 29
    if m==9 and short_kislev(y): return 29
    return 30
def fixed(y,m,d):  # m: 1=Nisan ... 7=Tishri, 9=Kislev
    r = new_year(y) + d - 1
    if m < 7:
        for mm in range(7, months(y)+1): r += last_day(y,mm)
        for mm in range(1, m): r += last_day(y,mm)
    else:
        for mm in range(7, m): r += last_day(y,mm)
    return r
def greg(rd): return datetime.date.fromordinal(rd)
# sanity: Rosh Hashana 5787 should be Sep 12 2026; Hanukkah 5786 = Dec 15 2025
print("RH 5787", greg(fixed(5787,7,1)))
print("25 Kislev 5786", greg(fixed(5786,9,25)))
for y in (5787,):
    s = greg(fixed(y,9,25)); print("25 Kislev", y, s, s.strftime("%A"), "| short kislev", short_kislev(y))
    for n in range(8):
        d = s + datetime.timedelta(days=n); print("night", n+1, "evening of", d - datetime.timedelta(days=1), (d - datetime.timedelta(days=1)).strftime("%a"))
