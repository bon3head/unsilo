# UnSilo — Master Architecture Prompt

**Document purpose.** This is the single orientation document for any fresh reasoning session joining the UnSilo program. Read it fully before doing any UnSilo work. It states what UnSilo is, what authority it operates under, what has been established, what is genuinely unknown, and the exact rules every session must follow. It authorizes **no build and no state change** — it is a research-program record.

**How to use this document.** Treat every factual claim below as sourced from the program ledger and its cited artifacts. Where this document says UNKNOWN, do not fill the gap from intuition. Where it cites an artifact, open that artifact before relying on it. If you discover a conflict between this document and a primary artifact, the primary artifact wins and the conflict must be recorded, not silently resolved.

**Primary sources.**
- Program ledger: `hidden_files/research-chain/triage-state-2026-10-01.md`
- Authority gate: `hidden_files/research-chain/authority-gate-decision-2026-10-01.md`
- Governing baseline: `hidden_files/research-chain/repair-foundation-v2-2026-10-01.md` (canonical SHA-256 `707269c9a2dd0029ca172aea8798e9719902596233ce54123c0c5a5c4bf2310f`)
- Foundation v1 (rubric origin): `hidden_files/research-chain/repair-foundation-artifacts-2026-10-01.md` (SHA-256 `bbd4e2404fc5ed9044b8ced069c74be93129f72b47da3c7a1a165a1c6bfcb88e`)
- Stage outputs: `hidden_files/research-chain/s1-output-2026-09-30.md` through `s10-output-2026-10-01.md`
- B1/B9 repair output: `hidden_files/research-chain/b1b9-repair-extracted/` (parts 1–4)
- Rollback correction: `~/memory/2026-10-01.md` lines ~520–530 (07:00 AM ET correction)

---

## 1. Program identity and positioning

UnSilo is Justin Poli's career-hunting intelligence harness. His positioning, verbatim: "we are the people's anti palantir. we are meta's meta. we track and we analyze using what they give us and what they dont."

**Core analytical principle: absence as signal.** What institutions do not publish — gaps, missing records, unpopulated fields — is first-class analytical material, with the accepted caveat that absence from a dataset is not evidence of absence in the world. His formulation: "everything that isn't 0 is data." The most surprising event carries the most bits; the program measures the shape of the missingness, not just the gaps.

**Scope discipline: v1 is the goal, the platform is the dream.** v1 reconstructs the state of public recruiting **representations** (not the state of recruiting itself) over three evidence sources: SEC EDGAR, company-published careers resources within the H∪D∪R boundary, and Wayback CDX. The platform direction — forensic recon on data-rich companies and high-power individuals, disclosed financial graphs, confidence-scored connections, a strict-lockdown data pipeline with poison guardrails — is explicitly out of v1 scope. WARN and H-1B LCA are separate source-extension decisions (S11/S12), gated behind research-chain completion; neither repairs a v1 blocker.

**v1 claim, frozen by S1:** `PublicRecruitingState(C, T, S) = <I, Co, L, D, O>` —
I (observed posting set: postings, not openings), Co (attribute distribution: publisher-declared attributes only unless a frozen classification semantics exists), L (representation/observation history: appearance/disappearance/change/reappearance across observations, not ATS requisition state), D (publisher/registrant statements; SEC disclosure stays registrant statement, materiality-conditioned), O (evidence coverage qualification: a property of the evidence, not the company). Determinism means the same answer from identical admitted evidence + scope + semantics — never a claim of equality with unobserved internal state.

---

## 2. Authority model: Option B — RECONSTRUCTED-AUTHORITY SEMANTIC COMPLETE

On 2026-10-01 the operator chose **Option B**. This is the single most load-bearing decision in the program. Understand it exactly:

