-- UnSilo store, migration 0003: staging for packet imports (stg_*) and the
-- receipted promotion boundary. Kept only for packet imports (ruling).
-- Staging carries no authority: no panel reads stg_*. Staging rows go through
-- the same one write path (receipts), so replay rebuilds them too.
-- Personal fields never enter staging: the packet parser keeps an allowlist of
-- application-fact lines and records only the COUNT of lines it skipped.

CREATE TABLE stg_ingest_batch (
  batch_id       INTEGER PRIMARY KEY,
  format_tag     TEXT    NOT NULL CHECK (format_tag IN ('DUOLINGO_PACKET')),
  artifact_id    INTEGER NOT NULL REFERENCES core_artifact (artifact_id),
  parser_id      TEXT    NOT NULL CHECK (length(parser_id) > 0),
  parser_version INTEGER NOT NULL CHECK (parser_version >= 1),
  lines_total    INTEGER NOT NULL CHECK (lines_total >= 0),
  lines_kept     INTEGER NOT NULL CHECK (lines_kept >= 0 AND lines_kept <= lines_total),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  UNIQUE (format_tag, artifact_id, parser_id, parser_version)
) STRICT;

-- One kept source line, verbatim, with its 1-based line number.
CREATE TABLE stg_raw_row (
  raw_row_id     INTEGER PRIMARY KEY,
  batch_id       INTEGER NOT NULL REFERENCES stg_ingest_batch (batch_id),
  line_no        INTEGER NOT NULL CHECK (line_no >= 1),
  raw_text       TEXT    NOT NULL,
  raw_sha256     TEXT    NOT NULL CHECK (length(raw_sha256) = 64 AND raw_sha256 NOT GLOB '*[^0-9a-f]*'),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  UNIQUE (batch_id, line_no)
) STRICT;

-- PARSED / PARTIAL / MALFORMED / NOT_APPLICABLE never collapse; a missing field
-- is listed, never defaulted.
CREATE TABLE stg_candidate (
  candidate_id         INTEGER PRIMARY KEY,
  raw_row_id           INTEGER NOT NULL REFERENCES stg_raw_row (raw_row_id),
  candidate_kind       TEXT    NOT NULL CHECK (candidate_kind IN ('APPLICATION_TERM', 'APPLICATION_STATE', 'ACTION_ITEM', 'NOTE', 'CLAIM_VERDICT')),
  parse_state          TEXT    NOT NULL CHECK (parse_state IN ('PARSED', 'PARTIAL', 'MALFORMED', 'NOT_APPLICABLE')),
  payload_json         TEXT    NOT NULL CHECK (json_valid(payload_json) AND json_type(payload_json) = 'object'),
  missing_fields_json  TEXT    NOT NULL CHECK (json_valid(missing_fields_json) AND json_type(missing_fields_json) = 'array'),
  receipt_id           INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((parse_state = 'PARTIAL') = (json_array_length(missing_fields_json) > 0)),
  CHECK (parse_state <> 'MALFORMED' OR payload_json = '{}')
) STRICT;

CREATE TABLE stg_promotion_decision (
  decision_id      INTEGER PRIMARY KEY,
  candidate_id     INTEGER NOT NULL REFERENCES stg_candidate (candidate_id),
  rule_id          TEXT    NOT NULL CHECK (length(rule_id) > 0),
  rule_version     INTEGER NOT NULL CHECK (rule_version >= 1),
  decision         TEXT    NOT NULL CHECK (decision IN ('PROMOTE', 'HOLD', 'REJECT')),
  reason           TEXT    NOT NULL CHECK (length(reason) > 0),
  receipt_id       INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  UNIQUE (candidate_id, rule_id, rule_version)
) STRICT;
CREATE TRIGGER stg_promotion_decision_needs_parse BEFORE INSERT ON stg_promotion_decision
WHEN NEW.decision = 'PROMOTE'
 AND (SELECT parse_state FROM stg_candidate WHERE candidate_id = NEW.candidate_id) NOT IN ('PARSED', 'PARTIAL')
BEGIN SELECT RAISE(ABORT, 'stg_promotion_decision: MALFORMED or NOT_APPLICABLE candidates cannot be promoted'); END;

