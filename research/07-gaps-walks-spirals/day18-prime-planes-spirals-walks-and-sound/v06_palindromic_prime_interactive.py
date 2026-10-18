# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v06_palindromic_prime_interactive.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v6.py   (last edited 2025-08-22)
# What this script does  :: Interactive plots over palindromic primes and other sequences.
# ----------------------------------------------------------------------------
import plotly.graph_objects as go
import sympy
import numpy as np
import os
import re
import ast

def is_palindrome(n):
    """Checks if a number is a palindrome."""
    return str(n) == str(n)[::-1]

def generate_sequence(seq_type, limit):
    """Generates a list of numbers based on the selected sequence type."""
    print(f"\nGenerating sequence for '{seq_type}' up to {limit}...")
    sequence = []
    if seq_type == 'primes':
        return list(sympy.primerange(2, limit + 1))
    
    # For palindrome types, we iterate and check conditions
    for n in range(limit + 1):
        if is_palindrome(n):
            if seq_type == 'palindromes':
                sequence.append(n)
            elif seq_type == 'palindromic_primes':
                if sympy.isprime(n):
                    sequence.append(n)
    print(f"  -> Found {len(sequence)} numbers in the sequence.")
    return sequence

def sanitize_filename(text):
    """Converts a string into a valid HTML filename."""
    s = text.replace('**', '_pow_').replace('*', '_mul_').replace('/', '_div_')
    # The FIX is here: Changed the invalid range '0--9' to the correct '0-9'
    s = re.sub(r'[^a-zA-Z0-9_\-]', '', s)
    return s[:100] + '.html'

def plot_interactive_and_save(func_str, sequence, seq_name, output_folder):
    """
    Creates an interactive 2D comparison plot using Plotly and saves it as an HTML file.
    """
    print(f"Processing function: '{func_str}'...")
    
    # 1. Parse the mathematical function
    try:
        x = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        f = sympy.lambdify(x, expr, 'numpy')
    except Exception as e:
        print(f"  -> ❌ Error parsing '{func_str}'. Skipping. (Reason: {e})")
        return

    # 2. Prepare data for plotting
    sequence_data = np.array(sequence)
    num_points = len(sequence_data)
    integers_data = np.arange(1, num_points + 1)
    x_indices = np.arange(num_points)

    # 3. Evaluate the function for both sequences with error handling
    try:
        y_sequence = f(sequence_data)
        y_integers = f(integers_data)
    except Exception as e:
        print(f"  -> ❌ Error evaluating '{func_str}'. Skipping. (Reason: {e})")
        return

    # 4. Create the interactive plot with Plotly
    fig = go.Figure()

    # Add the trace for the standard integer sequence
    fig.add_trace(go.Scatter(
        x=x_indices,
        y=y_integers,
        mode='lines+markers',
        name='Integer Inputs: f(n)',
        line=dict(color='dodgerblue', dash='dash'),
        marker=dict(size=5),
        hovertemplate='<b>Integer Input</b><br>Index (n): %{x}<br>Input Value: %{customdata}<br>f(n): %{y:.4f}<extra></extra>',
        customdata=integers_data
    ))

    # Add the trace for the custom sequence (e.g., Palindromes)
    fig.add_trace(go.Scatter(
        x=x_indices,
        y=y_sequence,
        mode='lines+markers',
        name=f'{seq_name} Inputs: f(sₙ)',
        line=dict(color='orangered'),
        marker=dict(size=7),
        hovertemplate=f'<b>{seq_name} Input</b><br>Index (n): %{x}<br>Input Value: %{{customdata}}<br>f(sₙ): %{{y:.4f}}<extra></extra>',
        customdata=sequence_data
    ))
    
    # 5. Customize the layout (title, axis labels, theme)
    fig.update_layout(
        title=f"Interactive Comparison for y = {func_str}<br><sup>{seq_name} vs. Integer Inputs</sup>",
        xaxis_title="Sequence Index (n)",
        yaxis_title="Function Value",
        legend_title="Input Type",
        template='plotly_white',
        hovermode='x unified'
    )

    # 6. Save the interactive plot as an HTML file
    filename = sanitize_filename(f'{seq_name}_{func_str}')
    output_path = os.path.join(output_folder, filename)
    fig.write_html(output_path)
    print(f"  -> ✅ Interactive graph saved as: '{output_path}'")


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'interactive_graphs'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ['x**0.5', 'log(x)', 'x/log(x)', 'sin(x/100)']
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
        if not isinstance(functions_to_plot, list): raise TypeError
    except Exception:
        print(f"Error reading '{INPUT_FILE}'. Please ensure it's a valid list.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("--- 🖱️ Interactive 2D Plotter ---")
    
    # Ask user for the sequence type
    print("\nChoose the number sequence for the x-axis:")
    print("  1. Primes")
    print("  2. Palindromes (all numbers that read the same forwards and backwards)")
    print("  3. Palindromic Primes (primes that are also palindromes)")
    
    choice_map = {'1': 'primes', '2': 'palindromes', '3': 'palindromic_primes'}
    seq_name_map = {'1': 'Prime', '2': 'Palindrome', '3': 'Palindromic Prime'}
    
    while True:
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in choice_map: break
        print("Invalid choice. Please try again.")

    seq_type = choice_map[choice]
    seq_name = seq_name_map[choice]

    while True:
        try:
            user_limit = int(input("Enter the upper numerical limit for the sequence (e.g., 10000): "))
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    # Generate the chosen sequence once
    sequence = generate_sequence(seq_type, user_limit)

    if len(sequence) < 2:
        print("\nNot enough numbers found in the sequence to create a plot. Please try a larger limit.")
    else:
        print("\n🚀 Starting batch process...")
        for func in functions_to_plot:
            plot_interactive_and_save(func, sequence, seq_name, OUTPUT_FOLDER)
        print("\n✨ Batch process complete!")