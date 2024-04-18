from core.sampling.samplers.node.nodesampler import NodeSampler
from core.sampling.samplers.node.nodesamplersprovider import NodeSamplersProvider
from core.sampling.samplingunit.descriptors.devicedescriptors import SingleClientDeviceDesc, FullDeviceDesc
from core.sampling.samplingunit.descriptors.nodedescriptor import NodeDescriptor
from core.sampling.samplingunit.descriptors.supportedclients import SupportedClients


def create_dual_dev_node_sampler(node_name: str,
                                 exec_descr: SingleClientDeviceDesc,
                                 consensus_descr: SingleClientDeviceDesc) -> NodeSampler:
    if consensus_descr.supported_client == SupportedClients.LIGHTHOUSE:
        return NodeSamplersProvider.dual_device_lighthouse(
            node_name,
            exec_descr.host, exec_descr.client_port, exec_descr.system_monitor_port,
            consensus_descr.host, consensus_descr.client_port, consensus_descr.system_monitor_port
        )
    else:
        assert consensus_descr.supported_client == SupportedClients.GENERIC_CONSENSUS
        return NodeSamplersProvider.dual_device_generic_consensus(
            node_name,
            exec_descr.host, exec_descr.client_port, exec_descr.system_monitor_port,
            consensus_descr.host, consensus_descr.client_port, consensus_descr.system_monitor_port
        )


def create_single_dev_node_sampler(node_name: str,
                                   descr: FullDeviceDesc) -> NodeSampler:
    assert descr.consensus_client != SupportedClients.GETH

    if descr.consensus_client == SupportedClients.LIGHTHOUSE:
        return NodeSamplersProvider.single_device_lighthouse(
            node_name, descr.host, descr.exec_client_port, descr.consensus_client_port, descr.system_monitor_port
        )
    else:
        assert descr.consensus_client == SupportedClients.GENERIC_CONSENSUS
        return NodeSamplersProvider.single_device_generic_consensus(
            node_name, descr.host, descr.exec_client_port, descr.consensus_client_port, descr.system_monitor_port
        )


def node_sampler_from_descriptor(node_descriptor: NodeDescriptor) -> NodeSampler:
    assert isinstance(node_descriptor, NodeDescriptor)

    if node_descriptor.is_dual_device():
        return create_dual_dev_node_sampler(
            node_descriptor.name,
            node_descriptor.get_execution_device_descriptor(),
            node_descriptor.get_consensus_device_descriptor()
        )
    else:
        return create_single_dev_node_sampler(
            node_descriptor.name,
            node_descriptor.get_full_device_descriptor()
        )
