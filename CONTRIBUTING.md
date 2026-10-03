# Contributing to Paramecia Core

This repository is a governed continuity ledger, not a dumping ground. Preserve
sources, uncertainty, sibling versions, and correction history.

## Before changing material

1. Search the canon index, alias registry, corrections registry, and open issues.
2. Name one concrete deliverable.
3. Identify the source and affected canon layer.
4. Separate evidence from interpretation.
5. Choose the smallest useful change.

## Lifecycle and canon status

Workflow state and canon authority are separate:

- Workflow: `RAW -> INGESTED -> NOTE -> DRAFT -> CANON_CANDIDATE -> CANON`
- Content authority: use the vocabulary in
  [`canon/registries/canon-index.md`](canon/registries/canon-index.md).
- `RETIRED` and `QUARANTINED` are flags, not replacements for either scale.

No issue, branch, commit, generated artifact, or pull request promotes material
to canon by itself. Canon promotion requires an explicit, field-level approval.

## Branch and pull-request practice

- Create a focused branch from `main`.
- Link the issue or source anchor in the pull request.
- State whether the change is canon-facing.
- Record contradictions instead of silently choosing a winner.
- Do not delete or overwrite provenance to make a consolidation look clean.
- Keep human-shaped imports out of Paramecia; humans never existed in this
  setting. Recreate imports through a grounded nonhuman ontology.

## Review gate

A pull request is ready only when its scope, sources, status, collisions,
affected files, and rollback path are visible. Merging records an accepted
repository change; it does not imply canon promotion unless the approval says
so explicitly.
