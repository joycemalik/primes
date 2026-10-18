# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v19_prime_factor_signature.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v19.py   (last edited 2025-08-22)
# What this script does  :: Prime-factor signature plots (signature_plots/).
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

def plot_prime_signature(func_str, limit, output_folder):
    """
    Creates a Prime Factor Signature plot.
    Each number's position is determined by the vector sum of its prime factors,
    scaled by the function f(x).
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

    # 2. Pre-calculate prime angles
    primes = list(sympy.primerange(2, limit + 1))
    # Use the Golden Angle for visually pleasing, non-overlapping distribution
    golden_angle = np.pi * (3. - np.sqrt(5.))
    prime_angles = {p: i * golden_angle for i, p in enumerate(primes)}

    # 3. Calculate signature for each number
    x_coords, y_coords, colors = [], [], []
    numbers_to_plot = np.arange(2, limit + 1)
    
    try:
        f_values = func(numbers_to_plot)
    except Exception as e:
        print(f"  -> ❌ Error evaluating '{func_str}'. Skipping. (Reason: {e})")
        return

    for i, n in enumerate(numbers_to_plot):
        factor_dict = sympy.factorint(n)
        
        vec_x, vec_y = 0.0, 0.0
        for p, exponent in factor_dict.items():
            if p in prime_angles:
                angle = prime_angles[p]
                vec_x += exponent * np.cos(angle)
                vec_y += exponent * np.sin(angle)
        
        # The function's value scales the signature's magnitude
        scale = f_values[i]
        x_coords.append(vec_x * scale)
        y_coords.append(vec_y * scale)
        colors.append(f_values[i])

    # 4. Create the plot
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_title(f'Prime Factor Signature Plot for f(x) = {func_str}', fontsize=16, pad=20)
    
    # Draw faint lines indicating the direction of the first few primes
    for i in range(min(10, len(primes))):
        p = primes[i]
        angle = prime_angles[p]
        ax.plot([0, np.cos(angle)], [0, np.sin(angle)], color='gray', alpha=0.3, linestyle='--')
        ax.text(np.cos(angle) * 1.05, np.sin(angle) * 1.05, str(p), color='gray', ha='center', va='center')
    
    # Create the scatter plot, coloring points by their function value
    scatter = ax.scatter(x_coords, y_coords, c=colors, cmap='viridis', s=15, alpha=0.8)
    
    ax.set_xlabel('Signature X-Component * f(x)')
    ax.set_ylabel('Signature Y-Component * f(x)')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_aspect('equal', 'box')
    
    # Add a color bar
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('f(x) Value (Color and Magnitude Scale)')
    
    # 5. Finalize and Save
    plt.tight_layout()
    filename = sanitize_filename(f'Signature_{func_str}')
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=150)
    print(f"  -> ✅ Signature graph saved as: '{output_path}'")
    plt.close(fig)

if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'signature_plots'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ["log(x)", "x**0.5", "10", "sin(x/10)+2"]
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
    except Exception:
        print(f"Error reading '{INPUT_FILE}'.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 🧬 Prime Factor Signature Plotter ---")
    while True:
        try:
            limit = int(input("Enter the upper numerical limit (e.g., 1000): "))
            if limit < 3: continue
            break
        except ValueError: print("Invalid input.")
            
    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        plot_prime_signature(func_str, limit, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")