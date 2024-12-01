import cv2
import numpy as np
from matplotlib import pyplot as plt


def apply_colormap(gray_image, colmap_name=None):
    # Normalize the grayscale image to [0, 1] range
    normalized_img = gray_image.astype(np.float32) / 255.0

    # Apply the Inferno colormap from matplotlib
    if colmap_name is None:
        # colmap_name = "inferno"
        colmap_name = "viridis"
    inferno_colormap = plt.get_cmap(colmap_name)

    # Map the grayscale image to Inferno colors
    colored_img = inferno_colormap(normalized_img)

    # Remove the alpha channel if present and convert to BGR
    colored_img_bgr = (colored_img[:, :, :3] * 255).astype(np.uint8)
    colored_img_bgr = cv2.cvtColor(colored_img_bgr, cv2.COLOR_RGB2BGR)

    return colored_img_bgr
