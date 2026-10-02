# UnSilo v1: integrated architecture (proposal, 2026-10-02)

Architecture proposal for the operator's single-pass ruling. Nothing implemented. No baseline file changed. The four quarantined B1/B9 files are untouched. Build authorization: NONE.

## 0. Blockers (lead)

| Item | State | What this design does about it |
|---|---|---|
| B2, B3, B4, B7, B8 | FROZEN | built on, not redesigned |
| B1, B9 | REPAIRED-PENDING-ADMISSION | the design runs without them in the operator-ledger plane; the evidence plane renders nothing until they are admitted (section 8) |
| B10 | OPEN, quarantined | sealing is designed as a slot; no VALUE is shown until B10 freezes |
| B5, B6 | RETAINED-INTEGRATION-VERIFIED | Sweep and Cleanroom implement them; first runtime evidence needs ruling D-3 |
| B11, B12 | RETAINED | Strata implements B11; Crosscheck implements B12 |
| RECON-ECLASS | UNADMITTED | every evidence-class slot renders `ABSTENTION(CLASSIFIER_NOT_ADMITTED)` or UR; ruling D-2 |

## 1. The system on one page

### 1.1 Two planes

| Plane | Working label | Holds | Authority it needs | Buildable when |
|---|---|---|---|---|
| Operator plane | **Docket** | applications, blockers and their states, action items, notes, external audit verdicts | the operator's records; B4 for time; B11 for storage | on a build authorization alone; no pending research blocker gates it |
| Evidence plane | Sweep, Cleanroom, Strata, Parallax, Sunroom, Lantern, Crosscheck | PublicRecruitingState results | the whole research chain | in stages, as blockers clear (section 8) |

The two planes share one SQLite file and one receipt ledger. The link between them is one-way: a Docket note may cite an evidence result; an evidence computation never reads Docket. This keeps operator judgment out of evidence lineage.

### 1.2 Data is king: what is authoritative

1. **Raw bytes are the authority.** Every fetched response, rendered DOM, and network capture is stored once as an immutable file named by its SHA-256.
2. **SQLite is an index and a derivation cache.** Every derived row can be rebuilt from the raw objects, the fetch receipts, and pinned code. That rebuild is the replay that S7 defines. Its folklore kill "the database is the backup" forbids the reverse.
3. **Nothing is deleted.** Change is a new row that supersedes an old one; heads are chosen per knowledge cut.
4. **Two clocks, never merged.** Observed time comes from the source (publication, capture, filing). Knowledge time is when UnSilo recorded the fact.
5. **Absence is a row only under an expectation.** It names what should exist and the dataset it was checked in. An exhausted, zero-result check is a qualified non-observation (QN); anything weaker is UR.
6. **Every number on screen is a result with lineage, or an explicit honest state.** A result names its query, its pins, its evidence, and its seal status. An honest state is NOT_EVALUATED, UR, ABSTENTION, or UNKNOWN.

### 1.3 The pipeline

```
Sweep ─► Cleanroom ─► Strata ─► (Query + Operators) ─► Crosscheck seal ─► surfaces
 fetch     admit        store      compute               B10 + B12         Lantern / Parallax /
 receipts  validate     identity   B1 / B9 / B2 / B3                       Sunroom / Docket
 exhaust   quarantine   time B4    QN (S4)
```

### 1.4 Working labels

| Label | Surface or stage | Fit |
|---|---|---|
| **Sweep** | acquisition: fetch, receipts, exhaustion proofs | good |
| **Cleanroom** | admission gate: parse, validate, write admission, quarantine | good |
| **Strata** | evidence store: raw objects, bitemporal layers, identity snapshots | good |
| **Lantern** | coverage and absence: O annotations, expectations, field-completeness grids | good |
| **Parallax** | comparison across cuts, companies, and versions (churn, momentum deltas) | good as an internal label (it was rejected as a product name for being crowded; that does not matter here) |
| **Sunroom** | disclosure stream: what registrants say in public filings | weak: "sunroom" connotes leisure; it fights the "closet" framing it serves. Flagged. |
| **Crosscheck** | evidence render: support, counterevidence, limitations, seal status on every claim | good |
| **Docket** | operator plane | mild collision: "docket" evokes court records, which are a platform-tier source; fine for v1 |

## 2. The v1 shape

