from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from app.models.user import UserRole

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    password: str
    role: UserRole = UserRole.CUSTOMER

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Ravi",
                "last_name": "Sharma",
                "email": "ravi.sharma@example.com",
                "phone_number": "9876543210",
                "password": "securepass123",
                "role": "CUSTOMER"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "ravi.sharma@example.com",
                "password": "securepass123"
            }
        }

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    profile_picture_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Ravi",
                "last_name": "Sharma",
                "phone_number": "9876543210",
                "profile_picture_url": "https://res.cloudinary.com/ha7wup79/image/upload/v1790415799/uploads/obwk7bx1efblwa3mcddy.png"
            }
        }

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    profile_picture_url: Optional[str] = None
    role: UserRole

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Ravi",
                "last_name": "Sharma",
                "email": "ravi.sharma@example.com",
                "phone_number": "9876543210",
                "profile_picture_url": "https://res.cloudinary.com/ha7wup79/image/upload/v1790415799/uploads/obwk7bx1efblwa3mcddy.png",
                "role": "CUSTOMER"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }