from pydantic import BaseModel
from typing import Optional
from typing import List

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