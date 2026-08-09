"""Data extraction for the retail sales pipeline."""

import pandas as pd

from src.config import RAW_DATA_PATH
from src.storage import get_raw_data_path
from src.logger import get_logger


def extract_data(path=None):
    """Read and return retail sales data from a CSV file."""
    path = str(get_raw_data_path() if path is None else path)
    try:
        dataframe = pd.read_csv(path)
    except (FileNotFoundError, pd.errors.ParserError, UnicodeDecodeError) as error:
        get_logger().exception("Extraction failed for %s", path)
        raise RuntimeError(f"Unable to read raw data from {path}: {error}") from error

    get_logger().info("Extracted %s rows and %s columns from %s", len(dataframe), len(dataframe.columns), path)
    print(f"Extracted {len(dataframe)} rows and {len(dataframe.columns)} columns from {path}")
    return dataframe


if __name__ == "__main__":
    extract_data()
