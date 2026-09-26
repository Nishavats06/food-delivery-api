from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class ResponseWrapper(BaseModel, Generic[T]):
    success: bool
    message: str = "success"
    data: Optional[T] = None


class ImageUploadOut(BaseModel):
    image_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "https://res.cloudinary.com/ha7wup79/image/upload/v1790415799/uploads/obwk7bx1efblwa3mcddy.png"
            }
        }
#from pydantic import BaseModel,Field
# from typing import TypeVar, Generic, Optional

# T = TypeVar("T")

# class ResponseWrapper(BaseModel, Generic[T]):
#     success: bool
#     message: str = "success"
#     data: Optional[T] = None

# class ImageUploadOut(BaseModel):
#     image_url: str

# class Config:
#         json_schema_extra = {
#             "example": {
#                 "image_url": "https://res.cloudinary.com/ha7wup79/image/upload/v123/uploads/abc.png"
#             }
#         }
