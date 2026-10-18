# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime09_spike_superposition.py
# Original location      :: learn/prime9.py   (last edited 2025-08-03)
# What this script does  :: Spike superposition: each context prime adds a spike at its multiples.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def prime_sieve(n):
    """Generates primes up to n using the Sieve of Eratosthenes."""
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i:n+1:i] = False
    return np.where(primes)[0]

# --- Parameters ---
# The upper limit of integers to analyze (the x-axis)
analysis_limit_x = 100

# For accurate prime detection, we need ALL primes up to sqrt(analysis_limit_x)
# This ensures no prime beyond our context window can be a false positive
prime_context_limit_p = int(np.sqrt(analysis_limit_x)) + 1

# --- 1. Generate Primes & Integers ---
# Generate the list of primes that will form our waves
primes = prime_sieve(prime_context_limit_p)

# Create the range of integers to analyze
x = np.arange(1, analysis_limit_x + 1)

# --- 2. Create and Superpose Waves ---
# Initialize an array to hold the final superimposed wave
superimposed_wave = np.zeros(x.shape)

# Create each prime wave that peaks at its multiples (composite numbers)
for p in primes:
    # Create a wave that has high amplitude at multiples of p
    # EXCLUDING the prime itself (start from 2*p, not p)
    wave = np.zeros(x.shape)
    for multiple in range(2*p, analysis_limit_x + 1, p):  # Start from 2*p, not p
        if multiple <= analysis_limit_x:
            # Add a peak at each multiple of the prime
            # Using a simple spike model where multiples get +1 amplitude
            idx = multiple - 1  # Convert to 0-based indexing
            wave[idx] += 1.0
    
    superimposed_wave += wave

# --- 3. Identify Prime/Composite for Plotting ---
# Find which numbers in our x-range are prime for color-coding the plot
all_primes_up_to_x = prime_sieve(analysis_limit_x)
is_prime_mask = np.isin(x, all_primes_up_to_x)

composites_x = x[~is_prime_mask]
composites_y = superimposed_wave[~is_prime_mask]

primes_x = x[is_prime_mask]
primes_y = superimposed_wave[is_prime_mask]

# --- Calculate Precision and Recall ---
# Predicted primes are numbers with amplitude 0
predicted_primes_mask = (superimposed_wave == 0)
predicted_primes = x[predicted_primes_mask]

# Actual primes
actual_primes = all_primes_up_to_x

# Convert to sets for easier calculation
predicted_set = set(predicted_primes)
actual_set = set(actual_primes)

# Calculate metrics
true_positives = len(predicted_set & actual_set)  # Correctly predicted primes
false_positives = len(predicted_set - actual_set)  # Incorrectly predicted as prime
false_negatives = len(actual_set - predicted_set)  # Missed actual primes

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print(f"Prime Wave Interference Model Results:")
print(f"Analysis range: 1 to {analysis_limit_x}")
print(f"Prime context window: primes up to {prime_context_limit_p}")
print(f"")
print(f"Total actual primes in range: {len(actual_primes)}")
print(f"Total predicted primes (amplitude = 0): {len(predicted_primes)}")
print(f"")
print(f"True Positives (correctly predicted primes): {true_positives}")
print(f"False Positives (incorrectly predicted as prime): {false_positives}")
print(f"False Negatives (missed actual primes): {false_negatives}")
print(f"")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall: {recall:.4f} ({recall*100:.2f}%)")
print(f"F1-Score: {2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0:.4f}")

# --- 4. Plot the Results ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(20, 8))

# Plot the main wave
plt.plot(x, superimposed_wave, label='Superimposed Prime Wave', color='black', alpha=0.6, zorder=1)

# Plot composites as high-emphasis points (red circles)
plt.scatter(composites_x, composites_y, color='red', s=50, label='Composite Numbers', zorder=2)

# Plot primes as low-emphasis points (blue circles)
plt.scatter(primes_x, primes_y, color='blue', s=80, marker='X', label='Prime Numbers', zorder=3)


# Add titles and labels
plt.title(f'Prime Wave Superposition (Primes up to {prime_context_limit_p})', fontsize=16)
plt.xlabel('Integer (x)', fontsize=12)
plt.ylabel('Wave Amplitude S(x)', fontsize=12)
plt.legend(fontsize=12)
plt.xticks(np.arange(0, analysis_limit_x + 1, 5))
plt.grid(True)
# Save the plot
plt.savefig('prime_wave_interference.png', dpi=300)
plt.show()