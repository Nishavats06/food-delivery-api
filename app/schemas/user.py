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

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"