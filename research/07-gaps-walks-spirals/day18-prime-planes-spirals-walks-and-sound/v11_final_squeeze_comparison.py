# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v11_final_squeeze_comparison.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v11.py   (last edited 2025-08-22)
# What this script does  :: Final squeeze comparison.
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
    Maps a set of standard integer coordinates to their "squeezed" equivalents.
    """
    # Create a mapping from a number to its squeezed x-coordinate
    coord_map = {}
    
    for i in range(len(primes) - 1):
        p_current, p_next = primes[i], primes[i+1]
        
        # Primes land on integer indices
        coord_map[p_current] = i
        
        # Squeeze composites into the (i, i+1) interval
        composites_in_gap = [n for n in range(p_current + 1, p_next)]
        k = len(composites_in_gap)
        if k > 0:
            for j, comp in enumerate(composites_in_gap):
                coord_map[comp] = i + (j + 1) / (k + 1)

    # Add the last prime
    coord_map[primes[-1]] = len(primes) - 1
    
    # Return the squeezed coordinates in the correct order
    return np.array([coord_map[x] for x in x_coords])


def plot_final_comparison(func_str, limit, output_folder):
    """
    Creates the definitive static, side-by-side comparison PNG, plotting all integer points.
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

    # 2. Generate data for ALL integers from 2 to limit
    primes_list = list(sympy.primerange(0, limit + 2))
    primes_array = np.array(primes_list)
    
    x_standard = np.arange(2, limit + 1) # All integers to be plotted
    
    try:
        y_standard = func(x_standard) # Y-values are THE SAME for both plots
    except Exception as e:
        print(f"  -> ❌ Error evaluating '{func_str}'. Skipping. (Reason: {e})")
        return

    # 3. Get squeezed X-coordinates for these integers
    x_squeezed = map_to_squeeze_coordinates(x_standard, primes_array)

    # 4. Create the side-by-side plot structure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    fig.suptitle(f'Comparison for y = {func_str}', fontsize=20)
    
    # Separate numbers into primes and composites for coloring
    prime_set = set(primes_list)
    is_prime_mask = np.array([i in prime_set for i in x_standard])

    # --- Plot 1: Composite Squeeze Plot ---
    ax1.set_title('"Squeezed" Prime Number Scale', fontsize=14)
    # Plot the connecting line for ALL numbers
    ax1.plot(x_squeezed, y_standard, color='black', alpha=0.4, linewidth=1, label='_nolegend_')
    # Overlay markers for composites
    ax1.scatter(x_squeezed[~is_prime_mask], y_standard[~is_prime_mask], c='gray', s=20, marker='x', label='Composites')
    # Overlay markers for primes
    ax1.scatter(x_squeezed[is_prime_mask], y_standard[is_prime_mask], c='orangered', s=60, marker='o', label='Primes', zorder=5)

    ax1.set_xticks(range(len(primes_list)-1))
    ax1.set_xticklabels(primes_list[:-1], rotation=45, ha='right')
    ax1.set_xlabel('Prime Number Landmarks')
    ax1.set_ylabel('Function Value')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()
    
    # --- Plot 2: Standard Number Line Plot ---
    ax2.set_title('Standard Linear Scale', fontsize=14)
    # Plot the connecting line for ALL numbers
    ax2.plot(x_standard, y_standard, color='black', alpha=0.4, linewidth=1, label='_nolegend_')
    # Overlay markers for composites
    ax2.scatter(x_standard[~is_prime_mask], y_standard[~is_prime_mask], c='gray', s=20, marker='x', label='Composites')
    # Overlay markers for primes
    ax2.scatter(x_standard[is_prime_mask], y_standard[is_prime_mask], c='orangered', s=60, marker='o', label='Primes', zorder=5)

    ax2.set_xlabel('Standard Number Line')
    ax2.set_ylabel('Function Value')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    
    # 5. Finalize and Save
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    filename = sanitize_filename(f'FinalCompare_{func_str}')
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=120)
    print(f"  -> ✅ Final comparison graph saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'final_comparison_plots'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ["x", "x**2", "x**0.5", "sin(x/3)"]
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
    except Exception:
        print(f"Error reading '{INPUT_FILE}'.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 📜 Final Static Comparison Plotter ---")
    while True:
        try:
            user_limit = int(input("Enter the upper numerical limit (e.g., 50): "))
            if user_limit < 3:
                print("Please enter a limit of 3 or higher.")
                continue
            break
        except ValueError:
            print("Invalid input.")
            
    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        plot_final_comparison(func_str, user_limit, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")