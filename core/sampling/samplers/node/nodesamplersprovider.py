from core.sampling.samplers.device.devicesamplersprovider import DeviceSamplersProvider
from core.sampling.samplers.node.nodesampler import NodeSampler


class NodeSamplersProvider:

    FACTORY = DeviceSamplersProvider

    @classmethod
    def dual_device_lighthouse(cls, node_name: str, endpoint_gth: str, gth_port: int, gth_sys_port: int,
                               endpoint_lhs: str, lhs_port: int, lhs_sys_port: int) -> NodeSampler:
        dev_exec = DeviceSamplersProvider.geth_exec_device_sampler(endpoint_gth, gth_port, gth_sys_port)
        dev_consensus = DeviceSamplersProvider.lighthouse_consensus_device_sampler(endpoint_lhs, lhs_port, lhs_sys_port)

        return NodeSampler(node_name, dev_exec, dev_consensus)

    @classmethod
    def dual_device_generic_consensus(cls, node_name: str, endpoint_gth: str, gth_port: int, gth_sys_port: int,
                                      endpoint_nbs: str, nbs_port: int, nbs_sys_port: int) -> NodeSampler:
        dev_exec = DeviceSamplersProvider.geth_exec_device_sampler(endpoint_gth, gth_port, gth_sys_port)
        dev_consensus = DeviceSamplersProvider.generic_consensus_device_sampler(endpoint_nbs, nbs_port, nbs_sys_port)

        return NodeSampler(node_name, dev_exec, dev_consensus)

    @classmethod
    def single_device_lighthouse(cls, node_name: str, endpoint: str,
                                 gth_port: int, lhs_port: int, sys_port: int) -> NodeSampler:

        dev = DeviceSamplersProvider.lighthouse_full_node_device_sampler(endpoint, gth_port, lhs_port, sys_port)

        return NodeSampler(node_name, dev)

    @classmethod
    def single_device_generic_consensus(cls, node_name: str, endpoint: str,
                                        gth_port: int, nbs_port: int, sys_port: int) -> NodeSampler:
        dev = DeviceSamplersProvider.generic_consensus_full_node_device_sampler(endpoint, gth_port, nbs_port, sys_port)

        return NodeSampler(node_name, dev)
