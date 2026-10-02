# UnSilo data theory — relational design (2026-10-02)

Theory only. No implementation. Claude implements later from this.

## 1. What the database is
One SQLite file (his stack: SQLite-first, local-first). Two schemas in one file:
`staging` (raw, tentative, Duolingo-style partial data lands here) and `core`
(promoted, verified, auditable). Promotion staging->core is an explicit,
receipted transition, never silent. This is what makes tentative data
transferable and upgradable to v1: partial rows live in staging with their
provenance; v1 hardens the promotion rules, not the tables.

## 2. Entity inventory (core)
- company (canonical entity; one row per real-world company, never per name variant)
- name_variant (company_id, variant string, source) — entity resolution lives here
- filing (company_id, filing_type, accession/id, filed_at, artifact_hash)
- claim (the atomic unit: one checkable assertion, source quote, artifact ref)
- verdict (claim_id, status in {confirmed, killed, downgraded, unresolved},
  decided_at, decided_by, rationale) — verdicts are ROWS, not columns, so a claim
  can carry a verdict history
- blocker (title, status open/closed, falsifier, owner, opened_at, closed_at)
- application (company_id, role, platform, req_id, status, applied_at, terms)
- action_item (application_id or blocker_id, text, owner, due, done)
- audit_run (worker set, date, scope) + audit_finding (audit_run_id, claim_id, delta)
- artifact (sha256, path, captured_at) — every file the intel rests on, content-addressed
- expectation (what SHOULD exist: e.g. "Form D filing for Q3") with fulfillment
  status — absence-as-signal made relational (section 5)

## 3. Normalization posture
- Core is 3NF/BCNF: no repeating groups, every non-key attribute depends on the
  key, the whole key, nothing but the key. Claim text, verdict status, and
  provenance are separate tables because they change on different schedules and
  for different reasons.
- The feed read path is a deliberately denormalized VIEW (feed_item), not a
  table: joins computed at query time, so the write side stays normalized and
  the read side stays fast. Never store the view's output.
- Name variants, salary figures, filing amounts: never merge entities in a
  string column (the TikTok 4-entity ILIKE merge was a kill). Entity boundaries
  are rows in name_variant with explicit mapping decisions, each dated.

## 4. Temporal modeling (bears directly on open blocker B4)
- Bitemporal tables where it matters: valid_time (when the claim was true in the
  world) vs transaction_time (when we recorded it). Claim lifespans, filing
  coverage windows, application statuses all get both.
- Interval discipline from Allen's algebra: before/meets/overlaps/during etc.
  are the vocabulary; the B4 failure was UNBOUNDED and UNKNOWN intervals being
  frozen as if bounded. Rule: an interval endpoint is either a timestamp or an
  explicit marker (UNBOUNDED_FUTURE / UNKNOWN), never NULL meaning two things.
  NULL means "not recorded"; unknown endpoints get their own marker values.
- Open intervals stay open: a still-open application has no closed_at, and every
  query that touches it must handle the open case explicitly. The freeze bug was
  treating open as closed; the schema makes that unrepresentable.

## 5. Absence as signal, relationally
- expectation table: (entity_id, expected_artifact_type, expected_window,
  status in {fulfilled, missing, late, refuted}). A missing Form D where the
  calendar says one should exist is a ROW with status=missing, not an empty
  result set. Surprise is queryable: ORDER BY expected_probability DESC,
  status=missing gives the loudest absences first (Shannon: most surprising
  event carries the most bits).
- Caveat encoded as a view comment, not a constraint: absence from a dataset
  is not evidence of absence in the world. The expectation row records the
  dataset it is missing FROM.

## 6. Receipts and determinism (his DVD doctrine)
- Append-only receipt ledger: every mutation to core writes a receipt row
  (before-image hash, after-image hash, actor, reason) BEFORE the mutation
  lands. Repair = replay the ledger, never edit history.
- artifact.sha256 is the join key between the database and the file corpus.
  A claim that cannot join to an artifact row is UNRESOLVED by construction.
- Deterministic feed: feed_item view orders by (event_time, id). No
  nondeterministic ordering, no LIMIT without ORDER BY. Same bytes in, same
  rows out.

## 7. Indexing and search (SQLite)
- Indexes on the feed's access paths: (event_time DESC), (company_id,
  event_time), (status) on blockers/applications, (verdict status) on claims.
- FTS5 virtual table over claim text + feed bodies for the dashboard search box.
  FTS index rebuilt on promotion, never on raw staging writes.
- WAL mode, single writer (Cipher), foreign keys enforced. No concurrent
  writers; the fleet reads replicas or the same file read-only.

## 8. Migration discipline (tentative -> v1)
- schema_version table, one row, integer. Migrations are numbered, forward-only,
  hash-receipted. Staging tables may change freely; core tables change only by
  migration.
- The Duolingo tentative structure: ingest lands in staging.duolingo_raw with
  source-file provenance; promotion rules (dedupe, entity-resolve, verdict
  attach) are documented per-table and versioned. When the full Duolingo pass
  lands, it replays through the same promotion path — no parallel schema.

## 9. Implementation stack (reconciled 2026-10-02, crawl + shootout)

Decision: **Rust**. Axum 0.8 + Askama + htmx (vendored, no build step);
rusqlite with `bundled` feature; PRAGMA journal_mode=WAL, foreign_keys=ON,
busy_timeout; DB access behind a dedicated thread or tokio-rusqlite (never
block the async runtime); interval endpoints as a Rust enum
(Timestamp / UnboundedFuture / Unknown); receipt ledger written in the same
transaction BEFORE the mutation; feed_item as a SQL VIEW ordered by
(event_time, id); target x86_64-unknown-linux-musl for the static binary.

Why it survived the crawl: the deciding factor was never velocity, it was B4.
Compiler-enforced interval markers beat schema CHECK constraints, and nothing
in the 16-repo survey overturned that. The crawl's two closest full
architectural templates are Go (glance, gatus), but what makes them good is
language-agnostic: config-driven UI, failure-isolated module registry,
verdict-pill grammar, per-panel staleness, query-backed panels. Those get
adopted as architecture, not as Go code. perspective (Rust-native,
Apache-2.0) independently reinforces the pick for the heavy audit-table
problem: virtualized datagrid, view-compiles-to-SQL.

License line: worldmonitor and glance are AGPL-3.0. Reimplement their
patterns, do not port their code. gatus and perspective are Apache-2.0.

Adopted patterns (from the crawl, as architecture):
- Config-driven UI: the dashboard is a config declaring feed sections, entity
  tables, blocker lists (glance pattern).
- Module registry: feed, verdicts, blockers, applications as independent
  modules with own refresh cadence and failure isolation (wtf pattern).
- Verdict pills as primary visual grammar: CONFIRMED / KILLED / DOWNGRADED /
  UNKNOWN (worldmonitor, gatus).
- Every number is a query you can open: panels trace to a SQL string
  (redash pattern). The dashboard is auditable by construction.
- Per-panel staleness: every lane shows its own freshness, a dead source
  never poses as fresh (worldmonitor, redash).
- Probe-history strip: per-claim evidence checks as a colored segment
  timeline, block characters in verdict colors (gatus pattern).
- Markdown + SQL as report source of truth for frozen briefings, so artifact
  history is hash-receipted by version control (evidence pattern).
- If a terminal-first surface is ever wanted, the Rust analog of wtf/tview
  is ratatui; the module-registry architecture carries over unchanged.
