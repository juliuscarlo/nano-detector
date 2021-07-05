"""Entry point for running the image annotation program.

Executes the individual steps for image annotation sequentially.

Author: Julius Nick (julius.nick@gmail.com)

"""

from model.detector import Detector


def run():
    """Run object detection and image annotation."""
    detector = Detector()
    detector.prepare_model()
    detector.load_images()

    # A queue of images is analyzed image by image sequentially, until empty
    while detector.img_loader.queue:
        detector.preprocess_data()
        detector.run_inference()
        detector.export_results()


if __name__ == "__main__":
    run()
