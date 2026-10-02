"""B4 point membership: is a declared cut inside [from, to)?

Frozen B4: each endpoint is KNOWN(v) | UNBOUNDED | UNKNOWN; point times are
never UNBOUNDED; truth is universal entailment over admissible completions
(dense completions, the only constraint is from < to).

One decision procedure, two domains:
  * POSITION: every KNOWN endpoint shares the cut's granularity and zone. Values
    are order positions compared as ISO strings. This is what the SQL view
    v_interval_membership implements; experiments/temporal_agreement.py proves
    the two agree on every case.
  * LIFTED (DL-2): granularities or zones differ. Every KNOWN value is lifted to
    UTC epoch seconds with pinned tzdata. A DAY endpoint is its calendar-day
    boundary; a DAY cut is an imprecise instant, i.e. the set of seconds in that
    day (section 5.4, standing ruling D-7).
FLOATING zone (DL-1): a DAY value with no zone context. Absolute comparison
against anything not FLOATING is UNKNOWN (S3).
"""
from __future__ import annotations

import datetime as dt
import importlib.metadata
import zoneinfo
from dataclasses import dataclass

# Force the pinned tzdata package; never the host zone database (G10).
zoneinfo.reset_tzpath(to=[])
TZDATA_VERSION = importlib.metadata.version("tzdata")
ET = zoneinfo.ZoneInfo("America/New_York")
UTC = dt.timezone.utc

KINDS_POINT = ("KNOWN", "UNKNOWN")
KINDS_END = ("KNOWN", "UNBOUNDED", "UNKNOWN")
GRANS = ("DAY", "SECOND")


@dataclass(frozen=True)
class End:
    kind: str
    value: str | None = None
    gran: str | None = None
    zone: str | None = None


@dataclass(frozen=True)
class Cut:
    value: str
    gran: str
    zone: str


def zone_ok(zone: str) -> bool:
    if zone in ("UTC", "FLOATING"):
        return True
    try:
        zoneinfo.ZoneInfo(zone)
        return True
    except (zoneinfo.ZoneInfoNotFoundError, ValueError):
        return False


def check_value(value: str, gran: str, zone: str) -> None:
    if gran == "DAY":
        dt.date.fromisoformat(value)
        if len(value) != 10:
            raise ValueError(f"DAY value must be YYYY-MM-DD: {value!r}")
        if not zone_ok(zone):
            raise ValueError(f"unknown zone {zone!r} (tzdata {TZDATA_VERSION})")
    elif gran == "SECOND":
        if zone != "UTC" or len(value) != 20 or not value.endswith("Z"):
            raise ValueError(f"SECOND values are UTC 'YYYY-MM-DDTHH:MM:SSZ': {value!r}")
        dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    else:
        raise ValueError(f"granularity {gran!r} not in {GRANS}")


def _day_start(day: str, zone: str) -> int:
    z = UTC if zone == "UTC" else zoneinfo.ZoneInfo(zone)
    d = dt.date.fromisoformat(day)
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=z).timestamp())


def _second(value: str) -> int:
    return int(dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).timestamp())


def lift_bound(value: str, gran: str, zone: str) -> int:
    """KNOWN endpoint -> UTC epoch second of the boundary it names."""
    return _second(value) if gran == "SECOND" else _day_start(value, zone)


def lift_cut(cut: Cut):
    if cut.gran == "SECOND":
        return ("POINT", _second(cut.value))
    nxt = (dt.date.fromisoformat(cut.value) + dt.timedelta(days=1)).isoformat()
    return ("RANGE", _day_start(cut.value, cut.zone), _day_start(nxt, cut.zone))


