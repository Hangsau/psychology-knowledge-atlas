"""Build deterministic generated indexes and reader profiles from canonical records."""

from __future__ import annotations

import json
import os
import re
import uuid
from pathlib import Path
from typing import Any

from store import record_lock


ROOT = Path(__file__).resolve().parents[1]
MAX_PROFILE_SPEC_BYTES = 2 * 1024 * 1024
MAX_COMPARISON_SPEC_BYTES = 2 * 1024 * 1024
SAFE_SPEC_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _load_directory(directory: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        record_id = data.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise ValueError(f"{path}: missing id")
        if record_id in records:
            raise ValueError(f"{path}: duplicate id {record_id}")
        records[record_id] = data
    return records


def _atomic_write_text(target: Path, payload: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    try:
        temp.write_text(payload, encoding="utf-8", newline="\n")
        os.replace(temp, target)
    finally:
        if temp.exists():
            temp.unlink()


def _json_payload(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _require_record(records: dict[str, dict[str, Any]], record_id: str, kind: str) -> dict[str, Any]:
    try:
        return records[record_id]
    except KeyError as exc:
        raise ValueError(f"reader profile references missing {kind} {record_id!r}") from exc


def _validate_profile_spec(spec: dict[str, Any], path: Path) -> None:
    allowed = {"id", "entity_id", "language", "sections", "relation_ids"}
    unknown = set(spec).difference(allowed)
    if unknown:
        raise ValueError(f"{path}: unknown profile fields {sorted(unknown)}")
    for field in ("id", "entity_id", "language"):
        if not isinstance(spec.get(field), str) or not spec[field].strip():
            raise ValueError(f"{path}: {field} must be a non-empty string")
    sections = spec.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError(f"{path}: sections must be a non-empty array")
    seen_sections: set[str] = set()
    seen_claims: set[str] = set()
    for section in sections:
        if not isinstance(section, dict) or set(section) != {"id", "title", "claim_ids"}:
            raise ValueError(f"{path}: each section requires only id, title and claim_ids")
        if not isinstance(section["id"], str) or not section["id"].strip():
            raise ValueError(f"{path}: section id must be a non-empty string")
        if section["id"] in seen_sections:
            raise ValueError(f"{path}: duplicate section id {section['id']!r}")
        seen_sections.add(section["id"])
        if not isinstance(section["title"], str) or not section["title"].strip():
            raise ValueError(f"{path}: section title must be a non-empty string")
        claim_ids = section["claim_ids"]
        if not isinstance(claim_ids, list) or not claim_ids:
            raise ValueError(f"{path}: section claim_ids must be a non-empty array")
        for claim_id in claim_ids:
            if not isinstance(claim_id, str) or not claim_id:
                raise ValueError(f"{path}: invalid claim id")
            if claim_id in seen_claims:
                raise ValueError(f"{path}: duplicate claim id {claim_id!r}")
            seen_claims.add(claim_id)
    relation_ids = spec.get("relation_ids")
    if not isinstance(relation_ids, list) or len(relation_ids) != len(set(relation_ids)):
        raise ValueError(f"{path}: relation_ids must be a unique array")


def _build_reader_profile(root: Path, spec_path: Path) -> tuple[Path, Path]:
    if spec_path.stat().st_size == 0:
        raise ValueError(f"{spec_path}: empty profile spec")
    if spec_path.stat().st_size > MAX_PROFILE_SPEC_BYTES:
        raise ValueError(f"{spec_path}: profile spec exceeds {MAX_PROFILE_SPEC_BYTES} bytes")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise ValueError(f"{spec_path}: profile must be an object")
    _validate_profile_spec(spec, spec_path)

    entities = _load_directory(root / "catalog" / "entities")
    claims = _load_directory(root / "knowledge" / "claims")
    evidence = _load_directory(root / "knowledge" / "evidence")
    sources = _load_directory(root / "library" / "sources")
    relations = _load_directory(root / "knowledge" / "relations")
    entity = _require_record(entities, spec["entity_id"], "entity")

    output_sections = []
    used_source_ids: set[str] = set()
    for section in spec["sections"]:
        output_claims = []
        for claim_id in section["claim_ids"]:
            claim = _require_record(claims, claim_id, "claim")
            if claim.get("status") != "verified" or claim.get("publishable") is not True:
                raise ValueError(f"reader profile claim {claim_id!r} is not verified and publishable")
            if spec["language"] == "zh-Hant" and not claim.get("statement_zh"):
                raise ValueError(f"reader profile claim {claim_id!r} lacks statement_zh")
            output_evidence = []
            for evidence_id in claim["evidence_ids"]:
                item = _require_record(evidence, evidence_id, "evidence")
                if item.get("status") != "verified" or item.get("publishable") is not True:
                    continue
                source = _require_record(sources, item["source_id"], "source")
                used_source_ids.add(source["id"])
                output_evidence.append(item | {"source": source})
            if not output_evidence:
                raise ValueError(f"reader profile claim {claim_id!r} has no publishable evidence")
            output_claims.append(claim | {"evidence": output_evidence})
        output_sections.append({"id": section["id"], "title": section["title"], "claims": output_claims})

    output_relations = []
    for relation_id in spec["relation_ids"]:
        relation = _require_record(relations, relation_id, "relation")
        if relation.get("status") != "verified" or relation.get("publishable") is not True:
            raise ValueError(f"reader profile relation {relation_id!r} is not verified and publishable")
        relation_evidence = []
        for evidence_id in relation["evidence_ids"]:
            item = _require_record(evidence, evidence_id, "evidence")
            if item.get("status") == "verified" and item.get("publishable") is True:
                relation_evidence.append(item)
        if not relation_evidence:
            raise ValueError(f"reader profile relation {relation_id!r} has no publishable evidence")
        output_relations.append(
            relation
            | {
                "subject": _require_record(entities, relation["subject_id"], "entity"),
                "object": _require_record(entities, relation["object_id"], "entity"),
                "evidence": relation_evidence,
            }
        )

    dossier = {
        "id": spec["id"],
        "language": spec["language"],
        "entity": entity,
        "sections": output_sections,
        "relations": output_relations,
        "sources": [sources[source_id] for source_id in sorted(used_source_ids)],
    }
    lines = [
        f"# {entity['name']}",
        "",
        "> 此頁由 canonical claims、evidence、sources 與 relations 自動生成；原始引文保留來源語言。",
        "",
    ]
    for section in output_sections:
        lines.extend([f"## {section['title']}", ""])
        for claim in section["claims"]:
            lines.extend(
                [
                    f"### {claim['statement_zh']}",
                    "",
                    f"- Claim：`{claim['id']}`",
                    f"- 英文原子主張：{claim['statement']}",
                    f"- 範圍限制：{claim.get('scope_note', '未另列')}",
                    "- 證據：",
                    "",
                ]
            )
            for item in claim["evidence"]:
                source = item["source"]
                title = source["title"]
                source_label = f"[{title}]({source['url']})" if source.get("url") else title
                lines.extend(
                    [
                        f"  - {source_label}；{item['locator']}",
                        f"    > {item['short_quote']}",
                        "",
                    ]
                )
    lines.extend(["## 關係與後續影響", ""])
    relation_labels = {"influenced": "影響", "opposed": "反對"}
    for relation in output_relations:
        label = relation_labels.get(relation["relation_type"], relation["relation_type"])
        lines.extend(
            [
                f"- {relation['subject']['name']} —{label}→ {relation['object']['name']}",
                f"  - 限定：{relation.get('scope_note', '未另列')}",
                f"  - Relation：`{relation['id']}`",
                "",
            ]
        )
    lines.extend(["## 來源索引", ""])
    for source in dossier["sources"]:
        label = f"[{source['title']}]({source['url']})" if source.get("url") else source["title"]
        lines.append(f"- {label} (`{source['id']}`)")
    lines.append("")

    output_dir = root / "views" / "generated"
    json_output = output_dir / f"{spec['id']}.json"
    markdown_output = output_dir / f"{spec['id']}.md"
    _atomic_write_text(json_output, _json_payload(dossier))
    _atomic_write_text(markdown_output, "\n".join(lines))
    return json_output, markdown_output


def _validate_comparison_spec(spec: dict[str, Any], path: Path) -> None:
    allowed = {"id", "title", "language", "profile_ids", "scope_note"}
    unknown = set(spec).difference(allowed)
    if unknown:
        raise ValueError(f"{path}: unknown comparison fields {sorted(unknown)}")
    for field in ("id", "title", "language", "scope_note"):
        if not isinstance(spec.get(field), str) or not spec[field].strip():
            raise ValueError(f"{path}: {field} must be a non-empty string")
    if not SAFE_SPEC_ID.fullmatch(spec["id"]):
        raise ValueError(f"{path}: id must be a safe slug")
    profile_ids = spec.get("profile_ids")
    if not isinstance(profile_ids, list) or len(profile_ids) != 4:
        raise ValueError(f"{path}: profile_ids must contain exactly four entries")
    if len(profile_ids) != len(set(profile_ids)):
        raise ValueError(f"{path}: profile_ids must be unique")
    for profile_id in profile_ids:
        if not isinstance(profile_id, str) or not SAFE_SPEC_ID.fullmatch(profile_id):
            raise ValueError(f"{path}: invalid profile id {profile_id!r}")


def _summarize_profile(root: Path, profile_id: str) -> dict[str, Any]:
    spec_path = root / "views" / "specs" / f"{profile_id}.json"
    if not spec_path.is_file():
        raise ValueError(f"comparison references missing profile {profile_id!r}")
    if spec_path.stat().st_size == 0:
        raise ValueError(f"{spec_path}: empty profile spec")
    if spec_path.stat().st_size > MAX_PROFILE_SPEC_BYTES:
        raise ValueError(f"{spec_path}: profile spec exceeds {MAX_PROFILE_SPEC_BYTES} bytes")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise ValueError(f"{spec_path}: profile must be an object")
    _validate_profile_spec(spec, spec_path)
    if spec["id"] != profile_id:
        raise ValueError(f"{spec_path}: profile id does not match filename")

    entities = _load_directory(root / "catalog" / "entities")
    claims = _load_directory(root / "knowledge" / "claims")
    evidence = _load_directory(root / "knowledge" / "evidence")
    sources = _load_directory(root / "library" / "sources")
    relations = _load_directory(root / "knowledge" / "relations")
    entity = _require_record(entities, spec["entity_id"], "entity")

    claim_ids: list[str] = []
    evidence_ids: set[str] = set()
    source_ids: set[str] = set()
    claim_type_counts: dict[str, int] = {}
    sections: list[dict[str, Any]] = []
    for section in spec["sections"]:
        sections.append(
            {"id": section["id"], "title": section["title"], "claim_count": len(section["claim_ids"])}
        )
        for claim_id in section["claim_ids"]:
            claim = _require_record(claims, claim_id, "claim")
            _require_record(entities, claim["subject_id"], "entity")
            if claim.get("status") != "verified" or claim.get("publishable") is not True:
                raise ValueError(f"comparison profile claim {claim_id!r} is not verified and publishable")
            claim_ids.append(claim_id)
            claim_type = claim["claim_type"]
            claim_type_counts[claim_type] = claim_type_counts.get(claim_type, 0) + 1
            publishable_evidence = 0
            for evidence_id in claim["evidence_ids"]:
                item = _require_record(evidence, evidence_id, "evidence")
                if item.get("status") != "verified" or item.get("publishable") is not True:
                    continue
                source = _require_record(sources, item["source_id"], "source")
                evidence_ids.add(evidence_id)
                source_ids.add(source["id"])
                publishable_evidence += 1
            if publishable_evidence == 0:
                raise ValueError(f"comparison profile claim {claim_id!r} has no publishable evidence")

    relation_ids: list[str] = []
    for relation_id in spec["relation_ids"]:
        relation = _require_record(relations, relation_id, "relation")
        _require_record(entities, relation["subject_id"], "entity")
        _require_record(entities, relation["object_id"], "entity")
        if relation.get("status") != "verified" or relation.get("publishable") is not True:
            raise ValueError(f"comparison profile relation {relation_id!r} is not verified and publishable")
        relation_ids.append(relation_id)
        publishable_evidence = 0
        for evidence_id in relation["evidence_ids"]:
            item = _require_record(evidence, evidence_id, "evidence")
            if item.get("status") != "verified" or item.get("publishable") is not True:
                continue
            source = _require_record(sources, item["source_id"], "source")
            evidence_ids.add(evidence_id)
            source_ids.add(source["id"])
            publishable_evidence += 1
        if publishable_evidence == 0:
            raise ValueError(f"comparison profile relation {relation_id!r} has no publishable evidence")

    return {
        "profile_id": profile_id,
        "entity": {key: entity[key] for key in ("id", "entity_type", "name")},
        "section_count": len(sections),
        "claim_count": len(claim_ids),
        "evidence_count": len(evidence_ids),
        "source_count": len(source_ids),
        "relation_count": len(relation_ids),
        "claim_type_counts": dict(sorted(claim_type_counts.items())),
        "sections": sections,
    }


def _build_comparison_view(root: Path, spec_path: Path) -> tuple[Path, Path]:
    if spec_path.stat().st_size == 0:
        raise ValueError(f"{spec_path}: empty comparison spec")
    if spec_path.stat().st_size > MAX_COMPARISON_SPEC_BYTES:
        raise ValueError(f"{spec_path}: comparison spec exceeds {MAX_COMPARISON_SPEC_BYTES} bytes")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise ValueError(f"{spec_path}: comparison spec must be an object")
    _validate_comparison_spec(spec, spec_path)
    profiles = [_summarize_profile(root, profile_id) for profile_id in spec["profile_ids"]]
    dossier = {
        "id": spec["id"],
        "title": spec["title"],
        "language": spec["language"],
        "scope_note": spec["scope_note"],
        "profiles": profiles,
    }

    lines = [
        f"# {spec['title']}",
        "",
        "> 此比較由四份 reader profile 及其 canonical records 重生；數量不代表品質、重要性或章節語義等價。",
        "",
        spec["scope_note"],
        "",
        "| Pilot | 章節 | Claims | Evidence | Sources | Relations |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for profile in profiles:
        lines.append(
            f"| {profile['entity']['name']} | {profile['section_count']} | {profile['claim_count']} | "
            f"{profile['evidence_count']} | {profile['source_count']} | {profile['relation_count']} |"
        )
    lines.append("")
    for profile in profiles:
        lines.extend([f"## {profile['entity']['name']}", "", "### 章節覆蓋", ""])
        for section in profile["sections"]:
            lines.append(f"- {section['title']}：{section['claim_count']} claims")
        lines.extend(["", "### Claim types", ""])
        for claim_type, count in profile["claim_type_counts"].items():
            lines.append(f"- `{claim_type}`：{count}")
        lines.append("")

    output_dir = root / "views" / "generated"
    json_output = output_dir / f"{spec['id']}.json"
    markdown_output = output_dir / f"{spec['id']}.md"
    _atomic_write_text(json_output, _json_payload(dossier))
    _atomic_write_text(markdown_output, "\n".join(lines))
    return json_output, markdown_output


def _build_unlocked(root: Path) -> Path:
    entities = []
    for path in sorted((root / "catalog" / "entities").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        entities.append({key: data[key] for key in ("id", "entity_type", "name", "status", "publishable")})
    output = root / "views" / "generated" / "entity-index.json"
    _atomic_write_text(output, _json_payload({"entities": entities}))

    systems = []
    decisions_by_system: dict[str, list[dict[str, Any]]] = {}
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
        systems.append(
            {
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
            }
        )
    coverage_output = root / "views" / "generated" / "coverage-report.json"
    _atomic_write_text(coverage_output, _json_payload({"reference_systems": systems}))

    for spec_path in sorted((root / "views" / "specs").glob("*.json")):
        _build_reader_profile(root, spec_path)
    for spec_path in sorted((root / "views" / "comparisons").glob("*.json")):
        _build_comparison_view(root, spec_path)
    return output


def build(root: Path = ROOT) -> Path:
    root = root.resolve()
    with record_lock(root, "generated-views", timeout=15.0):
        return _build_unlocked(root)


if __name__ == "__main__":
    print(build())
