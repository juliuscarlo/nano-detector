"""Loads images and creates a queue for batch processing."""
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

# def load(file="data/images/div2k/0178.png"):
#     img = cv2.imread(file)
#     return img
