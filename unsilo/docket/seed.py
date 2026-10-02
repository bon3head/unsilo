"""Seed the Docket from the operator's records.

Sources (all cited per row in basis/source_text):
  SPEC   pack/unsilo-feed-dashboard-spec-2026-10-02.md (true state as of 2026-10-02 ~2:00 AM ET)
  MASTER pack/unsilo-master-architecture-prompt-2026-10-02.md sections 6-7
  PACKET var/inbox/duolingo-application-packet-2026-09-29.md (SHA-256 0b8f184a..., local only)
  EXEC   the operator's MISSION EXECUTE message, 2026-10-02
Facts are transcribed as written. Approximate times ("~9:31 PM ET") are KNOWN at
DAY with the wording kept (R14). Nothing absent from a source is filled in:
missing fields get explicit UNKNOWN rows.
"""
from __future__ import annotations

from pathlib import Path

from ..temporal import End
from . import packet
from .records import REPO, Docket

ET = "America/New_York"
SPEC = REPO / "pack" / "unsilo-feed-dashboard-spec-2026-10-02.md"
MASTER = REPO / "pack" / "unsilo-master-architecture-prompt-2026-10-02.md"
PACKET = REPO / "var" / "inbox" / "duolingo-application-packet-2026-09-29.md"

K = lambda v, g="DAY", z=ET: End("KNOWN", v, g, z)  # noqa: E731
UNK = End("UNKNOWN")
UNB = End("UNBOUNDED")

# (app_key, employer, status, day, time wording, actor, terms, platform)
APPS = [
    ("palantir", "Palantir", "SUBMITTED", "2026-10-01", "2026-10-01 ~9:31 PM ET", None, [
        ("role", "FD SWE Intern Commercial"), ("location", "NYC"), ("platform", "Lever"),
        ("track", "Delta-vs-Dev track confirmed"), ("note", "Three numbers 2/8/5")]),
    ("superhuman", "Superhuman", "SUBMITTED", "2026-10-01", "2026-10-01 ~9:39 PM ET", None, [
        ("role", "SWE Intern Summer 2027"), ("location", "NY hub"), ("platform", "Ashby"),
        ("pay", (5000, "USD", "HOUR", "$50/hr")), ("stipend", (800000, "USD", "ONE_TIME", "$8K stipend")),
        ("duration_weeks", (12, "12 weeks"))]),
    ("ibm", "IBM", "SUBMITTED", "2026-10-01", "2026-10-01 ~9:52 PM ET", None, [
        ("role", "AI Foundations SWE Research Internship 2027"), ("req_ref", "131307"),
        ("location", "Yorktown Heights")]),
    ("cloudflare", "Cloudflare", "SUBMITTED", "2026-10-01", "2026-10-01 ~10:27 PM ET", None, [
        ("role", "SWE Intern 2027"), ("location", "Austin TX"), ("platform", "Greenhouse"),
        ("req_ref", "8199958"), ("track", "full-stack"), ("materials", "User-authored cover letter")]),
    ("datadog", "Datadog", "HELD_FOR_REVIEW", "2026-10-01", "2026-10-01 (filled and held for his review)", None, [
        ("role", "SWE Intern Summer"), ("location", "NYC"), ("req_ref", "8052118 / R20978"),
        ("program_window", ("2027-05-24", "2027-08-27", "May 24-Aug 27 2027")),
        ("preference", "Backend 1st, Distributed Systems 2nd, Infrastructure 3rd")]),
    ("nvidia", "NVIDIA", "SUBMITTED", "2026-10-02", "2026-10-02 ~12:21 AM ET", "Justin", [
        ("role", "2027 Internships Systems Software Engineering"), ("location", "Santa Clara CA"),
        ("req_ref", "JR2023492"),
        ("materials", "NVIDIA-tuned resume (C-first/systems, no CUDA-C++-kernel claims). Codeberg URL per standing pref."),
        ("preference", "Areas: Systems SW / Computer Arch / Security")]),
]
REQUIRED_TERMS = ("role", "platform", "req_ref", "location")

