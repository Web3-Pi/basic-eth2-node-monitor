from typing import Any

import websocket

from core.sampling.readers.interfaces.datareader import DataReader


class WebSocketReader(DataReader):

    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        self.ws: websocket.WebSocket | None = None

    def _connected_guard(self) -> bool:
        if self.ws is None:
            try:
                self.ws = websocket.WebSocket()
                self.ws.connect(self.endpoint_url)
            except Exception as ex:
                # print("_CG", ex)
                self.ws = None

        return self.ws is not None

    def _query_ws(self, msg: str) -> Any:
        self.ws.send(msg)
        return self.ws.recv()

    def query_data(self, args: str | None = None) -> Any:
        res = None
        if self._connected_guard():
            assert args is not None
            try:
                res = self._query_ws(args)
            except Exception as ex:
                # print("_QD", ex)
                self.ws = None

        return res

    def get_data_source(self) -> str:
        return self.endpoint_url
