# Bit-pair sequences

**When:** 11 – 12 Aug 2025

Primes written as bit pairs ([6k−1 prime], [6k+1 prime]) or ([10k+1 prime], [10k+3 prime]), turned into binary fractions, and fed to recurrences suggested by GPT and Gemini.

**Verdict:** Both AI recurrences reproduce the 100 pairs they were fit to and then score 24–25% on new pairs, below the 47% of always guessing (0, 0). Berlekamp–Massey shows no short linear rule exists.

| File / folder | Was | Last edited | What it is |
|---|---|---|---|
| `prime_vector_pairs.py` | `prime_vector_pairs.py` | 2025-08-11 | Pairs [is_prime(10k+1), is_prime(10k+3)] for k = 1..n. Ground truth for the comparisons. |
| `gpt_pairs_berlekamp_massey.py` | `gptpairs.py` | 2025-08-11 | GPT-suggested generator: Berlekamp-Massey over GF(2) fit to the first 100 pairs. |
| `gpt_pairs_context_model.py` | `gptpairs2.py` | 2025-08-11 | GPT-suggested generator: smallest deterministic k-context model with back-off. |
| `gemini_pairs_2adic_kick.py` | `geminiPrimes.py` | 2025-08-11 | Gemini-suggested generator: Fibonacci mod 2 with a 2-adic "kick". |
| `compare_gpt_pairs_with_prime_pairs.py` | `compare_gptpairs_primevectorpairs.py` | 2025-08-11 | Compares both GPT generators with the true pairs. |
| `compare_gemini_pairs_with_prime_pairs.py` | `compare_gemini_prime_vectors.py` | 2025-08-11 | Compares the Gemini generator with the true pairs. |
| `custom_pairs_v1_5wide_blocks.py` | `custom_prime_vector_pairs.py` | 2025-08-12 | Odd pairs from 5-wide blocks starting at 11. |
| `custom_pairs_v2_bitstream.py` | `custom_prime_vector_pairs copy.py` | 2025-08-12 | Adds bitstream and binary-fraction conversion. |
| `custom_pairs_v3_bitstream.py` | `custom_prime_vector_pairs copy 2.py` | 2025-08-12 | Bitstream version with higher precision. |
| `custom_pairs_v4_bitstream_graph.py` | `custom_prime_vector_pairs_graph.py` | 2025-08-12 | Plots the binary-fraction value for n = 1..N. |
| `pair_checker_seed_decoder.py` | `pair_checker.py` | 2025-08-12 | Decodes a decimal seed back into pairs and scores it against the truth. |
| `prime27_6k_plus_minus_1_pairs.py` | `prime27.py` | 2025-08-12 | Pairs [is_prime(6k-1), is_prime(6k+1)]. |
| `new_prime1_6k_pairs_bitstream.py` | `newPrime1.py` | 2025-08-19 | 6k+-1 pairs from (23, 25) turned into a high-precision binary fraction. |
| `new_primes2_ternary_signature.py` | `newPrimes2.py` | 2025-08-19 | Ternary signature of odd numbers: 0 composite, 1 = 6k-1 prime, 2 = 6k+1 prime. |
| `kolakoski_subword_complexity.py` | `kolonoski.py` | 2025-08-12 | Kolakoski sequence and its subword complexity P(n). |
