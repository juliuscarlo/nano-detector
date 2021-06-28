

class LabelLoader:

    @staticmethod
    def load_labels(path):
        """Load label data from specified path"""
        with open(path, 'r') as f:
            return [line.strip() for line in f.readlines()]


def load(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]
