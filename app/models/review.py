from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    restaurant = relationship("Restaurant")

    __table_args__ = (UniqueConstraint("user_id", "restaurant_id", name="unique_user_restaurant_review"),)