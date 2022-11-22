import os

import matplotlib.pyplot as plt
import numpy as np
from imageio import imread
from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.filters import threshold_isodata
from skimage.measure import label as sk_measure_label
from skimage.measure import regionprops
from skimage.morphology import binary_opening, binary_closing


def get_mask(filename, threshold):
    print("Getting mask from", filename)
    blur = gaussian(imread(filename), sigma=1.5, channel_axis=2)
    gray = rgb2gray(blur)
    thresh = threshold(gray)
    mask = gray >= thresh
    return mask


def polish_mask(mask):
    result = binary_closing(mask, footprint=np.ones((10, 10)))
    return binary_opening(result, footprint=np.ones((10, 10)))


def get_components(mask):
    labels = sk_measure_label(mask)  # разбиение маски на компоненты связности
    props = regionprops(labels)  # нахождение свойств каждой области (положение центра, ...)
    return props


def show_all_masks_in_folder(folder):
    for picture_name in os.listdir(folder):
        if not (picture_name.endswith(".jpg") or picture_name.endswith(".JPG")):
            print("Skipped ", picture_name)
            continue
        mask = polish_mask(get_mask(os.path.join(folder, picture_name), threshold_isodata))
        plt.imshow(mask, cmap='gray')
        plt.title(picture_name)
        plt.show()
        props = get_components(mask)
        # Считая многоугольник
        print("Components count: ", len(props))
