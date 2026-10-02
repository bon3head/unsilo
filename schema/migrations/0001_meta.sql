-- UnSilo dashboard schema, migration 0001: file identity, migration ledger,
-- receipt ledger, declared query cuts, contract-status registry.
-- Status: PROPOSED DESIGN ARTIFACT. Not approved. Build authorization: NONE.
-- Conforms to: S6 B11 SQLite safety profile (RETAINED), frozen B4 temporal
-- contract as recorded in the ledger (see schema/README.md section 3).
--
-- Physical layout: ONE SQLite file. SQLite has no schemas inside one file
-- ("staging.x" names an ATTACHed database), so the staging/core split is a
-- table-name namespace: meta_*, stg_*, core_*, v_*, fts_*. See README 2.1.
--
-- File-level pragmas. page_size must precede the first table. journal_mode=WAL
-- persists in the file. application_id 0x554E534C ("UNSL") = 1431196492.
-- user_version = 1 = physical schema generation 1 (S6), NOT a migration count;
-- the migration count lives in meta_migration.
PRAGMA page_size = 4096;
PRAGMA journal_mode = WAL;
PRAGMA application_id = 1431196492;
PRAGMA user_version = 1;

-- Per-connection pragmas are NOT persisted and are set by the runner on every
-- connection, then read back (README 2.2): foreign_keys=ON (readback 1),
-- synchronous=FULL, trusted_schema=OFF, busy_timeout=5000, encoding UTF-8.

