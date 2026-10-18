# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/gpt_pairs_context_model.py
# Original location      :: gptpairs2.py   (last edited 2025-08-11)
# What this script does  :: GPT-suggested generator: smallest deterministic k-context model with back-off.
# ----------------------------------------------------------------------------
# chaotic_deterministic.py
# Learn the minimal deterministic function f: (last k pairs) -> next pair
# from a prefix of the sequence, then keep generating.
#
# - Finds the smallest k (<= K_MAX) such that each length-k context maps to a
#   unique next pair (no conflicts).
# - Uses backoff (k, k-1, ..., 1) if a context hasn't been seen.
# - Can evaluate against a held-out tail if you provide more data.

from collections import defaultdict, Counter
from typing import List, Tuple, Dict, Optional

Pair = Tuple[int, int]
Context = Tuple[Pair, ...]


def build_context_table(seq: List[Pair], k: int):
    """
    For all i with i+k < len(seq), collect mapping: context(seq[i:i+k]) -> next seq[i+k]
    Returns: dict[Context] -> Counter[next_pair]
    """
    table: Dict[Context, Counter] = {}
    if k == 0:
        # Degenerate: counts over all next pairs
        table[tuple()] = Counter(seq[1:])
        return table
    for i in range(len(seq) - k):
        ctx = tuple(seq[i:i + k])
        nxt = seq[i + k]
        table.setdefault(ctx, Counter())[nxt] += 1
    return table


def is_deterministic(table: Dict[Context, Counter]) -> bool:
    """True if every context maps to exactly one next pair (no conflicts)."""
    return all(len(cnt) == 1 for cnt in table.values())


def to_deterministic_mapping(table: Dict[Context, Counter]) -> Dict[Context, Pair]:
    """
    Convert counts to a deterministic map. If multiple nexts exist, pick the most
    frequent; tie-break by recency/any (stable due to Counter order in Py>=3.7).
    """
    mapping: Dict[Context, Pair] = {}
    for ctx, cnt in table.items():
        nxt, _ = cnt.most_common(1)[0]
        mapping[ctx] = nxt
    return mapping


def find_min_k(seq: List[Pair], k_max: int = 64) -> Tuple[int, Dict[Context, Pair]]:
    """
    Increment k from 1..k_max; return first k with a deterministic mapping.
    If none is strictly deterministic, return k_max with majority mapping.
    """
    best_k = 1
    best_map: Dict[Context, Pair] = {}
    for k in range(1, min(k_max, len(seq) - 1) + 1):
        table = build_context_table(seq, k)
        mapping = to_deterministic_mapping(table)
        if is_deterministic(table):
            return k, mapping
        # keep latest as a fallback (will be refined as k grows)
        best_k, best_map = k, mapping
    return best_k, best_map


def build_backoff_maps(seq: List[Pair], k_max: int) -> List[Dict[Context, Pair]]:
    """
    Precompute deterministic maps for all orders 1..k_max.
    (Even if some orders have conflicts, we store majority choice for backoff.)
    """
    maps: List[Dict[Context, Pair]] = [dict()]  # index 0 unused for simplicity
    for k in range(1, k_max + 1):
        table = build_context_table(seq, k)
        maps.append(to_deterministic_mapping(table))
    return maps


def next_from_backoff(history: List[Pair],
                      det_map: Dict[Context, Pair],
                      k: int,
                      backoff_maps: List[Dict[Context, Pair]]) -> Pair:
    """
    Try full context of length k; if unseen, back off to k-1, ..., 1.
    As a last resort (no context at all), fall back to the global most frequent pair.
    """
    L = min(k, len(history))
    while L > 0:
        ctx = tuple(history[-L:])
        # Prefer the exact deterministic mapping if available at full k
        if L == k and ctx in det_map:
            return det_map[ctx]
        # Otherwise try learned majority for this shorter context
        mp = backoff_maps[L]
        if ctx in mp:
            return mp[ctx]
        L -= 1
    # No context available: return most frequent pair in training tail
    global_counts = Counter(p for p in history)
    return global_counts.most_common(1)[0][0]


