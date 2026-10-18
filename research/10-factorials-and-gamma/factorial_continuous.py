# ----------------------------------------------------------------------------
# Prime research archive :: research/10-factorials-and-gamma/factorial_continuous.py
# Original location      :: factorial_continuous.py   (last edited 2025-09-10)
# What this script does  :: Gamma-function factorial and weighted factorial variants.
# ----------------------------------------------------------------------------
# import numpy as np
# import matplotlib.pyplot as plt
# import math

# # 1. DEFINING THE FACTORIAL FUNCTIONS

# def standard_factorial(n):
#     """Calculates the standard n! for integers."""
#     if not isinstance(n, int) or n < 0: return None
#     try:
#         return float(math.factorial(n))
#     except (ValueError, OverflowError):
#         return None

# def log_weighted_factorial(n, base=10):
#     """Calculates factorial with your logarithmic weighting."""
#     if not isinstance(n, int) or n < 1: return None
    
#     numerator = standard_factorial(n)
#     if numerator is None: return None
    
#     # Denominator is the product of log_base(i+1)
#     denominator = 1.0
#     for i in range(1, n + 1):
#         # Using change of base formula: log_b(x) = ln(x) / ln(b)
#         denominator *= math.log(i + 1) / math.log(base)
        
#     if denominator == 0: return float('inf')
#     return numerator / denominator

# def poly_weighted_factorial(n, power=2):
#     """Calculates factorial with your polynomial weighting."""
#     base_factorial = standard_factorial(n)
#     if base_factorial is None: return None
    
#     # Formula simplifies to (n!)^(p+1)
#     return base_factorial ** (power + 1)

# # 2. GENERATING THE DATA FOR PLOTTING

# # We limit to n=12 because the polynomial function explodes
# x_integers = range(1, 13)

# y_standard = [standard_factorial(n) for n in x_integers]
# y_log = [log_weighted_factorial(n, base=10) for n in x_integers]
# y_poly = [poly_weighted_factorial(n, power=2) for n in x_integers]


# # 3. CREATING THE VISUALIZATION

# plt.style.use('seaborn-v0_8-whitegrid')
# fig, ax = plt.subplots(figsize=(12, 8))

# # Plot the standard factorial for reference
# ax.plot(x_integers, y_standard, label="Standard Factorial (n!)", color='green', marker='o', linestyle='--', linewidth=2)

# # Plot the Log-Weighted Factorial
# ax.plot(x_integers, y_log, label=f"Log-Weighted Factorial (base=10)", color='purple', marker='^', linewidth=2)

# # Plot the Polynomial-Weighted Factorial
# ax.plot(x_integers, y_poly, label=f"Poly-Weighted Factorial (power=2)", color='red', marker='s', linewidth=2)

# # A log scale is absolutely essential here
# ax.set_yscale('log')

# ax.set_xlabel("Number (n)", fontsize=12)
# ax.set_ylabel("Value (Logarithmic Scale)", fontsize=12)
# ax.set_title("Logarithmic vs. Polynomial Weighting", fontsize=16, fontweight='bold')
# ax.legend()
# ax.set_xlim(1, 12)

# plt.show()



import numpy as np
import matplotlib.pyplot as plt
import math

# --- PREVIOUS FUNCTIONS ---
def gamma_factorial(n):
    if n < 0 and int(n) == n: return None
    return math.gamma(n + 1)

def exp_weighted_factorial(n): # Your 1/2^i version
    if not isinstance(n, int) or n < 1: return None
    try:
        numerator = float(math.factorial(n))
    except (ValueError, OverflowError): return None
    sum_of_exponents = n * (n + 1) / 2
    denominator = 2**sum_of_exponents
    return numerator / denominator

# --- NEW FUNCTIONS ---
def log_weighted_factorial(n, base=2):
    if not isinstance(n, int) or n < 1: return None
    product = 1.0
    for i in range(1, n + 1):
        term = n - i + 1
        weight = 1 / math.log(i + 1, base)
        product *= (term * weight)
    return product

def poly_weighted_factorial(n, power=2):
    if not isinstance(n, int) or n < 1: return None
    try:
        return math.factorial(n)**(power + 1)
    except OverflowError:
        return float('inf')

# --- PLOTTING ---
x_integers = range(1, 16)
x_continuous = np.linspace(1, 15, 400) 

y_gamma = [gamma_factorial(n) for n in x_continuous]
y_exp_weighted = [exp_weighted_factorial(n) for n in x_integers]
y_log_weighted = [log_weighted_factorial(n) for n in x_integers]

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(x_continuous, y_gamma, label="True Factorial (Growth)", color='green', linestyle='--', linewidth=2)
ax.plot(x_integers, y_log_weighted, label="Logarithmic Weighted (Gentle Suppression)", color='orange', marker='o', linewidth=2)
ax.plot(x_integers, y_exp_weighted, label="Exponential Weighted (Strong Decay)", color='purple', marker='o', linewidth=2)

ax.set_yscale('log') # Log scale is essential
ax.set_xlabel("Number (n)", fontsize=12)
ax.set_ylabel("Factorial Value (Logarithmic Scale)", fontsize=12)
ax.set_title("Different Weighting Schemes for Factorials", fontsize=16, fontweight='bold')
ax.legend()
plt.show()


# --- DEMONSTRATING THE POLYNOMIAL EXPLOSION ---
print("--- Polynomial Weighted Factorial (Explosion) ---")
for i in range(1, 11):
    print(f"n={i}: {poly_weighted_factorial(i, power=2):,.2f}")