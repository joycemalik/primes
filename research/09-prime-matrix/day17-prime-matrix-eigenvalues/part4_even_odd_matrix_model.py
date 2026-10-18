# ----------------------------------------------------------------------------
# Prime research archive :: research/09-prime-matrix/day17-prime-matrix-eigenvalues/part4_even_odd_matrix_model.py
# Original location      :: research/09-prime-matrix/day17-prime-matrix-eigenvalues/part4.py   (last edited 2025-08-21)
# What this script does  :: Toy matrix model of the even/odd N difference.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def generate_matrix(N):
    """
    Generates a matrix based on a model that alternates structure for even/odd N.
    """
    A = np.zeros((N, N))

    # Create the main chain links (predator-prey)
    for i in range(N - 1):
        # Growing interaction strengths
        A[i, i + 1] = np.sqrt((i + 2) * (N - i - 1))
        A[i + 1, i] = np.sqrt((i + 2) * (N - i - 1))

    # The crucial "rule-breaker" for ODD N
    if N % 2 != 0:
        # Add a feedback loop that breaks the bipartite structure
        A[0, N - 1] = 1.0 # A link from the last species back to the first

    return A

# --- Visualize the Simulation vs. Your Data ---
fig, axes = plt.subplots(2, 4, figsize=(20, 10), sharex=True, sharey=True)

# N values to compare
n_vals_to_plot = [20, 21, 80, 81]

for i, n in enumerate(n_vals_to_plot):
    # Your Data (approximated from your text for plotting)
    # This part is illustrative; the full data would be used for exact matching.
    # We will simulate and show the pattern holds.

    # Our Simulation
    ax_sim = axes[0, i]
    mat_sim = generate_matrix(n)
    eigs_sim = np.linalg.eigvals(mat_sim)
    ax_sim.scatter(eigs_sim.real, eigs_sim.imag, c='r', marker='x', label=f'Simulated (N={n})')
    ax_sim.set_title(f'Simulation: N={n} ({"Odd" if n%2 else "Even"})')
    ax_sim.grid(True, linestyle=':')
    ax_sim.axhline(0, color='grey', lw=0.5)
    ax_sim.axvline(0, color='grey', lw=0.5)

    # Plot the matrix structure from our simulation
    ax_mat = axes[1, i]
    im = ax_mat.imshow(mat_sim != 0, cmap='binary', interpolation='none')
    ax_mat.set_title(f'Matrix Structure (N={n})')


axes[0,0].set_ylabel('Imaginary Part')
axes[1,0].set_ylabel('Matrix Rows')
fig.text(0.5, 0.48, 'Matrix Columns', ha='center')
fig.text(0.5, 0.92, 'Eigenvalues on the Complex Plane', ha='center', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.show()