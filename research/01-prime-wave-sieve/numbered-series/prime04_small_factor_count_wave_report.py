# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime04_small_factor_count_wave_report.py
# Original location      :: learn/prime4.py   (last edited 2025-08-01)
# What this script does  :: Same as prime03 plus a printed comparison of predicted and actual primes.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

# --- Core Logic: The Prime Factor Counter ---

# First, get a list of primes to use as potential factors
def get_primes_up_to(n):
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i::i] = False
    return np.where(primes)[0]

# Pre-calculate primes up to the sqrt of our max number
# This is an optimization so we don't recalculate them every time.
MAX_NUMBER = 200000
PRIMES_TO_TEST = get_primes_up_to(int(np.sqrt(MAX_NUMBER)) + 1)

def count_small_prime_factors(n):
    """Counts the number of unique prime factors of n that are <= sqrt(n)."""
    count = 0
    for p in PRIMES_TO_TEST:
        # Optimization: no need to check primes larger than sqrt(n)
        if p * p > n:
            break
        if n % p == 0:
            count += 1
    return count

# --- Data Generation ---
START_NUMBER = 100000
numbers = np.arange(START_NUMBER, MAX_NUMBER + 1)
amplitudes = [count_small_prime_factors(n) for n in numbers]

# --- Visualization ---
plt.style.use('seaborn-v0_8-darkgrid')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), sharex=True, sharey=True)
fig.tight_layout(pad=4.0)

# --- Top Plot: The Interference Pattern ---
ax1.plot(numbers, amplitudes, drawstyle='steps-post', label='Interference Pattern')
ax1.axhline(y=0.5, color='r', linestyle='--', label='Quiet Zone Threshold')
ax1.set_title('Prime Wave Interference Pattern', fontsize=14)
ax1.set_ylabel('Wave Amplitude', fontsize=12)
ax1.legend()

# --- Bottom Plot: Predictions vs Reality ---
ax2.plot(numbers, amplitudes, drawstyle='steps-post')

# Find actual primes in the range
all_primes_up_to_max = get_primes_up_to(MAX_NUMBER)
actual_primes_in_range = [p for p in all_primes_up_to_max if p >= START_NUMBER]

# Plot actual primes as green vertical lines
for p in actual_primes_in_range:
    ax2.axvline(x=p, color='g', linestyle='-', linewidth=1.5, alpha=0.8, label='Actual Prime' if p == actual_primes_in_range[0] else "")

# Identify and plot predicted primes (where amplitude is 0)
predicted_primes = numbers[np.array(amplitudes) == 0]
ax2.plot(predicted_primes, np.zeros_like(predicted_primes), 'ro', markersize=6, label='Predicted Prime')

# Print predicted primes and actual primes
print("Predicted Primes:", predicted_primes)
print("Actual Primes:", actual_primes_in_range)

# Print comparison result
predicted_set = set(predicted_primes)
actual_set = set(actual_primes_in_range)
intersection = predicted_set & actual_set
missed = actual_set - predicted_set
false_positives = predicted_set - actual_set
print(f"\nSummary:")
print(f"Total predicted primes: {len(predicted_primes)}")
print(f"Total actual primes: {len(actual_primes_in_range)}")
print(f"Correct predictions (intersection): {len(intersection)}")
print(f"Missed actual primes: {len(missed)}")
print(f"False positives: {len(false_positives)}")

ax2.set_title('Prime Predictions vs Reality', fontsize=14)
ax2.set_xlabel('Number', fontsize=12)
ax2.set_ylabel('Wave Amplitude', fontsize=12)
ax2.legend()

plt.show()