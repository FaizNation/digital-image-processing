import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def get_image(filename='input.jpg'):
    if os.path.exists(filename):
        img = cv2.imread(filename)
        return img
    else:
        raise FileNotFoundError(f"Image '{filename}' not found. Please ensure it exists in the current directory.")

# 1. Operasi Titik
def rgb_to_grayscale_average(img):
    # img is BGR in OpenCV
    b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
    gray = (r.astype(np.float32) + g.astype(np.float32) + b.astype(np.float32)) / 3.0
    return np.clip(gray, 0, 255).astype(np.uint8)

def rgb_to_grayscale_luminance(img):
    # L = 0.299*R + 0.587*G + 0.114*B
    b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
    gray = 0.299 * r.astype(np.float32) + 0.587 * g.astype(np.float32) + 0.114 * b.astype(np.float32)
    return np.clip(gray, 0, 255).astype(np.uint8)

def negative_image(img):
    return 255 - img

def brightness_adjustment(img, value):
    img_float = img.astype(np.float32) + value
    return np.clip(img_float, 0, 255).astype(np.uint8)

def thresholding(gray_img, t1, t2):
    # Returns a tuple of two binary images (using threshold t1 and t2)
    bin1 = np.where(gray_img >= t1, 255, 0).astype(np.uint8)
    bin2 = np.where(gray_img >= t2, 255, 0).astype(np.uint8)
    return bin1, bin2

# 2. Operasi Aritmatika
def add_images(img1, img2):
    res = img1.astype(np.float32) + img2.astype(np.float32)
    return np.clip(res, 0, 255).astype(np.uint8)

def subtract_images(img1, img2):
    res = img1.astype(np.float32) - img2.astype(np.float32)
    return np.clip(res, 0, 255).astype(np.uint8)

def scalar_multiply(img, scalar):
    res = img.astype(np.float32) * scalar
    return np.clip(res, 0, 255).astype(np.uint8)

# 3. Operasi Lokal (Filtering)
def mean_filter_3x3(img):
    # Implement scratch mean filter or use cv2.filter2D for speed.
    # Assignment implies understanding the mask. We'll use cv2.filter2D with a defined mask.
    kernel = np.ones((3, 3), np.float32) / 9.0
    return cv2.filter2D(img, -1, kernel)

# 4. Operasi Boolean
def boolean_operations(bin1, bin2):
    # Binary AND
    res_and = cv2.bitwise_and(bin1, bin2)
    # Binary OR
    res_or = cv2.bitwise_or(bin1, bin2)
    # Binary NOT (on bin1)
    res_not = cv2.bitwise_not(bin1)
    return res_and, res_or, res_not

# 5. Image Blending
def blend_images(img1, img2, alpha):
    # img1 * alpha + img2 * (1 - alpha)
    img1_f = img1.astype(np.float32)
    img2_f = img2.astype(np.float32)
    blended = img1_f * alpha + img2_f * (1.0 - alpha)
    return np.clip(blended, 0, 255).astype(np.uint8)

# Bonus: Histogram
def plot_histogram(image, title, ax):
    if len(image.shape) == 2:
        # Grayscale
        ax.hist(image.ravel(), 256, [0, 256], color='black')
    else:
        # Color
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            ax.plot(hist, color=col)
            ax.set_xlim([0, 256])
    ax.set_title(title)

# GUI Configuration (Bonus)
def run_gui(img, img2):
    cv2.namedWindow('Interactive GUI - Brightness & Blending')
    
    # Store initial alpha for blending
    initial_alpha = 50 # corresponds to 0.5
    
    def on_brightness_trackbar(val):
        pass # Handle inside loop
    def on_blend_trackbar(val):
        pass
        
    cv2.createTrackbar('Brightness', 'Interactive GUI - Brightness & Blending', 128, 255, on_brightness_trackbar)
    cv2.createTrackbar('Blending Alpha', 'Interactive GUI - Brightness & Blending', 50, 100, on_blend_trackbar)

    print("\n--- GUI Controls ---")
    print("- Atur slider 'Brightness' (0-255 dimana 128 = +0 offset)")
    print("- Atur slider 'Blending Alpha' (0-100% untuk blending img1 dan img2)")
    print("- Tekan 'q' atau 'ESC' pada jendela GUI untuk keluar dan melihat visualisasi lengkap (Matplotlib).")

    while True:
        b_val = cv2.getTrackbarPos('Brightness', 'Interactive GUI - Brightness & Blending') - 128
        alpha_val = cv2.getTrackbarPos('Blending Alpha', 'Interactive GUI - Brightness & Blending') / 100.0
        
        # Apply Brightness
        bright_img = brightness_adjustment(img, b_val)
        
        # Apply Blending with second image
        blended_img = blend_images(bright_img, img2, alpha_val)
        
        cv2.imshow('Interactive GUI - Brightness & Blending', blended_img)
        
        key = cv2.waitKey(30) & 0xFF
        if key == 27 or key == ord('q'): # ESC or q
            break
            
    cv2.destroyAllWindows()


