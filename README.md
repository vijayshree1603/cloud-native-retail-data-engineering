# 🛒 Cloud-Native Retail Data Engineering Platform

<p align="center">
  <strong>End-to-end ETL pipeline for retail sales data with data quality validation, SQL analytics, automated testing, and CI/CD.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas" />
  <img src="https://img.shields.io/badge/SQLAlchemy-Database-red" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite" />
  <img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?logo=githubactions" />
</p>

---

## 📌 What is this project?

This project is a **retail data engineering pipeline** that takes raw sales data and turns it into clean, validated, and analytics-ready data.

The pipeline performs:

**Extract → Validate → Transform → Load → Analyze**

It demonstrates practical concepts used in real-world data engineering projects, including:

- ETL pipeline development
- Data quality checks
- Data transformation
- Relational database loading
- SQL analytics
- Automated testing
- Logging
- Git/GitHub
- GitHub Actions CI

---

# 🏗️ Architecture

```text
                ┌─────────────────────┐
                │  Retail Sales CSV   │
                │   Raw Data Source   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │      EXTRACT        │
                │       Pandas        │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   DATA QUALITY      │
                │       CHECKS        │
                └──────────┬──────────┘
                           │
                      PASS │
                           ▼
                ┌─────────────────────┐
                │     TRANSFORM       │
                │  Clean + Calculate  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │        LOAD         │
                │ SQLite + SQLAlchemy │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     ANALYTICS       │
                │        SQL          │
                └─────────────────────┘
✨ Key Features
Feature	Description
📥 Data Extraction	Reads retail sales CSV using Pandas
🔍 Data Quality	Validates columns, missing values, duplicates, quantity, price and dates
🔄 Transformation	Cleans data and calculates total order value
💾 Database Loading	Loads transformed data into SQLite using SQLAlchemy
📊 SQL Analytics	Calculates revenue, quantity, AOV and category/region performance
🧪 Automated Testing	Pytest tests for transformation logic
📝 Logging	Records pipeline execution and failures
🤖 CI/CD	GitHub Actions automatically runs tests
📦 Dependency Management	Uses requirements.txt
🔄 ETL Pipeline
1️⃣ Extract

Raw data is stored in:

data/raw/retail_sales.csv

The pipeline loads the data using Pandas.

Example:

Rows: 10
Columns: 9
2️⃣ Data Quality Validation

Before processing the data, the pipeline performs validation checks.

Current checks
✓ Required columns
✓ Missing values
✓ Duplicate order IDs
✓ Quantity values
✓ Unit prices
✓ Order dates

Example:

DATA QUALITY CHECK: PASSED

If validation fails, the pipeline stops instead of processing invalid data.

3️⃣ Transform

The transformation stage:

Removes duplicate orders
Converts order dates
Sorts records
Calculates total order value
Business calculation
total_amount = quantity × unit_price

Example:

Quantity   = 2
Unit Price = ₹45,000

Total Amount = ₹90,000
4️⃣ Load

The transformed data is loaded into:

SQLite Database
      ↓
data/retail_sales.db
      ↓
retail_sales table

SQLAlchemy is used for database connectivity.

5️⃣ Analyze

SQL queries generate business insights such as:

💰 Total revenue
📦 Total quantity sold
🧾 Average order value
🏷️ Revenue by category
🌍 Revenue by region
🥇 Highest-value orders
📊 Sample Results

The current sample dataset contains 10 orders.

Metric	Result
🧾 Orders processed	10
📦 Quantity sold	27
💰 Total revenue	₹372,850
🛍️ Average order value	₹37,285
🥇 Top category	Electronics
📍 Top region	South
💰 Revenue by Category
Category	Revenue
🔌 Electronics	₹330,000
🛋️ Furniture	₹29,000
👕 Clothing	₹10,800
🛒 Groceries	₹3,050

Electronics generates the highest revenue.

🌍 Revenue by Region
Region	Revenue
🟢 South	₹292,200
🔵 West	₹58,250
🟡 East	₹17,000
🔴 North	₹5,400

South is the highest-performing region.

🧰 Tech Stack
Python 3.12
│
├── Pandas
├── SQLAlchemy
├── SQLite
├── SQL
├── Pytest
├── Git
├── GitHub
└── GitHub Actions
Technology	Used For
🐍 Python	Pipeline development
🐼 Pandas	Data processing
🔗 SQLAlchemy	Database connectivity
🗄️ SQLite	Data storage
🧮 SQL	Analytics
🧪 Pytest	Testing
🌐 GitHub	Version control
⚙️ GitHub Actions	Continuous integration
📁 Project Structure
cloud-native-retail-data-engineering/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
│   └── raw/
│       └── retail_sales.csv
│
├── sql/
│   └── analytics.sql
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── data_quality.py
│   ├── transform.py
│   ├── load.py
│   ├── logger.py
│   ├── pipeline.py
│   └── run_analytics.py
│
├── tests/
│   ├── __init__.py
│   └── test_transform.py
│
├── requirements.txt
├── .gitignore
└── README.md

Generated files such as:

.venv/
__pycache__/
.pytest_cache/
logs/
data/processed/
data/*.db

are excluded from Git using .gitignore.

🚀 Run the Project
1. Clone
git clone https://github.com/vijayshree1603/cloud-native-retail-data-engineering.git
cd cloud-native-retail-data-engineering
2. Create virtual environment
python -m venv .venv
3. Activate
Windows
.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Run the pipeline
python -m src.pipeline

The pipeline executes:

Extract
   ↓
Data Quality
   ↓
Transform
   ↓
Load
   ↓
SQL Analytics
🧪 Testing

Run:

pytest -v

Current tests verify:

✓ Total amount calculation
✓ Duplicate order removal

Expected:

2 passed
🤖 Continuous Integration

This project uses GitHub Actions to automatically test the project.

Whenever code is pushed to main or a pull request is created:

        Git Push
           │
           ▼
    GitHub Actions
           │
           ▼
     Python 3.12
           │
           ▼
Install requirements.txt
           │
           ▼
       Run Pytest
           │
           ▼
      ✅ CI Passed

Workflow:

.github/workflows/ci.yml
📝 Logging

Pipeline logs are written to:

logs/pipeline.log

The logging system records:

Pipeline execution
Pipeline stages
Successful completion
Errors/failures

Logs are intentionally excluded from Git.

☁️ Future Cloud Architecture

The current project runs locally using:

CSV → Python → SQLite → SQL

The next stage is to migrate the architecture toward cloud infrastructure.

                 Retail Data Sources
                         │
                         ▼
                ☁️ Cloud Object Storage
                         │
                         ▼
                    Data Lake
                         │
                         ▼
                Cloud ETL Processing
                         │
                         ▼
               Cloud Data Warehouse
                    │          │
                    ▼          ▼
               SQL Analytics  Power BI
Planned improvements
☁️ AWS S3 / Azure Data Lake
⚙️ AWS Glue / Azure Data Factory
🗄️ Cloud Data Warehouse
🔄 Apache Airflow
🐳 Docker
📊 Power BI dashboard
📈 Pipeline monitoring
🔐 Cloud security
🚀 Automated deployment

These are future enhancements. The current implementation is a local Python-based data engineering pipeline.

🎯 Learning Outcomes

Through this project, I gained practical experience in:

Building ETL pipelines
Data cleaning and validation
Pandas data processing
SQL analytics
Relational databases
SQLAlchemy
Automated testing
Pipeline logging
Git/GitHub
GitHub Actions
Cloud-native architecture concepts
👩‍💻 Author
S Vijayshree

B.E. Information Science & Engineering

🔗 Connect
GitHub: https://github.com/vijayshree1603
LinkedIn: https://www.linkedin.com/in/vijayshree-selva-214092297/
<p align="center"> ⭐ If you found this project useful, consider giving it a star! </p> ```