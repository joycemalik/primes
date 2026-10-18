# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v07_composite_squeeze_interactive.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v7.py   (last edited 2025-08-22)
# What this script does  :: Interactive "composite squeeze" plots.
# ----------------------------------------------------------------------------
import plotly.graph_objects as go
import sympy
import numpy as np
import os
import re
import ast

def sanitize_filename(text):
    """Converts a string into a valid HTML filename."""
    s = text.replace('**', '_pow_').replace('*', '_mul_').replace('/', '_div_')
    s = re.sub(r'[^a-zA-Z0-9_\-]', '', s)
    return s[:100] + '.html'

def generate_squeeze_data(func, limit):
    """
    Generates the data for a Composite Squeeze Plot.
    Primes are at integer coordinates, and composites are squeezed in between.
    """
    primes = list(sympy.primerange(0, limit + 1))
    
    # Store data for primes and composites separately for easier plotting
    prime_data = {'x': [], 'y': [], 'number': []}
    composite_data = {'x': [], 'y': [], 'number': []}

    # Generate the full number line up to the limit
    all_numbers = np.arange(2, limit + 1)
    all_y_values = func(all_numbers)
    
    prime_set = set(primes) # Use a set for fast lookups
    
    # This loop builds the mapping
    for i in range(len(primes) - 1):
        p_current = primes[i]
        p_next = primes[i+1]
        
        # Add the current prime's data
        prime_data['x'].append(i)
        prime_data['y'].append(func(p_current))
        prime_data['number'].append(p_current)
        
        # Find composites in the gap between p_current and p_next
        composites_in_gap = [n for n in range(p_current + 1, p_next)]
        
        k = len(composites_in_gap)
        if k > 0:
            for j, comp in enumerate(composites_in_gap):
                # Squeeze the composite into the interval (i, i+1)
                x_coord = i + (j + 1) / (k + 1)
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

def plot_composite_squeeze(func_str, output_folder):
    """
    Parses a function and creates the full interactive squeeze plot.
    """
    print(f"Processing function: '{func_str}'...")
    
    # 1. Parse function
    try:
        x_sym = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        func = sympy.lambdify(x_sym, expr, 'numpy')
    except Exception as e:
        print(f"  -> ❌ Error parsing '{func_str}'. Skipping. (Reason: {e})")
        return

    # 2. Generate the specially mapped data
    try:
        prime_data, composite_data, primes = generate_squeeze_data(func, user_limit)
    except Exception as e:
        print(f"  -> ❌ Error evaluating '{func_str}'. Skipping. (Reason: {e})")
        return

    # 3. Create the interactive plot
    fig = go.Figure()

    # Add composites first so they are in the background
    fig.add_trace(go.Scatter(
        x=composite_data['x'],
        y=composite_data['y'],
        mode='markers',
        name='Composites',
        marker=dict(size=6, color='lightgray', symbol='x'),
        hovertemplate='<b>Composite</b><br>Value: %{customdata}<br>f(x): %{y:.4f}<extra></extra>',
        customdata=composite_data['number']
    ))
    
    # Add primes, with a line connecting them
    fig.add_trace(go.Scatter(
        x=prime_data['x'],
        y=prime_data['y'],
        mode='lines+markers',
        name='Primes',
        line=dict(color='orangered', width=2),
        marker=dict(size=10, symbol='circle'),
        hovertemplate='<b>Prime</b><br>Value: %{customdata}<br>f(p): %{y:.4f}<extra></extra>',
        customdata=prime_data['number']
    ))

    # 4. Customize layout
    fig.update_layout(
        title=f'Composite Squeeze Plot for y = {func_str}',
        xaxis_title='Prime Index (Major Ticks are Primes)',
        yaxis_title='Function Value',
        legend_title='Number Type',
        template='plotly_white'
    )
    
    # Set the major x-axis ticks to be the primes themselves
    fig.update_xaxes(
        tickvals=list(range(len(primes))),
        ticktext=[str(p) for p in primes]
    )

    # 5. Save the plot
    filename = sanitize_filename(f'Squeeze_{func_str}')
    output_path = os.path.join(output_folder, filename)
    fig.write_html(output_path)
    print(f"  -> ✅ Interactive graph saved as: '{output_path}'")


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'squeeze_plots'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ['x', 'x**0.5', 'sin(x/3)', 'x % 5']
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
        if not isinstance(functions_to_plot, list): raise TypeError
    except Exception:
        print(f"Error reading '{INPUT_FILE}'. Please ensure it's a valid list.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 🧬 Composite Squeeze Plotter ---")
    print("This script plots f(x) for all x, squeezing composites between prime landmarks.")

    while True:
        try:
            user_limit = int(input("Enter the upper numerical limit (e.g., 100): "))
            break
        except ValueError:
            print("Invalid input.")
            
    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        plot_composite_squeeze(func_str, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")