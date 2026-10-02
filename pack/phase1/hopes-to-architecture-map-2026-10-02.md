# UnSilo hopes-to-architecture map (2026-10-02)

Analysis, not a build plan. Build authorization: NONE.

## Blockers (lead)

| Blocker | Effect on this map | Falsifier | Owner |
|---|---|---|---|
| RECON-ECLASS-PD-AO-DD-v2.0 UNADMITTED | Every evidence-class label below is the class the claim WOULD take; none is admitted. Every CLASSIFY path returns ABSTENTION(CLASSIFIER_NOT_ADMITTED). | fresh admission ACCEPT | harness program |
| B1, B9 REPAIRED-PENDING-ADMISSION; B10 OPEN | No v1 query result is admissible VALUE yet. "Determinism" and the B12 render are not established. | valid B1/B9 admission, then B10 freeze | harness program |
| QN availability: ALL source scopes UNKNOWN (B5/B6 checkpoint, ledger 3:28 AM) | Every "absence" hope is UR in practice until acquisition receipts exist | first receipted acquisition run passing B5/B6 | harness program |
| Build authorization NONE | No hope below is buildable today, including v1 | operator decision | operator |
| Stack conflict: your constraint says TypeScript/Python; the approved dashboard baseline is Rust; your frontend list is React | Every UI mapping depends on this ruling | operator ruling | operator |

## Legend

- Mapping: (a) grounded element in current contracts; (b) explicit deferral with the dependency named; (c) cut with the reason.
- Tier: v1, v1.1, platform, cut.
- Strength of an (a) mapping: GROUNDED = a frozen or retained contract plus an in-scope source; WEAK = the contract exists but a dependency is open or unadmitted, or the runtime evidence does not exist. Most (a) mappings are WEAK today because of the blockers above. That is stated per row, not hidden.
- Contract shorthand: S1 claim and classes; S2 sources and H∪D∪R; S3/B4 temporal (B4 FROZEN); S4 QN and completeness (B5/B6 retained); S5/B7 schema and vocabulary (B7 FROZEN); B8 identity registry (FROZEN); S6/B11 SQLite (retained); S7/B10 closure (OPEN) and B12 counterevidence (retained); S8/B1, B9 query and operators (pending admission); S9/B2, B3 comparison (FROZEN).

## 0. Correction to your v1 shape statement

You wrote `RecruitingState(t)`. The frozen claim is `PublicRecruitingState(C, T, S)` (S1): company C, time T, and declared source scope S are all parameters. Dropping C and S is not cosmetic. S8 makes a query with no declared scope malformed (REJECT), and S1 makes coverage (O) a property of the evidence under S, not of the company. Every view below inherits that: no number exists without its company, time cut, and declared scope.

## 1. The dream

