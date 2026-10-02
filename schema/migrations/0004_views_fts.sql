-- UnSilo dashboard schema, migration 0004: read-path views and the disposable
-- FTS5 projection.
-- Status: PROPOSED DESIGN ARTIFACT. Not approved. Build authorization: NONE.
--
-- Every view is evaluated against declared cuts in meta_cut (cut_id column on
-- every row). No view reads the clock. Knowledge-cut eligibility: a core row
-- is visible at cut c iff its receipt.recorded_at <= c.knowledge_cut.

------------------------------------------------------------------------------
-- Three-valued point membership: is the effective cut T inside [from, to)?
------------------------------------------------------------------------------
-- Universal entailment over admissible completions (frozen B4 principle):
-- TRUE iff every completion puts T in [from,to), FALSE iff none does,
-- else UNKNOWN. Completions: UNBOUNDED -> -inf / +inf; UNKNOWN -> any finite
-- value consistent with from < to. Derivation and the full 9-case table are in
-- README 3.3. This is NOT Kleene logic: case K(T) / UNKNOWN is TRUE, where a
-- Kleene AND of (TRUE, UNKNOWN) would say UNKNOWN; and it is NOT the S3
-- blanket rule: UNBOUNDED / K(t) with T < t is TRUE, not UNKNOWN.
-- Granularity: endpoints whose granularity or zone differ from the cut are
-- not lifted across granularity here; such rows return UNKNOWN with reason
-- GRANULARITY_NOT_LIFTED (conservative, OPEN U-DASH-03).
CREATE VIEW v_interval_membership AS
SELECT
  i.interval_id,
  c.cut_id,
  CASE
    WHEN (i.from_kind = 'KNOWN' AND (i.from_gran <> c.eff_gran OR i.from_zone <> c.eff_zone))
      OR (i.to_kind   = 'KNOWN' AND (i.to_gran   <> c.eff_gran OR i.to_zone   <> c.eff_zone))
      THEN 'UNKNOWN'
    WHEN i.from_kind = 'KNOWN' AND i.from_value > c.eff_value THEN 'FALSE'
    WHEN i.to_kind   = 'KNOWN' AND c.eff_value >= i.to_value  THEN 'FALSE'
    WHEN i.from_kind IN ('KNOWN', 'UNBOUNDED') AND i.to_kind IN ('KNOWN', 'UNBOUNDED') THEN 'TRUE'
    WHEN i.from_kind = 'KNOWN' AND i.from_value = c.eff_value AND i.to_kind = 'UNKNOWN' THEN 'TRUE'
    ELSE 'UNKNOWN'
  END AS truth,
  CASE
    WHEN (i.from_kind = 'KNOWN' AND (i.from_gran <> c.eff_gran OR i.from_zone <> c.eff_zone))
      OR (i.to_kind   = 'KNOWN' AND (i.to_gran   <> c.eff_gran OR i.to_zone   <> c.eff_zone))
      THEN 'GRANULARITY_NOT_LIFTED'
    WHEN i.from_kind = 'KNOWN' AND i.from_value > c.eff_value THEN 'CUT_BEFORE_KNOWN_FROM'
    WHEN i.to_kind   = 'KNOWN' AND c.eff_value >= i.to_value  THEN 'CUT_AT_OR_AFTER_KNOWN_TO'
    WHEN i.from_kind IN ('KNOWN', 'UNBOUNDED') AND i.to_kind IN ('KNOWN', 'UNBOUNDED') THEN 'ALL_COMPLETIONS_CONTAIN_CUT'
    WHEN i.from_kind = 'KNOWN' AND i.from_value = c.eff_value AND i.to_kind = 'UNKNOWN' THEN 'CUT_EQUALS_FROM_AND_TO_EXCEEDS_FROM'
    WHEN i.from_kind = 'UNKNOWN' THEN 'FROM_UNKNOWN_COMPLETIONS_SPLIT'
    ELSE 'TO_UNKNOWN_COMPLETIONS_SPLIT'
  END AS reason
FROM core_interval i
CROSS JOIN meta_cut c;

------------------------------------------------------------------------------
-- Knowledge-time visibility helper
------------------------------------------------------------------------------
CREATE VIEW v_receipt_visible AS
SELECT r.receipt_id, r.recorded_at, c.cut_id
FROM meta_receipt r
JOIN meta_cut c ON r.recorded_at <= c.knowledge_cut;