CREATE TABLE core_promotion_run (
  promotion_run_id INTEGER PRIMARY KEY,
  batch_id         INTEGER NOT NULL REFERENCES stg_ingest_batch (batch_id),
  rule_set_version INTEGER NOT NULL CHECK (rule_set_version >= 1),
  receipt_id       INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

-- Each promoted core row links back to its decision. target_receipt_id is the
-- receipt of the promoted row; that receipt must carry this run's id.
CREATE TABLE core_promotion_link (
  link_id           INTEGER PRIMARY KEY,
  promotion_run_id  INTEGER NOT NULL REFERENCES core_promotion_run (promotion_run_id),
  decision_id       INTEGER NOT NULL REFERENCES stg_promotion_decision (decision_id),
  target_receipt_id INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  receipt_id        INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK (target_receipt_id <> receipt_id)
) STRICT;
CREATE TRIGGER core_promotion_link_needs_promote BEFORE INSERT ON core_promotion_link
WHEN (SELECT decision FROM stg_promotion_decision WHERE decision_id = NEW.decision_id) IS NOT 'PROMOTE'
BEGIN SELECT RAISE(ABORT, 'core_promotion_link: decision is not PROMOTE'); END;
CREATE TRIGGER core_promotion_link_same_run BEFORE INSERT ON core_promotion_link
WHEN (SELECT promotion_run_id FROM meta_receipt WHERE receipt_id = NEW.target_receipt_id) IS NOT NEW.promotion_run_id
BEGIN SELECT RAISE(ABORT, 'core_promotion_link: target row was not written by this promotion run'); END;

-- ---------------------------------------------------------------------------
-- GENERATED by tools/gen_migrations.py: receipt-image equality + append-only.
-- Do not edit below this line; edit unsilo/schema_src and regenerate.
-- ---------------------------------------------------------------------------
CREATE TRIGGER core_promotion_link_receipt_image BEFORE INSERT ON core_promotion_link
WHEN NOT EXISTS (SELECT 1 FROM meta_receipt r
  WHERE r.receipt_id = NEW.receipt_id AND r.table_name = 'core_promotion_link' AND r.row_pk = NEW.link_id AND r.op = 'INSERT'
    AND (SELECT count(*) FROM json_each(r.after_image_json)) = 5
    AND NOT EXISTS (SELECT 1 FROM json_each(r.after_image_json) j WHERE j.key NOT IN ('link_id', 'promotion_run_id', 'decision_id', 'target_receipt_id', 'receipt_id'))
    AND json_extract(r.after_image_json, '$.link_id') IS NEW.link_id
    AND json_extract(r.after_image_json, '$.promotion_run_id') IS NEW.promotion_run_id
    AND json_extract(r.after_image_json, '$.decision_id') IS NEW.decision_id
    AND json_extract(r.after_image_json, '$.target_receipt_id') IS NEW.target_receipt_id
    AND json_extract(r.after_image_json, '$.receipt_id') IS NEW.receipt_id)
BEGIN SELECT RAISE(ABORT, 'core_promotion_link: row must equal its receipt after-image'); END;
CREATE TRIGGER core_promotion_link_no_update BEFORE UPDATE ON core_promotion_link
BEGIN SELECT RAISE(ABORT, 'core_promotion_link is append-only'); END;
CREATE TRIGGER core_promotion_link_no_delete BEFORE DELETE ON core_promotion_link
BEGIN SELECT RAISE(ABORT, 'core_promotion_link is append-only'); END;
CREATE TRIGGER core_promotion_run_receipt_image BEFORE INSERT ON core_promotion_run
WHEN NOT EXISTS (SELECT 1 FROM meta_receipt r
  WHERE r.receipt_id = NEW.receipt_id AND r.table_name = 'core_promotion_run' AND r.row_pk = NEW.promotion_run_id AND r.op = 'INSERT'
    AND (SELECT count(*) FROM json_each(r.after_image_json)) = 4
    AND NOT EXISTS (SELECT 1 FROM json_each(r.after_image_json) j WHERE j.key NOT IN ('promotion_run_id', 'batch_id', 'rule_set_version', 'receipt_id'))
    AND json_extract(r.after_image_json, '$.promotion_run_id') IS NEW.promotion_run_id
    AND json_extract(r.after_image_json, '$.batch_id') IS NEW.batch_id
    AND json_extract(r.after_image_json, '$.rule_set_version') IS NEW.rule_set_version
    AND json_extract(r.after_image_json, '$.receipt_id') IS NEW.receipt_id)
BEGIN SELECT RAISE(ABORT, 'core_promotion_run: row must equal its receipt after-image'); END;
CREATE TRIGGER core_promotion_run_no_update BEFORE UPDATE ON core_promotion_run
BEGIN SELECT RAISE(ABORT, 'core_promotion_run is append-only'); END;
CREATE TRIGGER core_promotion_run_no_delete BEFORE DELETE ON core_promotion_run
BEGIN SELECT RAISE(ABORT, 'core_promotion_run is append-only'); END;
CREATE TRIGGER stg_candidate_receipt_image BEFORE INSERT ON stg_candidate
WHEN NOT EXISTS (SELECT 1 FROM meta_receipt r
  WHERE r.receipt_id = NEW.receipt_id AND r.table_name = 'stg_candidate' AND r.row_pk = NEW.candidate_id AND r.op = 'INSERT'
    AND (SELECT count(*) FROM json_each(r.after_image_json)) = 7
    AND NOT EXISTS (SELECT 1 FROM json_each(r.after_image_json) j WHERE j.key NOT IN ('candidate_id', 'raw_row_id', 'candidate_kind', 'parse_state', 'payload_json', 'missing_fields_json', 'receipt_id'))
    AND json_extract(r.after_image_json, '$.candidate_id') IS NEW.candidate_id
    AND json_extract(r.after_image_json, '$.raw_row_id') IS NEW.raw_row_id
    AND json_extract(r.after_image_json, '$.candidate_kind') IS NEW.candidate_kind
    AND json_extract(r.after_image_json, '$.parse_state') IS NEW.parse_state
    AND json_extract(r.after_image_json, '$.payload_json') IS NEW.payload_json
    AND json_extract(r.after_image_json, '$.missing_fields_json') IS NEW.missing_fields_json
    AND json_extract(r.after_image_json, '$.receipt_id') IS NEW.receipt_id)
BEGIN SELECT RAISE(ABORT, 'stg_candidate: row must equal its receipt after-image'); END;
CREATE TRIGGER stg_candidate_no_update BEFORE UPDATE ON stg_candidate
BEGIN SELECT RAISE(ABORT, 'stg_candidate is append-only'); END;
CREATE TRIGGER stg_candidate_no_delete BEFORE DELETE ON stg_candidate
BEGIN SELECT RAISE(ABORT, 'stg_candidate is append-only'); END;
CREATE TRIGGER stg_ingest_batch_receipt_image BEFORE INSERT ON stg_ingest_batch
WHEN NOT EXISTS (SELECT 1 FROM meta_receipt r
  WHERE r.receipt_id = NEW.receipt_id AND r.table_name = 'stg_ingest_batch' AND r.row_pk = NEW.batch_id AND r.op = 'INSERT'
    AND (SELECT count(*) FROM json_each(r.after_image_json)) = 8
    AND NOT EXISTS (SELECT 1 FROM json_each(r.after_image_json) j WHERE j.key NOT IN ('batch_id', 'format_tag', 'artifact_id', 'parser_id', 'parser_version', 'lines_total', 'lines_kept', 'receipt_id'))
    AND json_extract(r.after_image_json, '$.batch_id') IS NEW.batch_id
    AND json_extract(r.after_image_json, '$.format_tag') IS NEW.format_tag
    AND json_extract(r.after_image_json, '$.artifact_id') IS NEW.artifact_id
    AND json_extract(r.after_image_json, '$.parser_id') IS NEW.parser_id
    AND json_extract(r.after_image_json, '$.parser_version') IS NEW.parser_version
    AND json_extract(r.after_image_json, '$.lines_total') IS NEW.lines_total
    AND json_extract(r.after_image_json, '$.lines_kept') IS NEW.lines_kept
    AND json_extract(r.after_image_json, '$.receipt_id') IS NEW.receipt_id)
BEGIN SELECT RAISE(ABORT, 'stg_ingest_batch: row must equal its receipt after-image'); END;
CREATE TRIGGER stg_ingest_batch_no_update BEFORE UPDATE ON stg_ingest_batch
BEGIN SELECT RAISE(ABORT, 'stg_ingest_batch is append-only'); END;
CREATE TRIGGER stg_ingest_batch_no_delete BEFORE DELETE ON stg_ingest_batch
BEGIN SELECT RAISE(ABORT, 'stg_ingest_batch is append-only'); END;
CREATE TRIGGER stg_promotion_decision_receipt_image BEFORE INSERT ON stg_promotion_decision
WHEN NOT EXISTS (SELECT 1 FROM meta_receipt r
  WHERE r.receipt_id = NEW.receipt_id AND r.table_name = 'stg_promotion_decision' AND r.row_pk = NEW.decision_id AND r.op = 'INSERT'
    AND (SELECT count(*) FROM json_each(r.after_image_json)) = 7
    AND NOT EXISTS (SELECT 1 FROM json_each(r.after_image_json) j WHERE j.key NOT IN ('decision_id', 'candidate_id', 'rule_id', 'rule_version', 'decision', 'reason', 'receipt_id'))
    AND json_extract(r.after_image_json, '$.decision_id') IS NEW.decision_id
    AND json_extract(r.after_image_json, '$.candidate_id') IS NEW.candidate_id
    AND json_extract(r.after_image_json, '$.rule_id') IS NEW.rule_id
    AND json_extract(r.after_image_json, '$.rule_version') IS NEW.rule_version
    AND json_extract(r.after_image_json, '$.decision') IS NEW.decision
    AND json_extract(r.after_image_json, '$.reason') IS NEW.reason
    AND json_extract(r.after_image_json, '$.receipt_id') IS NEW.receipt_id)
BEGIN SELECT RAISE(ABORT, 'stg_promotion_decision: row must equal its receipt after-image'); END;
CREATE TRIGGER stg_promotion_decision_no_update BEFORE UPDATE ON stg_promotion_decision
BEGIN SELECT RAISE(ABORT, 'stg_promotion_decision is append-only'); END;
CREATE TRIGGER stg_promotion_decision_no_delete BEFORE DELETE ON stg_promotion_decision
BEGIN SELECT RAISE(ABORT, 'stg_promotion_decision is append-only'); END;
CREATE TRIGGER stg_raw_row_receipt_image BEFORE INSERT ON stg_raw_row
WHEN NOT EXISTS (SELECT 1 FROM meta_receipt r
  WHERE r.receipt_id = NEW.receipt_id AND r.table_name = 'stg_raw_row' AND r.row_pk = NEW.raw_row_id AND r.op = 'INSERT'
    AND (SELECT count(*) FROM json_each(r.after_image_json)) = 6
    AND NOT EXISTS (SELECT 1 FROM json_each(r.after_image_json) j WHERE j.key NOT IN ('raw_row_id', 'batch_id', 'line_no', 'raw_text', 'raw_sha256', 'receipt_id'))
    AND json_extract(r.after_image_json, '$.raw_row_id') IS NEW.raw_row_id
    AND json_extract(r.after_image_json, '$.batch_id') IS NEW.batch_id
    AND json_extract(r.after_image_json, '$.line_no') IS NEW.line_no
    AND json_extract(r.after_image_json, '$.raw_text') IS NEW.raw_text
    AND json_extract(r.after_image_json, '$.raw_sha256') IS NEW.raw_sha256
    AND json_extract(r.after_image_json, '$.receipt_id') IS NEW.receipt_id)
BEGIN SELECT RAISE(ABORT, 'stg_raw_row: row must equal its receipt after-image'); END;
CREATE TRIGGER stg_raw_row_no_update BEFORE UPDATE ON stg_raw_row
BEGIN SELECT RAISE(ABORT, 'stg_raw_row is append-only'); END;
CREATE TRIGGER stg_raw_row_no_delete BEFORE DELETE ON stg_raw_row
BEGIN SELECT RAISE(ABORT, 'stg_raw_row is append-only'); END;
