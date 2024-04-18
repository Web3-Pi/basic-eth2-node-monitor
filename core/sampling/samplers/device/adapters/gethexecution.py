from core.sampling.samplers.device.adapters.endpointsampleradapter import EndpointSamplerAdapter
from core.sampling.samplers.device.samplingresults.executionsyncresult import ExecutionSyncResult
from core.sampling.samplers.endpoint.endpointsamplers.endpointsampler import EndpointSampler, DataSample
from core.sampling.samplers.endpoint.samplingresults.gethresults import EthSyncingResult, EthBlockNumberResult


class SamplerAdapterGethExecution(EndpointSamplerAdapter):

    def __init__(self, endpoint_sampler: EndpointSampler) -> None:
        super().__init__(endpoint_sampler)

    def convert_data_sample(self, sample: DataSample) -> ExecutionSyncResult:
        samples = sample.get_samples_list()
        assert len(samples) == 2

        esr: EthSyncingResult = samples[0]
        ebnr: EthBlockNumberResult = samples[1]

        if esr.is_synced():
            res = ExecutionSyncResult(True, ebnr.get_block_number(), 100.0)
        else:
            res = ExecutionSyncResult(False, ebnr.get_block_number(), esr.sync_percent())

        if not res.synced:
            if esr.get_current_block() != ebnr.get_block_number():
                print("WARNING: Geth not synced; block numbers mismatch; but maybe it should be "
                      "mismatched during syncing")

        return res
