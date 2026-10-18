# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v61_prime_river.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v61.py   (last edited 2025-08-23)
# What this script does  :: The "prime river" path.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import sympy
import os

def generate_and_plot_river(limit, output_folder):
    """
    Generates and plots the Prime River path.
    """
    print(f"Generating a Prime River up to {limit}...")

    # --- Pre-calculate primes for efficiency ---
    primes = list(sympy.primerange(11, limit + 2)) # Get one extra for the last gap
    if not primes:
        print("Not enough primes found in the range.")
        return

    # --- Initial State ---
    x_pos = 0.0
    # The 'velocity' or sideways drift of the river
    x_velocity = 0.0
    
    # The path will store the history of (x, y) coordinates
    path = []
    
    # --- The Flow ---
    prime_idx = 0
    for n in range(11, limit + 1):
        # The river always flows "down" the Y-axis
        y_pos = -n
        
        # The river's sideways position is updated by its current drift
        x_pos += x_velocity
        path.append([x_pos, y_pos])

        # Check if the current number is the next prime
        if n == primes[prime_idx]:
            # A prime has been hit. We need to calculate the next change in velocity.
            p_current = primes[prime_idx]
            p_next = primes[prime_idx + 1]
            
            prime_gap = p_next - p_current
            
            # The magnitude of the velocity change is proportional to the prime gap.
            # We use a small scaling factor to keep the plot manageable.
            velocity_change_magnitude = prime_gap * 0.01

            last_digit = p_current % 10
            
            # Primes ending in 1 or 3 push the current to the LEFT
            if last_digit in [1, 3]:
                x_velocity -= velocity_change_magnitude
            # Primes ending in 7 or 9 push the current to the RIGHT
            elif last_digit in [7, 9]:
                x_velocity += velocity_change_magnitude
            
            prime_idx += 1

    print("River path generated. Creating plot...")
    
    # --- Visualization ---
    path = np.array(path)
    x_coords, y_coords = path[:, 0], path[:, 1]
    
    fig, ax = plt.subplots(figsize=(12, 16))
    
    # Use a colormap to show the progression down the river
    colors = y_coords
    scatter = ax.scatter(x_coords, y_coords, c=colors, cmap='ocean', s=15)
    
    # Mark the prime locations on the path
    prime_y_coords = -np.array(primes)
    prime_indices_in_path = [np.where(y_coords == py)[0][0] for py in prime_y_coords if py in y_coords]
    prime_x_coords_on_path = x_coords[prime_indices_in_path]
    ax.scatter(prime_x_coords_on_path, y_coords[prime_indices_in_path], 
               c='red', s=50, marker='o', edgecolors='black', label='Primes (Turning Points)', zorder=5)

    ax.set_title(f'The Prime River up to {limit}', fontsize=16)
    ax.set_xlabel('Sideways Drift')
    ax.set_ylabel('Number Line (Flowing Down)')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Progression Down the Number Line')
    
    # Save the plot
    filename = f'PrimeRiver_up_to_{limit}.png'
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=150)
    print(f"✅ Plot saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    OUTPUT_FOLDER = 'prime_river_plots'
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 🏞️ The Prime River Plotter ---")
    
    while True:
        try:
            limit = int(input("Enter the upper numerical limit (e.g., 10000): "))
            if limit < 20:
                print("Please enter a limit of 20 or higher for a more interesting river.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    generate_and_plot_river(limit, OUTPUT_FOLDER)

    print("\n✨ Process complete!")