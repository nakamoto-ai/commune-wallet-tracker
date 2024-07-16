import argparse
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.db.base import Base
from app.models.db.wallets import ColdWallet
from app.models.db.users import User

from app.db.connection import SessionLocal


async def insert_cold_wallets(session: AsyncSession, wallet_addresses: list):
    for address in wallet_addresses:
        wallet = ColdWallet(ss58=address)
        session.add(wallet)
    await session.commit()


async def main(wallet_file: str):
    async with SessionLocal() as session:
        try:
            with open(wallet_file, 'r') as f:
                wallet_addresses = [line.strip() for line in f.readlines()]
            await insert_cold_wallets(session, wallet_addresses)
            print(f"Inserted {len(wallet_addresses)} cold wallet addresses.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert wallet addresses into the cold_wallets table.")
    parser.add_argument("--wallet_file", type=str, help="The file containing the list of cold wallet addresses.")

    args = parser.parse_args()

    asyncio.run(main(args.wallet_file))
