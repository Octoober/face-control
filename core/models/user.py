from typing import Optional, cast
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, DateTime, func
from core.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = cast(Optional[str], Column(String, unique=True))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    wallet = relationship("Wallet", back_populates="user", uselist=False)
