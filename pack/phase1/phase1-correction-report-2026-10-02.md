# UnSilo dashboard, Phase 1 correction report (2026-10-02)

Input to the operator's rerun, not its conclusion. Build authorization: NONE.

## Blockers (lead)

| Blocker | Falsifier | Owner |
|---|---|---|
| Research chain: FROZEN B2 B3 B4 B7 B8; REPAIRED-PENDING-ADMISSION B1 B9; OPEN B10; RETAINED-INTEGRATION-VERIFIED B5 B6; RETAINED B11 B12; RECON-ECLASS-PD-AO-DD-v2.0 UNADMITTED; build NONE | per master doc section 7 remediation sequence | harness program (not this session) |
| NEW, harness: the mirrored B1/B9 extraction in `pack/research-chain/` carries contamination deviations (b) and (c) | byte comparison of these files against the four retained extraction reports in task `browser-task:4b530c82-709f-4689-a576-12178d17259b` | operator |
| Dashboard: U-DASH-01 one file vs two (SQLite has no schemas inside one file) | operator ruling | operator |
| Dashboard: U-DASH-02 / U-DASH-08 receipt chain and receipt images | operator ruling | operator |
| Dashboard: U-DASH-07 real Duolingo packet format not in the pack | the file lands in the corpus | operator |
| Superhuman B4 Form D, B1 LinkedIn authwall, B3 interview loop | as in the feed spec | as in the feed spec |

## 1. Method

- Full read of all 31 files on `pack/unsilo-dashboard-pack-2026-10-02` (HEAD 0f942b2) and the 6 root-only files on `main`. Root `research-chain/s*.md` files are byte-identical to the pack mirror (`cmp`).
- Clones re-made this session; all 8 HEADs equal the session-3 recorded HEADs: worldmonitor 1ab4284, glance 372466c, wtf 2691919, perspective eec38ad, gatus 884f64d, axum f8b02f2, askama 8dbcdef, rusqlite 91f876c. No drift.
- Version truth from `git ls-remote --tags` and source files. Context7 consulted for rusqlite (bundled build, FTS5). Context7 was not consulted for axum, askama, or htmx: no API claim about them is made here, only version pins read from tags and manifests.
- Executed checks (SQLite 3.45.1 via Python) for every schema claim; see `schema/README.md` section 1.

## 2. Full-read proof: one non-obvious detail per document

