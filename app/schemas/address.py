from pydantic import BaseModel
from app.schemas.location import AddressLocation

class AddressCreate(BaseModel):
    label: str
    location: AddressLocation
    is_default: bool = False

class AddressOut(BaseModel):
    id: int
    label: str
    location: AddressLocation
    is_default: bool

    class Config:
        from_attributes = True