The frozen claim is `PublicRecruitingState(C, T, S) = <I, Co, L, D, O>`. Pivot P3 keeps every proposition in it and changes how the parts compose:

- **I, Co, L** share one acquisition path (careers surfaces and archive captures) and one population (B7 postings). They are computed together as `PRS(C, T, S) = <I, Co, L>`.
- **O** is not a peer dimension. It is a property of the evidence (S1), so it is attached to every I, Co, L, and D value as a mandatory annotation: SourceChecks, exhaustion status, limitations. A number without its O annotation does not render.
- **D** comes from a different source family (EDGAR registrant filings) with different time semantics (filing date vs acceptance time) and no content-acquisition contract yet. It runs as a separate stream, Sunroom.

Mapping the operator's uses:

- **Role surfacing and targeting:** I plus Co raw publisher labels, filtered by a declared predicate. The operator declares any ranking criterion.
- **"The closet":**
  - Sunroom: registrant statements, once the disclosure-span contract exists (section 8.4). Today, filing existence only.
  - Lantern: coverage and absence, always labeled as a property of the archive, never of the company.
- **Company profile:** the five dimensions for one company. Nothing else.

## 3. Pipeline stages: contract, evidence, failure

Each stage cites its governing contract once.

| Stage | Does | Governing contract | Evidence out | On failure | Today |
|---|---|---|---|---|---|
| Sweep.declare | names company identity, surfaces, window | S2 boundary `CareerSurface(C,t) = H ∪ D ∪ R`; S8 closed query Ω | a declared scope | missing field: REJECT | nothing built |
| Sweep.fetch | HTTP GET or headless render, one receipt per fetch (URL, params, UA, headers, redirect chain, status, bytes, SHA-256, timing, 429 state, challenge state) | S2 and S4 receipt lists; B5 SourceCheck | raw objects + receipts | any S4 demotion trigger: UR; CAPTCHA or authwall: blocked, never "empty" | nothing built |
| Sweep.exhaust | runs the per-source completeness predicate | S4: EDGAR continuations; Greenhouse `len(jobs) == unique(id) == meta.total`; Lever terminal empty page; CDX resume key | EnumerationProof or PARTIAL | PARTIAL or INVALID; generic careers HTML stays PARTIAL without its own terminal contract | nothing built |
| Cleanroom.parse | extracts fields; never defaults | B5 parser/schema validation; S5 raw publisher labels | field values with states UNAVAILABLE / NOT_ACQUIRED / MALFORMED / CONFLICTED | field state, never 0 or "" | staging shape exists (`stg_*`, proposed) |
| Cleanroom.admit | constructor admission; quarantine on failure | B6 constructors; S6 integrity gates | admitted source records | refused; store halts on integrity failure | ledger plane enforces S6 (executed) |
| Strata.identity | mention to company via registry snapshot | B8 FROZEN: deterministic snapshot materialization, at most one effective membership per mention, contradictory exact bindings → AMBIGUOUS | snapshot pin | AMBIGUOUS, never a silent pick | key column only; no binding table |
| Strata.population | observations to canonical postings | B7 FROZEN: identity hierarchy (req ID → ATS ID → source-native ID → normalized URL → bounded field comparison), five counting cases, ADMITTED / ABSTAINED / CONFLICTED / UNKNOWN | posting population | ABSTAINED | nothing built |
| Strata.time | point times and intervals; knowledge cuts | B4 FROZEN: `KNOWN(v) \| UNBOUNDED \| UNKNOWN`, entailment over admissible completions | bounds + three-valued truth | UNKNOWN band kept | `core_instant`, `core_interval`, `v_interval_membership` (executed) |
| Strata.class | evidence-class admission | RECON-ECLASS (UNADMITTED) | PD / AO / DD / QN / UR (+WEAK) | UR | everything is UR until ruling D-2 |
| Query | closed QueryDefinition, canonical hash | B1 (pending) | query identity | REJECT on missing pin or ambient state | nothing built |
| Operators | inventory, filter, aggregate, temporal, QN, Difference | B9 (pending); composition and comparison per B2/B3 FROZEN; QN per S4 | VALUE / ABSTENTION / UNKNOWN / UR / REJECT | per operator | nothing built |
| Crosscheck.seal | closure package BUILDING → SEALED → VERIFIED | B10 (OPEN) | sealed result | INVALID | slot only |
| Crosscheck.render | World(p) = support + counterevidence + limitations under one pin world | B12 (retained) | rendered claim | omission of counterevidence: INVALID | ledger-plane claims render both axes (executed) |

