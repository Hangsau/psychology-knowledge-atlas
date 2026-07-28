"""Audit the 48-target source-pack corpus without third-party packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SLOT_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SLOT_STATUSES = {"not_searched", "searching", "covered", "searched_no_qualifying_source", "blocked"}
PACK_STATUSES = {"not_started", "discovering", "retrieving", "audited"}
ITEM_STATUSES = {"candidate", "selected", "retrieved", "failed", "excluded"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audit(root: Path, require_files: bool = False) -> list[str]:
    errors: list[str] = []
    target_path = root / "research" / "targets.json"
    try:
        targets = json.loads(target_path.read_text(encoding="utf-8"))["targets"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        return [f"{target_path}: {exc}"]
    ids = [target.get("id") for target in targets]
    orders = [target.get("order") for target in targets]
    if len(targets) != 48 or len(set(ids)) != 48:
        errors.append("research target programme must contain exactly 48 unique targets")
    if orders != list(range(1, 49)):
        errors.append("research target orders must be exactly 1..48")
    if any(not isinstance(target_id, str) or not ID_RE.fullmatch(target_id) for target_id in ids):
        errors.append("research target ids must be safe kebab-case ids")

    pack_dir = root / "research" / "source-packs"
    pack_paths = sorted(pack_dir.glob("*.json"))
    if {path.stem for path in pack_paths} != set(ids):
        missing = sorted(set(ids) - {path.stem for path in pack_paths})
        extra = sorted({path.stem for path in pack_paths} - set(ids))
        errors.append(f"source-pack set mismatch; missing={missing}, extra={extra}")
    target_by_id = {target["id"]: target for target in targets}
    for path in pack_paths:
        try:
            pack = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        target_id = pack.get("target_id")
        if target_id != path.stem or target_id not in target_by_id:
            errors.append(f"{path}: target_id does not resolve")
            continue
        if pack.get("target_type") != target_by_id[target_id].get("target_type"):
            errors.append(f"{path}: target_type differs from programme")
        if pack.get("status") not in PACK_STATUSES:
            errors.append(f"{path}: invalid pack status")
        slots = pack.get("slots")
        if not isinstance(slots, dict) or not slots:
            errors.append(f"{path}: slots must be a non-empty object")
            continue
        for slot_id, slot in slots.items():
            if not SLOT_ID_RE.fullmatch(slot_id) or not isinstance(slot, dict):
                errors.append(f"{path}: malformed slot {slot_id!r}")
            elif slot.get("status") not in SLOT_STATUSES:
                errors.append(f"{path}: invalid status for slot {slot_id}")
        item_ids: set[str] = set()
        for item in pack.get("items", []):
            item_id = item.get("id")
            if not isinstance(item_id, str) or not ID_RE.fullmatch(item_id):
                errors.append(f"{path}: unsafe item id {item_id!r}")
                continue
            if item_id in item_ids:
                errors.append(f"{path}: duplicate item id {item_id}")
            item_ids.add(item_id)
            if item.get("slot") not in slots:
                errors.append(f"{path}: item {item_id} has unknown slot")
            if item.get("status") not in ITEM_STATUSES:
                errors.append(f"{path}: item {item_id} has invalid status")
            if item.get("status") == "retrieved":
                retrieval = item.get("retrieval")
                if not isinstance(retrieval, dict):
                    errors.append(f"{path}: retrieved item {item_id} lacks retrieval metadata")
                    continue
                required = {"retrieved_at", "sha256", "bytes", "media_type", "cache_key"}
                if not required.issubset(retrieval):
                    errors.append(f"{path}: retrieved item {item_id} lacks {sorted(required - set(retrieval))}")
                    continue
                cache_path = root / retrieval["cache_key"]
                try:
                    cache_path.resolve().relative_to((root / ".private-sources").resolve())
                except (OSError, ValueError):
                    errors.append(f"{path}: item {item_id} cache_key escapes .private-sources")
                    continue
                if require_files and not cache_path.is_file():
                    errors.append(f"{path}: item {item_id} body missing")
                elif require_files and sha256(cache_path) != retrieval["sha256"]:
                    errors.append(f"{path}: item {item_id} checksum mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--require-files", action="store_true")
    args = parser.parse_args()
    errors = audit(args.root.resolve(), args.require_files)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("source-pack audit passed: 48 targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
