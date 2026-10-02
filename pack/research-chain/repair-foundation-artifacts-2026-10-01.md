# UnSilo v1 Repair Round — Foundation Artifacts

Produced by GPT-6 Astra, High, 2026-10-01 ~10:10 PM ET.
Chat: https://chatgpt.com/g/g-p-6abd6123a014819192a3a400854f67b7-unsilo/c/6abdbfaf-8884-83e9-be93-8ffba12d2cd4
Title: "Research Completion Rubric". Response fully completed.

---

# ARTIFACT 1 — RESEARCH-COMPLETE DEFINITION

## Scope and starting authority

Research is complete when the UnSilo v1 semantic specification determines every in-scope operation's meaning, admissibility, dependencies, and permitted outcomes, with independently inspectable evidence and acceptance artifacts.

Implementation must no longer need to invent semantics.

This is a research-completion gate. It does not certify implemented software, authorize a build, or establish deployment readiness.

The starting disposition is:

| Disposition | Blockers |
|---|---|
| OPEN; require repair and acceptance | B1, B2, B3, B4, B7, B8, B9, B10 |
| RETAINED; require preservation and integration verification | B5, B6, B11, B12 |

B5's retained status remains conditional on its acquisition prerequisites. S10's assertions that "B4 alone remains open" and "7R cleared" cannot be inherited as clearance.

Authority: the original blocker obligations (build-blockers-b1-b12-verbatim-2026-09-30.md), the HIGH review record (astra-verdict-high-2026-10-01.md), and the MEDIUM review record (astra-verdict-medium-2026-10-01.md). The supplied review records and the S10 output (s10-output-2026-10-01.md) are summaries: they identify obligations but do not independently prove the underlying claims.

The frozen scope remains public recruiting representation over SEC EDGAR, company-published careers resources within the established H∪D∪R boundary, and Wayback CDX. Recover the authoritative definitions of that boundary. WARN and H-1B LCA remain separate source-extension decisions; neither repairs existing v1 blockers.

## Required freeze record

Every proposed blocker freeze must have a named record containing:

| Required field | Acceptance condition |
|---|---|
| Obligation | Stable requirement ID, original wording, and precise source location. |
| Normative resolution | Exact specification version and section determining the behavior. |
| Primary evidence | Primary source actually opened by the claimant; URL or artifact locator, version/date, section or span, and supported proposition. |
| Evidence class | Categorical class under the recovered, pinned evidence-class contract; its admission prerequisites are demonstrated. |
| Acceptance artifact | Exact filename or artifact ID, version/content digest, case IDs, inputs, expected outcomes, and rationale. |
| Verification | What was inspected or evaluated, by whom/session, against which artifact version, and the result. |
| Adversarial coverage | Counterexamples, boundary cases, and interactions with other blockers. |
| Limitations | Remaining unknowns, excluded claims, and conditions that would invalidate the freeze. |
| Reconciliation | Every superseded assertion and affected dependent contract identified. |

An opened digest is primary evidence *of what the digest says*, not of the underlying mechanism or experiment.

For externally factual claims, open the authoritative documentation, source data, or original observation artifact. For project-defined semantics, open the original obligation and the normative definition and derivation. For experimental claims, inspect the inputs, procedure, and original outputs. A bibliography entry, recalled source, or PoC summary does not meet this requirement.

A hand-authored golden specification can establish a research acceptance expectation. It must not be described as a passed implementation test. External documentation can support a design premise; it cannot prove that UnSilo implements or satisfies that design.

## Blocker acceptance criteria

