import requests
import inspect

from app.core.graphql.query import GraphQLQueryLoader

from app.exceptions.graphql import GraphQLException

from app.models.graphql.transfers import GraphQLTransfersResponse
from app.models.graphql.query import GraphQLQuery


class GraphQLClient:
    def __init__(self, url: str, headers: dict, query_loader: GraphQLQueryLoader):
        self.url = url
        self.headers = headers
        self.query_loader = query_loader

    def _fetch_data(self, graphql_query: GraphQLQuery, variables: dict):
        response = requests.post(
            url=self.url,
            json={'query': graphql_query.query, 'variables': variables},
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise GraphQLException(
                function_name=graphql_query.name,
                status_code=response.status_code,
                json_response=response.json()
            )

    def fetch_transfers(self, wallet_address: str, block_number: str) -> GraphQLTransfersResponse:
        variables = {
            "walletAddress": wallet_address,
            "blockNumber": block_number
        }

        return GraphQLTransfersResponse.from_json(
            json_data=self._fetch_data(
                graphql_query=self.query_loader.load_get_transfers_query(),
                variables=variables
            )
        )
