# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/custom_pairs_v1_5wide_blocks.py
# Original location      :: custom_prime_vector_pairs.py   (last edited 2025-08-12)
# What this script does  :: Odd pairs from 5-wide blocks starting at 11.
# ----------------------------------------------------------------------------
from sympy import isprime

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


print(vectors_upto(int(input("Enter n: ")))) 