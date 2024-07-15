
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.db.base import Base
from sqlalchemy import Column, String

from app.models.db.users import GUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class HotWallet(Base):
    __tablename__ = "hot_wallets"

    ss58 = Column(String, primary_key=True, index=True)
    owner_id = Column(GUID(), ForeignKey('users.id'), nullable=False, index=True)

    owner = relationship("User", back_populates="hot_wallets")


class ColdWallet(Base):
    __tablename__ = "cold_wallets"

    ss58 = Column(String, primary_key=True, index=True)
