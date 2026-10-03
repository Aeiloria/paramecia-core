# Hells Branch Runtime Architecture

## Purpose

This package is the machine-readable implementation layer for the Hells Branch quarantined side engine. It keeps narrative canon, runtime state, consent handling, civic ecology, and validator rules in one portable module so it can later move into a dedicated repository without rewriting the data model.

## Layer model

1. **Canon layer**
   - House laws
   - stewardship doctrine
   - civic ecology
   - named stewards and Housefolk
   - immutable branch invariants

2. **Runtime layer**
   - current location
   - capacity state
   - consent state
   - House attention
   - active NPCs and mysteries
   - visible exits and aftercare availability

3. **Routing layer**
   - need -> NPC activation
   - state -> House behavior
   - scene pressure -> consent response

4. **Relationship layer**
   - trust
   - recognition
   - comfort
   - playfulness
   - repair debt
   - House memory

5. **Validation layer**
   - structural checks
   - canon invariants
   - consent invariants
   - anti-coercion checks
   - anti-forced-healing checks
   - duck singularity enforcement

## Core scene loop

```text
NOTICE
  ↓
CHECK CAPACITY
  ↓
CHECK CONSENT
  ↓
OFFER
  ↓
WAIT
  ↓
RESPOND
  ↓
REPAIR / REVEAL / REST
  ↓
AFTERCARE
  ↓
MEMORY UPDATE
```

The loop is deliberately asymmetric: the system may notice and offer, but agency remains with the participant.

## Red behavior

`red` is not a dramatic scene state. It is an interrupt.

When Red activates:

- stop escalation immediately
- preserve or expose exits
- reduce sensory and social demand
- suspend symbolic pressure
- prioritize safety and explicit choices
- do not treat stopping as failure

## Purple behavior

Purple marks ambiguity, comfort, aftercare, or a state that must not be interpreted without clarification. Runtime systems should ask instead of guessing.

## House behavior

The House communicates environmentally through architecture and domestic infrastructure. Its valid output space includes doors, windows, lights, chairs, blankets, temperature, hallways, kettles, and repaired objects.

The House is prohibited from:

- locking participants in
- removing exits
- overriding consent
- hiding safety tools
- forcing confrontation
- manipulating comfort into compliance

## Civic ecology

Hells Branch institutions are not departments in a bureaucracy. They are mutually supporting ecological layers:

- Tea Gardens: roots
- Companion Bakery: nourishment
- Hearthroot Inn: pollination
- Community Hall: canopy
- Knotwork Nexus: repair/mycelium
- Housefolk Guild: continuity
- Midnight Archive: memory
- Living Question Observatory: seed/wonder
- Returning Stream: flow
- Quiet Room Network: rest

The intended design principle is redundancy without hierarchy. Multiple systems may support the same need so no single steward becomes indispensable.

## Extraction path

This directory is intentionally self-contained. To split it into a dedicated repository later, move the directory root unchanged and preserve:

- `package.json`
- `src/`
- `schema/`
- `scripts/`
- `.github/`
- `docs/`

No parent-repository imports are required for validation.
