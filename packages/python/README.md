# primewaves

The mathematics behind [*Where the Waves Go Quiet*](https://primes.joycemalik.com), a film about chasing the prime numbers and the Riemann hypothesis, as a small pure-Python library with no dependencies.

```python
import primewaves as pw

pw.zeta(complex(0.5, pw.ZETA_ZEROS[0]))   # ≈ 0: the first nontrivial zero, 1/2 + 14.1347i
pw.psi_explicit(30.5, 1000)               # Riemann's explicit formula with 1,000 zeros ≈ pw.psi(30.5)
pw.wave_survivors(200, 7)[1][0]           # 121: the first composite the prime wave of 2, 3, 5, 7 lets through
pw.robin_ratio(10080) < pw.ROBIN_BOUND    # Robin's inequality holds; a failure above 5040 would disprove RH
```

| Function | What it does |
|---|---|
| `sieve`, `primes` | Sieve of Eratosthenes |
| `prime_wave(n, P)`, `wave_survivors(N, P)` | The prime wave W(n) = Σ 1/√p over context primes p ≤ P dividing n. It is exact up to P² |
| `z_arrow(n)` | Z(n) = Σ_{p \| n} e^{i p ln n}. Its modulus is 1 exactly on prime powers |
| `zeta(s)`, `gamma(s)` | Complex ζ and Γ (Borwein series and the functional equation) |
| `ZETA_ZEROS` | Imaginary parts of the first 1,000 nontrivial zeros (mpmath) |
| `psi(x)`, `psi_explicit(x, K)` | Chebyshev's ψ and the Riemann–von Mangoldt explicit formula |
| `sigma`, `robin_ratio`, `ROBIN_BOUND` | Robin's criterion: σ(n) < e^γ n ln ln n for all n > 5040 ⇔ RH |
| `nth_prime_estimate(n)` | Cipolla's three-term estimate of the n-th prime |

## Install

Download the wheel from the [latest release](https://github.com/joycemalik/primes/releases/latest), then:

```sh
pip install primewaves-1.0.0-py3-none-any.whl
```

Or install straight from the repository:

```sh
pip install "git+https://github.com/joycemalik/primes.git#subdirectory=packages/python"
```

MIT licensed. Source and research: [github.com/joycemalik/primes](https://github.com/joycemalik/primes).
