[PART3-START]
Part 3 — RECON-ACCEPTANCE-CORPUS-v2.0 CROSSWALK, B1/B9 RECONCILIATION, RECONSTRUCTION LIMITATIONS
Disposition: REPAIRED-PENDING-ADMISSION.
Authority track: RECONSTRUCTED only.
Original authority status: U-1R-AUTH-001 remains carried.
Purpose: Demonstrate that every reconstructed acceptance question has a defined typed semantic path or an explicit UR/rejection state.
Build authorization: NONE.
1. Corpus crosswalk
Crosswalk notation
Typed expression references:
• INV — inventory operators
• FLT — filtering operators
• AGG — aggregation operators
• CMP — composition/comparison operators
• CLS — classification operators
• TMP — temporal operators
• DISC — disclosure operators
• COV — coverage/evidence operators
Result classes:
• VALUE — permitted only after dependency and closure obligations.
• UR(reason) — unresolved because required semantics/evidence are unavailable.
• REJECT(reason) — illegal request or unsupported semantic operation.
• ABSTENTION(reason) — defined operator exists, but evidence ceiling prevents assertion.
2. R-I* Inventory crosswalk
R-I1
Question: admitted observed postings for company, cuts, scope without equating postings to openings/hires.
Typed expression:
AGG.COUNT(
  FLT(
    INV.OBSERVE_SET(SourcePopulation),
    PostingRepresentation.admitted=true
  )
)
Result: VALUE
Restrictions:
• output is posting representation count only.
• no hiring/opening inference.
R-I2
Question: eligible source representations under H/D/R boundary.
Typed expression:
INV.OBSERVE_SET(
 SourcePopulation(source_contract_version)
)
Result:
• VALUE for admitted sources.
• REJECT(SOURCE_NOT_ADMITTED) otherwise.
R-I3
Question: identity, revisions, mirrors, duplicates, evergreen postings.
Typed expression:
INV.GET_FIELD(
 PostingRepresentation,
 identity_fields
)
+
B8 membership/version semantics
Result: VALUE
If identity rule missing: UR(IDENTITY_RULE_UNAVAILABLE)
R-I4
Question: publisher-declared fields with provenance.
Typed expression:
INV.GET_FIELD(
 PostingRepresentation,
 FieldIdentifier
)
Result: VALUE or: ABSTENTION(FIELD_UNAVAILABLE)
R-I5
Question: unavailable, malformed, conflicting fields.
Typed expression: INV.GET_FIELD() with field-state propagation.
Result: VALUE(FIELD_STATE=...)
Never: false/zero/empty substitution.
R-I6
Question: effective-time and knowledge-time eligibility.
Typed expression:
TMP.EFFECTIVE_ELIGIBLE()
AND
TMP.KNOWLEDGE_ELIGIBLE()
Result: VALUE or: UNKNOWN(TEMPORAL_BOUND_UNRESOLVED)
R-I7
Question: what is counted and filtering before counting.
Typed expression:
AGG.COUNT(
 FLT(population,predicate)
)
Result: VALUE
Illegal: COUNT(raw_join_output)
R-I8
Question: deterministic inventory result schema.
Typed expression:
AGG.COUNT()
→ ResultState
Result schema:
VALUE
UNKNOWN
REJECT
3. R-C* Composition crosswalk
R-C1
Question: publisher declarations vs classification-required attributes.
Typed expression: DISC.ADMIT_DISCLOSURE() or: CLS.CLASSIFY()
Result:
• declaration: VALUE
• classification without admitted contract: ABSTENTION
R-C2
Question: composition element and parameter types.
Typed expression:
CMP.COMPOSE_POPULATIONS(
 element_type,
 parameter_schema
)
Result: VALUE if types match.
R-C3
Question: classifier abstention/conflicting labels.
Typed expression: CLS.CLASSIFY()
States:
CLASSIFIED
ABSTAINED
CONFLICTED
UNAVAILABLE
R-C4
Question: composition filters before denominators.
Typed expression:
AGG.COUNT(
 FLT_WITH_UNKNOWN()
)
Result: VALUE
Unknown members retained separately.
R-C5
Question: source/schema/projection dependencies.
Typed expression:
CMP.COMPOSE_POPULATIONS(
 dependency_pins
)
Missing pin: REJECT(MISSING_DEPENDENCY)
R-C6
Question: combine or compare populations.
Typed expression:
CMP.COMPARE(
 PopulationA,
 PopulationB
)
Result:
• VALUE if B2 compatible.
• UNKNOWN_INCOMPARABLE otherwise.
R-C7
Question: requested semantics exceed evidence ceiling.
Typed expression: CLS.CLASSIFY()
or: CMP.COMPARE()
Result: ABSTENTION(EVIDENCE_CEILING_EXCEEDED)
4. R-L* Lifecycle crosswalk
R-L1
Question: first observation.
Typed expression:
TMP.KNOWLEDGE_ELIGIBLE(
 Observation,
 cut
)
Result: VALUE
R-L2
Question: disappearance/non-observation meaning.
Typed expression: COV.QUALIFIED_NON_OBSERVATION()
Result: Requires B5/B6.
Without prerequisites: REJECT(QN_PREREQUISITE_FAILED)
R-L3
Question: reappearance.
Typed expression:
INV.GET_FIELD(identity)
+
TMP.TEMPORAL_RELATE()
Result: VALUE only if identity continuity established.
Otherwise: UNKNOWN(IDENTITY_UNRESOLVED)
R-L4
Question: revision vs identity change.
Typed expression: RecordVersion comparison
Result: VALUE
R-L5
Question: publication, archive, observation, effective, knowledge times.
Typed expression:
TMP.KNOWLEDGE_ELIGIBLE()
TMP.EFFECTIVE_ELIGIBLE()
Result: VALUE
R-L6
Question: KNOWN/UNBOUNDED/UNKNOWN bounds.
Typed expression: TMP.TEMPORAL_RELATE()
Result: Explicit temporal state.
R-L7
Question: historical knowledge cut eligibility.
Typed expression: TMP.KNOWLEDGE_ELIGIBLE()
Result: VALUE/UNKNOWN.
R-L8
Question: unresolved lifecycle dependencies.
Typed expression: TMP.TEMPORAL_RELATE()
Result: UNKNOWN
5. R-D* Disclosure crosswalk
R-D1
Question: admitted publisher/registrant statements.
Typed expression: DISC.ADMIT_DISCLOSURE()
Result: VALUE.
R-D2
Question: source identity/document span preservation.
Typed expression:
DISC.ADMIT_DISCLOSURE()
→ provenance payload
Result: VALUE.
R-D3
Question: preserve wording without strengthening inference.
Typed expression: DISC.EXTRACT_PROPOSITION()
Result: Publisher proposition only.
R-D4
Question: disclosure times.
Typed expression:
TMP.KNOWLEDGE_ELIGIBLE()
TMP.EFFECTIVE_ELIGIBLE()
Result: VALUE/UNKNOWN.
R-D5
Question: conflicting/superseding disclosures.
Typed expression: GET_FIELD(PropertyAssertion) with conflict preservation.
Result: VALUE(CONFLICT_SET)
R-D6
Question: missing expected disclosure.
Typed expression: COV.QUALIFIED_NON_OBSERVATION()
Result: Requires B5/B6.
Otherwise: REJECT.
R-D7
Question: disclosure result schema.
Typed expression: DISC.ADMIT_DISCLOSURE()
States: VALUE, UR, REJECT.
6. R-O* Operational crosswalk
R-O1
Question: declared source scopes.
Typed expression: COV.SOURCE_COVERAGE_CHECK()
Result: VALUE.
R-O2
Question: SourceCheck.
Typed expression: COV.SOURCE_COVERAGE_CHECK()
Result: Required before interpretation.
R-O3
Question: EnumerationProof.
Typed expression: COV.QUALIFIED_NON_OBSERVATION()
Dependency: EnumerationProof required.
R-O4
Question: discovery, pagination, termination receipts.
Typed expression: COV.SOURCE_COVERAGE_CHECK()
Result: VALUE only with acquisition receipt.
R-O5
Question: parser/schema validation.
Typed expression: INV.OBSERVE_SET()
Requires: schema validation success.
R-O6
Question: Wayback/CDX limitations.
Typed expression:
COV.SOURCE_COVERAGE_CHECK(
 WaybackSourceContract
)
Result: VALUE with limitations.
R-O7
Question: equivalent comparison scopes.
Typed expression: CMP.COMPARE()
Result: VALUE or: UNKNOWN_INCOMPARABLE.
R-O8
Question: B5+B6 before qualified non-observation.
Typed expression: COV.QUALIFIED_NON_OBSERVATION()
Missing prerequisites: REJECT.
R-O9
Question: expose coverage limitations.
Typed expression: COV.SOURCE_COVERAGE_CHECK()
Result: VALUE with limitation payload.
R-O10
Question: stop at UR/QN/rejection.
Typed expression: All operators.
Invariant: No VALUE without satisfied evidence and dependency gates.
7. B1 freeze-criterion reconciliation
B1 criterion Status Evidence
Named B1 query-definition contract PASS UNSILO-B1-QUERY-DEFINITION-CONTRACT-RECONSTRUCTED-v1.0, Part 1 §1
Versioned closed AST schema PASS Part 1 §§3-6
Node forms PASS Part 1 §4
Operator types PASS Part 1 §6
Element types PASS Part 1 §5
Parameter types PASS Part 1 §7
Required fields PASS Part 1 §2
Dependency pins PASS Part 1 §8
Rejection rules PASS Part 1 §9
Canonical serialization PASS Part 1 §§10-13
Hash algorithm PASS Part 1 §14
Hashed boundary PASS Part 1 §14
Compiler identity/version PASS Part 1 §15
Query identity relationship PASS Part 1 §15
AST-to-SQL golden specs PASS Part 1 §16
Corpus crosswalk PASS Part 3 §§1-6
Missing corpus entries PASS No reconstructed entries omitted
Undefined syntax avoidance PASS Part 1 §17
UR not concealing undefined operators PASS Crosswalk assigns explicit reasons
8. B9 freeze-criterion reconciliation
B9 criterion Status Evidence
Named B9 operator contract PASS UNSILO-B9-OPERATOR-CONTRACT-RECONSTRUCTED-v1.0, Part 2 §1
Operator families PASS Part 2 §3
Input/output element types PASS Part 2 §§4-11
Parameter types PASS Part 2 §5 and Part 1 §7
Legality rules PASS Part 2 §§4-16
Dependency requirements PASS Part 2 §§15-16
Deterministic result schema PASS Part 2 §2
VALUE distinction PASS Part 2 §2.1
Abstention distinction PASS Part 2 §2.2
Unknown/incomparable distinction PASS Part 2 §2.3
Error/rejection distinction PASS Part 2 §2.4
Evidence propagation PASS Part 2 §12
Unavailable fields PASS Part 2 §13
Classifier abstention PASS Part 2 §14
Unresolved membership PASS Part 2 §15
Missing dependencies PASS Part 2 §16
Typing matrix PASS Part 2 §17
Corpus alignment PASS Part 3 §§1-6
B2/B3 integration PASS Part 2 §19
No runtime legality guessing PASS Part 2 §1 and §19
No VALUE without B10 closure PASS Part 2 §20
9. Reconstruction limitations
9.1 Original corpus limitation
The original Wave-7 forty question texts are not recovered.
Status: U-1R-AUTH-001 = CARRIED
This crosswalk proves:
• reconstructed corpus coverage,
• reconstructed operator coverage,
• explicit disposition behavior.
It does not prove:
• identity with original wording,
• identity with original intended semantics.
9.2 Missing authority limitation
No original authority artifact was available to compare:
• question ordering,
• hidden assumptions,
• intended edge cases,
• rejected semantics.
Therefore: ORIGINAL-AUTHORITY COMPLETE = UNREACHABLE
9.3 Classification dependency limitation
Classification-dependent expressions remain conditional.
RECON-ECLASS-PD-AO-DD-v2.0 was not admitted.
Therefore:
CLASSIFY()
=
ABSTENTION unless another admitted classifier contract exists.
9.4 Admission limitation
This contribution establishes candidate completeness.
It does not establish freeze.
Required next step: fresh independent admission session verifying:
• artifact integrity,
• criterion satisfaction,
• dependency alignment,
• reconstructed-authority sufficiency.
Disposition: REPAIRED-PENDING-ADMISSION.
[PART3-END]
