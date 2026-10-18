# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/07_nth_prime_linear_regression.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/7.py   (last edited 2025-08-26)
# What this script does  :: Linear regression for the nth prime (loaded by 08 and plot_primes.py).
# ----------------------------------------------------------------------------
"""
This script uses machine learning (Linear Regression) to predict the nth prime number.
The core concept is to use the Prime Number Theorem (p_n ≈ n*ln(n)) as a
powerful feature, allowing the model to learn a highly accurate prediction
from a relatively small dataset.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import math

# --- Step 1: Generate a "Small Corpus" of Data ---
# We'll generate the first 20,000 primes to serve as our ground truth.
# This is small in the grand scheme of number theory but sufficient for our model.

def generate_primes_corpus(num_primes):
    """
    Generates the first `num_primes` prime numbers.
    This is a reasonably efficient implementation for generating a moderately
    sized list of primes.
    """
    primes = []
    candidate = 2
    while len(primes) < num_primes:
        is_prime = True
        # Check for divisibility only up to the square root of the candidate
        limit = int(math.sqrt(candidate))
        for p in primes:
            if p > limit:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

# --- Main Script ---

# Define the size of our training data
CORPUS_SIZE = 2000
print(f"Generating a corpus of the first {CORPUS_SIZE} prime numbers...")
primes_corpus = generate_primes_corpus(CORPUS_SIZE)
print(f"Corpus created. The {CORPUS_SIZE}th prime is {primes_corpus[-1]}. 👍\n")


# --- Step 2: Feature Engineering & Data Preparation ---
# The target variable 'y' is the prime number itself.
y = np.array(primes_corpus)

# The input 'n' is the position of the prime in the sequence (1-based).
n_values = np.arange(1, len(primes_corpus) + 1)

# **Feature Engineering:** This is the most critical step.
# Instead of just using 'n', we provide a feature derived from the Prime Number Theorem.
# The theorem states p_n is approximately n * log(n).
# We handle n=1 separately since log(1)=0.
feature_n_log_n = n_values * np.log(n_values, where=(n_values > 1))

# We create our feature matrix X. We'll give the model both 'n' and 'n*log(n)'
# so it can learn the optimal linear combination.
X = np.c_[n_values, feature_n_log_n]


# --- Step 3: Model Training ---
# We split our data into a training set (80%) and a testing set (20%).
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# We choose a simple but effective model: Linear Regression.
# It will learn a function of the form: p_n ≈ w1*n + w2*(n*ln(n)) + b
model = LinearRegression()

# Train the model on our training data.
model.fit(X_train, y_train)

print("Model training complete. 🧠\n")
score = model.score(X_test, y_test)
print(f"Model R^2 score on test data: {score:.6f} (This indicates an excellent fit!)\n")


# --- Step 4: Create the Prediction Function g(n, x) ---
def g(n):
    """
    Predicts the nth prime number using the trained machine learning model.
    This function encapsulates the feature engineering required for a prediction.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input 'n' must be a positive integer.")
    
    # We must apply the *exact same feature engineering* to our new input 'n'.
    n_log_n_feature = n * math.log(n) if n > 1 else 0
    
    # The model expects a 2D array for prediction.
    features = np.array([[n, n_log_n_feature]])
    
    # Use the trained model to predict the prime.
    prediction = model.predict(features)
    
    return prediction[0]

# --- Step 5: Demonstration ---
# Let's test the model with the examples you provided.
print("--- Model Predictions ---")
test_cases = [1000, 500, 1800]

for n_val in test_cases:
    # Get the actual prime from our generated corpus for comparison.
    # We use n_val - 1 because our list is 0-indexed.
    actual_prime = primes_corpus[n_val - 1]
    
    # Get the model's prediction using our function g(n).
    predicted_prime = g(n_val)
    
    # Calculate the percentage error.
    error_percent = abs(actual_prime - predicted_prime) / actual_prime * 100
    
    print(f"n = {n_val}:")
    print(f"  Actual Prime    = {actual_prime}")
    print(f"  Predicted Prime = {predicted_prime:.2f}")
    print(f"  Error           = {error_percent:.3f}%\n")