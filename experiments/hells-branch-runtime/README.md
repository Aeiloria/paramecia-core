# Hells Branch Runtime

A repo-ready JSON runtime package for the **Hells Branch** quarantined side engine in Paramecia/Triquel.

> **No lantern walks alone.**

This package turns Hells Branch canon into machine-readable world state, consent/capacity logic, location routing, NPC activation, House behavior, memory records, scenario triggers, and canon validation.

## What is here

- `src/hells-branch.runtime.json` — canonical runtime payload
- `schema/hells-branch.schema.json` — JSON Schema for structural validation
- `scripts/validate.mjs` — zero-dependency validator for core invariants
- `docs/ARCHITECTURE.md` — runtime architecture and extension notes
- `.github/workflows/hells-branch-validate.yml` — CI validation

## Canon invariants

1. Hells Branch is a quarantined side engine.
2. The House is sentient architectural consciousness.
3. The House may suggest, never compel.
4. No room may become a prison.
5. Every locked door must have a key.
6. The occupant may always leave.
7. Care without consent becomes control.
8. A home exists to shelter becoming.
9. Roles are stewardship, not rank.
10. No lantern walks alone.
11. The Quiet Hands remain mysterious.
12. Ash Purrwell is not fully explained.
13. There is exactly one duck.

## Capacity model

- `green`: stable, available, continue normally
- `yellow`: strain rising, slow and clarify
- `orange`: overload near threshold, reduce demand
- `red`: stop immediately
- `purple`: ambiguity, comfort, or aftercare, ask before acting

## Development

Requires Node.js 20+.

```bash
npm run validate
```

The validator intentionally checks both JSON shape and story-level invariants. This is not merely data validation. Hells Branch gets a tiny ethics compiler because apparently architecture can now throw lint errors.

## Status

`7.1.2` implementation scaffold. Quarantined from main Triquel canon unless explicitly promoted.
