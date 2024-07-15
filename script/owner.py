import argparse
import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db.base import Base
from app.models.db.users import User
from app.db.connection import SessionLocal
from sqlalchemy import select


async def user_exists(session: AsyncSession, email: str) -> bool:
    result = await session.execute(select(User).filter_by(email=email))
    user = result.scalars().first()
    return user is not None


async def insert_user(session: AsyncSession, name: str, email: str):
    if await user_exists(session, email):
        print(f"User with email {email} already exists.")
        return

    new_user = User(name=name, email=email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    print(f"Inserted user {new_user.name} with email {new_user.email} and id {new_user.id}")


async def main(name: str, email: str):
    async with SessionLocal() as session:
        try:
            await insert_user(session, name, email)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert a new user into the users table.")
    parser.add_argument("--name", type=str, help="The name of the user.")
    parser.add_argument("--email", type=str, help="The email of the user.")

    args = parser.parse_args()

    asyncio.run(main(args.name, args.email))
