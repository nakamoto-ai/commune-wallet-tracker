import argparse
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.db.base import Base
from app.models.db.wallets import HotWallet
from app.models.db.users import User

from app.db.connection import SessionLocal
from sqlalchemy import select


async def get_owner_id(session: AsyncSession, owner_name: str):
    result = await session.execute(select(User).filter_by(name=owner_name))
    user = result.scalars().first()
    if user:
        return user.id
    else:
        raise ValueError(f"User with name {owner_name} does not exist.")


async def insert_wallets(session: AsyncSession, owner_id: str, wallet_addresses: list):
    for address in wallet_addresses:
        wallet = HotWallet(ss58=address, owner_id=owner_id)
        session.add(wallet)
    await session.commit()


async def main(owner_name: str, wallet_file: str):
    async with SessionLocal() as session:
        try:
            owner_id = await get_owner_id(session, owner_name)
            with open(wallet_file, 'r') as f:
                wallet_addresses = [line.strip() for line in f.readlines()]
            await insert_wallets(session, owner_id, wallet_addresses)
            print(f"Inserted {len(wallet_addresses)} wallet addresses for owner {owner_name}.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert wallet addresses into the hot_wallets table.")
    parser.add_argument("--owner", type=str, help="The name of the wallet owner.")
    parser.add_argument("--wallet_file", type=str, help="The file containing the list of wallet addresses.")

    args = parser.parse_args()

    asyncio.run(main(args.owner, args.wallet_file))
