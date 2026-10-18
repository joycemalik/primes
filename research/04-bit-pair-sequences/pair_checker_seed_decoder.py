# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/pair_checker_seed_decoder.py
# Original location      :: pair_checker.py   (last edited 2025-08-12)
# What this script does  :: Decodes a decimal seed back into pairs and scores it against the truth.
# ----------------------------------------------------------------------------
import mpmath as mp

def decimal_to_bitstream(seed_decimal, num_bits):
    """
    Converts a decimal number (seed) back into a bitstream.
    
    Args:
        seed_decimal (float): The input decimal seed.
        num_bits (int): The number of bits to extract.
        
    Returns:
        list[int]: The list of bits.
    """
    bits = []
    current_val = mp.mpf(seed_decimal)
    for _ in range(num_bits):
        current_val *= 2
        bit = int(current_val)
        bits.append(bit)
        current_val -= bit
    return bits

def bitstream_to_vectors(bits):
    """
    Converts a bitstream into a sequence of (a, b) vectors.
    
    Args:
        bits (list[int]): The list of bits.
        
    Returns:
        list[tuple[int, int]]: The sequence of vectors.
    """
    if len(bits) % 2 != 0:
        raise ValueError("Bitstream length must be even to form pairs.")
    return [(bits[i], bits[i+1]) for i in range(0, len(bits), 2)]

def get_vectors_from_seed(seed, n_blocks):
    """
    The main reverse function.
    
    Takes the seed number and the number of blocks (n) to reverse.
    It returns the original sequence of prime/non-prime vectors.
    
    Args:
        seed (float): The input seed number.
        n_blocks (int): The number of blocks to generate.
        
    Returns:
        list[tuple[int, int]]: The original vector sequence.
    """
    num_bits = n_blocks * 2
    bits = decimal_to_bitstream(seed, num_bits)
    vectors = bitstream_to_vectors(bits)
    return vectors


# --- Prime pair sequence generator (copied from custom_prime_vector_pairs.py) ---
from sympy import isprime
def _block_odds(n: int) -> tuple[int, int]:
    start = 11 + 5 * (n - 1)
    a = start if start % 2 else start + 1
    b = a + 2
    return a, b
def vector_for_block(n: int) -> tuple[int, int]:
    a, b = _block_odds(n)
    return int(isprime(a)), int(isprime(b))
def vectors_upto(n: int) -> list[tuple[int, int]]:
    if n <= 0:
        return []
    return [vector_for_block(i) for i in range(1, n + 1)]

def compare_sequences(seq1, seq2):
    """Return (score, total, mismatches) where score is number of matches."""
    total = min(len(seq1), len(seq2))
    score = sum(1 for i in range(total) if seq1[i] == seq2[i])
    mismatches = [(i, seq1[i], seq2[i]) for i in range(total) if seq1[i] != seq2[i]]
    return score, total, mismatches

if __name__ == "__main__":
    seed = 0.9596916933508150789027631175771447405492376550528
    n_blocks = 20
    mp.dps = 100
    sequence = get_vectors_from_seed(seed, n_blocks)
    print("Decoded sequence from seed:", sequence)
    true_sequence = vectors_upto(n_blocks)
    print("True prime pair sequence:", true_sequence)
    score, total, mismatches = compare_sequences(sequence, true_sequence)
    print(f"\nScore: {score}/{total} correct")
    if mismatches:
        print("Mismatches (index, decoded, true):")
        for idx, dec, tru in mismatches:
            print(f"  {idx}: {dec} vs {tru}")
    else:
        print("All pairs match!")