| # | Hope | Map | Tier | Mechanism, or the reason |
|---|---|---|---|---|
| D1 | "People's anti-Palantir", "meta's meta", personal power, looking back at the overlords | (c) | cut as requirement | Positioning, not a capability. No contract can implement or test it. Keep it as copy; it creates no obligation. |
| D2 | "Track using what they give us" | (a) WEAK | v1 | S1 classes PD (careers H∪D∪R, delegated public ATS, EDGAR registrant filings) and AO (Wayback CDX captures). Sources S2. WEAK: classes unadmitted; no acquisition run exists. |
| D3 | "and what they don't": absence as signal | (a) WEAK | v1 | S4 QN master rule: `QN(P) ⟺ CompleteWithinScope ∧ NegativeCheck=0 ∧ TemporalAdmissible ∧ PWithinClosedWorld`; B9 QUALIFIED_NON_OBSERVATION (pending). The claim is always "not observed in scope Q within W", never "does not exist". WEAK: QN is UNKNOWN for every source scope until receipted runs exist. |
| D4 | "Everything that isn't 0 is data" | (a) with correction | v1 | Harness spec v1.2 already corrected this: absence is signal only under an expectation. Mechanism: an expectation row naming what should exist and the dataset checked (proposed `core_expectation` in the dashboard schema; Expectation/SourceCheck in harness spec section 7, not a frozen contract). Without an expectation, a zero is not data; it is nothing. |
| D5 | "The most surprising event carries the most bits; measure the shape of the missingness" | (c) quantitative form | cut | Surprisal needs a probability model. The standing rule is categorical only, no numerical probability-style confidence. What survives: categorical ordering of absences by expectation basis (mandated, stated, routine, operator). "Shape of missingness" survives as field-completeness grids (V6 below), which are counts, not surprisal. |
| D6 | Forensic recon on data-rich companies | (b) | platform | Depends on: build authorization for the harness; Tier 0 to 2 adapters beyond the v1 three (harness spec D3 "promote on demand"); B8 identity binding for non-SEC sources; the ER service (harness Phase 2). None is authorized. |
| D7 | Forensic recon on high-power individuals | (c) | cut | `Person` is a deferred entity (harness spec 8); "private-person dossiers" and "named-person recon" are on the killed and dream lists (harness spec 1; blockers file triage). No contract defines identity for a person (B8 is company-only: CIK or opaque company ID). Legal exposure under state privacy and data-broker laws is real even for private use (WEAK: not legally researched here). |
| D8 | Disclosed financial graphs | (b) | platform | Depends on: harness Relationship/Event types with evidence for both ends (harness spec 8, not built); money as exact integer minor units (S6, frozen); procurement and spending adapters (USASpending, SAM.gov are promotion queue); "disclosed-money graph" is explicitly dream (blockers file). |
| D9 | Confidence-scored connections | (c) | cut | Directly contradicts the categorical evidence-class rule (S1; Foundation v2 "categorical, never scores"; README "no numerical probability-style confidence anywhere"). Harness spec 11: similarity scores are not probabilities and thresholds are never defaults. The honest replacement already exists: PD/AO/DD/QN/UR plus WEAK. |
| D10 | Strict-lockdown pipeline | (a) WEAK | v1 | Deterministic core with no model calls (harness spec 1, not authorized); fresh-admission gates (Foundation v2 Artifact 3); S6 fail-closed integrity gates; receipts (dashboard schema, proposed). WEAK: the harness is not authorized and B10 is OPEN. |
| D11 | Poison guardrails | (b) | platform | No contract defines an adversary. Harness spec v1.2 cut the ledger hash chain because there is "no adversary". Poisoning (fake postings, planted filings text, archive manipulation) needs a threat model first. Partial cover today: B12 forces conflicting evidence to be shown, and B8 forbids fuzzy identity, which blocks the cheapest poisoning path (name collision). Dependency: a written threat model, then contracts. |

## 2. The v1 shape

