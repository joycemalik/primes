# ----------------------------------------------------------------------------
# Prime research archive :: research/06-prime-music/prime_music_hex_v1.py
# Original location      :: learn/primemusic1.py   (last edited 2025-08-08)
# What this script does  :: First MIDI encoding of the hex string.
# ----------------------------------------------------------------------------
from midiutil import MIDIFile

def generate_music_from_hex(hex_sequence, output_filename="ghost_in_the_machine.mid"):
    """
    Translates a hexadecimal sequence into a musical MIDI file based on a
    pre-defined "Ghost in the Machine" cipher.
    
    Args:
        hex_sequence (str): The input string of hexadecimal characters.
        output_filename (str): The name of the MIDI file to create.
    """
    # --- The Musical Cipher ---

    # 1. Pitch Mapping (Hex digit -> MIDI Note Number)
    # Based on the A minor pentatonic scale across 3 octaves. '0' is a rest.
    PITCH_MAP = {
        '0': None,  # Rest
        '1': 57,    # A3
        '2': 60,    # C4
        '3': 62,    # D4
        '4': 64,    # E4
        '5': 67,    # G4
        '6': 69,    # A4
        '7': 72,    # C5
        '8': 74,    # D5
        '9': 76,    # E5
        'A': 79,    # G5
        'B': 81,    # A5
        'C': 84,    # C6
        'D': 86,    # D6
        'E': 88,    # E6
        'F': 91     # G6
    }

    # 2. Rhythm Mapping (Hex digit -> Duration in beats)
    # Even numbers are legato (full duration), odd are staccato (shorter duration).
    # A beat is equivalent to a quarter note.
    # Returns a tuple: (beat_duration, articulation_multiplier)
    RHYTHM_MAP = {
        '0': (0.25, 1.0),   # Sixteenth (Legato)
        '1': (0.25, 0.5),   # Sixteenth (Staccato)
        '2': (0.375, 1.0),  # Dotted Sixteenth (Legato)
        '3': (0.375, 0.5),  # Dotted Sixteenth (Staccato)
        '4': (0.5, 1.0),    # Eighth (Legato)
        '5': (0.5, 0.5),    # Eighth (Staccato)
        '6': (0.75, 1.0),   # Dotted Eighth (Legato)
        '7': (0.75, 0.5),   # Dotted Eighth (Staccato)
        '8': (1, 1.0),      # Quarter (Legato)
        '9': (1, 0.5),      # Quarter (Staccato)
        'A': (1.5, 1.0),    # Dotted Quarter (Legato)
        'B': (1.5, 0.5),    # Dotted Quarter (Staccato)
        'C': (2, 1.0),      # Half (Legato)
        'D': (2, 0.5),      # Half (Staccato)
        'E': (4, 1.0),      # Whole (Legato)
        'F': (4, 1.0)       # Whole (Legato - staccato makes less sense here)
    }

    # --- MIDI File Setup ---
    track    = 0
    channel  = 0
    time     = 0    # In beats
    tempo    = 140  # In BPM
    volume   = 100  # 0-127, as MIDI velocity

    # Create the MIDIFile Object with 1 track
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, tempo)
    MyMIDI.addTrackName(track, time, "Ghost in the Machine")
    
    # Set the instrument to Celesta (Program Number 8)
    # Music Box is 10, Piano is 0
    instrument = 8
    MyMIDI.addProgramChange(track, channel, time, instrument)

    # --- Process the Hex Sequence ---
    # Read the sequence two characters at a time
    for i in range(0, len(hex_sequence), 2):
        byte = hex_sequence[i:i+2]
        if len(byte) != 2:
            continue # Skip if there's a leftover character

        pitch_char = byte[0].upper()
        rhythm_char = byte[1].upper()

        # Look up the note properties from our cipher maps
        midi_pitch = PITCH_MAP.get(pitch_char)
        beat_duration, articulation = RHYTHM_MAP.get(rhythm_char, (0.25, 1.0)) # Default to 16th

        # If it's not a rest, add the note to the track
        if midi_pitch is not None:
            # The actual sounding duration is modified by the articulation
            sounding_duration = beat_duration * articulation
            MyMIDI.addNote(track, channel, midi_pitch, time, sounding_duration, volume)

        # Advance the time cursor by the note's full rhythmic value
        # This ensures rests and staccato notes maintain correct timing
        time += beat_duration

    # --- Save the MIDI file ---
    try:
        with open(output_filename, "wb") as output_file:
            MyMIDI.writeFile(output_file)
        print(f"✅ Success! Music file saved as '{output_filename}'")
    except Exception as e:
        print(f"❌ Error saving file: {e}")


if __name__ == "__main__":
    # The original hexadecimal sequence
    GHOST_SEQUENCE = "FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A1621984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51A49F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A4249848471A14A22415A4E5BD278514A211285F8A2154B8215258A5D814268254184624A8112132122C25944A54815A42A5A845818211943A518484A1A81B8638132E214A12845C855251A482488AD94424B846224C13818252D4D844A4D816A1618A82592461E824A124E258468122858A8D2152459188172A247582A4C8A165125C2221C8E5A49A4A552182681D8742A211A18538B841A4651258A5814432924B552A1F7A511A4141AA1A1C8481AAC51258AD165A1942C"
    
    # Generate the music!
    generate_music_from_hex(GHOST_SEQUENCE)