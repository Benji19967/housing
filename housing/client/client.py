import json
from typing import List, Optional, Tuple

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

    def _add_query_params(self, params: Optional[List[Tuple[str, str]]]) -> None:
        pass

    def get(self, id: int) -> models.Listing:
        url = self._base_url + "/" + str(id)
        r = self._http_client.get(url)
        return models.Listing(**r.json())

    def list(self, offset: int = 0, limit: int = 100) -> List[models.Listing]:
        # TODO: offset, limit
        url = self._base_url
        r = self._http_client.get(url)
        return [models.Listing(**listing) for listing in r.json()]