package main

import (
	"crypto/sha256"
	"database/sql"
	"database/sql/driver"
	"encoding/hex"
	"fmt"
	"sort"

	"modernc.org/sqlite"
)

func main() {
	sqlite.MustRegisterDeterministicScalarFunction("sha256_hex", 1, func(ctx *sqlite.FunctionContext, args []driver.Value) (driver.Value, error) {
		s := fmt.Sprint(args[0]); h := sha256.Sum256([]byte(s)); return hex.EncodeToString(h[:]), nil
	})
	db, _ := sql.Open("sqlite", ":memory:")
	db.SetMaxOpenConns(1)
	var v string
	db.QueryRow("select sqlite_version()").Scan(&v)
	fmt.Println("T-VER modernc sqlite", v)
	db.Exec("pragma trusted_schema=OFF")
	db.Exec("create table t(x text) strict; create table log(h text) strict; create trigger tr after insert on t begin insert into log values (sha256_hex(new.x)); end;")
	_, err := db.Exec("insert into t values ('a')")
	fmt.Println("T-INN modernc deterministic UDF under trusted_schema=OFF:", err)
	k := []string{"a", "｡", "\U0001F600"}; sort.Strings(k)
	for _, s := range k { fmt.Printf("%x ", []rune(s)[0]) }; fmt.Println("<- Go default string sort")
}
