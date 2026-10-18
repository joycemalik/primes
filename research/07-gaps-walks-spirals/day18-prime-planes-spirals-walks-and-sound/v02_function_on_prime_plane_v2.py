# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v02_function_on_prime_plane_v2.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v2.py   (last edited 2025-08-22)
# What this script does  :: Second version of the prime-plane plot.
# ----------------------------------------------------------------------------
# main_script.py
import matplotlib.pyplot as plt
import numpy as np
import sympy
import ast
import os

def get_primes_up_to(limit):
    """
    Generates a list of prime numbers up to a given limit using sympy.
    """
    # sympy.primerange is an efficient generator for primes in a range.
    return list(sympy.primerange(2, limit + 1))

def plot_function_on_prime_plane(func_str, prime_limit, save_folder=None):
    """
    Parses a function string and plots it on a plane where the x-axis
    is composed of uniformly spaced prime numbers.

    Args:
        func_str (str): The mathematical function in terms of 'x'.
        prime_limit (int): The upper limit for prime numbers on the x-axis.
    """
    # --- 1. Safely Parse the Mathematical Function ---
    try:
        x = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        f = sympy.lambdify(x, expr, 'numpy')
    except (sympy.SympifyError, SyntaxError):
        print(f"Error: Invalid function string '{func_str}'.")
        print("Please use Python/SymPy syntax (e.g., 'x**2', 'sin(x)', '1/x').")
        return

    # --- 2. Generate the Prime Numbers ---
    primes = np.array(get_primes_up_to(prime_limit))
    
    if len(primes) < 2:
        print(f"Error: Not enough primes found up to {prime_limit}. Please choose a larger limit.")
        return

    # --- 3. Prepare Data for Plotting ---
    # The actual positions on the x-axis are the indices [0, 1, 2, ...].
    # This creates the required uniform spacing for the primes.
    x_indices = np.arange(len(primes))

    # The y-values are the result of applying the function to each prime number.
    try:
        y_values = f(primes)
        # If output is complex, take real part and warn
        if np.iscomplexobj(y_values):
            print(f"Warning: Function '{func_str}' produced complex values. Using real part only.")
            y_values = np.real(y_values)
    except Exception as e:
        print(f"Error evaluating function '{func_str}' on primes: {e}")
        return

    # --- 4. Create the Plot ---
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(x_indices, y_values, marker='o', linestyle='-', markersize=4, color='b')

    # --- 5. Customize the Axes to Create the "Prime Plane" ---
    # Set the tick positions to the uniform indices...
    ax.set_xticks(x_indices)
    # ...but set the labels for those ticks to the actual prime numbers.
    # This is the key to creating the prime plane visualization.
    ax.set_xticklabels(primes, rotation=45, ha='right')
    
    # Make ticks less crowded if there are many primes
    if len(primes) > 40:
        ax.xaxis.set_major_locator(plt.MaxNLocator(25)) 

    # --- 6. Add Labels and Final Touches ---
    ax.set_xlabel('Prime Numbers (p)')
    ax.set_ylabel(f'f(p) = {func_str}')
    ax.set_title(f'Function y = {func_str} on a Prime Plane')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    if save_folder:
        # Save the plot to the folder
        safe_func = func_str.replace('/', '_').replace('*', '_').replace('**', 'pow').replace(' ', '')
        filename = f"prime_plane_{safe_func}.png"
        filepath = os.path.join(save_folder, filename)
        plt.savefig(filepath)
        print(f"Saved: {filepath}")
        plt.close(fig)
    else:
        plt.show()

if __name__ == '__main__':
    print("--- Prime Plane Function Plotter ---")
    print("Plots multiple functions from functions.txt, saving each graph to 'prime_graphs'.")
    print("Example functions: 'x', 'x**0.5', '1/log(x)', 'sin(x/10)'")
    print("-" * 34)

    # Read all functions from functions.txt
    with open('functions.txt', 'r') as f:
        func_list = ast.literal_eval(f.read())

    # Get user input for the prime number limit
    while True:
        try:
            user_limit = int(input("Enter the upper limit for the primes (e.g., 100): "))
            if user_limit < 3:
                print("Please enter a limit of 3 or higher to get at least two primes.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    save_folder = 'prime_graphs'
    os.makedirs(save_folder, exist_ok=True)

    for func_str in func_list:
        print(f"Plotting: {func_str}")
        plot_function_on_prime_plane(func_str, user_limit, save_folder=save_folder)