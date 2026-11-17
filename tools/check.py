"""Validador de coquito-ia/2. Solo stdlib.

Uso: python tools/check.py [--reindex]
Imprime OK o la lista de errores y sale con codigo 1.
"""
import argparse
import json
import re
import sys
import uuid
from pathlib import Path

KEYS = ("id", "sid", "k", "d", "imp", "t", "s", "sol", "less", "src", "tags", "at")
INDEX_KEYS = ("id", "sid", "k", "d", "imp", "t")
REQUIRED = {"id", "sid", "k", "d", "imp", "t"}
KINDS = {"doctrine", "recipe", "experience", "reference"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Solo valores largos: la doctrina menciona estos prefijos como regla, no como clave.
SECRETS = (
    re.compile(r"sb_secret_[A-Za-z0-9_-]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN "),
)


def read_lines(path, errors):
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{path.name}: BOM no permitido")
    if b"\r" in raw:
        errors.append(f"{path.name}: saltos CRLF; se exige LF")
    if raw and not raw.endswith(b"\n"):
        errors.append(f"{path.name}: falta LF final")
    text = raw.decode("utf-8")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    for i, line in enumerate(lines, 1):
        if not line.strip():
            errors.append(f"{path.name}:{i}: linea vacia")
    return lines


def check_records(lines, errors):
    records, ids, sids = [], set(), set()
    for i, line in enumerate(lines, 1):
        where = f"memories.jsonl:{i}"
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"{where}: JSON invalido ({e.msg})")
            continue
        if not isinstance(obj, dict):
            errors.append(f"{where}: no es objeto")
            continue
        pos = [KEYS.index(key) for key in obj if key in KEYS]
        if pos != sorted(pos):
            errors.append(f"{where}: orden de claves incorrecto: {list(obj)}")
        missing = REQUIRED - set(obj)
        if missing:
            errors.append(f"{where}: faltan {sorted(missing)}")
        extra = set(obj) - set(KEYS)
        if extra:
            errors.append(f"{where}: claves desconocidas {sorted(extra)}")
        for key in ("id", "sid", "k", "d", "t", "s", "sol", "less", "src", "at"):
            if key in obj and not isinstance(obj[key], str):
                errors.append(f"{where}: {key} debe ser string")
        rid, sid, k, d, imp = obj.get("id"), obj.get("sid"), obj.get("k"), obj.get("d"), obj.get("imp")
        if isinstance(rid, str):
            if not ID_RE.match(rid):
                errors.append(f"{where}: id mal formado: {rid}")
            if isinstance(d, str) and not rid.startswith(d + "/"):
                errors.append(f"{where}: id no empieza por dominio {d}")
            if rid in ids:
                errors.append(f"{where}: id duplicado: {rid}")
            ids.add(rid)
        if isinstance(sid, str):
            try:
                uuid.UUID(sid)
            except ValueError:
                errors.append(f"{where}: sid no es UUID: {sid}")
            if sid in sids:
                errors.append(f"{where}: sid duplicado: {sid}")
            sids.add(sid)
        for pattern in SECRETS:
            if pattern.search(line):
                errors.append(f"{where}: posible secreto ({pattern.pattern})")
        if k not in KINDS:
            errors.append(f"{where}: k invalido: {k}")
        if not isinstance(imp, int) or isinstance(imp, bool) or not 1 <= imp <= 10:
            errors.append(f"{where}: imp fuera de 1-10: {imp}")
        if "at" in obj and not DATE_RE.match(obj["at"]):
            errors.append(f"{where}: at debe ser AAAA-MM-DD")
        if "tags" in obj:
            tags = obj["tags"]
            if not isinstance(tags, list) or any(not isinstance(x, str) for x in tags):
                errors.append(f"{where}: tags debe ser lista de strings")
            elif tags != sorted(set(tags)) or any(x != x.lower() for x in tags):
                errors.append(f"{where}: tags no unicos/ordenados/minusculos")
        records.append(obj)
    order = [(r.get("d", ""), r.get("k", ""), r.get("id", "")) for r in records]
    if order != sorted(order):
        errors.append("memories.jsonl: filas desordenadas (se exige d,k,id)")
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reindex", action="store_true", help="regenera index.jsonl antes de validar")
    a = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    errors = []
    mem = read_lines(root / "memories.jsonl", errors)
    records = check_records(mem, errors)
    expected = [json.dumps({k: r[k] for k in INDEX_KEYS if k in r},
                           ensure_ascii=False, separators=(",", ":")) for r in records]

    if a.reindex and not errors:
        with (root / "index.jsonl").open("w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(expected) + "\n")
        idx = expected
    else:
        idx = read_lines(root / "index.jsonl", errors)

    if idx != expected:
        errors.append(f"index.jsonl: no coincide con la proyeccion de memories.jsonl ({len(idx)} vs {len(expected)})")

    if errors:
        for e in errors:
            print("ERROR " + e)
        print(f"FAIL errores={len(errors)}")
        sys.exit(1)
    print(f"OK memorias={len(records)} indice={len(idx)}")


if __name__ == "__main__":
    main()
