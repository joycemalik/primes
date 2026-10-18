# detectors

Part of **Prime wave sieve** (30 Jul – 3 Aug 2025). See `../README.md` for the overview.

| File / folder | Was | Last edited | What it is |
|---|---|---|---|
| `prime_wave_detector.py` | `prime_wave_detector.py` | 2025-08-02 | W(n) = sum over context primes p \| n of 1/sqrt(p); prime iff W(n) = 0. Exact only up to P^2. |
| `simple_prime_wave.py` | `simple_prime_wave.py` | 2025-08-02 | Minimal function version of the wave detector. |
| `minimal_prime_wave.py` | `minimal_prime_wave.py` | 2025-08-02 | Shortest generator of n primes using the wave formula. |
| `simple_prime_generator.py` | `simple_prime_generator.py` | 2025-08-02 | Class-based generator of the first n primes via the wave test. |
| `enhanced_prime_wave.py` | `enhanced_prime_wave.py` | 2025-08-02 | Adds a cancellation wave to remove false positives. |
| `perfect_prime_wave.py` | `perfect_prime_wave.py` | 2025-08-02 | Primary wave plus cancellation wave; equivalent to trial division up to sqrt(n). |
| `simplified_prime_wave.py` | `simplified_prime_wave.py` | 2025-08-02 | Simplified multi-level detector. |
| `ultimate_prime_wave.py` | `ultimate_prime_wave.py` | 2025-08-02 | Four-level cascading detector tested to 5,000,000. |
| `ultra_fast_prime_wave.py` | `ultra_fast_prime_wave.py` | 2025-08-02 | Fast detector with a 50,000-prime context, stress-tested toward 10^10. Imported by correctness_check.py. |
| `correctness_check.py` | `correctness_check.py` | 2025-08-02 | Correctness tests for ultra_fast_prime_wave (small primes, large primes, composites, SymPy). |
| `ultra_simple_wave_grapher.py` | `ultra_simple_wave.py` | 2025-08-02 | Graphs the wave function over a range and marks detections. |
| `graphical_prime_wave.py` | `graphical_prime_wave.py` | 2025-08-02 | Graphical analysis of W(n) and prime/composite classification. |