## 4. The joints between sessions, designed

| Joint | Problem | Design |
|---|---|---|
| J1 fetch → exhaustion (S2 → S4) | a receipt proves a fetch, not completeness | EnumerationProof is its own object referencing the exact receipt set and the predicate version; QN and inventory "complete" read only proofs, never receipts |
| J2 source → identity (S4 → B8) | ATS board tokens and domains look like identity | a company-attributed result requires a PublisherIdentityBinding (evidence: e.g. a first-party page linking the board) in the registry snapshot; without one, results attach to the board, not the company, and render "binding UNRESOLVED" |
| J3 observation → posting (S2 → B7) | locale mirrors, multi-location, revisions inflate counts | counts are taken only over B7 canonical postings, at a declared grain (S6 fanout proof); raw observation counts never render |
| J4 observation → lifecycle (B7 → B4) | first-seen is not published; last-seen is not closed | appearance = first observation (AO or PD point time); disappearance = QN at a later exhausted cut, else UR; the interval between observations is UNKNOWN, never drawn as continuous |
| J5 classes → admission (S1 → RECON-ECLASS) | one unadmitted contract blocks all classes | provenance (which source path) renders as fact; the class slot renders `ABSTENTION(CLASSIFIER_NOT_ADMITTED)`; no "would-be PD" label is ever shown |
| J6 evidence classes vs composition classifier | two different "classifications" | split (pivot P2): evidence classes come from RECON-ECLASS; inferred categories (role family, seniority) come only from a pinned composition classifier C with a published mapping (S5 B7.5). None exists; v1 Co is raw publisher labels only |
| J7 query → operators → comparison (B1 → B9 → B2/B3) | comparison across cuts, companies, or versions | Parallax uses B9 Difference only at equal pins; across pins it shows a B3 decomposition (four fields) or UNKNOWN; never one undifferentiated delta |
| J8 store → seal (B11 → B10) | the closure must pin the storage engine | the closure package pins the SQLite build (3.53.4 via the apsw wheel), the tzdata version, the code commit, and every raw-object hash; replay recomputes from the package alone |
| J9 seal → render (B10 → B12) | render must not mix worlds | Crosscheck renders only from one sealed package; mixed-world comparisons render as labeled comparisons with both pin vectors |
| J10 evidence ↔ operator plane | operator judgment must not leak into evidence | one-way citation (1.1) |
| J11 filings → statements (S2 → D) | EDGAR enumeration yields filing metadata, not statements | today Sunroom renders filing existence as a registrant representation (form type, accession, filing date); statement content waits on a new disclosure-span contract (8.4) |

## 5. Storage

### 5.1 Layout

- One SQLite file: SQLite cannot hold two schemas inside one file; executed, `CREATE TABLE staging.t` fails with `unknown database staging`.
  - Namespaces: `meta_*`, `stg_*`, `core_*` (Docket), `ev_*` (evidence plane), `v_*`, `fts_*`.
- A content-addressed object directory beside it (`objects/ab/cdef...`).
- SQLite 3.53.4 via the apsw wheel, pinned. Not the host's stdlib SQLite: on this machine stdlib links 3.45.1, so the engine would differ between the laptop and the VM, and B10 requires the engine in the closure.

### 5.2 Evidence-plane entities (proposed names; DDL deferred to the build)

| Entity | Contract |
|---|---|
| `ev_object` (sha256, length, media type) | raw-bytes authority |
| `ev_fetch_receipt` | S2/S4 receipt fields |
| `ev_source_check`, `ev_enumeration_proof` | B5 |
| `ev_source_record` + per-field state | B5; B1 field states |
| `ev_mention`, `ev_membership_decision`, `ev_registry_snapshot`, `ev_publisher_binding` | B8 |
| `ev_posting_observation`, `ev_canonical_posting` | B7 |
| intervals and instants | shared with Docket (`core_instant`, `core_interval`) |
| `ev_query_definition`, `ev_result`, `ev_closure_package` | B1, B9, B10 |
| `ev_expectation`, `ev_qn_witness` | S4 QN |

### 5.3 Deltas to the proposed Docket schema (proposed, not applied)

