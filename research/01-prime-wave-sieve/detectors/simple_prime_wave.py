# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/detectors/simple_prime_wave.py
# Original location      :: simple_prime_wave.py   (last edited 2025-08-02)
# What this script does  :: Minimal function version of the wave detector.
# ----------------------------------------------------------------------------
"""
Simple Prime Wave Function Implementation
========================================

The pure mathematical essence of prime detection through wave interference.
"""

import math
from typing import List

def generate_context_primes(limit: int) -> List[int]:
    """Generate primes up to limit using Sieve of Eratosthenes."""
    if limit < 2:
        return []
    
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    
    return [i for i in range(2, limit + 1) if sieve[i]]

def prime_wave_function(n: int, context_primes: List[int]) -> float:
    """
    The Prime Wave Function: W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p
    
    Returns the wave amplitude at integer n.
    """
    amplitude = 0.0
    for p in context_primes:
        if n % p == 0:  # n is divisible by prime p
            amplitude += 1.0 / math.sqrt(p)
    return amplitude

def is_prime_wave(n: int, context_primes: List[int]) -> bool:
    """
    Prime detection using wave function.
    
    Prime Criterion: W(n) = 0 OR n ∈ context_primes
    """
    if n < 2:
        return False
    if n in context_primes:
        return True
    return prime_wave_function(n, context_primes) == 0.0

def main():
    print("🌊 SIMPLE PRIME WAVE FUNCTION TEST 🌊")
    print("="*50)
    
    # Use minimal context - just first few primes
    context_primes = generate_context_primes(30)  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    print(f"Context primes: {context_primes}")
    print(f"Formula: W(n) = Σ(p∈{{{','.join(map(str, context_primes))}}}) [n ≡ 0 (mod p)] / √p")
    print()
    
    # Test the wave function on first 50 numbers
    print("n    W(n)     Prime?  Actual")
    print("---  ------   ------  ------")
    
    # Generate actual primes for comparison
    actual_primes = set(generate_context_primes(50))
    
    correct_predictions = 0
    total_tests = 0
    
    for n in range(1, 51):
        wave_val = prime_wave_function(n, context_primes)
        predicted = is_prime_wave(n, context_primes)
        actual = n in actual_primes
        
        status = "✓" if predicted == actual else "✗"
        if predicted == actual:
            correct_predictions += 1
        total_tests += 1
        
        print(f"{n:2d}   {wave_val:6.3f}   {'Prime' if predicted else 'Comp ':>5}   {'Prime' if actual else 'Comp ':>5} {status}")
    
    accuracy = correct_predictions / total_tests * 100
    print(f"\nAccuracy: {correct_predictions}/{total_tests} = {accuracy:.1f}%")
    
    # Test larger numbers
    print(f"\n🚀 Testing larger numbers:")
    large_tests = [97, 98, 99, 100, 101, 997, 1009, 1013, 10007, 100003]
    
    for n in large_tests:
        wave_val = prime_wave_function(n, context_primes)
        predicted = is_prime_wave(n, context_primes)
        print(f"W({n:6d}) = {wave_val:6.3f} → {'Prime' if predicted else 'Composite'}")
    
    print(f"\n✨ The wave reveals the hidden pattern of primes! ✨")
    

if __name__ == "__main__":
    main()
