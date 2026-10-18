# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/prime_vector_pairs.py
# Original location      :: prime_vector_pairs.py   (last edited 2025-08-11)
# What this script does  :: Pairs [is_prime(10k+1), is_prime(10k+3)] for k = 1..n. Ground truth for the comparisons.
# ----------------------------------------------------------------------------
"""
Prime Vector Pairs Generator
===========================

For each consecutive pair (10k+1, 10k+3), outputs [is_prime, is_prime] for each, up to n pairs.
"""
import math
from typing import List

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def prime_vector_pairs(n_pairs: int) -> List[List[int]]:
    """Generate vector pairs for (10k+1, 10k+3) for k=1 to n_pairs."""
    result = []
    for k in range(1, n_pairs + 1):
        a = 10 * k + 1
        b = 10 * k + 3
        vec = [int(is_prime(a)), int(is_prime(b))]
        result.append(vec)
    return result

def main():
    n = int(input("Enter n (number of pairs): "))
    vectors = prime_vector_pairs(n)
    print(f"\nFull matrix (as list of lists) for n={n}:")
    print(vectors)

if __name__ == "__main__":
    main()
