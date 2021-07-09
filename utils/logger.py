"""Logger module for the object detection program.

Contains a logger class to provide logging functionality.

Author: Julius Nick (julius.nick@gmail.com)

"""

import logging
import os
from datetime import datetime


class Logger:
    """A class that provides functionality to log events to a logfile."""
    def __init__(self, logging_level, root_dir, logs_path):
        """Set up the logging with level and logfile path.

        Args:
            logging_level: the logging level set in the config.yml
            root_dir: the project root set in the config.yml
            logs_path: the path where to write the logfile set in the config.yml
        """
        logging.basicConfig(level=logging_level,
                            filename=os.path.join(root_dir, logs_path))

    def log(self, event):
        """Logs an event.

        Args:
            event: the event that should be logged
        """
        logging.info("%s %s", self.current_time(), event)

    @staticmethod
    def current_time():
        """Returns the current timedate."""
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return now
