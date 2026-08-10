const detected = JSON.parse(process.env.DETECTED ?? '{}');
const needs = JSON.parse(process.env.NEEDS ?? '{}');

const failures = [];
if (needs.detect?.result !== 'success') {
  failures.push(`detect=${needs.detect?.result ?? 'missing'}`);
}

for (const [job, applicable] of Object.entries(detected)) {
  if (applicable !== true) continue;
  const result = needs[job]?.result ?? 'missing';
  if (result !== 'success') failures.push(`${job}=${result}`);
}

for (const [job, state] of Object.entries(needs)) {
  if (job === 'detect') continue;
  const result = state?.result ?? 'missing';
  if (result === 'failure' || result === 'cancelled') failures.push(`${job}=${result}`);
}

if (failures.length > 0) {
  console.error(`Quality gate failed: ${[...new Set(failures)].join(', ')}`);
  process.exit(1);
}

console.log('Quality gate passed: all applicable jobs succeeded.');
