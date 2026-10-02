-- UnSilo store, migration 0002: Docket, the operator plane (core_*).
-- Item/state pattern: an item row is identity; every change is a new state or
-- term row naming the row it supersedes. No UPDATE, no DELETE (generated
-- triggers below). Heads are chosen per knowledge cut. Integers for money and
-- counts. Company identity, filings and expectations live in the evidence
-- plane (ev_*); Docket rows carry the operator's labels only.
-- One-way link: Docket may cite evidence; evidence never reads Docket.

------------------------------------------------------------------------------
-- Temporal primitives (frozen B4; DL-1 FLOATING; R14 approximate times)
------------------------------------------------------------------------------
-- Point time: KNOWN or UNKNOWN, never UNBOUNDED. DAY values carry a civil zone
-- or FLOATING (no zone context, S3). SECOND values are UTC. source_text keeps
-- the original wording ("~9:31 PM ET") so unasserted precision is never stored.
CREATE TABLE core_instant (
  instant_id    INTEGER PRIMARY KEY,
  kind          TEXT    NOT NULL CHECK (kind IN ('KNOWN', 'UNKNOWN')),
  value         TEXT,
  gran          TEXT    CHECK (gran IN ('DAY', 'SECOND')),
  zone          TEXT,
  source_text   TEXT    NOT NULL,
  receipt_id    INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((kind = 'KNOWN') = (value IS NOT NULL AND gran IS NOT NULL AND zone IS NOT NULL)),
  CHECK (kind = 'KNOWN' OR (value IS NULL AND gran IS NULL AND zone IS NULL)),
  CHECK (gran IS NULL
      OR (gran = 'DAY' AND length(zone) > 0
          AND value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]' AND date(value) IS value)
      OR (gran = 'SECOND' AND zone = 'UTC'
          AND value GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]Z'
          AND datetime(value) IS replace(substr(value, 1, 19), 'T', ' ')))
) STRICT;

-- Effective-time interval, half-open [from, to). Endpoint: KNOWN | UNBOUNDED |
-- UNKNOWN. UNBOUNDED needs affirmative source wording (unbounded_basis).
-- Same granularity and zone: from < to checked here. Mixed granularity (R19):
-- the writer lifts with pinned tzdata and refuses from >= to (unsilo/temporal.py).
CREATE TABLE core_interval (
  interval_id     INTEGER PRIMARY KEY,
  from_kind       TEXT    NOT NULL CHECK (from_kind IN ('KNOWN', 'UNBOUNDED', 'UNKNOWN')),
  from_value      TEXT,
  from_gran       TEXT    CHECK (from_gran IN ('DAY', 'SECOND')),
  from_zone       TEXT,
  to_kind         TEXT    NOT NULL CHECK (to_kind IN ('KNOWN', 'UNBOUNDED', 'UNKNOWN')),
  to_value        TEXT,
  to_gran         TEXT    CHECK (to_gran IN ('DAY', 'SECOND')),
  to_zone         TEXT,
  unbounded_basis TEXT    NOT NULL,
  receipt_id      INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((from_kind = 'KNOWN') = (from_value IS NOT NULL AND from_gran IS NOT NULL AND from_zone IS NOT NULL)),
  CHECK (from_kind = 'KNOWN' OR (from_value IS NULL AND from_gran IS NULL AND from_zone IS NULL)),
  CHECK ((to_kind = 'KNOWN') = (to_value IS NOT NULL AND to_gran IS NOT NULL AND to_zone IS NOT NULL)),
  CHECK (to_kind = 'KNOWN' OR (to_value IS NULL AND to_gran IS NULL AND to_zone IS NULL)),
  CHECK (from_gran IS NOT 'SECOND' OR from_zone = 'UTC'),
  CHECK (to_gran IS NOT 'SECOND' OR to_zone = 'UTC'),
  CHECK (NOT (from_kind = 'KNOWN' AND to_kind = 'KNOWN' AND from_gran = to_gran AND from_zone = to_zone)
         OR from_value < to_value),
  CHECK ((from_kind = 'UNBOUNDED' OR to_kind = 'UNBOUNDED') = (length(unbounded_basis) > 0))
) STRICT;