- **ORIGINAL-AUTHORITY COMPLETE is UNREACHABLE.** The original Wave-7 acceptance-question corpus (40 questions with exact texts and locators), the original twelve B10 closure assertions, the original pinned PD/AO/DD evidence-class admission contract, and the full original S1/S2/S3/S4/S6/S8/S9 session records were not recovered within the documented bounded search. `ORIGINALS_RECOVERED = PARTIAL`, permanently.
- The program therefore rebuilds the v1 semantic specification as **labeled RECONSTRUCTED artifacts**: explicitly marked RECONSTRUCTED, never called original, recovered, or equivalent. They are adversarially tested and independently checkable under surviving material.
- **Missing originals remain permanent EVIDENCE unknowns** (U-1R-AUTH-001 through U-1R-AUTH-015, carried verbatim). They are never erased, never laundered, never silently resolved. A reconstructed substitute changes a missing original's *gate effect* on the reconstructed track; it never changes the historical fact of absence.
- **Automatic recovery-impact reopening rule (self-executing):** if any missing original is recovered later, every U-record citing its absence flips to REOPENED-PENDING-IMPACT-REVIEW, every dependent freeze/acceptance is flagged for reassessment, and no downstream work proceeds on affected dependencies until a fresh session opens the recovered original, establishes provenance, compares it against the substitute, and re-admits affected work. Recovery can invalidate reconstructed acceptance; it can never be silently folded into it.
- Two completion states exist and must never be conflated. ORIGINAL-AUTHORITY COMPLETE (all original predicates) is FALSE/UNREACHABLE. RECONSTRUCTED-AUTHORITY SEMANTIC COMPLETE requires nine exact predicates (scope/authority reconciled; every open blocker criterion satisfied via reconstructed authority; retained contracts preserved and integration-verified; every freeze claim has opened primary evidence and named acceptance artifacts; every obligation has an accepted disposition; baseline complete/versioned/consistent; adversarial traceability with no unresolved gap; unknown register clean except permanent evidence unknowns resolved-by-substitute; independent review of the exact baseline passes). Current evaluation: **FALSE** — open blockers and incomplete integration remain.
- `RECON-ACCEPTANCE-CORPUS-v2.0`: the reconstructed 40-question substitute (R-I1–R-I8 inventory, R-C1–R-C7 composition, R-L1–R-L8 lifecycle, R-D1–R-D7 disclosure, R-O1–R-O10 observability/coverage) for the missing original forty. It does not claim historical equivalence.
- `RECON-B10-CLOSURE-ASSERTIONS-v2.0`: the reconstructed twelve-assertion substitute (R-B10-A01–A12: query-definition, compiler/execution, source/acquisition, schema/vocabulary evolution, identity/registry, classification, temporal, population/composition, cross-version/comparison, evidence/counterevidence, proof lifecycle/replay closure) for the missing original twelve.
- `RECON-ECLASS-PD-AO-DD-v2.0`: the reconstructed evidence-class admission contract. **Status: UNADMITTED.** Until it is admitted, every CLASSIFY path deterministically yields ABSTENTION(CLASSIFIER_NOT_ADMITTED), and no session may invoke it as admitted authority.

---

## 3. Evidence classes

Categorical, never scores. From S1, with admission prerequisites defined by the (unadmitted) reconstructed contract:

- **PD — publisher-direct.** Only what the publisher/registrant representation explicitly states, obtained through an in-scope authoritative publisher path (careers resources within H∪D∪R, delegated public ATS, SEC/registrant filing paths). Parsing may expose stated fields; interpretation that adds a proposition is not PD. Proves only the representation it contains.
- **AO — archive-observed.** An archival observation at the admitted capture/observation boundary (archive system, target locator, capture time, and preserved representation all recorded). Cannot prove uninterrupted availability, original publication time, capture completeness, or nonexistence from a missing capture.
- **DD — deterministically derived.** Identical admitted inputs plus pinned semantics yield the same canonical result; the full dependency package must let an independent session reproduce or mechanically verify it. Preserves uncertainty and counterevidence — determinism never upgrades a weak premise to certainty.
- **QN — qualified non-observation.** Admitted only after B5/B6 prerequisites: `QN(P) ⟺ CompleteWithinScope ∧ NegativeCheck=0 ∧ TemporalAdmissible ∧ PWithinClosedWorld`. Phrased as non-observation within the declared qualified evidence scope, never real-world nonexistence.
- **UR — unresolved.** The required class when admission prerequisites fail, evidence conflicts without governing resolution, scope is insufficient, or a proposition exceeds the evidence ceiling. UR is not a weaker positive class and cannot satisfy a freeze claim requiring positive primary evidence.

**WEAK** is a modifier, not a sixth class: supporting material partial, indirect, summary-only, or inference-dependent. WEAK claims may guide further research; they cannot satisfy primary-evidence or freeze criteria unless the governing acceptance rule explicitly permits it.

