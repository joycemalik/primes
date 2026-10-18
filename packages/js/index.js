// primewaves: the mathematics behind "Where the Waves Go Quiet" (https://primes.joycemalik.com).
// Plain ES module, no dependencies. Complex numbers are [re, im] pairs.
export { ZETA_ZEROS } from './zeros.js';
import { ZETA_ZEROS } from './zeros.js';

const EULER_GAMMA = 0.5772156649015329;

/** Boolean sieve of Eratosthenes: result[n] === 1 when n is prime, for 0 <= n <= limit. */
export function sieve(limit) {
  const isPrime = new Uint8Array(limit + 1).fill(1);
  isPrime[0] = 0; if (limit >= 1) isPrime[1] = 0;
  for (let i = 2; i * i <= limit; i++) if (isPrime[i]) for (let j = i * i; j <= limit; j += i) isPrime[j] = 0;
  return isPrime;
}

/** All primes up to and including limit. */
export function primes(limit) {
  const s = sieve(limit), out = [];
  for (let i = 2; i <= limit; i++) if (s[i]) out.push(i);
  return out;
}

/** Distinct prime factors of n (n >= 1), in increasing order. */
export function distinctPrimeFactors(n) {
  const f = []; let t = n;
  for (let p = 2; p * p <= t; p++) if (t % p === 0) { f.push(p); while (t % p === 0) t /= p; }
  if (t > 1) f.push(t);
  return f;
}

/**
 * The prime wave W(n): every context prime p <= P sends a spike of height 1/sqrt(p) to each proper multiple.
 * n is called prime when W(n) = 0. This is exact for n <= P^2 and nowhere beyond (it is the sieve of Eratosthenes).
 */
export function primeWave(n, P) {
  let w = 0;
  for (const p of primes(P)) if (n % p === 0 && n !== p) w += 1 / Math.sqrt(p);
  return w;
}

/** Nodes of the prime wave in [2, N] with waves from primes <= P, split into true primes and composites that slip through. */
export function waveSurvivors(N, P) {
  const ctx = primes(P), isPrime = sieve(N), out = { primes: [], falsePositives: [] };
  for (let n = 2; n <= N; n++) {
    if (ctx.some(p => n % p === 0 && n !== p)) continue;
    (isPrime[n] ? out.primes : out.falsePositives).push(n);
  }
  return out;
}

/** Z(n) = sum over distinct primes p | n of e^{i p ln n}. |Z(n)| = 1 exactly when n is a prime power. */
export function zArrow(n) {
  let re = 0, im = 0; const L = Math.log(n);
  for (const p of distinctPrimeFactors(n)) { re += Math.cos(p * L); im += Math.sin(p * L); }
  return [re, im];
}

/* ---------- complex Gamma (Lanczos) and zeta (Borwein + functional equation) ---------- */
const LANCZOS = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];

/** Complex Gamma function Γ(re + i·im). */
export function gamma(re, im = 0) {
  if (re < 0.5) {
    const [gr, gi] = gamma(1 - re, -im);
    const x = Math.PI * re, y = Math.PI * im;
    const sr = Math.sin(x) * Math.cosh(y), si = Math.cos(x) * Math.sinh(y);
    const dr = sr * gr - si * gi, di = sr * gi + si * gr, dd = dr * dr + di * di;
    return [Math.PI * dr / dd, -Math.PI * di / dd];
  }
  re -= 1;
  let xr = LANCZOS[0], xi = 0;
  for (let i = 1; i < 9; i++) { const dr = re + i, dd = dr * dr + im * im; xr += LANCZOS[i] * dr / dd; xi -= LANCZOS[i] * im / dd; }
  const tr = re + 7.5, ti = im;
  const lt = 0.5 * Math.log(tr * tr + ti * ti), at = Math.atan2(ti, tr);
  const pr = (re + 0.5) * lt - im * at - tr, pa = (re + 0.5) * at + im * lt - ti;
  const m = Math.sqrt(2 * Math.PI) * Math.exp(pr), cr = m * Math.cos(pa), ci = m * Math.sin(pa);
  return [cr * xr - ci * xi, cr * xi + ci * xr];
}

