# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/37_evaluate_nth_prime_expression.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/37.py   (last edited 2025-08-27)
# What this script does  :: Evaluates an evolved expression (-1.14% at n = 10^5).
# ----------------------------------------------------------------------------
"""
37.py - Test mathematical expression for nth prime approximation

This script evaluates the performance of a mathematical expression
in approximating nth prime numbers for large n values (> 100,000).
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re

# --------- Mathematical Expression ---------
EXPR = "mul(abs(log(div(-0.981, sqrt(div(sqrt(0.382), abs(abs(add(div(sqrt(0.382), abs(0.120)), mul(log(log(n)), add(0.281, n)))))))))), abs(add(n, n)))"

# --------- Safe parser/evaluator ---------
EPS = 1e-12

def sdiv(a, b):
    """Safe division that handles division by zero"""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    out = np.full_like(a, np.nan, dtype=float)
    mask = np.abs(b) > EPS
    np.divide(a, b, out=out, where=mask)
    return out

def slog(a):
    """Safe logarithm that handles negative/zero values"""
    a = np.asarray(a, dtype=float)
    aa = np.abs(a)
    out = np.zeros_like(aa, dtype=float)
    mask = aa > EPS
    np.log(aa, out=out, where=mask)
    return out

def ssqrt(a):
    """Safe square root that handles negative values"""
    a = np.asarray(a, dtype=float)
    a = np.where(np.isfinite(a), a, np.nan)
    a = np.where(a >= 0, a, np.nan)
    with np.errstate(invalid='ignore'):
        return np.sqrt(a)

# Available functions
FUNCS = {
    "add": (2, lambda a, b: a + b),
    "sub": (2, lambda a, b: a - b),
    "mul": (2, lambda a, b: a * b),
    "div": (2, sdiv),
    "sqrt": (1, ssqrt),
    "log": (1, slog),
    "abs": (1, np.abs),
}

class Parser:
    """Mathematical expression parser"""
    def __init__(self, s: str):
        diff = s.count('(') - s.count(')')
        if diff > 0:
            s = s + (')' * diff)
        self.s, self.i, self.n = s, 0, len(s)

    def peek(self): return self.s[self.i] if self.i < self.n else ''
    def eat_ws(self):
        while self.i < self.n and self.s[self.i].isspace(): self.i += 1
    def expect(self, ch):
        self.eat_ws()
        if self.peek() != ch:
            raise ValueError(f"Expected '{ch}' at pos {self.i}: ...{self.s[max(0,self.i-12):self.i+12]}...")
        self.i += 1

    def parse(self):
        self.eat_ws()
        node = self.parse_expr()
        self.eat_ws()
        if self.i != self.n:
            raise ValueError(f"Unexpected trailing input at pos {self.i}: {self.s[self.i:self.i+20]}")
        return node

    def parse_expr(self):
        self.eat_ws()
        ch = self.peek()
        if ch == '': raise ValueError("Unexpected end of input")
        if ch.isalpha():
            name = self.parse_name()
            self.eat_ws()
            if self.peek() == '(':
                self.i += 1
                args = self.parse_args()
                self.expect(')')
                return ("call", name.lower(), args)
            else:
                if name.lower() in ("x","n"): return ("var",)
                raise ValueError(f"Unknown identifier '{name}' (only x/n allowed)")
        elif ch.isdigit() or ch in "+-.":
            return ("num", self.parse_number())
        elif ch == '(':
            self.i += 1
            node = self.parse_expr()
            self.expect(')')
            return node
        else:
            raise ValueError(f"Unexpected character '{ch}' at pos {self.i}")

    def parse_name(self):
        start = self.i
        while self.i < self.n and (self.s[self.i].isalnum() or self.s[self.i]=='_'):
            self.i += 1
        return self.s[start:self.i]

    def parse_number(self):
        m = re.match(r'[+\-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+\-]?\d+)?', self.s[self.i:])
        if not m: raise ValueError(f"Invalid number at pos {self.i}")
        self.i += len(m.group(0))
        return float(m.group(0))

    def parse_args(self):
        args = []
        self.eat_ws()
        if self.peek() == ')': return args
        while True:
            args.append(self.parse_expr())
            self.eat_ws()
            if self.peek() == ',':
                self.i += 1; self.eat_ws(); continue
            break
        return args

def eval_node(node, x):
    """Evaluate a parsed expression node"""
    k = node[0]
    if k == "num": return np.full_like(x, node[1], dtype=float)
    if k == "var": return x
    if k == "call":
        name, args = node[1], [eval_node(a, x) for a in node[2]]
        if name not in FUNCS:
            raise ValueError(f"Unknown function '{name}'. Allowed: {', '.join(sorted(FUNCS))}")
        arity, func = FUNCS[name]
        if len(args) != arity:
            raise ValueError(f"Function '{name}' expects {arity} args, got {len(args)}")
        return func(*args)
    raise ValueError(f"Unknown node type: {k}")

def compile_expr(expr: str):
    """Compile mathematical expression into a function"""
    # small cleanup: fix number(var) → mul(number, var), though not needed for this expr
    num = r'([+\-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+\-]?\d+)?)'
    expr = re.sub(rf'(?<![A-Za-z_]){num}\s*\(\s*([xXnN])\s*\)',
                  lambda m: f"mul({m.group(1)}, {m.group(2).lower()})", expr)
    node = Parser(expr).parse()
    def f(x):
        return eval_node(node, x)
    return f

def sieve_primes(limit: int):
    """Generate all primes up to limit using Sieve of Eratosthenes"""
    if limit < 2:
        return []
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i:limit+1:i] = False
    return np.flatnonzero(sieve)

def nth_prime(n: int):
    """Find the nth prime number"""
    if n < 1:
        raise ValueError("n must be positive")

    # Quick answers for small n
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n <= len(small_primes):
        return small_primes[n-1]

    # Estimate upper bound using prime number theorem
    if n < 6:
        upper = 15
    else:
        ln_n = math.log(n)
        ln_ln_n = math.log(ln_n)
        upper = int(n * (ln_n + ln_ln_n)) + 10

    # Generate primes until we have enough
    limit = upper
    for attempt in range(5):  # Allow up to 5 expansions
        primes = sieve_primes(limit)
        if len(primes) >= n:
            return int(primes[n-1])  # n-1 because primes[0] is the 1st prime
        limit = int(limit * 1.2) + 1000

    raise RuntimeError(f"Could not find the {n}th prime within reasonable limits")

def generate_test_data(num_samples: int = 10, min_n: int = 100000):
    """Generate test data with n > min_n"""
    # Generate n values spaced logarithmically for better coverage
    max_n = min_n + 100000  # Spread over 100k range

    # Use logarithmic spacing for better distribution
    n_values = np.logspace(np.log10(min_n), np.log10(max_n), num_samples)
    n_values = np.unique(np.round(n_values).astype(int))

    # Ensure we have exactly num_samples
    if len(n_values) < num_samples:
        additional = np.random.choice(range(min_n, max_n), num_samples - len(n_values), replace=False)
        n_values = np.concatenate([n_values, additional])
        n_values = np.unique(n_values)

    n_values = n_values[:num_samples]  # Take first num_samples

    test_data = []
    print(f"Generating test data for {len(n_values)} n values > {min_n}...")

    for i, n in enumerate(n_values):
        print(f"Computing {i+1}/{len(n_values)}: n = {n}")
        try:
            nth_prime_val = nth_prime(n)
            test_data.append((int(n), int(nth_prime_val)))
        except Exception as e:
            print(f"Warning: Could not compute {n}th prime: {e}")
            continue

    return test_data

def evaluate_function_on_test_data(f, test_data):
    """Evaluate the mathematical function on test data"""
    n_values = np.array([n for n, _ in test_data])
    actual_primes = np.array([p for _, p in test_data])

    # Evaluate function
    predicted_primes = f(n_values.astype(float))

    # Calculate errors
    errors = predicted_primes - actual_primes
    abs_errors = np.abs(errors)
    relative_errors = abs_errors / actual_primes

    # Create results dataframe
    results_df = pd.DataFrame({
        'n': n_values,
        'actual_nth_prime': actual_primes,
        'predicted_prime': predicted_primes,
        'error': errors,
        'abs_error': abs_errors,
        'relative_error': relative_errors
    })

    # Calculate metrics
    mae = float(abs_errors.mean())
    mape = float(relative_errors.mean())
    rmse = float(np.sqrt(np.mean(errors**2)))
    max_error = float(abs_errors.max())

    return results_df, mae, mape, rmse, max_error

def plot_results(results_df, save_path=None):
    """Create scatter plot of actual vs predicted values"""
    plt.figure(figsize=(10, 6))

    # Scatter plot
    plt.scatter(results_df['actual_nth_prime'], results_df['predicted_prime'],
               alpha=0.7, s=50, edgecolors='black', linewidth=0.5)

    # Perfect prediction line
    min_val = min(results_df['actual_nth_prime'].min(), results_df['predicted_prime'].min())
    max_val = max(results_df['actual_nth_prime'].max(), results_df['predicted_prime'].max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect prediction')

    plt.xlabel('Actual nth Prime', fontsize=12)
    plt.ylabel('Predicted Prime (f(n))', fontsize=12)
    plt.title('Mathematical Function Performance: Actual vs Predicted Primes', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add some statistics as text
    mae = results_df['abs_error'].mean()
    mape = results_df['relative_error'].mean()
    stats_text = '.2f'
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()

def main():
    """Main function to run the evaluation"""
    print("=" * 60)
    print("Mathematical Expression Evaluation for nth Prime Approximation")
    print("=" * 60)
    print(f"Expression: {EXPR}")
    print()

    # Compile the mathematical expression
    print("Compiling mathematical expression...")
    try:
        f = compile_expr(EXPR)
        print("✓ Expression compiled successfully")
    except Exception as e:
        print(f"✗ Failed to compile expression: {e}")
        return

    # Generate test data
    print("\nGenerating test data...")
    test_data = generate_test_data(num_samples=10, min_n=100000)

    if not test_data:
        print("✗ No test data generated")
        return

    print(f"✓ Generated {len(test_data)} test samples")
    print("\nTest data preview:")
    for n, prime in test_data[:5]:  # Show first 5
        print("8d")

    # Evaluate function
    print("\nEvaluating function on test data...")
    try:
        results_df, mae, mape, rmse, max_error = evaluate_function_on_test_data(f, test_data)
        print("✓ Evaluation completed")
    except Exception as e:
        print(f"✗ Evaluation failed: {e}")
        return

    # Display results
    print("\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)
    print("10.2f")
    print("8.4f")
    print("10.2f")
    print("10.2f")
    print()

    # Save results to CSV
    output_dir = Path("evaluation_output")
    output_dir.mkdir(exist_ok=True)

    csv_path = output_dir / "nth_prime_evaluation.csv"
    results_df.to_csv(csv_path, index=False)
    print(f"✓ Results saved to: {csv_path}")

    # Create and save plot
    plot_path = output_dir / "actual_vs_predicted.png"
    plot_results(results_df, save_path=plot_path)

    # Show detailed results
    print("\nDetailed Results:")
    print(results_df.to_string(index=False))

    print("\n" + "=" * 60)
    print("Evaluation completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
