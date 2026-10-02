-- UnSilo store, migration 0001: migration ledger, receipt ledger, declared
-- cuts, contract-status registry.
-- File-level pragmas (page_size, WAL, application_id, user_version) are set by
-- the runner before this file runs (unsilo/db.py); per-connection pragmas are
-- set and read back on every connection.
-- Namespaces in one file (R2): meta_*, stg_*, core_* (Docket), ev_* (evidence).

CREATE TABLE meta_migration (
  version      INTEGER PRIMARY KEY CHECK (version >= 1),
  name         TEXT    NOT NULL UNIQUE,
  sha256       TEXT    NOT NULL UNIQUE CHECK (length(sha256) = 64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  applied_at   TEXT    NOT NULL CHECK (applied_at GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z')
) STRICT;
CREATE TRIGGER meta_migration_no_update BEFORE UPDATE ON meta_migration
BEGIN SELECT RAISE(ABORT, 'meta_migration is append-only'); END;
CREATE TRIGGER meta_migration_no_delete BEFORE DELETE ON meta_migration
BEGIN SELECT RAISE(ABORT, 'meta_migration is append-only'); END;
CREATE TRIGGER meta_migration_forward_only BEFORE INSERT ON meta_migration
WHEN NEW.version <> coalesce((SELECT max(version) FROM meta_migration), 0) + 1
BEGIN SELECT RAISE(ABORT, 'meta_migration: versions must be contiguous and forward-only'); END;

-- Receipt ledger: the one write path. Every stg_/core_/ev_ row is preceded, in
-- the same transaction, by a receipt whose after_image_json is the canonical
-- JSON of exactly that row (per-table triggers check equality column by
-- column). receipt_sha256 = SHA-256 of the canonical JSON of every receipt
-- column except after_image_json and receipt_sha256 itself; prev_receipt_sha256
-- chains receipts (R18). Replay = rebuild every table from the after-images.
CREATE TABLE meta_receipt (
  receipt_id           INTEGER PRIMARY KEY CHECK (receipt_id >= 1),
  table_name           TEXT    NOT NULL CHECK (table_name GLOB 'core_*' OR table_name GLOB 'stg_*' OR table_name GLOB 'ev_*'),
  row_pk               INTEGER NOT NULL,
  op                   TEXT    NOT NULL CHECK (op IN ('INSERT')),
  actor                TEXT    NOT NULL CHECK (length(actor) > 0),
  reason               TEXT    NOT NULL CHECK (length(reason) > 0),
  promotion_run_id     INTEGER,
  before_kind          TEXT    NOT NULL CHECK (before_kind IN ('ABSENT')),
  before_sha256        TEXT    CHECK (before_sha256 IS NULL),
  after_sha256         TEXT    NOT NULL CHECK (length(after_sha256) = 64 AND after_sha256 NOT GLOB '*[^0-9a-f]*'),
  after_image_json     TEXT    NOT NULL CHECK (json_valid(after_image_json) AND json_type(after_image_json) = 'object'),
  prev_kind            TEXT    NOT NULL CHECK (prev_kind IN ('GENESIS', 'HASH')),
  prev_receipt_sha256  TEXT,
  receipt_sha256       TEXT    NOT NULL UNIQUE CHECK (length(receipt_sha256) = 64 AND receipt_sha256 NOT GLOB '*[^0-9a-f]*'),
  recorded_at          TEXT    NOT NULL CHECK (recorded_at GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'),
  UNIQUE (table_name, row_pk, op),
  CHECK ((prev_kind = 'HASH') = (prev_receipt_sha256 IS NOT NULL))
) STRICT;
CREATE TRIGGER meta_receipt_no_update BEFORE UPDATE ON meta_receipt
BEGIN SELECT RAISE(ABORT, 'meta_receipt is append-only'); END;
CREATE TRIGGER meta_receipt_no_delete BEFORE DELETE ON meta_receipt
BEGIN SELECT RAISE(ABORT, 'meta_receipt is append-only'); END;
CREATE TRIGGER meta_receipt_sequence BEFORE INSERT ON meta_receipt
WHEN NEW.receipt_id <> coalesce((SELECT max(receipt_id) FROM meta_receipt), 0) + 1
BEGIN SELECT RAISE(ABORT, 'meta_receipt: receipt_id must be max+1'); END;
CREATE TRIGGER meta_receipt_genesis BEFORE INSERT ON meta_receipt
WHEN (NEW.prev_kind = 'GENESIS') <> (NOT EXISTS (SELECT 1 FROM meta_receipt))
BEGIN SELECT RAISE(ABORT, 'meta_receipt: GENESIS iff ledger empty'); END;
CREATE TRIGGER meta_receipt_chain BEFORE INSERT ON meta_receipt
WHEN NEW.prev_kind = 'HASH'
 AND NEW.prev_receipt_sha256 IS NOT (SELECT receipt_sha256 FROM meta_receipt ORDER BY receipt_id DESC LIMIT 1)
BEGIN SELECT RAISE(ABORT, 'meta_receipt: prev_receipt_sha256 does not match chain head'); END;
CREATE TRIGGER meta_receipt_monotone_time BEFORE INSERT ON meta_receipt
WHEN NEW.recorded_at < coalesce((SELECT recorded_at FROM meta_receipt ORDER BY receipt_id DESC LIMIT 1), '')
BEGIN SELECT RAISE(ABORT, 'meta_receipt: recorded_at must not go backwards'); END;
-- DL-3: content check in-transaction. sha256_hex is registered DETERMINISTIC +
-- INNOCUOUS on every connection; a connection without it cannot write (fails closed).
CREATE TRIGGER meta_receipt_after_hash BEFORE INSERT ON meta_receipt
WHEN sha256_hex(NEW.after_image_json) IS NOT NEW.after_sha256
BEGIN SELECT RAISE(ABORT, 'meta_receipt: after_sha256 does not match after_image_json'); END;
CREATE INDEX meta_receipt_by_table ON meta_receipt (table_name, row_pk);
CREATE INDEX meta_receipt_by_time ON meta_receipt (recorded_at, receipt_id);

-- Declared, named cuts (S8: evaluation never reads the clock). The dashboard
-- also declares a per-request cut and prints it on the page.
CREATE TABLE meta_cut (
  cut_id         INTEGER PRIMARY KEY,
  label          TEXT    NOT NULL UNIQUE CHECK (length(label) > 0),
  eff_value      TEXT    NOT NULL,
  eff_gran       TEXT    NOT NULL CHECK (eff_gran IN ('DAY', 'SECOND')),
  eff_zone       TEXT    NOT NULL CHECK (length(eff_zone) > 0 AND eff_zone <> 'FLOATING'),
  knowledge_cut  TEXT    NOT NULL CHECK (knowledge_cut GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'),
  CHECK ((eff_gran = 'DAY' AND eff_value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]' AND date(eff_value) IS eff_value)
      OR (eff_gran = 'SECOND' AND eff_zone = 'UTC'
          AND eff_value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'))
) STRICT;
CREATE TRIGGER meta_cut_no_update BEFORE UPDATE ON meta_cut
BEGIN SELECT RAISE(ABORT, 'meta_cut is append-only'); END;
CREATE TRIGGER meta_cut_no_delete BEFORE DELETE ON meta_cut
BEGIN SELECT RAISE(ABORT, 'meta_cut is append-only'); END;

-- Contract-status registry: the evidence plane's gate (it never reads Docket).
-- History rows; the head per contract is the highest seq. Written only by
-- migrations, so a status change is a reviewed, hash-ledgered file.
CREATE TABLE meta_contract_status (
  contract_id  TEXT    NOT NULL CHECK (length(contract_id) > 0),
  seq          INTEGER NOT NULL CHECK (seq >= 1),
  status       TEXT    NOT NULL CHECK (status IN ('FROZEN', 'ADMITTED', 'RETAINED', 'RETAINED_INTEGRATION_VERIFIED',
                                                  'REPAIRED_PENDING_ADMISSION', 'OPEN', 'UNADMITTED')),
  source_ref   TEXT    NOT NULL CHECK (length(source_ref) > 0),
  PRIMARY KEY (contract_id, seq)
) STRICT;
CREATE TRIGGER meta_contract_status_no_update BEFORE UPDATE ON meta_contract_status
BEGIN SELECT RAISE(ABORT, 'meta_contract_status changes only by a new migration row'); END;
CREATE TRIGGER meta_contract_status_no_delete BEFORE DELETE ON meta_contract_status
BEGIN SELECT RAISE(ABORT, 'meta_contract_status changes only by a new migration row'); END;
CREATE TRIGGER meta_contract_status_seq BEFORE INSERT ON meta_contract_status
WHEN NEW.seq <> coalesce((SELECT max(seq) FROM meta_contract_status WHERE contract_id = NEW.contract_id), 0) + 1
BEGIN SELECT RAISE(ABORT, 'meta_contract_status: seq must be max+1 per contract'); END;
CREATE VIEW v_contract_head AS
SELECT s.contract_id, s.seq, s.status, s.source_ref
FROM meta_contract_status s
WHERE s.seq = (SELECT max(seq) FROM meta_contract_status x WHERE x.contract_id = s.contract_id);

INSERT INTO meta_contract_status (contract_id, seq, status, source_ref) VALUES
  ('B1', 1, 'REPAIRED_PENDING_ADMISSION', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers; freeze retracted 2026-10-01 7:00 AM ET'),
  ('B2', 1, 'FROZEN', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('B3', 1, 'FROZEN', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('B4', 1, 'FROZEN', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('B5', 1, 'RETAINED_INTEGRATION_VERIFIED', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('B6', 1, 'RETAINED_INTEGRATION_VERIFIED', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('B7', 1, 'FROZEN', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('B8', 1, 'FROZEN', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('B9', 1, 'REPAIRED_PENDING_ADMISSION', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers; freeze retracted 2026-10-01 7:00 AM ET'),
  ('B10', 1, 'OPEN', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers; later work quarantined provisional'),
  ('B11', 1, 'RETAINED', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('B12', 1, 'RETAINED', 'pack/unsilo-feed-dashboard-spec-2026-10-02.md Blockers'),
  ('RECON-ECLASS-PD-AO-DD-v2.0', 1, 'UNADMITTED', 'pack/unsilo-master-architecture-prompt-2026-10-02.md section 2; ruling D-2 (separate admission + Foundation v2 erratum)');
