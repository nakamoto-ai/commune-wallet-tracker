from fastapi import Request
from app.core.transactions.service import TransactionService
from app.core.graphql.client import GraphQLClient
from app.core.graphql.query import GraphQLQueryLoader
from app.core.graphql.client import GraphQLClient

from app.core.constants.http import HEADER_CONTENT_TYPE, APPLICATION_JSON
from app.core.constants.commune import COMMUNE_BLOCKCHAIN_API_URL

graphql_client = GraphQLClient(
    url=COMMUNE_BLOCKCHAIN_API_URL,
    headers={HEADER_CONTENT_TYPE: APPLICATION_JSON},
    query_loader=GraphQLQueryLoader())


def get_transaction_service(request: Request) -> TransactionService:
    return request.app.state.transaction_service
