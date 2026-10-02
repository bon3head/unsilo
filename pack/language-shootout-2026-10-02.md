# Language shootout: Rust vs Go vs Zig for the UnSilo intel dashboard (2026-10-02)

Theory and comparison only. No implementation. Claude implements from the winner's
one-liner in section 7.

Evaluated strictly against two specs:
- `files/unsilo-feed-dashboard-spec-2026-10-02.md` (single dark page, blockers
  head+tail, 7 application cards, filterable/searchable feed, surfaces catalog,
  no em dashes, 12-hour AM/PM ET, every number verbatim)
- `files/unsilo-data-theory-2026-10-02.md` (SQLite-first single file,
  staging->core promotion, FTS5 search, WAL, bitemporal valid_time/transaction_time,
  Allen-interval discipline with explicit UNBOUNDED_FUTURE/UNKNOWN markers instead
  of overloaded NULL, append-only hash-chained receipt ledger, deterministic
  feed_item VIEW ordered by (event_time, id), single static binary, no runtime,
  local-first single operator on Bluefin laptop + small Linux VM)

Baseline to beat (not a candidate): Bun/TS. Justin's default for quick scripts.
`bun:sqlite` is a capable built-in SQLite, but the runtime ships ~30MB+ resident
and the task explicitly says "super efficient language", so Bun is the floor,
not a contender.

## 1. Rust

### Efficiency profile (sourced)
- Idle RSS: ~3.6MB baseline for an Axum hello-world (nilo cross-framework
  comparison, 2026); weighted peak RSS 7.36MB for a SQLite-backed CRUD API on
  Pi 5 (Zenodo pilot benchmark, Oliveira 2026), best throughput-per-MB measured
  at 310 req/s/MB, 2.8x Go.
- Under load: Axum max RSS 12.1MB at ~769k req/s (programatik29 rust-web-benchmarks).
- Startup: instant, sub-10ms typical; cold start ~291ms in the Coolify sentinel
  bench (vs Go ~313ms).
- Binary: 5-15MB stripped for a simple web server (dingjiu1989-hue comparison);
  down to <6MB with LTO + opt-level=z + strip (hive-sync, Axum+tokio WebSocket relay,
  idles ~10MB RAM).
- What drives it: no GC, no runtime, monomorphization bloats binaries (each
  generic instantiation is a code copy) while keeping RSS tiny.

### Dashboard/web ecosystem
- Idiomatic pick for THIS spec: Axum 0.8 + Askama (compile-time-checked templates)
  + htmx + vendored CSS. Server-rendered, no WASM pipeline, no Node build step.
  Askama catches template errors at compile time; htmx gives filter chips and
  search-box partial updates without client state.
- Leptos 0.8 (SSR + hydration) exists and is production-used, but it drags a
  WASM/cargo-leptos pipeline and 150-300KB WASM output for a page that the spec
  defines as server-rendered tables. Rejected for this build: wrong tool for a
  read-mostly dense dashboard.
- Maturity: Axum is the default Rust web framework in 2026 (crates.io backend
  itself runs on it); tower middleware ecosystem is deep. Who uses it: crates.io,
  Cloudflare-adjacent tooling, countless self-hosted dashboards.

### SQLite story
- rusqlite 0.31+ with `bundled` feature: statically compiles the SQLite
  amalgamation, no system dependency. FTS5 enabled in the bundled build by
  default (verified in the julie project's ADR: SQLITE_ENABLE_FTS5 on, plus
  trigram tokenizer and porter unicode61).
- WAL via PRAGMA journal_mode=WAL; foreign_keys=ON; busy_timeout; all standard.
- Ergonomics: synchronous API with excellent prepared-statement ergonomics
  (named params, query_row/query_map, transactions). The wrinkle: Axum is async
  (tokio) and rusqlite is blocking, so DB access goes through spawn_blocking or
  tokio-rusqlite. For a single-operator dashboard this is a solved papercut, not
  a blocker, but it is the one place the stack fights itself.
- Connection pooling: r2d2_sqlite or deadpool; single writer is trivially enforced.

### Build/deploy for one operator
- `cargo build --release`; cross-compile via rustup target. Same-distro x86_64
  (Bluefin -> Ubuntu VM): trivial, links glibc dynamically.
- TRUE static binary needs x86_64-unknown-linux-musl + musl-tools installed;
  rusqlite bundled compiles its C amalgamation under musl fine. This is the one
  extra setup step vs Go/Zig.
