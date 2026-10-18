# ----------------------------------------------------------------------------
# Prime research archive :: research/06-prime-music/prime_music_nexus_decoder.py
# Original location      :: learn/primemusic2.py   (last edited 2025-08-08)
# What this script does  :: Multi-track "Nexus decoder" MIDI from the ghost hex sequence.
# ----------------------------------------------------------------------------
from midiutil import MIDIFile

# This script is a MIDI interpretation of the "Nexus Decoder" concept.
# It uses multiple MIDI tracks and parameters to simulate the behavior of a
# complex synthesizer, controlled by the input hexadecimal data.

def generate_nexus_midi(hex_sequence, output_filename="nexus_decoded_music.mid"):
    """
    Generates a multi-track MIDI file by interpreting a hex string as control
    data for a virtual modular synthesizer.

    Args:
        hex_sequence (str): The input string of hexadecimal characters.
        output_filename (str): The name of the MIDI file to create.
    """
    # --- DECODER MAPPING TABLES ---

    # Byte 1 -> Pitch (C Minor Scale)
    PITCH_MAP = {
        '0': 59, '1': 60, '2': 62, '3': 63, '4': 65, '5': 67, '6': 68, '7': 70,
        '8': 72, '9': 74, 'A': 75, 'B': 77, 'C': 79, 'D': 80, 'E': 82, 'F': 84
    }

    # Byte 1 -> Waveform (Simulated by changing MIDI synth instrument)
    # See General MIDI specification for instrument numbers.
    WAVEFORM_INSTRUMENT_MAP = {
        '0': 80, '1': 80, '2': 80, '3': 80, # 0-3: Square Lead
        '4': 81, '5': 81, '6': 81, '7': 81, # 4-7: Saw Lead
        '8': 84, '9': 84, 'A': 84, 'B': 84, # 8-B: Charang (Plucky)
        'C': 88, 'D': 88, 'E': 88, 'F': 88  # C-F: New Age Pad (Softer)
    }

    # Byte 2 -> Rhythm Pattern (Simulated by number of subdivisions)
    RHYTHM_PATTERN_MAP = {'0': 1, '1': 1, '2': 2, '3': 2, '4': 3, '5': 3, '6': 4, '7': 4,
                          '8': 6, '9': 6, 'A': 8, 'B': 8, 'C': 12, 'D': 12, 'E': 16, 'F': 16}


    # --- MIDI SETUP ---
    num_tracks = 3
    MyMIDI = MIDIFile(num_tracks)

    # Track 0: Lead Synth
    # Track 1: Bass Synth
    # Track 2: Rhythm/Arpeggiator
    
    tempo = 130
    time = 0
    
    # Initialize Tracks
    for i in range(num_tracks):
        MyMIDI.addTempo(i, time, tempo)

    MyMIDI.addTrackName(0, time, "Lead Synth")
    MyMIDI.addProgramChange(0, 0, time, 81) # Start with Saw Lead

    MyMIDI.addTrackName(1, time, "Bass Synth")
    MyMIDI.addProgramChange(1, 1, time, 38) # Synth Bass 1

    MyMIDI.addTrackName(2, time, "Rhythm")
    MyMIDI.addProgramChange(2, 2, time, 99) # Crystal FX (Percussive)


    # --- MAIN PROCESSING LOOP ---
    last_instrument = 81
    
    # Process data in 4-byte "packets"
    for i in range(0, len(hex_sequence), 8):
        packet = hex_sequence[i:i+8]
        if len(packet) != 8:
            continue

        b1, b2, b3, b4 = packet[0:2], packet[2:4], packet[4:6], packet[6:8]

        # --- Decode Packet into Synth Parameters ---

        # Byte 1: Pitch & Waveform
        pitch_char = b1[0].upper()
        wave_char = b1[1].upper()
        midi_note = PITCH_MAP.get(pitch_char, 60) # Default to C4 if not found
        bass_note = midi_note - 24 # 2 octaves lower
        lead_instrument = WAVEFORM_INSTRUMENT_MAP.get(wave_char, 81)

        # Byte 2: Rhythm & Gate
        rhythm_char = b2[0].upper()
        gate_char = b2[1].upper()
        subdivisions = RHYTHM_PATTERN_MAP.get(rhythm_char, 1)
        # Gate duration determines how long this whole event lasts
        gate_duration_beats = 0.5 + (int(gate_char, 16) / 15) * 3.5 # Range from 0.5 to 4 beats

        # Byte 3: Filter -> Note Velocity
        filter_char = b3[0].upper()
        # Low filter = quiet/muffled, High filter = loud/bright
        velocity = int(40 + (int(filter_char, 16) / 15) * 87) # Range from 40 to 127

        # Byte 4: Effects -> Note Duration
        reverb_char = b4[1].upper()
        # Low reverb = short note, High reverb = long, sustained note
        duration_multiplier = 0.1 + (int(reverb_char, 16) / 15) * 0.9 # Range from 10% to 100%
        note_duration = gate_duration_beats * duration_multiplier

        # --- Add Notes to MIDI Tracks ---
        
        # Change lead instrument if data dictates
        if lead_instrument != last_instrument:
            MyMIDI.addProgramChange(0, 0, time, lead_instrument)
            last_instrument = lead_instrument
        
        # 1. Add Lead Note
        MyMIDI.addNote(track=0, channel=0, pitch=midi_note, time=time, duration=note_duration, volume=velocity)
        
        # 2. Add Bass Note
        MyMIDI.addNote(track=1, channel=1, pitch=bass_note, time=time, duration=note_duration, volume=int(velocity*0.8)) # Bass is a bit quieter
        
        # 3. Add Rhythm Notes
        if subdivisions > 1:
            rhythm_note_duration = gate_duration_beats / subdivisions
            for step in range(subdivisions):
                rhythm_time = time + step * rhythm_note_duration
                # Alternate between two notes for more interest
                rhythm_pitch = 60 if step % 2 == 0 else 63
                MyMIDI.addNote(track=2, channel=2, pitch=rhythm_pitch, time=rhythm_time, duration=rhythm_note_duration * 0.5, volume=70)

        # Advance the master time cursor
        time += gate_duration_beats

    # --- SAVE THE MIDI FILE ---
    try:
        with open(output_filename, "wb") as output_file:
            MyMIDI.writeFile(output_file)
        print(f"✅ Success! Generative music file saved as '{output_filename}'")
        print("   Play it with a media player or import it into a DAW to explore the tracks.")
    except Exception as e:
        print(f"❌ Error saving file: {e}")


if __name__ == "__main__":
    GHOST_SEQUENCE = "FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A1621984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51A49F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A4249848471A14A22415A4E5BD278514A211285F8A2154B8215258A5D814268254184624A8112132122C25944A54815A42A5A845818211943A518484A1A81B8638132E214A12845C855251A482488AD94424B846224C13818252D4D844A4D816A1618A82592461E824A124E258468122858A8D2152459188172A247582A4C8A165125C2221C8E5A49A4A552182681D8742A211A18538B841A4651258A5814432924B552A1F7A511A4141AA1A1C8481AAC51258AD165A1942C"
    
    generate_nexus_midi(GHOST_SEQUENCE)