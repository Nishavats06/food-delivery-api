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

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ravi's Kitchen",
                "description": "Best North Indian food in town",
                "address": {
                    "formattedAddress": "MG Road, Sonipat, Haryana, India",
                    "latitude": 28.9953758,
                    "longitude": 77.0233627
                },
                "cuisine_type": "North Indian",
                "image_url": "https://res.cloudinary.com/ha7wup79/image/upload/v1790415799/uploads/obwk7bx1efblwa3mcddy.png",
                "category_id": None
            }
        }

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[AddressLocation] = None
    cuisine_type: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ravi's Kitchen Updated",
                "description": "Now serving South Indian too",
                "cuisine_type": "Multi-cuisine",
                "image_url": "https://res.cloudinary.com/ha7wup79/image/upload/v1790415799/uploads/obwk7bx1efblwa3mcddy.png"
            }
        }

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
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Ravi's Kitchen",
                "description": "Best North Indian food in town",
                "address": {
                    "formattedAddress": "MG Road, Sonipat, Haryana, India",
                    "latitude": 28.9953758,
                    "longitude": 77.0233627
                },
                "cuisine_type": "North Indian",
                "image_url": "https://res.cloudinary.com/ha7wup79/image/upload/v1790415799/uploads/obwk7bx1efblwa3mcddy.png",
                "rating": 4.5,
                "owner_id": 3,
                "category_id": None
            }
        }


        
# from pydantic import BaseModel
# from typing import Optional
# from app.schemas.location import AddressLocation

# class RestaurantCreate(BaseModel):
#     name: str
#     description: Optional[str] = None
#     address: AddressLocation
#     cuisine_type: Optional[str] = None
#     category_id: Optional[int] = None

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "name": "Ravi's Kitchen",
#                 "description": "Best North Indian food in town",
#                 "address": {
#                     "formattedAddress": "MG Road, Sonipat, Haryana, India",
#                     "latitude": 28.9953758,
#                     "longitude": 77.0233627
#                 },
#                 "cuisine_type": "North Indian",
#                 "image_url": None,
#                 "category_id": None
#             }
#         }

# class RestaurantUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     address: Optional[AddressLocation] = None
#     cuisine_type: Optional[str] = None
#     image_url: Optional[str] = None
#     category_id: Optional[int] = None

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "name": "Ravi's Kitchen Updated",
#                 "description": "Now serving South Indian too",
#                 "cuisine_type": "Multi-cuisine",
#                 "image_url": "https://res.cloudinary.com/ha7wup79/image/upload/v123/uploads/abc.png"
#             }
#         }

# class RestaurantOut(BaseModel):
#     id: int
#     name: str
#     description: Optional[str] = None
#     address: AddressLocation
#     cuisine_type: Optional[str] = None
#     image_url: Optional[str] = None
#     rating: float
#     owner_id: int
#     category_id: Optional[int] = None

# class Config:
#     from_attributes = True
#     json_schema_extra = {
#         "example": {
#             "id": 1,
#             "name": "Ravi's Kitchen",
#             "description": "Best North Indian food in town",
#             "address": {
#                 "formattedAddress": "MG Road, Sonipat, Haryana, India",
#                 "latitude": 28.9953758,
#                 "longitude": 77.0233627
#             },
#             "cuisine_type": "North Indian",
#             "image_url": "https://res.cloudinary.com/ha7wup79/image/upload/v123/uploads/abc.png",
#             "rating": 4.5,
#             "owner_id": 3,
#             "category_id": None
#         }
#     }
