from core.sampling.readers.impl.jsonreaderwrapper import JSONWrappedResponse
from core.sampling.samplers.endpoint.transformers.datatransformer import DataTransformer
from core.sampling.samplers.endpoint.samplingresults.systemstatusresults import SystemStatusResult


class SystemStatusDataTransformer(DataTransformer):
    def transform(self, res: JSONWrappedResponse) -> SystemStatusResult:
        return SystemStatusResult.from_dict(res.json)