RESEARCH_BLOCKERS = [
    ("B1", "Canonical QueryDefinition"), ("B2", "Cohort compatibility and composition"),
    ("B3", "Cross-version comparison"), ("B4", "Temporal semantics"), ("B5", "Acquisition prerequisites"),
    ("B6", "Constructor/write-admission prerequisites"), ("B7", "Ontology evolution and posting population"),
    ("B8", "Registry closure and ambiguous identity"), ("B9", "Operator type system"),
    ("B10", "Dependency closure and B12 integration"), ("B11", "SQLite safety"),
    ("B12", "Counterevidence invariant"),
    ("RECON-ECLASS-PD-AO-DD-v2.0", "Reconstructed evidence-class admission contract"),
]
STATE_OF = {"B2": "FROZEN", "B3": "FROZEN", "B4": "FROZEN", "B7": "FROZEN", "B8": "FROZEN",
            "B5": "RETAINED_INTEGRATION_VERIFIED", "B6": "RETAINED_INTEGRATION_VERIFIED",
            "B11": "RETAINED", "B12": "RETAINED", "B10": "OPEN", "RECON-ECLASS-PD-AO-DD-v2.0": "UNADMITTED"}
FALSIFIER_OF = {
    "B1": "valid fresh Sol/High admission ACCEPT that reuses the four retained extraction reports exactly (master section 7 steps 5-7)",
    "B9": "valid fresh Sol/High admission ACCEPT that reuses the four retained extraction reports exactly (master section 7 steps 5-7)",
    "B10": "reassessment after a valid B1/B9 ACCEPT, with executed verification receipts mapped (master section 7 steps 8-9)",
    "RECON-ECLASS-PD-AO-DD-v2.0": "separate fresh admission plus a Foundation v2 erratum (ruling D-2)",
    "B5": "runtime evidence from the D-3 acquisition run (architecture section 8.3)",
    "B6": "runtime evidence from the D-3 acquisition run (architecture section 8.3)",
    "B11": "fresh retained integration against the repaired baseline (master section 6)",
    "B12": "integration through B10 and comparisons (master section 6)",
}

NOTES = [  # (tag, day, title, body) verbatim from SPEC "Feed items"
    ("applications", "2026-10-02", "NVIDIA filed",
     "NVIDIA filed. Systems SW intern, req JR2023492. 7th application live."),
    ("applications", "2026-10-01", "Five filings in one night",
     "Five filings in one night. Palantir, Superhuman, IBM, Cloudflare submitted; Datadog filled and held for his review. IBM assessment email landed the same night."),
    ("forensics", "2026-10-01", "Superhuman 6-lane targeting run closed",
     "Superhuman 6-lane targeting run closed. Lane 2 company profile, lane 5 public-API gauntlet, lane 6 Gemini corroboration (external content, verify before citing). B4 Form D reconciliation stays open: carry $335.2M primary-backed, never cite $746.8M as a raise total. B2 closed: Ashby form read live, no GPA field, no essays; LinkedIn profile is part of the application."),
    ("surfaces", "2026-09-30", "UnSilo named and positioned",
     "UnSilo named and positioned. Justin verbatim: \"we are the people's anti palantir. we are meta's meta. we track and we analyze using what they give us and what they dont.\" Shannon doctrine: \"everything that isn't 0 is data.\" Research surfaces baseline catalog: Tier 0 compelled disclosure (FOIA, court records, Congress.gov), Tier 1 official datasets (EDGAR, FEC, DOL H-1B, OSHA, USASpending, ICIJ, ProPublica 990s, lobbying disclosures, property assessors), Tier 2 passive exhaust (Common Crawl, Wayback CDX, dorking, CT logs, DNS), Tier 3 visitor-level site-native, Tier 4 gray/verify-only. RED: hard lines, never in scope. Gray-surface rule: exposure verification is metadata only, never download content."),
    ("surfaces", "2026-09-30", "Research surfaces, Tier 0-4",
     "Tier 0 (GREEN, compelled): FOIA/state records, court records (RECAP/CourtListener), Congress.gov API v3. Tier 1 (GREEN, official datasets): EDGAR, FEC, DOL H-1B, OSHA, USASpending/SAM.gov, ICIJ leaks, ProPublica Nonprofit Explorer, Senate lobbying disclosures, property assessors. Tier 2 (GREEN, passive exhaust): Common Crawl, Wayback CDX, search dorking, CT logs (crt.sh), DNS/reverse-whois/ASN. Tier 3 (GREEN, ToS-aware): visitor-level site-native. Tier 4 (YELLOW): verify-only, metadata never content, never download. RED: hard lines, never in scope."),
    ("audits", "2026-09-29", "23-company adversarial audit gate",
     "23-company adversarial audit gate. 555 claims checked, 9 KILLED, 31 DOWNGRADED, 188 CONFIRMED load-bearing, 127 UNRESOLVED. Verdicts: 11 sound, 12 needs-patches, 0 systematically unreliable. Consequential kills: TikTok counts (65 not 67, 8 new-grad rows not 9), Epic OSS superlative belongs to Goldman (73 repos vs 56), Motorola campus-geography claim wrong (campus is New Paltz NY), Vanguard citizenship inference struck, Amazon 61% junior funnel retirement does not hold at :161."),
    ("forensics", "2026-09-29", "Duolingo forensic findings + application packet",
     "Duolingo forensic findings + application packet. req 1265 filed."),
    ("research-chain", "2026-10-01", "Research chain state",
     "S1-S10 ran Sep 30-Oct 1 plus repair round (Worker-1R3 admitted, Foundation v2 admitted as governing baseline). True blocker state 2026-10-02: FROZEN B2/B3/B4/B7/B8; REPAIRED-PENDING-ADMISSION B1/B9 (freeze retracted, contaminated admission package); OPEN B10 (later work quarantined provisional); RETAINED B5/B6/B11/B12; classifier UNADMITTED (CLASSIFY yields ABSTENTION); ORIGINALS_RECOVERED = PARTIAL. Authority gate decided Oct 1: Option B, RECONSTRUCTED-AUTHORITY SEMANTIC COMPLETE. S11 (WARN) + S12 (H-1B) gated behind chain completion. Build authorization NONE. Pending: ledger erratum first, then remediation sequence."),
]

