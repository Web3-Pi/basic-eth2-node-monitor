from core.sampling.readers.impl.jsonreaderwrapper import JSONWrappedResponse
from core.sampling.samplers.endpoint.transformers.datatransformer import DataTransformer
from core.sampling.samplers.endpoint.samplingresults.genericconsensusresults import EthV1NodeHealthResult, EthV1NodeSyncingResult


class GenericConsensusDataTransformerHealth(DataTransformer):
    def transform(self, res: JSONWrappedResponse) -> EthV1NodeHealthResult:
        return EthV1NodeHealthResult(res.status_code)


class GenericConsensusDataTransformerSyncing(DataTransformer):
    def transform(self, res: JSONWrappedResponse) -> EthV1NodeSyncingResult:
        return EthV1NodeSyncingResult(res.json["data"])
