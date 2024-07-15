from decimal import Decimal
from app.models.graphql.transfers import GraphQLTransfer
from app.models.db.transfers import Transfer


def graphql_to_db_transfer(graphql_transfer: GraphQLTransfer) -> Transfer:
    return Transfer(
        id=graphql_transfer.id,
        from_=graphql_transfer.from_,
        to=graphql_transfer.to,
        blockNumber=Decimal(graphql_transfer.blockNumber),
        amount=Decimal(graphql_transfer.amount)
    )
