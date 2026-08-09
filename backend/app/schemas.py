"""Explicit API response models."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MetricResponse(BaseModel):
    value: Decimal | int | float = 0


class RevenueBreakdown(BaseModel):
    name: str
    revenue: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id: int
    order_date: date
    customer_id: str
    product_id: str
    category: str
    quantity: int
    unit_price: Decimal
    region: str
    payment_method: str
    total_amount: Decimal


class HighestValueOrder(BaseModel):
    order_id: int
    customer_id: str
    category: str
    total_amount: Decimal


class SalesPage(BaseModel):
    items: list[OrderResponse]
    total: int
    limit: int
    offset: int


class HealthResponse(BaseModel):
    status: str = "ok"
    database: str = "connected"


class ErrorResponse(BaseModel):
    detail: str = Field(description="Human-readable error message")
