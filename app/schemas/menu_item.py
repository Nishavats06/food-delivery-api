from pydantic import BaseModel, field_validator
from typing import Optional

class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_available: bool = True

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_available: Optional[bool] = None

class MenuItemOut(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_available: bool

    class Config:
        from_attributes = True