def main():
    print("Memuat citra...")
    # Get main image
    img = get_image('input.jpg')
    
    # Second image for arithmetic and blending
    img2 = get_image('input2.jpg')
    # Resize img2 to match img size for easy operations
    img2 = cv2.resize(img2, (img.shape[1], img.shape[0]))
    
    # --- 1. Operasi Titik ---
    print("Menjalankan Operasi Titik...")
    gray_avg = rgb_to_grayscale_average(img)
    gray_lum = rgb_to_grayscale_luminance(img)
    neg_img = negative_image(img)
    bright_pos = brightness_adjustment(img, 50)
    bright_neg = brightness_adjustment(img, -50)
    # Thresholding using grayscale luminance
    bin_t1, bin_t2 = thresholding(gray_lum, 100, 200)

    # --- 2. Operasi Aritmatika ---
    print("Menjalankan Operasi Aritmatika...")
    added = add_images(img, img2)
    subbed = subtract_images(img, img2)
    scaled = scalar_multiply(img, 1.5)

    # --- 3. Operasi Lokal (Filtering) ---
    print("Menjalankan Operasi Filtering...")
    # Tambahkan sedikit noise untuk melihat efek mean filter
    noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
    noisy_img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    filtered = mean_filter_3x3(noisy_img)

    # --- 4. Operasi Boolean ---
    print("Menjalankan Operasi Boolean...")
    # Create two geometric binary masks for demonstration
    mask1 = np.zeros(gray_lum.shape, dtype=np.uint8)
    cv2.circle(mask1, (mask1.shape[1]//2 - 50, mask1.shape[0]//2), 80, 255, -1)
    
    mask2 = np.zeros(gray_lum.shape, dtype=np.uint8)
    cv2.circle(mask2, (mask2.shape[1]//2 + 50, mask2.shape[0]//2), 80, 255, -1)
    
    res_and, res_or, res_not = boolean_operations(mask1, mask2)

    # --- 5. Image Blending ---
    print("Menjalankan Operasi Blending...")
    blended_50 = blend_images(img, img2, 0.5)

    # --- Bonus GUI ---
    print("Membuka GUI...")
    run_gui(img, img2)
    
    # --- Visualisasi Menggunakan Matplotlib ---
    print("Membuka Visualisasi Keseluruhan Hasil (Matplotlib)...")
    
    # Helper for converting BGR to RGB for matplotlib
    def bgr2rgb(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Setup plotting grid
    fig, axs = plt.subplots(4, 4, figsize=(15, 12))
    fig.canvas.manager.set_window_title('Hasil Pemrosesan Citra Dasar')
    axs = axs.ravel()
    
    images = [
        (bgr2rgb(img), "Citra Asli"),
        (gray_avg, "Grayscale (Average)", 'gray'),
        (gray_lum, "Grayscale (Luminance)", 'gray'),
        (bgr2rgb(neg_img), "Citra Negatif"),
        (bgr2rgb(bright_pos), "Brightness (+50)"),
        (bgr2rgb(bright_neg), "Brightness (-50)"),
        (bin_t1, "Threshold (T=100)", 'gray'),
        (bin_t2, "Threshold (T=200)", 'gray'),
        (bgr2rgb(added), "Add: img1 + img2"),
        (bgr2rgb(subbed), "Sub: img1 - img2"),
        (bgr2rgb(scaled), "Scalar Mul (*1.5)"),
        (bgr2rgb(blended_50), "Blending (alpha=0.5)"),
        (bgr2rgb(noisy_img), "Noisy Image Before Filter"),
        (bgr2rgb(filtered), "After Mean Filter 3x3"),
        (res_and, "Boolean AND (binary)", 'gray'),
        (res_or, "Boolean OR (binary)", 'gray')
    ]
    
    for i, item in enumerate(images):
        if len(item) == 3:
            axs[i].imshow(item[0], cmap=item[2])
        else:
            axs[i].imshow(item[0])
        axs[i].set_title(item[1])
        axs[i].axis('off')
        
    plt.tight_layout()
    plt.show()

    # Plot Histogram
    fig_hist, axs_hist = plt.subplots(1, 2, figsize=(10, 4))
    fig_hist.canvas.manager.set_window_title('Bonus: Perbandingan Histogram')
    plot_histogram(img, "Histogram Citra Asli", axs_hist[0])
    plot_histogram(bright_pos, "Histogram Brightness (+50)", axs_hist[1])
    plt.tight_layout()
    plt.show()
    
    print("Selesai.")

if __name__ == '__main__':
    main()
