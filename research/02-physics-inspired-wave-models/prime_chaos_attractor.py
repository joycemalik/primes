# ----------------------------------------------------------------------------
# Prime research archive :: research/02-physics-inspired-wave-models/prime_chaos_attractor.py
# Original location      :: learn/prime_chaos_attractor.py   (last edited 2025-08-02)
# What this script does  :: Lorenz system forced by prime frequencies; Poincare sections and box-counting dimension.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import find_peaks

def prime_sieve(n):
    """Generates primes up to n using the Sieve of Eratosthenes."""
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i:n+1:i] = False
    return np.where(primes)[0]

# --- Chaos-Based Prime Attractor Model ---
# Concept: Primes emerge from strange attractor dynamics in phase space

print("=== Chaos Theory Prime Attractor Model ===")

# --- Parameters ---
training_limit = 20
prediction_limit = 500

training_primes = prime_sieve(training_limit)
print(f"Training primes: {training_primes}")

# --- 1. Prime-Driven Lorenz System ---
# Modified Lorenz equations where primes influence the dynamics

def prime_lorenz_system(state, t, primes):
    """
    Modified Lorenz system influenced by prime numbers
    dx/dt = σ(y - x) + prime_forcing(t)
    dy/dt = x(ρ - z) - y
    dz/dt = xy - βz
    """
    x, y, z = state
    
    # Standard Lorenz parameters
    sigma = 10.0
    rho = 28.0
    beta = 8.0/3.0
    
    # Prime forcing function - creates resonance at prime locations
    prime_forcing = 0
    for p in primes:
        # Each prime creates a forcing oscillation
        omega_p = 2 * np.pi / p
        amplitude_p = 1.0 / np.sqrt(p)
        prime_forcing += amplitude_p * np.sin(omega_p * t)
    
    # Modified Lorenz equations with prime forcing
    dxdt = sigma * (y - x) + 0.5 * prime_forcing
    dydt = x * (rho - z) - y + 0.1 * prime_forcing * np.cos(t)
    dzdt = x * y - beta * z
    
    return [dxdt, dydt, dzdt]

# --- 2. Generate Prime Attractor Trajectory ---
# Time corresponds to the number line
t_span = np.linspace(1, prediction_limit, 10000)
initial_state = [1.0, 1.0, 1.0]

# Solve the differential equation
trajectory = odeint(prime_lorenz_system, initial_state, t_span, args=(training_primes,))

x_traj, y_traj, z_traj = trajectory.T

# --- 3. Prime Detection via Poincaré Sections ---
# Primes appear where trajectory crosses certain planes in phase space

# Define Poincaré section: z = constant plane
z_section = np.mean(z_traj)

# Find crossings of the Poincaré section
crossings = []
crossing_times = []

for i in range(1, len(z_traj)):
    # Check if trajectory crosses the section plane
    if (z_traj[i-1] < z_section < z_traj[i]) or (z_traj[i] < z_section < z_traj[i-1]):
        # Linear interpolation to find exact crossing time
        alpha = (z_section - z_traj[i-1]) / (z_traj[i] - z_traj[i-1])
        crossing_time = t_span[i-1] + alpha * (t_span[i] - t_span[i-1])
        crossing_x = x_traj[i-1] + alpha * (x_traj[i] - x_traj[i-1])
        crossing_y = y_traj[i-1] + alpha * (y_traj[i] - y_traj[i-1])
        
        crossings.append([crossing_x, crossing_y])
        crossing_times.append(crossing_time)

crossings = np.array(crossings)
crossing_times = np.array(crossing_times)

# --- 4. Strange Attractor Prime Pattern ---
# Analyze the pattern in crossing coordinates to predict primes