**B1 — Canonical QueryDefinition.** Freeze requires a named B1-query-definition-contract and acceptance-question-crosswalk containing:
- A versioned, closed AST schema: node forms, operator and element types, parameter types, required fields, dependency pins, and rejection rules.
- A canonical serialization specification detailed enough for independent implementations to produce identical bytes, including ordering, literals, absent versus explicit values, and text/numeric normalization.
- A specified hash algorithm and precisely delimited hashed content; compiler identity/version and its relationship to query identity.
- Golden AST-to-SQL specifications with expected meaning and result shape. SQL must remain a compilation target.
- The recovered original acceptance-question corpus, with every question mapped to a canonical typed expression or an explicitly permitted UR outcome with a defined reason.
- Admission rules for unavailable or unacquired fields, including filtering before counting and knowledge-cut eligibility.

Missing corpus entries, unspecified syntax, or UR used to conceal an undefined operator prevent freeze.

**B2 — Cohort compatibility and composition.** Freeze requires a named B2-composition-contract containing:
- An explicit compatibility predicate over registry snapshot, ontology, transform/projection versions, temporal world, element type, population definition, and relevant source scope/contracts.
- A definition of which source-contract inputs affect membership and therefore require equality or other explicitly authorized treatment.
- A legal/illegal composition matrix covering union, intersection, and difference; equal pins, unequal pins, missing pins, incompatible populations, and uncertain compatibility.
- Deterministic rejection or abstention rules when admissibility cannot be established.
- An explicit distinction between composition and sanctioned cross-version comparison. A comparison bridge must not silently authorize unequal-pin set difference or other illegal composition.
- Golden cases demonstrating that unresolved membership is not silently removed to manufacture a comparable population.

**B3 — Cross-version comparison.** Freeze requires a named B3-change-decomposition-contract containing:
- Separate definitions and output fields for predicate drift, ontic change, epistemic ingestion, and entity-resolution churn.
- Stable population/identity rules and the prerequisites for attributing a difference to each component.
- Golden cases for each component separately, mixed changes, interacting or non-identifiable changes, and absent evidence.
- Defined interaction, residual, ordering, and double-counting treatment wherever relevant. No additive decomposition may be assumed without a stated justification.
- Source-contract-change handling and bridge coverage over all membership-affecting inputs.
- First-class UNKNOWN/incomparable outcomes when attribution cannot be established. An aggregate delta cannot substitute for missing decomposition.
- Preservation of B12 evidence obligations in comparison results.

**B4 — Temporal semantics.** Freeze requires a named B4-temporal-contract and B4-relation-oracles containing:
- The typed bound domain {KNOWN(value), UNBOUNDED, UNKNOWN}, half-open interval convention, granularity rules, and endpoint validity constraints.
- A precise admissible-completion domain, including what UNKNOWN ranges over, what UNBOUNDED means, and which constraints restrict completions.
- Explicit handling of invalid inputs and empty completion sets *before* universal entailment is evaluated. Empty admissibility cannot establish both a relation and its negation.
- Relation-specific semantics and golden oracles for every temporal operation exposed by v1, including point membership and RestrictTime.
- Coverage of all bound-type combinations and relevant ordering, equality, boundary, invalidity, and granularity cases.
- Effective-time and knowledge-time rules distinguishing acquisition, ingestion, and derived assertion; explicit eligibility at a knowledge cut.
- Preservation of unresolved dependencies even where a relation's truth can be determined despite an unknown input.
- Replacement or explicit retirement of obsolete fixtures and PoC conclusions.
- Integration checks against identity binding, acquisition admission, bridges, comparisons, and negative-evidence construction.

The required oracle is nonempty admissible-completion entailment, not an unqualified "any unknown means UNKNOWN" rule.

**B7 — Ontology evolution and posting population.** Freeze requires a named B7-ontology-evolution-contract and posting-population-contract containing:
- Canonical ontology serialization, schema identity/version, upcaster registry, historical interpretation rules, reified n-ary relation representation, and epistemic-state rules.
- A historical golden fixture carried through at least two version transitions, with expected interpretation, provenance, unresolved/lost information, and reproducibility under the original version.
- Defined behavior when an upcast cannot preserve meaning; no silent certainty or information gain.
- Posting identity and counting semantics for HTML/ATS JSON/locale mirrors, duplicates, multiple locations, prospect postings, and revisions.
- Classification admission and abstention rules. An unresolved or model-proposed classification cannot become DD merely by receiving a typed label.
- A requirement-by-requirement reconciliation of the original B7 gate.

