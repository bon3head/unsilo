# Dashboard Crawl Report — UnSilo prior-art survey (2026-10-02)

Research-only. No code implemented. All star counts and push dates verified against
api.github.com on 2026-10-02 (unauthenticated, rate-limited). All demo image URLs
below were found in the repos' READMEs and verified live by download; screenshots
were actually viewed by the survey workers.

## Methodology

Repo discovery ran on the GitHub code-search API with freshness and star gates baked
into the queries: `pushed:>2024-10-01` (2-year window) plus star floors, sorted
`sort=stars&order=desc`. Three query angles were used so the pool is not just SaaS
admin templates: (1) `dashboard in:name stars:>3000` for literal dashboard repos;
(2) `topic:dashboard stars:>1500` which surfaced the intel/BI/terminal long tail;
(3) `analytics dashboard stars:>2000` for the BI/analytics lane. Non-dashboards
(strapi, chatwoot, pi-hole, plotly.py, activitywatch) were filtered out by hand, as
were stale or tutorial-grade hits. The final 16 are the most-starred survivors that
are both fresh and actually dashboards. Four worker subagents then surveyed 4 repos
each: real metadata from the API, README screenshots downloaded and viewed, visual
style described from pixels, and "adoptable patterns" lists framed for a dense,
dark, terminal-style single-operator intel dashboard (UnSilo: claim verdicts,
blockers with falsifiers, application tracker, audit tables).

Language note: the word "steal" was scrubbed from this report at the operator's
request. Everything here is prior art to learn from and reimplement, not code to
lift. License column matters for exactly that reason: AGPL-3.0 repos are
concept-safe but code-hostile for a private build.

## Comparison table

| repo | stars | last push | lang / stack | visual style | license |
|---|---|---|---|---|---|
| koala73/worldmonitor | 87,672 | 2026-10-02 | TS + Vite, Tauri/Rust shell, globe.gl/deck.gl | dark dense command-center intel map | AGPL-3.0 |
| grafana/grafana | 77,044 | 2026-10-02 | TS/React + Go backend | dark collapsible panel grid | AGPL-3.0 |
| metabase/metabase | 49,507 | 2026-10-02 | Clojure + TS/React | light spacious BI cards | AGPL/commercial dual |
| tabler/tabler | 41,800 | 2026-10-01 | Bootstrap kit (Astro docs) | dark SaaS KPI cards | MIT |
| ant-design/ant-design-pro | 38,824 | 2026-10-01 | TS, React 19 + Umi 4, AntV | enterprise admin analytics | MIT |
| glanceapp/glance | 37,293 | 2026-09-05 | Go stdlib server-rendered, YAML config | dark dense widget grid, terminal-typed | AGPL-3.0 |
| getredash/redash | 28,830 | 2026-10-01 | Python Flask + React, Plotly | light BI, query-first | BSD-2-Clause |
| lissy93/dashy | 26,608 | 2026-10-01 | Vue 3 + Vite, conf.yml | dark icon-tile launchpad | MIT |
| allinurl/goaccess | 20,981 | 2026-10-01 | C + ncurses / generated HTML | dark terminal panels + light report | MIT |
| wtfutil/wtf | 17,110 | 2026-09-30 | Go + tview/tcell | dark terminal cockpit | MPL-2.0 |
| satnaing/shadcn-admin | 15,522 | 2026-09-10 | TS, React + Vite + Tailwind, recharts | SaaS admin, light/dark | MIT |
| TwiN/gatus | 12,218 | 2026-09-30 | Go + Vue, embedded SQLite | very dark navy status cards | Apache-2.0 |
| perspective-dev/perspective | 11,267 | 2026-10-01 | Rust (C++ WASM engine) | dark streaming datagrid | Apache-2.0 |
| hyperdxio/hyperdx | 9,924 | 2026-10-02 | TS React + ClickHouse, has TUI | dark observability tiles | MIT |
| evidence-dev/evidence | 6,970 | 2026-10-01 | TS Svelte + DuckDB, md+SQL pages | UNKNOWN, no screenshots found | MIT |
| chartbrew/chartbrew | 4,065 | 2026-09-29 | JS React + Node, Chart.js | light generic SaaS | Other (no SPDX) |

