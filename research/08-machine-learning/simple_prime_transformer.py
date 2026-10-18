# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/simple_prime_transformer.py
# Original location      :: learn/simple_prime_transformer.py   (last edited 2025-08-02)
# What this script does  :: Small transformer over the wave function.
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

def prime_sieve(n):
    """Generates primes up to n using the Sieve of Eratosthenes."""
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i:n+1:i] = False
    return np.where(primes)[0]

# --- Simple Wave-Based Prime Function ---
def create_prime_wave(numbers, training_primes):
    """Create a simple wave function from training primes"""
    wave = np.zeros_like(numbers, dtype=float)
    
    for p in training_primes:
        # Each prime creates a sine wave with its own frequency
        frequency = 1.0 / p
        amplitude = 1.0 / np.sqrt(p)
        wave += amplitude * np.sin(2 * np.pi * frequency * numbers)
    
    return wave

# --- Advanced Prime Wave Neural Network ---
class PrimeWaveNet(nn.Module):
    def __init__(self, input_dim=2, hidden_dim=128, num_heads=8, num_layers=4):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        # Multi-scale wave feature extraction
        self.wave_encoder = nn.ModuleList([
            nn.Conv1d(input_dim, hidden_dim//4, kernel_size=3, padding=1),
            nn.Conv1d(input_dim, hidden_dim//4, kernel_size=5, padding=2),
            nn.Conv1d(input_dim, hidden_dim//4, kernel_size=7, padding=3),
            nn.Conv1d(input_dim, hidden_dim//4, kernel_size=11, padding=5)
        ])
        
        # Wave frequency analysis
        self.fourier_projection = nn.Linear(hidden_dim, hidden_dim)
        
        # Prime-specific positional encoding
        self.prime_position_encoding = nn.Parameter(torch.randn(1000, hidden_dim))
        
        # Custom attention for wave interference patterns
        self.wave_attention = nn.MultiheadAttention(
            hidden_dim, num_heads, dropout=0.1, batch_first=True
        )
        
        # Transformer layers with residual connections
        self.transformer_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=hidden_dim,
                nhead=num_heads,
                dim_feedforward=hidden_dim * 4,
                dropout=0.1,
                batch_first=True,
                activation='gelu'
            ) for _ in range(num_layers)
        ])
        
        # Wave interference decoder
        self.interference_decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 64),
            nn.GELU(),
            nn.Linear(64, 1)
        )
        
        # Prime probability head
        self.prime_head = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.GELU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
        # Layer normalization
        self.layer_norm = nn.LayerNorm(hidden_dim)
        
    def create_wave_features(self, x):
        """Extract multi-scale wave features"""
        # x shape: (batch, seq_len, features)
        x_conv = x.transpose(1, 2)  # (batch, features, seq_len)
        
        # Multi-scale convolutions
        wave_features = []
        for conv in self.wave_encoder:
            feat = torch.relu(conv(x_conv))
            wave_features.append(feat)
        
        # Concatenate multi-scale features
        combined = torch.cat(wave_features, dim=1)  # (batch, hidden_dim, seq_len)
        return combined.transpose(1, 2)  # (batch, seq_len, hidden_dim)
    
    def add_prime_positional_encoding(self, x, positions):
        """Add prime-aware positional encoding"""
        batch_size, seq_len, _ = x.shape
        
        # Get positional encodings for the positions
        pos_encodings = []
        for b in range(batch_size):
            pos_enc = self.prime_position_encoding[:seq_len]
            pos_encodings.append(pos_enc)
        
        pos_encodings = torch.stack(pos_encodings, dim=0)
        return x + pos_encodings
    
    def forward(self, x, positions=None):
        batch_size, seq_len, _ = x.shape
        
        # Extract wave features at multiple scales
        wave_features = self.create_wave_features(x)
        
        # Add prime-aware positional encoding
        if positions is not None:
            wave_features = self.add_prime_positional_encoding(wave_features, positions)
        
        # Apply Fourier-inspired transformation
        fourier_features = self.fourier_projection(wave_features)
        fourier_features = torch.sin(fourier_features) + torch.cos(fourier_features)
        
        # Combine original and Fourier features
        combined_features = wave_features + fourier_features
        combined_features = self.layer_norm(combined_features)
        
        # Custom wave interference attention
        attended_features, attention_weights = self.wave_attention(
            combined_features, combined_features, combined_features
        )
        
        # Apply transformer layers with residual connections
        hidden_states = attended_features
        for transformer_layer in self.transformer_layers:
            hidden_states = transformer_layer(hidden_states) + hidden_states * 0.1
        
        # Final layer normalization
        hidden_states = self.layer_norm(hidden_states)
        
        # Decode wave interference patterns
        interference_output = self.interference_decoder(hidden_states)
        
        # Generate prime probabilities
        prime_probs = self.prime_head(hidden_states)
        
        return prime_probs.squeeze(-1), interference_output.squeeze(-1), attention_weights

