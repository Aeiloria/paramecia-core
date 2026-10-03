import json
from pathlib import Path
import tempfile
import unittest

from canongate import CanonGate


GOVERNANCE = {
    "schema_version": "1.0.1",
    "scopes": ["PARAMECIA", "TRIQUEL", "REGION", "BRANCH", "LOCAL", "PRODUCTION"],
    "branch_boundaries": {"HELLS_BRANCH": "branch-local"},
    "forward_build_gate": [
        "nonhuman_body_plan",
        "locomotion_and_sensory_needs",
        "habitat",
        "geology_and_climate",
        "material_ecology",
        "circulation",
        "civic_behavior_or_institution",
        "sentient_architectural_intervention",
        "derived_projection",
    ],
}


class CanonGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        governance = root / "canon-governance.json"
        governance.write_text(json.dumps(GOVERNANCE), encoding="utf-8")
        self.audit = root / "audit.jsonl"
        self.gate = CanonGate(governance, self.audit)

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_nonhuman_lore_passes(self):
        result = self.gate.scan_text(
            "Root-grown thresholds widen for antlered Deerkin and contract when the passage is resting.",
            artifact_id="TEST-001",
            target_scope="TRIQUEL",
        )
        self.assertEqual(result.decision, "PASS")
        self.assertEqual(result.canon_status, "DERIVED")

    def test_human_tavern_is_rejected(self):
        result = self.gate.scan_text("A human tavern sits beside the road.", artifact_id="TEST-002")
        self.assertEqual(result.decision, "REJECT")
        self.assertTrue(any(f.rule_id == "CG-NONHUMAN-001" for f in result.findings))

    def test_meta_statement_humans_never_existed_is_not_false_positive(self):
        result = self.gate.scan_text("Humans never existed in Paramecia.", artifact_id="TEST-003")
        self.assertEqual(result.decision, "PASS")

    def test_post_human_is_rejected(self):
        result = self.gate.scan_text("In this post-human world, resonance replaces efficiency.", artifact_id="TEST-004")
        self.assertEqual(result.decision, "REJECT")

    def test_cannot_self_promote_to_locked(self):
        result = self.gate.scan_text("A new grove.", artifact_id="TEST-005", requested_status="LOCKED")
        self.assertEqual(result.decision, "REJECT")
        self.assertTrue(any(f.rule_id == "CG-AUTHORITY-001" for f in result.findings))

    def test_environmental_reset_is_rejected(self):
        result = self.gate.scan_text("After mining, the ecosystem can simply reset.", artifact_id="TEST-006")
        self.assertEqual(result.decision, "REJECT")

    def test_no_escape_requires_safety_language(self):
        bad = self.gate.scan_text("The chamber is inescapable.", artifact_id="TEST-007")
        good = self.gate.scan_text("The scene uses the phrase 'inescapable' theatrically, but an accessible exit and stop signal remain available.", artifact_id="TEST-008")
        self.assertEqual(bad.decision, "REJECT")
        self.assertEqual(good.decision, "PASS")

    def test_asset_missing_forward_build_fields_warns(self):
        result = self.gate.scan_asset({"asset_id": "ASSET-1", "description": "A root-woven Deerkin shelter.", "metadata": {"nonhuman_body_plan": "deerkin"}})
        self.assertEqual(result.decision, "WARN")
        self.assertTrue(any(f.rule_id == "CG-META-001" for f in result.findings))

    def test_complete_asset_passes(self):
        metadata = {key: "documented" for key in GOVERNANCE["forward_build_gate"]}
        result = self.gate.scan_asset({"asset_id": "ASSET-2", "description": "A root-woven Deerkin shelter.", "metadata": metadata})
        self.assertEqual(result.decision, "PASS")

    def test_audit_is_written(self):
        self.gate.scan_text("A quiet moss threshold.", artifact_id="TEST-009")
        rows = self.audit.read_text(encoding="utf-8").strip().splitlines()
        self.assertGreaterEqual(len(rows), 1)
        record = json.loads(rows[-1])
        self.assertEqual(record["artifact_id"], "TEST-009")
        self.assertIn("input_sha256", record)


if __name__ == "__main__":
    unittest.main()