## Per-repo findings and adoptable patterns

### 1. koala73/worldmonitor (87,672 stars, pushed 2026-10-02, AGPL-3.0)
TypeScript + Vite frontend in a Tauri 2 (Rust) shell; maps via globe.gl/Three.js +
deck.gl/MapLibre; serves MCP + REST + CLI.
Screenshot: https://github.com/koala73/worldmonitor/raw/main/docs/images/worldmonitor-7-mar-2026.jpg
(viewed: dark command-center, LIVE pill, DEFCON 5 pill, layer checklist of ~10
toggleable intel layers, time-window chips, breaking-news ticker, AI INSIGHTS
column with WORLD BRIEF and AI STRATEGIC POSTURE cards.)
Adoptable patterns:
- Layer-toggle paradigm: one canonical view, each intel stream a toggleable lane
  (claims / blockers / applications / audits) instead of separate pages.
- Severity-pill taxonomy as first-class UI grammar: verdict pills
  (CONFIRMED/KILLED/DOWNGRADED/UNKNOWN) should be the primary visual language.
- Per-panel freshness state: every stream shows its own LIVE/PAUSED/staleness, so a
  dead scraper never poses as fresh data.
- Analyst brief cards above raw feeds: synthesized summary sitting next to the
  claim table, mirroring UnSilo's wanted pattern.
- One codebase, variant configs: design the layout as one app with build-time
  variants, never forks.
License caution: AGPL-3.0. Reimplement concepts, do not port code.

### 2. grafana/grafana (77,044 stars, pushed 2026-10-02, AGPL-3.0)
TypeScript React frontend, Go backend, panel/data-source plugin framework.
Screenshots: README has NO dashboard screenshots (verified). Community dashboard
viewed as reference: https://grafana.com/api/dashboards/24945/images/20508/image
(dark, collapsible row groups, panel grid, gradient area fills, flat zero-chrome).
Adoptable patterns:
- Collapsible row groups as the primary organization unit: group by entity with
  one-click collapse; beats tabs for scanning many categories.
- Panel card grammar: title + viz + micro-legend, nothing else. Verdict pills and
  falsifier links live in the title bar.
- Per-panel time-range independence: each feed lane keeps its own freshness window.
- Gradient area fills on near-black for trend sparklines (claim confidence over
  time, application funnel).
- Do NOT adopt: the metrics-first grid-of-charts assumption. UnSilo's core objects
  are relational/tabular; lift the density discipline, not the layout.

