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
analysis_limit_x = 1000000  # Test prediction far beyond context window

# EXTREMELY LIMITED context window - the ultimate test!
prime_context_limit_p = 50  # Use only primes up to 50 to predict up to 1M!

# --- 1. Generate Primes & Integers ---
# Generate the list of primes that will form our waves
primes = prime_sieve(prime_context_limit_p)

# Create the range of integers to analyze
x = np.arange(1, analysis_limit_x + 1)

# --- 2. Implement True Prime Wave Interference ---
# Your concept: Each prime creates a wave that peaks at the prime AND all its multiples
# When multiple waves interfere, primes should end up at nodes (low amplitude)
# while composites end up at peaks (high amplitude)

wave_function = np.zeros(x.shape, dtype=np.float64)

print(f"Building interference pattern with {len(primes)} primes...")

# Each prime contributes a wave that peaks at its multiples
for p in primes:
    # Create discrete spikes at multiples of p (including p itself)
    for multiple in range(p, analysis_limit_x + 1, p):
        if multiple <= analysis_limit_x:
            idx = multiple - 1  # Convert to 0-based indexing
            
            # Add a spike with amplitude weighted by the prime
            # Smaller primes have larger influence
            amplitude = 1.0 / np.sqrt(p)
            wave_function[idx] += amplitude

print(f"Wave interference pattern created.")

# --- 3. Identify Prime/Composite for Plotting ---
# Find which numbers in our x-range are prime for color-coding the plot
all_primes_up_to_x = prime_sieve(analysis_limit_x)
is_prime_mask = np.isin(x, all_primes_up_to_x)

composites_x = x[~is_prime_mask]
composites_y = wave_function[~is_prime_mask]

primes_x = x[is_prime_mask]
primes_y = wave_function[is_prime_mask]

# --- Calculate Precision and Recall ---
# Use a simple threshold approach since we're getting too many false positives with peak detection
threshold = np.percentile(wave_function[x > 1], 10)  # Bottom 10% are prime candidates
predicted_primes_mask = (wave_function <= threshold) & (x > 1)
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

# --- 4. Plot the Results (showing first 1000 for visualization) ---
plot_limit = min(1000, analysis_limit_x)
plot_mask = x <= plot_limit

plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(20, 8))

# Plot the main wave (first 1000 points for visibility)
plt.plot(x[plot_mask], wave_function[plot_mask], label='Prime Wave Function', color='black', alpha=0.8, linewidth=2, zorder=1)

# Plot composites as red points
comp_mask = (~is_prime_mask) & plot_mask
plt.scatter(x[comp_mask], wave_function[comp_mask], color='red', s=30, label='Composite Numbers', alpha=0.7, zorder=2)

# Plot primes as blue X's
prime_mask = is_prime_mask & plot_mask  
plt.scatter(x[prime_mask], wave_function[prime_mask], color='blue', s=60, marker='X', label='Prime Numbers', zorder=3)

# Show the threshold line
plt.axhline(y=threshold, color='green', linestyle='--', alpha=0.7, label=f'Prime Threshold = {threshold:.3f}')

# Add titles and labels
plt.title(f'Prime Wave Function Pattern (Context: primes ≤ {prime_context_limit_p}, Predicting up to {analysis_limit_x})', fontsize=14)
plt.xlabel('Integer (x)', fontsize=12)
plt.ylabel('Wave Amplitude', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(1, plot_limit)
# Save the plot
plt.savefig('prime_wave_function_pattern.png', dpi=300, bbox_inches='tight')
plt.show()