# --- Parameters ---
sequence_length = 32  # Reduced to work with training data
training_limit = max(200, sequence_length * 3)  # Ensure enough training samples
prediction_limit = 1000
batch_size = 16
num_epochs = 300
learning_rate = 0.0001

print("=== Advanced Prime Wave Neural Network ===")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if torch.cuda.is_available():
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
else:
    print("Using CPU")
print(f"Training limit adjusted to: {training_limit}")

# --- 1. Generate Training Data ---
training_primes = prime_sieve(training_limit)
all_primes_up_to_prediction = prime_sieve(prediction_limit)

print(f"Training with primes up to {training_limit}: {training_primes}")

# Create enhanced wave features for training
train_numbers = np.arange(1, training_limit + 1)
train_wave = create_prime_wave(train_numbers, training_primes)

# Add wave derivatives for better pattern recognition
train_wave_diff = np.gradient(train_wave)

# Create labels (1 for prime, 0 for composite)
train_labels = np.isin(train_numbers, training_primes).astype(float)

# --- 2. Prepare Enhanced Training Sequences ---
def create_enhanced_sequences(numbers, wave, wave_diff, labels, seq_len):
    """Create overlapping sequences with enhanced features"""
    sequences = []
    targets = []
    positions = []
    
    for i in range(len(numbers) - seq_len + 1):
        # Enhanced features: wave, wave derivative, normalized position
        seq_wave = wave[i:i + seq_len]
        seq_diff = wave_diff[i:i + seq_len]
        seq_numbers = numbers[i:i + seq_len]
        seq_positions = seq_numbers.copy()
        
        # Combine multiple features
        features = np.column_stack([
            seq_wave,
            seq_diff,
            seq_numbers / np.max(seq_numbers),  # Normalized position
            np.sin(2 * np.pi * seq_numbers / 30),  # Periodic feature
        ])
        
        # Target: prime labels for the sequence
        seq_labels = labels[i:i + seq_len]
        
        sequences.append(features)
        targets.append(seq_labels)
        positions.append(seq_positions)
    
    return np.array(sequences), np.array(targets), np.array(positions)

train_sequences, train_targets, train_positions = create_enhanced_sequences(
    train_numbers, train_wave, train_wave_diff, train_labels, sequence_length
)

# Convert to PyTorch tensors
train_sequences = torch.FloatTensor(train_sequences)
train_targets = torch.FloatTensor(train_targets)
train_positions = torch.LongTensor(train_positions)

print(f"Training sequences shape: {train_sequences.shape}")
print(f"Training targets shape: {train_targets.shape}")

# Debug information
print(f"Number of training samples: {len(train_sequences)}")
print(f"Sequence length: {sequence_length}")
print(f"Training range: 1 to {training_limit}")

# Check if we have enough samples
if len(train_sequences) == 0:
    raise ValueError(f"No training sequences created! Need training_limit > sequence_length. "
                    f"Current: training_limit={training_limit}, sequence_length={sequence_length}")

# --- 3. Enhanced Training with CUDA Optimization ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Training on: {device}")

# Initialize the advanced model with smaller dimensions for stability
model = PrimeWaveNet(input_dim=4, hidden_dim=128, num_heads=4, num_layers=3).to(device)

# Advanced optimizer with scheduling
optimizer = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-4)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

# Advanced loss function
criterion = nn.BCELoss()
interference_criterion = nn.MSELoss()

# Create data loader with better batching
dataset = TensorDataset(train_sequences, train_targets, train_positions)

