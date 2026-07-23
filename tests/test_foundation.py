from __future__ import annotations

import json
import multiprocessing
import shutil
import sys
import time
import unittest
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_views import build
from store import LockTimeoutError, atomic_write_json, record_lock
from validate import MAX_RECORD_BYTES, migrate_legacy_identity, validate_repository


def _hold_lock(root: str, record_id: str, ready: multiprocessing.Queue) -> None:
    with record_lock(Path(root), record_id, timeout=2):
        ready.put("locked")
        time.sleep(0.5)


def _try_lock(root: str, record_id: str, result: multiprocessing.Queue) -> None:
    try:
        with record_lock(Path(root), record_id, timeout=0.15):
            result.put("acquired")
    except LockTimeoutError:
        result.put("timeout")


def _write_record(root: str, record_id: str, result: multiprocessing.Queue) -> None:
    record = {
        "id": record_id,
        "record_type": "entity",
        "entity_type": "theory",
        "name": record_id,
        "aliases": [],
        "status": "unverified",
        "publishable": False,
        "provenance": "manual",
    }
    atomic_write_json(Path(root), Path("catalog/entities") / f"{record_id}.json", record)
    result.put(record_id)


class FoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.work = ROOT / ".test-work" / uuid.uuid4().hex
        self.work.mkdir(parents=True)
        for name in ("schemas", "catalog", "library", "knowledge", "vocabularies", "crosswalks", "views"):
            shutil.copytree(ROOT / name, self.work / name)

    def tearDown(self) -> None:
        shutil.rmtree(self.work, ignore_errors=True)

    def write_json(self, relative: str, data: dict) -> Path:
        path = self.work / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    def valid_entity(self, record_id: str) -> dict:
        return {
            "id": record_id,
            "record_type": "entity",
            "entity_type": "theory",
            "name": record_id,
            "aliases": [],
            "status": "unverified",
            "publishable": False,
            "provenance": "manual",
        }

    def valid_reference_system(self, record_id: str, candidate_ids: list[str]) -> dict:
        return {
            "id": record_id,
            "record_type": "reference_system",
            "title": record_id,
            "authority": "Test authority",
            "scope": "A bounded test inventory.",
            "version": "test-v1",
            "retrieved_at": "2026-07-22",
            "source_ids": [],
            "candidate_ids": candidate_ids,
            "status": "retrieved",
            "publishable": False,
            "provenance": "manual",
        }

    def valid_coverage(self, record_id: str, system_id: str, candidate_id: str, target_id: str) -> dict:
        return {
            "id": record_id,
            "record_type": "coverage",
            "reference_system_id": system_id,
            "candidate_id": candidate_id,
            "candidate_label": candidate_id,
            "decision": "included",
            "reason": "Explicitly included by the test reference system.",
            "target_entity_id": target_id,
            "status": "retrieved",
            "publishable": False,
            "provenance": "reference_system",
        }

    def test_repository_baseline_passes(self) -> None:
        self.assertEqual(validate_repository(ROOT), [])

    def test_empty_and_partial_json_are_rejected(self) -> None:
        empty = self.work / "catalog/entities/empty.json"
        empty.write_text("", encoding="utf-8")
        partial = self.work / "catalog/entities/partial.json"
        partial.write_text('{"id":"partial"', encoding="utf-8")
        errors = validate_repository(self.work)
        self.assertTrue(any("empty file" in error for error in errors))
        self.assertTrue(any("invalid JSON" in error for error in errors))

    def test_large_record_is_rejected(self) -> None:
        path = self.work / "catalog/entities/huge.json"
        path.write_text(" " * (MAX_RECORD_BYTES + 1), encoding="utf-8")
        self.assertTrue(any("exceeds" in error for error in validate_repository(self.work)))

    def test_unknown_field_and_duplicate_id_are_rejected(self) -> None:
        record = self.valid_entity("duplicate")
        record["legacy_verdict"] = "corroborated"
        self.write_json("catalog/entities/duplicate.json", record)
        source = {
            "id": "duplicate", "record_type": "source", "title": "x", "identifiers": {},
            "access_status": "metadata_only", "status": "unverified", "publishable": False,
            "provenance": "manual"
        }
        self.write_json("library/sources/duplicate.json", source)
        errors = validate_repository(self.work)
        self.assertTrue(any("unknown fields" in error for error in errors))
        self.assertTrue(any("duplicate id" in error for error in errors))

    def test_orphan_and_compound_claim_are_rejected(self) -> None:
        claim = {
            "id": "bad-claim", "record_type": "claim", "subject_id": "missing",
            "statement": "A 發生；B 也發生", "claim_type": "chronology", "evidence_ids": ["missing-evidence"],
            "status": "unverified", "publishable": False, "provenance": "manual"
        }
        self.write_json("knowledge/claims/bad-claim.json", claim)
        errors = validate_repository(self.work)
        self.assertTrue(any("orphan subject_id" in error for error in errors))
        self.assertTrue(any("compound claim" in error for error in errors))

    def test_metadata_only_cannot_support_publishable_evidence(self) -> None:
        source = {
            "id": "meta-source", "record_type": "source", "title": "Metadata", "identifiers": {},
            "access_status": "metadata_only", "status": "retrieved", "publishable": False,
            "provenance": "manual"
        }
        claim = {
            "id": "publish-claim", "record_type": "claim", "subject_id": "cbt",
            "statement": "A single testable statement", "claim_type": "identity", "evidence_ids": ["meta-evidence"],
            "status": "verified", "publishable": True, "provenance": "manual"
        }
        evidence = {
            "id": "meta-evidence", "record_type": "evidence", "claim_id": "publish-claim",
            "source_id": "meta-source", "locator": "metadata record", "evidence_level": "metadata_only",
            "status": "verified", "publishable": True, "provenance": "manual"
        }
        self.write_json("library/sources/meta-source.json", source)
        self.write_json("knowledge/claims/publish-claim.json", claim)
        self.write_json("knowledge/evidence/meta-evidence.json", evidence)
        errors = validate_repository(self.work)
        self.assertTrue(any("cannot support publishable" in error for error in errors))
        self.assertTrue(any("metadata/abstract" in error for error in errors))

    def test_legacy_migration_is_identity_only(self) -> None:
        migrated = migrate_legacy_identity({"id": "seed", "name": "Seed", "entity_type": "school"})
        self.assertEqual(migrated["status"], "unverified")
        self.assertFalse(migrated["publishable"])
        with self.assertRaises(ValueError):
            migrate_legacy_identity({"id": "seed", "name": "Seed", "entity_type": "school", "verdict": "corroborated"})

    def test_interrupted_write_preserves_existing_record(self) -> None:
        record = self.valid_entity("atomic-test")
        target = atomic_write_json(self.work, Path("catalog/entities/atomic-test.json"), record)
        before = target.read_bytes()
        broken = dict(record)
        broken["name"] = {"not-json-serializable"}
        with self.assertRaises(TypeError):
            atomic_write_json(self.work, Path("catalog/entities/atomic-test.json"), broken)
        self.assertEqual(target.read_bytes(), before)

    def test_same_record_lock_blocks_second_process(self) -> None:
        ready: multiprocessing.Queue = multiprocessing.Queue()
        result: multiprocessing.Queue = multiprocessing.Queue()
        first = multiprocessing.Process(target=_hold_lock, args=(str(self.work), "shared", ready))
        first.start()
        self.assertEqual(ready.get(timeout=2), "locked")
        second = multiprocessing.Process(target=_try_lock, args=(str(self.work), "shared", result))
        second.start()
        second.join(timeout=3)
        first.join(timeout=3)
        self.assertEqual(result.get(timeout=1), "timeout")
        self.assertEqual(second.exitcode, 0)
        self.assertEqual(first.exitcode, 0)

    def test_different_records_can_write_concurrently(self) -> None:
        result: multiprocessing.Queue = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=_write_record, args=(str(self.work), rid, result)) for rid in ("alpha", "beta")]
        for process in processes:
            process.start()
        for process in processes:
            process.join(timeout=3)
            self.assertEqual(process.exitcode, 0)
        self.assertEqual({result.get(timeout=1), result.get(timeout=1)}, {"alpha", "beta"})

    def test_generated_view_is_reproducible(self) -> None:
        build(self.work)
        first = {path.name: path.read_bytes() for path in sorted((self.work / "views/generated").glob("*.json"))}
        shutil.rmtree(self.work / "views/generated")
        build(self.work)
        second = {path.name: path.read_bytes() for path in sorted((self.work / "views/generated").glob("*.json"))}
        self.assertEqual(first, second)

    def test_private_and_publication_files_are_ignored(self) -> None:
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in (".private-sources/", "*.pdf", "*.epub", "*.mobi"):
            self.assertIn(pattern, ignore)

    def test_known_error_regression_fixture_is_not_canonical_knowledge(self) -> None:
        fixture = json.loads((ROOT / "tests/fixtures/legacy-known-errors.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(fixture["cases"]), 4)
        self.assertTrue(all("expected" in case for case in fixture["cases"]))

    def test_reference_system_requires_exact_candidate_coverage(self) -> None:
        system = self.valid_reference_system("test-system", ["alpha", "beta"])
        self.write_json("catalog/reference-systems/test-system.json", system)
        self.write_json(
            "catalog/coverage/test-system-alpha.json",
            self.valid_coverage("test-system-alpha", "test-system", "alpha", "cbt"),
        )
        errors = validate_repository(self.work)
        self.assertTrue(any("missing coverage decisions" in error and "beta" in error for error in errors))

    def test_coverage_rejects_orphan_system_and_target(self) -> None:
        coverage = self.valid_coverage("orphan-coverage", "missing-system", "alpha", "missing-entity")
        self.write_json("catalog/coverage/orphan-coverage.json", coverage)
        errors = validate_repository(self.work)
        self.assertTrue(any("orphan reference_system_id" in error for error in errors))
        self.assertTrue(any("orphan target_entity_id" in error for error in errors))

    def test_coverage_decision_target_rules_are_enforced(self) -> None:
        system = self.valid_reference_system("decision-system", ["included", "pending"])
        self.write_json("catalog/reference-systems/decision-system.json", system)
        included = self.valid_coverage("decision-included", "decision-system", "included", "cbt")
        included.pop("target_entity_id")
        pending = self.valid_coverage("decision-pending", "decision-system", "pending", "cbt")
        pending["decision"] = "pending"
        self.write_json("catalog/coverage/decision-included.json", included)
        self.write_json("catalog/coverage/decision-pending.json", pending)
        errors = validate_repository(self.work)
        self.assertTrue(any("included/merged decision requires target_entity_id" in error for error in errors))
        self.assertTrue(any("pending/excluded decision must not have target_entity_id" in error for error in errors))

    def test_duplicate_candidate_decisions_are_rejected(self) -> None:
        system = self.valid_reference_system("duplicate-system", ["alpha"])
        self.write_json("catalog/reference-systems/duplicate-system.json", system)
        first = self.valid_coverage("duplicate-first", "duplicate-system", "alpha", "cbt")
        second = self.valid_coverage("duplicate-second", "duplicate-system", "alpha", "cbt")
        self.write_json("catalog/coverage/duplicate-first.json", first)
        self.write_json("catalog/coverage/duplicate-second.json", second)
        self.assertTrue(any("duplicate candidate decision" in error for error in validate_repository(self.work)))

    def test_malformed_reference_system_input_is_rejected_without_crashing(self) -> None:
        system = self.valid_reference_system("malformed-system", [["not", "an", "id"]])
        system["source_ids"] = [{"not": "an id"}]
        system["retrieved_at"] = "not-a-date"
        self.write_json("catalog/reference-systems/malformed-system.json", system)
        errors = validate_repository(self.work)
        self.assertTrue(any("invalid candidate_id" in error for error in errors))
        self.assertTrue(any("invalid source_id" in error for error in errors))
        self.assertTrue(any("retrieved_at must be an ISO date" in error for error in errors))

    def test_p1_reference_system_coverage_is_complete(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        apa = next(item for item in report["reference_systems"] if item["id"] == "apa-coa-postdoctoral-specialty-practice-areas")
        self.assertEqual(apa["candidate_count"], 11)
        self.assertEqual(apa["decision_count"], 11)
        self.assertTrue(apa["complete"])
        self.assertTrue(apa["resolved"])
        self.assertEqual(apa["decision_counts"]["pending"], 0)

    def test_anzsrc_group_coverage_preserves_scope_and_residual_boundary(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        anzsrc = next(item for item in report["reference_systems"] if item["id"] == "anzsrc-2020-for-psychology-groups")
        self.assertEqual(anzsrc["candidate_count"], 6)
        self.assertEqual(anzsrc["decision_count"], 6)
        self.assertTrue(anzsrc["complete"])
        self.assertTrue(anzsrc["resolved"])
        decisions = {item["candidate_id"]: item for item in anzsrc["decisions"]}
        self.assertEqual(decisions["anzsrc-5202"]["decision"], "included")
        self.assertEqual(decisions["anzsrc-5202"]["target_entity_id"], "biological-psychology")
        self.assertEqual(decisions["anzsrc-5203"]["target_entity_id"], "clinical-and-health-psychology")
        self.assertNotEqual(decisions["anzsrc-5203"]["target_entity_id"], "clinical-health-psychology")
        self.assertEqual(decisions["anzsrc-5299"]["decision"], "excluded")
        self.assertNotIn("target_entity_id", decisions["anzsrc-5299"])

    def test_anzsrc_field_inventory_is_complete_and_resolved(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        fields = next(item for item in report["reference_systems"] if item["id"] == "anzsrc-2020-for-psychology-fields")
        self.assertEqual(fields["candidate_count"], 36)
        self.assertEqual(fields["decision_count"], 36)
        self.assertTrue(fields["complete"])
        self.assertTrue(fields["resolved"])
        self.assertEqual(
            fields["decision_counts"],
            {"included": 28, "merged": 2, "excluded": 6, "pending": 0},
        )
        decisions = {item["candidate_id"]: item for item in fields["decisions"]}
        self.assertEqual(decisions["anzsrc-520103"]["target_entity_id"], "forensic-psychology")
        self.assertEqual(decisions["anzsrc-520199"]["decision"], "excluded")
        self.assertEqual(decisions["anzsrc-520201"]["decision"], "included")

    def test_anzsrc_5202_batch_is_resolved(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        fields = next(item for item in report["reference_systems"] if item["id"] == "anzsrc-2020-for-psychology-fields")
        decisions = {item["candidate_id"]: item for item in fields["decisions"]}
        substantive = [decisions[f"anzsrc-52020{number}"] for number in range(1, 8)]
        self.assertTrue(all(item["decision"] == "included" for item in substantive))
        self.assertTrue(all("target_entity_id" in item for item in substantive))
        self.assertEqual(decisions["anzsrc-520299"]["decision"], "excluded")
        self.assertNotIn("target_entity_id", decisions["anzsrc-520299"])

    def test_anzsrc_5203_batch_is_resolved(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        fields = next(item for item in report["reference_systems"] if item["id"] == "anzsrc-2020-for-psychology-fields")
        decisions = {item["candidate_id"]: item for item in fields["decisions"]}
        self.assertEqual(decisions["anzsrc-520301"]["decision"], "merged")
        self.assertEqual(decisions["anzsrc-520301"]["target_entity_id"], "clinical-neuropsychology")
        substantive = [decisions[f"anzsrc-52030{number}"] for number in range(2, 5)]
        self.assertTrue(all(item["decision"] == "included" for item in substantive))
        self.assertTrue(all("target_entity_id" in item for item in substantive))
        self.assertNotEqual(decisions["anzsrc-520304"]["target_entity_id"], "clinical-health-psychology")
        self.assertEqual(decisions["anzsrc-520399"]["decision"], "excluded")
        self.assertNotIn("target_entity_id", decisions["anzsrc-520399"])

    def test_anzsrc_5204_batch_is_resolved_as_research_fields(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        fields = next(item for item in report["reference_systems"] if item["id"] == "anzsrc-2020-for-psychology-fields")
        decisions = {item["candidate_id"]: item for item in fields["decisions"]}
        substantive = [decisions[f"anzsrc-52040{number}"] for number in range(1, 7)]
        self.assertTrue(all(item["decision"] == "included" for item in substantive))
        self.assertTrue(all("target_entity_id" in item for item in substantive))
        cognition = json.loads((self.work / "catalog/entities/cognition.json").read_text(encoding="utf-8"))
        self.assertEqual(cognition["entity_type"], "subfield")
        self.assertIn("not a claim", cognition["notes"])
        self.assertEqual(decisions["anzsrc-520499"]["decision"], "excluded")
        self.assertNotIn("target_entity_id", decisions["anzsrc-520499"])

    def test_anzsrc_5205_batch_closes_field_inventory(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        fields = next(item for item in report["reference_systems"] if item["id"] == "anzsrc-2020-for-psychology-fields")
        decisions = {item["candidate_id"]: item for item in fields["decisions"]}
        substantive = [decisions[f"anzsrc-52050{number}"] for number in range(1, 6)]
        self.assertTrue(all(item["decision"] == "included" for item in substantive))
        self.assertTrue(all("target_entity_id" in item for item in substantive))
        self.assertEqual(decisions["anzsrc-520504"]["target_entity_id"], "psychology-of-religion")
        self.assertEqual(decisions["anzsrc-520599"]["decision"], "excluded")
        self.assertNotIn("target_entity_id", decisions["anzsrc-520599"])
        self.assertTrue(fields["resolved"])

    def test_iaap_active_division_inventory_is_complete_and_resolved(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        iaap = next(item for item in report["reference_systems"] if item["id"] == "iaap-active-divisions")
        self.assertEqual(iaap["candidate_count"], 18)
        self.assertEqual(iaap["decision_count"], 18)
        self.assertTrue(iaap["complete"])
        self.assertTrue(iaap["resolved"])
        self.assertEqual(
            iaap["decision_counts"],
            {"included": 12, "merged": 4, "excluded": 2, "pending": 0},
        )
        decisions = {item["candidate_id"]: item for item in iaap["decisions"]}
        self.assertEqual(
            decisions["iaap-division-01"]["target_entity_id"],
            "industrial-and-organisational-psychology",
        )
        self.assertEqual(decisions["iaap-division-08"]["target_entity_id"], "health-psychology")
        self.assertEqual(
            decisions["iaap-division-12"]["target_entity_id"],
            "sport-and-exercise-psychology",
        )
        self.assertEqual(decisions["iaap-division-16"]["target_entity_id"], "counselling-psychology")
        self.assertEqual(decisions["iaap-division-15"]["decision"], "excluded")
        self.assertEqual(decisions["iaap-division-17"]["decision"], "excluded")
        self.assertNotIn("target_entity_id", decisions["iaap-division-15"])
        self.assertNotIn("target_entity_id", decisions["iaap-division-17"])
        self.assertNotEqual(
            decisions["iaap-division-05"]["target_entity_id"],
            "educational-psychology",
        )

    def test_indigenous_studies_group_inventory_is_complete_but_pending(self) -> None:
        build(self.work)
        report = json.loads((self.work / "views/generated/coverage-report.json").read_text(encoding="utf-8"))
        indigenous = next(
            item
            for item in report["reference_systems"]
            if item["id"] == "anzsrc-2020-for-indigenous-studies-groups"
        )
        self.assertEqual(indigenous["candidate_count"], 20)
        self.assertEqual(indigenous["decision_count"], 20)
        self.assertTrue(indigenous["complete"])
        self.assertFalse(indigenous["resolved"])
        self.assertEqual(
            indigenous["decision_counts"],
            {"included": 0, "merged": 0, "excluded": 1, "pending": 19},
        )
        decisions = {item["candidate_id"]: item for item in indigenous["decisions"]}
        self.assertIn("Māori", decisions["anzsrc-4507"]["candidate_label"])
        self.assertEqual(decisions["anzsrc-4519"]["decision"], "pending")
        self.assertEqual(decisions["anzsrc-4599"]["decision"], "excluded")
        self.assertNotIn("target_entity_id", decisions["anzsrc-4599"])


if __name__ == "__main__":
    multiprocessing.freeze_support()
    unittest.main()