A requirement may be superseded only by a traceable replacement that preserves its semantic obligation. "Out of scope" is not a worker's unilateral exemption.

**B8 — Registry closure and ambiguous identity.** Freeze requires a named B8-registry-contract containing:
- Deterministic decision-to-snapshot materialization, including decision ordering, supersession, rejection, unresolved state, and conflict handling.
- At most one effective accepted membership per mention; zero accepted memberships must remain possible when unresolved.
- Cannot-link closure rules, snapshot canonicalization/hash specification, and stale-impact calculation over affected dependencies.
- Golden cases for merge, split, superseded accepts, transitive cannot-link conflicts, and replay of historical snapshots.
- An explicit ambiguity outcome for contradictory exact bindings, including one locator mapped exactly to different companies.
- Temporal eligibility and dependency rules for bindings.
- Reconciliation of every original registry obligation. "Exact-only" is not a substitute for conflict resolution or abstention semantics.

**B9 — Operator type system.** Freeze requires a named B9-operator-contract containing:
- Every operator family's input/output element types, parameter types, legality rules, dependency/version requirements, and deterministic result schema.
- Explicit VALUE, abstention, unknown/incomparable, and error/rejection distinctions, using the pinned vocabulary.
- Rules for evidence-class admission and propagation, unavailable fields, classifier abstention, unresolved membership, and missing dependencies.
- A complete typing matrix with valid, invalid, and underdetermined golden expressions.
- Alignment with B1's recovered acceptance-question corpus and B2/B3 composition/comparison semantics.
- No semantic legality decision left to compiler or runtime guesswork; no VALUE outcome without its required B10 closure obligations.

**B10 — Dependency closure and B12 integration.** Freeze requires a named B10-closure-crosswalk and B10-proof-lifecycle-contract containing:
- The recovered original twelve Wave-7 closure assertions, quoted or precisely referenced. Do not reconstruct a convenient substitute list.
- A crosswalk from each assertion to its current normative rule, required dependencies, verifier condition, and positive/negative golden cases.
- Coverage of decisions, mappings, ontology/upcasters, acquisition proofs, identity, classification, temporal eligibility, source contracts, and other dependencies required by the recovered assertions.
- The lifecycle BUILDING → SEALED → VERIFIED, with any verification failure producing INVALID; defined permissions and prohibited shortcuts at each state.
- Defined handling of missing, mismatched, stale, or unresolved dependencies and their impact on result emission and replay.
- B12 integration: supporting, conflicting, and unresolved evidence resolve under the same dependency world; omission of known counterevidence fails acceptance.

A generic "transitive closure included" statement cannot discharge an unrecovered assertion.

## Retained contracts and final re-assembly

B5, B6, B11, and B12 require source-backed integration checks. Reopen any retained obligation contradicted by a repair.

- B5: Preserve SourceCheck, EnumerationProof, discovery, mandatory continuation configuration, pagination, parser/schema validation, and scope-equivalence prerequisites.
- B6: Preserve constructor/write-admission prerequisites; malformed or incomplete acquisition cannot yield qualified negative evidence.
- B11: Preserve the adjudicated SQLite safety semantics and accepted hazard fixtures.
- B12: Preserve the counterevidence invariant throughout findings, comparison, and rendering.

