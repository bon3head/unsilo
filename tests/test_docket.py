"""Docket acceptance tests. Run: .venv/bin/python -m unittest discover -s tests -v

The seed tests need the Duolingo packet in var/inbox/ (local only); they skip
with a stated reason when it is absent.
"""
import asyncio
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import apsw

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from unsilo import db, ledger, temporal  # noqa: E402
from unsilo.docket import packet, queries as Q  # noqa: E402
from unsilo.docket.records import Docket  # noqa: E402
from unsilo.docket.seed import PACKET, seed  # noqa: E402
from unsilo.temporal import End  # noqa: E402

HAVE_PACKET = PACKET.exists()


def fresh(tmp):
    return db.open_store(Path(tmp) / "t.db")


class Clock:
    def __init__(self):
        self.t = 0

    def __call__(self):
        self.t += 1
        return f"2026-10-02T12:{self.t // 60:02d}:{self.t % 60:02d}Z"


class Migrations(unittest.TestCase):
    def test_generated_migrations_are_current(self):
        r = subprocess.run([sys.executable, str(REPO / "tools" / "gen_migrations.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_fresh_store_passes_gates(self):
        with tempfile.TemporaryDirectory() as t:
            facts = db.gates(fresh(t))
            self.assertEqual(facts["sqlite"], "3.53.4")
            self.assertEqual(facts["tzdata"], "2026.4")
            self.assertEqual(facts["ledger"]["receipts"], 0)

    def test_changed_migration_bytes_halt(self):
        with tempfile.TemporaryDirectory() as t:
            conn = fresh(t)
            conn.execute("PRAGMA writable_schema = 0").fetchall()
            files = db.migration_files()
            orig = db.migration_files
            try:
                db.migration_files = lambda: [(v, n, b + (b"\n-- tampered" if v == 2 else b"")) for v, n, b in files]
                with self.assertRaises(db.Halt):
                    db.gates(conn)
            finally:
                db.migration_files = orig


class WritePath(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = fresh(self.tmp.name)
        self.w = ledger.Writer(self.conn, "test", Clock())
        self.dk = Docket(self.w)
        with self.w.tx():
            self.i = self.dk.day("2026-10-01", "Oct 1")

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def blocked(self, sql, bindings=()):
        with self.assertRaises(apsw.Error):
            self.conn.execute(sql, bindings).fetchall()

    def test_no_update_no_delete_anywhere(self):
        tables = ledger.receipted_tables(self.conn) + ["meta_receipt", "meta_migration", "meta_contract_status", "meta_cut"]
        trig = {r[0] for r in self.conn.execute("SELECT name FROM sqlite_schema WHERE type = 'trigger'").fetchall()}
        for t in tables:
            self.assertIn(f"{t}_no_update", trig)
            self.assertIn(f"{t}_no_delete", trig)
            if self.conn.execute(f"SELECT count(*) FROM {t}").fetchall()[0][0]:  # triggers fire only on rows
                self.blocked(f"UPDATE {t} SET rowid = rowid")
                self.blocked(f"DELETE FROM {t}")

    def test_row_must_equal_receipt_image(self):
        with self.assertRaises(apsw.Error):
            with self.w.tx():
                self.conn.execute("INSERT INTO core_instant (instant_id, kind, source_text, receipt_id) VALUES (2, 'UNKNOWN', 'x', 1)").fetchall()

    def test_after_hash_trigger(self):
        with self.assertRaises(apsw.Error):
            with self.w.tx():
                self.conn.execute(
                    "INSERT INTO meta_receipt (receipt_id, table_name, row_pk, op, actor, reason, before_kind, after_sha256,"
                    " after_image_json, prev_kind, prev_receipt_sha256, receipt_sha256, recorded_at)"
                    " SELECT 2, 'core_instant', 2, 'INSERT', 'x', 'x', 'ABSENT', ?, '{}', 'HASH', receipt_sha256, ?, '2026-10-02T13:00:00Z'"
                    " FROM meta_receipt WHERE receipt_id = 1", ("0" * 64, "1" * 64)).fetchall()

    def test_chain_and_sequence(self):
        with self.assertRaises(apsw.Error):
            with self.w.tx():
                self.conn.execute(
                    "INSERT INTO meta_receipt (receipt_id, table_name, row_pk, op, actor, reason, before_kind, after_sha256,"
                    " after_image_json, prev_kind, prev_receipt_sha256, receipt_sha256, recorded_at)"
                    " VALUES (2, 'core_instant', 2, 'INSERT', 'x', 'x', 'ABSENT', sha256_hex('{}'), '{}', 'HASH', ?, ?, '2026-10-02T13:00:00Z')",
                    ("f" * 64, "2" * 64)).fetchall()

    def test_unjoined_claim_only_unresolved(self):
        with self.assertRaises(apsw.Error):
            with self.w.tx():
                c = self.dk.claim("X", "a claim")
                self.dk.verdict(c, "KILLED", self.i, "t", "r")
        with self.w.tx():
            c = self.dk.claim("X", "a claim")
            self.dk.verdict(c, "UNRESOLVED", self.i, "t", "r")

    def test_eclass_abstains_while_unadmitted(self):
        with self.w.tx():
            c = self.dk.claim("X", "a claim")
        with self.assertRaises(apsw.Error):
            with self.w.tx():
                self.w.insert("core_claim_eclass", {"claim_id": c, "contract_id": "RECON-ECLASS-PD-AO-DD-v2.0",
                                                    "state": "ADMITTED", "class": "PD", "weak": 0}, "t")

    def test_no_em_dash_in_notes(self):
        with self.assertRaises(apsw.Error):
            with self.w.tx():
                self.dk.note("build", "a — b", "body", self.i)

    def test_interval_validity_lifted(self):
        with self.assertRaises(ValueError):
            with self.w.tx():
                self.dk.interval(End("KNOWN", "2026-10-02", "DAY", "America/New_York"),
                                 End("KNOWN", "2026-10-02T03:00:00Z", "SECOND", "UTC"))  # 3:00Z is before ET midnight (4:00Z)
        with self.assertRaises(ValueError):
            with self.w.tx():
                self.dk.interval(End("KNOWN", "2026-10-01", "DAY", "FLOATING"),
                                 End("KNOWN", "2026-10-03T00:00:00Z", "SECOND", "UTC"))

    def test_verify_detects_nothing_on_clean_ledger(self):
        self.assertEqual(ledger.verify_ledger(self.conn)["receipts"], 1)


@unittest.skipUnless(HAVE_PACKET, "Duolingo packet not in var/inbox/ (local-only file)")
class SeedAndReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.conn = fresh(cls.tmp.name)
        w = ledger.Writer(cls.conn, "seed", Clock())
        with w.tx():
            cls.out = seed(Docket(w))
        cls.p = {"k": "2026-10-02T23:59:59Z", "eff_value": "2026-10-02", "eff_gran": "DAY", "eff_zone": "America/New_York"}

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        cls.tmp.cleanup()

    def test_packet_hash_and_allowlist(self):
        data = PACKET.read_bytes()
        import hashlib
        self.assertTrue(hashlib.sha256(data).hexdigest().startswith("0b8f184a"))
        self.assertEqual(self.out["packet"]["lines_total"], 129)
        self.assertEqual(self.out["packet"]["lines_kept"], 11)

    def test_no_personal_fields_in_store(self):
        # Forbidden strings are derived from the packet at test time, so no
        # personal value or outreach name is ever written into the repo.
        dump = ledger.canonical_dump(self.conn).decode()
        text = PACKET.read_text(encoding="utf-8")
        kept = {no for no, *_ in packet.parse(PACKET.read_bytes())[1]}
        forbidden = set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text))
        forbidden |= set(re.findall(r"\(\d{3}\) \d{3}-\d{4}", text))
        forbidden |= set(re.findall(r"GPA[^|]*?\|\s*([0-9.]+)", text))
        forbidden |= set(re.findall(r"([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?) \(", text.split("**Outreach targets")[1].split("\n")[0]))
        forbidden |= set(re.findall(r"\b[A-Z]{5,}\d{4,}\b", text))
        self.assertGreaterEqual(len(forbidden), 6)
        for f in forbidden:
            self.assertNotIn(f, dump)
        for no, line in enumerate(text.split("\n"), start=1):
            if no not in kept and len(line.strip()) >= 24:
                self.assertNotIn(line.strip(), dump, f"packet line {no} leaked")

    def test_seven_applications_with_spec_facts(self):
        apps = Q.run(self.conn, "applications", self.p)
        self.assertEqual([a["employer_label"] for a in apps],
                         ["Duolingo", "Palantir", "Superhuman", "IBM", "Cloudflare", "Datadog", "NVIDIA"])
        terms = Q.run(self.conn, "terms", self.p)
        reqs = {t["text_value"] for t in terms if t["term_key"] == "req_ref" and t["value_kind"] == "TEXT"}
        self.assertEqual(reqs, {"1265", "131307", "8199958", "8052118 / R20978", "JR2023492"})
        status = {a["employer_label"]: a["status"] for a in apps}
        self.assertEqual(status["Datadog"], "HELD_FOR_REVIEW")
        self.assertEqual(sum(1 for s in status.values() if s == "SUBMITTED"), 6)

    def test_strip_and_honest_states(self):
        rows = Q.run(self.conn, "blockers", self.p)
        strip = [r for r in rows if not r["is_terminal"] and r["in_effect"] != "FALSE"]
        codes = {(r["program"], r["code"]) for r in strip}
        self.assertIn(("RESEARCH_CHAIN", "B1"), codes)
        self.assertIn(("RESEARCH_CHAIN", "RECON-ECLASS-PD-AO-DD-v2.0"), codes)
        self.assertNotIn(("RESEARCH_CHAIN", "B4"), codes)  # FROZEN is terminal (R21)
        self.assertNotIn(("SUPERHUMAN_TARGETING", "B2"), codes)  # CLOSED
        b1 = [r for r in rows if r["code"] == "B1" and r["program"] == "RESEARCH_CHAIN"][0]
        self.assertEqual((b1["state"], b1["head_count"], b1["history_len"]), ("REPAIRED_PENDING_ADMISSION", 1, 2))

    def test_bitemporal_knowledge_cut(self):
        empty = dict(self.p, k="2026-10-02T11:00:00Z")  # before the first receipt
        self.assertEqual(Q.run(self.conn, "applications", empty), [])

    def test_contract_gate_agrees_with_docket(self):
        self.assertEqual({r["agreement"] for r in Q.run(self.conn, "contract_check", self.p)}, {"AGREE"})

    def test_replay_is_byte_identical(self):
        r = ledger.replay(self.conn, Path(self.tmp.name) / "replay.db")
        self.assertTrue(r["identical"], r)

    def test_dashboard_renders_honestly(self):
        from unsilo.web.app import create_app
        app = create_app(Path(self.tmp.name) / "t.db", clock=lambda: "2026-10-02T23:00:00Z")

        async def get(path, qs=b""):
            msgs = []

            async def receive():
                return {"type": "http.request", "body": b""}

            async def send(m):
                msgs.append(m)
            await app({"type": "http", "method": "GET", "path": path, "query_string": qs, "headers": [], "root_path": ""}, receive, send)
            return msgs[0]["status"], b"".join(m.get("body", b"") for m in msgs[1:]).decode()
        status, page = asyncio.run(get("/"))
        self.assertEqual(status, 200)
        self.assertEqual(page.count('aria-label="Blockers ('), 2)  # top AND bottom
        self.assertEqual(page.count('<article class="card">'), 7)
        self.assertNotIn("—", page)
        self.assertIn("ABSTENTION(CLASSIFIER_NOT_ADMITTED)", page)
        self.assertIn("UNRESOLVED", page)
        self.assertIn("Cut: effective Oct 2, 2026", page)
        status, frag = asyncio.run(get("/feed", b"tag=audits&q=tiktok"))
        self.assertEqual(frag.count("<li>"), 2)


class Temporal(unittest.TestCase):
    def test_dst_lifting(self):
        for day, hours in (("2026-03-08", 23), ("2026-11-01", 25), ("2026-09-30", 24)):
            kind, lo, hi = temporal.lift_cut(temporal.Cut(day, "DAY", "America/New_York"))
            self.assertEqual((hi - lo) // 3600, hours)

    def test_floating_is_unknown_across_zones(self):
        t, r = temporal.membership(End("KNOWN", "2026-01-01", "DAY", "FLOATING"), End("UNBOUNDED"),
                                   temporal.Cut("2026-10-02", "DAY", "America/New_York"))
        self.assertEqual((t, r), ("UNKNOWN", "FLOATING_ZONE_NOT_COMPARABLE"))


if __name__ == "__main__":
    unittest.main()
