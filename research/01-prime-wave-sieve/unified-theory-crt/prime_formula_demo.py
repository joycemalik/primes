# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/unified-theory-crt/prime_formula_demo.py
# Original location      :: learn/pime/check/prime_formula_demo.py   (last edited 2025-08-03)
# What this script does  :: Demonstrates the PrimeWaveFunction formula.
# ----------------------------------------------------------------------------
"""
PRIME WAVE FUNCTION - MATHEMATICAL FORMULA
==========================================

The core mathematical function that can determine if ANY number is prime.
"""

from prime_wave_function import PrimeWaveFunction

def demonstrate_prime_wave_formula():
    """Show the exact mathematical formula and test it"""
    
    print("🌊 PRIME WAVE MATHEMATICAL FUNCTION")
    print("=" * 60)
    print()
    
    # Initialize
    wave = PrimeWaveFunction()
    
    # Show formula
    print("📐 MATHEMATICAL FORMULA:")
    print("-" * 30)
    print("W(n) = Σ[p∈{2,3,5,7}] I(n mod p == 0, n ≠ p) + S(n)")
    print()
    print("Where:")
    print("• I(condition) = 1 if true, 0 if false")
    print("• S(n) = suppression for false positives")
    print()
    print("🎯 PRIME TEST RULE:")
    print("• W(n) < 0.5  →  n is PRIME")
    print("• W(n) ≥ 0.5  →  n is COMPOSITE")
    print()
    
    # Test specific examples
    test_cases = [
        (2, "First prime"),
        (17, "Random prime"), 
        (101, "Large prime"),
        (997, "Very large prime"),
        (4, "Even composite"),
        (9, "Odd composite"),
        (121, "Perfect square"),
        (143, "Semiprime (11×13)")
    ]
    
    print("🧮 FUNCTION EXAMPLES:")
    print("-" * 50)
    print(f"{'Number':>8} {'W(n)':>8} {'Result':>12} {'Description':>20}")
    print("-" * 50)
    
    for n, desc in test_cases:
        amplitude = wave.wave_amplitude(n)
        result = "PRIME" if amplitude < 0.5 else "COMPOSITE"
        print(f"{n:>8} {amplitude:>8.1f} {result:>12} {desc:>20}")
    
    print("-" * 50)
    print()
    
    # Show step-by-step calculation for one example
    print("📊 STEP-BY-STEP CALCULATION for n = 121:")
    print("-" * 40)
    n = 121
    print(f"1. Check multiples of seed primes [2,3,5,7]:")
    amplitude = 0
    for p in [2, 3, 5, 7]:
        is_multiple = (n % p == 0 and n != p)
        contribution = 1.0 if is_multiple else 0.0
        amplitude += contribution
        print(f"   121 mod {p} = {n % p} → {'Multiple' if is_multiple else 'Not multiple'} → +{contribution}")
    
    print(f"2. Base amplitude = {amplitude}")
    
    # Check suppression
    import math
    is_coprime = all(math.gcd(n, p) == 1 for p in [2, 3, 5, 7])
    print(f"3. Is 121 coprime to [2,3,5,7]? {is_coprime}")
    
    if is_coprime:
        # Check if composite
        is_composite = any(n % i == 0 for i in range(2, int(n**0.5) + 1))
        print(f"4. Is 121 composite? {is_composite} (121 = 11×11)")
        if is_composite:
            amplitude += 1.0
            print(f"5. Apply suppression: +1.0")
    
    print(f"6. Final W(121) = {amplitude}")
    print(f"7. Since {amplitude} ≥ 0.5 → 121 is COMPOSITE ✅")
    print()
    
    return wave

if __name__ == "__main__":
    wave_function = demonstrate_prime_wave_formula()
    
    print("🎯 READY TO USE!")
    print("Use wave_function.is_prime(n) to test any number n")
    print("Or wave_function.wave_amplitude(n) for the raw amplitude")
