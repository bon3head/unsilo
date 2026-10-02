# UnSilo dashboard schema (proposed, 2026-10-02)

Status: PROPOSED DESIGN ARTIFACT for operator review. Not approved. No UI, routes, or templates exist. Build authorization: NONE.

Blockers lead (dashboard track): U-DASH-01 namespace ruling, U-DASH-02 receipt chain ruling, U-DASH-08 receipt image ruling, U-DASH-07 real Duolingo packet format. Owner of every ruling: operator. Falsifier for each: listed in section 9.

## 0. Files

| Path | What | Generated? |
|---|---|---|
| `migrations/0001_meta.sql` | file identity pragmas, migration ledger, receipt ledger, declared cuts, contract status | hand-written |
| `migrations/0002_staging.sql` | `stg_*` staging namespace | hand-written |
| `src/0003_core_tables.sql` | `core_*` tables, CHECKs, cross-table triggers, indexes | hand-written |
| `tools/gen_0003.py` | emits `migrations/0003_core.sql` = src + receipt-first and append-only triggers | generator |
| `migrations/0003_core.sql` | the migration actually applied | generated, hash in `MIGRATIONS.sha256` |
| `migrations/0004_views_fts.sql` | views, `feed_item`, FTS5 projection | hand-written |
| `tools/build_fixtures.py` | emits the three fixtures with real SHA-256 receipts, fixed timestamps | generator |
| `fixtures/*.sql` | Duolingo walk, B4 regression, B1 retraction | generated, hash in `FIXTURES.sha256` |

Reproduce and check:

```
cd schema
python3 tools/gen_0003.py && python3 tools/build_fixtures.py
(cd migrations && sha256sum -c ../MIGRATIONS.sha256)
(cd fixtures && sha256sum -c ../FIXTURES.sha256)
```

Apply (runner contract, section 2.3), using the sqlite3 CLI for a manual check:

```
rm -f /tmp/u.db && for f in migrations/000*.sql; do sqlite3 /tmp/u.db < "$f"; done
sqlite3 /tmp/u.db < fixtures/duolingo_promotion_walk.sql
sqlite3 /tmp/u.db "PRAGMA foreign_keys=ON; PRAGMA integrity_check; PRAGMA foreign_key_check;"
```

The manual loop above does not write `meta_migration` rows; the runner does (2.3).

## 1. What was verified, and how

All checks were executed against Python's bundled SQLite 3.45.1 (floor is 3.37.0 per S6; rusqlite `bundled` at HEAD 91f876c ships 3.53.4). Evidence class of each result: DD, deterministic re-execution of the files above.

- All four migrations apply; `integrity_check = ok`; `foreign_key_check` empty; `application_id = 1431196492`; `user_version = 1`; `page_size = 4096`; `journal_mode = wal`; every non-FTS table is STRICT.
- Duolingo walk: results in 7.4.
- 26 adversarial writes blocked: UPDATE/DELETE on core, staging, receipts; core row with no receipt; broken receipt chain; receipt time going backwards; REAL into INTEGER; point time UNBOUNDED; KNOWN endpoint with NULL value; UNKNOWN endpoint carrying a value; empty `[t,t)`; mixed-granularity KNOWN interval; UNBOUNDED with no basis text; `2026-02-31`; SECOND value outside UTC; non-10-digit CIK; em dash in a note; falsifier UNKNOWN with text present; CONFIRMED verdict on an UNJOINED claim; ADMITTED evidence class under an UNADMITTED contract; promoting a MALFORMED candidate. Each constraint-level attack was re-run with a valid receipt in place so the CHECK itself fired, not the receipt trigger.
- Leap second `2016-12-31T23:59:60Z` accepted (S3: preserve, never clamp).
- B4 regression: section 8. B1 retraction: section 6.5.

Not verified: behavior under rusqlite, tokio-rusqlite, or a musl binary (no Rust code exists by design); concurrency; performance.

