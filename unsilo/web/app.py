"""Docket web surface: Starlette + Jinja2 + vendored htmx 2.0.11.

Local only (127.0.0.1). Reads use a read-only connection per request; writes go
through the one write path on a single writer connection. Every page declares
its cut and prints it; every panel links to its SQL.
"""
from __future__ import annotations

import datetime as dt
import secrets
import threading
import urllib.parse
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse, RedirectResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from .. import db, ledger, temporal, timefmt
from ..docket import queries as Q
from ..docket.records import Docket
from ..temporal import End
from . import svg
from .search import FeedIndex

HERE = Path(__file__).resolve().parent
TAGS = ("applications", "forensics", "audits", "research-chain", "surfaces", "build")
TERM_ORDER = ("role", "req_ref", "platform", "location", "posting_url", "deadline", "pay", "stipend",
              "duration_weeks", "program_window", "track", "preference", "materials", "note")
TERM_LABEL = {"req_ref": "req", "posting_url": "posting", "duration_weeks": "weeks", "program_window": "program"}


class Cut:
    def __init__(self, eff_value, k, explicit):
        self.eff_value, self.k, self.explicit = eff_value, k, explicit
        self.eff_gran, self.eff_zone = "DAY", "America/New_York"

    def params(self):
        return {"k": self.k, "eff_value": self.eff_value, "eff_gran": self.eff_gran, "eff_zone": self.eff_zone}

    def label(self):
        return f"effective {timefmt.instant('KNOWN', self.eff_value, 'DAY', self.eff_zone)} (ET day) · knowledge as of {timefmt.utc_to_et(self.k)}"


def declare_cut(request: Request, clock) -> Cut:
    """The page's cut: from the query string, else declared from the clock once,
    at the request boundary, and printed on the page (S8: never ambient)."""
    now = clock()
    eff = request.query_params.get("eff") or ""
    k = request.query_params.get("k") or ""
    explicit = bool(eff or k)
    if not eff:
        eff = dt.datetime.strptime(now, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=temporal.UTC).astimezone(temporal.ET).date().isoformat()
    if not k:
        k = now
    temporal.check_value(eff, "DAY", "America/New_York")
    temporal.check_value(k, "SECOND", "UTC")
    return Cut(eff, k, explicit)


def build_cards(apps, terms, actions):
    by_app = {}
    for r in apps:
        card = by_app.setdefault(r["application_id"], {"app": r, "states": [], "terms": {}, "actions": []})
        if r["state_id"] is not None:
            card["states"].append(r)
    for t in terms:
        if t["application_id"] in by_app:
            by_app[t["application_id"]]["terms"].setdefault(t["term_key"], []).append(t)
    for a in actions:
        if a["application_id"] in by_app and a["status"] == "OPEN":
            by_app[a["application_id"]]["actions"].append(a)
    out = []
    for card in by_app.values():
        rows = []
        for key in sorted(card["terms"], key=lambda k: (TERM_ORDER.index(k) if k in TERM_ORDER else 99, k)):
            for t in card["terms"][key]:
                rows.append((TERM_LABEL.get(key, key), render_term(t), t))
        card["rows"] = rows
        out.append(card)
    return out


def render_term(t):
    k = t["value_kind"]
    if k == "TEXT":
        return t["text_value"]
    if k == "INTEGER":
        return str(t["int_value"])
    if k == "UNKNOWN":
        return "UNKNOWN"
    if k == "MONEY_MINOR":
        unit = {"HOUR": "/hr", "ONE_TIME": " one-time", "WEEK": "/wk", "YEAR": "/yr"}[t["per_unit"]]
        return timefmt.money(t["amount_minor"], t["currency"]) + unit
    if k == "MONEY_RANGE_MINOR":
        unit = {"HOUR": "/hr", "ONE_TIME": " one-time", "WEEK": "/wk", "YEAR": "/yr"}[t["per_unit"]]
        return f"{timefmt.money(t['amount_minor'], t['currency'])}-{timefmt.money(t['amount_minor_hi'], t['currency'])}{unit}"
    if k == "INSTANT":
        s = timefmt.instant(t["i_kind"], t["i_value"], t["i_gran"], t["i_zone"], t["i_text"])
        if t["at_or_after_instant"] == "TRUE":
            s += " (passed at cut)"
        elif t["at_or_after_instant"] == "UNKNOWN":
            s += " (at cut: UNKNOWN)"
        return s
    if k == "INTERVAL":
        end = t["to_value"]
        if t["to_kind"] == "KNOWN" and t["from_gran"] == "DAY":
            end = (dt.date.fromisoformat(end) - dt.timedelta(days=1)).isoformat()
            return f"{timefmt.bound('KNOWN', t['from_value'], 'DAY', t['from_zone'])} through {timefmt.bound('KNOWN', end, 'DAY', t['from_zone'])}"
        return f"[{timefmt.bound(t['from_kind'], t['from_value'], t['from_gran'], t['from_zone'])}, {timefmt.bound(t['to_kind'], t['to_value'], t['from_gran'], t['from_zone'])})"
    return "?"


