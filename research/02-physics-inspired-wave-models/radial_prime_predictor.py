# ----------------------------------------------------------------------------
# Prime research archive :: research/02-physics-inspired-wave-models/radial_prime_predictor.py
# Original location      :: learn/radial_prime_predictor.py   (last edited 2025-08-02)
# What this script does  :: Radial standing waves on a spiral; minima as prime candidates.
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
training_limit = 50   # Train with primes up to 50
prediction_limit = 500  # Predict up to 500

# --- 1. Generate Training Data ---
training_primes = prime_sieve(training_limit)
print(f"Training with {len(training_primes)} primes up to {training_limit}")

# Create spiral coordinates for radial analysis
theta = np.linspace(0, 20 * np.pi, prediction_limit)  # 20 rotations
r = np.linspace(1, prediction_limit, prediction_limit)  # Radius increases linearly

# Convert to cartesian for wave analysis
x_spiral = r * np.cos(theta)
y_spiral = r * np.sin(theta)

# --- 2. Create Radial Wave Function ---
# Each prime creates a standing wave pattern in polar coordinates
radial_wave = np.zeros_like(r)

for prime in training_primes:
    # Create radial wave with frequency related to the prime
    angular_freq = 2 * np.pi / prime
    radial_freq = 1.0 / prime
    
    # Combine angular and radial components
    wave_component = np.sin(angular_freq * theta) * np.cos(radial_freq * r)
    radial_wave += wave_component / prime  # Weight by inverse of prime

# --- 3. Find Prime Candidates ---
# Look for local minima in the radial wave
from scipy.signal import find_peaks

# Find valleys (negative peaks)
valleys, _ = find_peaks(-radial_wave, distance=3, prominence=0.01)

# Map back to integer positions
predicted_positions = np.round(r[valleys]).astype(int)
predicted_primes = np.unique(predicted_positions)
predicted_primes = predicted_primes[predicted_primes > 1]

# --- 4. Calculate Performance ---
actual_primes = prime_sieve(prediction_limit)
predicted_set = set(predicted_primes)
actual_set = set(actual_primes)

true_positives = len(predicted_set & actual_set)
false_positives = len(predicted_set - actual_set)
false_negatives = len(actual_set - predicted_set)

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print(f"\nRadial Wave Prime Prediction Results:")
print(f"Training range: 1 to {training_limit}")
print(f"Prediction range: 1 to {prediction_limit}")
print(f"")
print(f"Total actual primes: {len(actual_primes)}")
print(f"Total predicted primes: {len(predicted_primes)}")
print(f"")
print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")
print(f"")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall: {recall:.4f} ({recall*100:.2f}%)")

# --- 5. Visualization ---
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

# Plot 1: Spiral representation with primes
ax1.plot(x_spiral, y_spiral, 'b-', alpha=0.6, linewidth=1)
for i, prime in enumerate(actual_primes):
    if prime < len(x_spiral):
        if prime <= training_limit:
            ax1.plot(x_spiral[prime-1], y_spiral[prime-1], 'go', markersize=8, label='Training Prime' if i == 0 else "")
        else:
            ax1.plot(x_spiral[prime-1], y_spiral[prime-1], 'ro', markersize=6, label='Actual Prime' if prime == [p for p in actual_primes if p > training_limit][0] else "")

ax1.set_title('Prime Spiral Pattern')
ax1.set_aspect('equal')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Radial wave function
ax2.plot(r, radial_wave, 'b-', linewidth=2)
ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)

# Mark actual primes
for prime in actual_primes:
    if prime < len(r):
        color = 'green' if prime <= training_limit else 'red'
        ax2.axvline(x=prime, color=color, alpha=0.6, linewidth=1)

ax2.set_title('Radial Wave Function')
ax2.set_xlabel('Position')
ax2.set_ylabel('Wave Amplitude')
ax2.grid(True, alpha=0.3)

# Plot 3: Polar wave pattern
ax3 = plt.subplot(2, 2, 3, projection='polar')
scatter_colors = ['green' if p <= training_limit else 'red' for p in actual_primes if p < len(theta)]
scatter_r = [p for p in actual_primes if p < len(theta)]
scatter_theta = [theta[p-1] for p in scatter_r]

ax3.plot(theta, r, 'b-', alpha=0.3, linewidth=1)
ax3.scatter(scatter_theta, scatter_r, c=scatter_colors, s=50)
ax3.set_title('Polar Prime Distribution')

# Plot 4: Prediction accuracy comparison
positions = np.arange(1, prediction_limit + 1)
actual_binary = np.isin(positions, actual_primes).astype(int)
predicted_binary = np.isin(positions, predicted_primes).astype(int)

ax4.plot(positions, actual_binary + 0.1, 'g-', linewidth=3, label='Actual Primes', alpha=0.7)
ax4.plot(positions, predicted_binary - 0.1, 'r-', linewidth=2, label='Predicted Primes', alpha=0.7)
ax4.axvline(x=training_limit, color='black', linestyle='--', linewidth=2, label='Training Limit')

ax4.set_title('Prediction vs Reality')
ax4.set_xlabel('Number')
ax4.set_ylabel('Is Prime')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, min(200, prediction_limit))

plt.tight_layout()
plt.savefig('radial_prime_wave.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\nSample predictions beyond training:")
beyond_predictions = [p for p in predicted_primes if p > training_limit][:15]
for p in beyond_predictions:
    is_prime = p in actual_set
    print(f"Position {p}: {'PRIME ✓' if is_prime else 'COMPOSITE ✗'}")
