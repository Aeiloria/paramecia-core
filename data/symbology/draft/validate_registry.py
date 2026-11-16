#!/usr/bin/env python3
"""Validate data-only emoji ledger snapshot; does not authorize promotion."""
import json
import re
from pathlib import Path

p = Path(__file__).with_name("emoji-registry.json")
d = json.loads(p.read_text(encoding="utf-8"))
rows = d["records"]
assert d["governance"]["canon_promoted"] is False
assert d["record_count"] == len(rows) == 72
ids = [r["symbol_id"] for r in rows]
assert len(set(ids)) == len(ids)
assert ids == [f"AEI-SYM-{i:04d}" for i in range(1, 73)]
for r in rows:
    assert re.fullmatch(r"AEI-SYM-[0-9]{4}", r["symbol_id"])
    assert r["glyph"] and r["source_meaning"] and r["source_receipt"]
    assert r["registry_status"] == "draft_not_canon"
    assert r["canon_promoted"] is False
assert next(r for r in rows if r["symbol_id"] == "AEI-SYM-0045")["glyph"] == "🔴"
print("PASS: 72 source records, stable IDs, source receipts, and no canon promotion")
