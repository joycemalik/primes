# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/11_plot_function.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/11.py   (last edited 2025-08-26)
# What this script does  :: Plots y = f(x) from the command line.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def plot_function(f, x_min, x_max, *,
                  n=2000,
                  title=None,
                  xlabel="x",
                  ylabel="f(x)",
                  grid=True,
                  safe=True,
                  samples=None,
                  logx=False,
                  logy=False,
                  show=True):
    """
    Plot y = f(x) on [x_min, x_max].

    Parameters
    ----------
    f : callable
        Function accepting a float or ndarray and returning a float/ndarray.
    x_min, x_max : float
        Domain to plot over (inclusive).
    n : int
        Number of sample points (ignored if `samples` is given).
    title, xlabel, ylabel : str
        Plot labels.
    grid : bool
        Show background grid.
    safe : bool
        If True, evaluates point-by-point and masks failures (good for discontinuities).
        If False, assumes f is NumPy-vectorized and evaluates in one shot (faster).
    samples : array-like | None
        Custom x-samples to use instead of a linear linspace.
    logx, logy : bool
        Use logarithmic x and/or y scales.
    show : bool
        Call plt.show() before returning.

    Returns
    -------
    (fig, ax, x, y) : tuple
        Matplotlib figure/axes and the sampled x, y arrays.
    """
    if samples is not None:
        x = np.asarray(samples, dtype=float)
    else:
        x = np.linspace(x_min, x_max, int(n))

    # Evaluate f with masking for errors / discontinuities
    if safe:
        y = np.empty_like(x, dtype=float)
        y.fill(np.nan)
        for i, xi in enumerate(x):
            try:
                yi = f(float(xi))
                # Handle complex outputs by defaulting to real part
                if np.iscomplexobj(yi):
                    yi = np.real(yi)
                y[i] = float(yi)
            except Exception:
                # leave as NaN (breaks the line so discontinuities don't connect)
                pass
    else:
        with np.errstate(all='ignore'):
            y = f(x)
        y = np.asarray(y)
        if np.iscomplexobj(y):
            y = np.real(y)
        y = y.astype(float, copy=False)
        y[~np.isfinite(y)] = np.nan

    fig, ax = plt.subplots()

    # Apply axis scales
    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")

    # Plot; NaNs automatically split the line
    ax.plot(x, y)

    # Labels & cosmetics
    if title: ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if grid:
        ax.grid(True, which="both", alpha=0.3)

    if show:
        plt.show()

    return fig, ax, x, y


def main():
    """Demo CLI for plot_function. Saves an example plot to a PNG by default.

    Examples supported: sin, reciprocal, step, log, gaussian
    """
    import argparse
    from pathlib import Path
    import math

    parser = argparse.ArgumentParser(description="Demo plotter for plot_function")
    parser.add_argument("--example", choices=["sin", "reciprocal", "step", "log", "gaussian"],
                        default="sin", help="Which example function to plot")
    parser.add_argument("--n", type=int, default=2000, help="Number of sample points")
    parser.add_argument("--outfile", type=str, default=None, help="Path to save PNG (default: ./11_<example>.png)")
    args = parser.parse_args()

    example = args.example
    n = args.n

    if example == "sin":
        f = np.sin
        x_min, x_max = 0.0, 2.0 * math.pi
        title = "sin(x)"
    elif example == "reciprocal":
        f = lambda x: 1.0 / x
        x_min, x_max = -1.0, 1.0
        title = "1/x (reciprocal) — discontinuity at 0"
    elif example == "step":
        f = lambda x: 1.0 if x >= 0 else 0.0
        x_min, x_max = -1.0, 1.0
        title = "Step function"
    elif example == "log":
        f = np.log
        x_min, x_max = 0.01, 10.0
        title = "log(x)"
    elif example == "gaussian":
        f = lambda x: math.exp(-x * x / 2.0)
        x_min, x_max = -5.0, 5.0
        title = "Gaussian exp(-x^2/2)"
    else:
        raise SystemExit("Unknown example")

    # Choose safe=True for potentially problematic examples
    safe = True

    # Build default outfile path if not provided
    out_path = Path(args.outfile) if args.outfile else (Path.cwd() / f"11_{example}.png")

    print(f"Plotting example '{example}' -> {out_path} (samples={n})")
    fig, ax, x, y = plot_function(f, x_min, x_max, n=n, title=title, xlabel="x", ylabel="f(x)",
                                  grid=True, safe=safe, show=False)

    # Ensure output directory exists and save
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    print(f"Saved plot to: {out_path}")


if __name__ == "__main__":
    main()
