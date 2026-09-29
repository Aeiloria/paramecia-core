from __future__ import annotations

import os
from pathlib import Path

from .asset_ingest import ingest_asset_manifest
from .engine import CanonGate


def build_gate() -> CanonGate:
    governance = Path(os.environ.get("PARAMECIA_GOVERNANCE", "canon/registries/canon-governance.json"))
    audit = Path(os.environ.get("PARAMECIA_CANONGATE_AUDIT", "build/canongate-audit.jsonl"))
    return CanonGate(governance_path=governance, audit_log=audit)


def main() -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise SystemExit("MCP package not installed. Install `mcp`, then run `python -m canongate.server`.") from exc

    gate = build_gate()
    receipt_log = Path(os.environ.get("PARAMECIA_CANONGATE_RECEIPTS", "build/canongate-ingest-receipts.jsonl"))
    mcp = FastMCP("Paramecia Canongate")

    @mcp.tool()
    def scan_lore(text: str, artifact_id: str = "UNSPECIFIED", target_scope: str = "TRIQUEL", requested_status: str = "DERIVED") -> dict:
        """Validate proposed lore without promoting it to canon."""
        return gate.scan_text(text, artifact_id=artifact_id, artifact_kind="lore", target_scope=target_scope, requested_status=requested_status).to_dict()

    @mcp.tool()
    def scan_asset(asset: dict) -> dict:
        """Validate one asset record and its canon-facing metadata without staging it."""
        return gate.scan_asset(asset).to_dict()

    @mcp.tool()
    def ingest_asset(asset: dict) -> dict:
        """Gate one asset manifest and issue an auditable staging receipt.

        PASS/WARN may enter staging; REJECT may not. This tool never promotes
        canon and every receipt records canon_promoted=false.
        """
        return ingest_asset_manifest(asset, gate=gate, receipt_log=receipt_log).to_dict()

    @mcp.resource("paramecia://canongate/status")
    def status() -> dict:
        """Return the active governance version and non-promotion guarantee."""
        return {
            "name": "Paramecia Canongate",
            "governance_version": gate.governance.get("schema_version"),
            "authority_root": gate.governance.get("authority", {}).get("root"),
            "can_promote_canon": False,
            "audit_log": str(gate.audit_log) if gate.audit_log else None,
            "receipt_log": str(receipt_log),
            "tools": ["scan_lore", "scan_asset", "ingest_asset"],
        }

    mcp.run()


if __name__ == "__main__":
    main()
