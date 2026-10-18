# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime05_raised_cosine_interference.py
# Original location      :: learn/prime5.py   (last edited 2025-08-01)
# What this script does  :: Sum of raised cosines (1 + cos 2 pi x / p) / 2 for primes up to sqrt(N).
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def sieve_for_primes_up_to(n):
    """
    Generates a list of prime numbers up to a given number n using the Sieve of Eratosthenes.
    This is an efficient way to get the primes we need for our waves.
    """
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            for multiple in range(i*i, n + 1, i):
                primes[multiple] = False
    
    prime_numbers = [i for i, is_prime in enumerate(primes) if is_prime]
    return prime_numbers

def visualize_prime_interference(max_number, resolution=600):
    """
    Generates and plots the wave interference pattern for prime numbers.

    Args:
        max_number (int): The upper limit of numbers to visualize.
        resolution (int): The number of points to compute per integer for a smooth curve.
    """
    print("Starting visualization...")
    
    # --- Step 1: Find the primes needed to generate the waves ---
    # According to the Sieve of Eratosthenes, we only need to use primes
    # up to the square root of our maximum number to find all primes up to N.
    wave_generating_primes = sieve_for_primes_up_to(int(np.sqrt(max_number)))
    if not wave_generating_primes:
        print("No primes found to generate waves. Increase max_number.")
        return
        
    print(f"Using primes {wave_generating_primes} to generate waves.")

    # --- Step 2: Create the continuous space and the final wave ---
    # We create a high-resolution space `x` to make the plot continuous and smooth.
    x = np.linspace(1, max_number, max_number * resolution)
    
    # This will be our final "interference pattern" wave, initialized to zero.
    y = np.zeros_like(x)

    # --- Step 3: Create and add each "marking wave" ---
    # For each prime, we create a wave and add it to our main `y` wave.
    # The wave is based on a cosine function. We use (1 + cos(...))/2 to make
    # the wave oscillate between 0 and 1. It will be exactly 1 at every
    # multiple of the prime `p`, creating the "peaks" you described.
    for p in wave_generating_primes:
        # This is the "marking wave" for a single prime 'p'.
        # It marks all multiples of p with a peak.
        marking_wave = (1 + np.cos(2 * np.pi * x / p)) / 2
        y += marking_wave
        
    print("Wave interference pattern calculated.")

    # --- Step 4: Find the actual primes in the range for plotting ---
    # We find all primes up to max_number to verify our visualization.
    actual_primes = sieve_for_primes_up_to(max_number)
    
    # Now, we find the y-value of our interference wave at each prime number.
    # According to your theory, these y-values should be very low.
    prime_y_values = np.zeros_like(actual_primes, dtype=float)
    for i, p_val in enumerate(actual_primes):
        # Re-calculate the summed wave value *only* at the integer point of the prime
        y_val_at_prime = 0
        for p_gen in wave_generating_primes:
            y_val_at_prime += (1 + np.cos(2 * np.pi * p_val / p_gen)) / 2
        prime_y_values[i] = y_val_at_prime

    # --- Step 5: Plot the results ---
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot the main interference wave
    ax.plot(x, y, label='Interference Wave (Sum of all marking waves)', color='royalblue', linewidth=2)

    # Plot the actual primes as red dots on the wave
    # This will show that they indeed fall in the "calm zones" (valleys)
    ax.plot(actual_primes, prime_y_values, 'o', color='red', markersize=8, 
            markeredgecolor='black', label=f'Actual Prime Numbers (Total: {len(actual_primes)})')

    # Formatting the plot for clarity
    ax.set_title('Prime Numbers Visualized as Wave Interference', fontsize=20, pad=20)
    ax.set_xlabel('Number (x)', fontsize=14)
    ax.set_ylabel('Interference Amplitude (Composite "Loudness")', fontsize=14)
    ax.legend(fontsize=12)
    ax.set_xlim(1, max_number)
    
    # Adding a threshold line to visually separate primes from composites
    # Primes will generally fall below this line.
    ax.axhline(y=0.5, color='green', linestyle='--', linewidth=1.5, label='Potential Prime Threshold')

    plt.tight_layout()
    print("Plot generated. Displaying now.")
    plt.show()


# --- Main execution ---
if __name__ == '__main__':
    # You can change this number to see the pattern over a larger range.
    # Ranges between 50 and 200 are great for visualization.
    UPPER_LIMIT = 1000
    visualize_prime_interference(UPPER_LIMIT)