- Toolchain is heavy: ~1.7GB + ~/.cargo (mc toolchain comparison). Cold builds
  take minutes. Incremental rebuilds are seconds.

### Honest weaknesses for THIS use case
- Iteration speed: compile times and borrow-checker friction are the real tax
  on a dashboard Justin will reshape weekly. Rust punishes exploratory UI work.
- Async/sync seam at the DB layer (above).
- 1.7GB toolchain on the laptop; fine on Bluefin, noisy on a small VM if he ever
  builds there.

## 2. Go

### Efficiency profile (sourced)
- Binary: ~7.6MB for stdlib net/http hello-world (dev.to benchmark suite,
  Go 1.24); ~9.4-9.8MB stripped for a real app with templates+markdown (mdblog
  investigation: .text 4.2MB, .gopclntab 3.5MB, plus a 32MB FIPS DRBG pool in
  Go 1.26 BSS at startup that cannot be disabled).
- Idle RSS: ~7.7MB baseline net/http (nilo comparison); ~31MB for a real service
  with embedded console (model-router bench); 19,897 bytes per idle connection.
- Startup: 17ms cold start to /healthz (model-router bench).
- What drives it: the GC + goroutine scheduler are a fixed floor (~7MB) that
  Rust and Zig do not pay; per-connection cost is ~20KB (goroutine stacks).

### Dashboard/web ecosystem
- Idiomatic pick: stdlib net/http (1.22+ routing is enough) or Chi + Templ +
  htmx. Templ (a-h/templ, active since 2023) is type-safe, compile-time-checked
  templates: the Go analogue of Askama, and the community has converged on
  templ+htmx as the server-rendered dashboard pattern (multiple 2026 ADRs).
- sqlc for type-safe SQL is optional; database/sql is fine at this scale.
- Maturity: net/http is decades-battle-tested; Templ is newer (2023+) but
  adopted and stable. Who uses it: the entire Go self-hosted dashboard world;
  Chi/Echo routers are boring and reliable.

### SQLite story (the one real decision in Go)
- Two drivers, genuine tradeoff, pick ONE:
  - mattn/go-sqlite3: cgo wrapping real SQLite C. Fastest (2.0-2.3x faster than
    modernc on read-heavy scans, 1.3x on prepared lookups; CoreScope head-to-head
    on 11M-row production DB). Binary ~3.6MB stripped. Cost: CGO_ENABLED=1,
    needs a C toolchain for the target; cross-compile is annoying (zig cc is the
    known workaround).
  - modernc.org/sqlite: pure Go, mechanical C-to-Go translation. Trivial
    cross-compile (GOOS/GOARCH just works), no toolchain. Cost: 10-25% slower on
    writes, up to ~2x slower on heavy read scans; binary ~6.3MB stripped;
    requires Go 1.25+.
- Both are full SQLite: FTS5, WAL, foreign keys all work. DSN pragmas
  (_journal_mode=WAL&_busy_timeout=5000&_foreign_keys=true) or PRAGMAs.
- database/sql pool footgun: default pool settings + SQLite writes = "database
  is locked" surprises. Fix is known: SetMaxOpenConns(1) or a single
  mutex-guarded writer, WAL mode, busy_timeout. Document it in the build; it
  bites every Go+SQLite project once.
- For THIS workload (single operator, feed queries over thousands of rows, not
  millions), the modernc perf gap is unmeasurable. The driver choice is really
  "do you want trivial cross-compile or maximum headroom".

### Build/deploy for one operator
- Best in class with modernc: `GOOS=linux GOARCH=amd64 go build` from Bluefin,
  one static binary, no toolchain beyond Go itself (~258MB toolchain).
- With mattn: needs CGO toolchain for the target; same-distro x86_64 is fine
  (gcc present), cross-arch is not.

### Honest weaknesses for THIS use case
- The B4 lesson (UNBOUNDED/UNKNOWN markers vs overloaded NULL) wants sum types.
  Go has no enums-as-ADTs: interval endpoints become string markers or custom
  types with runtime validation. The schema can still enforce it (CHECK
  constraints), but the compiler will not catch a misuse the way Rust's enum
  would. This is Go's single biggest spec-fit gap.
- GC floor (~7MB RSS) is 2x Rust's; irrelevant at this scale, but it is why Go
  loses "super efficient" on paper.
- Templ adds a `templ generate` codegen step to the build.

## 3. Zig

