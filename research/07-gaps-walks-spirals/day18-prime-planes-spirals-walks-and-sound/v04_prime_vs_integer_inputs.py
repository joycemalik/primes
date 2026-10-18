# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v04_prime_vs_integer_inputs.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v4.py   (last edited 2025-08-22)
# What this script does  :: Compares f on prime inputs with f on integer inputs.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import sympy
import os
import re
import ast # Used to safely evaluate the list of functions from the text file

def sanitize_filename(func_str):
    """Converts a function string into a valid and safe filename."""
    s = func_str.replace('**', '_pow_').replace('*', '_mul_').replace('/', '_div_')
    s = re.sub(r'[^a-zA-Z0-9_\-]', '', s)
    return s[:100] + '.png'

def plot_and_save(func_str, prime_limit, output_folder):
    """
    Creates a comparison plot of a function evaluated at prime numbers vs. integers,
    and saves it to a file.
    """
    print(f"Processing function: '{func_str}'...")
    
    # --- 1. Safely Parse the Mathematical Function ---
    try:
        x = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        # Create a fast, callable function that uses the numpy library
        f = sympy.lambdify(x, expr, 'numpy')
    except (sympy.SympifyError, SyntaxError):
        print(f"  -> ❌ Error: Could not parse '{func_str}'. Skipping.")
        return

    # --- 2. Generate the Prime and Integer Datasets ---
    primes = np.array(list(sympy.primerange(2, prime_limit + 1)))
    num_points = len(primes)
    
    if num_points < 2:
        return # This case is handled in the main block

    # Create a corresponding sequence of integers (1, 2, 3, ...) of the same length
    integers = np.arange(1, num_points + 1)
    
    # The x-axis is the index 'n' of the number in its sequence (e.g., n-th prime, n-th integer)
    x_indices = np.arange(num_points)

    # --- 3. Evaluate Function for Both Sequences with Error Handling ---
    try:
        y_values_prime = f(primes)
        if np.iscomplexobj(y_values_prime):
            print(f"  -> ⚠️ Warning (Primes): Function produced complex numbers. Plotting real part.")
            y_values_prime = np.real(y_values_prime)
    except Exception as e:
        print(f"  -> ❌ Error evaluating on primes for '{func_str}'. Skipping. (Reason: {e})")
        return
        
    try:
        # This context manager treats numpy warnings (like division by zero) as errors
        with np.errstate(all='raise'):
             y_values_integer = f(integers)
        if np.iscomplexobj(y_values_integer):
            print(f"  -> ⚠️ Warning (Integers): Function produced complex numbers. Plotting real part.")
            y_values_integer = np.real(y_values_integer)
    except Exception as e:
        print(f"  -> ❌ Error evaluating on integers for '{func_str}'. Skipping. (Reason: {e})")
        # This is common for functions like '1/log(x)', which fails at x=1.
        return

    # --- 4. Create and Customize the Comparison Plot ---
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot the line for INTEGER inputs
    ax.plot(x_indices, y_values_integer, marker='.', linestyle='--', markersize=4, 
            color='dodgerblue', label=f'Integer Inputs: f(n)')

    # Plot the line for PRIME inputs
    ax.plot(x_indices, y_values_prime, marker='.', linestyle='-', markersize=5, 
            color='orangered', label=f'Prime Inputs: f(pₙ)')
            
    # --- 5. Add Labels, Title, and Legend ---
    ax.set_xlabel('Sequence Index (n)')
    ax.set_ylabel('Function Value')
    ax.set_title(f"Comparison for y = {func_str}\n(Prime Inputs vs. Integer Inputs)")
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend() # This displays the labels for each line
    plt.tight_layout()

    # --- 6. Save the Figure and Free Memory ---
    filename = sanitize_filename(func_str)
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path)
    print(f"  -> ✅ Comparison graph saved as: '{output_path}'")
    plt.close(fig)

# --- Main execution block (remains the same) ---
if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'prime_plane_graphs'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file with examples.")
        default_functions = [
            'x', 'x**0.5', '1/x', 'log(x)', 'x / log(x)', 
            'sin(x)', 'cos(x/10)', 'x * sin(x/20)', 'sin(log(x))', 'x % 13'
        ]
        with open(INPUT_FILE, 'w') as f:
            f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f:
            content = f.read()
            functions_to_plot = ast.literal_eval(content)
        if not isinstance(functions_to_plot, list):
            raise TypeError("Content is not a list.")
    except Exception as e:
        print(f"Error reading '{INPUT_FILE}': {e}")
        print("Please ensure the file contains a valid Python list of strings, e.g., ['x**2', 'sin(x)']")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("--- 📊 Prime Plane Comparison Plotter ---")
    print(f"Reading functions from '{INPUT_FILE}'")
    print(f"Graphs will be saved in the '{OUTPUT_FOLDER}' directory.")
    print("-" * 35)

    while True:
        try:
            user_limit = int(input("Enter the upper limit for the primes for all functions (e.g., 200): "))
            if len(list(sympy.primerange(2, user_limit + 1))) < 2:
                 print(f"Not enough primes found up to {user_limit}. Please choose a larger limit.")
                 continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print("\n🚀 Starting batch process...")
    for func in functions_to_plot:
        plot_and_save(func, user_limit, OUTPUT_FOLDER)
    
    print("\n✨ Batch process complete!")