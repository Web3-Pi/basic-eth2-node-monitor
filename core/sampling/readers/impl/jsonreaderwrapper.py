import json
from dataclasses import dataclass
from typing import Any, List, Dict

from core.sampling.readers.interfaces.datareader import DataReader


@dataclass
class JSONWrappedResponse:
    status_code: int
    json: Any


class JSONReaderWrapper(DataReader):

    def __init__(self, reader: DataReader) -> None:
        self.reader = reader

    def query_data(self, args: str | None = None) -> JSONWrappedResponse | None:
        res = self.reader.query_data(args)

        if res is not None:
            if isinstance(res, str):
                return JSONWrappedResponse(200, json.loads(res))
            else:
                return JSONWrappedResponse(res.status_code, {} if len(res.content) == 0 else json.loads(res.content))

        return None

    def get_data_source(self) -> str:
        return self.reader.get_data_source()
