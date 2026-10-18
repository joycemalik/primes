# ----------------------------------------------------------------------------
# Prime research archive :: research/04-bit-pair-sequences/compare_gpt_pairs_with_prime_pairs.py
# Original location      :: compare_gptpairs_primevectorpairs.py   (last edited 2025-08-11)
# What this script does  :: Compares both GPT generators with the true pairs.
# ----------------------------------------------------------------------------
import os
"""
Compare GPT Pairs and Prime Vector Pairs
========================================

Compares the first n vectors from gptpairs.py and prime_vector_pairs.py.
Assumes both produce a list of [a, b] pairs of 0/1 values.
"""
import importlib.util
import sys

# Import prime_vector_pairs from the original file
def import_prime_vector_pairs():
    spec = importlib.util.spec_from_file_location("prime_vector_pairs", os.path.join(os.path.dirname(os.path.abspath(__file__)), "prime_vector_pairs.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules["prime_vector_pairs"] = module
    spec.loader.exec_module(module)
    return module.prime_vector_pairs


# Import pairs from gptpairs.py (use get_gpt_pairs(n))
def import_gpt_pairs(n):
    spec = importlib.util.spec_from_file_location("gptpairs", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gpt_pairs_berlekamp_massey.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules["gptpairs"] = module
    spec.loader.exec_module(module)
    if hasattr(module, 'get_gpt_pairs'):
        return module.get_gpt_pairs(n)
    else:
        raise AttributeError("No 'get_gpt_pairs' function found in gptpairs.py")

# Import pairs from gptpairs2.py (use get_gptpairs2(n))
def import_gpt_pairs2(n):
    spec = importlib.util.spec_from_file_location("gptpairs2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gpt_pairs_context_model.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules["gptpairs2"] = module
    spec.loader.exec_module(module)
    if hasattr(module, 'get_gptpairs2'):
        return module.get_gptpairs2(n)
    else:
        raise AttributeError("No 'get_gptpairs2' function found in gptpairs2.py")

def compare_vectors(vec1, vec2):
    errors = []
    for i, (a, b) in enumerate(zip(vec1, vec2), 1):
        # Compare as tuples to avoid list/tuple mismatch
        if tuple(a) != tuple(b):
            errors.append((i, a, b))
    return errors


def print_comparison(name, original_vectors, test_vectors, n):
    errors = compare_vectors(original_vectors, test_vectors)
    print(f"\n{name}:")
    print(f"  Total pairs compared: {n}")
    print(f"  Matches: {n - len(errors)}")
    print(f"  Mismatches: {len(errors)}")
    print(f"  Match percentage: {(n - len(errors)) / n * 100:.2f}%")
    if not errors:
        print(f"  ✅ All {n} vectors match perfectly!")
    else:
        print(f"  ❌ {len(errors)} mismatches found:")
        for idx, orig, gpt in errors[:10]:
            print(f"    At position {idx}: original={orig}, test={gpt}")
        if len(errors) > 10:
            print(f"    ...and {len(errors)-10} more mismatches.")

def main():
    n = int(input("Enter n (number of pairs to compare): "))
    print(f"Comparing first {n} vectors from gptpairs, gptpairs2, and prime_vector_pairs...")

    # Get original vectors
    prime_vector_func = import_prime_vector_pairs()
    original_vectors = prime_vector_func(n)

    # Get gptpairs1
    gpt_pairs = import_gpt_pairs(n)
    # Get gptpairs2
    gpt_pairs2 = import_gpt_pairs2(n)

    print_comparison("GPT Pairs (gptpairs.py)", original_vectors, gpt_pairs, n)
    print_comparison("GPT Pairs 2 (gptpairs2.py)", original_vectors, gpt_pairs2, n)

if __name__ == "__main__":
    main()
