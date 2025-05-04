from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from api.dependencies.database import get_db
from api.schemas.order import Order, OrderCreate
from api.schemas.revenue import RevenueResponse
from api.controllers.order import create_order, get_orders, get_order, get_revenue

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order, status_code=201)
def place_order(data: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, data)

@router.get("/", response_model=List[Order])
def read_orders(start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    return get_orders(db, start_date, end_date)

@router.get("/{order_id}", response_model=Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    return get_order(db, order_id)

@router.get("/revenue", response_model=RevenueResponse)
def daily_revenue(date: date, db: Session = Depends(get_db)):
    return get_revenue(db, date)