**What the contract cannot admit as PD/AO/DD:** a digest as proof of an omitted mechanism/source opening/experiment/question text/assertion; a prior reviewer's conclusion merely because it was accepted procedurally; a model proposal or typed label without semantic/adjudication prerequisites; a bounded NOT FOUND used beyond its search boundary; a missing record as real-world absence; a reconstructed artifact labeled original/recovered; an unopened source where first-hand evidence is required; an unresolved dependency hidden by filtering, narrowing, coercion, defaulting, or silent population change.

---

## 4. The research chain: S1 through S10

Each stage below is summarized from its output digest. A digest proves only what it says; full original session records for S1/S2/S3/S4/S6/S8/S9 are unrecovered (U-1R-AUTH-003/004/005/006/007/008/009). Do not cite a digest as proof of an omitted mechanism.

- **S1 — v1 claim and scope freeze.** Froze `PublicRecruitingState(C,T,S)=<I,Co,L,D,O>`; the PD/AO/DD/QN/UR evidence classes; the 40-question acceptance corpus (I1–I8, C1–C7, L1–L8, D1–D7, O1–O10); a terminology purge (cohort→comparison population, ontology→schema+controlled vocabulary, etc.); killed 11 folklore claims (postings=hires, disappeared=filled, SEC silence=no hiring, absence=intrinsic evidence of real-world absence, among others). Opened the careers-boundary question for S2.
- **S2 — acquisition surfaces.** Froze the careers boundary as `CareerSurface(C,t) = H ∪ D ∪ R`: company-controlled careers HTML + explicitly publisher-delegated public ATS surfaces + unauthenticated visitor-rendering GET resources ("first-party" = publisher attribution, not DNS). Established EDGAR enumeration (CIK canonical, ticker fallible; 10 req/sec; identifying User-Agent; missing UA yields silent empty body), Greenhouse/Lever public API acquisition rules, and Wayback CDX query/exhaustion mechanics (raw enumeration, resume-key traversal, lossy filter/collapse flags forbidden for exhaustion claims). Defined per-fetch acquisition metadata receipts. Killed 12 folklore claims.
- **S3 — B4 temporal semantics (later found defective).** Froze `Bound<T> = KNOWN(v) | UNBOUNDED | UNKNOWN`; half-open `[from,to)` intervals; bitemporal effective×knowledge time with correction non-leakage across knowledge cuts; granularity/timezone rules. Its blanket rule "any non-KNOWN required endpoint → UNKNOWN" was later proven by S10's adversarial review to conflate UNBOUNDED (information: affirmative no-finite-bound) with UNKNOWN (missing information) — the defect that reopened B4.
- **S4 — B5 completeness + B6 qualified non-observation.** Froze the QN master rule `QN(P) ⟺ CompleteWithinScope(F,Q,W,C,O) ∧ NegativeCheck(P)=0 ∧ TemporalAdmissible ∧ PWithinClosedWorld`; per-source exhaustion predicates (EDGAR continuations, Greenhouse meta.total reconciliation, Lever derived terminal rule, CDX resume-key exhaustion); mandatory acquisition receipts; UR demotion triggers (any one demotes to UR); cross-source negative rules (two negatives corroborate only under strict conditions; careers+EDGAR can never yield "not hiring"); B12 presentation requirements for displayed QN. 6 fixtures; 9 folklore kills.
- **S5 — B7 schema/vocabulary + B8 identity registry.** Froze schema, vocabulary, and classification as three independent versioned objects with a no-retroactive-reinterpretation rule (a result under pin vector P=(S,V,C,R) stays that result forever); vocabulary admission rules (Schema.org JobPosting is publisher vocabulary, never UnSilo's schema; inferred categories only through a frozen classifier); exact-only identity (10-digit CIK where the publisher is the filer, else opaque durable UnSilo ID; names/tickers/domains/URLs never canonical keys); PublisherIdentityBinding as evidence artifacts; bitemporal registry snapshots. 5 fixtures; 7 folklore kills.
- **S6 — B11 SQLite safety profile.** Froze the runtime contract: SQLite ≥3.37.0, STRICT tables, WAL / synchronous FULL / 4096 / UTF-8, application_id file identity, per-connection foreign_keys enforcement, integrity gates (integrity_check + foreign_key_check, fail-closed), exact numerics (INTEGER counts and money, no REAL ratios controlling thresholds), NULL≠FALSE≠QN≠UR≠domain UNKNOWN with explicit UNKNOWN channels, join fanout proofs at declared grain, FTS5 as disposable non-authoritative retrieval projection. 7 fixtures; 9 folklore kills.
- **S7 — B10 dependency closure + B12 presentation contract.** Froze dependency closure as a least fixed point over mandatory dependency classes (evidence+receipts, query+pins+cuts, vocabulary/classifier versions, registry snapshot+binding evidence, source-contract releases, SQLite build/profile, software version); replay semantics (recompute from same closed set; re-acquisition is not replay; pin migration is not replay); the B12 counterevidence contract — every claim presents World(p) = support + counterevidence + limitations under one version world, with claim-class obligations (QN, interval, classification, comparison, "no change detected"), anti-cherry-picking rules, and exact absence wording ("no counterevidence admitted under these pins", never "no counterevidence exists"). 6 fixtures; 7 folklore kills.
- **S8 — B1 query model + B9 operator algebra.** Froze the closed query model Q = ⟨φ, G, Ω, Ke, Kk, P, Ξ⟩ (typed predicate, declared grain, scope, effective/knowledge cuts, pin vector, evidence-class expectations; no implicit defaults — missing field = malformed, not UNKNOWN); the common outcome contract Outcome<T> = VALUE(T) | UR(reason), with static REJECT; six operators (Enumerate, RestrictTime, Classify_C, Aggregate_a, Difference, QN) with exact type signatures; exact-type static composition (no implicit coercions); the no-string-query rule (SQL is a compilation target, never the semantic interface); B10 emission as operator semantics (a VALUE without its dependency fragment is invalid); closure-relative determinism with ambient-state prohibition. 6 fixtures; 9 folklore kills.
- **S9 — B2 population compatibility + B3 version-aware comparison.** Froze population Π as an explicit finite set of durable identities (never inferred, never silently expanded/contracted); the DirectComparable structural predicate; four statuses (DIRECT / VERSION_AWARE_VALID / CONDITIONAL / NOT_COMPARABLE); per-axis pin-delta adjudication (ΔS/ΔV/ΔC/ΔR, one failed axis → INVALID); bridge semantics (frozen identity+version, explicit endpoints/scope/evidence, own pin vector, bitemporal validity, fail-closed; no silent composition of bridges); the Difference fence (unequal pins → REJECT even with a valid bridge; no seventh operator); peer-benchmarking and ranking fences. 6 fixtures; 7 folklore kills.
- **S10 — assembly + adversarial validation.** Assembled the 10-section unified spec and ran 20 adversarial attacks. **Verdict: NEEDS-REPAIR.** 18 attacks repelled by frozen contract language; 2 succeeded, both the same defect: S3's over-frozen "any non-KNOWN → UNKNOWN" rule conflates UNBOUNDED with UNKNOWN, which reopened B4 (only B4 stayed open; S10's claim that "7R cleared" was later rejected as unestablished). Prescribed the exact B4 repair: relation-specific logical entailment over admissible completions (TRUE iff every completion entails the relation, FALSE iff every completion entails its negation, else UNKNOWN) — not Kleene short-circuit, not a 9999-12-31 sentinel. Killed 7 session-level folklore claims; total kill log 77 + 7.

