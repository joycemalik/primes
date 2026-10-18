# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime10_spike_superposition_excluding_self.py
# Original location      :: learn/prime10.py   (last edited 2025-08-01)
# What this script does  :: Spikes start at 2p so the prime itself stays at 0.
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
analysis_limit_x = 10000

# The upper limit for the 'prime context window'
# (i.e., primes up to this number will be used to generate waves)
prime_context_limit_p = 100

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