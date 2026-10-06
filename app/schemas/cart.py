from pydantic import BaseModel, Field
from typing import List, Optional

class CartItemAdd(BaseModel):
    menu_item_id: int
    quantity: int = Field(1, ge=1)
    portion_name: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "menu_item_id": 1,
                "quantity": 2,
                "portion_name": "Full"
            }
        }

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

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
    portion_name: Optional[str] = None
    item_total: float

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "menu_item_id": 1,
                "name": "Butter Chicken",
                "price": 320.0,
                "quantity": 2,
                "portion_name": "Full",
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
                        "portion_name": "Full",
                        "item_total": 640.0
                    }
                ],
                "subtotal": 640.0,
                "delivery_fee": 40.0,
                "taxes": 32.0,
                "total": 712.0
            }
        }