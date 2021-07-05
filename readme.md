# Object Detection with Jetson Nano - Image Annotation System

# Prerequisites

## Installing TensorFlow Lite

From the official guide:
https://www.tensorflow.org/lite/guide/python

    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install python3-tflite-runtime

# Installing the Image Annotation System

1. Clone the repository to the desired location.
2. Adjust the config/config.yml to suit your specific preferences, particularly:
    - paths to the tflite model file and label file
    - input- and output paths
    - the maximum number of objects to detect per image
    - the minimum probability for an object to be considered a detection

# Using the Image Annotation System
## 1. Upload Images

Upload images to the input_images_path specified in the config.yml

## 2. Execute the image annotation for uploaded images

Execute the main.py Python program to run object detection and image annotation for the images in the input_images_path:

    python3 main.py

## 3. Monitor the progress

The progress of the image annotation can be monitored in the logs/detector.log file. To follow the last 100 lines of this log while the system is performing annotations, the following command is helpful:

    tail -f -n 100 logs/detector.log

The logfile shows annotation progress for individual images and informs when all images have been processed.

## 4. Retrieve annotation results

Results of a successful image annotation are saved in the output directories specified in the config.yml and can be retrieved from there.

The two directories are:

- xml_output_path for XML annotation files
- augmented_images_path for augmented copies of the original images

The augmented images contain bounding boxes, the name of the detected object category and the corresponding probability with which the model detected the object.


# Running the Image Annotation System on other hardware

It is possible to run the Image Annotation System on a regular x86 machine without a dedicated GPU. This has successfully been tested on a machine running Windows 10 Student Edition during development. In order to do this, some changes to the code are necessary, in particular the full Tensorflow2 installation contains the required packages to create an instance of the tflite interpreter. The exact steps depend on the particular environment chosen. All relative paths in the project are handled in a way that ensures compatibility with both Windows and Linux path conventions.

# TO-Dos

docstrings

remove print statements for final version

logging
    time the duration of the annotations and show t/image
    start and end
    if its running
    if folder was empty
    etc

unit-tests

