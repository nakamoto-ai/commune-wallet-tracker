from fastapi import Depends
from app.db.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.transactions.service import TransactionService
from app.core.graphql.client import GraphQLClient
from app.core.graphql.query import GraphQLQueryLoader
from app.core.graphql.client import GraphQLClient

from app.core.constants.http import HEADER_CONTENT_TYPE, APPLICATION_JSON
from app.core.constants.commune import COMMUNE_BLOCKCHAIN_API_URL
from app.db.queries import Queries

graphql_client = GraphQLClient(
    url=COMMUNE_BLOCKCHAIN_API_URL,
    headers={HEADER_CONTENT_TYPE: APPLICATION_JSON},
    query_loader=GraphQLQueryLoader())


def get_transaction_service(db: AsyncSession = Depends(get_db)) -> TransactionService:
    return TransactionService(graphql_client, Queries(db))
