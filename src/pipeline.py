import subprocess
import sys

from src.logger import get_logger
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

logger = get_logger()


def run_step(script):
    """Run a pipeline step and log its status."""

    print(f"\n{'=' * 60}")
    print(f"Running: {script}")
    print("=" * 60)

    logger.info(f"Starting step: {script}")

    result = subprocess.run(
        [sys.executable, script],
        check=False
    )

    if result.returncode != 0:
        logger.error(f"Step failed: {script}")
        print(f"\nPipeline failed at: {script}")
        sys.exit(result.returncode)

    logger.info(f"Step completed: {script}")
    print(f"\nCompleted: {script}")


def main():
    print("\n" + "=" * 60)
    print("RETAIL DATA ENGINEERING PIPELINE")
    print("=" * 60)

    logger.info("Pipeline started")

    run_step("src/extract.py")
    run_step("src/data_quality.py")
    run_step("src/transform.py")
    run_step("src/load.py")
    run_step("src/run_analytics.py")

    logger.info("Pipeline completed successfully")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()