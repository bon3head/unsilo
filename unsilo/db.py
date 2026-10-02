"""SQLite profile (S6/B11), migration runner, and startup gates.

Engine: SQLite 3.53.4 via the apsw wheel, never stdlib sqlite3 (G6: stdlib
cannot mark a function INNOCUOUS, so the receipt after-hash trigger fails under
trusted_schema=OFF). Every gate fails closed: a failed gate raises Halt.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

import apsw

from . import canon, temporal

APPLICATION_ID = 0x554E534C  # "UNSL" = 1431196492
USER_VERSION = 1  # physical generation (R26); migrations are counted in meta_migration
PINNED_SQLITE = "3.53.4"
MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
CONN_PRAGMAS = (
    ("foreign_keys", "ON", 1),
    ("synchronous", "FULL", 2),
    ("trusted_schema", "OFF", 0),
    ("busy_timeout", "5000", 5000),
)


class Halt(RuntimeError):
    """A gate failed. The store refuses to serve or write."""


def _q(conn, sql, bindings=()):
    return conn.execute(sql, bindings).fetchall()


def _register(conn: apsw.Connection) -> None:
    flags = apsw.SQLITE_INNOCUOUS
    conn.create_scalar_function(
        "sha256_hex", lambda s: None if s is None else canon.sha256_hex(s.encode()),
        1, deterministic=True, flags=flags)
    conn.create_scalar_function("b4_truth", temporal.sql_truth, 11, deterministic=True, flags=flags)
    conn.create_scalar_function("b4_reason", temporal.sql_reason, 11, deterministic=True, flags=flags)
    conn.create_scalar_function("instant_sort", temporal.sort_key, 4, deterministic=True, flags=flags)


def connect(path, readonly: bool = False) -> apsw.Connection:
    if apsw.sqlite_lib_version() != PINNED_SQLITE:
        raise Halt(f"SQLite {apsw.sqlite_lib_version()} is not the pinned {PINNED_SQLITE}")
    flags = apsw.SQLITE_OPEN_READONLY if readonly else (apsw.SQLITE_OPEN_READWRITE | apsw.SQLITE_OPEN_CREATE)
    conn = apsw.Connection(str(path), flags=flags)
    for name, value, expect in CONN_PRAGMAS:
        _q(conn, f"PRAGMA {name} = {value}")
        got = _q(conn, f"PRAGMA {name}")[0][0]
        if got != expect:
            raise Halt(f"PRAGMA {name} read back {got!r}, expected {expect!r} (G2)")
    _register(conn)
    return conn


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def migration_files():
    out = []
    for p in sorted(MIGRATIONS_DIR.glob("*.sql")):
        m = re.fullmatch(r"(\d{4})_([a-z0-9_]+)\.sql", p.name)
        if not m:
            raise Halt(f"unexpected migration file name {p.name}")
        out.append((int(m.group(1)), p.name, p.read_bytes()))
    for i, (v, _, _) in enumerate(out, start=1):
        if v != i:
            raise Halt("migration numbering must be contiguous from 0001")
    return out


def _tables(conn):
    return {r[0] for r in _q(conn, "SELECT name FROM sqlite_schema WHERE type IN ('table','view')")}


def migrate(conn: apsw.Connection, clock=utc_now) -> list[str]:
    """Apply pending migrations. Applied files whose bytes changed: Halt."""
    applied_now = []
    if not _tables(conn):
        # File-level pragmas: outside any transaction, before the first table.
        _q(conn, "PRAGMA page_size = 4096")
        _q(conn, "PRAGMA journal_mode = WAL")
        _q(conn, f"PRAGMA application_id = {APPLICATION_ID}")
        _q(conn, f"PRAGMA user_version = {USER_VERSION}")
    elif _q(conn, "PRAGMA application_id")[0][0] != APPLICATION_ID:
        raise Halt("application_id mismatch: not an UnSilo store")
    have = {}
    if "meta_migration" in _tables(conn):
        have = {v: (n, h) for v, n, h in _q(conn, "SELECT version, name, sha256 FROM meta_migration")}
    for version, name, body in migration_files():
        digest = canon.sha256_hex(body)
        if version in have:
            if have[version] != (name, digest):
                raise Halt(f"migration {name} bytes differ from the applied record")
            continue
        _q(conn, "BEGIN IMMEDIATE")
        try:
            _q(conn, body.decode("utf-8"))  # drain: apsw runs multi-statement SQL lazily (G1)
            _q(conn, "INSERT INTO meta_migration (version, name, sha256, applied_at) VALUES (?, ?, ?, ?)",
               (version, name, digest, clock()))
            _q(conn, "COMMIT")
        except BaseException:
            _q(conn, "ROLLBACK")
            raise
        applied_now.append(name)
    return applied_now


def gates(conn: apsw.Connection, verify_chain: bool = True) -> dict:
    """Startup gates. Returns facts for the closure; raises Halt on any failure."""
    facts = {}
    ic = _q(conn, "PRAGMA integrity_check")
    if ic != [("ok",)]:
        raise Halt(f"integrity_check: {ic[:5]}")
    fk = _q(conn, "PRAGMA foreign_key_check")
    if fk:
        raise Halt(f"foreign_key_check: {fk[:5]}")
    for name, expect in (("application_id", APPLICATION_ID), ("user_version", USER_VERSION),
                         ("journal_mode", "wal"), ("page_size", 4096)):
        got = _q(conn, f"PRAGMA {name}")[0][0]
        if got != expect:
            raise Halt(f"PRAGMA {name} = {got!r}, expected {expect!r}")
    files = {v: (n, canon.sha256_hex(b)) for v, n, b in migration_files()}
    rows = {v: (n, h) for v, n, h in _q(conn, "SELECT version, name, sha256 FROM meta_migration")}
    if rows != files:
        raise Halt("meta_migration does not match the migration files on disk")
    facts["migrations"] = [{"version": v, "name": n, "sha256": h} for v, (n, h) in sorted(rows.items())]
    facts["sqlite"] = apsw.sqlite_lib_version()
    facts["apsw"] = apsw.apsw_version()
    facts["tzdata"] = temporal.TZDATA_VERSION
    if verify_chain:
        from .ledger import verify_ledger
        facts["ledger"] = verify_ledger(conn)
    return facts


def open_store(path, clock=utc_now) -> apsw.Connection:
    conn = connect(path)
    migrate(conn, clock)
    gates(conn)
    return conn
