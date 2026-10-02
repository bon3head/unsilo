-- UnSilo dashboard schema, migration 0002: staging namespace (stg_*).
-- Status: PROPOSED DESIGN ARTIFACT. Not approved. Build authorization: NONE.
--
-- Staging holds raw, tentative, partial data with source-file provenance.
-- Staging rows carry no authority: no view, panel, or FTS projection reads
-- stg_* tables. Nothing leaves staging except through a receipted promotion
-- run (core_promotion_run in 0003). Staging is append-only too: a re-ingest of
-- a changed file is a new batch, never an edit of an old one.
--
-- The exact on-disk format of the Duolingo forensic packet is NOT in the pack
-- (OPEN U-DASH-07). This shape therefore stores every source row VERBATIM and
-- records parsing as a separate, versioned step, so the real format can land
-- without a parallel schema.

-- One row per ingested source file. source_sha256 is the join key to the file
-- corpus and becomes core_artifact.sha256 on promotion.
CREATE TABLE stg_ingest_batch (
  batch_id       INTEGER PRIMARY KEY,
  format_tag     TEXT    NOT NULL CHECK (format_tag IN ('DUOLINGO_PACKET', 'OPERATOR_NOTE', 'AUDIT_EXPORT')),
  source_path    TEXT    NOT NULL CHECK (length(source_path) > 0),
  source_sha256  TEXT    NOT NULL CHECK (length(source_sha256) = 64 AND source_sha256 NOT GLOB '*[^0-9a-f]*'),
  source_bytes   INTEGER NOT NULL CHECK (source_bytes >= 0),
  captured_at    TEXT    NOT NULL
                   CHECK (captured_at GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'),
  ingested_by    TEXT    NOT NULL CHECK (length(ingested_by) > 0),
  UNIQUE (format_tag, source_sha256)
) STRICT;

-- One row per source record, verbatim. row_ordinal is the 1-based position in
-- the source file; raw_text is the exact bytes of that record decoded UTF-8.
CREATE TABLE stg_raw_row (
  raw_row_id     INTEGER PRIMARY KEY,
  batch_id       INTEGER NOT NULL REFERENCES stg_ingest_batch (batch_id),
  row_ordinal    INTEGER NOT NULL CHECK (row_ordinal >= 1),
  raw_text       TEXT    NOT NULL,
  raw_sha256     TEXT    NOT NULL CHECK (length(raw_sha256) = 64 AND raw_sha256 NOT GLOB '*[^0-9a-f]*'),
  UNIQUE (batch_id, row_ordinal)
) STRICT;

-- Parse output: one candidate per (raw row, parser version, candidate kind).
-- parse_state separates the cases that must never collapse:
--   PARSED       payload_json is a complete candidate for candidate_kind
--   PARTIAL      payload_json holds what parsed; missing_fields_json lists the rest
--   MALFORMED    row could not be parsed; payload_json = '{}'
--   NOT_APPLICABLE  row carries no candidate of this kind
-- A missing field is listed, never defaulted to '', 0, or false.
CREATE TABLE stg_candidate (
  candidate_id         INTEGER PRIMARY KEY,
  raw_row_id           INTEGER NOT NULL REFERENCES stg_raw_row (raw_row_id),
  parser_id            TEXT    NOT NULL CHECK (length(parser_id) > 0),
  parser_version       INTEGER NOT NULL CHECK (parser_version >= 1),
  candidate_kind       TEXT    NOT NULL CHECK (candidate_kind IN
                         ('COMPANY', 'NAME_VARIANT', 'FILING', 'CLAIM', 'VERDICT',
                          'APPLICATION', 'APPLICATION_STATE', 'APPLICATION_TERM',
                          'ACTION_ITEM', 'BLOCKER', 'BLOCKER_STATE', 'EXPECTATION',
                          'NOTE')),
  parse_state          TEXT    NOT NULL CHECK (parse_state IN ('PARSED', 'PARTIAL', 'MALFORMED', 'NOT_APPLICABLE')),
  payload_json         TEXT    NOT NULL CHECK (json_valid(payload_json) AND json_type(payload_json) = 'object'),
  missing_fields_json  TEXT    NOT NULL CHECK (json_valid(missing_fields_json) AND json_type(missing_fields_json) = 'array'),
  UNIQUE (raw_row_id, parser_id, parser_version, candidate_kind),
  CHECK ((parse_state = 'PARTIAL') = (json_array_length(missing_fields_json) > 0)),
  CHECK (parse_state <> 'MALFORMED' OR payload_json = '{}')
) STRICT;

-- Promotion decisions: one per (candidate, rule version). Rules are documented
-- per table and versioned (README 7). HOLD keeps the candidate in staging with
-- a reason; REJECT is final for that rule version; PROMOTE is executed only by
-- a core_promotion_run, which writes receipts.
CREATE TABLE stg_promotion_decision (
  decision_id      INTEGER PRIMARY KEY,
  candidate_id     INTEGER NOT NULL REFERENCES stg_candidate (candidate_id),
  rule_id          TEXT    NOT NULL CHECK (length(rule_id) > 0),
  rule_version     INTEGER NOT NULL CHECK (rule_version >= 1),
  decision         TEXT    NOT NULL CHECK (decision IN ('PROMOTE', 'HOLD', 'REJECT')),
  reason           TEXT    NOT NULL CHECK (length(reason) > 0),
  decided_by       TEXT    NOT NULL CHECK (length(decided_by) > 0),
  decided_at       TEXT    NOT NULL
                     CHECK (decided_at GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'),
  UNIQUE (candidate_id, rule_id, rule_version)
) STRICT;

CREATE TRIGGER stg_promotion_decision_needs_parse BEFORE INSERT ON stg_promotion_decision
WHEN NEW.decision = 'PROMOTE'
 AND (SELECT parse_state FROM stg_candidate WHERE candidate_id = NEW.candidate_id) NOT IN ('PARSED', 'PARTIAL')
BEGIN SELECT RAISE(ABORT, 'stg_promotion_decision: MALFORMED or NOT_APPLICABLE candidates cannot be promoted'); END;

-- Append-only staging.
CREATE TRIGGER stg_ingest_batch_no_update BEFORE UPDATE ON stg_ingest_batch BEGIN SELECT RAISE(ABORT, 'staging is append-only'); END;
CREATE TRIGGER stg_ingest_batch_no_delete BEFORE DELETE ON stg_ingest_batch BEGIN SELECT RAISE(ABORT, 'staging is append-only'); END;
CREATE TRIGGER stg_raw_row_no_update BEFORE UPDATE ON stg_raw_row BEGIN SELECT RAISE(ABORT, 'staging is append-only'); END;
CREATE TRIGGER stg_raw_row_no_delete BEFORE DELETE ON stg_raw_row BEGIN SELECT RAISE(ABORT, 'staging is append-only'); END;
CREATE TRIGGER stg_candidate_no_update BEFORE UPDATE ON stg_candidate BEGIN SELECT RAISE(ABORT, 'staging is append-only'); END;
CREATE TRIGGER stg_candidate_no_delete BEFORE DELETE ON stg_candidate BEGIN SELECT RAISE(ABORT, 'staging is append-only'); END;
CREATE TRIGGER stg_promotion_decision_no_update BEFORE UPDATE ON stg_promotion_decision BEGIN SELECT RAISE(ABORT, 'staging is append-only'); END;
CREATE TRIGGER stg_promotion_decision_no_delete BEFORE DELETE ON stg_promotion_decision BEGIN SELECT RAISE(ABORT, 'staging is append-only'); END;

CREATE INDEX stg_candidate_by_kind ON stg_candidate (candidate_kind, parse_state);
