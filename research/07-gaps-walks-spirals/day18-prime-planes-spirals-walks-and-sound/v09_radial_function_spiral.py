# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v09_radial_function_spiral.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v9.py   (last edited 2025-08-24)
# What this script does  :: Radial function spirals (radial_plots/).
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

def plot_prime_radial(func_str, limit, plot_type, output_folder):
    """
    Creates and saves a static radial plot based on the chosen type.
    """
    print(f"Processing '{func_str}' for a '{plot_type}' plot...")
    
    # 1. Parse the function string
    try:
        x_sym = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        func = sympy.lambdify(x_sym, expr, 'numpy')
    except Exception as e:
        print(f"  -> ❌ Error parsing function. Skipping. (Reason: {e})")
        return

    # 2. Generate prime data
    try:
        primes = np.array(list(sympy.primerange(2, limit + 1)))
        indices = np.arange(len(primes))
        function_values = func(primes)
    except Exception as e:
        print(f"  -> ❌ Error evaluating function. Skipping. (Reason: {e})")
        return

    # 3. Create the polar plot structure
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='polar')
    ax.set_facecolor('black') # Dark background often looks good for spirals
    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    # 4. Draw the plot based on the selected type
    if plot_type == 'function_spiral':
        # Angle is the index, Radius is the function value
        theta = indices * (np.pi / 8) # Spreading the angle
        r = function_values
        
        ax.plot(theta, r, color='cyan', marker='o', markersize=4, linestyle='-')
        ax.set_title(f'Function Spiral for y = {func_str}', color='white', pad=20)
        # The 'r' grid shows the function's value
        
    elif plot_type == 'distribution_spiral':
        # Angle uses the Golden Angle for even distribution, Radius is the prime value
        golden_angle = np.pi * (3. - np.sqrt(5.))
        theta = indices * golden_angle
        r = primes
        colors = function_values
        
        scatter = ax.scatter(theta, r, c=colors, cmap='viridis', s=25)
        plt.colorbar(scatter, ax=ax, pad=0.1, label=f'f(pₙ) = {func_str}')
        ax.set_title(f'Prime Distribution Spiral\nColor mapped to y = {func_str}', color='white', pad=20)
        # The 'r' grid shows the prime's magnitude

    # 5. Finalize and Save
    filename = sanitize_filename(f'Radial_{plot_type}_{func_str}')
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='black')
    print(f"  -> ✅ Radial plot saved as: '{output_path}'")
    plt.close(fig)


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'radial_plots'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ["x**0.5", "log(x)", "x % 17"]
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
    except Exception:
        print(f"Error reading '{INPUT_FILE}'. Please ensure it's a valid list.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 🌀 Prime Spiral Plotter ---")
    
    # Get user input for limit
    while True:
        try:
            user_limit = int(input("Enter the upper numerical limit for primes (e.g., 1000): "))
            break
        except ValueError:
            print("Invalid input.")
            
    # Get user input for plot type
    print("\nChoose the type of radial plot to generate:")
    print("  1. Function Spiral (Radius = function value)")
    print("  2. Prime Distribution Spiral (Radius = prime value, Color = function value)")
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            plot_type_choice = 'function_spiral'
            break
        elif choice == '2':
            plot_type_choice = 'distribution_spiral'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
            
    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        plot_prime_radial(func_str, user_limit, plot_type_choice, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")