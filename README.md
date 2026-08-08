# Cloud-Native Retail Data Engineering

A beginner-friendly retail ETL project that turns a CSV extract into validated, analytics-ready SQLite data. It is local by design: the same separation of extract, validate, transform, load, and analytics stages can later be adapted to cloud storage and a managed warehouse.

## Architecture

```text
data/raw/retail_sales.csv
          |
       extract
          |
 data-quality validation
          |
      transform ------> data/processed/retail_sales_transformed.csv
          |
        load
          |
 data/retail_sales.db (retail_sales table)
          |
      SQL analytics
```

The pipeline stops before transformation when validation fails. Repository paths are resolved relative to the source code, so `python -m src.pipeline` works from the repository root on Windows, macOS, and Linux.

## Setup and installation

Requires Python 3.12 or newer.

```bash
git clone https://github.com/vijayshree1603/cloud-native-retail-data-engineering.git
cd cloud-native-retail-data-engineering
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the project

Run the complete ETL flow from the repository root:

```bash
python -m src.pipeline
```

This creates `data/processed/retail_sales_transformed.csv`, replaces the SQLite `retail_sales` table at `data/retail_sales.db`, verifies the table row count, and prints six analytics results. Generated outputs are intentionally ignored by Git.

To run analytics after a successful load:

```bash
python -m src.run_analytics
```

## Data quality checks

Before transformation, the pipeline requires `order_id`, `order_date`, `customer_id`, `product_id`, `category`, `quantity`, `unit_price`, `region`, and `payment_method`.

It rejects missing values, duplicate order IDs, non-numeric or non-positive quantities and unit prices, and unparseable order dates. A failing check returns a non-zero process status and stops the workflow before any output is written.

## SQLite and analytics

`src.load` uses SQLAlchemy to create or replace `retail_sales` and verifies both table existence and loaded row count. `src.run_analytics` checks that the table exists before running SQL for total revenue, revenue by category and region, total quantity, average order value, and the five highest-value orders. The SQL is also available in `sql/analytics.sql`.

## Tests and CI

Run the test suite with:

```bash
python -m pytest -v
```

The tests cover transformations, data-quality rejection, pipeline fail-fast behavior, and a temporary SQLite load-plus-analytics integration flow. GitHub Actions runs the same command on Ubuntu with Python 3.12 for pushes and pull requests targeting `main`.

## Project structure

```text
.github/workflows/ci.yml       GitHub Actions test workflow
data/raw/                      Versioned sample input
sql/analytics.sql              Reference analytics SQL
src/config.py                  Repository-relative paths
src/extract.py                 CSV extraction
src/data_quality.py            Validation rules
src/transform.py               Transform and processed CSV output
src/load.py                    SQLite load and verification
src/run_analytics.py           Analytics execution
src/pipeline.py                End-to-end orchestration
src/logger.py                  Shared UTF-8 file logging
tests/                         Unit and integration tests
```

## Docker

Docker is intentionally not included. The project has no service dependencies, uses a small local CSV and SQLite database, and runs with a single Python command; a container would add setup without improving the workflow. It becomes appropriate when deploying a scheduled job or standardizing execution across a larger team.
