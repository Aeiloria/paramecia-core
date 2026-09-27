from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .engine import CanonGate, GateResult


@dataclass(frozen=True)
class IngestReceipt:
    asset_id: str
    decision: str
    admitted_to_staging: bool
    canon_promoted: bool
    source_path: str | None
    source_sha256: str | None
    gate_input_sha256: str
    governance_version: str | None
    receipt_time: str
    findings: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def ingest_asset_manifest(
    manifest: dict[str, Any],
    *,
    gate: CanonGate,
    receipt_log: str | Path | None = None,
) -> IngestReceipt:
    """Gate one asset manifest before it may enter the staging asset pipeline.

    This function deliberately has no canon-promotion path. PASS/WARN means the
    record may enter staging for human review; REJECT means it may not. Canon
    promotion remains a separate creator-authority action outside this module.
    """
    result: GateResult = gate.scan_asset(manifest)
    asset_id = str(manifest.get("asset_id") or manifest.get("name") or "UNSPECIFIED-ASSET")
    provenance = manifest.get("provenance") or {}

    receipt = IngestReceipt(
        asset_id=asset_id,
        decision=result.decision,
        admitted_to_staging=result.accepted,
        canon_promoted=False,
        source_path=provenance.get("source_path") if isinstance(provenance, dict) else None,
        source_sha256=provenance.get("source_sha256") if isinstance(provenance, dict) else None,
        gate_input_sha256=result.input_sha256,
        governance_version=result.governance_version,
        receipt_time=datetime.now(timezone.utc).isoformat(),
        findings=[asdict(finding) for finding in result.findings],
    )

    if receipt_log:
        path = Path(receipt_log)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(receipt.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")

    return receipt
