from sqlalchemy import Column, String, Numeric

from app.models.db.base import Base


class Transfer(Base):
    __tablename__ = 'transfers'

    id = Column(String, primary_key=True)
    from_ = Column(String, nullable=False)
    to = Column(String, nullable=False)
    blockNumber = Column(Numeric, nullable=False)
    amount = Column(Numeric, nullable=False)