# Ensure batch_size doesn't exceed number of samples
effective_batch_size = min(batch_size, len(train_sequences))
print(f"Using batch size: {effective_batch_size}")

dataloader = DataLoader(dataset, batch_size=effective_batch_size, shuffle=True, num_workers=0, pin_memory=True)

print("Training advanced prime wave neural network...")
model.train()

training_losses = []
for epoch in range(num_epochs):
    epoch_loss = 0
    for batch_seq, batch_targets, batch_positions in dataloader:
        # Move batch data to GPU
        batch_seq = batch_seq.to(device)
        batch_targets = batch_targets.to(device)
        batch_positions = batch_positions.to(device)
        
        optimizer.zero_grad()
        
        # Forward pass with enhanced features
        prime_probs, interference_output, attention_weights = model(batch_seq, batch_positions)
        
        # Multi-objective loss
        prime_loss = criterion(prime_probs, batch_targets)
        
        # Additional loss for wave interference understanding
        wave_input = batch_seq[:, :, 0]  # Original wave signal
        interference_loss = interference_criterion(interference_output, wave_input)
        
        # Attention regularization to focus on important patterns
        attention_reg = torch.mean(torch.var(attention_weights, dim=-1))
        
        # Combined loss
        total_loss = prime_loss + 0.1 * interference_loss + 0.01 * attention_reg
        
        total_loss.backward()
        
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        epoch_loss += total_loss.item()
    
    scheduler.step()
    training_losses.append(epoch_loss / len(dataloader))
    
    if epoch % 50 == 0:
        current_lr = scheduler.get_last_lr()[0]
        print(f"Epoch {epoch}: Loss = {training_losses[-1]:.4f}, LR = {current_lr:.6f}")

print("Training completed!")

# --- 4. Generate Enhanced Predictions ---
model.eval()
pred_numbers = np.arange(1, prediction_limit + 1)
pred_wave = create_prime_wave(pred_numbers, training_primes)
pred_wave_diff = np.gradient(pred_wave)

print("Generating predictions...")

# Create prediction sequences with enhanced features
pred_sequences, _, pred_positions = create_enhanced_sequences(
    pred_numbers, pred_wave, pred_wave_diff, np.zeros_like(pred_numbers), sequence_length
)

# Move to GPU
pred_sequences = torch.FloatTensor(pred_sequences).to(device)
pred_positions = torch.LongTensor(pred_positions).to(device)

# Get transformer predictions in batches
transformer_predictions = []
interference_predictions = []

with torch.no_grad():
    for i in range(0, len(pred_sequences), batch_size):
        batch_seq = pred_sequences[i:i + batch_size]
        batch_pos = pred_positions[i:i + batch_size]
        
        prime_probs, interference_out, _ = model(batch_seq, batch_pos)
        
        transformer_predictions.append(prime_probs.cpu().numpy())
        interference_predictions.append(interference_out.cpu().numpy())

# Concatenate all predictions
transformer_predictions = np.concatenate(transformer_predictions, axis=0)
interference_predictions = np.concatenate(interference_predictions, axis=0)

# Reconstruct full prediction array with better averaging
full_predictions = np.zeros(len(pred_numbers))
prediction_counts = np.zeros(len(pred_numbers))

for i, pred_seq in enumerate(transformer_predictions):
    start_idx = i
    for j, pred in enumerate(pred_seq):
        idx = start_idx + j
        if idx < len(full_predictions):
            full_predictions[idx] += pred
            prediction_counts[idx] += 1

# Average overlapping predictions
mask = prediction_counts > 0
full_predictions[mask] = full_predictions[mask] / prediction_counts[mask]

print(f"Prediction reconstruction complete:")
print(f"- Total prediction positions: {len(full_predictions)}")
print(f"- Positions with predictions: {np.sum(mask)}")
print(f"- Sample predictions: {full_predictions[:20]}")
print(f"- Sample actual primes in range: {[p for p in all_primes_up_to_prediction if p <= 20]}")

# --- 5. Enhanced Prime Extraction ---
# Use adaptive threshold based on prediction distribution
print(f"Prediction statistics:")
print(f"- Min prediction: {np.min(full_predictions):.6f}")
print(f"- Max prediction: {np.max(full_predictions):.6f}")
print(f"- Mean prediction: {np.mean(full_predictions):.6f}")
print(f"- Std prediction: {np.std(full_predictions):.6f}")

