"""Duolingo packet import: allowlist parse -> staging -> receipted promotion.

The packet (SHA-256 0b8f184a..., 13,643 bytes) lives in var/inbox/ (gitignored)
and is cited by hash. Only application-fact lines are kept, matched by exact
line prefix. Personal fields (contact data, GPA, account names, resume),
essays, and named outreach targets are never read into the store; the batch
records only how many lines were skipped.
"""
from __future__ import annotations

import hashlib
import json
import re

from .. import canon
from ..temporal import End
from .records import Docket

PARSER_ID = "duolingo-packet"
PARSER_VERSION = 1
RULE_SET_VERSION = 1
EXPECT_PREFIX = "0b8f184a"

# (exact line prefix, candidate kind, parser function name)
ALLOW = (
    ("**Status:** FILED by justin on ", "APPLICATION_STATE", "status"),
    ("**Role:** ", "APPLICATION_TERM", "role"),
    ("**Apply:** ", "APPLICATION_TERM", "apply"),
    ("**Deadline:** ", "APPLICATION_TERM", "deadline"),
    ("**Pay:** ", "APPLICATION_TERM", "pay"),
    ("1. Recruiter screen ", "NOTE", "pipeline"),
    ("  - **Explain My Answer → free: CONFIRMED**", "CLAIM_VERDICT", "verdict"),
    ("  - **AI speaking/video tools → free tier: KILLED as stated.**", "CLAIM_VERDICT", "verdict"),
    ("- **Lily 10x: CONFIRMED (attributed).**", "CLAIM_VERDICT", "verdict"),
    ("- Outlet claim in essay 2 ", "ACTION_ITEM", "outlet"),
    ("**Second posting note (reconciled 2026-09-29):**", "ACTION_ITEM", "second_posting"),
)
MONTHS = {m: i for i, m in enumerate(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), 1)}


def _md(s):
    return s.replace("**", "").strip()


def _status(line):
    m = re.match(r"\*\*Status:\*\* FILED by justin on (\d{4}-\d{2}-\d{2})\.", line)
    if not m:
        return "MALFORMED", {}, []
    return "PARSED", {"status": "SUBMITTED", "day": m.group(1), "actor": "Justin"}, []


def _role(line):
    m = re.match(r"\*\*Role:\*\* (.+?) \(Req (\w+)\) — (.+)$", line)
    if not m:
        return "MALFORMED", {}, []
    return "PARSED", {"terms": [
        {"key": "role", "text": f"{m.group(1)} (Req {m.group(2)})"},
        {"key": "req_ref", "text": m.group(2)},
        {"key": "location", "text": m.group(3)}]}, []


def _apply(line):
    m = re.match(r"\*\*Apply:\*\* (https://\S+)$", line)
    if not m:
        return "MALFORMED", {}, []
    return "PARSED", {"terms": [{"key": "posting_url", "text": m.group(1)}]}, []


def _deadline(line):
    m = re.match(r"\*\*Deadline:\*\* (\w{3}) (\d{1,2}), (\d{4}), (\d{1,2}:\d{2} [AP]M) ET", line)
    if not m:
        return "MALFORMED", {}, []
    day = f"{m.group(3)}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"
    # The minute is asserted, but DAY granularity is kept (R14); the wording is kept verbatim.
    return "PARSED", {"terms": [{"key": "deadline", "day": day, "source": f"{m.group(1)} {m.group(2)}, {m.group(3)}, {m.group(4)} ET"}]}, []


def _pay(line):
    m = re.match(r"\*\*Pay:\*\* \$(\d+)–(\d+)/hr \| \*\*Program:\*\* (\d+) weeks, (\w{3}) (\d+)–(\w{3}) (\d+) OR (\w{3}) (\d+)–(\w{3}) (\d+), (\d{4})$", line)
    if not m:
        return "MALFORMED", {}, []
    g = m.groups()
    yr = int(g[11])

    def d(mon, day):
        return f"{yr}-{MONTHS[mon]:02d}-{int(day):02d}"
    return "PARSED", {"terms": [
        {"key": "pay", "lo": int(g[0]) * 100, "hi": int(g[1]) * 100},
        {"key": "duration_weeks", "integer": int(g[2])},
        # "May 24-Aug 13": Aug 13 is the last day; S3 exclusive bound = successor day.
        {"key": "program_window", "ordinal": 1, "from": d(g[3], g[4]), "through": d(g[5], g[6])},
        {"key": "program_window", "ordinal": 2, "from": d(g[7], g[8]), "through": d(g[9], g[10])},
    ]}, []


