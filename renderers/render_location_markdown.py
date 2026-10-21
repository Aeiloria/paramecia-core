#!/usr/bin/env python3
"""Render candidate location records to Markdown under build/ only."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validators"))
from validate_locations import DEFAULT_RECORDS, LOCATION_SCHEMA_PATH, METADATA_SCHEMA_PATH, load_records, read_json, validate_records  # noqa: E402


def render_record(record: dict) -> str:
    provenance = record["provenance"][0]
    pending = ", ".join(record["pending_fields"]) or "none"
    refs = ", ".join(record["references"]) or "none"
    return (
        f"# {record['name']}\n\n"
        f"- Record ID: `{record['record_id']}`\n"
        f"- Lifecycle: `{record['lifecycle_state']}`\n"
        f"- Review: `{record['review_state']}`\n"
        f"- Source completeness: `{record['source_completeness']}`\n"
        f"- References: {refs}\n"
        f"- Fields awaiting source recovery: {pending}\n\n"
        f"Source: [{provenance['source_title']}]({provenance['source_url']}) — "
        f"{provenance['source_section']} (`{provenance['source_excerpt']}`)\n"
    )


def render(records: list[dict]) -> dict[str, str]:
    return {f"{record['record_id']}.md": render_record(record) for record in sorted(records, key=lambda item: item["record_id"])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build/whisperwood/locations")
    args = parser.parse_args()
    try:
        records = load_records(args.records)
        errors = validate_records(records, read_json(METADATA_SCHEMA_PATH), read_json(LOCATION_SCHEMA_PATH))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in render(records).items():
        (args.output_dir / filename).write_text(content, encoding="utf-8", newline="\n")
    print(f"Rendered {len(records)} Markdown view(s) into {args.output_dir}; source records were not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
