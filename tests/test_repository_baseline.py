"""Baseline checks for the files currently present in paramecia-core.

These are structural/safety checks, NOT approval or canon promotion.
"""
import json
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class RepositoryBaselineTests(unittest.TestCase):
    def test_every_json_file_parses(self):
        paths = sorted(ROOT.rglob("*.json"))
        self.assertTrue(paths, "No JSON files found")
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                json.loads(path.read_text(encoding="utf-8"))

    def test_alias_ids_are_unique(self):
        entries = load("canon/registries/aliases.json")["entries"]
        ids = [entry["canonical_id"] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))

    def test_correction_ids_are_unique(self):
        entries = load("canon/registries/corrections.json")["entries"]
        ids = [entry["correction_id"] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))

    def test_region_ids_are_unique(self):
        regions = load("canon/regions/region-canon-status.json")["regions"]
        ids = [region["id"] for region in regions]
        self.assertEqual(len(ids), len(set(ids)))

    def test_canon_authority_requires_creator_declaration(self):
        governance = load("canon/registries/canon-governance.json")
        self.assertEqual(governance["authority"]["root"], "creator_explicit_declaration")
        self.assertIn("Only an explicit creator declaration", governance["authority"]["rule"])

    def test_corrections_preserve_history(self):
        policy = load("canon/registries/corrections.json")["policy"]
        self.assertIs(policy["corrections_are_first_class_events"], True)
        self.assertIs(policy["preserve_superseded_values"], True)

    def test_felix_runtime_never_promotes_without_authority(self):
        runtime = runpy.run_path(str(ROOT / "integrations/felix-null/agent/runtime.py"))
        for state in runtime["CanonState"]:
            with self.subTest(state=state):
                self.assertFalse(runtime["can_promote_to_canon"](state, False))


if __name__ == "__main__":
    unittest.main()
