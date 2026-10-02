"""Docket record API: typed constructors over the one write path.

Every method validates what SQL cannot (zones against pinned tzdata,
mixed-granularity interval order) and then calls Writer.insert. Callers wrap
calls in writer.tx().
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from .. import temporal
from ..ledger import Writer
from ..temporal import End

REPO = Path(__file__).resolve().parents[2]


class Docket:
    def __init__(self, writer: Writer):
        self.w = writer

    # time -------------------------------------------------------------------
    def instant(self, value=None, gran=None, zone=None, source_text="", reason="instant"):
        if value is None:
            row = {"kind": "UNKNOWN", "source_text": source_text}
        else:
            temporal.check_value(value, gran, zone)
            row = {"kind": "KNOWN", "value": value, "gran": gran, "zone": zone, "source_text": source_text}
        return self.w.insert("core_instant", row, reason)

    def day(self, value, source_text, zone="America/New_York"):
        return self.instant(value, "DAY", zone, source_text)

    def second(self, value, source_text):
        return self.instant(value, "SECOND", "UTC", source_text)

    def unknown_instant(self, source_text):
        return self.instant(None, source_text=source_text)

    def interval(self, frm: End, to: End, unbounded_basis="", reason="interval"):
        temporal.interval_valid(frm, to)
        row = {"unbounded_basis": unbounded_basis}
        for side, e in (("from", frm), ("to", to)):
            row[f"{side}_kind"] = e.kind
            row[f"{side}_value"], row[f"{side}_gran"], row[f"{side}_zone"] = e.value, e.gran, e.zone
        return self.w.insert("core_interval", row, reason)

    # artifacts --------------------------------------------------------------
    def artifact(self, path: Path, storage: str, label: str, media_type="text/markdown", expect_prefix=None):
        data = Path(path).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if expect_prefix and not digest.startswith(expect_prefix):
            raise ValueError(f"{path}: SHA-256 {digest[:8]} does not match expected prefix {expect_prefix}")
        rel = str(Path(path).resolve().relative_to(REPO))
        return self.w.insert("core_artifact", {"sha256": digest, "storage": storage, "path": rel,
                                               "byte_len": len(data), "media_type": media_type, "label": label},
                             f"artifact {label}")

    # applications -----------------------------------------------------------
    def application(self, app_key, employer_label):
        return self.w.insert("core_application", {"app_key": app_key, "employer_label": employer_label},
                             f"application {app_key}")

    def app_state(self, application_id, status, event_instant_id, valid_interval_id, basis,
                  actor=None, artifact_id=None, supersedes=None):
        return self.w.insert("core_application_state", {
            "application_id": application_id, "status": status, "event_instant_id": event_instant_id,
            "valid_interval_id": valid_interval_id, "actor_state": "STATED" if actor else "UNKNOWN",
            "actor": actor, "basis": basis, "artifact_id": artifact_id, "supersedes_state_id": supersedes},
            f"application {application_id} status {status}")

    def term(self, application_id, key, source_text, *, text=None, integer=None, money=None, money_range=None,
             instant_id=None, interval_id=None, unknown=False, ordinal=1, artifact_id=None, supersedes=None):
        row = {"application_id": application_id, "term_key": key, "ordinal": ordinal, "source_text": source_text,
               "artifact_id": artifact_id, "supersedes_term_id": supersedes}
        if text is not None:
            row.update(value_kind="TEXT", text_value=text)
        elif integer is not None:
            row.update(value_kind="INTEGER", int_value=integer)
        elif money is not None:
            amount, cur, unit = money
            row.update(value_kind="MONEY_MINOR", amount_minor=amount, currency=cur, per_unit=unit)
        elif money_range is not None:
            lo, hi, cur, unit = money_range
            row.update(value_kind="MONEY_RANGE_MINOR", amount_minor=lo, amount_minor_hi=hi, currency=cur, per_unit=unit)
        elif instant_id is not None:
            row.update(value_kind="INSTANT", instant_id=instant_id)
        elif interval_id is not None:
            row.update(value_kind="INTERVAL", interval_id=interval_id)
        elif unknown:
            row.update(value_kind="UNKNOWN")
        else:
            raise ValueError("term needs a value or unknown=True")
        return self.w.insert("core_application_term", row, f"application {application_id} term {key}")

    # blockers ---------------------------------------------------------------
    def blocker(self, program, code, title):
        return self.w.insert("core_blocker", {"program": program, "code": code, "title": title},
                             f"blocker {program}/{code}")

    def blocker_state(self, blocker_id, state, valid_interval_id, asserted_instant_id, basis,
                      falsifier=None, owner=None, artifact_id=None, supersedes=None):
        return self.w.insert("core_blocker_state", {
            "blocker_id": blocker_id, "state": state, "valid_interval_id": valid_interval_id,
            "asserted_instant_id": asserted_instant_id,
            "falsifier_state": "STATED" if falsifier else "UNKNOWN", "falsifier": falsifier,
            "owner_state": "STATED" if owner else "UNKNOWN", "owner": owner,
            "basis": basis, "artifact_id": artifact_id, "supersedes_state_id": supersedes},
            f"blocker {blocker_id} state {state}")

    # action items -----------------------------------------------------------
    def action_item(self, text, owner, due_instant_id, application_id=None, blocker_id=None):
        kind = "APPLICATION" if application_id else "BLOCKER"
        return self.w.insert("core_action_item", {
            "subject_kind": kind, "application_id": application_id, "blocker_id": blocker_id,
            "text": text, "owner": owner, "due_instant_id": due_instant_id}, f"action item ({kind})")

    def action_state(self, item_id, status, event_instant_id, note="", supersedes=None):
        return self.w.insert("core_action_item_state", {
            "item_id": item_id, "status": status, "event_instant_id": event_instant_id, "note": note,
            "supersedes_state_id": supersedes}, f"action item {item_id} {status}")

    # notes and claims -------------------------------------------------------
    def note(self, tag, title, body, event_instant_id, application_id=None, artifact_id=None, supersedes=None):
        return self.w.insert("core_note", {
            "tag": tag, "title": title, "body": body, "event_instant_id": event_instant_id,
            "application_id": application_id, "artifact_id": artifact_id, "supersedes_note_id": supersedes},
            f"note {tag}")

    def claim(self, subject_label, claim_text, source_quote="", artifact_id=None):
        return self.w.insert("core_claim", {
            "subject_label": subject_label, "claim_text": claim_text, "source_quote": source_quote,
            "artifact_state": "JOINED" if artifact_id else "UNJOINED", "artifact_id": artifact_id},
            f"claim on {subject_label}")

    def verdict(self, claim_id, status, decided_at_instant_id, decided_by, rationale, audit_run_id=None, supersedes=None):
        return self.w.insert("core_verdict", {
            "claim_id": claim_id, "status": status, "decided_at_instant_id": decided_at_instant_id,
            "decided_by": decided_by, "rationale": rationale, "audit_run_id": audit_run_id,
            "supersedes_verdict_id": supersedes}, f"verdict {status} on claim {claim_id}")

    def abstain_eclass(self, claim_id):
        return self.w.insert("core_claim_eclass", {
            "claim_id": claim_id, "contract_id": "RECON-ECLASS-PD-AO-DD-v2.0", "state": "ABSTENTION",
            "class": None, "weak": 0, "abstention_reason": "CLASSIFIER_NOT_ADMITTED"},
            f"evidence class for claim {claim_id}")

    def audit_run(self, run_instant_id, scope, worker_set=None):
        return self.w.insert("core_audit_run", {
            "run_instant_id": run_instant_id, "scope": scope,
            "worker_set_state": "STATED" if worker_set else "UNKNOWN", "worker_set": worker_set},
            "audit run")

    def audit_count(self, audit_run_id, key, value, source_text):
        return self.w.insert("core_audit_count", {
            "audit_run_id": audit_run_id, "count_key": key, "reported_value": value, "source_text": source_text},
            f"audit count {key}")

    def audit_finding(self, audit_run_id, claim_id, verdict_id, reported_status, delta):
        return self.w.insert("core_audit_finding", {
            "audit_run_id": audit_run_id, "claim_id": claim_id, "verdict_id": verdict_id,
            "reported_status": reported_status, "delta": delta}, "audit finding")
