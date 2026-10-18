# @joycemalik/primewaves

The mathematics behind [*Where the Waves Go Quiet*](https://primes.joycemalik.com), a film about chasing the prime numbers and the Riemann hypothesis, as a small dependency-free JavaScript library.

```js
import { zeta, ZETA_ZEROS, psi, psiExplicit, waveSurvivors, robinRatio, ROBIN_BOUND } from '@joycemalik/primewaves';

zeta(0.5, ZETA_ZEROS[0]);        // ≈ [0, 0]: the first nontrivial zero, 1/2 + 14.1347i
psiExplicit(30.5, 1000);         // Riemann's explicit formula with 1,000 zeros ≈ psi(30.5)
waveSurvivors(200, 7);           // the prime wave with waves from 2, 3, 5, 7: first false positive is 121 = 11²
robinRatio(10080) < ROBIN_BOUND; // Robin's inequality holds (it would fail for some n > 5040 if RH were false)
```

| Export | What it does |
|---|---|
| `sieve(limit)`, `primes(limit)` | Sieve of Eratosthenes |
| `primeWave(n, P)`, `waveSurvivors(N, P)` | The prime wave W(n) = Σ 1/√p over context primes p ≤ P dividing n. It is exact up to P² |
| `zArrow(n)` | Z(n) = Σ_{p | n} e^{i p ln n}. Its modulus is 1 exactly on prime powers |
| `zeta(re, im)`, `gamma(re, im)` | Complex ζ and Γ (Borwein series and the functional equation), about 8 significant digits for \|t\| ≤ 100 |
| `ZETA_ZEROS` | Imaginary parts of the first 1,000 nontrivial zeros (mpmath) |
| `psi(x)`, `psiExplicit(x, K)` | Chebyshev's ψ and the Riemann–von Mangoldt explicit formula truncated after K zeros |
| `sigma(n)`, `robinRatio(n)`, `ROBIN_BOUND` | Robin's criterion: σ(n) < e^γ n ln ln n for all n > 5040 ⇔ RH |
| `nthPrimeEstimate(n)` | Cipolla's three-term estimate of the n-th prime |

## Install from GitHub Packages

```sh
echo "@joycemalik:registry=https://npm.pkg.github.com" >> .npmrc
npm install @joycemalik/primewaves
```

GitHub Packages asks for a token with `read:packages` even for public packages; see [GitHub's guide](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry#installing-a-package).

MIT licensed. Source and research: [github.com/joycemalik/primes](https://github.com/joycemalik/primes).