------------------------------------------------------------------------------
-- Blockers: state heads at a cut. A head is a state row visible at the cut
-- that no other visible row supersedes. Two heads for one blocker = conflict;
-- both rows are shown, never a silent pick.
------------------------------------------------------------------------------
CREATE VIEW v_blocker_state_head AS
SELECT
  vis.cut_id,
  b.blocker_id, b.program, b.code, b.title,
  s.state_id, s.state, v.is_terminal,
  s.falsifier_state, s.falsifier, s.owner_state, s.owner, s.basis,
  m.truth AS in_effect_at_cut, m.reason AS in_effect_reason,
  (SELECT count(*)
     FROM core_blocker_state s2
     JOIN v_receipt_visible vis2 ON vis2.receipt_id = s2.receipt_id AND vis2.cut_id = vis.cut_id
    WHERE s2.blocker_id = s.blocker_id
      AND NOT EXISTS (SELECT 1 FROM core_blocker_state s3
                        JOIN v_receipt_visible vis3 ON vis3.receipt_id = s3.receipt_id AND vis3.cut_id = vis.cut_id
                       WHERE s3.supersedes_state_id = s2.state_id)) AS head_count
FROM core_blocker_state s
JOIN v_receipt_visible vis ON vis.receipt_id = s.receipt_id
JOIN core_blocker b ON b.blocker_id = s.blocker_id
JOIN core_blocker_state_vocab v ON v.state = s.state
JOIN v_interval_membership m ON m.interval_id = s.valid_interval_id AND m.cut_id = vis.cut_id
WHERE NOT EXISTS (SELECT 1 FROM core_blocker_state s4
                    JOIN v_receipt_visible vis4 ON vis4.receipt_id = s4.receipt_id AND vis4.cut_id = vis.cut_id
                   WHERE s4.supersedes_state_id = s.state_id);

-- The strip (rendered top AND bottom): non-terminal heads. A head whose
-- in_effect_at_cut is UNKNOWN stays on the strip in an explicit UNKNOWN band;
-- FALSE heads are dropped only because their state is not in effect at the cut.
CREATE VIEW v_blocker_strip AS
SELECT *
FROM v_blocker_state_head
WHERE is_terminal = 0 AND in_effect_at_cut IN ('TRUE', 'UNKNOWN')
ORDER BY cut_id, program, code, state_id;

------------------------------------------------------------------------------
-- Claims: both axes at a cut, never conflated.
------------------------------------------------------------------------------
CREATE VIEW v_verdict_head AS
SELECT vis.cut_id, vd.*
FROM core_verdict vd
JOIN v_receipt_visible vis ON vis.receipt_id = vd.receipt_id
WHERE NOT EXISTS (SELECT 1 FROM core_verdict v2
                    JOIN v_receipt_visible vis2 ON vis2.receipt_id = v2.receipt_id AND vis2.cut_id = vis.cut_id
                   WHERE v2.supersedes_verdict_id = vd.verdict_id);

CREATE VIEW v_eclass_head AS
SELECT vis.cut_id, e.*
FROM core_claim_eclass e
JOIN v_receipt_visible vis ON vis.receipt_id = e.receipt_id
WHERE NOT EXISTS (SELECT 1 FROM core_claim_eclass e2
                    JOIN v_receipt_visible vis2 ON vis2.receipt_id = e2.receipt_id AND vis2.cut_id = vis.cut_id
                   WHERE e2.supersedes_eclass_id = e.eclass_id);

-- verdict_axis: UNRESOLVED by construction for UNJOINED claims; NO_VERDICT_ROW
-- when nothing is recorded (shown, not hidden). eclass_axis: the head state,
-- or NOT_RECORDED. verdict_head_count > 1 means conflicting verdict heads.
CREATE VIEW v_claim_effective AS
SELECT
  vis.cut_id,
  cl.claim_id, cl.subject_kind, cl.company_id, cl.claim_text, cl.source_quote,
  cl.artifact_state,
  CASE
    WHEN cl.artifact_state = 'UNJOINED' THEN 'UNRESOLVED'
    WHEN vh.verdict_id IS NULL THEN 'NO_VERDICT_ROW'
    ELSE vh.status
  END AS verdict_axis,
  CASE
    WHEN cl.artifact_state = 'UNJOINED' THEN 'NO_ARTIFACT'
    WHEN vh.verdict_id IS NULL THEN 'NO_VERDICT_ROW'
    ELSE 'VERDICT_ROW'
  END AS verdict_basis,
  vh.verdict_id,
  (SELECT count(*) FROM v_verdict_head x WHERE x.cut_id = vis.cut_id AND x.claim_id = cl.claim_id) AS verdict_head_count,
  CASE
    WHEN eh.eclass_id IS NULL THEN 'NOT_RECORDED'
    WHEN eh.state = 'ABSTENTION' THEN 'ABSTENTION(' || eh.abstention_reason || ')'
    ELSE eh.class || CASE WHEN eh.weak = 1 THEN '+WEAK' ELSE '' END
  END AS eclass_axis
