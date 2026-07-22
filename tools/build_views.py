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
    systems = []
    decisions_by_system: dict[str, list[dict]] = {}
    for path in sorted((root / "catalog" / "coverage").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        decisions_by_system.setdefault(data["reference_system_id"], []).append(
            {key: data[key] for key in ("candidate_id", "candidate_label", "decision", "reason") if key in data}
            | ({"target_entity_id": data["target_entity_id"]} if "target_entity_id" in data else {})
        )
    for path in sorted((root / "catalog" / "reference-systems").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        decisions = sorted(decisions_by_system.get(data["id"], []), key=lambda item: item["candidate_id"])
        decision_counts = {
            decision: sum(item["decision"] == decision for item in decisions)
            for decision in ("included", "merged", "excluded", "pending")
        }
        complete = set(data["candidate_ids"]) == {item["candidate_id"] for item in decisions}
        systems.append({
            "id": data["id"],
            "title": data["title"],
            "authority": data["authority"],
            "scope": data["scope"],
            "version": data["version"],
            "retrieved_at": data["retrieved_at"],
            "candidate_count": len(data["candidate_ids"]),
            "decision_count": len(decisions),
            "decision_counts": decision_counts,
            "complete": complete,
            "resolved": complete and decision_counts["pending"] == 0,
            "decisions": decisions,
        })
    coverage_output = root / "views" / "generated" / "coverage-report.json"
    coverage_output.write_text(json.dumps({"reference_systems": systems}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return output


if __name__ == "__main__":
    print(build())
