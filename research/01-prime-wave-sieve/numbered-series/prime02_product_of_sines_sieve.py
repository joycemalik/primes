# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime02_product_of_sines_sieve.py
# Original location      :: learn/prime2.py   (last edited 2025-08-01)
# What this script does  :: Signed product of sines ("sieve of zeroes") with primes marked.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def get_primes_up_to(n):
    """Returns a boolean array where True indicates a prime number."""
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i::i] = False
    return primes

# --- Parameters ---
MAX_NUMBER = 100  # The range of numbers to visualize
WAVE_PRIMES_UP_TO = 7 # Use primes up to 7 (2, 3, 5, 7) to create waves

# --- Step 1: Create Waves and Multiply Them ---

# Get the list of prime numbers to generate waves from
primes_for_waves = np.where(get_primes_up_to(WAVE_PRIMES_UP_TO))[0]
print(f"Multiplying sin() waves from primes: {primes_for_waves}")

# Create a high-resolution, continuous x-axis for a smooth plot
x_continuous = np.linspace(0, MAX_NUMBER, MAX_NUMBER * 100)

# Start with a baseline of 1 to multiply onto
composite_detecting_wave = np.ones_like(x_continuous)

# For each prime, multiply the corresponding sin wave
for p in primes_for_waves:
    # sin(pi * x / p) is zero at every multiple of p
    wave = np.sin(np.pi * x_continuous / p)
    composite_detecting_wave *= wave

# --- Step 2: Plot the Wave and Identify Primes ---

# Get the actual prime numbers for marking on the plot
is_prime_array = get_primes_up_to(MAX_NUMBER)
all_integers = np.arange(2, MAX_NUMBER)
actual_primes = all_integers[is_prime_array[2:MAX_NUMBER]]
actual_composites = all_integers[~is_prime_array[2:MAX_NUMBER]]

# --- Visualization ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(18, 9))

# Plot the continuous "Sieve of Zeroes" wave
ax.plot(x_continuous, composite_detecting_wave, color='purple', label='Composite-Detecting Wave (Product of Sines)')

# --- Mark the Integers on the Wave ---
# Calculate the wave's value at each integer point
integer_values = np.prod([np.sin(np.pi * all_integers / p) for p in primes_for_waves], axis=0)

# Plot Composites: They should land at or very near zero
ax.plot(actual_composites, integer_values[actual_composites-2], 'o', markersize=8, color='gray', label='Composites (Caught by Zeroes)')

# Plot Primes: They "escape" the zeroes with non-zero amplitude
ax.plot(actual_primes, integer_values[actual_primes-2], 'o', markersize=10, markerfacecolor='gold', markeredgecolor='black', label='Primes (Escape the Zeroes)')

# --- Formatting the Plot ---
ax.set_title(f'Finding Primes by Escaping a "Sieve of Zeroes"', fontsize=18, fontweight='bold')
ax.set_xlabel('Integer', fontsize=14)
ax.set_ylabel('Wave Amplitude (Product)', fontsize=14)
ax.set_xlim(1.5, MAX_NUMBER)
ax.axhline(y=0, color='black', linestyle='-', linewidth=1.0) # Emphasize the zero line
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()