---

## 5. The rubric: R01–R16 (one line each)

Every dimension is binary PASS/FAIL. No weighting, no confidence scores, no "pass with reservations." A session may PASS while honestly reporting an open blocker; that never means the blocker passes. Worker self-assessment is provisional — the next fresh session checks it.

- **R01 Scope and authority:** claims stay within v1; original obligations and governing versions identified; changes carry explicit authority.
- **R02 Primary evidence:** every factual/freeze finding resolves to an opened primary source and exact supported proposition; unavailable evidence plainly identified.
- **R03 Evidence-class integrity:** class admission demonstrated under pinned definitions; weak claims labeled weak; unknowns explicit.
- **R04 No digest laundering:** summaries identify leads and prior claims; substantive acceptance rests on underlying authority, never on a digest chain.
- **R05 Obligation reconciliation:** every touched original requirement and review finding has a traceable disposition; unresolved obligations stay open.
- **R06 Semantic specificity:** inputs, preconditions, dependencies, operations, outputs, boundaries, failures all determinate.
- **R07 Acceptance-artifact sufficiency:** named, available, versioned artifacts expose inputs, expected results, rationale, and the verification actually performed.
- **R08 Adversarial adequacy:** cases challenge acceptance conditions, known attacks, invalid/unknown boundaries, material interactions; gaps explicitly open.
- **R09 Cross-contract consistency:** dependency impact examined; affected contracts agree or are reopened; retained contracts checked where affected.
- **R10 Unknown-register honesty:** every uncertainty has category, affected obligation, consequence, closure criterion, next action; no disappearing unknowns.
- **R11 Research/build separation:** meaning-defining decisions stay research; implementing frozen meaning is build work (never the reverse).
- **R12 Terminology stability:** pinned definitions used throughout; changes ship with a migration/crosswalk.
- **R13 Verdict discipline:** verdict follows stated criteria; acceptance, blocker freeze, research completion, and build authorization stay distinct.
- **R14 Version and change control:** exact versions cited; supersessions and downstream invalidations recorded; landscape changes evidence-backed.
- **R15 Handoff completeness:** the tail carries exact next state, artifacts, open threads, task, rubric results, admission status; references resolve.
- **R16 Independent checkability:** another session can reproduce the reasoning from the supplied package; observation, derivation, policy, and inference distinguished.

