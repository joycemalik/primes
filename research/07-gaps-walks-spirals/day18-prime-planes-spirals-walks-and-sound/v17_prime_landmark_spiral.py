# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v17_prime_landmark_spiral.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v17.py   (last edited 2025-08-22)
# What this script does  :: Spiral with angles warped toward prime landmarks.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import sympy
import numpy as np
import os
import re
import ast

def sanitize_filename(text):
    """Converts a string into a valid PNG filename."""
    s = text.replace('**', '_pow_').replace('*', '_mul_').replace('/', '_div_')
    s = re.sub(r'[^a-zA-Z0-9_\-]', '', s)
    return s[:100] + '.png'

def map_to_prime_angle(x_coords, primes, total_rotations):
    """
    Maps standard x-coordinates to a "warped" prime-centric angle.
    This is the core of the Prime Landmark Spiral.
    """
    # Find the index 'n' of the prime p_n that comes just before each x
    prime_indices = np.searchsorted(primes, x_coords, side='right') - 1

    p_n = primes[prime_indices]
    p_next = primes[prime_indices + 1]
    
    # Linearly interpolate each x within its prime gap [p_n, p_next]
    # to the corresponding angular landmark gap [n, n+1].
    fraction_through_gap = (x_coords - p_n) / (p_next - p_n)
    
    # This gives the "squeezed" index, which we convert to an angle
    squeezed_index = prime_indices + fraction_through_gap
    
    # Convert the squeezed index to a continuous angle
    total_angle = 2 * np.pi * total_rotations
    prime_angle = (squeezed_index / (len(primes) - 2)) * total_angle
    
    return prime_angle

def plot_spiral_comparison(func_str, limit, rotations, output_folder):
    """
    Creates a side-by-side comparison of a standard vs. prime-inflected spiral.
    """
    print(f"Processing function: '{func_str}'...")
    
    # 1. Parse the function
    try:
        x_sym = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        func = sympy.lambdify(x_sym, expr, 'numpy')
    except Exception as e:
        print(f"  -> ❌ Error parsing '{func_str}'. Skipping. (Reason: {e})")
        return

    # 2. Generate data for a smooth, continuous plot
    primes = np.array(list(sympy.primerange(0, limit + 20))) # Get extra primes for mapping
    # Generate a high-resolution set of x-coordinates
    x_continuous = np.linspace(2, limit, 4000)
    
    try:
        # For polar plots, the radius should be non-negative
        r_continuous = np.abs(func(x_continuous))
    except Exception as e:
        print(f"  -> ❌ Error evaluating '{func_str}'. Skipping. (Reason: {e})")
        return

    # 3. Create the side-by-side plot structure
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(20, 9))
    fig.suptitle(f'Radial Comparison for r = |{func_str}|', fontsize=20)

    # --- Plot 1: Prime Landmark Spiral (Warped Angle) ---
    ax1.set_title('Prime Landmark Spiral (Warped Angle)', va='bottom', pad=20)
    theta_warped = map_to_prime_angle(x_continuous, primes, rotations)
    ax1.plot(theta_warped, r_continuous, color='darkviolet', linewidth=1)
    
    # Overlay prime landmarks to show their even angular spacing
    primes_in_range = primes[primes <= limit]
    theta_prime_landmarks = map_to_prime_angle(primes_in_range, primes, rotations)
    ax1.scatter(theta_prime_landmarks, np.abs(func(primes_in_range)), c='orangered', s=40, label='Primes', zorder=5)
    
    # --- Plot 2: Standard Spiral (Linear Angle) ---
    ax2.set_title('Standard Spiral (Linear Angle)', va='bottom', pad=20)
    total_angle = 2 * np.pi * rotations
    theta_standard = (x_continuous / limit) * total_angle
    ax2.plot(theta_standard, r_continuous, color='darkviolet', linewidth=1)
    
    # Overlay primes to show their "bunching up"
    theta_standard_primes = (primes_in_range / limit) * total_angle
    ax2.scatter(theta_standard_primes, np.abs(func(primes_in_range)), c='orangered', s=40, label='Primes', zorder=5)
    
    # 4. Finalize and Save
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    filename = sanitize_filename(f'SpiralCompare_{func_str}')
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=120)
    print(f"  -> ✅ Spiral comparison graph saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'spiral_comparison_plots'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ["x", "log(x)*10", "sin(x/5)*x", "20 + x%13"]
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
    except Exception:
        print(f"Error reading '{INPUT_FILE}'.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 🌌 Prime Landmark Spiral Plotter ---")
    while True:
        try:
            limit = int(input("Enter the upper numerical limit (e.g., 200): "))
            if limit < 3:
                print("Please enter a limit of 3 or higher.")
                continue
            rotations = int(input("Enter the number of spiral rotations (e.g., 5): "))
            break
        except ValueError:
            print("Invalid input.")
            
    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        plot_spiral_comparison(func_str, limit, rotations, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")