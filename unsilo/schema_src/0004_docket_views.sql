-- UnSilo store, migration 0004: Docket read views that need no cut parameter.
-- Cut-dependent panels are parameterized SQL in unsilo/docket/queries.py; each
-- panel prints its SQL and bound cut (S8, R16: every panel states its ORDER BY).

-- Same-granularity B4 point membership in pure SQL over declared cuts
-- (R12/DL-2). Position domain only; any KNOWN endpoint whose granularity or zone
-- differs from the cut is GRANULARITY_NOT_LIFTED here and is decided by the
-- application evaluator (b4_truth). experiments/temporal_agreement.py proves the
-- two agree wherever this view decides.
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

-- Audit counts: reported aggregate vs finding rows held. A gap is surfaced.
CREATE VIEW v_audit_count_check AS
SELECT
  ac.audit_run_id, ac.count_key, ac.reported_value,
  (SELECT count(*) FROM core_audit_finding f
    WHERE f.audit_run_id = ac.audit_run_id AND f.reported_status = ac.count_key) AS findings_held,
  ac.source_text
FROM core_audit_count ac;

-- Operator record vs migration-governed contract gate. A mismatch is surfaced
-- on the dashboard; neither side silently wins.
CREATE VIEW v_contract_vs_blocker AS
SELECT c.contract_id, c.status AS gate_status, c.source_ref,
       (SELECT s.state FROM core_blocker b JOIN core_blocker_state s ON s.blocker_id = b.blocker_id
         WHERE b.program = 'RESEARCH_CHAIN' AND b.code = c.contract_id
           AND NOT EXISTS (SELECT 1 FROM core_blocker_state s2 WHERE s2.supersedes_state_id = s.state_id)
         ORDER BY s.state_id DESC LIMIT 1) AS docket_state
FROM v_contract_head c;
