from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus

class OrderCreate(BaseModel):
    address_id: int

class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    restaurant_id: int
    delivery_address: dict
    status: OrderStatus
    subtotal: float
    delivery_fee: float
    taxes: float
    total: float
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus