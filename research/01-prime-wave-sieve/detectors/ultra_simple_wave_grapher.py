# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/detectors/ultra_simple_wave_grapher.py
# Original location      :: ultra_simple_wave.py   (last edited 2025-08-02)
# What this script does  :: Graphs the wave function over a range and marks detections.
# ----------------------------------------------------------------------------
"""
Ultra-Simple Prime Wave Grapher
==============================

Minimal implementation for analyzing very large numbers
Usage: python ultra_simple_wave.py [start] [end] [step]
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

def sieve_primes(limit):
    """Generate primes up to limit using sieve."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def wave_function(n, context_primes):
    """W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p"""
    return sum(1.0 / math.sqrt(p) for p in context_primes if n % p == 0)

def is_prime_wave(n, context_primes):
    """Fast prime check using wave function."""
    if n < 2:
        return False
    if n in context_primes:
        return True
    if wave_function(n, context_primes) > 0:
        return False
    
    # Check beyond context
    max_context = max(context_primes) if context_primes else 1
    for i in range(max_context + 1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def analyze_and_plot(start, end, step=1, context_size=500):
    """Analyze range and create plots."""
    
    print(f"🌊 Generating {context_size} context primes...")
    context_primes = sieve_primes(context_size)
    context_set = set(context_primes)
    
    print(f"🔍 Analyzing range [{start:,}, {end:,}] with step {step}")
    print(f"📊 Context: {len(context_primes)} primes up to {max(context_primes)}")
    
    numbers = list(range(start, end + 1, step))
    wave_values = []
    prime_status = []
    
    start_time = time.time()
    
    for i, n in enumerate(numbers):
        if i % 10000 == 0 and i > 0:
            elapsed = time.time() - start_time
            rate = i / elapsed
            remaining = (len(numbers) - i) / rate
            print(f"   Progress: {i:,}/{len(numbers):,} ({i/len(numbers)*100:.1f}%) - {rate:,.0f} nums/sec - ETA: {remaining:.1f}s")
        
        wave_val = wave_function(n, context_primes)
        is_prime = is_prime_wave(n, context_primes)
        
        wave_values.append(wave_val)
        prime_status.append(is_prime)
    
    analysis_time = time.time() - start_time
    print(f"⚡ Analysis completed in {analysis_time:.2f}s ({len(numbers)/analysis_time:,.0f} nums/sec)")
    
    # Create plots
    print(f"📈 Creating visualizations...")
    
    # Separate primes and composites
    primes = [n for n, is_p in zip(numbers, prime_status) if is_p]
    prime_waves = [w for w, is_p in zip(wave_values, prime_status) if is_p]
    
    composites = [n for n, is_p in zip(numbers, prime_status) if not is_p]
    composite_waves = [w for w, is_p in zip(wave_values, prime_status) if not is_p]
    
    # Create comprehensive plot
    plt.figure(figsize=(16, 12))
    
    # 1. Main wave function
    plt.subplot(2, 3, 1)
    plt.plot(numbers, wave_values, 'b-', alpha=0.7, linewidth=0.8)
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    plt.xlabel('Number (n)')
    plt.ylabel('Wave Amplitude W(n)')
    plt.title(f'Prime Wave Function\nRange: [{start:,}, {end:,}]')
    plt.grid(True, alpha=0.3)
    
    # 2. Primes vs Composites scatter
    plt.subplot(2, 3, 2)
    if primes:
        plt.scatter(primes, [0]*len(primes), c='green', s=10, alpha=0.8, label=f'Primes ({len(primes)})')
    if composites:
        plt.scatter(composites, composite_waves, c='red', s=5, alpha=0.6, label=f'Composites ({len(composites)})')
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    plt.xlabel('Number (n)')
    plt.ylabel('Wave Amplitude')
    plt.title('Prime Detection via Wave Interference')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 3. Wave amplitude histogram
    plt.subplot(2, 3, 3)
    non_zero_waves = [w for w in wave_values if w > 0]
    if non_zero_waves:
        plt.hist(non_zero_waves, bins=50, alpha=0.7, edgecolor='black', color='red')
        plt.xlabel('Wave Amplitude')
        plt.ylabel('Frequency')
        plt.title('Composite Wave Distribution')
        plt.grid(True, alpha=0.3)
    
    # 4. Prime density
    plt.subplot(2, 3, 4)
    window_size = max(100, (end - start) // 100)
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
        plt.title(f'Prime Density (window: {window_size})')
        plt.grid(True, alpha=0.3)
    
    # 5. Log-scale wave analysis
    plt.subplot(2, 3, 5)
    if non_zero_waves:
        plt.semilogy(composites, composite_waves, 'r.', alpha=0.5, markersize=2)
        plt.xlabel('Number (n)')
        plt.ylabel('Wave Amplitude (log scale)')
        plt.title('Wave Amplitude Distribution (Log Scale)')
        plt.grid(True, alpha=0.3)
    
    # 6. Statistics
    plt.subplot(2, 3, 6)
    plt.axis('off')
    
    stats_text = f"""
ANALYSIS STATISTICS

Range: [{start:,}, {end:,}]
Step: {step}
Total analyzed: {len(numbers):,}

Primes found: {len(primes):,}
Prime density: {len(primes)/len(numbers)*100:.3f}%

Context primes: {len(context_primes)}
Context range: 2 to {max(context_primes)}

Analysis time: {analysis_time:.2f}s
Speed: {len(numbers)/analysis_time:,.0f} nums/sec

Wave statistics:
• Zero waves (primes): {len(prime_waves)}
• Non-zero waves: {len(non_zero_waves)}
• Max wave amplitude: {max(non_zero_waves):.4f if non_zero_waves else 0}
• Avg wave amplitude: {np.mean(non_zero_waves):.4f if non_zero_waves else 0}
"""
    
    plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes, 
             verticalalignment='top', fontfamily='monospace', fontsize=10)
    
    plt.tight_layout()
    
    # Save the plot
    filename = f"prime_wave_analysis_{start}_{end}_step{step}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"💾 Plot saved as: {filename}")
    
    plt.show()
    
    # Print final statistics
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Prime count: {len(primes):,}/{len(numbers):,} ({len(primes)/len(numbers)*100:.3f}%)")
    print(f"   Largest prime: {max(primes) if primes else 'None'}")
    print(f"   Wave range: {min(non_zero_waves):.6f} to {max(non_zero_waves):.6f}" if non_zero_waves else "   No composite waves")


def main():
    """Main function with command line arguments."""
    
    # Default values
    start, end, step = 10000, 20000, 1
    
    # Parse command line arguments
    if len(sys.argv) >= 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    if len(sys.argv) >= 4:
        step = int(sys.argv[3])
    
    print("="*80)
    print("🌊 ULTRA-SIMPLE PRIME WAVE GRAPHER")
    print("="*80)
    print(f"Formula: W(n) = Σ(p∈P) [n ≡ 0 (mod p)] / √p")
    print(f"Usage: python ultra_simple_wave.py [start] [end] [step]")
    print("="*80)
    
    # Adjust context size based on range
    range_size = end - start
    if range_size > 1000000:
        context_size = 10000  # Very large range
    elif range_size > 100000:
        context_size = 5000   # Large range
    elif range_size > 10000:
        context_size = 2000   # Medium range
    else:
        context_size = 1000   # Small range
    
    analyze_and_plot(start, end, step, context_size)


if __name__ == "__main__":
    main()
