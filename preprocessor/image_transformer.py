import cv2

def resize(img, dimensions):
    resized_img = cv2.resize(img, dimensions)
    return resized_img
