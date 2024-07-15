# app/db/users.py
import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.db.base import Base
from app.models.db.base import GUID


class User(Base):
    __tablename__ = 'users'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    hot_wallets = relationship("HotWallet", back_populates="owner")
