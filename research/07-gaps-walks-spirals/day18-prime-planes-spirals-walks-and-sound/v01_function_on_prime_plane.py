# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v01_function_on_prime_plane.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v1.py   (last edited 2025-08-22)
# What this script does  :: Plots y = f(x) with the x-axis made of primes (2, 3, 5, 7, ...).
# ----------------------------------------------------------------------------
# main_script.py
import matplotlib.pyplot as plt
import numpy as np
import sympy

def get_primes_up_to(limit):
    """
    Generates a list of prime numbers up to a given limit using sympy.
    """
    # sympy.primerange is an efficient generator for primes in a range.
    return list(sympy.primerange(2, limit + 1))

def plot_function_on_prime_plane(func_str, prime_limit):
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
        # sympify() converts the string into a symbolic expression.
        expr = sympy.sympify(func_str)
        # lambdify() converts the symbolic expression into a fast, callable function.
        # We use the 'numpy' backend to allow the function to process arrays efficiently.
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
    y_values = f(primes)

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
    plt.show()

if __name__ == '__main__':
    print("--- Prime Plane Function Plotter ---")
    print("Plots a function where the x-axis uses prime numbers with uniform spacing.")
    print("Example functions: 'x', 'x**0.5', '1/log(x)', 'sin(x/10)'")
    print("-" * 34)

    # Get user input for the function
    user_function = input("Enter a function in terms of 'x': ")
    
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

    plot_function_on_prime_plane(user_function, user_limit)