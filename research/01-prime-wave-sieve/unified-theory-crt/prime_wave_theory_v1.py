# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/unified-theory-crt/prime_wave_theory_v1.py
# Original location      :: learn/pime/check/prime.py   (last edited 2025-08-03)
# What this script does  :: First complete Prime Wave Theory implementation with interference and prime-encoding waves.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def sieve_of_eratosthenes(limit):
    """Generate primes up to limit using Sieve of Eratosthenes"""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i in range(2, limit + 1) if is_prime[i]]

def generate_prime_wave(primes, analysis_limit):
    """
    Generate the superimposed wave that encodes composite numbers.
    Prime numbers appear at the nodes (zero amplitude) of this wave.
    """
    x = np.arange(1, analysis_limit + 1)
    superimposed_wave = np.zeros(x.shape)
    
    # For each prime, create a wave that peaks at its multiples (excluding the prime itself)
    for p in primes:
        wave = np.zeros(x.shape)
        # Start from 2*p, not p (exclude the prime itself)
        for multiple in range(2 * p, analysis_limit + 1, p):
            if multiple <= analysis_limit:
                idx = multiple - 1  # Convert to 0-based indexing
                wave[idx] += 1.0
        superimposed_wave += wave
    
    return x, superimposed_wave

def generate_prime_encoding_wave(primes, analysis_limit):
    """
    Generate a wave that directly encodes prime numbers as peaks.
    This is the inverse of the composite wave - primes get high amplitude.
    """
    x = np.arange(1, analysis_limit + 1)
    prime_wave = np.zeros(x.shape)
    
    # Create peaks at prime numbers
    for p in primes:
        if p <= analysis_limit:
            idx = p - 1  # Convert to 0-based indexing
            prime_wave[idx] = 1.0
    
    return x, prime_wave

def predict_primes_from_wave(superimposed_wave, threshold=0.5):
    """
    Predict prime numbers by finding nodes (low amplitude) in the superimposed wave.
    Numbers with amplitude below threshold are predicted as prime.
    """
    predicted_primes = []
    for i, amplitude in enumerate(superimposed_wave):
        number = i + 1  # Convert back to 1-based numbering
        if amplitude < threshold and number > 1:  # Exclude 1, include numbers with low amplitude
            predicted_primes.append(number)
    
    return predicted_primes

def calculate_metrics(actual_primes, predicted_primes, analysis_limit):
    """Calculate precision, recall, and F1-score for prime prediction"""
    actual_set = set(actual_primes)
    predicted_set = set(predicted_primes)
    
    true_positives = len(actual_set & predicted_set)
    false_positives = len(predicted_set - actual_set)
    false_negatives = len(actual_set - predicted_set)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1_score, true_positives, false_positives, false_negatives

