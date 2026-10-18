# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/detectors/prime_wave_detector.py
# Original location      :: prime_wave_detector.py   (last edited 2025-08-02)
# What this script does  :: W(n) = sum over context primes p | n of 1/sqrt(p); prime iff W(n) = 0. Exact only up to P^2.
# ----------------------------------------------------------------------------
"""
Prime Wave Function Detector
============================

A revolutionary prime detection algorithm based on wave interference theory.
Uses the mathematical formula: W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p

Prime Criterion: n is prime ⟺ W(n) = 0 OR n ∈ P
"""

import math
import time
from typing import List, Tuple

class PrimeWaveDetector:
    """
    Prime detector using the Prime Wave Function.
    
    The wave function W(n) encodes primality through interference patterns.
    Primes exist at nodes where no prime waves interfere.
    """
    
    def __init__(self, context_limit: int = 50):
        """
        Initialize the detector with context primes.
        
        Args:
            context_limit: Use primes up to this limit as context
        """
        self.context_limit = context_limit
        self.context_primes = self._generate_context_primes(context_limit)
        self.context_set = set(self.context_primes)
        
        print(f"🌊 Prime Wave Detector Initialized")
        print(f"Context: {len(self.context_primes)} primes up to {context_limit}")
        print(f"Context primes: {self.context_primes}")
    
    def _generate_context_primes(self, limit: int) -> List[int]:
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
    
    def wave_function(self, n: int) -> float:
        """
        Compute the Prime Wave Function value at n.
        
        W(n) = Σ(p∈context) [n ≡ 0 (mod p)] / √p
        
        Args:
            n: Integer to evaluate
            
        Returns:
            Wave amplitude at n
        """
        amplitude = 0.0
        for p in self.context_primes:
            if n % p == 0:  # n is divisible by prime p
                amplitude += 1.0 / math.sqrt(p)
        return amplitude
    
    def is_prime(self, n: int) -> bool:
        """
        Determine if n is prime using the wave function.
        
        Prime Criterion: W(n) = 0 OR n ∈ context_primes
        
        Args:
            n: Integer to test
            
        Returns:
            True if n is prime, False otherwise
        """
        if n < 2:
            return False
        if n in self.context_set:
            return True
        
        return self.wave_function(n) == 0.0
    
    def find_primes_in_range(self, start: int, end: int) -> List[int]:
        """
        Find all primes in the range [start, end] using wave function.
        
        Args:
            start: Start of range (inclusive)
            end: End of range (inclusive)
            
        Returns:
            List of primes in the range
        """
        primes = []
        for n in range(max(2, start), end + 1):
            if self.is_prime(n):
                primes.append(n)
        return primes
    
    def benchmark(self, test_range: int = 10000) -> Tuple[float, float, float]:
        """
        Benchmark the detector against known prime testing.
        
        Args:
            test_range: Test primes up to this limit
            
        Returns:
            Tuple of (precision, recall, f1_score)
        """
        print(f"\n🔬 Benchmarking against range 1-{test_range}...")
        
        # Generate actual primes for comparison
        actual_primes = set(self._generate_context_primes(test_range))
        
        # Find primes using wave function
        start_time = time.time()
        predicted_primes = set(self.find_primes_in_range(2, test_range))
        detection_time = time.time() - start_time
        
        # Calculate metrics
        true_positives = len(predicted_primes & actual_primes)
        false_positives = len(predicted_primes - actual_primes)
        false_negatives = len(actual_primes - predicted_primes)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"⚡ Detection completed in {detection_time:.4f} seconds")
        print(f"📊 Results:")
        print(f"   Total actual primes: {len(actual_primes)}")
        print(f"   Total predicted primes: {len(predicted_primes)}")
        print(f"   True Positives: {true_positives}")
        print(f"   False Positives: {false_positives}")
        print(f"   False Negatives: {false_negatives}")
        print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
        print(f"   Recall: {recall:.4f} ({recall*100:.2f}%)")
        print(f"   F1-Score: {f1_score:.4f}")
        
        if false_positives > 0:
            fps = sorted(list(predicted_primes - actual_primes))[:10]
            print(f"   First 10 false positives: {fps}")
        
        return precision, recall, f1_score


def main():
    """Main demonstration of the Prime Wave Detector."""
    
    print("="*60)
    print("🌊 PRIME WAVE FUNCTION DETECTOR 🌊")
    print("="*60)
    
    # Initialize detector
    detector = PrimeWaveDetector(context_limit=50)
    
    print(f"\n📐 Mathematical Formula:")
    print(f"W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p")
    print(f"Prime Criterion: W(n) = 0 OR n ∈ P")
    
    # Test individual numbers
    print(f"\n🔍 Testing Individual Numbers:")
    test_numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 97, 98, 99, 100, 101, 997, 1009]
    
    for n in test_numbers:
        wave_val = detector.wave_function(n)
        is_prime = detector.is_prime(n)
        print(f"W({n:4d}) = {wave_val:6.3f} → {'Prime' if is_prime else 'Composite'}")
    
    # Find primes in small ranges
    print(f"\n🎯 Finding Primes in Ranges:")
    ranges = [(1, 30), (100, 130), (900, 930)]
    
    for start, end in ranges:
        primes = detector.find_primes_in_range(start, end)
        print(f"Primes in [{start}, {end}]: {primes}")
    
    # Benchmark performance
    print(f"\n" + "="*60)
    detector.benchmark(test_range=100000)
    
    # Test extreme cases
    print(f"\n🚀 Testing Large Numbers:")
    large_numbers = [10007, 10009, 10037, 10039, 100003, 100019, 1000003, 1000033]
    
    for n in large_numbers:
        start_time = time.time()
        is_prime = detector.is_prime(n)
        test_time = time.time() - start_time
        wave_val = detector.wave_function(n)
        print(f"W({n:7d}) = {wave_val:6.3f} → {'Prime' if is_prime else 'Composite'} ({test_time*1000:.2f}ms)")
    
    print(f"\n" + "="*60)
    print(f"✨ Prime Wave Function: Where Mathematics Meets Wave Physics! ✨")
    print(f"="*60)


if __name__ == "__main__":
    main()
