import cv2
import numpy as np
import matplotlib.pyplot as plt

def compute_histogram(image):
    hist = np.zeros(256, dtype=int)
    for pixel in image.ravel():
        hist[pixel] += 1
    return hist

def manual_histogram_equalization(image):
    hist = compute_histogram(image)
    
    cdf = hist.cumsum()
    
    cdf_masked = np.ma.masked_equal(cdf, 0)
    cdf_masked = (cdf_masked - cdf_masked.min()) * 255 / (cdf_masked.max() - cdf_masked.min())
    cdf_normalized = np.ma.filled(cdf_masked, 0).astype('uint8')
    
    equalized_image = cdf_normalized[image]
    
    return equalized_image, hist, compute_histogram(equalized_image)

def histogram_specification(source, target):
    src_hist = compute_histogram(source)
    tgt_hist = compute_histogram(target)
    
    src_cdf = src_hist.cumsum()
    tgt_cdf = tgt_hist.cumsum()
    
    src_cdf_norm = src_cdf / src_cdf.max()
    tgt_cdf_norm = tgt_cdf / tgt_cdf.max()
    
    mapping = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        diff = np.abs(tgt_cdf_norm - src_cdf_norm[i])
        mapping[i] = np.argmin(diff)
        
    specified_image = mapping[source]
    return specified_image, tgt_hist, compute_histogram(specified_image)

def plot_histogram(ax, hist, title, color='black'):
    ax.bar(range(256), hist, color=color, width=1)
    ax.set_title(title)
    ax.set_xlim([0, 256])

def main():
    # 1. Load original image
    img_path = 'img-grayscale.jpg'
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not load image {img_path}")
        return

    print("Successfully loaded img-grayscale.jpg")

    # 2 & 3. Manual Histogram Equalization
    print("Performing manual histogram equalization...")
    manual_eq_img, original_hist, manual_eq_hist = manual_histogram_equalization(img)

    # 4. Built-in Histogram Equalization
    print("Performing built-in histogram equalization...")
    cv2_eq_img = cv2.equalizeHist(img)
    cv2_eq_hist = compute_histogram(cv2_eq_img)

    # 5. Histogram Specification
    print("Performing histogram specification...")
    gamma = 0.5 # brighter
    target_img = np.array(255 * (img / 255) ** gamma, dtype='uint8')
    
    spec_img, target_hist, spec_hist = histogram_specification(img, target_img)

    # 6. Plotting
    print("Plotting results...")
    fig, axes = plt.subplots(5, 2, figsize=(12, 18))
    
    # Original
    axes[0, 0].imshow(img, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')
    plot_histogram(axes[0, 1], original_hist, 'Original Histogram')

    # Manual EQ
    axes[1, 0].imshow(manual_eq_img, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title('Manual Equalization')
    axes[1, 0].axis('off')
    plot_histogram(axes[1, 1], manual_eq_hist, 'Manual Equalization Histogram')

    # Built-in EQ
    axes[2, 0].imshow(cv2_eq_img, cmap='gray', vmin=0, vmax=255)
    axes[2, 0].set_title('Built-in (OpenCV) Equalization')
    axes[2, 0].axis('off')
    plot_histogram(axes[2, 1], cv2_eq_hist, 'Built-in Equalization Histogram')

    # Target image
    axes[3, 0].imshow(target_img, cmap='gray', vmin=0, vmax=255)
    axes[3, 0].set_title('Target Image for Specification')
    axes[3, 0].axis('off')
    plot_histogram(axes[3, 1], target_hist, 'Target Histogram')

    # Specification Result
    axes[4, 0].imshow(spec_img, cmap='gray', vmin=0, vmax=255)
    axes[4, 0].set_title('Specification Result')
    axes[4, 0].axis('off')
    plot_histogram(axes[4, 1], spec_hist, 'Specification Result Histogram')

    plt.tight_layout()
    plt.savefig('result.png')
    print("Results saved to result.png")

if __name__ == '__main__':
    main()
