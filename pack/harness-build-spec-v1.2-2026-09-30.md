# UnSilo — Cipher-Powered Intel Harness — Build Spec v1.2

Date: 2026-09-30. Status: SPEC BEFORE BUILD. No implementation starts from this document without Justin's go.
Goal: goal_761bac3a2569. Vendor repo (read-only): `~/workspace/vendor/openplanter/`.
v1.2 delta: folds in the 16-drill Sol research gauntlet (2026-09-30, ChatGPT Chat surface, GPT-5.6 Sol, UnSilo project), the 6-tier research-surfaces baseline, the 16-finding type-safety adjudication, and the false-conviction red team. v1.0 and v1.1 are preserved untouched. Justin ratified the drill-15 override: the first investigation is the hiring-footprint v1, not procurement.

## 1. Objective

Strip-mine OpenPlanter for its useful investigative primitives and fold them into a small harness Cipher operates directly. Working name: **UnSilo** (project-only; no public name chosen — Countertrace killed on a live defense-contractor trademark, Parallax crowded, NegativeSpace clean but unchosen).

Positioning: **personal investigative intelligence over public records**. The anti-Palantir stance is an internal design adversary, not the public brand. Personal power instead of institutional power: we are meta's meta — we track and we analyze using what they give us and what they don't.

