from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.models.api.transfers import TransferAPIData


class UserAPIData(BaseModel):
    id: UUID
    name: str
    transfers: List[TransferAPIData]
