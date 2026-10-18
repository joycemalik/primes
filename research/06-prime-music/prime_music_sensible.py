# ----------------------------------------------------------------------------
# Prime research archive :: research/06-prime-music/prime_music_sensible.py
# Original location      :: learn/prime_music_sensible.py   (last edited 2025-08-08)
# What this script does  :: Five MIDI encodings: gap intervals, digit rhythms, factor chords, golden spiral, interference.
# ----------------------------------------------------------------------------
"""
Sensible Musical Encoding of Prime Numbers
==========================================

Multiple approaches to convert prime sequences into meaningful music that reflects
the mathematical properties of primes rather than arbitrary hex mappings.
"""

from midiutil import MIDIFile
import math

def is_prime(n):
    """Check if a number is prime"""
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

def get_primes(start, count):
    """Get 'count' primes starting from 'start'"""
    primes = []
    n = start
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def approach1_prime_intervals(primes, filename="prime_intervals.mid"):
    """
    Approach 1: Prime Gaps as Musical Intervals
    The gaps between consecutive primes become musical intervals.
    Smaller gaps = closer harmonies, larger gaps = wider leaps.
    """
    track = 0
    channel = 0
    time = 0
    tempo = 120
    volume = 80
    
    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)
    midi.addTrackName(track, time, "Prime Intervals")
    midi.addProgramChange(track, channel, time, 0)  # Piano
    
    # Start with middle C
    base_note = 60
    current_note = base_note
    
    for i in range(len(primes) - 1):
        gap = primes[i + 1] - primes[i]
        
        # Map gap to musical interval (1-12 semitones)
        interval = min(gap, 12)
        current_note += interval
        
        # Keep notes in a reasonable range
        if current_note > 84:  # C6
            current_note = base_note + (current_note - base_note) % 24
        elif current_note < 36:  # C2
            current_note = base_note + (current_note - base_note) % 24
        
        # Duration based on prime size (larger primes = longer notes)
        duration = 0.5 + (primes[i] % 8) * 0.125  # 0.5 to 1.375 beats
        
        midi.addNote(track, channel, current_note, time, duration, volume)
        time += duration
    
    with open(filename, "wb") as f:
        midi.writeFile(f)
    print(f"✅ Prime Intervals saved as {filename}")

def approach2_prime_rhythms(primes, filename="prime_rhythms.mid"):
    """
    Approach 2: Prime Digits as Rhythm Patterns
    Each digit of a prime becomes a rhythmic element.
    Creates polyrhythmic patterns based on prime structure.
    """
    track = 0
    channel = 0
    time = 0
    tempo = 140
    volume = 90
    
    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)
    midi.addTrackName(track, time, "Prime Rhythms")
    midi.addProgramChange(track, channel, time, 9)  # Percussion
    
    # Different drums for different digits
    DIGIT_DRUMS = {
        1: 36,  # Bass drum
        2: 38,  # Snare
        3: 42,  # Hi-hat closed
        4: 46,  # Hi-hat open
        5: 49,  # Crash cymbal
        6: 51,  # Ride cymbal
        7: 56,  # Cowbell
        8: 60,  # High bongo
        9: 62,  # Mute high conga
        0: 64   # Low conga
    }
    
    beat_duration = 0.25  # Sixteenth notes
    
    for prime in primes[:50]:  # Limit to first 50 primes
        digits = [int(d) for d in str(prime)]
        
        for digit in digits:
            drum = DIGIT_DRUMS[digit]
            midi.addNote(track, 9, drum, time, beat_duration, volume)  # Channel 9 for drums
            time += beat_duration
        
        # Add a small pause between primes
        time += 0.25
    
    with open(filename, "wb") as f:
        midi.writeFile(f)
    print(f"✅ Prime Rhythms saved as {filename}")

def approach3_prime_harmony(primes, filename="prime_harmony.mid"):
    """
    Approach 3: Prime Factorization as Harmony
    For composite numbers between primes, use their prime factors as chords.
    Primes themselves are single notes. Creates a harmonic progression.
    """
    track = 0
    channel = 0
    time = 0
    tempo = 100
    volume = 70
    
    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)
    midi.addTrackName(track, time, "Prime Harmony")
    midi.addProgramChange(track, channel, time, 4)  # Electric Piano
    
    # Map primes to notes in C major scale
    SCALE_NOTES = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]
    
    def prime_factors(n):
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
    
    for i, prime in enumerate(primes[:20]):  # First 20 primes
        note = SCALE_NOTES[i % len(SCALE_NOTES)]
        duration = 1.0
        
        if is_prime(prime):
            # Prime: single note
            midi.addNote(track, channel, note, time, duration, volume)
        else:
            # Composite: chord based on factors
            factors = prime_factors(prime)
            for j, factor in enumerate(factors):
                factor_note = note + (factor % 12)
                midi.addNote(track, channel, factor_note, time, duration, volume - j * 10)
        
        time += duration
    
    with open(filename, "wb") as f:
        midi.writeFile(f)
    print(f"✅ Prime Harmony saved as {filename}")

