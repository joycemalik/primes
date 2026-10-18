# ----------------------------------------------------------------------------
# Prime research archive :: research/06-prime-music/prime_music_advanced.py
# Original location      :: learn/prime_music_advanced.py   (last edited 2025-08-08)
# What this script does  :: Hex-encoded prime symphony and chord progressions.
# ----------------------------------------------------------------------------
"""
Advanced Prime Music: Hex Encoding with Musical Intelligence
===========================================================

This approach uses the hex encoding from our prime analysis but maps it
to musically meaningful structures like scales, chord progressions,
and harmonic series rather than arbitrary mappings.
"""

from midiutil import MIDIFile
import json

def generate_advanced_prime_music(hex_sequence, filename="prime_hex_symphony.mid"):
    """
    Advanced musical encoding that treats hex digits as musical elements:
    - Hex values 0-F mapped to chromatic scale
    - Patterns in hex create chord progressions
    - Frequency analysis drives rhythm and dynamics
    - Multiple voices for harmonic richness
    """
    
    # Musical setup
    tempo = 120
    volume_base = 80
    
    # Create MIDI file with 4 tracks
    midi = MIDIFile(4)
    
    # Track 0: Melody (hex sequence as chromatic melody)
    # Track 1: Bass (root movements based on hex patterns)  
    # Track 2: Harmony (chords from hex digit combinations)
    # Track 3: Percussion (rhythm from hex frequency patterns)
    
    # Set up tracks
    for track in range(4):
        midi.addTempo(track, 0, tempo)
    
    midi.addTrackName(0, 0, "Prime Melody")
    midi.addTrackName(1, 0, "Prime Bass") 
    midi.addTrackName(2, 0, "Prime Harmony")
    midi.addTrackName(3, 0, "Prime Rhythm")
    
    # Instruments
    midi.addProgramChange(0, 0, 0, 73)  # Flute for melody
    midi.addProgramChange(1, 1, 0, 32)  # Electric Bass
    midi.addProgramChange(2, 2, 0, 4)   # Electric Piano for chords
    midi.addProgramChange(3, 9, 0, 1)   # Standard kit for drums
    
    # Musical mappings
    HEX_TO_CHROMATIC = {
        '0': 60, '1': 61, '2': 62, '3': 63,  # C C# D D#
        '4': 64, '5': 65, '6': 66, '7': 67,  # E F F# G  
        '8': 68, '9': 69, 'A': 70, 'B': 71,  # G# A A# B
        'C': 72, 'D': 73, 'E': 74, 'F': 75   # C5 C#5 D5 D#5
    }
    
    # Chord types based on hex patterns
    CHORD_TYPES = {
        'major': [0, 4, 7],
        'minor': [0, 3, 7], 
        'dim': [0, 3, 6],
        'aug': [0, 4, 8],
        'sus2': [0, 2, 7],
        'sus4': [0, 5, 7]
    }
    
    # Drum mapping for rhythm track
    DRUMS = {
        'kick': 36, 'snare': 38, 'hihat': 42, 
        'openhat': 46, 'crash': 49, 'ride': 51
    }
    
    time = 0
    beat_duration = 0.5  # Half note base duration
    
    # Process hex sequence in groups of 4 (measures)
    for i in range(0, min(len(hex_sequence), 200), 4):  # Limit for reasonable length
        measure = hex_sequence[i:i+4].ljust(4, '0')  # Pad if needed
        
        # --- TRACK 0: MELODY ---
        for j, hex_char in enumerate(measure):
            note = HEX_TO_CHROMATIC[hex_char.upper()]
            duration = beat_duration
            
            # Add musical phrasing - longer notes on strong beats
            if j % 2 == 0:
                duration *= 1.5
            
            midi.addNote(0, 0, note, time + j * beat_duration, duration, volume_base)
        
        # --- TRACK 1: BASS ---
        # Root note based on first hex digit of measure
        root_hex = measure[0].upper()
        root_note = HEX_TO_CHROMATIC[root_hex] - 24  # Two octaves lower
        
        # Bass pattern: root on beats 1 and 3
        midi.addNote(1, 1, root_note, time, beat_duration, volume_base + 10)
        midi.addNote(1, 1, root_note, time + 2 * beat_duration, beat_duration, volume_base + 10)
        
        # --- TRACK 2: HARMONY ---
        # Determine chord type from hex pattern
        hex_sum = sum(int(c, 16) for c in measure if c.upper() in '0123456789ABCDEF')
        chord_types = list(CHORD_TYPES.keys())
        chord_type = chord_types[hex_sum % len(chord_types)]
        
        chord_root = HEX_TO_CHROMATIC[measure[0].upper()]
        chord_notes = [chord_root + interval for interval in CHORD_TYPES[chord_type]]
        
        # Play chord on beats 2 and 4
        for note in chord_notes:
            midi.addNote(2, 2, note, time + beat_duration, beat_duration * 1.5, volume_base - 10)
            midi.addNote(2, 2, note, time + 3 * beat_duration, beat_duration * 1.5, volume_base - 10)
        
        # --- TRACK 3: RHYTHM ---
        # Create rhythm pattern from hex frequency
        for j, hex_char in enumerate(measure):
            hex_val = int(hex_char.upper(), 16) if hex_char.upper() in '0123456789ABCDEF' else 0
            
            # Different drums for different hex value ranges
            if hex_val < 4:
                drum = DRUMS['kick']
            elif hex_val < 8:
                drum = DRUMS['snare'] 
            elif hex_val < 12:
                drum = DRUMS['hihat']
            else:
                drum = DRUMS['ride']
            
            # Rhythm: kick on 1 and 3, others fill in
            if j % 2 == 0 or hex_val > 8:
                midi.addNote(3, 9, drum, time + j * beat_duration, beat_duration * 0.25, volume_base - 20)
        
        time += 4 * beat_duration  # Move to next measure
    
    # Save the file
    with open(filename, "wb") as f:
        midi.writeFile(f)
    
    print(f"✅ Advanced Prime Symphony saved as {filename}")
    
    # Analysis
    hex_freq = {}
    for char in hex_sequence.upper():
        if char in '0123456789ABCDEF':
            hex_freq[char] = hex_freq.get(char, 0) + 1
    
    print("\n🎼 Musical Analysis:")
    print(f"   Hex sequence length: {len(hex_sequence)}")
    print(f"   Measures created: {min(len(hex_sequence), 200) // 4}")
    print(f"   Most frequent hex: {max(hex_freq.items(), key=lambda x: x[1])}")
    print(f"   Musical key center: {list(HEX_TO_CHROMATIC.keys())[list(HEX_TO_CHROMATIC.values()).index(60)]} (C)")

