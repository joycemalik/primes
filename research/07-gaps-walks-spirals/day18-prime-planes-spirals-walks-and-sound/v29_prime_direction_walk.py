# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v29_prime_direction_walk.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v29.py   (last edited 2025-08-23)
# What this script does  :: Walk whose direction is set by primes.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import sympy
import numpy as np
import os

def generate_prime_walk(limit):
    """
    Generates the path coordinates for a walk directed by prime numbers.
    
    Rules:
    - Start at (0,0).
    - Iterate from 11 to the limit.
    - If a number is prime, change direction based on its last digit.
    - If a number is composite, take one step in the current direction.
    """
    print("Generating the walk path...")
    
    # Define the direction vectors
    directions = {
        1: np.array([0, 1]),   # Up
        3: np.array([-1, 0]),  # Left
        7: np.array([0, -1]),  # Down
        9: np.array([1, 0])    # Right
    }
    
    # Initialization
    current_pos = np.array([0, 0])
    # The first prime is 11, which ends in 1, so the initial direction is Up.
    current_dir = directions[1] 
    
    # Store the path and the locations of primes
    path_x, path_y = [current_pos[0]], [current_pos[1]]
    prime_points = {'x': [], 'y': [], 'label': []}

    # The walk starts at number 11
    for n in range(11, limit + 1):
        if sympy.isprime(n):
            # Record the current location as a prime turning point
            prime_points['x'].append(current_pos[0])
            prime_points['y'].append(current_pos[1])
            prime_points['label'].append(str(n))
            
            # Change direction based on the prime's last digit
            last_digit = n % 10
            if last_digit in directions:
                current_dir = directions[last_digit]
        else:
            # It's a composite number, so take a step
            current_pos = current_pos + current_dir
            path_x.append(current_pos[0])
            path_y.append(current_pos[1])
            
    print("Path generation complete.")
    return path_x, path_y, prime_points

def plot_walk(path_x, path_y, prime_points, limit):
    """
    Creates and saves a plot of the generated prime walk.
    """
    print("Creating the plot...")
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Plot the main path of the walk
    ax.plot(path_x, path_y, color='gray', linewidth=1, alpha=0.8, label='Composite Path')
    
    # Highlight the prime turning points with colored markers
    scatter = ax.scatter(prime_points['x'], prime_points['y'], 
                         c=range(len(prime_points['label'])), # Color by sequence
                         cmap='viridis', s=80, zorder=5, label='Primes (Turning Points)')
    
    # Add labels for the first few primes to show the pattern
    for i in range(min(15, len(prime_points['label']))):
        ax.text(prime_points['x'][i] + 0.1, prime_points['y'][i] + 0.1, 
                prime_points['label'][i], fontsize=9)

    # Styling the plot
    ax.set_title(f'Prime Direction Walk up to {limit}', fontsize=16)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_aspect('equal', 'box')
    ax.legend()
    
    # Add a color bar to show the progression of primes
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Prime Sequence Progression')
    
    # Save the plot
    output_folder = 'prime_walk_plots'
    os.makedirs(output_folder, exist_ok=True)
    filename = f'prime_walk_to_{limit}.png'
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=150)
    print(f"✅ Plot saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    print("--- 🚶 Prime Direction Walk Generator ---")
    while True:
        try:
            limit = int(input("Enter the upper numerical limit for the walk (e.g., 5000): "))
            if limit < 11:
                print("Please enter a limit of 11 or higher.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    # Generate the data and create the plot
    px, py, p_points = generate_prime_walk(limit)
    plot_walk(px, py, p_points, limit)