# ----------------------------------------------------------------------------
# Prime research archive :: research/10-factorials-and-gamma/day37-factorial-visualizer/factorial_values_plot.py
# Original location      :: research/10-factorials-and-gamma/day37-factorial-visualizer/factorial_visualizer.py   (last edited 2025-09-10)
# What this script does  :: Plots n! for n = 1..max_n.
# ----------------------------------------------------------------------------
"""
factorial_visualizer.py

Visualize factorial values using a bar chart.

Functions:
- factorial(n): compute n!
- plot_factorials(max_n): plot factorials from 1 to max_n

CLI: run file and enter max_n to plot.
"""
import math
import matplotlib.pyplot as plt
from typing import List


def factorial(n: int) -> int:
    """Compute n! using math.factorial."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    return math.factorial(n)


def plot_factorials(max_n: int):
    """Plot factorial values from 1 to max_n as a bar chart."""
    ns = list(range(1, max_n + 1))
    facts = [factorial(n) for n in ns]
    plt.figure(figsize=(12, 6))
    plt.bar(ns, facts, color='skyblue')
    plt.xlabel('n')
    plt.ylabel('n!')
    plt.title(f'Factorial Values for n=1 to {max_n}')
    plt.yscale('log')  # Use log scale for y-axis since factorials grow very fast
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(ns)  # Show all n values on x-axis
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    try:
        max_n = int(input("Enter max n for factorial visualization (default 20): ") or "20")
        if max_n < 1 or max_n > 100:  # Limit to avoid overflow
            print("Please enter a number between 1 and 100.")
            raise ValueError
    except ValueError:
        print("Invalid input; using default max_n=20.")
        max_n = 20
    plot_factorials(max_n)
