# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/g2_frames_to_animation.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/g2.py   (last edited 2025-08-24)
# What this script does  :: Turns numbered PNG frames into an animation (GIF/MP4).
# ----------------------------------------------------------------------------


# ---------- Settings (edit these for your full run) ----------
IMG_DIR = "radial_plots_generator"           # folder containing your frames
OUTPUT_BASENAME = "radial_plots_animation"  
import os
import re
import imageio

# --- CONFIGURATION: Please edit these values ---

# 1. Path to the folder containing your ~400 images.
#    Example for Windows: 'C:/Users/YourUser/Desktop/MyImages'
#    Example for Mac/Linux: '/Users/YourUser/Documents/MyImages'
image_folder = "radial_plot_gen2"           # folder containing your frames

# 2. Name of the output file. Use .mp4 for video or .gif for an animated GIF.
output_file = "radial_plots_animation2.mp4"  

# 3. Frames Per Second (FPS). This controls the speed of the animation.
#    Try values between 15 and 30 for different effects.
fps = 25

# --- END OF CONFIGURATION ---


def create_animation():
    """
    Finds images in the specified folder, sorts them numerically,
    and creates an animation.
    """
    try:
        # Get a list of all image files in the folder
        files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
        
        if not files:
            print("Error: No image files found in the specified folder.")
            print(f"Searched in: {os.path.abspath(image_folder)}")
            return

        # --- Smartly sort the files ---
        # This function extracts the number from filenames like '...x140.jpg'
        # to ensure correct sorting (e.g., 9, 10, 11, not 10, 11, 9).
        def extract_number(filename):
            match = re.search(r'(\d+)', filename)
            return int(match.group(1)) if match else -1

        files.sort(key=extract_number)
        
        print(f"Found {len(files)} images. Creating animation...")

        # Create the animation
        with imageio.get_writer(output_file, mode='I', fps=fps) as writer:
            for filename in files:
                file_path = os.path.join(image_folder, filename)
                image = imageio.imread(file_path)
                writer.append_data(image)
        
        print(f"🎉 Animation successfully saved as '{output_file}'!")

    except FileNotFoundError:
        print(f"Error: The folder '{image_folder}' was not found. Please check the path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    create_animation()