"""unsilo CLI.

  unsilo init                 create var/unsilo.db, run migrations and gates
  unsilo seed                 write the Docket seed (refuses a non-empty ledger)
  unsilo verify               gates + full ledger recomputation
  unsilo replay               rebuild a fresh store from receipts; prove byte identity
  unsilo serve [--port N]     dashboard on 127.0.0.1
  unsilo sweep-d3 ...         D-3 acquisition run (see unsilo/evidence)
  unsilo readmission ...      B1/B9 readmission kit (see unsilo/readmission.py)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import db, ledger

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO / "var" / "unsilo.db"


def _store(args):
    path = Path(args.db)
    path.parent.mkdir(parents=True, exist_ok=True)
    return db.open_store(path)


def cmd_init(args):
    conn = _store(args)
    print(json.dumps({"db": str(args.db), **{k: v for k, v in db.gates(conn).items() if k != "migrations"}}, indent=1))


def cmd_seed(args):
    from .docket.records import Docket
    from .docket.seed import seed
    conn = _store(args)
    if conn.execute("SELECT count(*) FROM meta_receipt").fetchall()[0][0]:
        sys.exit("refusing to seed: the ledger is not empty (seeding is a one-time genesis write)")
    w = ledger.Writer(conn, "seed:operator-records")
    with w.tx():
        out = seed(Docket(w))
    print(json.dumps({"seeded": out, "ledger": ledger.verify_ledger(conn)}, indent=1))


def cmd_verify(args):
    conn = db.connect(args.db)
    facts = db.gates(conn)
    print(json.dumps(facts, indent=1))


def cmd_replay(args):
    conn = db.connect(args.db)
    db.gates(conn)
    target = Path(args.to) if args.to else Path(args.db).with_suffix(".replay.db")
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(target) + suffix)
        if p.exists() and args.to is None:
            p.unlink()  # the default target is a disposable rebuild beside the store
    result = ledger.replay(conn, target)
    print(json.dumps(result, indent=1))
    if not result["identical"]:
        sys.exit("REPLAY MISMATCH")


def cmd_serve(args):
    import uvicorn
    from .web.app import create_app
    app = create_app(args.db)
    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="warning")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="unsilo")
    ap.add_argument("--db", default=str(DEFAULT_DB))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("seed").set_defaults(fn=cmd_seed)
    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    r = sub.add_parser("replay")
    r.add_argument("--to")
    r.set_defaults(fn=cmd_replay)
    s = sub.add_parser("serve")
    s.add_argument("--port", type=int, default=8765)
    s.set_defaults(fn=cmd_serve)
    try:
        from .evidence import cli as ev_cli
        ev_cli.register(sub)
    except ImportError:
        pass
    try:
        from . import readmission
        readmission.register(sub)
    except ImportError:
        pass
    args = ap.parse_args(argv)
    try:
        args.fn(args)
    except db.Halt as e:
        sys.exit(f"HALT: {e}")


if __name__ == "__main__":
    main()
