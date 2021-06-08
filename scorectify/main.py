#!/usr/bin/env python3
from typing import Union

import PIL.Image
import numpy as np
from PIL import ImageOps
from PIL.Image import Image
from skimage.filters import threshold_yen
from skimage.transform import hough_line, hough_line_peaks, rotate


def rectify_image(im: Union[np.ndarray, Image]) -> np.ndarray:
    """
    Rectify and grayscale image according to the stem lines

    :param im: Either a numpy array or a PIL image
    :type im: Union[np.ndarray, Image]
    :return: The rectified image as a numpy array
    :rtype: np.ndarray
    """

    # Standardize input
    if isinstance(im, np.ndarray):
        im = PIL.Image.fromarray(im)
    im = np.array(ImageOps.grayscale(im))

    # Threshold
    thresh = im < threshold_yen(im)

    # Estimate rotation
    max_angle = np.pi / 18 / 2  # Test within ±5°
    graining = 50  # Test 50 angles
    right_angle = np.pi / 2
    possible_angles = np.linspace(-max_angle, max_angle, graining, endpoint=False) + right_angle
    h, theta, d = hough_line(thresh, theta=possible_angles)
    _, angles, _ = hough_line_peaks(h, theta, d, min_distance=2)
    angles = np.array(sorted(angles)) - right_angle
    best_angle = np.rad2deg(np.median(angles))

    # Correct rotation
    rotation_threshold = 0.005  # Assume small angles are just noise
    if best_angle > rotation_threshold:
        im = rotate(im, best_angle, mode='edge')
    return im
