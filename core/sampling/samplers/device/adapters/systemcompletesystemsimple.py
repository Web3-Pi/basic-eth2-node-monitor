from core.sampling.samplers.device.adapters.endpointsampleradapter import EndpointSamplerAdapter
from core.sampling.samplers.device.samplingresults.systemresult import SystemResult
from core.sampling.samplers.endpoint.endpointsamplers.endpointsampler import EndpointSampler, DataSample
from core.sampling.samplers.endpoint.samplingresults.systemstatusresults import SystemStatusResult


class SamplerAdapterSystemCompleteSystemSimple(EndpointSamplerAdapter):

    def __init__(self, endpoint_sampler: EndpointSampler) -> None:
        super().__init__(endpoint_sampler)

    def convert_data_sample(self, sample: DataSample) -> SystemResult:
        samples = sample.get_samples_list()
        assert len(samples) == 1

        ssr: SystemStatusResult = samples[0]

        return SystemResult(
            ssr.host_name, ssr.num_cores, ssr.cpu_percent, ssr.mem_used, ssr.swap_used, ssr.disk_used,
            cpu_temp=ssr.cpu_temp, net_upload=ssr.net_upload, net_download=ssr.net_download
        )
