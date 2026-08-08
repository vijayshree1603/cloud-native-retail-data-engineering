import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "product_id",
    "category",
    "quantity",
    "unit_price",
    "region",
    "payment_method"
]


def validate_data(df):
    """Run data quality checks on retail sales data."""

    print("\n" + "=" * 60)
    print("DATA QUALITY CHECKS")
    print("=" * 60)

    errors = []

    # Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")
    else:
        print("✓ Required columns: PASS")

    # Check missing values
    missing_values = df[REQUIRED_COLUMNS].isnull().sum().sum()

    if missing_values > 0:
        errors.append(f"Missing values found: {missing_values}")
    else:
        print("✓ Missing values: PASS")

    # Check duplicate order IDs
    duplicate_orders = df["order_id"].duplicated().sum()

    if duplicate_orders > 0:
        errors.append(f"Duplicate order IDs found: {duplicate_orders}")
    else:
        print("✓ Duplicate order IDs: PASS")

    # Check quantity
    invalid_quantity = (df["quantity"] <= 0).sum()

    if invalid_quantity > 0:
        errors.append(f"Invalid quantities found: {invalid_quantity}")
    else:
        print("✓ Quantity values: PASS")

    # Check unit price
    invalid_prices = (df["unit_price"] <= 0).sum()

    if invalid_prices > 0:
        errors.append(f"Invalid unit prices found: {invalid_prices}")
    else:
        print("✓ Unit prices: PASS")

    # Check dates
    invalid_dates = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    ).isna().sum()

    if invalid_dates > 0:
        errors.append(f"Invalid dates found: {invalid_dates}")
    else:
        print("✓ Order dates: PASS")

    # Final result
    if errors:
        print("\nDATA QUALITY CHECK: FAILED")

        for error in errors:
            print(f"✗ {error}")

        return False

    print("\nDATA QUALITY CHECK: PASSED")
    return True


if __name__ == "__main__":
    df = pd.read_csv("data/raw/retail_sales.csv")
    validate_data(df)