import apsw, hashlib, json, os, sys, unicodedata
from pathlib import Path
S=Path('/home/user/unsilo/schema')
res={}
def sha(b): return hashlib.sha256(b).hexdigest()
def open_conn(path):
    c=apsw.Connection(path)
    for p in ("foreign_keys=ON","synchronous=FULL","trusted_schema=OFF","busy_timeout=5000"):
        c.execute("PRAGMA "+p)
    assert c.execute("PRAGMA foreign_keys").fetchone()[0]==1
    c.create_scalar_function("sha256_hex", lambda s: sha(s.encode()), 1, deterministic=True, flags=apsw.SQLITE_INNOCUOUS)
    return c
# T-VER
c=apsw.Connection(':memory:')
res['T-VER']=dict(sqlite=apsw.sqlite_lib_version(), fts5='ENABLE_FTS5' in [r[0] for r in c.execute('pragma compile_options')], default_fk=c.execute('pragma foreign_keys').fetchone()[0])
# T-MIG on a file DB with the real migrations + fixture, trusted_schema=OFF
db='./py.db'
for s_ in ('','-wal','-shm'):
    if os.path.exists(db+s_): os.remove(db+s_)
c=open_conn(db)
for i,f in enumerate(sorted((S/'migrations').glob('*.sql')),1):
    b=f.read_bytes(); c.execute(b.decode()).fetchall()
    c.execute("INSERT INTO meta_migration VALUES (?,?,?,?)",(i,f.name,sha(b),'2026-10-02T12:00:00Z'))
c.execute((S/'fixtures/duolingo_promotion_walk.sql').read_text()).fetchall()
ic=c.execute("PRAGMA integrity_check").fetchall(); fk=c.execute("PRAGMA foreign_key_check").fetchall()
res['T-MIG']=dict(integrity=ic, fk_violations=len(fk), claims=c.execute("select cut_id,claim_id,verdict_axis,eclass_axis from v_claim_effective order by 1,2").fetchall(), app=c.execute("select cut_id,status,in_effect_at_cut from v_application_state_head order by 1").fetchall(), journal=c.execute("pragma journal_mode").fetchone()[0])
# T-INN: in-transaction after-hash verification trigger (proposal f / DL-3), executed on the real receipt table
c.execute("""CREATE TEMP TRIGGER verify_after_hash BEFORE INSERT ON meta_receipt
WHEN sha256_hex(NEW.after_image_json) IS NOT NEW.after_sha256
BEGIN SELECT RAISE(ABORT,'after_sha256 does not match after_image_json'); END""")
head=c.execute("select receipt_sha256 from meta_receipt order by receipt_id desc limit 1").fetchone()[0]
n=c.execute("select max(receipt_id)+1 from meta_receipt").fetchone()[0]
img='{"note_id":9}'
try:
    c.execute("INSERT INTO meta_receipt VALUES (?,?,?,'INSERT','t','t',NULL,'ABSENT',NULL,?,?,'HASH',?,?,'2026-10-02T12:00:01Z')",(n,'core_note',9,'0'*64,img,head,'1'*64))
    res['T-INN-bad']='ACCEPTED (bad)'
except apsw.ConstraintError as e: res['T-INN-bad']='blocked: '+str(e)
c.execute("SAVEPOINT s")
c.execute("INSERT INTO meta_receipt VALUES (?,?,?,'INSERT','t','t',NULL,'ABSENT',NULL,?,?,'HASH',?,?,'2026-10-02T12:00:01Z')",(n,'core_note',9,sha(img.encode()),img,head,'1'*64))
res['T-INN-good']='accepted'; c.execute("ROLLBACK TO s"); c.execute("RELEASE s")
# T-REPLAY: rebuild every core table from after_image_json in receipt order into a fresh DB; compare canonical dumps
def dump(conn):
    out=[]
    for (t,) in conn.execute("select name from sqlite_schema where type='table' and name like 'core\\_%' escape '\\' order by name"):
        cols=[r[1] for r in conn.execute(f"pragma table_info({t})")]
        for row in conn.execute(f"select * from {t} order by 1"):
            out.append(json.dumps([t,dict(zip(cols,row))],sort_keys=True,separators=(',',':'),ensure_ascii=False))
    return sha("\n".join(out).encode()), len(out)
db2=db.replace('py.db','py_replay.db')
for s_ in ('','-wal','-shm'):
    if os.path.exists(db2+s_): os.remove(db2+s_)
r=open_conn(db2)
for i,f in enumerate(sorted((S/'migrations').glob('*.sql')),1):
    b=f.read_bytes(); r.execute(b.decode()).fetchall(); r.execute("INSERT INTO meta_migration VALUES (?,?,?,?)",(i,f.name,sha(b),'2026-10-02T12:00:00Z'))
# staging must exist for FK targets: replay staging rows verbatim (staging is the input, not core)
for t in ('stg_ingest_batch','stg_raw_row','stg_candidate','stg_promotion_decision'):
    for row in c.execute(f"select * from {t} order by 1"):
        r.execute(f"insert into {t} values ({','.join('?'*len(row))})",row)
r.execute("BEGIN")
for rec in c.execute("select receipt_id,table_name,row_pk,op,actor,reason,promotion_run_id,before_kind,before_sha256,after_sha256,after_image_json,prev_kind,prev_receipt_sha256,receipt_sha256,recorded_at from meta_receipt order by receipt_id"):
    r.execute("insert into meta_receipt values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",rec)
    img=json.loads(rec[10]); assert sha(rec[10].encode())==rec[9]
    r.execute(f"insert into {rec[1]} ({','.join(img)}) values ({','.join('?'*len(img))})",list(img.values()))
r.execute("COMMIT")
res['T-REPLAY']=dict(original=dump(c), replayed=dump(r))
res['T-REPLAY']['identical']=res['T-REPLAY']['original']==res['T-REPLAY']['replayed']
# T-KEY
k=['a','｡','\U0001F600']; res['T-KEY']=dict(default=[hex(ord(x)) for x in sorted(k)], utf8=[hex(ord(x)) for x in sorted(k,key=lambda s:s.encode())])
# T-ASYNC: apsw native async available?
res['T-ASYNC']=hasattr(apsw.Connection,'as_async')
for k_,v in res.items(): print(k_, v)