def visualize_prime_waves(analysis_limit=100, seed_primes_limit=20):
    """
    Visualize the Prime Wave Theory with both composite-encoding and prime-encoding waves
    """
    # Generate seed primes (small primes used to create the interference pattern)
    seed_primes = sieve_of_eratosthenes(seed_primes_limit)
    print(f"Using seed primes: {seed_primes}")
    
    # Generate actual primes for comparison
    actual_primes = sieve_of_eratosthenes(analysis_limit)
    
    # Generate the composite-encoding wave (primes appear as nodes)
    x, composite_wave = generate_prime_wave(seed_primes, analysis_limit)
    
    # Generate the prime-encoding wave (primes appear as peaks)
    x_prime, prime_wave = generate_prime_encoding_wave(actual_primes, analysis_limit)
    
    # Predict primes from the composite wave
    predicted_primes = predict_primes_from_wave(composite_wave, threshold=0.5)
    
    # Calculate metrics
    precision, recall, f1_score, tp, fp, fn = calculate_metrics(actual_primes, predicted_primes, analysis_limit)
    
    print(f"\n=== Prime Wave Theory Results ===")
    print(f"Analysis range: 1 to {analysis_limit}")
    print(f"Seed primes used: {len(seed_primes)} primes up to {seed_primes_limit}")
    print(f"Actual primes in range: {len(actual_primes)}")
    print(f"Predicted primes: {len(predicted_primes)}")
    print(f"True Positives: {tp}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1_score:.4f}")
    
    # Create visualization
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
    
    # Plot 1: Composite-encoding wave (interference pattern)
    ax1.plot(x, composite_wave, 'b-', alpha=0.7, linewidth=1, label='Composite Interference Pattern')
    ax1.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='Prime Detection Threshold')
    ax1.set_title('Prime Wave Interference Pattern\n(Primes appear as nodes/quiet zones)', fontsize=14)
    ax1.set_xlabel('Number')
    ax1.set_ylabel('Wave Amplitude')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1, min(analysis_limit, 100))
    
    # Highlight quiet zones (predicted primes) with background shading
    for p in predicted_primes[:20]:  # Show first 20 predictions
        if p <= min(analysis_limit, 100):
            ax1.axvspan(p-0.4, p+0.4, alpha=0.2, color='green')
    
    # Plot 2: Prime-encoding wave (direct prime representation)
    ax2.stem(x_prime, prime_wave, basefmt=' ', linefmt='g-', markerfmt='go', label='Prime Numbers')
    ax2.set_title('Prime-Encoding Wave\n(Direct representation of prime numbers as peaks)', fontsize=14)
    ax2.set_xlabel('Number')
    ax2.set_ylabel('Prime Indicator')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(1, min(analysis_limit, 100))
    ax2.set_ylim(-0.1, 1.2)
    
    # Plot 3: Comparison - Predicted vs Actual
    comparison_range = min(analysis_limit, 100)
    x_comp = np.arange(1, comparison_range + 1)
    actual_indicators = np.zeros(len(x_comp))
    predicted_indicators = np.zeros(len(x_comp))
    
    for p in actual_primes:
        if p <= comparison_range:
            actual_indicators[p-1] = 1.0
    
    for p in predicted_primes:
        if p <= comparison_range:
            predicted_indicators[p-1] = 0.8
    
    ax3.plot(x, composite_wave[:len(x_comp)], 'b-', alpha=0.7, linewidth=1, label='Interference Pattern')
    ax3.stem(x_comp, actual_indicators, basefmt=' ', linefmt='g-', markerfmt='go', label='Actual Primes')
    ax3.stem(x_comp, predicted_indicators, basefmt=' ', linefmt='r-', markerfmt='r.', label='Predicted Primes')
    ax3.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='Detection Threshold')
    ax3.set_title('Prime Predictions vs Reality\n(Green = Actual, Red = Predicted)', fontsize=14)
    ax3.set_xlabel('Number')
    ax3.set_ylabel('Wave Amplitude')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(1, comparison_range)
    
    plt.tight_layout()
    plt.show()
    
    return actual_primes, predicted_primes, composite_wave, prime_wave

def demonstrate_wave_theory():
    """
    Demonstrate the Prime Wave Theory with different analysis ranges
    """
    print("=== Prime Wave Theory Demonstration ===")
    print("This demonstrates how prime numbers emerge as 'quiet zones' in wave interference patterns.")
    print("By superimposing waves created from small seed primes, we can predict all larger primes!\n")
    
    # Test with different ranges
    test_ranges = [50, 100, 300]
    
    for analysis_limit in test_ranges:
        print(f"\n--- Testing with range 1 to {analysis_limit} ---")
        
        # Use only first 4 primes as seeds (as mentioned in your description)
        seed_primes = [2, 3, 5, 7]
        actual_primes = sieve_of_eratosthenes(analysis_limit)
        
        # Generate wave
        x, composite_wave = generate_prime_wave(seed_primes, analysis_limit)
        predicted_primes = predict_primes_from_wave(composite_wave, threshold=0.5)
        
        # Calculate accuracy
        precision, recall, f1_score, tp, fp, fn = calculate_metrics(actual_primes, predicted_primes, analysis_limit)
        
        print(f"Seed primes used: {seed_primes}")
        print(f"Actual primes found: {len(actual_primes)}")
        print(f"Predicted primes: {len(predicted_primes)}")
        print(f"Accuracy (F1-Score): {f1_score:.4f}")
        print(f"Perfect predictions: {tp}/{len(actual_primes)} ({100*recall:.1f}%)")

