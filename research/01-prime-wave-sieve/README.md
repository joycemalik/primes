# Prime wave sieve

**When:** 30 Jul – 3 Aug 2025

The founding idea: every small prime sends out a "wave" that peaks on its multiples. Add the waves and the primes are the nodes where the sum is zero. The numbered series (prime01 … prime22) is the original order of experiments. `detectors/` holds the 2 Aug class-based detectors, `unified-theory-crt/` the 3 Aug versions with Chinese-Remainder "suppression waves", and `notebooks/` the write-ups and proof attempts.

**Verdict:** The wave is exactly the Sieve of Eratosthenes. With context primes up to P it is correct on [1, P²] and nowhere beyond. Every "100%" result used primes up to √N, which is trial division, so the O(1) claims do not hold.

| Folder | What is in it |
|---|---|
| [`numbered-series/`](numbered-series/README.md) | prime01 – prime22 in their original order: product of sines, small-factor counts, raised cosines, spike superposition, the weighted wave, the multi-level detector, and an exact Möbius / von Mangoldt indicator. |
| [`detectors/`](detectors/README.md) | The 2 Aug detectors, from `prime_wave_detector.py` to `ultra_fast_prime_wave.py`, with `correctness_check.py`. |
| [`unified-theory-crt/`](unified-theory-crt/README.md) | The unified Prime Wave Theory with CRT suppression waves, the accuracy checker and `accuracy_report.txt` (78,498 / 78,498 below 10⁶). |
| [`notebooks/`](notebooks/README.md) | The Prime Wave Theorem notes, the zeta(2) cosine wave, and the prime18 / prime19 proof attempts. |
| [`figures/`](figures/README.md) | Saved plots of the wave patterns. |
