import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

INPUT_DIR = 'input_images'
RESULTS_DIR = 'experiment_results'

IMAGE_PATHS = [
    'gambar-internet.jpg'
]

def get_file_size_kb(file_path):
    """Returns the file size in kilobytes."""
    return os.path.getsize(file_path) / 1024

def show_comparison(original, edited_list, titles, output_path):
    """
    Generates and saves a comparison figure of the original and edited images.
    """
    n_images = len(edited_list) + 1
    
    fig, axes = plt.subplots(1, n_images, figsize=(n_images * 4, 4))
    
    # --- Display Original Image ---
    # Convert BGR to RGB for Matplotlib
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    axes[0].imshow(original_rgb)
    axes[0].set_title(titles[0])
    axes[0].axis('off') 

    # --- Display Edited Images ---
    for i, (edited_img, title) in enumerate(zip(edited_list, titles[1:])):
        # Convert BGR to RGB
        edited_rgb = cv2.cvtColor(edited_img, cv2.COLOR_BGR2RGB)
        ax = axes[i+1]
        ax.imshow(edited_rgb)
        ax.set_title(title)
        ax.axis('off')

    plt.tight_layout()
    # Save the full figure
    plt.savefig(output_path)
    plt.close(fig) # Close the figure to free up memory
    print(f"  [Visualization] Comparison chart saved to {output_path}")

# --- Main Processing Function ---

def process_image(image_path):
    """
    Applies a series of image processing tasks to a single image.
    """
    try:
        # Read the original image
        img = cv2.imread(os.path.join(INPUT_DIR, image_path))
        if img is None:
            raise FileNotFoundError(f"Image not found or unable to read: {os.path.join(INPUT_DIR, image_path)}")

        # Create a unique name for the output files based on the input filename
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        print(f"\n--- Processing Image: {image_path} ---")

        # --- Task A: Metadata Logging ---
        original_height, original_width = img.shape[:2]
        original_size_kb = get_file_size_kb(os.path.join(INPUT_DIR, image_path))
        print(f"  [Original] Resolution: {original_width}x{original_height}, Size: {original_size_kb:.2f} KB")

        # --- Task B: Sampling (Resizing) ---
        print("  Resizing...")
        for factor in [0.50, 0.25]:
            new_width = int(original_width * factor)
            new_height = int(original_height * factor)
            resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # Save the resized image
            out_path = os.path.join(RESULTS_DIR, f"{base_name}_resize_{int(factor*100)}.jpg")
            cv2.imwrite(out_path, resized_img)
            
            # Print new metadata
            resized_size_kb = get_file_size_kb(out_path)
            print(f"    [{int(factor*100)}% Resized] Resolution: {new_width}x{new_height}, Size: {resized_size_kb:.2f} KB")

        # --- Task C: Quantization (Color Depth) ---
        print("  Quantizing...")
        # Convert to Grayscale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(RESULTS_DIR, f"{base_name}_gray.jpg"), gray_img)
        print("    Saved Grayscale version.")

        # Convert to Binary (Black & White)
        _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite(os.path.join(RESULTS_DIR, f"{base_name}_binary.jpg"), binary_img)
        print("    Saved Binary (B&W) version.")
        
        # Convert to 16 Gray Levels
        quantized_16_levels = (gray_img // 16) * 16
        cv2.imwrite(os.path.join(RESULTS_DIR, f"{base_name}_16levels.jpg"), quantized_16_levels)
        print("    Saved 16 Gray Levels version.")

        # --- Task D: Interpolation Analysis ---
        print("  Analyzing Interpolation...")
        low_res_w, low_res_h = int(original_width * 0.25), int(original_height * 0.25)
        low_res_img = cv2.resize(img, (low_res_w, low_res_h), interpolation=cv2.INTER_AREA)

        interpolation_methods = {
            'nearest': cv2.INTER_NEAREST,
            'bilinear': cv2.INTER_LINEAR,
            'bicubic': cv2.INTER_CUBIC
        }
        
        upscaled_images = []
        titles = ["Original", "Nearest", "Bilinear", "Bicubic"]

        for name, method in interpolation_methods.items():
            upscaled_img = cv2.resize(low_res_img, (original_width, original_height), interpolation=method)
            out_path = os.path.join(RESULTS_DIR, f"{base_name}_interp_{name}.jpg")
            cv2.imwrite(out_path, upscaled_img)
            print(f"    Saved Upscaled version using {name.capitalize()} interpolation.")
            upscaled_images.append(upscaled_img)

        # --- Task E: Matplotlib Visualization ---
        comparison_chart_path = os.path.join(RESULTS_DIR, f"{base_name}_comparison_chart.png")
        show_comparison(img, upscaled_images, titles, comparison_chart_path)

        print(f"--- Finished: {image_path} ---")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {image_path}: {e}")

def main():
    """
    Main function to set up the environment and process all images.
    """
    # 1. Setup: Create the output and input directories if they don't exist
    if not os.path.exists(RESULTS_DIR):
        print(f"Creating results directory: {RESULTS_DIR}")
        os.makedirs(RESULTS_DIR)

    if not os.path.exists(INPUT_DIR):
        print(f"Creating input directory: {INPUT_DIR}")
        os.makedirs(INPUT_DIR)

    # Check if there are any images to process
    if not IMAGE_PATHS:
        print(f"The 'IMAGE_PATHS' list is empty. Please add image paths to the script, ensuring your images are in the '{INPUT_DIR}' directory.")
        return

    # 2. Loop through each image and process it
    for image_path in IMAGE_PATHS:
        process_image(image_path)

    print("\nAll image processing tasks complete.")

if __name__ == '__main__':
    main()
