# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v73_spiral_animation_with_sound.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/v73.py   (last edited 2025-08-24)
# What this script does  :: Spiral animation with sound, one prime per frame.
# ----------------------------------------------------------------------------
import os
import re
import ast
import shutil
import numpy as np
import sympy
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.generators import Sine
from moviepy.editor import ImageSequenceClip, AudioFileClip

# --- Configuration ---
NOTE_DURATION_MS = 120  # Duration of each sound/frame in milliseconds
MIN_FREQ = 220.0        # A3 note - The lowest pitch
MAX_FREQ = 880.0        # A5 note - The highest pitch
FPS = 1000 / NOTE_DURATION_MS # Frames per second for the video

# --- Helper Functions ---
def sanitize_filename(text, extension):
    """Converts a string into a valid filename with a given extension."""
    s = text.replace('**', '_pow_').replace('*', '_mul_').replace('/', '_div_')
    s = re.sub(r'[^a-zA-Z0-9_\-]', '', s)
    return s[:100] + extension

def normalize(value, min_val, max_val, new_min, new_max):
    """Linearly scales a value from one range to another."""
    if max_val == min_val:
        return new_min
    return (value - min_val) / (max_val - min_val) * (new_max - new_min) + new_min

# --- Core Logic ---
def create_sonified_animation(func_str, limit, plot_type, output_folder):
    """
    Generates a sonified video animation for a given mathematical function.
    """
    print(f"🎬 Processing '{func_str}' for a '{plot_type}' animation...")

    # --- 1. Setup Paths & Folders ---
    base_filename = f"Sonified_{plot_type}_{func_str}"
    video_filename = sanitize_filename(base_filename, '.mp4')
    audio_filename = sanitize_filename(base_filename, '.wav')
    output_path = os.path.join(output_folder, video_filename)
    temp_audio_path = os.path.join(output_folder, audio_filename)
    frames_folder = os.path.join(output_folder, 'temp_frames')

    if os.path.exists(frames_folder):
        shutil.rmtree(frames_folder)
    os.makedirs(frames_folder, exist_ok=True)

    # --- 2. Generate Prime & Function Data ---
    try:
        x_sym = sympy.symbols('x')
        expr = sympy.sympify(func_str)
        func = sympy.lambdify(x_sym, expr, 'numpy')
        primes = np.array(list(sympy.primerange(2, limit + 1)))
        indices = np.arange(len(primes))
        function_values = func(primes)
        # Handle potential complex numbers or NaNs
        function_values = np.nan_to_num(np.real(function_values))
    except Exception as e:
        print(f"   -> ❌ Error generating data for '{func_str}'. Skipping. (Reason: {e})")
        shutil.rmtree(frames_folder)
        return

    min_f_val, max_f_val = np.min(function_values), np.max(function_values)
    print(f"   -> Data range for sonification: [{min_f_val:.2f}, {max_f_val:.2f}]")
    
    # --- 3. Generate Sonification Track ---
    print("   -> 🎵 Generating audio track...")
    full_audio = AudioSegment.silent(duration=0)
    for val in function_values:
        freq = normalize(val, min_f_val, max_f_val, MIN_FREQ, MAX_FREQ)
        # Create a sine wave tone with a fade out to sound like a 'ping'
        tone = Sine(freq).to_audio_segment(duration=NOTE_DURATION_MS).fade_out(30)
        full_audio += tone
    full_audio.export(temp_audio_path, format="wav")

    # --- 4. Generate Animation Frames ---
    print(f"   -> 🖼️ Generating {len(primes)} animation frames (this may take a while)...")
    
    # Pre-calculate theta and r values for efficiency
    if plot_type == 'function_spiral':
        theta = indices * (np.pi / 8)
        r = function_values
    elif plot_type == 'distribution_spiral':
        golden_angle = np.pi * (3. - np.sqrt(5.))
        theta = indices * golden_angle
        r = primes

    for i in range(1, len(primes) + 1):
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='polar')
        ax.set_facecolor('black')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.grid(color='#2A2A2A', linestyle='--', linewidth=0.5)

        # Plot based on type
        if plot_type == 'function_spiral':
            ax.set_title(f'Function Spiral: y = {func_str}\nPrime {i}/{len(primes)}: p = {primes[i-1]}', color='white', pad=20)
            # Past points (faded)
            ax.plot(theta[:i-1], r[:i-1], color='cyan', marker='o', markersize=3, linestyle='-', alpha=0.3)
            # Current point (highlighted)
            ax.plot(theta[i-1], r[i-1], color='yellow', marker='o', markersize=8, linestyle='none')
            
        elif plot_type == 'distribution_spiral':
            ax.set_title(f'Prime Distribution Spiral: y = {func_str}\nPrime {i}/{len(primes)}: p = {primes[i-1]}', color='white', pad=20)
            colors = function_values
            # Past points (faded)
            ax.scatter(theta[:i-1], r[:i-1], c=colors[:i-1], cmap='viridis', s=25, alpha=0.4, vmin=min_f_val, vmax=max_f_val)
            # Current point (highlighted with white edge)
            ax.scatter(theta[i-1], r[i-1], c=[colors[i-1]], cmap='viridis', s=120, vmin=min_f_val, vmax=max_f_val, edgecolor='white', linewidth=1.5)

        frame_path = os.path.join(frames_folder, f"frame_{i:05d}.png")
        plt.savefig(frame_path, dpi=100, bbox_inches='tight', facecolor='black')
        plt.close(fig)

    # --- 5. Compile Video with Audio ---
    print("   -> 🎞️ Compiling video...")
    frame_files = [os.path.join(frames_folder, f) for f in sorted(os.listdir(frames_folder)) if f.endswith('.png')]
    
    try:
        clip = ImageSequenceClip(frame_files, fps=FPS)
        audio_clip = AudioFileClip(temp_audio_path)
        final_clip = clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        print(f"   -> ✅ Animation saved as: '{output_path}'")
    except Exception as e:
        print(f"   -> ❌ Error compiling video. (Reason: {e})")
        print("      Ensure FFmpeg is installed and accessible in your system's PATH.")

    # --- 6. Cleanup ---
    finally:
        print("   -> 🧹 Cleaning up temporary files...")
        shutil.rmtree(frames_folder)
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)


if __name__ == '__main__':
    INPUT_FILE = 'functions.txt'
    OUTPUT_FOLDER = 'sonified_videos'
    
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found. Creating a default file.")
        default_functions = ["x**0.5", "log(x)", "sin(x/10) * x", "x % 17"]
        with open(INPUT_FILE, 'w') as f: f.write(str(default_functions))
    
    try:
        with open(INPUT_FILE, 'r') as f: functions_to_plot = ast.literal_eval(f.read())
    except Exception:
        print(f"Error reading '{INPUT_FILE}'. Please ensure it's a valid list of strings.")
        exit()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("--- 🌀 Prime Sonification Animator ---")
    
    while True:
        try:
            user_limit = int(input("Enter the upper numerical limit for primes (e.g., 1000): "))
            if user_limit <= 2: print("Please enter a limit greater than 2.")
            else: break
        except ValueError:
            print("Invalid input. Please enter an integer.")
            
    print("\nChoose the type of radial plot to generate:")
    print("  1. Function Spiral (Radius = function value)")
    print("  2. Prime Distribution Spiral (Radius = prime value, Color = function value)")
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            plot_type_choice = 'function_spiral'
            break
        elif choice == '2':
            plot_type_choice = 'distribution_spiral'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
            
    print("\n🚀 Starting batch process...")
    for func_str in functions_to_plot:
        create_sonified_animation(func_str, user_limit, plot_type_choice, OUTPUT_FOLDER)
    print("\n✨ Batch process complete!")