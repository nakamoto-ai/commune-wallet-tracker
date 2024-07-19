from decimal import Decimal
from typing import List

from app.models.api.transfers import TransferAPIData
from app.models.api.users import UserAPIData
from app.models.db.transfers import Transfer
from app.models.db.users import User
from app.models.graphql.transfers import GraphQLTransfer


def graphql_to_db_transfer(graphql_transfer: GraphQLTransfer) -> Transfer:
    return Transfer(
        id=graphql_transfer.id,
        from_=graphql_transfer.from_,
        to=graphql_transfer.to,
        blockNumber=Decimal(graphql_transfer.blockNumber),
        amount=Decimal(graphql_transfer.amount)
    )


def db_to_api_transfer(transfer_db: Transfer) -> TransferAPIData:
    return TransferAPIData(
        id=transfer_db.id,
        from_=transfer_db.from_,
        to=transfer_db.to,
        amount=transfer_db.amount,
        blockNumber=transfer_db.blockNumber
    )


def db_to_api_user(user_db: User, transfers_db: List[Transfer]) -> UserAPIData:
    return UserAPIData(
        id=user_db.id,
        name=user_db.name,
        transfers=[db_to_api_transfer(t) for t in transfers_db]
    )
