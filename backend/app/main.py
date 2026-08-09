"""FastAPI REST API for retail sales and analytics."""

import os
from contextlib import asynccontextmanager
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.schemas import (
    ErrorResponse, HealthResponse, HighestValueOrder, MetricResponse,
    OrderResponse, RevenueBreakdown, SalesPage,
)
from src.database import get_session
from src.models import RetailSale


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="Cloud-Native Retail Analytics API",
    version="1.0.0",
    description="REST access to ETL-loaded retail sales and analytics.",
    lifespan=lifespan,
)
origins = [item.strip() for item in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if item.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(SQLAlchemyError)
async def database_error_handler(_: Request, __: SQLAlchemyError):
    return JSONResponse(status_code=503, content={"detail": "Database service is unavailable."})


def scalar_or_zero(session: Session, statement):
    return session.scalar(statement) or Decimal("0")


@app.get("/health", response_model=HealthResponse, responses={503: {"model": ErrorResponse}})
def health(session: Session = Depends(get_session)):
    session.execute(text("SELECT 1"))
    return HealthResponse()


@app.get("/api/sales", response_model=SalesPage, responses={503: {"model": ErrorResponse}})
def list_sales(
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    total = session.scalar(select(func.count()).select_from(RetailSale)) or 0
    rows = session.scalars(select(RetailSale).order_by(RetailSale.order_date.desc(), RetailSale.order_id.desc()).offset(offset).limit(limit)).all()
    return SalesPage(items=rows, total=total, limit=limit, offset=offset)


@app.get("/api/analytics/total-revenue", response_model=MetricResponse)
def total_revenue(session: Session = Depends(get_session)):
    return MetricResponse(value=scalar_or_zero(session, select(func.sum(RetailSale.total_amount))))


@app.get("/api/analytics/total-quantity", response_model=MetricResponse)
def total_quantity(session: Session = Depends(get_session)):
    return MetricResponse(value=scalar_or_zero(session, select(func.sum(RetailSale.quantity))))


@app.get("/api/analytics/average-order-value", response_model=MetricResponse)
def average_order_value(session: Session = Depends(get_session)):
    return MetricResponse(value=scalar_or_zero(session, select(func.avg(RetailSale.total_amount))))


def revenue_breakdown(session: Session, field):
    rows = session.execute(select(field, func.sum(RetailSale.total_amount)).group_by(field).order_by(func.sum(RetailSale.total_amount).desc())).all()
    return [RevenueBreakdown(name=name, revenue=revenue) for name, revenue in rows]


@app.get("/api/analytics/revenue-by-category", response_model=list[RevenueBreakdown])
def revenue_by_category(session: Session = Depends(get_session)):
    return revenue_breakdown(session, RetailSale.category)


@app.get("/api/analytics/revenue-by-region", response_model=list[RevenueBreakdown])
def revenue_by_region(session: Session = Depends(get_session)):
    return revenue_breakdown(session, RetailSale.region)


@app.get("/api/analytics/highest-value-orders", response_model=list[HighestValueOrder])
def highest_value_orders(limit: int = Query(5, ge=1, le=100), session: Session = Depends(get_session)):
    rows = session.execute(select(RetailSale.order_id, RetailSale.customer_id, RetailSale.category, RetailSale.total_amount).order_by(RetailSale.total_amount.desc()).limit(limit)).all()
    return [HighestValueOrder(order_id=row.order_id, customer_id=row.customer_id, category=row.category, total_amount=row.total_amount) for row in rows]
