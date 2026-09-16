from pydantic import BaseModel
from typing import Optional

class AddressCreate(BaseModel):
    label: str
    location: dict
    is_default: bool = False

class AddressOut(BaseModel):
    id: int
    label: str
    location: dict
    is_default: bool

    class Config:
        from_attributes = True