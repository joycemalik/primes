# ----------------------------------------------------------------------------
# Prime research archive :: research/02-physics-inspired-wave-models/ultra_simple_prime_wave.py
# Original location      :: learn/ultra_simple_prime_wave.py   (last edited 2025-08-02)
# What this script does  :: Ultra-simple continuous prime wave model.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def prime_sieve(n):
    """Generates primes up to n using the Sieve of Eratosthenes."""
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i:n+1:i] = False
    return np.where(primes)[0]

# --- Ultra-Simple Prime Wave Model ---
print("=== Ultra-Simple Prime Wave Predictor ===")

# Parameters
training_limit = 100
prediction_limit = 500

# Get training primes
training_primes = prime_sieve(training_limit)
print(f"Training primes: {training_primes}")

# --- Core Wave Function ---
def prime_wave_predictor(x, primes):
    """
    Simple wave function that learns from prime patterns
    Each prime creates interference - primes emerge at wave nodes
    """
    wave = np.zeros_like(x, dtype=float)
    
    for p in primes:
        # Each prime contributes a component wave
        # Frequency inversely related to prime size
        omega = 2 * np.pi / (p * np.log(p + 1))
        
        # Phase shift based on prime position
        phase = p * np.pi / len(primes)
        
        # Amplitude decreases with prime size
        amplitude = 1.0 / np.sqrt(p)
        
        # Create the wave component
        wave += amplitude * np.cos(omega * x + phase)
    
    return wave

# --- Generate Predictions ---
x = np.linspace(1, prediction_limit, 5000)  # High resolution
wave_output = prime_wave_predictor(x, training_primes)

# Find wave minima (nodes) - these indicate prime locations
minima_indices, properties = find_peaks(-wave_output, 
                                       distance=10,      # Minimum separation
                                       prominence=0.1)   # Minimum depth

# Convert indices to actual numbers
predicted_positions = x[minima_indices]
predicted_primes = np.unique(np.round(predicted_positions).astype(int))
predicted_primes = predicted_primes[predicted_primes > 1]

# --- Advanced Filtering ---
# Only keep predictions that satisfy wave coherence
filtered_primes = []
for p in predicted_primes:
    # Check wave value at this position
    wave_val = prime_wave_predictor(np.array([p]), training_primes)[0]
    
    # Only accept if wave is truly minimal
    if wave_val < -0.05:  # Threshold for "quiet zone"
        filtered_primes.append(p)

predicted_primes = np.array(filtered_primes)

# --- Validation ---
actual_primes = prime_sieve(prediction_limit)
predicted_set = set(predicted_primes)
actual_set = set(actual_primes)

true_positives = len(predicted_set & actual_set)
false_positives = len(predicted_set - actual_set)
false_negatives = len(actual_set - predicted_set)

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print(f"\n=== Simple Wave Results ===")
print(f"Training range: 1 to {training_limit}")
print(f"Prediction range: 1 to {prediction_limit}")
print(f"Total actual primes: {len(actual_primes)}")
print(f"Total predicted primes: {len(predicted_primes)}")
print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall: {recall:.4f} ({recall*100:.2f}%)")

# --- Elegant Visualization ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))

# Plot 1: The wave function with predictions
ax1.plot(x, wave_output, 'b-', linewidth=1.5, alpha=0.8, label='Prime Wave Function')
ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)

# Mark training primes (green)
for p in training_primes:
    if p <= prediction_limit:
        ax1.axvline(x=p, color='green', alpha=0.7, linewidth=2, label='Training Prime' if p == training_primes[0] else "")

# Mark actual primes beyond training (orange)
beyond_training_actual = [p for p in actual_primes if p > training_limit]
for p in beyond_training_actual[:20]:  # First 20 for clarity
    ax1.axvline(x=p, color='orange', alpha=0.5, linewidth=1, label='Actual Prime' if p == beyond_training_actual[0] else "")

# Mark predicted primes (red dots)
for p in predicted_primes:
    if p <= min(200, prediction_limit):
        is_correct = p in actual_set
        color = 'blue' if is_correct else 'red'
        size = 100 if is_correct else 60
        marker = 'o' if is_correct else 'x'
        ax1.scatter(p, prime_wave_predictor(np.array([p]), training_primes)[0], 
                   color=color, s=size, marker=marker, zorder=5,
                   label='Correct Prediction' if is_correct and p == [q for q in predicted_primes if q in actual_set][0] else 
                         'False Positive' if not is_correct and p == [q for q in predicted_primes if q not in actual_set][0] else "")

ax1.set_title('Prime Wave Interference Pattern', fontsize=14, fontweight='bold')
ax1.set_xlabel('Number')
ax1.set_ylabel('Wave Amplitude')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1, min(200, prediction_limit))

# Plot 2: Prediction accuracy visualization
zoom_end = min(150, prediction_limit)
positions = np.arange(training_limit + 1, zoom_end + 1)

# Create binary arrays for plotting
actual_in_range = [p for p in actual_primes if training_limit < p <= zoom_end]
predicted_in_range = [p for p in predicted_primes if training_limit < p <= zoom_end]

# Plot as impulse train
for p in actual_in_range:
    ax2.plot([p, p], [0, 1], 'g-', linewidth=3, alpha=0.7, label='Actual Prime' if p == actual_in_range[0] else "")

for p in predicted_in_range:
    is_correct = p in actual_set
    color = 'blue' if is_correct else 'red'
    height = 0.8 if is_correct else 0.6
    ax2.plot([p, p], [0, height], color=color, linewidth=2, alpha=0.8,
             label='Correct Prediction' if is_correct and p == [q for q in predicted_in_range if q in actual_set][0] else
                   'False Positive' if not is_correct and p == [q for q in predicted_in_range if q not in actual_set][0] else "")

ax2.axvline(x=training_limit, color='black', linestyle='--', linewidth=2, label='Training Boundary')
ax2.set_title('Predictions vs Reality (Beyond Training)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Number')
ax2.set_ylabel('Prime Indicator')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(training_limit, zoom_end)
ax2.set_ylim(-0.1, 1.1)

plt.tight_layout()
plt.savefig('ultra_simple_prime_wave.png', dpi=300, bbox_inches='tight')
plt.show()

# --- Mathematical Insights ---
print(f"\n=== Mathematical Beauty ===")
print(f"Wave equation: Σ (1/√p) * cos(2π*x/(p*ln(p+1)) + pπ/N)")
print(f"Primes emerge at wave interference minima")
print(f"No sieving - pure wave mathematics")

beyond_training = [p for p in predicted_primes if p > training_limit]
correct_beyond = [p for p in beyond_training if p in actual_set]

print(f"\nBeyond training predictions: {beyond_training[:15]}")
print(f"Correct: {correct_beyond[:10]}")
print(f"Generalization success: {len(correct_beyond)/len(beyond_training)*100:.1f}%" if beyond_training else "0%")

# --- Wave Function Analysis ---
print(f"\n=== Wave Function Properties ===")
print(f"Number of component waves: {len(training_primes)}")
print(f"Frequency range: {2*np.pi/(training_primes[-1]*np.log(training_primes[-1]+1)):.3f} to {2*np.pi/(training_primes[0]*np.log(training_primes[0]+1)):.3f}")
print(f"Wave nodes found: {len(minima_indices)}")
print(f"Prime candidates after filtering: {len(predicted_primes)}")
