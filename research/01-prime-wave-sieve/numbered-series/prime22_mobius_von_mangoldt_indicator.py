# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime22_mobius_von_mangoldt_indicator.py
# Original location      :: learn/prime22.py   (last edited 2025-08-08)
# What this script does  :: Exact prime indicator built from the Mobius and von Mangoldt functions.
# ----------------------------------------------------------------------------
# "Singular Prime Function" demo: exact indicator via Möbius-weighted von Mangoldt
#
# We implement:
#   P(n) = sum_{k >= 1} (mu(k)/k) * A(n^(1/k)),  with A(m) = Λ(m)/log(m) if m is integer >=2 else 0
# and show that P(n) == 1 iff n is prime, else 0.
#
# We'll:
#  1) Implement integer k-th root and perfect-power checks.
#  2) Implement mu(k) (Möbius) for small k and Λ(m) (von Mangoldt) for prime powers.
#  3) Evaluate P(n) for n up to N and compare to ground-truth primality.
#  4) Show a small table (n<=200) and summary stats up to 100000.
#
# Note: This is not optimized for huge n; it's a clear, correct reference implementation.


import math
import pandas as pd

def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    d = 3
    while d <= r:
        if n % d == 0:
            return False
        d += 2
    return True

def integer_kth_root(n: int, k: int) -> int:
    """Return floor(n**(1/k)) without floating error; assume n>=0, k>=1."""
    if k == 1:
        return n
    # initial guess via float then correct
    x = int(round(n ** (1.0 / k)))
    # fix rounding drift by adjusting
    while (x + 1) ** k <= n:
        x += 1
    while x ** k > n:
        x -= 1
    return x

def mobius(k: int) -> int:
    """Möbius function μ(k). Small k (<= log2 n) so trial division is fine."""
    if k == 1:
        return 1
    # factor k
    x = k
    mu = 1
    p = 2
    while p * p <= x:
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
            if cnt > 1:
                return 0  # square factor
        if cnt == 1:
            mu = -mu
        p += 1 if p == 2 else 2
    if x > 1:
        mu = -mu
    return mu

def is_prime_power(m: int):
    """Return (True, p, r) if m = p^r with prime p and r>=1; else (False, None, None)."""
    if m < 2:
        return (False, None, None)
    # check prime power by trying exponents r from max down to 1
    # but simplest: factor m by trial division and verify single prime factor
    x = m
    p = None
    r = 0
    d = 2
    while d * d <= x:
        if x % d == 0:
            if p is None:
                p = d
            elif p != d:
                return (False, None, None)  # more than one prime factor
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            r += cnt if p == d else 0
        d += 1 if d == 2 else 2
    if x > 1:
        if p is None:
            # m is prime -> p=m, r=1
            return (True, x, 1)
        if x != p:
            return (False, None, None)  # second distinct prime factor
        r += 1
    if p is None:
        # m was prime; already handled above
        return (True, m, 1)
    return (True, p, r)

def von_mangoldt(m: int) -> float:
    """Λ(m) = log p if m = p^r, else 0."""
    is_pp, p, r = is_prime_power(m)
    if not is_pp:
        return 0.0
    return math.log(p)

def A(m: int) -> float:
    """A(m) = Λ(m)/log m for integer m>=2 else 0."""
    if m < 2:
        return 0.0
    lam = von_mangoldt(m)
    if lam == 0.0:
        return 0.0
    return lam / math.log(m)

def prime_indicator_P(n: int) -> int:
    """P(n) = sum_{k>=1} mu(k)/k * A(n^(1/k)), where A(x)=0 if x not integer >=2."""
    if n < 2:
        return 0
    # Only k up to floor(log2 n) can matter because n^(1/k) >= 2 implies 2^k <= n.
    maxk = int(math.log(n, 2))
    acc = 0.0
    for k in range(1, maxk + 1):
        mu = mobius(k)
        if mu == 0:
            continue
        root = integer_kth_root(n, k)
        if root ** k != n:
            continue  # not a perfect k-th power
        acc += (mu / k) * A(root)
    # acc is exactly 0 or 1 in theory; map numerically
    return 1 if abs(acc - 1.0) < 1e-12 else 0

# --- Demo 1: small table n<=200
rows = []
for n in range(2, 201):
    gt = is_prime_trial(n)
    Pn = prime_indicator_P(n)
    case = "prime" if gt else ("prime power" if is_prime_power(n)[0] else "composite (non-pp)")
    rows.append({"n": n, "P(n)": Pn, "ground_truth_prime": int(gt), "classification": case})
df_small = pd.DataFrame(rows)
df_small = pd.DataFrame(rows)
print("Prime indicator P(n) vs ground truth (n<=200)")
print(df_small)
# --- Demo 2: large check up to 100000
LIMIT = 100000
errors = 0
for n in range(2, LIMIT + 1):
    gt = is_prime_trial(n)
    Pn = prime_indicator_P(n)
    if Pn != int(gt):
        errors += 1
errors
