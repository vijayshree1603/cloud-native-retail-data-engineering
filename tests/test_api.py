from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from src.database import get_session
from src.models import Base, RetailSale


def test_sales_and_analytics_api():
    from src.config import PROJECT_ROOT
    database_path = PROJECT_ROOT / "data" / "retail_sales_api_test.db"
    database_path.unlink(missing_ok=True)
    engine = create_engine(f"sqlite:///{database_path.as_posix()}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    test_session = sessionmaker(bind=engine)
    with test_session() as session:
        session.add_all([
            RetailSale(order_id=1, order_date=date(2026, 1, 1), customer_id="C1", product_id="P1", category="Electronics", quantity=2, unit_price=Decimal("100"), region="South", payment_method="UPI", total_amount=Decimal("200")),
            RetailSale(order_id=2, order_date=date(2026, 1, 2), customer_id="C2", product_id="P2", category="Clothing", quantity=3, unit_price=Decimal("50"), region="North", payment_method="Card", total_amount=Decimal("150")),
        ])
        session.commit()

    def override_session():
        with test_session() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    try:
        with TestClient(app) as client:
            assert client.get("/health").json() == {"status": "ok", "database": "connected"}
            assert client.get("/api/analytics/total-revenue").json()["value"] == "350.00"
            assert client.get("/api/analytics/total-quantity").json()["value"] == 5
            assert client.get("/api/analytics/average-order-value").json()["value"] == 175.0
            assert client.get("/api/analytics/revenue-by-category").json()[0]["name"] == "Electronics"
            assert client.get("/api/analytics/revenue-by-region").json()[0]["name"] == "South"
            assert client.get("/api/analytics/highest-value-orders").json()[0]["order_id"] == 1
            sales = client.get("/api/sales?limit=1").json()
            assert sales["total"] == 2 and len(sales["items"]) == 1
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
        database_path.unlink(missing_ok=True)
