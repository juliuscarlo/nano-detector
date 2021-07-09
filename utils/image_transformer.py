"""Module to transform images using cv2.

Contains a method to transform an image to a different target resolution / dimension.

Author: Julius Nick (julius.nick@gmail.com)

"""

import cv2


class Transformer:
    @staticmethod
    def resize(img, dimensions):
        """Resizes an image to the specified dimensions and returns the resized
        image.

        Args:
            img: the image to be resized
            dimensions: the target dimensions the image should be resized to
        """
        resized_img = cv2.resize(img, dimensions)
        return resized_img
