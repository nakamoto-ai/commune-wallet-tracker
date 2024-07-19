from fastapi import APIRouter, Depends

from app.core.transactions.service import TransactionService
from app.dependencies import get_transaction_service

router = APIRouter()


@router.get("/")
async def transfers(tx: TransactionService = Depends(get_transaction_service)):
    return await tx.get_transactions()