### Efficiency profile (sourced)
- Binary: 829KB for a zap web server vs 84.8MB Rust actix in one head-to-head
  (cppdozer; note the Rust binary was unstripped/debug, so treat the ratio with
  skepticism, but the Zig absolute number is real). Minimal Zig HTTP server:
  200-400KB stripped (dingjiu1989-hue comparison).
- Idle RSS: ~1MB for std.http.Server; zap ~6MB idle, 85MB at 10k connections
  (penchef 2026 bench). http.zig: 11.5MB baseline, 11,218 bytes/idle connection
  (nilo comparison).
- Startup: sub-millisecond to ~20ms.
- What drives it: no runtime, no GC, no monomorphization bloat, aggressive
  dead-code elimination at comptime. The efficiency winner on every absolute
  number.

### Dashboard/web ecosystem (the problem area)
- HTTP servers: http.zig (karlseguin, pure Zig, thread-pool, explicit buffer
  config) or zap (thin wrapper over C facil.io: fast, but a "debugging cliff"
  if a segfault crosses the C boundary; the Zig community itself flags this).
- Templating: NOTHING at the Askama/Templ level exists. Dashboard HTML is
  hand-rolled via std.fmt / custom writer code. For dense tables + filter chips
  + search partials, that is real toil with no component model and no
  compile-time template checking.
- Who actually uses it: small self-hosted projects (stardust monitoring uses
  zap + a React frontend, i.e. Zig serves JSON while TypeScript does the UI).
  No production dashboard with a Zig-rendered dense UI was found in the survey.
- htmx pairs fine with any server renderer, but the renderer itself is the gap.

### SQLite story
- karlseguin/zqlite.zig: C wrapper bundling real SQLite 3.53.0, statically
  linked, +682-808KB measured. 190 stars, maintained, proven API
  (exec/row/rows/changes/busyTimeout). FTS5 and WAL come from the real C
  library, so they work exactly as documented.
- ghostkellz/zqlite is a PURE-Zig SQLite reimplementation with its OWN file
  format: it cannot read real .db files. REJECTED for this spec (the data
  theory requires real SQLite files, FTS5 virtual tables, WAL).
- Honest note: Zig's viable SQLite story is a C wrapper, not Zig code. It
  satisfies every spec constraint functionally (single static binary, FTS5,
  WAL), but "super efficient language" purity takes a dent: the DB layer is C.
- Prepared-statement lifecycle is manual (bind/execute/reset/reuse); correct but
  verbose vs rusqlite.

### Build/deploy for one operator
- Best in class: `zig build -Dtarget=x86_64-linux-musl` from Bluefin, one
  static binary, no toolchain beyond Zig itself (~246MB). Cross-compile is a
  first-class feature, not an afterthought.

### Honest weaknesses for THIS use case
- No mature server-side templating: hand-rolled HTML for the whole dashboard.
  This is the dominant cost, larger than any efficiency win at this scale.
- Allocator ceremony: every function takes an allocator; fast iteration suffers
  and Claude has fewer training examples of idiomatic http.zig+zqlite code than
  of Axum or net/http patterns.
- 0.x churn: Zig is pre-1.0 (0.15/0.16 in 2026); libraries track releases but
  breaking changes happen. karlseguin is current today; pin it.
- Explicit error sets and manual memory management are great for efficiency and
  slow for dashboard velocity.

## 4. Spec-constraint scorecard

Constraint order follows the data-theory spec.

