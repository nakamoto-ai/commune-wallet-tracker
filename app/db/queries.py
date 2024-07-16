from decimal import Decimal
from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.models.db.transfers import Transfer
from app.models.db.users import User
from app.models.db.wallets import HotWallet, ColdWallet


class Queries:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def insert_transaction(self, tx: Transfer) -> Transfer:
        self.db.add(tx)
        await self.db.commit()
        await self.db.refresh(tx)
        return tx

    async def select_latest_block_number(self) -> Decimal:
        result = await self.db.execute(select(func.max(Transfer.blockNumber)))
        largest_block_number: Union[Decimal, None] = result.scalar_one_or_none()
        return largest_block_number if largest_block_number is not None else Decimal(0)

    async def get_all_owners(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_wallets_for_user(self, user_id: str) -> List[HotWallet]:
        result = await self.db.execute(select(HotWallet).filter_by(owner_id=user_id))
        return result.scalars().all()

    async def get_transfers_for_wallets(self, wallet_addresses: List[str]) -> List[Transfer]:
        result = await self.db.execute(select(Transfer).filter(Transfer.from_.in_(wallet_addresses)))
        return result.scalars().all()

    async def get_transfers_for_user(self, user_id: str) -> List[Transfer]:
        wallets = await self.get_wallets_for_user(user_id)
        wallet_addresses = [wallet.ss58 for wallet in wallets]
        return await self.get_transfers_for_wallets(wallet_addresses)

    async def get_all_cold_wallets(self) -> List[ColdWallet]:
        result = await self.db.execute(select(ColdWallet))
        return result.scalars().all()
