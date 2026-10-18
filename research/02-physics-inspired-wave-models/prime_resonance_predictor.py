# ----------------------------------------------------------------------------
# Prime research archive :: research/02-physics-inspired-wave-models/prime_resonance_predictor.py
# Original location      :: learn/prime_resonance_predictor.py   (last edited 2025-08-02)
# What this script does  :: Complex standing waves with harmonics; nodes as prime candidates.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq

def prime_sieve(n):
    """Generates primes up to n using the Sieve of Eratosthenes."""
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i:n+1:i] = False
    return np.where(primes)[0]

# --- Physics-Based Prime Resonance Model ---
# Concept: Each prime creates a "resonant frequency" in number space
# Primes emerge where constructive interference creates standing waves

# --- Parameters ---
training_limit = 30     # Limited training data
prediction_limit = 1000  # Predict much further

print(f"=== Prime Resonance Wave Theory ===")
print(f"Training with primes up to {training_limit}")
print(f"Predicting primes up to {prediction_limit}")

# --- 1. Generate Training Primes ---
training_primes = prime_sieve(training_limit)
print(f"Training primes: {training_primes}")

# --- 2. Create Continuous Space ---
# High resolution for wave analysis
N_points = 10000
x = np.linspace(1, prediction_limit, N_points)
dx = x[1] - x[0]

# --- 3. Prime Resonance Wave Function ---
# Based on quantum harmonic oscillator and standing wave theory

def prime_wave_function(x, primes):
    """
    Creates a wave function where primes generate resonant modes
    Each prime p creates a standing wave with wavelength λ = 2π/ln(p)
    This is inspired by the Prime Number Theorem: π(x) ~ x/ln(x)
    """
    psi = np.zeros_like(x, dtype=complex)
    
    for p in primes:
        # Fundamental frequency based on prime logarithmic density
        omega = 2 * np.pi / np.log(p) if p > 1 else 1
        
        # Phase related to prime index (quantum number)
        phase = np.pi * p / len(primes)
        
        # Amplitude decreases with prime size (like quantum energy levels)
        amplitude = 1.0 / np.sqrt(p)
        
        # Create standing wave: ψ(x) = A * exp(i(kx + φ))
        wave_component = amplitude * np.exp(1j * (omega * x + phase))
        
        # Add harmonic overtones (like musical harmonics)
        for harmonic in range(2, 4):  # 2nd and 3rd harmonics
            harmonic_amp = amplitude / (harmonic ** 1.5)
            harmonic_wave = harmonic_amp * np.exp(1j * (harmonic * omega * x + phase))
            wave_component += harmonic_wave
        
        psi += wave_component
    
    return psi

# Generate the complex wave function
psi = prime_wave_function(x, training_primes)

# --- 4. Quantum-Inspired Observable ---
# In quantum mechanics, |ψ|² gives probability density
probability_density = np.abs(psi) ** 2

# The "prime potential" - where energy wells indicate primes
# Use the imaginary part for phase information
phase_info = np.angle(psi)
amplitude_info = np.abs(psi)

# Create a composite observable that combines amplitude and phase
# Primes should appear at nodes (minima) of this function
prime_observable = amplitude_info * np.cos(phase_info)

# --- 5. Fourier Analysis for Hidden Frequencies ---
# Find hidden periodicities in the prime distribution
fourier_transform = fft(prime_observable)
frequencies = fftfreq(len(prime_observable), dx)

# Identify dominant frequencies
magnitude_spectrum = np.abs(fourier_transform)
dominant_freq_indices = find_peaks(magnitude_spectrum[1:len(magnitude_spectrum)//2], 
                                  height=np.max(magnitude_spectrum) * 0.1)[0] + 1

print(f"Dominant frequencies found: {len(dominant_freq_indices)}")

# --- 6. Resonance-Based Prime Detection ---
# Look for resonance nodes (destructive interference points)
# These should indicate prime locations

# Smooth the signal to find true nodes
from scipy.ndimage import gaussian_filter1d
smoothed_observable = gaussian_filter1d(prime_observable, sigma=2)

# Find local minima (nodes) - these are prime candidates
minima_indices, properties = find_peaks(-smoothed_observable, 
                                       distance=int(0.01 * len(x)),  # Minimum separation
                                       prominence=0.05)  # Minimum depth

# Convert indices back to number positions
predicted_positions = x[minima_indices]
predicted_primes = np.unique(np.round(predicted_positions).astype(int))
predicted_primes = predicted_primes[predicted_primes > 1]

# --- 7. Physics-Based Filtering ---
# Apply physical constraints based on wave theory

# Remove predictions that don't satisfy wave resonance conditions
filtered_predictions = []
for p in predicted_primes:
    # Check if position satisfies resonance condition with training primes
    resonance_score = 0
    for train_p in training_primes:
        # Calculate resonance coupling strength
        coupling = np.exp(-abs(p - train_p) / (train_p * np.log(train_p)))
        resonance_score += coupling
    
    # Only keep predictions with sufficient resonance coupling
    if resonance_score > 0.1:  # Threshold for resonance
        filtered_predictions.append(p)

predicted_primes = np.array(filtered_predictions)

# --- 8. Validation ---
actual_primes = prime_sieve(prediction_limit)
predicted_set = set(predicted_primes)
actual_set = set(actual_primes)

true_positives = len(predicted_set & actual_set)
false_positives = len(predicted_set - actual_set)
false_negatives = len(actual_set - predicted_set)

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print(f"\n=== Quantum Resonance Results ===")
print(f"Total actual primes: {len(actual_primes)}")
print(f"Total predicted primes: {len(predicted_primes)}")
print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall: {recall:.4f} ({recall*100:.2f}%)")
print(f"F1-Score: {2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0:.4f}")

# --- 9. Advanced Visualization ---
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

# Plot 1: Complex wave function (real and imaginary parts)
ax1.plot(x, np.real(psi), 'b-', label='Real part', alpha=0.7)
ax1.plot(x, np.imag(psi), 'r-', label='Imaginary part', alpha=0.7)
ax1.plot(x, np.abs(psi), 'k-', label='|ψ|', linewidth=2)

# Mark training primes
for p in training_primes:
    if p <= prediction_limit:
        ax1.axvline(x=p, color='green', alpha=0.8, linewidth=2)

ax1.set_title('Complex Prime Wave Function ψ(x)')
ax1.set_xlabel('Number')
ax1.set_ylabel('Wave Amplitude')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1, min(200, prediction_limit))

