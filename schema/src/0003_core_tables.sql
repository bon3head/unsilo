-- UnSilo dashboard schema, migration 0003: core namespace (core_*).
-- Status: PROPOSED DESIGN ARTIFACT. Not approved. Build authorization: NONE.
--
-- Core rules, enforced below:
--  1. Append-only. No UPDATE, no DELETE on any core_* table. A change is a new
--     row that names the row it supersedes. History is never edited.
--  2. Receipt first. Every core_* row cites receipt_id; the receipt must already
--     exist, name this table, this row's primary key, op INSERT, and be used by
--     exactly one row. Since the receipt row must exist for the FK and trigger
--     to pass, the receipt is written BEFORE the mutation, same transaction.
--  3. Explicit primary keys. The writer supplies every primary key (it needs the
--     key to write the receipt first). A NULL key aborts.
--  4. Temporal values live in core_instant (point times) and core_interval
--     (effective-time intervals). Every bound is a tagged triple; NULL is never
--     a bound. See README 3 for the frozen B4 conformance argument.
--  5. Knowledge time (transaction time) = meta_receipt.recorded_at of the row.
--  6. Integers for counts and money (minor units). No REAL column anywhere.

------------------------------------------------------------------------------
-- Temporal primitives
------------------------------------------------------------------------------

-- Point time. Frozen rule: point times are KNOWN or UNKNOWN, never UNBOUNDED.
-- KNOWN carries its own granularity (DAY in a named civil calendar zone, or
-- SECOND in UTC); a date-only value is never synthesized into a timestamp.
-- source_text keeps the original wording (e.g. "~9:31 PM ET") so precision the
-- source did not assert is never stored as if it had.
CREATE TABLE core_instant (
  instant_id    INTEGER PRIMARY KEY,
  kind          TEXT    NOT NULL CHECK (kind IN ('KNOWN', 'UNKNOWN')),
  value         TEXT,
  gran          TEXT,
  zone          TEXT,
  source_text   TEXT    NOT NULL,
  receipt_id    INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((kind = 'KNOWN') = (value IS NOT NULL AND gran IS NOT NULL AND zone IS NOT NULL)),
  CHECK (kind = 'KNOWN' OR (value IS NULL AND gran IS NULL AND zone IS NULL)),
  CHECK (gran IS NULL
      OR (gran = 'DAY'
          AND value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]'
          AND date(value) IS value)
      OR (gran = 'SECOND' AND zone = 'UTC'
          AND value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'
          AND date(substr(value, 1, 10)) IS substr(value, 1, 10)
          AND CAST(substr(value, 12, 2) AS INTEGER) < 24
          AND CAST(substr(value, 15, 2) AS INTEGER) < 60))
) STRICT;

