"""Run the read-only P2-SC exit gate over the 48 source packs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from audit_source_packs import audit

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


ROOT = Path(__file__).resolve().parents[1]
UNDER_20_KB = 20 * 1024
SCHEMA_CAVEAT = (
    "Slots carry only description and status, while searches[] entries have no slot linkage; "
    "therefore a searched_no_qualifying_source verdict cannot be machine-traced to the "
    "specific search that produced it. A PASS does not establish that linkage."
)
CHALLENGE_PATTERNS = (
    ("incapsula", re.compile(r"incapsula", re.IGNORECASE)),
    ("client challenge", re.compile(r"client[\s_-]+challenge", re.IGNORECASE)),
    ("just a moment", re.compile(r"just\s+a\s+moment", re.IGNORECASE)),
    ("checking your browser", re.compile(r"checking\s+your\s+browser", re.IGNORECASE)),
    ("cookies turned off", re.compile(r"cookies\s+turned\s+off", re.IGNORECASE)),
    ("proof of work", re.compile(r"proof[\s_-]+of[\s_-]+work", re.IGNORECASE)),
    (
        "enable javascript to continue",
        re.compile(r"enable\s+javascript\s+to\s+continue", re.IGNORECASE),
    ),
    ("ng-app", re.compile(r"\bng-app\b", re.IGNORECASE)),
    (
        "recaptcha challenge form",
        re.compile(
            r"<form\b(?:(?!</form>).){0,20000}?"
            r"(?:g-recaptcha|recaptcha/api2/(?:challenge|fallback)|"
            r"(?:id|class|action)=[\"'][^\"']*(?:captcha|challenge)[^\"']*[\"'])"
            r"(?:(?!</form>).)*?</form\s*>",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
)
WATERMARK_PATTERNS = (
    ("personal use only", re.compile(r"personal\s+use\s+only", re.IGNORECASE)),
    ("for personal use", re.compile(r"for\s+personal\s+use", re.IGNORECASE)),
    (
        "not to be disseminated",
        re.compile(r"not\s+to\s+be\s+disseminated", re.IGNORECASE),
    ),
    ("all use subject to", re.compile(r"all\s+use\s+subject\s+to", re.IGNORECASE)),
    ("downloaded by", re.compile(r"downloaded\s+by", re.IGNORECASE)),
    ("subscriber:", re.compile(r"subscriber\s*:", re.IGNORECASE)),
)


def new_stage(number: int, title: str) -> dict[str, Any]:
    return {
        "number": number,
        "title": title,
        "status": "PASS",
        "metrics": {},
        "failures": [],
        "notes": [],
        "items": [],
    }


def record_failure(stage: dict[str, Any], errors: list[str], message: str) -> None:
    stage["failures"].append(message)
    errors.append(f"Stage {stage['number']} ({stage['title']}): {message}")


def finish_stage(stage: dict[str, Any]) -> None:
    if stage["failures"]:
        stage["status"] = "FAIL"


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except (OSError, ValueError):
        return str(path)


def safe_cache_path(root: Path, retrieval: object) -> Path | None:
    if not isinstance(retrieval, dict):
        return None
    cache_key = retrieval.get("cache_key")
    if not isinstance(cache_key, str) or not cache_key:
        return None
    path = root / cache_key
    try:
        path.resolve().relative_to((root / ".private-sources").resolve())
    except (OSError, ValueError):
        return None
    return path


def excerpt(text: str, position: int, length: int = 200) -> str:
    start = max(0, position - length // 2)
    if len(text) >= length:
        start = min(start, len(text) - length)
    fragment = text[start : start + length]
    return fragment.replace("\r", " ").replace("\n", " ").replace("\t", " ")


def load_packs(root: Path, stage: dict[str, Any], errors: list[str]) -> list[tuple[Path, dict]]:
    packs: list[tuple[Path, dict]] = []
    for path in sorted((root / "research" / "source-packs").glob("*.json")):
        try:
            pack = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            record_failure(stage, errors, f"{relative_path(path, root)}: {exc}")
            continue
        if not isinstance(pack, dict):
            record_failure(stage, errors, f"{relative_path(path, root)}: pack must be an object")
            continue
        packs.append((path, pack))
    return packs


def item_records(packs: list[tuple[Path, dict]]) -> list[tuple[Path, dict, dict]]:
    records: list[tuple[Path, dict, dict]] = []
    for path, pack in packs:
        items = pack.get("items", [])
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict):
                records.append((path, pack, item))
    return records


def pack_label(path: Path, pack: dict) -> str:
    target_id = pack.get("target_id")
    return target_id if isinstance(target_id, str) and target_id else path.stem


def item_label(item: dict) -> str:
    item_id = item.get("id")
    return item_id if isinstance(item_id, str) and item_id else "<unknown-item>"


def build_report(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    stages: list[dict[str, Any]] = []

    baseline = new_stage(0, "Baseline source-pack audit")
    try:
        baseline_errors = audit(root, require_files=True)
    except Exception as exc:
        baseline_errors = [f"audit_source_packs.audit raised {type(exc).__name__}: {exc}"]
    for message in baseline_errors:
        record_failure(baseline, errors, message)
    baseline["metrics"] = {
        "audit_errors": len(baseline_errors),
        "require_files": True,
    }
    packs = load_packs(root, baseline, errors)
    baseline["metrics"]["packs_loaded"] = len(packs)
    finish_stage(baseline)
    stages.append(baseline)

    records = item_records(packs)
    retrieved_records = [record for record in records if record[2].get("status") == "retrieved"]
    excluded_records = [record for record in records if record[2].get("status") == "excluded"]

    adjudication = new_stage(1, "Adjudication completeness")
    audited_packs = 0
    terminal_slots = 0
    total_slots = 0
    slot_statuses: Counter[str] = Counter()
    for path, pack in packs:
        label = pack_label(path, pack)
        if pack.get("status") == "audited":
            audited_packs += 1
        else:
            record_failure(
                adjudication,
                errors,
                f"research/source-packs/{path.name}: pack status is {pack.get('status')!r}, not 'audited'",
            )
        slots = pack.get("slots", {})
        if not isinstance(slots, dict):
            record_failure(adjudication, errors, f"{label}: slots is not an object")
            continue
        for slot_id, slot in slots.items():
            total_slots += 1
            status = slot.get("status") if isinstance(slot, dict) else None
            slot_statuses[str(status)] += 1
            if status in {"covered", "searched_no_qualifying_source"}:
                terminal_slots += 1
            else:
                record_failure(
                    adjudication,
                    errors,
                    f"{label}: slot {slot_id} has non-terminal status {status!r}",
                )
    adjudication["metrics"] = {
        "audited_packs": audited_packs,
        "total_packs": len(packs),
        "terminal_slots": terminal_slots,
        "total_slots": total_slots,
        "slot_status_distribution": dict(sorted(slot_statuses.items())),
    }
    finish_stage(adjudication)
    stages.append(adjudication)

    searches_stage = new_stage(2, "Searches recorded")
    packs_with_searches = 0
    total_searches = 0
    valid_searches = 0
    for path, pack in packs:
        label = pack_label(path, pack)
        searches = pack.get("searches")
        if not isinstance(searches, list) or not searches:
            record_failure(searches_stage, errors, f"{label}: searches[] must be a non-empty list")
            continue
        packs_with_searches += 1
        total_searches += len(searches)
        for index, search in enumerate(searches):
            entry_errors: list[str] = []
            if not isinstance(search, dict):
                entry_errors.append("entry is not an object")
            else:
                if not isinstance(search.get("purpose"), str) or not search["purpose"].strip():
                    entry_errors.append("purpose is empty")
                if not isinstance(search.get("queries"), list) or not search["queries"]:
                    entry_errors.append("queries is not a non-empty list")
                if not isinstance(search.get("system"), str) or not search["system"].strip():
                    entry_errors.append("system is empty")
            if entry_errors:
                record_failure(
                    searches_stage,
                    errors,
                    f"{label}: searches[{index}] " + "; ".join(entry_errors),
                )
            else:
                valid_searches += 1
    searches_stage["metrics"] = {
        "packs_with_nonempty_searches": packs_with_searches,
        "total_packs": len(packs),
        "valid_search_entries": valid_searches,
        "total_search_entries": total_searches,
    }
    finish_stage(searches_stage)
    stages.append(searches_stage)

    consistency = new_stage(3, "Slot and item consistency")
    covered_slots = 0
    covered_slots_with_retrieved = 0
    no_source_slots = 0
    no_source_slots_without_retrieved = 0
    for path, pack in packs:
        label = pack_label(path, pack)
        slots = pack.get("slots", {})
        items = pack.get("items", [])
        if not isinstance(slots, dict) or not isinstance(items, list):
            continue
        for slot_id, slot in slots.items():
            status = slot.get("status") if isinstance(slot, dict) else None
            retrieved_ids = [
                item_label(item)
                for item in items
                if isinstance(item, dict)
                and item.get("slot") == slot_id
                and item.get("status") == "retrieved"
            ]
            if status == "covered":
                covered_slots += 1
                if retrieved_ids:
                    covered_slots_with_retrieved += 1
                else:
                    record_failure(
                        consistency,
                        errors,
                        f"{label}: covered slot {slot_id} has no retrieved item",
                    )
            elif status == "searched_no_qualifying_source":
                no_source_slots += 1
                if not retrieved_ids:
                    no_source_slots_without_retrieved += 1
                else:
                    record_failure(
                        consistency,
                        errors,
                        f"{label}: searched_no_qualifying_source slot {slot_id} has retrieved items "
                        f"{retrieved_ids}",
                    )
    consistency["metrics"] = {
        "covered_slots_with_retrieved": covered_slots_with_retrieved,
        "covered_slots": covered_slots,
        "searched_no_source_slots_without_retrieved": no_source_slots_without_retrieved,
        "searched_no_source_slots": no_source_slots,
    }
    finish_stage(consistency)
    stages.append(consistency)

    failures_stage = new_stage(4, "Failures explicit")
    documented_exclusions = 0
    for path, pack, item in excluded_records:
        rights_note = item.get("rights_note")
        if isinstance(rights_note, str) and rights_note.strip():
            documented_exclusions += 1
        else:
            record_failure(
                failures_stage,
                errors,
                f"{pack_label(path, pack)}/{item_label(item)}: excluded item has no rights_note",
            )
    failures_stage["metrics"] = {
        "excluded_items_with_rights_note": documented_exclusions,
        "excluded_items": len(excluded_records),
    }
    finish_stage(failures_stage)
    stages.append(failures_stage)

    size_stage = new_stage(5, "Declared size and media type")
    matching_sizes = 0
    media_types_present = 0
    inspectable_bodies = 0
    for path, pack, item in retrieved_records:
        label = f"{pack_label(path, pack)}/{item_label(item)}"
        retrieval = item.get("retrieval")
        if not isinstance(retrieval, dict):
            record_failure(size_stage, errors, f"{label}: retrieval metadata is unavailable")
            continue
        media_type = retrieval.get("media_type")
        if isinstance(media_type, str) and media_type.strip():
            media_types_present += 1
        else:
            record_failure(size_stage, errors, f"{label}: retrieval.media_type is empty")
        cache_path = safe_cache_path(root, retrieval)
        if cache_path is None:
            record_failure(size_stage, errors, f"{label}: cache path is not safely inspectable")
            continue
        try:
            disk_bytes = cache_path.stat().st_size
        except OSError as exc:
            record_failure(
                size_stage,
                errors,
                f"{label}: cannot read body size for {relative_path(cache_path, root)}: {exc}",
            )
            continue
        inspectable_bodies += 1
        declared_bytes = retrieval.get("bytes")
        if isinstance(declared_bytes, int) and not isinstance(declared_bytes, bool):
            if disk_bytes == declared_bytes:
                matching_sizes += 1
            else:
                record_failure(
                    size_stage,
                    errors,
                    f"{label}: {relative_path(cache_path, root)} has {disk_bytes} bytes on disk, "
                    f"but retrieval.bytes is {declared_bytes}",
                )
        else:
            record_failure(size_stage, errors, f"{label}: retrieval.bytes is not an integer")
    size_stage["metrics"] = {
        "matching_declared_sizes": matching_sizes,
        "media_types_present": media_types_present,
        "inspectable_bodies": inspectable_bodies,
        "retrieved_items": len(retrieved_records),
    }
    finish_stage(size_stage)
    stages.append(size_stage)

    challenge_stage = new_stage(6, "Bot-challenge shell detection")
    under_20_bodies = 0
    marker_hits = 0
    for path, pack, item in retrieved_records:
        retrieval = item.get("retrieval")
        cache_path = safe_cache_path(root, retrieval)
        if cache_path is None:
            continue
        try:
            disk_bytes = cache_path.stat().st_size
        except OSError:
            continue
        if disk_bytes >= UNDER_20_KB:
            continue
        under_20_bodies += 1
        media_type = retrieval.get("media_type") if isinstance(retrieval, dict) else None
        body_entry = {
            "kind": "under_20kb_body",
            "pack": pack_label(path, pack),
            "item_id": item_label(item),
            "file": relative_path(cache_path, root),
            "bytes": disk_bytes,
            "media_type": media_type,
        }
        challenge_stage["items"].append(body_entry)
        try:
            text = cache_path.read_bytes().decode("utf-8", errors="replace")
        except OSError as exc:
            record_failure(
                challenge_stage,
                errors,
                f"{body_entry['file']}: cannot read under-20 KB body: {exc}",
            )
            continue
        hits: list[tuple[str, re.Match[str]]] = []
        for marker, pattern in CHALLENGE_PATTERNS:
            match = pattern.search(text)
            if match:
                hits.append((marker, match))
        if hits:
            marker_hits += 1
            first_match = min((match for _, match in hits), key=lambda match: match.start())
            hit_entry = {
                "kind": "challenge_marker_hit",
                "pack": body_entry["pack"],
                "item_id": body_entry["item_id"],
                "file": body_entry["file"],
                "bytes": disk_bytes,
                "media_type": media_type,
                "markers": [marker for marker, _ in hits],
                "excerpt": excerpt(text, first_match.start()),
            }
            challenge_stage["items"].append(hit_entry)
            record_failure(
                challenge_stage,
                errors,
                f"{body_entry['file']} ({disk_bytes} bytes) matched challenge markers "
                f"{hit_entry['markers']}; human adjudication is required",
            )
    challenge_stage["metrics"] = {
        "under_20kb_bodies": under_20_bodies,
        "bodies_with_marker_hits": marker_hits,
        "threshold_bytes_exclusive": UNDER_20_KB,
    }
    challenge_stage["notes"].append(
        "Every under-20 KB body is listed above. A reCAPTCHA script tag alone is not treated as "
        "a challenge form; every reported marker hit still requires human adjudication."
    )
    finish_stage(challenge_stage)
    stages.append(challenge_stage)

    watermark_stage = new_stage(7, "Rights watermark scan")
    pdf_bodies = 0
    pdfs_with_extractable_text = 0
    extraction_notes = 0
    watermark_hits = 0
    if PdfReader is None:
        record_failure(
            watermark_stage,
            errors,
            "pypdf is not installed, so cached PDFs could not be scanned",
        )
    else:
        for path, pack, item in retrieved_records:
            retrieval = item.get("retrieval")
            cache_path = safe_cache_path(root, retrieval)
            if cache_path is None or not isinstance(retrieval, dict):
                continue
            media_type = retrieval.get("media_type")
            is_pdf = (
                isinstance(media_type, str)
                and media_type.lower().split(";", 1)[0].strip() == "application/pdf"
            ) or cache_path.suffix.lower() == ".pdf"
            if not is_pdf:
                continue
            pdf_bodies += 1
            file_name = relative_path(cache_path, root)
            page_texts: list[str] = []
            page_errors: list[str] = []
            try:
                reader = PdfReader(cache_path)
                page_count = min(3, len(reader.pages))
                for page_index in range(page_count):
                    try:
                        extracted = reader.pages[page_index].extract_text()
                    except Exception as exc:
                        page_errors.append(f"page {page_index + 1}: {type(exc).__name__}: {exc}")
                        continue
                    if isinstance(extracted, str) and extracted.strip():
                        page_texts.append(extracted)
            except Exception as exc:
                page_errors.append(f"{type(exc).__name__}: {exc}")
            text = "\n".join(page_texts)
            if text.strip():
                pdfs_with_extractable_text += 1
                matches: list[tuple[str, re.Match[str]]] = []
                for phrase, pattern in WATERMARK_PATTERNS:
                    match = pattern.search(text)
                    if match:
                        matches.append((phrase, match))
                if matches:
                    watermark_hits += 1
                    first_match = min((match for _, match in matches), key=lambda match: match.start())
                    hit_entry = {
                        "kind": "rights_watermark_hit",
                        "pack": pack_label(path, pack),
                        "item_id": item_label(item),
                        "file": file_name,
                        "phrases": [phrase for phrase, _ in matches],
                        "excerpt": excerpt(text, first_match.start()),
                    }
                    watermark_stage["items"].append(hit_entry)
                    record_failure(
                        watermark_stage,
                        errors,
                        f"{file_name} matched rights watermark phrases {hit_entry['phrases']}; "
                        "human adjudication is required",
                    )
            if not text.strip() or page_errors:
                extraction_notes += 1
                note_entry = {
                    "kind": "pdf_text_extraction_note",
                    "pack": pack_label(path, pack),
                    "item_id": item_label(item),
                    "file": file_name,
                    "extractable_text_found": bool(text.strip()),
                    "details": page_errors or ["No text was extracted from the first three pages"],
                }
                watermark_stage["items"].append(note_entry)
    watermark_stage["metrics"] = {
        "pdf_bodies": pdf_bodies,
        "pdfs_with_extractable_text": pdfs_with_extractable_text,
        "pdf_extraction_notes": extraction_notes,
        "pdfs_with_watermark_hits": watermark_hits,
        "pages_scanned_per_pdf": 3,
    }
    watermark_stage["notes"].append(
        "PDF text-extraction problems are informational because some legacy-font PDFs remain "
        "readable by eye; watermark phrase hits are failures requiring adjudication."
    )
    finish_stage(watermark_stage)
    stages.append(watermark_stage)

    shared_stage = new_stage(8, "Cross-pack shared bodies")
    bodies_by_hash: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for path, pack, item in retrieved_records:
        retrieval = item.get("retrieval")
        digest = retrieval.get("sha256") if isinstance(retrieval, dict) else None
        if not isinstance(digest, str) or not digest:
            continue
        cache_path = safe_cache_path(root, retrieval)
        bodies_by_hash[digest].append(
            {
                "pack": pack_label(path, pack),
                "item_id": item_label(item),
                "file": relative_path(cache_path, root) if cache_path else "<unsafe-cache-path>",
            }
        )
    shared_groups = 0
    shared_references = 0
    for digest, entries in sorted(bodies_by_hash.items()):
        if len({entry["pack"] for entry in entries}) < 2:
            continue
        shared_groups += 1
        shared_references += len(entries)
        shared_stage["items"].append(
            {
                "kind": "cross_pack_shared_body",
                "sha256": digest,
                "references": sorted(entries, key=lambda entry: (entry["pack"], entry["item_id"])),
            }
        )
    shared_stage["metrics"] = {
        "shared_hash_groups": shared_groups,
        "item_references_in_shared_groups": shared_references,
        "unique_retrieved_hashes": len(bodies_by_hash),
    }
    shared_stage["notes"].append(
        "Cross-pack shared hashes are informational and are not counted as independent sources."
    )
    finish_stage(shared_stage)
    stages.append(shared_stage)

    tally_stage = new_stage(9, "Tally")
    tally_stage["metrics"] = {
        "audited_packs": audited_packs,
        "retrieved_bodies": len(retrieved_records),
        "excluded_items": len(excluded_records),
        "slot_status_distribution": dict(sorted(slot_statuses.items())),
    }
    finish_stage(tally_stage)
    stages.append(tally_stage)

    return {
        "tool": "p2sc_exit_gate",
        "root": str(root),
        "read_only": True,
        "stages": stages,
        "schema_caveat": SCHEMA_CAVEAT,
        "failure_count": len(errors),
        "failures": errors,
        "result": "FAIL" if errors else "PASS",
    }


def format_value(value: object) -> str:
    if isinstance(value, (dict, list, bool)) or value is None:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def print_text_report(report: dict[str, Any]) -> None:
    print("P2-SC EXIT GATE REPORT")
    print(f"Root: {report['root']}")
    print(f"Read-only: {str(report['read_only']).lower()}")
    for stage in report["stages"]:
        print()
        print(f"[Stage {stage['number']}] {stage['title']}")
        print(f"Status: {stage['status']}")
        print("Metrics:")
        for name, value in stage["metrics"].items():
            print(f"  - {name}: {format_value(value)}")
        if stage["failures"]:
            print("Failures:")
            for failure in stage["failures"]:
                print(f"  - {failure}")
        else:
            print("Failures: none")
        if stage["notes"]:
            print("Notes:")
            for note in stage["notes"]:
                print(f"  - {note}")
        if stage["items"]:
            print("Items:")
            for item in stage["items"]:
                print(f"  - {json.dumps(item, ensure_ascii=False, sort_keys=True)}")
    print()
    print(f"CAVEAT: {report['schema_caveat']}")
    print(f"Failure count: {report['failure_count']}")
    print(f"FINAL RESULT: {report['result']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the read-only P2-SC exit gate")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true", help="emit the report as JSON")
    args = parser.parse_args()
    report = build_report(args.root.resolve())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text_report(report)
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
