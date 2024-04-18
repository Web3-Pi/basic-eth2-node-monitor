from typing import Any

import requests

from core.sampling.readers.interfaces.datareader import DataReader


class HTTPReader(DataReader):

    def __init__(self, endpoint_url: str):
        assert not endpoint_url.endswith("/")

        self.endpoint_url = endpoint_url

    def _query_str(self, args: str | None) -> str:
        if args is not None:
            assert args.startswith("/")

            query = f"{self.endpoint_url}{args}"
        else:
            query = self.endpoint_url

        return query

    def query_data(self, args: str | None = None) -> Any:
        try:
            query = self._query_str(args)
            res = requests.get(query)
            if res:
                return res
        except Exception:
            pass

        return None

    def get_data_source(self) -> str:
        return self.endpoint_url
