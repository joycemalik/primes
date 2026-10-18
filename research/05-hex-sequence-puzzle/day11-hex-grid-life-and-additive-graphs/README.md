# day11-hex-grid-life-and-additive-graphs

Day 11 (11 Aug 2025): hex-string checks, Game of Life seeded from hex, seed decoding, Kolakoski, additive construction graphs.

Moved from `learn/pime/check/day11`.

| Item | Was | Last edited | What it is |
|---|---|---|---|
| `01_hex_group_multiplier_check.py` | `1.py` | 2025-08-11 | Checks 6-digit hex groups: g * 0x1010101 mod 2^24 == 0xBC614E (matches 0 of 130). |
| `02_hex_group_check_decimal.py` | `2.py` | 2025-08-11 | The same check done in decimal arithmetic. |
| `03_hex_to_48x48_grid.py` | `3.py` | 2025-08-11 | Turns the hex string into a 48 x 48 binary grid. |
| `04_game_of_life_from_hex.py` | `4.py` | 2025-08-11 | Conway's Game of Life on a torus seeded from the hex grid. |
| `05_seed_decimal_comparison.py` | `5.py` | 2025-08-12 | Two long decimal seeds stored for comparison. |
| `06_decimal_seed_to_pairs.py` | `6.py` | 2025-08-12 | Decodes a decimal seed into a bitstream of prime pairs. |
| `07_kolakoski_sequence.py` | `7.py` | 2025-08-12 | Kolakoski sequence and subword counts (same as kolakoski_subword_complexity.py). |
| `08_additive_construction_graph.py` | `8.py` | 2025-08-12 | Integer partitions as an additive construction graph with Dijkstra paths. |
| `09_compare_two_strings.py` | `compare_strings.py` | 2025-08-12 | Finds where two long strings start to differ. |
| `10_additive_shortest_paths.py` | `test_complex_path.py` | 2025-08-13 | Shortest additive construction paths with alternatives. |
| `11_additive_shortest_paths_small.py` | `test_dijkstra.py` | 2025-08-12 | The same Dijkstra test on smaller numbers. |