FROM core_claim cl
JOIN v_receipt_visible vis ON vis.receipt_id = cl.receipt_id
LEFT JOIN v_verdict_head vh ON vh.claim_id = cl.claim_id AND vh.cut_id = vis.cut_id
LEFT JOIN v_eclass_head eh ON eh.claim_id = cl.claim_id AND eh.cut_id = vis.cut_id;

------------------------------------------------------------------------------
-- Applications at a cut
------------------------------------------------------------------------------
CREATE VIEW v_application_state_head AS
SELECT
  vis.cut_id,
  a.application_id, a.company_id, a.role_state, a.role, a.platform_state, a.platform,
  a.req_state, a.req_ref, a.location_state, a.location,
  s.state_id, s.status, s.submitted_by,
  ei.kind AS event_kind, ei.value AS event_value, ei.gran AS event_gran, ei.zone AS event_zone,
  ei.source_text AS event_source_text,
  m.truth AS in_effect_at_cut, m.reason AS in_effect_reason
FROM core_application_state s
JOIN v_receipt_visible vis ON vis.receipt_id = s.receipt_id
JOIN core_application a ON a.application_id = s.application_id
JOIN core_instant ei ON ei.instant_id = s.event_instant_id
JOIN v_interval_membership m ON m.interval_id = s.valid_interval_id AND m.cut_id = vis.cut_id
WHERE NOT EXISTS (SELECT 1 FROM core_application_state s2
                    JOIN v_receipt_visible vis2 ON vis2.receipt_id = s2.receipt_id AND vis2.cut_id = vis.cut_id
                   WHERE s2.supersedes_state_id = s.state_id);

------------------------------------------------------------------------------
-- Absence as signal: loudest unmet expectations first. Ordering is
-- categorical (basis rank), never a probability.
------------------------------------------------------------------------------
CREATE VIEW v_expectation_head AS
SELECT vis.cut_id, es.*
FROM core_expectation_state es
JOIN v_receipt_visible vis ON vis.receipt_id = es.receipt_id
WHERE NOT EXISTS (SELECT 1 FROM core_expectation_state e2
                    JOIN v_receipt_visible vis2 ON vis2.receipt_id = e2.receipt_id AND vis2.cut_id = vis.cut_id
                   WHERE e2.supersedes_state_id = es.state_id);

CREATE VIEW v_expectation_loudest AS
SELECT
  h.cut_id, e.expectation_id, e.subject_kind, e.expected_artifact_type,
  e.basis, e.basis_note, e.checked_scope, h.status, h.note,
  CASE e.basis WHEN 'MANDATED' THEN 1 WHEN 'STATED' THEN 2 WHEN 'ROUTINE' THEN 3 ELSE 4 END AS basis_rank,
  'not observed in ' || e.checked_scope || '; absence from this dataset is not evidence of absence in the world' AS caveat
FROM v_expectation_head h
JOIN core_expectation e ON e.expectation_id = h.expectation_id
WHERE h.status IN ('NOT_OBSERVED', 'LATE')
ORDER BY h.cut_id, basis_rank, e.expectation_id;

------------------------------------------------------------------------------
-- Audit counts: reported aggregate vs rows held. A gap is surfaced, not hidden.
------------------------------------------------------------------------------
CREATE VIEW v_audit_count_check AS
SELECT
  ac.audit_run_id, ac.count_key, ac.reported_value,
  (SELECT count(*) FROM core_audit_finding f
     JOIN core_verdict v ON v.verdict_id = f.verdict_id
    WHERE f.audit_run_id = ac.audit_run_id AND v.status = ac.count_key) AS rows_held,
  ac.source_text
