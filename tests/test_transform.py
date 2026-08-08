import pandas as pd

from src.transform import transform_data


def create_test_data():
    """Create sample retail data for testing."""

    return pd.DataFrame({
        "order_id": [2, 1, 1],
        "order_date": [
            "2026-01-02",
            "2026-01-01",
            "2026-01-01"
        ],
        "customer_id": ["C002", "C001", "C001"],
        "product_id": ["P002", "P001", "P001"],
        "category": [
            "Clothing",
            "Electronics",
            "Electronics"
        ],
        "quantity": [3, 2, 2],
        "unit_price": [1200, 1000, 1000],
        "region": ["North", "South", "South"],
        "payment_method": [
            "Credit Card",
            "UPI",
            "UPI"
        ]
    })


def test_total_amount_calculation():
    """Test that total_amount is calculated correctly."""

    data = create_test_data()

    result = transform_data(data)

    order = result[result["order_id"] == 1].iloc[0]

    assert order["total_amount"] == 2000


def test_duplicate_orders_are_removed():
    """Test that duplicate order IDs are removed."""

    data = create_test_data()

    result = transform_data(data)

    assert len(result) == 2
    assert result["order_id"].nunique() == 2


def test_order_date_is_converted_to_datetime():
    """Test that order_date is converted to datetime."""

    data = create_test_data()

    result = transform_data(data)

    assert pd.api.types.is_datetime64_any_dtype(
        result["order_date"]
    )


def test_data_is_sorted_by_order_date():
    """Test that transformed data is sorted by order date."""

    data = create_test_data()

    result = transform_data(data)

    assert result["order_date"].is_monotonic_increasing


def test_multiple_rows_are_transformed_correctly():
    """Test transformation across multiple orders."""

    data = create_test_data()

    result = transform_data(data)

    assert result.iloc[0]["order_id"] == 1
    assert result.iloc[0]["total_amount"] == 2000
    assert result.iloc[1]["order_id"] == 2
    assert result.iloc[1]["total_amount"] == 3600