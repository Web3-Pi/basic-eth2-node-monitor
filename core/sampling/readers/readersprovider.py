from core.sampling.readers.impl.jsonreaderwrapper import JSONReaderWrapper
from core.sampling.readers.interfaces.datareader import DataReader
from core.sampling.readers.impl.http_reader import HTTPReader
from core.sampling.readers.impl.websocket_reader import WebSocketReader


class ReadersProvider:

    @classmethod
    def geth_http_reader(cls) -> DataReader:
        assert False, "TODO: implement"
        pass

    @classmethod
    def geth_websocket_reader(cls, endpoint_url) -> DataReader:
        return JSONReaderWrapper(WebSocketReader(endpoint_url))

    @classmethod
    def json_http_reader(cls, endpoint_url) -> DataReader:
        return JSONReaderWrapper(HTTPReader(endpoint_url))
