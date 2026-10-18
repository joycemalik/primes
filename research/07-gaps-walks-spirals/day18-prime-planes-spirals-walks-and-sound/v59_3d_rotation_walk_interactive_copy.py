# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v59_3d_rotation_walk_interactive_copy.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v59.py   (last edited 2025-08-23)
# What this script does  :: Identical copy of v53.
# ----------------------------------------------------------------------------
import plotly.graph_objects as go
import numpy as np
import sympy
import os
from scipy.spatial.transform import Rotation as R # For easy 3D rotations

def generate_3d_prime_walk(limit):
    """
    Generates the 3D path data where primes dictate rotations.
    (This function is the same as the previous script)
    """
    print(f"Generating 3D Prime Rotation Walk up to {limit}...")

    # Define Rotation Axes
    axis_theta = np.array([0, 1, 0]) # Rotation around Y-axis
    axis_gamma = np.array([0, 0, 1]) # Rotation around Z-axis

    # Initial State
    position = np.array([0.0, 0.0, 0.0])
    direction = np.array([1.0, 0.0, 0.0]) # Start moving along X-axis
    path = [list(position)]

    primes = list(sympy.primerange(11, limit + 1))
    if not primes:
        print("No primes found in the specified range.")
        return np.array(path)

    for i in range(len(primes) - 1):
        p_current = primes[i]
        p_next = primes[i+1]
        num_composites = p_next - p_current - 1

        # 1. MOVE for each composite in the gap
        for _ in range(num_composites):
            position += direction
            path.append(list(position))

        # 2. ROTATE the direction vector based on the next prime
        last_digit = p_next % 10
        angle_rad = float(num_composites)
        
        rotation_axis = None
        rotation_sign = 1.0

        if last_digit == 1:    # +Theta
            rotation_axis, rotation_sign = axis_theta, 1.0
        elif last_digit == 3:  # +Gamma
            rotation_axis, rotation_sign = axis_gamma, 1.0
        elif last_digit == 7:  # -Theta
            rotation_axis, rotation_sign = axis_theta, -1.0
        elif last_digit == 9:  # -Gamma
            rotation_axis, rotation_sign = axis_gamma, -1.0
        
        if rotation_axis is not None:
            rotation = R.from_rotvec(rotation_axis * angle_rad * rotation_sign)
            direction = rotation.apply(direction)

    print("Walk generation complete.")
    return np.array(path)

def plot_interactive_3d_walk(path, limit):
    """
    Visualizes the generated 3D path in an interactive HTML file.
    """
    print("Generating interactive 3D plot...")
    
    x, y, z = path[:, 0], path[:, 1], path[:, 2]
    
    # Create the 3D scatter plot trace
    trace = go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines+markers',
        line=dict(
            color=np.arange(len(x)), # Color line by progression
            colorscale='Plasma',
            width=4
        ),
        marker=dict(
            size=3,
            color=np.arange(len(x)), # Color markers by progression
            colorscale='Plasma',
            colorbar=dict(title='Progression of Steps'),
            opacity=0.8
        ),
        hoverinfo='text',
        text=[f'Step: {i}' for i in range(len(x))]
    )
    
    # Create the layout for the 3D environment
    layout = go.Layout(
        title=f'Interactive 3D Prime Rotation Walk up to {limit}',
        scene=dict(
            xaxis=dict(title='X Coordinate'),
            yaxis=dict(title='Y Coordinate'),
            zaxis=dict(title='Z Coordinate'),
            aspectratio=dict(x=1, y=1, z=1) # Ensure correct proportions
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    fig = go.Figure(data=[trace], layout=layout)
    
    # Save the plot to a self-contained HTML file
    output_folder = 'interactive_3d_walks'
    os.makedirs(output_folder, exist_ok=True)
    filename = f'Interactive_3D_PrimeWalk_{limit}.html'
    output_path = os.path.join(output_folder, filename)
    fig.write_html(output_path)
    print(f"✅ Interactive 3D environment saved as: '{output_path}'")


if __name__ == '__main__':
    print("--- 🌐 Interactive 3D Prime Walk Plotter ---")
    
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
        plot_interactive_3d_walk(path_data, limit)
    else:
        print("No path generated. Check the limit.")

    print("\n✨ Process complete!")