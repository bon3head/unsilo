[PART1-START]
Part 1 — B1-QUERY-DEFINITION-CONTRACT (RECONSTRUCTED)
Disposition: REPAIRED-PENDING-ADMISSION.
Authority track: RECONSTRUCTED only.
Original authority status: U-1R-AUTH-001 remains carried; the original Wave-7 question corpus is not recovered. This contract defines the reconstructed semantic surface only and does not claim equivalence to the missing original.
Build authorization: NONE.
B1-QUERY-DEFINITION-CONTRACT-RECONSTRUCTED-v1.0
1. Contract identity
Contract ID
UNSILO-B1-QUERY-DEFINITION-CONTRACT-RECONSTRUCTED-v1.0
Contract purpose
Defines the closed typed query representation used by UnSilo v1 reconstructed acceptance semantics.
A query is not free-form SQL, natural language, or an implementation-defined predicate. A query is a closed abstract syntax tree (AST) whose:
• node forms are versioned,
• operators have declared signatures,
• parameters have declared types,
• dependencies are pinned,
• serialization is canonical,
• compilation target is deterministic SQL generation,
• unsupported semantics terminate as UR or REJECT rather than becoming implementation guesses.
SQL is an execution target, not a semantic authority.
2. Query identity model
2.1 Query object
A query object is:
QueryDefinition {
    contract_version,
    query_kind,
    ast,
    dependency_pins,
    scope_declaration,
    knowledge_cut,
    effective_cut,
    compiler_identity,
    serialization_version
}
Required fields:
Field Type Required Meaning
contract_version VersionString YES B1 contract version
query_kind Enum YES Inventory / Composition / Lifecycle / Disclosure / Coverage
ast ASTNode YES Closed query expression
dependency_pins DependencySet YES Exact semantic dependencies
scope_declaration ScopeObject YES Source and population boundaries
knowledge_cut TimeBound CONDITIONAL Required when historical knowledge eligibility applies
effective_cut TimeBound CONDITIONAL Required when effective-time eligibility applies
compiler_identity CompilerIdentity YES Compiler name/version
serialization_version VersionString YES Canonical byte format version
3. Closed AST schema
3.1 Root node
Every valid AST has exactly one root:
QueryRoot
Schema:
QueryRoot {
    select: Projection,
    from: PopulationExpression,
    where: PredicateExpression | TRUE,
    group_by: GroupExpression[],
    order_by: OrderExpression[],
    limit: Integer | ABSENT
}
No other root forms are permitted.
4. AST node forms
4.1 Population nodes
SourcePopulation
Represents an admitted source-backed population.
Fields:
SourcePopulation {
    source_contract_id: Identifier,
    source_contract_version: VersionString,
    entity_type: EntityType,
    scope_filter: PredicateExpression
}
Legal:
• SEC registrant disclosures
• company recruiting representations
• H/D/R source-contract surfaces
Illegal:
• undeclared source
• implicit crawling scope
• unspecified acquisition boundary
JoinPopulation
Represents a B2-governed composition of populations.
Fields:
JoinPopulation {
    left: PopulationExpression,
    right: PopulationExpression,
    join_operator: JoinOperator,
    compatibility_pin: DependencyReference
}
Allowed join operators:
EXACT_ID_JOIN
DECLARED_RELATION_JOIN
VERSIONED_MEMBERSHIP_JOIN
TEMPORAL_COMPATIBLE_JOIN
Rejected:
FUZZY_IMPLICIT_JOIN
NAME_ONLY_JOIN
UNDECLARED_GRAPH_EXPANSION
FilteredPopulation
Fields:
FilteredPopulation {
    population: PopulationExpression,
    predicate: PredicateExpression
}
Filtering occurs before:
• counting,
• aggregation,
• denominator construction.
A query MUST NOT remove unknown members after counting to create a clean percentage.
5. Element types
The closed element universe:
Posting
PostingRepresentation
Company
SourceRecord
DisclosureStatement
PropertyAssertion
ClassificationAssertion
MembershipDecision
TemporalAssertion
Observation
No runtime-created element types are legal.
Unknown element categories produce:
REJECT(UNDECLARED_ELEMENT_TYPE)
6. Predicate expression schema
6.1 Predicate node
Predicate {
    operator,
    operands[],
    parameters{}
}
Every predicate requires:
• declared operator,
• declared operand types,
• declared parameter schema.
Missing any component:
REJECT(UNBOUND_OPERATOR)
6.2 Predicate operators
Closed operator families:
Equality
EQ(element.field, typed_value)
Parameter:
typed_value:
    Text
    Integer
    Decimal
    Date
    Timestamp
    Enum