### 3. metabase/metabase (49,507 stars, pushed 2026-10-02, AGPL/commercial dual)
Clojure backend, TS/React frontend, own built-in viz.
Screenshot: https://github.com/metabase/metabase/raw/master/docs/images/metabase-product-screenshot-updated.png
(viewed: light theme, soft rounded cards, KPI + delta cards, donut, gauge,
stacked bars, choropleth, heat-shaded pivot table.)
Adoptable patterns:
- KPI-plus-delta card: number + window + delta ("open blockers: 7, +2 vs
  yesterday") is the densest summary atom there is.
- Heat-shaded pivot tables: cell intensity encodes evidence weight in entity
  tables without extra columns.
- Goal-progress bar with marker: adopt for blocker-resolution burn-down or
  application targets.
- Anti-pattern: the light spacious BI-consumer aesthetic is the explicit
  non-target. Take the card composition, leave the look.

### 4. tabler/tabler (41,800 stars, pushed 2026-10-01, MIT)
Bootstrap 5 kit (framework-agnostic), ApexCharts bundled (note: ApexCharts is no
longer MIT, dual-licensed Community <$2M revenue).
Screenshot: README has none (verified); dark demo verified at
https://erum2020.rinterface.com/static/images/tabler-dark.png (viewed).
Adoptable patterns:
- KPI card with embedded sparkline + delta arrow: reimplement for the feed header.
- Dark-mode token architecture: theme-as-token-layer from day one, so the
  terminal aesthetic is a skin, not a fork.
- Component inventory as parts catalog: tables, badges, timelines as primitives
  to borrow shapes from, not the visual direction.
- Tabler Icons (6,000+ MIT SVGs): consistent glyph set for verdict pills and
  entity types instead of emoji.
- Do NOT adopt: the SaaS-admin visual register.

### 5. ant-design/ant-design-pro (38,824 stars, pushed 2026-10-01, MIT)
TS, React 19 + Umi 4, Ant Design 6, pro-components, AntV charts.
Screenshots (both viewed):
- https://github.com/user-attachments/assets/74ad0b4a-e086-4955-8edd-9f2cff31aee8 (light)
- https://github.com/user-attachments/assets/d4bcb7c1-9029-4c0f-b130-1193a931f9f7 (dark)
Adoptable patterns:
- KPI card anatomy (big number + WoW/DoD delta pair + sparkline + footer metric):
  exactly the shape a verdict feed wants, restyled terminal.
- Ranked-list-with-numbered-badges rail next to the main chart: ranked entity rail
  reads faster than a full table.
- Date-range quick-select tabs (24h/7d/30d/all) bound to the feed instead of a
  calendar picker.
- Anti-pattern: SPA admin kit with Node build toolchain; adopt idioms, never the
  architecture.

### 6. glanceapp/glance (37,293 stars, pushed 2026-09-05, AGPL-3.0)
Go, stdlib net/http + html/template + gofeed + gopsutil + yaml.v3. Single binary,
server-rendered HTML, no JS build step, no Node toolchain.
Screenshots (both viewed):
- https://raw.githubusercontent.com/glanceapp/glance/main/docs/images/readme-main-image.png
- https://raw.githubusercontent.com/glanceapp/glance/main/docs/images/themes-example.png
  (six themes incl. green-terminal-on-dark)
Adoptable patterns:
- Single-Go-binary, zero-JS-build, server-rendered architecture: the closest
  structural match to the efficient-language shortlist. Trivial to self-host.
- Config-driven UI: one YAML declaring pages -> columns -> widgets, hot-reloaded.
  UnSilo should be a config declaring feed sections, entity tables, blocker lists.
- Per-widget fetch-and-cache with per-source intervals; a failing widget degrades
  its own block, never the page. Adopt per-source isolation: a dead source shrinks
  one block, never blanks the dashboard.
- Dense typographic register (small-caps section labels, tabular numerals,
  inline sparklines): the terminal aesthetic without cosplaying a terminal.
License caution: AGPL-3.0.

### 7. getredash/redash (28,830 stars, pushed 2026-10-01, BSD-2-Clause)
Python Flask backend, React 16 + AntD 4 frontend, Plotly.js/d3 viz-lib.
Screenshot (viewed first frame):
- https://raw.githubusercontent.com/getredash/website/8e820cd02c73a8ddf4f946a9d293c54fd3fb08b9/website/_assets/images/redash-anim.gif
Adoptable patterns:
- Query-backed widgets with named, openable queries: every panel traces to a SQL
  string you can click into. "Every number is a query you can open" is the
  accountability primitive; makes the dashboard auditable by construction.
- Scheduled refresh + staleness stamps on every widget: intel decays, the UI
  shows age not just value.
- Alerts as saved-queries-with-thresholds: a blocker list is a saved query with
  an alert threshold; adopt alert-on-query for falsifier triggers.
- Anti-pattern: 40-source BI pluralism is overkill for one operator. Adopt the
  query -> widget -> staleness chain, not the data-source zoo.

### 8. lissy93/dashy (26,608 stars, pushed 2026-10-01, MIT)
Vue 3.5 + Vite, frappe-charts, in-UI config editor (CodeMirror), Express.
Screenshots:
- https://i.ibb.co/L8YbNNc/dashy-demo2.gif (viewed first frame, dark Callisto theme)
- https://i.ibb.co/yhbt6CY/dashy.png (live, but it is the LOGO, not a UI screenshot)
Adoptable patterns:
- Single Docker container + one conf.yml + in-UI config editor with live preview:
  the single-operator self-hosting gold standard.
- Per-service status checking with status chips: map onto source-health
  monitoring (alive / stale / dead per intel source).
- Grouped collapsible sections with instant search-to-filter: Feeds / Verdicts /
  Blockers / Applications as filterable groups.
- Token-driven theme system with switcher: terminal aesthetic as a theme, not
  hard-coded.
- Anti-pattern: it is a link board, not a data surface. Adopt the ops machinery,
  never the tile-grid content model.

### 9. allinurl/goaccess (20,981 stars, pushed 2026-10-01, MIT)
C, ncurses terminal UI + self-generated HTML report.
Screenshots (both viewed):
- https://goaccess.io/images/goaccess-real-time-html-gh-2026.png?2026021201
- https://goaccess.io/images/goaccess-real-time-term-gh-2026-1.png?2026021201
Adoptable patterns:
- Terminal panel idiom: numbered, collapsible, keyboard-navigated panels, each =
  one entity table + inline ASCII bars. Maps 1:1 onto a claim-verdict feed.
- Color the CELL, not the row: verdict pills and metric cells colored by
  magnitude at cell level doubles readable density in a monospace grid.
- Dual surface from one analyzer: terminal as operator console, generated HTML
  report as the shareable frozen artifact. Adopt the split.
- Efficiency proof: pure C, in-memory hash-table aggregation, real-time tail, no
  DB, no GC pauses. The entire working set fits in RAM; Go/Rust core + SQLite for
  durability is more than enough.

### 10. wtfutil/wtf (17,110 stars, pushed 2026-09-30, MPL-2.0)
Go + tview/tcell. Single static binary, no browser.
Screenshot (viewed):
- https://raw.githubusercontent.com/wtfutil/wtf/trunk/images/screenshot.jpg
Adoptable patterns:
- Module registry as architecture: every widget is self-contained (own YAML
  block, own refresh goroutine, own bordered box, failure-isolated) plugged into
  a grid. Adopt for UnSilo: feed module, verdict module, blockers module,
  applications module, each with independent refresh cadence.
- Title-bar idiom: icon + label on a bordered box reads terminal-native without
  being ugly.
- Brutal single-screen density: one-line rows with keys as the left column
  (claim IDs, entity names).
- Efficiency: single static Go binary, starts instantly. tview/tcell is the
  fastest credible path to the terminal aesthetic.

### 11. satnaing/shadcn-admin (15,522 stars, pushed 2026-09-10, MIT)
TS, React + Vite + Tailwind + shadcn/ui (Radix), recharts.
Screenshot (viewed):
- https://raw.githubusercontent.com/satnaing/shadcn-admin/main/public/images/shadcn-admin.png
Adoptable patterns (weakest fit; the anti-pattern boundary):
- Data-table chrome from Users/Tasks pages: faceted filter pills, sortable
  columns, row selection. Adopt for audit and application-tracker tables.
- Global command palette (type-to-jump to entity/claim) worth copying into any
  web surface.
- Do NOT adopt: sidebar-nav SaaS chrome, light-mode default, heaviest stack here.

### 12. TwiN/gatus (12,218 stars, pushed 2026-09-30, Apache-2.0)
Go backend + Vue SPA, embedded SQLite, YAML config. Single static binary.
Screenshots (both viewed):
- https://raw.githubusercontent.com/TwiN/gatus/master/.github/assets/dashboard-dark.jpg
- https://raw.githubusercontent.com/TwiN/gatus/master/.github/assets/dashboard-conditions.jpg
Adoptable patterns:
- Probe-history strip: ~50 colored segments = per-check pass/fail timeline.
  Reimplement in terminal with block characters in verdict colors; each segment =
  one evidence check on a claim. This is UnSilo's claim-verdict timeline,
  ready-made.
- Condition tooltip as falsifier pattern: timestamp + the exact monospace
  condition checks that produced the verdict. Adopt as the claim-evidence popover.
- Health-condition DSL in YAML (`[STATUS] == 200`): adopt a parallel condition DSL
  for watchers (recheck claim every N; KILL if source 404s; DOWNGRADE if text
  changed).
- Verdict pills: the direct ancestor of CONFIRMED/KILLED/DOWNGRADED/UNKNOWN pills.
- Backend shape (Go core + SQLite + YAML config, negligible footprint) is the
  closest architectural template in the whole survey.

### 13. perspective-dev/perspective (11,267 stars, pushed 2026-10-01, Apache-2.0)
Rust (C++ engine compiled to WASM, incl. 64-bit memory64 build; Python/Rust
API targets). Web-component datagrid + WebGL chart engine.
Screenshots (viewed):
- https://perspective-dev.github.io/projects/dark/superstore.png (pure datagrid)
- https://perspective-dev.github.io/projects/dark/market-trading-desk.png (tiled workspace)
Adoptable patterns:
- Virtualized datagrid as the PRIMARY surface, not cards: row-number gutter,
  hairline borders, monospace numerals, color-coded cells. The correct primitive
  for audit and entity tables.
- Streaming-incremental table updates: keep verdict/audit rows in an
  append/update stream; views tick rather than re-render.
- Computed-column expression language: one-liner derived columns (verdict
  signals per row) as a tiny typed expression DSL over feed items.
- View-compiles-to-query: views translate to native SQL (their DuckDB/ClickHouse;
  UnSilo's analog is SQLite) instead of copying data. Dashboard view config ->
  one deterministic SQLite query, no duplicated pipeline.
- Server-side virtualization fallback: stream only visible rows; keeps latency
  flat as tables grow.

### 14. hyperdxio/hyperdx (9,924 stars, pushed 2026-10-02, MIT)
TS React on ClickHouse; Docker all-in-one. README ships `hdx tui`: interactive
TUI with vim keybindings, ANSI dashboard tiles, agent-friendly SQL/NDJSON output
(appearance UNKNOWN, no screenshots in repo).
Screenshots (both viewed):
- https://raw.githubusercontent.com/hyperdxio/hyperdx/main/.github/images/dashboard.png
- https://raw.githubusercontent.com/hyperdxio/hyperdx/main/.github/images/search_splash.png
Adoptable patterns:
- Tile grid + global filter/search bar + time-range selector as dashboard grammar.
- Trace waterfall idiom for provenance chains: nested spans, red on error ->
  claim -> evidence -> source chains and blocker/falsifier trees, restyled
  monochrome with verdict colors.
- Key-value attribute pane under each item: click a feed item -> its metadata,
  verdict history, source hashes.
- TUI as first-class surface sharing one query backend: for a single operator the
  TUI is arguably the primary surface, web UI secondary.
- Alert tiles / event deltas: anomaly pings on the feed (verdict flips, new
  blockers).

### 15. evidence-dev/evidence (6,970 stars, pushed 2026-10-01, MIT)
TS Svelte + Tailwind + DuckDB (incl. WASM); markdown+SQL pages; CLI; builds to a
static site; scheduled email reports; PDF/XLSX export.
Screenshots: NONE found. README has only wordmark SVGs; docs site returned no
image links and a page fetch timed out. Product appearance is UNKNOWN from
repo-side sources. (Site copy describes KPI cards and tables; unverified
presentation, treat as text-only.)
Adoptable patterns:
- Markdown + SQL as the dashboard source of truth: each intel page/report is a
  git-committed file, so the artifact history is hash-receipted by version
  control. Strongest idea in the survey for a hash-receipted workflow.
- Static-site build as delivery artifact: deterministic build from SQLite +
  markdown sources to a frozen report; hash inputs, hash outputs.
- CLI with local preview + markup validation: validate before render, never vibes.
- Scheduled reports: the intel digest on a cron, with preview before send.
- Agent-ready authoring: reports authored by coding agents via CLI; aligned with
  a Cipher-generated intel surface.

### 16. chartbrew/chartbrew (4,065 stars, pushed 2026-09-29, Other/no SPDX)
JS React + Redux + Node, Chart.js, REST + SQL/NoSQL connectors.
Screenshots (viewed):
- https://chartbrew-static.b-cdn.net/banners/hero-v4.webp
- https://chartbrew-static.b-cdn.net/banners/banner_dark_mode.svg
Adoptable patterns (operational only; the visual language is the anti-target):
- Dashboard visibility model: public URL / password-protected / iframe embed.
  Read-only shareable intel view with a password gate.
- Scheduled snapshot deliveries with preview: briefing dispatch pattern.
- Dashboard-as-template: named, reusable, versionable view configs over the feed.

## Top-5 lift shortlist (ranked by fit for UnSilo)

1. **koala73/worldmonitor** — the closest visual+structural DNA in the survey:
   dark dense intel-native surface, verdict-pill grammar, layered toggleable
   feeds, per-panel staleness, analyst brief cards above raw streams. Primary
   reference for look and feed architecture. AGPL: reimplement, do not port.
2. **glanceapp/glance** — the architecture reference: single Go binary,
   zero-JS-build server-rendered HTML, config-driven UI (YAML -> pages/columns/
   widgets), per-widget fetch isolation. Proves the efficient-language +
   config-driven model scales to dense dashboards. AGPL: patterns only.
3. **wtfutil/wtf** — the terminal-cockpit reference: Go + tview/tcell module
   registry (own config block, own refresh goroutine, failure-isolated), brutal
   single-screen density, instant-start static binary. The fastest credible path
   to a terminal-first UnSilo surface.
4. **perspective-dev/perspective** — the data-engine reference: virtualized
   streaming datagrid as primary surface, view-compiles-to-SQL, computed-column
   expressions. Solves the heavy audit-table problem. Apache-2.0, Rust-native
   path exists.
5. **TwiN/gatus** — the verdict-language reference: probe-history strip as
   claim-verdict timeline, condition DSL in YAML for watchers, falsifier-style
   tooltips, and the Go + embedded SQLite + YAML config backend shape. The
   closest full architectural template. Apache-2.0.

Representative screenshots for the top 5 are saved locally at
`hidden_files/dashboard-screenshots/` for eyeballing without chasing links.

## Gaps and honesty notes

- evidence-dev/evidence: no screenshots reachable from repo-side sources;
  appearance UNKNOWN. Its value here is architectural (md+SQL as source), not visual.
- grafana README has no dashboard screenshots; the viewed Grafana shot is a
  community dashboard from grafana.com, not from the repo. A training-site URL
  (promlabs) was DEAD (404).
- tabler README has no screenshots; the viewed dark-mode shot came from an
  external demo mirror (erum2020.rinterface.com), and a tabler.io preview URL was
  DEAD (400). Verified authentic by the Tabler logo/nav in the shot.
- lissy93/dashy: one README image URL is the project logo, not a UI screenshot;
  noted explicitly above.
- hyperdx's `hdx tui` is stated in README text; no screenshots exist, so its
  appearance is UNKNOWN.
- browser_open on github.com/TwiN/gatus timed out worker-side; gatus images were
  recovered from the raw README instead and verified live.
- chartbrew license field returns no SPDX; verify before any commercial use.
- Star counts are a snapshot of 2026-10-02; they drift. Push dates are from the
  API's pushed_at field, verified the same day.
