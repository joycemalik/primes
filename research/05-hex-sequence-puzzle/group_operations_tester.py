# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/group_operations_tester.py
# Original location      :: learn/group_operations_tester.py   (last edited 2025-08-11)
# What this script does  :: Tests arithmetic and XOR operations between hex groups.
# ----------------------------------------------------------------------------
"""
Group Operations Tester - Validation and Extension Tool
======================================================

Test the predicted groups and perform systematic operations to find patterns
that might be related to prime number generation or other mathematical sequences.
"""

import math
from typing import List, Dict, Tuple, Set
from collections import Counter
import itertools

class GroupOperationsTester:
    """Test and validate group predictions with systematic operations."""
    
    def __init__(self, hex_sequence: str):
        self.sequence = hex_sequence.upper().replace(' ', '')
        self.length = len(self.sequence)
        
        # Predictions from enhanced analysis
        self.predictions = {
            2: ['03', '94'],
            3: ['194'],
            4: ['A194'],
            6: ['65A194'],
            8: ['258AD165']
        }
    
    def test_prediction_validity(self, group_size: int, prediction: str) -> Dict:
        """Test if a prediction makes mathematical sense."""
        current_groups = [self.sequence[i:i+group_size] for i in range(0, self.length, group_size)]
        current_decimals = [int(group, 16) for group in current_groups if len(group) == group_size]
        
        if not current_decimals:
            return {'valid': False, 'reason': 'No complete groups found'}
        
        pred_decimal = int(prediction, 16)
        
        # Test 1: Range check
        min_val, max_val = min(current_decimals), max(current_decimals)
        range_valid = min_val <= pred_decimal <= max_val * 2  # Allow some expansion
        
        # Test 2: Mathematical progression check
        recent_values = current_decimals[-5:]
        if len(recent_values) >= 3:
            diffs = [recent_values[i+1] - recent_values[i] for i in range(len(recent_values)-1)]
            avg_diff = sum(diffs) / len(diffs)
            expected_next = recent_values[-1] + avg_diff
            progression_error = abs(pred_decimal - expected_next) / abs(expected_next) if expected_next != 0 else float('inf')
            progression_valid = progression_error < 0.5  # 50% tolerance
        else:
            progression_valid = True
            progression_error = 0
        
        # Test 3: Pattern consistency
        pred_hex_patterns = self._extract_hex_patterns(prediction)
        current_patterns = []
        for group in current_groups[-10:]:  # Check last 10 groups
            current_patterns.extend(self._extract_hex_patterns(group))
        
        common_patterns = set(pred_hex_patterns) & set(current_patterns)
        pattern_score = len(common_patterns) / len(pred_hex_patterns) if pred_hex_patterns else 0
        
        return {
            'valid': range_valid and progression_valid,
            'prediction': prediction,
            'decimal_value': pred_decimal,
            'range_valid': range_valid,
            'range_info': f'{min_val} <= {pred_decimal} <= {max_val * 2}',
            'progression_valid': progression_valid,
            'progression_error': progression_error,
            'pattern_score': pattern_score,
            'common_patterns': list(common_patterns),
            'confidence': (0.4 * range_valid + 0.4 * progression_valid + 0.2 * pattern_score)
        }
    
    def _extract_hex_patterns(self, hex_string: str) -> List[str]:
        """Extract common hex patterns from a string."""
        patterns = []
        for length in [1, 2]:
            for i in range(len(hex_string) - length + 1):
                patterns.append(hex_string[i:i+length])
        return patterns
    
    def perform_group_operations(self, groups: List[str]) -> Dict:
        """Perform various mathematical operations on groups."""
        if not groups:
            return {}
        
        # Convert to decimal
        decimals = [int(group, 16) for group in groups if group]
        
        operations = {}
        
        # Basic operations
        operations['sum'] = sum(decimals)
        operations['product'] = math.prod(decimals[:5])  # Limit to avoid overflow
        operations['xor_chain'] = self._xor_chain(decimals)
        operations['gcd_chain'] = self._gcd_chain(decimals[:10])
        
        # Prime-related operations
        operations['prime_factors'] = self._find_prime_factors_in_groups(decimals[:20])
        operations['digit_sums'] = [sum(int(d) for d in str(n)) for n in decimals[:10]]
        operations['digital_roots'] = [self._digital_root(n) for n in decimals[:10]]
        
        # Pattern operations
        operations['modular_classes'] = self._analyze_modular_classes(decimals[:20])
        operations['fibonacci_like'] = self._check_fibonacci_like(decimals[:10])
        
        return operations
    
    def _xor_chain(self, numbers: List[int]) -> int:
        """XOR all numbers in sequence."""
        result = 0
        for num in numbers:
            result ^= num
        return result
    
    def _gcd_chain(self, numbers: List[int]) -> int:
        """Find GCD of all numbers."""
        if not numbers:
            return 0
        result = numbers[0]
        for num in numbers[1:]:
            result = math.gcd(result, num)
            if result == 1:
                break
        return result
    
    def _find_prime_factors_in_groups(self, numbers: List[int]) -> Dict:
        """Find prime factors present in the groups."""
        all_factors = []
        
        for num in numbers:
            if num < 2:
                continue
            factors = self._prime_factors(num)
            all_factors.extend(factors)
        
        factor_freq = Counter(all_factors)
        return {
            'most_common_factors': factor_freq.most_common(10),
            'unique_primes': len(set(all_factors)),
            'total_prime_factors': len(all_factors)
        }
    
    def _prime_factors(self, n: int) -> List[int]:
        """Find prime factors of a number."""
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
    
    def _digital_root(self, n: int) -> int:
        """Calculate digital root of a number."""
        while n >= 10:
            n = sum(int(digit) for digit in str(n))
        return n
    
    def _analyze_modular_classes(self, numbers: List[int]) -> Dict:
        """Analyze modular arithmetic patterns."""
        modular_analysis = {}
        
        for mod in [3, 7, 11, 13, 17, 19]:
            remainders = [n % mod for n in numbers]
            modular_analysis[f'mod_{mod}'] = {
                'remainders': remainders,
                'distribution': dict(Counter(remainders)),
                'most_common': Counter(remainders).most_common(1)[0] if remainders else (0, 0)
            }
        
        return modular_analysis
    
    def _check_fibonacci_like(self, numbers: List[int]) -> Dict:
        """Check if sequence has Fibonacci-like properties."""
        if len(numbers) < 3:
            return {'is_fibonacci_like': False}
        
        fibonacci_matches = 0
        total_checks = 0
        
        for i in range(2, len(numbers)):
            if numbers[i] == numbers[i-1] + numbers[i-2]:
                fibonacci_matches += 1
            total_checks += 1
        
        fibonacci_ratio = fibonacci_matches / total_checks if total_checks > 0 else 0
        
        return {
            'is_fibonacci_like': fibonacci_ratio > 0.5,
            'fibonacci_ratio': fibonacci_ratio,
            'matches': fibonacci_matches,
            'total_checks': total_checks
        }
    
    def compare_group_operations(self, sizes: List[int]) -> Dict:
        """Compare operations across different group sizes."""
        comparison = {}
        
        for size in sizes:
            groups = [self.sequence[i:i+size] for i in range(0, self.length, size)]
            operations = self.perform_group_operations(groups)
            comparison[f'size_{size}'] = operations
        
        # Find similarities
        similarities = {}
        for op_type in ['digital_roots', 'modular_classes']:
            similarities[op_type] = {}
            for size1, size2 in itertools.combinations(sizes, 2):
                key = f'{size1}_vs_{size2}'
                ops1 = comparison[f'size_{size1}'].get(op_type, {})
                ops2 = comparison[f'size_{size2}'].get(op_type, {})
                
                if isinstance(ops1, list) and isinstance(ops2, list):
                    common = set(ops1[:10]) & set(ops2[:10])
                    similarities[op_type][key] = list(common)
        
        comparison['similarities'] = similarities
        return comparison
    
    def generate_next_sequence_candidates(self, group_size: int, num_candidates: int = 5) -> List[str]:
        """Generate multiple candidates for the next part of the sequence."""
        candidates = []
        
        current_groups = [self.sequence[i:i+group_size] for i in range(0, self.length, group_size)]
        complete_groups = [g for g in current_groups if len(g) == group_size]
        
        if len(complete_groups) < 2:
            return candidates
        
        # Method 1: Continue most frequent patterns
        all_patterns = []
        for group in complete_groups:
            for i in range(len(group) - 1):
                all_patterns.append(group[i:i+2])
        
        pattern_freq = Counter(all_patterns)
        for pattern, _ in pattern_freq.most_common(3):
            candidate = pattern * (group_size // 2) + pattern[:group_size % 2]
            if candidate not in candidates:
                candidates.append(candidate)
        
        # Method 2: Mathematical progressions
        decimals = [int(g, 16) for g in complete_groups[-5:]]
        if len(decimals) >= 2:
            diff = decimals[-1] - decimals[-2]
            next_decimal = decimals[-1] + diff
            if next_decimal > 0:
                next_hex = hex(next_decimal)[2:].upper()
                next_hex = next_hex[-group_size:].zfill(group_size)
                if next_hex not in candidates:
                    candidates.append(next_hex)
        
        # Method 3: XOR patterns
        if len(decimals) >= 2:
            xor_result = decimals[-1] ^ decimals[-2]
            next_xor = decimals[-1] ^ xor_result
            next_hex_xor = hex(next_xor)[2:].upper()
            next_hex_xor = next_hex_xor[-group_size:].zfill(group_size)
            if next_hex_xor not in candidates:
                candidates.append(next_hex_xor)
        
        # Method 4: Reverse patterns
        if complete_groups:
            reversed_last = complete_groups[-1][::-1]
            if reversed_last not in candidates:
                candidates.append(reversed_last)
        
        return candidates[:num_candidates]


def main():
    """Main testing and validation function."""
    print("🧪 GROUP OPERATIONS TESTER - VALIDATION & EXTENSION")
    print("=" * 55)
    
    # Your hex sequence
    hex_sequence = """FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A1621984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51A49F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A4249848471A14A22415A4E5BD278514A211285F8A2154B8215258A5D814268254184624A8112132122C25944A54815A42A5A845818211943A518484A1A81B8638132E214A12845C855251A482488AD94424B846224C13818252D4D844A4D816A1618A82592461E824A124E258468122858A8D2152459188172A247582A4C8A165125C2221C8E5A49A4A552182681D8742A211A18538B841A4651258A5814432924B552A1F7A511A4141AA1A1C8481AAC51258AD165A1942C"""
    
    tester = GroupOperationsTester(hex_sequence)
    
    print(f"📊 Testing predictions and generating candidates...")
    print(f"Original sequence length: {tester.length}")
    
    # Test all predictions
    print(f"\n🔍 PREDICTION VALIDATION")
    print("-" * 25)
    
    for size, predictions in tester.predictions.items():
        print(f"\n📦 Group size {size}:")
        for pred in predictions:
            validation = tester.test_prediction_validity(size, pred)
            confidence = validation['confidence']
            status = "✅ VALID" if validation['valid'] else "⚠️ QUESTIONABLE"
            
            print(f"   Prediction: {pred}")
            print(f"   Status: {status} (confidence: {confidence:.1%})")
            print(f"   Decimal value: {validation['decimal_value']:,}")
            if validation['common_patterns']:
                print(f"   Common patterns: {validation['common_patterns']}")
    
    # Generate additional candidates
    print(f"\n🎯 ADDITIONAL CANDIDATES")
    print("-" * 25)
    
    for size in [2, 3, 4, 6]:
        candidates = tester.generate_next_sequence_candidates(size)
        print(f"\nGroup size {size} candidates:")
        for i, candidate in enumerate(candidates, 1):
            print(f"   {i}. {candidate}")
    
    # Perform cross-group analysis
    print(f"\n🔬 CROSS-GROUP OPERATIONS ANALYSIS")
    print("-" * 35)
    
    comparison = tester.compare_group_operations([2, 3, 4])
    
    for size_key, operations in comparison.items():
        if size_key == 'similarities':
            continue
        
        size = size_key.split('_')[1]
        print(f"\n📊 Group size {size} operations:")
        
        if 'prime_factors' in operations:
            pf = operations['prime_factors']
            if pf['most_common_factors']:
                print(f"   Most common prime factors: {pf['most_common_factors'][:3]}")
        
        if 'digital_roots' in operations:
            roots = operations['digital_roots']
            root_freq = Counter(roots)
            print(f"   Digital roots distribution: {dict(root_freq.most_common(3))}")
        
        if 'fibonacci_like' in operations:
            fib = operations['fibonacci_like']
            if fib['fibonacci_ratio'] > 0.2:
                print(f"   Fibonacci-like ratio: {fib['fibonacci_ratio']:.1%}")
        
        if 'xor_chain' in operations:
            print(f"   XOR chain result: {operations['xor_chain']} (0x{operations['xor_chain']:X})")
    
    # Show similarities
    if 'similarities' in comparison:
        print(f"\n🔗 CROSS-SIZE SIMILARITIES")
        print("-" * 25)
        sims = comparison['similarities']
        for op_type, sim_data in sims.items():
            if any(sim_data.values()):
                print(f"\n{op_type} similarities:")
                for comparison_key, common_items in sim_data.items():
                    if common_items:
                        print(f"   {comparison_key}: {common_items}")
    
    # Final recommendations
    print(f"\n💡 SYSTEMATIC NEXT STEPS")
    print("-" * 25)
    print("1. Test the highest confidence predictions first")
    print("2. Look for mathematical progressions in your data")
    print("3. Check if XOR operations reveal hidden patterns")
    print("4. Monitor digital root distributions for anomalies")
    print("5. Use the generated candidates as starting points")
    print("6. Compare results across different group sizes")
    
    print(f"\n✅ TESTING COMPLETE - Ready for pattern exploration!")
    print("=" * 55)


if __name__ == "__main__":
    main()
