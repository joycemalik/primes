# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/detectors/minimal_prime_wave.py
# Original location      :: minimal_prime_wave.py   (last edited 2025-08-02)
# What this script does  :: Shortest generator of n primes using the wave formula.
# ----------------------------------------------------------------------------
"""
Minimal Prime Generator Using Wave Formula
=========================================

Pure implementation of W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p
"""

import math

def wave_function(n, context_primes):
    """
    W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p
    
    Returns the wave amplitude. If W(n) > 0, n is composite.
    """
    return sum(1.0 / math.sqrt(p) for p in context_primes if n % p == 0)

def is_prime_wave(n, context_primes):
    """Check if n is prime using wave interference."""
    if n < 2:
        return False
    if n in context_primes:
        return True
    if wave_function(n, context_primes) > 0:
        return False
    
    # Check beyond context using trial division
    max_context = max(context_primes) if context_primes else 1
    for i in range(max_context + 1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_n_primes(n):
    """Generate first n primes using wave formula."""
    context_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    primes = []
    candidate = 2
    
    while len(primes) < n:
        if is_prime_wave(candidate, context_primes):
            primes.append(candidate)
        candidate += 1
    
    return primes

# Demo
if __name__ == "__main__":
    print("🌊 Generating 50 primes using W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p")
    primes = generate_n_primes(50)
    
    print(f"First 50 primes: {primes}")
    print(f"Range: {primes[0]} to {primes[-1]}")
    
    # Show wave values for some numbers
    context = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    print(f"\nWave amplitudes for numbers 10-20:")
    for i in range(10, 10*6):
        w = wave_function(i, context)
        prime = is_prime_wave(i, context)
        print(f"W({i:2d}) = {w:6.4f} → {'Prime' if prime else 'Composite'}")
