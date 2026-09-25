// Checks js/trip-calc.js against the ready-made budgets in /blog/skolko-stoit-otdyh-v-gruzii/.
// Run: node scripts/trip-calc.test.js
const assert = require('assert');
const { calc } = require('../js/trip-calc.js');

const TOLERANCE = 0.15;
const near = (got, want, what) =>
  assert(Math.abs(got - want) / want <= TOLERANCE, `${what}: ${got} vs article ${want}`);

// Article: 3 days (3 nights), two people: eco 680–1020, comfort 1190–1730, lux 2520–4820 GEL
let r = calc({ days: 3, people: 2, level: 'eco' });
near(r.total[0], 680, 'eco 3d min'); near(r.total[1], 1020, 'eco 3d max');
r = calc({ days: 3, people: 2, level: 'comfort' });
near(r.total[0], 1190, 'comfort 3d min'); near(r.total[1], 1730, 'comfort 3d max');
r = calc({ days: 3, people: 2, level: 'lux' });
near(r.total[0], 2520, 'lux 3d min'); near(r.total[1], 4820, 'lux 3d max');

// Article: 7 days, two people, economy = 1720–2580 GEL (fun there includes excursions)
r = calc({ days: 7, people: 2, level: 'eco' });
near(r.total[0], 1720, 'eco 7d min'); near(r.total[1], 2580, 'eco 7d max');

// tours are per person; three people need two rooms; a tour day has no extra fun spend
r = calc({ days: 1, people: 3, level: 'eco', tours: [175, 170] });
assert.deepStrictEqual(r.parts.tours, [1035, 1035]);
assert.deepStrictEqual(r.parts.stay, [160, 300]);
assert.deepStrictEqual(r.parts.fun, [0, 0]);
r = calc({ days: 5, people: 2, level: 'eco', tours: [175] });
assert.deepStrictEqual(r.parts.fun, [13 * 2 * 4, 22 * 2 * 4]);

// junk input is clamped, not NaN
r = calc({ days: 'abc', people: -5, level: 'nope' });
assert.strictEqual(r.days, 1); assert.strictEqual(r.people, 1);
assert(Number.isFinite(r.total[0]));

console.log('trip-calc: ok');
