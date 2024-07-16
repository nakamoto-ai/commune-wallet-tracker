import asyncio
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
import uvicorn

from app.db.connection import init_db, SessionLocal
from app.api.routes import router as api_router
from app.core.transactions.service import TransactionService
from app.dependencies import get_transaction_service

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))


async def background_task(transaction_service: TransactionService):
    try:
        while True:
            await transaction_service.sync_transactions()
            await asyncio.sleep(300)  # Wait for a second before running again
    except asyncio.CancelledError:
        print("Background task cancelled")


@asynccontextmanager
async def lifespan(api: FastAPI):
    await init_db()
    async with SessionLocal() as session:
        transaction_service = get_transaction_service(session)
        task = asyncio.create_task(background_task(transaction_service))
        yield
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

api = FastAPI(lifespan=lifespan)
api.include_router(api_router)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


def start():
    uvicorn.run(
        "app.main:api",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["./app"]
    )


if __name__ == "__main__":
    start()
