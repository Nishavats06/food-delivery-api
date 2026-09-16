import enum
from sqlalchemy import Column, Integer, String, Enum
from app.db.session import Base

class UserRole(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    profile_picture_url = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)