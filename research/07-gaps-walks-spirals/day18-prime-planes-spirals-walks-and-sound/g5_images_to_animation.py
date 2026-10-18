# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/g5_images_to_animation.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/g5.py   (last edited 2025-08-24)
# What this script does  :: Animates the generated_images folder.
# ----------------------------------------------------------------------------
import os
import re
from moviepy.editor import ImageSequenceClip

# --- Configuration ---
IMAGE_FOLDER = 'generated_images'  # The folder with your PNGs
OUTPUT_FILE = 'silent_animation.mp4'
FPS = 30 # Set your desired frame rate

# --- Main Logic ---
print("Finding and sorting image files...")
image_files = [os.path.join(IMAGE_FOLDER, f)
               for f in os.listdir(IMAGE_FOLDER)
               if f.endswith('.png')]

# Sort files numerically (e.g., frame_001, frame_002, ...)
image_files.sort()

if not image_files:
    print("No images found! Make sure you ran the generation script first.")
else:
    print(f"Found {len(image_files)} frames. Creating video clip...")
    video_clip = ImageSequenceClip(image_files, fps=FPS)
    
    print(f"Writing video file to '{OUTPUT_FILE}'...")
    # Use a high-quality preset for the best visual result
    video_clip.write_videofile(OUTPUT_FILE, codec='libx24')
    
    print("🎉 Silent video created successfully!")