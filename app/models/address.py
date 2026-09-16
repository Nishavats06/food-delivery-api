from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    label = Column(String, nullable=False)
    location = Column(JSON, nullable=False)
    is_default = Column(Boolean, default=False)

    user = relationship("User")