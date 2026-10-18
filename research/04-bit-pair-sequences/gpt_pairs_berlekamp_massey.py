# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/gpt_pairs_berlekamp_massey.py
# Original location      :: gptpairs.py   (last edited 2025-08-11)
# What this script does  :: GPT-suggested generator: Berlekamp-Massey over GF(2) fit to the first 100 pairs.
# ----------------------------------------------------------------------------
# generate_seq.py
# Learns the minimal linear recurrence (GF(2)) for each column and keeps generating.

from typing import List, Tuple

def berlekamp_massey_gf2(s: List[int]) -> Tuple[int, List[int]]:
    """
    Return (L, taps)
    Recurrence: s[n] = XOR_{i in taps} s[n - i], for n >= L
    taps are positive integers 1..L.
    """
    C = [1]            # connection polynomial
    B = [1]
    L = 0
    m = -1
    for n in range(len(s)):
        # discrepancy d
        d = s[n]
        for i in range(1, L + 1):
            if i < len(C) and C[i]:
                d ^= s[n - i]
        if d == 0:
            continue
        T = C[:]
        shift = [0] * (n - m) + B
        if len(C) < len(shift):
            C += [0] * (len(shift) - len(C))
        C = [(ci ^ si) for ci, si in zip(C, shift)]
        if 2 * L <= n:
            L = n + 1 - L
            B = T
            m = n
    # taps are the indices with coefficient 1 (exclude C[0])
    taps = [i for i in range(1, len(C)) if C[i] == 1]
    return L, taps

def next_bit(seq: List[int], taps: List[int]) -> int:
    x = 0
    for i in taps:
        x ^= seq[-i]
    return x

def extend_with_recurrence(seq: List[int], taps: List[int], k: int) -> List[int]:
    out = []
    for _ in range(k):
        b = next_bit(seq, taps)
        seq.append(b)
        out.append(b)
    return out


# --- API for n pairs ---
def get_gpt_pairs(n: int) -> list[list[int]]:
    """
    Returns n pairs using the learned recurrence from the initial data.
    """
    # Initial pairs (from the original data)
    base_pairs = [[1, 1], [0, 1], [1, 0], [1, 1], [0, 1], [1, 0], [1, 1], [0, 1], [0, 0], [1, 1], [0, 1], [0, 0], [1, 0], [0, 0], [1, 0], [0, 1], [0, 1], [1, 0], [1, 1], [0, 0], [1, 0], [0, 1], [0, 1], [1, 0], [1, 0], [0, 1], [1, 0], [1, 1], [0, 1], [0, 0], [1, 1], [0, 0], [1, 0], [0, 0], [0, 1], [0, 0], [0, 1], [0, 1], [0, 0], [1, 0], [0, 0], [1, 0], [1, 1], [0, 1], [0, 0], [1, 1], [0, 0], [0, 0], [1, 0], [0, 1], [0, 0], [1, 1], [0, 0], [1, 0], [0, 0], [0, 1], [1, 0], [0, 0], [0, 1], [1, 0], [0, 1], [0, 0], [1, 0], [1, 1], [0, 1], [1, 0], [0, 1], [0, 1], [1, 0], [1, 0], [0, 0], [0, 0], [0, 1], [0, 1], [1, 0], [1, 0], [0, 1], [0, 0], [0, 0], [0, 0], [1, 0], [1, 1], [0, 0], [0, 0], [0, 1], [0, 1], [0, 0], [1, 1], [0, 0], [0, 0], [1, 0], [0, 0], [0, 0], [1, 0], [0, 1], [0, 0], [1, 0], [0, 1], [1, 0], [0, 0]]
    a = [p[0] for p in base_pairs]
    b = [p[1] for p in base_pairs]
    La, taps_a = berlekamp_massey_gf2(a)
    Lb, taps_b = berlekamp_massey_gf2(b)
    if len(a) < n:
        extend_with_recurrence(a, taps_a, n - len(a))
        extend_with_recurrence(b, taps_b, n - len(b))
    return list(map(list, zip(a[:n], b[:n])))


if __name__ == "__main__":
    n = int(input("Enter n (number of pairs): "))
    pairs = get_gpt_pairs(n)
    print(f"\nFirst {n} pairs:")
    for i, p in enumerate(pairs, 1):
        print(f"{i:3d}: {p}")