| # | Hope | Map | Tier | Mechanism |
|---|---|---|---|---|
| V0 | Public recruiting representation, not internal truth | (a) GROUNDED | v1 | S1 frozen claim; Foundation v2 scope. |
| V1-I | Inventory: observed posting set | (a) WEAK | v1 | S1 I; B7 POSTING-POPULATION-CONTRACT (FROZEN: identity hierarchy, mirrors, duplicates, locations, prospect postings, revisions); completeness S4 (Greenhouse `meta.total` reconciliation, Lever derived terminal rule, CDX resume-key exhaustion). Class PD (careers/ATS) or AO (CDX). WEAK: B1/B9 pending; no runs. |
| V1-Co | Composition: publisher-declared attributes | (a) WEAK | v1 | S1 Co; S5 B7.4 (raw labels, no silent rewrite); B9 GET_FIELD with FIELD_UNAVAILABLE propagation. Any inferred category: B7.5 requires a frozen classifier, and none is admitted, so ABSTENTION. |
| V1-L | Lifecycle: representation history | (a) WEAK | v1 | S1 L; B4 FROZEN (first-observed is not published; last-observed is not closure; captures do not bound continuity); B7 identity across observations. Disappearance is UR unless QN prerequisites hold at both cuts. |
| V1-D | Disclosure: publisher and registrant statements | (a) WEAK | v1 | S1 D; EDGAR (S2); B9 ADMIT_DISCLOSURE / EXTRACT_PROPOSITION returns "publisher stated X", never "X". S4 open unknown: content-level EDGAR claims need full-document acquisition and parsing, which no contract specifies yet. |
| V1-O | Observability: coverage qualification | (a) WEAK | v1 | S1 O; B5 SourceCheck, EnumerationProof, mandatory receipts (S2 per-fetch metadata list). Retained-integration-verified on paper; zero runtime receipts exist. |
| V2 | Sources: EDGAR, declared first-party careers, Wayback CDX | (a) GROUNDED | v1 | S2 per-source rules. Infra note: Duolingo's careers page needs JS (S2), so careers acquisition needs a headless browser on your laptop (Chromium/Playwright). Feasible without GPU; not currently in your stack list. |
| V3 | Public only, no logins | (a) GROUNDED, with a live contradiction | v1 | S2 excludes authenticated surfaces, social pages, and aggregators. Contradiction: the dashboard spec's own Superhuman blocker B1 names "logged-in browser pass" as its falsifier, and LinkedIn is outside H∪D∪R. That blocker is outside v1 by your own rule. Recommend re-scoping it as operator-manual, never ingested. |
| V4 | Determinism = same answer from identical admitted evidence | (a) WEAK | v1 | S1 definition; S7/B10 closure (OPEN); S8 ambient-state prohibition. Not established until B10 freezes. |
| V5 | Cut: actual hires, vacancy from counts, time-to-fill, ghost jobs, hiring-freeze intent, narrative headcount | (c) | cut | Confirmed against S1 kills (postings = hires, one posting = one opening, disappeared = filled, SEC silence = no hiring). "Session A cut all fifteen" is not verifiable from the repo: S1 records 11 kills. The cut stands on the S1 record either way. |
| V6 | The whole dream list out of v1 | (c) for v1 | cut from v1 | Blockers file triage: "Dream (out of v1's mouth)". Consistent. |
| V7 | Compensation deferred to v1.1 | (b) | v1.1 | Dependencies: B7 vocabulary entries for pay unit (hourly, annual, one-time) and currency; S6 exact integer money; per-source rule for where a range is a structured field vs free text. Note the conflict in section 4, V-comp. |

## 3. What you want to use it for

| # | Hope | Map | Tier | Mechanism, or the reason |
|---|---|---|---|---|
| U1 | Role surfacing | (a) WEAK, narrowed | v1 | Inventory plus raw publisher fields, filtered by a declared typed predicate (S8: the predicate is part of the query). Text search through FTS5 is allowed only as candidate retrieval (S6: FTS has zero authority; "no match" is never absence). |
| U2 | Targeting (ranking companies or roles for you) | (a) WEAK, narrowed | v1 | S9 ranking fence: ranking needs a declared ordering criterion in the closed query; an undeclared "rank by what obviously matters" is REJECT. So: you declare the criterion over published fields, the system sorts. Any "fit score" that infers seniority or role family from text is classification: ABSTENTION. |
| U3 | "Full company DNA" | (c) | cut | No mechanism; the phrase names no observable. Decomposed, the parts that map are V1-I, V1-Co, V1-L, V1-D, V1-O for one company. Everything else implied (culture, org chart, tech stack, strategy) has no source and no contract. |
| U4 | Closet: layoffs | (a) WEAK, narrow + (b) | v1 narrow; v1.1 WARN | v1: registrant statements in EDGAR (8-K, 10-K) are D-dimension PD, rendered as "registrant stated X", only where a filing says it. v1.1: WARN notices are S11, a separate source extension gated behind research-chain completion. SEC silence implies nothing (S1 kill 6). |
| U5 | Closet: lawsuits | (a) WEAK, narrow + (b) | v1 narrow; platform | v1: legal-proceedings statements inside EDGAR filings, as registrant statements. Court records (RECAP/CourtListener, Tier 0) are not a v1 source. Platform dependency: a court-record source contract plus B8 binding from party names to company identity (courts do not use CIKs; name-only matching is forbidden by B8.2). |
| U6 | Closet: bad conditions | (b) / (c) | platform / cut | OSHA (Tier 1) is not a v1 source: platform, with the same B8 binding dependency. Employee sentiment (review sites) is on the harness spec's killed list: cut. |
| U7 | Interview prep | (c) as architecture | cut | Not a system capability. You read V1-D and V1-Co outputs and prepare. Anything generative is a model call, which the deterministic core forbids (harness spec 1). The assistance inbox pattern exists only in the unauthorized harness spec. |
| U8 | Public-source direct-email outreach | (c) | cut | Finding a person's address is person-level data (D7, cut). Guessing address patterns is inference that no contract admits (S2 forbids guessed endpoints; the same logic applies). A recruiter address printed on an in-scope careers page is PD text, and you can read it; UnSilo should not harvest, store, or enumerate people's addresses. Outreach itself is yours (harness Tier 5: Cipher never sends). |
| U9 | Tangential forensic tasks for financial advantage | (c) | cut | "Personal investment/stock-picking" is on the harness spec's killed list. No contract supports market inference. |
| U10 | ... for personal advantage | (c) | cut | Names no observable, no source, no contract. |