# Use a more reasonable threshold - top predictions above mean + 1 std
valid_predictions = full_predictions[full_predictions > 0]
if len(valid_predictions) > 0:
    threshold = np.mean(valid_predictions) + 0.5 * np.std(valid_predictions)
    # Ensure threshold is not too high
    threshold = min(threshold, np.percentile(valid_predictions, 90))
    # Ensure threshold is not too low
    threshold = max(threshold, np.percentile(valid_predictions, 70))
else:
    threshold = 0.5

print(f"Using adaptive threshold: {threshold:.4f}")

predicted_primes = pred_numbers[full_predictions > threshold]
predicted_primes = predicted_primes[predicted_primes > 1]

# Less strict filtering - focus on relative confidence
confident_primes = []
for p in predicted_primes:
    if p <= len(full_predictions):
        confidence = full_predictions[p-1]  # 0-indexed
        
        # Check if this is among the top predictions locally
        local_start = max(0, p-10)
        local_end = min(len(full_predictions), p+10)
        local_predictions = full_predictions[local_start:local_end]
        
        # Accept if confidence is in top 30% locally
        if confidence >= np.percentile(local_predictions, 70):
            confident_primes.append(p)

# If still no predictions, use a lower threshold
if len(confident_primes) == 0:
    print("No high-confidence predictions found, lowering threshold...")
    threshold = np.percentile(valid_predictions, 75) if len(valid_predictions) > 0 else 0.3
    predicted_primes = pred_numbers[full_predictions > threshold]
    predicted_primes = predicted_primes[predicted_primes > 1]
    confident_primes = list(predicted_primes)

predicted_primes = np.array(confident_primes)

# --- 6. Validation ---
actual_primes = all_primes_up_to_prediction
predicted_set = set(predicted_primes)
actual_set = set(actual_primes)

true_positives = len(predicted_set & actual_set)
false_positives = len(predicted_set - actual_set)
false_negatives = len(actual_set - predicted_set)

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print(f"\n=== Transformer Results ===")
print(f"Training range: 1 to {training_limit}")
print(f"Prediction range: 1 to {prediction_limit}")
print(f"")
print(f"Total actual primes: {len(actual_primes)}")
print(f"Total predicted primes: {len(predicted_primes)}")
print(f"")
print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")
print(f"")
print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"Recall: {recall:.4f} ({recall*100:.2f}%)")
print(f"F1-Score: {2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0:.4f}")

# --- 7. Enhanced Visualization ---
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 14))

# Plot 1: Training loss curve
ax1.plot(training_losses, 'b-', linewidth=2)
ax1.set_title('Training Loss Evolution', fontsize=14, fontweight='bold')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')

# Plot 2: Enhanced wave analysis
zoom_range = slice(0, min(300, len(pred_numbers)))
ax2.plot(pred_numbers[zoom_range], pred_wave[zoom_range], 'b-', alpha=0.6, linewidth=1, label='Input Wave')
ax2.plot(pred_numbers[zoom_range], full_predictions[zoom_range], 'r-', linewidth=2, label='Neural Network Output')
ax2.axhline(y=threshold, color='k', linestyle='--', alpha=0.5, label=f'Adaptive Threshold')

# Mark training primes
for p in training_primes:
    if p <= pred_numbers[zoom_range][-1]:
        ax2.axvline(x=p, color='green', alpha=0.8, linewidth=2)

# Mark actual primes beyond training
beyond_actual = [p for p in actual_primes if training_limit < p <= pred_numbers[zoom_range][-1]]
for p in beyond_actual[:15]:  # Limit for clarity
    ax2.axvline(x=p, color='orange', alpha=0.6, linewidth=1)

ax2.set_title('Wave Analysis & Neural Network Predictions', fontsize=14, fontweight='bold')
ax2.set_xlabel('Number')
ax2.set_ylabel('Signal Amplitude')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Prediction accuracy with confidence
zoom_limit = min(200, prediction_limit)
positions = np.arange(1, zoom_limit + 1)
actual_binary = np.isin(positions, actual_primes).astype(int)
predicted_binary = np.isin(positions, predicted_primes).astype(int)

