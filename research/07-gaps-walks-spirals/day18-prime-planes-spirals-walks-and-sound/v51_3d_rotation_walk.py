# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v51_3d_rotation_walk.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v51.py   (last edited 2025-08-23)
# What this script does  :: 3D walk: rotate by (gap - 1) about y or z depending on last digit.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy
import os
from scipy.spatial.transform import Rotation as R # For easy 3D rotations

def generate_3d_prime_walk(limit):
    """
    Generates a 3D path where primes dictate rotations.
    """
    print(f"Generating 3D Prime Rotation Walk up to {limit}...")

    # --- Define Rotation Axes ---
    # Theta axis will be rotation around the global Y-axis (pitch)
    axis_theta = np.array([0, 1, 0])
    # Gamma axis will be rotation around the global Z-axis (yaw)
    axis_gamma = np.array([0, 0, 1])

    # --- Initial State ---
    position = np.array([0.0, 0.0, 0.0])
    # Start by moving forward along the X-axis
    direction = np.array([1.0, 0.0, 0.0])
    path = [list(position)]

    # --- Pre-calculate primes for efficiency ---
    primes = list(sympy.primerange(11, limit + 1))
    if not primes:
        print("No primes found in the specified range.")
        return np.array(path)

    # --- The Walk ---
    for i in range(len(primes) - 1):
        p_current = primes[i]
        p_next = primes[i+1]

        # All numbers between p_current and p_next are composites
        num_composites = p_next - p_current - 1

        # 1. MOVE for each composite in the gap
        # The direction remains constant throughout this segment.
        for _ in range(num_composites):
            position += direction
            path.append(list(position))

        # 2. ROTATE the direction vector based on the next prime (p_next)
        last_digit = p_next % 10
        
        # The rotation angle is the number of composites we just passed
        angle_rad = float(num_composites) 
        
        rotation_axis = None
        rotation_sign = 1.0

        if last_digit == 1: # +Theta
            rotation_axis = axis_theta
            rotation_sign = 1.0
        elif last_digit == 3: # +Gamma
            rotation_axis = axis_gamma
            rotation_sign = 1.0
        elif last_digit == 7: # -Theta
            rotation_axis = axis_theta
            rotation_sign = -1.0
        elif last_digit == 9: # -Gamma
            rotation_axis = axis_gamma
            rotation_sign = -1.0
        
        if rotation_axis is not None:
            # Create a rotation object from the axis and angle
            rotation_vector = rotation_axis * angle_rad * rotation_sign
            rotation = R.from_rotvec(rotation_vector)
            # Apply the rotation to the current direction vector
            direction = rotation.apply(direction)

    print("Walk generation complete.")
    return np.array(path)

def plot_3d_walk(path, limit):
    """
    Visualizes the generated 3D path.
    """
    print("Generating 3D plot...")
    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(111, projection='3d')

    path = np.array(path)
    x, y, z = path[:, 0], path[:, 1], path[:, 2]

    # Use a colormap to show progression
    colors = np.arange(len(x))
    scatter = ax.scatter(x, y, z, c=colors, cmap='plasma', s=5)
    ax.plot(x, y, z, color='gray', linewidth=0.5, alpha=0.5)

    # Mark Start and End
    ax.scatter(x[0], y[0], z[0], c='lime', s=200, marker='o', edgecolors='black', label='Start')
    ax.scatter(x[-1], y[-1], z[-1], c='red', s=200, marker='X', label='End')
    
    ax.set_title(f'3D Prime Rotation Walk up to {limit}', fontsize=16)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    ax.legend()
    
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.6)
    cbar.set_label('Progression of Steps')
    
    # Set a good initial viewing angle
    ax.view_init(elev=25, azim=-60)
    
    output_folder = '3d_prime_walks'
    os.makedirs(output_folder, exist_ok=True)
    filename = f'3D_PrimeWalk_{limit}.png'
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=150)
    print(f"✅ Plot saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    print("--- 🌀 3D Prime Rotation Walk Plotter ---")
    
    while True:
        try:
            limit = int(input("Enter the upper numerical limit (e.g., 20000): "))
            if limit < 13:
                print("Please enter a limit of 13 or higher.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    path_data = generate_3d_prime_walk(limit)
    
    if len(path_data) > 1:
        plot_3d_walk(path_data, limit)
    else:
        print("No path generated. Check the limit.")

    print("\n✨ Process complete!")