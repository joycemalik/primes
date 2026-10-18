# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/29_gplearn_symbolic_regression.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/29.py   (last edited 2025-08-27)
# What this script does  :: gplearn symbolic regression for p_n.
# ----------------------------------------------------------------------------
import pandas as pd
from gplearn.genetic import SymbolicRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from sklearn.utils.validation import validate_data
from gplearn.genetic import SymbolicRegressor, SymbolicTransformer, SymbolicClassifier
from gplearn.functions import make_function

EPS = 1e-12

def _safe_exp(x):
    # clip to prevent overflow
    return np.exp(np.clip(x, -50, 50))

import numpy as np
EPS = 1e-12

def _safe_inv(x):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x, dtype=float)
    mask = np.abs(x) > EPS
    # only divide where mask is True; elsewhere leave zeros in `out`
    np.divide(1.0, x, out=out, where=mask)
    return out


def _safe_tan(x):
    # protect near asymptotes; clip extremes
    y = np.tan(x)
    y = np.where(np.isfinite(y), y, 0.0)
    return np.clip(y, -1e6, 1e6)

# Wrap as gplearn Function objects
exp = make_function(function=_safe_exp, name='exp', arity=1)
inv = make_function(function=_safe_inv, name='inv', arity=1)
sin = make_function(function=np.sin,     name='sin', arity=1)
cos = make_function(function=np.cos,     name='cos', arity=1)
tan = make_function(function=_safe_tan,  name='tan', arity=1)


def _gp_validate_data(self, X, y=None, **kwargs):
    # Drop-in replacement for the removed BaseEstimator._validate_data
    # Works with sklearn >= 1.6 (where validate_data was introduced)
    return validate_data(self, X=X, y=y, **kwargs)

for cls in (SymbolicRegressor, SymbolicTransformer, SymbolicClassifier):
    if not hasattr(cls, "_validate_data"):
        cls._validate_data = _gp_validate_data


# --- 1. DATA LOADING ---
# Load the complete dataset to find the universal rule.
try:
    df = pd.read_csv('prime_dataset/complete_dataset.csv')
except FileNotFoundError:
    print("Error: 'prime_dataset/complete_dataset.csv' not found.")
    print("Please make sure the dataset is in the correct folder.")
    exit()

X = df['input'].values.reshape(-1, 1)
y = df['output'].values

# Split data to prevent the model from seeing the test set during evolution
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 2. SYMBOLIC REGRESSION MODEL ---
print("Starting Symbolic Regression...")
# Define the regressor
est_gp = SymbolicRegressor(
    population_size=5000,
    generations=6,
    stopping_criteria=0.01,
    p_crossover=0.7,
    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    verbose=1,
    feature_names=['n'], # Name your input variable
    function_set=('add','sub','mul','div','sqrt','log','abs'),
    random_state=42
)


# --- 3. TRAINING ---
est_gp.fit(X_train, y_train)

# --- 4. RESULTS ---
# Print the formula the model discovered
print("\n" + "="*40)
print("Discovered symbolic formula:")
print(est_gp._program)
print("="*40 + "\n")

# --- 5. VISUALIZATION ---
print("Visualizing model performance on test data...")
# Make predictions on the unseen test data
y_pred = est_gp.predict(X_test)

# Create the scatter plot
# --- Line plot like your example (first N points) ---
N = 100  # how many points to show

# 1) Sort by X so it looks like a time series
order = np.argsort(X_test.ravel())
x_sorted   = X_test.ravel()[order]
y_true     = y_test[order]
y_pred_srt = y_pred[order]

# 2) Plot as two lines over "time steps" (0..N-1)
steps = np.arange(min(N, len(y_true)))

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(steps, y_true[:N], label='Actual')
ax.plot(steps, y_pred_srt[:N], label='Predicted')

ax.set_title("Time Series Comparison (First 100 Points)")
ax.set_xlabel("Time Step")
ax.set_ylabel("Output Value")  # rename to "Prime Value" if that's your target
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
