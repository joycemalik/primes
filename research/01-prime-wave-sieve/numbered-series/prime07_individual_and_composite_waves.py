# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime07_individual_and_composite_waves.py
# Original location      :: learn/prime7.py   (last edited 2025-08-01)
# What this script does  :: Plots each prime wave and the combined interference pattern.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime_wave(prime, x_range, amplitude=1, wavelength_factor=1):
    """Generate a wave for a prime number that peaks at its multiples"""
    x = np.linspace(0, x_range, x_range * 10)
    # Create a wave that has peaks at multiples of the prime
    # Using sine wave with frequency adjusted to peak at multiples
    wave = amplitude * np.sin(2 * np.pi * x / prime) * np.exp(-0.01 * x / prime)
    return x, wave

def create_composite_wave(primes, x_range, amplitudes=None):
    """Create composite wave from multiple prime waves"""
    if amplitudes is None:
        amplitudes = [1] * len(primes)
    
    x = np.linspace(0, x_range, x_range * 10)
    composite = np.zeros_like(x)
    
    individual_waves = {}
    
    for i, prime in enumerate(primes):
        # Create wave that peaks at multiples of prime
        wave = amplitudes[i] * np.sin(2 * np.pi * x / prime) * np.exp(-0.005 * x / prime)
        individual_waves[prime] = wave
        composite += wave
    
    return x, composite, individual_waves