FROM core_audit_count ac;

------------------------------------------------------------------------------
-- feed_item: the denormalized read path. A VIEW, never a table; its output is
-- never stored (the FTS projection below is a disposable search index, not
-- the feed). Deterministic order: (cut, time kind, time value, item_kind,
-- item_id). UNKNOWN-time items sort after KNOWN ones, explicitly.
-- Cross-granularity ordering (DAY vs SECOND values) is a display order only;
-- it is never a temporal relation (README 4.3).
------------------------------------------------------------------------------
CREATE VIEW feed_item AS
SELECT * FROM (
  SELECT vis.cut_id, 'NOTE' AS item_kind, n.note_id AS item_id, n.tag,
         n.title, n.body, 'NOT_APPLICABLE' AS verdict_axis, 'NOT_APPLICABLE' AS eclass_axis,
         i.kind AS time_kind, i.value AS time_value, i.gran AS time_gran, i.zone AS time_zone, i.source_text AS time_source_text
    FROM core_note n
    JOIN v_receipt_visible vis ON vis.receipt_id = n.receipt_id
    JOIN core_instant i ON i.instant_id = n.event_instant_id
   WHERE NOT EXISTS (SELECT 1 FROM core_note n2
                       JOIN v_receipt_visible vis2 ON vis2.receipt_id = n2.receipt_id AND vis2.cut_id = vis.cut_id
                      WHERE n2.supersedes_note_id = n.note_id)
  UNION ALL
  SELECT vis.cut_id, 'VERDICT', vd.verdict_id,
         CASE WHEN vd.audit_run_id IS NULL THEN 'forensics' ELSE 'audits' END,
         cl.claim_text, vd.rationale, vd.status, ce.eclass_axis,
         i.kind, i.value, i.gran, i.zone, i.source_text
    FROM core_verdict vd
    JOIN v_receipt_visible vis ON vis.receipt_id = vd.receipt_id
    JOIN core_claim cl ON cl.claim_id = vd.claim_id
    JOIN v_claim_effective ce ON ce.claim_id = cl.claim_id AND ce.cut_id = vis.cut_id
    JOIN core_instant i ON i.instant_id = vd.decided_at_instant_id
  UNION ALL
  SELECT vis.cut_id, 'APPLICATION_STATE', s.state_id, 'applications',
         co.company_key || ' ' || CASE WHEN a.role_state = 'STATED' THEN a.role ELSE 'role UNKNOWN' END, s.status || CASE WHEN a.req_state = 'STATED' THEN ' req ' || a.req_ref ELSE '' END,
         'NOT_APPLICABLE', 'NOT_APPLICABLE',
         i.kind, i.value, i.gran, i.zone, i.source_text
    FROM core_application_state s
    JOIN v_receipt_visible vis ON vis.receipt_id = s.receipt_id
    JOIN core_application a ON a.application_id = s.application_id
    JOIN core_company co ON co.company_id = a.company_id
    JOIN core_instant i ON i.instant_id = s.event_instant_id
  UNION ALL
  SELECT vis.cut_id, 'AUDIT_RUN', ar.audit_run_id, 'audits',
         ar.scope, ar.worker_set, 'NOT_APPLICABLE', 'NOT_APPLICABLE',
         i.kind, i.value, i.gran, i.zone, i.source_text
    FROM core_audit_run ar
    JOIN v_receipt_visible vis ON vis.receipt_id = ar.receipt_id
    JOIN core_instant i ON i.instant_id = ar.run_instant_id
)
ORDER BY cut_id,
         CASE time_kind WHEN 'KNOWN' THEN 0 ELSE 1 END,
         time_value, item_kind, item_id;

------------------------------------------------------------------------------
-- FTS5: disposable, non-authoritative retrieval projection (S6). Rebuilt from
-- feed_item at the end of every promotion run (README 7.6), never on staging
-- writes. Destroying it destroys zero evidence. No classification, count,
-- verdict, or absence claim may depend on FTS hit/miss or rank.
-- FTS5 virtual tables cannot be STRICT; nothing canonical lives here.
------------------------------------------------------------------------------
CREATE VIRTUAL TABLE fts_feed USING fts5 (
  cut_id UNINDEXED,
  item_kind UNINDEXED,
  item_id UNINDEXED,
  title,
  body,
  tokenize = 'unicode61'
);
