"""Docket panel queries. Each panel is one named SQL text with bound cut
parameters; the page prints both (the openable query, S8/R16).

Cut parameters:
  :k           knowledge cut, UTC second. A row is visible iff its receipt was
               recorded at or before :k. recorded_at never decreases with
               receipt_id (trigger), so visibility = receipt_id <= kr.
  :eff_value, :eff_gran, :eff_zone   effective cut for B4 membership.
Heads: a visible row that no visible row supersedes. Two heads = conflict,
both shown (head_count), never a silent pick.
"""
from __future__ import annotations

KC = "kc(kr) AS (SELECT coalesce(max(receipt_id), 0) FROM meta_receipt WHERE recorded_at <= :k)"
B4 = ("{i}.from_kind, {i}.from_value, {i}.from_gran, {i}.from_zone, "
      "{i}.to_kind, {i}.to_value, {i}.to_gran, {i}.to_zone, :eff_value, :eff_gran, :eff_zone")

PANELS = {}


def panel(name):
    def deco(sql):
        PANELS[name] = sql.strip()
        return sql
    return deco


BLOCKERS = panel("blockers")(f"""
WITH {KC},
head AS (
  SELECT s.* FROM core_blocker_state s, kc
   WHERE s.receipt_id <= kc.kr
     AND NOT EXISTS (SELECT 1 FROM core_blocker_state x
                      WHERE x.supersedes_state_id = s.state_id AND x.receipt_id <= kc.kr))
SELECT b.blocker_id, b.program, b.code, b.title,
       h.state_id, h.state, v.is_terminal,
       h.falsifier_state, h.falsifier, h.owner_state, h.owner, h.basis,
       b4_truth({B4.format(i='i')}) AS in_effect,
       b4_reason({B4.format(i='i')}) AS in_effect_reason,
       a.kind AS asof_kind, a.value AS asof_value, a.gran AS asof_gran, a.zone AS asof_zone, a.source_text AS asof_text,
       (SELECT count(*) FROM head h2 WHERE h2.blocker_id = h.blocker_id) AS head_count,
       (SELECT count(*) FROM core_blocker_state p, kc WHERE p.blocker_id = b.blocker_id AND p.receipt_id <= kc.kr) AS history_len
  FROM head h
  JOIN core_blocker b ON b.blocker_id = h.blocker_id
  JOIN core_blocker_state_vocab v ON v.state = h.state
  JOIN core_interval i ON i.interval_id = h.valid_interval_id
  JOIN core_instant a ON a.instant_id = h.asserted_instant_id
 ORDER BY CASE b.program WHEN 'UNSILO_BUILD' THEN 0 WHEN 'RESEARCH_CHAIN' THEN 1 ELSE 2 END,
          b.blocker_id, h.state_id
""")

APPLICATIONS = panel("applications")(f"""
WITH {KC},
head AS (
  SELECT s.* FROM core_application_state s, kc
   WHERE s.receipt_id <= kc.kr
     AND NOT EXISTS (SELECT 1 FROM core_application_state x
                      WHERE x.supersedes_state_id = s.state_id AND x.receipt_id <= kc.kr))
SELECT ap.application_id, ap.app_key, ap.employer_label,
       h.state_id, h.status, h.actor_state, h.actor, h.basis,
       e.kind AS ev_kind, e.value AS ev_value, e.gran AS ev_gran, e.zone AS ev_zone, e.source_text AS ev_text,
       b4_truth({B4.format(i='i')}) AS in_effect,
       b4_reason({B4.format(i='i')}) AS in_effect_reason,
       (SELECT count(*) FROM head h2 WHERE h2.application_id = ap.application_id) AS head_count
  FROM core_application ap, kc
  LEFT JOIN head h ON h.application_id = ap.application_id
  LEFT JOIN core_instant e ON e.instant_id = h.event_instant_id
  LEFT JOIN core_interval i ON i.interval_id = h.valid_interval_id
 WHERE ap.receipt_id <= kc.kr
 ORDER BY ap.application_id, h.state_id
""")

