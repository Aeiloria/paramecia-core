import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = path.resolve(import.meta.dirname, '..');
const runtimePath = path.join(root, 'src', 'hells-branch.runtime.json');
const runtime = JSON.parse(fs.readFileSync(runtimePath, 'utf8'));

const errors = [];
const assert = (condition, message) => {
  if (!condition) errors.push(message);
};

assert(runtime?.meta?.status === 'QUARANTINED_SIDE_ENGINE', 'Hells Branch must remain quarantined.');
assert(runtime?.meta?.tagline === 'No lantern walks alone.', 'Canonical tagline changed.');
assert(runtime?.house?.type === 'sentient_architectural_consciousness', 'House type must remain sentient architectural consciousness.');

const laws = new Set(runtime?.house?.laws ?? []);
for (const law of [
  'No room may become a prison.',
  'Every locked door must have a key.',
  'The occupant may always leave.',
  'Care without consent becomes control.',
  'A home exists to shelter becoming.'
]) {
  assert(laws.has(law), `Missing House law: ${law}`);
}

for (const state of ['green', 'yellow', 'orange', 'red', 'purple']) {
  assert(runtime?.capacity?.[state], `Missing capacity state: ${state}`);
}

assert((runtime?.capacity?.red?.response ?? '').toLowerCase().includes('stop immediately'), 'Red must stop immediately.');
assert(runtime?.runtime?.scene_state?.open_exits_visible === true, 'Default scene must keep exits visible.');
assert(runtime?.runtime?.scene_state?.aftercare_available === true, 'Default scene must keep aftercare available.');
assert((runtime?.runtime?.consent_states ?? []).includes('red_stop'), 'Consent states must include red_stop.');

const mustPreserve = new Set(runtime?.validation?.must_preserve ?? []);
for (const invariant of [
  'house_may_suggest_never_compel',
  'no_room_becomes_prison',
  'care_without_consent_is_control',
  'roles_are_stewardship',
  'no_lantern_walks_alone',
  'exactly_one_duck'
]) {
  assert(mustPreserve.has(invariant), `Missing invariant: ${invariant}`);
}

const mustNever = new Set(runtime?.validation?.must_never ?? []);
assert(mustNever.has('second_duck'), 'Duck duplication protection missing. This is apparently critical infrastructure now.');
assert(mustNever.has('optimization_over_agency'), 'Agency protection missing.');
assert(mustNever.has('force_healing'), 'Forced-healing prohibition missing.');

if (errors.length) {
  console.error('\nHells Branch validation failed:\n');
  for (const error of errors) console.error(`  ✗ ${error}`);
  console.error(`\n${errors.length} invariant(s) failed.\n`);
  process.exit(1);
}

console.log('✓ Hells Branch JSON parsed');
console.log('✓ Five House laws preserved');
console.log('✓ Capacity states preserved');
console.log('✓ Consent and exit invariants preserved');
console.log('✓ Stewardship and agency invariants preserved');
console.log('✓ Duck count remains cosmologically acceptable');
console.log('\nCANON PASSED 🟢\n');
