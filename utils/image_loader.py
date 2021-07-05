"""Module to load image paths from a directory and create a queue for batch processing.

Contains an ImageLoader class that is used to initialize a queue and contains methods for
popping image names from this queue.

Author: Julius Nick (julius.nick@gmail.com)

"""

import cv2
import os


class ImageLoader:
    """Reads the files from the input_images_path specified in the config and adds them to a queue."""

    def __init__(self, images_input_path):
        self.queue = self.get_img_queue(self, images_input_path)

    @staticmethod
    def get_img_queue(self, path):
        return os.listdir(path)

    def load_img(self, images_input_path):
        self.img_name = self.queue.pop()
        img_path = os.path.join(images_input_path, self.img_name)
        print(img_path)

        self.img = cv2.imread(img_path)
        return self.img, self.img_name