## 2. Physical layout and connection profile

### 2.1 One file, namespaced tables (CORRECTION to the data theory)

The data theory says "one SQLite file, two schemas: staging and core". SQLite cannot do that. A schema name in SQLite (`staging.x`) names an attached database, which is a separate file. Executed: `CREATE TABLE staging.t(x)` on a single file fails with `unknown database staging`; a foreign key naming another attached database fails to parse. Two attached files would also lose foreign keys from core back to staging and lose atomic commit across files in WAL mode.

This schema keeps ONE file and makes the split a name namespace: `meta_*` (identity, ledgers, cuts), `stg_*` (staging), `core_*` (promoted), `v_*` and `feed_item` (views), `fts_*` (disposable index). This is a proposed spec edit (U-DASH-01). The alternative is two files with no cross-file FKs.

### 2.2 Connection profile (S6, retained B11)

File-level, set by 0001 and persisted: `page_size=4096` (before any table), `journal_mode=WAL`, `application_id=1431196492` (`0x554E534C`, "UNSL"), `user_version=1`.

`user_version` is held at 1 = physical schema generation 1, as S6 states. The migration count lives in `meta_migration`. This reading is recorded as U-DASH-12.

Per connection, every time, then read back (not persisted by SQLite): `foreign_keys=ON` (read back must be 1), `synchronous=FULL`, `trusted_schema=OFF`, `busy_timeout=5000`. Analytics connections: `mode=ro` and `query_only=ON`. Writer: `mode=rw`, never `rwc` except explicit bootstrap.

Note: rusqlite's bundled build compiles SQLite with `-DSQLITE_DEFAULT_FOREIGN_KEYS=1` (`libsqlite3-sys/build.rs:158` at HEAD 91f876c). The per-connection set-and-read-back stays mandatory; it is what S6 freezes, and the default does not hold for non-bundled builds.

Startup order (S6): open, set pragmas, read back, check `application_id` and `user_version`, check every `meta_migration.sha256` against the migration file bytes, check STRICT manifest, `PRAGMA integrity_check` = `ok`, `PRAGMA foreign_key_check` empty, then SERVABLE. Any failure halts. A halted store serves nothing: no partial panels, no cached results.

### 2.3 Migration runner contract

For each file `NNNN_name.sql` in order: compute SHA-256 of the exact bytes, then in ONE transaction apply the file and insert `(NNNN, name, sha256, applied_at)` into `meta_migration`. Triggers make the ledger append-only and contiguous. Forward-only: there is no down migration. Core tables change only by a new migration.

## 3. Temporal layer and the frozen B4 contract

### 3.1 What is frozen, and what this file can and cannot see

The frozen B4 contract text lives in repair chats, not in this repo. What the repo establishes (ledger `triage-state-2026-10-01.md`, 2:12 to 2:29 AM ET entries; master doc section 6; S3/S10 digests):

- Typed bound domain `KNOWN(v) | UNBOUNDED | UNKNOWN`, per endpoint.
- Admissible completions: UNKNOWN goes to a finite value, UNBOUNDED stays infinite.
- Universal entailment: TRUE iff every completion entails the relation, FALSE iff every completion entails its negation, else UNKNOWN. Not Kleene. Not a 9999-12-31 sentinel.
- Decision procedure (rework, chat 6abdfc6f): normalize endpoints, build a finite constraint set, enumerate finite total-order extensions of the endpoint variables, evaluate the relation per extension.
- Point times are never UNBOUNDED. Half-open `[from, to)`. Effective time and knowledge time are separate. KNOWN is at the evidence's own granularity; date-only is a calendar-day granule, never synthesized to midnight UTC.
- The worker's normative Allen definitions use non-strict variants (BEFORE: `A.end <= B.start`; CONTAINS: `B.end <= A.end`). This schema implements no Allen relation (3.5).

### 3.2 Encoding

