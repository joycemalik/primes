# Hex sequence puzzle

**When:** 8 – 11 Aug 2025

A 782-character hex string (FA57A5BA4F24D856…) analysed by grouping, pattern search, extension, XOR tests, a middle-square generator, and Conway's Game of Life. `day11-…/` keeps the day's original order (01 … 11).

**Verdict:** The middle-square generator matches the string for only 9 characters, and the 0x1010101 group check matches 0 of 130 groups.

| File / folder | Was | Last edited | What it is |
|---|---|---|---|
| `day11-hex-grid-life-and-additive-graphs/` | `learn/pime/check/day11` | 2026-10-18 | Day 11 (11 Aug 2025): hex-string checks, Game of Life seeded from hex, seed decoding, Kolakoski, additive construction graphs. |
| `primes24_hex_sequence_analyzer.py` | `learn/primes24.py` | 2025-08-11 | Hex-sequence analyser: groupings, sliding windows, statistics. |
| `prime23_prime_hex_encoding.py` | `learn/prime23.py` | 2025-08-11 | Encodes primes from 11 upward as hex by last-digit pattern and checks periods. |
| `prime25_middle_square_generator.py` | `prime25.py` | 2025-08-11 | Middle-square generator from seed FA57A5BA (matches the puzzle string for 9 characters only). |
| `enhanced_pattern_finder.py` | `learn/enhanced_pattern_finder.py` | 2025-08-11 | Searches the hex string for repeated patterns. |
| `pattern_discovery_analyzer.py` | `learn/pattern_discovery_analyzer.py` | 2025-08-11 | Analyses the 71C3 pattern and predicts continuations. |
| `hex_sequence_extender.py` | `learn/hex_sequence_extender.py` | 2025-08-11 | Extends the hex string with discovered patterns. |
| `group_modulo_transform.py` | `learn/group_modulo_transform.py` | 2025-08-11 | Group-and-modulo transform of the hex string. |
| `group_operations_tester.py` | `learn/group_operations_tester.py` | 2025-08-11 | Tests arithmetic and XOR operations between hex groups. |
| `test_hex_generator.py` | `learn/test_hex_generator.py` | 2025-08-08 | Compares an external hex generator (Downloads/hex_sequence_generator.py) with the string. |
