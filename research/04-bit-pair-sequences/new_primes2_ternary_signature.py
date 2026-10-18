# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/new_primes2_ternary_signature.py
# Original location      :: newPrimes2.py   (last edited 2025-08-19)
# What this script does  :: Ternary signature of odd numbers: 0 composite, 1 = 6k-1 prime, 2 = 6k+1 prime.
# ----------------------------------------------------------------------------
from sympy import isprime

def ternary_prime_signature(limit: int):
    """
    Generates a ternary (0, 1, 2) string for odd numbers.
    0 = composite, 1 = prime of form 6k-1, 2 = prime of form 6k+1.
    """
    signature = []
    print(f"\n--- System 2: Ternary Prime Signature ---")
    print(f"Scanning odd numbers up to {limit}...\n")
    for n in range(3, limit + 1, 2):
        if isprime(n):
            if (n + 1) % 6 == 0:
                signature.append('1') # 6k-1 prime
            else:
                signature.append('2') # 6k+1 prime
        else:
            signature.append('0')
    
    ternary_string = "".join(signature)
    print("Resulting Ternary Signature:")
    print(ternary_string)
    return ternary_string

# --- Run the system ---
signature_string = ternary_prime_signature(1000)