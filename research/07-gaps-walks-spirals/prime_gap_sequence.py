# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/prime_gap_sequence.py
# Original location      :: prime_gap_sequence.py   (last edited 2025-09-10)
# What this script does  :: First n prime gaps, their frequencies and a bar chart.
# ----------------------------------------------------------------------------
"""
prime_gap_sequence.py

Provide functions to compute the first n prime gaps (differences between consecutive primes).

Functions:
- prime_gaps(n): return list of first n prime gaps
- prime_gap_generator(): infinite generator yielding prime gaps

CLI: run file and enter n to print the gaps.
"""
from sympy import isprime
from typing import Iterator, List
from collections import Counter
import matplotlib.pyplot as plt


def prime_gap_generator(start: int = 2) -> Iterator[int]:
    """Yield prime gaps indefinitely starting from the first prime >= start.

    Yields p_{k+1} - p_k for consecutive primes.
    """
    prev = None
    num = start
    # find the first prime >= start
    while True:
        if isprime(num):
            prev = num
            num += 1
            break
        num += 1
    while True:
        # find next prime
        while not isprime(num):
            num += 1
        gap = num - prev
        yield gap
        prev = num
        num += 1


def prime_gaps(n: int) -> List[int]:
    """Return the first n prime gaps as a list.

    Example: prime_gaps(10) -> [1,2,2,4,2,4,2,4,6,2]
    """
    if n <= 0:
        return []
    gen = prime_gap_generator(start=2)
    gaps = []
    for _ in range(n):
        gaps.append(next(gen))
    return gaps


def gap_counts(n: int) -> Counter:
    """Return a Counter mapping gap -> frequency for the first n prime gaps."""
    gaps = prime_gaps(n)
    return Counter(gaps)


def plot_gap_counts(n: int, save_path: str = "prime_gap_counts.png"):
    """Plot and save a bar chart of gap frequencies for first n prime gaps."""
    counts = gap_counts(n)
    items = sorted(counts.items())
    gaps, freqs = zip(*items) if items else ([], [])
    plt.figure(figsize=(10, 5))
    plt.bar(gaps, freqs, color="C0")
    plt.xlabel("Prime gap")
    plt.ylabel("Frequency")
    plt.title(f"Prime gap frequencies for first {n} gaps")
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    # Save the figure and try to show it. In interactive environments plt.show()
    # will display the chart; in headless environments the file is still saved.
    try:
        plt.savefig(save_path)
    except Exception:
        pass
    try:
        plt.show()
    except Exception:
        # If show fails (headless), saving the file is still useful.
        pass
    return counts


if __name__ == "__main__":
    try:
        n = int(input("Enter n (number of prime gaps to produce): "))
    except Exception:
        print("Invalid input; please enter a positive integer.")
        raise
    g = prime_gaps(n)
    print(g)
    # Print distribution in requested format, sorted by gap value
    counts = gap_counts(n)
    print('\nDistribution:')
    for gap, freq in sorted(counts.items()):
        print(f"{gap}  -> {freq} times")

    # Plot and show the distribution; file will be saved as prime_gap_counts.png
    plot_gap_counts(n, save_path="prime_gap_counts.png")
    print("Plot saved to prime_gap_counts.png")
