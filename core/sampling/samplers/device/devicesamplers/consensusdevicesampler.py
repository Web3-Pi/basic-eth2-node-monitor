from core.sampling.samplers.device.adapters.endpointsampleradapter import EndpointSamplerAdapter
from core.sampling.samplers.device.devicesamplers.devicesample import DeviceSample
from core.sampling.samplers.device.devicesamplers.devicesampler import DeviceSampler
from core.sampling.samplers.device.devicesamplers.devicesamplertypes import DeviceSamplerType
from core.sampling.samplers.device.samplingresults.consensussyncresult import ConsensusSyncResult
from core.sampling.samplers.device.samplingresults.systemresult import SystemResult


class ConsensusDeviceSample(DeviceSample):
    def __init__(self, consensus_sample: ConsensusSyncResult | None, system_sample: SystemResult | None) -> None:
        super().__init__(DeviceSamplerType.CONSENSUS_ONLY, system_sample)

        self.consensus_sample: ConsensusSyncResult | None = consensus_sample
        self.register_generic_sample(consensus_sample)

    def get_client_sample(self):
        return self.consensus_sample

    def __str__(self):
        return f'{self.__class__.__name__}\n' \
               f'consensus sample {self.consensus_sample}\n' \
               f'system sample {self.system_sample}'


class ConsensusDeviceSampler(DeviceSampler):

    def __init__(self, host_name: str,
                 consensus_sampler: EndpointSamplerAdapter, sys_sampler: EndpointSamplerAdapter) -> None:
        super().__init__(DeviceSamplerType.CONSENSUS_ONLY, host_name, sys_sampler)

        self.consensus_sampler = consensus_sampler

    def sample_device(self) -> DeviceSample:
        return ConsensusDeviceSample(self.consensus_sampler.sample(), self.sample_system_sampler())