- `core_instant`: point time. `kind IN (KNOWN, UNKNOWN)`. KNOWN carries `(value, gran, zone)`; UNKNOWN carries none of them. `source_text` keeps the source wording.
- `core_interval`: `[from, to)`, each endpoint a `(kind, value, gran, zone)` tuple. The `kind` column is NOT NULL, so NULL in `value` never carries meaning by itself. UNBOUNDED requires non-empty `unbounded_basis` (S3: UNBOUNDED is affirmative source semantics, never inferred from a missing field; "until filled" is not unbounded).
- Granularity: `DAY` (value `YYYY-MM-DD`, zone = civil calendar zone, e.g. `America/New_York`) or `SECOND` (value `YYYY-MM-DDTHH:MM:SSZ`, zone `UTC`). Date validity uses `date(v) IS v` so an invalid date cannot pass through NULL.
- Knowledge time is `meta_receipt.recorded_at`. Cuts are rows in `meta_cut`; every view is evaluated per declared cut and never reads the clock (S8).

### 3.3 Point membership, derived

`v_interval_membership` answers: is effective cut T in `[from, to)`? Derivation from the frozen principle (my derivation, not the frozen oracle text): membership = `from <= T AND T < to` over every admissible completion; the only completion constraint is interval validity `from < to`; under the total-order-extension procedure an UNKNOWN endpoint can take any position consistent with that constraint.

| from | to | Result | Why |
|---|---|---|---|
| KNOWN(f), f > T | any | FALSE | lower bound fails in every completion |
| any | KNOWN(t), T >= t | FALSE | upper bound fails in every completion |
| KNOWN(f) or UNBOUNDED, f <= T | KNOWN(t) or UNBOUNDED, T < t | TRUE | fully determined |
| KNOWN(f), f = T | UNKNOWN | TRUE | every completion has t > f = T |
| KNOWN(f), f < T | UNKNOWN | UNKNOWN | t may land in `(f, T]` or above T |
| UNBOUNDED | UNKNOWN | UNKNOWN | t is any finite value |
| UNKNOWN | KNOWN(t), T < t | UNKNOWN | f may land in `(T, t)` or at or below T |
| UNKNOWN | UNBOUNDED | UNKNOWN | f is any finite value |
| UNKNOWN | UNKNOWN | UNKNOWN | both split |

The row "KNOWN(f), f = T / UNKNOWN = TRUE" is where this differs from Kleene logic (Kleene: TRUE AND UNKNOWN = UNKNOWN). The rows with UNBOUNDED and a KNOWN partner are where it differs from the superseded S3 blanket rule.

Dense versus discrete completions (U-DASH-04): if completions ranged over day granules instead of order positions, "UNKNOWN / KNOWN(t) with T = t minus one day" would become TRUE. The ledger's procedure enumerates order extensions, which is the dense reading, and this view follows it. Confirm against the frozen oracle text in chat 6abdfc6f.

### 3.4 Granularity gap (conservative, OPEN)

Cross-granularity lifting is not implemented. Any KNOWN endpoint whose granularity or zone differs from the cut returns UNKNOWN with reason `GRANULARITY_NOT_LIFTED`, and a KNOWN-KNOWN interval with mixed granularity is refused at write time. This never overclaims, but it can return UNKNOWN where the frozen rule ("TRUE only if true under every compatible interpretation") would return a determinate answer. Recorded as U-DASH-03 and U-DASH-14.

### 3.5 Not implemented

Allen relations between two intervals, RestrictTime, and any B1/B9 operator. The dashboard needs only point membership at declared cuts. Implementing relation oracles here would mean writing frozen B4 clause detail that this repo does not contain.

## 4. Claims, both axes, and the feed

### 4.1 Two axes, never conflated

