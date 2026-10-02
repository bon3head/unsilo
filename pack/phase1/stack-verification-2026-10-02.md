# UnSilo stack and integration verification (2026-10-02)

Experiments, not a build. The scripts in `pack/phase1/lab/` are verification artifacts, not product code. Nothing in the baseline changed. Build authorization: NONE.

## 0. Blockers (lead)

Unchanged. FROZEN B2, B3, B4, B7, B8. REPAIRED-PENDING-ADMISSION B1, B9. OPEN B10 (quarantined). RETAINED-INTEGRATION-VERIFIED B5, B6. RETAINED B11, B12. RECON-ECLASS UNADMITTED.

This pass closes decision D-1 (stack) on evidence and records the license posture. It does not move any blocker.

## 1. License posture: recorded

Operator's text, as pasted in this session on 2026-10-02 (quoted as received; the paste ends mid-sentence):

> "## License posture (Justin's call, 2026-09-30)
>
> Take whatever. Nothing leaves his possession, nothing is published or distributed — so the GPL's copyleft trigger (distribution) never fires. GPL items are no longer ideas-only; their code can be"

Also from this session (2026-10-02): "this code will never touch anything public or be distributed".

Effects:
- **Ruling recorded.** Licenses no longer gate any choice below. They were still read from the shipped files, so the record stays exact.
- **Pack text to amend.** The pack's "patterns only" lines need a matching edit, done on the operator's instruction, not by me.
- **Missing words.** The tail of the 9/30 sentence is not in hand. If the omitted words add a condition, this record is incomplete.

## 2. The battery: the same requirements, four languages, executed

Each requirement comes from a frozen or retained contract. Every cell was executed in this container on 2026-10-02 unless marked.

| Requirement (source) | Python: apsw 3.53.4.0 | Rust: rusqlite 0.40.2 `bundled,functions` | Node: better-sqlite3 13.0.3 / `node:sqlite` | Go: modernc.org/sqlite 1.60.1 |
|---|---|---|---|---|
| Pinned SQLite engine, recorded in the closure (B10 dependency class "SQLite build") | **3.53.4**, bundled in the wheel | **3.53.2** (published crate; git HEAD has 3.53.4) | better-sqlite3 **3.53.4**; `node:sqlite` **3.50.4** (tied to the Node build, not pinnable) | **3.53.4** |
| SHA-256 callable inside a trigger under `trusted_schema=OFF` (S6 + receipt check) | **PASS** (`flags=SQLITE_INNOCUOUS`) | **PASS** with `SQLITE_INNOCUOUS`; FAIL with deterministic only (`unsafe use of sha256_hex()`) | **FAIL** in both drivers (`unsafe use of sha256_hex()`); no innocuous option exists | **FAIL** (`unsafe use of sha256_hex()`); no innocuous registration API in the module source |
| Real migrations 0001 to 0004 + Duolingo fixture, `trusted_schema=OFF`, FK on | **PASS**: integrity ok, 0 FK violations, WAL | **PASS**: same | **PASS** (better-sqlite3): same | not run (FAIL above already disqualifies) |
| Honest states render as designed (4 claim rows UNRESOLVED + ABSTENTION) | **PASS** | **PASS** | **PASS** | not run |
| Canonical JSON key order = bytewise UTF-8 (B8 frozen snapshot hash) | **PASS** by default | **PASS** by default | **FAIL** by default (`a, U+1F600, U+FF61`); PASS with `Buffer.compare` | **PASS** by default |
| JS-rendered careers pages with network capture (S2: rendering is admissible observation) | **PASS**: Playwright 1.56.0 captured the XHR JSON body byte-identical to the served file; S4 exhaustion predicate evaluated on the captured bytes | no official Playwright; `playwright` crate last release 2022-08-20; `chromiumoxide` 0.9.1 is CDP-only, without HAR (not executed) | official Playwright (not executed here) | community `playwright-go` (not checked) |
| Default FK enforcement in the bundled build | OFF (read-back is load-bearing) | ON | ON (better-sqlite3) | not checked |
| Replay: rebuild core from receipt after-images | **PASS**: 30 rows, byte-identical canonical dump `97ee49a5...` | not run | not run | not run |
| Cold build cost | `pip install` seconds | 1 min 24 s release build | `npm install` seconds | seconds |

**Verdict.**
- **Two stacks qualify.** Only Python and Rust pass the in-trigger hash check under the frozen security setting.
- **Python wins on acquisition.** Of those two, only Python has official Playwright with HAR, which is what the S2 rendered-page evidence path needs.
- **Rust has a gap there.** A Rust system would need a second language for acquisition, or a hand-built CDP network capture.
- **Recommendation: Python, single language.** Confidence HIGH. Every deciding row is executed.
- **What would change my mind:** a hard requirement for a single static binary, or a measured performance limit. Neither exists for one operator.

## 3. Integration findings from running it

