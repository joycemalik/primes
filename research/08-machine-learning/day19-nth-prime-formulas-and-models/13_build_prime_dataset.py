# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/13_build_prime_dataset.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/13.py   (last edited 2025-08-27)
# What this script does  :: Builds prime_dataset/ train, validation and test CSVs.
# ----------------------------------------------------------------------------
import math
import random
import os

def is_prime(num):
    """Check if a number is prime"""
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    
    # Check for factors up to sqrt(num)
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    """Generate all prime numbers up to n"""
    primes = []
    for num in range(2, n + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def create_dataset(primes, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """Create train, validation, and test datasets"""
    # Create input (n) and output (nth prime) pairs
    data = []
    for i, prime in enumerate(primes, 1):
        data.append((i, prime))
    
    # Shuffle the data
    random.shuffle(data)
    
    # Split the data
    total = len(data)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_data = data[:train_end]
    val_data = data[train_end:val_end]
    test_data = data[val_end:]
    
    return train_data, val_data, test_data

def save_data(data, filename):
    """Save data to CSV file"""
    with open(filename, 'w') as f:
        f.write("input,output\n")
        for input_val, output_val in data:
            f.write(f"{input_val},{output_val}\n")

def main():
    # Get user input
    try:
        n = int(input("Enter the maximum number (n) to generate primes up to: "))
        if n < 2:
            print("Please enter a number greater than 1")
            return
    except ValueError:
        print("Please enter a valid integer")
        return
    
    # Generate primes
    primes = generate_primes(n)
    print(f"Generated {len(primes)} prime numbers up to {n}")
    print(f"First 10 primes: {primes[:10]}")
    print(f"Last 10 primes: {primes[-10:]}")
    
    # Create datasets
    train_data, val_data, test_data = create_dataset(primes)
    
    # Create directory for output files
    os.makedirs("prime_dataset", exist_ok=True)
    
    # Save datasets
    save_data(train_data, "prime_dataset/train.csv")
    save_data(val_data, "prime_dataset/validation.csv")
    save_data(test_data, "prime_dataset/test.csv")
    
    # Save complete dataset for reference
    complete_data = [(i+1, prime) for i, prime in enumerate(primes)]
    save_data(complete_data, "prime_dataset/complete_dataset.csv")
    
    # Save just the primes list
    with open("prime_dataset/primes_list.txt", 'w') as f:
        f.write(",".join(map(str, primes)))
    
    print(f"\nFiles created in 'prime_dataset' directory:")
    print(f"- train.csv: {len(train_data)} samples")
    print(f"- validation.csv: {len(val_data)} samples")
    print(f"- test.csv: {len(test_data)} samples")
    print(f"- complete_dataset.csv: All {len(primes)} prime numbers")
    print(f"- primes_list.txt: Comma-separated list of primes")

if __name__ == "__main__":
    main()