- Audit-verdict axis: `core_verdict` rows (`CONFIRMED`, `KILLED`, `DOWNGRADED`, `UNRESOLVED`) with history via `supersedes_verdict_id`.
- Evidence-class axis: `core_claim_eclass` rows (`PD`, `AO`, `DD`, `QN`, `UR`, `weak` modifier). While `RECON-ECLASS-PD-AO-DD-v2.0` is UNADMITTED in `meta_contract_status`, a trigger allows only `ABSTENTION` rows, so the axis renders `ABSTENTION(CLASSIFIER_NOT_ADMITTED)`. Admission is a new migration that changes the status row.
- `v_claim_effective` exposes `verdict_axis` and `eclass_axis` side by side. A claim with no artifact row is `UNRESOLVED` with basis `NO_ARTIFACT` by construction (view), and a trigger refuses any other verdict for it (write path).
- Stored status is `UNRESOLVED` (data theory, audit record). The spec's pill label is `UNKNOWN`. Which label renders is U-DASH-05.

### 4.2 feed_item

A VIEW, never a table; its output is never stored. One row per (cut, item). Sources: `core_note`, `core_verdict`, `core_application_state`, `core_audit_run`. Order: `(cut_id, KNOWN before UNKNOWN time, time value, item_kind, item_id)`. Items with UNKNOWN time are kept, placed after KNOWN ones, never dropped.

### 4.3 Ordering caveat

SQLite does not promise that a view's ORDER BY survives into an outer query. Panels must state their own ORDER BY (parked proposal (g)). Cross-granularity ordering in the feed (a DAY value next to a SECOND value) is a display order only, never a temporal relation.

### 4.4 FTS5

`fts_feed` is rebuilt from `feed_item` at the end of each promotion run (`DELETE` then `INSERT ... SELECT`). It is never written from staging. It has no authority: destroying it destroys no evidence, and no count, verdict, or absence claim may depend on a hit, a miss, or rank (S6). FTS5 tables cannot be STRICT.

## 5. Absence as signal

### 5.1 Expectation rows

`core_expectation` says what should exist, for which subject, in which window (`core_interval`), on what basis, checked in which dataset (`checked_scope`). `core_expectation_state` records `NOT_EVALUATED`, `FULFILLED`, `NOT_OBSERVED`, `LATE`, `REFUTED` over time. `NOT_OBSERVED` means not observed in `checked_scope`; it is not QN (B5/B6 prerequisites are not modeled) and never renders as "does not exist". The view `v_expectation_loudest` carries the caveat text on every row.

### 5.2 CORRECTION: no probability column

The data theory orders absences by `expected_probability DESC`. The standing rules say categorical only, no numerical probability-style confidence. This schema replaces it with a categorical `basis` (`MANDATED`, `STATED`, `ROUTINE`, `OPERATOR`) and orders loudest-first by that rank. Shannon's point survives as ordering by how strongly the record says the thing should exist, not as a number. U-DASH-09.

## 6. Receipts and determinism

### 6.1 Receipt first

Every `core_*` row carries `receipt_id` (UNIQUE, FK). A BEFORE INSERT trigger requires a receipt that already exists and names the same table, the same primary key, and `op = INSERT`. The receipt therefore lands before the mutation, in the same transaction. Core is append-only: UPDATE and DELETE abort on every core table, the receipt ledger, and staging.

### 6.2 Hash definitions (used by `tools/build_fixtures.py`)

- `after_image_json` = canonical JSON of the full row: keys sorted, separators `,` and `:`, UTF-8, no ASCII escaping.
- `after_sha256` = SHA-256 of `after_image_json` bytes.
- `receipt_sha256` = SHA-256 of canonical JSON of `{receipt_id, table_name, row_pk, op, actor, reason, promotion_run_id, before_kind, before_sha256, after_sha256, prev_kind, prev_receipt_sha256, recorded_at}`.

SQLite core has no SHA-256 SQL function, so the database checks hash shape and chain linkage only. It does not recompute content hashes. Recomputing in-transaction is parked proposal (f).

### 6.3 Chain

