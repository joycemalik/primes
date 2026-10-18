# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/kolakoski_subword_complexity.py
# Original location      :: kolonoski.py   (last edited 2025-08-12)
# What this script does  :: Kolakoski sequence and its subword complexity P(n).
# ----------------------------------------------------------------------------
import math

def generate_kolakoski(max_len=100000):
    """
    Generates the Kolakoski sequence up to a specified maximum length.
    The sequence is its own run-length encoding.
    """
    k = [1, 2, 2]  # Start with the initial seed
    i = 2          # Index to read the next run-length from
    symbol_to_add = 1 # The next symbol (1 or 2) to be added

    while len(k) < max_len:
        # The number of times to add the symbol is determined by the sequence itself
        run_length = k[i]
        
        for _ in range(run_length):
            k.append(symbol_to_add)

        # Alternate the symbol between 1 and 2
        symbol_to_add = 3 - symbol_to_add # A clever way to switch 1->2 and 2->1
        
        i += 1
        
    return k[:max_len]

def count_subwords(sequence, n):
    """
    Counts the number of unique contiguous subwords of length n.
    This is the value P(n).
    """
    if n > len(sequence):
        return 0
        
    subwords = set()
    # Slide a window of size n across the sequence
    for i in range(len(sequence) - n + 1):
        # We use a tuple because lists cannot be added to a set, but tuples can.
        subword = tuple(sequence[i : i+n])
        subwords.add(subword)
        
    return len(subwords)

if __name__ == "__main__":
    # --- Configuration ---
    # WARNING: Increasing these values will significantly increase runtime!
    # To get a good estimate, SEQ_LEN should be much larger than 2**MAX_N.
    SEQ_LEN = 200000   # How long of a sequence to generate.
    MAX_N = 1000         # The maximum length of subwords to check.
    
    print("Generating Kolakoski sequence...")
    kolakoski_seq = generate_kolakoski(SEQ_LEN)
    print(f"Sequence generated with {len(kolakoski_seq)} terms.")
    print("-" * 40)
    
    print(f"{'n':>3} | {'P(n)':>10} | {'Lambda Estimate (P(n))^(1/n)':>30}")
    print(f"{'-'*3:->} | {'-'*10:->} | {'-'*30:->}")

    for n in range(1, MAX_N + 1):
        # Count the unique subwords of length n
        p_n = count_subwords(kolakoski_seq, n)
        
        if p_n == 0:
            break
        
        # Calculate the estimate for lambda
        lambda_n = p_n**(1/n)
        
        print(f"{n:3d} | {p_n:10d} | {lambda_n:.15f}")

    print("-" * 40)
    print("Notice how the lambda estimate slowly converges.")
    print("The true value is conjectured to be ~1.04200115...")
    print("Getting that precision requires immense computation.")