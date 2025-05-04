from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderBase(BaseModel):
    customer_name: str
    phone: str
    address: str
    order_type: str | None = None
    promo_code: str | None = None

class OrderCreate(OrderBase):
    items: List[OrderItemBase]

class Order(OrderBase):
    id: int
    status: str
    total: float
    created_at: datetime
    items: List[OrderItemBase]
    class Config:
        orm_mode = True
