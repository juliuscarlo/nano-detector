from numpy.lib.function_base import interp
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import pathlib

# label loader
def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]["index"]
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image

def analyze_image(interpreter, image, top_k=1):
    set_input_tensor(interpreter, image)

    interpreter.invoke()
    output_details = interpreter.get_output_details()
    print(output_details)
    print("-----output location-----")
    output_location = np.squeeze(interpreter.get_tensor(output_details[0]["index"]))
    print(output_location)
    print("----output category------")
    output_category = np.squeeze(interpreter.get_tensor(output_details[1]["index"]))
    print(output_category)
    print("----output score------")
    output_score = np.squeeze(interpreter.get_tensor(output_details[2]["index"]))
    print(output_score)
    print("----output number of detections------")
    output_freq = np.squeeze(interpreter.get_tensor(output_details[3]["index"]))
    print(output_freq)

    # scale, zero_point = output_details["quantization"]
    # output = scale * (output - zero_point)

    return [output_location, output_category, output_score, output_freq]

# Load the model into memory
# (a .tflite model containing the execution graph)

model_path = "data/saved_models/lite-model_ssd_mobilenet_v1_1_metadata_2.tflite"
labels_path = "data/saved_models/labelmap.txt"

# Load model and allocate tensorfs
interpreter = tflite.Interpreter(model_path)
print("Model loaded.")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]["shape"]
print("Image Shape (", width, ",", height, ")")

# Get input and output tensors

# input_details = interpreter.get_input_details()
# print(input_details)
# output_details = interpreter.get_output_details()

# Transform / Preprocess the data (e.g. resize, change format)
# (Raw data regularly does not match the input data format expected by the model)

# Run inference
# (Use the TensorFlow Lite API to execute the model)

## build an interpreter
## allocate tensors (set input tensor values)


# Interpret output
## (read output tensor values to interpret them depending on application
## e.g. list of probabilities, categories, etc..)

# Test the model

img = cv2.imread("./data/images/examples/test/object_6.jpg")
input_data = cv2.resize(img, (width, height))
input_data = np.expand_dims(input_data, axis=0)
print(input_data.shape)

location, category, score, freq = analyze_image(interpreter, input_data)

labels = load_labels(labels_path)
print(labels)
print(labels[0])


def draw_rect(image, box):
    h = image.shape[0]
    w = image.shape[1]
    y_min = int(max(1, (box[0] * h)))
    x_min = int(max(1, (box[1] * w)))
    y_max = int(min(h, (box[2] * h)))
    x_max = int(min(w, (box[3] * w)))
    
    # draw a rectangle on the image
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (155, 255, 0), 2)


for i in range(min(int(freq), 3)):
    category_label = labels[int(category[i])]
    print(location[i], category[i], score[i], category_label)

    # copy the base image
    base_img = img.copy()
    box = location[i]

    # add bounding boxes (top, left, bot, right)
    # t, l, b, r = location[i][:2]*
    draw_rect(base_img, box)

    #augmented_image = cv.rectangle

    # add text label to box

    # save image to output folder data/images/examples/test/out
    cv2.imwrite("data/images/examples/test/out/" + str(i) + ".jpg", base_img)






# run the inference

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.

# output_data = interpreter.get_output_details()
# output_data = interpreter.get_tensor(output_details[0]['index'])
# print(output_data)
# print(output_data.shape)
# print("----------")
# results = np.squeeze(output_data) # what does this do?
# print(results)
# print("sssssssssssssssssss")
# print(results.shape)


# top_k = results.argsort()[-5:][::-1]
# print(top_k)
# print("++++++++++++++")
# labels = load_labels(labels_path)
# print(labels)

# for i in top_k:
#     print(results[i], labels[i])
#     # print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))

# NOTES #

# Example of how to run a model:

# https://www.tensorflow.org/lite/guide/inference#load_and_run_a_model_in_python
