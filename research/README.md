# Research

Everything about primes and the Riemann hypothesis, grouped by idea. Folders are numbered in the order the ideas were explored, and file names keep their original numbers so the sequence of experiments is never lost.

| # | Topic | When | Folder |
|---|---|---|---|
| 01 | Prime wave sieve | 30 Jul – 3 Aug 2025 | [`01-prime-wave-sieve/`](01-prime-wave-sieve/README.md) |
| 02 | Physics-inspired wave models | 2 Aug 2025 | [`02-physics-inspired-wave-models/`](02-physics-inspired-wave-models/README.md) |
| 03 | Complex plane | 4 – 11 Aug 2025 | [`03-complex-plane/`](03-complex-plane/README.md) |
| 04 | Bit-pair sequences | 11 – 12 Aug 2025 | [`04-bit-pair-sequences/`](04-bit-pair-sequences/README.md) |
| 05 | Hex sequence puzzle | 8 – 11 Aug 2025 | [`05-hex-sequence-puzzle/`](05-hex-sequence-puzzle/README.md) |
| 06 | Prime music | 8 Aug 2025 | [`06-prime-music/`](06-prime-music/README.md) |
| 07 | Gaps, walks and spirals | 18 – 27 Aug 2025 | [`07-gaps-walks-spirals/`](07-gaps-walks-spirals/README.md) |
| 08 | Machine learning | 30 Jul – 27 Aug 2025 | [`08-machine-learning/`](08-machine-learning/README.md) |
| 09 | Prime matrix | 17 Aug 2025 | [`09-prime-matrix/`](09-prime-matrix/README.md) |
| 10 | Factorials and Gamma | 10 Sep 2025 | [`10-factorials-and-gamma/`](10-factorials-and-gamma/README.md) |

## The original numbered "prime" series

The scripts and notebooks you numbered prime1 … prime27 are spread across topics now. This is their original order:

| No. | Original name | New location | What it is |
|---|---|---|---|
| 1 | `prime1.py` | `research/01-prime-wave-sieve/numbered-series/prime01_sine_product_zero_crossings.py` | g(x) = \|prod sin(pi x / p)\| for p in {2,3,5,7}: composites hit zeros, primes escape. |
| 2 | `prime2.py` | `research/01-prime-wave-sieve/numbered-series/prime02_product_of_sines_sieve.py` | Signed product of sines ("sieve of zeroes") with primes marked. |
| 3 | `prime3.py` | `research/01-prime-wave-sieve/numbered-series/prime03_small_factor_count_wave.py` | Counts small prime factors of n in [100000, 200000] and predicts primes where the count is 0. |
| 4 | `prime4.py` | `research/01-prime-wave-sieve/numbered-series/prime04_small_factor_count_wave_report.py` | Same as prime03 plus a printed comparison of predicted and actual primes. |
| 5 | `prime5.py` | `research/01-prime-wave-sieve/numbered-series/prime05_raised_cosine_interference.py` | Sum of raised cosines (1 + cos 2 pi x / p) / 2 for primes up to sqrt(N). |
| 6 | `prime6.py` | `research/01-prime-wave-sieve/numbered-series/prime06_raised_cosine_prediction.py` | Raised-cosine interference with a prediction panel. |
| 7 | `prime7.py` | `research/01-prime-wave-sieve/numbered-series/prime07_individual_and_composite_waves.py` | Plots each prime wave and the combined interference pattern. |
| 8 | `prime8.py` | `research/01-prime-wave-sieve/numbered-series/prime08_marking_waves_quiet_zones.py` | Marking waves and "quiet zones" where primes appear. |
| 9 | `prime9.py` | `research/01-prime-wave-sieve/numbered-series/prime09_spike_superposition.py` | Spike superposition: each context prime adds a spike at its multiples. |
| 10 | `prime10.py` | `research/01-prime-wave-sieve/numbered-series/prime10_spike_superposition_excluding_self.py` | Spikes start at 2p so the prime itself stays at 0. |
| 11 | `prime11.py` | `research/01-prime-wave-sieve/numbered-series/prime11_spike_superposition_metrics.py` | Spike superposition with precision / recall. |
| 12 | `prime12.py` | `research/01-prime-wave-sieve/numbered-series/prime12_spike_superposition_metrics_v2.py` | Refined spike superposition with metrics (root copy). |
| 13 | `prime13.py` | `research/01-prime-wave-sieve/numbered-series/prime13_spike_superposition_v3.py` | Spike superposition, third variant. |
| 14 | `prime14.py` | `research/01-prime-wave-sieve/numbered-series/prime14_weighted_wave_context_50.py` | Waves weighted by 1/sqrt(p) using only primes <= 50, tested up to 10,000. |
| 15 | `prime15.py` | `research/01-prime-wave-sieve/numbered-series/prime15_weighted_wave_function.py` | Weighted prime wave function with threshold detection. |
| 16 | `prime16.py` | `research/01-prime-wave-sieve/numbered-series/prime16_weighted_wave_function_copy.py` | Identical copy of prime15 (same size and code). |
| 17 | `prime17.py` | `research/01-prime-wave-sieve/numbered-series/prime17_ultimate_multilevel_detector.py` | Multi-level interference detector (same code as ultimate_prime_wave.py). |
| 18 | `prime18.ipnyb` | `archive/empty-placeholders/root__prime18.ipnyb` | Empty file with a misspelled extension. |
| 18 | `prime18.ipynb` | `research/01-prime-wave-sieve/notebooks/prime18_absolute_wave_function_proof_attempt.ipynb` | Attempted proof of an O(1) context-free prime test (its own validation prints 58% accuracy). |
| 19 | `prime19.ipnyb` | `archive/empty-placeholders/root__prime19.ipnyb` | Empty file with a misspelled extension. |
| 19 | `prime19.ipynb` | `research/01-prime-wave-sieve/notebooks/prime19_absolute_wave_100000th_prime.ipynb` | Uses W_abs to find the 100,000th prime; also wrongly flags 1,299,707 = 23 x 56,509. |
| 20 | `prime20.py` | `research/01-prime-wave-sieve/numbered-series/prime20_spike_superposition_v4.py` | Spike superposition, fourth variant. |
| 21 | `prime21.ipynb` | `research/01-prime-wave-sieve/notebooks/prime21_o1_prime_wave_inversion.ipynb` | Prime wave "inversion" functions and accuracy tests. |
| 22 | `prime22.py` | `research/01-prime-wave-sieve/numbered-series/prime22_mobius_von_mangoldt_indicator.py` | Exact prime indicator built from the Mobius and von Mangoldt functions. |
| 23 | `prime23.py` | `research/05-hex-sequence-puzzle/prime23_prime_hex_encoding.py` | Encodes primes from 11 upward as hex by last-digit pattern and checks periods. |
| 25 | `prime25.py` | `research/05-hex-sequence-puzzle/prime25_middle_square_generator.py` | Middle-square generator from seed FA57A5BA (matches the puzzle string for 9 characters only). |
| 26 | `prime26.py` | `archive/empty-placeholders/root__prime26.py` | Empty file (0 bytes). |
| 27 | `prime27.py` | `research/04-bit-pair-sequences/prime27_6k_plus_minus_1_pairs.py` | Pairs [is_prime(6k-1), is_prime(6k+1)]. |
| 31 | `prime31.py` | `research/07-gaps-walks-spirals/factorization-graph/prime31_factorization_relational_graph.py` | Builds an interactive pyvis graph of prime factorisations (writes relational_model_graph.html). |
| 31 | `prime31.py.tmp` | `archive/temp-files/prime31.py.tmp` | Editor temp copy of prime31.py. |

## Environment

* `requirements.txt` lists the packages the notebooks use.
* `.venv-notebooks/` is the environment that lived in `learn/pime/check/.venv`. After the move, run tools as `research/.venv-notebooks/Scripts/python -m pip …` (the old `pip.exe` launcher remembers its old path).
