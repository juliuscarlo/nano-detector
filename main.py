"""Entry point for running the object detection program."""

from model.detector import Detector


def run():
    detector = Detector()
    detector.prepare_model()
    detector.load_images()

    # The queue of images is analyzed one by one, until it is empty.
    while detector.img_loader.queue:
        detector.preprocess_data()
        detector.run_inference()
        detector.export_results()


if __name__ == "__main__":
    run()