The final **corrected-v1-baseline** must contain:
1. One versioned normative specification with scope, glossary, evidence-class definitions, outcome types, dependency world, and explicit precedence over superseded text.
2. The complete obligation ledger: original B1–B12 requirements, both reviews' findings, and all newly discovered obligations.
3. All named acceptance artifacts above, available by exact version.
4. The recovered acceptance corpus and an explicit 7R disposition covering B1/B2/B3/B9.
5. A traceability matrix: obligation → normative clause → primary evidence → golden case/oracle → adversarial case → reviewed outcome.
6. Adversarial coverage of each requirement, its invalid/unknown boundaries, and affected cross-blocker interactions. Include the reviews' successful attacks and reassess S10's claimed repulsions against the corrected contracts.
7. A corrected folklore ledger distinguishing externally refuted claims, logical non-entailments, and project prohibitions; weak or unverified entries remain labeled.
8. An honest unknowns register separating semantic gaps, evidence gaps, implementation tasks, operational unknowns, and source extensions.
9. A supersession/change ledger and dependency-impact review showing that no obsolete rule remains authoritative.
10. An independent review of these exact versions. Any subsequent semantic change invalidates affected acceptance and requires reassessment.

An unresolved real-world observation may remain UR after research completion if the contract completely specifies its admission, propagation, dependencies, and consequences. An unresolved question about what UR means or when to return it remains a research gap.

## Explicit non-completion conditions

Research is **not** complete when:
- Clearance rests on summaries, unavailable artifacts, citation lists, or prior reviewers' authority.
- The original acceptance corpus or twelve closure assertions remain unrecovered.
- An original obligation disappears without explicit reconciliation.
- B1 serialization semantics, B7 historical interpretation, B8 materialization semantics, or another meaning-defining decision is relabeled "build work."
- Conversely, implementation of settled semantics — DDL, indexes, fetch scheduling, cache layout, UI layout, or serializer code — is incorrectly required as research.
- A fixture states only a desired answer without an independently checkable oracle or derivation.
- A known attack lacks a resolution, a justified falsification, or a fully specified conservative outcome.
- A frozen contract depends on an unresolved semantic prerequisite.
- Unknown inputs are discarded, populations narrowed, or classes upgraded to produce VALUE.
- "Principles frozen," "directionally correct," "mostly complete," or a conditional clearance substitutes for a satisfied gate.
- A timebox expires, a session count is reached, or source extensions succeed.
- The final baseline differs from the version independently reviewed.

## Boolean decision procedure

Evaluate every predicate against the exact candidate baseline. Missing evidence, unavailable artifacts, unresolved applicability, or contradictory results evaluate to FALSE.

```
RESEARCH_CAN_BE_COMPLETED :=
    SCOPE_AND_AUTHORITY_RECONCILED
    AND ORIGINAL_OBLIGATIONS_AND_ACCEPTANCE_CORPUS_RECOVERED
    AND EVERY_OPEN_BLOCKER_ACCEPTANCE_CRITERION_SATISFIED
    AND RETAINED_CONTRACTS_PRESERVED_AND_INTEGRATION_VERIFIED
    AND EVERY_FREEZE_CLAIM_HAS_OPENED_PRIMARY_EVIDENCE_AND_NAMED_ACCEPTANCE_ARTIFACTS
    AND EVERY_ORIGINAL_AND_NEW_OBLIGATION_HAS_AN_ACCEPTED_DISPOSITION
    AND CORRECTED_BASELINE_IS_COMPLETE_VERSIONED_AND_INTERNALLY_CONSISTENT
    AND ADVERSARIAL_TRACEABILITY_HAS_NO_UNRESOLVED_SEMANTIC_OR_EVIDENCE_GAP
    AND UNKNOWN_REGISTER_CONTAINS_NO_COMPLETION_BLOCKING_ITEM
    AND INDEPENDENT_REVIEW_OF_THIS_EXACT_BASELINE_PASSES_ARTIFACT_2
```

---

# ARTIFACT 2 — THE RUBRIC

## Scoring contract

Every dimension is **PASS** or **FAIL**. There is no weighted average, numerical confidence, compensating strength, or "pass with reservations."

