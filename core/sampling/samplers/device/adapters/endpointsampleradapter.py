from abc import abstractmethod, ABC

from core.sampling.samplers.endpoint.endpointsamplers.endpointsampler import EndpointSampler, DataSample


class EndpointSamplerAdapter(ABC):

    def __init__(self, endpoint_sampler: EndpointSampler) -> None:
        self.endpoint_sampler = endpoint_sampler

    def sample(self):
        sample = self.endpoint_sampler.sample_endpoint()

        if self.is_active(sample):
            return self.convert_data_sample(sample)
        else:
            return None

    @staticmethod
    def is_active(sample: DataSample) -> bool:
        return all(s is not None for s in sample.samples)

    @abstractmethod
    def convert_data_sample(self, sample: DataSample):
        pass
