from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_available = Column(Boolean, default=True)

    restaurant = relationship("Restaurant")
    category = relationship("Category")