"""Repository-relative locations used by the pipeline."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "retail_sales.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "retail_sales_transformed.csv"
DATABASE_PATH = PROJECT_ROOT / "data" / "retail_sales.db"
LOG_FILE = PROJECT_ROOT / "logs" / "pipeline.log"
