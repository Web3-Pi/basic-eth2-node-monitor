from core.sampling.samplers.device.adapters.endpointsampleradapter import EndpointSamplerAdapter
from core.sampling.samplers.device.samplingresults.consensussyncresult import ConsensusSyncResult
from core.sampling.samplers.endpoint.endpointsamplers.endpointsampler import EndpointSampler, DataSample
from core.sampling.samplers.endpoint.samplingresults.lighthouseresults import LighthouseEth1SyncingResult, \
    LighthouseSyncingResult


class SamplerAdapterLighthouseConsensus(EndpointSamplerAdapter):

    def __init__(self, endpoint_sampler: EndpointSampler) -> None:
        super().__init__(endpoint_sampler)

    def convert_data_sample(self, sample: DataSample) -> ConsensusSyncResult:
        samples = sample.get_samples_list()
        assert len(samples) == 2

        lesr: LighthouseEth1SyncingResult = samples[0]
        lsr: LighthouseSyncingResult = samples[1]

        sync_percent = lesr.get_eth1_node_sync_status_percentage()

        return ConsensusSyncResult(lsr.is_synced() and sync_percent == 100.0, sync_percent)
