# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v05_3d_function_plots.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v5.py   (last edited 2025-08-22)
# What this script does  :: 3D versions of the function plots (prime_3d_graphs/).
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Important: This enables 3D plotting
import numpy as np
import sympy
import os
import re
import ast

def sanitize_filename(text):
    """Converts a string into a valid and safe filename."""
    s = text.replace('**', '_pow_').replace('*', '_mul_').replace('/', '_div_')
    s = re.sub(r'[^a-zA-Z0-9_\-]', '', s)
    return s[:100] + '.png'

def plot_3d_and_save(x_data, y_data, z_data, z_axis_label, title, filename, output_folder):
    """
    Creates a 3D plot with customized labels and saves it to a file.
    """
    print(f"Generating 3D plot for: '{title}'...")
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Create a scatter plot with a color map based on the Z value
    # This makes high and low values easy to spot.
    scatter = ax.scatter(x_data, y_data, z_data, c=z_data, cmap='viridis', marker='o', s=25)
    
    # Add a color bar to show the mapping of colors to Z values
    fig.colorbar(scatter, ax=ax, shrink=0.6, label=z_axis_label)

    # Set the labels for each axis
    ax.set_xlabel('\nPrime Index (n)', linespacing=2)
    ax.set_ylabel('\nPrime Value (pₙ)', linespacing=2)
    ax.set_zlabel(f'\n{z_axis_label}', linespacing=2)
    ax.set_title(title, fontsize=16, pad=20)
    
    # Set a good viewing angle
    ax.view_init(elev=20, azim=-65)
    
    # Save the Figure
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=120) # Use higher DPI for better image quality
    print(f"  -> ✅ 3D Graph saved as: '{output_path}'")
    plt.close(fig)

# --- Main execution block ---
if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'prime_3d_graphs'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file with examples.")
        default_functions = ['log(x)', 'x**0.5', 'x % 13']
        with open(INPUT_FILE, 'w') as f:
            f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f:
            functions_to_plot = ast.literal_eval(f.read())
        if not isinstance(functions_to_plot, list): raise TypeError
    except Exception:
        print(f"Error reading '{INPUT_FILE}'. Please ensure it's a valid list of strings.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("--- 🧊 3D Prime Plotter ---")
    print(f"Graphs will be saved in the '{OUTPUT_FOLDER}' directory.")
    print("-" * 35)

    while True:
        try:
            user_limit = int(input("Enter the upper limit for the primes (e.g., 1000): "))
            if len(list(sympy.primerange(2, user_limit + 1))) < 2:
                 print("Not enough primes found. Please choose a larger limit.")
                 continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
    
    # --- Ask user to choose the Z-axis variable ---
    print("\nWhat should be plotted on the Z-axis?")
    print("  1. A function f(pₙ) from the functions.txt file")
    print("  2. The gap to the next prime (pₙ₊₁ - pₙ)")
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice in ['1', '2']: break
        print("Invalid choice. Please enter 1 or 2.")
    
    print("\n🚀 Starting batch process...")
    primes = np.array(list(sympy.primerange(2, user_limit + 1)))

    # --- Process based on user's choice ---
    if choice == '1':
        # Mode 1: Loop through functions from functions.txt
        for func_str in functions_to_plot:
            try:
                x = sympy.symbols('x')
                expr = sympy.sympify(func_str)
                f = sympy.lambdify(x, expr, 'numpy')

                z_data = f(primes)
                if np.iscomplexobj(z_data):
                    print(f"  -> ⚠️ Warning: '{func_str}' produced complex numbers. Plotting real part.")
                    z_data = np.real(z_data)

                plot_3d_and_save(
                    x_data=np.arange(len(primes)),
                    y_data=primes,
                    z_data=z_data,
                    z_axis_label=f'f(pₙ) = {func_str}',
                    title=f'3D Plot for f(pₙ) = {func_str}',
                    filename=sanitize_filename(f'3D_func_{func_str}'),
                    output_folder=OUTPUT_FOLDER
                )
            except Exception as e:
                print(f"  -> ❌ Error processing '{func_str}'. Skipping. (Reason: {e})")

    elif choice == '2':
        # Mode 2: Plot prime gaps
        prime_gaps = np.diff(primes)
        
        plot_3d_and_save(
            x_data=np.arange(len(prime_gaps)), # Index
            y_data=primes[:-1], # Prime value corresponding to each gap
            z_data=prime_gaps, # The gap value
            z_axis_label='Prime Gap (pₙ₊₁ - pₙ)',
            title='3D Plot of Prime Gaps',
            filename='3D_prime_gaps.png',
            output_folder=OUTPUT_FOLDER
        )
            
    print("\n✨ Batch process complete!")