# ----------------------------------------------------------------------------
# Prime research archive :: research/10-factorials-and-gamma/factorial_visualizer_custom_definition.py
# Original location      :: factorial_visualizer.py   (last edited 2025-09-10)
# What this script does  :: Custom factorial via Gamma for positive and negative x.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

def custom_factorial(x):
    """
    Calculates the factorial based on the custom definition using the Gamma function
    for continuous values.
    - For x > 0: n! = Gamma(n+1)
    - For x < 0: (-n)! = (-1)^n * n! 
      The continuous extension is cos(pi*x) * Gamma(1-x).
    """
    # Create an empty array to store the results
    result = np.empty_like(x)
    
    # Condition for positive values
    positive_mask = x > 0
    result[positive_mask] = gamma(x[positive_mask] + 1)
    
    # Condition for negative values
    negative_mask = x < 0
    # The term np.cos(np.pi * x) provides the alternating sign (-1)^n for integers
    result[negative_mask] = np.cos(np.pi * x[negative_mask]) * gamma(1 - x[negative_mask])
    
    # Set values very close to zero or non-numeric to NaN so they aren't plotted
    result[np.abs(x) < 1e-9] = np.nan 
    
    return result

# --- Data Generation ---
# Generate a range of x values for the positive and negative sides.
# We avoid x=0 where the function is undefined.
x_positive = np.linspace(0.01, 100, 2000)
x_negative = np.linspace(-100, -0.01, 2000)

# Calculate the corresponding y values using our custom function
y_positive = custom_factorial(x_positive)
y_negative = custom_factorial(x_negative)


# --- Plotting ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the positive and negative sides separately for different colors
ax.plot(x_negative, y_negative, label='n! for n < 0', color='cyan')
ax.plot(x_positive, y_positive, label='n! for n > 0', color='magenta')

# --- Scaling and Labels ---
# Set the y-axis to a symmetric logarithmic scale.
# This is crucial for visualizing the huge range of values from 100!
# while also seeing the detail near zero.
ax.set_yscale('symlog')

ax.set_title('Visualization of Custom Factorial Function (up to 100!)', fontsize=16)
ax.set_xlabel('n', fontsize=12)
ax.set_ylabel('n! (Symmetric Log Scale)', fontsize=12)

# Add a grid for better readability
ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

# Add a horizontal line at y=0
ax.axhline(0, color='white', linewidth=0.7)
# Add a vertical line at x=0
ax.axvline(0, color='white', linewidth=0.7)

ax.legend()
plt.show()
