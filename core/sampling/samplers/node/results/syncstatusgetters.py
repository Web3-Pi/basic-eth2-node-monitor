from core.sampling.samplers.device.devicesamplers.consensusdevicesampler import ConsensusDeviceSample
from core.sampling.samplers.device.devicesamplers.executiondevicesampler import ExecutionDeviceSample
from core.sampling.samplers.device.devicesamplers.fullnodedevicesampler import FullDeviceSample
from core.sampling.samplers.node.results.syncstatus import ClientSyncingStatus
from core.sampling.samplers.node.results.nodesamplingresult import NodeSyncingStatus


def sync_status_from_dual_cli(main_cli_sample, second_cli_sample) -> ClientSyncingStatus:
    if main_cli_sample.represents_active_device():
        if second_cli_sample.represents_active_device():
            main_sample = main_cli_sample.get_client_sample()
            return ClientSyncingStatus.SYNCED if main_sample.synced else ClientSyncingStatus.SYNCING
        else:
            return ClientSyncingStatus.WAITING
    else:
        return ClientSyncingStatus.INACTIVE


def node_sync_status(exec_cli_sync_status: ClientSyncingStatus,
                     consensus_cli_sync_status: ClientSyncingStatus) -> NodeSyncingStatus:

    inactive_set = {ClientSyncingStatus.INACTIVE, ClientSyncingStatus.WAITING}
    syncing_status = ClientSyncingStatus.SYNCING

    if exec_cli_sync_status in inactive_set or consensus_cli_sync_status in inactive_set:
        return NodeSyncingStatus.INACTIVE
    elif exec_cli_sync_status == syncing_status or consensus_cli_sync_status == syncing_status:
        return NodeSyncingStatus.SYNCING
    else:
        return NodeSyncingStatus.SYNCED


def dual_dev_sync_status(eds: ExecutionDeviceSample,
                         cds: ConsensusDeviceSample) -> [ClientSyncingStatus, ClientSyncingStatus, NodeSyncingStatus]:

    exec_status = sync_status_from_dual_cli(eds, cds)
    cons_status = sync_status_from_dual_cli(cds, eds)

    return exec_status, cons_status, node_sync_status(exec_status, cons_status)


def full_dev_sync_status(dev_sample: FullDeviceSample) -> [ClientSyncingStatus, ClientSyncingStatus, NodeSyncingStatus]:
    exec_status = ClientSyncingStatus.INACTIVE
    cons_status = ClientSyncingStatus.INACTIVE

    if dev_sample.represents_active_device():
        exec_status = ClientSyncingStatus.SYNCED if dev_sample.execution_sample.synced else ClientSyncingStatus.SYNCING
        cons_status = ClientSyncingStatus.SYNCED if dev_sample.consensus_sample.synced else ClientSyncingStatus.SYNCING
    elif dev_sample.system_sample is not None:
        if dev_sample.execution_sample is not None:
            assert dev_sample.consensus_sample is None
            exec_status = ClientSyncingStatus.WAITING
        elif dev_sample.consensus_sample is not None:
            cons_status = ClientSyncingStatus.WAITING

    return exec_status, cons_status, node_sync_status(exec_status, cons_status)