Apply the rubric to the session body, referenced artifacts, and mandatory tail together. A polished tail cannot repair unsupported claims in the body.

The rubric assesses whether a session's contribution is admissible. A session may pass while accurately reporting an open blocker. That does not mean the blocker or research program passes Artifact 1.

| ID | Dimension | PASS requires | Concrete FAIL example |
|---|---|---|---|
| R01 | Scope and authority | Claims stay within v1; original obligations and current governing versions are identified; changes have explicit authority. | Treating WARN coverage as closure of a v1 gap, or importing dream functionality into acceptance. |
| R02 | Primary evidence | Each claimed factual finding or freeze resolves to an opened primary source and exact supported proposition; unavailable evidence is plainly identified. | "The API guarantees completeness," supported only by S4's digest. |
| R03 | Evidence-class integrity | Class admission is demonstrated under the pinned definitions; weak claims are labeled weak; unknowns remain explicit. | Labeling a classification DD because its JSON validates, despite unresolved classification semantics. |
| R04 | No digest laundering | Summaries identify leads and prior claims; underlying authority supports substantive acceptance. | Citing S10, which cites S8, as proof that canonical serialization is frozen. |
| R05 | Obligation reconciliation | Every touched original requirement and prior review finding has a traceable disposition; unresolved obligations remain open. | Replacing B8's materializer, cannot-link, hash, and stale-impact gate with "exact bindings only." |
| R06 | Semantic specificity | Inputs, preconditions, dependencies, operations, outputs, boundaries, and failures are determinate. | "Compare compatible cohorts" without defining compatibility. |
| R07 | Acceptance-artifact sufficiency | Named, available, versioned artifacts expose inputs, expected results, rationale, and the actual verification performed. | "PoC passed" with only a narrative summary; an unexecuted golden fixture labeled an implementation test. |
| R08 | Adversarial adequacy | Cases challenge the actual acceptance conditions, known attacks, invalid/unknown boundaries, and material interactions. Gaps are explicitly open. | Temporal examples omit empty admissibility; registry cases omit contradictory exact bindings. |
| R09 | Cross-contract consistency | Dependency impact is examined; affected contracts agree or are reopened; retained contracts are checked where affected. | Repairing RestrictTime while preserving a contradictory knowledge-cut rule in comparison. |
| R10 | Unknown-register honesty | Every uncertainty has a category, affected obligation, consequence, closure criterion, and next action; no disappearing unknowns. | Calling "exactly one gap" while historical schema interpretation remains unspecified. |
| R11 | Research/build separation | Decisions determining meaning remain research; implementation of already frozen meaning is classified as build work. | Deferring the hash-input definition to the serializer implementer, or blocking semantic freeze on cache implementation. |
| R12 | Terminology stability | Terms, symbols, evidence classes, and outcome types use pinned definitions; changes include a migration/crosswalk. | Using "posting," "role," and "source row" interchangeably in counts. |
| R13 | Verdict discipline | The verdict follows the stated criteria; acceptance, blocker freeze, research completion, and build authorization remain distinct. | "Essentially build-ready pending the missing corpus." |
| R14 | Version and change control | Claims identify exact versions; superseded rules and downstream invalidations are recorded; landscape changes are evidence-backed. | Updating ontology semantics while retaining prior fixture approvals without review. |
| R15 | Handoff completeness | The tail contains the next session's exact state, artifacts, open threads, task, rubric results, and admission status; references resolve. | "Continue from here" or links to unspecified "latest" files. |
| R16 | Independent checkability | Another session can reproduce the reasoning from the supplied package; observation, derivation, policy choice, and inference are distinguished. | "The reviewer confirmed it" without the source, rule, artifact, or derivation needed to check it. |

A dimension outside the worker's assigned scope may pass only with an explicit scope explanation and evidence that the session neither changes nor relies on an unchecked claim there. Bare N/A is insufficient. Final assembly and independent completion review cannot exempt any dimension.

