# Paramecia Canongate

A deterministic admission gate for Paramecia lore and production assets.

**Status:** implementation, not canon authority.

Canongate reads the existing `canon/registries/canon-governance.json` registry and returns `PASS`, `WARN`, or `REJECT`. A pass never promotes material to canon. The creator-explicit-declaration rule remains authoritative.

## What v0.1 actually enforces

- blocks explicit human-presence / human-default architecture patterns
- blocks `post-human` framing because humans never existed in Paramecia
- blocks trivial ecological reversibility claims
- blocks confinement / absolute-control phrasing when no exit or consent/safety mechanism is present
- blocks any attempt to self-promote material directly to `LOCKED`
- warns on unknown scope and Hell's Branch scope leakage
- checks asset records for the existing `forward_build_gate` metadata keys
- writes JSONL audit records with SHA-256 fingerprints

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Use as Python

```python
from canongate import CanonGate

gate = CanonGate(audit_log="build/canongate-audit.jsonl")
result = gate.scan_text(
    "A human tavern sits beside the road.",
    artifact_id="example-001",
    target_scope="TRIQUEL",
)
print(result.to_dict())
```

## MCP adapter

The core validator uses only Python's standard library. The MCP adapter is optional and lives in `canongate/server.py`.

```bash
pip install mcp
python -m canongate.server
```

It exposes:

- `scan_lore`
- `scan_asset`
- `paramecia://canongate/status`

The MCP layer cannot promote canon.

## What v0.1 does not claim

- no image/mesh geometry inspection yet
- no automatic Inkarnate ingestion yet
- no semantic LLM judgment inside the hard gate
- no automatic canon mutation
- no claim that every Paramecia rule is encoded

Those are later layers. This version exists to provide a small, inspectable, testable enforcement kernel first.
