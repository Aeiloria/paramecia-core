from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validators"))
sys.path.insert(0, str(ROOT / "renderers"))
from validate_locations import DEFAULT_RECORDS, LOCATION_SCHEMA_PATH, METADATA_SCHEMA_PATH, load_records, read_json, validate_records
from render_location_markdown import render


class LocationPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metadata_schema = read_json(METADATA_SCHEMA_PATH)
        cls.location_schema = read_json(LOCATION_SCHEMA_PATH)
        cls.records = load_records(DEFAULT_RECORDS)

    def test_exact_six_candidate_names_have_provenance_and_validate(self):
        expected = {"Whisperwood Village", "Memory Grove", "Riverforge", "Shadow-Edge", "Silver Canopy", "Lantern Market"}
        self.assertEqual({record["name"] for record in self.records}, expected)
        self.assertEqual(len(self.records), 6)
        self.assertEqual(validate_records(self.records, self.metadata_schema, self.location_schema), [])
        self.assertTrue(all(record["lifecycle_state"] == "candidate" for record in self.records))
        self.assertTrue(all(record["provenance"] for record in self.records))

    def test_duplicate_ids_fail_loudly(self):
        records = copy.deepcopy(self.records)
        records[1]["record_id"] = records[0]["record_id"]
        errors = validate_records(records, self.metadata_schema, self.location_schema)
        self.assertTrue(any("duplicate record_id" in error for error in errors), errors)

    def test_broken_references_fail_loudly(self):
        records = copy.deepcopy(self.records)
        records[0]["references"] = ["WW-LOC-9999"]
        errors = validate_records(records, self.metadata_schema, self.location_schema)
        self.assertTrue(any("unknown record_id" in error for error in errors), errors)

    def test_promotion_requires_recorded_approval(self):
        record = copy.deepcopy(self.records[0])
        record["lifecycle_state"] = "approved"
        errors = validate_records([record], self.metadata_schema, self.location_schema)
        self.assertTrue(any("promotion_approval" in error for error in errors), errors)

    def test_renderer_is_byte_reproducible_and_does_not_fill_missing_details(self):
        first = render(self.records)
        second = render(self.records)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 6)
        self.assertIn("Fields awaiting source recovery", first["WW-LOC-0001.md"])
        self.assertIn("candidate", first["WW-LOC-0001.md"])


if __name__ == "__main__":
    unittest.main()
