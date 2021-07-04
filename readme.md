# Jetson Nano Object Detection



# Installing TensorFlow Lite

From the official guide:
https://www.tensorflow.org/lite/guide/python

    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install python3-tflite-runtime



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

