# UnSilo Intel Feed Dashboard — Claude Launch Prompt (2026-10-02)

## 0. How to read this prompt

This is a two-phase engagement. Phase 1 is MANDATORY and comes first:
confirm or correct the research pack before writing any implementation code.
Phase 2 (implementation) starts only after the operator approves your
corrected research. Do not skip Phase 1. Do not blend the phases.

## 1. Mission

Build the UnSilo intel feed dashboard: a local-first, single-operator,
single-binary dashboard over Justin's career-hunting intel corpus. It tracks
company audits, forensic findings, claim verdicts (CONFIRMED / KILLED /
DOWNGRADED / UNKNOWN), open blockers with falsifiers, and job applications.
Working name: UnSilo. Justin's positioning, verbatim: "we are the people's
anti palantir. we are meta's meta. we track and we analyze using what they
give us and what they dont." Analytical principle: absence as signal. What
institutions don't publish is first-class data.

Scope boundary: this task is the intel feed DASHBOARD only. A separate
program (the intel harness / research chain) has build NOT authorized. Do not
build the harness. Do not expand scope into it.

## 2. The research pack (in this Drive folder)

1. `unsilo-feed-dashboard-spec-2026-10-02.md` — WHAT the dashboard shows:
   layout (blockers strip top and bottom, applications tracker, filterable
   intel feed, research surfaces), copy rules, and the full data inventory
   (7 job applications with req IDs and statuses, open blockers with
   falsifiers and owners, feed items reverse-chronological).
2. `unsilo-data-theory-2026-10-02.md` — HOW it is built, relational theory:
   staging vs core schemas, entity inventory, 3NF/BCNF posture,
   bitemporal tables with Allen interval discipline, absence-as-signal as an
   `expectation` table, verdicts as rows with history, hash-chained receipt
   ledger, FTS5 search, migration discipline. Section 9 holds the reconciled
   implementation stack.
3. `dashboard-crawl-report.md` — prior-art survey: 16 dashboard repos,
   star-sorted, all pushed within 2 years of 2026-10-02, screenshots viewed,
   dead links marked, license cautions flagged, top-5 shortlist with
   adoptable patterns. Language is "prior art to reimplement," never
   "stealing." AGPL repos (worldmonitor, glance) are concept-safe and
   code-hostile: reimplement patterns, do not port code.
4. `language-shootout-2026-10-02.md` — Rust vs Go vs Zig, ranked against the
   spec. Winner: Rust. Read the kill criteria per language and the
   UNVERIFIED items before trusting any number.
5. `dashboard-screenshots/` — representative screenshots for the top-5
   shortlist repos.
6. `harness-build-spec-v1.2-2026-09-30.md` — the intel HARNESS build spec.
   Read for scope-boundary awareness ONLY. This is the program you must
   NOT build. It is in the pack so there is no ambiguity about where the
   dashboard ends and the harness begins.

## 3. Phase 1: research confirmation / correction (DO THIS FIRST)

Your job in Phase 1 is adversarial confirmation, not implementation. For
each document in the pack:

a. Restate its load-bearing claims in your own words, one per line.
b. For each claim, mark it: CONFIRMED (you verified it against a primary
   source you name), PLAUSIBLE (consistent but you could not verify),
   WRONG (with the correction and your evidence), or UNKNOWN (cannot be
   determined from available sources; say what would determine it).
c. Attack the two decisions most likely to be wrong:
   - The Rust pick. The strongest counter-evidence is that the crawl's two
     closest full architectural templates (glance, gatus) are Go, and Go
     wins on iteration velocity. Steelman the Go case. If you conclude the
     pick should flip, show the mechanism, not a vibe.
   - The B4 interval design (bitemporal tables, explicit UNBOUNDED_FUTURE /
     UNKNOWN markers, Rust enums making the freeze bug unrepresentable).
     Try to break it: find a query or state transition where the markers
     leak, get conflated with NULL, or silently freeze.
d. Check the shootout's efficiency numbers against primary sources where
   reachable. The report marks UNVERIFIED items explicitly; verify or
   downgrade each one.
e. Check the crawl's star counts and push dates are a 2026-10-02 snapshot
   and note any drift you observe.
f. Flag anything in the spec's data inventory (req IDs, dates, application
   statuses, blocker falsifiers) that is internally inconsistent.
g. FULL SPEC READ (no skimming): read every pack document cover to cover
   before marking any claim CONFIRMED. No verdicts from summaries, section
   headers, or file names. If a document is long, read it in full anyway;
   "I read the headers" is not a read. Also read
   `harness-build-spec-v1.2-2026-09-30.md` (in this folder) for
   scope-boundary awareness only: it defines the program you must NOT
   build. Confirm in your report that you read each document in full by
   naming one non-obvious detail from each.

