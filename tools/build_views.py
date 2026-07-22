"""Build deterministic generated indexes from canonical records."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build(root: Path = ROOT) -> Path:
    entities = []
    for path in sorted((root / "catalog" / "entities").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        entities.append({key: data[key] for key in ("id", "entity_type", "name", "status", "publishable")})
    output = root / "views" / "generated" / "entity-index.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"entities": entities}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return output


if __name__ == "__main__":
    print(build())
