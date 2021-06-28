"""Entry point for running the object detection program."""

from model.detector import Detector


def run():
    detector = Detector()
    detector.prepare_model()
    detector.load_images()

    # The queue of images is analyzed one by one, until it is empty.
    while detector.img_loader.queue:
        detector.preprocess_data()
        detector.run_inference()
        detector.export_results()



if __name__ == "__main__":
    run()

# interpreter = tflite.Interpreter(config.model_path)

# interpreter.allocate_tensors()
# _, height, width, _ = interpreter.get_input_details()[0]["shape"]
# print("Image Shape (", width, ",", height, ")")

# # Get input and output tensors

# input_details = interpreter.get_input_details()
# print("input_details: ", input_details)
# output_details = interpreter.get_output_details()
# print("output_details: ", output_details)

# img = image_loader.load("data/images/div2k/0013.png")

# input_data = image_transformer.resize(img, (width, height))
# input_data = np.expand_dims(input_data, axis=0)
# print(input_data.shape)

# location, category, score, freq = inference.analyze_image(
#     interpreter, input_data)

# labels = label_loader.load(config.labels_path)
# # print(labels)
# # print(labels[0])

# # copy the base image
# base_img = img.copy()

# objects = []

# for i in range(min(int(freq), 7)):
#     category_label = labels[int(category[i])]
#     print(location[i], category[i], score[i], category_label)

#     objects.append(
#         {"loc": location[i], "probability": score[i], "term": category_label})

#     box = location[i]

#     augmentor.label(base_img, box, category_label)

# # save image to output folder data/images/examples/test/out
# cv2.imwrite("data/out/images/" + "annotated" + ".jpg", base_img)

# print(objects)
# tree = xml_writer.create_tree(objects)

# # NOTES #

# # https://www.tensorflow.org/lite/guide/inference#load_and_run_a_model_in_python
