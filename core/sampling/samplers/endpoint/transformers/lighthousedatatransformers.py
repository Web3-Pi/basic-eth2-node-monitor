from core.sampling.readers.impl.jsonreaderwrapper import JSONWrappedResponse
from core.sampling.samplers.endpoint.transformers.datatransformer import DataTransformer
from core.sampling.samplers.endpoint.samplingresults.lighthouseresults import LighthouseEth1SyncingResult, LighthouseSyncingResult


class LighthouseDataTransformerSyncingEth1(DataTransformer):
    def transform(self, res: JSONWrappedResponse) -> LighthouseEth1SyncingResult:
        return LighthouseEth1SyncingResult(res.json["data"])


class LighthouseDataTransformerSyncing(DataTransformer):
    def transform(self, res: JSONWrappedResponse) -> LighthouseSyncingResult:
        return LighthouseSyncingResult(res.json["data"])
