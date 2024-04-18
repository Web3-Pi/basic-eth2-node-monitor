from abc import ABC, abstractmethod
from typing import List


class DataSample:

    def __init__(self, samples: List) -> None:
        self.samples = samples

    def get_samples_list(self) -> List:
        return self.samples

    def __str__(self):
        res = "["

        for i in range(len(self.samples) - 1):
            res += f"{self.samples[i]}, "

        if len(self.samples) >= 1:
            res += f"{self.samples[-1]}"

        res += "]"

        return res


class EndpointSampler(ABC):

    @abstractmethod
    def sample_endpoint(self) -> DataSample:
        pass

    @abstractmethod
    def get_endpoint(self) -> str:
        pass