| Delta | Why | Evidence |
|---|---|---|
| DL-1: allow `zone = 'FLOATING'` for DAY values with no zone context; absolute comparisons with a floating date return UNKNOWN | S3: "Local civil time without zone context → absolute comparison UNKNOWN"; publisher dates often carry no zone; the schema today forces a zone, which would be invented | S3 freeze, read 2026-10-02 |
| DL-2: cross-granularity lifting moves from the SQL view into the application evaluator, using pinned tzdata; the SQL view keeps same-granularity cases; an agreement test covers both | lifting needs a tz database; SQLite has none that is deterministic | executed: tzdata 2026.4 lifts `2026-09-30` America/New_York to `[2026-09-30T04:00Z, 2026-10-01T04:00Z)`, `2026-03-08` to a 23-hour range, `2026-11-01` to a 25-hour range |
| DL-3: receipt after-hash verified in-transaction by a trigger calling a SHA-256 function registered DETERMINISTIC + INNOCUOUS | proposal (f), now feasible | executed: stdlib `sqlite3` UDF in a trigger under `trusted_schema=OFF` fails `unsafe use of sha256hex()`; apsw 3.53.4.0 with `flags=SQLITE_INNOCUOUS` succeeds |
| DL-4: drop `core_research_surface` | measures nothing | none needed |
| DL-5: stored verdict status is shown verbatim (UNRESOLVED) | "UNKNOWN" is already a B4 truth value and a B9 result state; a third meaning on one screen would collide | vocabulary collision, by inspection |

### 5.4 Granule semantics (DL-1 and DL-2 depend on this)

- **Interval endpoints at DAY granularity are calendar-day boundaries.** S3 freezes "exclusive boundary = successor day in same calendar semantics", so `[2026-09-01, 2026-09-30)` at DAY covers whole days, and lifting is exact.
- **Point times at DAY granularity are imprecise instants** inside the day (e.g. "submitted 2026-09-29"). Every compatible interpretation is any second in that day.

Confidence MEDIUM: the frozen B4 text, which is not in the repo, should confirm both readings. See decision D-7.

## 6. Surfaces and what each renders today

| Surface | Element | Renders today | Becomes real when |
|---|---|---|---|
| Docket | blockers strip (top and bottom), applications, action items, notes | operator records as recorded, each labeled OPERATOR RECORD; interval states TRUE / FALSE / UNKNOWN with reason | build authorization |
| Docket | audit verdict pills | verdict axis labeled "audit verdict (operator taxonomy)" + evidence-class axis `ABSTENTION(CLASSIFIER_NOT_ADMITTED)`; claims without an artifact show UNRESOLVED (trigger-enforced, executed) | already enforced in the proposed schema |
| Lantern | coverage map, field-completeness grid, expectations | `NOT_EVALUATED: no acquisition run` | first Sweep run (D-3), then UR until D-2 |
| Parallax | momentum points, churn per cut pair | `NOT_EVALUATED` | Sweep runs at two or more cuts + B1/B9 + B10 |
| Strata | role labels as published, locations as published | `NOT_EVALUATED`; inferred role family or seniority: `ABSTENTION` until a classifier C exists | Sweep + B1/B9 + B10; classifier is v1.1 |
| Sunroom | filing existence | `NOT_EVALUATED` | first EDGAR enumeration run |
| Sunroom | statement content | `UR(NO_DISCLOSURE_CONTRACT)` | disclosure-span contract (8.4) |
| Crosscheck | claim panel | Docket claims: both axes; evidence results: none | B10 + B12 |

Rendering rules:
- A panel opens its query. Docket panels open SQL; evidence panels open the B1 QueryDefinition, the compiled SQL marked as a compilation target, and the closure package ID. S8 forbids raw SQL as an analytic result.
- Charts are server-rendered SVG.
- UNKNOWN is a visible band, never a hidden row.

## 7. Stack: verified by reproduction

The question is directive 9 ("TS/Python") vs the Rust approval. I ran the deciding mechanisms instead of re-reading documents. Python 3.11.15 is in the container; package versions are from PyPI and crates.io (fetched 2026-10-02).

