# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/new_prime1_6k_pairs_bitstream.py
# Original location      :: newPrime1.py   (last edited 2025-08-19)
# What this script does  :: 6k+-1 pairs from (23, 25) turned into a high-precision binary fraction.
# ----------------------------------------------------------------------------
from sympy import isprime
from mpmath import mp

def vector_for_block(n: int) -> tuple[int, int]:
    """
    Prime/non-prime vector for the n-th block.
    We set the starting 'k' value such that n=1 corresponds to k=4.
    """
    # For n=1, k becomes 4. This starts the sequence with the pair (6*4-1, 6*4+1) = (23, 25).
    k = n + 3
    
    a = 6 * k - 1
    b = 6 * k + 1
    
    # The vector is (isprime(6k-1), isprime(6k+1))
    return int(isprime(a)), int(isprime(b))

def vectors_upto(n: int) -> list[tuple[int, int]]:
    """Vectors from block 1 through block n (inclusive)."""
    if n <= 0:
        return []
    return [vector_for_block(i) for i in range(1, n + 1)]

# --- These functions remain the same ---
def flatten_vectors_to_bits(vectors):
    """Flatten list of (a, b) pairs to a list of bits [a, b, ...]."""
    return [bit for pair in vectors for bit in pair]

def bitstream_to_decimal(bits, precision=300):
    """Convert bitstream to decimal as 0.b1b2...bn with high precision."""
    mp.dps = precision
    N = 0
    for bit in bits:
        N = (N << 1) | bit
    denom = mp.power(2, len(bits))
    return mp.mpf(N) / denom

# --- Main execution block ---
if __name__ == "__main__":
    n = int(input("Enter the number of blocks (n): "))
    try:
        precision = int(input("Enter decimal precision (default 300): ") or "300")
    except ValueError:
        precision = 300
        
    vectors = vectors_upto(n)
    print("\nVectors (starting from pair (23, 25)):", vectors)
    
    bits = flatten_vectors_to_bits(vectors)
    bit_string = ''.join(str(b) for b in bits)
    print("Bitstream:", bit_string)
    
    dec = bitstream_to_decimal(bits, precision=precision)
    print(f"\nDecimal value (0.{bit_string} in binary, {precision} dps):\n{dec}")