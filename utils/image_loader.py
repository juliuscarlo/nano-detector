import cv2
import os

class ImageLoader():
    def __init__(self, images_input_path):
        self.get_img_queue

    def get_img_queue(self, path):
        return os.listdir(path)

def load(file="data/images/div2k/0178.png"):
    img = cv2.imread(file)
    return img

