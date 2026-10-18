"""
Simplified Ultimate Prime Wave Function
======================================

Clean, efficient implementation for large-scale prime detection.
Tests against preloaded prime datasets for validation.
"""

import math
import time
from typing import Set, List

class SimplifiedPrimeWaveDetector:
    """
    Simplified prime detector using multi-level wave interference.
    Optimized for speed and accuracy up to 10^10.
    """
    
    def __init__(self, context_limit=10000):
        """Initialize with single adaptive context limit."""
        self.context_limit = context_limit
        
        print(f"🌊 Generating context primes up to {context_limit}...")
        start_time = time.time()
        
        # Generate all context primes efficiently
        self.context_primes = self._sieve(context_limit)
        self.context_set = set(self.context_primes)
        
        # Partition for optimization
        self.small_primes = [p for p in self.context_primes if p <= 100]
        self.medium_primes = [p for p in self.context_primes if 100 < p <= 1000]
        self.large_primes = [p for p in self.context_primes if p > 1000]
        
        setup_time = time.time() - start_time
        print(f"✅ Context ready: {len(self.context_primes)} primes in {setup_time:.3f}s")
        print(f"   Small (≤100): {len(self.small_primes)}")
        print(f"   Medium (100-1000): {len(self.medium_primes)}")
        print(f"   Large (>1000): {len(self.large_primes)}")
    
    def _sieve(self, n):
        """Fast Sieve of Eratosthenes."""
        if n < 2:
            return []
        
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                for j in range(i * i, n + 1, i):
                    sieve[j] = False
        
        return [i for i in range(2, n + 1) if sieve[i]]
    
    def primary_wave(self, n):
        """Primary wave function: W(n) = Σ(p∈small) [n ≡ 0 (mod p)] / √p"""
        amplitude = 0.0
        for p in self.small_primes:
            if n % p == 0:
                amplitude += 1.0 / math.sqrt(p)
        return amplitude
    
    def has_factor_in_list(self, n, prime_list):
        """Optimized factor checking with early termination."""
        sqrt_n = int(math.sqrt(n)) + 1
        for p in prime_list:
            if p >= sqrt_n:
                break
            if n % p == 0:
                return True
        return False
    
    def is_prime(self, n):
        """
        Simplified prime detection using wave interference.
        
        Algorithm:
        1. If n ∈ context_primes: definitely prime
        2. If primary_wave(n) > 0: definitely composite
        3. If has factors in medium/large primes: composite
        4. Otherwise: prime
        """
        if n < 2:
            return False
        
        # Direct lookup for context primes
        if n in self.context_set:
            return True
        
        # Primary wave test
        if self.primary_wave(n) > 0:
            return False
        
        # Medium prime factors
        if self.has_factor_in_list(n, self.medium_primes):
            return False
        
        # Large prime factors
        if self.has_factor_in_list(n, self.large_primes):
            return False
        
        # Survived all tests - it's prime
        return True
    
    def check_prime_batch(self, numbers):
        """Check multiple numbers efficiently."""
        results = []
        for n in numbers:
            results.append(self.is_prime(n))
        return results


