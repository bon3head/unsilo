"""The one write path, ledger verification, and replay-by-rebuild.

Every stg_/core_/ev_ row is written as: receipt (canonical after-image, hash,
chain link) then the row, inside one IMMEDIATE transaction. The database
re-checks the after-hash (DL-3 trigger) and the row-equals-image property
(generated per-table triggers). Nothing is ever updated or deleted.
"""
from __future__ import annotations

import json
import time
from contextlib import contextmanager
from pathlib import Path

import apsw

from . import canon, db

RECEIPT_HASHED = ("receipt_id", "table_name", "row_pk", "op", "actor", "reason", "promotion_run_id",
                  "before_kind", "before_sha256", "after_sha256", "prev_kind", "prev_receipt_sha256",
                  "recorded_at")
RECEIPT_COLS = RECEIPT_HASHED + ("after_image_json", "receipt_sha256")


def _q(conn, sql, b=()):
    return conn.execute(sql, b).fetchall()


class Writer:
    def __init__(self, conn: apsw.Connection, actor: str, clock=db.utc_now):
        self.conn = conn
        self.actor = actor
        self.clock = clock
        self._cols = {}
        self.promotion_run_id = None

    def columns(self, table):
        if table not in self._cols:
            info = _q(self.conn, f"PRAGMA table_info({table})")
            if not info:
                raise ValueError(f"no such table {table}")
            pk = [r[1] for r in info if r[5] == 1]
            self._cols[table] = ([r[1] for r in info], pk[0])
        return self._cols[table]

    @contextmanager
    def tx(self):
        _q(self.conn, "BEGIN IMMEDIATE")
        try:
            yield self
        except BaseException:
            _q(self.conn, "ROLLBACK")
            raise
        _q(self.conn, "COMMIT")

    def insert(self, table: str, row: dict, reason: str) -> int:
        """Write receipt then row. Must run inside tx(). Returns the row's pk."""
        if not self.conn.in_transaction:
            raise RuntimeError("Writer.insert outside a transaction")
        cols, pk = self.columns(table)
        unknown = set(row) - set(cols)
        if unknown:
            raise ValueError(f"{table}: unknown columns {sorted(unknown)}")
        full = {c: row.get(c) for c in cols}
        if full[pk] is None:
            full[pk] = (_q(self.conn, f"SELECT coalesce(max({pk}), 0) + 1 FROM {table}")[0][0])
        last = _q(self.conn, "SELECT receipt_id, receipt_sha256, recorded_at FROM meta_receipt ORDER BY receipt_id DESC LIMIT 1")
        rid = last[0][0] + 1 if last else 1
        full["receipt_id"] = rid
        full = canon.canon(full)  # NFC strings, no floats: the row equals its image
        image = canon.text(full)
        rec = {
            "receipt_id": rid, "table_name": table, "row_pk": full[pk], "op": "INSERT",
            "actor": self.actor, "reason": reason, "promotion_run_id": self.promotion_run_id,
            "before_kind": "ABSENT", "before_sha256": None,
            "after_sha256": canon.sha256_hex(image.encode()),
            "prev_kind": "HASH" if last else "GENESIS",
            "prev_receipt_sha256": last[0][1] if last else None,
            "recorded_at": self.clock(),
        }
        rec["receipt_sha256"] = canon.digest(rec)
        rec["after_image_json"] = image
        _q(self.conn, f"INSERT INTO meta_receipt ({', '.join(RECEIPT_COLS)}) VALUES ({', '.join('?' * len(RECEIPT_COLS))})",
           tuple(rec[c] for c in RECEIPT_COLS))
        names = list(full)
        _q(self.conn, f"INSERT INTO {table} ({', '.join(names)}) VALUES ({', '.join('?' * len(names))})",
           tuple(full[c] for c in names))
        return full[pk]


def receipted_tables(conn):
    out = []
    for (name,) in _q(conn, "SELECT name FROM sqlite_schema WHERE type = 'table' ORDER BY name"):
        if name.startswith(("core_", "stg_", "ev_")):
            cols = [r[1] for r in _q(conn, f"PRAGMA table_info({name})")]
            if "receipt_id" in cols:
                out.append(name)
    return out