| Spec constraint | Rust | Go | Zig |
|---|---|---|---|
| Single SQLite file, FTS5 + WAL | rusqlite bundled: FTS5 on by default, WAL via PRAGMA. Cleanest story. | modernc or mattn: full SQLite, FTS5+WAL fine. Pool config must be set deliberately. | karlseguin/zqlite.zig bundles real SQLite 3.53: FTS5+WAL fine. C wrapper, not pure Zig. |
| Single static binary, no runtime | Yes via musl target (extra setup: musl-tools). gnu target links glibc (fine on the Ubuntu VM, not strictly static). | Yes, trivially with modernc. With mattn, cgo complicates it. | Yes, trivially. `zig build -Dtarget=...-musl`. Cleanest. |
| Local-first, single operator, Bluefin + Linux VM | Cargo workspace, fine. 1.7GB toolchain. | Go toolchain 258MB, trivial cross-compile. | Zig toolchain 246MB, trivial cross-compile. |
| Deterministic feed (ORDER BY event_time, id; no bare LIMIT) | Trivial. | Trivial. | Trivial. |
| Bitemporal intervals; UNBOUNDED_FUTURE/UNKNOWN as explicit markers, never overloaded NULL (the B4 lesson) | STRONGEST FIT: `enum Endpoint { Timestamp(i64), UnboundedFuture, Unknown }` makes the B4 bug unrepresentable at compile time. | Weakest: no sum types; markers become strings/consts with runtime checks. Schema CHECK constraints carry the enforcement instead. | Strong: tagged unions express it exactly. More manual code than Rust. |
| Append-only receipt ledger (receipt row BEFORE mutation, same tx) | rusqlite sync transactions: ergonomic, exact. | database/sql Tx: fine. Single-writer discipline required. | Manual tx control: fine, verbose. |
| Staging->core promotion, forward-only migrations, schema_version | Any migration runner; refinery or hand-rolled. | Hand-rolled migrator (schema_migrations table) is the idiom; golang-migrate exists. | Hand-rolled. |
| Dense tables, FTS5 search box, filter chips | Axum + Askama + htmx: mature, compile-time templates. | net/http/Chi + Templ + htmx: the converged Go dashboard pattern. | Hand-rolled HTML via std.fmt. No component story. Weakest. |
| 12-hour AM/PM ET rendering | chrono + chrono-tz. | time package + tzdata import (must embed tzdata for static binary). | std.time, manual formatting. All fine. |
| SHA-256 artifact hashing | std-adjacent (sha2 crate). | crypto/sha256 stdlib. | std.crypto. All fine. |

Kill criteria (what would disqualify each option for THIS spec):
- Rust is KILLED if: iteration velocity dominates the decision (Justin reshaping
  the dashboard weekly; multi-minute cold builds + borrow-checker friction tax
  every change), or the tokio/rusqlite sync-async seam becomes a bug source.
- Go is KILLED if: the B4 interval-marker discipline must be compiler-enforced
  rather than schema-enforced (Go cannot express it as a sum type), or cgo is
  chosen (mattn) AND cross-arch deploy becomes real (then the build story rots).
- Zig is KILLED if: the dashboard outgrows server-rendered tables into anything
  needing a component/template system (no Askama/Templ equivalent exists), or
  karlseguin/zqlite.zig stops tracking Zig releases (0.x churn is the
  background risk).

No language is hard-killed by the spec as written: all three CAN satisfy every
constraint. The ranking below is fit, not feasibility.

## 5. Ranked recommendation

1. RUST. Best spec fit. The B4 lesson (explicit interval markers, never
   overloaded NULL) is a type-system problem and Rust's enums solve it at
   compile time; rusqlite/bundled is the cleanest FTS5+WAL story surveyed;
   Axum+Askama+htmx is a mature, production-proven dashboard pattern with no
   WASM/Node pipeline; idle RSS ~3.6-7MB is the lowest of the GC/runtime
   options. Costs: slowest iteration (compile times, borrow checker), musl
   setup for true static binaries, the tokio/rusqlite seam.
2. GO. Best iteration speed and deploy ergonomics. If Justin values reshaping
   the dashboard fast over squeezing RSS, Go wins on velocity: trivial
   cross-compile, huge ecosystem, templ+htmx is the converged pattern, and at
   this scale the modernc perf gap is unmeasurable. Costs: B4 markers enforced
   by schema not compiler (weakest spec-fit point), ~7MB GC floor, the
   database/sql pool footgun must be handled deliberately, pick modernc
   (portability) over mattn (cgo) unless a measured gap appears.
3. ZIG. Most efficient in absolute terms (sub-MB binaries, ~1MB RSS, trivial
   static cross-compile) and the honest winner of "super efficient" as a pure
   number. Ranked third because the dashboard is a UI problem more than a
   bytes problem: no mature templating story means hand-rolled HTML for every
   table, card, and filter chip, and Claude has the thinnest training data for
   http.zig+zqlite idioms. Right choice if the build ever becomes a tiny
   always-on sidecar where binary size is the binding constraint; wrong choice
   for a dashboard Justin will iterate on.

The deciding logic: at single-operator scale, the efficiency differences
between these three are unmeasurable in practice (all idle under 10MB, all
start in milliseconds). What differs is (a) how well the language prevents the
B4 class of bug, and (b) how fast Justin can reshape the UI. Rust wins (a),
Go wins (b), Zig wins neither for this workload despite winning the raw
numbers.

## 6. Numbers appendix (all sourced, 2026)

