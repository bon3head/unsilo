# UnSilo final grounding pass, before rulings (2026-10-02)

Research only. Nothing implemented; no baseline file changed. Build authorization: NONE.

## Blockers (lead)

| Blocker | Falsifier | Owner |
|---|---|---|
| Research chain: FROZEN B2 B3 B4 B7 B8; REPAIRED-PENDING-ADMISSION B1 B9; OPEN B10; RETAINED-INTEGRATION-VERIFIED B5 B6; RETAINED B11 B12; RECON-ECLASS UNADMITTED | master doc 7 remediation sequence | harness program |
| B1/B9 mirror quarantined: `pack/research-chain/part4-tail.md` SHA-256 `be9155fc64e1d064859a3c87c9c476877718420a5852fcc96dd60aa8e11b660f` (recomputed this pass; equals the operator's known-contaminated copy). Step 6 must not reuse parts 1 to 4 or `full-repair-output.txt` | byte match against the retained reports of `browser-task:4b530c82` | operator |
| One-pass ruling package: 8 corrections, proposals (a) to (g), U-DASH-01 to 14, stack | operator's written rulings | operator |

## Method and evidence rules

- "Opened" means read this pass, with file:line. Repo anchors are at commit `52509f5` on `claude/unsilo-dashboard-schema-b4-klcoqc`.
- External sources: git tags and commits (`git ls-remote`, shallow clones), npm registry metadata and tarballs (registry.npmjs.org, fetched 2026-10-02), crates.io API (fetched 2026-10-02), and SQLite's own source (the 3.53.4 amalgamation inside rusqlite HEAD 91f876c, `libsqlite3-sys/sqlite3/sqlite3.c` and `sqlite3.h`).
- sqlite.org itself was not reachable: the egress proxy refused `www.sqlite.org:443`. Every SQLite claim below rests on SQLite's source text and on executed tests under Python's SQLite 3.45.1, not on the website.
- Em dashes appear only inside verbatim quotes of pack files; they are the source's characters, kept for fidelity.
- Confidence: HIGH = executed or read in a primary artifact, with no plausible alternative reading; MEDIUM = primary text read, but it admits another reading, or it rests on a summary of a frozen contract; LOW = inference.
- License posture: the operator stated in this session (2026-10-02) that license issues are settled because this code will never be public or distributed. Licenses below are still read from the actual files, as the task asks. They do not gate any recommendation. The pack still says "AGPL: patterns only" (`pack/dashboard-crawl-report.md:323`; `pack/unsilo-claude-launch-prompt-2026-10-02.md:108, :178`). Until the ruling is written into the pack, the pack text and the ruling disagree on paper.

---

## A. The 8 Phase 1 corrections

These are the eight named in the Phase 1 chat summary. In the report they are C1 to C6, C9, and O5 (the last now U-DASH-13). The other report items (C7, C8, C10, C11, C12) are anchored in A9.

### A1. htmx 4.x exists (report C1)

- Baseline claim: "htmx 2.0.11 (4.x does not exist)" (`pack/unsilo-session-prompt-2026-10-02.md:245`; `pack/unsilo-session3-prompt-2026-10-02.md:266`).
- Evidence:
  - git tag `v4.0.0` at commit `4195bc0dc26b612ea5bea46f5914c6386eadeba3`, commit date 2026-08-28; its `package.json` reads `"version": "4.0.0"`.
  - npm `htmx.org`: `dist-tags = {latest: 2.0.11, next: 4.0.0}`; 4.0.0 published 2026-08-28T12:56:49Z; 2.0.11 published 2026-09-22T20:20:43Z.
  - Both tarballs' `LICENSE` files read "Zero-Clause BSD".
- Mechanism: 4.0.0 is published, but on the `next` channel; `latest` is still 2.0.11.
- Corrected claim: "pin 2.0.11, the current npm `latest`; 4.0.0 exists on `next`".
- Confidence: HIGH.
- What would change my mind: npm deprecating 4.0.0, or retagging it as `latest`.

### A2. One SQLite file cannot hold two schemas (report C2, U-DASH-01)

- Baseline claim: "One SQLite file ... Two schemas in one file" (`pack/unsilo-data-theory-2026-10-02.md:6`); also `pack/unsilo-session-prompt-2026-10-02.md:178`; `staging.duolingo_raw` (data theory :87).
- Mechanism, four independent facts:
  1. Executed, SQLite 3.45.1: `CREATE TABLE staging.t(x)` on a lone file fails with `unknown database staging`. A schema name only resolves to `main`, `temp`, or an ATTACHed database, and an attached database is a separate file.
  2. Executed: with `staging` attached, `CREATE TRIGGER main.t ... (SELECT ... FROM staging.dec ...)` fails with `trigger t cannot reference objects in database staging`.
     - Source: `sqlite3.c:126200-126214`: "These routines are used to make sure that an index, trigger, or view in one database does not refer to objects in a different database."
     - Consequence: a two-file design could not keep `core_promotion_link_needs_promote` (a trigger on core that reads a staging table).
  3. Executed: a foreign key naming `staging.p` fails to parse ("near '.': syntax error"); a foreign key's parent must be in the same database.
  4. Source: `sqlite3.c:90828-90844` (`vdbeCommit`). The `aMJNeeded[]` table maps `/* WAL */` to `0`, so a WAL database never counts toward the super-journal (`nTrans`). A commit spanning two WAL files therefore does not use the multi-file atomic path. A crash mid-commit can leave one file promoted and the other not.
- Corrected claim: one file with table-name namespaces (as proposed), or two files that lose cross-file triggers, foreign keys, and atomic promotion.
- Confidence: HIGH on 1 to 3 (executed). MEDIUM-HIGH on 4: source read, crash not reproduced.
- What would change my mind: a SQLite release that adds intra-file schemas, which none has.

### A3. The mirrored B1/B9 extraction is the contaminated copy (report C3)

- Baseline claim: "Their repair output (46,227 bytes, extracted verbatim to `b1b9-repair-extracted/`) stands as a valid repair candidate" (`pack/unsilo-master-architecture-prompt-2026-10-02.md:132`).
- Evidence:
  - `part4-tail.md:92` reads "Recovered authority or newly available evidence: NONE evaluated." This is deviation (c) per master doc :129.
  - `part4-tail.md:75`, the B9 admission open thread, has no "blocker/completion impact" clause, while the parallel B1 line at :74 has one. This is deviation (b).
  - The file's SHA-256 `be9155fc...b660f` matches the operator's known-contaminated copy.
  - `full-repair-output.txt` is 46,227 bytes and equals parts 1 to 4 minus the `[PARTn-...]` markers, so it carries the same deviations.
- Deviation (a), the split typed-expression line in Part 3, cannot be checked without the originals.
- Corrected claim: master doc 7's sentence applies to the retained reports in the browser task, not to these files. These files are quarantined.
- Confidence: HIGH.
- What would change my mind: the retained reports showing the same bytes, which would mean the "deviations" were in the originals.

### A4. Interval markers: the baseline set is too narrow (report C4)

- Baseline claims:
  - "explicit marker (UNBOUNDED_FUTURE / UNKNOWN)" (data theory :48).
  - "interval endpoints as a Rust enum (Timestamp / UnboundedFuture / Unknown)" (data theory :97-98).
  - Same at `pack/language-shootout-2026-10-02.md:208`, `pack/unsilo-claude-launch-prompt-2026-10-02.md:123`, and `pack/unsilo-session3-prompt-2026-10-02.md:209`.
- Frozen side:
  - B4 "typed bound domain `KNOWN(v) | UNBOUNDED | UNKNOWN`" (master doc :111).
  - Ledger rework worked example "Case S3-1 OVERLAPS=TRUE determinate (A=[UNBOUNDED-start, KNOWN(2024-06-01)), ...)" (`pack/research-chain/triage-state-2026-10-01.md:104`).
  - Granularity: "KNOWN(v): established at the evidence's own granularity; not arbitrary precision" (`pack/research-chain/s3-output-2026-09-30.md:5`).
- Mechanism:
  - A start endpoint has no marker at all in the baseline enum (`Timestamp` or nothing). So Case S3-1's interval A cannot be represented.
  - `Timestamp(i64)` carries no granularity, so a date-only value must be synthesized into an instant. Folklore kill #25 forbids exactly that.
- Corrected claim: each endpoint carries `KNOWN(value, granularity, zone) | UNBOUNDED | UNKNOWN`.
- Confidence: HIGH on the start-endpoint gap. MEDIUM on granularity, because the frozen B4 wording is summarized, not quoted (section C).

### A5. `expected_probability` violates the categorical rule (report C5, U-DASH-09)

- Baseline claim: "Surprise is queryable: ORDER BY expected_probability DESC" (data theory :58).
- Standing rules:
  - "No numerical probability-style confidence anywhere." (`README.md:18`)
  - "Categorical, never scores." (master doc :48)
- Mechanism: the column is a numeric probability that orders claims. Both texts forbid such a value. There is no third reading under which a probability column is not probability-style.
- Corrected claim: a categorical basis rank, as proposed.
- Confidence: HIGH that it conflicts.
- What would change my mind: an operator ruling that expectation ordering is exempt because it orders work, not claims. The texts contain no such exemption.

### A6. Replay needs after-images, not only hashes (report C6, U-DASH-08)

- Baseline claim: "every mutation to core writes a receipt row (before-image hash, after-image hash, actor, reason) BEFORE the mutation lands. Repair = replay the ledger, never edit history." (data theory :66-68)
- Mechanism: SHA-256 is one-way. A ledger holding only hashes can detect that a row differs from what was receipted. It cannot reconstruct the row, so "replay" has no input. Replay needs the content: an after-image, or the operation plus its arguments.
- Corrected claim: store the canonical after-image (proposed `after_image_json`), or redefine "repair" as "verify plus re-derive from staging". The second only works for rows that came from staging; operator-authored rows have no other source.
- Confidence: HIGH.
- What would change my mind: a definition of "replay" in the pack that means verification only. None exists.

### A7. The pending B9 contract restates the superseded S3 rule (report C9)

- B9 text (`pack/research-chain/part2-b9.md`):
  - :263-269 `EFFECTIVE_ELIGIBLE(...) → BooleanState`, with states listed as "KNOWN / UNKNOWN / UNBOUNDED". Those are bound kinds, not truth values.
  - :291-296 relations "BEFORE / AFTER / OVERLAPS / CONTAINS", then "Unknown bounds produce: UNKNOWN_TEMPORAL_RELATION".
- Frozen side:
  - S10: "Over-frozen (wrong): 'any non-KNOWN required endpoint → UNKNOWN'" (`pack/research-chain/s10-output-2026-10-01.md`, B4 repair contract section).
  - Folklore kill #81: "Any unknown interval endpoint forces the entire temporal relation to UNKNOWN."
  - Ledger :110: B4 FROZEN with relation oracles.
- Mechanism: read literally, B9 9.3 returns UNKNOWN for `[UNBOUNDED, KNOWN(2024-06-01))` OVERLAPS `[2024-01-01, 2024-12-31)`, which frozen B4 decides TRUE (ledger :104). The B9 contract also says "Consumes B4 accepted temporal semantics" (`part2-b9.md` section 9 header), so it can also be read as a loose paraphrase that defers to B4.
- Status: a cross-contract inconsistency (R09) for the fresh B1/B9 admission to weigh. It is not this session's to repair, and these quarantined bytes may differ from the retained reports.
- Confidence: MEDIUM. The literal reading conflicts; the deferring reading does not.
- What would change my mind: the retained (uncontaminated) B9 text wording 9.3 differently.

### A8. Audit counts, 555 vs 355: DOWNGRADED from "inconsistent" to "underspecified" (U-DASH-13)

- Source: "555 claims checked, 9 KILLED, 31 DOWNGRADED, 188 CONFIRMED load-bearing, 127 UNRESOLVED" (`pack/unsilo-feed-dashboard-spec-2026-10-02.md:103-104`).
- Correction to my own Phase 1 claim:
  - The qualifier "load-bearing" makes 188 a subset of CONFIRMED.
  - If 200 confirmed claims were not load-bearing, then 9 + 31 + 388 + 127 = 555, and the record is consistent.
  - The spec does not say this either way. So it is not established as an inconsistency; it is an undisclosed count.
- Schema effect: none. `core_audit_count` stores counts as reported, keyed by name, so "CONFIRMED_LOAD_BEARING" and "CONFIRMED" can both be stored.
- Confidence: MEDIUM that the subset reading is right.
- What would change my mind: the audit export.

### A9. Other report items, anchored

- C7, blocker status too coarse: data theory :21 "status open/closed" vs master doc :108-119 (states FROZEN, REPAIRED-PENDING-ADMISSION, OPEN, RETAINED-INTEGRATION-VERIFIED, RETAINED). HIGH.
- C8, S8 folklore count: `pack/research-chain/s8-output-2026-09-30.md:127` "Folklore killed (6)" vs `research-chain/folklore-kill-log-2026-10-01.md:83-89` (kills 64 to 70, seven). HIGH.
- C10, R-L4 undefined operator: `pack/research-chain/part3-crosswalk.md:170-173` "Typed expression: RecordVersion comparison". `part2-b9.md` section 3 lists 10 families, and none defines a RecordVersion comparison. HIGH on the literal text; quarantine caveat as in A7.
- C11, blocker code collision: `pack/unsilo-feed-dashboard-spec-2026-10-02.md:55, :58, :60` (Superhuman B4, B1, B3) vs research-chain B1 to B12 (master doc :108-119). HIGH.
- C12, FTS5 source: `libsqlite3-sys/build.rs:163` `-DSQLITE_ENABLE_FTS5`. HIGH.

---

## B. Proposals (a) to (g): residuals needing a ruling

### (a) The enum alone does not make the freeze bug unrepresentable

Exact baseline claims:

- Data theory :48-52: "an interval endpoint is either a timestamp or an explicit marker (UNBOUNDED_FUTURE / UNKNOWN), never NULL meaning two things. ... The freeze bug was treating open as closed; the schema makes that unrepresentable."
- Data theory :102-103: "the deciding factor was never velocity, it was B4. Compiler-enforced interval markers beat schema CHECK constraints".
- Shootout :208: "`enum Endpoint { Timestamp(i64), UnboundedFuture, Unknown }` makes the B4 bug unrepresentable at compile time."
- Launch prompt :149-150 (definition of done): "B4 interval bug is unrepresentable: interval endpoints are a Rust enum, NULL never means an unknown endpoint."

The freeze-bug mechanism, executed (`schema/fixtures/b4_regression.sql`, cut DAY 2026-10-02):

- Store the endpoint in one nullable column and query `valid_from <= T AND (valid_to IS NULL OR T < valid_to)`.
- That returns rows 1 (`[2026-09-29, UNKNOWN)`), 2, and 6 (`[2026-09-01, UNBOUNDED)`). Rows 1 and 6 are indistinguishable: an unknown end is read as "still open". That is the freeze.
- The variant without `IS NULL` drops every NULL row.

Why the enum does not prevent it. Each of these compiles with the enum in place:

1. `match (from, to) { (Known(_), Known(_)) => decide(), _ => Unknown }` is the superseded S3 rule.
2. `Option<i64>` as the column type, mapping both `UnboundedFuture` and `Unknown` to NULL, recreates the single-column store above.
3. Any panel that reads SQL directly never passes through the enum.

The type constrains values in memory. The freeze was an evaluation and persistence rule.

- Residual for ruling: adopt (a) as a correction of the four texts above. Then restate the Rust rationale (see F, where this narrows the shootout's stated deciding argument).
- Confidence: HIGH (executed for the persistence path; the other two are by construction).
- What would change my mind: a design where the database column itself is a Rust-generated type with no NULL path and no SQL panel bypass. Nothing in the pack proposes that.

### (b) Per-endpoint Known / Unbounded / Unknown

- Mandated by master doc :111 and ledger :104 (Case S3-1 uses an UNBOUNDED start).
- Residual: none beyond recording that the schema implements it on B4's authority, not on the proposal's.
- Confidence: HIGH.

### (c) CHECK constraints plus three-valued views

Grounds:

- S6 text (`pack/research-chain/s6-output-2026-09-30.md`, type and numeric section):
  - "Tri-valued interval predicates must return TRUE/FALSE/UNKNOWN distinctly; UNKNOWN rows enter the UNKNOWN channel explicitly."
  - "CHECK(x>0) satisfied by NULL → requiredness and validity are separate constraints".
- Executed: every CHECK in `core_interval` and `core_instant` fires on its own with a valid receipt present (`schema/README.md` 1). It held under `trusted_schema=OFF`: the built-ins `date()`, `json_valid()`, `json_type()`, `json_array_length()`, `instr()`, `substr()`, and `CAST` all ran inside CHECKs on 3.45.1 with that setting.

Residual for ruling: where the evaluator lives.

- Option 1: the SQL view only (current proposal).
- Option 2: Rust only.
- Option 3: both, plus a test asserting they agree on every case in the regression table.

The view keeps "every number is an openable query"; a Rust-only evaluator would not be openable as SQL.

Confidence: HIGH on the grounds; the residual is a design choice.

### (d) Explicit UNKNOWN band

- Grounds: the S6 sentence above, plus S7/B12: "UNKNOWN/coverage limits survive the renderer" (`pack/research-chain/s7-output-2026-09-30.md`, anti-cherry-picking list).
- Residual: layout only (Phase 2 UI). The schema exposes `in_effect_at_cut` and `in_effect_reason`.
- Confidence: HIGH.

### (e) What the record actually says about approximate times like "~9:31 PM"

Searched every pack and root file for `approx`, `precision`, `precise`, and `~`-prefixed times.

What exists:

- The data, verbatim: "Palantir — SUBMITTED 2026-10-01 ~9:31 PM ET" (`pack/unsilo-feed-dashboard-spec-2026-10-02.md:65`); likewise :67 (~9:39 PM) and :78 (~12:21 AM). The tilde appears only in data rows.
- S3 :5: "KNOWN(v): established at the evidence's own granularity; not arbitrary precision."
- S3 :47-48: "Finest required granularity = 1 second ... no v1 conclusion may depend on sub-second ordering."
- Harness spec v1.2 :243 (not a frozen contract): "Uncertain dates are never represented as precise ones."
- The ledger writes its own times as "around 2:12 AM ET" (34 occurrences in `triage-state-2026-10-01.md`). That is narrative wording in a log, not a temporal rule.

What does not exist: any rule defining an approximate time, a tolerance, or a minute granularity. No frozen text says what "~9:31 PM" means as a bound.

Mechanism and options:

- Under S3 :5, a KNOWN value must be at the evidence's own granularity.
- "~9:31 PM" asserts neither the second nor the minute. So storing `21:31:00` is "arbitrary precision" and violates S3 :5.
- What the evidence does establish is the calendar day 2026-10-01 in America/New_York, so DAY granularity is admissible.
- Option 1, the current proposal: KNOWN at DAY plus the verbatim text.
- Option 2: KNOWN at HOUR. Not in the frozen granularity set; it would be a B4 change.
- Option 3: an interval-valued instant (e.g. 9:00 to 10:00 PM). Not in the frozen domain, since point times are KNOWN or UNKNOWN only (master doc :111). A B4 change.

Residual for ruling: accept DAY plus text, or take options 2 or 3 to the B4 owner as a temporal-semantics change.

Confidence: HIGH that the record contains no rule; MEDIUM on the S3 :5 reading.

### (f) What SQLite 3.45.1 actually provides for SHA-256

Executed on 3.45.1:

- `SELECT sha256('x')`, `sha3('x')`, `sha1('x')`, and `sha3_query('select 1')` each fail with "no such function".
- `PRAGMA compile_options` shows FTS3/4/5 and LOAD_EXTENSION, with no hash function.

Bundled 3.53.4 amalgamation: no `sha3`, `sha256`, `sha1`, or `shathree` registration anywhere in `sqlite3.c`. (The `sha3()` function people know from the `sqlite3` command-line shell is a shell extension, `ext/misc/shathree.c`. It is not in the library, and it is SHA-3, not SHA-256.)

So SHA-256 can enter SQL only as an application-defined function. In rusqlite that is `Connection::create_scalar_function` behind the `functions` feature (`rusqlite/Cargo.toml:49`), using a hashing crate.

Constraint found, `sqlite3.h:5939-5948`:

> "Some heightened security settings ([SQLITE_DBCONFIG_TRUSTED_SCHEMA] and [PRAGMA trusted_schema=OFF]) disable the use of SQL functions inside views and triggers and in schema structures such as [CHECK constraints] ... unless the function is tagged with SQLITE_INNOCUOUS."

Also `:2541-2544`. rusqlite exposes `FunctionFlags::SQLITE_INNOCUOUS` (`src/functions.rs:431`). S6 freezes `trusted_schema=OFF`.

Mechanism: proposal (f) can work in two ways:

1. In the Rust writer: write, re-read, hash, compare, then commit or roll back. Needs no flag.
2. As a trigger calling a per-connection UDF. That needs the UDF registered on every connection with `SQLITE_DETERMINISTIC | SQLITE_INNOCUOUS`. Missing it on any connection makes every trigger that calls it fail on that connection, which fails closed.

Residual for ruling: (f) yes or no, and if yes, route 1 or route 2.

Confidence: HIGH (executed plus source text).

### (g) Ordering in the query

- Grounds: S8: "Ambient-state-dependent operators inadmissible: wall clock, implicit current/latest, retrieval order ..." (`pack/research-chain/s8-output-2026-09-30.md`, determinism section).
- I could not open SQLite's documentation on view ORDER BY propagation (sqlite.org blocked), and I did not find a counterexample in source this pass.
- Residual: adopt as a rule for panel queries. Zero schema change.
- Confidence: MEDIUM. The rule is cheap and harmless whether or not SQLite currently preserves view ordering.

---

## C. Schema claims touching frozen contracts

### C.1 U-DASH-03 and U-DASH-14: cross-granularity

The frozen B4 contract text is not in the repo. The repo holds only these verbatim lines:

- S3 digest, `pack/research-chain/s3-output-2026-09-30.md:49-50`:
  > "Cross-granularity: TRUE only if true under every compatible interpretation; FALSE only if false under all; else UNKNOWN."
- S10 digest, `pack/research-chain/s10-output-2026-10-01.md:40-42`, in the B4 repair contract, under "Frozen and must NOT reopen":
  > "...day-granule discipline; sound cross-granularity lifting; correction non-leakage..."
- Foundation v2 B4 acceptance criteria, `:335`: "granularity rules"; `:339`: "All bound-type combinations and relevant ordering/equality/boundary/invalidity/granularity cases"; `:1220`: "mixed-granularity invalidity".

What I cannot quote: the reconstructed B4-TEMPORAL-CONTRACT's own cross-granularity clause. It lives in chats 6abdf9e2 and 6abdfc6f.

Where `GRANULARITY_NOT_LIFTED` diverges, executed on the proposed schema:

| Interval | Cut | Every compatible interpretation | Schema returns |
|---|---|---|---|
| `[DAY 2026-09-01 ET, DAY 2026-09-30 ET)` | SECOND `2026-10-15T12:00:00Z` | FALSE. The end 2026-09-30 00:00 America/New_York is `2026-09-30T04:00:00Z`, earlier than the cut; no interpretation of either day puts the cut inside. | UNKNOWN, `GRANULARITY_NOT_LIFTED` |
| same | DAY `2026-10-15` in zone UTC | FALSE, same reason | UNKNOWN, `GRANULARITY_NOT_LIFTED` |
| `[DAY 2026-09-01 ET, UNKNOWN)` | SECOND `2026-10-15T12:00:00Z` | UNKNOWN; the lower bound holds under every interpretation and the upper is split | UNKNOWN (agrees) |

- U-DASH-03: the view returns UNKNOWN wherever any KNOWN endpoint's granularity or zone differs from the cut's. The S3 rule requires FALSE in rows 1 and 2.
  - Effect: the schema under-claims (UNKNOWN for a determinate FALSE). It never over-claims.
  - Still a conformance gap: "else UNKNOWN" applies only when the interpretations disagree.
- U-DASH-14: executed, a KNOWN-KNOWN interval `[DAY 2026-09-29 ET, SECOND 2026-10-02T01:31:00Z)` is refused at write ("CHECK constraint failed: NOT (from_kind = 'KNOWN' AND to_kind = 'KNOWN' ...").
  - Under the S3 rule, its validity (from < to) holds under every compatible interpretation: the latest instant of 2026-09-29 ET is `2026-09-30T03:59:59Z`, earlier than `2026-10-02T01:31:00Z`.
  - So the frozen rule would admit an interval the schema refuses.
- Why lifting is mechanical here: a DAY with a named zone such as America/New_York maps to an exact half-open UTC range, and local midnight never falls in a DST gap or overlap there (the shifts happen at 2:00 AM). It needs a timezone database.
  - SQLite has none that is deterministic. `localtime` modifiers read the host zone, which S8 bans as ambient state.
  - So lifting belongs in Rust, or in a precomputed day-to-UTC table pinned as a dependency (B10 would require the tz version as part of the closure).
- Residual for ruling: implement lifting per the S3 rule, after the B4 owner confirms the reconstructed contract wording.
- Confidence: HIGH on the divergence (executed); MEDIUM that the reconstructed B4 clause matches S3 :49-50, since S10 says it was preserved but I have not read it.

### C.2 U-DASH-04: dense vs discrete completions; what to pull from chat 6abdfc6f

What I need, verbatim:

1. The sentence defining the admissible-completion domain for UNKNOWN. Does UNKNOWN range over any value on the time line, or over values at the endpoint's (or the relation's) granularity?
2. Step 3 of DecideRelation, "generate finite total-order extensions over the four endpoint variables" (ledger :103). Specifically:
   - (i) whether extensions include ties (equalities) as well as strict orders;
   - (ii) whether two variables may occupy adjacent granules with nothing between them, or whether the procedure treats any two distinct positions as having room between them.
3. The point-membership oracle, if written separately. Foundation v2 :338 requires "golden oracles for every v1 temporal operation, including point membership and RestrictTime".
4. Any worked example where an UNKNOWN endpoint sits one granule away from a KNOWN value or a cut.

What the two readings predict differently:

| Case (DAY granularity) | Dense reading (order positions; what the schema implements) | Discrete reading (completions are granules) |
|---|---|---|
| `[UNKNOWN, KNOWN(2026-10-03))` at cut 2026-10-02 | UNKNOWN: the start can sit strictly between the cut and the end | TRUE: the only start values below 10-03 are 10-02 or earlier, and all of them are at or before the cut |
| `[KNOWN(2026-10-02), UNKNOWN)` at cut 2026-10-02 | TRUE | TRUE (agrees) |
| `[KNOWN(2026-10-01), UNKNOWN)` at cut 2026-10-02 | UNKNOWN | UNKNOWN: the end may be 10-02 (cut excluded) or later (agrees) |
| Relation needing an UNKNOWN strictly between two KNOWN days that are adjacent, e.g. A.start UNKNOWN with constraints `2026-10-01 < A.start < 2026-10-02` | nonempty completion set | EMPTY completion set, so Foundation v2 :337's empty-admissibility rule fires ("Empty admissibility cannot establish both relation and negation") |

The last row matters most: discreteness can turn a determinate answer into an invalid-input case.

- Confidence that the ledger's procedure implies the dense reading: MEDIUM. "Total-order extensions over variables" is a standard order-theoretic procedure, and such procedures ignore adjacency unless told otherwise. The ledger summary does not say.
- What would change my mind: item 1 or 2(ii) in the chat stating granule-valued completions.

---

## D. Charting layer for Rust + Askama + htmx with no JS build step

Constraint, verbatim (data theory :94): "Axum 0.8 + Askama + htmx (vendored, no build step)".

"No build step" means one of two things:

- (i) no chart library: the server emits markup; or
- (ii) one prebuilt file vendored like `htmx.min.js` and loaded with a plain `<script>`, with no bundler, transpiler, or npm install at build time.

### D.1 Candidates, grounded

Release dates are from npm (`time[latest]`) or crates.io (`updated_at`), fetched 2026-10-02. HEAD dates are from shallow clones on 2026-10-02. Licenses were read from the shipped `LICENSE` file. Sizes are measured from the npm tarballs ("min" = shipped minified browser file; "gz" = `gzip -9`).

| Candidate | Latest release | Upstream HEAD | License (file read) | No-build artifact | Size min / gz | Rendering |
|---|---|---|---|---|---|---|
| Hand-rolled SVG in Askama templates | n/a | n/a | n/a | none needed | 0 / 0 | server SVG |
| plotters (Rust crate) | 0.3.7; crate `updated_at` 2024-09-08 | 2026-03-17 `c63248e` | MIT (`LICENSE`, "Copyright (c) 2019-2022 Hao Hou ... 2022-2025 The plotters-rs contributors") | Rust dependency; server SVG backend | 0 client bytes | server SVG |
| uPlot | 1.6.32, 2025-03-14 | 2026-09-28 `e62f123` | MIT (`LICENSE`, Leon Sorokin) | `dist/uPlot.iife.min.js` + `uPlot.min.css`, no dependencies | 51,081 / 22,009 (+1,857 CSS) | client canvas |
| Chart.js | 4.5.1, 2025-10-13 | 2026-09-14 `6a86e23` | MIT (`LICENSE.md`) | `dist/chart.umd.min.js` | 208,522 / 70,402 | client canvas |
| Observable Plot | 0.6.17, 2025-02-14 | 2026-09-01 `535723d` | ISC (`LICENSE`, Observable) | `dist/plot.umd.min.js`, but its UMD header requires `d3@7.9.0/dist/d3.min.js`, so D3 must be vendored too | 209,183 / 68,818, plus D3 = about 161 KB gz | client SVG |
| D3 | 7.9.0, 2024-03-12 | 2026-05-28 `ca958d4` | ISC (`LICENSE`, Bostock) | `dist/d3.min.js` | 279,706 / 92,370 | toolkit; you write the chart in JS |
| Apache ECharts | 6.1.0, 2026-05-19 | 2026-09-30 `62e3373` | Apache-2.0 (`LICENSE`) | `dist/echarts.min.js` (or `echarts.simple.min.js`, 500,315 min) | 1,121,883 / 367,915 | client canvas or SVG |
| charming (Rust wrapper for ECharts) | 0.6.0, crate `updated_at` 2025-06-17 | 2026-09-27 `e34296b` | Apache-2.0 (`LICENSE-APACHE` read; other license files not checked) | emits ECharts option JSON; still needs `echarts.min.js` in the browser (its server-side image path not verified) | inherits ECharts | client |
| Frappe Charts | 1.6.2, 2021-06-16 | not cloned | MIT (npm metadata only) | UMD file | not measured | dormant since 2021; excluded for the same reason as Plottable |

### D.2 Fit against what the charts must show

The v1 views from the hopes map:

- momentum as discrete points with completeness basis;
- churn per cut pair;
- per-company raw label counts;
- field-completeness grids;
- coverage tables;
- lifecycle bars with UNKNOWN ends.

Every one is points, bars, grids, or interval bars. None needs zoom over thousands of points.

How the candidates fit:

- Hand-rolled SVG in Askama:
  - Zero client bytes, deterministic output bytes, works with no JavaScript, and htmx can swap it as a fragment.
  - The UNKNOWN band and B12 annotations are drawn by the same server code that ran the three-valued SQL, so the semantics have one implementation.
  - The cost is writing axes, ticks, and scales yourself. For bar, point, and grid charts that is small, bounded work.
- plotters gives the same server-side property with less hand work. Its last release is about two years old (repo active), and its chart model is generic: an UNKNOWN band is custom drawing either way.
- uPlot is the strongest client option: the smallest file (22 KB gz, about the size of htmx itself, which is 16,838 gz), no dependencies, active. But:
  - It draws canvas, so values are not in the DOM as text.
  - The UNKNOWN band would be a second implementation in JS.
  - It earns its place only if dense, zoomable time series become a need. Momentum points do not need it.
- Chart.js, Observable Plot plus D3, and ECharts are vendorable without a build. At 70 to 368 KB gz they buy features (themes, legends, geographic charts in ECharts) that the v1 view list does not use. ECharts' geographic components belong to the map question, which the hopes map deferred.

### D.3 Recommendation (for ruling)

1. Server-rendered SVG from Askama templates as the charting layer.
2. Keep uPlot (vendored IIFE, pinned 1.6.32) as the named fallback if a zoomable dense series is ever needed.
3. Do not adopt a full chart framework for v1.

Confidence: MEDIUM-HIGH. The facts are HIGH. The recommendation depends on the v1 view list staying points, bars, and grids.

What would change my mind: a ruling that the visual language must be motion-heavy (the hopes map conflict, F9). Animated transitions are where client libraries earn their weight.

### D.4 Blueprint vs the server-rendered stack

Grounded facts, fetched 2026-10-02:

- `@blueprintjs/core` 6.21.0, published 2026-09-30, Apache-2.0 (`LICENSE` read). Repo HEAD 2026-09-30 `c5a3873`. Active.
- `peerDependencies: react 18 || 19, react-dom 18 || 19`.
- It ships `lib/cjs`, `lib/esm`, `lib/esnext`, and CSS only. There is no UMD or browser bundle (no `unpkg`/`jsdelivr` field; no `*.bundle.js` or `*umd*` file in the tarball).
- Its ESM files import bare specifiers (`react/jsx-runtime`, `classnames`, `react`; `lib/esm/components/button/buttons.js`) and have 9 runtime dependencies (`@floating-ui/react`, `@popperjs/core`, `react-popper`, `react-transition-group`, ...). A bundler, or a hand-maintained import map across that tree, is required.
- `lib/css/blueprint.css` is 562,119 bytes.
- React 19.3.0 (published 2026-09-09): `react-dom-client.production.js` is 625,168 bytes as shipped (110,528 gz before a bundler minifies it).
- htmx 2.0.11 for comparison: 52,182 / 16,838 gz, zero dependencies, 0BSD.

Costs of choosing Blueprint:

- A Node toolchain and bundler at build time. This directly contradicts "no build step" (data theory :94).
- A JSON API between server and client, so view logic exists twice.
  - The three-valued membership, the UNKNOWN band, and the B12 support/counterevidence/limitations render would have to be enforced in React as well as in SQL.
  - Each is a frozen-contract obligation, so the duplication is a place for them to diverge.
- About 110+ KB gz of React runtime, plus Blueprint and its CSS.
- A second language surface (TypeScript) next to Rust. This connects to the stack conflict in F.

What Blueprint buys:

- Mature, accessible interactive components: popovers, menus, dialogs, keyboard navigation, dark theme. Its table is a separate package (`@blueprintjs/table`, not checked this pass).
- Fewer hand-rolled widgets.

What it does not break: a single static binary. Built assets can be embedded in the Rust binary at compile time, so that constraint survives. The constraints it breaks are "no build step" and "one implementation of render semantics".

Costs of staying server-rendered (Askama + htmx):

- Hand-rolled filter chips, popovers, and tables.
- Server pagination instead of client virtualization.
- A round trip per interaction. It is local, so latency is small but not zero.
- Fewer accessibility guarantees out of the box.

What it buys:

- One implementation of every semantic rule.
- Deterministic HTML that can be hashed and receipted.
- A 16.8 KB gz client.
- No Node at build.

Residual for ruling: Blueprint means changing the approved stack text (data theory :94 and the session prompt Layer 4). Staying server-rendered means accepting hand-rolled widgets.

Confidence: HIGH on the facts; the tradeoff is a judgment.

---

## E. Hopes to kill, re-presented with grounding

### Kill 1. Confidence-scored connections

- Where the hope is stated: master doc :24 lists "confidence-scored connections" in the platform direction.
- Why kill:
  - `README.md:18`: "No numerical probability-style confidence anywhere."
  - Master doc :48: "Categorical, never scores."
  - Harness spec v1.2 :214, on ER candidate generation: "similarity scores are similarity measures, not probabilities; thresholds are case heuristics, never defaults".
  - S5 B8.2 (`pack/research-chain/s5-output-2026-09-30.md:39`): "NO probabilistic company matching in v1 (Fellegi-Sunter deliberately excluded)".
- Mechanism: a connection score is a number that ranks or gates claims. It is exactly what the two standing rules forbid, and the entity-resolution rule forbids the matching that would produce it.
- Replacement already in the contracts: PD/AO/DD/QN/UR plus the WEAK modifier.
- Confidence: HIGH.
- What would change my mind: an operator ruling that repeals the categorical rule program-wide. That would also invalidate B12 and every freeze record.

### Kill 2. Forensic recon on high-power individuals, with public-source email harvesting

- Where stated: master doc :24 ("forensic recon on ... high-power individuals"); your use list ("public-source direct-email outreach").
- Why kill:
  - Harness spec v1.2 :15 lists "private-person dossiers" among the killed expansions.
  - Its ontology at :162 defers `Person`.
  - Blockers file `build-blockers-b1-b12-verbatim-2026-09-30.md:115` puts "named-person recon" in "Dream (out of v1's mouth)".
  - B8 identity is company-only: "Non-filer: opaque durable UnSilo company ID" (`s5-output-2026-09-30.md:33`). No person-identity contract exists, so person linkage would be name matching, which B8.2 forbids.
  - Guessing address patterns is inference outside every source boundary. S2 :9 excludes "guessed endpoints"; the same principle applies.
  - Harness spec v1.2 :156 (Tier 5): Cipher never performs outbound; outreach is yours.
- Mechanism: without a person-identity contract, every person-level link is an unadmitted inference.
- What survives: reading a recruiter address printed on an in-scope careers page (PD text). UnSilo does not store or enumerate it.
- Confidence: HIGH on the contract grounds. LOW on legal exposure, which was not researched (state privacy and data-broker law).
- What would change my mind: a written person-identity contract with evidence classes and exclusions, plus legal review. That is platform work, not a v1 deferral.

### Kill 3. "Full company DNA"

- Where stated: your use list.
- Why kill:
  - Foundation v2 Artifact 2, R06 (`repair-foundation-v2-2026-10-01.md:754`): PASS requires "Inputs, preconditions, dependencies, operations, outputs, boundaries, and failures are determinate". Its FAIL example is an undefined target ("Compare compatible cohorts" without defining compatibility).
  - "DNA" names no observable, source, or operator.
  - S1 bounds what can be said about a company to five dimensions, with Co limited to "publisher-declared attributes only unless a frozen classification semantics exists" (`s1-output-2026-09-30.md:33`).
  - Folklore kills #1, #6, and #9 forbid the usual DNA inferences: postings as hires, SEC silence as no hiring, sparse observations as continuous state.
- Mechanism: an undefined aggregate invites unsourced fill-in, which is the failure the folklore log exists to stop.
- Replacement: "PublicRecruitingState(C, T, S) for one company", plus registrant disclosures.
- Confidence: HIGH that it fails R06 as stated. A defined version would be a different hope.
- What would change my mind: a definition of "DNA" as a list of observables, each mapped to a source and contract.

---

## F. Stack conflict: the texts

### F.1 Master doc directive 9, verbatim

`pack/unsilo-master-architecture-prompt-2026-10-02.md:177`:

> "9. **Scope discipline.** v1 is the goal, the platform is the dream. Every plan flags scope creep explicitly and feasibility-checks against the real stack (single operator, local-first laptop + VM, SQLite-first, no GPU, TS/Python, deterministic pipelines, private use)."

### F.2 Rust approval: what the repo holds, verbatim

The quote "Rust pick stands (narrowed)" from the 2026-10-02 session handoff is not in this repo. Searched all files on the branch; no match for "stands (narrowed)" or "narrowed" in that sense. The operator holds that text locally and should attach it to the ruling package. The repo texts are:

`pack/unsilo-data-theory-2026-10-02.md:94-104`:

> "Decision: **Rust**. Axum 0.8 + Askama + htmx (vendored, no build step); rusqlite with `bundled` feature; PRAGMA journal_mode=WAL, foreign_keys=ON, busy_timeout; DB access behind a dedicated thread or tokio-rusqlite (never block the async runtime); interval endpoints as a Rust enum (Timestamp / UnboundedFuture / Unknown); receipt ledger written in the same transaction BEFORE the mutation; feed_item as a SQL VIEW ordered by (event_time, id); target x86_64-unknown-linux-musl for the static binary.
>
> Why it survived the crawl: the deciding factor was never velocity, it was B4. Compiler-enforced interval markers beat schema CHECK constraints, and nothing in the 16-repo survey overturned that."

`pack/language-shootout-2026-10-02.md:232-238`:

> "1. RUST. Best spec fit. The B4 lesson (explicit interval markers, never overloaded NULL) is a type-system problem and Rust's enums solve it at compile time; rusqlite/bundled is the cleanest FTS5+WAL story surveyed; Axum+Askama+htmx is a mature, production-proven dashboard pattern with no WASM/Node pipeline; idle RSS ~3.6-7MB is the lowest of the GC/runtime options. Costs: slowest iteration (compile times, borrow checker), musl setup for true static binaries, the tokio/rusqlite seam."

`pack/unsilo-session-prompt-2026-10-02.md:234-235`:

> "### Layer 4 — Implementation stack
> Rust, ranked against the spec."

### F.3 What links the texts, stated neutrally

- Directive 9 is a feasibility-check list, not a stack decision. Read literally, it names TS/Python as "the real stack", so a Rust plan fails its own feasibility check.
- The data theory's stated deciding reason is the B4 type-system argument. Proposal (a), if adopted, finds that argument does not hold as written: the enum does not prevent the freeze bug (section B (a)).
- What survives from the shootout without that argument: the bundled SQLite/FTS5 story, no Node pipeline, low resident memory, and enums as a second line of defense.
- Under that reading Rust's margin over Go narrows. A TS/Python stack was never ranked in the shootout at all (it compared Rust, Go, Zig, with Bun/TS as "the floor, not a contender", `language-shootout-2026-10-02.md:17-20`).
- Ruling needed on text:
  - (1) Is directive 9's "TS/Python" a binding constraint on the dashboard, or a description of the harness's default?
  - (2) Does the Rust decision stand on the narrowed reasons?
  - (3) If Blueprint is wanted, the TS side becomes real regardless (D.4).

Confidence: HIGH on the quotes; the linkage is analysis.

---

## G. Provisional status of the hopes map

`pack/phase1/hopes-to-architecture-map-2026-10-02.md` stays provisional. Every WEAK label stands until all four clear:

1. RECON-ECLASS-PD-AO-DD-v2.0 admitted;
2. B1/B9 validly admitted and B10 settled;
3. a first receipted acquisition run passes B5/B6;
4. build authorized.

No label has been raised in this pass. Two mappings move down, not up:

- U-DASH-13 (audit counts) is now "underspecified" rather than "inconsistent" (A8).
- A7 is held at MEDIUM pending the uncontaminated B9 text.

## Ruling package index

| Item | Section | Residual question |
|---|---|---|
| Corrections A1 to A8 (+A9) | A | adopt each as corrected text |
| (a) | B | adopt the correction; restate the Rust rationale |
| (b) | B | record as mandated |
| (c) | B | evaluator in SQL, Rust, or both with an agreement test |
| (d) | B | layout deferred to UI |
| (e) | B | DAY plus text, or a B4 change for finer approximate times |
| (f) | B | yes/no; Rust writer route or INNOCUOUS UDF route |
| (g) | B | adopt as a panel-query rule |
| U-DASH-01 to 14 | `schema/README.md` 9; C.1, C.2 here | as listed; 03/14 and 04 need the chat text in C.2 |
| License | Method | settled in chat 2026-10-02; pack text still says "patterns only" |
| Stack | F, D.4 | directive 9 scope; Rust on narrowed reasons; Blueprint or not |
| Charting | D.3 | server SVG primary, uPlot fallback |

Build authorization: NONE
