import logging
import os


LOG_DIRECTORY = "logs"
LOG_FILE = os.path.join(LOG_DIRECTORY, "pipeline.log")


def get_logger():
    """Create and return the pipeline logger."""

    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger("retail_pipeline")