from core.sampling.readers.impl.jsonreaderwrapper import JSONWrappedResponse
from core.sampling.samplers.endpoint.transformers.datatransformer import DataTransformer
from core.sampling.samplers.endpoint.samplingresults.gethresults import EthSyncingResult, EthBlockNumberResult


class GethDataTransformerSyncing(DataTransformer):
    def transform(self, res: JSONWrappedResponse) -> EthSyncingResult:
        data = res.json
        if not data["result"]:
            return EthSyncingResult(None)
        else:
            return EthSyncingResult(data["result"])


class GethDataTransformerBlockNumber(DataTransformer):

    def transform(self, res: JSONWrappedResponse) -> EthBlockNumberResult:
        return EthBlockNumberResult(res.json["result"])