def generate_prime_chord_progression(hex_sequence, filename="prime_chords.mid"):
    """
    Creates a chord progression where each hex digit maps to a chord degree
    in multiple keys, creating interesting harmonic movements.
    """
    tempo = 100
    volume = 75
    
    midi = MIDIFile(1)
    midi.addTempo(0, 0, tempo)
    midi.addTrackName(0, 0, "Prime Chord Progression")
    midi.addProgramChange(0, 0, 0, 0)  # Acoustic Grand Piano
    
    # Key centers (major scales)
    KEYS = {
        'C': [60, 62, 64, 65, 67, 69, 71],  # C major
        'G': [67, 69, 71, 72, 74, 76, 78],  # G major  
        'F': [65, 67, 69, 70, 72, 74, 76],  # F major
        'Am': [69, 71, 72, 74, 76, 77, 79], # A minor
    }
    
    # Hex to scale degree mapping
    HEX_TO_DEGREE = {
        '0': 0, '1': 0, '2': 1, '3': 1,  # I and ii
        '4': 2, '5': 2, '6': 3, '7': 3,  # iii and IV
        '8': 4, '9': 4, 'A': 5, 'B': 5,  # V and vi
        'C': 6, 'D': 6, 'E': 0, 'F': 0   # vii and back to I
    }
    
    time = 0
    chord_duration = 2.0
    current_key = 'C'
    
    # Process hex in pairs for chord changes
    for i in range(0, min(len(hex_sequence), 100), 2):
        hex_pair = hex_sequence[i:i+2].upper()
        
        if len(hex_pair) == 2:
            # First hex determines chord degree
            degree = HEX_TO_DEGREE.get(hex_pair[0], 0)
            
            # Second hex might change key
            if hex_pair[1] in 'CF':
                current_key = 'C'
            elif hex_pair[1] in '58':
                current_key = 'G' 
            elif hex_pair[1] in '47':
                current_key = 'F'
            elif hex_pair[1] in 'AE':
                current_key = 'Am'
            
            # Build triad
            scale = KEYS[current_key]
            root = scale[degree]
            third = scale[(degree + 2) % 7]
            fifth = scale[(degree + 4) % 7]
            
            # Play chord
            for note in [root, third, fifth]:
                midi.addNote(0, 0, note, time, chord_duration, volume)
            
            time += chord_duration
    
    with open(filename, "wb") as f:
        midi.writeFile(f)
    
    print(f"✅ Prime Chord Progression saved as {filename}")

def main():
    """Generate advanced prime music from our hex sequence"""
    print("🎼 ADVANCED PRIME MUSIC GENERATION")
    print("=" * 50)
    
    # Use the hex sequence from our prime analysis
    PRIME_HEX = "FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A162984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51AA9F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A424984847"
    
    print(f"Using prime hex sequence ({len(PRIME_HEX)} characters)")
    print(f"First 50 chars: {PRIME_HEX[:50]}...")
    print()
    
    # Generate advanced musical interpretations
    generate_advanced_prime_music(PRIME_HEX)
    generate_prime_chord_progression(PRIME_HEX)
    
    print()
    print("🎵 Advanced prime music complete!")
    print("Created:")
    print("• prime_hex_symphony.mid - 4-track orchestral arrangement")
    print("• prime_chords.mid - harmonic progression based on hex patterns")
    print()
    print("These use musically intelligent mappings that reflect the")
    print("mathematical structure of primes rather than arbitrary assignments!")

if __name__ == "__main__":
    main()
