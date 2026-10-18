import { test } from 'node:test';
import assert from 'node:assert/strict';
import { primes, primeWave, waveSurvivors, zArrow, zeta, gamma, psi, psiExplicit, sigma, robinRatio, ROBIN_BOUND, ZETA_ZEROS, nthPrimeEstimate } from '../index.js';

const close = (a, b, tol) => assert.ok(Math.abs(a - b) <= tol, `${a} is not within ${tol} of ${b}`);

test('primes', () => {
  assert.equal(primes(100).length, 25);
  assert.equal(primes(100000).length, 9592);
});

test('the prime wave is exact up to P squared', () => {
  assert.equal(primeWave(97, 7), 0);
  assert.ok(primeWave(98, 7) > 0);
  const s = waveSurvivors(200, 7);
  assert.equal(s.falsePositives[0], 121);
  assert.ok(s.falsePositives.every(n => n > 49));
});

test('Z(n) has modulus 1 on primes and prime powers only', () => {
  for (const n of [2, 7, 9, 16, 25]) close(Math.hypot(...zArrow(n)), 1, 1e-12);
  assert.ok(Math.abs(Math.hypot(...zArrow(6)) - 1) > 1e-6);
});

test('Gamma and zeta match known values', () => {
  close(gamma(5)[0], 24, 1e-9);
  close(zeta(2)[0], Math.PI ** 2 / 6, 1e-12);
  close(zeta(-1)[0], -1 / 12, 1e-10);
  const [r, i] = zeta(0.5, ZETA_ZEROS[0]);
  close(Math.hypot(r, i), 0, 1e-5);
  const [r2, i2] = zeta(0.5, 30); // mpmath: -0.12064229 - 0.58369121i
  close(r2, -0.12064229, 1e-7); close(i2, -0.58369121, 1e-7);
});

test('the explicit formula rebuilds psi', () => {
  close(psiExplicit(30.5, 1000), psi(30.5), 0.6);
});

test('Robin and Cipolla', () => {
  assert.equal(sigma(12), 28);
  assert.ok(robinRatio(5040) > ROBIN_BOUND);
  assert.ok(robinRatio(10080) < ROBIN_BOUND);
  close(nthPrimeEstimate(100000) / 1299709, 1, 0.001);
});
