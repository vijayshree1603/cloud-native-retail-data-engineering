import pandas as pd

from src.transform import transform_data


def test_total_amount_calculation():
    """Test that total_amount is calculated correctly."""

    data = pd.DataFrame({
        "order_id": [1],
        "order_date": ["2026-01-01"],
        "customer_id": ["C001"],
        "product_id": ["P001"],
        "category": ["Electronics"],
        "quantity": [2],
        "unit_price": [1000],
        "region": ["South"],
        "payment_method": ["UPI"]
    })

    result = transform_data(data)

    assert result.iloc[0]["total_amount"] == 2000


def test_duplicate_orders_are_removed():
    """Test that duplicate order IDs are removed."""

    data = pd.DataFrame({
        "order_id": [1, 1],
        "order_date": ["2026-01-01", "2026-01-01"],
        "customer_id": ["C001", "C001"],
        "product_id": ["P001", "P001"],
        "category": ["Electronics", "Electronics"],
        "quantity": [2, 2],
        "unit_price": [1000, 1000],
        "region": ["South", "South"],
        "payment_method": ["UPI", "UPI"]
    })

    result = transform_data(data)

    assert len(result) == 1