def verify_ledger(conn) -> dict:
    """Recompute every hash and link; check every row equals its image and
    every receipted row has exactly one receipt. Raises db.Halt on any break."""
    t0 = time.perf_counter()
    prev = None
    prev_time = ""
    per_table = {}
    rows = _q(conn, f"SELECT {', '.join(RECEIPT_COLS)} FROM meta_receipt ORDER BY receipt_id")
    for i, r in enumerate(rows, start=1):
        rec = dict(zip(RECEIPT_COLS, r))
        if rec["receipt_id"] != i:
            raise db.Halt(f"receipt sequence gap at {i}")
        img = rec["after_image_json"]
        obj = json.loads(img)
        if canon.text(obj) != img:
            raise db.Halt(f"receipt {i}: after-image is not canonical")
        if canon.sha256_hex(img.encode()) != rec["after_sha256"]:
            raise db.Halt(f"receipt {i}: after_sha256 mismatch")
        hashed = {k: rec[k] for k in RECEIPT_HASHED}
        if canon.digest(hashed) != rec["receipt_sha256"]:
            raise db.Halt(f"receipt {i}: receipt_sha256 mismatch")
        if rec["prev_receipt_sha256"] != prev or (rec["prev_kind"] == "GENESIS") != (prev is None):
            raise db.Halt(f"receipt {i}: chain break")
        if rec["recorded_at"] < prev_time:
            raise db.Halt(f"receipt {i}: recorded_at went backwards")
        if obj.get("receipt_id") != i:
            raise db.Halt(f"receipt {i}: image names receipt {obj.get('receipt_id')}")
        per_table[rec["table_name"]] = per_table.get(rec["table_name"], 0) + 1
        prev, prev_time = rec["receipt_sha256"], rec["recorded_at"]
    for t in receipted_tables(conn):
        cols = [c[1] for c in _q(conn, f"PRAGMA table_info({t})")]
        held = _q(conn, f"SELECT {', '.join(cols)} FROM {t} ORDER BY receipt_id")
        imgs = _q(conn, "SELECT after_image_json FROM meta_receipt WHERE table_name = ? ORDER BY receipt_id", (t,))
        if len(held) != len(imgs):
            raise db.Halt(f"{t}: {len(held)} rows vs {len(imgs)} receipts (orphan receipt or unreceipted row)")
        for row, (img,) in zip(held, imgs):
            if dict(zip(cols, row)) != json.loads(img):
                raise db.Halt(f"{t}: row {row[0]} differs from its receipt image")
    return {"receipts": len(rows), "head": prev, "tables": per_table,
            "verify_ms": int((time.perf_counter() - t0) * 1000)}


def canonical_dump(conn) -> bytes:
    """Canonical bytes of the ledger and every receipted table, ordered by pk."""
    out = {"meta_receipt": [list(r) for r in _q(conn, f"SELECT {', '.join(RECEIPT_COLS)} FROM meta_receipt ORDER BY receipt_id")]}
    for t in receipted_tables(conn):
        cols = [c[1] for c in _q(conn, f"PRAGMA table_info({t})")]
        out[t] = {"cols": cols, "rows": [list(r) for r in _q(conn, f"SELECT {', '.join(cols)} FROM {t} ORDER BY 1")]}
    return canon.dumps(out)


def replay(src_conn, dst_path) -> dict:
    """Rebuild a fresh store from receipts alone; prove byte identity."""
    dst_path = Path(dst_path)
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(dst_path) + suffix)
        if p.exists():
            raise FileExistsError(f"replay target exists: {p}")
    t0 = time.perf_counter()
    dst = db.connect(dst_path)
    db.migrate(dst)
    rows = _q(src_conn, f"SELECT {', '.join(RECEIPT_COLS)} FROM meta_receipt ORDER BY receipt_id")
    _q(dst, "BEGIN IMMEDIATE")
    try:
        for r in rows:
            rec = dict(zip(RECEIPT_COLS, r))
            _q(dst, f"INSERT INTO meta_receipt ({', '.join(RECEIPT_COLS)}) VALUES ({', '.join('?' * len(RECEIPT_COLS))})", r)
            img = json.loads(rec["after_image_json"])
            names = list(img)
            _q(dst, f"INSERT INTO {rec['table_name']} ({', '.join(names)}) VALUES ({', '.join('?' * len(names))})",
               tuple(img[c] for c in names))
        _q(dst, "COMMIT")
    except BaseException:
        _q(dst, "ROLLBACK")
        raise
    rebuild_ms = int((time.perf_counter() - t0) * 1000)
    db.gates(dst)
    a, b = canonical_dump(src_conn), canonical_dump(dst)
    result = {"receipts": len(rows), "rebuild_ms": rebuild_ms,
              "src_sha256": canon.sha256_hex(a), "dst_sha256": canon.sha256_hex(b), "identical": a == b}
    dst.close()
    return result
