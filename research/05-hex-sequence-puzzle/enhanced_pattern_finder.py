# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/enhanced_pattern_finder.py
# Original location      :: learn/enhanced_pattern_finder.py   (last edited 2025-08-11)
# What this script does  :: Searches the hex string for repeated patterns.
# ----------------------------------------------------------------------------
"""
Enhanced Pattern Finder for Hex Sequences
==========================================

Focuses on the most promising patterns discovered in the initial analysis
and implements sophisticated prediction algorithms.
"""

import math
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
import re

class EnhancedPatternFinder:
    """Advanced pattern finder focusing on discovered repetitions and mathematical relationships."""
    
    def __init__(self, hex_sequence: str):
        self.sequence = hex_sequence.upper().replace(' ', '')
        self.length = len(self.sequence)
        
        # Key patterns discovered in initial analysis
        self.key_patterns = {
            2: ['24', '81', 'A4'],  # Most frequent 2-char patterns
            3: ['58A', 'A16', '924'],  # Most frequent 3-char patterns
            4: ['258A', '5245', '2152'],  # Most frequent 4-char patterns
            6: ['51258A']  # 6-char repeating pattern
        }
        
    def find_pattern_positions(self, pattern: str) -> List[int]:
        """Find all positions where a pattern occurs."""
        positions = []
        start = 0
        while True:
            pos = self.sequence.find(pattern, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        return positions
    
    def analyze_pattern_spacing(self, pattern: str) -> Dict:
        """Analyze the spacing between pattern occurrences."""
        positions = self.find_pattern_positions(pattern)
        
        if len(positions) < 2:
            return {'pattern': pattern, 'positions': positions, 'spacing': []}
        
        spacings = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        
        return {
            'pattern': pattern,
            'positions': positions,
            'spacing': spacings,
            'avg_spacing': sum(spacings) / len(spacings) if spacings else 0,
            'spacing_frequency': Counter(spacings),
            'total_occurrences': len(positions)
        }
    
    def predict_next_pattern_occurrence(self, pattern: str) -> Dict:
        """Predict where a pattern might next occur."""
        analysis = self.analyze_pattern_spacing(pattern)
        
        if not analysis['spacing']:
            return {'prediction': None, 'confidence': 0}
        
        last_position = analysis['positions'][-1]
        spacings = analysis['spacing']
        
        # Method 1: Use most common spacing
        most_common_spacing = analysis['spacing_frequency'].most_common(1)[0][0]
        prediction_1 = last_position + most_common_spacing
        
        # Method 2: Use average spacing
        avg_spacing = int(analysis['avg_spacing'])
        prediction_2 = last_position + avg_spacing
        
        # Method 3: Look for arithmetic progression in spacings
        if len(spacings) >= 3:
            recent_spacings = spacings[-3:]
            if len(set(recent_spacings)) == 1:  # Constant spacing
                prediction_3 = last_position + recent_spacings[0]
                confidence = 0.8
            else:
                # Try to find pattern in spacing changes
                spacing_diffs = [recent_spacings[i+1] - recent_spacings[i] for i in range(len(recent_spacings)-1)]
                if len(set(spacing_diffs)) == 1:  # Arithmetic progression in spacings
                    next_spacing = recent_spacings[-1] + spacing_diffs[0]
                    prediction_3 = last_position + next_spacing
                    confidence = 0.6
                else:
                    prediction_3 = prediction_2
                    confidence = 0.4
        else:
            prediction_3 = prediction_2
            confidence = 0.3
        
        return {
            'pattern': pattern,
            'last_position': last_position,
            'predictions': {
                'most_common_spacing': prediction_1,
                'average_spacing': prediction_2,
                'pattern_based': prediction_3
            },
            'confidence': confidence,
            'analysis': analysis
        }
    
    def find_mathematical_relationships(self) -> Dict:
        """Find mathematical relationships in group values."""
        relationships = {}
        
        # Analyze different group sizes
        for size in [2, 3, 4, 6]:
            groups = [self.sequence[i:i+size] for i in range(0, self.length, size)]
            decimal_values = [int(group, 16) for group in groups if group]
            
            if len(decimal_values) < 3:
                continue
            
            # Look for arithmetic sequences
            differences = [decimal_values[i+1] - decimal_values[i] for i in range(len(decimal_values)-1)]
            
            # Look for geometric relationships
            ratios = []
            for i in range(len(decimal_values)-1):
                if decimal_values[i] != 0:
                    ratio = decimal_values[i+1] / decimal_values[i]
                    ratios.append(ratio)
            
            # Look for modular relationships
            modular_patterns = {}
            for mod in [7, 11, 13, 17, 19, 23]:  # Check small primes
                remainders = [val % mod for val in decimal_values[:20]]
                modular_patterns[mod] = Counter(remainders).most_common(3)
            
            relationships[f'size_{size}'] = {
                'arithmetic_differences': differences[:10],
                'geometric_ratios': ratios[:10],
                'modular_patterns': modular_patterns,
                'values_sample': decimal_values[:10]
            }
        
        return relationships
    
    def generate_next_groups(self, group_size: int, num_predictions: int = 3) -> List[str]:
        """Generate predictions for the next groups."""
        groups = [self.sequence[i:i+group_size] for i in range(0, self.length, group_size)]
        
        if len(groups) < 3:
            return []
        
        predictions = []
        
        # Method 1: Pattern continuation
        last_group = groups[-1]
        for pattern_size in self.key_patterns:
            if pattern_size <= group_size:
                for pattern in self.key_patterns[pattern_size]:
                    if pattern in last_group:
                        # Try to extend based on this pattern
                        extended = self._extend_with_pattern(last_group, pattern, group_size)
                        if extended and extended not in predictions:
                            predictions.append(extended)
        
        # Method 2: Mathematical progression
        decimal_values = [int(group, 16) for group in groups[-5:] if group]
        if len(decimal_values) >= 3:
            # Arithmetic progression
            recent_diffs = [decimal_values[i+1] - decimal_values[i] for i in range(len(decimal_values)-1)]
            if recent_diffs:
                avg_diff = sum(recent_diffs) / len(recent_diffs)
                next_decimal = decimal_values[-1] + int(avg_diff)
                if next_decimal > 0:
                    next_hex = hex(next_decimal)[2:].upper()
                    if len(next_hex) <= group_size:
                        next_hex = next_hex.zfill(group_size)
                        if next_hex not in predictions:
                            predictions.append(next_hex)
        
        # Method 3: XOR-based prediction
        if len(groups) >= 2:
            last_two_decimal = [int(groups[-2], 16), int(groups[-1], 16)]
            xor_result = last_two_decimal[0] ^ last_two_decimal[1]
            next_xor = last_two_decimal[1] ^ xor_result
            next_hex_xor = hex(next_xor)[2:].upper().zfill(group_size)
            if next_hex_xor not in predictions:
                predictions.append(next_hex_xor)
        
        return predictions[:num_predictions]
    
    def _extend_with_pattern(self, base_group: str, pattern: str, target_length: int) -> str:
        """Extend a group using a discovered pattern."""
        if len(base_group) >= target_length:
            return base_group[:target_length]
        
        # Find pattern position in base_group
        pattern_pos = base_group.find(pattern)
        if pattern_pos == -1:
            return None
        
        # Try to extend by repeating or cycling through the pattern
        extended = base_group
        while len(extended) < target_length:
            extended += pattern
        
        return extended[:target_length]
    
    def comprehensive_analysis(self) -> Dict:
        """Perform comprehensive analysis of all discovered patterns."""
        analysis = {
            'sequence_length': self.length,
            'pattern_predictions': {},
            'mathematical_relationships': self.find_mathematical_relationships(),
            'next_group_predictions': {}
        }
        
        # Analyze all key patterns
        for size, patterns in self.key_patterns.items():
            analysis['pattern_predictions'][f'size_{size}'] = {}
            for pattern in patterns:
                prediction = self.predict_next_pattern_occurrence(pattern)
                analysis['pattern_predictions'][f'size_{size}'][pattern] = prediction
        
        # Generate next group predictions
        for size in [2, 3, 4, 6, 8]:
            predictions = self.generate_next_groups(size)
            analysis['next_group_predictions'][f'size_{size}'] = predictions
        
        return analysis


def main():
    """Main analysis focusing on pattern prediction."""
    print("🔮 ENHANCED PATTERN FINDER - NEXT GROUP PREDICTION")
    print("=" * 55)
    
    # Your hex sequence
    hex_sequence = """FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A1621984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51A49F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A4249848471A14A22415A4E5BD278514A211285F8A2154B8215258A5D814268254184624A8112132122C25944A54815A42A5A845818211943A518484A1A81B8638132E214A12845C855251A482488AD94424B846224C13818252D4D844A4D816A1618A82592461E824A124E258468122858A8D2152459188172A247582A4C8A165125C2221C8E5A49A4A552182681D8742A211A18538B841A4651258A5814432924B552A1F7A511A4141AA1A1C8481AAC51258AD165A1942C"""
    
    finder = EnhancedPatternFinder(hex_sequence)
    analysis = finder.comprehensive_analysis()
    
    print(f"📊 Sequence Length: {analysis['sequence_length']} characters")
    
    # Show pattern predictions
    print(f"\n🎯 PATTERN OCCURRENCE PREDICTIONS")
    print("-" * 35)
    
    for size_key, patterns in analysis['pattern_predictions'].items():
        size = size_key.split('_')[1]
        print(f"\n📦 {size}-character patterns:")
        
        for pattern, prediction in patterns.items():
            if prediction['predictions']:
                print(f"   Pattern '{pattern}':")
                print(f"     Last seen at position: {prediction['last_position']}")
                print(f"     Next occurrence predictions:")
                for method, pos in prediction['predictions'].items():
                    print(f"       {method}: position {pos}")
                print(f"     Confidence: {prediction['confidence']:.1%}")
                print(f"     Total occurrences: {prediction['analysis']['total_occurrences']}")
    
    # Show next group predictions
    print(f"\n🔮 NEXT GROUP PREDICTIONS")
    print("-" * 25)
    
    for size_key, predictions in analysis['next_group_predictions'].items():
        size = size_key.split('_')[1]
        if predictions:
            print(f"\nNext {size}-character group predictions:")
            for i, pred in enumerate(predictions, 1):
                print(f"   Option {i}: {pred}")
    
    # Show mathematical relationships
    print(f"\n🧮 MATHEMATICAL RELATIONSHIPS")
    print("-" * 30)
    
    for size_key, relationships in analysis['mathematical_relationships'].items():
        size = size_key.split('_')[1]
        print(f"\n📊 {size}-character groups:")
        
        # Show arithmetic patterns
        if relationships['arithmetic_differences']:
            diffs = relationships['arithmetic_differences']
            print(f"   Arithmetic differences: {diffs[:5]}...")
            diff_counter = Counter(diffs)
            most_common = diff_counter.most_common(3)
            print(f"   Most common differences: {most_common}")
        
        # Show modular patterns
        print(f"   Modular patterns (most frequent remainders):")
        for mod, remainders in list(relationships['modular_patterns'].items())[:3]:
            top_remainder = remainders[0] if remainders else (0, 0)
            print(f"     mod {mod}: remainder {top_remainder[0]} appears {top_remainder[1]} times")
    
    # Final recommendations
    print(f"\n💡 RECOMMENDATIONS FOR NEXT STEPS")
    print("-" * 35)
    print("1. Test the predicted next groups by extending your sequence")
    print("2. Look for the patterns '24', '81', 'A4' which appear most frequently")
    print("3. Watch for the 6-character pattern '51258A' which shows strong repetition")
    print("4. Consider the mathematical progressions in 2-4 character groups")
    print("5. Monitor positions where patterns typically reoccur")
    
    print(f"\n✨ PATTERN ANALYSIS COMPLETE!")
    print("=" * 55)


if __name__ == "__main__":
    main()
