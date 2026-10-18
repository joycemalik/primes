# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v10_continuous_squeeze_comparison.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v10.py   (last edited 2025-08-22)
# What this script does  :: Continuous squeeze comparison.
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

def map_to_squeeze_coordinates(x_coords, primes):
    """
    Maps a set of standard x-coordinates to their "squeezed" equivalents.
    This is a vectorized function for speed.
    """
    # For each x, find the index of the prime that comes just before it.
    # np.searchsorted finds the insertion point, so we subtract 1.
    prime_indices = np.searchsorted(primes, x_coords, side='right') - 1

    # Get the bracketing primes for each x coordinate
    p_n = primes[prime_indices]
    p_next = primes[prime_indices + 1]
    
    # Linearly interpolate each x within its prime gap [p_n, p_next]
    # to the corresponding index gap [n, n+1].
    fraction_through_gap = (x_coords - p_n) / (p_next - p_n)
    
    squeezed_x = prime_indices + fraction_through_gap
    return squeezed_x

def plot_side_by_side_continuous(func_str, limit, output_folder):
    """
    Creates a static, side-by-side comparison of a continuous function
    on a standard axis and a prime-squeezed axis.
    """
    print(f"Processing function: '{func_str}'...")
    
    # 1. Parse the function string
    try:
        x_sym = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        func = sympy.lambdify(x_sym, expr, 'numpy')
    except Exception as e:
        print(f"  -> ❌ Error parsing '{func_str}'. Skipping. (Reason: {e})")
        return

    # 2. Generate data for a smooth, continuous plot
    primes = np.array(list(sympy.primerange(0, limit + 2))) # Get one extra prime for mapping
    # Create a high-resolution set of x-coordinates for a smooth line
    x_continuous = np.linspace(primes[0], primes[-2], 2000) # Plot up to the user's limit
    
    try:
        y_continuous = func(x_continuous)
    except Exception as e:
        print(f"  -> ❌ Error evaluating '{func_str}'. Skipping. (Reason: {e})")
        return

    # 3. Map the standard coordinates to the squeezed coordinates
    x_squeezed = map_to_squeeze_coordinates(x_continuous, primes)

    # 4. Create the plot structure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    fig.suptitle(f'Continuous Function y = {func_str}', fontsize=20)

    # --- Plot 1: Composite Squeeze Plot (Warped X-Axis) ---
    ax1.set_title('"Squeezed" Prime Number Scale', fontsize=14)
    ax1.plot(x_squeezed, y_continuous, color='darkviolet', label='Continuous f(x)')
    # Overlay prime points to show the landmarks
    prime_indices_for_plot = np.arange(len(primes)-1)
    ax1.plot(prime_indices_for_plot, func(primes[:-1]), 'o', color='orangered', markersize=8, label='Value at Primes')
    
    ax1.set_xticks(prime_indices_for_plot)
    ax1.set_xticklabels(primes[:-1], rotation=45, ha='right')
    ax1.set_xlabel('Prime Number Landmarks')
    ax1.set_ylabel('Function Value')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()
    ax1.set_xlim(left=0, right=len(primes)-2)

    # --- Plot 2: Standard Number Line Plot (True Scale) ---
    ax2.set_title('Standard Linear Scale', fontsize=14)
    ax2.plot(x_continuous, y_continuous, color='darkviolet', label='Continuous f(x)')
    # Overlay prime points to show where they fall on the standard line
    ax2.plot(primes[:-1], func(primes[:-1]), 'o', color='orangered', markersize=8, label='Value at Primes')
    
    ax2.set_xlabel('Standard Number Line')
    ax2.set_ylabel('Function Value')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    ax2.set_xlim(left=0, right=limit)
    
    # 5. Finalize and Save
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    filename = sanitize_filename(f'ContinuousCompare_{func_str}')
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=120)
    print(f"  -> ✅ Continuous comparison graph saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'continuous_comparison_plots'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ["sin(x/5) * (x**0.5)", "log(x)", "x % 11", "diff(x**2 * sin(x))"]
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
    except Exception:
        print(f"Error reading '{INPUT_FILE}'.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 📜 Continuous Scale Comparison Plotter ---")
    while True:
        try:
            user_limit = int(input("Enter the upper numerical limit (e.g., 100): "))
            break
        except ValueError:
            print("Invalid input.")
            
    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        plot_side_by_side_continuous(func_str, user_limit, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")