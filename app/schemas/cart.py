from pydantic import BaseModel, field_validator
from typing import List

class CartItemAdd(BaseModel):
    menu_item_id: int
    quantity: int = 1

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        return value

class CartItemUpdate(BaseModel):
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        return value

class CartItemOut(BaseModel):
    id: int
    menu_item_id: int
    name: str
    price: float
    quantity: int
    item_total: float

class CartOut(BaseModel):
    id: int
    items: List[CartItemOut]
    subtotal: float
    delivery_fee: float
    taxes: float
    total: float