Global pass rule: `SESSION_PASS := every dimension PASS AND mandatory tail complete AND tail accurately describes body/artifacts AND no unresolved contradiction undermines claimed results.` FAIL means the contribution does not enter the accepted chain; it is preserved as rejected material with exact repair instructions. A later failure revokes the affected acceptance and flags every dependent claim for reassessment.

---

## 6. The twelve blockers: what each governs, and its TRUE current state

States below reflect the 07:00 AM 2026-10-01 correction (see §7). Do not use the ledger's superseded 04:38–05:04 AM freeze claims for B1/B9/B10.

- **B1 — Canonical QueryDefinition. State: REPAIRED-PENDING-ADMISSION.** Governs the closed typed query representation: `UNSILO-B1-QUERY-DEFINITION-CONTRACT-RECONSTRUCTED-v1.0` (19 sections) defines the QueryDefinition object (contract_version, query_kind, AST, dependency_pins, scope_declaration, knowledge/effective cuts, compiler_identity, serialization_version), a closed AST schema (QueryRoot with select/from/where/group_by/order_by/limit; population nodes SourcePopulation/JoinPopulation/FilteredPopulation; closed element universe), canonical serialization sufficient for independent byte-identical implementations, SHA-256 over delimited hashed content, a compiler identity/version with its relationship to query identity, golden AST-to-SQL specifications, and a crosswalk mapping all 40 `RECON-ACCEPTANCE-CORPUS-v2.0` questions to typed expressions or permitted UR/rejection with defined reasons. Repair output exists and is semantically sound; its admission was ruled invalid (see §7), so it must be freshly admitted before any freeze.
- **B2 — Cohort compatibility and composition. State: FROZEN (reconstructed authority).** Governs the `B2-COMPOSITION-CONTRACT` (RECONSTRUCTED): a 9-term compatibility predicate (registry/snapshot, schema/vocabulary, transform/projection, temporal world, element type, population, source contracts); a legal/illegal/abstain composition matrix for union/intersection/difference across equal pins, unequal pins (±authorized bridge), missing pins, incompatible populations, and uncertain compatibility; deterministic rejection/abstention triggers; the composition-vs-sanctioned-comparison distinction; golden cases against silently dropping unresolved membership.
- **B3 — Cross-version comparison. State: FROZEN (reconstructed authority).** Governs the `B3-CHANGE-DECOMPOSITION-CONTRACT` (RECONSTRUCTED): ChangeDecomposition with four distinct output fields (predicate_drift, ontic_change, epistemic_ingestion, entity_resolution_churn); golden cases per component plus mixed/interaction/non-identifiability cases ("do not choose the most plausible explanation" — all fields UNKNOWN); absent-evidence handling; additivity only under stated conditions; B12 counterevidence preservation.
- **B4 — Temporal semantics. State: FROZEN (reconstructed authority).** Governs the `B4-TEMPORAL-CONTRACT` + `B4-RELATION-ORACLES` (RECONSTRUCTED): typed bound domain `KNOWN(v) | UNBOUNDED | UNKNOWN`; admissible completions with universal entailment (TRUE iff all completions true, FALSE iff all false, else UNKNOWN); all Allen relations with per-relation oracles implemented as a finite symbolic decision procedure over endpoint orderings (no infinite enumeration); scope limits (point times never UNBOUNDED); effective/knowledge time separation; supersession of S3's defective blanket rule. First admitted after a substantive REJECT (wrong OVERLAPS label, under-specified completion enumeration) and a bounded rework.
- **B5 — Acquisition prerequisites. State: RETAINED-INTEGRATION-VERIFIED.** Governs SourceCheck, EnumerationProof, discovery, mandatory continuation configuration, pagination, parser/schema validation, and scope-equivalence prerequisites. Nothing frozen; integration verified against B4/B7/B8 and the reconstructed evidence-class contract; QN remains unavailable where prerequisites are not established; runtime evidence still required.
- **B6 — Constructor/write-admission prerequisites. State: RETAINED-INTEGRATION-VERIFIED.** Governs constructor and write-admission validity; malformed/incomplete acquisition cannot yield QN. Same retained/integration-verified status as B5.
- **B7 — Ontology evolution and posting population. State: FROZEN (reconstructed authority).** Governs the `B7-ONTOLOGY-EVOLUTION-CONTRACT` + `POSTING-POPULATION-CONTRACT` (RECONSTRUCTED): ontology package serialization; migration ops (RENAME/SPLIT/MERGE/ADD/DEPRECATE/REINTERPRET/NO_CHANGE) forbidding silent UNKNOWN→KNOWN / AMBIGUOUS→CONFIRMED / ABSENT→PRESENT transitions; finite upcaster application; historical interpretation rules; reified relation assertions; posting identity hierarchy (employer req ID → ATS ID → source-native ID → normalized URL → bounded field comparison); the five counting cases (mirrors/duplicates/locations/prospect postings/revisions); ADMITTED/ABSTAINED/CONFLICTED/UNKNOWN classification states with mandatory abstention cases.
- **B8 — Registry closure and ambiguous identity. State: FROZEN (reconstructed authority).** Governs the `B8-REGISTRY-CONTRACT` (RECONSTRUCTED): deterministic decision-to-snapshot materialization; membership invariant (mention_id primary key, entity_id nullable; at most one effective accepted membership per mention; zero memberships possible when unresolved); cannot-link closure as DIRECT-PAIR ONLY, non-transitive; contradictory exact bindings → AMBIGUOUS outcomes (never silent picks); snapshot canonical JSON with bytewise-ascending keys, UTF-8, SHA-256; stale-impact procedure; temporal eligibility citing frozen B4 ("B8 consumes temporal semantics. It does not redefine them."). First admission attempt voided as a tooling artifact (condensed evidence); re-admitted against full verbatim output.
- **B9 — Operator type system. State: REPAIRED-PENDING-ADMISSION.** Governs the `UNSILO-B9-OPERATOR-CONTRACT-RECONSTRUCTED-v1.0` (21 sections): 10 operator families (Inventory, Filtering, Aggregation, Comparison, Classification, Temporal, Disclosure, Coverage, Comparison, Evidence) each with fixed input/output element types, parameter schemas, legality rules, dependency/version requirements, and deterministic result schemas; the pinned result-state vocabulary VALUE / ABSTENTION / UNKNOWN-or-INCOMPARABLE / ERROR-or-REJECTION; evidence-class admission and propagation rules; classifier abstention deterministically yielding ABSTENTION(CLASSIFIER_NOT_ADMITTED) while `RECON-ECLASS-PD-AO-DD-v2.0` remains unadmitted; complete valid/invalid/underdetermined typing matrix; alignment to all 40 reconstructed corpus questions and B2/B3 semantics. Like B1: repair sound, admission invalid, must be freshly admitted.
- **B10 — Dependency closure and B12 integration. State: OPEN (later work provisional — see §7).** Governs the closure crosswalk and proof-lifecycle contract: every emitted result pins its complete dependency world; lifecycle BUILDING → SEALED → VERIFIED with any verification failure → INVALID; B12 counterevidence integration under the same dependency world. A repair contract exists and is semantically sound, but all B10 work after the invalid B1/B9 admission is quarantined as provisional pending restoration of the sequential chain.
- **B11 — SQLite safety. State: RETAINED.** Governs the adjudicated SQLite safety semantics and accepted hazard fixtures (S6 contract). Awaiting fresh retained integration.
- **B12 — Counterevidence invariant. State: RETAINED.** Governs the counterevidence invariant across findings, comparison, and rendering. Awaiting integration through B10/comparisons.

