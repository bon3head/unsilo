# Parked B4 proposals (a) to (g), judged against the frozen B4 contract (2026-10-02)

PROPOSALS, not adopted. Each needs an individual operator ruling. Build authorization: NONE.

Blockers lead: research-chain B4 is FROZEN under reconstructed authority. Its contract text is in repair chats (chat 6abdfc6f rework, admitted in chat 6abdfd90), not in this repo. Judgments below rest on what the ledger, the master doc, S3, and S10 establish (summarized in `schema/README.md` 3.1). Where clause detail would be needed, it is marked UNKNOWN.

Yardstick, the frozen contract as established: per-endpoint `KNOWN(v) | UNBOUNDED | UNKNOWN`; admissible completions (UNKNOWN to finite, UNBOUNDED to infinite); universal entailment, TRUE / FALSE / UNKNOWN; finite symbolic procedure over endpoint order extensions; point times never UNBOUNDED; half-open intervals; granularity discipline; effective and knowledge time separate; no Kleene, no sentinel.

Summary:

| | Proposal | Against frozen B4 | Recommendation |
|---|---|---|---|
| a | The enum alone does not make the freeze bug unrepresentable | consistent; it is a correction of the baseline's claim | ADOPT as a claim correction (no mechanism to build) |
| b | Per-endpoint Known / Unbounded / Unknown | MANDATED by the contract | already in the schema on the contract's authority; rule to record |
| c | SQL CHECK constraints plus three-valued TRUE/UNKNOWN/FALSE views | CHECK side mandated by S6; three-valued output mandated by B4 and S6 | already in the schema on that authority; residual: which layer owns evaluation |
| d | Explicit UNKNOWN band in current panels | mandated in substance by S6 and B12; layout is UI | schema supplies the channel; layout ruling deferred to UI phase |
| e | Precision-carrying Known dates | granularity per value mandated; anything finer is open | schema carries granularity and zone; residual (approximate times) needs a ruling |
| f | After-hash verified in-transaction with rollback | not a B4 matter | NOT implemented; rule separately |
| g | Ordering in the query, not the view | not a B4 matter; determinism matter | NOT implemented beyond the baseline; recommend adopting |

## (a) The enum alone does not make the freeze bug unrepresentable

Mechanism. A Rust `enum Endpoint { Timestamp(i64), UnboundedFuture, Unknown }` constrains values in memory. The B4 defect was never a value; it was an evaluation rule. Three paths reproduce the freeze with the enum in place:

1. Evaluator: `match (a, b) { (Known, Known) => compare(), _ => Unknown }` compiles and is exactly the superseded S3 blanket rule.
2. Persistence: mapping `Unknown` to SQL NULL and `UnboundedFuture` to NULL too (or to `9999-12-31`, folklore kill #80) collapses the two the moment the value leaves Rust. A query `WHERE valid_to IS NULL OR valid_to > ?` then reads UNKNOWN as open (executed, `schema/README.md` 8, Old A row 1).
3. Bypass: any SQL panel reading the table directly never passes through the enum.

Failing case for the baseline: interval `[2026-09-29, UNKNOWN)` at cut 2026-10-02, stored with a NULL `valid_to`: Old A returns it as in effect (TRUE). Frozen B4 requires UNKNOWN.

Against the contract: consistent. The contract mandates relation-specific entailment; the enum encodes none of it.

Recommendation: adopt as a correction to the data theory and launch prompt claim "the schema makes that unrepresentable" / "Rust enums making the freeze bug unrepresentable". What makes it unrepresentable in this schema is a NOT NULL `kind` column per endpoint plus a single evaluation view; the enum is a second, in-process line of defense.

## (b) Per-endpoint Known / Unbounded / Unknown

Mechanism. The baseline enum offers `UnboundedFuture` only. The frozen domain applies to each endpoint.

Failing case for the baseline: ledger Case S3-1, `A = [UNBOUNDED, KNOWN(2024-06-01))`, `B = [KNOWN(2024-01-01), KNOWN(2024-12-31))`, OVERLAPS determinately TRUE. The baseline cannot store A's start. Dashboard case: a research-chain state "in force since an unrecorded time" needs an UNKNOWN start; the baseline has no start marker at all.

Against the contract: mandated. Not a choice.

Recommendation: record that (b) is subsumed by the frozen contract. The schema implements it (`core_interval`, both endpoints), citing B4, not the proposal.

## (c) SQL CHECK constraints plus three-valued views

Mechanism. CHECKs make malformed bounds unwritable; views return TRUE, FALSE, UNKNOWN as values instead of letting WHERE drop UNKNOWN rows.

Failing case for the baseline: S6 notes `CHECK (x > 0)` passes on NULL and WHERE discards FALSE and NULL alike. A panel `SELECT ... WHERE in_effect` silently drops UNKNOWN rows (executed, Old B drops every NULL row). The schema's `v_interval_membership.truth` returns a string, so UNKNOWN rows survive any filter that does not name them.

Against the contract: the three-valued output is the contract; S6 (retained) requires "tri-valued interval predicates must return TRUE/FALSE/UNKNOWN distinctly" and separate requiredness and validity constraints.

Residual for a ruling: whether evaluation lives only in SQL views, only in Rust, or both with a cross-check test. The schema puts it in one SQL view so every panel query is openable (redash pattern) and there is one implementation to test against the frozen oracles.

## (d) Explicit UNKNOWN band in current panels

Mechanism. "Current" panels (blockers strip, applications) show items whose in-effect status is UNKNOWN in a labeled band, rather than hiding them or showing them as current.

Failing case for the baseline: Duolingo req 1265, SUBMITTED from 2026-09-29, end UNKNOWN. At cut 2026-10-02 it is UNKNOWN whether SUBMITTED still holds (an unseen rejection is possible). A two-state panel shows it as current (overclaim) or drops it (loses the application).

Against the contract: B4 yields the UNKNOWN; S6 requires an explicit UNKNOWN channel; B12 requires that UNKNOWN survive the renderer. So the band's existence is mandated; its layout is not.

Recommendation: schema provides `in_effect_at_cut` and `in_effect_reason` on `v_blocker_strip` and `v_application_state_head`; `v_blocker_strip` keeps UNKNOWN rows. The visual band is a UI ruling for Phase 2.

## (e) Precision-carrying Known dates

Mechanism. A KNOWN value carries the precision the source asserted.

Failing case for the baseline: "Duolingo submitted Sep 29" stored as `2026-09-29T00:00:00Z` asserts midnight UTC, which is 8:00 PM ET on Sep 28: wrong day in the operator's calendar (folklore kill #25). "Palantir ~9:31 PM ET" stored as a second-precision timestamp asserts precision the source denies with "~".

Against the contract: granularity per KNOWN value is frozen (KNOWN at the evidence's own granularity; date-only is a calendar-day granule). Anything beyond DAY and SECOND (minute precision, approximate values) is not established as frozen: UNKNOWN.

Recommendation: the schema carries `(value, gran, zone)` with DAY in a named calendar zone or SECOND in UTC, plus verbatim `source_text`. Approximate times are stored at DAY with the "~" wording preserved (U-DASH-11). A ruling is needed on whether to add MINUTE and an approximation marker; that would be a temporal-semantics change and belongs to the B4 owner, not the dashboard.

## (f) After-hash verified in-transaction with rollback

Mechanism. Inside the write transaction, recompute the canonical hash of the row actually written and roll back if it differs from the receipt's `after_sha256`.

Failing case for the baseline: writer computes the receipt from row image R, then (bug) writes R' with a different field. Ledger says R; table holds R'; replay produces R; the store silently disagrees with its own ledger.

Against the contract: B4 is silent; this is a receipt-integrity matter (data theory 6, DVD).

Constraint found: SQLite core has no SHA-256 SQL function, so this cannot be a pure trigger without loading an extension (and S6 sets `trusted_schema=OFF`). It would live in the Rust writer: write, re-read, hash, compare, commit or roll back.

Recommendation: NOT implemented. The schema enforces only receipt existence, 1:1 receipt use, chain linkage, and append-only, and stores `after_image_json` so a verifier can recompute offline. Rule on (f) for Phase 2.

## (g) Ordering in the query, not the view

Mechanism. Every panel query states its own ORDER BY.

Failing case for the baseline: SQLite does not promise that a view's ORDER BY governs an outer query that filters or joins it; a panel `SELECT * FROM feed_item WHERE tag = 'audits'` relies on behavior the docs do not guarantee. S8 forbids retrieval order as ambient state. (WEAK: stated from SQL semantics; no SQLite counterexample executed this session.)

Against the contract: not a B4 matter.

Recommendation: keep the baseline's view ORDER BY (it is in `feed_item`) and adopt (g) as a rule for every panel query. Zero schema change.

Build authorization: NONE