-- Effective-time interval, half-open [from, to).
-- Each endpoint: KNOWN(value, gran, zone) | UNBOUNDED | UNKNOWN.
-- UNBOUNDED is affirmative source semantics of no finite bound; it is never
-- derived from a missing field. UNKNOWN means a finite bound may exist but is
-- not established. Neither is ever encoded as NULL-as-meaning or as a sentinel
-- date (no 9999-12-31).
-- Validity: if both endpoints are KNOWN they must share granularity and zone,
-- and from < to (empty [t,t) is not a state interval). Mixed-granularity KNOWN
-- endpoints are refused at write time (README 3.4, OPEN U-DASH-03).
CREATE TABLE core_interval (
  interval_id    INTEGER PRIMARY KEY,
  from_kind      TEXT    NOT NULL CHECK (from_kind IN ('KNOWN', 'UNBOUNDED', 'UNKNOWN')),
  from_value     TEXT,
  from_gran      TEXT,
  from_zone      TEXT,
  to_kind        TEXT    NOT NULL CHECK (to_kind IN ('KNOWN', 'UNBOUNDED', 'UNKNOWN')),
  to_value       TEXT,
  to_gran        TEXT,
  to_zone        TEXT,
  unbounded_basis TEXT   NOT NULL,   -- source wording that asserts no finite bound; '' iff no endpoint is UNBOUNDED
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((from_kind = 'KNOWN') = (from_value IS NOT NULL AND from_gran IS NOT NULL AND from_zone IS NOT NULL)),
  CHECK (from_kind = 'KNOWN' OR (from_value IS NULL AND from_gran IS NULL AND from_zone IS NULL)),
  CHECK ((to_kind = 'KNOWN') = (to_value IS NOT NULL AND to_gran IS NOT NULL AND to_zone IS NOT NULL)),
  CHECK (to_kind = 'KNOWN' OR (to_value IS NULL AND to_gran IS NULL AND to_zone IS NULL)),
  CHECK (from_gran IS NULL
      OR (from_gran = 'DAY' AND from_value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]' AND date(from_value) IS from_value)
      OR (from_gran = 'SECOND' AND from_zone = 'UTC'
          AND from_value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'
          AND date(substr(from_value, 1, 10)) IS substr(from_value, 1, 10)
          AND CAST(substr(from_value, 12, 2) AS INTEGER) < 24
          AND CAST(substr(from_value, 15, 2) AS INTEGER) < 60)),
  CHECK (to_gran IS NULL
      OR (to_gran = 'DAY' AND to_value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]' AND date(to_value) IS to_value)
      OR (to_gran = 'SECOND' AND to_zone = 'UTC'
          AND to_value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'
          AND date(substr(to_value, 1, 10)) IS substr(to_value, 1, 10)
          AND CAST(substr(to_value, 12, 2) AS INTEGER) < 24
          AND CAST(substr(to_value, 15, 2) AS INTEGER) < 60)),
  CHECK (NOT (from_kind = 'KNOWN' AND to_kind = 'KNOWN')
      OR (from_gran = to_gran AND from_zone = to_zone AND from_value < to_value)),
  CHECK ((from_kind = 'UNBOUNDED' OR to_kind = 'UNBOUNDED') = (length(unbounded_basis) > 0))
) STRICT;

------------------------------------------------------------------------------
-- Corpus and identity
------------------------------------------------------------------------------

