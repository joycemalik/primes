# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v67_prime_push_walk.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v67.py   (last edited 2025-08-23)
# What this script does  :: "Prime push" walk (prime_push_plots/).
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import sympy
import os

def generate_and_plot_push_walk(limit, output_folder):
    """
    Generates and plots a path based on 2D "Prime Push" dynamics.
    """
    print(f"Generating a 'Prime Push' walk up to {limit}...")

    # --- Pre-calculate primes for efficiency ---
    # FIX #1: Generate primes up to the prime AFTER the limit.
    # This guarantees that when we are at the last prime <= limit,
    # we can safely look ahead to the next one to calculate the gap.
    primes = list(sympy.primerange(11, sympy.nextprime(limit) + 1))
    if not primes or len(primes) < 2:
        print("Not enough primes found in the range.")
        return

    # --- Initial State ---
    position = np.array([0.0, 0.0])
    velocity = np.array([0.0, 0.0]) # Particle starts at rest
    path = []
    
    # --- The Walk ---
    prime_idx = 0
    for n in range(11, limit + 1):
        # The particle always moves one step according to its current velocity
        position += velocity
        path.append(list(position))

        # Check if the current number is the next prime
        if n == primes[prime_idx]:
            p_current = primes[prime_idx]
            # This is now safe because we generated enough primes
            p_next = primes[prime_idx + 1]
            prime_gap = p_next - p_current
            
            # The magnitude of the velocity change (the "push") is proportional to the prime gap
            push_magnitude = prime_gap * 0.005 # Scaling factor to keep plot tidy

            last_digit = p_current % 10
            
            # Apply the unique directional push to the velocity vector
            if last_digit == 1:   # Push UP
                velocity[1] += push_magnitude
            elif last_digit == 3: # Push LEFT
                velocity[0] -= push_magnitude
            elif last_digit == 7: # Push DOWN
                velocity[1] -= push_magnitude
            elif last_digit == 9: # Push RIGHT
                velocity[0] += push_magnitude
            
            # Move to the next prime in our list
            prime_idx += 1

    print("Path generated. Creating plot...")
    
    # --- Visualization ---
    path = np.array(path)
    x_coords, y_coords = path[:, 0], path[:, 1]
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Color the path to show progression
    colors = np.arange(len(x_coords))
    scatter = ax.scatter(x_coords, y_coords, c=colors, cmap='plasma', s=5, zorder=2)
    ax.plot(x_coords, y_coords, color='black', linewidth=0.5, alpha=0.5, zorder=1)
    
    # FIX #2: A more robust way to get the coordinates of the prime points.
    # First, get the list of primes that are within our walking limit.
    primes_on_path = [p for p in primes if p <= limit]
    # Then, calculate their corresponding indices in the 'path' array.
    prime_indices = [p - 11 for p in primes_on_path]
    # Finally, use these indices to get the coordinates from the path.
    prime_coords = path[prime_indices]
    
    ax.scatter(prime_coords[:,0], prime_coords[:,1], 
               c='white', s=25, marker='o', edgecolors='black', label='Primes (Push Points)', zorder=5)

    ax.set_title(f'The "Prime Push" Walk up to {limit}', fontsize=16)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_aspect('equal', 'box')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Progression (Number of Steps)')
    
    # Save the plot
    filename = f'PrimePush_up_to_{limit}.png'
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=150)
    print(f"✅ Plot saved as: '{output_path}'")
    plt.show()
    plt.close(fig)


if __name__ == '__main__':
    OUTPUT_FOLDER = 'prime_push_plots'
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 💫 The 'Prime Push' Plotter ---")
    
    while True:
        try:
            limit = int(input("Enter the upper numerical limit (e.g., 20000): "))
            if limit < 20:
                print("Please enter a limit of 20 or higher for a more interesting path.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    generate_and_plot_push_walk(limit, OUTPUT_FOLDER)

    print("\n✨ Process complete!")