# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v08_composite_squeeze_comparison.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v8.py   (last edited 2025-08-22)
# What this script does  :: Squeeze plot vs standard plot.
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

def generate_squeeze_data(func, limit):
    """
    Generates data for the Composite Squeeze Plot.
    Primes are at integer x-coordinates, composites are squeezed in between.
    """
    primes = list(sympy.primerange(0, limit + 1))
    prime_data = {'x': [], 'y': [], 'number': []}
    composite_data = {'x': [], 'y': [], 'number': []}

    for i in range(len(primes) - 1):
        p_current, p_next = primes[i], primes[i+1]
        
        # Add the prime's data point at the integer index 'i'
        prime_data['x'].append(i)
        prime_data['y'].append(func(p_current))
        prime_data['number'].append(p_current)
        
        # Find and map composites in the gap
        composites_in_gap = [n for n in range(p_current + 1, p_next)]
        k = len(composites_in_gap)
        if k > 0:
            for j, comp in enumerate(composites_in_gap):
                x_coord = i + (j + 1) / (k + 1) # Squeeze into the (i, i+1) interval
                composite_data['x'].append(x_coord)
                composite_data['y'].append(func(comp))
                composite_data['number'].append(comp)

    # Add the last prime
    last_prime_index = len(primes) - 1
    last_prime = primes[-1]
    prime_data['x'].append(last_prime_index)
    prime_data['y'].append(func(last_prime))
    prime_data['number'].append(last_prime)
            
    return prime_data, composite_data, primes

def plot_side_by_side(func_str, limit, output_folder):
    """
    Creates and saves a static, side-by-side comparison PNG for a given function.
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

    # 2. Generate data for both plots
    try:
        squeeze_prime_data, squeeze_comp_data, primes = generate_squeeze_data(func, limit)
        
        # Data for the standard plot
        x_standard = np.arange(2, limit + 1)
        y_standard = func(x_standard)
        
    except Exception as e:
        print(f"  -> ❌ Error evaluating '{func_str}'. Skipping. (Reason: {e})")
        return

    # 3. Create the side-by-side plot structure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    fig.suptitle(f'Comparison for y = {func_str}', fontsize=20)

    # --- Plot 1: Composite Squeeze Plot ---
    ax1.set_title('Composite Squeeze Plot', fontsize=14)
    ax1.scatter(squeeze_comp_data['x'], squeeze_comp_data['y'], c='gray', s=15, marker='x', label='Composites')
    ax1.plot(squeeze_prime_data['x'], squeeze_prime_data['y'], color='orangered', marker='o', markersize=7, linestyle='-', label='Primes')
    ax1.set_xticks(range(len(primes)))
    ax1.set_xticklabels(primes, rotation=45, ha='right')
    ax1.set_xlabel('Prime Number Landmarks')
    ax1.set_ylabel('Function Value')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()
    
    # --- Plot 2: Standard Number Line Plot ---
    ax2.set_title('Standard Number Line Plot', fontsize=14)
    prime_set = set(primes)
    standard_primes_x = [n for n in x_standard if n in prime_set]
    standard_primes_y = func(np.array(standard_primes_x))
    standard_comps_x = [n for n in x_standard if n not in prime_set]
    standard_comps_y = func(np.array(standard_comps_x))

    ax2.scatter(standard_comps_x, standard_comps_y, c='gray', s=15, marker='x', label='Composites')
    ax2.plot(standard_primes_x, standard_primes_y, color='orangered', marker='o', markersize=7, linestyle='-', label='Primes')
    ax2.set_xlabel('Standard Number Line')
    ax2.set_ylabel('Function Value')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    
    # 4. Finalize and Save
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust for suptitle
    filename = sanitize_filename(f'Compare_{func_str}')
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=120)
    print(f"  -> ✅ Static comparison graph saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'static_comparison_plots'
    
    # Use the valid function list we created
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = [
            "x**0.5",
            "sin(x/3)",
            "log(x)",
            "Abs(x % 7 - 3)",
            "diff(x*sin(x))"
        ]
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
    except Exception:
        print(f"Error reading '{INPUT_FILE}'. Please ensure it's a valid list.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 📜 Static Side-by-Side Plotter ---")
    while True:
        try:
            user_limit = int(input("Enter the upper numerical limit (e.g., 100): "))
            break
        except ValueError:
            print("Invalid input.")
            
    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        plot_side_by_side(func_str, user_limit, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")