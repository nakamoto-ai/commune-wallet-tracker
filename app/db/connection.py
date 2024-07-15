from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.db.users import Base

# Include unused imports so database tables are created.
from app.models.db.wallets import HotWallet, ColdWallet
from app.models.db.transfers import Transfer

DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Example using SQLite

# Create engine and session
engine = create_async_engine(DATABASE_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
