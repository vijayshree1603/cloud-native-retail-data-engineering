import pandas as pd

RAW_DATA_PATH = "data/raw/retail_sales.csv"


def extract_data():
    """Extract retail sales data from the raw CSV file."""
    df = pd.read_csv(RAW_DATA_PATH)

    print("Data extracted successfully!")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())

    return df


if __name__ == "__main__":
    extract_data()