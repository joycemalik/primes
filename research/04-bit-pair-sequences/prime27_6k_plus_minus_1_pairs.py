# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/prime27_6k_plus_minus_1_pairs.py
# Original location      :: prime27.py   (last edited 2025-08-12)
# What this script does  :: Pairs [is_prime(6k-1), is_prime(6k+1)].
# ----------------------------------------------------------------------------
from typing import List
import sympy

def custom_prime_vector_pairs(n: int) -> List[list]:
    """
    For each k from 1 to n, generate the pair (6k-1, 6k+1) and return a list of [is_prime(6k-1), is_prime(6k+1)]
    """
    result = []
    for k in range(1, n+1):
        a = 6*k - 1
        b = 6*k + 1
        vec = [int(sympy.isprime(a)), int(sympy.isprime(b))]
        result.append(vec)
    return result

# Example usage:
if __name__ == "__main__":
    n = int(input("Enter n: "))
    vectors = custom_prime_vector_pairs(n)
    for idx, v in enumerate(vectors, 1):
        print(f"{idx}: {v}")
