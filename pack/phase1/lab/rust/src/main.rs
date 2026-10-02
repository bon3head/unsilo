use rusqlite::{functions::FunctionFlags, Connection};
use sha2::{Digest, Sha256};
fn hexsha(s: &str) -> String { Sha256::digest(s.as_bytes()).iter().map(|b| format!("{:02x}", b)).collect() }
fn main() -> rusqlite::Result<()> {
    let c = Connection::open_in_memory()?;
    let v: String = c.query_row("select sqlite_version()", [], |r| r.get(0))?;
    let fk: i64 = c.query_row("pragma foreign_keys", [], |r| r.get(0))?;
    println!("T-VER sqlite={v} default_fk={fk}");
    c.pragma_update(None, "trusted_schema", "OFF")?;
    for (label, flags) in [("deterministic-only", FunctionFlags::SQLITE_UTF8 | FunctionFlags::SQLITE_DETERMINISTIC),
                           ("deterministic+innocuous", FunctionFlags::SQLITE_UTF8 | FunctionFlags::SQLITE_DETERMINISTIC | FunctionFlags::SQLITE_INNOCUOUS)] {
        let c = Connection::open_in_memory()?;
        c.pragma_update(None, "trusted_schema", "OFF")?;
        c.create_scalar_function("sha256_hex", 1, flags, |ctx| { let s: String = ctx.get(0)?; Ok(hexsha(&s)) })?;
        c.execute_batch("create table t(x text) strict; create table log(h text) strict; create trigger tr after insert on t begin insert into log values (sha256_hex(new.x)); end;")?;
        match c.execute("insert into t values ('a')", []) {
            Ok(_) => { let h: String = c.query_row("select h from log", [], |r| r.get(0))?; println!("T-INN {label}: ok {}", &h[..12]); }
            Err(e) => println!("T-INN {label}: {e}"),
        }
    }
    // T-MIG: real migrations
    let dir = std::path::Path::new("/home/user/unsilo/schema/migrations");
    let mut files: Vec<_> = std::fs::read_dir(dir).unwrap().map(|e| e.unwrap().path()).collect(); files.sort();
    let path = "./rs.db";
    for s in ["", "-wal", "-shm"] { let _ = std::fs::remove_file(format!("{path}{s}")); }
    let c = Connection::open(path)?;
    c.pragma_update(None, "foreign_keys", "ON")?; c.pragma_update(None, "trusted_schema", "OFF")?;
    for (i, f) in files.iter().enumerate() {
        let sql = std::fs::read_to_string(f).unwrap();
        match c.execute_batch(&sql) { Ok(_) => {}, Err(e) => { println!("T-MIG execute_batch {:?}: {e}", f.file_name().unwrap()); } }
        c.execute("insert into meta_migration values (?1,?2,?3,'2026-10-02T12:00:00Z')", (i as i64 + 1, f.file_name().unwrap().to_str().unwrap(), hexsha(&sql)))?;
    }
    let fx = std::fs::read_to_string("/home/user/unsilo/schema/fixtures/duolingo_promotion_walk.sql").unwrap();
    c.execute_batch(&fx)?;
    let ic: String = c.query_row("pragma integrity_check", [], |r| r.get(0))?;
    let mut st = c.prepare("select count(*) from pragma_foreign_key_check")?; let fkv: i64 = st.query_row([], |r| r.get(0))?;
    let jm: String = c.query_row("pragma journal_mode", [], |r| r.get(0))?;
    let n: i64 = c.query_row("select count(*) from v_claim_effective where verdict_axis='UNRESOLVED' and eclass_axis like 'ABSTENTION%'", [], |r| r.get(0))?;
    println!("T-MIG integrity={ic} fk_violations={fkv} journal={jm} claims_honest={n}");
    let mut k = vec!["a".to_string(), "\u{FF61}".to_string(), "\u{1F600}".to_string()]; k.sort();
    println!("T-KEY default sort = {:?}", k.iter().map(|s| format!("{:x}", s.chars().next().unwrap() as u32)).collect::<Vec<_>>());
    Ok(())
}