KILLS = [  # SPEC audit line: reported KILLED; the audit export is not in hand
    ("TikTok", "TikTok counts: 67 (and 9 new-grad rows)", "TikTok counts (65 not 67, 8 new-grad rows not 9)"),
    ("Epic", "Epic OSS superlative", "Epic OSS superlative belongs to Goldman (73 repos vs 56)"),
    ("Motorola", "Motorola campus-geography claim", "Motorola campus-geography claim wrong (campus is New Paltz NY)"),
    ("Vanguard", "Vanguard citizenship inference", "Vanguard citizenship inference struck"),
    ("Amazon", "Amazon 61% junior funnel retirement", "Amazon 61% junior funnel retirement does not hold at :161"),
]
AUDIT_COUNTS = [("companies", 23), ("claims_checked", 555), ("KILLED", 9), ("DOWNGRADED", 31),
                ("CONFIRMED", 188), ("UNRESOLVED", 127), ("verdict_sound", 11),
                ("verdict_needs_patches", 12), ("verdict_systematically_unreliable", 0)]


def seed(dk: Docket, packet_path: Path = PACKET) -> dict:
    """Write the full seed. Caller holds the transaction."""
    spec = dk.artifact(SPEC, "REPO", "feed dashboard spec 2026-10-02")
    master = dk.artifact(MASTER, "REPO", "master architecture prompt 2026-10-02")
    asof = dk.day("2026-10-02", "true state as of 2026-10-02 ~2:00 AM ET (SPEC Blockers)")
    out = {"applications": {}}

    # Duolingo: everything comes through the packet import.
    pk = dk.artifact(packet_path, "LOCAL", "Duolingo application packet 2026-09-29", expect_prefix=packet.EXPECT_PREFIX)
    duo = dk.application("duolingo", "Duolingo")
    dk.term(duo, "platform", "Apply: https://careers.duolingo.com/jobs/8805925002 (ATS not established by the packet)",
            unknown=True, artifact_id=pk)
    out["packet"] = packet.import_packet(dk, packet_path, duo, pk)
    out["applications"]["duolingo"] = duo

    for key, label, status, day, wording, actor, terms in APPS:
        app = dk.application(key, label)
        ev = dk.day(day, wording)
        iv = dk.interval(K(day), UNK)
        dk.app_state(app, status, ev, iv, f"SPEC Applications: {wording}", actor=actor, artifact_id=spec)
        have = set()
        ordinals = {}
        for tkey, val in terms:
            have.add(tkey)
            ordinals[tkey] = ordinals.get(tkey, 0) + 1
            o = ordinals[tkey]
            if tkey in ("pay", "stipend"):
                amt, cur, unit, src = val
                dk.term(app, tkey, src, money=(amt, cur, unit), ordinal=o, artifact_id=spec)
            elif tkey == "duration_weeks":
                dk.term(app, tkey, val[1], integer=val[0], ordinal=o, artifact_id=spec)
            elif tkey == "program_window":
                start, through, src = val
                import datetime as dt
                end = (dt.date.fromisoformat(through) + dt.timedelta(days=1)).isoformat()
                pw = dk.interval(K(start), K(end))
                dk.term(app, tkey, src, interval_id=pw, ordinal=o, artifact_id=spec)
            else:
                dk.term(app, tkey, val, text=val, ordinal=o, artifact_id=spec)
        for req in REQUIRED_TERMS:
            if req not in have:
                dk.term(app, req, f"not stated in SPEC Applications entry for {label}", unknown=True, artifact_id=spec)
        out["applications"][key] = app

    apps = out["applications"]
    unk_due = dk.unknown_instant("no due date stated")
    for app, text in (
        (apps["ibm"], "Accommodation form (assessment-process email arrived ~10:30 PM ET); the only immediate action item"),
        (apps["datadog"], "Why-Datadog rewrite awaiting his yes"),
        (apps["datadog"], "Two certification boxes for him to read and check himself"),
    ):
        item = dk.action_item(text, "Justin", unk_due, application_id=app)
        dk.action_state(item, "OPEN", asof, "SPEC Applications")

    # Blockers: research chain (MASTER section 6-7; SPEC Blockers).
    blockers = {}
    for code, title in RESEARCH_BLOCKERS:
        b = dk.blocker("RESEARCH_CHAIN", code, title)
        blockers[("RESEARCH_CHAIN", code)] = b
        if code in ("B1", "B9"):
            frm = dk.day("2026-10-01", "2026-10-01 ~04:38 AM ET admission ACCEPT (MASTER section 7)")
            iv1 = dk.interval(K("2026-10-01"), K("2026-10-01T11:00:00Z", "SECOND", "UTC"))
            s1 = dk.blocker_state(b, "FROZEN", iv1, frm, "MASTER section 7: ledger recorded FROZEN after the ~04:38 AM ET ACCEPT", artifact_id=master)
            ret = dk.second("2026-10-01T11:00:00Z", "freeze retracted 2026-10-01 7:00 AM (ET)")
            iv2 = dk.interval(K("2026-10-01T11:00:00Z", "SECOND", "UTC"), UNK)
            dk.blocker_state(b, "REPAIRED_PENDING_ADMISSION", iv2, asof,
                             "MASTER section 7: admission procedurally non-admissible (contaminated package); freeze retracted 7:00 AM ET",
                             falsifier=FALSIFIER_OF[code], artifact_id=master, supersedes=s1)
            continue
        state = STATE_OF[code]
        if state == "FROZEN":
            iv = dk.interval(UNK, UNB, unbounded_basis="EXEC 2026-10-02: \"Frozen B2/B3/B4/B7/B8 are bedrock. Build on them, never through them.\"")
        else:
            iv = dk.interval(UNK, UNK)
        dk.blocker_state(b, state, iv, asof, "SPEC Blockers; MASTER section 6", falsifier=FALSIFIER_OF.get(code), artifact_id=master)

    # Superhuman targeting (SPEC "Dashboard build" blockers + feed item).
    sh = [("B4", "Form D reconciliation (RuntimeWire $746.8M vs EDGAR-parsed $335.2M primary-backed figure)", "OPEN",
           "enumerate all 12 Form D/D-A filings for CIK 0002033975", "coordinator/worker"),
          ("B1", "LinkedIn authwall", "OPEN", "logged-in browser pass", "main agent (live browser)"),
          ("B3", "Intern interview loop, no public signal", "OPEN", "recruiter outreach or former-intern write-up", "future"),
          ("B2", "Ashby application form fields", "CLOSED", None, None)]
    for code, title, state, fals, owner in sh:
        b = dk.blocker("SUPERHUMAN_TARGETING", code, title)
        blockers[("SUPERHUMAN_TARGETING", code)] = b
        if state == "CLOSED":
            closed = dk.day("2026-10-01", "2026-10-01 (SPEC feed: B2 closed)")
            iv = dk.interval(K("2026-10-01"), UNB, unbounded_basis="SPEC feed 2026-10-01: \"B2 closed: Ashby form read live\"")
            dk.blocker_state(b, "CLOSED", iv, closed, "SPEC feed: Ashby form read live, no GPA field, no essays; LinkedIn profile is part of the application", artifact_id=spec)
        else:
            dk.blocker_state(b, state, dk.interval(UNK, UNK), asof, "SPEC Blockers (Dashboard build)", falsifier=fals, owner=owner, artifact_id=spec)

    # Build blockers found while executing (2026-10-02).
    today = dk.day("2026-10-02", "observed in the build session 2026-10-02")
    for code, title, fals, owner, basis in (
        ("D3-NETWORK", "D-3 hosts denied by the environment network policy",
         "proxy CONNECT to boards-api.greenhouse.io, data.sec.gov and web.archive.org stops returning 403",
         "operator (cloud environment settings: Network access)",
         "probe 2026-10-02: gateway 403 on CONNECT for boards-api.greenhouse.io and data.sec.gov; web.archive.org no response"),
        ("B1B9-REPORTS", "Retained B1/B9 extraction reports not in hand",
         "the four retained reports (SHA-256 prefixes f584f159, 32163955, 85aa04a6, 10199d25) placed in var/readmission/",
         "operator",
         "repo and Drive searched 2026-10-02: only the quarantined transcriptions found"),
    ):
        b = dk.blocker("UNSILO_BUILD", code, title)
        blockers[("UNSILO_BUILD", code)] = b
        iv = dk.interval(K("2026-10-02"), UNK)
        dk.blocker_state(b, "OPEN", iv, today, basis, falsifier=fals, owner=owner)
    out["blockers"] = len(blockers)

    # Action items on blockers.
    for key, text, owner in (
        (("UNSILO_BUILD", "D3-NETWORK"), "Allow boards-api.greenhouse.io, data.sec.gov, web.archive.org (or broaden network access), then run: unsilo sweep-d3 --live", "operator"),
        (("UNSILO_BUILD", "B1B9-REPORTS"), "Place the four retained extraction reports in var/readmission/, then run: unsilo readmission build", "operator"),
        (("SUPERHUMAN_TARGETING", "B4"), "D-3 EDGAR enumeration of CIK 0002033975 lists the Form D/D-A filings (filing existence only)", "UnSilo D-3 run"),
    ):
        item = dk.action_item(text, owner, unk_due, blocker_id=blockers[key])
        dk.action_state(item, "OPEN", today, "build session 2026-10-02")

    # Notes (SPEC feed, verbatim).
    for tag, day, title, body in NOTES:
        dk.note(tag, title, body, dk.day(day, f"SPEC feed item {day}"), artifact_id=spec)

    # Audit 2026-09-29: counts as reported; the five named kills as findings.
    run = dk.audit_run(dk.day("2026-09-29", "SPEC feed item 2026-09-29"), "23-company adversarial audit gate")
    for k, v in AUDIT_COUNTS:
        dk.audit_count(run, k, v, "SPEC feed item 2026-09-29")
    decided = dk.day("2026-09-29", "audit 2026-09-29")
    for subject, claim_text, delta in KILLS:
        c = dk.claim(subject, claim_text)
        v = dk.verdict(c, "UNRESOLVED", decided, "audit gate 2026-09-29",
                       f"Audit reported KILLED: {delta}. Audit export not in hand, so the claim has no artifact and is UNRESOLVED by construction (R8).",
                       audit_run_id=run)
        dk.abstain_eclass(c)
        dk.audit_finding(run, c, v, "KILLED", delta)
    return out