**Also UNADMITTED:** `RECON-ECLASS-PD-AO-DD-v2.0` (the reconstructed evidence-class admission contract). It is Foundation v2's contract text, but it has never passed fresh admission as invoked authority; no session may rely on it as admitted authority until it does.

---

## 7. The B1/B9 invalid admission and the pending remediation

**What happened.** On 2026-10-01 ~04:38 AM ET, a fresh admission session in chat `6abe1a5b-621c-83e9-8508-19caa91f6b01` returned ACCEPT for the B1/B9 repair, R01–R16 all PASS, and the ledger recorded B1 and B9 as FROZEN. B10 work then proceeded on that basis (repair, acceptance artifacts, and a second admission returning ACCEPT).

**Why it was ruled invalid.** At 07:00 AM ET the same day, a correction ruled the admission **procedurally non-admissible**: instead of continuing the original task that retained the four exact extraction reports, a new task was opened and fed a locally transcribed package that was **known-contaminated** at the time of use. Three known deviations: (a) a Part 3 typed-expression line was split; (b) Part 4 omitted the line `blocker/completion impact: B9 remains REPAIRED-PENDING-ADMISSION;`; (c) Part 4 changed `Recovered authority or newly available evidence: NONE.` to `Recovered authority or newly available evidence: NONE evaluated.` A checker admitted a package the program already knew was deviated. The freeze was therefore retracted.

