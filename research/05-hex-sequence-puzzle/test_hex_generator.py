#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/test_hex_generator.py
# Original location      :: learn/test_hex_generator.py   (last edited 2025-08-08)
# What this script does  :: Compares an external hex generator (Downloads/hex_sequence_generator.py) with the string.
# ----------------------------------------------------------------------------
"""
Test script to compare hex sequence generator output with actual prime hex sequence
"""

import sys
import os
sys.path.append(r'C:\Users\joyce\Downloads')
from hex_sequence_generator import generate

# Our known prime hex sequence (first part)
PRIME_HEX_SEQUENCE = "FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A162984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51AA9F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A424984847"

def test_exact_reproduction():
    """Test if generator exactly reproduces training data"""
    print("🔬 TEST 1: Exact Reproduction")
    print("=" * 50)
    
    training_lengths = [50, 100, 200, 300]
    
    for length in training_lengths:
        if length <= len(PRIME_HEX_SEQUENCE):
            training = PRIME_HEX_SEQUENCE[:length]
            generated = generate(training, length, order=3)
            
            match = training == generated
            print(f"Length {length}: {'✅ MATCH' if match else '❌ NO MATCH'}")
            
            if not match:
                print(f"  Expected: {training[:20]}...")
                print(f"  Got:      {generated[:20]}...")
                # Find first difference
                for i, (a, b) in enumerate(zip(training, generated)):
                    if a != b:
                        print(f"  First diff at position {i}: '{a}' vs '{b}'")
                        break
    print()

def test_extrapolation_consistency():
    """Test if extrapolation is consistent with different training lengths"""
    print("🔬 TEST 2: Extrapolation Consistency")
    print("=" * 50)
    
    target_length = 400
    training_lengths = [100, 150, 200, 250]
    
    results = {}
    
    for train_len in training_lengths:
        if train_len <= len(PRIME_HEX_SEQUENCE):
            training = PRIME_HEX_SEQUENCE[:train_len]
            generated = generate(training, target_length, order=3)
            results[train_len] = generated
            print(f"Training length {train_len}: Generated {len(generated)} chars")
    
    # Compare extrapolated portions
    print("\n🔍 Comparing extrapolated portions:")
    base_result = results[min(training_lengths)]
    
    for train_len in training_lengths[1:]:
        if train_len in results:
            current = results[train_len]
            # Compare the overlapping extrapolated part
            min_len = min(len(base_result), len(current))
            
            differences = 0
            for i in range(min_len):
                if base_result[i] != current[i]:
                    differences += 1
            
            match_rate = (min_len - differences) / min_len * 100
            print(f"  vs training {train_len}: {match_rate:.1f}% match")
            
            if differences > 0:
                print(f"    First 20 chars: {current[:20]}")
    print()

def test_pattern_learning():
    """Test if generator learns meaningful patterns"""
    print("🔬 TEST 3: Pattern Learning Analysis")
    print("=" * 50)
    
    training = PRIME_HEX_SEQUENCE[:200]
    
    # Generate longer sequences
    for target_len in [300, 400, 500]:
        generated = generate(training, target_len, order=3)
        extrapolated = generated[200:]  # Just the new part
        
        print(f"Target length {target_len}:")
        print(f"  Extrapolated: {extrapolated[:50]}...")
        
        # Analyze hex digit frequency in extrapolated part
        hex_counts = {}
        for char in extrapolated:
            hex_counts[char] = hex_counts.get(char, 0) + 1
        
        print(f"  Top 3 hex digits: {sorted(hex_counts.items(), key=lambda x: x[1], reverse=True)[:3]}")
    print()

def test_prime_sequence_prediction():
    """Test how well generator predicts the actual prime sequence"""
    print("🔬 TEST 4: Prime Sequence Prediction")
    print("=" * 50)
    
    # Use first 300 chars to predict next 100
    if len(PRIME_HEX_SEQUENCE) >= 400:
        training = PRIME_HEX_SEQUENCE[:300]
        actual_next = PRIME_HEX_SEQUENCE[300:400]
        
        generated = generate(training, 400, order=3)
        predicted_next = generated[300:400]
        
        print(f"Training length: 300")
        print(f"Predicting next: 100 chars")
        print(f"Actual  : {actual_next[:30]}...")
        print(f"Predicted: {predicted_next[:30]}...")
        
        # Calculate accuracy
        matches = sum(1 for a, p in zip(actual_next, predicted_next) if a == p)
        accuracy = matches / len(actual_next) * 100
        
        print(f"Accuracy: {matches}/{len(actual_next)} = {accuracy:.1f}%")
        
        # Show character-by-character comparison
        print("\nFirst 20 char comparison:")
        for i in range(min(20, len(actual_next))):
            status = "✅" if actual_next[i] == predicted_next[i] else "❌"
            print(f"  {i:2d}: {actual_next[i]} vs {predicted_next[i]} {status}")
    print()

def main():
    print("🧪 HEX SEQUENCE GENERATOR vs PRIME SEQUENCE ANALYSIS")
    print("=" * 60)
    print(f"Prime sequence length: {len(PRIME_HEX_SEQUENCE)}")
    print(f"First 50 chars: {PRIME_HEX_SEQUENCE[:50]}")
    print()
    
    test_exact_reproduction()
    test_extrapolation_consistency()
    test_pattern_learning()
    test_prime_sequence_prediction()
    
    print("🏁 Analysis Complete!")

if __name__ == "__main__":
    main()
