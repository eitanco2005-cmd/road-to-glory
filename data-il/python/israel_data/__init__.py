"""israel_data — Israeli holidays 2025–2030, VAT, osek patur ceiling and minimum wage. Zero dependencies.

Data: CC0 1.0 · Code: MIT · https://github.com/eitanco2005-cmd/road-to-glory/tree/main/data-il
Live calculators: https://tichnun.netlify.app/tools/

    >>> import israel_data as il
    >>> [h["name_en"] for h in il.is_israeli_holiday("2026-04-22")]
    ['Yom HaAtzmaut (Independence Day)']
    >>> il.is_rest_day("2026-04-22")
    True
    >>> il.add_vat(1000)
    {'net': 1000.0, 'vat': 180.0, 'gross': 1180.0, 'rate': 0.18}
    >>> il.remove_vat(1180)
    {'net': 1000.0, 'vat': 180.0, 'gross': 1180.0, 'rate': 0.18}
    >>> il.vat_rate("2024-06-01")
    0.17
"""
import datetime as _dt
from decimal import ROUND_HALF_UP, Decimal

from ._data import DATA

__all__ = ["DATA", "holidays", "is_israeli_holiday", "is_rest_day", "next_holiday", "vat_rate", "add_vat",
           "remove_vat", "osek_patur_ceiling", "minimum_wage"]
__version__ = DATA["version"]


def _iso(d=None):
    if d is None:
        return _dt.date.today().isoformat()
    if isinstance(d, (_dt.date, _dt.datetime)):
        return d.strftime("%Y-%m-%d")
    s = str(d)[:10]
    _dt.date.fromisoformat(s)  # validates
    return s


def _r2(x):
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _by_date(rows, day):
    hit = None
    for r in rows:
        if r["from"] <= day:
            hit = r
    return hit


def holidays(year=None):
    """All holidays (optionally of one Gregorian year), sorted by start date."""
    return [h for h in DATA["holidays"] if not year or h["start"][:4] == str(year)]


def is_israeli_holiday(date=None, types=None):
    """Holidays covering the date (multi-day ones included). Empty list if none. types: e.g. ["major", "modern"]."""
    day = _iso(date)
    return [h for h in DATA["holidays"] if h["start"] <= day <= h["end"] and (not types or h["type"] in types)]


def is_rest_day(date=None, shabbat=False):
    """Israeli statutory rest day (Yom Tov or Independence Day); shabbat=True also counts Saturdays."""
    day = _iso(date)
    if shabbat and _dt.date.fromisoformat(day).weekday() == 5:
        return True
    return any(h["rest_day"] for h in is_israeli_holiday(day))


def next_holiday(date=None, types=None):
    """First holiday starting on or after the date (None past the end of the dataset)."""
    day = _iso(date)
    for h in DATA["holidays"]:
        if h["start"] >= day and (not types or h["type"] in types):
            return h
    return None


def vat_rate(date=None):
    """Standard VAT rate (fraction, e.g. 0.18) in force on the date."""
    row = _by_date(DATA["vat"], _iso(date))
    if not row:
        raise ValueError(f"no VAT rate in the dataset for {_iso(date)}")
    return row["rate"] / 100


def _rate(rate, date):
    if rate is None:
        return vat_rate(date)
    return rate / 100 if rate > 1 else rate


def add_vat(net, rate=None, date=None):
    """Add VAT to a net amount. rate: 18 or 0.18 (default: the rate in force on `date`, default today)."""
    R = _rate(rate, date)
    vat = _r2(net * R)
    return {"net": _r2(net), "vat": vat, "gross": _r2(net + vat), "rate": R}


def remove_vat(gross, rate=None, date=None):
    """Take VAT out of a VAT-inclusive amount (divide by 1+rate; never subtract the rate)."""
    R = _rate(rate, date)
    net = _r2(gross / (1 + R))
    return {"net": net, "vat": _r2(gross - net), "gross": _r2(gross), "rate": R}


def osek_patur_ceiling(year=None):
    """Osek patur annual turnover ceiling (ILS) for a tax year, or None if not in the dataset."""
    y = int(year or _dt.date.today().year)
    for r in DATA["osek_patur"]:
        if r["year"] == y:
            return r["ceiling_ils"]
    return None


def minimum_wage(date=None):
    """Adult minimum wage in force on the date: {monthly, hourly, from, source}."""
    row = _by_date(DATA["minimum_wage"], _iso(date))
    if not row:
        return None
    return {"monthly": row["monthly_ils"], "hourly": row["hourly_ils"], "from": row["from"], "source": row["source_url"]}