if len(crossings) > 0:
    # Calculate radial distance from origin in Poincaré section
    radial_distances = np.sqrt(crossings[:, 0]**2 + crossings[:, 1]**2)
    
    # Find local maxima in radial distance - these indicate prime positions
    max_indices, _ = find_peaks(radial_distances, 
                               distance=5,  # Minimum separation
                               prominence=np.std(radial_distances) * 0.5)
    
    # Map crossing times to prime candidates
    prime_candidate_times = crossing_times[max_indices]
    predicted_primes = np.unique(np.round(prime_candidate_times).astype(int))
    predicted_primes = predicted_primes[predicted_primes > 1]
else:
    predicted_primes = np.array([])

# --- 5. Fractal Dimension Analysis ---
# Primes might follow fractal patterns in the attractor

def box_counting_dimension(points, max_box_size=100):
    """Estimate fractal dimension using box counting"""
    if len(points) < 10:
        return 1.0
        
    box_sizes = np.logspace(0, np.log10(max_box_size), 20)
    box_counts = []
    
    for box_size in box_sizes:
        # Count boxes needed to cover all points
        if len(points.shape) == 1:
            points_2d = np.column_stack([points, np.zeros_like(points)])
        else:
            points_2d = points
            
        x_min, x_max = points_2d[:, 0].min(), points_2d[:, 0].max()
        y_min, y_max = points_2d[:, 1].min(), points_2d[:, 1].max()
        
        x_boxes = int(np.ceil((x_max - x_min) / box_size))
        y_boxes = int(np.ceil((y_max - y_min) / box_size))
        
        occupied_boxes = set()
        for point in points_2d:
            box_x = int((point[0] - x_min) / box_size)
            box_y = int((point[1] - y_min) / box_size)
            occupied_boxes.add((box_x, box_y))
        
        box_counts.append(len(occupied_boxes))
    
    # Fit power law: N(ε) ∝ ε^(-D)
    log_box_sizes = np.log(box_sizes)
    log_box_counts = np.log(box_counts)
    
    # Linear regression to find dimension
    coeffs = np.polyfit(log_box_sizes, log_box_counts, 1)
    fractal_dimension = -coeffs[0]
    
    return fractal_dimension

if len(crossings) > 10:
    attractor_dimension = box_counting_dimension(crossings)
    print(f"Attractor fractal dimension: {attractor_dimension:.3f}")
else:
    attractor_dimension = 1.0

# --- 6. Validation ---
actual_primes = prime_sieve(prediction_limit)
predicted_set = set(predicted_primes)
actual_set = set(actual_primes)

true_positives = len(predicted_set & actual_set)
false_positives = len(predicted_set - actual_set)
false_negatives = len(actual_set - predicted_set)

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print(f"\n=== Chaos Attractor Results ===")
print(f"Poincaré crossings found: {len(crossings)}")
print(f"Total predicted primes: {len(predicted_primes)}")
print(f"Total actual primes: {len(actual_primes)}")
print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall: {recall:.4f} ({recall*100:.2f}%)")

# --- 7. Advanced Visualization ---
fig = plt.figure(figsize=(20, 16))

# Plot 1: 3D Attractor
ax1 = fig.add_subplot(2, 3, 1, projection='3d')
ax1.plot(x_traj, y_traj, z_traj, 'b-', alpha=0.6, linewidth=0.5)

# Mark points corresponding to training primes
for p in training_primes:
    if p < len(t_span):
        idx = int(p * len(t_span) / prediction_limit)
        if idx < len(x_traj):
            ax1.scatter(x_traj[idx], y_traj[idx], z_traj[idx], 
                       color='red', s=100, alpha=0.8)

ax1.set_title('Prime-Driven Strange Attractor')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

# Plot 2: Poincaré Section
ax2 = fig.add_subplot(2, 3, 2)
if len(crossings) > 0:
    ax2.scatter(crossings[:, 0], crossings[:, 1], c=crossing_times, 
               cmap='viridis', s=30, alpha=0.7)
    
    # Highlight crossings corresponding to predicted primes
    for p in predicted_primes:
        if p < prediction_limit:
            # Find closest crossing to this prime
            time_diffs = np.abs(crossing_times - p)
            if len(time_diffs) > 0:
                closest_idx = np.argmin(time_diffs)
                if time_diffs[closest_idx] < 2.0:  # Close enough
                    ax2.scatter(crossings[closest_idx, 0], crossings[closest_idx, 1], 
                               color='red', s=100, marker='x')

