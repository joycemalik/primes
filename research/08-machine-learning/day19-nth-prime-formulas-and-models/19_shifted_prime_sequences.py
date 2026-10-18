# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day19-nth-prime-formulas-and-models/19_shifted_prime_sequences.py
# Original location      :: research/08-machine-learning/day19-nth-prime-formulas-and-models/19.py   (last edited 2025-08-27)
# What this script does  :: Sequences of primes shifted by +m (prime_sequences/).
# ----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import os

def is_prime(num):
    """Check if a number is prime"""
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    """Generate first n prime numbers"""
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def generate_prime_sequences(primes, m):
    """Generate sequences by moving each prime by m units until no more primes"""
    sequences = []
    last_numbers = []
    
    for prime in primes:
        sequence = [prime]
        current = prime
        
        while True:
            current += m
            if is_prime(current):
                sequence.append(current)
            else:
                break
        
        sequences.append(sequence)
        last_numbers.append(sequence[-1])
    
    return sequences, last_numbers

def save_sequences(sequences, last_numbers, filename):
    """Save sequences and last numbers to file"""
    with open(filename, 'w') as f:
        f.write("Prime Sequences (each prime moved by +m until no more primes):\n")
        f.write("=" * 60 + "\n\n")
        
        for i, seq in enumerate(sequences):
            f.write(f"Prime {i+1}: {seq[0]} -> ")
            f.write(" -> ".join(map(str, seq[1:])))
            f.write(f" (Last: {last_numbers[i]})\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Last numbers: {last_numbers}\n")
        f.write(f"Max last number: {max(last_numbers)}\n")
        f.write(f"Min last number: {min(last_numbers)}\n")
        f.write(f"Average last number: {sum(last_numbers)/len(last_numbers):.2f}\n")

def plot_sequences(sequences, last_numbers, n, m):
    # """Create visualization of the sequences"""
    # plt.figure(figsize=(12, 8))
    
    # # Plot each sequence
    # for i, seq in enumerate(sequences):
    #     x = list(range(len(seq)))
    #     plt.plot(x, seq, 'o-', label=f'Prime {i+1}: {seq[0]}', alpha=0.7, linewidth=2)
    
    # # Highlight last numbers
    # x_last = [len(seq)-1 for seq in sequences]
    # plt.scatter(x_last, last_numbers, color='red', s=100, zorder=5, 
    #             label='Last numbers', edgecolors='black')
    
    # plt.xlabel('Step Number')
    # plt.ylabel('Number Value')
    # plt.title(f'Prime Sequences (n={n}, m={m})\nEach prime moved by +{m} until no more primes')
    # plt.grid(True, alpha=0.3)
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.tight_layout()
    
    # # Save plot
    # plt.savefig(f'prime_sequences_n{n}_m{m}.png', dpi=300, bbox_inches='tight')
    # plt.show()
    print("last numbers:", last_numbers[1])

def main():
    # Get user input
    try:
        n = int(input("Enter the number of primes to generate (n): "))
        m = int(input("Enter the step size (m): "))
        
        if n <= 0 or m <= 0:
            print("Please enter positive integers for n and m")
            return
            
    except ValueError:
        print("Please enter valid integers")
        return
    
    # Generate primes
    primes = generate_primes(n)
    print(f"\nGenerated first {n} primes: {primes}")
    
    # Generate sequences
    sequences, last_numbers = generate_prime_sequences(primes, m)
    
    # Display results
    print(f"\nSequences (each prime moved by +{m} until no more primes):")
    print("=" * 50)
    # for i, seq in enumerate(sequences):
    #     print(f"Prime {i+1}: {seq[0]} -> {' -> '.join(map(str, seq[1:]))} (Last: {last_numbers[i]})")
    
    # print(f"\nLast numbers: {last_numbers}")
    
    # Create output directory
    os.makedirs("prime_sequences", exist_ok=True)
    
    # Save to file
    filename = f"prime_sequences/sequences_n{n}_m{m}.txt"
    save_sequences(sequences, last_numbers, filename)
    
    # Create visualization
    # plot_sequences(sequences, last_numbers, n, m)
    
    print(f"\nResults saved to: {filename}")
    print(f"Plot saved as: prime_sequences_n{n}_m{m}.png")
    
    # Additional analysis
    print(f"\nAnalysis:")
    print(f"Total sequences: {len(sequences)}")
    print(f"Max sequence length: {max(len(seq) for seq in sequences)}")
    print(f"Min sequence length: {min(len(seq) for seq in sequences)}")
    print(f"Average sequence length: {sum(len(seq) for seq in sequences)/len(sequences):.2f}")

if __name__ == "__main__":
    main()