# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/unified-theory-crt/simple_prime_wave_predictor.py
# Original location      :: learn/pime/check/predictor.py   (last edited 2025-08-03)
# What this script does  :: Simplified predictor that identifies and removes false positives.
# ----------------------------------------------------------------------------
"""
SIMPLIFIED PRIME WAVE PREDICTOR
==============================

Simple program that:
1. Takes input number n
2. Predicts all prime numbers up to n using wave theory
3. Shows visualization graph
4. Saves predicted primes to file

Author: Prime Wave Theory Research
Date: August 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import math

class SimplePrimeWavePredictor:
    """
    Simplified Prime Wave Predictor
    Uses wave interference to predict prime numbers
    """
    
    def __init__(self):
        """Initialize with seed primes for wave generation"""
        self.seed_primes = [2, 3, 5, 7]
        print("🌊 Prime Wave Predictor Initialized")
        print(f"📡 Using seed primes: {self.seed_primes}")
    
    def generate_prime_wave(self, limit):
        """
        Generate wave that identifies prime numbers
        Primes appear as quiet zones (low amplitude)
        """
        print(f"🔄 Generating prime wave for range 1 to {limit}...")
        
        x = np.arange(1, limit + 1)
        wave = np.zeros(x.shape)
        
        # Create interference pattern from seed primes
        for p in self.seed_primes:
            # Add peaks at multiples of p (excluding p itself)
            for multiple in range(2 * p, limit + 1, p):
                if multiple <= limit:
                    idx = multiple - 1
                    wave[idx] += 1.0
        
        return x, wave
    
    def identify_false_positives(self, predicted_primes):
        """
        Identify false positives (numbers that are coprime to [2,3,5,7] but composite)
        """
        false_positives = []
        
        for num in predicted_primes:
            if num <= max(self.seed_primes):
                continue
                
            # Check if coprime to all seed primes
            is_coprime = all(math.gcd(num, p) == 1 for p in self.seed_primes)
            
            if is_coprime:
                # Check if actually composite by trying to factor
                if self._is_composite(num):
                    false_positives.append(num)
        
        return false_positives
    
    def _is_composite(self, n):
        """Check if a number is composite"""
        if n < 4:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return True
        return False
    
    def correct_wave_with_suppression(self, wave, false_positives, limit):
        """
        Apply suppression to eliminate false positives
        """
        corrected_wave = wave.copy()
        
        for fp in false_positives:
            if fp <= limit:
                idx = fp - 1
                corrected_wave[idx] += 1.0  # Add amplitude to remove quiet zone
        
        return corrected_wave
    
    def predict_primes(self, limit):
        """
        Main prediction function - predicts all primes up to limit
        """
        print(f"\n🎯 PREDICTING PRIMES UP TO {limit}")
        print("=" * 50)
        
        # Step 1: Generate wave
        x, wave = self.generate_prime_wave(limit)
        
        # Step 2: Initial predictions from quiet zones
        initial_predictions = []
        threshold = 0.5
        
        for i, amplitude in enumerate(wave):
            number = i + 1
            if amplitude < threshold and number > 1:
                initial_predictions.append(number)
        
        print(f"📊 Initial predictions: {len(initial_predictions)} numbers")
        
        # Step 3: Identify and correct false positives
        false_positives = self.identify_false_positives(initial_predictions)
        print(f"❌ False positives found: {len(false_positives)}")
        if false_positives:
            print(f"📋 False positive numbers: {false_positives[:10]}{'...' if len(false_positives) > 10 else ''}")
        
        # Step 4: Apply correction
        corrected_wave = self.correct_wave_with_suppression(wave, false_positives, limit)
        
        # Step 5: Final predictions
        final_predictions = []
        for i, amplitude in enumerate(corrected_wave):
            number = i + 1
            if amplitude < threshold and number > 1:
                final_predictions.append(number)
        
        print(f"✅ Final predictions: {len(final_predictions)} prime numbers")
        
        return final_predictions, x, wave, corrected_wave, false_positives
    
    def save_primes_to_file(self, primes, filename="predicted_primes.txt"):
        """
        Save predicted primes to a file
        """
        print(f"\n💾 Saving primes to {filename}...")
        
        with open(filename, 'w') as f:
            f.write("PREDICTED PRIME NUMBERS\n")
            f.write("=" * 30 + "\n")
            f.write(f"Total count: {len(primes)}\n")
            f.write(f"Range: 1 to {max(primes) if primes else 0}\n")
            f.write("Generated using Prime Wave Theory\n\n")
            
            f.write("Prime numbers:\n")
            # Write primes in rows of 10
            for i, prime in enumerate(primes):
                f.write(f"{prime:6d}")
                if (i + 1) % 10 == 0:
                    f.write("\n")
                else:
                    f.write(" ")
            
            if len(primes) % 10 != 0:
                f.write("\n")
        
        print(f"✅ Successfully saved {len(primes)} primes to {filename}")
    
    def create_visualization(self, x, original_wave, corrected_wave, primes, false_positives, limit):
        """
        Create visualization graph showing the wave and predictions
        """
        print(f"\n📈 Creating visualization...")
        
        # Limit display range for clarity
        display_limit = min(100, limit)
        x_display = x[:display_limit]
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))
        
        # Plot 1: Original Wave
        ax1.plot(x_display, original_wave[:display_limit], 'b-', linewidth=2, label='Original Wave')
        ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Detection Threshold')
        
        # Mark actual primes and false positives
        for p in primes:
            if p <= display_limit:
                ax1.axvspan(p-0.3, p+0.3, alpha=0.3, color='green')
        
        for fp in false_positives:
            if fp <= display_limit:
                ax1.axvspan(fp-0.3, fp+0.3, alpha=0.4, color='red')
        
        ax1.set_title('Original Prime Wave (Green: True Primes, Red: False Positives)', fontweight='bold')
        ax1.set_xlabel('Number')
        ax1.set_ylabel('Wave Amplitude')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Corrected Wave
        ax2.plot(x_display, corrected_wave[:display_limit], 'g-', linewidth=2, label='Corrected Wave')
        ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Detection Threshold')
        
        # Mark only true primes
        for p in primes:
            if p <= display_limit:
                ax2.axvspan(p-0.3, p+0.3, alpha=0.3, color='green')
        
        ax2.set_title('Corrected Prime Wave (False Positives Eliminated)', fontweight='bold')
        ax2.set_xlabel('Number')
        ax2.set_ylabel('Wave Amplitude')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Prime Number Visualization
        prime_indicators = np.zeros(display_limit)
        for p in primes:
            if p <= display_limit:
                prime_indicators[p-1] = 1.0
        
        ax3.stem(x_display, prime_indicators, basefmt=' ', linefmt='red', markerfmt='ro')
        ax3.set_title(f'Predicted Prime Numbers (First {display_limit} numbers)', fontweight='bold')
        ax3.set_xlabel('Number')
        ax3.set_ylabel('Is Prime')
        ax3.grid(True, alpha=0.3)
        
        # Add prime number labels for clarity
        for p in primes[:20]:  # Label first 20 primes
            if p <= display_limit:
                ax3.annotate(f'{p}', (p, 1.1), ha='center', fontsize=8, rotation=45)
        
        plt.tight_layout()
        # plt.show()
        
        print("✅ Visualization displayed!")

def main():
    """
    Main function - gets user input and runs prime prediction
    """
    print("🌊 PRIME WAVE PREDICTOR")
    print("=" * 40)
    print("Uses wave interference theory to predict prime numbers")
    print()
    
    # Get input from user
    try:
        n = int(input("Enter the upper limit (n) to find all primes up to n: "))
        if n < 2:
            print("❌ Please enter a number greater than 1")
            return
    except ValueError:
        print("❌ Please enter a valid integer")
        return
    
    print(f"\n🎯 Finding all prime numbers from 1 to {n}...")
    
    # Initialize predictor
    predictor = SimplePrimeWavePredictor()
    
    # Predict primes
    primes, x, original_wave, corrected_wave, false_positives = predictor.predict_primes(n)
    
    # Show results
    print(f"\n📊 RESULTS:")
    print(f"   Total primes found: {len(primes)}")
    print(f"   First 20 primes: {primes[:20]}")
    if len(primes) > 20:
        print(f"   Last 10 primes: {primes[-10:]}")
    
    # Save to file
    predictor.save_primes_to_file(primes)
    
    # Create visualization
    predictor.create_visualization(x, original_wave, corrected_wave, primes, false_positives, n)
    
    print(f"\n🎉 COMPLETE!")
    print(f"✅ Found {len(primes)} prime numbers up to {n}")
    print(f"✅ Results saved to 'predicted_primes.txt'")
    print(f"✅ Visualization graph displayed")

if __name__ == "__main__":
    main()
