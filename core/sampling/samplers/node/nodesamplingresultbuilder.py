from typing import List, Any

from core.sampling.samplers.device.devicesamplers.consensusdevicesampler import ConsensusDeviceSample
from core.sampling.samplers.device.devicesamplers.devicesample import DeviceSample
from core.sampling.samplers.device.devicesamplers.executiondevicesampler import ExecutionDeviceSample
from core.sampling.samplers.device.devicesamplers.fullnodedevicesampler import FullDeviceSample
from core.sampling.samplers.device.samplingresults.consensussyncresult import ConsensusSyncResult
from core.sampling.samplers.device.samplingresults.executionsyncresult import ExecutionSyncResult
from core.sampling.samplers.device.samplingresults.systemresult import SystemResult
from core.sampling.samplers.node.results.nodesamplingresult import NodeSamplingResult, NodeSyncingStatus, NodeSyncingResult
from core.sampling.samplers.node.results.syncstatusgetters import dual_dev_sync_status, full_dev_sync_status


class NodeSamplingResultBuilder:

    @classmethod
    def system_samples(cls, *device_samples: DeviceSample) -> List[SystemResult]:
        return [dev.system_sample for dev in device_samples]

    @classmethod
    def canonical_dev_samples(cls, dev0_sample: DeviceSample,
                              dev1_sample: DeviceSample) -> [ExecutionDeviceSample, ConsensusDeviceSample]:
        if isinstance(dev0_sample, ExecutionDeviceSample):
            exec_dev_sample = dev0_sample
            consensus_dev_sample = dev1_sample
        else:
            exec_dev_sample = dev1_sample
            consensus_dev_sample = dev0_sample

        assert isinstance(exec_dev_sample, ExecutionDeviceSample)
        assert isinstance(consensus_dev_sample, ConsensusDeviceSample)

        return exec_dev_sample, consensus_dev_sample

    @classmethod
    def sync_details(cls, ns: NodeSyncingStatus, es: ExecutionSyncResult, cs: ConsensusSyncResult) -> [Any, Any]:
        if ns == NodeSyncingStatus.INACTIVE:
            sync_percent = None
            last_block_num = None
        else:
            sync_percent = min(cs.sync_percent, es.sync_percent)
            last_block_num = es.last_block

        return sync_percent, last_block_num

    @classmethod
    def from_dual(cls, node_name: str, dev0_sample: DeviceSample, dev1_sample: DeviceSample) -> NodeSamplingResult:
        exec_dev_sample, cons_dev_sample = cls.canonical_dev_samples(dev0_sample, dev1_sample)

        exec_status, cons_status, node_status = dual_dev_sync_status(exec_dev_sample, cons_dev_sample)

        return NodeSamplingResult(
            node_name,
            cls.system_samples(exec_dev_sample, cons_dev_sample),
            NodeSyncingResult(exec_status, cons_status, node_status),
            *cls.sync_details(node_status, exec_dev_sample.get_client_sample(), cons_dev_sample.get_client_sample())
        )

    @classmethod
    def from_single(cls, node_name: str, dev_sample: DeviceSample) -> NodeSamplingResult:
        assert isinstance(dev_sample, FullDeviceSample)

        exec_status, cons_status, node_status = full_dev_sync_status(dev_sample)

        return NodeSamplingResult(
            node_name,
            cls.system_samples(dev_sample),
            NodeSyncingResult(exec_status, cons_status, node_status),
            *cls.sync_details(node_status, *dev_sample.get_client_sample())
        )

    @classmethod
    def create(cls, node_name: str, *args: DeviceSample) -> NodeSamplingResult:
        if len(args) == 1:
            return cls.from_single(node_name, args[0])
        else:
            assert len(args) == 2
            return cls.from_dual(node_name, *args)