def _decide(f, t, x):
    """f, t: ('K', v) | ('N',) for UNBOUNDED | ('U',) for UNKNOWN.
    x: ('POINT', p) | ('RANGE', lo, hi) with hi exclusive (dense instants).
    Returns (truth, reason)."""
    point = x[0] == "POINT"
    lo = x[1]
    # all_below(v): every instant < v.  all_at_or_above(v): every instant >= v.
    if point:
        def all_below(v): return lo < v
    else:
        def all_below(v): return x[2] <= v
    def all_at_or_above(v): return lo >= v
    # FALSE: no (instant, completion) pair satisfies f <= instant < t.
    if f[0] == "K" and all_below(f[1]):
        return "FALSE", "CUT_BEFORE_KNOWN_FROM"
    if t[0] == "K" and all_at_or_above(t[1]):
        return "FALSE", "CUT_AT_OR_AFTER_KNOWN_TO"
    # TRUE: every instant under every completion satisfies it.
    from_ok = f[0] == "N" or (f[0] == "K" and all_at_or_above(f[1]))
    if from_ok and (t[0] == "N" or (t[0] == "K" and all_below(t[1]))):
        return "TRUE", "ALL_COMPLETIONS_CONTAIN_CUT"
    if f[0] == "K" and t[0] == "U" and point and lo == f[1]:
        return "TRUE", "CUT_EQUALS_FROM_AND_TO_EXCEEDS_FROM"
    if f[0] == "U":
        return "UNKNOWN", "FROM_UNKNOWN_COMPLETIONS_SPLIT"
    if t[0] == "U":
        return "UNKNOWN", "TO_UNKNOWN_COMPLETIONS_SPLIT"
    return "UNKNOWN", "CUT_GRANULE_STRADDLES_BOUND"


def _tag(e: End, lifted: bool):
    if e.kind == "UNBOUNDED":
        return ("N",)
    if e.kind == "UNKNOWN":
        return ("U",)
    return ("K", lift_bound(e.value, e.gran, e.zone) if lifted else e.value)


def same_domain(frm: End, to: End, cut: Cut) -> bool:
    return all(e.kind != "KNOWN" or (e.gran == cut.gran and e.zone == cut.zone) for e in (frm, to))


def membership(frm: End, to: End, cut: Cut):
    """(truth, reason). truth in TRUE / FALSE / UNKNOWN."""
    if cut.zone == "FLOATING":
        raise ValueError("a cut must name a zone; FLOATING cuts are not admissible")
    if same_domain(frm, to, cut):
        return _decide(_tag(frm, False), _tag(to, False), ("POINT", cut.value))
    if any(e.kind == "KNOWN" and e.zone == "FLOATING" for e in (frm, to)):
        return "UNKNOWN", "FLOATING_ZONE_NOT_COMPARABLE"
    truth, reason = _decide(_tag(frm, True), _tag(to, True), lift_cut(cut))
    return truth, reason


def interval_valid(frm: End, to: End) -> None:
    """Write-time validity: from < to when both KNOWN (lifted if needed)."""
    for e in (frm, to):
        if e.kind not in KINDS_END:
            raise ValueError(f"endpoint kind {e.kind!r}")
        if e.kind == "KNOWN":
            check_value(e.value, e.gran, e.zone)
    if frm.kind == "KNOWN" and to.kind == "KNOWN":
        if frm.gran == to.gran and frm.zone == to.zone:
            if not frm.value < to.value:
                raise ValueError("interval requires from < to")
        elif "FLOATING" in (frm.zone, to.zone):
            raise ValueError("mixed FLOATING/zoned KNOWN endpoints cannot be ordered (S3)")
        elif not lift_bound(frm.value, frm.gran, frm.zone) < lift_bound(to.value, to.gran, to.zone):
            raise ValueError("interval requires from < to (lifted)")


# SQLite bindings: registered DETERMINISTIC + INNOCUOUS on every connection.
def sql_truth(fk, fv, fg, fz, tk, tv, tg, tz, cv, cg, cz):
    return membership(End(fk, fv, fg, fz), End(tk, tv, tg, tz), Cut(cv, cg, cz))[0]


def sql_reason(fk, fv, fg, fz, tk, tv, tg, tz, cv, cg, cz):
    return membership(End(fk, fv, fg, fz), End(tk, tv, tg, tz), Cut(cv, cg, cz))[1]


def sort_key(kind, value, gran, zone) -> int:
    """Display order only (never a temporal relation): lifted start, FLOATING as UTC."""
    if kind != "KNOWN":
        return -(2**62)
    return lift_bound(value, gran, "UTC" if zone == "FLOATING" else zone)