`prev_kind = GENESIS` iff the ledger is empty; otherwise `prev_receipt_sha256` must equal the current head. `receipt_id` must be `max + 1`; `recorded_at` must not go backwards. Chaining conflicts with harness spec v1.2, which cut its ledger hash chain; the launch prompt describes the dashboard ledger as hash-chained. Ruling: U-DASH-02.

### 6.4 CORRECTION: replay needs images, not just hashes

The data theory says repair = replay the ledger, with receipts holding before and after hashes. A hash cannot be replayed. Each receipt therefore also stores `after_image_json`. Rebuilding core = replaying `after_image_json` in `receipt_id` order and checking each `after_sha256`. U-DASH-08.

### 6.5 Mutation, repair, repair of a repair

Since core is append-only, all three are inserts:

1. Mutation: insert a new row whose `supersedes_*_id` names the old row, with its own receipt.
2. Repair: insert another row superseding the bad one; reason names the defect.
3. Repair of a repair: insert a third row superseding the repair.

The ledger bounds all three; no row is edited. Views pick heads per knowledge cut. Two unsuperseded heads for one subject are both shown (`head_count > 1`), never a silent pick.

Executed (`fixtures/b1_retraction_bitemporal.sql`): research-chain B1 recorded `FROZEN` at 08:38Z (4:38 AM ET), then `REPAIRED_PENDING_ADMISSION` superseding it at 11:00Z (7:00 AM ET). Knowledge cut 09:00Z returns `FROZEN`; knowledge cut 12:00Z returns `REPAIRED_PENDING_ADMISSION`; the strip at the later cut shows only the latter. The superseded row stays in the file. These recording times are illustrative: in a real store, `recorded_at` is when UnSilo learned the fact.

## 7. Duolingo-format staging ingest and promotion, walked by hand

### 7.1 Sources of every value

The real Duolingo packet file is not in the pack (U-DASH-07), so the walk uses an ILLUSTRATIVE packet whose rows restate pack facts only:

- Duolingo, req 1265, submitted 2026-09-29: feed spec, Applications item 1.
- `CIK0001562088`, "Duolingo, Inc.", 776 recent filings: `research-chain/poc-results-2026-09-30.md`, P2.
- "Duolingo careers requires JS": `research-chain/s2-output-2026-09-30.md`, Careers acquisition.

### 7.2 Shape

`stg_ingest_batch` (one row per file, SHA-256 of exact bytes) → `stg_raw_row` (each record verbatim, per-row SHA-256) → `stg_candidate` (parser id and version, candidate kind, `parse_state` in `PARSED`, `PARTIAL`, `MALFORMED`, `NOT_APPLICABLE`, payload JSON, missing-fields list) → `stg_promotion_decision` (`PROMOTE`, `HOLD`, `REJECT` per rule version) → `core_promotion_run` and `core_promotion_link` (each promoted core row linked to its staging decision by receipt).

Staging is append-only. A changed file is a new batch. A missing field is listed in `missing_fields_json`, never defaulted.

### 7.3 Promotion rules, version 1

| Rule | Input | Decision | Effect |
|---|---|---|---|
| R-PARSE-1 | candidate `MALFORMED` or `NOT_APPLICABLE` | REJECT | trigger refuses PROMOTE for these states |
| R-DEDUPE-1 | `raw_sha256` equal to an earlier row in this batch or any promoted batch | REJECT | duplicate never reaches core |
| R-CO-1 | company name in candidate | exactly one `core_name_variant` exact match: use it. Zero: create company with `UNSILO_OPAQUE` key, unless a CIK binding artifact is in the corpus (then `CIK`). More than one: HOLD | no fuzzy match, ever (B8.2) |
| R-APP-1 | APPLICATION `PARSED` or `PARTIAL` | PROMOTE after R-CO-1 resolves | each missing field becomes its `*_state = UNKNOWN`; initial `SUBMITTED` state with interval `[submitted day, UNKNOWN)` |
| R-CLAIM-1 | CLAIM | PROMOTE | `JOINED` iff its cited source file is a `core_artifact`; else `UNJOINED`. Default verdict row `UNRESOLVED`; default evidence-class row `ABSTENTION(CLASSIFIER_NOT_ADMITTED)` |