Doctrine: **presence is data, change is data, absence under an expectation is data.** (Refines Justin's "everything that isn't 0 is data": the correction, from the gauntlet, is that absence is only signal *under an expectation* — absence from a dataset is never evidence of absence in the world.)

Scope: a **career-intelligence system with a narrow corporate-forensics perimeter**. It investigates organizations, labor markets, roles, teams, and the public economic relationships around them. Every domain must pass through the core identity-resolution and relationship tables; new domains must reuse existing typed relations or they are out. Killed expansions (do not revisit without a scope review): competing vendor landscape, employee sentiment tracking, per-company competitive landscape, funding history, M&A history, customer references, personal investment/stock-picking, personal credit/debt, general real-estate intel, private-person dossiers, employee surveillance/attrition prediction, political opposition research, general cyber reconnaissance, consumer competitive intelligence, universal corporate knowledge graph.

Target capability, v1: **deterministically reconstruct and compare a company's publicly observable hiring state across time from public records.** One bounded question: "What material changes in this company's publicly observable hiring footprint occurred during period X?" Two public-company targets (dev case + transfer test). "Nothing consequential survived the evidence gates" is a successful run; UNRESOLVED is not a demo failure.

Hard constraints:

- Zero Anthropic/Claude API keys anywhere in the path. Verified: no script, fetcher, logger, or analysis module in the vendor repo imports Anthropic; the key dependence lives entirely in the excluded agent platform.
- Deterministic core: every number the harness reports is recomputed from hashed inputs by versioned code. Stochastic subjects stay stochastic; the instrument is deterministic.
- No model calls in the analytical pipeline. Model seats (ChatGPT, Gemini CLI) assist through bounded file-based contracts, never as inline dependencies. The core pipeline runs end-to-end with model access disabled.
- Vendor code is never imported. Adopted code is copied into the new package, hashed, and tested against current behavior before it replaces anything.
- Tier-4 operator policy: exposure verification is metadata only — listings, headers, scan records. Never download content from gray surfaces, never content retrieval, never use found credentials, never bypass access controls.

Done criteria (the 15 acceptance gates): two-target transfer; three real surfaces; no model dependency; acquisition truth survives failure; absence is earned (every negative claim carries its Expectation + SourceCheck); presentation set ≠ publication set demonstrated; identity correction doesn't leak into stale findings; declared grain holds on every metric; no coercion as interpretation; referential closure; mutation sensitivity (change a record → the finding changes); offline replay from receipts alone; epistemic red team run against the v1; maintenance proof (one month of simulated neglect degrades coverage, never silently corrupts truth); one genuinely useful result.

## 2. What the three passes agreed on (all verified against repo bytes)

Astra (GPT-6), Gemini (3.8 Flash via agy), and Codex (gpt-5.5) independently converged on:

1. **The cartel finding is hardcoded, not computed.** `scripts/build_findings_json.py:54` embeds "13 family-owned firms hold $163M in limited-competition contracts with zero new entrants in 6 years and 33-67% price escalation"; `:56-57` hardcode vendor_count 13 and total_contract_value 163170000; `:61` hardcodes the price range. Record counts are also hardcoded (`:146` 33481, `:149` 1497, `:152` 894). There is no reproducible implementation of the discovery. The capability must be rebuilt, not de-Bostoned.
2. **The four scripts are not a pipeline.** `entity_resolution.py:661` and `cross_link_analysis.py:475` both write `output/red_flags.csv` with different schemas (14-column manual CSV vs pandas DataFrame dump) — run order silently changes downstream data. `timing_analysis.py` consumes `output/cross_links.csv` plus `politician_risk_scores.json` and `snow_vendor_profiles.json`, which no script produces. `build_findings_json.py:8` reads `output/politician_timing_analysis.json`; `timing_analysis.py:301` writes `output/timing_statistical_analysis.json`. It also reads `politician_shared_network.json`, `bundling_events.csv`, `contribution_limit_flags.csv` — none produced anywhere. Wrapping the scripts preserves unreliable behavior.
3. **No Anthropic key is needed for any adopted component.** Verified by import grep across all candidate files.
4. **Take the wiki template and replay-log pattern; skip the engine, desktop, prompts, and TUI.** Unanimous.
5. **Phase order: contracts → ingestion → entity resolution → cross-link → timing → findings.** Unanimous.

## 3. Adjudicated disagreements

**D1. When is the harness first usable?** Astra: Phase 3. Gemini: Phase 1 is immediately usable — Cipher can operate the fetch CLIs directly on day one, and building an OCPF adapter in Phase 1 for a non-Boston investigation is wasted state-specific work. Adjudication: Gemini is right on both counts. Fetch CLIs need no build to be useful (Cipher invokes them now). Generic CSV/TSV/JSON ingestion comes before any domain adapter; jurisdiction-specific adapters are built on demand when an investigation needs them, not speculatively.

**D2. Fate of `timing_analysis.py`.** Astra: take distance primitives, redesign stats. Codex: primitives only, too brittle for Phase 1. Gemini: KILL the script — statistically broken and `censor_name` (`:28-32`, applied `:274-275`) replaces names with █ blocks, destroying the output's utility for downstream joins. Adjudication: the script dies; the 6-line `days_to_nearest_award` date-subtraction algorithm is reimplemented fresh from its description, not ported.

**D3. The eleven non-SEC fetch CLIs.** Codex: defer, bodies unverified. Gemini: take all 12, stdlib-only. v1.1: take all 12 with repairs. v1.2 (gauntlet override): **promote on demand.** The CLIs remain operator tools Cipher runs directly. The harness absorbs an adapter only when an investigation needs it and it passes the per-source behavior checklist (pagination, throttling, completeness, credential needs, bulk-use terms) — "earn promotion by becoming painful twice." v1 ships with exactly 3 promoted adapters (SEC EDGAR, first-party careers surface, Wayback CDX).

**D4. Receipt 204.** Astra: the two scripts disagree on inclusion. Gemini sharpened: 204s ("Non-contribution receipt", `entity_resolution.py:118`) are extracted into `contributions`, counted in `boston_contributions.csv` (`:683`), but `match_entities` only matches record types `201` (`:343`) and `202/203/211` (`:407`) — 204s are counted and never matched. Verified. Spec consequence: record-type semantics belong in the source adapter, and counting populations must never mix matched and unmatched record types silently.

**D5. First-investigation target: procurement vs hiring footprint.** v1.1: procurement recommended (Astra's call). Gauntlet drill 15: hiring-footprint v1 — 3 surfaces, tighter portfolio story, directly exercises the career-intelligence thesis. Adjudication (ratified by Justin 2026-09-30): hiring footprint wins. Procurement moves to the promotion queue; it has not earned its adapter yet.

**D6. "Take all 12 fetchers" vs fewer excellent surfaces.** v1.1 took all 12. Gauntlet: 26 surfaces ranked across 5 tiers; 26 continuously maintained surfaces is a solo trap (8–12 h/week, too much for one operator). Adjudication: the catalog is the baseline, the v1 hot set is 3 surfaces, the 7-surface bootstrap (SEC EDGAR, DOL H-1B, USASpending, SAM.gov, first-party sitemaps/RSS/JSON-LD, one visitor-visible jobs/frontend API, Wayback CDX) is the promotion queue. Maintenance principle: **never require immediate repair; require immediate loss of authority** — neglected sources degrade coverage visibly, never silently corrupt truth.

## 4. Verified defect register (do not reintroduce)

All items verified at the cited file:line. Any adopted code touching these areas must carry a regression test for the defect.

- **V1.** Hardcoded conclusions in the findings builder (build_findings_json.py:51-61, :146-152). Findings must be computed from evidence, never templated.
- **V2.** `red_flags.csv` schema collision (entity_resolution.py:661 vs cross_link_analysis.py:475). One writer per artifact name; schema declared in the case manifest.
- **V3.** Phantom inputs: findings builder reads four files no script produces (build_findings_json.py:8,14,19,25); timing needs two more (politician_risk_scores.json, snow_vendor_profiles.json). Every declared input must have a producer or an explicit completeness flag.
- **V4.** Permutation test is not a permutation test (timing_analysis.py:15 docstring claims 10,000 shuffles; :95/:265 execute 1,000 uniform-random draws via np.random.uniform at :128; no seed set anywhere). Null model, seed, and iteration count are recorded parameters.
- **V5.** Begin date relabeled as award date (timing_analysis.py:167: `contracts['award_date'] = contracts['cntrct_hdr_cntrct_begin_dt']`). Date semantics are declared per source; the pipeline distinguishes award date, contract start, transaction date, and filing date as separate typed fields.
- **V6.** Rejoin by exact display name loses alias-grouped contracts (timing_analysis.py:240). All joins use canonical entity IDs, never display names.
- **V7.** Destructive normalization merges identities before decisions (vendor dicts keyed by normalized names; aggressive normalization strips SERVICES/GROUP/TECHNOLOGY). Normalization is comparison-only; originals are preserved; canonical entities get stable IDs.
- **V8.** `seen_matches` dedup is a no-op (entity_resolution.py:349-352 — `matches.append` sits outside the `if match_key not in seen_matches` block). Dedup logic gets a direct unit test.
- **V9.** 204 non-contribution receipts counted but never matched (entity_resolution.py:118, :343, :407, :683). Adapter declares record-type semantics; unmatched types are quarantined from match populations, not silently counted.
- **V10.** Censored output destroys joinability (timing_analysis.py:274-275). Redaction is an export-view concern only; analytical keys are never redacted in the pipeline.
- **V11.** Logger cannot replay (agent/replay_log.py:82,88 — message-count deltas miss edits; restart reuses sequence numbers; no input snapshots, code versions, or seeds). The run ledger records inputs, hashes, versions, params, and seeds; model outputs are recorded artifacts, re-calling the model is not replay.
- **V12.** Money and dates are untyped (amounts as floats/strings; date meanings conflated). Money is exact decimal or integer minor units; malformed values are quarantined, never zeroed.

## 5. Final component decisions

| Component | Decision | Form in the harness |
|---|---|---|
| 12 fetch CLIs (`fetch_sec_edgar.py` et al.) | Operator tools; promote on demand | Cipher runs them directly from day one. Harness absorbs an adapter only when an investigation needs it and it passes the behavior checklist. v1 promotes exactly 3: SEC EDGAR, first-party careers surface, Wayback CDX. |
| `wiki/template.md` + source pages | TAKE as docs | Source-onboarding contract format → upgraded to executable source contracts (§6): machine-readable source ID, adapter version, snapshot hash, exact join keys, date semantics, verification date, plus identity/enumeration/temporal/boundary sub-contracts. |
| `agent/replay_log.py` | TAKE pattern, rewrite contract | JSONL run ledger: run IDs, artifact SHA-256 hashes, input snapshots, code version, parameters, seeds, stage names, decision provenance, model request/result hashes. Append-only, concurrency-safe. v1.2: hash-chaining cut (no adversary) — SHA-256 content addressing + git carry history integrity. |
| `entity_resolution.py` | TAKE algorithms only | OCPF join path, employer/vendor matching ideas, token indexing → reimplemented inside the Phase 2 ER service. Script itself is discarded. Membership decisions versioned and reversible (§7). |
| `cross_link_analysis.py` | TAKE analytical patterns only | Grouping/aggregation patterns → reimplemented as Phase 3 rules on canonical IDs, driven by pivot algebra (§9). Pipeline discarded. |
| `timing_analysis.py` | KILL script; reimplement primitive | `days_to_nearest_award` reimplemented from description in Phase 4. Nothing else survives. Selective temporality (§11): observation time everywhere, effective time only where the source asserts intervals. |
| `build_findings_json.py` | SKIP implementation; keep the idea | New schema-validated findings exporter (Phase 3). No embedded cases, counts, dates, severities, or labels. Two-tier evidence: ordinary query results carry a provenance receipt; consequential published claims carry the closed dependency package. |
| `quickstart_investigation.py` | SKIP as entry point | Salvage CLI-shape ideas only. |
| `agent/demo.py` | SKIP from core | Optional export-redaction step later, with stable pseudonyms. |
| Engine, model factory, credentials, prompts, tool runtime, TUI, Tauri desktop | EXCLUDED | Cipher is the orchestrator. No imports from `agent.*`, provider factories, or credential stores in the deterministic core. |
| `pyproject.toml` | REPLACE | Fresh package with explicit dependencies. Working name: `unsilo` (project-only). |
| Typed command/event-sourcing system (v1.1 §6) | CUT | Replaced by an append-only decision journal: decisions are rows, not commands. No expected_state_version preconditions, no idempotency-key machinery, no generic command type system. Reversibility is preserved through superseding MembershipDecisions, not compensating events. |
| Generalized BoundaryPolicy engine (v1.1) | CUT | Replaced by per-source export flags + license/terms metadata in the Source contract. Exports check flags; denials are logged. No policy engine. |
| Hash-chained ledger + independent checkpointing (v1.1) | CUT | SHA-256 content addressing + append-only JSONL + git. No ledger hash chain, no per-run chain-head checkpointing. |
| Generalized property-projection policies (v1.1) | CUT | Competing assertions coexist; per-query explicit preference; undefined conflict yields `conflicted`/`unknown`, never a silent pick. No projection-policy engine. |
| v1 watches (v1.1) | DEFER | Saved query + deterministic run diffs. The Watch type with temporal predicates is a promotion candidate, not v1. |
| Universal MetricProof (v1.1) | DOWNGRADE | Two tiers: provenance receipt (ordinary results) vs closed dependency package (consequential claims only). |
| Bitemporality everywhere (v1.1) | SELECTIVE | `observed_at` on everything; `valid_from`/`valid_to` only where sources assert effective intervals. Knowledge-time queries via observation cutoffs. |
| Release/branch language (v1.1 §16) | CUT | Git tags + migrations + fixture gate. |

## 6. Architecture

Layers, kept small:

| Layer | Responsibility |
|---|---|
| Cipher | Chooses questions, invokes stages, inspects failures, reviews ambiguous pairs, requests model assistance, explains findings; records investigations, hypotheses, and decisions |
| Case configuration | Declares sources, field mappings, scope, entity types, relationship types, rules, thresholds, property definitions, grain declarations |
| Acquisition truth | Expectations, SourceChecks, NegativeObservations, TraversalState; the `probe(surface, expectation)` primitive; executable source contracts; probe --qualification |
| Deterministic core | Ingests, validates, resolves identities, joins, aggregates, analyzes time, exports — no model calls, no network except fetch adapters |
| Evidence store | Raw snapshots (immutable), source records with revisions, decisions, relationships, events, findings, investigations; local relational store + immutable files + JSON/CSV exports; edge table for graph relationships |
| Decision journal | Append-only record of every accepted investigative decision (replaces the v1.1 typed-command system): decision rows, not commands; reversibility through superseding decisions |
| Assistance inbox/outbox | Bounded model tasks (file in: evidence refs + output schema; file out: validated artifact). Manual export/import is a valid fallback. Every package's source export flags are checked before a model seat sees it |
| Run ledger | Inputs, code versions, parameters, seeds, outputs, decisions, completeness — append-only JSONL, every artifact SHA-256 hashed. No hash chain (no adversary); git carries history integrity |

No graph database, vector store, scheduler, or recursive agent runtime. Those are not prerequisites. Saved queries plus deterministic run diffs replace v1.1's watches; the Watch type is a promotion candidate, not v1.

**Deterministic vs model-assisted.** Deterministic: probing, ingestion, validation, normalization, candidate-pair generation, aggregation, distance computation, export, ledger writes, diff evaluation. Model-assisted (never inline, always through inbox/outbox): field-mapping proposals for new sources, entity-mention extraction from documents, ambiguous identity-pair adjudication (Cipher reviews first; seats consulted only when Cipher cannot decide). Every model output is deterministically validated against its schema before entering accepted data; rejected proposals never touch the store. Accepted model proposals additionally pass semantic checks (evidence references resolve, types are consistent); JSON-schema validity alone is not acceptance. The core pipeline runs end-to-end with model access disabled; model-assisted stages pause as `needs_review` while accepted artifacts remain replayable.

**Seat fallback.** Codex CLI → Gemini CLI (agy) → Cipher direct. Fallbacks are ledger-logged events. Known flakiness: agy throws geo-400s intermittently; codex is bound to account usage. Neither is load-bearing for the deterministic core.

**Pivot-first workspace.** The investigation workspace is pivot-first, not answer-first. A pivot is a deterministic function from one evidence object to a bounded set of related objects, each with declared grain and a provenance receipt. Pivot types: entity→records, entity→relationships, relationship→entities, record→entities, time-slice diff (same cohort, two effective times), cohort→members, expectation→source-checks. The workspace never presents an aggregate without its cohort, grain, and acquisition truth on the same screen.

## 7. Acquisition truth

The layer that makes "everything claimed is evidence-backed" executable. Three closures are distinguished: **graph closure** (every claimed edge resolves to evidence for both ends — achievable), **acquisition closure** (every expected surface was checked and its state recorded — achievable only with the expectedness engine), **world closure** (the records reflect the world — impossible under open-world public records; never claimed).

- `Expectation`: expectation_id, version, statement (what should exist), provenance (source contract clause / prior observation / schema — never invented), scope (surface, time bounds, entity bounds), created_by, created_at. Expectations are versioned; changing one appends a new version, never edits.
- `SourceCheck`: check_id, expectation_id + version, surface_id, adapter version, executed_at, acquisition_state, evidence refs (snapshot hash, row locators), notes. A re-probe appends a new SourceCheck; states are never mutated.
- `NegativeObservation`: observation_id, source_check_id, what was expected, what was found, interpretation — closes a branch, qualifies a finding, or triggers a probe. Never a graph anti-edge: it does not assert non-existence in the world.
- `TraversalState`: investigation_id, frontier (entity/relationship/record refs under active pursuit), visited set with acquisition states, open branches, closed branches with reasons.

Acquisition state machine:

- `NOT_EVALUATED` → `ATTEMPTED` → one of the terminal states.
- Terminal: `COMPLETE_WITH_MATCHES`, `COMPLETE_NO_MATCHES`, `SOURCE_SAYS_ZERO`, `FIELD_ABSENT`, `NOT_APPLICABLE` — final for that expectation version.
- Terminal-for-this-run, re-probeable: `FETCH_INCOMPLETE`, `COVERAGE_INCOMPLETE`, `SCHEMA_DRIFT` — a re-probe appends a new SourceCheck; the old state is never overwritten.

Seven-way absence semantics as data: every "nothing found" resolves to exactly one state. `SOURCE_SAYS_ZERO` (the surface asserts zero) is evidence; `COMPLETE_NO_MATCHES` (checked, nothing matched) closes a branch; `FIELD_ABSENT` (the surface has no such field) kills the expectation's applicability; `FETCH_INCOMPLETE` / `COVERAGE_INCOMPLETE` (we didn't see everything) forbid any absence claim; `SCHEMA_DRIFT` (the surface changed shape) invalidates the expectation version; `NOT_EVALUATED` / `NOT_APPLICABLE` are not absence at all.

**Executable source contracts.** Four clauses, machine-checkable:

- Identity clause: what identifies a record — exact keys (CIK, EIN, filing IDs), quasi-keys (normalized name + address block + date).
- Enumeration clause: how listing completeness is known — pagination mechanics, count reconciliation, coverage statements.
- Temporal clause: date semantics per field (award vs start vs transaction vs filing), amendment/supersession behavior, which fields carry effective intervals.
- Boundary clause: what is in and out of the surface, export flags, license/terms note, and for Tier 3+ the exact access boundary touched.

**Deterministic expectedness and applicability predicates.** Boolean functions over (surface, scope): does this expectation apply here? Example: "EDGAR 10-K expectation applies to CIKs with active filer status for fiscal year Y." Applicability is computed, never assumed; an inapplicable expectation yields `NOT_APPLICABLE`, not silence.

**`probe(surface, expectation)`.** The single acquisition primitive. Takes a surface handle and an Expectation version, executes the contract's enumeration, and returns a SourceCheck with an acquisition state. All acquisition flows through probe; there is no ad-hoc fetching path in the deterministic core.

**probe --qualification.** The one automation the maintenance doctrine allows. Four fingerprints per surface: transport (does the surface respond as the contract says), structural (does the schema match the contract), semantic (are values in expected domains), enumeration (do completeness signals hold). Outputs: `QUALIFIED`, `DRIFTED`, `INCOMPLETE`, `UNAVAILABLE`, `NOT_EVALUATED`. A `DRIFTED` or worse result revokes the surface's authority for new claims until re-qualified — never require immediate repair; require immediate loss of authority.

### 7.6 Per-tier methodology (drills 17–22, 2026-09-30)

Six methodology playbooks, one per research-surface tier, each produced in its own fresh UnSilo-project Sol chat (Chat surface, GPT-5.6 Sol verified, research only, no outbound actions). Every playbook delivers: step-by-step acquisition procedure, Expectation-predicate construction, SourceCheck contract, NegativeObservation earn/never rules, four-dimensional probe --qualification fingerprints (transport, structural, semantic, enumeration), and characteristic failure modes. The chats are the canonical playbooks; this section records the load-bearing invariants. No ethics pushback occurred in any of the six drills, including the gray Tier 4 drill — the defensive exposure-verification framing held throughout.

- **Tier 0 — compelled disclosure** (FOIA/state records, RECAP/CourtListener, legislative records). Playbook: [Tier 0 methodology chat](https://chatgpt.com/g/g-p-6abd6123a014819192a3a400854f67b7-unsilo/c/6abd6b93-9078-83ea-b5f2-3130af0f97e0). Agency targeting, narrow request drafting, fee-waiver handling, tracking numbers, production-completeness analysis via Vaughn indices. A Glomar response is not absence — it is a refusal that leaves the SourceCheck at ATTEMPTED with a refusal note; it never licenses SOURCE_SAYS_ZERO. RECAP docket acquisition via CourtListener; PACER cost discipline; legislative pulls via Congress.gov and state legislatures. Justin owns all filing and outreach; the harness covers preparation, tracking, and analysis of returns. Incomplete productions are recorded as COVERAGE_INCOMPLETE, never silently treated as complete.
- **Tier 1 — official public datasets** (SEC EDGAR, FEC, DOL H-1B, OSHA, USASpending, SAM.gov, ICIJ, nonprofit 990s, lobbying records, assessor/GIS). Playbook: [Tier 1 methodology chat](https://chatgpt.com/g/g-p-6abd6123a014819192a3a400854f67b7-unsilo/c/6abd6c0f-96f8-83e9-9dc9-8441520ed7b3). Bulk vs API acquisition paths, schema-drift detection against the contract's structural fingerprint, enumeration completeness checks, amendment/supersession handling (new versions, never mutated rows), cross-dataset join keys (CIK, EIN), coverage statements. Expectedness predicates take the form "dataset D should contain records of type T for period P". The tier's core discipline is distinguishing SOURCE_SAYS_ZERO (the dataset asserts zero) from COVERAGE_INCOMPLETE (we didn't see everything) from FIELD_ABSENT (the dataset has no such field).
- **Tier 2 — passive web exhaust** (Common Crawl, Wayback CDX, search/GitHub dorking, Certificate Transparency, DNS/ASN). Playbook: [Tier 2 methodology chat](https://chatgpt.com/g/g-p-6abd6123a014819192a3a400854f67b7-unsilo/c/6abd6c8d-9630-83e9-bb9e-14d132f16c49). CDX API query construction (URL wildcards, collapse, filters), Common Crawl index queries and WARC record handling, CT log querying, passive DNS/ASN correlation, dork construction and result triage. Eight deterministic change predicates — APPEARED, DISAPPEARED, TEXT_CHANGED, ENTITY_RENAMED, RELATIONSHIP_REMOVED, DISCLOSURE_NARROWED, SUBDOMAIN_APPEARED, SOURCE_SCHEMA_CHANGED — each with claim-licensing rules: a firing predicate licenses a claim about the captured record set, never about the world beyond the captures. Capture coverage itself requires an Expectation (were captures expected in this window?).
- **Tier 3 — visitor-level site-native** (undocumented frontend APIs, sitemaps, RSS/Atom, JSON-LD). Playbook: [Tier 3 methodology chat](https://chatgpt.com/g/g-p-6abd6123a014819192a3a400854f67b7-unsilo/c/6abd6cf6-27ec-83e9-8af7-47d0e3e50117). Discovery graph: sitemap → robots.txt as discovery document → feeds → JSON-LD → frontend APIs observed through normal browsing. Endpoint classification (public vs access-controlled), boundary clauses recording exactly what was touched, rate discipline. Invariant: a 404 or empty array is not a NegativeObservation — it means the endpoint moved, the contract is wrong, or the expectation is inapplicable (SCHEMA_DRIFT / NOT_APPLICABLE / re-probe), never earned absence. Red lines: no authentication bypass, no parameter tampering to reach non-public data, no credential use.
- **Tier 4 — exposure verification** (open-bucket indexes, Shodan/Censys records, public code/document exposure, breach-presence awareness). Playbook: [Tier 4 methodology chat](https://chatgpt.com/g/g-p-6abd6123a014819192a3a400854f67b7-unsilo/c/6abd6d44-a400-83ea-84f1-bb07e24f04df). Maximum-care gray tier, framed as defensive exposure verification throughout. Query bucket-index metadata (indexes, never the buckets); interpret Shodan/Censys scan records and banners as metadata; find public code/document exposure through search indexes; breach-presence awareness through presence-check metadata. ABSOLUTE RULES: metadata only (listings, headers, scan records); never download content; never access the exposed service itself; never use found credentials, tokens, or sessions; never attempt authentication of any kind; on confirming an exposure, record the exposure fact (which index, which record, when observed) and stop. Fourteen characteristic failure modes including boundary-creep cases ("just one GET to confirm", preview thumbnails rendering content, cached copies) — each is a KILL, not a judgment call. A NegativeObservation here is earned only by a clean check against the relevant indexes with the expectation version recorded.
- **Tier 5 — human sources** (Justin-owned outreach, FOIA follow-ups). Playbook: [Tier 5 methodology chat](https://chatgpt.com/g/g-p-6abd6123a014819192a3a400854f67b7-unsilo/c/6abd6dad-b114-83ea-93eb-83561f71d6b7). Cipher never performs outbound — all outreach is Justin's. No pretexting, ever. Outreach packet preparation, FOIA follow-up state machine (filed → acknowledged → production → appeal → closed), interview note structure, source characterization. Human-source claims enter the evidence model as attributed assertions, never ground truth; corroboration gates apply before they support any finding above UNRESOLVED.

## 8. Data contracts

Shared model, declared in Phase 0 before any code. v1.1 types retained except where §5 cuts them; v1.2 additions:

**Career ontology (fixed vocabulary).** The narrow ontology the gauntlet froze: `Company`, `BusinessUnit/Team`, `Role`, `JobPosting`, `Skill/Technology`, `Location` (v1; `Person` and `CompensationObservation` deferred to promotion). Typed relations: `ROLE_AT`, `POSTED_BY`, `MEMBER_OF_TEAM`, `REQUIRES_SKILL`, `INSTANCE_OF`. New domains must reuse these relations or stay out. Every analytical value carries its declared grain (§9, law 1).

- `Source`: source ID, adapter name + version, access method, coverage statement, snapshot hash, verification date, license/terms note, export flags, boundary clause ref. v1.2: executable contract clauses (§7) live here.
- `Record`: source-scoped stable ID (`{source_id}:{native_id}`), raw field values preserved verbatim, row/document locator, ingest timestamp, SHA-256 of the raw snapshot it came from.
- `RecordVersion`: logical_record_id, record_version_id, snapshot_hash, row_locator, content_hash, observed_at, valid_from / valid_to (only where the source asserts an effective interval — selective temporality, not universal bitemporality). A `{source_id}:{native_id}` is a logical identity, not a revision. Unknown endpoints are unknown, never silently open-ended; source disagreements are preserved, never forced into global non-overlap.
- `Entity`: canonical stable ID (never a normalized display name), entity type, merged-from mention IDs, effective identity state (the registry version whose membership decisions are in force for this view).
- `EntityMention`: the as-observed name/alias/address block tied to a Record ID and record version ID.
- `ResolutionDecision`: candidate pair, decision (accepted / rejected / unresolved), evidence refs, rule name + version, decider (deterministic rule / Cipher / model seat + artifact hash), timestamp.
- `MembershipDecision`: decision_id, mention_id, entity_id, decision_version, supersedes_decision_id, decision (accepted / rejected / cannot-link / unresolved), evidence refs, rule version, decider, timestamp. Entity IDs stay stable; every downstream artifact pins the `registry_version` it computed against. Merges append decisions; nothing is rewritten. A split preserves the previous registry snapshot. Previously computed findings remain reproducible under their original registry; current findings depending on changed membership become stale until recomputed (transitive staleness, §10). An explicit "these are different entities" is a `cannot-link` constraint: an ordinary rejection is not a cannot-link, and an A–B plus B–C match can never silently override an explicit A–C cannot-link (resolution non-circularity, §10).
- `DecisionJournalEntry` (replaces v1.1 `Command`): decision_id, decision_type, subject refs, evidence refs, reason, decider, timestamp, supersedes_id. Append-only. No expected-state preconditions, no idempotency machinery — the journal is a record, not a state machine.
- `PropertyAssertion`: assertion_id, subject_ref (entity or mention ID, preserving the originating mention so identity corrections don't destroy property history), property_type, typed_value, record_version_id, field locator. Competing source statements coexist as separate assertions. Per-query explicit preference; undefined conflict yields `conflicted` or `unknown`, never a silent pick. No generalized projection-policy engine. Property definitions declare units, currency, cardinality, meaning — a contract ceiling and an amount paid are different properties even when both are money.
- `Relationship`: subject entity ID, object entity ID, relationship type from the case-declared allowlist, evidence record IDs for both ends, the join or decision that connects them, validity interval (selective — where the relationship is time-bounded).
- `Event`: typed date (award / start / transaction / filing), entity refs, amount in minor units, record ID + record version ID.
- `Finding`: finding ID, rule name + version, entity IDs, evidence record IDs, computed metrics, parameters used, limitations, claim-scope ceiling (§10), verdict (CONFIRMED / DOWNGRADED / KILLED / UNRESOLVED).
- `EvidencePackage` (replaces universal v1.1 MetricProof): two tiers. **ProvenanceReceipt** (ordinary results): input artifact hashes, record_version_set_hash, registry_version, code version, parameter set, seed. **ClaimPackage** (consequential published claims only): everything in the receipt plus the closed dependency set — review decisions, mappings, model artifacts. A clean, network-disabled process can reconstruct the claim from the package alone; missing dependencies produce `unreplayable`, never a cached successful answer. Recomputation never consults the current registry or current case configuration implicitly. Bit-for-bit requirement is scoped: the canonical analytical payload (stable sorting, decimal encoding, null handling) must reproduce exactly; the execution receipt around it may differ.
- `Investigation`: investigation_id, question, scope_hash, completion_criteria, status, epistemic perimeter (§13).
- `SavedQuery`: query_id, investigation_id, query text + parameter version, executed_at, cohort_hash, truncation notes. Returned cohorts are frozen and reproducible.
- `Hypothesis`: hypothesis_id, investigation_id, statement, plausible alternatives, falsifier, status (open / supported / weakened / killed), assessment history in the decision journal. A confirmed descriptive finding never auto-confirms a causal hypothesis; when a finding dependency changes, linked hypotheses become `needs_review` without rewriting their history.
- `Run`: run ID, case ID, code version, input hashes, parameter set, seeds, stage outputs with hashes, completeness status, started/finished timestamps.

Source observations, identity decisions, property assertions, and analytical hypotheses are stored separately and never mixed. Every derived relationship cites evidence for both ends. Every displayed factual property resolves to its supporting assertion.

**v1.1 types cut or deferred:** `Command` → `DecisionJournalEntry`; `BoundaryPolicy` → per-source export flags; `Watch` → deferred (saved query + run diffs in v1); universal `MetricProof` → two-tier `EvidencePackage`.

## 9. Type-safety laws

Seven laws, from the adjudicated 16-finding type-safety review (13 concede, 3 contest-as-written; findings #2 and #16 used incorrect SQLite examples but their policy concerns partly survived). Every analytical value in the harness obeys all seven; violations are defects, not style issues.

1. **Declared analytical grain.** Every metric declares the grain it is computed at (per-posting, per-role, per-company-per-month, …). The grain is part of the metric's identity; changing grain creates a different metric. No grain, no number.
2. **Canonical typed analytical values.** Money is integer minor units or exact decimal; dates are typed (award / start / transaction / filing / observed); counts are integers over declared populations. Malformed values are quarantined, never zeroed or coerced.
3. **Exact arithmetic domain and explicit rounding.** Aggregation arithmetic is exact until the declared rounding point; rounding rules are recorded parameters. Floats never carry money.
4. **Effective-state projections.** Any view of "current state" is an explicit projection over the versioned record set at a declared registry version and observation cutoff — never a read of mutable rows. There is no mutable "current" table.
5. **Acquisition truth before analytical truth.** No analytical claim may outrun its acquisition truth: every metric's SourceChecks must be terminal (not FETCH_INCOMPLETE / COVERAGE_INCOMPLETE / NOT_EVALUATED) before the metric is computed. Absence claims additionally require an earned NegativeObservation.
6. **Referential closure.** Every ID a finding cites — entity, record, record version, decision, expectation — must resolve inside the evidence store at the pinned versions. Dangling references are defects; a finding with an unresolvable reference is KILLED.
7. **No coercion as interpretation.** Missing is never zero, unknown is never a default, a string is never silently a number, a display name is never an identity. Every coercion is an explicit, recorded, reversible decision or it does not happen.

## 10. Epistemic invariants

Six invariants from the false-conviction red team. The red team's central conclusion: **the hardest remaining problem is not provenance — it is licensing: does this evidence actually license the sentence Cipher is about to say?** The most dangerous failure mode is a coherent, provenance-rich false narrative assembled from individually defensible observations. These invariants are the defense.

1. **Expectation provenance.** Every Expectation records where it came from (contract clause, prior observation, schema). An expectation with no provenance cannot license an absence claim.
2. **Claim-scope ceiling.** Every finding carries the maximum it is allowed to assert, derived from its evidence: population, time bounds, surface coverage. A finding about "postings on the careers surface" never speaks about "hiring."
3. **Resolution non-circularity.** Identity decisions cannot be justified by the findings they would support. An A–B plus B–C match never silently overrides an explicit A–C cannot-link. The resolution graph is checked for circular justification before any finding that depends on it is published.
4. **Transitive staleness.** When a membership decision is superseded, every downstream artifact — findings, cohorts, saved queries, hypotheses — is marked stale until recomputed or explicitly revalidated. Stale artifacts are never served as current. (This was the review's most consequential finding: superseded membership leakage.)
5. **Traversal non-entailment.** Traversing a relationship path does not entail the claim the traversal suggests. person→employer→vendor→contract is a path to investigate, not evidence of a scheme. Each hop's evidentiary weight is assessed separately.
6. **Presentation monotonicity.** Adding evidence to a presentation never silently strengthens a claim: new supporting evidence is labeled new, and the claim's ceiling is recomputed. A presentation that looks more convincing because more was piled on, without re-derivation, is a defect.

## 11. Entity-resolution policy

Three separated operations, one service:

1. **Normalize for comparison.** Type-appropriate normalization (person vs organization rules differ); originals always preserved; normalization output is never a key.
2. **Generate candidate pairs.** Exact source identifiers first, then normalized names, alias lists, address blocks, token/fuzzy retrieval (similarity scores are similarity measures, not probabilities; thresholds are case heuristics, never defaults). Candidate-generation configuration, block sizes, and recall are recorded; candidate recall is validated separately from decision accuracy on hand-built fixtures. A non-generated pair is not an adjudicated nonmatch. v1.2: candidate generation is a pivot (mention→candidate mentions) with declared grain.
3. **Decide identity.** Accepted / rejected / cannot-link / unresolved, each with evidence refs and rule version. Ambiguity produces `unresolved`, never a forced best match. Same-name distinct organizations stay separate (counterexample fixture, §16).

Versioning discipline: identity is correctable without destroying history. Merges and splits are appended `MembershipDecision` rows against a versioned registry; entity IDs stay stable; every downstream artifact pins its `registry_version`; a membership change marks every dependent artifact stale (invariant 4). Cipher reviews the ambiguous queue through the decision journal; decisions are recorded so reruns never repeat a consultation. Effective identity state: any view of "the entities" is a projection at a declared registry version — there is no mutable entity table.

Person/organization discipline: an employee's contribution creates a person→employer→organization relationship; it never becomes a corporate donation. A shared address is a relationship signal, not an identity merge.

## 12. Cross-link / join-key model and pivot algebra

Join keys are declared per source in the case manifest (from the executable source contract): exact keys (CIK, EIN, filing IDs), quasi-keys (normalized name + address block + date), and relationship paths (person→employer→vendor→contract; shared officer/registered agent). Phase 3 rules run against canonical entity IDs and emit findings for: cross-dataset entity overlap; person→employer→vendor→contract paths; shared address/officer/agent links; distinct-donor clusters within configurable windows (count distinct resolved donors, not rows); vendor/recipient breadth and shared-donor hubs; hiring-footprint changes (posting appearance/disappearance, role mix shifts, location mix shifts, skill-mix shifts across effective time). Output labels stay neutral ("repeated supplier cohort", "same-day employer-linked contributions", "posting cohort contraction"); stronger readings are hypotheses requiring more evidence. Every rule declares the record versions and registry version it ran against; rules over historical relationships respect validity intervals and observation cutoffs (§8).

**Pivot algebra.** The investigation workspace exposes a closed set of deterministic pivots, each a pure function from evidence objects to bounded evidence-object sets with declared grain and provenance receipts: entity→records, entity→relationships, relationship→entities, record→entities, mention→candidate-mentions, cohort→members, expectation→source-checks, time-slice diff (same cohort definition, two observation cutoffs). Composing pivots is the only traversal mechanism; there is no free-form graph walk. Traversal non-entailment (invariant 5) applies at every hop: the pivot returns candidates for investigation, not conclusions.

## 13. Findings taxonomy, licensing, and the epistemic perimeter

Four-state verdicts, Justin's standing taxonomy: **CONFIRMED / DOWNGRADED / KILLED / UNRESOLVED**. Every UNKNOWN stays explicit; quarantined records are listed, not dropped. No finding carries a severity or verdict the evidence does not support. UNRESOLVED is a correct final state, not a demo failure — "nothing consequential survived the evidence gates" is a successful run.

**Licensing check.** Before any finding is presented, the licensing question is answered in writing: does this evidence actually license the sentence Cipher is about to say? The check covers: claim-scope ceiling (invariant 2), acquisition truth completeness (law 5), resolution non-circularity (invariant 3), and alternative explanations (the hypothesis's plausible-alternatives field). A finding that fails licensing is DOWNGRADED or KILLED, never presented with softened language.

**Epistemic perimeter.** Every investigation declares its perimeter up front: which surfaces were probed, which expectations applied, which acquisition states are terminal, and therefore what the investigation *cannot* see. The perimeter is part of every presentation. Claims outside the perimeter are not made.

**Presentation monotonicity** (invariant 6) governs every report: the presentation set (what is shown) is explicitly distinguished from the publication set (what the surface published) and from the acquisition set (what was checked). Adding evidence recomputes ceilings; it never silently strengthens.

Evidence format: every artifact gets a SHA-256 receipt (hash, producer, timestamp, input hashes). Ordinary results carry a ProvenanceReceipt; consequential claims carry the closed ClaimPackage (§8). A finding is valid only if its entity IDs, evidence record IDs, metrics, parameters, rule version, and acquisition truth are all present and recomputable.

## 14. Timing-analysis minimum-data gates

Timing runs only when: identities are resolved, events are deduplicated, dates are typed (§8), the cohort is declared, and acquisition truth is terminal for the cohort's sources (law 5). Descriptive output first: signed event-to-event distances, before/after window counts and amounts, distinct participants, coverage and missing-date accounting, the exact date type used. Statistical testing only with a defensible null model, and then with recorded observation interval, cohort definition, random seed, simulation count, test family, calendar-structure handling, and multiple-testing correction. "Three donations = statistical validity" and "nonsignificant = normal" are banned inferences; where assumptions fail, the stage returns descriptive results with an explicit abstention from significance claims. Deterministic reruns must reproduce results bit-for-bit given the recorded seed.

Selective temporality: `observed_at` is recorded on everything; `valid_from`/`valid_to` only where sources assert effective intervals (employment spans, filing effective dates, posting open/close windows). Knowledge-time queries use observation cutoffs. A filing received in June that corrects ownership effective in January must not leak into a March knowledge-time analysis. Uncertain dates are never represented as precise ones.

## 15. Phases and exit gates

**Phase 0 — Evidence contract and acceptance case.** Findings schema, case-manifest schema, executable source-contract format, run-ledger format, acquisition-truth object schemas (Expectation, SourceCheck, NegativeObservation, TraversalState), career ontology, pivot definitions, and a synthetic acceptance fixture (aliases, same-name distinct orgs, duplicates, amendments, missing dates, employer-linked donations, shared addresses, repeated procurement cycles, posting appearance/disappearance, expectation-version changes; known positives and negatives). Boston kept only as an optional regression case. Exit gate: a case is specifiable with zero Boston-specific fields; the package starts with no model credentials anywhere; every contract type has a schema and at least one fixture row; §7.6 per-tier methodology is filled from drills 17–22.

**Phase 1 — Ingestion, evidence preservation, acquisition truth.** The 3 promoted adapters (SEC EDGAR, first-party careers surface, Wayback CDX); generic CSV/TSV/JSON → canonical records with source-scoped IDs; raw snapshots preserved; money as minor units; malformed values quarantined; coverage gaps recorded; the `probe(surface, expectation)` primitive and probe --qualification; thin command runner (structured status, per-run dirs, input/output hashes). Successive versions of the same native record are preserved as `RecordVersion` rows; observation dates stored from the first ingest, effective intervals only where asserted. Exit gate: every accepted record resolves to its exact source bytes; missing required data cannot read as "zero findings"; a re-ingested amended source produces a new record version, not a mutated row; every acquisition flow goes through probe; a DRIFTED surface loses authority visibly. (Cipher can operate the fetch CLIs directly from day one, independent of this build.)

**Phase 2 — One entity-resolution service.** §11 implemented; persistent entity registry, alias mappings, review queue, auditable edges; all identity changes flow through the decision journal; every downstream artifact pins its registry version; a membership change identifies every affected downstream artifact as stale. Exit gate: alias variants resolve consistently; same-name counterexamples stay separate; ambiguity yields `unresolved`; merge two fixture suppliers, compute concentration, supersede the merge, and verify the concentration and its evidence package reproduce under the restored registry.

**Phase 3 — Hiring-footprint v1 and the investigation workspace.** The pivot-first workspace: Cipher saves the question and comparison population, executes pivots and bounded traversals, freezes cohorts with their supporting paths, inspects the source records behind each edge, and records hypotheses with alternatives and falsifiers, all as ledgered artifacts. §12 rules on canonical IDs; first generic findings exporter; neutral labels; every consequential claim carries its ClaimPackage. The v1 demonstration: two public-company targets (dev case + transfer test), deterministic pipeline (probe → preserve → type → resolve → project effective state → compare → find → receipt), no model dependency, clean network-disabled replay. The 15 acceptance gates (§1) are the exit gate. **First usable milestone.**

**Phase 4 — Defensible timing.** §14, with selective temporality. Exit gate: deterministic reruns reproduce; seasonal counterexamples do not auto-flag; start dates are never labeled award dates; a June-received correction with January effective time does not alter a March knowledge-time result.

**Phase 5 — Cipher operation and documents.** Inbox/outbox assistance contracts; text extraction + OCR with page/span refs and quality indicators; schema-constrained model proposals with deterministic validation plus semantic checks; final report generated from validated findings. Exit gate: a second investigation runs on a newly promoted adapter with zero core edits; a structured-data case completes with model access disabled; at least one mechanism has earned core promotion on the two-case rule, or the journal records why nothing qualified.

**Promotion queue (not phases):** procurement investigation, DOL H-1B adapter, USASpending adapter, SAM.gov adapter, first-party sitemap/RSS/JSON-LD adapter, Watch type with temporal predicates, `Person` and `CompensationObservation` ontology entities. Promotion requires the two-case rule: a mechanism enters the core only after demonstrating its use across two distinct investigations.

**Cross-cutting stale rule.** Any artifact whose dependencies changed — source version, registry version, rule version, case configuration, expectation version — is stale until recomputed or explicitly revalidated. Stale artifacts are never served as current. This rule sits above all phase gates.

## 16. Acceptance fixtures and tests

The Phase 0 synthetic fixture is the standing acceptance suite, extended per phase: alias resolution, same-name counterexamples, duplicate/amendment handling, missing-date behavior, distinct-donor counting (rows ≠ donors), 204-type record quarantine, red-flag schema stability (one writer per artifact), begin-date/award-date separation, seed-deterministic reruns, fixture-mutation sensitivity (change a record → the finding changes). v1.2 fixture additions: a seven-way absence fixture (one fixture row per acquisition state, asserting the correct absence semantics); an expectation-version change that invalidates prior SourceChecks without deleting them; merge → compute → supersede → verify concentration reproduces; a DRIFTED surface that loses authority visibly; a traversal that must not entail its suggested claim (non-entailment fixture); a presentation that must recompute its ceiling when evidence is added; a Tier-4 metadata-only fixture (exposure recorded from index metadata, no content touched). Regression tests pin every defect in §4. No AI-authored test suites — per Justin's standing rule, Gemini never authors tests; fixtures are hand-built, tests assert deterministic behavior.

## 17. Kill gates

- Any phase whose exit gate fails twice consecutively triggers a design review, not a third attempt with tweaks.
- If the deterministic core ever requires a model call to complete a run, the phase is failed — model assistance is optional by architecture.
- If adopted code cannot be tested against current behavior (no fixture exercises it), it is not adopted.
- If a second investigator cannot recompute a finding from the ledger + snapshots alone, the finding is KILLED, not downgraded.
- If a consequential claim's ClaimPackage cannot be reconstructed by a clean network-disabled process, the finding is KILLED.
- If any Tier-4 workflow downloads content, accesses an exposed service, or touches credentials, the workflow is KILLED and the incident is journaled.
- If a finding's acquisition truth is not terminal (any source at FETCH_INCOMPLETE / COVERAGE_INCOMPLETE / NOT_EVALUATED), the finding cannot rise above UNRESOLVED.
- Scope kill: graph DB, vector store, desktop UI, scheduler, recursive agent loops, and the sixteen killed expansions (§1) are out. Proposing them reopens this spec.

## 18. Open decisions

- Public name (UnSilo is the working project title only).
- Storage backend shape: SQLite + immutable files is the default; confirm before Phase 1.
- OCR engine for Phase 5 document handling.
- Whether the Boston reference case is worth reconstructing as a regression (inputs may be unavailable; optional either way).
- v1 target companies (Justin's call; dev case + transfer test).
- Whether `Person`/`CompensationObservation` promotion happens before or after the v1 demo.

Resolved since v1.1: first-investigation target (hiring footprint, not procurement); fetcher strategy (promote on demand, not take-all-12); universal MetricProof (two-tier evidence packages); typed commands (decision journal); BoundaryPolicy engine (per-source export flags); ledger hash chain (cut); bitemporality (selective); releases (git tags).

## 19. Migration sequence

1. This spec approved (SHA-256 receipted candidate; Justin's explicit build go still required separately).
2. New package scaffold in the workspace (not in the vendor dir); vendor stays read-only and unimported.
3. Phase 0 schemas + fixture land first; everything downstream builds against them.
4. Adopted code is copied file-by-file, hashed at copy time, and tested against current behavior before the original is referenced.
5. Each phase merges only on its exit gate; the ledger records every phase's inputs, code version, and outputs.
6. Phase merges are git-tagged; a failed exit gate rolls back to the last good tag, never forward-fixes in place.

## 20. What the 16-drill gauntlet changed, ranked

From the September 30, 2026 Sol gauntlet (16 drills, 4 waves, ChatGPT Chat surface, GPT-5.6 Sol, UnSilo project). Ordered by value divided by effort; every item is a concrete delta against v1.1:

1. Acquisition-truth objects (Expectation, SourceCheck, NegativeObservation, TraversalState) — the layer that makes "everything claimed is evidence-backed" executable.
2. Explicit acquisition state machine with seven-way absence semantics — absence becomes data instead of a hole.
3. Executable source contracts (identity/enumeration/temporal/boundary clauses) — the wiki template grows teeth.
4. Deterministic expectedness and applicability predicates — expectations apply by computation, never by assumption.
5. Career ontology as fixed vocabulary — scope discipline becomes a schema, not a memo.
6. Pivot algebra — traversal becomes a closed set of deterministic functions; the workspace goes pivot-first.
7. Deterministic lexical text retrieval — no vector store, no embeddings in the core.
8. Declared analytical grain as a physical invariant — every metric carries its grain or it doesn't exist.
9. Typed analytical values as physical invariants — money, dates, counts with types enforced, not documented.
10. Effective identity state — "current entities" is always a projection at a declared registry version.
11. Selective temporal projections — observation time everywhere, effective time only where asserted; universal bitemporality cut.
12. Transitive staleness — membership changes propagate invalidation to every dependent artifact.
13. Traversal non-entailment + claim-scope ceilings — paths suggest, evidence licenses.
14. Presentation monotonicity — adding evidence recomputes ceilings, never silently strengthens.
15. MetricProof downgraded to two-tier evidence packages — ordinary results get receipts, consequential claims get closed packages.
16. Typed command/event-sourcing cut → append-only decision journal.
17. Generalized BoundaryPolicy cut → per-source export flags.
18. v1 watches, property-projection machinery, and ledger hash-chain cut or deferred.
19. "Take all 12 fetchers" replaced by promote-on-demand adapters; v1 ships 3.
20. Reusable deterministic investigation recipes — the hiring-footprint recipe is the first; procurement must earn its own.

Palantir provenance (condensed): the v1.1 Palantir-derived additions (saved cohorts, MetricProof, reversible resolution, watches, bitemporality) came from the Astra public-source research pass (`hidden_files/astra-palantir-research-2026-09-30.md`). The gauntlet kept the ideas and cut the enterprise machinery: saved cohorts survive as SavedQuery + decision journal; MetricProof survives as the two-tier evidence package; reversible resolution survives as versioned MembershipDecisions; watches are deferred to the promotion queue; bitemporality is selective. Palantir-derived factual claims remain public-source research, not primary-verified — marked as such wherever they constrain the design.

---

*Provenance: v1.0 synthesized 2026-09-30 from Astra (GPT-6) roadmap, Gemini 3.8 Flash identification pass, and Codex (gpt-5.5) identification pass, every load-bearing claim verified by Cipher against `~/workspace/vendor/openplanter/` bytes at the cited file:line. v1.1 folded in the Astra Palantir deep-research pass (public sources only). v1.2 folds in the 16-drill Sol gauntlet (2026-09-30, ChatGPT Chat surface, GPT-5.6 Sol, UnSilo project), the adjudicated 16-finding type-safety review, the false-conviction red team, the 6-tier research-surfaces baseline (`files/unsilo-research-surfaces-2026-09-30.md`), and the six per-tier methodology drills (17–22, §7.6). Model agreement was treated as corroboration throughout; repo bytes and executed checks were the authority. Tier-4 policy is absolute: exposure metadata only, never download, never access, never authenticate.*
