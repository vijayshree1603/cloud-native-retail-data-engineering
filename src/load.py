import pandas as pd
from sqlalchemy import create_engine, text

PROCESSED_DATA_PATH = "data/processed/retail_sales_transformed.csv"
DATABASE_PATH = "data/retail_sales.db"


def load_data():
    """Load transformed retail data into SQLite database."""

    # Read transformed data
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Create SQLite database connection
    engine = create_engine(f"sqlite:///{DATABASE_PATH}")

    # Load data into database
    df.to_sql(
        "retail_sales",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully!")
    print(f"Rows loaded: {len(df)}")
    print(f"Database: {DATABASE_PATH}")
    print("Table: retail_sales")

    # Verify the loaded data
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM retail_sales")
        )
        count = result.scalar()

    print(f"Rows in database: {count}")


if __name__ == "__main__":
    load_data()