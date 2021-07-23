# Object Detection with Jetson Nano - Image Annotation System

## Prerequisites

### Installing TensorFlow Lite

From the official guide:
https://www.tensorflow.org/lite/guide/python

    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install python3-tflite-runtime

## Installing the Image Annotation System

### 1. Clone the repository to the desired location.

### 2. Adjust the config/config.yml to suit your specific preferences, particularly:

    - paths to the tflite model file and label file
    - input- and output paths
    - the maximum number of objects to detect per image
    - the minimum probability for an object to be considered a detection

## Using the Image Annotation System (4 Modes)

The Image Annotation System has 4 modes that can be selected via the command line interface. A single argument selects
the mode.

Run the system using the command:

    python3 main.py [mode]

## 1. Upload Images

Upload images to the input_images_path specified in the config.yml

To check the specified input directory, run in upload_images mode, which will print the specified path:

    python3 main.py upload_images

Place any images to be annotated in this directory.

## 2. Execute the image annotation for uploaded images

To run object detection and image annotation for the images in the input_images_path, run in annotate mode:

    python3 main.py annotate

## 3. Monitor the progress

The progress of the image annotation can be monitored in the logs/detector.log file. To view this log while the system
is performing annotations, use the view_logs mode:

    python3 main.py view_logs

This will show annotation progress for individual images and informs when all images have been processed. Only up to 100
lines of the log file are printed, check the log file manually if you require more lines.

## 4. Retrieve annotation results

Results of a successful image annotation are saved in the output directories specified in the config.yml and can be
retrieved from there.

- xml_output_path for XML annotation files
- augmented_images_path for augmented copies of the original images

The specified paths of these directories can be checked using the retrieve_results mode:

    python3 main.py retrieve_results

# Running the Image Annotation System on other hardware

It is possible to run the Image Annotation System on a regular x86 machine without a dedicated GPU. This has
successfully been tested on a machine running Windows 10 Student Edition during development. In order to do this, some
changes to the code are necessary, in particular the full tensorflow installation contains the required packages to
create an instance of the tflite interpreter. The exact steps depend on the particular environment chosen.

A python environment with tensorflow, opencv-python, pyyaml and numpy is required.

Two changes are required in the detector.py module. First, the import statement needs to be changed, as we no longer
import the tflite runtime. Comment out the import of the tflite runtime and instead import tensorflow:

    import tensorflow as tf

Then the instance of the Interpreter needs to be initialized using the new tensorflow import:

    self.interpreter = tflite.Interpreter(self.config.model_path)

Now you can run the system on other platforms for testing purposes.

Relative paths in the project are handled in a way that ensures compatibility with both Windows and Linux path
conventions.