## Mandatory unknown-record schema

Each unresolved item must contain:

```
Unknown ID:
Question:
Category: SEMANTIC / EVIDENCE / IMPLEMENTATION / OPERATIONAL / SOURCE_EXTENSION
Affected requirements and artifact versions:
Known evidence and its class:
What remains unknown:
Effect on outputs and permitted claims:
Blocks this blocker's freeze: YES / NO — reason
Blocks research completion: YES / NO — reason
Exact closure condition:
Next action and owning sequential session:
```

A conservative UR result closes a semantic requirement only when its triggering conditions and downstream behavior are fully specified. Renaming an undefined behavior UR does not close it.

## Global pass and admission rule

```
SESSION_PASS :=
    every rubric dimension is PASS
    AND the mandatory tail is complete
    AND the tail accurately describes the body and referenced artifacts
    AND no unresolved contradiction undermines the session's claimed results
```

- PASS: The contribution is eligible for chain admission after fresh-session checking.
- FAIL: The contribution does not enter the accepted chain. Preserve it as rejected material with exact repair instructions.
- An honest report of missing evidence may pass as an *open finding*; it cannot support a freeze.
- Worker self-assessment is provisional. The next fresh session checks it before relying on the contribution.
- A later failure revokes the affected contribution's acceptance and flags every dependent claim for reassessment. Previous accepted state remains identifiable.

---

# ARTIFACT 3 — THE SESSION PROTOCOL

## Operating contract

One worker at a time, in a single sequential chain. No parallel repair tracks, simultaneous blocker owners, or unreviewed merge of competing baselines.

Each session receives one bounded primary assignment and its integration dependencies. An assignment may require multiple sessions. Additional sessions are allocated according to unresolved acceptance criteria, adversarial failures, or hardening needs — not a predetermined session quota.

This round establishes and verifies semantic contracts. Production implementation, migrations, deployment, and build authorization are outside its authority. Non-runtime design fixtures and explicitly identified research experiments may support acceptance; their evidentiary limits must be stated.

## Sequence and entry requirements

The repair sequence is:
1. **Recover authority:** Original acceptance-question corpus, original twelve closure assertions, relevant S1–S9 source artifacts, full review material where available, and authoritative evidence-class/glossary definitions. Maintain an explicit missing-artifact ledger.
2. **B4:** Completion semantics, temporal oracles, and knowledge-time admission.
3. **B7/B8:** Dedicated handling of ontology evolution, posting population, and registry closure. Split these into successive sessions whenever their unresolved obligations warrant it.
4. **B1/B9:** Canonical queries, serialization/hash/compiler identity, operator typing, and complete corpus coverage.
5. **B2/B3:** Composition, comparison, change decomposition, and membership-affecting source contracts.
6. **B10/B12:** Original closure-assertion reconciliation, lifecycle, and evidence presentation.
7. **Retained-contract integration:** B5/B6/B11/B12 and all dependencies affected by repairs.
8. **Corrected assembly.**
9. **Fresh independent completion review.**

A discovered prerequisite may change this order, but the reason and resulting queue must be recorded. Work remains sequential. Missing authority blocks affected freeze claims; it need not prevent other well-grounded work in the current assignment.

## Required session procedure

**On entry**
- Open the incoming tail and the exact referenced artifacts.
- Check the previous contribution against every rubric dimension before admitting or relying on it.
- Confirm the last accepted baseline separately from pending or rejected proposals.
- Identify the assigned original obligations, review findings, acceptance criteria, and dependencies.
- Record unavailable artifacts or conflicting authority immediately. Do not invent missing content.
- State the precise question this session will resolve and the artifact it will produce or amend.

