"""Inference module for object detection.

Provides methods to run inference with an interpreter and an image.

Author: Julius Nick (julius.nick@gmail.com)

"""

import numpy as np


class Inference:
    @staticmethod
    def set_input_tensor(interpreter, image):
        """Sets the input tensor for inference.

        Args:
            interpreter: instance of the tflite interpreter.
            image: the image for which inference should be run.
        """
        # Get the tensor index of the tensor that should be set (the input tensor)
        tensor_index = interpreter.get_input_details()[0]["index"]
        # Get the actual tensor
        input_tensor = interpreter.tensor(tensor_index)()[0]
        # Set the image as the input
        input_tensor[:, :] = image

    @staticmethod
    def analyze_image(interpreter, image):
        """ Analyzes a preprocessed image using the interpreter and returns the
            output location, output category, output score and the number of detected
            images as a list.

        Args:
            interpreter: instance of the tflite interpreter.
            image: the image for which inference should be run

        """
        Inference.set_input_tensor(interpreter, image)

        interpreter.invoke()
        output_details = interpreter.get_output_details()

        output_location = np.squeeze(
            interpreter.get_tensor(output_details[0]["index"]))

        output_category = np.squeeze(
            interpreter.get_tensor(output_details[1]["index"]))

        output_score = np.squeeze(
            interpreter.get_tensor(output_details[2]["index"]))

        output_freq = np.squeeze(
            interpreter.get_tensor(output_details[3]["index"]))

        return [output_location, output_category, output_score, output_freq]