def create_app(db_path, clock=db.utc_now):
    db_path = Path(db_path)
    writer_conn = db.open_store(db_path)  # migrate + gates (fail closed) before serving
    gate_facts = db.gates(writer_conn)
    write_lock = threading.Lock()
    csrf = secrets.token_urlsafe(24)
    index = FeedIndex()
    # Standing copy rule: no em dashes on the page. Verbatim bytes stay in the store;
    # only the rendering normalizes U+2014 to a hyphen.
    env = Environment(loader=FileSystemLoader(HERE / "templates"), autoescape=select_autoescape(["html"]),
                      finalize=lambda v: v.replace("\u2014", "-") if isinstance(v, str) else v)
    env.globals.update(fmt=timefmt, tags=TAGS, svg=svg)

    def reader():
        return db.connect(db_path, readonly=True)

    def page_data(conn, cut, tag, q):
        p = cut.params()
        blockers = Q.run(conn, "blockers", p)
        actions = Q.run(conn, "actions", p)
        for b in blockers:
            b["actions"] = [a for a in actions if a["blocker_id"] == b["blocker_id"] and a["status"] == "OPEN"]
        cards = build_cards(Q.run(conn, "applications", p), Q.run(conn, "terms", p), actions)
        feed = filtered_feed(conn, cut, tag, q)
        return {
            "cut": cut, "strip": [b for b in blockers if not b["is_terminal"] and b["in_effect"] != "FALSE"],
            "bedrock": [b for b in blockers if b["state"] == "FROZEN"], "blockers": blockers, "cards": cards,
            "feed": feed, "tag": tag, "q": q, "audit": Q.run(conn, "audit_check", p),
            "contracts": Q.run(conn, "contract_check", p), "ledger": Q.run(conn, "ledger", p)[0],
            "gates": gate_facts, "csrf": csrf, "timeline": svg.timeline(cards, cut),
        }

    def filtered_feed(conn, cut, tag, q):
        rows = Q.run(conn, "feed", cut.params())
        if tag in TAGS:
            rows = [r for r in rows if r["tag"] == tag]
        if q:
            hits = index.search(conn, q)
            rows = [r for r in rows if (r["item_kind"], r["item_id"]) in hits]
        return rows

    def html(template, **ctx):
        return HTMLResponse(env.get_template(template).render(**ctx))

    async def home(request: Request):
        cut = declare_cut(request, clock)
        tag, q = request.query_params.get("tag", ""), request.query_params.get("q", "").strip()
        conn = reader()
        try:
            return html("index.html", **page_data(conn, cut, tag, q))
        finally:
            conn.close()

    async def feed(request: Request):
        cut = declare_cut(request, clock)
        tag, q = request.query_params.get("tag", ""), request.query_params.get("q", "").strip()
        conn = reader()
        try:
            return html("_feed.html", feed=filtered_feed(conn, cut, tag, q), tag=tag, q=q, cut=cut)
        finally:
            conn.close()

    async def query(request: Request):
        name = request.path_params["name"]
        if name not in Q.PANELS:
            return PlainTextResponse("no such panel", status_code=404)
        cut = declare_cut(request, clock)
        return html("query.html", name=name, sql=Q.PANELS[name], params=cut.params(), cut=cut)

    async def write(request: Request):
        # urlencoded only, parsed with the stdlib (no python-multipart dependency)
        if not request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
            return PlainTextResponse("urlencoded forms only", status_code=415)
        body = await request.body()
        if len(body) > 16384:
            return PlainTextResponse("form too large", status_code=413)
        form = {k: v[0] for k, v in urllib.parse.parse_qs(body.decode("utf-8"), keep_blank_values=True).items()}
        if not secrets.compare_digest(str(form.get("csrf", "")), csrf):
            return PlainTextResponse("bad form token", status_code=403)
        now = clock()
        with write_lock:
            w = ledger.Writer(writer_conn, "operator:web", clock)
            dk = Docket(w)
            kind = request.path_params["kind"]
            with w.tx():
                if kind == "action":
                    item, prev, status = int(form["item_id"]), int(form["state_id"]), form["status"]
                    if status not in ("DONE", "DROPPED", "OPEN"):
                        return PlainTextResponse("bad status", status_code=400)
                    dk.action_state(item, status, dk.second(now, "recorded via web"), str(form.get("note", ""))[:500], supersedes=prev)
                elif kind == "note":
                    tag, title, body = form["tag"], str(form["title"]).strip(), str(form["body"]).strip()
                    if tag not in TAGS or not title or not body:
                        return PlainTextResponse("note needs tag, title, body", status_code=400)
                    if "—" in title + body:
                        return PlainTextResponse("no em dashes in people-facing copy", status_code=400)
                    dk.note(tag, title, body, dk.second(now, "recorded via web"))
                elif kind == "app-status":
                    app, prev, status = int(form["application_id"]), form.get("state_id"), form["status"]
                    ev = dk.second(now, "recorded via web")
                    iv = dk.interval(End("KNOWN", now, "SECOND", "UTC"), End("UNKNOWN"))
                    dk.app_state(app, status, ev, iv, str(form.get("basis") or "operator via web"), actor="Justin",
                                 supersedes=int(prev) if prev else None)
                else:
                    return PlainTextResponse("unknown write", status_code=404)
        index.invalidate()
        return RedirectResponse("/", status_code=303)

    async def health(request: Request):
        conn = reader()
        try:
            return PlainTextResponse(f"ok receipts={Q.run(conn, 'ledger', {})[0]['receipts']}")
        finally:
            conn.close()

    routes = [
        Route("/", home), Route("/feed", feed), Route("/query/{name}", query),
        Route("/write/{kind}", write, methods=["POST"]), Route("/health", health),
        Mount("/static", StaticFiles(directory=HERE / "static"), name="static"),
    ]
    return Starlette(routes=routes)
