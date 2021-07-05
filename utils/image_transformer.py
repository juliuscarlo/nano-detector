"""Module to transform images using cv2.

Author: Julius Nick (julius.nick@gmail.com)

"""

import cv2


def resize(img, dimensions):
    """resizes an image to the specified dimensions and returns the resized image."""
    resized_img = cv2.resize(img, dimensions)
    return resized_img