def approach4_prime_golden_ratio(primes, filename="prime_golden_spiral.mid"):
    """
    Approach 4: Prime Distribution and Golden Ratio
    Use the golden ratio to create musical spirals based on prime distribution.
    Maps prime density to pitch and rhythm in a fibonacci-like progression.
    """
    track = 0
    channel = 0
    time = 0
    tempo = 110
    volume = 85
    
    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)
    midi.addTrackName(track, time, "Prime Golden Spiral")
    midi.addProgramChange(track, channel, time, 68)  # Oboe
    
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    
    # Fibonacci sequence for rhythms
    fib = [1, 1]
    for _ in range(10):
        fib.append(fib[-1] + fib[-2])
    
    base_note = 60
    
    for i, prime in enumerate(primes[:30]):
        # Use golden ratio to determine pitch spiral
        spiral_factor = (prime * phi) % 24
        note = base_note + int(spiral_factor)
        
        # Use fibonacci sequence for rhythm
        fib_index = i % len(fib)
        duration = fib[fib_index] * 0.125  # Scale to reasonable duration
        
        # Add some harmonics based on prime properties
        if prime % 4 == 1:
            # Add perfect fifth
            midi.addNote(track, channel, note + 7, time, duration, volume - 20)
        elif prime % 4 == 3:
            # Add perfect fourth
            midi.addNote(track, channel, note + 5, time, duration, volume - 20)
        
        midi.addNote(track, channel, note, time, duration, volume)
        time += duration
    
    with open(filename, "wb") as f:
        midi.writeFile(f)
    print(f"✅ Prime Golden Spiral saved as {filename}")

def approach5_prime_wave_interference(primes, filename="prime_wave_interference.mid"):
    """
    Approach 5: Prime Frequencies as Wave Interference
    Convert primes to frequencies and create interference patterns as melody.
    Based on wave physics and harmonic series.
    """
    track = 0
    channel = 0
    time = 0
    tempo = 90
    volume = 75
    
    midi = MIDIFile(2)  # Two tracks for interference
    midi.addTempo(track, time, tempo)
    midi.addTrackName(0, time, "Prime Wave A")
    midi.addTrackName(1, time, "Prime Wave B")
    midi.addProgramChange(0, 0, time, 73)  # Flute
    midi.addProgramChange(1, 1, time, 74)  # Recorder
    
    base_freq = 440  # A4
    
    for i in range(0, len(primes) - 1, 2):
        # Create interference between consecutive prime pairs
        prime1 = primes[i]
        prime2 = primes[i + 1] if i + 1 < len(primes) else primes[i]
        
        # Convert primes to frequencies
        freq1 = base_freq * (prime1 % 16) / 8
        freq2 = base_freq * (prime2 % 16) / 8
        
        # Convert frequencies to MIDI notes
        note1 = 69 + 12 * math.log2(freq1 / 440)
        note2 = 69 + 12 * math.log2(freq2 / 440)
        
        note1 = max(36, min(84, int(note1)))
        note2 = max(36, min(84, int(note2)))
        
        duration = 0.75
        
        # Add notes to different tracks for stereo effect
        midi.addNote(0, 0, note1, time, duration, volume)
        midi.addNote(1, 1, note2, time, duration, volume)
        
        time += duration * 0.75  # Overlap for interference
    
    with open(filename, "wb") as f:
        midi.writeFile(f)
    print(f"✅ Prime Wave Interference saved as {filename}")

def main():
    """Generate all musical approaches"""
    print("🎵 GENERATING SENSIBLE PRIME MUSIC")
    print("=" * 50)
    
    # Get first 100 primes starting from 11
    primes = get_primes(11, 100)
    print(f"Using {len(primes)} primes: {primes[:10]}...")
    print()
    
    # Generate all approaches
    approach1_prime_intervals(primes)
    approach2_prime_rhythms(primes)
    approach3_prime_harmony(primes)
    approach4_prime_golden_ratio(primes)
    approach5_prime_wave_interference(primes)
    
    print()
    print("🎼 All music files generated!")
    print("Each approach represents a different mathematical aspect of primes:")
    print("1. Prime Intervals: Gaps between primes as melodic intervals")
    print("2. Prime Rhythms: Prime digits as percussion patterns")
    print("3. Prime Harmony: Factorization as harmonic progressions") 
    print("4. Golden Spiral: Prime distribution with phi ratios")
    print("5. Wave Interference: Prime frequencies as wave physics")

if __name__ == "__main__":
    main()
