from typing import List, Optional, Tuple, Union

from http_client.http_client import HTTPClient

from housing import models


class ListingsClient:
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8989,
        api_version: str = "v1",
    ):
        self._host: str = host
        self._port: int = port
        self._api_version: str = api_version
        self._base_url = (
            f"http://{self._host}:{self._port}/{self._api_version}/listings"
        )
        self._http_client: HTTPClient = HTTPClient()

    def get(self, id: int) -> models.Listing:
        """
        Get Listings by id.
        """
        url = self._base_url + "/" + str(id)
        r = self._http_client.get(url)
        return models.Listing(**r.json())

    def list(self, offset: int = 0, limit: int = 5) -> List[models.Listing]:
        """
        Get a list of Listings.
        """
        # TODO: make this cleaner
        # TODO: would it be cleaner to use **kwargs?
        #       pro: extensible
        #       con: no suggestions and type hints
        url = self._base_url + self._formatted_query_params(
            [
                ("offset", offset),
                ("limit", limit),
            ]
        )
        r = self._http_client.get(url)
        return [models.Listing(**listing) for listing in r.json()]

    def _formatted_query_params(
        self, params: Optional[List[Tuple[str, Union[str, int]]]]
    ) -> str:
        """
        Example

        params: [("offset": 0), ("limit": 100)]
        return: "?offset=0&limit=100"
        """
        if params:
            query_params = [f"{k}={v}" for k, v in params]
            return "?" + "&".join(query_params)
        return ""
