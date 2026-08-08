import sqlite3

import pandas as pd

from src import pipeline
from src.config import PROJECT_ROOT
from src.load import load_data
from src.run_analytics import run_analytics


def sample_data():
    return pd.DataFrame({
        "order_id": [1, 2],
        "order_date": ["2026-01-01", "2026-01-02"],
        "customer_id": ["C1", "C2"],
        "product_id": ["P1", "P2"],
        "category": ["Electronics", "Clothing"],
        "quantity": [2, 3],
        "unit_price": [100, 50],
        "region": ["South", "North"],
        "payment_method": ["UPI", "Card"],
        "total_amount": [200, 150],
    })


def test_load_creates_and_verifies_retail_sales_table():
    database_path = PROJECT_ROOT / "data" / "retail_sales_test.db"
    database_path.unlink(missing_ok=True)
    assert load_data(sample_data(), database_path) == 2
    with sqlite3.connect(database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM retail_sales").fetchone()[0] == 2

    results = run_analytics(database_path)
    assert results["total_revenue"] == [(350,)]
    assert results["total_quantity"] == [(5,)]


def test_pipeline_stops_when_quality_validation_fails(monkeypatch):
    calls = []
    monkeypatch.setattr(pipeline, "extract_data", lambda: sample_data())
    monkeypatch.setattr(pipeline, "validate_data", lambda _: False)
    monkeypatch.setattr(pipeline, "transform_data", lambda _: calls.append("transform"))
    monkeypatch.setattr(pipeline, "load_data", lambda _: calls.append("load"))
    monkeypatch.setattr(pipeline, "run_analytics", lambda: calls.append("analytics"))

    assert pipeline.main() == 1
    assert calls == []