ax2.set_title('Poincaré Section (z = const)')
ax2.set_xlabel('X at crossing')
ax2.set_ylabel('Y at crossing')
ax2.grid(True, alpha=0.3)

# Plot 3: Time series with predictions
ax3 = fig.add_subplot(2, 3, 3)
ax3.plot(t_span, x_traj, 'b-', alpha=0.7, linewidth=1, label='X trajectory')

# Mark actual primes
for p in actual_primes:
    if p <= prediction_limit:
        color = 'green' if p <= training_limit else 'orange'
        ax3.axvline(x=p, color=color, alpha=0.6, linewidth=1)

# Mark predictions
for p in predicted_primes:
    if p <= prediction_limit:
        is_correct = p in actual_set
        color = 'blue' if is_correct else 'red'
        style = '-' if is_correct else '--'
        ax3.axvline(x=p, color=color, linestyle=style, alpha=0.8, linewidth=2)

ax3.set_title('X Trajectory with Prime Predictions')
ax3.set_xlabel('Time (Number)')
ax3.set_ylabel('X coordinate')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_xlim(1, min(100, prediction_limit))

# Plot 4: Phase portrait (X vs Y)
ax4 = fig.add_subplot(2, 3, 4)
ax4.plot(x_traj, y_traj, 'b-', alpha=0.6, linewidth=0.5)
ax4.set_title('Phase Portrait (X vs Y)')
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.grid(True, alpha=0.3)

# Plot 5: Radial distance in Poincaré section
ax5 = fig.add_subplot(2, 3, 5)
if len(crossings) > 0:
    ax5.plot(crossing_times, radial_distances, 'b-o', markersize=3, linewidth=1)
    
    # Mark peaks (predicted primes)
    if len(max_indices) > 0:
        ax5.plot(crossing_times[max_indices], radial_distances[max_indices], 
                'ro', markersize=8, label='Predicted Primes')

ax5.set_title('Radial Distance in Poincaré Section')
ax5.set_xlabel('Time')
ax5.set_ylabel('Radial Distance')
ax5.legend()
ax5.grid(True, alpha=0.3)

# Plot 6: Prediction accuracy
ax6 = fig.add_subplot(2, 3, 6)
positions = np.arange(1, min(200, prediction_limit) + 1)
actual_binary = np.isin(positions, actual_primes).astype(int)
predicted_binary = np.isin(positions, predicted_primes).astype(int)

ax6.plot(positions, actual_binary + 0.1, 'g-', linewidth=3, label='Actual Primes', alpha=0.7)
ax6.plot(positions, predicted_binary - 0.1, 'r-', linewidth=2, label='Predicted Primes', alpha=0.7)
ax6.axvline(x=training_limit, color='black', linestyle='--', linewidth=2, label='Training Limit')

ax6.set_title('Prediction vs Reality')
ax6.set_xlabel('Number')
ax6.set_ylabel('Is Prime')
ax6.legend()
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('chaos_prime_attractor.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\n=== Chaos Theory Insights ===")
print(f"1. Strange attractor dimension: {attractor_dimension:.3f}")
print(f"2. Poincaré crossings: {len(crossings)}")
print(f"3. Prime predictions emerge from attractor geometry")
print(f"4. Fractal patterns in phase space reveal prime structure")

if len(predicted_primes) > 0:
    beyond_training = [p for p in predicted_primes if p > training_limit]
    correct_beyond = [p for p in beyond_training if p in actual_set]
    print(f"\nPredictions beyond training: {beyond_training[:15]}")
    print(f"Correct predictions: {correct_beyond}")
    print(f"Success rate: {len(correct_beyond)/len(beyond_training)*100:.1f}%" if beyond_training else "0%")