def _pipeline(line):
    stages = re.findall(r"\d\. ([^→]+?)(?: →|$)", line.split(" ~9%")[0])
    if len(stages) < 6:
        return "PARTIAL", {"stages": stages}, ["stages"]
    return "PARSED", {"stages": [_md(s).rstrip('.') for s in stages], "pass_rate_text": "~9% intern pass rate"}, []


def _verdict(line):
    body = _md(line.lstrip(" -"))
    if body.startswith("Explain My Answer"):
        return "PARSED", {"subject": "Duolingo", "claim": "Explain My Answer moved to the free tier",
                          "status": "CONFIRMED", "basis": "official blog, per packet forensic pass; scope: most learners in ES/FR/DE/JA/PT/IT/KO courses"}, []
    if body.startswith("AI speaking/video tools"):
        return "PARSED", {"subject": "Duolingo", "claim": "AI speaking and video tools moved to the free tier (essay 1 wording)",
                          "status": "KILLED", "basis": "Reuters 2026-02-26 per packet: Video Call moved Max to Super (paid); free-tier speaking tools planned, not shipped"}, []
    if body.startswith("Lily 10x"):
        return "PARSED", {"subject": "Duolingo", "claim": "Lily video-call tutor became more than ten times cheaper to run than at launch",
                          "status": "CONFIRMED", "basis": "Reuters quote of von Ahn, corroborated by Q2 10-Q filed 2026-08-06, per packet; attributed, mechanism undefined"}, []
    return "MALFORMED", {}, []


def _outlet(line):
    return "PARSED", {"text": "Confirm the switched outlet in essay 2 is actually wired before any interview; if not, the honest answer is \"wiring it up now\"",
                      "owner": "Justin", "due": None}, []


def _second_posting(line):
    m = re.search(r"(\d{10}) on the `(\w+)` board", line)
    if not m:
        return "MALFORMED", {}, []
    return "PARSED", {"text": f"Decide whether to also file via posting {m.group(1)} on the {m.group(2)} board (same role as req 1265)",
                      "owner": "Justin", "due": "2026-09-30", "due_source": "Sep 30, 11:59 PM ET deadline",
                      "posting": m.group(1), "board": m.group(2)}, []


PARSERS = {name: globals()["_" + name] for name in
           ("status", "role", "apply", "deadline", "pay", "pipeline", "verdict", "outlet", "second_posting")}


def parse(data: bytes):
    lines = data.decode("utf-8").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    kept = []
    for no, line in enumerate(lines, start=1):
        for prefix, kind, fn in ALLOW:
            if line.startswith(prefix):
                state, payload, missing = PARSERS[fn](line)
                kept.append((no, line, kind, state, payload, missing))
                break
    return len(lines), kept


def import_packet(dk: Docket, path, app_id, artifact_id):
    """Ingest, decide, promote. Caller holds the transaction."""
    w = dk.w
    with open(path, "rb") as f:
        data = f.read()
    total, kept = parse(data)
    batch = w.insert("stg_ingest_batch", {
        "format_tag": "DUOLINGO_PACKET", "artifact_id": artifact_id, "parser_id": PARSER_ID,
        "parser_version": PARSER_VERSION, "lines_total": total, "lines_kept": len(kept)}, "packet ingest")
    decisions = []
    for no, line, kind, state, payload, missing in kept:
        raw = w.insert("stg_raw_row", {"batch_id": batch, "line_no": no, "raw_text": line,
                                       "raw_sha256": hashlib.sha256(line.encode()).hexdigest()}, f"packet line {no}")
        cand = w.insert("stg_candidate", {"raw_row_id": raw, "candidate_kind": kind, "parse_state": state,
                                          "payload_json": canon.text(payload) if state != "MALFORMED" else "{}",
                                          "missing_fields_json": json.dumps(missing)}, f"candidate line {no}")
        ok = state == "PARSED"
        dec = w.insert("stg_promotion_decision", {
            "candidate_id": cand, "rule_id": f"duolingo-{kind.lower()}", "rule_version": RULE_SET_VERSION,
            "decision": "PROMOTE" if ok else "HOLD",
            "reason": "parsed, allowlisted application fact" if ok else f"parse_state {state}"}, f"decision line {no}")
        if ok:
            decisions.append((dec, no, line, kind, payload))
    run = w.insert("core_promotion_run", {"batch_id": batch, "rule_set_version": RULE_SET_VERSION}, "promotion run")
    w.promotion_run_id = run
    try:
        for dec, no, line, kind, payload in decisions:
            for target in list(_promote(dk, app_id, artifact_id, kind, payload, line)):
                rid = w.conn.execute(f"SELECT receipt_id FROM {target[0]} WHERE {target[1]} = ?", (target[2],)).fetchall()[0][0]
                w.insert("core_promotion_link", {"promotion_run_id": run, "decision_id": dec, "target_receipt_id": rid},
                         f"link line {no}")
    finally:
        w.promotion_run_id = None
    return {"batch_id": batch, "lines_total": total, "lines_kept": len(kept), "promoted": len(decisions), "run": run}


