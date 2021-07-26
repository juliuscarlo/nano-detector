"""Detector module for object detection.

Implements the abstract methods of the detector base class.

Author: Julius Nick (julius.nick@gmail.com)

"""

import tflite_runtime.interpreter as tflite

# alternative import statement for running on other platforms, see readme for details.
# import tensorflow as tf

import numpy as np
import cv2
import os
from datetime import date

from model.detector_base import BaseClass
from model import inference
from model import label_loader
from utils import image_transformer
from utils import augmentor
from utils import image_loader
from utils import xml_writer

import utils.logger


class Detector(BaseClass):
    """Inherits from the detector base class and implements its abstract methods
    for the object detection and image annotation.
    """

    def __init__(self):
        """Initializes the logger and a tflite interpreter."""
        super().__init__()

        # Initialize the instance attributes of a Detector
        self.todays_date = None
        self.input_height = None
        self.input_width = None
        self.input_shape = None
        self.labels = None
        self.img_loader = None
        self.img = None
        self.img_name = None
        self.input_data = None
        self.location, self.category, self.score, self.freq = [None] * 4

        # Initialize a logger
        self.logger = utils.logger.Logger(logging_level=self.config.logging_level,
                                          root_dir=self.config.root_dir,
                                          logs_path=self.config.logs_path)

        self.logger.log("Logger initialized.")

        # Generate an instance of the tflite Interpreter class
        self.interpreter = tflite.Interpreter(self.config.model_path)

        # alternative interpreter for running on other platforms, see readme for details.
        # self.interpreter = tf.lite.Interpreter(self.config.model_path)

        self.logger.log("Tflite Interpreter initialized.")

    def prepare_model(self):
        """Get the input dimensions of the model and load the label file."""
        self.interpreter.allocate_tensors()

        # Get the models input dimensions as the target dimension for an image to be analyzed
        self.input_height = self.interpreter.get_input_details()[0]["shape"][1]
        self.input_width = self.interpreter.get_input_details()[0]["shape"][2]
        self.input_shape = (self.input_width, self.input_height)

        # Load the model labels for matching numerical output of the model to categories
        self.labels = label_loader.LabelLoader.load_labels(
            self.config.label_path)

        self.logger.log("Model prepared.")

    def load_images(self):
        """Load the images to be annotated and put them in a queue to be processed later."""
        self.img_loader = image_loader.ImageLoader(
            self.config.input_images_path)

        if not self.img_loader.queue:
            self.logger.log(
                "Queue is empty. No images to process found in input folder.")
        else:
            self.logger.log("Loaded image queue: " +
                            str(self.img_loader.queue))

    def preprocess_data(self):
        """Preprocess the image for the chosen model."""
        self.img, self.img_name = self.img_loader.load_img(
            self.config.input_images_path)
        self.input_data = image_transformer.Transformer.resize(
            self.img, self.input_shape)
        self.input_data = np.expand_dims(self.input_data, axis=0)

        self.logger.log("Preprocessed image: " + self.img_name)

    def run_inference(self):
        """Run inference on a preprocessed image."""
        self.location, self.category, self.score, self.freq = inference.Inference.analyze_image(
            self.interpreter, self.input_data)

        self.logger.log("Ran inference for image: " + self.img_name)

    def export_results(self):
        """Export the results (XML/augmented image)."""
        base_img = self.img.copy()

        objects = []

        # Relevant objects are only considered up to the specified max_detections threshold
        for i in range(min(int(self.freq), self.config.max_detections)):
            score = self.score[i]
            if score < self.config.min_probability:
                break
            category_label = self.labels[int(self.category[i])]
            objects.append(
                {"loc": self.location[i], "probability": score, "term": category_label})

            box = self.location[i]
            # concatenate the box label, consisting of the label and probability
            text = category_label + "@" + "{:.2f}".format(score)

            # put the concatenated box label in the image
            augmentor.label(base_img, box, text)

        cv2.imwrite(os.path.join(
            self.config.augmented_images_path, self.img_name), base_img)

        # Get todays date for the XML export
        self.todays_date = date.today().strftime("%d.%m.%Y")

        # Generate the tree and export the XML file
        tree = xml_writer.create_tree(
            img_shape=self.img.shape, object_list=objects, filename=self.img_name, date=self.todays_date)
        xml_writer.write(tree, path=os.path.join(
            self.config.xml_output_path, (os.path.splitext(self.img_name)[0] + ".xml")))

        self.logger.log("Exported results for image: " + self.img_name)

        if not self.img_loader.queue:
            self.logger.log(
                "All images processed. Augmented images and XML are in the specified out folder.")
