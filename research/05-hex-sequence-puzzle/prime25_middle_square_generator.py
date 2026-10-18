# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/prime25_middle_square_generator.py
# Original location      :: prime25.py   (last edited 2025-08-11)
# What this script does  :: Middle-square generator from seed FA57A5BA (matches the puzzle string for 9 characters only).
# ----------------------------------------------------------------------------
def middle_square(seed):
    n = int(seed, 16)
    n2 = n * n
    middle = (n2 >> 16) & 0xFFFFFFFF
    return hex(middle)[2:].upper().zfill(8)

def generate_pattern(initial_seed, num_states):
    pattern = initial_seed
    seed = initial_seed
    for _ in range(1, num_states):
        seed = middle_square(seed)
        pattern += seed
    return pattern

# Example: Generate the first 10 states (including the seed)
initial_seed = "FA57A5BA"
pattern = generate_pattern(initial_seed, 10)
print(pattern)