## 4. The visualization list, adversarially

| # | View | Map | Tier | What is actually allowed |
|---|---|---|---|---|
| V-mom | Momentum: inventory time series | (a) WEAK | v1 | Points, not a line. Inventory exists only at observation cuts (S3: two captures do not establish continuity; S1 kill 9). Drawing a line between points asserts state between observations, which is folklore. Render discrete points with each point's completeness basis. "Gone quiet" is a non-observation: QN at best, UR today. Infra reality: Wayback rarely captures ATS JSON endpoints, so history for most companies starts when YOUR polling starts. Repeated polling needs a scheduler (cron on the VM); the harness spec says "no scheduler", so this is a small, real infra addition. |
| V-churn | New vs removed; posting lifespan | (a) WEAK | v1 | New and removed = B9 Difference at two cuts with identical pins (S8: one cut or unequal pins is REJECT). "Removed" is disappearance from an exhausted scope, cause unknown. "Lifespan first-seen to last-seen" is wrong by S3: that is the OBSERVED SPAN, a lower bound on nothing, because first-observed is not publication and last-observed is not closure. Rename it "observed span". |
| V-role | Role composition: families, seniority mix | split | families as published: v1; seniority and normalized families: (b) v1.1+ | Only raw publisher labels (Lever `categories.department`, Greenhouse departments, Schema.org `employmentUnit`) per company, not compared across companies without a vocabulary bridge (S9 ΔV). "Seniority mix" and "role families" across companies are classification: ABSTENTION(CLASSIFIER_NOT_ADMITTED). Dependency: an admitted classifier contract (B7.5) and RECON-ECLASS admission. This is the weakest leg of your "targeting engine". |
| V-geo | Geography, remote/hybrid/onsite | split | as-published table: v1; map: (b) v1.1+ | Location strings and workplace-type fields as published (Schema.org `jobLocationType`, ATS fields). A map needs coordinates, so geocoding is a mapping/classification step with no admitted contract, plus a geocoder and tiles (section 6). |
| V-comp | Compensation as disclosed | (b) | v1.1 | Conflicts with your own v1 cut. Technically a published range is a publisher-declared attribute (Co), but unit and currency normalization is a vocabulary decision (B7) not yet made. Honor your v1.1 ruling; remove it from the v1 view list. |
| V-cov | Archival coverage map: who is "dark" on Wayback | (a) WEAK, wording corrected | v1 | An exhausted CDX query with zero rows supports only "CDX returned no capture rows for query Q at time O" (S4 closed world = capture rows returned). It does not support "the company is dark", "the page never existed", or anything about the company. S1: O is a property of the evidence, not the company. Label the view as coverage of the archive, not of the companies. |
| V-fields | Field completeness: what postings carry vs omit | (a) GROUNDED in contracts, WEAK at runtime | v1 | The strongest absence view. A field absent from an acquired, parsed representation is directly observable in that representation (B9 FIELD_UNAVAILABLE; B1 field states UNAVAILABLE / NOT_ACQUIRED / MALFORMED / CONFLICTED, kept distinct). Cross-company comparison needs the same schema and vocabulary pins (S9). |
| V-wf | Workforce context from filings | (a) WEAK | v1 | Registrant human-capital statements (S1 cites 17 CFR 229.101(c)(2)(ii)); materiality-conditioned; rendered as "registrant stated". Needs full-document parsing (S4 open unknown). |
| V-not | Hires, headcount deltas, time-to-fill, ghost jobs, freeze intent | (c) | cut | Agreed. |
| V-closet | "Coverage gaps plus disclosures is the closet" | (c) for the coverage half | cut | Coverage gaps are properties of the archive and your acquisition, not of the company (S1 O). A dark Wayback record says nothing about layoffs or conditions. Only the disclosure half maps (U4, U5). Treating coverage gaps as the closet is the exact conflation S1 was written to prevent. |

