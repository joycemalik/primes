# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/gemini_pairs_2adic_kick.py
# Original location      :: geminiPrimes.py   (last edited 2025-08-11)
# What this script does  :: Gemini-suggested generator: Fibonacci mod 2 with a 2-adic "kick".
# ----------------------------------------------------------------------------
import math

def get_v2(k):
    """Calculates the 2-adic valuation of k."""
    if k == 0:
        return 0 # Or handle as an error/infinity
    return (k & -k).bit_length() - 1

def generate_true_sequence(n: int) -> list[list[int]]:
    """
    Generates the correct vector sequence up to a given length n.
    The function is V_{i+1} = (V_i + V_{i-1} + K_i) mod 2,
    where the kick K_i depends on the 2-adic valuation of (i+1).
    """
    if n == 0:
        return []
    sequence = [[1, 1]]
    if n == 1:
        return sequence
    sequence.append([0, 1])
    if n == 2:
        return sequence

    for i in range(2, n):
        v_i = sequence[-1]
        v_i_minus_1 = sequence[-2]

        # Base Fibonacci recurrence
        fib_pred_x = (v_i[0] + v_i_minus_1[0]) % 2
        fib_pred_y = (v_i[1] + v_i_minus_1[1]) % 2

        kick_vector = [0, 0]
        # The kick rule activates for index i=8 and onwards.
        if i >= 8:
            v2_of_i_plus_1 = get_v2(i + 1)
            kx = v2_of_i_plus_1 % 2
            ky = (v2_of_i_plus_1 - 1) % 2
            kick_vector = [kx, ky]
        
        x_next = (fib_pred_x + kick_vector[0]) % 2
        y_next = (fib_pred_y + kick_vector[1]) % 2

        sequence.append([x_next, y_next])
    
    return sequence

def gemini_prime_vectors(n: int) -> list[list[int]]:
    """
    Compatibility wrapper for comparison: returns the first n vectors using the true sequence.
    """
    return generate_true_sequence(n)

# --- Verification ---
# Generate sequence up to n=202 and check the last vector.
sequence_length = 202
final_sequence = generate_true_sequence(sequence_length)

print(f"Generated sequence of length {len(final_sequence)}.")
print(f"Vector at n=202 is: {final_sequence[-1]}")