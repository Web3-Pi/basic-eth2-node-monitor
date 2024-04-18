from typing import List

from core.sampling.readers.interfaces.datareader import DataReader
from core.sampling.samplers.endpoint.endpointsamplers.endpointsampler import EndpointSampler, DataSample
from core.sampling.samplers.endpoint.transformers.datatransformer import DataTransformer


class BatchEndpointSampler(EndpointSampler):

    def __init__(self, endpoint_reader: DataReader, queries: List[str], transformers: List[DataTransformer]) -> None:
        assert len(queries) >= 1

        self.endpoint_reader = endpoint_reader
        self.queries = queries

        self.transformers = transformers

    def sample_endpoint(self) -> DataSample:
        res = [None for _ in range(len(self.queries))]

        for i, query in enumerate(self.queries):
            query_res = self.endpoint_reader.query_data(query)

            if query_res is None:
                break

            res[i] = self.transformers[i].transform(query_res)

        return DataSample(res)

    def get_endpoint(self) -> str:
        return self.endpoint_reader.get_data_source()
