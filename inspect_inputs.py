"""Check names, structure and cross-references of the local input pack."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

DEFAULT_INPUT = Path(__file__).resolve().parent / "data"


def inspect_inputs(directory: Path) -> dict:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    tables = {}
    for name, contract in manifest["tables"].items():
        path = directory / (name + ".csv")
        if hashlib.sha256(path.read_bytes()).hexdigest() != contract["sha256"]:
            raise ValueError(f"{name}: digest differs from manifest")
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            if reader.fieldnames != contract["columns"]:
                raise ValueError(f"{name}: invalid header")
            rows = list(reader)
        if len(rows) != contract["rows"] or any(None in r or None in r.values() for r in rows):
            raise ValueError(f"{name}: invalid rows")
        tables[name] = rows
    for child, field, parent, key in manifest["references"]:
        parents = {row[key] for row in tables[parent]}
        unresolved = {row[field] for row in tables[child] if row[field]} - parents
        if unresolved:
            raise ValueError(f"{child}.{field}: missing {parent}.{key}: {sorted(unresolved)}")
    for row in tables.get("mutations", []):
        if not isinstance(json.loads(row["ops"]), list):
            raise ValueError("mutations.ops must contain a JSON array")
    return {"input_pack": manifest["pack"], "tables": {name: len(rows) for name, rows in tables.items()}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args()
    print(json.dumps(inspect_inputs(args.data), sort_keys=True))
