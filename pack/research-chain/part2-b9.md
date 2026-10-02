[PART2-START]
Part 2 — B9-OPERATOR-CONTRACT (RECONSTRUCTED)
Disposition: REPAIRED-PENDING-ADMISSION.
Authority track: RECONSTRUCTED only.
Original authority status: U-1R-AUTH-001 remains carried.
Dependency caution: RECON-ECLASS-PD-AO-DD-v2.0 is not admitted authority. Any classification-dependent behavior below requires either Foundation-v2 explicit clauses or fresh admission of the classifier dependency.
Build authorization: NONE.
B9-OPERATOR-CONTRACT-RECONSTRUCTED-v1.0
1. Contract identity
Contract ID
UNSILO-B9-OPERATOR-CONTRACT-RECONSTRUCTED-v1.0
Purpose
Defines the complete operator legality layer for UnSilo v1 reconstructed semantic queries.
An operator is a typed semantic transformation.
An operator is not:
• a SQL fragment,
• an implementation convenience,
• an inference shortcut,
• a model-generated interpretation.
Every operator has:
1. fixed input element types,
2. fixed output element/result types,
3. parameter schema,
4. dependency requirements,
5. legality conditions,
6. deterministic result schema,
7. explicit non-VALUE states.
No runtime or compiler component may infer missing legality.
2. Result-state vocabulary
All operators emit one of the pinned result states.
2.1 VALUE
Meaning: The requested semantic operation completed and all required dependencies were satisfied.
Schema:
VALUE {
    result_payload,
    evidence_refs,
    dependency_hashes,
    computation_receipt
}
A VALUE requires:
• admitted evidence,
• valid dependencies,
• legal composition,
• satisfied B5/B6 prerequisites where applicable,
• B10 closure obligations before final factual emission.
2.2 ABSTENTION
Meaning: The operator is defined, but the evidence ceiling prevents producing the requested semantic claim.
Schema:
ABSTENTION {
    reason_code,
    missing_capability,
    evidence_ceiling,
    available_observation
}
Examples:
• classifier cannot determine category,
• temporal relation cannot be established,
• source does not expose required field.
2.3 UNKNOWN / INCOMPARABLE
Meaning: The comparison or relation cannot be determined under current compatible evidence.
Schema:
UNKNOWN {
    reason_code,
    unresolved_dependencies,
    compared_scopes
}
Examples:
• incompatible populations,
• unresolved membership,
• unknown temporal bound.
2.4 ERROR / REJECTION
Meaning: The requested operation is illegal.
Schema:
REJECT {
    reason_code,
    violated_contract,
    offending_node
}
Examples:
• undefined operator,
• illegal composition,
• missing required dependency.
3. Operator family registry
Closed operator families:
1. Inventory operators
2. Filtering operators
3. Aggregation operators
4. Composition operators
5. Classification operators
6. Temporal operators
7. Disclosure operators
8. Coverage operators
9. Comparison operators
10. Evidence operators
No additional family may be introduced without a new contract version.
4. Inventory operators
4.1 OBSERVE_SET
Signature
OBSERVE_SET(
    SourcePopulation
)
→ Set<Element>
Parameters
source_contract_id
source_contract_version
scope
Legality
Requires:
• SourceCheck passed,
• source contract admitted,
• acquisition receipt exists.
Forbidden:
• uncontracted source,
• implicit source expansion.
Output
VALUE {
    admitted_elements[],
    provenance[]
}
Failure:
REJECT(SOURCE_NOT_ADMITTED)
4.2 GET_FIELD
Signature
GET_FIELD(
    Element,
    FieldIdentifier
)
→ FieldValue
Output states
VALUE:
field_value
ABSTENTION:
FIELD_UNAVAILABLE
UNKNOWN:
FIELD_CONFLICTED
Reject:
FIELD_NOT_DECLARED
5. Filtering operators
5.1 FILTER
Signature:
FILTER(
    Set<Element>,
    Predicate
)
→ Set<Element>
Parameters:
predicate_version
Legality:
• predicate must have valid type signature,
• filtering occurs before counting,
• unknown predicate results propagate.
Illegal:
FILTER_AFTER_AGGREGATION
5.2 FILTER_WITH_UNKNOWN
Explicit three-way filtering.
Signature:
FILTER_WITH_UNKNOWN(
    Set<Element>,
    Predicate
)
→ {
    matched,
    unmatched,
    unknown
}
Purpose: Prevents silent removal of unknown records.
6. Aggregation operators
6.1 COUNT
Signature:
COUNT(
    Set<Element>
)
→ Integer
Legality:
Requires:
• input population frozen,
• filters already applied.
Forbidden:
COUNT(raw_join_output)
where joins can multiply rows.
6.2 DISTINCT_COUNT
Signature:
DISTINCT_COUNT(
    Set<Element>,
    identity_key
)
→ Integer
Requires:
• stable identity contract,
• pinned registry version where entities are involved.
6.3 GROUP_BY
Signature:
GROUP_BY(
    Set<Element>,
    GroupExpression
)
→ GroupedSet
Requires:
• grouping element type declared,
• vocabulary version pinned.
7. Composition operators
Composition operators consume B2/B3 legality rules.
7.1 COMPOSE_POPULATIONS
Signature:
COMPOSE_POPULATIONS(
    PopulationA,
    PopulationB,
    CompositionRule
)
→ Population
Required:
B2 composition compatibility
B3 change/decomposition semantics
Allowed:
• compatible source scopes,
• compatible ontology versions,
• compatible membership versions.
Reject:
ILLEGAL_COMPOSITION
7.2 COMPARISON
Signature:
COMPARE(
    PopulationA,
    PopulationB,
    ComparisonRule
)
→ ComparisonResult
Result:
VALUE
UNKNOWN_INCOMPARABLE
REJECT
A comparison cannot silently normalize incompatible populations.
8. Classification operators
8.1 CLASSIFY
Signature
CLASSIFY(
    Element,
    ClassificationContract,
    Version
)
→ ClassificationAssertion
Dependency: Classification contract must be admitted.
Current state: RECON-ECLASS-PD-AO-DD-v2.0 is pending admission.
Therefore:
CLASSIFY(...)

