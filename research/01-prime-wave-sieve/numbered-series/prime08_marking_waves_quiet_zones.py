# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime08_marking_waves_quiet_zones.py
# Original location      :: learn/prime8.py   (last edited 2025-08-01)
# What this script does  :: Marking waves and "quiet zones" where primes appear.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def create_marking_wave(prime, max_num, resolution=100):
    """Create a wave that marks (peaks at) all multiples of a prime"""
    x = np.linspace(1, max_num, max_num * resolution)
    
    # Create impulses at multiples of the prime (excluding the prime itself)
    wave = np.zeros_like(x)
    
    # Add peaks at each multiple (starting from 2*prime to exclude prime itself)
    for multiple in range(2 * prime, max_num + 1, prime):
        # Create a peak centered at the multiple
        peak_center = multiple
        peak_width = 0.5  # Width of each peak
        
        # Gaussian-like peak at each multiple
        peak_mask = np.abs(x - peak_center) <= peak_width
        if np.any(peak_mask):
            peak_values = np.exp(-((x[peak_mask] - peak_center) / (peak_width/3))**2)
            wave[peak_mask] += peak_values
    
    return x, wave

def create_interference_pattern(primes, max_num, resolution=100):
    """Create the interference pattern by adding all marking waves"""
    x = np.linspace(1, max_num, max_num * resolution)
    total_interference = np.zeros_like(x)
    individual_waves = {}
    
    print(f"Creating marking waves for primes: {primes}")
    
    for prime in primes:
        x_wave, wave = create_marking_wave(prime, max_num, resolution)
        individual_waves[prime] = wave
        total_interference += wave
        print(f"  Prime {prime}: marks multiples {list(range(2*prime, min(max_num+1, 6*prime), prime))}")
    
    return x, total_interference, individual_waves

def find_quiet_zones(x, interference, threshold=0.1):
    """Find the quiet zones (low interference areas) where primes might be"""
    quiet_indices = interference < threshold
    quiet_x = x[quiet_indices]
    
    # Round to nearest integers and remove duplicates
    quiet_numbers = []
    for val in quiet_x:
        rounded = round(val)
        if rounded >= 2 and rounded not in quiet_numbers:
            quiet_numbers.append(rounded)
    
    return sorted(quiet_numbers)

