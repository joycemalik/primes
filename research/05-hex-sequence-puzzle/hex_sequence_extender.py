# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/hex_sequence_extender.py
# Original location      :: learn/hex_sequence_extender.py   (last edited 2025-08-11)
# What this script does  :: Extends the hex string with discovered patterns.
# ----------------------------------------------------------------------------
"""
Hex Sequence Pattern Extender
============================

Extends the hex sequence using discovered patterns and validates new extensions
to find the most likely continuation patterns.
"""

import math
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
import itertools

class HexSequenceExtender:
    """Extend hex sequences using pattern analysis and validation."""
    
    def __init__(self, hex_sequence: str):
        self.original_sequence = hex_sequence.upper().replace(' ', '')
        self.length = len(self.original_sequence)
        
        # Best predictions from our analysis
        self.validated_predictions = {
            4: "A194",      # 100% confidence
            6: "65A194",    # 100% confidence
            2: "94",        # 60% confidence
            3: "194",       # 60% confidence
        }
        
        # Key repeating patterns discovered
        self.key_patterns = {
            '24': 27,   # appears 27 times
            '81': 24,   # appears 24 times
            'A4': 23,   # appears 23 times
            '58A': 7,   # appears 7 times
            '51258A': 2 # appears 2 times
        }
    
    def extend_sequence(self, extension_length: int = 50) -> str:
        """Extend the sequence using validated patterns."""
        extended = self.original_sequence
        target_length = self.length + extension_length
        
        print(f"🚀 Extending sequence from {self.length} to {target_length} characters")
        
        while len(extended) < target_length:
            # Use different strategies based on remaining length needed
            remaining = target_length - len(extended)
            
            if remaining >= 6:
                # Use 6-character prediction
                next_part = self.validated_predictions[6]
                print(f"   Adding 6-char pattern: {next_part}")
            elif remaining >= 4:
                # Use 4-character prediction
                next_part = self.validated_predictions[4]
                print(f"   Adding 4-char pattern: {next_part}")
            elif remaining >= 3:
                # Use 3-character prediction
                next_part = self.validated_predictions[3]
                print(f"   Adding 3-char pattern: {next_part}")
            elif remaining >= 2:
                # Use 2-character prediction
                next_part = self.validated_predictions[2]
                print(f"   Adding 2-char pattern: {next_part}")
            else:
                # Single character - use most common
                next_part = self._get_most_common_char(extended)
                print(f"   Adding single char: {next_part}")
            
            extended += next_part
        
        return extended[:target_length]
    
    def _get_most_common_char(self, sequence: str) -> str:
        """Get the most common character in the sequence."""
        char_freq = Counter(sequence)
        return char_freq.most_common(1)[0][0]
    
    def validate_extension(self, extended_sequence: str) -> Dict:
        """Validate the extended sequence for pattern consistency."""
        extension_start = self.length
        extension = extended_sequence[extension_start:]
        
        validation = {
            'extension': extension,
            'extension_length': len(extension),
            'pattern_matches': {},
            'mathematical_consistency': {},
            'new_patterns_found': {}
        }
        
        # Check if our key patterns appear in the extension
        for pattern, original_count in self.key_patterns.items():
            extension_count = extension.count(pattern)
            total_count = extended_sequence.count(pattern)
            
            validation['pattern_matches'][pattern] = {
                'original_count': original_count,
                'extension_count': extension_count,
                'new_total': total_count,
                'pattern_density': extension_count / len(extension) if extension else 0
            }
        
        # Check mathematical consistency
        validation['mathematical_consistency'] = self._check_mathematical_consistency(extended_sequence)
        
        # Find new patterns in the extension
        validation['new_patterns_found'] = self._find_new_patterns(extension)
        
        return validation
    
    def _check_mathematical_consistency(self, sequence: str) -> Dict:
        """Check if mathematical relationships hold in the extended sequence."""
        consistency = {}
        
        # Test different group sizes
        for size in [2, 3, 4, 6]:
            groups = [sequence[i:i+size] for i in range(0, len(sequence), size)]
            complete_groups = [g for g in groups if len(g) == size]
            
            if len(complete_groups) < 5:
                continue
            
            # Convert to decimal and analyze
            decimals = [int(group, 16) for group in complete_groups]
            
            # Check arithmetic progression consistency
            diffs = [decimals[i+1] - decimals[i] for i in range(len(decimals)-1)]
            recent_diffs = diffs[-5:]  # Last 5 differences
            
            diff_consistency = len(set(recent_diffs)) / len(recent_diffs) if recent_diffs else 0
            
            # Check XOR pattern consistency
            xor_results = [decimals[i] ^ decimals[i+1] for i in range(len(decimals)-1)]
            recent_xors = xor_results[-5:]
            
            xor_consistency = len(set(recent_xors)) / len(recent_xors) if recent_xors else 0
            
            consistency[f'size_{size}'] = {
                'arithmetic_consistency': 1 - diff_consistency,  # Lower diversity = higher consistency
                'xor_consistency': 1 - xor_consistency,
                'recent_differences': recent_diffs,
                'recent_xors': recent_xors
            }
        
        return consistency
    
    def _find_new_patterns(self, extension: str) -> Dict:
        """Find new repeating patterns in the extension."""
        new_patterns = {}
        
        for length in range(2, min(8, len(extension) // 2)):
            pattern_counts = Counter()
            
            for i in range(len(extension) - length + 1):
                pattern = extension[i:i + length]
                pattern_counts[pattern] += 1
            
            # Only include patterns that repeat
            repeating = {pattern: count for pattern, count in pattern_counts.items() if count > 1}
            if repeating:
                new_patterns[f'length_{length}'] = dict(Counter(repeating).most_common(5))
        
        return new_patterns
    
    def progressive_extension(self, steps: int = 5, step_size: int = 10) -> List[Dict]:
        """Extend sequence progressively and analyze each step."""
        results = []
        current_sequence = self.original_sequence
        
        print(f"🔄 Progressive extension: {steps} steps of {step_size} characters each")
        
        for step in range(steps):
            print(f"\n📊 Step {step + 1}/{steps}")
            
            # Extend by step_size characters
            extended = self.extend_sequence_smart(current_sequence, step_size)
            
            # Validate the extension
            validation = self.validate_extension_from_base(current_sequence, extended)
            
            # Analyze new patterns
            analysis = self.analyze_step_patterns(current_sequence, extended)
            
            step_result = {
                'step': step + 1,
                'base_length': len(current_sequence),
                'extended_length': len(extended),
                'extension': extended[len(current_sequence):],
                'validation': validation,
                'analysis': analysis
            }
            
            results.append(step_result)
            current_sequence = extended
            
            print(f"   Extension: {step_result['extension']}")
            print(f"   New patterns found: {len(analysis.get('new_patterns', {}))}")
        
        return results
    
    def extend_sequence_smart(self, base_sequence: str, extension_length: int) -> str:
        """Smart extension using pattern analysis of the base sequence."""
        extended = base_sequence
        
        # Analyze the end of the current sequence for patterns
        tail_analysis = self._analyze_sequence_tail(base_sequence, 50)
        
        remaining = extension_length
        while remaining > 0:
            # Choose extension method based on tail analysis
            if remaining >= 6 and '51258A' in tail_analysis['recent_patterns']:
                next_part = '51258A'
            elif remaining >= 4:
                next_part = self._predict_next_group(base_sequence, 4)
            elif remaining >= 3:
                next_part = self._predict_next_group(base_sequence, 3)
            elif remaining >= 2:
                next_part = self._predict_next_group(base_sequence, 2)
            else:
                next_part = self._predict_next_char(base_sequence)
            
            extended += next_part
            remaining -= len(next_part)
        
        return extended
    
    def _analyze_sequence_tail(self, sequence: str, tail_length: int) -> Dict:
        """Analyze patterns in the tail of the sequence."""
        tail = sequence[-tail_length:] if len(sequence) > tail_length else sequence
        
        analysis = {
            'tail': tail,
            'tail_length': len(tail),
            'recent_patterns': [],
            'char_frequency': Counter(tail),
            'pattern_frequency': {}
        }
        
        # Find patterns in the tail
        for length in range(2, min(6, len(tail) // 2)):
            patterns = []
            for i in range(len(tail) - length + 1):
                patterns.append(tail[i:i + length])
            
            pattern_freq = Counter(patterns)
            analysis['pattern_frequency'][length] = pattern_freq.most_common(3)
            analysis['recent_patterns'].extend([p for p, c in pattern_freq.items() if c > 1])
        
        return analysis
    
    def _predict_next_group(self, sequence: str, group_size: int) -> str:
        """Predict the next group based on sequence analysis."""
        # Get recent groups
        groups = [sequence[i:i+group_size] for i in range(0, len(sequence), group_size)]
        complete_groups = [g for g in groups if len(g) == group_size]
        
        if len(complete_groups) < 2:
            # Fallback to most common pattern
            return self._get_most_common_pattern(sequence, group_size)
        
        # Try arithmetic progression
        decimals = [int(g, 16) for g in complete_groups[-3:]]
        if len(decimals) >= 2:
            diff = decimals[-1] - decimals[-2]
            next_decimal = decimals[-1] + diff
            if next_decimal > 0:
                next_hex = hex(next_decimal)[2:].upper()
                if len(next_hex) <= group_size:
                    return next_hex.zfill(group_size)
        
        # Fallback to pattern repetition
        return self._get_most_common_pattern(sequence, group_size)
    
    def _predict_next_char(self, sequence: str) -> str:
        """Predict the next single character."""
        recent_chars = sequence[-10:]  # Look at last 10 characters
        char_freq = Counter(recent_chars)
        return char_freq.most_common(1)[0][0]
    
    def _get_most_common_pattern(self, sequence: str, length: int) -> str:
        """Get the most common pattern of given length."""
        patterns = []
        for i in range(len(sequence) - length + 1):
            patterns.append(sequence[i:i + length])
        
        pattern_freq = Counter(patterns)
        if pattern_freq:
            return pattern_freq.most_common(1)[0][0]
        else:
            return 'A' * length  # Fallback
    
    def validate_extension_from_base(self, base: str, extended: str) -> Dict:
        """Validate extension from a base sequence."""
        extension = extended[len(base):]
        
        return {
            'extension': extension,
            'length': len(extension),
            'pattern_density': self._calculate_pattern_density(extension),
            'mathematical_fit': self._check_mathematical_fit(base, extended)
        }
    
    def _calculate_pattern_density(self, text: str) -> Dict:
        """Calculate density of known patterns in text."""
        density = {}
        for pattern in self.key_patterns:
            count = text.count(pattern)
            density[pattern] = count / len(text) if text else 0
        return density
    
    def _check_mathematical_fit(self, base: str, extended: str) -> float:
        """Check how well the extension fits mathematically."""
        # Simple metric: consistency of character frequency
        base_freq = Counter(base)
        extended_freq = Counter(extended)
        
        # Calculate similarity
        all_chars = set(base_freq.keys()) | set(extended_freq.keys())
        similarity = 0
        
        for char in all_chars:
            base_ratio = base_freq.get(char, 0) / len(base) if base else 0
            extended_ratio = extended_freq.get(char, 0) / len(extended) if extended else 0
            similarity += 1 - abs(base_ratio - extended_ratio)
        
        return similarity / len(all_chars) if all_chars else 0
    
    def analyze_step_patterns(self, base: str, extended: str) -> Dict:
        """Analyze patterns that emerge in each extension step."""
        extension = extended[len(base):]
        
        analysis = {
            'new_patterns': self._find_new_patterns(extension),
            'pattern_evolution': self._track_pattern_evolution(base, extended),
            'mathematical_trends': self._analyze_mathematical_trends(extended)
        }
        
        return analysis
    
    def _track_pattern_evolution(self, base: str, extended: str) -> Dict:
        """Track how patterns evolve with extension."""
        evolution = {}
        
        for pattern in self.key_patterns:
            base_count = base.count(pattern)
            extended_count = extended.count(pattern)
            
            evolution[pattern] = {
                'base_count': base_count,
                'extended_count': extended_count,
                'growth': extended_count - base_count,
                'growth_rate': (extended_count - base_count) / base_count if base_count > 0 else float('inf')
            }
        
        return evolution
    
    def _analyze_mathematical_trends(self, sequence: str) -> Dict:
        """Analyze mathematical trends in the sequence."""
        trends = {}
        
        # Analyze different group sizes
        for size in [2, 4, 6]:
            groups = [sequence[i:i+size] for i in range(0, len(sequence), size)]
            complete_groups = [g for g in groups if len(g) == size]
            
            if len(complete_groups) >= 5:
                decimals = [int(g, 16) for g in complete_groups[-5:]]
                
                # Calculate trend metrics
                diffs = [decimals[i+1] - decimals[i] for i in range(len(decimals)-1)]
                
                trends[f'size_{size}'] = {
                    'recent_values': decimals,
                    'differences': diffs,
                    'trend_direction': 'increasing' if sum(diffs) > 0 else 'decreasing',
                    'volatility': max(diffs) - min(diffs) if diffs else 0
                }
        
        return trends


def main():
    """Main extension and pattern discovery function."""
    print("🚀 HEX SEQUENCE PATTERN EXTENDER")
    print("=" * 40)
    
    # Your original hex sequence
    hex_sequence = """FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A1621984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51A49F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A4249848471A14A22415A4E5BD278514A211285F8A2154B8215258A5D814268254184624A8112132122C25944A54815A42A5A845818211943A518484A1A81B8638132E214A12845C855251A482488AD94424B846224C13818252D4D844A4D816A1618A82592461E824A124E258468122858A8D2152459188172A247582A4C8A165125C2221C8E5A49A4A552182681D8742A211A18538B841A4651258A5814432924B552A1F7A511A4141AA1A1C8481AAC51258AD165A1942C"""
    
    extender = HexSequenceExtender(hex_sequence)
    
    print(f"📊 Original sequence length: {extender.length}")
    print(f"Using validated predictions: {extender.validated_predictions}")
    
    # Progressive extension analysis
    print(f"\n🔄 PROGRESSIVE PATTERN EXTENSION")
    print("-" * 35)
    
    results = extender.progressive_extension(steps=3, step_size=20)
    
    # Analyze the results
    print(f"\n📈 EXTENSION ANALYSIS RESULTS")
    print("-" * 30)
    
    all_extensions = []
    for result in results:
        step = result['step']
        extension = result['extension']
        analysis = result['analysis']
        
        print(f"\nStep {step} Extension: {extension}")
        all_extensions.append(extension)
        
        # Show new patterns found
        new_patterns = analysis.get('new_patterns', {})
        if new_patterns:
            print(f"   New patterns discovered:")
            for length_key, patterns in new_patterns.items():
                length = length_key.split('_')[1]
                print(f"     {length}-char: {list(patterns.keys())[:3]}")
        
        # Show pattern evolution
        evolution = analysis.get('pattern_evolution', {})
        growing_patterns = [p for p, data in evolution.items() if data.get('growth', 0) > 0]
        if growing_patterns:
            print(f"   Growing patterns: {growing_patterns}")
        
        # Show mathematical trends
        trends = analysis.get('mathematical_trends', {})
        for size_key, trend_data in trends.items():
            if trend_data.get('trend_direction') == 'increasing':
                print(f"   {size_key}: {trend_data['trend_direction']} trend")
    
    # Generate the complete extended sequence
    complete_extension = ''.join(all_extensions)
    final_sequence = hex_sequence + complete_extension
    
    print(f"\n🎯 FINAL EXTENDED SEQUENCE")
    print("-" * 26)
    print(f"Original length: {len(hex_sequence)}")
    print(f"Extension length: {len(complete_extension)}")
    print(f"Final length: {len(final_sequence)}")
    print(f"\nComplete extension: {complete_extension}")
    
    # Validate the complete extension
    print(f"\n✅ FINAL VALIDATION")
    print("-" * 16)
    
    final_validation = extender.validate_extension(final_sequence)
    
    # Show pattern matches
    print("Pattern frequency changes:")
    for pattern, data in final_validation['pattern_matches'].items():
        if data['extension_count'] > 0:
            print(f"   '{pattern}': {data['original_count']} → {data['new_total']} (+{data['extension_count']})")
    
    # Show new patterns
    new_patterns = final_validation.get('new_patterns_found', {})
    if new_patterns:
        print("\nNew patterns discovered in extension:")
        for length_key, patterns in new_patterns.items():
            print(f"   {length_key}: {list(patterns.keys())[:3]}")
    
    print(f"\n🔍 NEXT PATTERN PREDICTIONS")
    print("-" * 25)
    
    # Based on the extension, predict what comes next
    next_predictions = extender._predict_next_group(final_sequence, 4)
    print(f"Next 4-character group prediction: {next_predictions}")
    
    next_char = extender._predict_next_char(final_sequence)
    print(f"Next character prediction: {next_char}")
    
    print(f"\n✨ PATTERN EXTENSION COMPLETE!")
    print("=" * 40)
    
    return final_sequence, complete_extension


if __name__ == "__main__":
    final_sequence, extension = main()
    print(f"\nFINAL RESULT:")
    print(f"Extension discovered: {extension}")
    print(f"Full sequence length: {len(final_sequence)}")

