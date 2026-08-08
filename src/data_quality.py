"""Data quality checks for retail sales data."""

import pandas as pd

from src.config import RAW_DATA_PATH
from src.logger import get_logger

REQUIRED_COLUMNS = [
    "order_id", "order_date", "customer_id", "product_id", "category",
    "quantity", "unit_price", "region", "payment_method",
]


def validate_data(dataframe):
    """Return ``True`` only when the dataset meets the required quality rules."""
    logger = get_logger()
    errors = []
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]
    if missing_columns:
        logger.error("Data quality failure: missing columns: %s", missing_columns)
        print("Data quality check: FAILED")
        return False

    missing_values = dataframe[REQUIRED_COLUMNS].isna().sum().sum()
    if missing_values:
        errors.append(f"missing values: {missing_values}")

    duplicate_orders = dataframe["order_id"].duplicated().sum()
    if duplicate_orders:
        errors.append(f"duplicate order IDs: {duplicate_orders}")

    quantities = pd.to_numeric(dataframe["quantity"], errors="coerce")
    invalid_quantity = (quantities.isna() | (quantities <= 0)).sum()
    if invalid_quantity:
        errors.append(f"invalid quantities: {invalid_quantity}")

    prices = pd.to_numeric(dataframe["unit_price"], errors="coerce")
    invalid_prices = (prices.isna() | (prices <= 0)).sum()
    if invalid_prices:
        errors.append(f"invalid unit prices: {invalid_prices}")

    invalid_dates = pd.to_datetime(dataframe["order_date"], errors="coerce").isna().sum()
    if invalid_dates:
        errors.append(f"invalid order dates: {invalid_dates}")

    if errors:
        for error in errors:
            logger.error("Data quality failure: %s", error)
        print("Data quality check: FAILED")
        return False

    logger.info("Data quality check passed for %s rows", len(dataframe))
    print("Data quality check: PASSED")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if validate_data(pd.read_csv(RAW_DATA_PATH)) else 1)
