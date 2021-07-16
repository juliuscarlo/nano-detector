"""Entry point for running the image annotation system from the command line.

Executes the specified mode (upload images, check system status, annotate
images, retrieve results) depending on the chosen command line argument.

Author: Julius Nick (julius.nick@gmail.com)

"""

from model.detector import Detector
import argparse
import os


def run():
    """Run the Image Annotation System."""
    detector = Detector()

    # Initialize an ArgumentParser and parse the given arguments
    parser = argparse.ArgumentParser(description="Image Annotation System")
    parser.add_argument("mode", type=str,
                        help="Select the mode, one of: [upload_images, retrieve_results, annotate, view_logs].")
    args = parser.parse_args()

    if args.mode not in ["upload_images", "retrieve_results", "annotate", "view_logs"]:
        print(
            "Invalid mode. Mode must be one of: [upload_images, retrieve_results, annotate, view_logs].")

    if args.mode == "upload_images":
        print("input directory: " + detector.config.input_images_path)

    if args.mode == "retrieve_results":
        print("xml output path (from project root): " +
              detector.config.xml_output_path)
        print("augmented images path (from project root): " +
              detector.config.augmented_images_path)

    if args.mode == "view_logs":
        os.system("tail -f -n 100 logs/detector.log")

    if args.mode == "annotate":
        detector.prepare_model()
        detector.load_images()

        # A queue of images is analyzed image by image sequentially, until empty
        while detector.img_loader.queue:
            detector.preprocess_data()
            detector.run_inference()
            detector.export_results()


if __name__ == "__main__":
    run()
