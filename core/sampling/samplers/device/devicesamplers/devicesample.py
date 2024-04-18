from abc import ABC, abstractmethod

from core.sampling.samplers.device.devicesamplers.devicesamplertypes import DeviceSamplerType
from core.sampling.samplers.device.samplingresults.systemresult import SystemResult


class DeviceSample(ABC):

    def __init__(self, sampler_type: DeviceSamplerType, system_sample: SystemResult | None) -> None:
        self.sampler_type = sampler_type

        self.system_sample: SystemResult | None = system_sample

        self.all_samples = [system_sample]

    def register_generic_sample(self, sample) -> None:
        self.all_samples.append(sample)

    def represents_active_device(self) -> bool:
        return all([sample is not None for sample in self.all_samples])

    def sample_type(self) -> DeviceSamplerType:
        return self.sampler_type

    def get_system_sample(self) -> SystemResult | None:
        return self.system_sample

    @abstractmethod
    def get_client_sample(self):
        pass
