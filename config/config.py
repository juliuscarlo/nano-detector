"""Config class to provide config data to the object detection system.

Contains a class to load and parse a yml config file to python objects.

Author: Julius Nick (julius.nick@gmail.com)

"""

import os
import yaml


class Config:
    def __init__(self):
        """Get python objects using the from_yml method and set up the
        corresponding attributes.
        """

        params = self.from_yml()

        self.model_path = os.path.normpath(params["model_path"])
        self.label_path = os.path.normpath(params["label_path"])
        self.input_images_path = os.path.normpath(params["input_images_path"])
        self.xml_output_path = os.path.normpath(params["xml_output_path"])
        self.augmented_images_path = os.path.normpath(params["augmented_images_path"])

        self.max_detections = params["max_detections"]
        self.min_probability = params["min_probability"]

        self.root_dir = os.path.normpath(os.path.dirname(os.path.abspath(params["main_path"])))

        self.logging_level = params["logging_level"]
        self.logs_path = os.path.normpath(params["logs_path"])

    @classmethod
    def from_yml(cls, cfg="config/config.yml"):
        """Parses the config from a yml file and returns a python object.

        Args:
            cfg: the config.yml file that should be parsed
        """

        with open(cfg, "r") as file:
            params = yaml.safe_load(file)
        return params
