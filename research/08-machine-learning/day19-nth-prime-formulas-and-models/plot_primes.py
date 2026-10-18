# -*- coding: utf-8 -*-
"""
Plot real primes vs predicted primes using the model trained in 7.py
Saves the figure as `primes_vs_predicted.png` in the same folder.
This script loads `7.py` as a module (so it will train the model the same way)
and then computes predictions for the generated corpus and saves a PNG.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def load_module_from_path(path: Path, name: str = "model7"):
	spec = importlib.util.spec_from_file_location(name, str(path))
	module = importlib.util.module_from_spec(spec)
	loader = spec.loader
	if loader is None:
		raise ImportError(f"Can't load module from {path}")
	loader.exec_module(module)
	return module


def main():
	script_dir = Path(__file__).resolve().parent
	module_path = script_dir / "07_nth_prime_linear_regression.py"
	if not module_path.exists():
		print(f"Error: {module_path} not found")
		return

	# Load 7.py as a module (it will run and create `primes_corpus` and `g`)
	module = load_module_from_path(module_path)

	# Extract the corpus and prediction function
	try:
		primes_corpus = getattr(module, "primes_corpus")
		predict_fn = getattr(module, "g")
	except AttributeError as e:
		print("Required symbols not found in 7.py:", e)
		return

	# Prepare data
	n_values = np.arange(1, len(primes_corpus) + 1)

	# Compute predictions (use vectorized comprehension)
	predictions = np.array([predict_fn(int(n)) for n in n_values])
	actuals = np.array(primes_corpus)

	# Plot
	plt.style.use("ggplot")
	fig, ax = plt.subplots(figsize=(10, 6))
	ax.plot(n_values, actuals, label="Actual primes (p_n)", color="#1f77b4")
	ax.plot(n_values, predictions, label="Predicted primes (model)", color="#ff7f0e", linestyle="--")
	ax.set_xlabel("n (index of prime)")
	ax.set_ylabel("Prime value")
	ax.set_title("Actual primes vs Predicted primes")
	ax.legend()

	out_path = script_dir / "primes_vs_predicted.png"
	fig.tight_layout()
	plt.show()
	fig.savefig(out_path, dpi=150)
	print(f"Saved plot to: {out_path}")


if __name__ == "__main__":
	main()
