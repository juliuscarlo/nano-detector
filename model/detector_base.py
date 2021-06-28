"""Contains a base class that specifies abstract methods to be implemented by the detector."""

from abc import ABC, abstractmethod
from config import config

# to-do: limit freq, limit prob
# logging module
# testcases

# Load the model into memory
# (a .tflite model containing the execution graph)

# Build an interpreter, allocate tensors (set input tensor values)


class BaseClass(ABC):
    def __init__(self, cfg):
        self.config = config.Config()

    @abstractmethod
    def prepare_model(self):
        pass

    @abstractmethod
    def load_images(self):
        pass

    @abstractmethod
    def preprocess_data(self):
        pass

    @abstractmethod
    def run_inference(self):
        pass

    @abstractmethod
    def export_results(self):
        pass