Deliverable for Phase 1: a correction report with three sections.
CONFIRMED (claims that survived, with sources), CORRECTED (claims that
changed, old vs new with evidence), OPEN (unknowns with the exact falsifier
or source that would close each). Do not write implementation code in
Phase 1. End Phase 1 by stating explicitly what you need from the operator
before Phase 2.

## 4. Standing rules (non-negotiable, both phases)

- No em dashes in any people-facing copy, ever. Use hyphens or periods.
- Terse, technically dense prose. No filler, no purple language.
- All times in 12-hour AM/PM America/New_York.
- Verify before declaring. A search snippet is not a source; open the source.
- DVD: data, verification, determinism. Every judgment traces to a sourced
  row or finding. Auditable output uses deterministic pipelines.
- Spec-driven: the spec and theory doc are authoritative. If implementation
  reality forces a spec change, propose the spec edit first; do not silently
  diverge.
- Prior-art framing: the crawl surveyed open-source dashboards to learn
  from. Reimplement patterns; do not port code, especially from AGPL
  sources. Never describe this as stealing.
- Blockers lead: surface blockers first in any status report, with
  falsifier and owner each.
- Never invent identifiers: req IDs, dates, counts come from the pack or
  from sources you opened, never from memory.
- Unknowns stay UNKNOWN. Do not smooth them over.

## 5. Phase 2: implementation (GATED — starts only on operator approval)

Stack (from the reconciled research; re-confirm in Phase 1 before using):
Rust. Axum 0.8 + Askama + htmx (vendored, no build step). rusqlite with
`bundled` feature. PRAGMA journal_mode=WAL, foreign_keys=ON, busy_timeout.
DB access behind a dedicated thread or tokio-rusqlite, never blocking the
async runtime. Interval endpoints as a Rust enum (Timestamp /
UnboundedFuture / Unknown). Receipt ledger written in the same transaction
BEFORE the mutation. feed_item as a SQL VIEW ordered by (event_time, id).
Target x86_64-unknown-linux-musl. Single static binary, no runtime.

Adopted architecture patterns (from the crawl):
- Config-driven UI: dashboard declared in config (sections, entity tables,
  blocker lists).
- Module registry: feed, verdicts, blockers, applications as independent
  modules with own refresh cadence and failure isolation.
- Verdict pills as primary visual grammar.
- Every number is a query you can open (redash pattern).
- Per-panel staleness; a dead source never poses as fresh.
- Probe-history strip for claim-evidence timelines (gatus pattern).
- Markdown + SQL as the source of truth for frozen briefing reports.

Build order: schema and migrations first (theory doc sections 2-4, 8),
then the feed VIEW and FTS5 search, then modules, then the config layer.
Hash-receipt every migration. The staging schema must accept the tentative
Duolingo-format data and promote it through the documented path; design
for partial data, not just the clean case.

## 6. Definition of done

- Single static binary serves the dashboard; no Node, no runtime.
- All spec sections render from the SQLite database, no hardcoded content.
- Every panel traces to an openable SQL query.
- B4 interval bug is unrepresentable: interval endpoints are a Rust enum,
  NULL never means an unknown endpoint.
- Receipt ledger: every core mutation has a before/after hash receipt.
- Blockers strip renders top and bottom with falsifier and owner.
- Operator runs one command and gets the dashboard; document that command.

## 7. Tool invocations (Phase 1 and Phase 2)

Use these specific tools for verification and implementation. Do not rely on
training data for library APIs, versions, or repo contents.

### Context7 (library docs — verify every API claim)
For each of these, resolve the library ID via Context7 then pull docs:
axum (0.8), askama, rusqlite (with `bundled` feature), htmx (vendored),
tokio-rusqlite. Rule: any claim you make about an API signature, feature
flag, PRAGMA interaction, or version behavior must be backed by a Context7
doc lookup from the current release, not from memory. When docs and the
research pack disagree, the docs win and the pack gets a CORRECTED entry.

### GitHub (prior art and version truth)
- Releases: check the latest release tags for axum, askama, rusqlite via
  the GitHub releases API before pinning versions. Pin exact versions in
  Cargo.toml; no floating minors.
- Pattern confirmation: before reimplementing any adoptable pattern from
  the crawl (config-driven UI, module registry, probe-history strip,
  verdict pills, per-panel staleness), open the actual source file in the
  referenced repo and confirm the pattern exists as described. Name the
  file and lines in your Phase 1 report.
- License check: confirm the license file of any repo whose pattern you
  adopt (worldmonitor and glance are AGPL-3.0: patterns only, no ported
  code). Record the license you found, not the one the report claims.

## 8. What not to do

- Do not build the intel harness or touch the research chain program.
- Do not port code from AGPL-licensed repos.
- Do not add features not in the spec without proposing a spec edit first.
- Do not present unverified claims as confirmed. Mark them.
- Do not optimize for how the report reads; optimize for the work.