**Consequences (current truth).**
- B1 and B9 revert to **REPAIRED-PENDING-ADMISSION**, not FROZEN. Their repair output (46,227 bytes, extracted verbatim to `b1b9-repair-extracted/`) stands as a valid repair candidate; only the admission is void.
- Chat `6abe1a5b-621c-83e9-8508-19caa91f6b01` is marked **non-admissible** and must never be cited as an admission.
- All B10 work after the invalid admission is **quarantined as provisional**, including the B10 repair output and acceptance artifacts in `b1b9-repair-extracted/b10-repair-output.txt` and `b10-acceptance-artifacts.txt`. B10 remains **OPEN**.
- The **46,227-byte versus approximately 190 KB package-size discrepancy is restored to unresolved.** The earlier claim that rendered duplication explained it was not established.
- The local ledger (`triage-state-2026-10-01.md`) still contains the superseded freeze claims; it **needs an append-only erratum** (step 1 below). Until that erratum exists, do not treat the ledger's 04:38–05:04 AM entries as current.

**Pending remediation sequence (in order, still open).**
1. Append the ledger erratum (retract B1/B9 freeze, mark the chat non-admissible).
2. Restore B1/B9 to REPAIRED-PENDING-ADMISSION in the ledger.
3. Quarantine the later B10 work as provisional in the ledger.
4. Restore the package-size discrepancy to unresolved in the ledger.
5. Resume the exact retained task `browser-task:4b530c82-709f-4689-a576-12178d17259b`.
6. Reuse the retained reports directly in a fresh Sol/High admission (exact reuse — the four original extraction reports, not a re-transcription).
7. Stop if exact reuse is impossible; do not substitute a new transcription.
8. Reassess B10 only after a valid B1/B9 ACCEPT.
9. Map illustrative "verification receipts" before another B10 admission (the second B10 admission's evidence was authored fixtures, not executed cryptographic receipts).

---

## 8. Admission and session protocol

**Fresh independent admission is the only gate.** Worker self-assessment is provisional. A contribution enters the accepted chain only when a fresh session — one that did not author the contribution — checks it against R01–R16 and the governing baseline. A later failure revokes the affected acceptance and flags every dependent claim for reassessment; previous accepted state remains identifiable.

**Verbatim evidence delivery (the B8 lesson).** Evidence must be delivered to checker sessions verbatim, in full. Condensation is forbidden: a condensed B8 package once produced a REJECT on artifacts the full output actually contained; that verdict was voided as a tooling artifact with no semantic weight. Proven protocol: two-message delivery (framing + evidence parts, then tail + admission prompt), ≤10KB chunks with per-chunk read-back verification, explicit no-condensation instruction. Repair outputs above ~40KB cannot rely on viewport transcription — have the worker's handoff carry verbatim text in the task report.

**Tail discipline.** Every session ends with the populated mandatory tail (v2 template in Foundation v2 §Artifact 3), and nothing follows it. The final line must read exactly `Build authorization: NONE` — no trailing period, no continuation. (A trailing period once rendered; the response was complete so no regeneration was performed, but the exact form is required.)

**Entry procedure for every session.** Open the incoming tail and every exact referenced artifact. Verify the previous contribution against all R01–R16 before relying on it. Confirm the last accepted baseline separately from pending/rejected material. Verify the Foundation-v2 canonical self-pin whenever Foundation v2 or its contracts are used. Run the automatic recovery-impact check (`NOT CHECKED` ≠ `NO CHANGE`). Record unavailable artifacts immediately; never invent missing content.

**Reopening.** A blocker stays open until all acceptance criteria are satisfied and a fresh session admits the freeze candidate. "Principles settled," "directionally correct," and "substitute exists" are not freezes. Retained or previously accepted contracts reopen when a new contradiction or dependency failure warrants it; earlier acceptance is not immunity. One bounded reissue per defect (anti-slop rule): if a bounded rework is rejected, the blocker stays OPEN with the defect recorded and the program moves on — no second reissue.

---

## 9. Standing operating directives

These are operator-issued and binding on every session, worker, and subagent:

1. **BLOCKERS LEAD.** Every project message carries granular lifecycle/stage at head and tail, plus what is next.
2. **One sequential track.** No parallel repair tracks, simultaneous blocker owners, or unreviewed merges. A discovered prerequisite may reorder the queue only with the defect, affected criteria, and revised queue recorded.
3. **Weak claims never exit labeled strong.** Confidence is a property of the evidence world, not the presentation. Categorical evidence classes only (PD/AO/DD/QN/UR); WEAK is a modifier with prohibited uses.
4. **Unknowns stay UNKNOWN** in the mandatory unknown-record schema (ID, question, category, affected requirements, known evidence + class, what remains unknown, effects, closure condition, next action + owning session). No disappearing unknowns.
5. **No build without separate operator authorization.** Research completion — even if ever established — does not authorize a build. Every session ends `Build authorization: NONE`.
6. **Effort policy.** Blockers settled one by one for quality assurance, never parallel. Medium effort for basic worker sessions; high effort reserved for altitude and big-information moments. Sol does worker labor on the Chat surface; Astra is conserved for governance gates (budget resets Oct 4).
7. **Sol maps first, then act.** On step-back requests, the mapping burden goes to the strongest reasoning seat; the operator keeps the authority call.
8. **Unexpected roadblock → stop and analyze.** Never route around a defect with a hack; diagnose the actual defect (the B8 condensed-evidence void and the B1/B9 transcription rollback are the standing examples).
9. **Scope discipline.** v1 is the goal, the platform is the dream. Every plan flags scope creep explicitly and feasibility-checks against the real stack (single operator, local-first laptop + VM, SQLite-first, no GPU, TS/Python, deterministic pipelines, private use).
10. **Correct the operator when he is wrong, with mechanism** (invited). Never adopt his guesses about internals, or anything unverifiable, as fact.

---

## 10. Current program state and what comes next

**True blocker table (2026-10-02):**
FROZEN — B2, B3, B4, B7, B8 (all under reconstructed authority).
REPAIRED-PENDING-ADMISSION — B1, B9 (repair output sound; admission void, must be re-admitted).
OPEN — B10 (repair exists; all post-rollback work provisional).
RETAINED-INTEGRATION-VERIFIED — B5, B6. RETAINED — B11, B12.
UNADMITTED — RECON-ECLASS-PD-AO-DD-v2.0.
ORIGINALS_RECOVERED = PARTIAL. ORIGINAL-AUTHORITY COMPLETE: UNREACHABLE. RECONSTRUCTED-AUTHORITY SEMANTIC COMPLETE: FALSE.

**What comes next, in order:** the nine-step remediation sequence in §7 (ledger erratum first), then valid B1/B9 admission by exact reuse of the retained extraction reports, then B10 reassessment with mapped verification receipts, then full retained-contract integration (B5/B6/B11/B12 against the repaired baseline), then corrected assembly (one versioned normative baseline, obligation ledger, reconstructed glossary/crosswalk, traceability matrix, unknown register, supersession ledger), then fresh independent final review of the exact baseline, then operator disposition. S11/S12 (WARN, H-1B LCA source extensions) remain gated behind chain completion.

**Key artifact locators.** Ledger: `hidden_files/research-chain/triage-state-2026-10-01.md` (needs the §7 erratum). Governing baseline: `hidden_files/research-chain/repair-foundation-v2-2026-10-01.md` (canonical SHA-256 `707269c9a2dd0029ca172aea8798e9719902596233ce54123c0c5a5c4bf2310f`). B1/B9 verbatim repair output: `hidden_files/research-chain/b1b9-repair-extracted/` (parts 1–4; the b10 files there are quarantined provisional). Rollback correction: `~/memory/2026-10-01.md` ~lines 520–530. Public mirror (digests only): https://github.com/bon3head/unsilo.

Build authorization: NONE
