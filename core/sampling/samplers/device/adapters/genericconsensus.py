from core.sampling.samplers.device.adapters.endpointsampleradapter import EndpointSamplerAdapter
from core.sampling.samplers.device.samplingresults.consensussyncresult import ConsensusSyncResult
from core.sampling.samplers.endpoint.endpointsamplers.endpointsampler import EndpointSampler, DataSample
from core.sampling.samplers.endpoint.samplingresults.genericconsensusresults import EthV1NodeHealthResult, \
    EthV1NodeSyncingResult, EthV1NodeHealthStatus


class SamplerAdapterGenericConsensus(EndpointSamplerAdapter):

    def __init__(self, endpoint_sampler: EndpointSampler) -> None:
        super().__init__(endpoint_sampler)

    def convert_data_sample(self, sample: DataSample) -> ConsensusSyncResult:
        samples = sample.get_samples_list()
        assert len(samples) == 2

        nhr: EthV1NodeHealthResult = samples[0]
        nsr: EthV1NodeSyncingResult = samples[1]

        synced = nhr.get_status() == EthV1NodeHealthStatus.SYNCED and nsr.is_synced()

        return ConsensusSyncResult(synced, nsr.get_sync_progress_percent())