-- Every file the intel rests on, content-addressed. sha256 is the join key
-- between the database and the file corpus.
CREATE TABLE core_artifact (
  artifact_id    INTEGER PRIMARY KEY,
  sha256         TEXT    NOT NULL UNIQUE CHECK (length(sha256) = 64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  path           TEXT    NOT NULL CHECK (length(path) > 0),
  byte_len       INTEGER NOT NULL CHECK (byte_len >= 0),
  captured_at_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

-- One row per real-world company. company_key is a 10-digit CIK only where the
-- recruiting publisher is the filer (S5/B8); otherwise an opaque durable
-- UnSilo key. Names, tickers, domains, board tokens are never keys.
CREATE TABLE core_company (
  company_id     INTEGER PRIMARY KEY,
  key_kind       TEXT    NOT NULL CHECK (key_kind IN ('CIK', 'UNSILO_OPAQUE')),
  company_key    TEXT    NOT NULL UNIQUE,
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((key_kind = 'CIK' AND company_key GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
      OR (key_kind = 'UNSILO_OPAQUE' AND company_key GLOB 'us-co-*'))
) STRICT;

-- Entity resolution lives here: each name string is a row with a dated
-- mapping decision and its basis. Never merged in a string column.
CREATE TABLE core_name_variant (
  variant_id     INTEGER PRIMARY KEY,
  company_id     INTEGER NOT NULL REFERENCES core_company (company_id),
  variant        TEXT    NOT NULL CHECK (length(variant) > 0),
  basis_kind     TEXT    NOT NULL CHECK (basis_kind IN ('ARTIFACT', 'OPERATOR_STATEMENT')),
  basis_artifact_id INTEGER REFERENCES core_artifact (artifact_id),
  basis_note     TEXT    NOT NULL,
  decided_at_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((basis_kind = 'ARTIFACT') = (basis_artifact_id IS NOT NULL)),
  UNIQUE (company_id, variant)
) STRICT;

CREATE TABLE core_filing (
  filing_id      INTEGER PRIMARY KEY,
  company_id     INTEGER NOT NULL REFERENCES core_company (company_id),
  filing_type    TEXT    NOT NULL CHECK (length(filing_type) > 0),
  accession      TEXT    NOT NULL UNIQUE CHECK (length(accession) > 0),
  filed_at_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  artifact_id    INTEGER NOT NULL REFERENCES core_artifact (artifact_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

------------------------------------------------------------------------------
-- Claims and the two verdict axes
------------------------------------------------------------------------------

-- Atomic claim: one checkable assertion. A claim with artifact_state UNJOINED
-- has no artifact row behind it and is UNRESOLVED by construction (trigger on
-- core_verdict; view v_claim_effective in 0004).
CREATE TABLE core_claim (
  claim_id       INTEGER PRIMARY KEY,
  subject_kind   TEXT    NOT NULL CHECK (subject_kind IN ('COMPANY', 'PROGRAM')),
  company_id     INTEGER REFERENCES core_company (company_id),
  claim_text     TEXT    NOT NULL CHECK (length(claim_text) > 0),
  source_quote   TEXT    NOT NULL,
  artifact_state TEXT    NOT NULL CHECK (artifact_state IN ('JOINED', 'UNJOINED')),
  artifact_id    INTEGER REFERENCES core_artifact (artifact_id),
  supersedes_claim_id INTEGER REFERENCES core_claim (claim_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((subject_kind = 'COMPANY') = (company_id IS NOT NULL)),
  CHECK ((artifact_state = 'JOINED') = (artifact_id IS NOT NULL)),
  CHECK (artifact_state = 'UNJOINED' OR length(source_quote) > 0)
) STRICT;

-- Audit-verdict axis. Verdicts are ROWS: a claim carries a verdict history.
-- Stored status vocabulary follows the data theory and the audit record
-- (UNRESOLVED); the dashboard pill label for UNRESOLVED is OPEN U-DASH-05.
CREATE TABLE core_verdict (
  verdict_id     INTEGER PRIMARY KEY,
  claim_id       INTEGER NOT NULL REFERENCES core_claim (claim_id),
  status         TEXT    NOT NULL CHECK (status IN ('CONFIRMED', 'KILLED', 'DOWNGRADED', 'UNRESOLVED')),
  decided_at_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  decided_by     TEXT    NOT NULL CHECK (length(decided_by) > 0),
  rationale      TEXT    NOT NULL CHECK (length(rationale) > 0),
  audit_run_id   INTEGER REFERENCES core_audit_run (audit_run_id),
  supersedes_verdict_id INTEGER REFERENCES core_verdict (verdict_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

-- Evidence-class axis, kept separate from verdicts. While
-- RECON-ECLASS-PD-AO-DD-v2.0 is UNADMITTED, only ABSTENTION rows are possible
-- (trigger below): every CLASSIFY path yields ABSTENTION(CLASSIFIER_NOT_ADMITTED).
CREATE TABLE core_claim_eclass (
  eclass_id      INTEGER PRIMARY KEY,
  claim_id       INTEGER NOT NULL REFERENCES core_claim (claim_id),
  contract_id    TEXT    NOT NULL REFERENCES meta_contract_status (contract_id),
  state          TEXT    NOT NULL CHECK (state IN ('ADMITTED', 'ABSTENTION')),
  class          TEXT    CHECK (class IN ('PD', 'AO', 'DD', 'QN', 'UR')),
  weak           INTEGER NOT NULL CHECK (weak IN (0, 1)),
  abstention_reason TEXT,
  supersedes_eclass_id INTEGER REFERENCES core_claim_eclass (eclass_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((state = 'ADMITTED') = (class IS NOT NULL)),
  CHECK ((state = 'ABSTENTION') = (abstention_reason IS NOT NULL)),
  CHECK (state = 'ADMITTED' OR weak = 0)
) STRICT;

------------------------------------------------------------------------------
-- Blockers
------------------------------------------------------------------------------

-- Blocker identity. (program, code) is the key: "B4" exists in more than one
-- program (research-chain B4 temporal semantics vs Superhuman B4 Form D), so a
-- bare code is never an identifier.
CREATE TABLE core_blocker (
  blocker_id     INTEGER PRIMARY KEY,
  program        TEXT    NOT NULL CHECK (program IN ('RESEARCH_CHAIN', 'SUPERHUMAN_TARGETING', 'DASHBOARD')),
  code           TEXT    NOT NULL CHECK (length(code) > 0),
  title          TEXT    NOT NULL CHECK (length(title) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  UNIQUE (program, code)
) STRICT;

-- Blocker lifecycle states. The vocabulary is wider than open/closed because
-- the research chain's true states are wider (master doc section 10).
-- is_terminal decides strip visibility; values below are a proposal (OPEN U-DASH-06).
CREATE TABLE core_blocker_state_vocab (
  state          TEXT    PRIMARY KEY,
  is_terminal    INTEGER NOT NULL CHECK (is_terminal IN (0, 1))
) STRICT;

INSERT INTO core_blocker_state_vocab (state, is_terminal) VALUES
  ('OPEN', 0),
  ('REPAIRED_PENDING_ADMISSION', 0),
  ('RETAINED', 0),
  ('RETAINED_INTEGRATION_VERIFIED', 0),
  ('UNADMITTED', 0),
  ('FROZEN', 1),
  ('CLOSED', 1);

-- One row per recorded state. valid_interval = when the state held (effective
-- time). Knowledge time = the receipt. A retraction (e.g. B1/B9 FROZEN at
-- 4:38 AM, retracted 7:00 AM on 2026-10-01) is a NEW row superseding the old;
-- the old row stays visible to knowledge cuts before the retraction.
-- falsifier/owner: STATED or UNKNOWN, never blank-as-unknown.
CREATE TABLE core_blocker_state (
  state_id       INTEGER PRIMARY KEY,
  blocker_id     INTEGER NOT NULL REFERENCES core_blocker (blocker_id),
  state          TEXT    NOT NULL REFERENCES core_blocker_state_vocab (state),
  valid_interval_id INTEGER NOT NULL REFERENCES core_interval (interval_id),
  falsifier_state TEXT   NOT NULL CHECK (falsifier_state IN ('STATED', 'UNKNOWN')),
  falsifier      TEXT,
  owner_state    TEXT    NOT NULL CHECK (owner_state IN ('STATED', 'UNKNOWN')),
  owner          TEXT,
  basis          TEXT    NOT NULL CHECK (length(basis) > 0),
  supersedes_state_id INTEGER REFERENCES core_blocker_state (state_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((falsifier_state = 'STATED') = (falsifier IS NOT NULL AND length(falsifier) > 0)),
  CHECK (falsifier_state = 'STATED' OR falsifier IS NULL),
  CHECK ((owner_state = 'STATED') = (owner IS NOT NULL AND length(owner) > 0)),
  CHECK (owner_state = 'STATED' OR owner IS NULL)
) STRICT;

------------------------------------------------------------------------------
-- Applications
------------------------------------------------------------------------------

-- req_ref: the identifier exactly as the posting/platform shows it (e.g.
-- "1265", "JR2023492", "8052118 / R20978"). Never parsed into a number.
CREATE TABLE core_application (
  application_id INTEGER PRIMARY KEY,
  company_id     INTEGER NOT NULL REFERENCES core_company (company_id),
  role_state     TEXT    NOT NULL CHECK (role_state IN ('STATED', 'UNKNOWN')),
  role           TEXT,
  platform_state TEXT    NOT NULL CHECK (platform_state IN ('STATED', 'UNKNOWN')),
  platform       TEXT,
  req_state      TEXT    NOT NULL CHECK (req_state IN ('STATED', 'UNKNOWN')),
  req_ref        TEXT,
  location_state TEXT    NOT NULL CHECK (location_state IN ('STATED', 'UNKNOWN')),
  location       TEXT,
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((role_state = 'STATED') = (role IS NOT NULL AND length(role) > 0)),
  CHECK (role_state = 'STATED' OR role IS NULL),
  CHECK ((location_state = 'STATED') = (location IS NOT NULL AND length(location) > 0)),
  CHECK (location_state = 'STATED' OR location IS NULL),
  CHECK ((platform_state = 'STATED') = (platform IS NOT NULL AND length(platform) > 0)),
  CHECK (platform_state = 'STATED' OR platform IS NULL),
  CHECK ((req_state = 'STATED') = (req_ref IS NOT NULL AND length(req_ref) > 0)),
  CHECK (req_state = 'STATED' OR req_ref IS NULL)
) STRICT;

-- Status history. SUBMITTED / HELD_FOR_REVIEW / ACTION_NEEDED are the spec's
-- statuses. REJECTED and WITHDRAWN are PROPOSED additions so the rerun
-- protocol's open, rejected, reopened case is representable (README 9).
-- event_instant = when the transition happened (applied_at for SUBMITTED).
CREATE TABLE core_application_state (
  state_id       INTEGER PRIMARY KEY,
  application_id INTEGER NOT NULL REFERENCES core_application (application_id),
  status         TEXT    NOT NULL CHECK (status IN ('SUBMITTED', 'HELD_FOR_REVIEW', 'ACTION_NEEDED', 'REJECTED', 'WITHDRAWN')),
  event_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  valid_interval_id INTEGER NOT NULL REFERENCES core_interval (interval_id),
  submitted_by   TEXT    NOT NULL CHECK (length(submitted_by) > 0),
  supersedes_state_id INTEGER REFERENCES core_application_state (state_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

-- Key terms. Money in integer minor units with explicit currency and unit.
CREATE TABLE core_application_term (
  term_id        INTEGER PRIMARY KEY,
  application_id INTEGER NOT NULL REFERENCES core_application (application_id),
  term_key       TEXT    NOT NULL CHECK (length(term_key) > 0),
  value_kind     TEXT    NOT NULL CHECK (value_kind IN ('MONEY_MINOR', 'INTEGER', 'TEXT')),
  amount_minor   INTEGER,
  currency       TEXT,
  per_unit       TEXT,
  int_value      INTEGER,
  text_value     TEXT,
  source_text    TEXT    NOT NULL CHECK (length(source_text) > 0),
  supersedes_term_id INTEGER REFERENCES core_application_term (term_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((value_kind = 'MONEY_MINOR') = (amount_minor IS NOT NULL AND currency IS NOT NULL AND per_unit IS NOT NULL)),
  CHECK (value_kind = 'MONEY_MINOR' OR (amount_minor IS NULL AND currency IS NULL AND per_unit IS NULL)),
  CHECK ((value_kind = 'INTEGER') = (int_value IS NOT NULL)),
  CHECK ((value_kind = 'TEXT') = (text_value IS NOT NULL)),
  CHECK (currency IS NULL OR currency GLOB '[A-Z][A-Z][A-Z]'),
  CHECK (per_unit IS NULL OR per_unit IN ('HOUR', 'ONE_TIME', 'WEEK', 'YEAR'))
) STRICT;

-- Action items attach to exactly one application or one blocker.
CREATE TABLE core_action_item (
  item_id        INTEGER PRIMARY KEY,
  subject_kind   TEXT    NOT NULL CHECK (subject_kind IN ('APPLICATION', 'BLOCKER')),
  application_id INTEGER REFERENCES core_application (application_id),
  blocker_id     INTEGER REFERENCES core_blocker (blocker_id),
  text           TEXT    NOT NULL CHECK (length(text) > 0),
  owner          TEXT    NOT NULL CHECK (length(owner) > 0),
  due_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((subject_kind = 'APPLICATION') = (application_id IS NOT NULL)),
  CHECK ((subject_kind = 'BLOCKER') = (blocker_id IS NOT NULL))
) STRICT;

CREATE TABLE core_action_item_state (
  state_id       INTEGER PRIMARY KEY,
  item_id        INTEGER NOT NULL REFERENCES core_action_item (item_id),
  status         TEXT    NOT NULL CHECK (status IN ('OPEN', 'DONE', 'DROPPED')),
  event_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  supersedes_state_id INTEGER REFERENCES core_action_item_state (state_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

------------------------------------------------------------------------------
-- Audits
------------------------------------------------------------------------------

CREATE TABLE core_audit_run (
  audit_run_id   INTEGER PRIMARY KEY,
  run_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  worker_set     TEXT    NOT NULL CHECK (length(worker_set) > 0),
  scope          TEXT    NOT NULL CHECK (length(scope) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

-- Aggregate counts reported by an audit run, stored as reported (INTEGER).
-- Kept separate from per-claim verdict rows: a reported count is a statement
-- by the audit, not a derivation from rows we hold. v_audit_count_check (0004)
-- compares the two and surfaces any gap.
CREATE TABLE core_audit_count (
  count_id       INTEGER PRIMARY KEY,
  audit_run_id   INTEGER NOT NULL REFERENCES core_audit_run (audit_run_id),
  count_key      TEXT    NOT NULL CHECK (length(count_key) > 0),
  reported_value INTEGER NOT NULL CHECK (reported_value >= 0),
  source_text    TEXT    NOT NULL CHECK (length(source_text) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  UNIQUE (audit_run_id, count_key)
) STRICT;

CREATE TABLE core_audit_finding (
  finding_id     INTEGER PRIMARY KEY,
  audit_run_id   INTEGER NOT NULL REFERENCES core_audit_run (audit_run_id),
  claim_id       INTEGER NOT NULL REFERENCES core_claim (claim_id),
  verdict_id     INTEGER NOT NULL REFERENCES core_verdict (verdict_id),
  delta          TEXT    NOT NULL CHECK (length(delta) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  UNIQUE (audit_run_id, claim_id)
) STRICT;

------------------------------------------------------------------------------
-- Absence as signal
------------------------------------------------------------------------------

-- What SHOULD exist. Categorical basis, never a probability (README 5.2):
--   MANDATED  a rule or calendar requires it (e.g. a periodic filing)
--   ROUTINE   prior observations establish a pattern
--   STATED    the subject said it would happen (e.g. "we reply in 2 weeks")
--   OPERATOR  operator expectation with no external basis
-- checked_scope names the dataset the thing is or is not observed IN.
-- Absence from that dataset is not evidence of absence in the world.
CREATE TABLE core_expectation (
  expectation_id INTEGER PRIMARY KEY,
  subject_kind   TEXT    NOT NULL CHECK (subject_kind IN ('COMPANY', 'APPLICATION', 'CLAIM', 'BLOCKER')),
  company_id     INTEGER REFERENCES core_company (company_id),
  application_id INTEGER REFERENCES core_application (application_id),
  claim_id       INTEGER REFERENCES core_claim (claim_id),
  blocker_id     INTEGER REFERENCES core_blocker (blocker_id),
  expected_artifact_type TEXT NOT NULL CHECK (length(expected_artifact_type) > 0),
  expected_window_interval_id INTEGER NOT NULL REFERENCES core_interval (interval_id),
  basis          TEXT    NOT NULL CHECK (basis IN ('MANDATED', 'ROUTINE', 'STATED', 'OPERATOR')),
  basis_note     TEXT    NOT NULL CHECK (length(basis_note) > 0),
  checked_scope  TEXT    NOT NULL CHECK (length(checked_scope) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((subject_kind = 'COMPANY') = (company_id IS NOT NULL)),
  CHECK ((subject_kind = 'APPLICATION') = (application_id IS NOT NULL)),
  CHECK ((subject_kind = 'CLAIM') = (claim_id IS NOT NULL)),
  CHECK ((subject_kind = 'BLOCKER') = (blocker_id IS NOT NULL))
) STRICT;

-- Fulfillment status history. NOT_OBSERVED means "not observed in checked_scope
-- as of the check"; it is not QN (B5/B6 prerequisites are not modeled here)
-- and the dashboard never renders it as "does not exist".
CREATE TABLE core_expectation_state (
  state_id       INTEGER PRIMARY KEY,
  expectation_id INTEGER NOT NULL REFERENCES core_expectation (expectation_id),
  status         TEXT    NOT NULL CHECK (status IN ('NOT_EVALUATED', 'FULFILLED', 'NOT_OBSERVED', 'LATE', 'REFUTED')),
  checked_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  evidence_artifact_id INTEGER REFERENCES core_artifact (artifact_id),
  note           TEXT    NOT NULL,
  supersedes_state_id INTEGER REFERENCES core_expectation_state (state_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK (status NOT IN ('FULFILLED', 'REFUTED') OR evidence_artifact_id IS NOT NULL)
) STRICT;

------------------------------------------------------------------------------
-- Feed notes and research surfaces
------------------------------------------------------------------------------

-- Narrative feed entries that no other table derives (e.g. "UnSilo named and
-- positioned"). This is a source table; feed_item (0004) remains a VIEW.
CREATE TABLE core_note (
  note_id        INTEGER PRIMARY KEY,
  tag            TEXT    NOT NULL CHECK (tag IN ('applications', 'forensics', 'audits', 'research-chain', 'surfaces')),
  title          TEXT    NOT NULL CHECK (length(title) > 0),
  body           TEXT    NOT NULL CHECK (length(body) > 0),
  event_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  artifact_id    INTEGER REFERENCES core_artifact (artifact_id),
  supersedes_note_id INTEGER REFERENCES core_note (note_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK (instr(title, char(8212)) = 0 AND instr(body, char(8212)) = 0)
) STRICT;

CREATE TABLE core_research_surface (
  surface_id     INTEGER PRIMARY KEY,
  tier_code      TEXT    NOT NULL CHECK (tier_code IN ('T0', 'T1', 'T2', 'T3', 'T4', 'RED')),
  handling       TEXT    NOT NULL CHECK (handling IN ('GREEN', 'YELLOW', 'RED')),
  name           TEXT    NOT NULL CHECK (length(name) > 0),
  handling_note  TEXT    NOT NULL,
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((tier_code = 'RED') = (handling = 'RED')),
  CHECK (tier_code <> 'T4' OR handling = 'YELLOW')
) STRICT;

------------------------------------------------------------------------------
-- Promotion runs
------------------------------------------------------------------------------

-- One staging-to-core promotion run. Every receipt it writes carries its
-- promotion_run_id. fts_rebuilt records that the disposable FTS projection was
-- rebuilt at the end of the run (FTS is never written on raw staging writes).
CREATE TABLE core_promotion_run (
  promotion_run_id INTEGER PRIMARY KEY,
  batch_id       INTEGER NOT NULL REFERENCES stg_ingest_batch (batch_id),
  rule_set_version INTEGER NOT NULL CHECK (rule_set_version >= 1),
  started_at     TEXT    NOT NULL CHECK (started_at GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]Z'),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

-- Link from each promoted core row back to the staging candidate it came from.
CREATE TABLE core_promotion_link (
  link_id        INTEGER PRIMARY KEY,
  promotion_run_id INTEGER NOT NULL REFERENCES core_promotion_run (promotion_run_id),
  decision_id    INTEGER NOT NULL REFERENCES stg_promotion_decision (decision_id),
  target_receipt_id INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK (target_receipt_id <> receipt_id)
) STRICT;

CREATE TRIGGER core_promotion_link_needs_promote BEFORE INSERT ON core_promotion_link
WHEN (SELECT decision FROM stg_promotion_decision WHERE decision_id = NEW.decision_id) IS NOT 'PROMOTE'
BEGIN SELECT RAISE(ABORT, 'core_promotion_link: decision is not PROMOTE'); END;

------------------------------------------------------------------------------
-- Cross-table invariants
------------------------------------------------------------------------------

-- UNRESOLVED by construction: a claim with no artifact cannot receive any
-- verdict other than UNRESOLVED.
CREATE TRIGGER core_verdict_unjoined_is_unresolved BEFORE INSERT ON core_verdict
WHEN NEW.status <> 'UNRESOLVED'
 AND (SELECT artifact_state FROM core_claim WHERE claim_id = NEW.claim_id) = 'UNJOINED'
BEGIN SELECT RAISE(ABORT, 'core_verdict: claim has no artifact; only UNRESOLVED is admissible'); END;

-- Classifier abstention: no ADMITTED evidence class while the governing
-- contract is UNADMITTED.
CREATE TRIGGER core_claim_eclass_needs_admitted_contract BEFORE INSERT ON core_claim_eclass
WHEN NEW.state = 'ADMITTED'
 AND (SELECT status FROM meta_contract_status WHERE contract_id = NEW.contract_id) <> 'ADMITTED'
BEGIN SELECT RAISE(ABORT, 'core_claim_eclass: contract not admitted; only ABSTENTION(CLASSIFIER_NOT_ADMITTED)'); END;

-- Supersession must stay within the same subject.
CREATE TRIGGER core_verdict_supersedes_same_claim BEFORE INSERT ON core_verdict
WHEN NEW.supersedes_verdict_id IS NOT NULL
 AND (SELECT claim_id FROM core_verdict WHERE verdict_id = NEW.supersedes_verdict_id) IS NOT NEW.claim_id
BEGIN SELECT RAISE(ABORT, 'core_verdict: supersedes a verdict of another claim'); END;
CREATE TRIGGER core_blocker_state_supersedes_same_blocker BEFORE INSERT ON core_blocker_state
WHEN NEW.supersedes_state_id IS NOT NULL
 AND (SELECT blocker_id FROM core_blocker_state WHERE state_id = NEW.supersedes_state_id) IS NOT NEW.blocker_id
BEGIN SELECT RAISE(ABORT, 'core_blocker_state: supersedes a state of another blocker'); END;
CREATE TRIGGER core_application_state_supersedes_same_app BEFORE INSERT ON core_application_state
WHEN NEW.supersedes_state_id IS NOT NULL
 AND (SELECT application_id FROM core_application_state WHERE state_id = NEW.supersedes_state_id) IS NOT NEW.application_id
BEGIN SELECT RAISE(ABORT, 'core_application_state: supersedes a state of another application'); END;

------------------------------------------------------------------------------
-- Indexes on the feed and panel access paths
------------------------------------------------------------------------------

CREATE INDEX core_verdict_by_claim ON core_verdict (claim_id, verdict_id);
CREATE INDEX core_verdict_by_status ON core_verdict (status);
CREATE INDEX core_claim_by_company ON core_claim (company_id);
CREATE INDEX core_blocker_state_by_blocker ON core_blocker_state (blocker_id, state_id);
CREATE INDEX core_blocker_state_by_state ON core_blocker_state (state);
CREATE INDEX core_application_by_company ON core_application (company_id);
CREATE INDEX core_application_state_by_app ON core_application_state (application_id, state_id);
CREATE INDEX core_application_state_by_status ON core_application_state (status);
CREATE INDEX core_instant_by_value ON core_instant (kind, gran, value);
CREATE INDEX core_note_by_tag ON core_note (tag);
CREATE INDEX core_expectation_state_by_exp ON core_expectation_state (expectation_id, state_id);
CREATE INDEX meta_receipt_by_time ON meta_receipt (recorded_at, receipt_id);
