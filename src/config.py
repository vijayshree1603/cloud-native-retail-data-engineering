"""Environment-driven settings and repository-relative development defaults."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "retail_sales.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "retail_sales_transformed.csv"
DATABASE_PATH = PROJECT_ROOT / "data" / "retail_sales.db"
LOG_FILE = PROJECT_ROOT / "logs" / "pipeline.log"

# SQLite is deliberately the default to preserve the zero-infrastructure local ETL flow.
# Production deployments set DATABASE_URL to a PostgreSQL SQLAlchemy URL.
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH.as_posix()}")
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local").lower()
RAW_DATA_KEY = os.getenv("RAW_DATA_KEY", "retail_sales.csv")
LOCAL_STORAGE_PATH = Path(os.getenv("LOCAL_STORAGE_PATH", str(RAW_DATA_PATH.parent)))
S3_BUCKET = os.getenv("S3_BUCKET", "")
S3_PREFIX = os.getenv("S3_PREFIX", "raw")
