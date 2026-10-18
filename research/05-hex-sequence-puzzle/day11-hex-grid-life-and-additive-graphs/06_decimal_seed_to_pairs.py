# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/06_decimal_seed_to_pairs.py
# Original location      :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/6.py   (last edited 2025-08-12)
# What this script does  :: Decodes a decimal seed into a bitstream of prime pairs.
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

# --- Example Usage ---
seed = 0.9596916933508150789027631175771447405492376550528
n_blocks = 20 # To get the first 5 vectors (10 bits)
mp.dps = 100 # Set precision for mpmath

sequence = get_vectors_from_seed(seed, n_blocks)
print(sequence)