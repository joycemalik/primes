# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/23_chaotic_function_model_training.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/23.py   (last edited 2025-08-27)
# What this script does  :: Trains and saves chaotic_function_model.joblib.
# ----------------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import joblib # Used for saving the trained model

# --- 1. DATA LOADING AND PREPARATION ---

def load_data(file_path):
    """Loads data from a CSV file and separates it into features (X) and target (y)."""
    df = pd.read_csv(file_path)
    # Ensure columns are named 'input' and 'output'
    if 'input' not in df.columns or 'output' not in df.columns:
        raise ValueError("CSV must contain 'input' and 'output' columns")
    
    # Reshape for scikit-learn: (n_samples, n_features)
    X = df['input'].values.reshape(-1, 1)
    y = df['output'].values
    return X, y

print("Loading datasets...")
# Define the paths to your dataset files
base_path = 'prime_dataset/'
train_path = base_path + 'train.csv'
validation_path = base_path + 'validation.csv'
test_path = base_path + 'test.csv'

# Load the data using the function
X_train, y_train = load_data(train_path)
X_val, y_val = load_data(validation_path)
X_test, y_test = load_data(test_path)

print(f"Training data loaded: {len(X_train)} samples.")
print(f"Validation data loaded: {len(X_val)} samples.")
print(f"Test data loaded: {len(X_test)} samples.")


# --- 2. MODEL DEFINITION ---

print("\nDefining the neural network model...")
# MLPRegressor is a Multi-layer Perceptron (a type of neural network)
# We set verbose=True to see the training progress for each epoch (iteration).
# max_iter is the maximum number of epochs. We'll set it higher and use early stopping.
# early_stopping=True tells the model to stop training if the validation score doesn't improve.
model = MLPRegressor(
    hidden_layer_sizes=(128, 64, 32), # Three hidden layers for complexity
    activation='relu',               # Standard activation function
    solver='adam',                   # Efficient optimizer
    max_iter=200,                    # Set max epochs high, early stopping will handle it
    random_state=42,                 # For reproducible results
    verbose=True,                    # Print progress during training
    early_stopping=True,             # Stop training when validation score is not improving
    validation_fraction=0.1,         # Use 10% of training data for validation if no validation set is passed
    n_iter_no_change=25              # Stop if no improvement for 25 consecutive epochs
)


# --- 3. MODEL TRAINING ---

print("\nStarting model training...")
# The .fit() method starts the training process.
# We pass the training data to learn the relationship.
model.fit(X_train, y_train)

print("\nTraining complete.")


# --- 4. MODEL EVALUATION ---

print("\nEvaluating model performance on the test set...")
# Use the trained model to make predictions on the unseen test data
y_pred = model.predict(X_test)

# Calculate the Mean Squared Error to see how close the predictions are to the actual values
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error on Test Data: {mse:.4f}")


# --- 5. VISUALIZATION ---

print("Visualizing results...")
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(y_test, y_pred, alpha=0.6, edgecolors='k', label='Predicted vs. Actual')
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Prediction Line')
ax.set_xlabel("Actual Output Values")
ax.set_ylabel("Predicted Output Values")
ax.set_title("Model Performance: Actual vs. Predicted")
ax.legend()
ax.grid(True)
plt.show()


# --- 6. SAVING THE TRAINED MODEL ---
# The trained model is your "local function". Let's save it.
model_filename = 'chaotic_function_model.joblib'
joblib.dump(model, model_filename)
print(f"\nModel saved as {model_filename}. You can now load this file to make future predictions.")
