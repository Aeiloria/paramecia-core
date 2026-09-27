import json
from pathlib import Path
import tempfile
import unittest

from canongate import CanonGate
from canongate.asset_ingest import ingest_asset_manifest


GOVERNANCE = {
    "schema_version": "1.0.1",
    "scopes": ["PARAMECIA", "TRIQUEL", "REGION", "BRANCH", "LOCAL", "PRODUCTION"],
    "branch_boundaries": {"HELLS_BRANCH": "branch-local"},
    "forward_build_gate": ["nonhuman_body_plan"],
}


class AssetIngestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        governance = root / "canon-governance.json"
        governance.write_text(json.dumps(GOVERNANCE), encoding="utf-8")
        self.receipts = root / "receipts.jsonl"
        self.gate = CanonGate(governance)

    def tearDown(self):
        self.tmp.cleanup()

    def test_pass_enters_staging_but_never_promotes_canon(self):
        receipt = ingest_asset_manifest({
            "asset_id": "A-1",
            "description": "A root-woven Deerkin shelter.",
            "scope": "TRIQUEL",
            "metadata": {"nonhuman_body_plan": "deerkin"},
            "provenance": {"source_path": "a.png", "source_sha256": "abc123"},
        }, gate=self.gate, receipt_log=self.receipts)
        self.assertTrue(receipt.admitted_to_staging)
        self.assertFalse(receipt.canon_promoted)
        self.assertEqual(receipt.source_sha256, "abc123")

    def test_rejected_asset_does_not_enter_staging(self):
        receipt = ingest_asset_manifest({
            "asset_id": "A-2",
            "description": "A human tavern sits beside the road.",
            "metadata": {"nonhuman_body_plan": "human"},
        }, gate=self.gate, receipt_log=self.receipts)
        self.assertEqual(receipt.decision, "REJECT")
        self.assertFalse(receipt.admitted_to_staging)
        self.assertFalse(receipt.canon_promoted)

    def test_locked_request_cannot_cross_ingestion_boundary(self):
        receipt = ingest_asset_manifest({
            "asset_id": "A-3",
            "description": "A root-woven Deerkin shelter.",
            "requested_status": "LOCKED",
            "metadata": {"nonhuman_body_plan": "deerkin"},
        }, gate=self.gate)
        self.assertEqual(receipt.decision, "REJECT")
        self.assertFalse(receipt.canon_promoted)


if __name__ == "__main__":
    unittest.main()
