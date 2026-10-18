# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v43_gap_turn_walk_by_last_digit.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v43.py   (last edited 2025-08-23)
# What this script does  :: Turn by gap, direction set by the last digit (prime_walk_plots/).
# ----------------------------------------------------------------------------
import numpy as np
import sympy
import matplotlib.pyplot as plt
import os

def prime_gap(n: int) -> int:
    """
    Return the number of composites after n up to (but not including) the next prime.
    If p = nextprime(n), gap = p - n - 1.
    """
    p_next = sympy.nextprime(n)
    return max(0, p_next - n - 1)

def generate_prime_gap_turn_walk(limit: int, theta_scale: float = 1.0, gamma_scale: float = 1.0, step_size: float = 1.0):
    """
    Generate a path where primes rotate and composites move.
    
    Parameters
    ----------
    limit : int
        Highest integer to consider (inclusive).
    theta_scale : float
        Radian multiplier used for digits {1,7}.
    gamma_scale : float
        Radian multiplier used for digits {3,9}.
    step_size : float
        Distance moved on each composite.
        
    Returns
    -------
    path : np.ndarray of shape (k, 2)
        Sequence of (x, y) positions after each composite step (including the start).
    meta : dict
        Useful metadata (e.g., final angle).
    """
    if limit < 12:
        return np.array([[0.0, 0.0]]), {"final_angle": 0.0}
    
    pos = np.array([0.0, 0.0], dtype=float)
    angle = 0.0  # radians, 0 points to +x (right)

    path = [pos.copy()]
    
    for n in range(11, limit + 1):
        if sympy.isprime(n):
            # Compute the gap once, then adjust heading based on last digit
            gap = prime_gap(n)
            last = n % 10
            if last == 1:
                angle += theta_scale * gap
            elif last == 3:
                angle += gamma_scale * gap
            elif last == 7:
                angle -= theta_scale * gap
            elif last == 9:
                angle -= gamma_scale * gap
            # (2 and 5 won't occur here since we start at 11)
        else:
            # Move one step forward in current heading
            dx = step_size * np.cos(angle)
            dy = step_size * np.sin(angle)
            pos = pos + np.array([dx, dy], dtype=float)
            path.append(pos.copy())
    
    return np.array(path), {"final_angle": angle}

def plot_walk(path: np.ndarray, limit: int, theta_scale: float, gamma_scale: float, outdir: str = "prime_gap_walk_plots"):
    """
    Visualize the walk with a simple scatter+line and save to disk.
    """
    os.makedirs(outdir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 12))
    
    x, y = path[:, 0], path[:, 1]
    t = np.arange(len(path))  # for color progression
    
    sc = ax.scatter(x, y, c=t, cmap='viridis', s=10, zorder=3)
    ax.plot(x, y, color='gray', linewidth=0.75, alpha=0.8, zorder=2)
    
    ax.scatter(path[0,0], path[0,1], c='lime', s=150, marker='o', edgecolors='black', label='Start', zorder=5)
    ax.scatter(path[-1,0], path[-1,1], c='red', s=150, marker='X', label='End', zorder=5)
    
    ax.set_title(f'Prime Gap Turn Walk up to {limit}\nθ-scale={theta_scale}, γ-scale={gamma_scale}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect('equal', 'box')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    cbar = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Composite Step Index')
    
    fname = os.path.join(outdir, f'PrimeGapWalk_limit{limit}_theta{theta_scale}_gamma{gamma_scale}.png')
    plt.savefig(fname, dpi=150)
    plt.close(fig)
    print(f"✅ Plot saved to {fname}")

if __name__ == "__main__":
    print("--- 🔁 Prime Gap Turn Walk ---")
    print("Primes rotate by (gap * scale), composites move one step.")
    try:
        limit = int(input("Enter the upper limit (e.g., 50000): "))
    except ValueError:
        raise SystemExit("Please enter a whole number.")
    if limit < 12:
        raise SystemExit("Enter a limit ≥ 12.")
    
    # Tune these to make each of {1,3,7,9} feel distinct
    theta_scale = float(input("theta_scale (e.g., 1.0): ") or 1.0)
    gamma_scale = float(input("gamma_scale (e.g., 0.75): ") or 1.0)
    
    path, meta = generate_prime_gap_turn_walk(limit, theta_scale, gamma_scale)
    if len(path) > 1:
        plot_walk(path, limit, theta_scale, gamma_scale)
    else:
        print("No composite steps occurred; nothing to plot.")