Membership
IN(element.field, ControlledVocabulary)
Requires:
• vocabulary ID,
• vocabulary version.
Temporal eligibility
ELIGIBLE_AT(
    assertion,
    effective_cut,
    knowledge_cut
)
Consumes B4 semantics.
Allowed temporal states:
KNOWN
UNBOUNDED
UNKNOWN
No UNKNOWN coercion.
Evidence availability
HAS_EVIDENCE(
    evidence_class
)
Evidence classes are dependency-pinned.
Classification predicate
CLASSIFIED_AS(
    element,
    classification_contract,
    label
)
Requires:
• admitted classifier contract,
• classifier version,
• evidence reference.
Unadmitted labels:
UR(CLASSIFICATION_NOT_ADMITTED)
7. Parameter type system
Allowed primitive parameters:
Type Encoding
String UTF-8 normalized string
Integer Signed canonical decimal
Decimal Exact decimal representation
Boolean true/false
Date YYYY-MM-DD
Timestamp UTC ISO-8601 Z form
Enum Versioned symbol
Identifier Contract-scoped identifier
Version Semantic version
Forbidden:
• floating-point parameters,
• locale-dependent dates,
• implementation-specific objects,
• arbitrary JSON blobs without schema.
8. Dependency pin model
Every query pins dependencies that can affect meaning.
Required dependency categories:
DependencySet {
    schema_version,
    source_contract_versions[],
    ontology_version,
    registry_version,
    temporal_contract_version,
    classification_contract_versions[],
    compiler_version
}
A missing dependency pin creates:
REJECT(MISSING_SEMANTIC_DEPENDENCY)
A changed dependency makes prior results stale.
9. Rejection rules
The compiler MUST reject:
Syntax rejection
MALFORMED_AST
Examples:
• missing required field,
• wrong node shape,
• unknown node type.
Type rejection
TYPE_ERROR
Examples:
• comparing date to integer,
• applying composition operator to disclosure element.
Semantic rejection
ILLEGAL_COMPOSITION
Examples:
• combining incompatible populations,
• bypassing B2 compatibility rules.
Evidence rejection
INSUFFICIENT_EVIDENCE
Examples:
• emitting VALUE without required evidence class,
• missing SourceCheck prerequisite.
Dependency rejection
MISSING_DEPENDENCY
Examples:
• missing ontology version,
• missing registry version.
Unsupported reconstruction
UNSUPPORTED_RECONSTRUCTED_SEMANTIC
Used where the reconstructed contract cannot establish the intended original meaning.
10. Canonical serialization specification
10.1 Serialization format
Canonical representation:
UTF-8 JSON Canonical Form
with additional UnSilo ordering rules.
Serialized bytes are:
UTF8(
    canonical_json(
        QueryDefinition
    )
)
11. Canonical ordering
Objects:
• keys sorted lexicographically by UTF-8 byte order.
Arrays:
• semantic arrays preserve declared order.
• unordered collections are sorted by canonical child serialization bytes.
Dependency pins:
[
 dep_A,
 dep_B,
 dep_C
]
must be byte-sorted.
12. Literal normalization
Strings
Before serialization:
• Unicode NFC normalization.
• No trimming unless field contract explicitly requires trimming.
• Case normalization only where schema declares case-insensitive semantics.
Numbers
Integer:
0012
becomes:
12
Decimal:
1.0
becomes:
1
No scientific notation.
Boolean
Only:
true
false
Dates
Only:
YYYY-MM-DD
Timestamps
Only:
YYYY-MM-DDTHH:MM:SSZ
13. Absent versus explicit values
ABSENT and NULL are different.
ABSENT
Field not present because:
• not applicable,
• not requested,
• not part of schema branch.
NULL
Explicit unknown value.
Serialized:
"field": null
ABSENT:
field omitted
They MUST NOT hash identically.
14. Query hash specification
Hash algorithm
SHA-256
Hashed content
Exactly:
canonical_serialized_query_definition_bytes
excluding:
• execution timestamp,
• runtime receipt,
• generated SQL text,
• execution environment.
Including:
• AST,
• dependencies,
• compiler identity,
• serialization version,
• scope,
• cuts.
Hash field:
query_definition_hash
15. Compiler identity and query identity
Compiler identity:
UNSILO-B1-COMPILER-v1.0
Compiler identity is part of query semantics.
Relationship:
QueryDefinitionHash =
SHA256(
    serialized QueryDefinition
)
Compiler version is included in the serialized dependency set.
Therefore:
same AST + different compiler version ≠ identical query identity.
Compilation changes require a new compiler identity.
16. AST-to-SQL golden specifications
SQL is generated from AST.
SQL is never authored directly.
Golden 1 — Posting inventory
AST:
COUNT(
 FILTER(
   PostingRepresentation,
   SourceContract = "H"
 )
)
Expected meaning:
Count admitted posting representations from H boundary only.
Expected SQL shape:
SELECT COUNT(posting_id)
FROM admitted_postings
WHERE source_contract='H';
Result shape:
{
 outcome: VALUE,
 count: Integer
}
Golden 2 — Knowledge-cut eligibility
AST:
ELIGIBLE_AT(
 PostingRepresentation,
 knowledge_cut="2026-01-01"
)
Expected meaning:
Return representations known by the specified knowledge cut.
Result:
VALUE
UNKNOWN
REJECT
depending on temporal evidence completeness.
Golden 3 — Composition count
AST:
COUNT(
 FILTER(
   Posting,
   CLASSIFIED_AS(
      Posting,
      ClassificationContract-v1,
      label
   )
 )
)
Expected:
Classifier admission required.
Missing classification:
UR(CLASSIFICATION_NOT_AVAILABLE)
17. Acceptance corpus crosswalk policy
The reconstructed corpus:
RECON-ACCEPTANCE-CORPUS-v2.0
is the required acceptance surface.
Each item MUST map to exactly one:
1. canonical typed expression,
2. permitted UR with reason,
3. rejection with reason.
No item may disappear.
No item may be satisfied by undefined syntax.
18. Corpus admission rules
Fields unavailable or unacquired
FIELD_STATE.UNAVAILABLE
FIELD_STATE.NOT_ACQUIRED
FIELD_STATE.MALFORMED
FIELD_STATE.CONFLICTED
These states propagate.
They do not become:
false
zero
empty
not present
Filtering before counting
Required execution order:
source admission
→ schema validation
→ evidence eligibility
→ dependency compatibility
→ filtering
→ grouping
→ counting
→ result emission
Illegal:
count first
remove unknowns later
emit percentage
Knowledge-cut eligibility
A fact may answer a historical query only when:
effective eligibility
AND
knowledge availability
are satisfied under the accepted temporal contract.
Unknown temporal boundaries produce:
UNKNOWN
not inferred inclusion/exclusion.
19. B1 completion status
Required B1 artifacts defined:
• versioned closed AST schema: PRESENT
• canonical serialization specification: PRESENT
• hash algorithm and hashed boundary: PRESENT
• compiler/query identity relationship: PRESENT
• AST-to-SQL golden specification format: PRESENT
• reconstructed corpus crosswalk framework: PRESENT
• unavailable-field/filtering/knowledge-cut admission rules: PRESENT
Remaining admission dependency:
• Full 40-item corpus crosswalk execution is deferred to Part 3.
• Original Wave-7 corpus remains unrecovered.
• This artifact is a reconstructed candidate and not a freeze claim.
Disposition: REPAIRED-PENDING-ADMISSION.
[PART1-END]
