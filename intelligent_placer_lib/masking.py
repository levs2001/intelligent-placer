import logging

import numpy as np
from imageio import imread
from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.morphology import binary_opening


def get_mask(filename, threshold, threshold_delimeter, opening_radius):
    logging.info(f"Getting mask from: {filename}")
    blur = gaussian(imread(filename), sigma=1.5, channel_axis=2)
    gray = rgb2gray(blur)
    thresh = threshold(gray) / threshold_delimeter
    mask = gray >= thresh
    return binary_opening(mask, footprint=np.ones((opening_radius, opening_radius)))
