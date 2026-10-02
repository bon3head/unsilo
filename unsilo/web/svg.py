"""Server-rendered SVG (R28). One mark per recorded fact; UNKNOWN is a visible
hatched band, never a hidden row or an implied line."""
from __future__ import annotations

import datetime as dt
from html import escape

from markupsafe import Markup

ROW, LEFT, DAYW, TOP = 22, 96, 46, 26


def timeline(cards, cut):
    cut_day = dt.date.fromisoformat(cut.eff_value)
    days = []
    for c in cards:
        for s in c["states"]:
            if s["ev_kind"] == "KNOWN" and s["ev_gran"] == "DAY":
                days.append(dt.date.fromisoformat(s["ev_value"]))
    if not days:
        return Markup("")
    start = min(days) - dt.timedelta(days=1)
    end = max(max(days), cut_day) + dt.timedelta(days=1)
    if (end - start).days > 45:
        start = end - dt.timedelta(days=45)
    n = (end - start).days + 1
    w, h = LEFT + n * DAYW + 10, TOP + ROW * len(cards) + 30
    x = lambda d: LEFT + (d - start).days * DAYW  # noqa: E731
    out = [f'<svg class="tl" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="max-width:100%;height:auto" role="img" aria-label="Application events by ET day">',
           '<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<line x1="0" y1="0" x2="0" y2="6" class="hatch"/></pattern></defs>']
    for i in range(n):
        d = start + dt.timedelta(days=i)
        out.append(f'<text x="{x(d) + DAYW / 2:.0f}" y="14" class="ax">{d.strftime("%b")} {d.day}</text>')
        out.append(f'<line x1="{x(d)}" y1="{TOP - 4}" x2="{x(d)}" y2="{h - 22}" class="grid"/>')
    if start <= cut_day <= end:
        cx = x(cut_day)
        out.append(f'<rect x="{cx}" y="{TOP - 4}" width="{DAYW}" height="{h - TOP - 18}" class="cut"/>')
        out.append(f'<text x="{cx + DAYW / 2:.0f}" y="{h - 8}" class="ax cutl">cut</text>')
    for r, c in enumerate(cards):
        y = TOP + r * ROW
        out.append(f'<text x="4" y="{y + 14}" class="lab">{escape(c["app"]["employer_label"])}</text>')
        for s in c["states"]:
            if s["ev_kind"] != "KNOWN" or s["ev_gran"] != "DAY":
                continue
            d = dt.date.fromisoformat(s["ev_value"])
            if d < start:
                continue
            band_end = min(cut_day + dt.timedelta(days=1), end + dt.timedelta(days=1))
            if band_end > d + dt.timedelta(days=1):
                cls = "known" if s["in_effect"] == "TRUE" else "unk"
                fill = "" if cls == "known" else ' fill="url(#hatch)"'
                bx = x(d + dt.timedelta(days=1))
                out.append(f'<rect x="{bx}" y="{y + 5}" width="{x(band_end) - bx}" height="10" class="{cls}"{fill}>'
                           f'<title>{escape(s["status"])} in effect at cut: {escape(s["in_effect"])} ({escape(s["in_effect_reason"])})</title></rect>')
            out.append(f'<rect x="{x(d)}" y="{y + 3}" width="{DAYW}" height="14" class="ev st-{escape(s["status"])}">'
                       f'<title>{escape(s["status"])} {escape(s["ev_text"])} (DAY granule: the mark spans the whole ET day)</title></rect>')
    out.append("</svg>")
    return Markup("".join(out))
