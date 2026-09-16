from pydantic import BaseModel
from typing import Optional, Any

class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: dict
    cuisine_type: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[dict] = None
    cuisine_type: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class RestaurantOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    address: Any
    cuisine_type: Optional[str] = None
    image_url: Optional[str] = None
    rating: float
    owner_id: int
    category_id: Optional[int] = None

    class Config:
        from_attributes = True