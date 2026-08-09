"""Database loading and verification for transformed retail data."""

from pathlib import Path

import pandas as pd
from sqlalchemy import inspect, text

from src.config import DATABASE_PATH, PROCESSED_DATA_PATH
from src.database import create_database_engine
from src.logger import get_logger


def load_data(dataframe=None, database_path=DATABASE_PATH, database_url=None):
    """Replace ``retail_sales`` and verify table creation and row count.

    ``database_path`` remains supported for SQLite tests; setting ``database_url``
    enables PostgreSQL and other SQLAlchemy-supported production databases.
    """
    dataframe = pd.read_csv(PROCESSED_DATA_PATH) if dataframe is None else dataframe.copy()
    if dataframe.empty:
        raise ValueError("Refusing to load an empty retail_sales dataset.")

    if database_url is None:
        database_path = Path(database_path)
        database_path.parent.mkdir(parents=True, exist_ok=True)
        database_url = f"sqlite:///{database_path.as_posix()}"
    engine = create_database_engine(database_url)
    try:
        dataframe.to_sql("retail_sales", con=engine, if_exists="replace", index=False)
        if not inspect(engine).has_table("retail_sales"):
            raise RuntimeError("retail_sales table was not created.")
        with engine.connect() as connection:
            row_count = connection.execute(text("SELECT COUNT(*) FROM retail_sales")).scalar_one()
        if row_count != len(dataframe):
            raise RuntimeError(f"Load verification failed: expected {len(dataframe)} rows, found {row_count}.")
    finally:
        engine.dispose()

    get_logger().info("Loaded and verified %s rows in retail_sales at %s", row_count, database_url)
    print(f"Loaded and verified {row_count} rows in retail_sales at {database_url}")
    return row_count


if __name__ == "__main__":
    load_data()
