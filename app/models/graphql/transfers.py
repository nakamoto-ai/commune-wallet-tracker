from dataclasses import dataclass
from typing import List, Dict, Iterator


@dataclass
class GraphQLTransfer:
    id: str
    from_: str  # 'from' is a reserved keyword, so use 'from_'
    to: str
    blockNumber: str  # BigFloat type in GraphQL, use str for no precision loss.
    amount: str  # BigFloat type in GraphQL, use str for no precision loss.

    @classmethod
    def from_json(cls, json: dict) -> 'GraphQLTransfer':
        return cls(
            id=json["id"],
            from_=json["from"],
            to=json["to"],
            blockNumber=json["blockNumber"],
            amount=json["amount"]
        )


@dataclass
class GraphQLTransfersResponse:
    nodes: List[GraphQLTransfer]

    @classmethod
    def from_json(cls, json_data: Dict[str, List[Dict]]) -> 'GraphQLTransfersResponse':
        return cls(
            nodes=[GraphQLTransfer.from_json(node) for node in json_data["data"]["transfers"]["nodes"]]
        )

    def __iter__(self) -> Iterator[GraphQLTransfer]:
        return iter(self.nodes)
