"""Module to augment images using cv2.

Contains methods for labeling images with bounding boxes and text.

Author: Julius Nick (julius.nick@gmail.com)

"""

import cv2


def label(image, box, text):
    """Labels the specified image with a bounding box and prints text in that box."""
    # Get the dimensions of the image
    h = image.shape[0]
    w = image.shape[1]

    # Convert relative dimensions to absolute
    y_min = int(max(1, (box[0] * h)))
    x_min = int(max(1, (box[1] * w)))
    y_max = int(min(h, (box[2] * h)))
    x_max = int(min(w, (box[3] * w)))

    # draw a rectangle on the image
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (60, 200, 12), 3)

    # draw text inside the rectangle
    draw_text(image, x_min, y_min, text)


def draw_text(image, x, y, text):
    """Draws text on an image at an offset from the specified x and y coordinates"""
    cv2.putText(image, text, (x + 2, y + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (60, 200, 12), 2)