### 7.4 Result of the walk (executed)

| Candidate | Raw row | Parse | Decision | Core result |
|---|---|---|---|---|
| 1 | APPLICATION req 1265 | PARTIAL (platform, role, location missing) | PROMOTE R-APP-1 | application 1: req `1265` STATED; platform, role, location UNKNOWN; state SUBMITTED from DAY 2026-09-29 ET |
| 2 | CLAIM CIK, 776 filings | PARSED | PROMOTE R-CLAIM-1 | claim 1 `UNJOINED` (raw P2 output missing, U-1R-AUTH-013): verdict axis `UNRESOLVED` basis `NO_ARTIFACT`; eclass axis `ABSTENTION(CLASSIFIER_NOT_ADMITTED)` |
| 3 | CLAIM careers needs JS | PARSED | PROMOTE R-CLAIM-1 | claim 2 `JOINED` to the S2 digest artifact; verdict `UNRESOLVED` (a digest proves only what it says); eclass ABSTENTION |
| 4 | APPLICATION `req=` empty | MALFORMED | REJECT R-PARSE-1 | none |
| 5 | duplicate of row 1 | PARTIAL | REJECT R-DEDUPE-1 | none |

Company: `us-co-duolingo` (`UNSILO_OPAQUE`). The CIK stays a claim, not a key, because no PublisherIdentityBinding artifact is in the corpus.

Application membership at declared cuts: at effective cut 2026-09-29 the SUBMITTED state is `TRUE` (cut equals the known start); at 2026-10-02 it is `UNKNOWN`, because an unseen later change cannot be ruled out. That is the correct reading of an open status with an unknown end.

Absence row: expectation "recruiter reply for req 1265", basis `OPERATOR` (no reply SLA in the pack), checked scope "operator inbox as recorded in UnSilo", state `NOT_EVALUATED`.

