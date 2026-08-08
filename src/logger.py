"""Shared UTF-8 file logger for the pipeline."""

import logging

from src.config import LOG_FILE


def get_logger():
    """Return the configured pipeline logger without duplicating handlers."""
    logger = logging.getLogger("retail_pipeline")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if logger.handlers:
        return logger

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
    logger.addHandler(handler)
    return logger
