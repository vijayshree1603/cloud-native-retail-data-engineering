# Cloud-Native Retail Data Engineering Platform

An end-to-end retail data engineering pipeline that extracts, validates, transforms, loads, and analyzes retail sales data.

This project demonstrates practical **ETL, data quality validation, SQL analytics, logging, automated testing, and pipeline orchestration**. It is designed as a foundation for building a cloud-native data engineering platform.

---

## Architecture

```text
                    Retail Sales CSV
                           |
                           v
                    +-------------+
                    |   Extract   |
                    |   Pandas    |
                    +------+------+
                           |
                           v
                    +-------------+
                    | Data Quality|
                    |   Checks    |
                    +------+------+
                           |
                         PASS
                           |
                           v
                    +-------------+
                    | Transform   |
                    |   Pandas    |
                    +------+------+
                           |
                           v
                 Processed Retail Data
                           |
                           v
                    +-------------+
                    |    Load     |
                    |   SQLite    |
                    +------+------+
                           |
                           v
                    +-------------+
                    |    SQL      |
                    |  Analytics  |
                    +-------------+
```

---

## Features

* CSV-based retail data ingestion
* Data extraction using Pandas
* Data quality validation
* Missing-value detection
* Duplicate order detection
* Quantity and price validation
* Date validation
* Sales/revenue calculation
* SQLite database loading
* SQL-based business analytics
* Pipeline logging
* Automated unit tests
* Single-command pipeline execution

---

## Technology Stack

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| Python     | ETL and pipeline development       |
| Pandas     | Data processing and transformation |
| SQL        | Data analysis                      |
| SQLite     | Local data storage                 |
| SQLAlchemy | Database connectivity              |
| Pytest     | Automated testing                  |
| Git/GitHub | Version control                    |

---

## Project Structure

```text
cloud-native-retail-data-engineering/
|
+-- data/
|   +-- raw/
|       +-- retail_sales.csv
|
+-- sql/
|   +-- analytics.sql
|
+-- src/
|   +-- __init__.py
|   +-- extract.py
|   +-- data_quality.py
|   +-- transform.py
|   +-- load.py
|   +-- logger.py
|   +-- pipeline.py
|   +-- run_analytics.py
|
+-- tests/
|   +-- __init__.py
|   +-- test_transform.py
|
+-- logs/
+-- README.md
+-- .gitignore
```

---

## ETL Workflow

### 1. Extract

The pipeline reads raw retail sales data from:

```text
data/raw/retail_sales.csv
```

Pandas loads the CSV into a DataFrame.

### 2. Data Quality

The pipeline validates:

* Required columns
* Missing values
* Duplicate order IDs
* Positive quantities
* Positive unit prices
* Valid order dates

The pipeline stops if validation fails.

### 3. Transform

The transformation stage:

* Converts order dates to datetime
* Removes duplicate orders
* Sorts records by order date
* Calculates total order value

```text
total_amount = quantity × unit_price
```

### 4. Load

The transformed data is loaded into a SQLite database:

```text
data/retail_sales.db
```

Table:

```text
retail_sales
```

### 5. Analytics

SQL queries calculate:

* Total revenue
* Revenue by category
* Revenue by region
* Total quantity sold
* Average order value
* Highest-value orders

---

## Sample Results

Using the sample dataset:

| Metric              |      Result |
| ------------------- | ----------: |
| Orders processed    |          10 |
| Total quantity sold |          27 |
| Total revenue       |    ₹372,850 |
| Average order value |     ₹37,285 |
| Top category        | Electronics |
| Top region          |       South |

### Revenue by Category

| Category    |  Revenue |
| ----------- | -------: |
| Electronics | ₹330,000 |
| Furniture   |  ₹29,000 |
| Clothing    |  ₹10,800 |
| Groceries   |   ₹3,050 |

### Revenue by Region

| Region |  Revenue |
| ------ | -------: |
| South  | ₹292,200 |
| West   |  ₹58,250 |
| East   |  ₹17,000 |
| North  |   ₹5,400 |

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/vijayshree1603/cloud-native-retail-data-engineering.git
cd cloud-native-retail-data-engineering
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install pandas sqlalchemy pytest
```

### 4. Run the complete pipeline

```bash
python src/pipeline.py
```

The pipeline executes:

```text
Extract
   ↓
Data Quality
   ↓
Transform
   ↓
Load
   ↓
SQL Analytics
```

---

## Testing

Run:

```bash
pytest
```

Current tests verify:

* Total amount calculation
* Duplicate order removal

Expected result:

```text
2 passed
```

---

## Logging

Pipeline execution is logged to:

```text
logs/pipeline.log
```

The log records:

* Pipeline start
* Individual pipeline stages
* Successful completion
* Pipeline failures

---

## Future Cloud-Native Architecture

The current implementation provides the local foundation for a cloud-native data platform.

Planned architecture:

```text
Retail Data Sources
        |
        v
Cloud Object Storage
        |
        v
Data Lake
        |
        v
Cloud ETL / Data Processing
        |
        v
Cloud Data Warehouse
        |
        +----------------+
        |                |
        v                v
   SQL Analytics     Power BI
```

Planned improvements include:

* AWS S3 / Azure Data Lake
* Cloud ETL services
* Cloud data warehouse
* Apache Airflow
* Docker
* CI/CD
* Data pipeline monitoring
* Power BI dashboards

---

## Learning Outcomes

This project demonstrates practical experience with:

* ETL pipeline development
* Data cleaning
* Data validation
* Python data engineering
* SQL analytics
* Relational databases
* Pipeline automation
* Logging
* Unit testing
* Git and GitHub
* Cloud-native data architecture concepts

---

## Author

**S Vijayshree**



GitHub:
https://github.com/vijayshree1603
