from numpy.lib.function_base import interp
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import pathlib

# to-do: limit freq, limit prob, write to same img
# refactor, modularize
# logging module
# testcases 

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

model_path = "data/saved_models/inception/inception_resnet_v2.tflite"
labels_path = "data/saved_models/inception/labels.txt"

# Load model and allocate tensorfs
interpreter = tflite.Interpreter(model_path)
print("Model loaded.")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]["shape"]
print("Image Shape (", width, ",", height, ")")

# Get input and output tensors

input_details = interpreter.get_input_details()
print("input_details: ", input_details)
output_details = interpreter.get_output_details()
print("output_details: ", output_details)

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

img = cv2.imread("./data/images/examples/banana_0.jpg")
input_data = cv2.resize(img, (width, height))
input_data = np.expand_dims(input_data, axis=0)
print(input_data.shape)

location, category, score, freq = analyze_image(interpreter, input_data)

labels = load_labels(labels_path)
print(labels)
print(labels[0])


def draw_rect(image, box, text):
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
    cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (60,200,12), 2)

# copy the base image
base_img = img.copy()

for i in range(min(int(freq), 3)):
    category_label = labels[int(category[i])]
    print(location[i], category[i], score[i], category_label)

    box = location[i]

    # add bounding boxes (top, left, bot, right)
    # t, l, b, r = location[i][:2]*
    draw_rect(base_img, box, category_label)

    #augmented_image = cv.rectangle

    # add text label to box

# save image to output folder data/images/examples/test/out
cv2.imwrite("data/images/examples/test/out/" + "annotated" + ".jpg", base_img)






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
