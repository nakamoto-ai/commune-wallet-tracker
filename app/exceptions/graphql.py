from requests import Response


class GraphQLException(Exception):
    def __init__(self, function_name: str, status_code: int, json_response: Response):
        super().__init__(f"GraphQL request failed with {status_code} status code")
        self.function_name = function_name
        self.status_code = status_code
        self.json_response = json_response
        self.response_error = self.json_response['errors'][0]['message']

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}: GraphQL function '{self.function_name}' " +
            f"failed: {self.args[0]}: {self.response_error}"
        )
