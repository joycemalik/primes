"""
Enhanced Prime Wave Function with False Positive Cancellation
============================================================

Discovering the complementary wave that cancels false positives through destructive interference.
"""

import numpy as np
import math
from typing import List, Set

def prime_sieve(n):
    """Generates primes up to n using the Sieve of Eratosthenes."""
    primes = np.ones(n + 1, dtype=bool)
    primes[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if primes[i]:
            primes[i*i:n+1:i] = False
    return np.where(primes)[0]

def prime_wave_function(n, context_primes):
    """The fundamental prime wave function."""
    amplitude = 0.0
    for p in context_primes:
        if n % p == 0:
            amplitude += 1.0 / np.sqrt(p)
    return amplitude

def analyze_false_positives(context_primes, test_range=10000):
    """Analyze the pattern of false positives to design a cancellation wave."""
    
    print(f"🔍 Analyzing False Positive Patterns up to {test_range}")
    print(f"Context primes: {list(context_primes)}")
    
    # Get actual primes
    actual_primes = set(prime_sieve(test_range))
    
    # Find numbers with W(n) = 0 (predicted primes from wave)
    zero_amplitude_numbers = []
    for n in range(2, test_range + 1):
        if prime_wave_function(n, context_primes) == 0:
            zero_amplitude_numbers.append(n)
    
    # Add context primes
    predicted_primes = set(zero_amplitude_numbers + list(context_primes))
    
    # Find false positives
    false_positives = predicted_primes - actual_primes
    true_primes = predicted_primes & actual_primes
    
    print(f"Zero amplitude numbers: {len(zero_amplitude_numbers)}")
    print(f"Total predicted primes: {len(predicted_primes)}")
    print(f"True primes: {len(true_primes)}")
    print(f"False positives: {len(false_positives)}")
    
    # Analyze false positive patterns
    false_pos_list = sorted(list(false_positives))
    print(f"First 20 false positives: {false_pos_list[:20]}")
    
    # Factor analysis of false positives
    print(f"\n🧮 Factorization Analysis of False Positives:")
    factor_patterns = {}
    
    for fp in false_pos_list[:50]:  # Analyze first 50
        factors = []
        temp = fp
        
        # Find prime factors
        for p in range(2, int(math.sqrt(fp)) + 1):
            while temp % p == 0:
                factors.append(p)
                temp //= p
        if temp > 1:
            factors.append(temp)
        
        if len(factors) >= 2:
            # Look for patterns in factor combinations
            min_factor = min(factors)
            max_factor = max(factors)
            
            pattern_key = f"min:{min_factor}, max:{max_factor}, len:{len(factors)}"
            if pattern_key not in factor_patterns:
                factor_patterns[pattern_key] = []
            factor_patterns[pattern_key].append((fp, factors))
    
    print(f"Factor patterns found:")
    for pattern, examples in factor_patterns.items():
        print(f"  {pattern}: {len(examples)} numbers")
        if len(examples) <= 5:
            for num, factors in examples:
                print(f"    {num} = {' × '.join(map(str, factors))}")
    
    # Find the range of primes that appear in false positives
    all_factors = set()
    for fp in false_pos_list[:100]:
        temp = fp
        for p in range(2, int(math.sqrt(fp)) + 1):
            while temp % p == 0:
                all_factors.add(p)
                temp //= p
        if temp > 1:
            all_factors.add(temp)
    
    # Factors beyond our context window
    beyond_context = sorted([f for f in all_factors if f not in context_primes])
    print(f"\n🎯 Prime factors in false positives beyond context window:")
    print(f"Beyond context primes: {beyond_context[:20]}...")
    
    return false_positives, beyond_context

def create_cancellation_wave(context_primes, beyond_context_primes, extended_limit=100):
    """Create a complementary wave function to cancel false positives."""
    
    print(f"\n🌊 Creating Cancellation Wave Function")
    
    # Use primes beyond context window to create cancellation pattern
    cancellation_primes = beyond_context_primes[:extended_limit]  # Use limited set
    
    print(f"Cancellation context: {len(cancellation_primes)} primes")
    print(f"Cancellation primes: {cancellation_primes[:10]}...")
    
    def enhanced_prime_detector(n):
        """Enhanced detector with cancellation wave."""
        
        # Original wave function
        primary_amplitude = prime_wave_function(n, context_primes)
        
        # If primary wave says composite, it's definitely composite
        if primary_amplitude > 0:
            return False
        
        # If it's a context prime, it's definitely prime
        if n in context_primes:
            return True
        
        # For zero-amplitude numbers, check cancellation wave
        # If n has factors from cancellation primes, it's composite
        for p in cancellation_primes:
            if n % p == 0:
                return False  # Cancelled out - it's composite
        
        # Survived both waves - likely prime
        return True
    
    return enhanced_prime_detector, cancellation_primes

def test_enhanced_detector():
    """Test the enhanced prime detector with cancellation wave."""
    
    print(f"\n" + "="*80)
    print(f"🧪 TESTING ENHANCED PRIME WAVE DETECTOR 🧪")
    print(f"="*80)
    
    # Setup
    context_limit = 50
    test_range = 100000
    
    context_primes = prime_sieve(context_limit)
    
    # Analyze false positives
    false_positives, beyond_context = analyze_false_positives(context_primes, test_range//10)
    
    # Create enhanced detector
    enhanced_detector, cancellation_primes = create_cancellation_wave(
        context_primes, beyond_context, extended_limit=50
    )
    
    # Test enhanced detector
    print(f"\n🎯 Testing Enhanced Detector on range 1-{test_range}")
    
    actual_primes = set(prime_sieve(test_range))
    predicted_primes = set()
    
    for n in range(2, test_range + 1):
        if enhanced_detector(n):
            predicted_primes.add(n)
    
    # Calculate metrics
    true_positives = len(predicted_primes & actual_primes)
    false_positives_new = len(predicted_primes - actual_primes)
    false_negatives = len(actual_primes - predicted_primes)
    
    precision = true_positives / (true_positives + false_positives_new) if (true_positives + false_positives_new) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\n📊 ENHANCED DETECTOR RESULTS:")
    print(f"Context primes: {list(context_primes)}")
    print(f"Cancellation primes: {cancellation_primes[:10]}...")
    print(f"Range: 1 to {test_range}")
    print(f"")
    print(f"Total actual primes: {len(actual_primes)}")
    print(f"Total predicted primes: {len(predicted_primes)}")
    print(f"True Positives: {true_positives}")
    print(f"False Positives: {false_positives_new}")
    print(f"False Negatives: {false_negatives}")
    print(f"")
    print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"Recall: {recall:.4f} ({recall*100:.2f}%)")
    print(f"F1-Score: {f1_score:.4f}")
    
    if false_positives_new > 0:
        remaining_fps = sorted(list(predicted_primes - actual_primes))[:10]
        print(f"Remaining false positives: {remaining_fps}")
    
    return precision, recall, f1_score

if __name__ == "__main__":
    test_enhanced_detector()
