import os

from core.constants.graphql import GRAPHQL_GET_TRANSFERS

from models.graphql.query import GraphQLQuery


class GraphQLQueryLoader:
    def __init__(self):
        root_path = os.path.abspath(os.curdir)
        graphql_queries_path = "app/graphql_queries"

        self.graphql_path = os.path.join(root_path, graphql_queries_path)

    def _load_query(self, query: str) -> GraphQLQuery:
        query_file = query + ".graphql"
        query_path = os.path.join(self.graphql_path, query_file)

        with open(query_path, 'r') as file:
            return GraphQLQuery(
                name=query,
                query=file.read()
            )

    def load_get_transfers_query(self) -> GraphQLQuery:
        return self._load_query(GRAPHQL_GET_TRANSFERS)
