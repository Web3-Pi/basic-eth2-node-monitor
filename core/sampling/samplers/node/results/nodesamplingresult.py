from __future__ import annotations

from dataclasses import dataclass
from typing import List

from core.sampling.samplers.device.samplingresults.systemresult import SystemResult
from core.sampling.samplers.node.results.syncstatus import ClientSyncingStatus, NodeSyncingStatus


@dataclass
class NodeSyncingResult:
    exec_cli_sync_status: ClientSyncingStatus
    consensus_cli_sync_status: ClientSyncingStatus
    node_sync_status: NodeSyncingStatus

    def represents_active_node(self) -> bool:
        return self.node_sync_status != NodeSyncingStatus.INACTIVE


@dataclass
class NodeSamplingResult:
    node_name: str

    # This list is ordered in a canonical way for dual-device setup:
    # 1. Execution device
    # 2. Consensus Device
    device_system_samples: List[SystemResult | None]

    sync_result: NodeSyncingResult

    sync_percent: float | None
    last_block_num: int | None

    def execution_dev_system_sample(self) -> SystemResult | None:
        assert self.num_system_samples() >= 1
        return self.device_system_samples[0]

    def consensus_dev_system_sample(self) -> SystemResult | None:
        assert self.num_system_samples() >= 1

        if self.num_system_samples() > 1:
            assert self.num_system_samples() == 2
            return self.device_system_samples[1]
        else:
            return self.device_system_samples[0]

    def exec_cli_sync_status(self) -> ClientSyncingStatus:
        return self.sync_result.exec_cli_sync_status

    def consensus_cli_sync_status(self) -> ClientSyncingStatus:
        return self.sync_result.consensus_cli_sync_status

    def node_sync_status(self) -> NodeSyncingStatus:
        return self.sync_result.node_sync_status

    def system_sample(self, idx: int) -> SystemResult | None:
        return self.device_system_samples[idx]

    def system_samples(self) -> List[SystemResult | None]:
        return self.device_system_samples

    def num_system_samples(self) -> int:
        return len(self.device_system_samples)

    def represents_active_node(self) -> bool:
        res = self.sync_result.represents_active_node()
        if res:
            assert self.sync_percent is not None and self.last_block_num is not None

        return res
