# ----------------------------------------------------------------------------
# Prime research archive :: research/01-prime-wave-sieve/unified-theory-crt/accuracy_checker.py
# Original location      :: learn/pime/check/accuracy_checker.py   (last edited 2025-08-03)
# What this script does  :: Scores predicted_primes.txt against a sieve (writes accuracy_report.txt).
# ----------------------------------------------------------------------------
"""
PRIME ACCURACY CHECKER
======================

Validates the accuracy of predicted primes from the Prime Wave Theory
by comparing against ground truth (Sieve of Eratosthenes).

Calculates:
- True Positives (TP): Correctly predicted primes
- False Positives (FP): Non-primes predicted as primes  
- False Negatives (FN): Primes missed by prediction
- True Negatives (TN): Non-primes correctly not predicted

Metrics:
- Precision: TP / (TP + FP)
- Recall: TP / (TP + FN)  
- F1-Score: 2 * (Precision * Recall) / (Precision + Recall)
- Accuracy: (TP + TN) / (TP + TN + FP + FN)

Author: Prime Wave Theory Research
Date: August 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import time

class PrimeAccuracyChecker:
    """
    Comprehensive accuracy checker for prime predictions
    """
    
    def __init__(self):
        """Initialize the accuracy checker"""
        print("🔍 Prime Accuracy Checker Initialized")
        self.predicted_primes = []
        self.true_primes = []
        self.range_limit = 0
        
    def load_predicted_primes(self, filename="predicted_primes.txt"):
        """
        Load predicted primes from file
        """
        print(f"📁 Loading predicted primes from {filename}...")
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            # Parse the file to extract primes
            primes = []
            parsing_primes = False
            
            for line in lines:
                line = line.strip()
                
                # Extract range information
                if line.startswith("Range: 1 to"):
                    range_str = line.split("Range: 1 to ")[1]
                    self.range_limit = int(range_str)
                    print(f"📊 Detected range: 1 to {self.range_limit}")
                
                # Start parsing primes after "Prime numbers:" line
                if line == "Prime numbers:":
                    parsing_primes = True
                    continue
                
                if parsing_primes and line:
                    # Parse numbers from the line
                    numbers = line.split()
                    for num_str in numbers:
                        try:
                            num = int(num_str)
                            primes.append(num)
                        except ValueError:
                            continue
            
            self.predicted_primes = sorted(primes)
            print(f"✅ Loaded {len(self.predicted_primes)} predicted primes")
            print(f"📈 Range: {min(self.predicted_primes)} to {max(self.predicted_primes)}")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: File {filename} not found!")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def generate_true_primes_sieve(self, limit):
        """
        Generate true primes using Sieve of Eratosthenes (ground truth)
        """
        print(f"🎯 Generating true primes up to {limit} using Sieve of Eratosthenes...")
        
        start_time = time.time()
        
        # Sieve of Eratosthenes
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, limit + 1, i):
                    sieve[j] = False
        
        # Extract primes
        self.true_primes = [i for i in range(2, limit + 1) if sieve[i]]
        
        end_time = time.time()
        print(f"✅ Generated {len(self.true_primes)} true primes in {end_time - start_time:.4f} seconds")
        
        return self.true_primes
    
    def calculate_confusion_matrix(self):
        """
        Calculate confusion matrix components
        """
        print(f"\n🧮 Calculating confusion matrix...")
        
        # Convert to sets for faster operations
        predicted_set = set(self.predicted_primes)
        true_set = set(self.true_primes)
        
        # True Positives: Correctly predicted primes
        tp_set = predicted_set.intersection(true_set)
        tp = len(tp_set)
        
        # False Positives: Non-primes predicted as primes
        fp_set = predicted_set - true_set
        fp = len(fp_set)
        
        # False Negatives: Primes missed by prediction
        fn_set = true_set - predicted_set
        fn = len(fn_set)
        
        # True Negatives: Non-primes correctly not predicted
        # TN = Total numbers - TP - FP - FN
        total_numbers = self.range_limit - 1  # Exclude 1
        tn = total_numbers - tp - fp - fn
        
        confusion_matrix = {
            'TP': tp,
            'FP': fp,
            'FN': fn,
            'TN': tn,
            'TP_numbers': sorted(list(tp_set)),
            'FP_numbers': sorted(list(fp_set)),
            'FN_numbers': sorted(list(fn_set))
        }
        
        print(f"📊 Confusion Matrix:")
        print(f"   True Positives (TP):  {tp:6d}")
        print(f"   False Positives (FP): {fp:6d}")
        print(f"   False Negatives (FN): {fn:6d}")
        print(f"   True Negatives (TN):  {tn:6d}")
        
        return confusion_matrix
    
    def calculate_metrics(self, confusion_matrix):
        """
        Calculate all accuracy metrics
        """
        print(f"\n📈 Calculating performance metrics...")
        
        tp = confusion_matrix['TP']
        fp = confusion_matrix['FP']
        fn = confusion_matrix['FN']
        tn = confusion_matrix['TN']
        
        # Precision = TP / (TP + FP)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        
        # Recall = TP / (TP + FN)
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        # F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Accuracy = (TP + TN) / (TP + TN + FP + FN)
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        
        # Specificity = TN / (TN + FP)
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        metrics = {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'accuracy': accuracy,
            'specificity': specificity
        }
        
        print(f"🎯 PERFORMANCE METRICS:")
        print(f"   Precision:    {precision:.6f} ({precision*100:.4f}%)")
        print(f"   Recall:       {recall:.6f} ({recall*100:.4f}%)")
        print(f"   F1-Score:     {f1_score:.6f} ({f1_score*100:.4f}%)")
        print(f"   Accuracy:     {accuracy:.6f} ({accuracy*100:.4f}%)")
        print(f"   Specificity:  {specificity:.6f} ({specificity*100:.4f}%)")
        
        return metrics
    
    def analyze_errors(self, confusion_matrix):
        """
        Detailed analysis of false positives and false negatives
        """
        print(f"\n🔍 ERROR ANALYSIS:")
        print("=" * 50)
        
        fp_numbers = confusion_matrix['FP_numbers']
        fn_numbers = confusion_matrix['FN_numbers']
        
        # False Positive Analysis
        print(f"\n❌ FALSE POSITIVES ({len(fp_numbers)} total):")
        if fp_numbers:
            print(f"   First 20: {fp_numbers[:20]}")
            if len(fp_numbers) > 20:
                print(f"   Last 10:  {fp_numbers[-10:]}")
            
            # Analyze patterns in false positives
            fp_factors = []
            for fp in fp_numbers[:50]:  # Analyze first 50
                factors = self._get_prime_factors(fp)
                fp_factors.append((fp, factors))
            
            print(f"\n🔍 False Positive Factor Analysis (first 10):")
            for fp, factors in fp_factors[:10]:
                print(f"   {fp} = {' × '.join(map(str, factors))}")
        else:
            print("   ✅ No false positives!")
        
        # False Negative Analysis  
        print(f"\n❌ FALSE NEGATIVES ({len(fn_numbers)} total):")
        if fn_numbers:
            print(f"   First 20: {fn_numbers[:20]}")
            if len(fn_numbers) > 20:
                print(f"   Last 10:  {fn_numbers[-10:]}")
            
            # Check if missed primes follow any pattern
            gaps = []
            for i in range(1, min(len(fn_numbers), 20)):
                gap = fn_numbers[i] - fn_numbers[i-1]
                gaps.append(gap)
            
            if gaps:
                print(f"   Gap patterns: {gaps[:10]}")
        else:
            print("   ✅ No false negatives!")
    
    def _get_prime_factors(self, n):
        """Get prime factorization of a number"""
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    def create_accuracy_visualization(self, confusion_matrix, metrics):
        """
        Create comprehensive visualization of accuracy results
        """
        print(f"\n📊 Creating accuracy visualization...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Confusion Matrix Heatmap
        cm_data = np.array([[confusion_matrix['TP'], confusion_matrix['FN']],
                           [confusion_matrix['FP'], confusion_matrix['TN']]])
        
        im1 = ax1.imshow(cm_data, cmap='Blues', interpolation='nearest')
        ax1.set_title('Confusion Matrix', fontweight='bold', fontsize=14)
        ax1.set_xlabel('Actual')
        ax1.set_ylabel('Predicted')
        ax1.set_xticks([0, 1])
        ax1.set_yticks([0, 1])
        ax1.set_xticklabels(['Prime', 'Non-Prime'])
        ax1.set_yticklabels(['Prime', 'Non-Prime'])
        
        # Add text annotations
        for i in range(2):
            for j in range(2):
                text = ax1.text(j, i, f'{cm_data[i, j]:,}',
                              ha="center", va="center", color="black", fontweight='bold')
        
        # Plot 2: Metrics Bar Chart
        metric_names = ['Precision', 'Recall', 'F1-Score', 'Accuracy', 'Specificity']
        metric_values = [metrics['precision'], metrics['recall'], metrics['f1_score'], 
                        metrics['accuracy'], metrics['specificity']]
        
        bars = ax2.bar(metric_names, metric_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'])
        ax2.set_title('Performance Metrics', fontweight='bold', fontsize=14)
        ax2.set_ylabel('Score')
        ax2.set_ylim(0, 1.1)
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
        
        # Plot 3: Prime Distribution Comparison
        true_count = len(self.true_primes)
        pred_count = len(self.predicted_primes)
        
        categories = ['True Primes', 'Predicted Primes', 'Correct (TP)', 'False Positive', 'False Negative']
        counts = [true_count, pred_count, confusion_matrix['TP'], 
                 confusion_matrix['FP'], confusion_matrix['FN']]
        colors = ['#2E8B57', '#4169E1', '#32CD32', '#FF4500', '#DC143C']
        
        bars3 = ax3.bar(categories, counts, color=colors)
        ax3.set_title('Prime Count Comparison', fontweight='bold', fontsize=14)
        ax3.set_ylabel('Count')
        ax3.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, count in zip(bars3, counts):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + max(counts)*0.01,
                    f'{count:,}', ha='center', va='bottom', fontweight='bold')
        
        # Plot 4: Error Rate Analysis
        total_predictions = len(self.predicted_primes)
        total_actual_primes = len(self.true_primes)
        
        error_data = {
            'False Positive Rate': confusion_matrix['FP'] / total_predictions if total_predictions > 0 else 0,
            'False Negative Rate': confusion_matrix['FN'] / total_actual_primes if total_actual_primes > 0 else 0,
            'Miss Rate': confusion_matrix['FN'] / total_actual_primes if total_actual_primes > 0 else 0,
            'Fall-out': confusion_matrix['FP'] / (confusion_matrix['FP'] + confusion_matrix['TN']) if (confusion_matrix['FP'] + confusion_matrix['TN']) > 0 else 0
        }
        
        error_names = list(error_data.keys())
        error_values = list(error_data.values())
        
        bars4 = ax4.bar(error_names, error_values, color=['#FF6B6B', '#FF8E53', '#FF6B9D', '#C44569'])
        ax4.set_title('Error Rates', fontweight='bold', fontsize=14)
        ax4.set_ylabel('Error Rate')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars4, error_values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + max(error_values)*0.01,
                    f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Visualization complete!")
    
    def save_accuracy_report(self, confusion_matrix, metrics, filename="accuracy_report.txt"):
        """
        Save detailed accuracy report to file
        """
        print(f"\n💾 Saving accuracy report to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("PRIME WAVE THEORY - ACCURACY REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: August 3, 2025\n")
            f.write(f"Analysis Range: 1 to {self.range_limit}\n")
            f.write(f"Total Numbers Analyzed: {self.range_limit - 1:,}\n\n")
            
            # Summary
            f.write("SUMMARY:\n")
            f.write("-" * 20 + "\n")
            f.write(f"True Primes (Ground Truth):    {len(self.true_primes):6,}\n")
            f.write(f"Predicted Primes:              {len(self.predicted_primes):6,}\n")
            f.write(f"Correctly Predicted:           {confusion_matrix['TP']:6,}\n")
            f.write(f"False Positives:               {confusion_matrix['FP']:6,}\n")
            f.write(f"False Negatives:               {confusion_matrix['FN']:6,}\n\n")
            
            # Confusion Matrix
            f.write("CONFUSION MATRIX:\n")
            f.write("-" * 20 + "\n")
            f.write(f"True Positives (TP):           {confusion_matrix['TP']:6,}\n")
            f.write(f"False Positives (FP):          {confusion_matrix['FP']:6,}\n")
            f.write(f"False Negatives (FN):          {confusion_matrix['FN']:6,}\n")
            f.write(f"True Negatives (TN):           {confusion_matrix['TN']:6,}\n\n")
            
            # Performance Metrics
            f.write("PERFORMANCE METRICS:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Precision:     {metrics['precision']:.6f} ({metrics['precision']*100:.4f}%)\n")
            f.write(f"Recall:        {metrics['recall']:.6f} ({metrics['recall']*100:.4f}%)\n")
            f.write(f"F1-Score:      {metrics['f1_score']:.6f} ({metrics['f1_score']*100:.4f}%)\n")
            f.write(f"Accuracy:      {metrics['accuracy']:.6f} ({metrics['accuracy']*100:.4f}%)\n")
            f.write(f"Specificity:   {metrics['specificity']:.6f} ({metrics['specificity']*100:.4f}%)\n\n")
            
            # Error Analysis
            f.write("ERROR ANALYSIS:\n")
            f.write("-" * 20 + "\n")
            
            if confusion_matrix['FP_numbers']:
                f.write(f"False Positives ({len(confusion_matrix['FP_numbers'])} total):\n")
                fp_numbers = confusion_matrix['FP_numbers']
                for i in range(0, len(fp_numbers), 10):
                    line_fps = fp_numbers[i:i+10]
                    f.write("  " + " ".join(f"{fp:6d}" for fp in line_fps) + "\n")
                f.write("\n")
            
            if confusion_matrix['FN_numbers']:
                f.write(f"False Negatives ({len(confusion_matrix['FN_numbers'])} total):\n")
                fn_numbers = confusion_matrix['FN_numbers']
                for i in range(0, len(fn_numbers), 10):
                    line_fns = fn_numbers[i:i+10]
                    f.write("  " + " ".join(f"{fn:6d}" for fn in line_fns) + "\n")
                f.write("\n")
            
            # Interpretation
            f.write("INTERPRETATION:\n")
            f.write("-" * 20 + "\n")
            f1 = metrics['f1_score']
            if f1 >= 0.99:
                f.write("🎉 EXCELLENT: Near-perfect prime prediction!\n")
            elif f1 >= 0.95:
                f.write("✅ VERY GOOD: High-quality prime prediction.\n")
            elif f1 >= 0.90:
                f.write("👍 GOOD: Solid prime prediction performance.\n")
            elif f1 >= 0.80:
                f.write("⚠️  FAIR: Moderate prime prediction accuracy.\n")
            else:
                f.write("❌ POOR: Low prime prediction accuracy.\n")
            
            f.write(f"\nThe Prime Wave Theory achieved an F1-Score of {f1:.6f},\n")
            f.write(f"indicating {'excellent' if f1 >= 0.99 else 'good' if f1 >= 0.90 else 'moderate'} performance in prime number prediction.\n")
        
        print(f"✅ Accuracy report saved to {filename}")

def main():
    """
    Main function to run the accuracy checker
    """
    print("🔍 PRIME ACCURACY CHECKER")
    print("=" * 40)
    print("Validating Prime Wave Theory predictions against ground truth")
    print()
    
    # Initialize checker
    checker = PrimeAccuracyChecker()
    
    # Load predicted primes
    if not checker.load_predicted_primes():
        print("❌ Failed to load predicted primes. Exiting.")
        return
    
    # Generate ground truth
    if checker.range_limit == 0:
        print("❌ Could not determine range limit. Exiting.")
        return
    
    checker.generate_true_primes_sieve(checker.range_limit)
    
    # Calculate accuracy
    confusion_matrix = checker.calculate_confusion_matrix()
    metrics = checker.calculate_metrics(confusion_matrix)
    
    # Analyze errors
    checker.analyze_errors(confusion_matrix)
    
    # Create visualization
    checker.create_accuracy_visualization(confusion_matrix, metrics)
    
    # Save report
    checker.save_accuracy_report(confusion_matrix, metrics)
    
    # Final summary
    print(f"\n🎉 ACCURACY CHECK COMPLETE!")
    print(f"✅ F1-Score: {metrics['f1_score']:.6f}")
    print(f"✅ Precision: {metrics['precision']:.6f}")  
    print(f"✅ Recall: {metrics['recall']:.6f}")
    print(f"✅ Detailed report saved to 'accuracy_report.txt'")

if __name__ == "__main__":
    main()
