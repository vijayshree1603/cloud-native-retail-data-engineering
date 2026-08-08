"""Transformation and persistence of validated retail sales data."""

import pandas as pd

from src.config import PROCESSED_DATA_PATH, RAW_DATA_PATH
from src.logger import get_logger


def transform_data(dataframe):
    """Return cleaned data with parsed dates and calculated order totals."""
    dataframe = dataframe.copy()
    dataframe["order_date"] = pd.to_datetime(dataframe["order_date"])
    dataframe["total_amount"] = dataframe["quantity"] * dataframe["unit_price"]
    return dataframe.drop_duplicates(subset=["order_id"]).sort_values("order_date")


def save_transformed_data(dataframe, path=PROCESSED_DATA_PATH):
    """Write transformed data to CSV, creating its output directory if needed."""
    path = path if hasattr(path, "parent") else pd.io.common.stringify_path(path)
    from pathlib import Path
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False)
    get_logger().info("Saved %s transformed rows to %s", len(dataframe), path)
    return path


def main():
    raw_data = pd.read_csv(RAW_DATA_PATH)
    transformed_data = transform_data(raw_data)
    save_transformed_data(transformed_data)
    print(f"Transformed {len(transformed_data)} rows to {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()
