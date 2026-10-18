# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v13_radial_angle_by_smallest_factor.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v13.py   (last edited 2025-08-22)
# What this script does  :: Radial plot with angle set by the smallest prime factor.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import sympy
import os
import re
import ast

def sanitize_filename(text):
    """Converts a string into a valid PNG filename."""
    s = text.replace('**', '_pow_').replace('*', '_mul_').replace('/', '_div_')
    s = re.sub(r'[^a-zA-Z0-9_\-]', '', s)
    return s[:100] + '.png'

def smallest_prime_factor(n):
    """Returns the smallest prime factor of a number n."""
    n = int(n)
    if n < 2:
        return None
    if n % 2 == 0:
        return 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return d
        d += 2
    return n

# FIX #1: Added 'limit' as an argument to the function definition.
def angle_by_smallest_prime(n, prime_categories, limit):
    """Determines the angle based on the smallest prime factor."""
    spf = smallest_prime_factor(n)
    if spf is None:
        return None
    
    # Check if the smallest prime factor is in our predefined categories
    if spf in prime_categories:
        idx = prime_categories.index(spf)
        angle_start = (2 * np.pi / len(prime_categories)) * idx
    # If not, it belongs to the 'other' category
    else:
        idx = len(prime_categories)
        angle_start = (2 * np.pi / len(prime_categories)) * idx

    # Normalize the number's position within its category to create a smooth progression
    segment_width = (2 * np.pi / (len(prime_categories) + 1))
    
    # A simple normalization based on the number's value relative to the limit
    normalized_pos = (n / limit) * segment_width
    
    return angle_start + normalized_pos


def plot_radial_comparison(func_str, limit, output_folder):
    """Creates a side-by-side comparison of radial plots."""
    print(f"Processing function: '{func_str}'...")

    try:
        x_sym = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        func = sympy.lambdify(x_sym, expr, 'numpy')
    except Exception as e:
        print(f"  -> ❌ Error parsing '{func_str}'. Skipping. (Reason: {e})")
        return

    num_points = 2000
    x = np.linspace(2, limit, num_points)
    
    try:
        r = np.abs(func(x)) # Radius should be non-negative
    except Exception as e:
        print(f"  -> ❌ Error evaluating '{func_str}'. Skipping. (Reason: {e})")
        return

    # Define categories for smallest prime factor
    prime_categories = [2, 3, 5, 7, 11, 13] 
    
    # FIX #2: Passed 'limit' when calling the function.
    theta_prime = np.array([angle_by_smallest_prime(val, prime_categories, limit) for val in x])
     
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(20, 9))
    fig.suptitle(f'Radial Comparison for y = {func_str}', fontsize=20)

    # Left Plot: Prime-Inflected Radial Plot
    ax1.set_title('Prime-Inflected Plot (Angle by Smallest Prime Factor)', va='bottom', pad=20)
    ax1.plot(theta_prime, r, color='mediumseagreen', linewidth=1)
    # Set radial tick labels to show different prime categories
    num_categories = len(prime_categories) + 1 # Plus one for 'other' primes
    ax1.set_xticks(np.linspace(0, 2 * np.pi, num_categories, endpoint=False))
    ax1.set_xticklabels([str(p) for p in prime_categories] + ['Other'])
    
    # Right Plot: Standard Radial Plot
    theta_standard = np.linspace(0, 2 * np.pi, num_points) # Angle directly proportional to the number's progression
    ax2.set_title('Standard Radial Plot (Angle Proportional to Number)', va='bottom', pad=20)
    ax2.plot(theta_standard, r, color='cornflowerblue', linewidth=1)

    # Save the figure
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    filename = sanitize_filename(f'RadialCompare_{func_str}')
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=120)
    print(f"  -> ✅ Radial comparison graph saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'radial_comparison_plots'

    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ["x", "log(x)", "sin(x/10) * x", "1/x"]
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))

    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
    except Exception:
        print(f"Error reading '{INPUT_FILE}'.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("--- 🌌 Prime-Inflected Radial Plotter ---")
    while True:
        try:
            limit = int(input("Enter the upper numerical limit (e.g., 100): "))
            if limit < 4:
                print("Please enter a limit of 4 or higher for better plots.")
                continue
            break
        except ValueError:
            print("Invalid input.")

    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        plot_radial_comparison(func_str, limit, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")