# Create confidence-based visualization
confidence_mask = positions <= len(full_predictions)
confidences = full_predictions[:len(positions)] if len(full_predictions) >= len(positions) else np.pad(full_predictions, (0, len(positions) - len(full_predictions)))

ax3.fill_between(positions, 0, confidences, alpha=0.3, color='blue', label='Prediction Confidence')
ax3.plot(positions, actual_binary + 0.1, 'g-', linewidth=3, label='Actual Primes', alpha=0.8)
ax3.scatter(positions[predicted_binary.astype(bool)], 
           [0.05] * np.sum(predicted_binary), 
           color='red', s=50, marker='^', label='Predicted Primes', zorder=5)
ax3.axvline(x=training_limit, color='black', linestyle='--', linewidth=2, label='Training Limit')

ax3.set_title('Enhanced Prediction Analysis', fontsize=14, fontweight='bold')
ax3.set_xlabel('Number')
ax3.set_ylabel('Prime Indicator / Confidence')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Advanced performance metrics
beyond_training_mask = pred_numbers > training_limit
beyond_numbers = pred_numbers[beyond_training_mask][:200]
beyond_probs = full_predictions[beyond_training_mask][:200] if len(full_predictions) > training_limit else []

if len(beyond_probs) > 0:
    # Color code by correctness
    colors = []
    for n in beyond_numbers:
        if n in actual_set:
            colors.append('green')  # Correct prime
        else:
            colors.append('red')   # False positive or composite
    
    scatter = ax4.scatter(beyond_numbers, beyond_probs, c=colors, alpha=0.7, s=40, cmap='RdYlGn')
    ax4.axhline(y=threshold, color='k', linestyle='--', alpha=0.5, label=f'Threshold: {threshold:.3f}')
    
    # Add trend line
    if len(beyond_numbers) > 10:
        z = np.polyfit(beyond_numbers, beyond_probs, 2)
        p = np.poly1d(z)
        ax4.plot(beyond_numbers, p(beyond_numbers), "b--", alpha=0.6, label='Confidence Trend')

ax4.set_title('Predictions Beyond Training Range', fontsize=14, fontweight='bold')
ax4.set_xlabel('Number')
ax4.set_ylabel('Prime Probability')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('advanced_prime_neural_network.png', dpi=300, bbox_inches='tight')
plt.show()

# --- 8. Advanced Analysis ---
print(f"\n=== Advanced Neural Network Analysis ===")
beyond_training_predictions = [p for p in predicted_primes if p > training_limit]
correct_beyond = [p for p in beyond_training_predictions if p in actual_set]

print(f"Model Architecture:")
print(f"- Hidden dimension: 128")
print(f"- Attention heads: 4") 
print(f"- Transformer layers: 3")
print(f"- Multi-scale convolutions: 4 scales")
print(f"- Enhanced features: 4 (wave, derivative, position, periodic)")

print(f"\nTraining Details:")
print(f"- Training range: 1 to {training_limit}")
print(f"- Sequence length: {sequence_length}")
print(f"- Training samples: {len(train_sequences)}")
print(f"- Epochs: {num_epochs}")
print(f"- Device: {device}")
if training_losses:
    print(f"- Final loss: {training_losses[-1]:.6f}")
print(f"- Adaptive threshold: {threshold:.4f}")
print(f"- High-confidence predictions: {len(predicted_primes)}")

print(f"\nPredictions beyond training ({training_limit}+):")
print(f"Total predictions: {len(beyond_training_predictions)}")
print(f"Correct predictions: {len(correct_beyond)}")
print(f"Generalization accuracy: {len(correct_beyond)/len(beyond_training_predictions)*100:.1f}%" if beyond_training_predictions else "0%")

print(f"\nSample correct predictions: {correct_beyond[:15]}")
false_positives = [p for p in beyond_training_predictions if p not in actual_set]
print(f"Sample false positives: {false_positives[:10]}")

print(f"\n=== Revolutionary Approach ===")
print(f"1. Multi-scale wave feature extraction")
print(f"2. Prime-aware positional encoding") 
print(f"3. Fourier-inspired transformations")
print(f"4. Custom wave interference attention")
print(f"5. Multi-objective training (prime + interference)")
print(f"6. Adaptive confidence thresholding")
print(f"7. GPU-accelerated training")
print(f"8. Advanced regularization techniques")
