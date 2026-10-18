"""The mathematics behind "Where the Waves Go Quiet" (https://primes.joycemalik.com)."""
from __future__ import annotations

import cmath
import math

from .zeros import ZETA_ZEROS

EULER_GAMMA = 0.5772156649015329
ROBIN_BOUND = math.exp(EULER_GAMMA)  # e^gamma, about 1.78107


def sieve(limit: int) -> bytearray:
    """Sieve of Eratosthenes: result[n] == 1 when n is prime, for 0 <= n <= limit."""
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0:2] = b"\x00\x00"[: min(2, limit + 1)]
    for i in range(2, math.isqrt(limit) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = bytearray(len(range(i * i, limit + 1, i)))
    return is_prime


def primes(limit: int) -> list[int]:
    """All primes up to and including limit."""
    s = sieve(limit)
    return [n for n in range(2, limit + 1) if s[n]]


def distinct_prime_factors(n: int) -> list[int]:
    """Distinct prime factors of n, in increasing order."""
    factors, p = [], 2
    while p * p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        factors.append(n)
    return factors


def prime_wave(n: int, P: int) -> float:
    """W(n): every context prime p <= P sends 1/sqrt(p) to each proper multiple. Exact for n <= P**2 only."""
    return sum(1 / math.sqrt(p) for p in primes(P) if n % p == 0 and n != p)


def wave_survivors(N: int, P: int) -> tuple[list[int], list[int]]:
    """Nodes of the prime wave in [2, N]: (true primes, composites that slip through)."""
    ctx, is_prime = primes(P), sieve(N)
    good, bad = [], []
    for n in range(2, N + 1):
        if any(n % p == 0 and n != p for p in ctx):
            continue
        (good if is_prime[n] else bad).append(n)
    return good, bad


def z_arrow(n: int) -> complex:
    """Z(n) = sum over distinct primes p | n of e^{i p ln n}. |Z(n)| == 1 exactly on prime powers."""
    return sum(cmath.exp(1j * p * math.log(n)) for p in distinct_prime_factors(n))


_LANCZOS = (0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
            -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7)


def gamma(s: complex) -> complex:
    """Complex Gamma function (Lanczos approximation with reflection)."""
    s = complex(s)
    if s.real < 0.5:
        return math.pi / (cmath.sin(math.pi * s) * gamma(1 - s))
    s -= 1
    x = _LANCZOS[0] + sum(c / (s + i) for i, c in enumerate(_LANCZOS[1:], start=1))
    t = s + 7.5
    return math.sqrt(2 * math.pi) * t ** (s + 0.5) * cmath.exp(-t) * x


_N = 64
_D = []
_term, _sum = 1 / _N, 0.0
for _i in range(_N + 1):
    if _i > 0:
        _term *= 4 * (_N + _i - 1) * (_N - _i + 1) / ((2 * _i - 1) * (2 * _i))
    _sum += _term
    _D.append(_N * _sum)


def zeta(s: complex) -> complex:
    """Riemann zeta function (Borwein's series, functional equation for Re s < 1/2). About 8 digits for |Im s| <= 100."""
    s = complex(s)
    if s.real < 0.5:
        return 2 ** s * math.pi ** (s - 1) * cmath.sin(math.pi * s / 2) * gamma(1 - s) * zeta(1 - s)
    total = sum((-1) ** k * (_D[k] - _D[_N]) / (k + 1) ** s for k in range(_N))
    return -total / _D[_N] / (1 - 2 ** (1 - s))


def psi(x: float) -> float:
    """Chebyshev's psi(x): sum of ln p over prime powers p**k <= x."""
    total = 0.0
    for p in primes(int(x)):
        q = p
        while q <= x:
            total += math.log(p)
            q *= p
    return total


def psi_explicit(x: float, K: int = 100) -> float:
    """Riemann–von Mangoldt explicit formula for psi(x), truncated after the first K zeros (K <= 1000)."""
    lx, sx = math.log(x), math.sqrt(x)
    v = x - math.log(2 * math.pi) - 0.5 * math.log(1 - 1 / (x * x))
    for g in ZETA_ZEROS[:K]:
        v -= 2 * sx * (0.5 * math.cos(g * lx) + g * math.sin(g * lx)) / (0.25 + g * g)
    return v


def nth_prime_estimate(n: int) -> float:
    """Cipolla's three-term estimate of the n-th prime (n >= 6)."""
    L = math.log(n)
    LL = math.log(L)
    return n * (L + LL - 1 + (LL - 2) / L)


def sigma(n: int) -> int:
    """Sum of the divisors of n."""
    total, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            pk, s = 1, 1
            while n % p == 0:
                n //= p
                pk *= p
                s += pk
            total *= s
        p += 1
    if n > 1:
        total *= n + 1
    return total


def robin_ratio(n: int) -> float:
    """sigma(n) / (n ln ln n). Robin (1984): RH holds iff this is below e^gamma for every n > 5040."""
    return sigma(n) / (n * math.log(math.log(n)))
