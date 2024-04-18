from abc import ABC, abstractmethod

from core.sampling.samplers.node.results.nodesamplingresult import NodeSamplingResult


class WaitPolicy(ABC):

    @abstractmethod
    def get_current_delay(self, sample: NodeSamplingResult) -> float:
        pass


class WaitPolicyDefault(WaitPolicy):

    def __init__(self, active_delay_secs: float, degraded_delay_secs: float) -> None:
        self.active_wait = active_delay_secs
        self.degraded_wait = degraded_delay_secs

    def get_current_delay(self, sample: NodeSamplingResult) -> float:
        if sample.represents_active_node():
            return self.active_wait
        else:
            return self.degraded_wait
