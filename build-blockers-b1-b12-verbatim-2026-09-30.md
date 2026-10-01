# Build blockers B1–B12 — verbatim extraction, 2026-09-30 ~6:39 PM ET

Source: UnSilo "Sprint plan revisions" chat (session E)
https://chatgpt.com/g/g-p-6abd6123a014819192a3a400854f67b7-unsilo/c/6abd8973-f884-83ea-bd14-3a28dd48891c
Extraction: read-only browser pull, high effort, fresh window. Reproduced faithfully;
not paraphrased.

## B1 — Canonical QueryDefinition AST unspecified.
Why: without it, SQL becomes semantic source-of-truth again and CIRCE's key seam is lost.
Unblock: versioned AST schema; canonical serialization; hash algorithm; operator/element
types; parameter types; compiler-version field; golden AST->SQL fixtures.

## B2 — Legal cohort compatibility predicate missing.
Why: Wave 7 killed unrestricted A union B, A intersect B, A\B.
Unblock: define equality requirements over registry snapshot, ontology version,
transform/projection versions, temporal world, element type and relevant source scope.
Illegal composition fails closed.

## B3 — Cross-version comparison semantics missing.
Why: "old cohort minus new cohort" confounds reality with changed machinery.
Unblock: implement four separately reported components: predicate drift / ontic change /
epistemic ingestion / ER churn. If decomposition cannot be computed, return
incomparable/UNKNOWN rather than one delta.

## B4 — Temporal bound representation not frozen.
Why: nullable endpoints cannot distinguish unknown from unbounded and invite accidental
closed-world semantics.
Unblock: typed bounds {KNOWN(value), UNBOUNDED, UNKNOWN}; [from,to) algebra; fixtures for
all combinations; effective/knowledge cuts defined.

## B5 — Acquisition completeness proof isn't executable yet.
Why: negative evidence otherwise becomes "HTTP 200 therefore absent."
Unblock: SourceCheck vector + EnumerationProof + discovery graph + pagination proof +
parser/schema validation + scope equivalence implemented and fixture-tested.

## B6 — Negative-evidence constructors need admission rules.
Why: NegativeObservation, VerifiedEmptyScope, MemoryHole are dangerous if ordinary code can
insert them freely.
Unblock: central constructors/write-admission rules proving prerequisites;
malformed/incomplete acquisition must make construction impossible.

## B7 — Ontology evolution contract incomplete.
Why: immutable versions alone don't guarantee old data remains interpretable.
Unblock: canonical ontology serialization, schema ID/version, upcaster registry, reified
n-ary relation representation, epistemic-state rules, historical fixture upgraded through
>=2 versions.

## B8 — Registry snapshot closure needs specification.
Why: append-only membership logs can leak superseded accepts and violate cannot-link constraints.
Unblock: deterministic materializer from decisions->snapshot; one effective membership per
mention; cannot-link closure verifier; snapshot hash; stale-impact calculation;
merge/split/cannot-link fixtures.

## B9 — Operator type system unspecified.
Why: otherwise the "new algebra" is just another bag of SQL helpers.
Unblock: input/output element type per family; legality rules; version dependencies;
deterministic result schema; explicit abstention/error behavior.

## B10 — Dependency closure verifier incomplete.
Why: MetricProof can look sealed while omitting a decision, mapping, ontology/upcaster or
acquisition proof.
Unblock: implement all 12 Wave-7 closure assertions; lifecycle strictly
BUILDING -> SEALED -> VERIFIED, any verification failure -> INVALID.

## B11 — SQLite safety profile needs adjudication and freeze.
Why: SQLite can produce syntactically successful but semantically wrong analytical results.
Unblock: STRICT schema policy; FK-on connection invariant; identifier typing; money/unit
model; projection rules; anti-fan-out grain rules; query lints; integrity checks;
exact-arithmetic policy; adversarial fixtures for every accepted hazard.

## B12 — Counterevidence render invariant lacks a machine contract.
Why: supporting evidence can otherwise be presented without known contradictory evidence.
Unblock: every finding render resolves supporting + conflicting + unresolved evidence under
the same dependency world; fixture fails if known counterevidence is omitted.

## Safe build frontier (verbatim)

"Safe build frontier: Layers 1-5 can proceed substantially now, provided their fenced
capabilities are inaccessible. Layers 7-8 are the architectural stop line — do not
implement a "temporary SavedQuery/cohort engine" using v1.2 semantics; that would entrench
exactly the abstraction Wave 7 invalidated."

## Sprint 7R (verbatim from the sprint table)

- Title: 7R — Query architecture unblock, research only
- Blockers covered: B1, B2, B3, B9
- Duration: Timebox 5 working days
- Goal: Resolve the architectural stop line. No production query/cohort/operator code in this sprint.
- DB work / migration scope: No migration. Draft schemas live as non-runtime design fixtures only.
- Tests: Hand-authored golden specifications rather than implementation tests: AST canonicalization
  examples; legal/illegal cohort-composition matrix; cross-version decomposition examples; operator
  typing matrix.
- Research spike + kill criteria: B1, B2, B3, B9. Timebox 5 working days. Deliver canonical
  QueryDefinition AST + serialization/hash/compiler version; cohort compatibility predicate;
  four-way drift decomposition; operator type system. Kill: (a) SQL text remains semantic authority;
  (b) two cohorts can compose without dependency-world equality proof; (c) old-new comparison can
  emit one undifferentiated delta; (d) operator legality requires runtime guesswork;
  (e) UNKNOWN/incomparable has no first-class result. If killed, redesign—do not implement.
- Experiment: Paper/compiler prototype may operate entirely in memory against tiny literals.
  Hypothesis: every intended hiring-footprint question can be expressed without source-specific SQL
  leaking into semantic definition. Metric: 100% of the acceptance question corpus represented
  canonically; deliberate illegal compositions rejected.
- Acceptance gates: Architecture review explicitly reclassifies Layers 7–8 from BLOCKED to
  BUILD-READY. Until then the implementation critical path stops here.

Critical-path note (verbatim): "S7R is a hard architectural gate, not schedule padding. If its
fifth day ends without a canonical AST, compatibility predicate, cross-version decomposition and
operator typing contract, Sprint 8 does not start. There is no "basic SavedQuery implementation
while we work it out." That would recreate the abstraction Session D rejected."

## v1 vs dream triage (Cipher, 2026-09-30)

v1 construction gate (S0–S6): B4, B5, B6, B7, B8, B10, B11, B12.
7R research gate (Layers 7–8): B1, B2, B3, B9. No production code until it passes.
Dream (out of v1's mouth): disclosed-money graph, named-person recon, writeback (v1.3 §D),
analytic technique (v1.3 §G), continuous surveillance, universal knowledge graph.
