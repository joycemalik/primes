#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v71_radial_spiral_sonified_midi.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v71.py   (last edited 2025-08-24)
# What this script does  :: Radial spiral frames plus a MIDI sonification.
# ----------------------------------------------------------------------------
"""
Generates a sequence of radial plot images (PNG) and corresponding
sonified audio data (MIDI) for creating an animated music video.
"""

import matplotlib.pyplot as plt
import sympy
import numpy as np
import os
import re
from midiutil import MIDIFile

# --- HELPER FUNCTION FOR SCALING DATA ---
def scale_value(value, min_val, max_val, new_min, new_max):
    """Scales a value from one range to another, handling division by zero."""
    if max_val == min_val:
        return (new_min + new_max) / 2
    return (((value - min_val) * (new_max - new_min)) / (max_val - min_val)) + new_min

# --- SONIFICATION FUNCTION ---
def sonify_data_to_midi(output_path, indices, function_values, theta):
    """
    Generates a MIDI file from the spiral's data.
    - Pitch is mapped from the function's value.
    - Panning (stereo left/right) is mapped from the angle (theta).
    """
    try:
        # 1. MIDI Setup
        track = 0
        channel = 0
        time = 0    # In beats
        duration = 0.25 # Each note is a 16th note
        tempo = 140   # Beats per minute
        volume = 110  # 0-127, as MIDI velocity

        midi_file = MIDIFile(1) # One track
        midi_file.addTempo(track, time, tempo)

        # 2. Determine data ranges for scaling
        min_func_val = np.min(function_values)
        max_func_val = np.max(function_values)

        # 3. Loop through data and create notes
        for i in range(len(indices)):
            # Map function value to a musical pitch (MIDI notes 36-96: C2 to C7)
            pitch = int(scale_value(function_values[i], min_func_val, max_func_val, 36, 96))
            
            # Map angle to stereo pan (0=left, 64=center, 127=right)
            pan_value = int(scale_value(theta[i] % (2 * np.pi), 0, 2 * np.pi, 0, 127))

            # Add the note and its panning position to the MIDI file
            midi_file.addNote(track, channel, pitch, time, duration, volume)
            midi_file.addControllerEvent(track, channel, time, 10, pan_value) # Controller 10 is Pan
            
            time += duration # Move to the next note's start time

        # 4. Save the MIDI file
        with open(output_path, "wb") as f:
            midi_file.writeFile(f)
        print(f"   -> 🎼 Sonified MIDI saved.")

    except Exception as e:
        print(f"   -> ❌ Error creating MIDI file. (Reason: {e})")

# --- PLOTTING AND SONIFICATION FUNCTION ---
def plot_and_sonify(func_str, limit, output_folder_images, output_folder_midi, frame_number):
    """
    Creates and saves a static radial plot and a corresponding MIDI file for one frame.
    """
    print(f"Processing Frame {frame_number}: y = {func_str}")
    
    # 1. Parse the function string
    try:
        x_sym = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        func = sympy.lambdify(x_sym, expr, 'numpy')
    except Exception as e:
        print(f"   -> ❌ Error parsing function. Skipping. (Reason: {e})")
        return

    # 2. Generate prime data
    try:
        primes = np.array(list(sympy.primerange(2, limit + 1)))
        if len(primes) == 0:
            print("   -> ❌ No primes found in the given limit. Skipping.")
            return
        indices = np.arange(len(primes))
        function_values = func(primes)
    except Exception as e:
        print(f"   -> ❌ Error evaluating function. Skipping. (Reason: {e})")
        return
        
    # 3. Create the polar plot structure
    fig = plt.figure(figsize=(12, 12), dpi=150)
    ax = fig.add_subplot(111, projection='polar')
    ax.set_facecolor('black')
    ax.grid(color='#2A2A2A', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # 4. Plot the data
    theta = indices * (np.pi / 8) # Spreading the angle for visual clarity
    r = function_values
    ax.plot(theta, r, color='cyan', linestyle='-', linewidth=1.5)
    ax.scatter(theta, r, color='cyan', s=15, zorder=10) # Add points on top
    ax.set_title(f'Function Spiral for y = {func_str}', color='white', pad=20, fontsize=16)

    # 5. Save the image file
    # Use a zero-padded filename for correct sorting (e.g., frame_001.png, frame_002.png)
    img_filename = f"frame_{frame_number:04d}.png"
    img_output_path = os.path.join(output_folder_images, img_filename)
    plt.savefig(img_output_path, bbox_inches='tight', facecolor='black')
    print(f"   -> ✅ Radial plot saved.")
    plt.close(fig)
    
    # 6. Sonify the data to a MIDI file
    midi_filename = f"frame_{frame_number:04d}.mid"
    midi_output_path = os.path.join(output_folder_midi, midi_filename)
    sonify_data_to_midi(midi_output_path, indices, function_values, theta)

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    # --- Animation Settings ---
    OUTPUT_FOLDER_IMAGES = 'generated_images'
    OUTPUT_FOLDER_MIDI = 'generated_midi'
    START_FRAME = 2
    END_FRAME = 400
    PRIME_LIMIT = 1000 # Upper limit for primes used in each frame's calculation

    # Create output directories if they don't exist
    os.makedirs(OUTPUT_FOLDER_IMAGES, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER_MIDI, exist_ok=True)
    
    print("--- 🌀✨ Starting Audio-Visual Frame Generation ✨🌀 ---")
    
    # Loop to generate each frame of the animation
    for n in range(START_FRAME, END_FRAME + 1):
        function_string = f"x % {n}"
        plot_and_sonify(
            func_str=function_string,
            limit=PRIME_LIMIT,
            output_folder_images=OUTPUT_FOLDER_IMAGES,
            output_folder_midi=OUTPUT_FOLDER_MIDI,
            frame_number=n
        )
    
    print("\n✨ Batch process complete! You are ready for the next steps. ✨")