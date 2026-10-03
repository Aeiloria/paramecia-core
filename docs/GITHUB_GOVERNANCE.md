# GitHub Governance

GitHub is the reviewable control surface for Paramecia Core.

## What each surface does

- **Issues** capture bounded intake, contradictions, corrections, and work.
- **Branches** isolate one proposed change from the authoritative line.
- **Pull requests** expose sources, status, collisions, and review decisions.
- **Checks** catch mechanical failures; they do not decide canon.
- **Tags/releases** mark named, recoverable checkpoints after explicit review.
- **`main`** is the accepted repository history, not automatic proof that every
  statement within it is canon locked.

## Intake path

`SOURCE -> INTAKE ISSUE -> BRANCH -> PULL REQUEST -> REVIEW -> MERGE OR HOLD`

Canon-facing work adds a separate decision:

`... -> CANON CANDIDATE -> EXPLICIT FIELD-LEVEL APPROVAL -> CANON`

## Labels to create in GitHub

The repository owner can create these labels when convenient:

- `intake`
- `provenance`
- `collision`
- `canon-candidate`
- `canon-review`
- `quarantined`
- `retired`
- `blocked-source`

Labels help routing but never change authority by themselves.

## First project board

Use a repository Project with these columns:

1. Intake
2. Source verification
3. Drafting
4. Canon review
5. Accepted
6. Held / quarantined

Move cards for visibility only. A card position is not a canon decision.

## Release checkpoints

Create a release only for a reviewed, named checkpoint. Release notes should
include the commit, scope, source ledger changes, canon decisions, unresolved
collisions, and rollback notes.