| Requirement (contract) | Python | Rust | TypeScript |
|---|---|---|---|
| Pinned SQLite engine in the closure (S7, B10) | **verified**: apsw 3.53.4.0 (wheel 2026-07-26) bundles SQLite 3.53.4 with FTS5; stdlib `sqlite3` links the host library (3.45.1 here), so stdlib is not pinnable | verified: rusqlite `bundled` ships 3.53.4 (`sqlite3.c:470`) | not checked |
| Hash functions callable from triggers under `trusted_schema=OFF` (S6 + proposal f) | **verified**: apsw `SQLITE_INNOCUOUS` UDF works in a trigger; stdlib fails `unsafe use of sha256hex()` | `FunctionFlags::SQLITE_INNOCUOUS` exists (`rusqlite src/functions.rs:431`); not executed | not checked |
| JS-rendered careers pages (S2: rendering is admissible observation) | **verified**: Playwright 1.63.0 (2026-09-15) drove Chromium 141; the rendered DOM contained the JS-built list and the raw bytes did not; `new_context` has `record_har_path` and `record_har_content` for network capture | no official Playwright: `playwright` crate 0.0.20, last 2022-08-20; `chromiumoxide` 0.9.1 (2026-02-25) is CDP-only, no built-in HAR (network capture is yours to build) | official Playwright |
| B8 canonical JSON: keys in bytewise UTF-8 order (frozen) | **verified**: default `sorted` order equals UTF-8 byte order (`'a' < U+FF61 < U+1F600`) | `String` ordering is byte order (by language definition; not executed) | **verified wrong by default**: `Array.prototype.sort` gave `a, U+1F600, U+FF61` (UTF-16 code units); needs a custom comparator everywhere |
| No ambient nondeterminism (S8) | **hazard verified**: set iteration changed between `PYTHONHASHSEED=1` and `=2`; `json.dumps` leaks floats (`0.30000000000000004`). Fix: one canonical encoder that sorts, rejects float, NFC-normalizes; lint against iterating sets | `HashMap` is also randomized; same discipline | same |
| Server-rendered HTML, no JS build | Jinja2 3.1.6 + Starlette 1.7.0 (2026-09-23) + vendored htmx 2.0.11 | Axum 0.8.9 + Askama 0.16.1 | needs a build for TS |
| Day-to-UTC lifting with a pinned tz database (DL-2) | **verified**: `zoneinfo` + `tzdata` 2026.4 package, host tz path disabled | `chrono-tz` (not checked) | not checked |
| Single static binary | no (lockfile + venv) | yes | no |
| Compile-time B4 markers | no, but proposal (a) shows the enum was never the guarantee: the NOT NULL kind column and one evaluator are | yes, as a second line | partial |
| Operator's stated stack (directive 9) | yes | no | yes |

**Diagnosis.** The acquisition layer decides the stack:
- S2 makes JS-rendered careers pages admissible evidence, and capturing them needs a real browser with network capture.
- Official Playwright exists for Python and TypeScript, not Rust.
- So a Rust dashboard implies a second language for acquisition anyway. Two languages would mean two implementations of the canonical encoder, and the B8 snapshot hash has to be byte-identical across them.
- TypeScript's default ordering breaks the frozen B8 rule, and it brings a build step.
- Python satisfies every row with one language, matches directive 9, and pins the engine through apsw.

**Recommendation:** a single Python stack.

| Layer | Components |
|---|---|
| Acquisition | Playwright (with HAR capture) for rendered surfaces; an HTTP client with full receipts for APIs |
| Storage | apsw + pinned SQLite 3.53.4; tzdata pinned |
| Web | Starlette + Jinja2 + vendored htmx 2.0.11 |
| Charts | server SVG |
| Lockfile | everything pinned, including Chromium (pin a Playwright version whose browser build is installed; the mismatch reproduced here: Playwright 1.63.0 wanted build 1243, the container has 1194) |

Confidence: HIGH on each verified row; MEDIUM on the overall call.

What would change my mind: a requirement for a single static binary, or a measured performance need, neither of which exists for one operator. The HTTP client is not pinned here: httpx's last release is 2024-12-06; choosing between it and the stdlib is a build-time detail.

## 8. Unblock paths

### 8.1 B1, B9

- Master doc section 7 steps 1 to 6 as written.
- Two findings travel to the fresh admission:
  - B9 ties CLASSIFY to the evidence-class contract (joint J6).
  - B9's temporal operator text restates the retired S3 blanket rule ("unknown bounds produce UNKNOWN").
- The checker decides; a rejection gets one bounded rework.
- If step 7 fires (exact reuse impossible), see decision D-4.

