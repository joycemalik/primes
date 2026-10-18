# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/detectors/graphical_prime_wave.py
# Original location      :: graphical_prime_wave.py   (last edited 2025-08-02)
# What this script does  :: Graphical analysis of W(n) and prime/composite classification.
# ----------------------------------------------------------------------------
"""
Graphical Prime Wave Function Analysis
=====================================

Visual analysis of W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p for large numbers
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from sympy import isprime
import time

class GraphicalPrimeWave:
    """Simplified prime wave with graphical analysis."""
    
    def __init__(self, context_size=100):
        """Initialize with configurable context size."""
        self.context_primes = self._generate_context_primes(context_size)
        print(f"🌊 Initialized with {len(self.context_primes)} context primes (up to {max(self.context_primes)})")
    
    def _generate_context_primes(self, limit):
        """Generate context primes using simple sieve."""
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(limit)) + 1):
            if sieve[i]:
                for j in range(i*i, limit + 1, i):
                    sieve[j] = False
        
        return [i for i, is_prime in enumerate(sieve) if is_prime]
    
    def wave_function(self, n):
        """W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p"""
        if n in self.context_primes:
            return 0.0  # Context primes have zero wave (by definition)
        return sum(1.0 / math.sqrt(p) for p in self.context_primes if n % p == 0)
    
    def is_prime_fast(self, n):
        """Fast prime check using wave + trial division."""
        if n < 2:
            return False
        if n in self.context_primes:
            return True
        if self.wave_function(n) > 0:
            return False
        
        # Check beyond context
        max_context = max(self.context_primes)
        for i in range(max_context + 1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def analyze_range(self, start, end, step=1):
        """Analyze wave function over a range of numbers."""
        numbers = list(range(start, end + 1, step))
        wave_values = []
        prime_status = []
        
        print(f"🔍 Analyzing range [{start:,}, {end:,}] with step {step}")
        
        start_time = time.time()
        for n in numbers:
            wave_val = self.wave_function(n)
            is_prime = self.is_prime_fast(n)
            
            wave_values.append(wave_val)
            prime_status.append(is_prime)
        
        analysis_time = time.time() - start_time
        print(f"⚡ Analysis completed in {analysis_time:.2f}s ({len(numbers)/analysis_time:,.0f} nums/sec)")
        
        return numbers, wave_values, prime_status
    
    def plot_wave_function(self, start, end, step=1, title_suffix=""):
        """Create a comprehensive wave function plot."""
        numbers, wave_values, prime_status = self.analyze_range(start, end, step)
        
        # Separate primes and composites
        primes = [n for n, is_p in zip(numbers, prime_status) if is_p]
        prime_waves = [w for w, is_p in zip(wave_values, prime_status) if is_p]
        
        composites = [n for n, is_p in zip(numbers, prime_status) if not is_p]
        composite_waves = [w for w, is_p in zip(wave_values, prime_status) if not is_p]
        
        # Create the plot
        plt.figure(figsize=(15, 10))
        
        # Main wave function plot
        plt.subplot(2, 2, 1)
        plt.plot(numbers, wave_values, 'b-', alpha=0.7, linewidth=0.8, label='Wave Function W(n)')
        plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        plt.xlabel('Number (n)')
        plt.ylabel('Wave Amplitude W(n)')
        plt.title(f'Prime Wave Function W(n) = Σ[n≡0(mod p)]/√p\nRange: [{start:,}, {end:,}]{title_suffix}')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Scatter plot: Primes vs Composites
        plt.subplot(2, 2, 2)
        if primes:
            plt.scatter(primes, prime_waves, c='green', s=20, alpha=0.7, label=f'Primes ({len(primes)})')
        if composites:
            plt.scatter(composites, composite_waves, c='red', s=10, alpha=0.5, label=f'Composites ({len(composites)})')
        plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        plt.xlabel('Number (n)')
        plt.ylabel('Wave Amplitude W(n)')
        plt.title('Prime vs Composite Classification')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Wave amplitude histogram
        plt.subplot(2, 2, 3)
        non_zero_waves = [w for w in wave_values if w > 0]
        if non_zero_waves:
            plt.hist(non_zero_waves, bins=50, alpha=0.7, edgecolor='black')
            plt.xlabel('Wave Amplitude')
            plt.ylabel('Frequency')
            plt.title('Distribution of Non-Zero Wave Amplitudes')
            plt.grid(True, alpha=0.3)
        
        # Prime density
        plt.subplot(2, 2, 4)
        window_size = max(1, (end - start) // 50)
        density_points = []
        density_values = []
        
        for i in range(start, end - window_size, window_size):
            window_primes = sum(1 for n in range(i, i + window_size) if n in primes)
            density = window_primes / window_size
            density_points.append(i + window_size // 2)
            density_values.append(density)
        
        if density_points:
            plt.plot(density_points, density_values, 'purple', linewidth=2)
            plt.xlabel('Number (n)')
            plt.ylabel('Prime Density')
            plt.title(f'Local Prime Density (window size: {window_size})')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Print statistics
        prime_count = len(primes)
        total_count = len(numbers)
        
        print(f"\n📊 ANALYSIS RESULTS:")
        print(f"   Range: [{start:,}, {end:,}] (step: {step})")
        print(f"   Total numbers analyzed: {total_count:,}")
        print(f"   Primes found: {prime_count:,} ({prime_count/total_count*100:.2f}%)")
        print(f"   Context primes: {len(self.context_primes)} (up to {max(self.context_primes)})")
        
        if non_zero_waves:
            print(f"   Wave amplitude range: {min(non_zero_waves):.4f} to {max(non_zero_waves):.4f}")
            print(f"   Average composite wave: {np.mean(non_zero_waves):.4f}")
        
        return numbers, wave_values, prime_status
    
    def compare_with_sympy(self, start, end, sample_size=1000):
        """Compare wave function results with SymPy for validation."""
        import random
        
        # Sample random numbers from the range
        if end - start < sample_size:
            test_numbers = list(range(start, end + 1))
        else:
            test_numbers = random.sample(range(start, end + 1), sample_size)
        
        print(f"🔬 Validating {len(test_numbers)} numbers against SymPy...")
        
        errors = []
        start_time = time.time()
        
        for n in test_numbers:
            wave_result = self.is_prime_fast(n)
            sympy_result = isprime(n)
            
            if wave_result != sympy_result:
                errors.append((n, wave_result, sympy_result))
        
        validation_time = time.time() - start_time
        
        if errors:
            print(f"❌ {len(errors)} mismatches found:")
            for n, wave, sympy in errors[:5]:
                print(f"   {n}: Wave={wave}, SymPy={sympy}")
        else:
            print(f"✅ Perfect validation! ({len(test_numbers)}/{ len(test_numbers)} correct)")
        
        print(f"⚡ Validation speed: {len(test_numbers)/validation_time:,.0f} comparisons/sec")
        return len(errors) == 0


def main():
    """Interactive graphical analysis."""
    
    print("="*80)
    print("🌊 GRAPHICAL PRIME WAVE FUNCTION ANALYSIS")
    print("="*80)
    
    # Initialize with larger context for better accuracy on large numbers
    analyzer = GraphicalPrimeWave(context_size=1000)
    
    while True:
        print(f"\n📊 ANALYSIS OPTIONS:")
        print(f"1. Small range (detailed view)")
        print(f"2. Medium range (1,000s)")
        print(f"3. Large range (10,000s)")
        print(f"4. Very large range (100,000s+)")
        print(f"5. Custom range")
        print(f"6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            # Small range - detailed
            start, end, step = 100, 200, 1
            analyzer.plot_wave_function(start, end, step, " - Detailed View")
            
        elif choice == '2':
            # Medium range
            start, end, step = 1000, 2000, 1
            analyzer.plot_wave_function(start, end, step, " - Medium Range")
            
        elif choice == '3':
            # Large range
            start, end, step = 10000, 20000, 1
            analyzer.plot_wave_function(start, end, step, " - Large Range")
            
        elif choice == '4':
            # Very large range (with sampling)
            start, end, step = 100000, 200000, 10
            analyzer.plot_wave_function(start, end, step, " - Very Large Range (sampled)")
            
        elif choice == '5':
            # Custom range
            try:
                start = int(input("Start number: "))
                end = int(input("End number: "))
                step = int(input("Step size (1 for full analysis): ") or "1")
                analyzer.plot_wave_function(start, end, step, " - Custom Range")
            except ValueError:
                print("Invalid input. Please enter integers.")
                continue
                
        elif choice == '6':
            print("👋 Goodbye!")
            break
            
        else:
            print("Invalid choice. Please select 1-6.")
            continue
        
        # Offer validation
        validate = input("\nValidate against SymPy? (y/N): ").strip().lower()
        if validate == 'y':
            # Use the same range as the plot
            if 'start' in locals() and 'end' in locals():
                analyzer.compare_with_sympy(start, end, min(1000, end - start))


if __name__ == "__main__":
    main()
