from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "rating": 5,
                "comment": "Great food, fast delivery!"
            }
        }

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "rating": 4,
                "comment": "Updated my review after second order"
            }
        }

class ReviewOut(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 2,
                "restaurant_id": 1,
                "rating": 5,
                "comment": "Great food, fast delivery!",
                "created_at": "2026-09-16T15:45:00Z"
            }
        }