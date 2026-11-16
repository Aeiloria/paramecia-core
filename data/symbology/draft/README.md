# Aeiloria emoji symbology registry (draft only)

**Status:** DRAFT / NOT CANON. **Canon promotion:** false for all entries. **Purpose:** preserve and review a 72-record source-ledger snapshot without touching authoritative canon.

## Files

- `emoji-registry.json`: source columns, original tags, stable source IDs, receipts, original verification labels, and explicit draft status.
- `source-manifest.json`: exact source location and provenance limitations.
- `validate_registry.py`: stdlib-only checks; manually run with `python data/symbology/draft/validate_registry.py`.

## Source and lineage

- Google Sheet: https://docs.google.com/spreadsheets/d/1o8B4HTX_4f3cL6M7N0dli0oCP9mraMC7nTSeRGURlbg/edit
- Tab and range: `Emoji Ledger!A1:H73`; 72 records, IDs `AEI-SYM-0001` through `AEI-SYM-0072`.
- Source receipts embedded in each row are preserved **verbatim**. Some are filenames or conversation claims, not resolvable archival anchors. The registry does not certify them.
- Other named materials in the ledger include `01_Master_Symbology_Color_Tagging_Library.md`, `05_Safety_And_Consent_Signals.md`, and creator/project-context entries. These are not reinterpreted here.
- GitHub governance: `canon/registries/canon-index.md`, `canon/registries/corrections.json`. These existing files are not modified.

## Semantics and conflicts

- `source_verification` and `source_canon_handling` are **copied source claims**, not approval produced by this PR.
- `registry_status=draft_not_canon` and `canon_promoted=false` are authoritative for **this export only**.
- Older source descriptions mentioning black or circular geometry are retained as documentary evidence only and must not be treated as approved visual instructions.
- Keep Hell's Branch traffic-circle reservation and Red=STOP. Do not infer that Purple curiosity or a visible symbol constitutes consent.
- Do not generate or mutate lore, routes, characters, rights, or world state from these records.

## Promotion boundary

Do **not** merge this PR as a canon approval. Explicit review, source recovery and conflict adjudication are separate work. Merging a data-only draft is also not requested in this task.
