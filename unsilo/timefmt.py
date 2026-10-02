"""People-facing time: 12-hour ET (standing rule). Display only, never evaluation."""
from __future__ import annotations

import datetime as dt
import re

from .temporal import ET, UTC

_TIME_WORDING = re.compile(r"~?\d{1,2}:\d{2}\s?[AP]M(\s?ET)?")


def _day(value: str) -> str:
    d = dt.date.fromisoformat(value)
    return f"{d.strftime('%b')} {d.day}, {d.year}"


def utc_to_et(value: str) -> str:
    t = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).astimezone(ET)
    h = t.hour % 12 or 12
    return f"{t.strftime('%b')} {t.day}, {t.year}, {h}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'} ET"


def instant(kind, value, gran, zone, source_text="") -> str:
    if kind != "KNOWN":
        return "UNKNOWN"
    if gran == "SECOND":
        return utc_to_et(value)
    out = _day(value)
    if zone == "FLOATING":
        out += " (no zone)"
    elif zone not in ("America/New_York",):
        out += f" ({zone})"
    m = _TIME_WORDING.search(source_text or "")
    if m:
        wording = m.group(0)
        out += f", {wording}" + ("" if "ET" in wording else " ET")
    return out


def bound(kind, value, gran, zone) -> str:
    if kind == "UNBOUNDED":
        return "unbounded"
    if kind == "UNKNOWN":
        return "UNKNOWN"
    return utc_to_et(value) if gran == "SECOND" else _day(value)


def money(minor: int, currency: str) -> str:
    sym = "$" if currency == "USD" else currency + " "
    whole, cents = divmod(minor, 100)
    return f"{sym}{whole:,}" + (f".{cents:02d}" if cents else "")
