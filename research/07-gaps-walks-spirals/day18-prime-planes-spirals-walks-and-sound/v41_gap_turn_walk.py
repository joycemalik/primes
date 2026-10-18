# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v41_gap_turn_walk.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v41.py   (last edited 2025-08-23)
# What this script does  :: Composites step forward, primes turn.
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import sympy
import os

def generate_prime_walk_gap_turn(limit, max_turn=np.pi):
    """
    Generates a walk where composites move one unit forward,
    and primes rotate the heading by up to `max_turn` radians.
    The rotation magnitude equals the prime gap, capped at `max_turn`.
    Turn direction is based on the prime's last digit:
      1 or 3 -> CCW (+), 7 or 9 -> CW (-).
    """
    print(f"Generating a Prime-Gap Turn Walk up to {limit} (max turn = {max_turn} rad)...")

    # Start at origin, heading 0 radians (pointing +x)
    pos = np.array([0.0, 0.0], dtype=float)
    heading = 0.0  # radians, 0 = +x

    path = [pos.copy()]

    # helper to get signed turn based on last digit
    def turn_sign(last_digit):
        # primes > 10 end with 1,3,7,9
        if last_digit in (1, 3):
            return +1.0  # CCW
        elif last_digit in (7, 9):
            return -1.0  # CW
        return 0.0

    for n in range(11, limit + 1):
        if sympy.isprime(n):
            # compute prime gap to the next prime
            npn = sympy.nextprime(n)
            gap = max(0, npn - n - 1)  # number of composites until next prime
            theta = min(max_turn, float(gap))  # "up to x radians"
            sgn = turn_sign(n % 10)
            heading += sgn * theta
            # no movement on prime
        else:
            # move one unit step along current heading
            step = np.array([np.cos(heading), np.sin(heading)], dtype=float)
            pos = pos + step
            path.append(pos.copy())

    print("Walk generation complete.")
    return np.array(path)

def plot_walk(path, limit, title_suffix="(gap-turned)"):
    print("Generating plot...")
    fig, ax = plt.subplots(figsize=(12, 12))

    x = path[:, 0]
    y = path[:, 1]
    colors = np.arange(len(path))

    scatter = ax.scatter(x, y, c=colors, cmap='viridis', s=10, zorder=3)
    ax.plot(x, y, color='gray', linewidth=0.75, alpha=0.8, zorder=2)

    ax.scatter(x[0], y[0], c='lime', s=150, marker='o', edgecolors='black', label='Start', zorder=5)
    ax.scatter(x[-1], y[-1], c='red', s=150, marker='X', label='End', zorder=5)

    ax.set_title(f'Prime Walk {title_suffix} up to {limit}', fontsize=16)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_aspect('equal', 'box')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Progression of Steps')

    out_dir = 'prime_walk_plots'
    os.makedirs(out_dir, exist_ok=True)
    fname = f'PrimeWalk_gap_turn_up_to_{limit}.png'
    out_path = os.path.join(out_dir, fname)
    plt.savefig(out_path, dpi=150)
    print(f"✅ Plot saved as: '{out_path}'")
    plt.close(fig)

if __name__ == '__main__':
    print("--- 🔀 Prime Gap-Turn Walk Plotter ---")
    print("Primes rotate by up to X radians (gap-capped); composites step forward.")

    while True:
        try:
            limit = int(input("Enter the upper numerical limit (e.g., 50000): "))
            if limit < 12:
                print("Please enter a limit of 12 or higher to see at least one step.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    while True:
        try:
            x_input = float(input("Enter max turn X (radians, e.g., 3.14159 for π): "))
            if x_input <= 0:
                print("Please enter a positive number for X.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    path_data = generate_prime_walk_gap_turn(limit, max_turn=x_input)

    if len(path_data) > 1:
        plot_walk(path_data, limit, title_suffix=f"(gap-turned, X={x_input} rad)")
    else:
        print("No composite numbers were found in the range, so no path was generated.")

    print("\n✨ Process complete!")