## 5. The frontend list, adversarially

| # | Item | Map | Tier | Finding |
|---|---|---|---|---|
| F1 | Plottable as the charting layer | (c) | cut | Checked this session: last release 3.13.0 on 2021-11-22; last human commit 2023-01-09; since then only bot config commits (latest 2024-09-19); depends on `d3 ^4.13.0` (`package.json:67`). Dormant. "Top data-viz candidate" does not survive. If a JS chart layer is ever used, use D3 directly or a maintained library, by a fresh survey. |
| F2 | Blueprint for tables, filters, panels | (b) | blocked on stack ruling | Active (`@blueprintjs/core@6.21.0` tag), Apache-2.0. But it is React, which needs a JS build pipeline. The approved baseline is server-rendered Askama + vendored htmx, no build step, single static binary. You can have Blueprint or the approved stack, not both. Operator ruling. |
| F3 | MapLibre for geography | (b) | v1.1+ | BSD-3 (by its own repo; license not re-read this session). Needs vector tiles (a remote tile service breaks local-first; a self-hosted PMTiles file avoids a server) and geocoding (no admitted contract, see V-geo). Two dependencies before a single pin is honest. |
| F4 | SingleFile / Monolith offline evidence packages | (b) | after B10 | Monolith is CC0; SingleFile is AGPL-3.0 (read from both LICENSE files). An inlined HTML snapshot is a presentation export, not evidence: S7 killed "a screenshot is evidence", and a page snapshot is the same thing. The real evidence package is the B10 closure package (OPEN). Export can wrap a closure package later; it cannot stand in for one. |
| F5 | Absence views designed first | (a) WEAK | v1 | Agreed, with V-cov and V-fields wording. These are the most contract-backed UnSilo views. |
| F6 | B12 render | (a) WEAK | v1 | B12 retained; "one dependency world" needs B10 (OPEN). Until then the render can show support, counterevidence, and limitations from stored rows, but cannot claim a closed dependency world. |
| F7 | Lifecycle timelines on frozen B4 | (a) WEAK | v1 | Point membership is implemented in the proposed schema (`v_interval_membership`). Timelines must draw UNKNOWN endpoints as UNKNOWN, never as open bars to "now". |
| F8 | Cognitive scratchpad outside the relational substrate | (b) | v1.1 | No contract. "Round 2 confirmed pivot algebra can't express it" is not in the repo (UNVERIFIED). Required guard if built: scratchpad content never feeds a claim, view, count, or verdict (harness spec 10: identity decisions cannot be justified by the findings they support; Hypothesis is separate from findings). |
| F9 | Visual language: motion-heavy, cinematic | (c) for v1 | cut from v1 | Contradicts the dashboard spec: "single-page, dark, terminal-dense", "dense data tables and cards, not hero sections". Motion also fights the single static binary with no build step. Operator ruling if you want to change the spec. |
| F10 | "License posture: take whatever", GPL liftable | (c) as stated | needs ruling | Not in the repo. The pack, dated after 9/30, says AGPL is "concept-safe, code-hostile" and the word "steal" was scrubbed at your request (crawl report). Legally, GPL/AGPL obligations attach mainly to distribution or to serving other users; strictly private use triggers little (WEAK: not legal advice, not researched here). The binding problem is the conflict between the two records. Rule once, write it into the pack. |
| F11 | "Palantir's own libraries, the irony" | (c) | cut | Brochure framing. The tool choice must stand on maintenance and stack fit, and on that test F1 fails. |

## 6. Feasibility against your stack

