#!/usr/bin/env python3
"""Validate Whisperwood candidate location records without modifying them."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORDS = ROOT / "canon/whisperwood/locations"
METADATA_SCHEMA_PATH = ROOT / "schemas/canon-metadata.schema.json"
LOCATION_SCHEMA_PATH = ROOT / "schemas/location.schema.json"


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_records(records: list[dict[str, Any]], metadata_schema: dict[str, Any], location_schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(metadata_schema)
    Draft202012Validator.check_schema(location_schema)
    formats = FormatChecker()
    registry = Registry().with_resource(metadata_schema["$id"], Resource.from_contents(metadata_schema))
    validators = [
        Draft202012Validator(metadata_schema, registry=registry, format_checker=formats),
        Draft202012Validator(location_schema, registry=registry, format_checker=formats),
    ]
    errors: list[str] = []
    ids: dict[str, int] = {}
    for index, record in enumerate(records):
        for validator in validators:
            for error in validator.iter_errors(record):
                path = ".".join(str(part) for part in error.absolute_path) or "<record>"
                errors.append(f"record {index + 1} {path}: {error.message}")
        record_id = record.get("record_id")
        if isinstance(record_id, str):
            ids[record_id] = ids.get(record_id, 0) + 1
    for record_id, count in sorted(ids.items()):
        if count > 1:
            errors.append(f"duplicate record_id {record_id!r} appears {count} times")
    known_ids = set(ids)
    for index, record in enumerate(records):
        for reference in record.get("references", []):
            if reference not in known_ids:
                errors.append(f"record {index + 1} references unknown record_id {reference!r}")
    return sorted(errors)


def load_records(directory: Path) -> list[dict[str, Any]]:
    paths = sorted(directory.glob("*.json"))
    if not paths:
        raise ValueError(f"no location JSON files found in {directory}")
    return [read_json(path) for path in paths]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS, help="directory of source location JSON")
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
    print(f"Validated {len(records)} location record(s); no files changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
