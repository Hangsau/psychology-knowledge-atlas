"""Create missing source-pack manifests from the fixed 48-target programme."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "research" / "targets.json"
PACKS = ROOT / "research" / "source-packs"

BASE_SLOTS = {
    "identity_history": "Independent scholarly identity and historical placement",
    "primary_works": "Primary works or first-generation programme statements",
    "theory_methods": "Core concepts, methods and internal variants",
    "independent_critique": "Independent historiography, criticism or boundary analysis",
    "empirical_status": "Empirical tests, syntheses, replications or current assessment",
    "current_status": "Contemporary continuation, institutions or present disciplinary status",
}
THERAPY_SLOTS = {
    "clinical_outcomes": "Systematic reviews, meta-analyses or comparative outcome research",
    "safety_guidelines": "Guidelines, limitations, adverse effects or contraindications",
}
CONTEXT_SLOTS = {
    "cultural_language_context": "Non-English, local, cultural or knowledge-sovereignty context where applicable"
}


def slots_for(target_type: str) -> dict[str, dict[str, str]]:
    slots = dict(BASE_SLOTS)
    if target_type in {"therapy", "theory_therapy", "therapy_family"}:
        slots.update(THERAPY_SLOTS)
    slots.update(CONTEXT_SLOTS)
    return {
        slot_id: {"description": description, "status": "not_searched"}
        for slot_id, description in slots.items()
    }


def main() -> int:
    programme = json.loads(TARGETS.read_text(encoding="utf-8"))
    PACKS.mkdir(parents=True, exist_ok=True)
    created = 0
    for target in programme["targets"]:
        path = PACKS / f"{target['id']}.json"
        if path.exists():
            continue
        pack = {
            "target_id": target["id"],
            "target_type": target["target_type"],
            "search_protocol_version": "1.0.0",
            "slots": slots_for(target["target_type"]),
            "searches": [],
            "items": [],
            "status": "not_started",
        }
        path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created += 1
    print(f"source packs: {len(list(PACKS.glob('*.json')))}; created: {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