| # | Finding | Mechanism, observed | Design rule |
|---|---|---|---|
| G1 | apsw executes multi-statement SQL lazily | the migration stopped at `PRAGMA journal_mode=WAL` (it returns a row); `meta_migration` did not exist yet (`no such table`) | the migration runner drains every cursor (`.fetchall()`) and then asserts the expected objects exist |
| G2 | apsw's bundled build leaves foreign keys OFF | `pragma foreign_keys` read 0 on a fresh connection | set + read back on every connection (already S6); a startup gate fails closed if the read-back is not 1 |
| G3 | Playwright's version pins its browser build | Playwright 1.63.0 demanded build 1243; the container has 1194; 1.56.0 maps to 1194 (npm `playwright-core` `browsers.json`: 1.56.0 → chromium 1194 / 141.0.7390.37) | pin the Playwright version and the browser build together in the lockfile; record both in the closure |
| G4 | Python hash seed changes set iteration order | `PYTHONHASHSEED=1` vs `2` gave different orders | one canonical encoder: keys and sets sorted by UTF-8 bytes, strings NFC, floats refused; executed: identical bytes under seeds 1, 2, 3 (`9364b48f...`) |
| G5 | floats leak through `json.dumps` | `0.1 + 0.2` serialized as `0.30000000000000004` | the encoder raises on float; money and counts are integers (S6) |
| G6 | stdlib `sqlite3` cannot mark a function innocuous | trigger failed with `unsafe use of sha256hex()` | use apsw, never stdlib `sqlite3` |
| G7 | read-only reader + single writer works in WAL | the `mode=ro` connection's write raised `ReadOnlyError`; a reader inside a transaction kept its snapshot (3 rows) while the writer committed (4 rows) | S6 profile confirmed on the pinned engine; one writer thread, readers read-only |
| G8 | the after-hash trigger works on the real receipt table | a mismatched `after_sha256` was blocked; a correct one was accepted | adopt as a migration (proposal (f)); the function must be registered on every connection, otherwise every receipt insert fails, which fails closed |
| G9 | rendered DOM ≠ raw bytes | raw HTML lacked the JS-built list; the rendered DOM and HAR had it | evidence for a rendered surface = raw response + HAR (network bodies) + rendered DOM, each its own content-addressed object; the HAR JSON body is the publisher-direct record when it comes from the publisher's own endpoint |
| G10 | day-to-UTC lifting needs a pinned tz database | `tzdata` 2026.4 with the host tz path disabled gave exact ranges, 23-hour and 25-hour days included | pin `tzdata` and record its version in the closure |

## 4. The pinned v1 stack (proposal for ratification)

| Layer | Pin | Verified here | Why |
|---|---|---|---|
| Language | Python 3.11+ (3.11.15 tested) | yes | section 2 |
| Storage | apsw 3.53.4.0 (SQLite 3.53.4) | yes | pinned engine; innocuous functions; native async (`Connection.as_async` present) |
| Time zones | tzdata 2026.4 | yes | deterministic lifting |
| Rendered acquisition | Playwright 1.56.0 + Chromium build 1194 (141.0.7390.37) | yes | official, HAR capture |
| API acquisition | HTTP client with full receipts | no | open (G-open-1) |
| Web | Starlette 1.7.0 + Jinja2 3.1.6 | versions only (PyPI) | server-rendered |
| Client | htmx 2.0.11 vendored (0BSD) | npm `latest` | no build step |
| Charts | server-rendered SVG via Jinja2; uPlot 1.6.32 as a vendored fallback | sizes measured earlier | one implementation of UNKNOWN and B12 rendering |
| Canonical encoder | in-house, about 15 lines (`lab/canon.py`) | yes | B8 byte order, NFC, no float |

Removed by this choice:
- the Rust toolchain, musl, Axum, Askama, and askama_web;
- any Node build;
- Blueprint and React;
- a second canonical encoder.

## 5. What remains open after this pass

| ID | Open item | What closes it |
|---|---|---|
| G-open-1 | HTTP client for API sources (receipts need the redirect chain, every status, headers, timing) | pick at build; httpx 0.28.1 was last released 2024-12-06, which is the only reason it is not simply named |
| G-open-2 | Python 3.12+ behavior | rerun `lab/py_battery.py` on the target interpreter (the battery is the acceptance test) |
| G-open-3 | VM vs laptop parity | run the battery on both; identical outputs required |
| G-open-4 | Remainder of the 9/30 license sentence | the operator's local file |
| G-open-5 | Live acquisition behavior (rate limits, real ATS payloads) | the research-experiment charter, D-3 |

## 6. How to reproduce

From `pack/phase1/lab/`:

- **Python:** `pip install apsw==3.53.4.0`, then `python py_battery.py`. Also `python canon.py`, run under different `PYTHONHASHSEED` values.
- **HAR test:**
  1. `pip install playwright==1.56.0`.
  2. Serve the test site: `python -m http.server 8765 --bind 127.0.0.1 --directory site`.
  3. Run `PLAYWRIGHT_BROWSERS_PATH=<dir with chromium-1194> python har_test.py`.
- **Rust:** `cd rust && cargo run --release`.
- **Node:** `cd node && npm install better-sqlite3 && node battery.mjs`.
- **Go:** `cd go && go run .`.

Build authorization: NONE
