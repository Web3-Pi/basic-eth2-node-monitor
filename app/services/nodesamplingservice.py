from __future__ import annotations

from app.appdescr.applicationdescriptor import ApplicationDescriptor
from core.sampling.samplers.node.results.nodesamplingresult import NodeSamplingResult
from core.sampling.samplingunit.samplingunitthreaded import SamplingUnitThreaded


class NodeSamplingService:

    def __init__(self, sampling_unit: SamplingUnitThreaded) -> None:
        self.sampling_unit = sampling_unit
        self.q = None

    def start(self) -> None:
        if self.q is None:
            self.q = self.sampling_unit.start()

    def wait_for_sample(self) -> NodeSamplingResult:
        assert self.q is not None
        return self.q.get()

    def shutdown(self):
        print("NodeSamplingService: shutting down")
        self.sampling_unit.shutdown()

    @classmethod
    def create(cls, app_descr: ApplicationDescriptor) -> NodeSamplingService:
        sampling_unit = SamplingUnitThreaded.create(
            app_descr.wait_delay.delay_active,
            app_descr.wait_delay.delay_degraded,
            *app_descr.nodes
        )

        return NodeSamplingService(sampling_unit)