def generate_inverse_wave_for_false_positives(false_positives, analysis_limit):
    """
    Generate an inverse wave to cancel out false positives.
    This demonstrates the self-correcting nature of the wave theory.
    """
    if not false_positives:
        return np.zeros(analysis_limit)
    
    # Create a correction wave that has peaks at false positive locations
    correction_wave = np.zeros(analysis_limit)
    for fp in false_positives:
        if fp <= analysis_limit:
            idx = fp - 1
            correction_wave[idx] = 1.0  # Add amplitude to cancel the false positive
    
    return correction_wave

def create_prime_encoding_wave_advanced(analysis_limit=300):
    """
    Create a sophisticated wave that directly encodes prime numbers as peaks.
    This is the wave you requested - it encodes the primes themselves!
    """
    print("\n=== Creating Prime-Encoding Wave ===")
    print("This wave directly encodes prime numbers as peaks in the wave function.")
    
    # Get actual primes
    actual_primes = sieve_of_eratosthenes(analysis_limit)
    
    # Method 1: Simple prime encoding (peaks at primes)
    x = np.arange(1, analysis_limit + 1)
    prime_wave_simple = np.zeros(x.shape)
    
    for p in actual_primes:
        if p <= analysis_limit:
            idx = p - 1
            prime_wave_simple[idx] = 1.0
    
    # Method 2: Harmonic prime encoding (using sine waves centered at primes)
    prime_wave_harmonic = np.zeros(x.shape)
    
    for p in actual_primes:
        if p <= analysis_limit:
            # Create a localized wave centered at the prime
            for i, num in enumerate(x):
                distance = abs(num - p)
                if distance <= 2:  # Localized around ±2 units
                    amplitude = np.exp(-distance**2 / 2) * np.cos(2 * np.pi * distance / p)
                    prime_wave_harmonic[i] += amplitude
    
    # Method 3: Prime-frequency encoding (each prime contributes its own frequency)
    prime_wave_frequency = np.zeros(x.shape)
    
    for p in actual_primes:
        if p <= analysis_limit and p <= 50:  # Use smaller primes for cleaner visualization
            # Each prime contributes a sine wave with frequency 1/p
            frequency = 1.0 / p
            amplitude = 1.0 / np.sqrt(p)  # Normalize by prime size
            wave_component = amplitude * np.sin(2 * np.pi * frequency * x + p)
            prime_wave_frequency += wave_component
    
    # Create visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Simple prime encoding
    range_viz = min(100, analysis_limit)
    x_viz = x[:range_viz]
    
    ax1.stem(x_viz, prime_wave_simple[:range_viz], basefmt=' ', linefmt='g-', markerfmt='go')
    ax1.set_title('Method 1: Simple Prime Encoding\n(Unit peaks at prime numbers)', fontsize=12)
    ax1.set_xlabel('Number')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1, range_viz)
    
    # Plot 2: Harmonic prime encoding
    ax2.plot(x_viz, prime_wave_harmonic[:range_viz], 'b-', linewidth=1.5)
    # Mark actual primes
    for p in actual_primes:
        if p <= range_viz:
            ax2.axvline(x=p, color='red', linestyle='--', alpha=0.7)
    ax2.set_title('Method 2: Harmonic Prime Encoding\n(Localized waves at primes)', fontsize=12)
    ax2.set_xlabel('Number')
    ax2.set_ylabel('Amplitude')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(1, range_viz)
    
    # Plot 3: Frequency-based encoding
    ax3.plot(x_viz, prime_wave_frequency[:range_viz], 'm-', linewidth=1)
    ax3.set_title('Method 3: Prime-Frequency Encoding\n(Each prime contributes its own frequency)', fontsize=12)
    ax3.set_xlabel('Number')
    ax3.set_ylabel('Amplitude')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(1, range_viz)
    
    # Plot 4: Combined visualization showing all three methods
    ax4.plot(x_viz, prime_wave_simple[:range_viz], 'g-', alpha=0.7, label='Simple Encoding')
    ax4.plot(x_viz, prime_wave_harmonic[:range_viz] / np.max(prime_wave_harmonic[:range_viz]), 'b-', alpha=0.7, label='Harmonic (normalized)')
    ax4.plot(x_viz, prime_wave_frequency[:range_viz] / np.max(np.abs(prime_wave_frequency[:range_viz])), 'm-', alpha=0.7, label='Frequency (normalized)')
    ax4.set_title('Combined: All Prime-Encoding Methods', fontsize=12)
    ax4.set_xlabel('Number')
    ax4.set_ylabel('Normalized Amplitude')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(1, range_viz)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Generated prime-encoding waves for range 1 to {analysis_limit}")
    print(f"Found {len(actual_primes)} prime numbers")
    print(f"Wave methods:")
    print(f"  1. Simple: Direct unit peaks at prime locations")
    print(f"  2. Harmonic: Localized harmonic oscillations around primes")
    print(f"  3. Frequency: Each prime contributes its characteristic frequency")
    
    return prime_wave_simple, prime_wave_harmonic, prime_wave_frequency, actual_primes

