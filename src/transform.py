import pandas as pd

RAW_DATA_PATH = "data/raw/retail_sales.csv"
PROCESSED_DATA_PATH = "data/processed/retail_sales_transformed.csv"


def transform_data(df):
    """Clean and transform retail sales data."""

    # Convert order_date to datetime
    df["order_date"] = pd.to_datetime(df["order_date"])

    # Calculate total sales for each order
    df["total_amount"] = df["quantity"] * df["unit_price"]

    # Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"])

    # Sort by order date
    df = df.sort_values("order_date")

    return df


def main():
    # Extract
    df = pd.read_csv(RAW_DATA_PATH)

    print("Raw data loaded successfully!")
    print(f"Rows before transformation: {len(df)}")

    # Transform
    transformed_df = transform_data(df)

    print("\nTransformation completed!")
    print(f"Rows after transformation: {len(transformed_df)}")

    print("\nTransformed data:")
    print(transformed_df.head())

    # Save transformed data
    transformed_df.to_csv(PROCESSED_DATA_PATH, index=False)

    print(f"\nTransformed data saved to: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()