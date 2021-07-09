"""Contains the object detector base class.

Specifies abstract methods to be implemented by the detector.

Author: Julius Nick (julius.nick@gmail.com)

"""

from abc import ABC, abstractmethod
from config import config


class BaseClass(ABC):
    """The baseclass methods are overridden in the detector."""
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
