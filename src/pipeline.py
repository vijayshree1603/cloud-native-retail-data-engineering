"""Run the extract, validate, transform, load, and analytics workflow."""

import sys

from src.data_quality import validate_data
from src.extract import extract_data
from src.load import load_data
from src.logger import get_logger
from src.run_analytics import run_analytics
from src.transform import save_transformed_data, transform_data


def main():
    """Execute the complete ETL flow; return a shell-compatible status code."""
    logger = get_logger()
    logger.info("Pipeline started")
    try:
        raw_data = extract_data()
        if not validate_data(raw_data):
            raise ValueError("Data quality validation failed; pipeline stopped before transformation.")
        transformed_data = transform_data(raw_data)
        save_transformed_data(transformed_data)
        load_data(transformed_data)
        run_analytics()
    except Exception as error:
        logger.exception("Pipeline failed: %s", error)
        print(f"Pipeline failed: {error}", file=sys.stderr)
        return 1

    logger.info("Pipeline completed successfully")
    print("Pipeline completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