**During work**
- Open primary sources for every load-bearing factual or freeze claim.
- Separate source observation, formal derivation, design decision, inference, and unresolved claim.
- Produce explicit contract text and golden acceptance cases; challenge them with counterexamples.
- Check affected downstream contracts and preserve relevant upstream dependencies.
- Add new obligations and unknowns when discovered. Do not silently broaden the task or conceal discoveries to preserve a freeze.
- Record superseded text and invalidate affected prior acceptance.
- Stop claiming closure when evidence runs out. State the exact missing evidence or semantic decision.

**Before handoff**
- Evaluate every assigned acceptance criterion as SATISFIED or OPEN, with artifact references.
- Evaluate every rubric dimension.
- Verify that the body and tail agree.
- Distinguish three separate outcomes: session quality, blocker disposition, and program completion.
- End with the mandatory tail below. Nothing follows it.

## Dedicated handling and reopening

A blocker remains open until all its acceptance criteria are satisfied. "Principles settled" is not a freeze. Allocate another dedicated session when:
- A required original obligation or source artifact is missing.
- An oracle is underdetermined or challenged by a surviving counterexample.
- A repair changes another blocker's meaning or evidence admission.
- Required integration cannot be inspected within the current session.
- The rubric fails.
- Independent review finds a defect.

The next session's assignment must identify the exact unresolved criteria and required acceptance artifacts. Avoid generic tasks such as "harden more."

Worker freezes are *freeze candidates* until checked by a fresh session. Retained or previously accepted contracts reopen when a new contradiction or dependency failure warrants it; earlier acceptance is not immunity.

## Mandatory end-of-session tail

The following is the required copy-paste handoff. Replace every placeholder; use explicit NONE — reason where appropriate. Include this tail and all named artifacts in the next fresh session.