def _promote(dk: Docket, app_id, art, kind, p, line):
    """Write core rows for one decision; yield (table, pk_col, pk) for each."""
    if kind == "APPLICATION_STATE":
        ev = dk.day(p["day"], "FILED by justin on " + p["day"])
        iv = dk.interval(End("KNOWN", p["day"], "DAY", "America/New_York"), End("UNKNOWN"))
        sid = dk.app_state(app_id, p["status"], ev, iv, "Duolingo packet status line", actor=p["actor"], artifact_id=art)
        yield ("core_instant", "instant_id", ev)
        yield ("core_interval", "interval_id", iv)
        yield ("core_application_state", "state_id", sid)
    elif kind == "APPLICATION_TERM":
        for t in p["terms"]:
            k = t["key"]
            if k == "deadline":
                ev = dk.day(t["day"], t["source"])
                yield ("core_instant", "instant_id", ev)
                tid = dk.term(app_id, k, line, instant_id=ev, artifact_id=art)
            elif k == "pay":
                tid = dk.term(app_id, k, line, money_range=(t["lo"], t["hi"], "USD", "HOUR"), artifact_id=art)
            elif k == "duration_weeks":
                tid = dk.term(app_id, k, line, integer=t["integer"], artifact_id=art)
            elif k == "program_window":
                import datetime as dt
                end = (dt.date.fromisoformat(t["through"]) + dt.timedelta(days=1)).isoformat()
                iv = dk.interval(End("KNOWN", t["from"], "DAY", "America/New_York"), End("KNOWN", end, "DAY", "America/New_York"))
                yield ("core_interval", "interval_id", iv)
                tid = dk.term(app_id, k, line, interval_id=iv, ordinal=t["ordinal"], artifact_id=art)
            else:
                tid = dk.term(app_id, k, line, text=t["text"], artifact_id=art)
            yield ("core_application_term", "term_id", tid)
    elif kind == "NOTE":
        ev = dk.day("2026-09-29", "packet dated 2026-09-29")
        body = "Public reports, per packet: " + "; ".join(f"{i}. {s}" for i, s in enumerate(p["stages"], 1)) + ". " + p["pass_rate_text"] + "."
        nid = dk.note("applications", "Duolingo interview pipeline if the screen lands", body, ev, application_id=app_id, artifact_id=art)
        yield ("core_instant", "instant_id", ev)
        yield ("core_note", "note_id", nid)
    elif kind == "CLAIM_VERDICT":
        ev = dk.day("2026-09-29", "forensic pass verified 2026-09-29")
        cid = dk.claim(p["subject"], p["claim"], source_quote=line, artifact_id=art)
        vid = dk.verdict(cid, p["status"], ev, "forensic pass (packet)", p["basis"])
        eid = dk.abstain_eclass(cid)
        yield ("core_instant", "instant_id", ev)
        yield ("core_claim", "claim_id", cid)
        yield ("core_verdict", "verdict_id", vid)
        yield ("core_claim_eclass", "eclass_id", eid)
    elif kind == "ACTION_ITEM":
        due = dk.day(p["due"], p["due_source"]) if p.get("due") else dk.unknown_instant("no due date in packet")
        item = dk.action_item(p["text"], p["owner"], due, application_id=app_id)
        ev = dk.day("2026-09-29", "packet dated 2026-09-29")
        st = dk.action_state(item, "OPEN", ev, "from Duolingo packet")
        yield ("core_instant", "instant_id", due)
        yield ("core_action_item", "item_id", item)
        yield ("core_instant", "instant_id", ev)
        yield ("core_action_item_state", "state_id", st)
