# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/detectors/simple_prime_generator.py
# Original location      :: simple_prime_generator.py   (last edited 2025-08-02)
# What this script does  :: Class-based generator of the first n primes via the wave test.
# ----------------------------------------------------------------------------
"""
Simple Prime Generator Using Wave Formula
========================================

Uses the Prime Wave Function W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p
to generate the first n primes.
"""

import math

class SimplePrimeGenerator:
    """Generate primes using the wave interference formula."""
    
    def __init__(self):
        """Initialize with minimal context primes."""
        self.context_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        self.context_set = set(self.context_primes)
        print(f"🌊 Simple Prime Generator initialized with {len(self.context_primes)} context primes")
    
    def wave_function(self, n):
        """
        Calculate W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p
        
        Returns the wave amplitude at n.
        If W(n) > 0, then n has prime factors in our context set.
        """
        amplitude = 0.0
        
        for p in self.context_primes:
            if n % p == 0:  # [n ≡ 0 (mod p)] = 1 if true, 0 if false
                amplitude += 1.0 / math.sqrt(p)
        
        return amplitude
    
    def is_prime_by_wave(self, n):
        """
        Determine if n is prime using the wave function.
        
        Algorithm:
        1. If n < 2: not prime
        2. If n in context_primes: definitely prime  
        3. If W(n) > 0: n is composite (has factors in context)
        4. If W(n) = 0: n might be prime (no small factors detected)
        5. For numbers beyond our context, use trial division up to √n
        """
        if n < 2:
            return False
        
        # If n is in our context primes, it's definitely prime
        if n in self.context_set:
            return True
        
        # Apply wave function
        wave_amplitude = self.wave_function(n)
        
        # If wave detects interference (amplitude > 0), n is composite
        if wave_amplitude > 0:
            return False
        
        # Wave detected no interference, but we need to check beyond our context
        # Use trial division for factors larger than our largest context prime
        max_context = max(self.context_primes)
        
        # Check for factors from max_context+1 up to √n
        sqrt_n = int(math.sqrt(n)) + 1
        for factor in range(max_context + 1, sqrt_n + 1):
            if n % factor == 0:
                return False
        
        # No factors found - it's prime!
        return True
    
    def generate_n_primes(self, n):
        """
        Generate the first n prime numbers using the wave formula.
        
        Args:
            n (int): Number of primes to generate
            
        Returns:
            list: First n prime numbers
        """
        if n <= 0:
            return []
        
        primes = []
        candidate = 2
        
        print(f"🎯 Generating first {n} primes using wave formula...")
        print(f"📊 Progress:")
        
        while len(primes) < n:
            if self.is_prime_by_wave(candidate):
                primes.append(candidate)
                
                # Show progress for larger requests
                if len(primes) % max(1, n // 10) == 0 or len(primes) <= 20:
                    wave_amp = self.wave_function(candidate)
                    print(f"   Prime #{len(primes):3d}: {candidate:6d} (W({candidate}) = {wave_amp:.4f})")
            
            candidate += 1
        
        return primes
    
    def demonstrate_wave_behavior(self, start=10, end=30):
        """Demonstrate how the wave function behaves on different numbers."""
        print(f"\n🌊 Wave Function Demonstration (range {start}-{end}):")
        print(f"{'Number':>6} {'Prime?':>6} {'W(n)':>8} {'Explanation'}")
        print(f"{'-'*6} {'-'*6} {'-'*8} {'-'*20}")
        
        for n in range(start, end + 1):
            is_prime = self.is_prime_by_wave(n)
            wave_val = self.wave_function(n)
            
            if is_prime:
                explanation = "Prime (W=0, no factors)"
            elif wave_val > 0:
                explanation = f"Composite (W>0, has factors)"
            else:
                explanation = "Composite (factors beyond context)"
            
            print(f"{n:6d} {str(is_prime):>6} {wave_val:8.4f} {explanation}")


def main():
    """Main demonstration of the prime generator."""
    
    print("="*70)
    print("🚀 SIMPLE PRIME GENERATOR USING WAVE FORMULA")
    print("="*70)
    
    generator = SimplePrimeGenerator()
    
    # Show the mathematical formula
    print(f"\n📐 Mathematical Formula:")
    print(f"   W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p")
    print(f"   where P = {generator.context_primes}")
    print(f"   [condition] = 1 if true, 0 if false")
    
    # Demonstrate wave behavior
    generator.demonstrate_wave_behavior(10, 25)
    
    # Generate first 20 primes
    print(f"\n" + "="*70)
    first_20_primes = generator.generate_n_primes(20)
    
    print(f"\n✨ RESULTS:")
    print(f"First 20 primes: {first_20_primes}")
    
    # Verify correctness
    expected_20_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
    
    if first_20_primes == expected_20_primes:
        print(f"✅ Perfect match with known first 20 primes!")
    else:
        print(f"❌ Mismatch detected!")
        print(f"Expected: {expected_20_primes}")
        print(f"Got:      {first_20_primes}")
    
    # Generate more primes
    print(f"\n" + "="*70)
    num_primes = int(input("How many primes would you like to generate? (e.g., 50): ") or "50")
    
    primes = generator.generate_n_primes(num_primes)
    
    print(f"\n🎉 Generated {len(primes)} primes:")
    print(f"Range: {primes[0]} to {primes[-1]}")
    
    # Show in groups of 10
    for i in range(0, len(primes), 10):
        group = primes[i:i+10]
        print(f"Primes {i+1:3d}-{min(i+10, len(primes)):3d}: {group}")
    
    print(f"\n🌊 Wave interference successfully generated all primes! 🌊")


if __name__ == "__main__":
    main()
