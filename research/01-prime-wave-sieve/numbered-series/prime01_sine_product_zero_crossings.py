# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime01_sine_product_zero_crossings.py
# Original location      :: learn/prime1.py   (last edited 2025-08-01)
# What this script does  :: g(x) = |prod sin(pi x / p)| for p in {2,3,5,7}: composites hit zeros, primes escape.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
MAX_NUMBER = 100  # The range of numbers to visualize
# Primes to use for generating the wave function. The more primes we use,
# the more composites will be "cancelled out" to zero.
WAVE_PRIMES = [2, 3, 5, 7]

# --- 1. The Continuous Function ---

# Create a high-resolution x-axis for a smooth, continuous plot
x_continuous = np.linspace(0, MAX_NUMBER, 20000)

# We will multiply sine waves together, so we start with 1.0
g_x = np.ones_like(x_continuous, dtype=float)

# The new logic: g(x) = |sin(πx/2) * sin(πx/3) * sin(πx/5) * ...|
# This function is zero if x is a multiple of any of the WAVE_PRIMES.
for p in WAVE_PRIMES:
    # We take the absolute value of the sine wave to make the peaks easy to see
    g_x *= np.abs(np.sin(np.pi * x_continuous / p))

# --- 2. The Discrete Integers (Where Primes Live) ---

# Sieve of Eratosthenes to find the actual primes (our ground truth)
def get_primes_up_to(n):
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i::i] = False
    return primes

# Get the locations of the actual prime numbers up to MAX_NUMBER
is_prime_array = get_primes_up_to(MAX_NUMBER)
actual_primes = np.where(is_prime_array)[0]

# --- 3. Visualization ---

plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(18, 9))

# Plot the continuous function g(x)
ax.plot(x_continuous, g_x, color='darkviolet', linewidth=2, label='$g(x) = |\\prod_{p} \\sin(\\frac{\\pi x}{p})|$')

# At each integer, calculate the value of g(x) to identify primes vs. composites
integers = np.arange(0, MAX_NUMBER + 1)
g_x_at_integers = np.ones_like(integers, dtype=float)
for p in WAVE_PRIMES:
    g_x_at_integers *= np.abs(np.sin(np.pi * integers / p))

# Mark the primes and composites at their integer locations
# Note: due to floating point precision, we check for values very close to 0
is_composite_at_integer = g_x_at_integers < 1e-9
is_prime_at_integer = ~is_composite_at_integer

# Filter out numbers from our WAVE_PRIMES list itself and 0, 1
is_prime_at_integer[WAVE_PRIMES] = False
is_prime_at_integer[0:2] = False


ax.plot(integers[is_composite_at_integer], g_x_at_integers[is_composite_at_integer], 'o', markersize=8, color='gray', label='Composite Numbers (g(x) ≈ 0)')
ax.plot(integers[is_prime_at_integer], g_x_at_integers[is_prime_at_integer], 'D', markersize=8, color='gold', markeredgecolor='black', label='Prime Numbers (g(x) > 0)')


# --- Formatting the Plot ---
ax.set_title('Visualizing Primes with a Continuous Zero-Crossing Function', fontsize=18, fontweight='bold')
ax.set_xlabel('Integer (x)', fontsize=14)
ax.set_ylabel('Function Value |g(x)|', fontsize=14)
ax.set_xlim(1.5, MAX_NUMBER)
ax.set_ylim(-0.1, 1.2)
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()