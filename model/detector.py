"""Detector module for object detection.

Implements the abstract methods of the detector base class.

Author: Julius Nick (julius.nick@gmail.com)

"""

import tensorflow as tf
# import tflite_runtime.interpreter as tflite

import numpy as np
import cv2
import os
from datetime import date

from model.detector_base import BaseClass
from model import inference
from model import label_loader
from utils import image_transformer
from utils import augmentor
from config import config
from utils import image_loader
from utils import xml_writer

import utils.logger


class Detector(BaseClass):
    """Inherits from the detector base class and implements its abstract methods for the object detection."""

    def __init__(self):
        super().__init__(config)

        # Initialize a logger
        self.logger = utils.logger.Logger(logging_level=self.config.logging_level,
                                          root_dir=self.config.root_dir,
                                          logs_path=self.config.logs_path)

        self.logger.log("Logger initialized.")

        # Generate an instance of the tflite Interpreter class
        # self.interpreter = tflite.Interpreter(self.config.model_path)
        self.interpreter = tf.lite.Interpreter(self.config.model_path)

        self.logger.log("Tflite Interpreter initialized.")

    def prepare_model(self):
        self.interpreter.allocate_tensors()

        # Get the models input dimensions as the target dimension for an image to be analyzed
        self.input_height = self.interpreter.get_input_details()[0]["shape"][1]
        self.input_width = self.interpreter.get_input_details()[0]["shape"][2]
        self.input_shape = (self.input_width, self.input_height)

        # Load the model labels for matching numerical output of the model to categories
        self.labels = label_loader.load(self.config.label_path)

        self.logger.log("Model prepared.")

    def load_images(self):
        self.img_loader = image_loader.ImageLoader(
            self.config.input_images_path)

        if not self.img_loader.queue:
            self.logger.log(
                "Queue is empty. No images to process found in input folder.")
        else:
            self.logger.log("Loaded image queue: " +
                            str(self.img_loader.queue))

    def preprocess_data(self):
        self.img, self.img_name = self.img_loader.load_img(
            self.config.input_images_path)
        self.input_data = image_transformer.resize(self.img, self.input_shape)
        self.input_data = np.expand_dims(self.input_data, axis=0)

        self.logger.log("Preprocessed image: " + self.img_name)

    def run_inference(self):
        self.location, self.category, self.score, self.freq = inference.analyze_image(
            self.interpreter, self.input_data)

        self.logger.log("Ran inference for image: " + self.img_name)

    def export_results(self):
        # export xml to out folder and augment input images with detected object information
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

            augmentor.label(base_img, box, text)

        cv2.imwrite(os.path.join(
            self.config.augmented_images_path, self.img_name), base_img)

        print(objects)

        # Get todays date for the XML export
        self.todays_date = date.today().strftime("%d.%m.%Y")

        # Generate the tree and export the XML file
        tree = xml_writer.create_tree(
            img=self.img, object_list=objects, filename=self.img_name, date=self.todays_date)
        xml_writer.write(tree, path=os.path.join(
            self.config.xml_output_path, (os.path.splitext(self.img_name)[0] + ".xml")))

        self.logger.log("Exported results for image: " + self.img_name)

        if not self.img_loader.queue:
            self.logger.log(
                "All images processed. Augmented images and XML are in the specified out folder.")
