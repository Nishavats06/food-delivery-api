from pydantic import BaseModel
from typing import Optional
from app.schemas.location import AddressLocation

class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: AddressLocation
    cuisine_type: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[AddressLocation] = None
    cuisine_type: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class RestaurantOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    address: AddressLocation
    cuisine_type: Optional[str] = None
    image_url: Optional[str] = None
    rating: float
    owner_id: int
    category_id: Optional[int] = None

    class Config:
        from_attributes = True