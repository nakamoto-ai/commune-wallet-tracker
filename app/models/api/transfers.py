from decimal import Decimal

from pydantic import BaseModel


class TransferAPIData(BaseModel):
    id: str
    from_: str
    to: str
    amount: Decimal
    blockNumber: int