TERMS = panel("terms")(f"""
WITH {KC}
SELECT t.application_id, t.term_id, t.term_key, t.ordinal, t.value_kind, t.text_value, t.int_value,
       t.amount_minor, t.amount_minor_hi, t.currency, t.per_unit, t.source_text,
       ti.kind AS i_kind, ti.value AS i_value, ti.gran AS i_gran, ti.zone AS i_zone, ti.source_text AS i_text,
       tv.from_kind, tv.from_value, tv.to_kind, tv.to_value, tv.from_gran, tv.from_zone,
       CASE WHEN ti.kind = 'KNOWN' THEN b4_truth('KNOWN', ti.value, ti.gran, ti.zone, 'UNBOUNDED', NULL, NULL, NULL,
                                                  :eff_value, :eff_gran, :eff_zone) END AS at_or_after_instant
  FROM core_application_term t, kc
  LEFT JOIN core_instant ti ON ti.instant_id = t.instant_id
  LEFT JOIN core_interval tv ON tv.interval_id = t.interval_id
 WHERE t.receipt_id <= kc.kr
   AND NOT EXISTS (SELECT 1 FROM core_application_term x
                    WHERE x.supersedes_term_id = t.term_id AND x.receipt_id <= kc.kr)
 ORDER BY t.application_id, t.term_key, t.ordinal, t.term_id
""")

ACTIONS = panel("actions")(f"""
WITH {KC},
head AS (
  SELECT s.* FROM core_action_item_state s, kc
   WHERE s.receipt_id <= kc.kr
     AND NOT EXISTS (SELECT 1 FROM core_action_item_state x
                      WHERE x.supersedes_state_id = s.state_id AND x.receipt_id <= kc.kr))
SELECT it.item_id, it.subject_kind, it.application_id, it.blocker_id, it.text, it.owner,
       h.state_id, h.status,
       d.kind AS due_kind, d.value AS due_value, d.gran AS due_gran, d.zone AS due_zone, d.source_text AS due_text,
       CASE WHEN d.kind = 'KNOWN' THEN b4_truth('KNOWN', d.value, d.gran, d.zone, 'UNBOUNDED', NULL, NULL, NULL,
                                                 :eff_value, :eff_gran, :eff_zone) END AS cut_at_or_after_due
  FROM core_action_item it, kc
  JOIN head h ON h.item_id = it.item_id
  JOIN core_instant d ON d.instant_id = it.due_instant_id
 WHERE it.receipt_id <= kc.kr
 ORDER BY it.item_id, h.state_id
""")