```
## MANDATORY TAIL — COPY INTO THE NEXT FRESH SESSION

### 1. Identity and authority
Session ID:
Primary assignment:
Incoming last accepted baseline: [exact ID/version/content digest]
Incoming pending contribution: [exact ID/version/content digest, or NONE]
Candidate outgoing contribution: [exact ID/version/content digest]
Governing scope and protocol versions:
Build authorization: NONE

### 2. Admission of the previous contribution
Incoming tail checked: YES / NO
Incoming artifacts opened: [exact list; identify unavailable items]
Previous contribution rubric:
R01: PASS / FAIL — [reason and evidence]
R02: PASS / FAIL — [reason and evidence]
R03: PASS / FAIL — [reason and evidence]
R04: PASS / FAIL — [reason and evidence]
R05: PASS / FAIL — [reason and evidence]
R06: PASS / FAIL — [reason and evidence]
R07: PASS / FAIL — [reason and evidence]
R08: PASS / FAIL — [reason and evidence]
R09: PASS / FAIL — [reason and evidence]
R10: PASS / FAIL — [reason and evidence]
R11: PASS / FAIL — [reason and evidence]
R12: PASS / FAIL — [reason and evidence]
R13: PASS / FAIL — [reason and evidence]
R14: PASS / FAIL — [reason and evidence]
R15: PASS / FAIL — [reason and evidence]
R16: PASS / FAIL — [reason and evidence]
Admission decision: ACCEPT / REJECT
Last accepted state after this check:
Rejected claims and dependent claims requiring reassessment:

[For the first worker only: identify the foundation packet instead of a
previous worker contribution; do not invent an earlier acceptance.]

### 3. State to carry forward
Blocker table:
[B1–B12, each with OPEN / FREEZE-CANDIDATE / ACCEPTED-FREEZE / RETAINED;
exact contract version; satisfied criteria; remaining criteria]

7R status and supporting crosswalk:
Retained-contract conditions and integration status:
Accepted facts/derivations: [claim IDs, categorical classes, source/artifact refs]
Weak or unverified claims: [explicit labels and prohibited uses]
Superseded rules: [old clause → replacement clause]
Reopened or invalidated claims and dependency impact:

### 4. Exact artifacts to bring
[For each artifact:
ID/name; locator or attached filename; version/content digest;
required sections/case IDs; purpose; availability]

Mandatory packet:
- This complete tail.
- Current accepted normative baseline and pending delta.
- Original obligation ledger and review-finding crosswalk.
- Relevant opened primary-source snapshots or precise retrieval locators.
- Acceptance corpus and relevant golden artifacts/oracles.
- Adversarial coverage matrix.
- Unknowns register.
- Supersession and dependency-impact ledger.

Missing artifacts and the claims they prevent:
Do not rely on these rejected or superseded artifacts:

### 5. Open threads
[For each:
unknown/requirement ID; exact unresolved question; category;
current evidence; blocker/completion impact; closure condition;
next action; assigned next sequential session]

Unresolved contradictions:
Surviving adversarial cases:
Original obligations not yet reconciled:

### 6. Landscape change
Changed since the previous accepted state: YES / NO / UNKNOWN
External source or source-contract changes:
Recovered authority or newly available evidence:
Semantic changes:
Scope/authority changes:
Blocker and dependency consequences:
What was actually checked:
What was not checked:

[NO must be limited to the inspected scope.
UNKNOWN is required where change was not established.]

### 7. Rubric assessment of this outgoing contribution
R01: PASS / FAIL — [reason and evidence]
R02: PASS / FAIL — [reason and evidence]
R03: PASS / FAIL — [reason and evidence]
R04: PASS / FAIL — [reason and evidence]
R05: PASS / FAIL — [reason and evidence]
R06: PASS / FAIL — [reason and evidence]
R07: PASS / FAIL — [reason and evidence]
R08: PASS / FAIL — [reason and evidence]
R09: PASS / FAIL — [reason and evidence]
R10: PASS / FAIL — [reason and evidence]
R11: PASS / FAIL — [reason and evidence]
R12: PASS / FAIL — [reason and evidence]
R13: PASS / FAIL — [reason and evidence]
R14: PASS / FAIL — [reason and evidence]
R15: PASS / FAIL — [reason and evidence]
R16: PASS / FAIL — [reason and evidence]
Global self-assessment: PASS / FAIL
Contribution status:
PENDING FRESH-SESSION ADMISSION / REJECTED
If failed: exact repairs required before admission

### 8. Copy-paste instruction for the next session
You are the next sequential UnSilo v1 repair worker.
First verify this tail and its exact artifacts against the rubric.
Admit no failed contribution.
Use this accepted baseline: [exact identifier].
Your single primary assignment is: [bounded question].
Resolve these obligations: [IDs and acceptance criteria].
Open these artifacts first: [exact list].
Produce or amend: [named artifact and required contents].
Challenge it with: [specific adversarial cases].
Check these dependencies: [exact list].
Do not reopen settled matters without a cited defect or dependency impact.
If the assignment cannot close, preserve the open criteria and specify
the next dedicated session. End with this mandatory tail.

### 9. Program disposition
Artifact 1 decision procedure evaluated in full: YES / NO
Evaluator role: REPAIR WORKER / ASSEMBLER / INDEPENDENT FINAL REVIEWER
Research completion: NOT ESTABLISHED / FALSE / TRUE
Unsatisfied or unevaluated predicates:
Next sequential action:
Build authorization: NONE
```

## Independent stop rule

The assembler may propose completion but cannot terminate the round. A fresh independent session must open the exact corrected baseline and acceptance package, check the full obligation ledger and primary evidence, examine the adversarial coverage, apply every rubric dimension, and evaluate Artifact 1's complete boolean procedure.

- If any predicate is false or unevaluated, the round continues with a bounded, sequential repair assignment.
- If a correction changes semantics or supporting evidence, affected acceptance is repeated before another completion claim.
- The round ends only when that independent session records **rubric PASS**, evaluates the boolean procedure as **TRUE**, and states definitively: **RESEARCH CAN BE COMPLETED**.
- That statement closes the research gate only. Build authorization remains a separate operator decision.
