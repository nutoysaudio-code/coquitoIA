"""Importador unico del snapshot inicial a coquito-ia/1.

Uso: python tools/seed.py --input <dump.json> [--out <dir>] [--force]
No sincroniza: solo convierte un dump de agent_experiences ya obtenido.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

KEYS = ("id", "k", "d", "imp", "t", "s", "sol", "less", "src", "tags", "at")
INDEX_KEYS = ("id", "k", "d", "imp", "t")
KINDS = {"doctrine", "recipe", "experience", "reference"}


def ascii_slug(text, limit=80):
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(text) > limit:
        text = text[:limit].rsplit("-", 1)[0].strip("-")
    return text or "sin-titulo"


def flat(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).replace("\r", " ").replace("\n", " ")).strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="JSON con filas de agent_experiences")
    p.add_argument("--out", default=str(Path(__file__).resolve().parent.parent))
    p.add_argument("--force", action="store_true")
    a = p.parse_args()

    rows = json.loads(Path(a.input).read_text(encoding="utf-8-sig"))
    if not isinstance(rows, list):
        raise SystemExit("El input debe ser una lista de filas")

    seen, records = {}, []
    for r in rows:
        d = ascii_slug(flat(r.get("domain")) or "general", 40)
        t = flat(r.get("title")) or "Sin titulo"
        k = flat(r.get("kind")) or "experience"
        if k not in KINDS:
            raise SystemExit("kind desconocido: " + k)
        slug = ascii_slug(t)
        base = d + "/" + slug
        rid, n = base, 2
        while rid in seen:
            rid, n = base + "-" + str(n), n + 1
        seen[rid] = True

        imp = r.get("importance")
        imp = int(imp) if isinstance(imp, (int, float)) else 5
        imp = max(1, min(10, imp))

        created = flat(r.get("created_at"))
        tags = sorted({ascii_slug(flat(x)) for x in (r.get("tags") or []) if flat(x)})

        rec = {"id": rid, "k": k, "d": d, "imp": imp, "t": t}
        for key, field in (("s", "summary"), ("sol", "solution"), ("less", "lessons_learned"), ("src", "source_path")):
            v = flat(r.get(field))
            if v:
                rec[key] = v
        if tags:
            rec["tags"] = tags
        if re.match(r"^\d{4}-\d{2}-\d{2}", created):
            rec["at"] = created[:10]
        records.append(rec)

    records.sort(key=lambda x: (x["d"], x["k"], x["id"]))
    out = Path(a.out)
    mem, idx = out / "memories.jsonl", out / "index.jsonl"
    if not a.force and (mem.exists() or idx.exists()):
        raise SystemExit("Ya existen los archivos; usa --force para sobrescribir")

    def dump(path, items, keys):
        with path.open("w", encoding="utf-8", newline="\n") as f:
            for item in items:
                ordered = {key: item[key] for key in keys if key in item}
                f.write(json.dumps(ordered, ensure_ascii=False, separators=(",", ":")) + "\n")

    dump(mem, records, KEYS)
    dump(idx, records, INDEX_KEYS)
    print("OK memorias=%s indice=%s" % (len(records), len(records)))


if __name__ == "__main__":
    main()