→ ABSTENTION(CLASSIFIER_NOT_ADMITTED)
unless another admitted contract exists.
8.2 CLASSIFICATION_FILTER
Signature:
CLASSIFICATION_FILTER(
    Set<Element>,
    Label,
    ClassificationContract
)
Possible outputs:
VALUE: classification exists.
ABSTENTION: classifier unavailable.
UNKNOWN: conflicting labels.
Reject: classifier contract missing.
9. Temporal operators
Consumes B4 accepted temporal semantics.
9.1 EFFECTIVE_ELIGIBLE
Signature:
EFFECTIVE_ELIGIBLE(
    Assertion,
    EffectiveCut
)
→ BooleanState
States:
KNOWN
UNKNOWN
UNBOUNDED
No conversion:
UNBOUNDED ≠ TRUE
9.2 KNOWLEDGE_ELIGIBLE
Signature:
KNOWLEDGE_ELIGIBLE(
    Assertion,
    KnowledgeCut
)
Checks whether assertion was available at the specified knowledge boundary.
9.3 TEMPORAL_RELATE
Signature:
TEMPORAL_RELATE(
    AssertionA,
    AssertionB,
    Relation
)
Relations:
BEFORE
AFTER
OVERLAPS
CONTAINS
Unknown bounds produce:
UNKNOWN_TEMPORAL_RELATION
10. Disclosure operators
10.1 ADMIT_DISCLOSURE
Signature:
ADMIT_DISCLOSURE(
    SourceRecord
)
→ DisclosureStatement
Requires:
• publisher/registrant source,
• exact provenance,
• document version.
10.2 DISCLOSURE_PROPOSITION
Signature:
EXTRACT_PROPOSITION(
    DisclosureStatement
)
→ Proposition
Output: VALUE only represents: "publisher stated X"
Never: "world is X"
11. Coverage operators
11.1 SOURCE_COVERAGE_CHECK
Signature:
SOURCE_COVERAGE_CHECK(
    SourceContract,
    QueryScope
)
→ CoverageResult
Requires:
• SourceCheck,
• EnumerationProof where completeness/non-observation is claimed.
11.2 NON_OBSERVATION
Signature:
QUALIFIED_NON_OBSERVATION(
    Scope,
    ExpectedPopulation
)
Requires:
B5:
• SourceCheck,
• EnumerationProof.
B6:
• write/admission prerequisites.
Without these:
REJECT(QN_PREREQUISITE_FAILED)
12. Evidence-class propagation
Every operator declares evidence behavior.
Evidence classes
SOURCE_RECORD
PUBLISHER_STATEMENT
REGISTRANT_STATEMENT
CLASSIFICATION_ASSERTION
DERIVED_METRIC
COUNTEREVIDENCE
Propagation rules:
Input Output
Source record may support derived assertion
Publisher statement remains attributed
Classification assertion cannot exceed classifier ceiling
Derived metric requires MetricProof/B10 closure
Counterevidence preserved, never discarded
13. Unavailable field behavior
Unavailable:
FIELD_UNAVAILABLE
must propagate unless the operator explicitly defines handling.
Forbidden:
missing field → false
missing field → zero
missing field → empty
14. Classifier abstention behavior
Classifier states:
CLASSIFIED
ABSTAINED
CONFLICTED
UNAVAILABLE
Rules:
• ABSTAINED cannot enter VALUE population.
• CONFLICTED cannot be silently projected.
• UNAVAILABLE cannot become negative evidence.
15. Membership behavior
Consumes B8 registry semantics.
Every membership-sensitive operator requires:
registry_version
membership_snapshot
Raw membership history cannot be joined directly.
Allowed:
registry_snapshot(version)
Forbidden:
join(all_membership_decisions)
16. Missing dependency behavior
Any missing dependency:
MISSING_DEPENDENCY
No operator may:
• infer defaults,
• choose latest version,
• use current registry implicitly,
• use current ontology implicitly.
17. Complete typing matrix
Valid expressions
Expression Result
COUNT(Filter(Posting, Predicate)) VALUE
TEMPORAL_ELIGIBLE(Assertion, Cut) VALUE/UNKNOWN
COMPARE(CompatiblePopulationA,B) VALUE
SOURCE_COVERAGE_CHECK(AdmittedSource) VALUE
DISCLOSURE_PROPOSITION(RegistrantStatement) VALUE
Invalid expressions
Expression Result
COUNT(Classification without admitted contract) REJECT
Compare incompatible registries UNKNOWN_INCOMPARABLE
SUM(untyped amount field) REJECT
Non-observation without EnumerationProof REJECT
Temporal relation with missing required bounds UNKNOWN
Underdetermined expressions
Expression Result
CLASSIFY using pending RECON-ECLASS contract ABSTENTION
Combine populations with unresolved B2 compatibility UNKNOWN
Claim absence from incomplete source REJECT
18. Corpus alignment requirement
All RECON-ACCEPTANCE-CORPUS-v2.0 questions must resolve through this operator vocabulary.
Mapping rules:
• R-I questions → inventory/filter/evidence operators.
• R-C questions → composition/classification/comparison operators.
• R-L questions → temporal operators.
• R-D questions → disclosure operators.
• R-O questions → coverage/evidence operators.
The full item-by-item mapping is deferred to Part 3.
19. B2/B3 integration
Operator legality depends on:
B2
Composition legality:
• compatible populations,
• compatible dependencies,
• explicit join semantics.
B3
Change/decomposition:
• changed dependencies invalidate prior results,
• decompositions preserve history,
• comparisons require compatible versions.
No operator may bypass B2/B3 by compiling directly into SQL.
20. B10 boundary
No operator emits final factual VALUE when B10 closure obligations are unmet.
Required closure:
• evidence refs,
• dependency hashes,
• computation receipt,
• counterevidence obligations,
• reproducibility package.
Before B10:
semantic VALUE candidate
After B10:
admissible result
21. B9 completion status
Required artifacts:
Criterion Status
Operator families defined PRESENT
Input/output types PRESENT
Parameter types PRESENT
Legality rules PRESENT
Dependency/version requirements PRESENT
Deterministic result schema PRESENT
VALUE/abstention/unknown/error vocabulary PRESENT
Evidence propagation PRESENT
Unavailable fields PRESENT
Classifier abstention PRESENT
Membership handling PRESENT
Missing dependency handling PRESENT
Typing matrix PRESENT
Corpus alignment FRAMEWORK PRESENT; full crosswalk Part 3
Remaining admission dependencies:
• Full 40-item corpus operator mapping.
• Independent fresh admission.
• Original Wave-7 authority remains unavailable.
• RECON-ECLASS-PD-AO-DD-v2.0 remains unadmitted.
Disposition: REPAIRED-PENDING-ADMISSION.
[PART2-END]
