# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/01_prime_transformer_first_try.py
# Original location      :: learn/1.py   (last edited 2025-07-30)
# What this script does  :: First transformer on prime sequences (30 Jul).
# ----------------------------------------------------------------------------
import torch
import torch.nn as nn
import torch.optim as optim
import math
import random

# --- 1. Generate Primes ---
# A simple function to generate prime numbers up to a limit 'n'
def generate_primes(n):
    """Generates a list of primes up to n."""
    primes = []
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return primes

# --- 2. Prepare the Data ---
def create_sequences(primes, seq_length):
    """Create input-target pairs from the list of primes."""
    sequences = []
    for i in range(len(primes) - seq_length):
        # Input is a sequence of primes
        input_seq = primes[i:i + seq_length]
        # Target is the very next prime
        target = primes[i + seq_length]
        sequences.append((torch.tensor(input_seq, dtype=torch.float32), torch.tensor([target], dtype=torch.float32)))
    return sequences

# --- 3. Define the Transformer Model ---
# A simple model using PyTorch's built-in TransformerEncoder layer.
class PrimeTransformer(nn.Module):
    def __init__(self, input_dim=1, model_dim=32, nhead=4, num_encoder_layers=2, dim_feedforward=64, dropout=0.1):
        super(PrimeTransformer, self).__init__()
        self.model_dim = model_dim
        # Positional encoding adds information about the position of each prime in the sequence
        self.pos_encoder = nn.Parameter(torch.zeros(1, 5000, model_dim)) # Max sequence length 5000
        # A linear layer to project the input prime into the model's dimension
        self.input_projector = nn.Linear(input_dim, model_dim)
        # The transformer encoder stack
        encoder_layers = nn.TransformerEncoderLayer(d_model=model_dim, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers=num_encoder_layers)
        # A final linear layer to predict the next prime
        self.output_layer = nn.Linear(model_dim, 1)

    def forward(self, src):
        # src shape: [batch_size, seq_len]
        src = src.unsqueeze(-1) # Add feature dimension: [batch_size, seq_len, 1]
        src = self.input_projector(src) * math.sqrt(self.model_dim)
        src = src + self.pos_encoder[:, :src.size(1), :]
        output = self.transformer_encoder(src)
        # We only care about the output of the last element in the sequence
        output = self.output_layer(output[:, -1, :])
        return output

# --- 4. Main Training Script ---
if __name__ == '__main__':
    # Hyperparameters
    N_PRIMES = 10000  # Generate primes up to 10,000
    SEQ_LENGTH = 10   # Use 10 primes to predict the 11th
    LEARNING_RATE = 0.001
    EPOCHS = 50
    BATCH_SIZE = 32

    # Generate data
    print(f"Generating primes up to {N_PRIMES}...")
    primes_list = generate_primes(N_PRIMES)
    sequences = create_sequences(primes_list, SEQ_LENGTH)
    print(f"Generated {len(primes_list)} primes, creating {len(sequences)} sequences.")

    # Model, Loss, and Optimizer
    model = PrimeTransformer()
    criterion = nn.L1Loss() # Mean Absolute Error is good for this kind of regression
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # --- 5. The Training Loop ---
    print("\nStarting training... 🚀")
    for epoch in range(EPOCHS):
        model.train()
        random.shuffle(sequences) # Shuffle data each epoch
        total_loss = 0
        
        # Simple batching
        for i in range(0, len(sequences), BATCH_SIZE):
            batch = sequences[i:i+BATCH_SIZE]
            if not batch:
                continue

            inputs = torch.stack([item[0] for item in batch])
            targets = torch.stack([item[1] for item in batch])
            
            optimizer.zero_grad()
            output = model(inputs)
            loss = criterion(output, targets)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / (len(sequences) / BATCH_SIZE)
        print(f"Epoch {epoch+1}/{EPOCHS}, Average Loss: {avg_loss:.4f}")

    # --- 6. Let's Test It ---
    print("\nTraining finished. Let's see a prediction.")
    model.eval()
    with torch.no_grad():
        # Take the last 10 primes from our list before the one we want to predict
        test_sequence_input = torch.tensor(primes_list[500:500+SEQ_LENGTH], dtype=torch.float32).unsqueeze(0)
        actual_next_prime = primes_list[500+SEQ_LENGTH]
        
        predicted_next_prime = model(test_sequence_input)

        print(f"\nInput sequence: ...{test_sequence_input.numpy().flatten()[-3:]}")
        print(f"Actual next prime: {actual_next_prime}")
        print(f"Model's prediction: {predicted_next_prime.item():.2f}")