- Rust Axum hello-world: 3.6MB baseline RSS; 12.1MB max at 769k req/s
  (nevindra/nilo comparison; programatik29/rust-web-benchmarks).
- Rust SQLite CRUD on Pi 5: 7.36MB weighted peak RSS, 310 req/s/MB, 2.8x Go
  (Zenodo pilot, Oliveira 2026).
- Rust Axum+tokio WS relay: <6MB binary (LTO+z+strip), ~10MB idle
  (devmercenary/hive-sync).
- Go net/http hello-world: 7.6MB binary; 7.7MB baseline RSS; 19,897 B per idle
  conn (dev.to suite; nilo comparison).
- Go real service: 31MB idle RSS, 17ms cold start, 9.4MB static binary
  (satomic/model-router).
- Go 1.26 BSS: 32MB FIPS DRBG pool at startup, cannot be disabled via build
  flags (ramayac/mdblog investigation). Real but irrelevant at this scale.
- mattn vs modernc: 2.0-2.3x read-scan gap, 1.3x prepared-lookup gap on
  11M-row production DB (Kpa-clawbot/CoreScope). modernc requires Go 1.25+.
- Zig zap server: 829KB binary; 6MB idle, 85MB at 10k conns (cppdozer;
  penchef 2026). Zig std.http.Server: ~1MB idle (dingjiu1989-hue comparison).
- karlseguin/zqlite.zig: +682-808KB measured, bundles SQLite 3.53.0, 190 stars
  (bevry-vibes/agent-detect plan).
- Toolchains: Rust 1.7GB + ~/.cargo; Go 258MB; Zig 246MB (minicompiler/mc
  comparison).
- Coolify sentinel bench (Go vs Rust, 2026-08): Rust +67% mixed RPS, ~2x
  tighter p99, ~3x idle RSS, -44% binary. Both passed stress.

UNVERIFIED: exact Axum+Askama+rusqlite combined binary size for a dashboard of
this shape (no published build found; estimate 8-14MB stripped from component
figures). Exact Templ+htmx dashboard cold-start numbers (no isolated bench
found; net/http baseline 17ms is the floor).

## 7. Implementation one-liners for Claude

- If RUST: Axum 0.8 + Askama + htmx (vendored, no build step); rusqlite with
  `bundled` feature, PRAGMA journal_mode=WAL, foreign_keys=ON, busy_timeout;
  DB access behind a dedicated thread or tokio-rusqlite (never block the async
  runtime); interval endpoints as a Rust enum (Timestamp / UnboundedFuture /
  Unknown); receipt ledger written in the same transaction BEFORE the mutation;
  feed_item as a SQL VIEW ordered by (event_time, id); target
  x86_64-unknown-linux-musl for the static binary.
- If GO: stdlib net/http (1.22+ routing) or Chi + Templ + htmx; modernc.org/sqlite
  (pure Go, trivial cross-compile; switch to mattn/go-sqlite3 only on a measured
  gap); DSN `_journal_mode=WAL&_busy_timeout=5000&_foreign_keys=true`,
  db.SetMaxOpenConns(1) with a single writer goroutine; interval markers as
  string constants with CHECK constraints in the schema (compiler cannot
  enforce); receipt ledger in the same Tx before mutation; feed_item VIEW
  ordered by (event_time, id); embed tzdata for ET rendering; GOOS/GOARCH build.
- If ZIG: http.zig + hand-rolled HTML rendering (no template engine; keep pages
  to tables/cards/partials); karlseguin/zqlite.zig (bundles real SQLite 3.53.0;
  do NOT use ghostkellz/zqlite, it is a proprietary-format reimplementation);
  PRAGMA journal_mode=WAL, busy_timeout; interval endpoints as a tagged union;
  explicit allocator threading, arena per request; receipt ledger in the same
  transaction before mutation; feed_item VIEW ordered by (event_time, id);
  `zig build -Dtarget=x86_64-linux-musl` for the static binary; pin the
  zqlite.zig version (0.x churn).

Sources: search-result URLs are in the parent agent's search context; key
primary documents: programatik29/rust-web-benchmarks, nevindra/nilo
docs/comparison.md, Zenodo 20775739 (Oliveira Pi 5 pilot), coollabsio/sentinel
2026-08-09 bench, ramayac/mdblog binary-size investigation, Kpa-clawbot/CoreScope
PR #1992, bevry-vibes/agent-detect sqlite plan, anortham/julie FTS5 ADR,
luizvbo/axum-kickoff, clownware/go-performance-starter ADR-017.
