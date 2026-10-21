# Paramecia Core

Central repository for the Paramecia, Triquel, and Hells Branch lore databases, system logic, recovery architecture, and AI agent instructions.

## Core Navigation

- [Canon Index](canon/registries/canon-index.md) — authoritative civilizational stack, Five Founding Paths / Nine Civilizational Paths resolution, Hells Branch laws, naming priorities, and integration rules
- [Alias and Naming Crosswalk](canon/registries/aliases.json) — machine-readable identity relationships, deprecated names, duplicate hazards, and required separations
- [Canon Corrections](canon/registries/corrections.json) — first-class correction events that downstream prose, visuals, modules, and exports must apply
- [Project Core Integration Map](docs/project-core-integration-map.md) — operational map for cosmology, canon governance, care ecology, characters, regions, scenarios, recovery systems, visual canon, and production order
- [Core Chats Integration — Living Canon Expansion](docs/core-chats-integration-living-canon-expansion.md) — capture-to-canon bridge connecting live creation, Notion synthesis, GitHub governance, runtime testing, and production routing
- [Core Chats Utilization Pass v2.0](docs/core-chats-utilization-pass-v2.md) — converts named canon into registries, relationship runtime, living-place systems, visual provenance, and production routes
- [Whisperwood Location Canon Pipeline v0.1](canon/whisperwood/locations/) — candidate records, schema, validators, tests, and generated Markdown boundary
- [`canon/`](canon/) — authoritative and reviewable world material
- [`docs/recovery/`](docs/recovery/) — recovery architecture and operational references
- [`skills/project-0-core-pack-v1/`](skills/project-0-core-pack-v1/) — executable behavioral skills and workflows

## Canon Architecture

The mature civilizational stack is:

1. **Layer 0 — Care Ecology**
2. **Cosmology — Paramecia, Triquel, First Thoughts, Point 0**
3. **Three Accords — Recognition → Midnight → Harmony**
4. **Five Founding Paths / Nine Civilizational Paths**
5. **Civic and ecological systems**
6. **Living places and architecture**
7. **Characters and relationships**
8. **Scenario runtime**
9. **Production and recovery architecture**

The Five Paths describe the founding Whisperwood collaboration engine. The Nine Paths describe the mature civilizational ecology. They are related layers, not competing canons.

## Codex Hub Workflow

When starting a new session or creating a pull request, always follow the core Hub tasks:

1. Name the next concrete deliverable
2. Mark what is canon versus volatile
3. Choose the pass: canon, system, scene, or artifact
4. Ask Codex for the smallest useful next build

Before creating another master document:

1. search the existing ledger
2. extend an existing node where possible
3. identify the affected layer
4. mark canon status
5. preserve source anchors and correction history

## Capture-to-Canon Loop

Substantial material should move through:

**capture → stabilize → route → test → remember**

No derived artifact silently promotes itself into canon. Exact corrections, status, provenance, relationships, runtime consequences, and the next production destination must remain visible.

## Recovery Architecture

The integrated recovery system lives in:

- [`docs/recovery/recovery-atlas.md`](docs/recovery/recovery-atlas.md) — state map, consent colors, Morning Recovery Bundle, repair protocol, world integration, and implementation map
- [`docs/recovery/recovery-operational-modules.md`](docs/recovery/recovery-operational-modules.md) — transition logic, care by energy level, sensory matrix, interruption and restart, evening closure, Drop Point template, and world-state consequences
- [`docs/recovery/recovery-field-card.md`](docs/recovery/recovery-field-card.md) — compact operational reference and Drop Point record
- [`skills/project-0-core-pack-v1/`](skills/project-0-core-pack-v1/) — executable behavioral skills for Embercurrent, Recovery Amber, Re-entry Corridor, Morning Re-entry, Harbor, Boundary Keeper, and related workflows

> Recovery is not a detour from the work. Recovery is part of the world engine.

## Current Highest-Leverage Build

Expand the canon ledger into machine-readable node and relationship registries, using the alias and correction registries as identity guardrails before producing additional decks, lorebooks, character exports, or visual collections.

Current registry set:

- [`canon/registries/canon-index.md`](canon/registries/canon-index.md)
- [`canon/registries/aliases.json`](canon/registries/aliases.json)
- [`canon/registries/corrections.json`](canon/registries/corrections.json)

Next suggested companions:

- `canon/registries/nodes.json`
- `canon/registries/relationships.json`

## Whisperwood Location Canon Pipeline v0.1

The six location records are candidates containing only source-backed names and provenance. Symbols, tags, purposes, and relationship hooks remain pending source recovery. The separate RPG map is not imported as canon.

- `canon/whisperwood/locations/*.json` is the only editing source for this pipeline.
- `schemas/` defines metadata and location record shape, including the approval requirement for `approved` lifecycle state.
- `validators/validate_locations.py` reports schema, duplicate-ID, and broken-reference errors without editing source files.
- `renderers/render_location_markdown.py` writes rendered views under `build/whisperwood/locations/`, which is ignored and rebuildable.
- `tests/` and `.github/workflows/whisperwood-v0.1.yml` verify the six-name seed set, provenance, hard failures, approval gating, and deterministic rendering.

Run with Python 3.12:

```sh
python -m pip install -r requirements-dev.txt
python validators/validate_locations.py
python -m unittest discover -s tests -v
python renderers/render_location_markdown.py
```

