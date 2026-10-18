# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/primes24_hex_sequence_analyzer.py
# Original location      :: learn/primes24.py   (last edited 2025-08-11)
# What this script does  :: Hex-sequence analyser: groupings, sliding windows, statistics.
# ----------------------------------------------------------------------------
"""
Hexadecimal Sequence Grouping and Pattern Analysis
==================================================

Analyzing hex sequences through multiple grouping strategies to discover patterns
that might relate to prime number generation or mathematical sequences.
"""

import math
import re
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
import itertools

class HexSequenceAnalyzer:
    """Comprehensive analyzer for hexadecimal sequences with multiple grouping strategies."""
    
    def __init__(self, hex_sequence: str):
        """Initialize with the hex sequence."""
        self.original_sequence = hex_sequence.upper().replace(' ', '')
        self.length = len(self.original_sequence)
        print(f"🔍 Initialized with sequence of length: {self.length}")
        
    def validate_hex(self) -> bool:
        """Validate that the sequence contains only valid hex characters."""
        valid_chars = set('0123456789ABCDEF')
        sequence_chars = set(self.original_sequence)
        invalid = sequence_chars - valid_chars
        
        if invalid:
            print(f"⚠️ Invalid hex characters found: {invalid}")
            return False
        print("✅ Valid hexadecimal sequence")
        return True
    
    def convert_to_numbers(self, base: int = 16) -> List[int]:
        """Convert hex digits to numbers in specified base."""
        return [int(char, base) for char in self.original_sequence]
    
    def group_by_size(self, group_size: int) -> List[str]:
        """Group sequence into chunks of specified size."""
        groups = []
        for i in range(0, self.length, group_size):
            group = self.original_sequence[i:i + group_size]
            groups.append(group)
        return groups
    
    def analyze_group_patterns(self, groups: List[str]) -> Dict:
        """Analyze patterns within groups."""
        analysis = {
            'group_count': len(groups),
            'group_frequencies': Counter(groups),
            'unique_groups': len(set(groups)),
            'most_common': Counter(groups).most_common(5),
            'group_lengths': [len(g) for g in groups],
            'repeated_groups': [group for group, count in Counter(groups).items() if count > 1]
        }
        return analysis
    
    def sliding_window_analysis(self, window_size: int, step: int = 1) -> Dict:
        """Analyze using sliding window approach."""
        windows = []
        for i in range(0, self.length - window_size + 1, step):
            window = self.original_sequence[i:i + window_size]
            windows.append(window)
        
        return self.analyze_group_patterns(windows)
    
    def mathematical_operations_on_groups(self, groups: List[str]) -> Dict:
        """Perform mathematical operations on hex groups."""
        operations = {}
        
        # Convert to decimal values
        decimal_values = [int(group, 16) if group else 0 for group in groups]
        operations['decimal_values'] = decimal_values[:10]  # Show first 10
        
        # Basic statistics
        if decimal_values:
            operations['sum'] = sum(decimal_values)
            operations['average'] = sum(decimal_values) / len(decimal_values)
            operations['min'] = min(decimal_values)
            operations['max'] = max(decimal_values)
            operations['range'] = max(decimal_values) - min(decimal_values)
        
        # Differences between consecutive groups
        if len(decimal_values) > 1:
            differences = [decimal_values[i+1] - decimal_values[i] for i in range(len(decimal_values)-1)]
            operations['differences'] = differences[:10]  # Show first 10
            operations['diff_patterns'] = Counter(differences).most_common(5)
        
        # XOR operations
        if len(decimal_values) > 1:
            xor_results = [decimal_values[i] ^ decimal_values[i+1] for i in range(len(decimal_values)-1)]
            operations['xor_results'] = xor_results[:10]
        
        # Check for prime-related patterns
        operations['potentially_prime'] = [val for val in decimal_values[:20] if self.is_likely_prime(val)]
        
        return operations
    
    def is_likely_prime(self, n: int) -> bool:
        """Quick primality check for pattern detection."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def find_repeating_patterns(self, min_length: int = 2, max_length: int = 10) -> Dict:
        """Find repeating patterns of various lengths."""
        patterns = {}
        
        for length in range(min_length, min(max_length + 1, self.length // 2)):
            pattern_counts = Counter()
            
            for i in range(self.length - length + 1):
                pattern = self.original_sequence[i:i + length]
                pattern_counts[pattern] += 1
            
            # Only include patterns that repeat
            repeating = {pattern: count for pattern, count in pattern_counts.items() if count > 1}
            if repeating:
                patterns[f'length_{length}'] = dict(Counter(repeating).most_common(5))
        
        return patterns
    
    def analyze_multiple_group_sizes(self, sizes: List[int]) -> Dict:
        """Analyze the sequence with multiple grouping sizes and compare results."""
        multi_analysis = {}
        
        for size in sizes:
            groups = self.group_by_size(size)
            analysis = self.analyze_group_patterns(groups)
            operations = self.mathematical_operations_on_groups(groups)
            
            multi_analysis[f'size_{size}'] = {
                'groups': groups[:5],  # Show first 5 groups
                'analysis': analysis,
                'operations': operations
            }
        
        return multi_analysis
    
    def find_cross_group_similarities(self, sizes: List[int]) -> Dict:
        """Find similarities across different grouping strategies."""
        similarities = {}
        all_group_data = {}
        
        # Collect data from all grouping sizes
        for size in sizes:
            groups = self.group_by_size(size)
            operations = self.mathematical_operations_on_groups(groups)
            all_group_data[size] = {
                'groups': groups,
                'decimal_values': operations.get('decimal_values', []),
                'differences': operations.get('differences', []),
                'xor_results': operations.get('xor_results', [])
            }
        
        # Compare patterns across sizes
        for i, size1 in enumerate(sizes):
            for size2 in sizes[i+1:]:
                key = f'{size1}_vs_{size2}'
                similarities[key] = {
                    'common_decimal_values': list(set(all_group_data[size1]['decimal_values']) & 
                                                 set(all_group_data[size2]['decimal_values'])),
                    'similar_differences': list(set(all_group_data[size1]['differences']) & 
                                              set(all_group_data[size2]['differences']))
                }
        
        return similarities
    
    def predict_next_group(self, group_size: int, prediction_methods: List[str] = None) -> Dict:
        """Attempt to predict the next group based on patterns."""
        if prediction_methods is None:
            prediction_methods = ['arithmetic', 'geometric', 'pattern_continuation', 'xor_pattern']
        
        groups = self.group_by_size(group_size)
        operations = self.mathematical_operations_on_groups(groups)
        decimal_values = operations.get('decimal_values', [])
        
        predictions = {}
        
        # Arithmetic progression
        if 'arithmetic' in prediction_methods and len(decimal_values) >= 2:
            differences = operations.get('differences', [])
            if differences:
                avg_diff = sum(differences) / len(differences)
                next_arithmetic = decimal_values[-1] + int(avg_diff)
                predictions['arithmetic'] = {
                    'next_decimal': next_arithmetic,
                    'next_hex': hex(max(0, next_arithmetic))[2:].upper(),
                    'confidence': 'medium'
                }
        
        # Pattern continuation
        if 'pattern_continuation' in prediction_methods and len(groups) >= 3:
            # Look for repeating patterns
            last_three = groups[-3:]
            if len(set(last_three)) == 1:  # All same
                predictions['pattern_continuation'] = {
                    'next_hex': last_three[0],
                    'confidence': 'high',
                    'reason': 'repeating_pattern'
                }
            elif last_three[0] == last_three[2]:  # Alternating
                predictions['pattern_continuation'] = {
                    'next_hex': last_three[1],
                    'confidence': 'medium',
                    'reason': 'alternating_pattern'
                }
        
        # XOR pattern
        if 'xor_pattern' in prediction_methods and len(decimal_values) >= 2:
            xor_results = operations.get('xor_results', [])
            if xor_results:
                # Assume XOR pattern continues
                last_xor = xor_results[-1]
                next_xor_based = decimal_values[-1] ^ last_xor
                predictions['xor_pattern'] = {
                    'next_decimal': next_xor_based,
                    'next_hex': hex(next_xor_based)[2:].upper(),
                    'confidence': 'low'
                }
        
        return predictions


def main():
    """Main analysis function."""
    print("🔬 HEXADECIMAL SEQUENCE GROUPING AND PATTERN ANALYSIS")
    print("=" * 60)
    
    # Your hex sequence
    hex_sequence = """FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A1621984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51A49F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A4249848471A14A22415A4E5BD278514A211285F8A2154B8215258A5D814268254184624A8112132122C25944A54815A42A5A845818211943A518484A1A81B8638132E214A12845C855251A482488AD94424B846224C13818252D4D844A4D816A1618A82592461E824A124E258468122858A8D2152459188172A247582A4C8A165125C2221C8E5A49A4A552182681D8742A211A18538B841A4651258A5814432924B552A1F7A511A4141AA1A1C8481AAC51258AD165A1942C"""
    
    # Initialize analyzer
    analyzer = HexSequenceAnalyzer(hex_sequence)
    
    # Validate sequence
    if not analyzer.validate_hex():
        return
    
    print(f"\n📊 BASIC SEQUENCE INFO")
    print(f"Length: {analyzer.length} characters")
    print(f"First 50 chars: {analyzer.original_sequence[:50]}...")
    print(f"Last 50 chars: ...{analyzer.original_sequence[-50:]}")
    
    # Test multiple grouping sizes
    test_sizes = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16]
    
    print(f"\n🔍 MULTI-SIZE GROUP ANALYSIS")
    print("-" * 40)
    
    multi_analysis = analyzer.analyze_multiple_group_sizes(test_sizes)
    
    for size_key, data in multi_analysis.items():
        size = int(size_key.split('_')[1])
        analysis = data['analysis']
        operations = data['operations']
        
        print(f"\n📦 Group Size: {size}")
        print(f"   Groups created: {analysis['group_count']}")
        print(f"   Unique groups: {analysis['unique_groups']}")
        print(f"   First 3 groups: {data['groups'][:3]}")
        
        if operations.get('decimal_values'):
            print(f"   Decimal values (first 5): {operations['decimal_values'][:5]}")
            print(f"   Sum: {operations.get('sum', 'N/A')}")
            print(f"   Average: {operations.get('average', 'N/A'):.2f}" if operations.get('average') else "   Average: N/A")
        
        if operations.get('potentially_prime'):
            print(f"   Potential primes found: {len(operations['potentially_prime'])}")
            print(f"   Prime candidates: {operations['potentially_prime'][:5]}")
    
    # Find cross-group similarities
    print(f"\n🔗 CROSS-GROUP SIMILARITIES")
    print("-" * 30)
    
    similarities = analyzer.find_cross_group_similarities([2, 3, 4, 6, 8])
    
    for comparison, sim_data in similarities.items():
        if sim_data['common_decimal_values'] or sim_data['similar_differences']:
            print(f"\n{comparison}:")
            if sim_data['common_decimal_values']:
                print(f"   Common values: {sim_data['common_decimal_values'][:5]}")
            if sim_data['similar_differences']:
                print(f"   Similar differences: {sim_data['similar_differences'][:5]}")
    
    # Find repeating patterns
    print(f"\n🔄 REPEATING PATTERNS")
    print("-" * 20)
    
    patterns = analyzer.find_repeating_patterns(min_length=2, max_length=8)
    
    for pattern_type, pattern_data in patterns.items():
        print(f"\n{pattern_type}:")
        for pattern, count in list(pattern_data.items())[:3]:
            print(f"   '{pattern}' appears {count} times")
    
    # Predict next groups
    print(f"\n🔮 PREDICTION ATTEMPTS")
    print("-" * 22)
    
    for size in [2, 3, 4, 6]:
        print(f"\nGroup size {size} predictions:")
        predictions = analyzer.predict_next_group(size)
        
        for method, pred_data in predictions.items():
            print(f"   {method}: {pred_data.get('next_hex', 'N/A')} (confidence: {pred_data.get('confidence', 'unknown')})")
            if 'reason' in pred_data:
                print(f"     Reason: {pred_data['reason']}")
    
    # Special analysis for potential prime connections
    print(f"\n🔢 PRIME-RELATED ANALYSIS")
    print("-" * 25)
    
    # Convert entire sequence to numbers and look for prime patterns
    all_numbers = analyzer.convert_to_numbers()
    prime_positions = []
    
    for i, num in enumerate(all_numbers[:100]):  # Check first 100
        if analyzer.is_likely_prime(num):
            prime_positions.append((i, num, hex(num)[2:].upper()))
    
    if prime_positions:
        print(f"Prime numbers found in first 100 positions:")
        for pos, num, hex_val in prime_positions[:10]:
            print(f"   Position {pos}: {num} (0x{hex_val})")
        
        # Look for patterns in prime positions
        positions = [pos for pos, _, _ in prime_positions]
        if len(positions) > 1:
            pos_diffs = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
            print(f"   Position differences: {pos_diffs[:10]}")
            common_diffs = Counter(pos_diffs).most_common(3)
            print(f"   Most common differences: {common_diffs}")
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