FEED = panel("feed")(f"""
WITH {KC},
items AS (
  SELECT 'NOTE' AS item_kind, n.note_id AS item_id, n.tag, n.title, n.body,
         NULL AS verdict_axis, NULL AS eclass_axis, n.event_instant_id AS instant_id, n.receipt_id
    FROM core_note n, kc
   WHERE n.receipt_id <= kc.kr
     AND NOT EXISTS (SELECT 1 FROM core_note x WHERE x.supersedes_note_id = n.note_id AND x.receipt_id <= kc.kr)
  UNION ALL
  SELECT 'APPLICATION_STATE', s.state_id, 'applications',
         ap.employer_label || ': ' || s.status,
         s.basis || CASE WHEN s.actor_state = 'STATED' THEN ' (by ' || s.actor || ')' ELSE '' END,
         NULL, NULL, s.event_instant_id, s.receipt_id
    FROM core_application_state s JOIN core_application ap ON ap.application_id = s.application_id, kc
   WHERE s.receipt_id <= kc.kr
  UNION ALL
  SELECT 'BLOCKER_STATE', s.state_id,
         CASE b.program WHEN 'RESEARCH_CHAIN' THEN 'research-chain' WHEN 'UNSILO_BUILD' THEN 'build' ELSE 'forensics' END,
         b.program || ' ' || b.code || ': ' || s.state,
         b.title || '. ' || s.basis, NULL, NULL, s.asserted_instant_id, s.receipt_id
    FROM core_blocker_state s JOIN core_blocker b ON b.blocker_id = s.blocker_id, kc
   WHERE s.receipt_id <= kc.kr
  UNION ALL
  SELECT 'VERDICT', v.verdict_id,
         CASE WHEN v.audit_run_id IS NULL THEN 'forensics' ELSE 'audits' END,
         c.subject_label || ': ' || c.claim_text, v.rationale,
         CASE WHEN c.artifact_state = 'UNJOINED' THEN 'UNRESOLVED' ELSE v.status END,
         coalesce((SELECT CASE e.state WHEN 'ABSTENTION' THEN 'ABSTENTION(' || e.abstention_reason || ')'
                                       ELSE e.class || CASE WHEN e.weak = 1 THEN '+WEAK' ELSE '' END END
                     FROM core_claim_eclass e
                    WHERE e.claim_id = c.claim_id AND e.receipt_id <= kc.kr
                      AND NOT EXISTS (SELECT 1 FROM core_claim_eclass y
                                       WHERE y.supersedes_eclass_id = e.eclass_id AND y.receipt_id <= kc.kr)
                    ORDER BY e.eclass_id DESC LIMIT 1), 'NOT_RECORDED'),
         v.decided_at_instant_id, v.receipt_id
    FROM core_verdict v JOIN core_claim c ON c.claim_id = v.claim_id, kc
   WHERE v.receipt_id <= kc.kr
  UNION ALL
  SELECT 'ACTION_STATE', s.state_id,
         CASE WHEN it.subject_kind = 'APPLICATION' THEN 'applications'
              ELSE (SELECT CASE b.program WHEN 'RESEARCH_CHAIN' THEN 'research-chain' WHEN 'UNSILO_BUILD' THEN 'build'
                                          ELSE 'forensics' END FROM core_blocker b WHERE b.blocker_id = it.blocker_id) END,
         'Action ' || s.status || ': ' || it.text, s.note, NULL, NULL, s.event_instant_id, s.receipt_id
    FROM core_action_item_state s JOIN core_action_item it ON it.item_id = s.item_id, kc
   WHERE s.receipt_id <= kc.kr
  UNION ALL
  SELECT 'AUDIT_RUN', r.audit_run_id, 'audits', 'Audit run: ' || r.scope,
         (SELECT group_concat(count_key || ' ' || reported_value, ', ')
            FROM (SELECT count_key, reported_value FROM core_audit_count WHERE audit_run_id = r.audit_run_id ORDER BY count_id)),
         NULL, NULL, r.run_instant_id, r.receipt_id
    FROM core_audit_run r, kc
   WHERE r.receipt_id <= kc.kr
)
SELECT it.item_kind, it.item_id, it.tag, it.title, it.body, it.verdict_axis, it.eclass_axis,
       i.kind AS t_kind, i.value AS t_value, i.gran AS t_gran, i.zone AS t_zone, i.source_text AS t_text,
       r.recorded_at, it.receipt_id
  FROM items it
  JOIN core_instant i ON i.instant_id = it.instant_id
  JOIN meta_receipt r ON r.receipt_id = it.receipt_id
 ORDER BY instant_sort(i.kind, i.value, i.gran, i.zone) DESC, it.receipt_id DESC
""")

AUDIT_CHECK = panel("audit_check")("""
SELECT audit_run_id, count_key, reported_value, findings_held, source_text
  FROM v_audit_count_check
 ORDER BY audit_run_id, count_key
""")

CONTRACT_CHECK = panel("contract_check")("""
SELECT contract_id, gate_status, docket_state, source_ref,
       CASE WHEN docket_state IS NULL THEN 'NO_DOCKET_RECORD'
            WHEN docket_state = gate_status THEN 'AGREE' ELSE 'MISMATCH' END AS agreement
  FROM v_contract_vs_blocker
 ORDER BY CASE WHEN contract_id GLOB 'B[0-9]*' THEN CAST(substr(contract_id, 2) AS INTEGER) ELSE 99 END, contract_id
""")

LEDGER = panel("ledger")("""
SELECT count(*) AS receipts, max(receipt_id) AS head_id,
       (SELECT receipt_sha256 FROM meta_receipt ORDER BY receipt_id DESC LIMIT 1) AS head_sha256,
       (SELECT recorded_at FROM meta_receipt ORDER BY receipt_id DESC LIMIT 1) AS head_recorded_at
  FROM meta_receipt
""")


def run(conn, name, params):
    cur = conn.execute(PANELS[name], params)
    try:
        cols = [d[0] for d in cur.getdescription()]
    except Exception:
        return []
    return [dict(zip(cols, r)) for r in cur]
