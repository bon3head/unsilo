import hashlib, json, sys, unicodedata
def canon(o):
    if isinstance(o, float): raise TypeError("float forbidden in canonical form")
    if isinstance(o, bool) or o is None or isinstance(o, int): return o
    if isinstance(o, str): return unicodedata.normalize("NFC", o)
    if isinstance(o, (set, frozenset)): return sorted((canon(x) for x in o), key=lambda s: json.dumps(s, ensure_ascii=False).encode())
    if isinstance(o, (list, tuple)): return [canon(x) for x in o]
    if isinstance(o, dict): return {canon(k): canon(v) for k, v in sorted(o.items(), key=lambda kv: kv[0].encode())}
    raise TypeError(type(o))
def dumps(o): return json.dumps(canon(o), ensure_ascii=False, separators=(",", ":")).encode()
obj={"sources":{"greenhouse","lever","edgar","cdx","careers"},"name":"Café","\U0001F600":1,"｡":2}
print(hashlib.sha256(dumps(obj)).hexdigest()[:16], dumps(obj).decode())
try: dumps({"x":0.1}); print("float accepted (bad)")
except TypeError as e: print("float rejected:", e)
