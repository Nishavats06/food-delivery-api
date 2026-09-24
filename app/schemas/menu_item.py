from pydantic import BaseModel, field_validator
from typing import Optional, List


class Portion(BaseModel):
    name: str
    price: float


class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_available: bool = True
    portions: Optional[List[Portion]] = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Butter Chicken",
                "description": "Creamy tomato-based curry with tender chicken",
                "price": 320.0,
                "image_url": None,
                "category_id": None,
                "is_available": True,
                "portions": [
                    {"name": "Half", "price": 180.0},
                    {"name": "Full", "price": 320.0}
                ]
            }
        }


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_available: Optional[bool] = None
    portions: Optional[List[Portion]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "price": 350.0,
                "is_available": True
            }
        }


class MenuItemOut(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_available: bool
    portions: Optional[List[Portion]] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "restaurant_id": 1,
                "name": "Butter Chicken",
                "description": "Creamy tomato-based curry with tender chicken",
                "price": 320.0,
                "image_url": None,
                "category_id": None,
                "is_available": True,
                "portions": [
                    {"name": "Half", "price": 180.0},
                    {"name": "Full", "price": 320.0}
                ]
            }
        }