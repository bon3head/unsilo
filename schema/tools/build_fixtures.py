"""Emit deterministic SQL fixtures for the schema walk-throughs.

Output:
  fixtures/duolingo_promotion_walk.sql
  fixtures/b4_regression.sql
  fixtures/b1_retraction_bitemporal.sql

Every core row is written as (receipt INSERT, row INSERT) in that order, with
real SHA-256 values computed per README 6.2. Timestamps are fixed literals,
never the clock, so the same script always emits the same bytes.
All rows are ILLUSTRATIVE fixtures built only from facts in the pack.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def lit(v):
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


class Ledger:
    def __init__(self):
        self.lines = []
        self.next_receipt = 1
        self.head = None

    def raw(self, sql):
        self.lines.append(sql)

    def core(self, table, pk_col, row, actor, reason, recorded_at, run_id=None):
        rid = self.next_receipt
        row = dict(row)
        row["receipt_id"] = rid
        image = canon(row)
        rec = {
            "receipt_id": rid, "table_name": table, "row_pk": row[pk_col], "op": "INSERT",
            "actor": actor, "reason": reason, "promotion_run_id": run_id,
            "before_kind": "ABSENT", "before_sha256": None,
            "after_sha256": sha(image),
            "prev_kind": "GENESIS" if self.head is None else "HASH",
            "prev_receipt_sha256": self.head,
            "recorded_at": recorded_at,
        }
        rec["receipt_sha256"] = sha(canon(rec))
        rec["after_image_json"] = image
        cols = ["receipt_id", "table_name", "row_pk", "op", "actor", "reason", "promotion_run_id",
                "before_kind", "before_sha256", "after_sha256", "after_image_json",
                "prev_kind", "prev_receipt_sha256", "receipt_sha256", "recorded_at"]
        self.lines.append(f"INSERT INTO meta_receipt ({', '.join(cols)}) VALUES ({', '.join(lit(rec[c]) for c in cols)});")
        rcols = list(row.keys())
        self.lines.append(f"INSERT INTO {table} ({', '.join(rcols)}) VALUES ({', '.join(lit(row[c]) for c in rcols)});")
        self.head = rec["receipt_sha256"]
        self.next_receipt += 1
        return rid

    def text(self):
        return "\n".join(self.lines) + "\n"


def duolingo_walk():
    L = Ledger()
    T0 = "2026-10-02T12:00:00Z"
    L.raw("-- Duolingo-format staging ingest and promotion, walked by hand.")
    L.raw("-- ILLUSTRATIVE: the real packet file is not in the pack (OPEN U-DASH-07).")
    L.raw("-- Every value below is taken from a pack document named in README 7.")
    L.raw("BEGIN;")
    raw_rows = [
        "APPLICATION | company=Duolingo | req=1265 | submitted=2026-09-29",
        "CLAIM | company=Duolingo | text=SEC Submissions JSON for CIK0001562088 returned Duolingo, Inc. with 776 recent filings | source=poc-results-2026-09-30.md P2",
        "CLAIM | company=Duolingo | text=Duolingo careers requires JS rendering | source=s2-output-2026-09-30.md",
        "APPLICATION | company=Duolingo | req=",
        "APPLICATION | company=Duolingo | req=1265 | submitted=2026-09-29",
    ]
    packet = "\n".join(raw_rows) + "\n"
    L.raw("-- Step 1. Batch: one row per source file, hash of the exact bytes.")
    L.raw(f"INSERT INTO stg_ingest_batch VALUES (1, 'DUOLINGO_PACKET', 'ILLUSTRATIVE/duolingo-packet.txt', {lit(sha(packet))}, {len(packet.encode())}, '2026-10-02T11:00:00Z', 'operator-agent');")
    L.raw("-- Step 2. Raw rows, verbatim, with per-row hash.")
    for i, r in enumerate(raw_rows, 1):
        L.raw(f"INSERT INTO stg_raw_row VALUES ({i}, 1, {i}, {lit(r)}, {lit(sha(r))});")
    L.raw("-- Step 3. Parse (parser duolingo-packet v1). Missing fields are listed, never defaulted.")
    cands = [
        (1, 1, "APPLICATION", "PARTIAL", {"company_name": "Duolingo", "req_ref": "1265", "submitted_day": "2026-09-29"}, ["platform", "role", "location"]),
        (2, 2, "CLAIM", "PARSED", {"company_name": "Duolingo", "claim_text": "SEC Submissions JSON for CIK0001562088 returned Duolingo, Inc. with 776 recent filings", "source_ref": "poc-results-2026-09-30.md P2"}, []),
        (3, 3, "CLAIM", "PARSED", {"company_name": "Duolingo", "claim_text": "Duolingo careers requires JS rendering", "source_ref": "s2-output-2026-09-30.md"}, []),
        (4, 4, "APPLICATION", "MALFORMED", {}, []),
        (5, 5, "APPLICATION", "PARTIAL", {"company_name": "Duolingo", "req_ref": "1265", "submitted_day": "2026-09-29"}, ["platform", "role", "location"]),
    ]
    for cid, rr, kind, st, payload, missing in cands:
        L.raw(f"INSERT INTO stg_candidate VALUES ({cid}, {rr}, 'duolingo-packet', 1, '{kind}', '{st}', {lit(canon(payload))}, {lit(canon(missing))});")
    L.raw("-- Step 4. Promotion decisions (rules in README 7.3).")
    decisions = [
        (1, 1, "R-APP-1", "PROMOTE", "exact single company match after R-CO-1; platform, role, location UNKNOWN"),
        (2, 2, "R-CLAIM-1", "PROMOTE", "claim promoted UNJOINED: raw P2 output is not in the corpus (U-1R-AUTH-013)"),
        (3, 3, "R-CLAIM-1", "PROMOTE", "claim promoted JOINED to the S2 digest artifact; digest proves only what it says"),
        (4, 4, "R-PARSE-1", "REJECT", "MALFORMED: req field empty"),
        (5, 5, "R-DEDUPE-1", "REJECT", "raw_sha256 identical to raw row 1 in this batch; duplicate"),
    ]
    for did, cid, rule, dec, why in decisions:
        L.raw(f"INSERT INTO stg_promotion_decision VALUES ({did}, {cid}, '{rule}', 1, '{dec}', {lit(why)}, 'operator-agent', '2026-10-02T11:30:00Z');")

    L.raw("-- Step 5. Promotion run 1. Receipt first, then row, for every core row.")
    A = "promotion-run-1"
    run_rid = L.core("core_promotion_run", "promotion_run_id",
                     {"promotion_run_id": 1, "batch_id": 1, "rule_set_version": 1, "started_at": T0},
                     A, "open promotion run for batch 1", T0, 1)

    def link(link_id, decision_id, target_rid):
        L.core("core_promotion_link", "link_id",
               {"link_id": link_id, "promotion_run_id": 1, "decision_id": decision_id, "target_receipt_id": target_rid},
               A, f"link decision {decision_id} to receipt {target_rid}", T0, 1)

    # Instants and intervals.
    L.core("core_instant", "instant_id", {"instant_id": 1, "kind": "KNOWN", "value": "2026-09-29", "gran": "DAY", "zone": "America/New_York", "source_text": "submitted=2026-09-29"}, A, "application submission day", T0, 1)
    L.core("core_instant", "instant_id", {"instant_id": 2, "kind": "KNOWN", "value": "2026-10-02T11:00:00Z", "gran": "SECOND", "zone": "UTC", "source_text": "batch captured_at"}, A, "artifact capture time", T0, 1)
    L.core("core_instant", "instant_id", {"instant_id": 3, "kind": "KNOWN", "value": "2026-10-02T12:00:00Z", "gran": "SECOND", "zone": "UTC", "source_text": "promotion run decision time"}, A, "decision time", T0, 1)
    L.core("core_interval", "interval_id", {"interval_id": 1, "from_kind": "KNOWN", "from_value": "2026-09-29", "from_gran": "DAY", "from_zone": "America/New_York", "to_kind": "UNKNOWN", "to_value": None, "to_gran": None, "to_zone": None, "unbounded_basis": ""}, A, "SUBMITTED holds from submission day until an unknown later change", T0, 1)

    # Company: opaque key. The CIK is a claim, not yet a key (no binding artifact).
    co_rid = L.core("core_company", "company_id", {"company_id": 1, "key_kind": "UNSILO_OPAQUE", "company_key": "us-co-duolingo"}, A, "R-CO-1: no exact variant match; no CIK binding artifact in corpus", T0, 1)
    nv_rid = L.core("core_name_variant", "variant_id", {"variant_id": 1, "company_id": 1, "variant": "Duolingo", "basis_kind": "OPERATOR_STATEMENT", "basis_artifact_id": None, "basis_note": "name as written in the operator packet", "decided_at_instant_id": 3}, A, "R-CO-1 variant", T0, 1)

    # Artifacts.
    s2 = (ROOT.parent / "research-chain" / "s2-output-2026-09-30.md").read_bytes()
    L.core("core_artifact", "artifact_id", {"artifact_id": 1, "sha256": sha(packet), "path": "ILLUSTRATIVE/duolingo-packet.txt", "byte_len": len(packet.encode()), "captured_at_instant_id": 2}, A, "batch source file", T0, 1)
    L.core("core_artifact", "artifact_id", {"artifact_id": 2, "sha256": hashlib.sha256(s2).hexdigest(), "path": "research-chain/s2-output-2026-09-30.md", "byte_len": len(s2), "captured_at_instant_id": 2}, A, "S2 digest as cited by candidate 3", T0, 1)

    # Application (candidate 1).
    app_rid = L.core("core_application", "application_id", {"application_id": 1, "company_id": 1, "role_state": "UNKNOWN", "role": None, "platform_state": "UNKNOWN", "platform": None, "req_state": "STATED", "req_ref": "1265", "location_state": "UNKNOWN", "location": None}, A, "R-APP-1", T0, 1)
    st_rid = L.core("core_application_state", "state_id", {"state_id": 1, "application_id": 1, "status": "SUBMITTED", "event_instant_id": 1, "valid_interval_id": 1, "submitted_by": "operator", "supersedes_state_id": None}, A, "R-APP-1 initial state", T0, 1)

    # Claims (candidates 2, 3) with both axes.
    c1 = L.core("core_claim", "claim_id", {"claim_id": 1, "subject_kind": "COMPANY", "company_id": 1, "claim_text": "SEC Submissions JSON for CIK0001562088 returned Duolingo, Inc. with 776 recent filings", "source_quote": "", "artifact_state": "UNJOINED", "artifact_id": None, "supersedes_claim_id": None}, A, "R-CLAIM-1 unjoined", T0, 1)
    v1 = L.core("core_verdict", "verdict_id", {"verdict_id": 1, "claim_id": 1, "status": "UNRESOLVED", "decided_at_instant_id": 3, "decided_by": "promotion-run-1", "rationale": "no artifact row; UNRESOLVED by construction", "audit_run_id": None, "supersedes_verdict_id": None}, A, "R-CLAIM-1 default verdict", T0, 1)
    e1 = L.core("core_claim_eclass", "eclass_id", {"eclass_id": 1, "claim_id": 1, "contract_id": "RECON-ECLASS-PD-AO-DD-v2.0", "state": "ABSTENTION", "class": None, "weak": 0, "abstention_reason": "CLASSIFIER_NOT_ADMITTED", "supersedes_eclass_id": None}, A, "R-CLAIM-1 evidence-class axis", T0, 1)
    c2 = L.core("core_claim", "claim_id", {"claim_id": 2, "subject_kind": "COMPANY", "company_id": 1, "claim_text": "Duolingo careers requires JS rendering", "source_quote": "JS rendering is admissible observation (Duolingo careers requires JS).", "artifact_state": "JOINED", "artifact_id": 2, "supersedes_claim_id": None}, A, "R-CLAIM-1 joined", T0, 1)
    v2 = L.core("core_verdict", "verdict_id", {"verdict_id": 2, "claim_id": 2, "status": "UNRESOLVED", "decided_at_instant_id": 3, "decided_by": "promotion-run-1", "rationale": "artifact is a digest; it proves only that the digest says this", "audit_run_id": None, "supersedes_verdict_id": None}, A, "R-CLAIM-1 default verdict", T0, 1)
    e2 = L.core("core_claim_eclass", "eclass_id", {"eclass_id": 2, "claim_id": 2, "contract_id": "RECON-ECLASS-PD-AO-DD-v2.0", "state": "ABSTENTION", "class": None, "weak": 0, "abstention_reason": "CLASSIFIER_NOT_ADMITTED", "supersedes_eclass_id": None}, A, "R-CLAIM-1 evidence-class axis", T0, 1)

    # Expectation: a reply to req 1265, operator-basis, not yet evaluated.
    L.core("core_interval", "interval_id", {"interval_id": 2, "from_kind": "KNOWN", "from_value": "2026-09-29", "from_gran": "DAY", "from_zone": "America/New_York", "to_kind": "UNKNOWN", "to_value": None, "to_gran": None, "to_zone": None, "unbounded_basis": ""}, A, "reply window opens at submission; close unknown", T0, 1)
    L.core("core_expectation", "expectation_id", {"expectation_id": 1, "subject_kind": "APPLICATION", "company_id": None, "application_id": 1, "claim_id": None, "blocker_id": None, "expected_artifact_type": "recruiter reply for req 1265", "expected_window_interval_id": 2, "basis": "OPERATOR", "basis_note": "no stated reply SLA in the pack", "checked_scope": "operator inbox as recorded in UnSilo"}, A, "absence-as-signal row", T0, 1)
    L.core("core_expectation_state", "state_id", {"state_id": 1, "expectation_id": 1, "status": "NOT_EVALUATED", "checked_instant_id": 3, "evidence_artifact_id": None, "note": "no inbox check recorded", "supersedes_state_id": None}, A, "initial expectation state", T0, 1)

    link(1, 1, app_rid)
    link(2, 2, c1)
    link(3, 3, c2)
    L.raw("-- Step 6. Declared cuts. Evaluation never reads the clock.")
    L.raw("INSERT INTO meta_cut VALUES (1, 'submission-day', '2026-09-29', 'DAY', 'America/New_York', '2026-10-02T12:00:00Z');")
    L.raw("INSERT INTO meta_cut VALUES (2, 'walk-2026-10-02', '2026-10-02', 'DAY', 'America/New_York', '2026-10-02T12:00:00Z');")
    L.raw("INSERT INTO meta_cut VALUES (3, 'before-promotion', '2026-10-02', 'DAY', 'America/New_York', '2026-10-02T11:59:59Z');")
    L.raw("-- Step 7. Rebuild the disposable FTS projection at the end of the run.")
    L.raw("DELETE FROM fts_feed;")
    L.raw("INSERT INTO fts_feed (cut_id, item_kind, item_id, title, body) SELECT cut_id, item_kind, item_id, title, body FROM feed_item;")
    L.raw("COMMIT;")
    return L.text()


def b4_regression():
    L = Ledger()
    T0 = "2026-10-02T12:00:00Z"
    A = "b4-regression"
    L.raw("-- B4 regression: the freeze/collapse failure modes vs the new design.")
    L.raw("BEGIN;")
    cases = [
        # id, from, to, note
        (1, ("KNOWN", "2026-09-29"), ("UNKNOWN", None), "open application, close unknown"),
        (2, ("KNOWN", "2026-10-02"), ("UNKNOWN", None), "cut equals known start, end unknown"),
        (3, ("UNBOUNDED", None), ("KNOWN", "2026-10-05"), "unbounded start, known end after cut"),
        (4, ("UNKNOWN", None), ("KNOWN", "2026-10-05"), "unknown start, known end after cut"),
        (5, ("UNKNOWN", None), ("KNOWN", "2026-10-01"), "unknown start, known end before cut"),
        (6, ("KNOWN", "2026-09-01"), ("UNBOUNDED", None), "known start, affirmatively unbounded end"),
        (7, ("KNOWN", "2026-10-03"), ("UNKNOWN", None), "known start after cut, end unknown"),
        (8, ("UNBOUNDED", None), ("UNBOUNDED", None), "both unbounded"),
        (9, ("UNKNOWN", None), ("UNKNOWN", None), "both unknown"),
        (10, ("KNOWN", "2026-09-01"), ("KNOWN", "2026-10-02"), "half-open: cut equals known end"),
    ]
    for cid, (fk, fv), (tk, tv), note in cases:
        row = {"interval_id": cid,
               "from_kind": fk, "from_value": fv, "from_gran": "DAY" if fv else None, "from_zone": "America/New_York" if fv else None,
               "to_kind": tk, "to_value": tv, "to_gran": "DAY" if tv else None, "to_zone": "America/New_York" if tv else None,
               "unbounded_basis": "fixture: source asserts no finite bound" if "UNBOUNDED" in (fk, tk) else ""}
        L.core("core_interval", "interval_id", row, A, note, T0)
    L.raw("INSERT INTO meta_cut VALUES (1, 'cut-2026-10-02', '2026-10-02', 'DAY', 'America/New_York', '2026-10-02T12:00:00Z');")
    L.raw("COMMIT;")
    L.raw("")
    L.raw("-- OLD DESIGN (nullable valid_to; NULL means both 'still open' and 'unknown'):")
    L.raw("CREATE TEMP TABLE old_design (id INTEGER PRIMARY KEY, valid_from TEXT, valid_to TEXT);")
    for cid, (fk, fv), (tk, tv), note in cases:
        L.raw(f"INSERT INTO old_design VALUES ({cid}, {lit(fv)}, {lit(tv)});")
    return L.text()


def b1_retraction():
    L = Ledger()
    A = "retraction-fixture"
    t1, t2 = "2026-10-01T08:38:00Z", "2026-10-01T11:00:00Z"
    L.raw("-- B1 FROZEN at 4:38 AM ET, retracted at 7:00 AM ET (master doc section 7).")
    L.raw("-- ILLUSTRATIVE recording times: 08:38Z and 11:00Z are the ledger times in UTC.")
    L.raw("BEGIN;")
    L.core("core_blocker", "blocker_id", {"blocker_id": 1, "program": "RESEARCH_CHAIN", "code": "B1", "title": "Canonical QueryDefinition"}, A, "blocker identity", t1)
    L.core("core_interval", "interval_id", {"interval_id": 1, "from_kind": "KNOWN", "from_value": "2026-10-01", "from_gran": "DAY", "from_zone": "America/New_York", "to_kind": "UNKNOWN", "to_value": None, "to_gran": None, "to_zone": None, "unbounded_basis": ""}, A, "state holds from 2026-10-01", t1)
    L.core("core_blocker_state", "state_id", {"state_id": 1, "blocker_id": 1, "state": "FROZEN", "valid_interval_id": 1, "falsifier_state": "UNKNOWN", "falsifier": None, "owner_state": "UNKNOWN", "owner": None, "basis": "ledger 4:38 AM ET admission ACCEPT entry", "supersedes_state_id": None}, A, "admission ACCEPT recorded", t1)
    L.core("core_blocker_state", "state_id", {"state_id": 2, "blocker_id": 1, "state": "REPAIRED_PENDING_ADMISSION", "valid_interval_id": 1, "falsifier_state": "STATED", "falsifier": "fresh Sol/High admission by exact reuse of the retained extraction reports returns ACCEPT", "owner_state": "UNKNOWN", "owner": None, "basis": "7:00 AM ET correction: admission procedurally non-admissible", "supersedes_state_id": 1}, A, "retraction", t2)
    L.raw("INSERT INTO meta_cut VALUES (1, 'k-before-retraction', '2026-10-01', 'DAY', 'America/New_York', '2026-10-01T09:00:00Z');")
    L.raw("INSERT INTO meta_cut VALUES (2, 'k-after-retraction', '2026-10-01', 'DAY', 'America/New_York', '2026-10-01T12:00:00Z');")
    L.raw("COMMIT;")
    return L.text()


if __name__ == "__main__":
    out = ROOT / "fixtures"
    out.mkdir(exist_ok=True)
    (out / "duolingo_promotion_walk.sql").write_text(duolingo_walk(), encoding="utf-8")
    (out / "b4_regression.sql").write_text(b4_regression(), encoding="utf-8")
    (out / "b1_retraction_bitemporal.sql").write_text(b1_retraction(), encoding="utf-8")
    print("ok")