const ZN = 64;
const ZD = (() => { const d = new Float64Array(ZN + 1); let s = 0, term = 1 / ZN; for (let i = 0; i <= ZN; i++) { if (i > 0) term *= 4 * (ZN + i - 1) * (ZN - i + 1) / ((2 * i - 1) * (2 * i)); s += term; d[i] = ZN * s; } return d; })();
const LNK = Array.from({ length: ZN }, (_, k) => Math.log(k + 1));

/** Riemann zeta function ζ(re + i·im). Accurate to about 8 significant digits for |im| <= 100. */
export function zeta(re, im = 0) {
  if (re < 0.5) { // ζ(s) = 2^s π^(s−1) sin(πs/2) Γ(1−s) ζ(1−s)
    const [zr, zi] = zeta(1 - re, -im), [gr, gi] = gamma(1 - re, -im);
    const er = re * Math.LN2 + (re - 1) * Math.log(Math.PI), ei = im * (Math.LN2 + Math.log(Math.PI));
    const ea = Math.exp(er), pr = ea * Math.cos(ei), pi = ea * Math.sin(ei);
    const x = Math.PI * re / 2, y = Math.PI * im / 2, sr = Math.sin(x) * Math.cosh(y), si = Math.cos(x) * Math.sinh(y);
    const ar = pr * sr - pi * si, ai = pr * si + pi * sr, br = ar * gr - ai * gi, bi = ar * gi + ai * gr;
    return [br * zr - bi * zi, br * zi + bi * zr];
  }
  let sr = 0, si = 0;
  for (let k = 0; k < ZN; k++) {
    const c = ((k & 1) ? -1 : 1) * (ZD[k] - ZD[ZN]), m = Math.exp(-re * LNK[k]), a = -im * LNK[k];
    sr += c * m * Math.cos(a); si += c * m * Math.sin(a);
  }
  sr /= -ZD[ZN]; si /= -ZD[ZN];
  const m = Math.exp((1 - re) * Math.LN2), a = -im * Math.LN2, dr = 1 - m * Math.cos(a), di = -m * Math.sin(a), dd = dr * dr + di * di;
  return [(sr * dr + si * di) / dd, (si * dr - sr * di) / dd];
}

/* ---------- prime counting and Riemann's explicit formula ---------- */
/** Chebyshev's ψ(x) = sum of ln p over prime powers p^k <= x. */
export function psi(x) {
  let s = 0;
  for (const p of primes(Math.floor(x))) for (let q = p; q <= x; q *= p) s += Math.log(p);
  return s;
}

/** Riemann–von Mangoldt explicit formula for ψ(x), truncated after the first K zeros (K <= 1000). */
export function psiExplicit(x, K = 100) {
  const Lx = Math.log(x), sx = Math.sqrt(x);
  let v = x - Math.log(2 * Math.PI) - 0.5 * Math.log(1 - 1 / (x * x));
  for (let k = 0; k < Math.min(K, ZETA_ZEROS.length); k++) {
    const g = ZETA_ZEROS[k];
    v -= 2 * sx * (0.5 * Math.cos(g * Lx) + g * Math.sin(g * Lx)) / (0.25 + g * g);
  }
  return v;
}

/** Cipolla's three-term estimate of the n-th prime (n >= 6). */
export function nthPrimeEstimate(n) {
  const L = Math.log(n), LL = Math.log(L);
  return n * (L + LL - 1 + (LL - 2) / L);
}

/* ---------- Robin's inequality ---------- */
/** Sum of divisors σ(n), for n up to about 10^14. */
export function sigma(n) {
  let t = n, s = 1;
  for (let p = 2; p * p <= t; p++) if (t % p === 0) { let pk = 1, sum = 1; while (t % p === 0) { t /= p; pk *= p; sum += pk; } s *= sum; }
  if (t > 1) s *= t + 1;
  return s;
}

/** σ(n) / (n ln ln n). Robin (1984): the Riemann hypothesis holds iff this is below e^γ for every n > 5040. */
export function robinRatio(n) { return sigma(n) / (n * Math.log(Math.log(n))); }

/** The bound e^γ ≈ 1.78107 in Robin's inequality. */
export const ROBIN_BOUND = Math.exp(EULER_GAMMA);
