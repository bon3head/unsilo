# UnSilo Dashboard Program — Continuation Report (2026-10-02 ~2:15 AM ET)

## 1. Where this program stands

The UnSilo intel feed dashboard program is in RESEARCH phase. No implementation
code has been written by anyone. The full research pack lives in the UnSilo
Drive folder (12 files after this report is uploaded):

1. `unsilo-claude-launch-prompt-2026-10-02.md` — the Claude engagement prompt
   (two-phase: Phase 1 adversarial confirmation, Phase 2 gated implementation).
2. `unsilo-feed-dashboard-spec-2026-10-02.md` — WHAT the dashboard shows.
3. `unsilo-data-theory-2026-10-02.md` — relational design theory, HOW it is built.
4. `dashboard-crawl-report.md` — 16-repo prior-art survey with screenshots.
5. `language-shootout-2026-10-02.md` — Rust vs Go vs Zig, Rust wins on spec-fit.
6. `harness-build-spec-v1.2-2026-09-30.md` — scope boundary ONLY. Not to be built.
7-11. Five top-5 shortlist screenshots.
12. This report.

Claude currently holds the launch prompt and is executing Phase 1
(research confirmation/correction). Phase 2 has NOT started and starts only
on the operator's explicit approval.

## 2. State corrections already applied (2026-10-02 ~2:00 AM ET)

The pack was stale on two points; both are corrected in the spec and Drive:

- Authority gate: was listed OPEN, now DECIDED 2026-10-02-01. Option B:
  RECONSTRUCTED-AUTHORITY SEMANTIC COMPLETE. Original-authority completion
  is unreachable. v1 artifacts are labeled RECONSTRUCTED, never original.
- Research-chain blocker table: was "B4 single open blocker," now the true
  state. FROZEN: B2, B3, B4, B7, B8. REPAIRED-PENDING-ADMISSION: B1, B9
  (freeze retracted; contaminated admission package in chat 6abe1a5b).
  OPEN: B10 (later work quarantined provisional). RETAINED: B5, B6, B11,
  B12. UNADMITTED: RECON-ECLASS-PD-AO-DD-v2.0 classifier (CLASSIFY yields
  ABSTENTION). ORIGINALS_RECOVERED = PARTIAL.
- Build authorization: NONE, has never been anything else. S11/S12 gated
  behind chain completion. Pending remediation starts with the ledger erratum.

## 3. The rerun protocol (runs after Claude's Phase 1 report lands)

When Claude delivers its Phase 1 correction report (CONFIRMED / CORRECTED /
OPEN), the program reruns reconciliation in extreme detail before any Phase 2
approval. The rerun is owned by the operator's agent (Cipher), with Claude's
report as input, not as authority. Steps, in order, no parallelization:

### Step 1 — Ingest Claude's report against the pack
For every CORRECTED claim: open the cited primary source, verify the
correction independently, and mark it ADOPTED or CONTESTED (with mechanism).
For every OPEN unknown: check whether the falsifier or source it names is
actually reachable; if yes, go get it before proceeding. For every CONFIRMED
claim: spot-check at least 20% against primary sources; a CONFIRMED section
with zero spot-check failures is still not trusted wholesale.

### Step 2 — Relational theory audit (extreme detail)
Re-derive the schema from the data theory doc with the full context in mind:
- Entity inventory vs the actual intel corpus: every table in section 2
  must join to a real artifact or a real feed section. Orphan tables get
  cut or justified.
- Normalization: re-prove 3NF/BCNF per table. Name the functional
  dependencies. Any table that fails gets redesigned, not excused.
- Bitemporal discipline: construct adversarial cases. An application that
  was open, then rejected, then reopened. A claim confirmed, then killed
  by new evidence, then re-confirmed. A filing whose valid_time is
  disputed between two sources. Run each through the interval-enum design
  and show the failure mode if the design is wrong.
- The B4 regression test: write the exact query/transition that froze
  UNBOUNDED/UNKNOWN under the old design, run it against the new design,
  and confirm it cannot produce the freeze. This is the single highest
  value verification in the rerun.
- Absence-as-signal: build three `expectation` rows from real intel
  (a missing filing, a missing verdict, a missing application response),
  write the loudest-absence query, and confirm the ordering matches the
  Shannon intuition (most surprising first).
- Receipt ledger: simulate a mutation, a repair, and a repair-of-a-repair;
  confirm the ledger bounds all three and history is never edited.
- Staging-to-core promotion: take the tentative Duolingo-format data shape
  and walk it through promotion by hand. Every promotion rule must be
  executable, not aspirational. Gaps become OPEN unknowns with owners.

### Step 3 — Stack re-verification
Re-run the language decision against Claude's Phase 1 findings:
- If Claude's Context7/GitHub verification changed any shootout number,
  re-rank. The Rust pick is provisional until this step passes.
- Confirm the adopted prior-art patterns still have no AGPL contamination
  in the reimplementation plan.
- Confirm the one-liner stack (Axum 0.8 + Askama + htmx, rusqlite bundled,
  musl) pins exact versions from the releases API.

### Step 4 — Slop reconciliation
Claude has full permission to flag slop in the pack: inflated claims,
decorative architecture, patterns adopted without a mechanism, numbers
without sources. Every flag gets triaged: CONCEDE with the fix, or CONTEST
with the mechanism. A flag neither conceded nor contested is itself slop;
do not carry it forward silently.

### Step 5 — Pivot proposals
Claude may propose pivots (different stack, different schema shape,
different dashboard architecture, scope changes). Each pivot proposal must
carry: what changes, why the current design fails (mechanism, not vibe),
what it costs (migration, rework, risk), and what would falsify the pivot.
Pivots are proposals, not decisions. The operator decides.

### Step 6 — Updated pack
The rerun produces: an updated spec (versioned, dated), an updated theory
doc (versioned, dated), a reconciliation log (every Claude flag with
CONCEDE/CONTEST and the evidence), and a go/no-go recommendation for
Phase 2 with named residual risks. All four land in the Drive folder before
the operator is asked for Phase 2 approval.

## 4. Permissions granted to Claude for this rerun

- Full permission to suggest pivots, updates, and reconciliations.
- Full permission to call out slop anywhere in the pack, including in the
  operator's own prior decisions, with the mechanism.
- Full permission to mark pack claims WRONG with evidence.
- NOT granted: expanding scope into the harness program, porting AGPL code,
  writing Phase 2 implementation code before approval, or treating its own
  Phase 1 report as verified (it is input to the rerun, not its conclusion).

## 5. Standing constraints (unchanged)

No em dashes in people-facing copy. Terse, technically dense. 12-hour
AM/PM ET. Verify before declaring. DVD. Spec-driven. Unknowns stay UNKNOWN.
Blockers lead. One sequential track for the harness program; the dashboard
rerun is its own track and does not unblock harness work.
