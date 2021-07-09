"""Label loader for object detection models.

Provides methods to load labels from a file to a python object.

Author: Julius Nick (julius.nick@gmail.com)

"""


class LabelLoader:
    @staticmethod
    def load_labels(path):
        """Load label data from specified path. This is needed to map the
        numerical output of the model to human readable categories.

        Args:
            path: path to the labels file specified in the config.yml
        """
        with open(path, 'r') as f:
            return [line.strip() for line in f.readlines()]