### 8.2 B10

- After a valid B1/B9 ACCEPT.
- Its acceptance needs executed verification receipts, which need running code. Build authorization is NONE. Foundation v2 permits "explicitly identified research experiments" for semantic acceptance. See decision D-3.
- The quarantined procurement fixture is replaced by a hiring-footprint fixture from that experiment.

### 8.3 B5, B6

Runtime evidence comes from the same experiment (D-3). Sources that have S4 exhaustion predicates go first: Greenhouse, Lever, EDGAR, CDX.
- Among the operator's targets, Palantir (Lever) and Cloudflare (Greenhouse) qualify.
- Superhuman (Ashby) has no predicate.
- The others' platforms are not established. I do not guess them.

### 8.4 New research items (no frozen contract covers them)

| Item | Needed for | Status |
|---|---|---|
| Disclosure-span contract: acquiring filing documents and extracting a statement as (accession, document, byte range, text hash, filing acceptance time) | Sunroom statement content; the closet | not started; research (meaning of a "statement span") |
| Composition classifier C with a published mapping | role family, seniority | not started; v1.1 |
| Terminal contracts for specific careers HTML surfaces | completeness on non-ATS careers pages | per surface, as needed |
| Ashby source contract | Superhuman | not started |

## 9. Decisions

The decisions fall into two groups:

- **9.1, resolved by verification:** I settled these with reproductions or mechanisms. Recommendation: ratify them as a block. Object to any line and it reopens.
- **9.2, your calls:** they need your authority or your values.

### 9.1 Resolved by verification (ratify as a block)

| # | Decision | Resolution | Evidence |
|---|---|---|---|
| R1 | htmx pin | 2.0.11, because it is npm `latest`; 4.0.0 exists on `next` (published 2026-08-28) | npm dist-tags |
| R2 | One file vs two schemas | one file, table-name namespaces | executed: `unknown database staging`; triggers cannot reference another attached database; cross-database FKs fail to parse; WAL files never join SQLite's super-journal (`sqlite3.c:90828-90844`) |
| R3 | Contaminated B1/B9 mirror | stays quarantined; step 6 uses the retained reports only | SHA-256 `be9155fc...b660f` matches the known-contaminated copy |
| R4 | Interval markers | per-endpoint `KNOWN(value, gran, zone) \| UNBOUNDED \| UNKNOWN`, zone allowing FLOATING (DL-1) | B4 domain; S3 granularity |
| R5 | `expected_probability` | replaced by categorical basis MANDATED / STATED / ROUTINE / OPERATOR | categorical-only rule; a probability column is probability-style by definition |
| R6 | Replay | receipts carry the canonical after-image | SHA-256 is one-way; a hash cannot be replayed |
| R7 | B9 restating the S3 rule | route to the fresh B1/B9 admission as a finding | not the dashboard's to repair |
| R8 | Audit counts 555 vs 355 | store counts as reported; "188 CONFIRMED load-bearing" is a subset; ask for the export | arithmetic |
| R9 | Prior-art patterns and licenses | confirmed at file:line; licenses read from files | Phase 1 report section 6 |
| R10 | (a) enum | adopt: the enum is a second line of defense; the guarantee is the NOT NULL kind column plus one evaluator | executed regression (nullable `valid_to` reads an UNKNOWN end as open) |
| R11 | (b) per-endpoint tri-state | mandated by B4 | B4 domain |
| R12 | (c) evaluator location | SQL view for same-granularity cases; application evaluator for lifting; one agreement test over the regression table | DL-2 |
| R13 | (d) UNKNOWN band | yes; layout in the UI phase | S6 explicit UNKNOWN channel |
| R14 | (e) approximate times ("~9:31 PM") | KNOWN at DAY + verbatim source text | S3: date-only is a calendar-day granule; "~" asserts no minute |
| R15 | (f) after-hash check | yes, as a trigger with an INNOCUOUS SHA-256 function (DL-3) | executed under apsw |
| R16 | (g) ordering | every panel query states its own ORDER BY | S8 bans retrieval order as ambient state |
| R17 | U-DASH-01 | = R2 | |
| R18 | U-DASH-02 receipt chain | keep the chain | costs one column; detects truncation and reordering, which content addressing alone does not |
| R19 | U-DASH-03 / 14 cross-granularity | lift per S3 with pinned tzdata (DL-2); accept mixed-granularity KNOWN intervals once lifting exists | executed DST cases |
| R20 | U-DASH-05 pill label | show UNRESOLVED verbatim | DL-5 collision |
| R21 | U-DASH-06 strip membership | non-terminal states: everything except FROZEN and CLOSED | strip purpose: what still blocks |
| R22 | U-DASH-08 | = R6 | |
| R23 | U-DASH-09 | = R5 | |
| R24 | U-DASH-10 application statuses | add REJECTED and WITHDRAWN | otherwise an open, rejected, reopened history is unrepresentable |
| R25 | U-DASH-11 | = R14 | |
| R26 | U-DASH-12 `user_version` | 1 = physical generation; migrations counted in `meta_migration` | S6 |
| R27 | U-DASH-13 | = R8 | |
| R28 | Charting | server-rendered SVG; uPlot 1.6.32 (MIT, 22,009 bytes gz) as a vendored fallback | grounding-final D |
| R29 | Blueprint | no | React 18 or 19 + bundler (no browser bundle shipped); a Node build on top of a Python stack; a second implementation of render semantics |
| R30 | License posture | your 2026-10-02 statement governs ("this code will never touch anything public or be distributed"); the pack's "patterns only" lines get amended to match | your statement; ratify the text edit |

