# PoC results — 2026-09-30 ~6:50 PM ET (run while S1 in flight)

## P1: Wayback CDX probe — CONFIRMED
Query: `url=duolingo.com/careers*`, limit 5. Returned real captures: timestamps
(2019–2025), status codes (200/301/404), digests, byte lengths. Query-param URLs are
captured as distinct entries (department filters). Feeds S2: enumeration must handle
URL variants, non-200 captures are first-class records, not errors.

## P2: SEC EDGAR probe — CONFIRMED (with constraint)
`company_tickers.json` + `data.sec.gov/submissions/CIK0001562088.json`: Duolingo, Inc.,
776 recent filings, forms/dates returned. CONSTRAINT FOUND: SEC silently returns empty
body without a descriptive User-Agent header — bare requests fail closed with no error.
Acquisition layer must set UA per SEC fair-access rules; this is a real enumerated
hazard for S2, not an assumption.

## P3: temporal bound algebra — CONFIRMED (B4 rationale)
256 bound combinations over {KNOWN, UNBOUNDED, UNKNOWN} x [from,to): only 16
determinate; any non-KNOWN bound forces overlap to UNKNOWN. Mechanical confirmation
that nullable endpoints conflate unknown with unbounded. Feeds S3.

## P4: SQLite adversarial fixtures — ALL FOUR HAZARDS CONFIRMED LIVE
- STRICT table rejects TEXT into INTEGER (IntegrityError) — STRICT works as claimed.
- FK off by default: orphan row inserted, `PRAGMA foreign_keys = 0` — B11's FK-on
  connection invariant is load-bearing, not belt-and-braces.
- Fan-out: 1x3 join yields 3 rows — anti-fan-out grain rules required.
- REAL 0.1+0.2 = 0.30000000000000004 — exact-arithmetic policy required for money.
Feeds S6.

## Folklore kill log
(none yet — PoCs confirmed rather than killed; EDGAR UA behavior was an unknown, now a
confirmed constraint)
