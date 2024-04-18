from abc import abstractmethod, ABC

from core.sampling.samplers.device.adapters.endpointsampleradapter import EndpointSamplerAdapter
from core.sampling.samplers.device.devicesamplers.devicesample import DeviceSample
from core.sampling.samplers.device.devicesamplers.devicesamplertypes import DeviceSamplerType


class DeviceSampler(ABC):

    def __init__(self, sampler_type: DeviceSamplerType, host_name: str, sys_sampler: EndpointSamplerAdapter) -> None:
        self.sampler_type = sampler_type
        self.host_name = host_name
        self.sys_sampler = sys_sampler

    def get_host_name(self) -> str:
        return self.host_name

    def sampler_type(self) -> DeviceSamplerType:
        return self.sampler_type

    def sample_system_sampler(self):
        return self.sys_sampler.sample()

    @abstractmethod
    def sample_device(self) -> DeviceSample:
        pass
