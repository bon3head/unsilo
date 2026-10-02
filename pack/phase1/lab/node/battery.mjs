import { createHash } from 'node:crypto';
import { readFileSync, readdirSync } from 'node:fs';
const sha = s => createHash('sha256').update(s).digest('hex');
const out = {};
// node:sqlite builtin
const { DatabaseSync } = await import('node:sqlite');
{ const d = new DatabaseSync(':memory:'); out.nodesqlite_version = d.prepare('select sqlite_version() v').get().v;
  d.exec("pragma trusted_schema=OFF");
  d.function('sha256_hex', { deterministic: true }, s => sha(s));
  d.exec("create table t(x text) strict; create table log(h text) strict; create trigger tr after insert on t begin insert into log values (sha256_hex(new.x)); end;");
  try { d.exec("insert into t values ('a')"); out.nodesqlite_inn = 'ok'; } catch (e) { out.nodesqlite_inn = e.message; } }
// better-sqlite3
try { const B = (await import('better-sqlite3')).default; const d = new B(':memory:');
  out.bs3_version = d.prepare('select sqlite_version() v').get().v; out.bs3_fk_default = d.pragma('foreign_keys', { simple: true });
  d.pragma('trusted_schema=OFF');
  d.function('sha256_hex', { deterministic: true }, s => sha(s));
  d.exec("create table t(x text) strict; create table log(h text) strict; create trigger tr after insert on t begin insert into log values (sha256_hex(new.x)); end;");
  try { d.exec("insert into t values ('a')"); out.bs3_inn = 'ok'; } catch (e) { out.bs3_inn = e.message; }
  // real migrations
  const f = new B('./node.db'); f.pragma('foreign_keys=ON'); f.pragma('trusted_schema=OFF');
  const dir = '/home/user/unsilo/schema/migrations'; let i = 0;
  for (const n of readdirSync(dir).sort()) { const sql = readFileSync(`${dir}/${n}`, 'utf8'); try { f.exec(sql); } catch (e) { out['mig_'+n] = e.message; } f.prepare("insert or ignore into meta_migration values (?,?,?,'2026-10-02T12:00:00Z')").run(++i, n, sha(sql)); }
  f.exec(readFileSync('/home/user/unsilo/schema/fixtures/duolingo_promotion_walk.sql','utf8'));
  out.bs3_mig = { integrity: f.pragma('integrity_check', {simple:true}), fk: f.pragma('foreign_key_check').length, journal: f.pragma('journal_mode',{simple:true}), honest: f.prepare("select count(*) n from v_claim_effective where verdict_axis='UNRESOLVED' and eclass_axis like 'ABSTENTION%'").get().n };
} catch (e) { out.bs3_error = String(e).slice(0,200); }
out.key_default = ['a','｡','\u{1F600}'].sort().map(s => s.codePointAt(0).toString(16));
out.key_fixed = ['a','｡','\u{1F600}'].sort((x,y)=>Buffer.compare(Buffer.from(x),Buffer.from(y))).map(s => s.codePointAt(0).toString(16));
console.log(JSON.stringify(out, null, 1));
