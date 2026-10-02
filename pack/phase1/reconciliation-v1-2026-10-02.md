# UnSilo v1 end-to-end reconciliation (2026-10-02)

Research only. Nothing implemented; no baseline file changed; the four quarantined B1/B9 files untouched. Build authorization: NONE.

## 0. Blockers (lead)

| Item | True state | Unblock path | Owner |
|---|---|---|---|
| B2, B3, B4, B7, B8 | FROZEN (reconstructed authority) | none needed; consumed by everything below | n/a |
| B1, B9 | REPAIRED-PENDING-ADMISSION | master doc 7 steps 1 to 7 only; see pivot P6 for the step-7 dead end | harness program |
| B10 | OPEN; later work quarantined | master doc 7 steps 8 to 9, after a valid B1/B9 ACCEPT; see pivot P7 | harness program |
| B5, B6 | RETAINED-INTEGRATION-VERIFIED | runtime evidence: first receipted acquisition run | harness program |
| B11, B12 | RETAINED | final retained integration; B12 needs B10 first | harness program |
| RECON-ECLASS-PD-AO-DD-v2.0 | UNADMITTED (held; see IC-01: Foundation v2's own text makes this state ambiguous) | operator ruling R-ECLASS, then admission if required | operator |
| Build | NONE | operator | operator |

Five findings that change the picture (each grounded below):

1. **IC-01.** The UNADMITTED state of RECON-ECLASS rests on a distinction Foundation v2 never writes down. Foundation v2 says the contract resolves U-010 "once this Foundation v2 contribution is independently admitted" (`repair-foundation-v2:128`), and Foundation v2 was admitted (ledger `:71`). I relabel nothing. This needs a ruling.
2. **IC-02.** "Classification" names two different contracts. B9 ties composition classification (CLASSIFY) to the evidence-class admission contract. They are different objects. Admitting RECON-ECLASS would NOT make role families or seniority classifiable; no composition classifier exists at all. This corrects my own hopes map.
3. **IC-05.** The dashboard's "every number is a query you can open" (a SQL string) conflicts with S8's no-string-query rule for analytic results.
4. **DP-1.** The proposed schema has no evidence plane: no posting, observation, fetch-receipt, SourceCheck, or registry table. It is the tail of the operator's ledger, not of the v1 data path. Every v1 analytic panel has zero machinery behind it today.
5. **IC-12.** The B1/B9 unblock path has a dead end: master doc 7 step 7 says "Stop if exact reuse is impossible", and the retained browser task is state-unknown (`unsilo-session-prompt-2026-10-02.md:136`). If that task is gone, v1 has no path.

Grounding conventions are as in `grounding-final-2026-10-02.md`:
- File:line anchors are at branch HEAD.
- Drive files were read 2026-10-02 via the Drive connector.
- Confidence is HIGH, MEDIUM, or LOW, with what would change it.

Short paths (in the tables and citations below):
- `RC/` = `pack/research-chain/`
- `master` = `pack/unsilo-master-architecture-prompt-2026-10-02.md`
- `ledger` = `RC/triage-state-2026-10-01.md`
- `FV2` = `RC/repair-foundation-v2-2026-10-01.md`

---

## 1. S1 to S10 coherence: integration defects

Every row cites both sides. "Severity" is my judgment of effect on v1: BLOCKING (changes what v1 can emit), MATERIAL (changes a contract's meaning or a consumer), RECORD (bookkeeping, but R12/R14 failures).

| ID | Defect | Side A | Side B | Severity | Proposed disposition |
|---|---|---|---|---|---|
| IC-01 | RECON-ECLASS admission state is ambiguous | FV2:128 "resolved-by-substitute ... once this Foundation v2 contribution is independently admitted"; FV2:1166 "pending Foundation-v2 admission"; ledger:71 Foundation v2 ACCEPT, "reconstructed contract ... present" | master:121 "never passed fresh admission as invoked authority"; ledger:180 "RECON-ECLASS pending admission" (after the ACCEPT); FV2:1175 "requires fresh admission before downstream invocation" | BLOCKING: while unadmitted, every evidence class is formally UR (FV2:417), so no v1 VALUE can carry PD/AO/DD | Ruling R-ECLASS (section 6.10). Confidence MEDIUM: FV2:1175 can be read as requiring a separate admission. |
| IC-02 | "Classification" conflates evidence-class admission with composition classification | `part2-b9.md:243-245` (quarantined text): "Current state: RECON-ECLASS-PD-AO-DD-v2.0 is pending admission. Therefore: CLASSIFY(...) → ABSTENTION(CLASSIFIER_NOT_ADMITTED)"; master:42 same | FV2:122-127: RECON-ECLASS is the evidence-class admission contract (PD/AO/DD prerequisites); `RC/s5-output-2026-09-30.md:24` B7.5: "inferred categories enter results ONLY through a frozen classifier with a published mapping", the C axis of P=(S,V,C,R) | BLOCKING for composition (Co beyond raw labels) | Pivot P2. Confidence HIGH on the texts; MEDIUM that B9's retained (uncontaminated) text says the same. |
| IC-03 | Operator count: six closed operators vs ten families | `RC/s8-output-2026-09-30.md:36` "six-operator algebra (complete for the v1 question family)"; `RC/s9-output-2026-10-01.md:67` "No seventh operator." | `part2-b9.md:84` "Closed operator families:" 10, including COMPARE and COMPOSE_POPULATIONS | MATERIAL: S9's fence is stated against S8's six | Record as a supersession at corrected assembly: B9 (if admitted) replaces S8's six. S9's fence must be restated as "Difference never accepts unequal pins", which B2/B3 already freeze. Confidence HIGH. |
| IC-04 | Outcome vocabulary fragmented across contracts | S8:31 `VALUE(T) / UR(reason)` + static `REJECT`; S9:29 DIRECT / VERSION_AWARE_VALID / CONDITIONAL / NOT_COMPARABLE | `part2-b9.md:31, :46, :59` VALUE / ABSTENTION / UNKNOWN-INCOMPARABLE / REJECT; B7 ADMITTED / ABSTAINED / CONFLICTED / UNKNOWN (master:114); B2 LEGAL / ILLEGAL / ABSTAIN (master:109); B10 BUILDING / SEALED / VERIFIED / INVALID | MATERIAL: the UI must render one state per element, and the corpus crosswalk uses UR and ABSTENTION side by side (`part3-crosswalk.md` notation) | Pivot P8 (one crosswalk, no new machinery). R12 requires it anyway (FV2:92 glossary/crosswalk). Confidence HIGH. |
| IC-05 | Openable SQL vs no-string-query rule | `pack/unsilo-data-theory-2026-10-02.md:122` "Every number is a query you can open: panels trace to a SQL string"; launch prompt :133 | S8:67-71 "No ad-hoc SQL ... Raw SQL run against canonical tables is not a valid UnSilo analytic result" | BLOCKING for the evidence plane's render path | Pivot P4. Confidence HIGH. |
| IC-06 | Terminology purge undone | `RC/s1-output-2026-09-30.md:53` "cohort → comparison population; ontology → schema + controlled vocabulary" | `part1-b1.md:206` `ontology_version`; master:114 "B7-ONTOLOGY-EVOLUTION-CONTRACT"; master:109 and FV2:317 "Cohort compatibility" | RECORD (R12) | Crosswalk entry at assembly: "ontology" = schema + controlled vocabulary version; "cohort" = comparison population. Do not rename frozen contract IDs. Confidence HIGH. |
| IC-07 | D dimension has no acquisition contract for statement content | S1:37 D = "recruiting/workforce statements; SEC disclosure stays registrant statement"; R-D1 to R-D7 (FV2:234-240) | S2:15 EDGAR enumeration covers Submissions JSON plus continuations (filing metadata), with no section or span extraction; S4:103 open unknown "content-level EDGAR QN needs full document acquisition+parse (storage/operators open)" | BLOCKING for D | Gap: needs a source contract for filing-document acquisition and span extraction before any D VALUE. Not frozen anywhere; it is research (R11: meaning of "statement span" is semantic). Confidence HIGH. |
| IC-08 | Generic careers HTML (H) and visitor resources (R) cannot reach completeness | S2 boundary H∪D∪R; S2: "JS rendering is admissible observation (Duolingo careers requires JS)" | S4:31 "Generic H/R surfaces: each frozen member needs its own finite terminal contract or stays PARTIAL" | MATERIAL: H and R surfaces yield PARTIAL, so no QN and no complete inventory, until per-surface terminal contracts exist | Pivot P5. Confidence HIGH. |
| IC-09 | B10 lifecycle vs S7's two-status replay vocabulary unmapped | S7:36 "Complete-but-never-replayed = 'replayable', not 'replay-verified'" | FV2:378 lifecycle BUILDING → SEALED → VERIFIED, failure → INVALID | RECORD | Crosswalk: replayable ↔ SEALED; replay-verified ↔ VERIFIED (proposal; to be confirmed at B10 reassessment). Confidence MEDIUM. |
| IC-10 | S10 and the root README still state superseded dispositions | S10:36 "FROZEN: B1, B2, B3, B5, B6, B7, B8, B9, B10, B11, B12" | master:184-190 true table; FV2:1154 "Do not rely on ... S10 'B4 alone open' / '7R cleared'" | RECORD (R14) | Append supersession notes in the mirror or README by operator ruling; never edit the digests. Confidence HIGH. |
| IC-11 | S8 folklore count three ways; R-B10 list incomplete | S8:127 "Folklore killed (6)"; Drive `unsilo-architecture-prompt-2026-10-02.md` (read 2026-10-02) "6 fixtures; 6 folklore kills" | master:73 "6 fixtures; 9 folklore kills"; `research-chain/folklore-kill-log-2026-10-01.md:83-89` seven (#64 to #70). master:41 names 11 assertions for "A01–A12" (omits A04 mapping/projection, FV2:281); the Drive variant includes it | RECORD | Two near-identical master documents exist (pack 37,073 bytes; Drive 37,084 bytes). Ruling: which is authoritative. Confidence HIGH. |
| IC-12 | B1/B9 unblock path can dead-end | master:143-146 steps 5 to 7: resume `browser-task:4b530c82`; exact reuse; "Stop if exact reuse is impossible" | `pack/unsilo-session-prompt-2026-10-02.md:136` "The retained browser task is state-unknown." | BLOCKING if the task is gone | Pivot P6. Confidence HIGH that the path has no branch for that case. |
| IC-13 | B10 acceptance needs executed receipts; the build is NONE | ledger:259 bounded rework requires "independent verification receipts binding dependency world hash, computation receipt, replay output" | FV2:816 "Non-runtime design fixtures and explicitly identified research experiments may support semantic acceptance only within their stated evidentiary limits"; build NONE (master:173 directive 5) | BLOCKING for B10 unless experiments are used | Pivot P7. Confidence HIGH. |
| IC-14 | QN temporal admission stricter than B4 | S4:44 "point QN → point KNOWN; interval QN → both endpoints KNOWN ... UNBOUNDED insufficient" | B4 entailment can decide relations with UNBOUNDED and some UNKNOWN endpoints (ledger:104) | none: deliberate asymmetry; QN admission is not relation evaluation | Write it into the crosswalk so a later reader does not "fix" S4 toward B4. The B5/B6 checkpoint already verified integration with B4 (ledger:151). Confidence HIGH. |
| IC-15 | B9 temporal text restates the retired S3 rule | `part2-b9.md:263-269, :291-296` | S10 B4 repair contract; folklore kill #81; ledger:110 | MATERIAL | For the fresh B1/B9 admission to weigh (grounding-final A7). Confidence MEDIUM (quarantined bytes). |
| IC-16 | Evidence class (S1) vs B9's "evidence classes" list | S1 PD / AO / DD / QN / UR | `part2-b9.md` section 12 "Evidence classes: SOURCE_RECORD, PUBLISHER_STATEMENT, REGISTRANT_STATEMENT, CLASSIFICATION_ASSERTION, DERIVED_METRIC, COUNTEREVIDENCE" | MATERIAL (R12): a second vocabulary under the same name | Crosswalk or rename at admission; these are element kinds, not evidence classes. Confidence HIGH on the text (quarantine caveat). |
| IC-17 | Verdict taxonomy has no frozen home | Dashboard verdict pills CONFIRMED / KILLED / DOWNGRADED / UNKNOWN (feed spec); data theory verdict statuses | Harness spec v1.2:229 "Four-state verdicts, Justin's standing taxonomy: CONFIRMED / DOWNGRADED / KILLED / UNRESOLVED" (not a frozen contract); S1 to S10 define no verdict axis | MATERIAL: the audit-verdict axis is an operator taxonomy, not a v1 contract | Pivot P1 puts it in the ledger plane, labeled as such. Confidence HIGH. |

Checked and found coherent (no defect): S2 vs S4 per-source exhaustion predicates; S5 identity vs S9 durable-ID population; S3 knowledge-cut non-leakage vs S7 replay vs B8 snapshots; S6 NULL ≠ UNKNOWN vs B4 bound typing; S4 cross-source negatives vs S1 kill 6.

---

## 2. Blocker integration table

"Consumes" means the blocker's contract cites or depends on the other. Sources: master:108-119; FV2:306-391; ledger.

| Blocker | True state | Consumes | Consumed by | Integration status | Unblock path or freeze rationale |
|---|---|---|---|---|---|
| B1 QueryDefinition | REPAIRED-PENDING-ADMISSION | B4 (ELIGIBLE_AT), B7 (`ontology_version`), B8 (`registry_version`), B2/B3 (JoinPopulation `compatibility_pin`) per `part1-b1.md` sections 4, 6, 8 | B9, B10 (A01, A02) | Not admitted; the quarantined text has defects IC-06 and C10 (R-L4) | Master 7 steps 1 to 7; P6 if step 7 fires |
| B2 composition | FROZEN | B7 (vocabulary), B8 (registry snapshot), B4 (temporal world) | B1, B3, B9, B10 (A09) | Frozen ledger:172 | Admitted against the 9-term predicate |
| B3 change decomposition | FROZEN | B2, B7, B8, B12 | B9, B10 (A10) | Frozen ledger:172 | Admitted |
| B4 temporal | FROZEN | none upstream | B1, B5/B6, B8, B9, B10 (A08), the dashboard schema | Frozen ledger:110; dashboard point membership derived (U-DASH-04 open) | Admitted after REJECT plus bounded rework |
| B5 acquisition | RETAINED-INTEGRATION-VERIFIED | B4, B7, B8, RECON-ECLASS (ledger:151) | B6, QN, B9 coverage, B10 (A03) | Paper-verified; zero runtime receipts; QN UNKNOWN for all scopes (ledger:153) | First receipted acquisition run, as a research experiment (P7) |
| B6 write admission | RETAINED-INTEGRATION-VERIFIED | B5 | QN, B9, B10 | Same as B5 | Same as B5 |
| B7 schema evolution and posting population | FROZEN | B4 | B1, B2, B3, B9, B10 (A04, A05) | Frozen ledger:129 | Admitted |
| B8 registry | FROZEN | B4 ("consumes temporal semantics") | B1, B2, B3, B9, B10 (A06) | Frozen ledger:144 | Admitted on verbatim re-delivery |
| B9 operators | REPAIRED-PENDING-ADMISSION | B1, B2, B3, B4, B5/B6, B8, RECON-ECLASS | B10 (A01, A02, A07) | Not admitted; IC-02, IC-03, IC-15, IC-16 for the checker | Master 7 steps 1 to 7 |
| B10 closure | OPEN; post-rollback work quarantined | everything (A01 to A12) + B12 | B12 (same world), every displayed VALUE | Provisional fixtures synthetic (`RC/PROVISIONAL-b10-acceptance-artifacts.txt:548, :714`) | Master 7 steps 8 to 9, after valid B1/B9; P7 |
| B11 SQLite | RETAINED | none | everything stored | Dashboard scratch runs exercised an analog of FX-STRICT-REJECTS-TYPE-MISMATCH (REAL into INTEGER refused) and part of FX-FTS5-REBUILD (rebuild only, not canonical-equality). The other 5 S6 fixtures were not run. | Fresh retained integration at step "full retained-contract integration" (master:192) |
| B12 counterevidence | RETAINED | B10 world | every render | Cannot be verified before B10 | After B10 |
| RECON-ECLASS | UNADMITTED (held) | FV2 | B5, B9, every evidence class | IC-01 | Ruling R-ECLASS |

No blocker dropped, double-counted, or relabeled. The table's states equal the task's states and master:184-190.

---

## 3. End-to-end data path: acquisition to render

### 3.1 The path as the contracts define it

| # | Handoff | Governing contract | Evidence class carried out | On failure | Machinery today |
|---|---|---|---|---|---|
| 1 | Declare scope: company identity, surfaces, window | S2 H∪D∪R; S5/B8 PublisherIdentityBinding; S8 Q's Ω | none (declaration) | missing field = REJECT (S8); unbound identity = UNRESOLVED (B8) | none |
| 2 | Discover surface members | S2 discovery; B5 discovery graph | none | unchecked member = UR trigger (S4) | none |
| 3 | Fetch, with a per-fetch receipt | S2 metadata list; S4 mandatory receipts; B5 SourceCheck | raw bytes, no class yet | any S4 demotion trigger: UR; challenge or CAPTCHA: blocked, never empty | none |
| 4 | Exhaustion proof | S4 per-source predicates (EDGAR, Greenhouse, Lever, CDX); B5 EnumerationProof | completeness witness | PARTIAL or INVALID (S4) | none |
| 5 | Parse and validate | B5 parser/schema validation; S5 B7.4 raw labels; B1 field states (`part1-b1.md` section 18) | field states UNAVAILABLE / NOT_ACQUIRED / MALFORMED / CONFLICTED | malformed: field state, never zero | none |
| 6 | Write admission | B6 constructors; S6 STRICT, FK, integrity gates | admitted record | constructor refuses; integrity failure halts | none for evidence; the dashboard schema enforces the S6 profile for ledger rows |
| 7 | Identity | B8 snapshot materialization | registry snapshot pin | AMBIGUOUS outcomes, never a silent pick | none |
| 8 | Posting population | B7 POSTING-POPULATION (identity hierarchy, five counting cases) | ADMITTED / ABSTAINED / CONFLICTED / UNKNOWN | ABSTAINED | none |
| 9 | Temporal assertions | B4 (first/last observed as AO point times; captures do not bound continuity) | AO / PD point times | UNKNOWN bounds kept | dashboard `core_instant` / `core_interval` encode bounds |
| 10 | Evidence-class admission | RECON-ECLASS | PD / AO / DD / QN / UR (+WEAK) | UR | contract UNADMITTED, so everything is UR (FV2:417) |
| 11 | Query | B1 QueryDefinition (pending) | n/a | REJECT on missing pin or ambient state (S8) | none |
| 12 | Operators | B9 (pending); B2/B3 for composition and comparison; S4/B6 QN | VALUE / ABSTENTION / UNKNOWN / REJECT | per operator | none |
| 13 | Closure | B10 (OPEN) | BUILDING → SEALED → VERIFIED / INVALID | INVALID | none |
| 14 | Presentation | B12 (retained); S7 wording ("no counterevidence admitted under these pins") | World(p) | omission of counterevidence = INVALID (S7) | none |
| 15 | Dashboard ingest | data theory 1, 6, 8 (not frozen); proposed schema | ledger plane only | receipts refuse | proposed DDL, executed in scratch |
| 16 | Render | dashboard spec; S6 UNKNOWN channel; S8 no-string rule | as carried | honest-state map 3.3 | no UI (by design) |

**DP-1 (BLOCKING).** Steps 1 to 14 have no DDL, no code, and no acquisition run. The proposed schema covers only step 15 for the operator's ledger.
- It has no table for postings, observations, fetch receipts, SourceChecks, EnumerationProofs, registry snapshots, PublisherIdentityBindings, query definitions, or closure packages.
- `core_company` stores a key but no binding evidence (B8 requires it, S5 B8.3).

Confidence HIGH (`schema/migrations/0003_core.sql` is the full core).

### 3.2 Schema trace: each table and view to its authority

| Object | Authority | Frozen? |
|---|---|---|
| file pragmas, `meta_migration`, integrity gates | S6 (B11 retained) | retained |
| `meta_cut` | S8 Ke/Kk cuts; S3 cuts | S8 digest (B1/B9 pending) |
| `core_instant`, `core_interval`, `v_interval_membership` | B4 (summarized; U-DASH-03/04) | FROZEN, derived |
| `core_company`, `core_name_variant` | S5/B8 key rules; no binding table | FROZEN in part; binding missing |
| `core_filing`, `core_artifact` | S2 EDGAR; data theory 6 | retained / not frozen |
| `core_claim`, `core_verdict`, `core_audit_*` | harness spec 13 taxonomy; data theory 2 | NOT frozen (IC-17) |
| `core_claim_eclass` | FV2 RECON-ECLASS | UNADMITTED |
| `core_blocker*`, `core_application*`, `core_action_item*`, `core_note`, `core_research_surface` | dashboard spec only | NOT frozen; operator records |
| `core_expectation*`, `v_expectation_loudest` | harness spec 7 Expectation (not frozen); S4 QN as limit | NOT frozen |
| `meta_receipt`, promotion tables, `stg_*` | data theory 1, 6, 8 | NOT frozen |
| `feed_item` | data theory 3 | NOT frozen; IC-05 |
| `fts_feed` | S6 FTS5 boundary | retained |

### 3.3 Honest-state render map (what the UI shows today, by rule)

The rule: an element renders only the state its machinery can produce.

| Element | Today's honest state | Source of the state |
|---|---|---|
| Blockers strip, applications, notes | operator records, rendered as recorded, labeled OPERATOR RECORD | ledger plane |
| Audit verdict pills | verdict axis labeled "audit verdict (operator taxonomy)" + evidence-class axis `ABSTENTION(CLASSIFIER_NOT_ADMITTED)` | `v_claim_effective` (executed) |
| Claims without an artifact | `UNRESOLVED`, basis `NO_ARTIFACT` | trigger + view (executed) |
| Momentum, churn, role, geography, coverage, field-completeness, workforce panels | `NOT_EVALUATED: no acquisition run` (harness spec 7 acquisition-state term). If a run existed: `UR(EVIDENCE_CLASS_CONTRACT_UNADMITTED)` until R-ECLASS. Composition beyond raw labels: `ABSTENTION(CLASSIFIER_NOT_ADMITTED)` until a classifier C exists (IC-02). Any VALUE: none until B1/B9 admitted and B10 seals. | sections 1 and 3.1 |
| Any QN wording | not rendered; QN UNKNOWN for every scope (ledger:153) | S4 |
| Interval states at a cut | TRUE / FALSE / UNKNOWN with reason; UNKNOWN band kept | `v_interval_membership` (executed) |

---

## 4. Pivots

Each lists: change, replaces, mechanism, migration, what breaks if wrong, what it unlocks. None touches B2, B3, B4, B7, or B8.

### P1. Two planes: an operator Ledger plane and a v1 Evidence plane (recommended, highest value)

- **Change:**
  - Split the dashboard into a Ledger plane (applications, blockers, notes, audit verdicts, action items: the operator's own records) and an Evidence plane (PublicRecruitingState results only, entering only as B10-sealed packages).
  - Every rendered element carries its plane.
  - Audit verdicts stay in the Ledger plane, labeled as an operator taxonomy (IC-17).
- **Replaces:** the single "intel feed" that mixes operator records, external audit verdicts (Gemini corroboration, LinkedIn, RuntimeWire: feed spec :55, :58, :89), and v1 claims under one pill grammar.
- **Mechanism:**
  - Ledger plane rows need only S6 and B4 (both available).
  - Evidence plane rows need the whole chain (section 3.1).
  - The planes share the file and the receipt ledger. No ledger row ever feeds an evidence-plane computation (S8: no ambient state; harness spec 10 invariant 3 non-circularity).
- **Migration:**
  - The proposed schema is already the Ledger plane: rename nothing.
  - Add a `plane` attribute only where an element could be ambiguous (notes).
  - The Evidence plane gets its own migrations when B10 defines the package.
- **What breaks if wrong:** if the operator wants audit verdicts to count as v1 evidence, P1 demotes them. Undoing it means a contract for audit findings as evidence. None exists.
- **Unlocks:**
  - The Ledger plane depends on no pending research blocker. The operator could authorize a Ledger-plane build without waiting for B1/B9/B10.
  - That authorization remains the operator's; this report authorizes nothing.
- **Confidence:** HIGH that the two kinds of content have different authorities (section 3.2).

### P2. Split "classification" into its two real contracts; rule on RECON-ECLASS (recommended)

- **Change:**
  - (i) The evidence-class admission contract RECON-ECLASS governs PD/AO/DD/QN/UR labels.
  - (ii) A composition classifier C (S5 B7.5; pin vector C axis) governs inferred categories such as role family and seniority.
  - B9's CLASSIFY depends on (ii). Its admission must also depend on (i) only through evidence-class propagation.
- **Replaces:** master:42 and `part2-b9.md:243-245` wording, which ties CLASSIFY to (i).
- **Mechanism:** texts in IC-02. Under the current wording, admitting RECON-ECLASS would "unblock" CLASSIFY with no classifier existing. That is a path to typed labels without a mapping, which B7.5 and FV2:173 forbid ("a model proposal or typed label without the governing semantic/adjudication prerequisites").
- **Migration:**
  - Record as a finding for the fresh B1/B9 admission (step 6). The checker may REJECT on R09/R12; then one bounded rework (master:161).
  - No frozen contract changes: B7 already distinguishes classifier admission states.
- **What breaks if wrong:** if the program intended RECON-ECLASS to be the classifier contract, then a classifier mapping must be added to it. Same work, different home.
- **Unlocks:** honest dependency labels. Role and seniority views depend on authoring classifier C, a research item no one has scheduled. The evidence-class question becomes a single ruling.
- **Erratum to my hopes map:** rows V-role and U2 named "RECON-ECLASS admission" as the dependency. That is insufficient: classifier C is also required.

### P3. Keep PublicRecruitingState; make O an annotation and D a separate stream (recommended, presentation level)

Does PRS(C,T,S) = <I, Co, L, D, O> hang together end to end? Partly.

- I, Co, and L share one acquisition path (steps 1 to 9) and one population (B7).
- **D** comes from a different source family. Registrant documents have no acquisition contract for content (IC-07) and different time semantics: filing date vs acceptance time (S3, Filer Manual note).
- **O** is defined by S1 as "a property of the evidence, not the company" (master:27). It describes the other four; it is not a peer.

The change:
- Render PRS as `<I, Co, L>`, each value carrying a mandatory O annotation (its SourceChecks, exhaustion, limitations, the B12 "limitations" slot).
- Render D as a separate disclosure stream with its own coverage annotation.
- No S1 proposition changes. R-O questions stay valid, because they ask about coverage per query, which an annotation answers.

Details:
- **Replaces:** a five-panel layout where coverage could be read as a company attribute (the "dark on Wayback" error, hopes map V-cov).
- **Migration:** presentation and assembly crosswalk only. The S1 claim text is not edited.
- **What breaks if wrong:** if a reviewer reads S1's tuple as requiring O-as-dimension queries (e.g., "rank companies by coverage"), P3 makes those awkward, which is the point (S9 ranking fence).
- **Unlocks:** every number on screen is accompanied by its coverage, by construction. The honest-state requirement then holds for free.
- **Confidence:** MEDIUM-HIGH. It is a semantics-preserving restructure, but S1's original record is unrecovered (U-1R-AUTH-003).

### P4. "Openable query" means the QueryDefinition, not SQL (recommended)

- **Change:**
  - Evidence plane: a panel opens its B1 QueryDefinition (canonical JSON, hash), the compiler identity, the compiled SQL as a labeled compilation target, and the B10 package ID.
  - Ledger plane: panels may open SQL, because they are not analytic results.
- **Replaces:** data theory :122 "panels trace to a SQL string" for analytic panels.
- **Mechanism:** S8:67-71 forbids SQL as the semantic interface; B1 sections 14 to 16 define the query identity and AST-to-SQL goldens (`part1-b1.md`).
- **Migration:** a spec edit to data theory 9; no schema change.
- **What breaks if wrong:** nothing structural; at worst an extra click.
- **Unlocks:** keeps the redash accountability pattern without violating S8.

### P5. v1.0 source order: begin with surfaces that have exhaustion predicates (proposal)

- **Change:**
  - First acquisition runs target Greenhouse and Lever board APIs, EDGAR filing enumeration (metadata), and CDX capture enumeration.
  - Defer generic careers HTML (H) and visitor resources (R) until per-surface terminal contracts exist.
- **Replaces:** treating all of H∪D∪R plus CDX as one v1 acquisition front.
- **Mechanism:**
  - S4 gives explicit exhaustion predicates for exactly these four (S4 "Exhaustion predicates" section).
  - S4:31 leaves generic H/R surfaces PARTIAL.
  - The S2 boundary is unchanged; this is ordering within it, not narrowing it.
- **Grounded consequence for the operator's own targets** (feed spec :63-81):
  - Palantir is on Lever (:65) and Cloudflare is on Greenhouse 8199958 (:69): covered.
  - Superhuman is on Ashby (:67): no S4 predicate exists for Ashby, so it stays PARTIAL.
  - Duolingo, IBM, Datadog, NVIDIA: platform not established in the pack. UNKNOWN; I do not infer them.
- **Migration:** none; it is a sequencing decision for the first experiment (P7).
- **What breaks if wrong:** targets on other platforms get only PARTIAL coverage longer.
- **Unlocks:** the first runs that can ever produce QN and complete inventories.
- **Confidence:** HIGH on the predicate inventory; LOW on how many target companies use Greenhouse or Lever.

### P6. Pre-ruled fallback for remediation step 7 (requires an operator ruling)

- **Change:** if exact reuse of the retained extraction reports is impossible (step 7 fires), run a fresh B1/B9 repair session from Foundation v2, with new bytes, delivered in-task (the B2/B3 pattern, ledger:210). Then a fresh admission.
- **Replaces:** the open-ended "Stop" (master:146).
- **Mechanism:**
  - The voided item was the admission, not the repair (master:129-132).
  - The anti-slop rule limits reissues per defect (master:161); a fresh repair after unrecoverable evidence is a new contribution, not a reissue of a rejected one.
- **Migration:** a ruling text only.
- **What breaks if wrong:** the program loses the exact earlier repair text. The four quarantined files stay preserved as history, not as input.
- **Unlocks:** v1 cannot be stranded by a lost browser task.
- **Confidence:** HIGH that the gap exists; the fallback's legitimacy is the operator's call.

### P7. Declare the first acquisition run and the B10 replay as research experiments (requires an operator ruling)

- **Change:** authorize, as research experiments under FV2:816, a bounded, receipted, non-production run whose only purpose is:
  - (a) B5/B6 runtime evidence; and
  - (b) executed B10 verification receipts (dependency-world hash, computation receipt, replay output; ledger:259).
- **Replaces:** the implicit circularity (IC-13): B10 needs executed receipts, executed receipts need code, code needs a build, build is NONE.
- **Mechanism:** FV2:816 explicitly allows "explicitly identified research experiments" within stated evidentiary limits. U-1R-AUTH-012 to 015 closure conditions already name "rerun an explicitly RECONSTRUCTED experiment with receipted inputs/procedure/output" (FV2:576, :590, :604, :618).
- **Migration:** a ruling text plus an experiment charter (scope, sources per P5, retention, no production use).
- **What breaks if wrong:** if the operator views any executed code as "build", P7 is refused and B10 stays OPEN indefinitely.
- **Unlocks:** the only path I can find by which B5, B6, and B10 ever leave paper.
- **Confidence:** HIGH that the circularity exists without P7.

### P8. One outcome crosswalk at corrected assembly (recommended)

- **Change:** a single table mapping every contract's native states to one display lattice (VALUE, ABSTENTION, UNKNOWN, UR, REJECT, plus lifecycle states). Elements always render their native state plus the lattice class.
- **Replaces:** six vocabularies with no crosswalk (IC-04, IC-16).
- **Mechanism:** FV2:92 already requires "glossary/crosswalk ... outcome vocabulary" in the corrected baseline.
- **Migration:** assembly artifact; no contract edit.
- **What breaks if wrong:** a lossy mapping. Mitigation: always render the native state too.
- **Unlocks:** one honest-state UI grammar.

### Pivots considered and rejected

- **Switch to Go:** rejected. No new evidence beyond the shootout; Go's velocity case is unchanged and the B4 argument narrowed for Rust and Go alike (proposal (a)).
- **TS/Python rewrite:** not rejected, not proposed. It turns on the stack ruling (5f); the evidence does not decide it.
- **Unfreeze B4 to add approximate times:** rejected. DAY plus verbatim text satisfies S3:5 without touching B4.
- **Postgres instead of SQLite:** rejected. S6 freezes SQLite; local-first single file is a constraint.
- **LLM classifier to unblock composition:** rejected. B7.5 forbids it; FV2:173 forbids typed labels without prerequisites.
- **Merge staging into core:** rejected. Loses the receipted promotion boundary.
- **Drop the receipt hash chain:** left to ruling U-DASH-02; no evidence decides it.
- **Drop Wayback from v1:** rejected. CDX has an S4 exhaustion predicate; it stays as AO capture metadata.
- **Scores for connection strength:** rejected (kill 1).
- **Graph database:** rejected (harness spec 6 "No graph database").

---

## 5. Cut and park list (ruling recommendations)

| # | Item | Where | Recommendation | Why |
|---|---|---|---|---|
| X1 | Tier 4 exposure verification | harness spec v1.2:155; feed spec :100, :127 | CUT from the dashboard catalog and from v1; PARK the methodology chat as a record | Serves no listed hope; highest legal and ethical exposure in the pack |
| X2 | Donation and award timing analysis (Phase 4) | harness spec v1.2:239-255 | PARK to platform (money graph D8) | Boston procurement legacy; no v1 consumer |
| X3 | Money-graph traversal paths | harness spec v1.2:221-225 | PARK with D8 | Serves only the dream |
| X4 | Procurement B10 fixture `repeated_supplier_cohort.v1` | `RC/PROVISIONAL-b10-acceptance-artifacts.txt:242, :511` | Keep quarantined; never promote; require a hiring-footprint replacement at master 7 step 9 | Out of v1 domain; patterned hashes (:548, :714) |
| X5 | `core_research_surface` table | proposed schema | CUT to a static note | Measures nothing |
| X6 | Superhuman B4 Form D raise-total reconciliation | feed spec :55 | Move to Ledger plane only; mark out of v1 | Money amounts are D8 (dream); v1 D is "recruiting/workforce statements" (S1:37) |
| X7 | Superhuman B1 "logged-in browser pass" | feed spec :58 | Ledger-plane note only; never ingested | S2 excludes authenticated surfaces |
| X8 | Harness assistance inbox and model seats | harness spec v1.2:106 | PARK | No v1 hope needs a model |
| X9 | `expected_probability` | data theory :58 | CUT (replaced by categorical basis, U-DASH-09) | Categorical-only rule |

---

## 6. Grounded corrections package

Full grounding for 6.1 to 6.4, 6.7, and 6.8 is in `pack/phase1/grounding-final-2026-10-02.md` (sections A to F, commit 06049cb). This section restates each item in ruling form and adds what is new.

### 6.1 (a) The 8 Phase 1 corrections

| # | Correction | Grounding | Confidence | New this pass |
|---|---|---|---|---|
| 1 | htmx: pin 2.0.11 as npm `latest`; 4.0.0 exists on `next` (published 2026-08-28) | grounding-final A1 | HIGH | Drive-only `unsilo-session2-prompt-2026-10-02.md` also says "Verified pins (crates.io / npm, 2026-10-02) ... htmx 2.0.11 (version 4.x does not exist)". npm `next` was 4.0.0 since 2026-08-28, so that verification line was wrong when written. |
| 2 | One file, table-name namespaces; two-file design loses triggers, FKs, atomic promotion | A2: executed reproductions; `sqlite3.c:126200-126214`, `:90828-90844` | HIGH | none |
| 3 | Marker enum vs frozen B4: start endpoint unrepresentable; no granularity | A4 | HIGH / MEDIUM | none |
| 4 | `expected_probability` vs categorical-only | A5 | HIGH | none |
| 5 | Replay needs row images | A6 | HIGH | none |
| 6 | B9 repeats the retired S3 rule | A7; IC-15 | MEDIUM | none |
| 7 | 555 vs 355: underspecified, not inconsistent | A8 | MEDIUM | none |
| 8 | Pattern and license confirmations | Phase 1 report section 6 (file:line per pattern; licenses from files); grounding-final D.1 | HIGH | none |

### 6.2 (b) Proposals (a) to (g)

Each is as grounded in grounding-final B. The ruling text is in 6.9.

- **(e):** the record defines no approximate-time rule. The tilde appears only in data rows (feed spec :65, :67, :78).
- **(f):** SQLite 3.45.1 provides no SHA-256 (executed); any UDF used in a trigger needs `SQLITE_INNOCUOUS` under `trusted_schema=OFF` (`sqlite3.h:5939-5948`).

### 6.3 (c) U-DASH-01 to U-DASH-14: ruling text

Tick one option each.

| ID | Rule on this text |
|---|---|
| U-DASH-01 | [ ] Amend data theory 1 (line 6) to "one SQLite file; namespaces meta_, stg_, core_, v_, fts_". [ ] Keep two schemas as two attached files, accepting loss of cross-file triggers, foreign keys, and atomic promotion (grounding-final A2). |
| U-DASH-02 | [ ] Receipts are hash-chained (launch prompt :35). [ ] No chain; content addressing plus git only (harness spec v1.2:87, :107). |
| U-DASH-03 | [ ] Implement cross-granularity lifting per S3:49-50, after the B4 owner confirms the reconstructed clause; until then the view returns UNKNOWN with `GRANULARITY_NOT_LIFTED`. [ ] Keep not-lifted permanently and record it as a conformance gap. |
| U-DASH-04 | [ ] Operator pulls the four passages listed in grounding-final C.2 from chat 6abdfc6f; adopt whichever reading they state. [ ] Adopt the dense reading now, provisionally. |
| U-DASH-05 | [ ] Pill label for stored UNRESOLVED is "UNKNOWN" (feed spec). [ ] Pill label is "UNRESOLVED" (audit record, harness spec v1.2:229). |
| U-DASH-06 | [ ] Strip shows non-terminal states (all except FROZEN, CLOSED). [ ] Strip shows only OPEN and REPAIRED-PENDING-ADMISSION. [ ] Other: ____ |
| U-DASH-07 | [ ] Operator supplies the real Duolingo packet; until then the parser is a stand-in. |
| U-DASH-08 | [ ] Amend data theory 6 (lines 66-68): receipts carry the canonical after-image. [ ] Redefine repair as verify plus re-derive from staging (operator-authored rows then have no repair source). |
| U-DASH-09 | [ ] Replace `expected_probability` (data theory :58) with categorical basis MANDATED / STATED / ROUTINE / OPERATOR. [ ] Exempt expectation ordering from the categorical rule (requires amending README:18 and master:48). |
| U-DASH-10 | [ ] Add REJECTED and WITHDRAWN application statuses. [ ] Keep the spec's three. |
| U-DASH-11 | [ ] "~" times stored as KNOWN at DAY plus verbatim text. [ ] Ask the B4 owner for an approximate-time extension (a B4 change). |
| U-DASH-12 | [ ] `user_version` = 1 is physical generation 1 (S6:6); migrations counted in `meta_migration`. [ ] `user_version` = latest migration number (departs from S6's literal text). |
| U-DASH-13 | [ ] Store audit counts as reported, with keys distinguishing "CONFIRMED load-bearing"; obtain the audit export to account for 200 claims. |
| U-DASH-14 | Same choice as U-DASH-03, applied to write-time validity of mixed-granularity KNOWN-KNOWN intervals. |

### 6.4 (d) U-DASH-03/14 and U-DASH-04

Verbatim frozen-adjacent text (the reconstructed B4 clause itself is not in the repo or Drive):

- `RC/s3-output-2026-09-30.md:49-50`: "Cross-granularity: TRUE only if true under every compatible interpretation; FALSE only if false under all; else UNKNOWN."
- `RC/s10-output-2026-10-01.md:40-42`: "Frozen and must NOT reopen: ... day-granule discipline; sound cross-granularity lifting; correction non-leakage ..."

Divergence (executed; grounding-final C.1):

- `[DAY 2026-09-01 ET, DAY 2026-09-30 ET)` at SECOND `2026-10-15T12:00:00Z` should be FALSE under every interpretation; the schema returns UNKNOWN.
- A valid mixed-granularity interval is refused at write.

U-DASH-04: the four passages to pull, and the four cases where the dense and discrete readings disagree, are in grounding-final C.2.

### 6.5 (e) License posture: both texts verbatim

Pack (read this pass):

- `pack/dashboard-crawl-report.md:323`: "AGPL: patterns only."
- `pack/unsilo-claude-launch-prompt-2026-10-02.md:106-108`: "Prior-art framing: the crawl surveyed open-source dashboards to learn from. Reimplement patterns; do not port code, especially from AGPL sources. Never describe this as stealing."
- `pack/unsilo-claude-launch-prompt-2026-10-02.md:177-178`: "worldmonitor and glance are AGPL-3.0: patterns only, no ported code"
- Also `pack/dashboard-crawl-report.md:24`: "the word 'steal' was scrubbed from this report at the operator's request."

Operator's local record: `steal-lift-list-2026-09-30.md:141-144`. NOT opened by me: it is not in the repo, and a Drive search on 2026-10-02 (`title contains 'steal'`, `fullText contains 'take whatever'`) returned no match. The operator's agent reported it verified. Verbatim text must be pasted by the operator's agent; I will not paraphrase a file I have not read.

Operator's statement in this session (2026-10-02), verbatim: "Lisxence issues are settled. this code will never touch anything public or be distributed"

Ruling text:

- [ ] Private-use posture: any license's code may be used; nothing is distributed or served to others; amend crawl report :323 and launch prompt :106-108, :177-178 accordingly.
- [ ] Keep "patterns only".

Either way the ruling is written into the pack, so one text governs.

### 6.6 (f) Stack: both texts verbatim

`master:177`:

> "9. **Scope discipline.** v1 is the goal, the platform is the dream. Every plan flags scope creep explicitly and feasibility-checks against the real stack (single operator, local-first laptop + VM, SQLite-first, no GPU, TS/Python, deterministic pipelines, private use)."

Rust approval, repo texts: `pack/unsilo-data-theory-2026-10-02.md:94-104` and `pack/language-shootout-2026-10-02.md:232-238` (quoted in full in grounding-final F.2). Drive-only `unsilo-session2-prompt-2026-10-02.md` Layer 4, read 2026-10-02, verbatim:

> "Rust, ranked against the spec (not raw speed). Axum 0.8 + Askama + htmx (vendored, no build step). ... Kill criteria (from the shootout): Rust dies if iteration velocity dominates the build; Go was second (velocity king, but B4 markers live in CHECK constraints, not the compiler); Zig was third (best absolute efficiency, no mature server templating, thinnest training data)."

"Rust pick stands (narrowed)": NOT FOUND in the repo, and not found by a Drive full-text search on 2026-10-02 (`fullText contains 'stands (narrowed)'`). The operator must attach the 2026-10-02 handoff containing it.

Linkage (unchanged from grounding-final F.3): the shootout's deciding argument is the one proposal (a) refutes.

Ruling text:

- [ ] Directive 9's "TS/Python" describes the harness default; the dashboard stack is Rust on the narrowed reasons.
- [ ] Directive 9 binds the dashboard; re-run the stack decision with TS/Python as a candidate.
- [ ] Rust, plus a TS front end (Blueprint), accepting a Node build (6.7).

### 6.7 (g) Charting layer and Blueprint

As grounded in grounding-final D.1 to D.4. Recommendation:

- Server-rendered SVG from Askama templates (zero client bytes, one implementation of the UNKNOWN and B12 rendering rules).
- uPlot 1.6.32 IIFE as the vendored fallback: MIT from its `LICENSE` file; 51,081 bytes min, 22,009 gz; upstream HEAD 2026-09-28.

Blueprint 6.21.0 (2026-09-30, Apache-2.0 from its `LICENSE` file) needs React 18 or 19 and a bundler (no browser bundle shipped). The real cost is a second implementation of render semantics and a Node build, not the binary.

Ruling text:

- [ ] Server SVG plus uPlot fallback.
- [ ] Blueprint and React (amends data theory :94).

### 6.8 (h) Hopes to kill, all three

As grounded in grounding-final E:

1. **Confidence-scored connections:** README:18; master:48; harness spec v1.2:214; S5:39.
2. **Recon on high-power individuals, with email harvesting:** harness spec v1.2:15, :162, :156; `build-blockers-b1-b12-verbatim-2026-09-30.md:115`; S5:33, :39; S2:9.
3. **"Full company DNA":** FV2:754 (R06); S1:33; folklore kills #1, #6, #9.

Ruling text per kill: [ ] Kill. [ ] Keep, with a definition that maps to sources and contracts (the listed dependencies apply).

### 6.9 Proposals (a) to (g): ruling text

| # | Rule on this text |
|---|---|
| (a) | [ ] Adopt: amend data theory :48-52, :102-103, shootout :208, launch prompt :149-150 to "the enum is a second line of defense; unrepresentability comes from a NOT NULL kind column per endpoint and one evaluation view". |
| (b) | [ ] Record as mandated by B4 (master:111; ledger:104). |
| (c) | [ ] Evaluator in the SQL view only. [ ] In Rust only. [ ] Both, with an agreement test over the B4 regression table. |
| (d) | [ ] UNKNOWN band exists; layout ruled in the UI phase. |
| (e) | Same as U-DASH-11. |
| (f) | [ ] No. [ ] Yes, in the Rust writer (re-read, hash, compare, then commit or roll back). [ ] Yes, as a trigger UDF registered DETERMINISTIC + INNOCUOUS on every connection. |
| (g) | [ ] Every panel query states its own ORDER BY. |

### 6.10 New rulings raised by this reconciliation

| ID | Rule on this text |
|---|---|
| R-ECLASS | [ ] FV2:128 governs: RECON-ECLASS was admitted for the reconstructed gate when Foundation v2 was admitted (ledger:71); update master:42, :121. [ ] A separate admission "as invoked authority" is required; record that requirement in an FV2 erratum so the text matches the state. |
| R-P1 to R-P8 | [ ] Adopt. [ ] Reject (parked with rationale), for each of pivots P1 to P8. |
| R-MASTER | [ ] The pack master (37,073 bytes) is authoritative. [ ] The Drive `unsilo-architecture-prompt-2026-10-02.md` (37,084 bytes) is authoritative. Either way, fix the S8 kill count and the A04 omission (IC-11). |
| R-CUTS | [ ] Adopt X1 to X9 as recommended. [ ] Per-item. |
| R-HOPES-ERRATUM | Acknowledge: the hopes map's V-role and U2 dependency is "RECON-ECLASS admission AND an authored classifier C" (IC-02). No label raised. |

### 6.11 (i) Hopes map stays provisional

Every WEAK label stands until all four clear: RECON-ECLASS admitted (now also subject to R-ECLASS); B1/B9 admitted and B10 settled; a first receipted acquisition run; build authorized. Nothing raised. One dependency added (IC-02).

---

## 7. Hand-waving register (what in this report is not fully grounded)

| Item | Why it is not fully grounded | What would ground it |
|---|---|---|
| The reconstructed B4 cross-granularity clause | not in repo or Drive | chats 6abdf9e2 and 6abdfc6f |
| Dense vs discrete completions | ledger summary only | chat 6abdfc6f |
| B9 text (IC-02, IC-03, IC-15, IC-16) | read from quarantined bytes | the retained extraction reports |
| ATS platform of Duolingo, IBM, Datadog, NVIDIA | not in the pack | their careers pages, observed per S2 |
| Legal exposure of person-level data | not researched | counsel |
| replayable ↔ SEALED mapping (IC-09) | my proposal | B10 reassessment |
| The local steal-lift list and the "narrowed" handoff | not opened | operator's agent pastes them |
| SQLite view ORDER BY behavior (g) | sqlite.org blocked by the proxy | sqlite.org `lang_select.html` |

## 8. What "done" looks like after the ruling

If the operator adopts P1, P2, P4, P8, R-ECLASS, the U-DASH rulings, and 6.5 to 6.7:

- A Ledger-plane build can be authorized on its own. Every element traces to the dashboard spec, S6, and B4, and the honest states in 3.3 are enforced.
- The Evidence plane stays visibly `NOT_EVALUATED` until P7's experiment and the master 7 sequence complete.

That split is the whole reconciliation: build what has authority now, and show the rest as honestly empty.

Build authorization: NONE