def generate(seq_seed: List[Pair],
             k: int,
             det_map: Dict[Context, Pair],
             backoff_maps: List[Dict[Context, Pair]],
             n_more: int) -> List[Pair]:
    """
    Generate n_more pairs continuing from seq_seed (not modifying it).
    """
    hist = list(seq_seed)
    out: List[Pair] = []
    for _ in range(n_more):
        nxt = next_from_backoff(hist, det_map, k, backoff_maps)
        hist.append(nxt)
        out.append(nxt)
    return out


def evaluate(reference: List[Pair], predicted: List[Pair], start_index: int = 0) -> None:
    """
    Print match stats for two equally-long lists of pairs.
    start_index is the 1-based position in the *full* stream where predicted[0] sits.
    """
    total = len(predicted)
    matches = sum(1 for i in range(total) if predicted[i] == reference[i])
    mismatches = total - matches
    pct = 100.0 * matches / max(1, total)
    print(f"\nSummary:\n  Total pairs compared: {total}\n  Matches: {matches}\n  Mismatches: {mismatches}\n  Match percentage: {pct:.2f}%")
    if mismatches:
        print("\n❌ mismatches found:")
        shown = 0
        for i in range(total):
            if predicted[i] != reference[i]:
                pos = start_index + i
                print(f"  At position {pos}: original={reference[i]}, pred={predicted[i]}")
                shown += 1
                if shown >= 20:
                    print(f"  ...and {mismatches - shown} more mismatches.")
                    break





# ---------------------- EXAMPLE USAGE ----------------------

def get_gptpairs2(n: int) -> List[Pair]:
    """
    Returns the first n pairs generated by the learned recurrence (train on first 100, predict the rest).
    For n <= 100, returns the prefix. For n > 100, returns prefix + generated.
    """
    # Full sequence prefix (n=100)
    pairs: List[Pair] = [
        (1, 1), (0, 1), (1, 0), (1, 1), (0, 1), (1, 0), (1, 1), (0, 1), (0, 0), (1, 1),
        (0, 1), (0, 0), (1, 0), (0, 0), (1, 0), (0, 1), (0, 1), (1, 0), (1, 1), (0, 0),
        (1, 0), (0, 1), (0, 1), (1, 0), (1, 0), (0, 1), (1, 0), (1, 1), (0, 1), (0, 0),
        (1, 1), (0, 0), (1, 0), (0, 0), (0, 1), (0, 0), (0, 1), (0, 1), (0, 0), (1, 0),
        (0, 0), (1, 0), (1, 1), (0, 1), (0, 0), (1, 1), (0, 0), (0, 0), (1, 0), (0, 1),
        (0, 0), (1, 1), (0, 0), (1, 0), (0, 0), (0, 1), (1, 0), (0, 0), (0, 1), (1, 0),
        (0, 1), (0, 0), (1, 0), (1, 1), (0, 1), (1, 0), (0, 1), (0, 1), (1, 0), (1, 0),
        (0, 0), (0, 0), (0, 1), (0, 1), (1, 0), (1, 0), (0, 1), (0, 0), (0, 0), (0, 0),
        (1, 0), (1, 1), (0, 0), (0, 0), (0, 1), (0, 1), (0, 0), (1, 1), (0, 0), (0, 0),
        (1, 0), (0, 0), (0, 0), (1, 0), (0, 1), (0, 0), (1, 0), (0, 1), (1, 0), (0, 0)
    ]
    TRAIN_LEN = 100
    train = pairs[:TRAIN_LEN]
    K_MAX = 64
    k, det_map = find_min_k(train, k_max=K_MAX)
    backoff_maps = build_backoff_maps(train, k_max=k)
    if n <= TRAIN_LEN:
        return pairs[:n]
    else:
        n_more = n - TRAIN_LEN
        tail_pred = generate(train, k, det_map, backoff_maps, n_more=n_more)
        return pairs + tail_pred[:n_more]


# ...existing code...

if __name__ == "__main__":
    # Example usage: print first n pairs
    n = int(input("Enter n (number of pairs to generate): "))
    result = get_gptpairs2(n)
    for idx, p in enumerate(result, 1):
        print(f"{idx}: {p}")