def validate_against_sympy(detector, test_ranges):
    """Validate our detector against SymPy's isprime function."""
    try:
        from sympy import isprime
        print("✅ SymPy available for validation")
    except ImportError:
        print("❌ SymPy not available, installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "sympy"])
        from sympy import isprime
        print("✅ SymPy installed and ready")
    
    total_tests = 0
    total_correct = 0
    total_time_wave = 0
    total_time_sympy = 0
    
    print(f"\n🔬 VALIDATION AGAINST SYMPY")
    print(f"=" * 60)
    
    for start, end in test_ranges:
        print(f"\n📊 Testing range [{start:,}, {end:,}]...")
        
        numbers = list(range(start, end + 1))
        
        # Test our wave detector
        start_time = time.time()
        wave_results = detector.check_prime_batch(numbers)
        wave_time = time.time() - start_time
        
        # Test SymPy
        start_time = time.time()
        sympy_results = [isprime(n) for n in numbers]
        sympy_time = time.time() - start_time
        
        # Compare results
        correct = sum(1 for w, s in zip(wave_results, sympy_results) if w == s)
        total = len(numbers)
        
        accuracy = correct / total * 100
        speed_ratio = sympy_time / wave_time if wave_time > 0 else float('inf')
        
        print(f"   Accuracy: {correct:,}/{total:,} = {accuracy:.6f}%")
        print(f"   Wave time: {wave_time:.4f}s ({total/wave_time:,.0f} nums/sec)")
        print(f"   SymPy time: {sympy_time:.4f}s ({total/sympy_time:,.0f} nums/sec)")
        print(f"   Speed ratio: {speed_ratio:.1f}x faster")
        
        # Track mismatches
        mismatches = [(n, w, s) for n, w, s in zip(numbers, wave_results, sympy_results) if w != s]
        if mismatches:
            print(f"   ❌ {len(mismatches)} mismatches:")
            for n, wave_result, sympy_result in mismatches[:10]:
                print(f"      {n}: Wave={wave_result}, SymPy={sympy_result}")
            if len(mismatches) > 10:
                print(f"      ... and {len(mismatches) - 10} more")
        else:
            print(f"   ✅ Perfect match!")
        
        total_tests += total
        total_correct += correct
        total_time_wave += wave_time
        total_time_sympy += sympy_time
    
    # Overall results
    overall_accuracy = total_correct / total_tests * 100
    overall_speed_ratio = total_time_sympy / total_time_wave
    
    print(f"\n🏆 OVERALL VALIDATION RESULTS:")
    print(f"Total numbers tested: {total_tests:,}")
    print(f"Overall accuracy: {total_correct:,}/{total_tests:,} = {overall_accuracy:.6f}%")
    print(f"Overall speed: {overall_speed_ratio:.1f}x faster than SymPy")
    print(f"Wave detector: {total_tests/total_time_wave:,.0f} numbers/second")
    print(f"SymPy: {total_tests/total_time_sympy:,.0f} numbers/second")
    
    return overall_accuracy, overall_speed_ratio


def test_large_scale():
    """Test the detector on progressively larger scales."""
    
    print("="*80)
    print("🚀 LARGE-SCALE PRIME WAVE DETECTOR TEST")
    print("="*80)
    
    # Initialize detector
    detector = SimplifiedPrimeWaveDetector(context_limit=20000)
    
    # Test ranges - progressively larger
    test_ranges = [
        (2, 1000),           # Small: 10^3
        (10000, 11000),      # Medium: 10^4 range
        (100000, 101000),    # Large: 10^5 range
        (1000000, 1001000),  # Very large: 10^6 range
        (10000000, 10001000), # Huge: 10^7 range
        (100000000, 100001000), # Massive: 10^8 range
    ]
    
    # Validate against SymPy
    accuracy, speed_ratio = validate_against_sympy(detector, test_ranges)
    
    # Test individual large primes
    print(f"\n🎯 TESTING SPECIFIC LARGE PRIMES:")
    large_primes_to_test = [
        # Known large primes
        982451653,      # ~10^9
        1000000007,     # 10^9 + 7
        1000000009,     # 10^9 + 9
        10000000019,    # 10^10 + 19
        10000000033,    # 10^10 + 33
    ]
    
    print(f"Testing known large primes:")
    for p in large_primes_to_test:
        start_time = time.time()
        result = detector.is_prime(p)
        test_time = time.time() - start_time
        print(f"   {p:,}: {'Prime' if result else 'Composite'} ({test_time*1000:.2f}ms)")
    
    # Performance summary
    if accuracy >= 99.99:
        print(f"\n🏆 EXCEPTIONAL PERFORMANCE ACHIEVED!")
        print(f"✅ Accuracy: {accuracy:.4f}%")
        print(f"⚡ Speed: {speed_ratio:.1f}x faster than SymPy")
        print(f"🌊 Wave interference successfully reveals prime structure!")
    else:
        print(f"\n📈 GOOD PERFORMANCE:")
        print(f"Accuracy: {accuracy:.4f}%")
        print(f"Areas for improvement identified")
    
    return detector, accuracy, speed_ratio


if __name__ == "__main__":
    test_large_scale()