def plot_prime_wave_interference():
    """Main plotting function for prime wave interference"""
    # Parameters
    x_range = 50
    primes = [2, 3, 5, 7]  # Prime context window
    
    # Create the plot
    fig, axes = plt.subplots(3, 1, figsize=(15, 12))
    
    # Plot 1: Individual prime waves
    x, composite, individual_waves = create_composite_wave(primes, x_range)
    
    colors = ['red', 'blue', 'green', 'orange']
    for i, prime in enumerate(primes):
        axes[0].plot(x, individual_waves[prime], 
                    color=colors[i], alpha=0.7, 
                    label=f'Prime {prime} wave', linewidth=1.5)
        
        # Mark the multiples (peaks)
        multiples = np.arange(prime, x_range + 1, prime)
        for mult in multiples:
            if mult <= x_range:
                mult_idx = int(mult * 10)
                if mult_idx < len(x):
                    axes[0].axvline(x=mult, color=colors[i], 
                                  alpha=0.3, linestyle='--', linewidth=0.8)
    
    axes[0].set_title('Individual Prime Waves (Each peaks at its multiples)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Number')
    axes[0].set_ylabel('Amplitude')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Composite wave (interference pattern)
    axes[1].plot(x, composite, 'purple', linewidth=2, label='Composite Wave (Superposition)')
    axes[1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Highlight peaks and troughs
    peaks_idx = []
    troughs_idx = []
    for i in range(1, len(composite)-1):
        if composite[i] > composite[i-1] and composite[i] > composite[i+1]:
            peaks_idx.append(i)
        elif composite[i] < composite[i-1] and composite[i] < composite[i+1]:
            troughs_idx.append(i)
    
    # Mark significant peaks and troughs
    if peaks_idx:
        peak_x = x[peaks_idx]
        peak_y = composite[peaks_idx]
        axes[1].scatter(peak_x, peak_y, color='red', s=30, alpha=0.7, label='Peaks (Constructive Interference)')
    
    if troughs_idx:
        trough_x = x[troughs_idx]
        trough_y = composite[troughs_idx]
        axes[1].scatter(trough_x, trough_y, color='blue', s=30, alpha=0.7, label='Troughs (Destructive Interference)')
    
    axes[1].set_title('Composite Prime Wave (Interference Pattern)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Number')
    axes[1].set_ylabel('Amplitude')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Prime vs Composite analysis
    numbers = np.arange(1, x_range + 1)
    prime_mask = [is_prime(n) for n in numbers]
    composite_mask = [not is_prime(n) and n > 1 for n in numbers]
    
    # Sample the composite wave at integer points
    wave_values = []
    for n in numbers:
        idx = int(n * 10) if int(n * 10) < len(composite) else -1
        wave_values.append(composite[idx])
    
    # Plot prime numbers
    prime_numbers = numbers[np.array(prime_mask)]
    prime_values = np.array(wave_values)[np.array(prime_mask)]
    axes[2].scatter(prime_numbers, prime_values, color='green', s=50, 
                   alpha=0.8, label='Prime Numbers', marker='^')
    
    # Plot composite numbers
    composite_numbers = numbers[np.array(composite_mask)]
    composite_values = np.array(wave_values)[np.array(composite_mask)]
    axes[2].scatter(composite_numbers, composite_values, color='red', s=50, 
                   alpha=0.8, label='Composite Numbers', marker='v')
    
    # Plot the wave
    axes[2].plot(x, composite, 'purple', alpha=0.5, linewidth=1)
    axes[2].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    axes[2].set_title('Prime Wave Pattern: Primes vs Composites Analysis)', fontsize=14, fontweight='bold')
    axes[2].set_xlabel('Number')
    axes[2].set_ylabel('Wave Amplitude')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def analyze_prime_pattern(primes, x_range=100):
    """Analyze the relationship between wave amplitude and prime/composite nature"""
    x, composite, _ = create_composite_wave(primes, x_range)
    
    results = {
        'primes': [],
        'composites': [],
        'prime_amplitudes': [],
        'composite_amplitudes': []
    }
    
    for n in range(2, x_range + 1):
        idx = int(n * 10) if int(n * 10) < len(composite) else -1
        amplitude = composite[idx]
        
        if is_prime(n):
            results['primes'].append(n)
            results['prime_amplitudes'].append(amplitude)
        else:
            results['composites'].append(n)
            results['composite_amplitudes'].append(amplitude)
    
    print(f"Analysis for primes {primes}:")
    print(f"Average amplitude at primes: {np.mean(results['prime_amplitudes']):.4f}")
    print(f"Average amplitude at composites: {np.mean(results['composite_amplitudes']):.4f}")
    print(f"Standard deviation at primes: {np.std(results['prime_amplitudes']):.4f}")
    print(f"Standard deviation at composites: {np.std(results['composite_amplitudes']):.4f}")
    
    return results

# Create and display the main plot
if __name__ == "__main__":
    fig = plot_prime_wave_interference()
    plt.show()
    
    # Run analysis
    print("\n" + "="*50)
    analyze_prime_pattern([2, 3, 5, 7], 50)
    
    # Create a second plot with different prime context window
    print("\n" + "="*50)
    print("Creating second analysis with different prime set...")
    
    fig2, axes2 = plt.subplots(2, 1, figsize=(15, 10))
    
    # Compare different prime sets
    prime_sets = [[2, 3], [2, 3, 5], [2, 3, 5, 7], [2, 3, 5, 7, 11]]
    colors = ['red', 'blue', 'green', 'purple']
    
    x_range = 60
    
    for i, primes in enumerate(prime_sets):
        x, composite, _ = create_composite_wave(primes, x_range)
        axes2[0].plot(x, composite, color=colors[i], alpha=0.8, 
                     label=f'Primes: {primes}', linewidth=1.5)
    
    axes2[0].set_title('Comparison of Different Prime Context Windows', fontsize=14, fontweight='bold')
    axes2[0].set_xlabel('Number')
    axes2[0].set_ylabel('Amplitude')
    axes2[0].legend()
    axes2[0].grid(True, alpha=0.3)
    
    # Analyze pattern for the largest prime set
    largest_set = [2, 3, 5, 7, 11]
    x, composite, _ = create_composite_wave(largest_set, x_range)
    
    numbers = np.arange(1, x_range + 1)
    wave_values = []
    for n in numbers:
        idx = int(n * 10) if int(n * 10) < len(composite) else -1
        wave_values.append(composite[idx])
    
    prime_mask = [is_prime(n) for n in numbers]
    composite_mask = [not is_prime(n) and n > 1 for n in numbers]
    
    prime_numbers = numbers[np.array(prime_mask)]
    prime_values = np.array(wave_values)[np.array(prime_mask)]
    axes2[1].scatter(prime_numbers, prime_values, color='green', s=40, 
                    alpha=0.8, label='Prime Numbers', marker='^')
    
    composite_numbers = numbers[np.array(composite_mask)]
    composite_values = np.array(wave_values)[np.array(composite_mask)]
    axes2[1].scatter(composite_numbers, composite_values, color='red', s=40, 
                    alpha=0.8, label='Composite Numbers', marker='v')
    
    axes2[1].plot(x, composite, 'purple', alpha=0.4, linewidth=1)
    axes2[1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    axes2[1].set_title(f'Extended Prime Wave Analysis (Primes: {largest_set})', fontsize=14, fontweight='bold')
    axes2[1].set_xlabel('Number')
    axes2[1].set_ylabel('Wave Amplitude')
    axes2[1].legend()
    axes2[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Analyze the extended pattern
    analyze_prime_pattern(largest_set, x_range)