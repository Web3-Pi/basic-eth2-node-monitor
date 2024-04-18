from __future__ import annotations

from queue import Queue
from typing import List

from core.sampling.samplers.node.nodesampler import NodeSampler
from core.sampling.samplingunit.factoryhelpers.nodesamplersfactory import node_sampler_from_descriptor
from core.sampling.samplingunit.threading.nodesamplingthread import NodeSamplingThread
from core.sampling.samplingunit.threading.waitpolicy import WaitPolicy, WaitPolicyDefault


class SamplingUnitThreaded:

    def __init__(self, wait_policy: WaitPolicy, node_samplers: List[NodeSampler]) -> None:
        self.queue = Queue()
        self.node_sampling_threads: List[NodeSamplingThread] = []

        for node_sampler in node_samplers:
            self.node_sampling_threads.append(NodeSamplingThread(node_sampler, wait_policy, self.queue))

    def start(self) -> Queue:
        print(f"SamplingUnitThreaded: Starting {len(self.node_sampling_threads)} threads")
        for th in self.node_sampling_threads:
            th.start()

        return self.queue

    def shutdown(self) -> None:
        print(f"SamplingUnitThreaded: Shutting down {len(self.node_sampling_threads)} threads")
        for th in self.node_sampling_threads:
            th.shutdown()

    @classmethod
    def create(cls, wait_active: float, wait_degraded: float, *node_descriptors) -> SamplingUnitThreaded:
        return SamplingUnitThreaded(
            WaitPolicyDefault(wait_active, wait_degraded),
            [node_sampler_from_descriptor(descr) for descr in node_descriptors]
        )
