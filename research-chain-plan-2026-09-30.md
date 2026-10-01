# UnSilo v1 research chain — 10 sequential Sol sessions

Launched 2026-09-30 ~6:46 PM ET per Justin: "scope everything... launch 10 separate sol
sessions that build off the last until you have the actionable confirmed research baseline
without these folklore claims and aspirations."

## Chain rules (every session)

- v1 scope ONLY. v1 = Public Recruiting State: "deterministically reconstructs and compares
  a company's publicly observable recruiting state across time from public records, with
  declared evidence scopes and coverage qualification." Dream (dossiers, person recon,
  money graphs, writeback, analytic technique, surveillance) is out; label DREAM and exclude.
- Trust Sol. Primary sources for every factual claim (URL + section). No source = UNVERIFIED.
- Folklore purge: unsourced claims and aspirations killed on sight, kept in a kill log.
- Jargon purge: replace project jargon with proper standard terminology (name the standard);
  formal definition where no standard term exists. Maintain a running terminology map.
- Blockers lead: B1–B12 gate everything. Safe frontier: Layers 1–5 buildable now (fenced);
  Layers 7–8 stop line until 7R passes.
- Each session ends with: CONFIRMED FINDINGS (sourced), KILLED FOLKLORE, OPEN UNKNOWNS,
  BASELINE DELTA (tight bullets appended to the running log).
- Effort: high. Fresh chat per session in the UnSilo project, GPT-5.6 Sol, verified before send.
- PoCs (local, parallel): short testable claims get executed immediately — CDX/EDGAR probes,
  temporal bound algebra, SQLite adversarial fixtures. Results feed the sessions.

## Sessions

- S1: v1 claim & scope freeze. Formalize the claim in standards language; exact non-claims;
  acceptance question corpus mapped to surfaces; terminology map; scope ambiguities resolved
  or marked UNKNOWN. No architecture.
- S2: acquisition surfaces, confirmed. Per surface (SEC EDGAR, first-party careers, Wayback
  CDX): exact endpoints, rate limits, ToS/robots constraints, enumeration + pagination
  mechanics, what "complete" means. Primary docs only. (Feeds on PoC: CDX + EDGAR probes.)
- S3: temporal semantics (B4). Frozen bound representation {KNOWN, UNBOUNDED, UNKNOWN},
  [from,to) algebra, bitemporal mapping (SQL:2011 / Snodgrass), fixtures for all combinations.
  (Feeds on PoC: bound algebra implementation.)
- S4: completeness & negative evidence (B5+B6). Executable completeness proof per surface;
  admission rules/constructors for negative claims; dangerous-default analysis.
- S5: ontology & registry (B7+B8). Ontology versioning contract (serialization, upcasters);
  snapshot materialization; cannot-link closure; judgment model in record-linkage terms.
- S6: SQLite safety (B11). Adjudicated hazard list, frozen policy, adversarial fixture specs.
  (Feeds on PoC: real SQLite adversarial runs.)
- S7: closure & presentation (B10+B12). The 12 closure assertions formalized; lifecycle
  BUILDING→SEALED→VERIFIED in W3C PROV terms; counterevidence render contract.
- S8: query AST & operators (B1+B9; 7R core). Canonical versioned QueryDefinition AST
  (serialization, hash, compiler version); operator type system; golden AST→SQL fixtures.
  Research-only, paper prototype.
- S9: cohort & comparison (B2+B3; 7R remainder). Compatibility predicate; four-way drift
  decomposition; UNKNOWN/incomparable contract; v1-scoped comparison (machinery pinned).
- S10: v1 spec assembly & validation. Synthesize S1–S9 into the Sol-validated v1 spec:
  full sources, acceptance gates, explicit unknowns, folklore purge log. Final adversarial
  validation pass — Sol signs or lists blocking findings.

## Outputs

- Per session: `hidden_files/research-chain/sN-output-2026-09-30.md`
- Running log: `hidden_files/research-chain/baseline-log-2026-09-30.md`
- Folklore kills: `hidden_files/research-chain/folklore-kill-log-2026-09-30.md`
- Terminology map: `hidden_files/research-chain/terminology-map-2026-09-30.md`
- Final: Sol-validated v1 spec (S10 output)
