from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


audit_module = load_module("audit_source_packs", ROOT / "tools" / "audit_source_packs.py")
collector = load_module("collect_sources", ROOT / "tools" / "collect_sources.py")


class SourceCollectionTests(unittest.TestCase):
    def test_fixed_programme_has_48_unique_ordered_targets_and_packs(self) -> None:
        self.assertEqual(audit_module.audit(ROOT), [])

    def test_media_type_uses_body_signature_for_pdf_and_html(self) -> None:
        self.assertEqual(collector.media_type("text/html", b"%PDF-1.7\n"), "application/pdf")
        self.assertEqual(collector.media_type("application/pdf", b"<!doctype html>"), "text/html")

    def test_audit_rejects_cache_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            (work / "research/source-packs").mkdir(parents=True)
            programme = json.loads((ROOT / "research/targets.json").read_text(encoding="utf-8"))
            (work / "research/targets.json").write_text(
                json.dumps(programme, ensure_ascii=False), encoding="utf-8"
            )
            for source in (ROOT / "research/source-packs").glob("*.json"):
                (work / "research/source-packs" / source.name).write_text(
                    source.read_text(encoding="utf-8"), encoding="utf-8"
                )
            path = work / "research/source-packs/individual-psychology.json"
            pack = json.loads(path.read_text(encoding="utf-8"))
            pack["items"] = [{
                "id": "escape-test",
                "slot": "identity_history",
                "status": "retrieved",
                "retrieval": {
                    "retrieved_at": "2026-07-28T00:00:00+00:00",
                    "sha256": "0" * 64,
                    "bytes": 1,
                    "media_type": "application/pdf",
                    "cache_key": "../outside.pdf"
                }
            }]
            path.write_text(json.dumps(pack), encoding="utf-8")
            errors = audit_module.audit(work)
            self.assertTrue(any("escapes .private-sources" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