Knowledge cut 11:59:59Z (one second before the run's receipts) shows nothing from core: the promotion is invisible before it was recorded.

### 7.5 Gaps found by the walk (now OPEN)

- U-DASH-07: real packet format unknown; the parser in the walk is a stand-in.
- R-DEDUPE-1 compares raw row hashes only. Two differently formatted rows describing the same application pass dedupe and would hit R-APP-1 twice. Identity of an application across rows (company plus req) needs a rule; proposed: HOLD when an application with the same company and req exists.
- R-CO-1 needs the operator to say whether "Duolingo" in a packet is the same publisher as the EDGAR filer before the CIK can become the key (B8 binding evidence).

### 7.6 FTS on promotion

The walk ends by rebuilding `fts_feed`. A search for `rendering` returns claim 2's verdict item at both cuts. Staging rows are never indexed.

## 8. B4 regression (executed, `fixtures/b4_regression.sql`)

Cut: DAY 2026-10-02 ET. Old design: one nullable `valid_to` column.

| # | from | to | Old A: `valid_to IS NULL` read as open | Old B: NULL dropped by WHERE | S3 blanket rule | This schema |
|---|---|---|---|---|---|---|
| 1 | K 2026-09-29 | UNKNOWN | TRUE (freezes unknown as open) | dropped | UNKNOWN | UNKNOWN |
| 2 | K 2026-10-02 | UNKNOWN | TRUE | dropped | UNKNOWN | TRUE |
| 3 | UNBOUNDED | K 2026-10-05 | dropped | dropped | UNKNOWN | TRUE |
| 4 | UNKNOWN | K 2026-10-05 | dropped | dropped | UNKNOWN | UNKNOWN |
| 5 | UNKNOWN | K 2026-10-01 | dropped | dropped | UNKNOWN | FALSE |
| 6 | K 2026-09-01 | UNBOUNDED | TRUE | dropped | UNKNOWN | TRUE |
| 7 | K 2026-10-03 | UNKNOWN | dropped | dropped | UNKNOWN | FALSE |
| 8 | UNBOUNDED | UNBOUNDED | dropped | dropped | UNKNOWN | TRUE |
| 9 | UNKNOWN | UNKNOWN | dropped | dropped | UNKNOWN | UNKNOWN |
| 10 | K 2026-09-01 | K 2026-10-02 | dropped | dropped | FALSE | FALSE |

Old A cannot tell row 1 (unknown end) from row 6 (unbounded end): both read as open, which is the freeze. Old B drops every row that has a NULL. The S3 rule returns UNKNOWN for rows 2, 3, 5, 6, 7, and 8, which are determinate. This schema cannot store row 1 and row 6 the same way: they differ in `to_kind`, and the kind column is NOT NULL.

## 9. Open unknowns raised by this schema

Each needs an operator ruling unless noted. Falsifier = what would close it.

| ID | Question | Current choice | Closes when |
|---|---|---|---|
| U-DASH-01 | One file with name prefixes, or two attached files? | one file, prefixes | operator ruling on the spec edit |
| U-DASH-02 | Hash-chain receipts (launch prompt) or no chain (harness v1.2 cut)? | chained | operator ruling |
| U-DASH-03 | Cross-granularity lifting in membership | not lifted; UNKNOWN | a lifting rule written from the frozen B4 text and tested |
| U-DASH-04 | Dense or discrete completion domain | dense (order extensions) | frozen oracle text in chat 6abdfc6f opened and compared |
| U-DASH-05 | Pill label for stored UNRESOLVED | not decided | operator ruling (UNKNOWN per spec, or UNRESOLVED per audit record) |
| U-DASH-06 | Which research-chain states show on the blockers strip | non-terminal = all except FROZEN, CLOSED | operator ruling |
| U-DASH-07 | Real Duolingo packet format | stand-in parser | the packet file lands in the corpus |
| U-DASH-08 | Receipts carry `after_image_json` | yes | operator ruling on the data-theory edit |
| U-DASH-09 | Categorical expectation basis instead of probability | categorical | operator ruling |
| U-DASH-10 | Add REJECTED and WITHDRAWN application statuses | added | operator ruling (needed for the rerun's open, rejected, reopened case) |
| U-DASH-11 | Approximate times ("~9:31 PM ET") | KNOWN at DAY plus verbatim source text | operator ruling; minute precision is not claimed |
| U-DASH-12 | `user_version` = generation 1, migrations counted in `meta_migration` | as stated | operator confirms the S6 reading |
| U-DASH-13 | Audit counts: 9 + 31 + 188 + 127 = 355, not 555 | stored as reported; `v_audit_count_check` shows rows held | audit export opened; the other 200 accounted for |
| U-DASH-14 | Mixed-granularity KNOWN intervals refused at write | refused | same as U-DASH-03 |

## 10. Normal form notes (core)

Each core table has one candidate key besides `receipt_id` (also unique, but a pure function of the row's write event), and every non-key attribute depends on the whole key:

- `core_company`: `company_id → key_kind, company_key`; `company_key → company_id` (second candidate key). BCNF.
- `core_name_variant`: `variant_id → ...`; `(company_id, variant)` unique. A variant string mapping to two companies is two rows, which is the ambiguity B8 requires surfacing, not a normalization defect.
- `core_claim`, `core_verdict`, `core_claim_eclass`: claim text, verdict status, and evidence class change on different schedules and are separate tables (data theory 3).
- `core_application` holds only attributes fixed for the application; status and terms are separate tables because they change over time.
- `core_blocker` vs `core_blocker_state`: identity vs lifecycle; `(program, code)` is the business key.
- Interval and instant values are factored into `core_interval` and `core_instant` so the B4 constraints are written once.

Build authorization: NONE
