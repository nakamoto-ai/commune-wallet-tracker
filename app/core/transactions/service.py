from typing import List

from app.core.graphql.client import GraphQLClient
from app.db.queries import Queries
from app.models.api.users import UserAPIData
from app.models.utils.conversion import graphql_to_db_transfer, db_to_api_user


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
            user_api_data = db_to_api_user(
                user_db=u,
                transfers_db=await self.db_query.get_transfers_for_user(u.id)
            )

            data.append(user_api_data)

        return data
