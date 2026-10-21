# Whisperwood Location Canon Pipeline v0.1

This first slice structures the six locations named in the Notion architecture review. The records are **candidates** and contain only the names supported by that source. Symbols, tags, purposes, and relationship hooks remain marked for source recovery; they are not inferred from the separate RPG map.

## Source and generated views

- `canon/whisperwood/locations/*.json` is the only editing source for this pipeline.
- `schemas/` defines record shape and the approval requirement for `approved` lifecycle state.
- `validators/validate_locations.py` reads source records and reports schema, duplicate-ID, and broken-reference errors. It never edits source files.
- `renderers/render_location_markdown.py` writes Markdown views only under `build/whisperwood/locations/` by default. Do not edit generated files.
- `tests/` checks the six-name seed set, provenance, duplicate and broken-reference failures, approval gating, and deterministic rendering.

## Run locally

```sh
python -m pip install -r requirements-dev.txt
python validators/validate_locations.py
python -m unittest discover -s tests -v
python renderers/render_location_markdown.py
```

The records use `artifact_role: source`, selecting one controlled value from the architecture review's artifact-role vocabulary. The review's example `foundational_source` is treated as descriptive prose, not as a second enum value.

No automatic canon promotion or rewrite exists. Promotion requires an explicit `promotion_approval` object and a reviewed source change; the renderer and validator cannot apply one.
