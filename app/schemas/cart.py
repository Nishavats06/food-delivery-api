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

    class Config:
        json_schema_extra = {
            "example": {
                "menu_item_id": 1,
                "quantity": 2
            }
        }

class CartItemUpdate(BaseModel):
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "quantity": 3
            }
        }

class CartItemOut(BaseModel):
    id: int
    menu_item_id: int
    name: str
    price: float
    quantity: int
    item_total: float

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "menu_item_id": 1,
                "name": "Butter Chicken",
                "price": 320.0,
                "quantity": 2,
                "item_total": 640.0
            }
        }

class CartOut(BaseModel):
    id: int
    items: List[CartItemOut]
    subtotal: float
    delivery_fee: float
    taxes: float
    total: float

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "items": [
                    {
                        "id": 1,
                        "menu_item_id": 1,
                        "name": "Butter Chicken",
                        "price": 320.0,
                        "quantity": 2,
                        "item_total": 640.0
                    }
                ],
                "subtotal": 640.0,
                "delivery_fee": 40.0,
                "taxes": 32.0,
                "total": 712.0
            }
        }