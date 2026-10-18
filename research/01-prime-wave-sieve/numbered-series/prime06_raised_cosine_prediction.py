# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/numbered-series/prime06_raised_cosine_prediction.py
# Original location      :: learn/prime6.py   (last edited 2025-08-01)
# What this script does  :: Raised-cosine interference with a prediction panel.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def sieve_for_primes_up_to(n):
    """
    Generates a list of prime numbers up to a given number n using the Sieve of Eratosthenes.
    This is an efficient way to get the primes we need for our waves.
    """
    # Ensure n is an integer for list indexing
    n = int(n)
    primes = [True] * (n + 1)
    if n >= 0:
        primes[0] = False
    if n >= 1:
        primes[1] = False
        
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            for multiple in range(i*i, n + 1, i):
                primes[multiple] = False
    
    prime_numbers = [i for i, is_prime in enumerate(primes) if is_prime]
    return prime_numbers

def visualize_prime_interference(max_number, resolution=200, prediction_threshold=0.15):
    """
    Generates and plots a wave interference pattern to predict prime numbers.

    This version uses true wave mechanics, where primes are predicted at the 
    zero-crossings of the interference pattern.

    Args:
        max_number (int): The upper limit of numbers to visualize.
        resolution (int): The number of points to compute per integer for a smooth curve.
        prediction_threshold (float): The tolerance around zero to predict a prime.
    """
    print("Starting visualization based on wave mechanics...")
    
    # --- Step 1: Find primes to generate the marking waves ---
    # We only need primes up to sqrt(N) to identify all composites up to N.
    wave_generating_primes = sieve_for_primes_up_to(np.sqrt(max_number))
    if not wave_generating_primes:
        print(f"No primes found up to {int(np.sqrt(max_number))}. Increase max_number.")
        return
    print(f"Using primes {wave_generating_primes} to generate interference pattern.")

    # --- Step 2: Create the continuous space and the final wave ---
    x = np.linspace(1, max_number, max_number * resolution)
    y = np.zeros_like(x) # This will be our final interference wave

    # --- Step 3: Create and sum the marking waves ---
    # Each prime `p` generates a wave: cos(2 * pi * x / p).
    # This wave oscillates between -1 and 1.
    # At every multiple of p, the wave is at a peak of +1.
    for p in wave_generating_primes:
        marking_wave = np.cos(2 * np.pi * x / p)
        y += marking_wave
        
    print("Interference pattern calculated.")

    # --- Step 4: Predict primes based on zero-crossings ---
    predicted_primes = []
    # We check each integer in our range
    for n in range(2, max_number + 1):
        # Calculate the wave's amplitude *exactly* at the integer `n`
        y_at_n = 0
        for p in wave_generating_primes:
            y_at_n += np.cos(2 * np.pi * n / p)
        
        # If the absolute amplitude is very close to zero, it's a "quiet spot"
        if abs(y_at_n) < prediction_threshold:
            predicted_primes.append(n)
            
    print(f"Predicted Primes (amplitude < {prediction_threshold}): {predicted_primes}")

    # --- Step 5: Get actual primes for comparison ---
    actual_primes = sieve_for_primes_up_to(max_number)
    print(f"Actual Primes: {actual_primes}")

    # --- Step 6: Plot the results in two subplots ---
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12), sharex=True)
    fig.suptitle('Prime Number Prediction via Wave Mechanics', fontsize=22, y=0.96)

    # --- Top Plot: The Interference Pattern ---
    ax1.plot(x, y, color='dodgerblue', linewidth=1.5, label='Interference Wave')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax1.axhline(y=prediction_threshold, color='red', linestyle='--', linewidth=1, label=f'Zero-Crossing Threshold (±{prediction_threshold})')
    ax1.axhline(y=-prediction_threshold, color='red', linestyle='--', linewidth=1)
    ax1.set_title('Interference Pattern of Prime Waves', fontsize=16)
    ax1.set_ylabel('Wave Amplitude', fontsize=12)
    ax1.legend()

    # --- Bottom Plot: Predictions vs. Reality ---
    ax2.plot(x, y, color='dodgerblue', linewidth=1.5, alpha=0.4) # Faded wave in background
    # Plot actual primes as solid green lines
    for p in actual_primes:
        ax2.axvline(x=p, color='forestgreen', linestyle='-', linewidth=1.5, label='Actual Prime' if p==actual_primes[0] else "")
    # Plot predicted primes as red dots
    ax2.plot(predicted_primes, [0]*len(predicted_primes), 'o', color='red', markersize=8, 
             markeredgecolor='black', label='Predicted Prime')
    
    ax2.set_title('Prime Predictions vs. Reality', fontsize=16)
    ax2.set_xlabel('Number', fontsize=12)
    ax2.set_ylabel('Wave Amplitude', fontsize=12)
    ax2.set_xlim(1, max_number)
    ax2.legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95]) # Adjust layout to make room for suptitle
    print("Plot generated. Displaying now.")
    plt.show()

# --- Main execution ---
if __name__ == '__main__':
    UPPER_LIMIT = 150
    # You can adjust this threshold. A smaller value is more strict.
    PREDICTION_THRESHOLD = 0.2 
    visualize_prime_interference(UPPER_LIMIT, prediction_threshold=PREDICTION_THRESHOLD)