def plot_prime_wave_interference():
    """Main plotting function for the wave-based prime interference"""
    max_num = 30
    primes_to_use = [2, 3, 5]  # Small primes to create marking waves
    
    # Create the interference pattern
    x, total_interference, individual_waves = create_interference_pattern(
        primes_to_use, max_num, resolution=50
    )
    
    # Create the plot
    fig, axes = plt.subplots(4, 1, figsize=(16, 14))
    
    # Plot 1: Individual marking waves
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for i, prime in enumerate(primes_to_use):
        axes[0].plot(x, individual_waves[prime], 
                    color=colors[i], alpha=0.7, 
                    label=f'Prime {prime} marking wave', linewidth=2)
        
        # Mark the multiples being targeted
        multiples = list(range(2 * prime, max_num + 1, prime))
        for mult in multiples:
            axes[0].axvline(x=mult, color=colors[i], 
                          alpha=0.4, linestyle='--', linewidth=1)
            axes[0].text(mult, axes[0].get_ylim()[1] * 0.9, 
                        str(mult), ha='center', va='bottom', 
                        color=colors[i], fontsize=8, rotation=90)
    
    axes[0].set_title('Step 1: Individual Marking Waves (Each marks multiples of its prime)', 
                     fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Number')
    axes[0].set_ylabel('Wave Amplitude')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(1, max_num)
    
    # Plot 2: Total interference pattern
    axes[1].fill_between(x, total_interference, alpha=0.6, color='purple', 
                        label='Total Interference')
    axes[1].plot(x, total_interference, 'purple', linewidth=2)
    
    # Add threshold line for quiet zones
    threshold = np.max(total_interference) * 0.2
    axes[1].axhline(y=threshold, color='orange', linestyle='--', 
                   label=f'Quiet Zone Threshold', linewidth=2)
    
    axes[1].set_title('Step 2: Total Interference Pattern (All waves combined)', 
                     fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Number')
    axes[1].set_ylabel('Interference Level')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(1, max_num)
    
    # Plot 3: Prime detection
    # Get actual primes and composites in range
    numbers = list(range(2, max_num + 1))
    actual_primes = [n for n in numbers if is_prime(n)]
    composites = [n for n in numbers if not is_prime(n)]
    
    # Sample interference at integer points
    interference_at_integers = []
    integer_points = []
    
    for n in numbers:
        # Find closest x value to n
        closest_idx = np.argmin(np.abs(x - n))
        interference_at_integers.append(total_interference[closest_idx])
        integer_points.append(n)
    
    # Plot the interference pattern
    axes[2].fill_between(x, total_interference, alpha=0.3, color='lightgray')
    axes[2].plot(x, total_interference, 'gray', linewidth=1, alpha=0.7)
    
    # Plot primes and composites
    prime_interferences = []
    composite_interferences = []
    
    for i, n in enumerate(integer_points):
        if n in actual_primes:
            prime_interferences.append(interference_at_integers[i])
            axes[2].scatter(n, interference_at_integers[i], 
                           color='green', s=100, marker='^', 
                           edgecolor='darkgreen', linewidth=2, alpha=0.8)
        else:
            composite_interferences.append(interference_at_integers[i])
            axes[2].scatter(n, interference_at_integers[i], 
                           color='red', s=100, marker='v', 
                           edgecolor='darkred', linewidth=2, alpha=0.8)
    
    # Add threshold line
    axes[2].axhline(y=threshold, color='orange', linestyle='--', 
                   linewidth=2, alpha=0.8)
    
    # Add number labels
    for n in range(2, max_num + 1):
        closest_idx = np.argmin(np.abs(x - n))
        y_pos = total_interference[closest_idx]
        axes[2].text(n, y_pos + 0.1, str(n), ha='center', va='bottom', 
                    fontsize=10, fontweight='bold')
    
    axes[2].set_title('Step 3: Prime Detection - Primes in Quiet Zones!', 
                     fontsize=14, fontweight='bold')
    axes[2].set_xlabel('Number')
    axes[2].set_ylabel('Interference Level')
    axes[2].grid(True, alpha=0.3)
    axes[2].set_xlim(1, max_num)
    
    # Create custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='green', 
                   markersize=10, label='Prime Numbers'),
        plt.Line2D([0], [0], marker='v', color='w', markerfacecolor='red', 
                   markersize=10, label='Composite Numbers'),
        plt.Line2D([0], [0], color='orange', linestyle='--', 
                   label='Quiet Zone Threshold')
    ]
    axes[2].legend(handles=legend_elements, loc='upper right')
    
    # Plot 4: Analysis summary
    axes[3].bar(['Average Interference\nat Primes', 'Average Interference\nat Composites'], 
               [np.mean(prime_interferences), np.mean(composite_interferences)],
               color=['green', 'red'], alpha=0.7, width=0.6)
    
    axes[3].set_title('Step 4: Analysis - Do Primes Really Live in Quiet Zones?', 
                     fontsize=14, fontweight='bold')
    axes[3].set_ylabel('Average Interference Level')
    axes[3].grid(True, alpha=0.3)
    
    # Add value labels on bars
    axes[3].text(0, np.mean(prime_interferences) + 0.05, 
                f'{np.mean(prime_interferences):.3f}', 
                ha='center', va='bottom', fontweight='bold')
    axes[3].text(1, np.mean(composite_interferences) + 0.05, 
                f'{np.mean(composite_interferences):.3f}', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Print analysis
    print(f"\n{'='*60}")
    print("WAVE INTERFERENCE PRIME DETECTION ANALYSIS")
    print(f"{'='*60}")
    print(f"Using marking waves from primes: {primes_to_use}")
    print(f"Analyzing numbers 2 to {max_num}")
    print(f"\nActual primes in range: {actual_primes}")
    print(f"Composite numbers in range: {composites}")
    print(f"\nInterference Analysis:")
    print(f"  Average interference at primes: {np.mean(prime_interferences):.4f}")
    print(f"  Average interference at composites: {np.mean(composite_interferences):.4f}")
    print(f"  Ratio (composite/prime): {np.mean(composite_interferences)/np.mean(prime_interferences):.2f}x")
    
    # Check how many primes are in quiet zones
    quiet_numbers = find_quiet_zones(x, total_interference, threshold)
    predicted_primes = [n for n in quiet_numbers if n <= max_num and n >= 2]
    
    print(f"\nQuiet Zone Prediction:")
    print(f"  Numbers in quiet zones: {predicted_primes}")
    print(f"  Actual primes found in quiet zones: {len(set(predicted_primes) & set(actual_primes))}/{len(actual_primes)}")
    print(f"  False positives (quiet but not prime): {set(predicted_primes) - set(actual_primes)}")
    print(f"  Missed primes (prime but not quiet): {set(actual_primes) - set(predicted_primes)}")
    
    return fig

def demonstrate_extended_interference():
    """Demonstrate the interference with more primes for better accuracy"""
    print(f"\n{'='*60}")
    print("EXTENDED WAVE interference DEMONSTRATION")
    print(f"{'='*60}")
    
    max_num = 50
    extended_primes = [2, 3, 5, 7]  # More primes for better sieving
    
    x, total_interference, _ = create_interference_pattern(
        extended_primes, max_num, resolution=20
    )
    
    # Analyze results
    numbers = list(range(2, max_num + 1))
    actual_primes = [n for n in numbers if is_prime(n)]
    
    # Find quiet zones with a lower threshold
    threshold = np.max(total_interference) * 0.15
    quiet_numbers = find_quiet_zones(x, total_interference, threshold)
    predicted_primes = [n for n in quiet_numbers if n <= max_num and n >= 2]
    
    print(f"Using marking waves from primes: {extended_primes}")
    print(f"Analyzing numbers 2 to {max_num}")
    print(f"\nResults:")
    print(f"  Actual primes: {actual_primes}")
    print(f"  Predicted by wave interference: {predicted_primes}")
    print(f"  Accuracy: {len(set(predicted_primes) & set(actual_primes))}/{len(actual_primes)} = {100*len(set(predicted_primes) & set(actual_primes))/len(actual_primes):.1f}%")
    print(f"  False positives: {sorted(set(predicted_primes) - set(actual_primes))}")
    print(f"  Missed primes: {sorted(set(actual_primes) - set(predicted_primes))}")

# Run the demonstration
if __name__ == "__main__":
    # Main visualization
    fig = plot_prime_wave_interference()
    plt.show()
    
    # Extended demonstration
    demonstrate_extended_interference()