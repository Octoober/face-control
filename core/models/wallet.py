from typing import cast
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, func
from core.models.base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = cast(str, Column(String, unique=True))
    balance = cast(int, Column(Numeric(38, 0), default=0))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    pk_user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="wallet")
