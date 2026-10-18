# Prime Hexadecimal Encoding System
# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/prime23_prime_hex_encoding.py
# Original location      :: learn/prime23.py   (last edited 2025-08-11)
# What this script does  :: Encodes primes from 11 upward as hex by last-digit pattern and checks periods.
# ----------------------------------------------------------------------------
# Starting from 11, encode primes based on last digit patterns
# Last digits 1,3,7,9 -> binary positions -> hex encoding

def is_prime(n):
    """Simple primality test"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_primes_from(start, count):
    """Get 'count' primes starting from 'start'"""
    primes = []
    n = start
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def encode_prime_to_hex(prime_group):
    """
    Encode a group of primes to hexadecimal based on last digit
    Last digit mapping: 1->bit0, 3->bit1, 7->bit2, 9->bit3
    """
    # Initialize 4-bit pattern (for digits 1,3,7,9)
    bit_pattern = 0
    
    for prime in prime_group:
        last_digit = prime % 10
        if last_digit == 1:
            bit_pattern |= 0b0001  # Set bit 0
        elif last_digit == 3:
            bit_pattern |= 0b0010  # Set bit 1
        elif last_digit == 7:
            bit_pattern |= 0b0100  # Set bit 2
        elif last_digit == 9:
            bit_pattern |= 0b1000  # Set bit 3
    
    return format(bit_pattern, 'X')  # Convert to hex

def prime_hex_encoding_system(start=11, max_n=10000):
    """
    Create hexadecimal encoding system for primes
    Groups primes and encodes based on last digit patterns
    """
    print(f"🔢 PRIME HEXADECIMAL ENCODING SYSTEM")
    print(f"=" * 60)
    print(f"Starting from: {start}")
    print(f"Encoding rule: Last digits 1,3,7,9 -> bits 0,1,2,3 -> hex")
    print()
    
    # Get all primes in range
    primes = []
    n = start
    while n <= max_n:
        if is_prime(n):
            primes.append(n)
        n += 1
    
    print(f"Found {len(primes)} primes from {start} to {max_n}")
    print()
    
    # First, let's show the initial example
    print("📍 INITIAL EXAMPLE (as described):")
    initial_primes = [11, 13, 17, 19]
    print(f"Primes: {initial_primes}")
    
    # Show bit mapping
    bit_pattern = 0
    bit_details = []
    for prime in initial_primes:
        last_digit = prime % 10
        if last_digit == 1:
            bit_pattern |= 0b0001
            bit_details.append(f"{prime} (ends in 1) -> bit 0")
        elif last_digit == 3:
            bit_pattern |= 0b0010
            bit_details.append(f"{prime} (ends in 3) -> bit 1")
        elif last_digit == 7:
            bit_pattern |= 0b0100
            bit_details.append(f"{prime} (ends in 7) -> bit 2")
        elif last_digit == 9:
            bit_pattern |= 0b1000
            bit_details.append(f"{prime} (ends in 9) -> bit 3")
    
    for detail in bit_details:
        print(f"  {detail}")
    
    print(f"Binary pattern: {format(bit_pattern, '04b')} = {bit_pattern}")
    print(f"Hexadecimal: {format(bit_pattern, 'X')}")
    print()
    
    # Now encode in groups
    print("🔤 ENCODING BY GROUPS:")
    print("Group | Primes in Group | Last Digits | Binary | Hex")
    print("-" * 55)
    
    group_size = 4  # Group primes in sets of 4
    hex_sequence = []
    
    for i in range(0, len(primes), group_size):
        group = primes[i:i+group_size]
        last_digits = [p % 10 for p in group]
        hex_code = encode_prime_to_hex(group)
        hex_sequence.append(hex_code)
        
        # Create binary representation
        bit_pattern = 0
        for prime in group:
            last_digit = prime % 10
            if last_digit == 1:
                bit_pattern |= 0b0001
            elif last_digit == 3:
                bit_pattern |= 0b0010
            elif last_digit == 7:
                bit_pattern |= 0b0100
            elif last_digit == 9:
                bit_pattern |= 0b1000
        
        binary = format(bit_pattern, '04b')
        
        print(f"{i//group_size + 1:5} | {str(group):15} | {str(last_digits):11} | {binary:6} | {hex_code}")
    
    print()
    print(f"🔤 COMPLETE HEX SEQUENCE: {''.join(hex_sequence)}")
    print()
    
    # Alternative: Encode each decade
    print("📊 ENCODING BY DECADES:")
    print("Decade | Primes | Last Digits | Binary | Hex")
    print("-" * 45)
    
    decade_hex = []
    for decade_start in range(10, max_n, 10):
        decade_end = decade_start + 9
        decade_primes = [p for p in primes if decade_start <= p <= decade_end]
        
        if decade_primes:
            last_digits = [p % 10 for p in decade_primes]
            hex_code = encode_prime_to_hex(decade_primes)
            decade_hex.append(hex_code)
            
            # Create binary for display
            bit_pattern = 0
            for prime in decade_primes:
                last_digit = prime % 10
                if last_digit == 1:
                    bit_pattern |= 0b0001
                elif last_digit == 3:
                    bit_pattern |= 0b0010
                elif last_digit == 7:
                    bit_pattern |= 0b0100
                elif last_digit == 9:
                    bit_pattern |= 0b1000
            
            binary = format(bit_pattern, '04b')
            
            print(f"{decade_start}-{decade_end:2} | {str(decade_primes):6} | {str(last_digits):11} | {binary:6} | {hex_code}")
    
    print()
    print(f"🔤 DECADE HEX SEQUENCE: {''.join(decade_hex)}")
    
    # Statistics
    print()
    print("📈 ENCODING STATISTICS:")
    last_digit_counts = {1: 0, 3: 0, 7: 0, 9: 0}
    for prime in primes:
        digit = prime % 10
        if digit in last_digit_counts:
            last_digit_counts[digit] += 1
    
    print(f"Primes ending in 1: {last_digit_counts[1]}")
    print(f"Primes ending in 3: {last_digit_counts[3]}")
    print(f"Primes ending in 7: {last_digit_counts[7]}")
    print(f"Primes ending in 9: {last_digit_counts[9]}")
    print(f"Total encoded primes: {sum(last_digit_counts.values())}")
    
    return {
        'primes': primes,
        'group_hex_sequence': ''.join(hex_sequence),
        'decade_hex_sequence': ''.join(decade_hex),
        'last_digit_distribution': last_digit_counts
    }

def analyze_hex_patterns(hex_sequence):
    """Analyze patterns in the hex sequence"""
    print(f"\n🔍 HEX PATTERN ANALYSIS:")
    print(f"Sequence: {hex_sequence}")
    print(f"Length: {len(hex_sequence)} hex digits")
    
    # Count hex digit frequencies
    hex_counts = {}
    for hex_digit in hex_sequence:
        hex_counts[hex_digit] = hex_counts.get(hex_digit, 0) + 1
    
    print("\nHex digit frequencies:")
    for digit in sorted(hex_counts.keys()):
        print(f"  {digit}: {hex_counts[digit]} times")
    
    # Look for patterns
    print(f"\nPattern analysis:")
    print(f"  Most common hex: {max(hex_counts, key=hex_counts.get)}")
    print(f"  Least common hex: {min(hex_counts, key=hex_counts.get)}")
    print(f"  Unique hex digits: {len(hex_counts)}")

# Run the encoding system
if __name__ == "__main__":
    # Extended version up to 10,000
    print("🚀 PRIME HEX ENCODING UP TO 10,000:")
    result_10000 = prime_hex_encoding_system(start=11, max_n=11010)
    
    print("\n" + "="*80)
    print("🔍 DETAILED PATTERN ANALYSIS:")
    analyze_hex_patterns(result_10000['decade_hex_sequence'])
    
    # Additional advanced pattern analysis
    hex_seq = result_10000['decade_hex_sequence']
    print(f"\n📊 ADVANCED PATTERN DETECTION:")
    print(f"Full sequence: {hex_seq}")
    print(f"Sequence length: {len(hex_seq)} hex digits")
    
    # Look for repeating patterns
    print(f"\n🔄 REPEATING PATTERN ANALYSIS:")
    
    # Check for 2-character patterns
    pairs = {}
    for i in range(len(hex_seq) - 1):
        pair = hex_seq[i:i+2]
        pairs[pair] = pairs.get(pair, 0) + 1
    
    print("Most common 2-character patterns:")
    sorted_pairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)
    for pair, count in sorted_pairs[:10]:
        if count > 1:
            print(f"  '{pair}': {count} times")
    
    # Check for 3-character patterns
    triplets = {}
    for i in range(len(hex_seq) - 2):
        triplet = hex_seq[i:i+3]
        triplets[triplet] = triplets.get(triplet, 0) + 1
    
    print("\nMost common 3-character patterns:")
    sorted_triplets = sorted(triplets.items(), key=lambda x: x[1], reverse=True)
    for triplet, count in sorted_triplets[:5]:
        if count > 1:
            print(f"  '{triplet}': {count} times")
    
    # Analyze hex digit distribution
    print(f"\n� HEX DIGIT DISTRIBUTION ANALYSIS:")
    total_digits = len(hex_seq)
    hex_counts = {}
    for digit in hex_seq:
        hex_counts[digit] = hex_counts.get(digit, 0) + 1
    
    print("Hex digit frequencies and percentages:")
    for digit in sorted(hex_counts.keys()):
        count = hex_counts[digit]
        percentage = (count / total_digits) * 100
        print(f"  {digit}: {count:3} times ({percentage:5.1f}%)")
    
    # Look for mathematical patterns
    print(f"\n🔢 MATHEMATICAL PATTERN ANALYSIS:")
    
    # Convert hex to decimal values
    decimal_values = [int(c, 16) for c in hex_seq]
    print(f"Decimal sequence: {decimal_values[:20]}...")  # Show first 20
    
    # Statistical analysis
    import statistics
    mean_val = statistics.mean(decimal_values)
    median_val = statistics.median(decimal_values)
    
    print(f"Statistical properties:")
    print(f"  Mean hex value: {mean_val:.2f}")
    print(f"  Median hex value: {median_val}")
    print(f"  Min hex value: {min(decimal_values)}")
    print(f"  Max hex value: {max(decimal_values)}")
    
    # Look for periodicity
    print(f"\n🌊 PERIODICITY ANALYSIS:")
    
    # Check for periods of different lengths
    def check_period(seq, period_len):
        if len(seq) < 2 * period_len:
            return False
        
        matches = 0
        total_checks = len(seq) - period_len
        
        for i in range(total_checks):
            if seq[i] == seq[i + period_len]:
                matches += 1
        
        return matches / total_checks if total_checks > 0 else 0
    
    print("Checking for periodic patterns:")
    for period in range(2, min(20, len(hex_seq)//2)):
        match_ratio = check_period(hex_seq, period)
        if match_ratio > 0.3:  # Show periods with >30% match
            print(f"  Period {period}: {match_ratio:.1%} matches")
    
    # Entropy analysis
    print(f"\n🎲 RANDOMNESS ANALYSIS:")
    
    # Calculate entropy
    import math
    entropy = 0
    for count in hex_counts.values():
        if count > 0:
            p = count / total_digits
            entropy -= p * math.log2(p)
    
    max_entropy = math.log2(16)  # Maximum entropy for hex digits
    entropy_ratio = entropy / max_entropy
    
    print(f"Entropy: {entropy:.3f} bits (max: {max_entropy:.3f})")
    print(f"Entropy ratio: {entropy_ratio:.3f} (1.0 = perfectly random)")
    
    if entropy_ratio > 0.9:
        print("  → High entropy: sequence appears quite random")
    elif entropy_ratio > 0.7:
        print("  → Medium entropy: some patterns present")
    else:
        print("  → Low entropy: strong patterns detected")
    
    print(f"\n🎯 SUMMARY:")
    print(f"  Total primes encoded: {len(result_10000['primes'])}")
    print(f"  Hex sequence length: {len(hex_seq)}")
    print(f"  Most frequent hex digit: {max(hex_counts, key=hex_counts.get)}")
    print(f"  Entropy ratio: {entropy_ratio:.3f}")
    print(f"  Unique hex digits used: {len(hex_counts)}/16")
