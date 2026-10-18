# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v31_prime_composite_walk.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v31.py   (last edited 2025-08-23)
# What this script does  :: Walk driven by primes and composites.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import sympy # For its fast isprime() function
import os

def generate_prime_walk(limit):
    """
    Generates the path of a walk based on prime and composite numbers.
    """
    print(f"Generating a Prime Walk up to {limit}...")
    
    # --- Initial State ---
    # Directions: UP, LEFT, DOWN, RIGHT
    direction_map = {
        1: np.array([0, 1]),   # Ending in 1 moves UP
        3: np.array([-1, 0]),  # Ending in 3 moves LEFT
        7: np.array([0, -1]),  # Ending in 7 moves DOWN
        9: np.array([1, 0])    # Ending in 9 moves RIGHT
    }
    
    # Start at the origin, facing RIGHT
    position = np.array([0, 0])
    direction = np.array([1, 0]) # Initial direction is RIGHT
    
    # The path will store the history of (x, y) coordinates
    path = [list(position)]

    # --- The Walk ---
    # Iterate through numbers starting from 11, as requested.
    for n in range(11, limit + 1):
        if sympy.isprime(n):
            # If it's a prime, we CHANGE the direction vector
            last_digit = n % 10
            if last_digit in direction_map:
                direction = direction_map[last_digit]
                # Note: No movement occurs on a prime number
        else:
            # If it's a composite, we MOVE one step in the current direction
            position = position + direction
            path.append(list(position))
            
    print("Walk generation complete.")
    return np.array(path)

def plot_walk(path, limit):
    """
    Visualizes the generated path using matplotlib.
    """
    print("Generating plot...")
    fig, ax = plt.subplots(figsize=(12, 12))
    
    x_coords = path[:, 0]
    y_coords = path[:, 1]
    
    # Use a colormap to show the progression of the walk over time
    num_steps = len(x_coords)
    colors = np.arange(num_steps)

    # Plot the path with a color gradient
    scatter = ax.scatter(x_coords, y_coords, c=colors, cmap='viridis', s=10, zorder=3)
    # Plot a faint line connecting the points
    ax.plot(x_coords, y_coords, color='gray', linewidth=0.75, alpha=0.8, zorder=2)
    
    # Mark the Start and End points
    ax.scatter(path[0, 0], path[0, 1], c='lime', s=150, marker='o', edgecolors='black', label='Start', zorder=5)
    ax.scatter(path[-1, 0], path[-1, 1], c='red', s=150, marker='X', label='End', zorder=5)

    # --- Final Touches ---
    ax.set_title(f'Prime Walk Path up to {limit}', fontsize=16)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_aspect('equal', 'box') # Ensures UP and RIGHT steps are the same length
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    # Add a color bar to indicate time/progression
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Progression of Steps')
    
    # Save the plot to a file
    output_folder = 'prime_walk_plots'
    os.makedirs(output_folder, exist_ok=True)
    filename = f'PrimeWalk_up_to_{limit}.png'
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=150)
    print(f"✅ Plot saved as: '{output_path}'")
    plt.close(fig)

if __name__ == '__main__':
    print("--- 🚶‍♂️ Prime Walk Plotter ---")
    print("Primes change the direction, composites take the steps.")
    
    while True:
        try:
            # A larger number of steps creates more interesting patterns
            limit = int(input("Enter the upper numerical limit (e.g., 50000): "))
            if limit < 12:
                print("Please enter a limit of 12 or higher to see at least one step.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    path_data = generate_prime_walk(limit)
    
    if len(path_data) > 1:
        plot_walk(path_data, limit)
    else:
        print("No composite numbers were found in the range, so no path was generated.")

    print("\n✨ Process complete!")