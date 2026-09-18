from pydantic import BaseModel
from app.schemas.location import AddressLocation

class AddressCreate(BaseModel):
    label: str
    location: AddressLocation
    is_default: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "label": "Home",
                "location": {
                    "formattedAddress": "Sonipat Bus Stand, NH352A, Sonipat, Haryana, 131001, India",
                    "latitude": 28.9973644,
                    "longitude": 77.0233632
                },
                "is_default": True
            }
        }

class AddressOut(BaseModel):
    id: int
    label: str
    location: AddressLocation
    is_default: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "label": "Home",
                "location": {
                    "formattedAddress": "Sonipat Bus Stand, NH352A, Sonipat, Haryana, 131001, India",
                    "latitude": 28.9973644,
                    "longitude": 77.0233632
                },
                "is_default": True
            }
        }



# from pydantic import BaseModel
# from app.schemas.location import AddressLocation

# class AddressCreate(BaseModel):
#     label: str
#     location: AddressLocation
#     is_default: bool = False

# class AddressOut(BaseModel):
#     id: int
#     label: str
#     location: AddressLocation
#     is_default: bool

#     class Config:
#         from_attributes = True