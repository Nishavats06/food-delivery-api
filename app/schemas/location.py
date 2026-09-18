from pydantic import BaseModel
from typing import Optional, List

class AddressLocation(BaseModel):
    formattedAddress: str
    latitude: float
    longitude: float

class LocationResult(BaseModel):
    display_name: str
    latitude: float
    longitude: float

class GeocodeData(BaseModel):
    formattedAddress: str
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    latitude: float
    longitude: float

class GeocodeResponse(BaseModel):
    success: bool
    message: str
    data: GeocodeData

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "success",
                "data": {
                    "formattedAddress": "MG Road, Sonipat, Haryana, India",
                    "addressLine1": "MG Road",
                    "addressLine2": None,
                    "city": "Sonipat",
                    "state": "Haryana",
                    "country": "India",
                    "pincode": "131001",
                    "latitude": 28.9953758,
                    "longitude": 77.0233627
                }
            }
        }

class SearchResultItem(BaseModel):
    formattedAddress: str
    latitude: float
    longitude: float

class SearchResponse(BaseModel):
    success: bool
    message: str
    data: List[SearchResultItem]

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "success",
                "data": [
                    {
                        "formattedAddress": "Sonipat, Haryana, 131001, India",
                        "latitude": 28.9953758,
                        "longitude": 77.0233627
                    }
                ]
            }
        }