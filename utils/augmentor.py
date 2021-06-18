import cv2

def label(image, box, text):
    h = image.shape[0]
    w = image.shape[1]
    y_min = int(max(1, (box[0] * h)))
    x_min = int(max(1, (box[1] * w)))
    y_max = int(min(h, (box[2] * h)))
    x_max = int(min(w, (box[3] * w)))
    
    # draw a rectangle on the image
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (60, 200, 12), 3)
    draw_text(image, x_min, y_min, text)


def draw_text(image, x, y, text):
    cv2.putText(image, text, (x+2, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (60,200,12), 2)
