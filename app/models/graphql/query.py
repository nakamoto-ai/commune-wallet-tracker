from dataclasses import dataclass


@dataclass
class GraphQLQuery:
    name: str
    query: str
