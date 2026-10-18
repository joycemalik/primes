# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/08_wave_guided_nth_prime.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/8.py   (last edited 2025-08-26)
# What this script does  :: Cipolla estimate + Legendre count + wave score to find p_n.
# ----------------------------------------------------------------------------
# wave_guided_nth_prime.py
import math
from functools import lru_cache

# --- 1) small-prime base (odd-only sieve) ---
def primes_up_to(n: int):
    if n < 2: return []
    if n == 2: return [2]
    m = (n - 3)//2 + 1
    is_p = bytearray(b"\x01") * m
    r = int(n**0.5)
    for i in range((r - 3)//2 + 1):
        if is_p[i]:
            p = 2*i + 3
            start = (p*p - 3)//2
            is_p[start::p] = b"\x00" * (((m - start - 1)//p) + 1)
    return [2] + [2*i + 3 for i,b in enumerate(is_p) if b]

# --- 2) PNT/Cipolla seed for p_n and a narrow window ---
def cipolla_seed(n: int) -> float:
    if n <= 5: return [2,3,5,7,11][n-1]
    ln = math.log(n); lln = math.log(ln)
    # good 2-term refinement
    return n*(ln + lln - 1 + (lln - 2)/ln)

def bracket(n: int, k: float = 14.0):
    a = int(cipolla_seed(n))
    w = max(64, int(k * math.log(max(10, a))**2))  # ~ gap ~ O(log^2 n)
    return max(2, a - w), a + w

# --- 3) Legendre's π(x) using primes up to sqrt(x) only ---
def pi_legendre(x: int, base_primes):
    if x < 2: return 0
    a_max = 0
    while a_max < len(base_primes) and base_primes[a_max] <= int(x**0.5):
        a_max += 1
    @lru_cache(maxsize=None)
    def phi(xv: int, a: int) -> int:
        if a == 0: return xv
        p = base_primes[a-1]
        return phi(xv, a-1) - phi(xv // p, a-1)
    return phi(x, a_max) + a_max - 1

# --- 4) optional: your "wave" score to rank candidates ---
def wave_score(x: int, small_primes=(2,3,5,7,11,13,17,19,23,29)):
    # simple superposition score; higher means "more prime-like" in your sense
    import math
    return sum(math.cos(2*math.pi*x/p) for p in small_primes)

# --- 5) exact primality using trial division by base primes up to sqrt(U) ---
def is_prime_exact(x: int, base_primes):
    if x < 2: return False
    for p in base_primes:
        if p*p > x: break
        if x % p == 0: return False
    return True

# --- 6) fast residue wheel (skip obvious composites) ---
def wheel_residues(mod):
    res = [r for r in range(mod) if math.gcd(r, mod) == 1]
    return mod, res

def generate_candidates(L: int, U: int, mod, residues):
    start = (L // mod) * mod
    for block in range(start, U + mod, mod):
        for r in residues:
            x = block + r
            if L <= x <= U:
                yield x

# --- 7) glue it together: exact nth prime, wave-guided ---
def nth_prime_wave_guided(n: int, use_wave=True) -> int:
    if n <= 5: return [2,3,5,7,11][n-1]

    # bracket near p_n
    L, U = bracket(n)

    # base primes up to sqrt(U) only (small!)
    base = primes_up_to(int(U**0.5) + 1)

    # exact rank at L-1 via Legendre π(x)
    pi_before = pi_legendre(L-1, base)

    # wheel on first few primes to jump over obvious composites
    W = 2*3*5*7*11  # 2310 wheel is fine; raise if you like
    mod, residues = wheel_residues(W)

    # enumerate candidates; optionally rank with your wave score
    cands = list(generate_candidates(L, U, mod, residues))
    if use_wave:
        cands.sort(key=lambda x: (-wave_score(x), x))  # try “most prime-like” first
    else:
        cands.sort()

    # scan & count exactly
    count = pi_before
    for x in cands:
        if is_prime_exact(x, base):
            count += 1
            if count == n:
                return x

    # if bracket missed, widen safely and retry (rare)
    # fallback: widen by a factor and try again
    L2 = max(2, L - (U - L))
    U2 = U + (U - L)
    base2 = primes_up_to(int(U2**0.5) + 1)
    pi_before2 = pi_legendre(L2-1, base2)
    cands = list(generate_candidates(L2, U2, mod, residues))
    if use_wave:
        cands.sort(key=lambda x: (-wave_score(x), x))
    else:
        cands.sort()

    count = pi_before2
    for x in cands:
        if is_prime_exact(x, base2):
            count += 1
            if count == n:
                return x

    # As a last resort you can drop to a classic segmented sieve from 2..U2.
    raise RuntimeError("Bracket too narrow; widen further or fall back to segmented sieve.")


# --- 8) simple CLI / runner + plotting ---
def main():
    """Run a few sample queries, print timings, and plot n vs p_n."""
    import time
    import matplotlib.pyplot as plt
    from pathlib import Path

    # sample n values (kept moderate to keep runtime reasonable)
    sample_n = [10, 50, 100, 200, 500, 1000, 1800]

    results = []
    print("Computing nth primes using nth_prime_wave_guided() and (if available) predicting via 7.py:g()")

    # Try to load prediction function `g` from 7.py
    predict_model = None
    try:
        import importlib.util
        module7_path = Path(__file__).resolve().parent / '07_nth_prime_linear_regression.py'
        if module7_path.exists():
            spec = importlib.util.spec_from_file_location('model7', str(module7_path))
            model7 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(model7)
            predict_model = getattr(model7, 'g', None)
            if predict_model:
                print('Loaded predictor g(n) from 7.py')
        else:
            print('7.py not found; skipping predictions')
    except Exception as e:
        print('Failed to load 7.py predictor:', e)
        predict_model = None

    for n in sample_n:
        t0 = time.time()
        try:
            p = nth_prime_wave_guided(n, use_wave=True)
        except Exception as e:
            print(f"n={n}: ERROR: {e}")
            p = None
        dt = time.time() - t0

        pred = None
        if predict_model and p is not None:
            try:
                pred = predict_model(int(n))
            except Exception as e:
                print(f"Prediction error for n={n}: {e}")
                pred = None

        print(f"n={n}: p_n={p} (t={dt:.3f}s), predicted={pred}")
        results.append((n, p, pred, dt))

    # Filter out failed actual results
    valid = [(n, p, pred) for n, p, pred, _ in results if p is not None]
    if valid:
        ns = [t[0] for t in valid]
        ps = [t[1] for t in valid]
        preds = [t[2] for t in valid]

        plt.figure(figsize=(10, 6))
        plt.plot(ns, ps, marker='o', linestyle='-', label='Actual p_n')
        if any(pred is not None for pred in preds):
            # For plotting, replace None with NaN so matplotlib skips them
            import math as _math
            preds_plot = [(_math.nan if v is None else v) for v in preds]
            plt.plot(ns, preds_plot, marker='x', linestyle='--', label='Predicted (7.py:g)')

        plt.xlabel('n')
        plt.ylabel('Prime value')
        plt.title('Actual primes vs Predicted primes')
        plt.legend()
        plt.grid(True)

        out_path = Path(__file__).resolve().parent / '8_results.png'
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        print(f"Saved plot to: {out_path}")
    else:
        print("No valid results to plot.")


if __name__ == '__main__':
    main()
