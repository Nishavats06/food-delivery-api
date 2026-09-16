from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.category import Category

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    address = Column(JSON, nullable=False)
    cuisine_type = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    rating = Column(Float, default=0.0)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    owner = relationship("User")
    category = relationship("Category")