# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/g3_frames_to_consistent_video.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/g3.py   (last edited 2025-08-24)
# What this script does  :: Resizes frames to one size and writes a video.
# ----------------------------------------------------------------------------
import os
import re
import imageio.v2 as imageio  # Use imageio.v2 to avoid deprecation warnings
from PIL import Image         # Import the Pillow library for resizing
import numpy as np            # Import numpy to format the image data

# --- CONFIGURATION: Please edit these values ---

# 1. Path to the folder containing your image files.
image_folder = "radial_plot_gen2"

# 2. Name of the output video file.
output_file = "radial_plots_animation3.mp4"

# 3. Frames Per Second (FPS) for the animation.
fps = 24

# --- NEW: Set a consistent video resolution ---
# All images will be resized to these dimensions.
# Using dimensions divisible by 16 (like 1280x720) is best for video compatibility.
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1920

# --- END OF CONFIGURATION ---


def create_consistent_video():
    """
    Finds images, resizes them to a consistent size, and creates an animation.
    """
    try:
        # Get a list of all image files in the folder
        files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
        
        if not files:
            print("Error: No image files found in the specified folder.")
            print(f"Searched in: {os.path.abspath(image_folder)}")
            return

        # --- Smartly sort the files ---
        def extract_number(filename):
            match = re.search(r'(\d+)', filename)
            return int(match.group(1)) if match else -1

        files.sort(key=extract_number)
        
        print(f"Found {len(files)} images. Resizing and creating animation...")

        # Create the animation
        with imageio.get_writer(output_file, mode='I', fps=fps) as writer:
            for filename in files:
                file_path = os.path.join(image_folder, filename)
                
                # --- THIS IS THE NEW RESIZING LOGIC ---
                # 1. Open the image using Pillow
                img = Image.open(file_path)
                
                # 2. Resize it to the target dimensions using a high-quality filter
                img_resized = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
                
                # 3. Convert the resized image to a numpy array and append it to the video
                writer.append_data(np.array(img_resized))
        
        print(f"🎉 Animation successfully saved as '{output_file}'!")

    except FileNotFoundError:
        print(f"Error: The folder '{image_folder}' was not found. Please check the path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    create_consistent_video()