
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus
from app.schemas.location import AddressLocation

class OrderCreate(BaseModel):
    address_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "address_id": 1
            }
        }

class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "menu_item_id": 1,
                "name": "Butter Chicken",
                "price": 320.0,
                "quantity": 2
            }
        }

class OrderOut(BaseModel):
    id: int
    restaurant_id: int
    delivery_address: AddressLocation
    status: OrderStatus
    subtotal: float
    delivery_fee: float
    taxes: float
    total: float
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "restaurant_id": 1,
                "delivery_address": {
                    "formattedAddress": "MG Road, Sonipat, Haryana, India",
                    "latitude": 28.9953758,
                    "longitude": 77.0233627
                },
                "status": "PLACED",
                "subtotal": 640.0,
                "delivery_fee": 40.0,
                "taxes": 32.0,
                "total": 712.0,
                "created_at": "2026-09-16T10:30:00Z",
                "items": [
                    {
                        "id": 1,
                        "menu_item_id": 1,
                        "name": "Butter Chicken",
                        "price": 320.0,
                        "quantity": 2
                    }
                ]
            }
        }

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

    class Config:
        json_schema_extra = {
            "example": {
                "status": "CONFIRMED"
            }
        }


# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime
# from app.models.order import OrderStatus

# class OrderCreate(BaseModel):
#     address_id: int

# class OrderItemOut(BaseModel):
#     id: int
#     menu_item_id: int
#     name: str
#     price: float
#     quantity: int

#     class Config:
#         from_attributes = True

# class OrderOut(BaseModel):
#     id: int
#     restaurant_id: int
#     delivery_address: dict
#     status: OrderStatus
#     subtotal: float
#     delivery_fee: float
#     taxes: float
#     total: float
#     created_at: datetime
#     items: List[OrderItemOut]

#     class Config:
#         from_attributes = True

# class OrderStatusUpdate(BaseModel):
#     status: OrderStatus