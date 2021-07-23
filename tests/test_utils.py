"""Unit tests for the utils module.

Performs the specified unit tests.

Author: Julius Nick (julius.nick@gmail.com)

"""

import os
import unittest

import cv2
import numpy as np

from utils import image_loader
from utils import image_transformer


class TestImageTransformer(unittest.TestCase):

    def test_image_transformer(self):
        """Test that the image transformer transforms image dimensions as
        expected.
        """
        small_image = 255 * np.ones(shape=[50, 80, 3], dtype=np.uint8)
        large_image = 255 * np.ones(shape=[70, 100, 3], dtype=np.uint8)
        target_shape = (small_image.shape[1], small_image.shape[0])
        transformed_image = image_transformer.Transformer.resize(
            large_image, target_shape)
        self.assertEqual(small_image.shape, transformed_image.shape)


class TestImageLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource_path = os.path.normpath("tests/resources/temp")
        cls.test_image = 255 * np.ones(shape=[50, 80, 3], dtype=np.uint8)
        cv2.imwrite(os.path.join(cls.resource_path,
                    "test_image_1.png"), cls.test_image)
        cv2.imwrite(os.path.join(cls.resource_path,
                    "test_image_2.png"), cls.test_image)

    @classmethod
    def tearDownClass(cls):
        cls.resource_path = os.path.normpath("tests/resources/temp")
        os.remove(os.path.join(cls.resource_path, "test_image_1.png"))
        os.remove(os.path.join(cls.resource_path, "test_image_2.png"))

    def test_image_loader(self):
        """Test that the image loader creates the expected image queue."""
        queue = image_loader.ImageLoader.get_img_queue(self.resource_path)
        expected_queue = ["test_image_1.png", "test_image_2.png"]
        self.assertEqual(queue, expected_queue)


if __name__ == "__main__":
    unittest.main()