# Plot 2: Prime observable with predictions
ax2.plot(x, prime_observable, 'b-', linewidth=1, alpha=0.7)
ax2.plot(x, smoothed_observable, 'k-', linewidth=2, label='Smoothed Observable')

# Mark actual primes
for p in actual_primes:
    if p <= min(200, prediction_limit):
        color = 'green' if p <= training_limit else 'orange'
        ax2.axvline(x=p, color=color, alpha=0.6, linewidth=1)

# Mark predictions
for p in predicted_primes:
    if p <= min(200, prediction_limit):
        is_correct = p in actual_set
        color = 'blue' if is_correct else 'red'
        style = '-' if is_correct else '--'
        ax2.axvline(x=p, color=color, linestyle=style, alpha=0.8, linewidth=2)

ax2.set_title('Prime Observable & Predictions')
ax2.set_xlabel('Number')
ax2.set_ylabel('Observable Value')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1, min(200, prediction_limit))

# Plot 3: Fourier spectrum
freq_positive = frequencies[1:len(frequencies)//2]
magnitude_positive = magnitude_spectrum[1:len(magnitude_spectrum)//2]

ax3.plot(freq_positive, magnitude_positive, 'b-', linewidth=1)
ax3.scatter(freq_positive[dominant_freq_indices-1], magnitude_positive[dominant_freq_indices-1], 
           color='red', s=100, zorder=5, label='Dominant Frequencies')
ax3.set_title('Fourier Spectrum of Prime Observable')
ax3.set_xlabel('Frequency')
ax3.set_ylabel('Magnitude')
ax3.set_yscale('log')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Prediction accuracy over range
window_size = 50
accuracy_x = []
accuracy_y = []

for start in range(training_limit, prediction_limit - window_size, 10):
    end = start + window_size
    window_actual = [p for p in actual_primes if start <= p < end]
    window_predicted = [p for p in predicted_primes if start <= p < end]
    
    if len(window_actual) > 0:
        window_tp = len(set(window_predicted) & set(window_actual))
        window_precision = window_tp / len(window_predicted) if len(window_predicted) > 0 else 0
        accuracy_x.append(start + window_size // 2)
        accuracy_y.append(window_precision)

ax4.plot(accuracy_x, accuracy_y, 'b-o', linewidth=2, markersize=4)
ax4.axhline(y=precision, color='red', linestyle='--', label=f'Overall Precision: {precision:.3f}')
ax4.set_title('Prediction Accuracy vs Range')
ax4.set_xlabel('Number Range')
ax4.set_ylabel('Local Precision')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('quantum_prime_resonance.png', dpi=300, bbox_inches='tight')
plt.show()

# --- 10. Physical Interpretation ---
print(f"\n=== Physical Interpretation ===")
print(f"Wave resonance model based on:")
print(f"1. Prime Number Theorem: π(x) ~ x/ln(x)")
print(f"2. Quantum harmonic oscillator energy levels")
print(f"3. Standing wave interference patterns")
print(f"4. Fourier analysis of hidden periodicities")
print(f"5. Resonance coupling between primes")

print(f"\nPredictions beyond training range ({training_limit}+):")
beyond_predictions = [p for p in predicted_primes if p > training_limit][:20]
correct_predictions = [p for p in beyond_predictions if p in actual_set]
print(f"Predicted: {beyond_predictions}")
print(f"Correct: {correct_predictions}")
print(f"Success rate: {len(correct_predictions)/len(beyond_predictions)*100:.1f}%" if beyond_predictions else "No predictions")
