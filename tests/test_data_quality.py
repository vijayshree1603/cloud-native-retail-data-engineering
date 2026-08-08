import pandas as pd

from src.data_quality import REQUIRED_COLUMNS, validate_data


def valid_data():
    return pd.DataFrame([{
        "order_id": 1, "order_date": "2026-01-01", "customer_id": "C1",
        "product_id": "P1", "category": "Electronics", "quantity": 1,
        "unit_price": 100, "region": "South", "payment_method": "UPI",
    }])


def test_validation_rejects_missing_required_column():
    data = valid_data().drop(columns=["region"])

    assert validate_data(data) is False


def test_validation_rejects_non_numeric_quantity_and_invalid_date():
    data = valid_data()
    data["quantity"] = "unknown"
    data.loc[0, "order_date"] = "not-a-date"

    assert validate_data(data) is False


def test_valid_dataset_passes_quality_checks():
    assert list(valid_data().columns) == REQUIRED_COLUMNS
    assert validate_data(valid_data()) is True
