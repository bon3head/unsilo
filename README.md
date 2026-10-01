> **Status: research in progress.** S1-S10 sessions are complete but
> blockers B1, B9, and B10 are still open and final approval is pending. Nothing
> in this repo is a finished specification.
>
# UnSilo v1 research chain — final approval and reconciliation drive package

## Lifecycle
Research chain S1–S10 complete (2026-09-30 → 2026-10-01). Current stage: final
approval and reconciliation. Next step: this review determines whether the v1
semantic specification is build-ready or needs more research.

## What this is
UnSilo v1 = Public Recruiting State. The frozen claim: it deterministically
reconstructs and compares a company's publicly observable recruiting
representation state across time from public records (SEC EDGAR, declared
careers boundary H∪D∪R, Wayback CDX), with declared evidence scopes and
coverage qualification. Evidence classes are categorical: PD, AO, DD, QN, UR.
No numerical probability-style confidence anywhere.

## Reading order
1. `research-chain/s10-output-2026-10-01.md` — the assembled v1 semantic
   specification, adversarial validation (20 attacks), B1–B12 disposition,
   open-unknowns register, and the exact B4 repair contract.
2. `research-chain/s1-output-2026-09-30.md` through
   `research-chain/s9-output-2026-10-01.md` — per-session semantic freezes.
3. `research-chain/folklore-kill-log-2026-10-01.md` — 84 killed claims.
4. `research-chain/poc-results-2026-09-30.md` — PoC evidence folded into
   sessions (CDX, EDGAR, temporal toy, SQLite hazards).
5. `research-chain-plan-2026-09-30.md` — the original sequential plan.
6. `build-blockers-b1-b12-verbatim-2026-09-30.md` — the twelve blockers,
   verbatim.

## Current standing (as of S10)
- v1 semantic specification verdict from the S1–S10 chain: **NEEDS-REPAIR**.
- 7R research gate (B1, B2, B3, B9): **CLEARED**.
- B1, B2, B3, B5, B6, B7, B8, B9, B10, B11, B12: **FROZEN**.
- **B4 (temporal interval algebra): OPEN.** S3 over-froze "any non-KNOWN
  required endpoint → UNKNOWN," conflating UNBOUNDED (information) with
  UNKNOWN (missing information). The repair contract is specified exactly in
  `research-chain/s10-output-2026-10-01.md` §VI.
- Build is **not authorized**. No implementation exists. This review decides
  research sufficiency only — it does not authorize a build.

## The reconciliation task
Determine, with reasons, whether the v1 semantic specification is
**build-ready** or **needs more research**, and exactly what research remains
if the latter. Verify: (a) the S10 NEEDS-REPAIR verdict is correct and
complete; (b) the B4 repair contract is sufficient and correctly scoped (no
other session needs reopening); (c) the 84 folklore kills hold; (d) no
UR→VALUE escape exists in the assembled spec; (e) the open-unknowns register
is honest (semantic gaps vs build work). Weak claims must never pass
confidently — any verdict you emit must name its evidence class and limits.
