/** A complex number as [real, imaginary]. */
export type Complex = [number, number];

/** Imaginary parts of the first 1,000 nontrivial zeros of ζ (ρ = 1/2 + iγ). */
export const ZETA_ZEROS: readonly number[];
/** e^γ ≈ 1.78107, the bound in Robin's inequality. */
export const ROBIN_BOUND: number;

export function sieve(limit: number): Uint8Array;
export function primes(limit: number): number[];
export function distinctPrimeFactors(n: number): number[];
export function primeWave(n: number, P: number): number;
export function waveSurvivors(N: number, P: number): { primes: number[]; falsePositives: number[] };
export function zArrow(n: number): Complex;
export function gamma(re: number, im?: number): Complex;
export function zeta(re: number, im?: number): Complex;
export function psi(x: number): number;
export function psiExplicit(x: number, K?: number): number;
export function nthPrimeEstimate(n: number): number;
export function sigma(n: number): number;
export function robinRatio(n: number): number;
