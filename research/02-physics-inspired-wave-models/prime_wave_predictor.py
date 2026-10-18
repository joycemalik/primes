# ----------------------------------------------------------------------------
# Prime research archive :: research/02-physics-inspired-wave-models/prime_wave_predictor.py
# Original location      :: learn/prime_wave_predictor.py   (last edited 2025-08-02)
# What this script does  :: Wave predictor with correction analysis.
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
# Use limited primes to create the wave function
training_limit = 100  # Only use primes up to 100
prediction_limit = 1000  # Predict primes up to 1000

# --- 1. Generate Training Data ---
training_primes = prime_sieve(training_limit)
print(f"Training with {len(training_primes)} primes up to {training_limit}")

# Create continuous range for wave analysis
x_continuous = np.linspace(1, prediction_limit, 10000)

# --- 2. Create Continuous Wave Function ---
# Each prime contributes a sinusoidal wave with its characteristic frequency
prime_wave_function = np.zeros_like(x_continuous)

for prime in training_primes:
    # Each prime creates a wave with frequency 1/prime
    # This creates interference patterns that should reveal prime locations
    frequency = 1.0 / prime
    phase = np.random.uniform(0, 2*np.pi)  # Random phase for each prime
    amplitude = 1.0 / np.sqrt(prime)  # Amplitude decreases with larger primes
    
    # Add the prime's wave contribution
    wave_component = amplitude * np.sin(2 * np.pi * frequency * x_continuous + phase)
    prime_wave_function += wave_component

# --- 3. Find Prediction Points ---
# Look for local minima (valleys) in the wave - these should indicate primes
from scipy.signal import find_peaks

# Invert the signal to find valleys as peaks
inverted_wave = -prime_wave_function

# Find peaks (which are valleys in original signal)
peaks, properties = find_peaks(inverted_wave, 
                              height=None,  # Any height
                              distance=5,   # Minimum distance between peaks
                              prominence=0.1)  # Minimum prominence

# Convert peak indices back to x values
predicted_prime_positions = x_continuous[peaks]

# Round to nearest integers and filter
predicted_primes = np.unique(np.round(predicted_prime_positions).astype(int))
predicted_primes = predicted_primes[predicted_primes > 1]  # Remove 1

# --- 4. Get Actual Primes for Comparison ---
actual_primes = prime_sieve(prediction_limit)

# --- 5. Calculate Metrics ---
predicted_set = set(predicted_primes)
actual_set = set(actual_primes)

true_positives = len(predicted_set & actual_set)
false_positives = len(predicted_set - actual_set)
false_negatives = len(actual_set - predicted_set)

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print(f"\nWave-Based Prime Prediction Results:")
print(f"Training range: 1 to {training_limit}")
print(f"Prediction range: 1 to {prediction_limit}")
print(f"")
print(f"Total actual primes in prediction range: {len(actual_primes)}")
print(f"Total predicted primes: {len(predicted_primes)}")
print(f"")
print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")
print(f"")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall: {recall:.4f} ({recall*100:.2f}%)")
print(f"F1-Score: {2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0:.4f}")

# --- 6. Visualization ---
plt.figure(figsize=(20, 12))

# Plot 1: The continuous wave function
plt.subplot(2, 1, 1)
plt.plot(x_continuous, prime_wave_function, 'b-', alpha=0.7, linewidth=1)
plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)

# Mark actual primes in training range
training_actual = [p for p in actual_primes if p <= training_limit]
for p in training_actual:
    plt.axvline(x=p, color='green', alpha=0.6, linewidth=2)

# Mark predicted primes beyond training range
beyond_training = [p for p in predicted_primes if p > training_limit]
for p in beyond_training:
    plt.axvline(x=p, color='red', alpha=0.6, linewidth=1, linestyle='--')

plt.title('Continuous Prime Wave Function (Green=Training Primes, Red=Predictions)')
plt.xlabel('Number')
plt.ylabel('Wave Amplitude')
plt.grid(True, alpha=0.3)
plt.xlim(1, prediction_limit)

# Plot 2: Zoomed view of prediction region
plt.subplot(2, 1, 2)
zoom_start = training_limit
zoom_end = min(300, prediction_limit)
zoom_mask = (x_continuous >= zoom_start) & (x_continuous <= zoom_end)

plt.plot(x_continuous[zoom_mask], prime_wave_function[zoom_mask], 'b-', linewidth=2)
plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)

# Mark actual primes in zoom region
zoom_actual = [p for p in actual_primes if zoom_start <= p <= zoom_end]
zoom_predicted = [p for p in predicted_primes if zoom_start <= p <= zoom_end]

for p in zoom_actual:
    plt.axvline(x=p, color='green', alpha=0.8, linewidth=2, label='Actual Prime' if p == zoom_actual[0] else "")

for p in zoom_predicted:
    if p in zoom_actual:
        plt.axvline(x=p, color='blue', alpha=0.8, linewidth=1, linestyle=':', label='Correct Prediction' if p == [q for q in zoom_predicted if q in zoom_actual][0] else "")
    else:
        plt.axvline(x=p, color='red', alpha=0.8, linewidth=1, linestyle='--', label='False Positive' if p == [q for q in zoom_predicted if q not in zoom_actual][0] else "")

plt.title(f'Prediction Region Detail ({zoom_start}-{zoom_end})')
plt.xlabel('Number')
plt.ylabel('Wave Amplitude')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig('prime_wave_predictor.png', dpi=300, bbox_inches='tight')
plt.show()

# --- 7. Test Specific Predictions ---
print(f"\nSample predictions beyond training range:")
beyond_predictions = [p for p in predicted_primes if p > training_limit][:10]
for p in beyond_predictions:
    is_actually_prime = p in actual_set
    status = "✓ CORRECT" if is_actually_prime else "✗ FALSE POSITIVE"
    print(f"Predicted: {p} -> {status}")
