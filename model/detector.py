import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import pathlib
import model
from preprocessor import image_transformer
from postprocessor import augmentor
from config import config
from input import image_loader
from output import xml_writer

from model.base import BaseClass


class Detector(BaseClass):
    def __init__(self):
        super().__init__(config)

        self.interpreter = tflite.Interpreter(self.config.model_path)

    def prepare_model(self):
        self.interpreter.allocate_tensors()
        self.input_height = self.interpreter.get_input_details()[0]["shape"][1]
        self.input_width = self.interpreter.get_input_details()[0]["shape"][2]

        self.labels = model.label_loader.load(self.config.label_path)

    def load_image(self):
        self.img = image_loader.load("data/in/2.png")

    def _preprocess_data(self):
        self.input_data = image_transformer.resize(self.img, (self.input_width, self.input_height))
        self.input_data = np.expand_dims(self.input_data, axis=0)

    def _run_inference(self):
        self.location, self.category, self.score, self.freq = model.inference.analyze_image(
            self.interpreter, self.input_data)
    
    def _export_results(self):
        # export xml to folder from config
        # augment input image if this option is specified
        base_img = self.img.copy()

        objects = []

        for i in range(min(int(self.freq), self.config.max_detections)):
            category_label = self.labels[int(self.category[i])]
            objects.append(
                {"loc": self.location[i], "probability": self.score[i], "term": category_label})

            box = self.location[i]

            augmentor.label(base_img, box, category_label)

        cv2.imwrite("data/out/augmented/" + "annotated" + ".jpg", base_img)

        print(objects)
        tree = xml_writer.create_tree(objects)