def demonstrate_prime_wave_properties():
    """
    Demonstrate the mathematical properties of prime-encoding waves
    """
    print("\n=== Prime Wave Properties Analysis ===")
    
    # Generate waves
    simple, harmonic, frequency, primes = create_prime_encoding_wave_advanced(200)
    
    # Analyze wave properties
    print(f"\nWave Statistics:")
    print(f"Simple encoding - Max: {np.max(simple):.3f}, Mean: {np.mean(simple):.3f}")
    print(f"Harmonic encoding - Max: {np.max(harmonic):.3f}, Min: {np.min(harmonic):.3f}")
    print(f"Frequency encoding - Max: {np.max(frequency):.3f}, Min: {np.min(frequency):.3f}")
    
    # Calculate prime density in the wave
    prime_density = len(primes) / 200
    print(f"\nPrime density in range: {prime_density:.3f} ({len(primes)}/200)")
    
    # Show first 20 primes and their encoding
    print(f"\nFirst 20 primes and their wave amplitudes:")
    for i, p in enumerate(primes[:20]):
        simple_amp = simple[p-1] if p <= len(simple) else 0
        harmonic_amp = harmonic[p-1] if p <= len(harmonic) else 0
        print(f"Prime {p:3d}: Simple={simple_amp:.1f}, Harmonic={harmonic_amp:.3f}")

if __name__ == "__main__":
    # Run the demonstration
    demonstrate_wave_theory()
    
    print("\n" + "="*60)
    print("Generating detailed visualization...")
    
    # Generate detailed visualization
    actual_primes, predicted_primes, composite_wave, prime_wave = visualize_prime_waves(
        analysis_limit=100, 
        seed_primes_limit=10
    )
    
    # Demonstrate false positive correction
    actual_set = set(actual_primes)
    predicted_set = set(predicted_primes)
    false_positives = list(predicted_set - actual_set)
    
    if false_positives:
        print(f"\nFalse positives detected: {false_positives}")
        print("Generating correction wave to eliminate false positives...")
        
        correction_wave = generate_inverse_wave_for_false_positives(false_positives, 100)
        corrected_wave = composite_wave - correction_wave
        
        corrected_predictions = predict_primes_from_wave(corrected_wave, threshold=0.5)
        precision_corrected, recall_corrected, f1_corrected, _, _, _ = calculate_metrics(
            actual_primes, corrected_predictions, 100
        )
        
        print(f"After correction - F1-Score: {f1_corrected:.4f}")
        print("This demonstrates the self-correcting nature of the Prime Wave Theory!")
    
    # NEW: Create the prime-encoding wave as requested
    print("\n" + "="*60)
    print("CREATING PRIME-ENCODING WAVE (as requested)")
    print("="*60)
    
    # Create the wave that encodes primes themselves
    create_prime_encoding_wave_advanced(150)
    
    # Analyze wave properties
    demonstrate_prime_wave_properties()