------------------------------------------------------------------------------
-- Artifacts: files the records rest on, content-addressed
------------------------------------------------------------------------------
-- storage REPO: path inside the git tree. LOCAL: path under var/ (gitignored;
-- personal data stays there and is cited by hash only).
CREATE TABLE core_artifact (
  artifact_id    INTEGER PRIMARY KEY,
  sha256         TEXT    NOT NULL UNIQUE CHECK (length(sha256) = 64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  storage        TEXT    NOT NULL CHECK (storage IN ('REPO', 'LOCAL')),
  path           TEXT    NOT NULL CHECK (length(path) > 0),
  byte_len       INTEGER NOT NULL CHECK (byte_len >= 0),
  media_type     TEXT    NOT NULL CHECK (length(media_type) > 0),
  label          TEXT    NOT NULL CHECK (length(label) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

------------------------------------------------------------------------------
-- Applications
------------------------------------------------------------------------------
CREATE TABLE core_application (
  application_id INTEGER PRIMARY KEY,
  app_key        TEXT    NOT NULL UNIQUE CHECK (length(app_key) > 0 AND app_key NOT GLOB '*[^a-z0-9-]*'),
  employer_label TEXT    NOT NULL CHECK (length(employer_label) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

-- Status history (R24 adds REJECTED and WITHDRAWN). event_instant = when the
-- transition happened. actor: who acted, STATED or UNKNOWN.
CREATE TABLE core_application_state (
  state_id         INTEGER PRIMARY KEY,
  application_id   INTEGER NOT NULL REFERENCES core_application (application_id),
  status           TEXT    NOT NULL CHECK (status IN ('SUBMITTED', 'HELD_FOR_REVIEW', 'ACTION_NEEDED', 'REJECTED', 'WITHDRAWN')),
  event_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  valid_interval_id INTEGER NOT NULL REFERENCES core_interval (interval_id),
  actor_state      TEXT    NOT NULL CHECK (actor_state IN ('STATED', 'UNKNOWN')),
  actor            TEXT,
  basis            TEXT    NOT NULL CHECK (length(basis) > 0),
  artifact_id      INTEGER REFERENCES core_artifact (artifact_id),
  supersedes_state_id INTEGER REFERENCES core_application_state (state_id),
  receipt_id       INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((actor_state = 'STATED') = (actor IS NOT NULL AND length(actor) > 0)),
  CHECK (actor_state = 'STATED' OR actor IS NULL)
) STRICT;

-- Terms: every descriptive field is a term row, so a correction is a new row.
-- value_kind UNKNOWN states the field is not established (never a sentinel).
-- Money in integer minor units with currency and unit; ranges carry both ends.
CREATE TABLE core_application_term (
  term_id         INTEGER PRIMARY KEY,
  application_id  INTEGER NOT NULL REFERENCES core_application (application_id),
  term_key        TEXT    NOT NULL CHECK (length(term_key) > 0 AND term_key NOT GLOB '*[^a-z_]*'),
  ordinal         INTEGER NOT NULL CHECK (ordinal >= 1),
  value_kind      TEXT    NOT NULL CHECK (value_kind IN ('TEXT', 'INTEGER', 'MONEY_MINOR', 'MONEY_RANGE_MINOR', 'INSTANT', 'INTERVAL', 'UNKNOWN')),
  text_value      TEXT,
  int_value       INTEGER,
  amount_minor    INTEGER,
  amount_minor_hi INTEGER,
  currency        TEXT    CHECK (currency IS NULL OR currency GLOB '[A-Z][A-Z][A-Z]'),
  per_unit        TEXT    CHECK (per_unit IS NULL OR per_unit IN ('HOUR', 'WEEK', 'YEAR', 'ONE_TIME')),
  instant_id      INTEGER REFERENCES core_instant (instant_id),
  interval_id     INTEGER REFERENCES core_interval (interval_id),
  source_text     TEXT    NOT NULL CHECK (length(source_text) > 0),
  artifact_id     INTEGER REFERENCES core_artifact (artifact_id),
  supersedes_term_id INTEGER REFERENCES core_application_term (term_id),
  receipt_id      INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((value_kind = 'TEXT') = (text_value IS NOT NULL)),
  CHECK ((value_kind = 'INTEGER') = (int_value IS NOT NULL)),
  CHECK ((value_kind IN ('MONEY_MINOR', 'MONEY_RANGE_MINOR')) = (amount_minor IS NOT NULL AND currency IS NOT NULL AND per_unit IS NOT NULL)),
  CHECK ((value_kind = 'MONEY_RANGE_MINOR') = (amount_minor_hi IS NOT NULL)),
  CHECK (amount_minor_hi IS NULL OR amount_minor_hi > amount_minor),
  CHECK (value_kind IN ('MONEY_MINOR', 'MONEY_RANGE_MINOR') OR (currency IS NULL AND per_unit IS NULL)),
  CHECK ((value_kind = 'INSTANT') = (instant_id IS NOT NULL)),
  CHECK ((value_kind = 'INTERVAL') = (interval_id IS NOT NULL))
) STRICT;

------------------------------------------------------------------------------
-- Blockers: identity is (program, code); "B4" exists in two programs.
------------------------------------------------------------------------------
CREATE TABLE core_blocker (
  blocker_id     INTEGER PRIMARY KEY,
  program        TEXT    NOT NULL CHECK (program IN ('RESEARCH_CHAIN', 'SUPERHUMAN_TARGETING', 'UNSILO_BUILD')),
  code           TEXT    NOT NULL CHECK (length(code) > 0),
  title          TEXT    NOT NULL CHECK (length(title) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  UNIQUE (program, code)
) STRICT;

-- R21: the strip shows non-terminal states (everything except FROZEN, CLOSED).
CREATE TABLE core_blocker_state_vocab (
  state        TEXT    PRIMARY KEY,
  is_terminal  INTEGER NOT NULL CHECK (is_terminal IN (0, 1))
) STRICT;
INSERT INTO core_blocker_state_vocab (state, is_terminal) VALUES
  ('OPEN', 0), ('REPAIRED_PENDING_ADMISSION', 0), ('RETAINED', 0),
  ('RETAINED_INTEGRATION_VERIFIED', 0), ('UNADMITTED', 0), ('FROZEN', 1), ('CLOSED', 1);
CREATE TRIGGER core_blocker_state_vocab_no_update BEFORE UPDATE ON core_blocker_state_vocab
BEGIN SELECT RAISE(ABORT, 'vocabulary changes only by migration'); END;
CREATE TRIGGER core_blocker_state_vocab_no_delete BEFORE DELETE ON core_blocker_state_vocab
BEGIN SELECT RAISE(ABORT, 'vocabulary changes only by migration'); END;

-- valid_interval: when the state held (effective time). asserted_instant: the
-- source's "as of" time. Knowledge time is the receipt. A retraction is a new
-- row that supersedes; the old row stays visible to earlier knowledge cuts.
CREATE TABLE core_blocker_state (
  state_id          INTEGER PRIMARY KEY,
  blocker_id        INTEGER NOT NULL REFERENCES core_blocker (blocker_id),
  state             TEXT    NOT NULL REFERENCES core_blocker_state_vocab (state),
  valid_interval_id INTEGER NOT NULL REFERENCES core_interval (interval_id),
  asserted_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  falsifier_state   TEXT    NOT NULL CHECK (falsifier_state IN ('STATED', 'UNKNOWN')),
  falsifier         TEXT,
  owner_state       TEXT    NOT NULL CHECK (owner_state IN ('STATED', 'UNKNOWN')),
  owner             TEXT,
  basis             TEXT    NOT NULL CHECK (length(basis) > 0),
  artifact_id       INTEGER REFERENCES core_artifact (artifact_id),
  supersedes_state_id INTEGER REFERENCES core_blocker_state (state_id),
  receipt_id        INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((falsifier_state = 'STATED') = (falsifier IS NOT NULL AND length(falsifier) > 0)),
  CHECK (falsifier_state = 'STATED' OR falsifier IS NULL),
  CHECK ((owner_state = 'STATED') = (owner IS NOT NULL AND length(owner) > 0)),
  CHECK (owner_state = 'STATED' OR owner IS NULL)
) STRICT;

------------------------------------------------------------------------------
-- Action items: on exactly one application or one blocker
------------------------------------------------------------------------------
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
  state_id         INTEGER PRIMARY KEY,
  item_id          INTEGER NOT NULL REFERENCES core_action_item (item_id),
  status           TEXT    NOT NULL CHECK (status IN ('OPEN', 'DONE', 'DROPPED')),
  event_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  note             TEXT    NOT NULL,
  supersedes_state_id INTEGER REFERENCES core_action_item_state (state_id),
  receipt_id       INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id)
) STRICT;

------------------------------------------------------------------------------
-- Notes: narrative feed entries no other table derives
------------------------------------------------------------------------------
CREATE TABLE core_note (
  note_id          INTEGER PRIMARY KEY,
  tag              TEXT    NOT NULL CHECK (tag IN ('applications', 'forensics', 'audits', 'research-chain', 'surfaces', 'build')),
  title            TEXT    NOT NULL CHECK (length(title) > 0),
  body             TEXT    NOT NULL CHECK (length(body) > 0),
  event_instant_id INTEGER NOT NULL REFERENCES core_instant (instant_id),
  application_id   INTEGER REFERENCES core_application (application_id),
  artifact_id      INTEGER REFERENCES core_artifact (artifact_id),
  supersedes_note_id INTEGER REFERENCES core_note (note_id),
  receipt_id       INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK (instr(title, char(8212)) = 0 AND instr(body, char(8212)) = 0)
) STRICT;

------------------------------------------------------------------------------
-- Claims: two axes, never conflated (verdict; evidence class)
------------------------------------------------------------------------------
CREATE TABLE core_claim (
  claim_id       INTEGER PRIMARY KEY,
  subject_label  TEXT    NOT NULL CHECK (length(subject_label) > 0),
  claim_text     TEXT    NOT NULL CHECK (length(claim_text) > 0),
  source_quote   TEXT    NOT NULL,
  artifact_state TEXT    NOT NULL CHECK (artifact_state IN ('JOINED', 'UNJOINED')),
  artifact_id    INTEGER REFERENCES core_artifact (artifact_id),
  supersedes_claim_id INTEGER REFERENCES core_claim (claim_id),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((artifact_state = 'JOINED') = (artifact_id IS NOT NULL)),
  CHECK (artifact_state = 'UNJOINED' OR length(source_quote) > 0)
) STRICT;

CREATE TABLE core_audit_run (
  audit_run_id     INTEGER PRIMARY KEY,
  run_instant_id   INTEGER NOT NULL REFERENCES core_instant (instant_id),
  scope            TEXT    NOT NULL CHECK (length(scope) > 0),
  worker_set_state TEXT    NOT NULL CHECK (worker_set_state IN ('STATED', 'UNKNOWN')),
  worker_set       TEXT,
  receipt_id       INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  CHECK ((worker_set_state = 'STATED') = (worker_set IS NOT NULL AND length(worker_set) > 0)),
  CHECK (worker_set_state = 'STATED' OR worker_set IS NULL)
) STRICT;

-- Stored verdict status is shown verbatim (DL-5, R20).
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

-- While RECON-ECLASS is UNADMITTED only ABSTENTION rows are admissible.
CREATE TABLE core_claim_eclass (
  eclass_id      INTEGER PRIMARY KEY,
  claim_id       INTEGER NOT NULL REFERENCES core_claim (claim_id),
  contract_id    TEXT    NOT NULL,
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

-- Counts reported by an audit, stored as reported (R8). Not derived.
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
  reported_status TEXT   NOT NULL CHECK (reported_status IN ('CONFIRMED', 'KILLED', 'DOWNGRADED', 'UNRESOLVED')),
  delta          TEXT    NOT NULL CHECK (length(delta) > 0),
  receipt_id     INTEGER NOT NULL UNIQUE REFERENCES meta_receipt (receipt_id),
  UNIQUE (audit_run_id, claim_id)
) STRICT;

------------------------------------------------------------------------------
-- Cross-table invariants
------------------------------------------------------------------------------
CREATE TRIGGER core_verdict_unjoined_is_unresolved BEFORE INSERT ON core_verdict
WHEN NEW.status <> 'UNRESOLVED'
 AND (SELECT artifact_state FROM core_claim WHERE claim_id = NEW.claim_id) = 'UNJOINED'
BEGIN SELECT RAISE(ABORT, 'core_verdict: claim has no artifact; only UNRESOLVED is admissible'); END;

CREATE TRIGGER core_claim_eclass_needs_admitted_contract BEFORE INSERT ON core_claim_eclass
WHEN NEW.state = 'ADMITTED'
 AND (SELECT status FROM v_contract_head WHERE contract_id = NEW.contract_id) IS NOT 'ADMITTED'
BEGIN SELECT RAISE(ABORT, 'core_claim_eclass: contract not admitted; only ABSTENTION(CLASSIFIER_NOT_ADMITTED)'); END;

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
CREATE TRIGGER core_application_term_supersedes_same_key BEFORE INSERT ON core_application_term
WHEN NEW.supersedes_term_id IS NOT NULL
 AND (SELECT application_id || '/' || term_key FROM core_application_term WHERE term_id = NEW.supersedes_term_id)
     IS NOT (NEW.application_id || '/' || NEW.term_key)
BEGIN SELECT RAISE(ABORT, 'core_application_term: supersedes a term of another application or key'); END;
CREATE TRIGGER core_action_item_state_supersedes_same_item BEFORE INSERT ON core_action_item_state
WHEN NEW.supersedes_state_id IS NOT NULL
 AND (SELECT item_id FROM core_action_item_state WHERE state_id = NEW.supersedes_state_id) IS NOT NEW.item_id
BEGIN SELECT RAISE(ABORT, 'core_action_item_state: supersedes a state of another item'); END;

------------------------------------------------------------------------------
-- Access paths for the head-at-cut queries (experiments/head_selection.py)
------------------------------------------------------------------------------
CREATE INDEX core_application_state_by_app ON core_application_state (application_id, state_id);
CREATE INDEX core_application_state_by_sup ON core_application_state (supersedes_state_id);
CREATE INDEX core_application_term_by_app ON core_application_term (application_id, term_key, ordinal);
CREATE INDEX core_application_term_by_sup ON core_application_term (supersedes_term_id);
CREATE INDEX core_blocker_state_by_blocker ON core_blocker_state (blocker_id, state_id);
CREATE INDEX core_blocker_state_by_sup ON core_blocker_state (supersedes_state_id);
CREATE INDEX core_action_item_by_app ON core_action_item (application_id);
CREATE INDEX core_action_item_by_blocker ON core_action_item (blocker_id);
CREATE INDEX core_action_item_state_by_item ON core_action_item_state (item_id, state_id);
CREATE INDEX core_action_item_state_by_sup ON core_action_item_state (supersedes_state_id);
CREATE INDEX core_note_by_sup ON core_note (supersedes_note_id);
CREATE INDEX core_verdict_by_claim ON core_verdict (claim_id, verdict_id);
CREATE INDEX core_verdict_by_sup ON core_verdict (supersedes_verdict_id);
CREATE INDEX core_claim_eclass_by_claim ON core_claim_eclass (claim_id, eclass_id);
CREATE INDEX core_claim_eclass_by_sup ON core_claim_eclass (supersedes_eclass_id);