### 9.2 Your calls

| # | Decision | Options and tradeoffs | My recommendation |
|---|---|---|---|
| D-1 | Stack | (i) Python only, as verified in section 7: one language, official Playwright, pinned SQLite, matches directive 9; cost: no single binary, discipline needed against hash-seed and float leaks. (ii) Rust dashboard + Python acquisition: two canonical encoders that must agree byte for byte. (iii) Rust only: build your own network capture on CDP. | (i). Supersedes the Rust approval. |
| D-2 | RECON-ECLASS | (i) Foundation v2's text governs: its admission already admitted the contract for the reconstructed gate; every class becomes assignable. (ii) A separate admission is required: record why in a Foundation v2 erratum and schedule it next in the chain. | (ii). It is the conservative reading, and one admission session costs little. The current state is defended by no written rule, which is worse than either option. |
| D-3 | Research-experiment charter: one bounded, receipted acquisition run (Lever and Greenhouse boards for two of your targets, one EDGAR enumeration, one CDX query), retained as evidence, no production use | Yes: B5/B6 get runtime evidence and B10 gets real receipts. No: B10 can never freeze. | Yes. You supply the board identifiers; I will not guess them (S2 forbids guessed endpoints). |
| D-4 | If remediation step 7 fires | (i) commission a fresh B1/B9 repair from Foundation v2; (ii) stop indefinitely | (i). The admission was voided, not the repair. |
| D-5 | Adopt the two-plane split (P1) | Yes: Docket can be built now. No: everything waits on the chain. | Yes |
| D-6 | Adopt the v1 shape restructure (P3) | Yes: O becomes an annotation and D a separate stream; no S1 proposition changes. No: five peer panels. | Yes |
| D-7 | Granule semantics (5.4) | Confirm "DAY intervals = whole days; DAY points = imprecise instants", or pull the frozen B4 text (chat 6abdfc6f) and adopt what it says; the same pull settles dense vs discrete completions | Pull the text; until then use 5.4 and label it provisional |
| D-8 | The three kills | confidence-scored connections; recon on individuals (with email harvesting); "full company DNA" | Kill all three: they conflict with the categorical rule, with company-only identity (B8), and with the requirement that semantics be specified |
| D-9 | Supply the real Duolingo packet | needed for the real staging parser | supply it |

## 10. Pivots

Pivots that remove machinery come first.

