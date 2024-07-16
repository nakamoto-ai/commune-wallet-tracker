from typing import List

from app.core.graphql.client import GraphQLClient
from app.db.queries import Queries
from app.models.api.users import UserAPIData
from app.models.api.transfers import TransferAPIData
from app.models.utils.conversion import graphql_to_db_transfer


class TransactionService:
    def __init__(self, graphql_client: GraphQLClient, db_query: Queries):
        self.graphql_client = graphql_client
        self.db_query = db_query

    async def sync_transactions(self):
        cold_wallets = await self.db_query.get_all_cold_wallets()

        latest_block_number = await self.db_query.select_latest_block_number()
        print(f"Block Number of Last Transaction: {latest_block_number}")

        for cold_wallet in cold_wallets:
            print(f"Querying TX for {cold_wallet.ss58}")
            graphql_transfers = self.graphql_client.fetch_transfers(
                wallet_address=cold_wallet.ss58,
                block_number=str(latest_block_number))

            for tx in graphql_transfers:
                db_tx = graphql_to_db_transfer(tx)
                inserted_tx = await self.db_query.insert_transaction(db_tx)
                print(f"Transaction inserted: {inserted_tx}")

    async def get_transactions(self) -> List[UserAPIData]:
        users = await self.db_query.get_all_owners()

        data: List[UserAPIData] = []
        for u in users:
            transfers_db = await self.db_query.get_transfers_for_user(u.id)

            transfer_api_data = [TransferAPIData(
                id=t.id,
                from_=t.from_,
                to=t.to,
                amount=t.amount,
                blockNumber=t.blockNumber
            ) for t in transfers_db]

            user_api_data = UserAPIData(
                id=u.id,
                name=u.name,
                transfers=transfer_api_data
            )

            data.append(user_api_data)

        return data
