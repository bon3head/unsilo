"""Canonical JSON: the only encoder used for hashed bytes.

Keys and sets sort by UTF-8 bytes (B8 frozen snapshot order), strings are NFC,
floats are refused (S6: integers for money and counts). Identical bytes under
any PYTHONHASHSEED (stack-verification G4).
"""
import hashlib
import json
import unicodedata


def canon(o):
    if isinstance(o, float):
        raise TypeError("float forbidden in canonical form")
    if isinstance(o, bool) or o is None or isinstance(o, int):
        return o
    if isinstance(o, str):
        return unicodedata.normalize("NFC", o)
    if isinstance(o, (set, frozenset)):
        return sorted((canon(x) for x in o), key=lambda s: json.dumps(s, ensure_ascii=False).encode())
    if isinstance(o, (list, tuple)):
        return [canon(x) for x in o]
    if isinstance(o, dict):
        for k in o:
            if not isinstance(k, str):
                raise TypeError("canonical keys must be str")
        return {canon(k): canon(v) for k, v in sorted(o.items(), key=lambda kv: kv[0].encode())}
    raise TypeError(f"not canonicalizable: {type(o).__name__}")


def dumps(o) -> bytes:
    return json.dumps(canon(o), ensure_ascii=False, separators=(",", ":")).encode()


def text(o) -> str:
    return dumps(o).decode()


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def digest(o) -> str:
    return sha256_hex(dumps(o))