| # | Pivot | Changes | Migration | Breaks if wrong | Unlocks |
|---|---|---|---|---|---|
| P9 | One language: Python | drops the Rust toolchain, musl, and the Askama/Axum stack; drops any second canonical encoder | rewrite nothing (no code exists); move the proposed SQL as is | if a static binary becomes mandatory, packaging gets harder | one canonical encoder for B8 and B10 hashes; official Playwright; pinned SQLite |
| P1 | Two planes (Docket / evidence) | splits the "intel feed" into operator records and evidence results | label existing tables as Docket; evidence tables are new | if audit verdicts were meant to count as v1 evidence, they get demoted | a Docket build gated by no research blocker |
| P3 | Shape: `<I, Co, L>` with an O annotation + D stream | removes the "observability panel" and "disclosure as a posting dimension" | presentation and crosswalk only | a reader may want O-as-dimension queries (S9's ranking fence disallows the bad ones anyway) | coverage on every number by construction |
| P10 | Raw objects are the authority; SQLite is rebuildable | no backup-as-truth; derived tables are disposable | object store beside the file | disk use for raw captures (no number measured; likely modest for one operator) | replay is the rebuild path; B10 gets a real mechanism |
| P2 | Split classification (J6) | B9's CLASSIFY depends on a composition classifier, not RECON-ECLASS | admission finding (8.1) | none if B7.5 is read as frozen | honest dependencies for the targeting views |
| P4 | Openable query = QueryDefinition for evidence panels | the SQL-string pattern stays for Docket only | spec edit | none | S8 compliance with the redash accountability kept |
| P5 | Sources with exhaustion predicates first | ordering inside the S2 boundary | experiment scope (D-3) | non-ATS targets wait longer | the first runs that can produce QN |
| P6 | Step-7 fallback | D-4 | ruling text | earlier repair bytes lost as input | v1 cannot be stranded |
| P7 | Experiments for runtime evidence | D-3 | charter | refused, then B10 stays OPEN | B5/B6/B10 leave paper |
| P8 | One outcome crosswalk | maps VALUE, ABSTENTION, UNKNOWN, UR, REJECT, B2 legal/illegal/abstain, B7 states, B10 lifecycle onto one display grammar, always showing the native state | assembly artifact | lossy mapping (mitigated by showing the native state) | one honest-state UI grammar |

Considered and rejected:
- **Go:** no new evidence; same acquisition-layer problem as Rust.
- **TypeScript:** violates B8 key order by default (verified) and adds a build step.
- **Rust + Python:** two canonical encoders that must stay byte-identical.
- **Postgres:** S6 freezes SQLite; local single file is a constraint.
- **Unfreeze B4 for approximate times:** DAY + verbatim text satisfies S3.
- **LLM classifier for role families:** S5 B7.5 forbids it.
- **Merge staging into core:** loses the receipted promotion boundary.
- **Drop the receipt chain:** cheap to keep; detects truncation.
- **Drop Wayback:** CDX has an S4 exhaustion predicate; keep it as AO capture metadata.
- **Graph database:** no v1 consumer.
- **Scores for connections:** the categorical rule.
- **A "closet" surface built from coverage gaps:** gaps are archive properties, not company facts.

## 11. Cut and park

| Item | Disposition | Rationale |
|---|---|---|
| Tier 4 exposure verification | CUT from the catalog and from v1; park the methodology as a record | no use; highest exposure |
| Donation and award timing analysis | PARK (platform) | money-graph only |
| Money-graph traversal paths | PARK (platform) | dream only |
| Procurement B10 fixture | stays quarantined; replaced via D-3 | out of domain; patterned hashes |
| `core_research_surface` | CUT (DL-4) | measures nothing |
| Superhuman Form D raise reconciliation | Docket only; outside v1 | money amounts are dream scope |
| Superhuman LinkedIn logged-in pass | Docket note only; never ingested | authenticated surfaces are outside S2 |
| Model-assistance inbox | PARK | no v1 need |
| Rust toolchain, musl target, Axum/Askama pins | PARK if D-1 = Python | superseded |
| Plottable | CUT | dormant (last release 2021-11-22, D3 v4) |
| Blueprint | CUT (R29) | build step, second render implementation |

## 12. Hand-waving register

| Item | State | What grounds it |
|---|---|---|
| Granule semantics (5.4); dense vs discrete completions | provisional | frozen B4 text in chat 6abdfc6f (D-7) |
| Disclosure-span contract | not designed | research item 8.4 |
| Evidence-plane DDL | named, not written | build phase |
| Composition classifier C | not designed | v1.1 research |
| ATS platforms of Duolingo, IBM, Datadog, NVIDIA | unknown | their careers pages, observed under S2 |
| Disk cost of raw captures | not measured | first experiment (D-3) |
| HTTP client choice | open | build detail |
| TypeScript rows not checked (pinned SQLite, INNOCUOUS) | unverified | not needed if D-1 = Python |
| Legal exposure of person-level data | not researched | moot if D-8 kills it |

Build authorization: NONE
