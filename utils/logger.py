"""Logger module for the object detection program.

Contains a logger class to provide logging functionality.

Author: Julius Nick (julius.nick@gmail.com)

"""

import logging
import os
from config import config
from datetime import datetime


class Logger:
    def __init__(self, logging_level, root_dir, logs_path):

        # Set up the logging with level and logfile path
        logging.basicConfig(level=logging_level,
                            filename=os.path.join(root_dir, logs_path))

    def log(self, event):
        logging.info("%s %s", self.current_time(), event)

    @staticmethod
    def current_time():
        """Returns the current timedate."""

        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return now
