import yaml
import os

model_path = "models/coco_efficientdet_v4/lite-model_efficientdet_lite4_detection_metadata_2.tflite"
labels_path = "models/coco_efficientdet_v4/labelmap.txt"


class Config:
    def __init__(self):
        params = self.from_yaml()
        self.model_path = params["model_path"]
        self.label_path = params["label_path"]
        self.input_images_path = params["input_images_path"]
        self.xml_output_path = params["xml_output_path"]
        self.augmented_images_path = params["augmented_images_path"]

        self.max_detections = params["max_detections"]
        self.min_probability = params["min_probability"]

    @classmethod
    def from_yaml(cls, cfg="config/config.yml"):
        """Create a config from a json file."""
        with open(cfg, "r") as file:
            params = yaml.safe_load(file)
        return params

