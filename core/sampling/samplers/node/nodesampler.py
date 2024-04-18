from typing import List

from core.sampling.samplers.device.devicesamplers.devicesample import DeviceSample
from core.sampling.samplers.device.devicesamplers.devicesampler import DeviceSampler
from core.sampling.samplers.node.nodesamplingresultbuilder import NodeSamplingResultBuilder
from core.sampling.samplers.node.results.nodesamplingresult import NodeSamplingResult


class NodeSampler:

    def __init__(self, name: str, *device_samplers: DeviceSampler) -> None:
        self.name = name
        self.device_samplers = device_samplers

    def _sample_node(self) -> List[DeviceSample]:
        return [sampler.sample_device() for sampler in self.device_samplers]

    def sample_node(self) -> NodeSamplingResult:
        return NodeSamplingResultBuilder.create(self.name, *self._sample_node())

    def get_node_name(self) -> str:
        return self.name
