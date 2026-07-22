"""Validate canonical Psychology Knowledge Atlas records using only stdlib."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_RECORD_BYTES = 2 * 1024 * 1024

STATUS = {"unverified", "retrieved", "verified", "disputed", "excluded"}
PROVENANCE = {"legacy_seed", "reference_system", "source_derived", "manual"}
ENTITY_TYPES = {"tradition", "school", "paradigm", "theory", "model", "therapy", "subfield", "method", "construct", "person", "work", "institution", "event", "finding", "controversy"}
ACCESS_STATUSES = {"open_fulltext", "public_domain_fulltext", "repository_manuscript", "preprint", "publicly_readable_license_unclear", "privately_observed_unredistributable", "abstract_only", "metadata_only", "paywalled_unread", "unavailable"}
EVIDENCE_LEVELS = {"fulltext_direct", "fulltext_indirect", "abstract_only", "metadata_only"}
RELATION_TYPES = {"alias_of", "parent_of", "branch_of", "influenced", "opposed", "explains", "contextualizes", "compares_with", "contrasts_with", "empirical_research_on", "clinical_application", "appropriation_risk", "not_applicable"}

COMMON = {"id", "record_type", "status", "publishable", "provenance"}
ALLOWED = {
    "entity": COMMON | {"entity_type", "name", "aliases", "source_ids", "tags", "notes"},
    "source": COMMON | {"title", "identifiers", "access_status", "authors", "issued", "url", "version_note"},
    "claim": COMMON | {"subject_id", "statement", "claim_type", "evidence_ids", "scope_note"},
    "evidence": COMMON | {"claim_id", "source_id", "locator", "evidence_level", "summary", "short_quote"},
    "relation": COMMON | {"subject_id", "object_id", "relation_type", "evidence_ids", "scope_note"},
}
REQUIRED = {
    "entity": COMMON | {"entity_type", "name", "aliases"},
    "source": COMMON | {"title", "identifiers", "access_status"},
    "claim": COMMON | {"subject_id", "statement", "claim_type", "evidence_ids"},
    "evidence": COMMON | {"claim_id", "source_id", "locator", "evidence_level"},
    "relation": COMMON | {"subject_id", "object_id", "relation_type", "evidence_ids"},
}
LOCATIONS = {
    "entity": "catalog/entities",
    "source": "library/sources",
    "claim": "knowledge/claims",
    "evidence": "knowledge/evidence",
    "relation": "knowledge/relations",
}


@dataclass(frozen=True)
class Record:
    path: Path
    data: dict[str, Any]


def migrate_legacy_identity(candidate: dict[str, Any]) -> dict[str, Any]:
    """Convert only a legacy identity seed; reject prose and old verdict fields."""

    forbidden = {"synthesis", "confidence", "verdict", "reviewed", "claims"}
    found = forbidden.intersection(candidate)
    if found:
        raise ValueError(f"legacy knowledge fields are forbidden: {sorted(found)}")
    required = {"id", "name", "entity_type"}
    missing = required.difference(candidate)
    if missing:
        raise ValueError(f"missing legacy identity fields: {sorted(missing)}")
    return {
        "id": candidate["id"],
        "record_type": "entity",
        "entity_type": candidate["entity_type"],
        "name": candidate["name"],
        "aliases": list(candidate.get("aliases", [])),
        "status": "unverified",
        "publishable": False,
        "provenance": "legacy_seed",
        "source_ids": [],
        "tags": [],
        "notes": "Migrated identity-only legacy seed.",
    }


def _read_json(path: Path, errors: list[str]) -> Any | None:
    try:
        if path.stat().st_size == 0:
            errors.append(f"{path}: empty file")
            return None
        if path.stat().st_size > MAX_RECORD_BYTES:
            errors.append(f"{path}: record exceeds {MAX_RECORD_BYTES} bytes")
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON/UTF-8: {exc}")
        return None


def load_records(root: Path, errors: list[str]) -> list[Record]:
    records: list[Record] = []
    for record_type, relative in LOCATIONS.items():
        directory = root / relative
        if not directory.exists():
            errors.append(f"{directory}: required directory missing")
            continue
        for path in sorted(directory.glob("*.json")):
            data = _read_json(path, errors)
            if data is None:
                continue
            if not isinstance(data, dict):
                errors.append(f"{path}: top level must be an object")
                continue
            if data.get("record_type") != record_type:
                errors.append(f"{path}: record_type must be {record_type!r}")
            records.append(Record(path, data))
    return records


def _validate_shape(record: Record, errors: list[str]) -> None:
    data, path = record.data, record.path
    record_type = data.get("record_type")
    if record_type not in ALLOWED:
        return
    missing = REQUIRED[record_type].difference(data)
    unknown = set(data).difference(ALLOWED[record_type])
    if missing:
        errors.append(f"{path}: missing fields {sorted(missing)}")
    if unknown:
        errors.append(f"{path}: unknown fields {sorted(unknown)}")
    record_id = data.get("id")
    if not isinstance(record_id, str) or not ID_RE.fullmatch(record_id):
        errors.append(f"{path}: invalid id")
    elif path.stem != record_id:
        errors.append(f"{path}: filename must equal id {record_id!r}")
    if data.get("status") not in STATUS:
        errors.append(f"{path}: invalid status")
    if data.get("provenance") not in PROVENANCE:
        errors.append(f"{path}: invalid provenance")
    if not isinstance(data.get("publishable"), bool):
        errors.append(f"{path}: publishable must be boolean")
    if data.get("provenance") == "legacy_seed" and (data.get("status") != "unverified" or data.get("publishable") is not False):
        errors.append(f"{path}: legacy_seed must be unverified and not publishable")

    if record_type == "entity":
        if data.get("entity_type") not in ENTITY_TYPES:
            errors.append(f"{path}: invalid entity_type")
        if not isinstance(data.get("aliases"), list):
            errors.append(f"{path}: aliases must be an array")
    elif record_type == "source" and data.get("access_status") not in ACCESS_STATUSES:
        errors.append(f"{path}: invalid access_status")
    elif record_type == "evidence":
        if data.get("evidence_level") not in EVIDENCE_LEVELS:
            errors.append(f"{path}: invalid evidence_level")
        if not isinstance(data.get("locator"), str) or not data.get("locator", "").strip():
            errors.append(f"{path}: evidence locator is required")
    elif record_type == "relation" and data.get("relation_type") not in RELATION_TYPES:
        errors.append(f"{path}: invalid relation_type")
    elif record_type == "claim":
        statement = data.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            errors.append(f"{path}: statement is required")
        elif any(marker in statement for marker in ("；", ";", "以及同時", "並且還")):
            errors.append(f"{path}: likely compound claim; split into atomic claims")


def validate_repository(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for schema in sorted((root / "schemas").glob("*.json")):
        data = _read_json(schema, errors)
        if isinstance(data, dict) and not data.get("$id"):
            errors.append(f"{schema}: schema $id missing")

    records = load_records(root, errors)
    seen: dict[str, Path] = {}
    by_type: dict[str, dict[str, Record]] = {key: {} for key in LOCATIONS}
    for record in records:
        _validate_shape(record, errors)
        record_id = record.data.get("id")
        record_type = record.data.get("record_type")
        if isinstance(record_id, str):
            if record_id in seen:
                errors.append(f"{record.path}: duplicate id also used by {seen[record_id]}")
            else:
                seen[record_id] = record.path
            if record_type in by_type:
                by_type[record_type][record_id] = record

    entities, sources = by_type["entity"], by_type["source"]
    claims, evidence = by_type["claim"], by_type["evidence"]
    for record in entities.values():
        for source_id in record.data.get("source_ids", []):
            if source_id not in sources:
                errors.append(f"{record.path}: orphan source_id {source_id!r}")
    for record in claims.values():
        data = record.data
        if data.get("subject_id") not in entities:
            errors.append(f"{record.path}: orphan subject_id {data.get('subject_id')!r}")
        for evidence_id in data.get("evidence_ids", []):
            if evidence_id not in evidence:
                errors.append(f"{record.path}: orphan evidence_id {evidence_id!r}")
        if data.get("publishable") and (data.get("status") != "verified" or not data.get("evidence_ids")):
            errors.append(f"{record.path}: publishable claim requires verified status and evidence")
    for record in evidence.values():
        data = record.data
        claim = claims.get(data.get("claim_id"))
        source = sources.get(data.get("source_id"))
        if claim is None:
            errors.append(f"{record.path}: orphan claim_id {data.get('claim_id')!r}")
        if source is None:
            errors.append(f"{record.path}: orphan source_id {data.get('source_id')!r}")
        elif data.get("publishable") and source.data.get("access_status") in {"metadata_only", "abstract_only", "paywalled_unread", "unavailable"}:
            errors.append(f"{record.path}: source access cannot support publishable evidence")
        if data.get("publishable") and data.get("evidence_level") in {"metadata_only", "abstract_only"}:
            errors.append(f"{record.path}: metadata/abstract cannot be publishable evidence")
        if claim is not None and record.data.get("id") not in claim.data.get("evidence_ids", []):
            errors.append(f"{record.path}: claim does not backlink this evidence")
    for record in by_type["relation"].values():
        data = record.data
        for field in ("subject_id", "object_id"):
            if data.get(field) not in entities:
                errors.append(f"{record.path}: orphan {field} {data.get(field)!r}")
        for evidence_id in data.get("evidence_ids", []):
            if evidence_id not in evidence:
                errors.append(f"{record.path}: orphan evidence_id {evidence_id!r}")
        if data.get("publishable") and not data.get("evidence_ids"):
            errors.append(f"{record.path}: publishable relation requires evidence")

    vocabulary = _read_json(root / "vocabularies" / "entity-types.json", errors)
    if isinstance(vocabulary, dict):
        term_ids = [term.get("id") for term in vocabulary.get("terms", []) if isinstance(term, dict)]
        if len(term_ids) != len(set(term_ids)):
            errors.append("entity-types vocabulary has duplicate term ids")
    crosswalk = _read_json(root / "crosswalks" / "d1-d13.json", errors)
    if isinstance(crosswalk, dict):
        domain_ids = [item.get("id") for item in crosswalk.get("domains", []) if isinstance(item, dict)]
        if domain_ids != [f"D{i}" for i in range(1, 14)]:
            errors.append("D1-D13 crosswalk must contain exactly ordered D1 through D13")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate_repository(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print("PASS: canonical records, references, vocabularies and crosswalk are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
