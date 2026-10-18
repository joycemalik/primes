# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v03_prime_plane_batch_plots.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v3.py   (last edited 2025-08-22)
# What this script does  :: Batch prime-plane plots saved to prime_plane_graphs/.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import sympy
import os
import re
import ast # Used to safely evaluate the list of functions from the text file

def sanitize_filename(func_str):
    """Converts a function string into a valid and safe filename."""
    # Replace common operators with words to make filenames more readable
    s = func_str.replace('**', '_pow_').replace('*', '_mul_').replace('/', '_div_')
    
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    s = re.sub(r'[^a-zA-Z0-9_\-]', '', s)
    
    # Trim to a reasonable length and add the .png extension
    return s[:100] + '.png'

def plot_and_save(func_str, prime_limit, output_folder):
    """
    Parses a function, plots it on the prime plane, and saves it to a file.
    """
    print(f"Processing function: '{func_str}'...")
    
    # --- 1. Safely Parse the Mathematical Function ---
    try:
        x = sympy.symbols('x')
        # THE FIX IS HERE: Removed strict=True to allow for more flexible parsing
        expr = sympy.sympify(func_str) 
        f = sympy.lambdify(x, expr, 'numpy')
    except (sympy.SympifyError, SyntaxError):
        print(f"  -> ❌ Error: Could not parse '{func_str}'. Skipping.")
        return

    # --- 2. Generate Prime Numbers ---
    primes = np.array(list(sympy.primerange(2, prime_limit + 1)))
    
    # --- 3. Prepare Data, Handling Potential Math Errors ---
    x_indices = np.arange(len(primes))
    
    try:
        # Evaluate the function for all primes.
        y_values = f(primes)
        # If the function produces complex numbers (e.g., '(-x)**0.5'),
        # we plot only the real part to keep the graph 2D.
        if np.iscomplexobj(y_values):
            print(f"  -> ⚠️ Warning: Function produced complex numbers. Plotting real part only.")
            y_values = np.real(y_values)
    except (ValueError, ZeroDivisionError, TypeError) as e:
        print(f"  -> ❌ Error: Could not evaluate '{func_str}' for these primes. Skipping. (Reason: {e})")
        return

    # --- 4. Create and Customize the Plot ---
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(x_indices, y_values, marker='.', linestyle='-', markersize=5, color='darkslateblue')

    ax.set_xticks(x_indices)
    ax.set_xticklabels(primes, rotation=45, ha='right')
    
    # Prevent the x-axis from being too crowded with labels
    if len(primes) > 40:
        ax.xaxis.set_major_locator(plt.MaxNLocator(25)) 

    ax.set_xlabel('Prime Numbers (p)')
    ax.set_ylabel(f'f(p) = {func_str}')
    ax.set_title(f'Function y = {func_str} on a Prime Plane')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # --- 5. Save the Figure and Free Memory ---
    filename = sanitize_filename(func_str)
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path)
    print(f"  -> ✅ Graph saved as: '{output_path}'")
    
    # IMPORTANT: Close the figure to free up memory before the next loop iteration
    plt.close(fig)

# --- Main execution block ---
if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'prime_plane_graphs'
    
    # Create a default functions.txt if it doesn't exist to make it easy to start
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file with examples.")
        default_functions = [
            'x', 'x**0.5', '1/x', 'log(x)', 'x / log(x)', 
            'sin(x)', 'cos(x/10)', 'x * sin(x/20)', 'sin(log(x))', 'x % 13'
        ]
        with open(INPUT_FILE, 'w') as f:
            f.write(str(default_functions))
    
    # Read the list of functions from the file
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

    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("--- 📊 Prime Plane Batch Plotter ---")
    print(f"Reading functions from '{INPUT_FILE}'")
    print(f"Graphs will be saved in the '{OUTPUT_FOLDER}' directory.")
    print("-" * 35)

    # Get the single prime limit from the user for all functions
    while True:
        try:
            user_limit = int(input("Enter the upper limit for the primes for all functions (e.g., 200): "))
            if len(list(sympy.primerange(2, user_limit + 1))) < 2:
                 print(f"Not enough primes found up to {user_limit}. Please choose a larger limit.")
                 continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Loop through each function and generate its plot
    print("\n🚀 Starting batch process...")
    for func in functions_to_plot:
        plot_and_save(func, user_limit, OUTPUT_FOLDER)
    
    print("\n✨ Batch process complete!")