| Document | Detail |
|---|---|
| `pack/unsilo-session-prompt-2026-10-02.md` | drops session 3's HEAD list but keeps "8/8 PASS"; the HEADs are only in the session-3 prompt |
| `pack/unsilo-session3-prompt-2026-10-02.md` | records both write paths failing: git push and the connector ("Resource not accessible by integration") |
| `pack/unsilo-master-architecture-prompt-2026-10-02.md` | directive 9 feasibility-checks against "TS/Python", which conflicts with the approved Rust stack (recorded, not resolved) |
| `pack/unsilo-claude-launch-prompt-2026-10-02.md` | describes the receipt ledger as "hash-chained"; the data theory says only before/after hashes |
| `pack/unsilo-continuation-report-2026-10-02.md` | gives the gate date as "DECIDED 2026-10-02-01", a malformed date |
| `pack/unsilo-feed-dashboard-spec-2026-10-02.md` | header spelled "UNISILO"; audit counts 9+31+188+127 = 355, not the stated 555 |
| `pack/unsilo-data-theory-2026-10-02.md` | orders absences by `expected_probability DESC`, a numeric probability |
| `pack/dashboard-crawl-report.md` | tabler bundles ApexCharts, which it notes is no longer MIT |
| `pack/language-shootout-2026-10-02.md` | sources "FTS5 on in bundled rusqlite" to a third-party ADR (julie), not to rusqlite itself |
| `pack/harness-build-spec-v1.2-2026-09-30.md` | cuts the ledger hash chain ("no adversary"); also has a Tier 5 (human sources) the dashboard spec omits |
| `pack/research-chain/triage-state-2026-10-01.md` | "B10 REPAIR COMPLETE ~4:42 AM" is logged after "B10 REPAIR LAUNCHED ~4:45 AM" |
| `pack/research-chain/authority-gate-decision-2026-10-01.md` | dated 2026-10-01 ~11:26 PM ET, yet Foundation v2, which records that decision, was authored 2026-10-01 ~2:06 AM ET |
| `pack/research-chain/repair-foundation-v2-2026-10-01.md` | the canonical digest appears 6 times; zeroing them reproduces `707269c9...310f` only with the trailing LF kept |
| `pack/research-chain/repair-foundation-artifacts-2026-10-01.md` | header says 2026-10-01 ~10:10 PM ET, after the v2 that supersedes it |
| `pack/research-chain/s1-output-2026-09-30.md` | the terminology map is partial; it points to a "full map in S1 text" (U-1R-AUTH-011) |
| `pack/research-chain/s2-output-2026-09-30.md` | EDGAR with no User-Agent returns a silent empty body |
| `pack/research-chain/s3-output-2026-09-30.md` | 81-signature overlap matrix with 80 cells UNKNOWN (the rule later found defective) |
| `pack/research-chain/s4-output-2026-09-30.md` | the Lever terminal rule is derived, not published by Lever |
| `pack/research-chain/s5-output-2026-09-30.md` | Schema.org JobPosting has no `department`; it has `employmentUnit` |
| `pack/research-chain/s6-output-2026-09-30.md` | `application_id` 0x554E534C ("UNSL"); `user_version=1` is physical generation, not S/V/C/R |
| `pack/research-chain/s7-output-2026-09-30.md` | the ChatGPT UI showed no model picker, so model identity was not verifiable |
| `pack/research-chain/s8-output-2026-09-30.md` | lists 6 folklore kills; the kill log lists 7 for S8 (#64 to #70) |
| `pack/research-chain/s9-output-2026-10-01.md` | a CIK reassigned to an unrelated company is NOT_COMPARABLE plus a registry-integrity anomaly |
| `pack/research-chain/s10-output-2026-10-01.md` | marks B1..B12 except B4 FROZEN; superseded by Foundation v2 |
| `pack/research-chain/part1-b1.md` | ABSENT and NULL must not hash identically |
| `pack/research-chain/part2-b9.md` | section 9.3: "Unknown bounds produce UNKNOWN_TEMPORAL_RELATION", the superseded S3 blanket rule (see CORRECTED C9) |
| `pack/research-chain/part3-crosswalk.md` | R-L4 maps to "RecordVersion comparison", which is not an operator in the B9 family registry |
| `pack/research-chain/part4-tail.md` | says `ORIGINALS_RECOVERED status: NO`; the program state is PARTIAL |
| `pack/research-chain/full-repair-output.txt` | exactly 46,227 bytes = parts 1 to 4 minus the `[PARTn-...]` markers; the Part 1 to 3 headers read "Build authorization: NONE." with a trailing period (lines 5, 457, 925) |
| `pack/research-chain/PROVISIONAL-b10-repair-output.txt` | lists the unadmitted RECON-ECLASS contract under "Depends on" |
| `pack/research-chain/PROVISIONAL-b10-acceptance-artifacts.txt` | receipt hashes are patterned (`cccc...`, `...ffeeddccbbaa9988`), and the golden finding `repeated_supplier_cohort.v1` is procurement, outside v1 |
| `pack/research-chain/s*` mirror vs root | byte-identical (10/10) |
| `README.md` (root) | still says B1..B12 FROZEN except B4; stale |
| `build-blockers-b1-b12-verbatim-2026-09-30.md` | B11's unblock includes "query lints" and a "money/unit model" |
| `research-chain-plan-2026-09-30.md` | promises `baseline-log` and `terminology-map` files that appear nowhere in the repo |
| `astra-final-approval-prompt-2026-10-01.md` | instructs reviewers that "7R gate B1/B2/B3/B9 cleared", later rejected |
| `research-chain/folklore-kill-log-2026-10-01.md` | kill #80 explicitly forbids a far-future date for UNBOUNDED |
| `research-chain/poc-results-2026-09-30.md` | P3's 256 combinations, 16 determinate, is the evidence the blanket rule rested on (now retired, U-1R-AUTH-014) |

## 3. CONFIRMED

| # | Claim | Evidence (opened this session) | Class |
|---|---|---|---|
| F1 | Foundation v2 canonical SHA-256 `707269c9...310f` | recomputed by the self-pin rule (6 occurrences zeroed, trailing LF kept); raw file SHA-256 `88e2c48e...f8c8` matches the ledger | DD |
| F2 | Foundation v1 SHA-256 `bbd4e240...b88e` | `sha256sum` | DD |
| F3 | B1/B9 repair output is 46,227 bytes | `wc -c full-repair-output.txt` | DD (but see C3) |
| F4 | Clone HEADs (8/8) unchanged since session 3 | fresh clones | DD |
| F5 | axum 0.8.9 is the latest 0.8 | tag `axum-v0.8.9`; `axum/Cargo.toml:3` | DD |
| F6 | askama 0.16.1 | tag `v0.16.1`; workspace `Cargo.toml:17` | DD |
| F7 | askama_web 0.16.0 with feature `axum-0.8`; askama_axum is not the path | tag `v0.16.0` in askama-rs/askama_web; `askama/book/src/frameworks.md:121` | DD |
| F8 | rusqlite 0.40.2 | tag `v0.40.2` exists (main `Cargo.toml:4` still reads 0.40.1; the release is on a tag) | DD |
| F9 | `bundled` compiles FTS5 | `libsqlite3-sys/build.rs:163` `-DSQLITE_ENABLE_FTS5`; Context7 rusqlite build.rs excerpt agrees | DD |
| F10 | tokio-rusqlite 0.8.0 latest | tag `v0.8.0` | DD |
| F11 | htmx 2.0.11 is the latest 2.x | tag `v2.0.11`, commit dated 2026-09-22, package.json 2.0.11 | DD |
| F12 | bundled SQLite meets the S6 floor (>= 3.37.0) | `sqlite3.c:470` `3.53.4` | DD |
| F13 | STRICT, FK readback, integrity gates, FTS5 rebuild all work as S6 describes | executed, `schema/README.md` 1 | DD |
| F14 | Rust pick holds on B4 grounds, with the caveat in the B4 judgment doc proposal (a) | no new evidence moves the shootout ranking | WEAK (shootout benchmark numbers not re-verified) |

## 4. CORRECTED

| # | Old | New | Evidence |
|---|---|---|---|
| C1 | "htmx 2.0.11 (4.x does not exist)" | htmx 4.0.0 exists: tag `v4.0.0` at 4195bc0, commit dated 2026-08-28, package.json `4.0.0`. 2.0.11 remains a defensible pin (newest 2.x, 2026-09-22) but the reason must be "stay on 2.x", not "4.x does not exist". Whether 4.0.0 is a GitHub Release or npm `latest` is not established. | `git ls-remote`, tag checkout |
| C2 | "One SQLite file, two schemas (staging, core)" | Not implementable: a SQLite schema name is an attached file. Proposed: one file, table-name namespaces. | executed: `unknown database staging`; cross-db FK fails to parse |
| C3 | Master doc 7: the extracted B1/B9 repair output "stands as a valid repair candidate" | The mirrored extraction carries deviation (c) (`part4-tail.md:92` "NONE evaluated.") and deviation (b) (B9 open-thread line at `part4-tail.md:75` lacks "blocker/completion impact"; the B1 line at :74 has it). These files must not be the source for remediation step 6. Deviation (a) cannot be checked without the originals. | `grep` on `part4-tail.md` and `full-repair-output.txt` |
| C4 | Interval markers "Timestamp / UnboundedFuture / Unknown" | Frozen B4 needs UNBOUNDED at either endpoint (ledger Case S3-1 uses an UNBOUNDED start) plus per-value granularity. A future-only marker cannot express it. | ledger 2:24 AM entry; S3 |
| C5 | `ORDER BY expected_probability DESC` | categorical basis rank; numeric probability violates the standing rule | README; master doc 3 |
| C6 | Receipts = before/after hashes; repair = replay | a hash cannot be replayed; receipts need the after-image | mechanism |
| C7 | blocker status open/closed | the true research-chain states need the full vocabulary (FROZEN, REPAIRED-PENDING-ADMISSION, RETAINED, ...) | master doc 10 |
| C8 | S8 digest "Folklore killed (6)" | the kill log lists 7 for S8; the 84 total depends on 7 | kill log #64 to #70 |
| C9 | B9 contract (harness, pending admission) section 9.3 and typing matrix | "Unknown bounds produce UNKNOWN_TEMPORAL_RELATION" restates the superseded S3 rule; `EFFECTIVE_ELIGIBLE` returns bound kinds (KNOWN/UNKNOWN/UNBOUNDED) as truth states. Both conflict with frozen B4. Recorded for the fresh B1/B9 admission; not this session's to repair. | `part2-b9.md` 9.1, 9.3, 17 |
| C10 | B1 crosswalk R-L4 | "RecordVersion comparison" is not a defined operator; under Foundation v2 B1 criteria that is undefined syntax | `part3-crosswalk.md` R-L4 |
| C11 | Superhuman blockers named "B1, B3, B4" | collide with research-chain B1..B12; identity must be (program, code) | feed spec |
| C12 | Shootout cites a third party for bundled FTS5 | primary source now: `build.rs:163` | F9 |

## 5. OPEN

| # | Unknown | Falsifier / source that closes it |
|---|---|---|
| O1 | Timestamps: ledger header "~10:53 PM", Foundation v1 "~10:10 PM", gate decision "~11:26 PM", all labeled 2026-10-01, precede Oct 1 early-morning entries that depend on them. Likely 2026-09-30 evening. | operator memory file `~/memory/2026-10-01.md` or chat timestamps |
| O2 | Ledger erratum not yet appended (remediation step 1) | the erratum line in `triage-state` |
| O3 | Palantir "Three numbers 2/8/5" meaning | operator |
| O4 | Datadog "job 8052118 / req R20978": which is the platform req ID | the posting |
| O5 | Audit 555 vs 355 | audit export |
| O6 | "Proven: 2.67 MB static-pie musl binary, FTS5 working, 1 min 14 s cold build" came from a reclaimed container | rebuild a hello-world Axum+rusqlite musl binary (Phase 2 gate) |
| O7 | Shootout efficiency numbers (RSS, binary sizes, toolchain sizes) | each cited benchmark opened; not done this session (WEAK) |
| O8 | Crawl star counts on 2026-10-02 | GitHub API; not re-fetched this session |
| O9 | B4 dense vs discrete completions; cross-granularity lifting | frozen oracle text, chat 6abdfc6f |
| O10 | U-DASH-01 to U-DASH-14 | `schema/README.md` 9 |

## 6. Prior-art patterns, confirmed at file and line (HEADs in section 1)

| Pattern | Repo, file:line | License (read from the file) |
|---|---|---|
| Config-driven UI: page, columns, widgets declared in YAML | glance `internal/glance/config.go:77-91` (`page` struct; `Columns []struct{ Widgets widgets yaml:"widgets" }`) | AGPL-3.0 (`LICENSE`): pattern only |
| Widget failure isolation and per-widget cache | glance `internal/glance/widget.go:283-322` (`withError`, `canContinueUpdateAfterHandlingErr`); cache duration `:163`, `:263-265` | AGPL-3.0 |
| Module registry with per-module refresh | wtf `app/widget_maker.go:98` (`MakeWidget` switch over module names); `app/scheduler.go:11-26` (per-widget `RefreshInterval` loop) | MPL-2.0 (`LICENSE.md`) |
| Per-panel staleness | worldmonitor `src/components/Panel.ts:13-14, 113-115, 229-230` (freshness badge); `src/services/panel-freshness-display.ts:12-13` (`stale`, `very_stale`) | AGPL-3.0: pattern only |
| Severity pills | worldmonitor `src/components/CountryDeepDivePanel.ts:496, 3658` (`cdp-severity-badge sev-*`) | AGPL-3.0 |
| Toggleable layers | worldmonitor `src/components/Map.ts:4266` (`toggleLayer`) | AGPL-3.0 |
| Probe-history strip | gatus `web/app/src/components/EndpointCard.vue:38-44` (one segment per result, colored by `success`), `:110-114` (padded to `maxResults`) | Apache-2.0 |
| Per-condition results stored in SQLite | gatus `storage/store/sql/specific_sqlite.go:76-81` (`endpoint_result_conditions`) | Apache-2.0 |
| Condition DSL | gatus `config/endpoint/condition.go:37` (`evaluate`); `placeholder.go:17` (`[STATUS]`) | Apache-2.0 |
| View compiles to SQL | perspective `rust/perspective-client/src/rust/virtual_server/generic_sql_model/table_make_view.rs:408-415` (`build_query` emits `SELECT ... FROM ...`) | Apache-2.0 (`LICENSE.md`) |

Other licenses read: axum MIT (`LICENSE`), askama MIT or Apache-2.0 (`LICENSE-MIT`, `LICENSE-APACHE`), rusqlite MIT (`LICENSE`). All match the crawl report. No code was copied; the schema reimplements none of these files.

Not confirmed: "verdict pills" in worldmonitor as CONFIRMED/KILLED-style verdicts. Its pills are severity badges. The pattern (categorical pill as primary grammar) holds; the vocabulary is ours.

## 7. Conflicts recorded, not resolved

1. Master doc directive 9 (TS/Python stack) vs approved Rust baseline. Master doc wins by the stated hierarchy, but the baseline changes only on the operator's ruling. Needs a ruling.
2. Launch prompt "hash-chained" vs harness v1.2 "hash chain cut" vs data theory silent. Schema chains; U-DASH-02.
3. Master doc 7 "extracted output is a valid candidate" vs the contamination markers in the extraction (C3).
4. Session prompt 2.10 asks the DDL to conform to frozen B4, which mandates per-endpoint tri-state and three-valued evaluation, while section 4 says implement none of the parked proposals. Where the frozen contract itself mandates a mechanism, the schema implements it on the contract's authority and says so (B4 judgment doc).

## 8. What I need from the operator before Phase 2

1. Rulings U-DASH-01, 02, 05, 06, 08, 09, 10, 11, 12.
2. The real Duolingo packet file (U-DASH-07).
3. Rulings on parked proposals (a) to (g), per the B4 judgment doc.
4. Confirmation that the schema may be committed as the approved baseline after the rerun, or the list of changes.

Build authorization: NONE