| Need | Your stack | Verdict |
|---|---|---|
| EDGAR, CDX, ATS JSON over HTTPS | laptop + VM | fine; EDGAR 10 req/s and a User-Agent are mandatory (S2) |
| JS-rendered careers pages | not listed | needs headless Chromium; feasible, no GPU |
| Repeated observations for momentum | "no scheduler" (harness spec) | needs cron on the VM; trivial, but a real change |
| SQLite, FTS5, WAL | SQLite-first | fine; verified |
| Language | TypeScript/Python (yours, master doc directive 9) vs Rust (approved dashboard baseline) | conflict; must be ruled before any build |
| React UI (Blueprint) | approved baseline has no JS build | conflict |
| Maps | none | tiles plus geocoder; v1.1+ |
| Person and graph analytics | "no graph database" (harness spec) | fine for v1 (none needed); platform needs revisit |
| GPU | none | nothing above needs one; any model-based classifier would be run outside the core anyway |

## 7. Current architecture that serves no hope on your list

| Element | Where | Why it serves nothing listed |
|---|---|---|
| Tier 4 exposure verification (open buckets, Shodan/Censys, breach presence) | harness spec 7.6, research-surfaces catalog in the feed spec | No hope above needs it. Highest legal and ethical exposure in the whole pack. Recommend removing it from the catalog, not just marking it YELLOW. |
| Timing analysis (Phase 4: donations vs awards, permutation tests) | harness spec 14, 15 | Boston procurement legacy. Serves only the money-graph dream (D8). |
| Pivot algebra paths person→employer→vendor→contract, donor clusters | harness spec 12 | Same: money graph and person recon, both dream or cut. |
| Golden finding `repeated_supplier_cohort.v1` in the B10 acceptance artifacts | `PROVISIONAL-b10-acceptance-artifacts.txt` | Procurement domain, outside v1. Already quarantined; do not reuse it as a v1 fixture. |
| `core_research_surface` table | proposed dashboard schema | A static catalog; it measures nothing. Keep only if you want the list visible; otherwise it is a note, not a table. |
| B3 four-way change decomposition (predicate drift, ontic, ingestion, ER churn) | FROZEN | Serves a hope you did not list: comparing a company's state across schema or registry versions. It becomes necessary the first time your classifier or vocabulary changes under momentum or churn. Keep, but know it is latent until then. |

## 8. Conflicts needing your ruling

1. Stack: TypeScript/Python vs Rust vs React (sections 5, 6).
2. License posture: "take whatever" (your 9/30 call, not in the repo) vs "patterns only" (pack, 10/02).
3. Compensation: v1.1 (your text) vs in the v1 view list (your text).
4. Superhuman B1 "logged-in browser pass" vs "public only, no logins".
5. Visual register: cinematic vs terminal-dense spec.

## 9. Three highest-risk mappings

1. V-role / U2, the targeting engine. Everything you want from it (seniority mix, role families across companies, fit ranking) is classification, and no classifier is admitted. As built from current contracts it is per-company raw labels plus your declared sort. If the UI quietly normalizes titles, it re-commits S5 kill 41 ("we'll just normalize titles") and every downstream count becomes unlicensed.
2. V-mom, momentum. It will look like the core feature, but history mostly does not exist (Wayback rarely holds ATS JSON), points between observations are unknown, and "gone quiet" is UR until QN prerequisites hold. The pull to draw a smooth line is strong, and that line is folklore.
3. V-cov / V-closet, absence views read as company facts. "Dark on Wayback" and "the closet" both slide from a property of the archive to a property of the company. That slide is the single error S1, S4, and B12 exist to stop, and it is the easiest one to make in a view titled "absence".

## 10. Three hopes to kill outright

1. Confidence-scored connections (D9). It contradicts the categorical evidence-class doctrine the whole program rests on. Keep PD/AO/DD/QN/UR plus WEAK; never add a score.
2. Forensic recon on high-power individuals (D7), together with direct-email harvesting (U8). No person-identity contract exists or is planned for v1; it is on the killed list already; it carries the most legal risk; and it pulls the project from looking at institutions to looking at people.
3. "Full company DNA" (U3). It names no observable and invites every unsourced claim the folklore log was built to kill. Replace it with the five dimensions for one company, which is what v1 can honestly show.

Build authorization: NONE
