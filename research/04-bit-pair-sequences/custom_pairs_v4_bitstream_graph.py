# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/custom_pairs_v4_bitstream_graph.py
# Original location      :: custom_prime_vector_pairs_graph.py   (last edited 2025-08-12)
# What this script does  :: Plots the binary-fraction value for n = 1..N.
# ----------------------------------------------------------------------------
from sympy import isprime

from mpmath import mp

def _block_odds(n: int) -> tuple[int, int]:
    """Return the two odd numbers in the n-th 5-wide block starting at 11."""
    start = 11 + 5 * (n - 1)          # n=1 -> 11..15, n=2 -> 16..20, etc.
    a = start if start % 2 else start + 1
    b = a + 2
    return a, b

def vector_for_block(n: int) -> tuple[int, int]:
    """Prime/non-prime vector for the n-th block as (v1, v2)."""
    a, b = _block_odds(n)
    return int(isprime(a)), int(isprime(b))

def vectors_upto(n: int) -> list[tuple[int, int]]:
    """Vectors from block 1 through block n (inclusive)."""
    if n <= 0:
        return []
    return [vector_for_block(i) for i in range(1, n + 1)]

# --- New functions for bitstream and decimal conversion ---
def flatten_vectors_to_bits(vectors):
    """Flatten list of (a, b) pairs to a list of bits [a, b, ...]."""
    return [bit for pair in vectors for bit in pair]

def bitstream_to_decimal(bits, precision=100):
    """Convert bitstream to decimal as 0.b1b2...bn with high precision."""
    mp.dps = precision
    N = 0
    for bit in bits:
        N = (N << 1) | bit
    denom = mp.power(2, len(bits))
    return mp.mpf(N) / denom

def prime_vector_decimal(n, precision=100):
    vectors = vectors_upto(n)
    bits = flatten_vectors_to_bits(vectors)
    return bitstream_to_decimal(bits, precision)



import matplotlib.pyplot as plt

if __name__ == "__main__":
    n = int(input("Enter n (max for graph): "))
    xs = list(range(1, n+1))
    ys = [prime_vector_decimal(i, precision=50) for i in xs]
    plt.figure(figsize=(10, 5))
    plt.plot(xs, ys, marker='o', linestyle='-', color='b')
    plt.xlabel('n (number of pairs)')
    plt.ylabel('Decimal value of bitstream')
    plt.title('Prime Vector Bitstream as Binary Fraction (n=1 to n)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()