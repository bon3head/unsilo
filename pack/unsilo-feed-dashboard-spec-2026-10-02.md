# UnSilo Intel Feed Dashboard — build spec (2026-10-02)

## What it is
A single-page, dark, terminal-dense static dashboard Justin can actually use.
Personal-use dashboard over the UnSilo intel corpus (career-hunting intel core,
Public Recruiting State v1 scope). Read-only. No harness implementation in scope.

## Copy rules (load-bearing, do not violate)
- No em dashes anywhere in people-facing copy. Use hyphens or periods.
- Terse, technically dense. Short flat sentences. No AI slop, no purple prose.
- All dates in 12-hour AM/PM ET. Date-stamp every feed item.

## Layout (single page, dense, scannable)
1. **Header**: UNISILO / intel feed. Tagline: "the people's anti-palantir" (Justin's words).
   Subline: absence as signal. What institutions don't publish is first-class data.
2. **BLOCKERS strip (top)**: open blockers only, each with falsifier + owner.
   (Justin's standing rule: blockers lead, head and tail of every project message.)
3. **Applications tracker**: 7 cards, one per filing. Status pill (submitted / held /
   action-needed), platform, req/job id, key terms, and any open action item.
4. **Intel feed**: reverse-chronological. Filter chips by tag
   (applications, forensics, audits, research-chain, surfaces). Search box over
   title + body. Each item: date, tag, title, 1-3 line body, verdict pills where
   applicable (CONFIRMED / KILLED / DOWNGRADED / UNKNOWN).
5. **Research surfaces**: Tier 0-4 compact list with GREEN/YELLOW/RED handling notes.
6. **BLOCKERS strip repeated (bottom)** — same strip, head and tail.

## Data (embed verbatim as static JSON, verify against sources before build)

### Blockers (true state as of 2026-10-02 ~2:00 AM ET; corrected from stale ledger)

Research chain (harness program; dashboard surfaces these read-only):
- FROZEN under reconstructed authority: B2, B3, B4, B7, B8.
- REPAIRED-PENDING-ADMISSION: B1, B9. Repair output exists and is sound;
  the admission that froze them was procedurally invalid (contaminated
  package in chat 6abe1a5b: split typed-expression line, dropped
  blocker/completion-impact line, altered "NONE." to "NONE evaluated."),
  freeze retracted 2026-10-01 7:00 AM.
- OPEN: B10. All B10 work after the bad B1/B9 admission is quarantined as
  provisional (second ACCEPT used authored fixtures, not executed receipts).
- RETAINED-INTEGRATION-VERIFIED: B5, B6. RETAINED: B11, B12.
- UNADMITTED: RECON-ECLASS-PD-AO-DD-v2.0 classifier dependency. Every
  CLASSIFY path yields ABSTENTION until admitted.
- ORIGINALS_RECOVERED = PARTIAL. Still missing: 40 Wave-7 question texts,
  12 B10 assertion texts, full S1/S2/S3/S4/S6/S8/S9 sessions, pinned
  admission contract, complete glossary, raw P1-P4.
- Authority gate: DECIDED 2026-10-01. Option B: RECONSTRUCTED-AUTHORITY
  SEMANTIC COMPLETE. Original-authority completion unreachable; v1 spec
  rebuilds as labeled RECONSTRUCTED artifacts, never called original or
  recovered. Missing originals stay permanent evidence unknowns.
- Build authorization: NONE, has never been anything else. S11/S12 gated
  behind chain completion. Pending remediation sequence runs
  ledger-erratum first; nothing in UnSilo needs the operator tonight.

Dashboard build (this spec's scope):
- Superhuman B4: Form D reconciliation OPEN (RuntimeWire $746.8M vs EDGAR-parsed
  $335.2M primary-backed figure). Falsifier: enumerate all 12 Form D/D-A filings
  for CIK 0002033975. Owner: coordinator/worker.
- Superhuman B1: LinkedIn authwall OPEN. Falsifier: logged-in browser pass.
  Owner: main agent (live browser).
- Superhuman B3: intern interview loop OPEN, no public signal. Falsifier: recruiter
  outreach or former-intern write-up. Owner: future.

### Applications (all status as of 2026-10-02)
1. Duolingo — SUBMITTED 2026-09-29. req 1265.
2. Palantir — SUBMITTED 2026-10-01 ~9:31 PM ET. FD SWE Intern Commercial NYC (Lever).
   Delta-vs-Dev track confirmed. Three numbers 2/8/5.
3. Superhuman — SUBMITTED 2026-10-01 ~9:39 PM ET. SWE Intern Summer 2027 NY hub
   (Ashby). $50/hr + $8K stipend, 12 weeks.
4. IBM — SUBMITTED 2026-10-01 ~9:52 PM ET. AI Foundations SWE Research Internship
   2027, Job ID 131307, Yorktown Heights. ACTION: assessment-process email arrived
   ~10:30 PM ET; accommodation form is the only immediate action item.
5. Cloudflare — SUBMITTED 2026-10-01 ~10:27 PM ET. SWE Intern 2027 Austin TX,
   Greenhouse 8199958, full-stack. User-authored cover letter.
6. Datadog — HELD FOR REVIEW (not submitted). SWE Intern Summer NYC, May 24-Aug 27
   2027, job 8052118 / req R20978. Backend 1st, Distributed Systems 2nd,
   Infrastructure 3rd. ACTION: why-Datadog rewrite awaiting his yes; two
   certification boxes for him to read and check himself.
7. NVIDIA — SUBMITTED 2026-10-02 ~12:21 AM ET (by Justin himself). 2027 Internships
   Systems Software Engineering, Santa Clara CA, req JR2023492. NVIDIA-tuned resume
   (C-first/systems, no CUDA-C++-kernel claims). Areas: Systems SW / Computer Arch /
   Security. Codeberg URL per standing pref.

### Feed items (reverse chron)
- 2026-10-02: NVIDIA filed. Systems SW intern, req JR2023492. 7th application live.
- 2026-10-01: Five filings in one night. Palantir, Superhuman, IBM, Cloudflare
  submitted; Datadog filled and held for his review. IBM assessment email landed
  the same night.
- 2026-10-01: Superhuman 6-lane targeting run closed. Lane 2 company profile,
  lane 5 public-API gauntlet, lane 6 Gemini corroboration (external content, verify
  before citing). B4 Form D reconciliation stays open: carry $335.2M primary-backed,
  never cite $746.8M as a raise total. B2 closed: Ashby form read live, no GPA
  field, no essays; LinkedIn profile is part of the application.
- 2026-09-30: UnSilo named and positioned. Justin verbatim: "we are the people's
  anti palantir. we are meta's meta. we track and we analyze using what they give
  us and what they dont." Shannon doctrine: "everything that isn't 0 is data."
  Research surfaces baseline catalog: Tier 0 compelled disclosure (FOIA, court
  records, Congress.gov), Tier 1 official datasets (EDGAR, FEC, DOL H-1B, OSHA,
  USASpending, ICIJ, ProPublica 990s, lobbying disclosures, property assessors),
  Tier 2 passive exhaust (Common Crawl, Wayback CDX, dorking, CT logs, DNS),
  Tier 3 visitor-level site-native, Tier 4 gray/verify-only. RED: hard lines,
  never in scope. Gray-surface rule: exposure verification is metadata only,
  never download content.
- 2026-09-29: 23-company adversarial audit gate. 555 claims checked, 9 KILLED,
  31 DOWNGRADED, 188 CONFIRMED load-bearing, 127 UNRESOLVED. Verdicts: 11 sound,
  12 needs-patches, 0 systematically unreliable. Consequential kills: TikTok
  counts (65 not 67, 8 new-grad rows not 9), Epic OSS superlative belongs to
  Goldman (73 repos vs 56), Motorola campus-geography claim wrong (campus is
  New Paltz NY), Vanguard citizenship inference struck, Amazon 61% junior funnel
  retirement does not hold at :161.
- 2026-09-29: Duolingo forensic findings + application packet. req 1265 filed.
- Research chain: S1-S10 ran Sep 30-Oct 1 plus repair round (Worker-1R3
  admitted, Foundation v2 admitted as governing baseline). True blocker
  state 2026-10-02: FROZEN B2/B3/B4/B7/B8; REPAIRED-PENDING-ADMISSION B1/B9
  (freeze retracted, contaminated admission package); OPEN B10 (later work
  quarantined provisional); RETAINED B5/B6/B11/B12; classifier UNADMITTED
  (CLASSIFY yields ABSTENTION); ORIGINALS_RECOVERED = PARTIAL. Authority
  gate decided Oct 1: Option B, RECONSTRUCTED-AUTHORITY SEMANTIC COMPLETE.
  S11 (WARN) + S12 (H-1B) gated behind chain completion. Build authorization
  NONE. Pending: ledger erratum first, then remediation sequence.

### Research surfaces (Tier 0-4, compact)
Tier 0 (GREEN, compelled): FOIA/state records, court records (RECAP/CourtListener),
Congress.gov API v3. Tier 1 (GREEN, official datasets): EDGAR, FEC, DOL H-1B,
OSHA, USASpending/SAM.gov, ICIJ leaks, ProPublica Nonprofit Explorer, Senate
lobbying disclosures, property assessors. Tier 2 (GREEN, passive exhaust):
Common Crawl, Wayback CDX, search dorking, CT logs (crt.sh), DNS/reverse-whois/ASN.
Tier 3 (GREEN, ToS-aware): visitor-level site-native. Tier 4 (YELLOW): verify-only,
metadata never content, never download. RED: hard lines, never in scope.

## Style
Dark page, near-black background, green/amber accent on monospace type. Dense
data tables and cards, not hero sections. No stock imagery. Mobile-readable.
Everything on one screen family, no multi-page nav.

## Acceptance
- Every fact above appears exactly as written (dates, numbers, req IDs).
- No em dashes in copy.
- Blockers appear at top AND bottom.
- Filters and search work on the feed.

## Implementation stack (reconciled 2026-10-02)
Rust: Axum 0.8 + Askama + htmx, rusqlite bundled, musl static binary. Full
rationale, kill criteria, and adopted prior-art patterns live in
unsilo-data-theory-2026-10-02.md section 9. This spec describes WHAT the
dashboard shows; the theory doc describes HOW it is built. Claude implements
from both.