-- Migration ledger. Numbered, forward-only. sha256 = SHA-256 of the exact
-- migration file bytes, computed by the runner BEFORE apply and inserted in the
-- same transaction as the migration body. A file whose bytes differ from the
-- recorded hash on a later startup is a HALT condition.
CREATE TABLE meta_migration (
  version      INTEGER PRIMARY KEY CHECK (version >= 1),
  name         TEXT    NOT NULL UNIQUE,
  sha256       TEXT    NOT NULL UNIQUE
                 CHECK (length(sha256) = 64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  applied_at   TEXT    NOT NULL
                 CHECK (applied_at GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z')
) STRICT;

CREATE TRIGGER meta_migration_no_update BEFORE UPDATE ON meta_migration
BEGIN SELECT RAISE(ABORT, 'meta_migration is append-only'); END;
CREATE TRIGGER meta_migration_no_delete BEFORE DELETE ON meta_migration
BEGIN SELECT RAISE(ABORT, 'meta_migration is append-only'); END;
CREATE TRIGGER meta_migration_forward_only BEFORE INSERT ON meta_migration
WHEN NEW.version <> coalesce((SELECT max(version) FROM meta_migration), 0) + 1
BEGIN SELECT RAISE(ABORT, 'meta_migration: versions must be contiguous and forward-only'); END;

-- Receipt ledger. Append-only. Every core_* row insert must cite a receipt that
-- was inserted FIRST (FK + trigger in 0003), so the receipt is written before
-- the mutation inside the same transaction.
--   before_kind ABSENT  : insert of a new row (core is append-only, so this is
--                         the only kind used today; HASH is reserved).
--   after_image_json    : canonical JSON of the row as it will be written; this
--                         is what makes "repair = replay the ledger" executable.
--                         Hashes alone cannot be replayed (README 6.4).
--   prev_kind/prev_receipt_sha256 : hash chain over receipts (GENESIS first).
-- The SHA-256 values are computed by the writer; SQLite core has no SHA-256
-- SQL function, so the database checks shape and chain linkage, not content.
-- Content verification in-transaction is parked proposal (f).
CREATE TABLE meta_receipt (
  receipt_id           INTEGER PRIMARY KEY CHECK (receipt_id >= 1),
  table_name           TEXT    NOT NULL CHECK (table_name GLOB 'core_*'),
  row_pk               INTEGER NOT NULL,
  op                   TEXT    NOT NULL CHECK (op IN ('INSERT')),
  actor                TEXT    NOT NULL CHECK (length(actor) > 0),
  reason               TEXT    NOT NULL CHECK (length(reason) > 0),
  promotion_run_id     INTEGER,            -- set when written by a promotion run; FK added logically in 0003 view checks
  before_kind          TEXT    NOT NULL CHECK (before_kind IN ('ABSENT', 'HASH')),
  before_sha256        TEXT,
  after_sha256         TEXT    NOT NULL CHECK (length(after_sha256) = 64 AND after_sha256 NOT GLOB '*[^0-9a-f]*'),
  after_image_json     TEXT    NOT NULL CHECK (json_valid(after_image_json)),
  prev_kind            TEXT    NOT NULL CHECK (prev_kind IN ('GENESIS', 'HASH')),
  prev_receipt_sha256  TEXT,
  receipt_sha256       TEXT    NOT NULL UNIQUE CHECK (length(receipt_sha256) = 64 AND receipt_sha256 NOT GLOB '*[^0-9a-f]*'),
  recorded_at          TEXT    NOT NULL
                         CHECK (recorded_at GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'),
  UNIQUE (table_name, row_pk, op),
  CHECK ((before_kind = 'HASH') = (before_sha256 IS NOT NULL)),
  CHECK (before_sha256 IS NULL OR (length(before_sha256) = 64 AND before_sha256 NOT GLOB '*[^0-9a-f]*')),
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
 AND NEW.prev_receipt_sha256 IS NOT
     (SELECT receipt_sha256 FROM meta_receipt ORDER BY receipt_id DESC LIMIT 1)
BEGIN SELECT RAISE(ABORT, 'meta_receipt: prev_receipt_sha256 does not match chain head'); END;
CREATE TRIGGER meta_receipt_monotone_time BEFORE INSERT ON meta_receipt
WHEN NEW.recorded_at < coalesce((SELECT recorded_at FROM meta_receipt ORDER BY receipt_id DESC LIMIT 1), '')
BEGIN SELECT RAISE(ABORT, 'meta_receipt: recorded_at must not go backwards'); END;

-- Declared cuts (S8: no implicit now/latest/wall clock in evaluation). Every
-- temporal view evaluates against rows of this table, never against the clock.
-- Effective cut is a point time: KNOWN only (an UNKNOWN cut would be REJECT,
-- so it is unrepresentable here). Knowledge cut is a UTC second compared to
-- meta_receipt.recorded_at.
CREATE TABLE meta_cut (
  cut_id             INTEGER PRIMARY KEY,
  label              TEXT    NOT NULL UNIQUE,
  eff_value          TEXT    NOT NULL,
  eff_gran           TEXT    NOT NULL CHECK (eff_gran IN ('DAY', 'SECOND')),
  eff_zone           TEXT    NOT NULL CHECK (length(eff_zone) > 0),
  knowledge_cut      TEXT    NOT NULL
                       CHECK (knowledge_cut GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'),
  CHECK ((eff_gran = 'DAY'
          AND eff_value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]'
          AND date(eff_value) IS eff_value)
      OR (eff_gran = 'SECOND' AND eff_zone = 'UTC'
          AND eff_value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'
          AND date(substr(eff_value, 1, 10)) IS substr(eff_value, 1, 10)
          AND CAST(substr(eff_value, 12, 2) AS INTEGER) < 24
          AND CAST(substr(eff_value, 15, 2) AS INTEGER) < 60))
) STRICT;

-- Contract-status registry. Seeded by migration; changes only by migration.
-- RECON-ECLASS-PD-AO-DD-v2.0 is UNADMITTED, so core_claim_eclass rows can only
-- be ABSTENTION (enforced by trigger in 0003).
CREATE TABLE meta_contract_status (
  contract_id   TEXT PRIMARY KEY,
  status        TEXT NOT NULL CHECK (status IN ('ADMITTED', 'UNADMITTED')),
  source_ref    TEXT NOT NULL CHECK (length(source_ref) > 0)
) STRICT;

INSERT INTO meta_contract_status (contract_id, status, source_ref) VALUES
  ('RECON-ECLASS-PD-AO-DD-v2.0', 'UNADMITTED',
   'pack/unsilo-master-architecture-prompt-2026-10-02.md section 2; Foundation v2 canonical SHA-256 707269c9a2dd0029ca172aea8798e9719902596233ce54123c0c5a5c4bf2310f');

CREATE TRIGGER meta_contract_status_no_update BEFORE UPDATE ON meta_contract_status
BEGIN SELECT RAISE(ABORT, 'meta_contract_status changes only by migration (append a new migration)'); END;
CREATE TRIGGER meta_contract_status_no_delete BEFORE DELETE ON meta_contract_status
BEGIN SELECT RAISE(ABORT, 'meta_contract_status changes only by migration'); END;
