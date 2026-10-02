"""Feed search: a disposable in-memory FTS5 projection (S6).

Nothing in the store file is mutable: the index lives in a ':memory:' database,
is rebuilt from the feed whenever the receipt head moves, and no count, verdict
or absence claim depends on its hits or rank.
"""
from __future__ import annotations

import re
import threading

import apsw

from ..docket import queries as Q

FAR = {"k": "9999-12-31T23:59:59Z", "eff_value": "9999-12-31", "eff_gran": "DAY", "eff_zone": "UTC"}


class FeedIndex:
    def __init__(self):
        self.mem = apsw.Connection(":memory:")
        self.mem.execute("CREATE VIRTUAL TABLE fts_feed USING fts5(item_kind UNINDEXED, item_id UNINDEXED, title, body, tokenize='unicode61')").fetchall()
        self.head = None
        self.lock = threading.Lock()

    def invalidate(self):
        with self.lock:
            self.head = None

    def _ensure(self, conn):
        head = conn.execute("SELECT coalesce(max(receipt_id), 0) FROM meta_receipt").fetchall()[0][0]
        if head == self.head:
            return
        rows = Q.run(conn, "feed", FAR)
        self.mem.execute("DELETE FROM fts_feed").fetchall()
        with self.mem:
            for r in rows:
                self.mem.execute("INSERT INTO fts_feed VALUES (?, ?, ?, ?)",
                                 (r["item_kind"], r["item_id"], r["title"], r["body"] or "")).fetchall()
        self.head = head

    @staticmethod
    def to_match(q: str) -> str:
        toks = re.findall(r"\w+", q, flags=re.UNICODE)
        return " AND ".join(f'"{t}"*' for t in toks)

    def search(self, conn, q: str) -> set:
        m = self.to_match(q)
        if not m:
            return set()
        with self.lock:
            self._ensure(conn)
            return {(k, i) for k, i in self.mem.execute("SELECT item_kind, item_id FROM fts_feed WHERE fts_feed MATCH ?", (m,)).fetchall()}
