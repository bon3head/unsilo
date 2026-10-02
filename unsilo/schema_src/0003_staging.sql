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
