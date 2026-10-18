# day18-prime-planes-spirals-walks-and-sound

Day 18 (18-24 Aug 2025): functions on a prime plane, radial spirals, 2D and 3D prime walks, animations and sonification. Output folders keep their original names because the scripts write to them.

Moved from `learn/pime/check/day18`.

| Item | Was | Last edited | What it is |
|---|---|---|---|
| `3d_prime_walks/` | same name | 2025-08-23 | Output / data folder (2 files, 714 KB); name kept because scripts use it. |
| `continuous_comparison_plots/` | same name | 2025-08-22 | Output / data folder (19 files, 2 MB); name kept because scripts use it. |
| `final_comparison_plots/` | same name | 2025-08-22 | Output / data folder (19 files, 3 MB); name kept because scripts use it. |
| `functions copy.txt` | same name | 2025-08-22 | |
| `functions.txt` | same name | 2025-08-24 | |
| `g1_print_modulo_function_list.py` | `g1.py` | 2025-08-24 | Prints the list of "x % i" functions used for the radial plots. |
| `g2_frames_to_animation.py` | `g2.py` | 2025-08-24 | Turns numbered PNG frames into an animation (GIF/MP4). |
| `g3_frames_to_consistent_video.py` | `g3.py` | 2025-08-24 | Resizes frames to one size and writes a video. |
| `g5_images_to_animation.py` | `g5.py` | 2025-08-24 | Animates the generated_images folder. |
| `generated_images/` | same name | 2025-08-24 | Output / data folder (54 files, 18 MB); name kept because scripts use it. |
| `generated_midi/` | same name | 2025-08-24 | Output / data folder (54 files, 118 KB); name kept because scripts use it. |
| `interactive_3d_walks/` | same name | 2025-08-23 | Output / data folder (3 files, 72 MB); name kept because scripts use it. |
| `interactive_graphs/` | same name | 2025-08-22 | Output / data folder (18 files, 82 MB); name kept because scripts use it. |
| `prime_3d_graphs/` | same name | 2025-08-22 | Output / data folder (17 files, 3 MB); name kept because scripts use it. |
| `prime_gap_walk_plots/` | same name | 2025-08-23 | Output / data folder (2 files, 347 KB); name kept because scripts use it. |
| `prime_graphs/` | same name | 2025-08-22 | Output / data folder (18 files, 1 MB); name kept because scripts use it. |
| `prime_plane_graphs/` | same name | 2025-08-22 | Output / data folder (18 files, 3 MB); name kept because scripts use it. |
| `prime_push_plots/` | same name | 2025-08-24 | Output / data folder (7 files, 591 KB); name kept because scripts use it. |
| `prime_river_plots/` | same name | 2025-08-23 | Output / data folder (1 files, 115 KB); name kept because scripts use it. |
| `prime_spiral_plots/` | same name | 2025-08-22 | Output / data folder (19 files, 2 MB); name kept because scripts use it. |
| `prime_walk_plots/` | same name | 2025-08-23 | Output / data folder (14 files, 2 MB); name kept because scripts use it. |
| `radial_comparison_plots/` | same name | 2025-08-22 | Output / data folder (19 files, 7 MB); name kept because scripts use it. |
| `radial_plot_gen2/` | same name | 2025-08-24 | Output / data folder (400 files, 219 MB); name kept because scripts use it. |
| `radial_plots/` | same name | 2025-08-24 | Output / data folder (528 files, 243 MB); name kept because scripts use it. |
| `radial_plots_animation.gif` | same name | 2025-08-24 | |
| `radial_plots_animation.mp4` | same name | 2025-08-24 | |
| `radial_plots_animation2.gif` | same name | 2025-08-24 | |
| `radial_plots_animation2.mp4` | same name | 2025-08-24 | |
| `radial_plots_animation3.mp4` | same name | 2025-08-24 | |
| `radial_plots_generator/` | same name | 2025-08-24 | Output / data folder (400 files, 248 MB); name kept because scripts use it. |
| `raw_prompts_approach.txt` | same name | 2025-08-22 | |
| `signature_plots/` | same name | 2025-08-23 | Output / data folder (19 files, 4 MB); name kept because scripts use it. |
| `sonified_videos/` | same name | 2025-08-24 | Output / data folder (11 files, 10 MB); name kept because scripts use it. |
| `sonified_videos_1/` | same name | 2025-08-24 | Output / data folder (1 files, 3 MB); name kept because scripts use it. |
| `spiral_comparison_plots/` | same name | 2025-08-22 | Output / data folder (19 files, 7 MB); name kept because scripts use it. |
| `static_comparison_plots/` | same name | 2025-08-22 | Output / data folder (18 files, 3 MB); name kept because scripts use it. |
| `v01_function_on_prime_plane.py` | `v1.py` | 2025-08-22 | Plots y = f(x) with the x-axis made of primes (2, 3, 5, 7, ...). |
| `v02_function_on_prime_plane_v2.py` | `v2.py` | 2025-08-22 | Second version of the prime-plane plot. |
| `v03_prime_plane_batch_plots.py` | `v3.py` | 2025-08-22 | Batch prime-plane plots saved to prime_plane_graphs/. |
| `v04_prime_vs_integer_inputs.py` | `v4.py` | 2025-08-22 | Compares f on prime inputs with f on integer inputs. |
| `v05_3d_function_plots.py` | `v5.py` | 2025-08-22 | 3D versions of the function plots (prime_3d_graphs/). |
| `v06_palindromic_prime_interactive.py` | `v6.py` | 2025-08-22 | Interactive plots over palindromic primes and other sequences. |
| `v07_composite_squeeze_interactive.py` | `v7.py` | 2025-08-22 | Interactive "composite squeeze" plots. |
| `v08_composite_squeeze_comparison.py` | `v8.py` | 2025-08-22 | Squeeze plot vs standard plot. |
| `v09_radial_function_spiral.py` | `v9.py` | 2025-08-24 | Radial function spirals (radial_plots/). |
| `v10_continuous_squeeze_comparison.py` | `v10.py` | 2025-08-22 | Continuous squeeze comparison. |
| `v11_final_squeeze_comparison.py` | `v11.py` | 2025-08-22 | Final squeeze comparison. |
| `v13_radial_angle_by_smallest_factor.py` | `v13.py` | 2025-08-22 | Radial plot with angle set by the smallest prime factor. |
| `v17_prime_landmark_spiral.py` | `v17.py` | 2025-08-22 | Spiral with angles warped toward prime landmarks. |
| `v19_prime_factor_signature.py` | `v19.py` | 2025-08-22 | Prime-factor signature plots (signature_plots/). |
| `v23_prime_waterfall_simulation.html` | `v23.html` | 2025-08-23 | Browser "prime waterfall" simulation. |
| `v29_prime_direction_walk.py` | `v29.py` | 2025-08-23 | Walk whose direction is set by primes. |
| `v31_prime_composite_walk.py` | `v31.py` | 2025-08-23 | Walk driven by primes and composites. |
| `v37_prime_composite_walk_copy.py` | `v37.py` | 2025-08-23 | Identical copy of v31. |
| `v41_gap_turn_walk.py` | `v41.py` | 2025-08-23 | Composites step forward, primes turn. |
| `v43_gap_turn_walk_by_last_digit.py` | `v43.py` | 2025-08-23 | Turn by gap, direction set by the last digit (prime_walk_plots/). |
| `v51_3d_rotation_walk.py` | `v51.py` | 2025-08-23 | 3D walk: rotate by (gap - 1) about y or z depending on last digit. |
| `v53_3d_rotation_walk_interactive.py` | `v53.py` | 2025-08-23 | Interactive Plotly version of the 3D walk. |
| `v59_3d_rotation_walk_interactive_copy.py` | `v59.py` | 2025-08-23 | Identical copy of v53. |
| `v61_prime_river.py` | `v61.py` | 2025-08-23 | The "prime river" path. |
| `v67_prime_push_walk.py` | `v67.py` | 2025-08-23 | "Prime push" walk (prime_push_plots/). |
| `v71_radial_spiral_sonified_midi.py` | `v71.py` | 2025-08-24 | Radial spiral frames plus a MIDI sonification. |
| `v73_spiral_animation_with_sound.py` | `v73.py` | 2025-08-24 | Spiral animation with sound, one prime per frame. |
| `v79_accelerating_spiral_animation_with_sound.py` | `v79.py` | 2025-08-24 | Accelerating spiral animation with smoothed audio (sonified_videos/). |
