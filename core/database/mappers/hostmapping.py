from core.sampling.samplers.node.results.nodesamplingresult import NodeSamplingResult


class HostTagMapper:

    @classmethod
    def node_name_wih_type_suffix(cls, sample: NodeSamplingResult) -> str:
        if sample.num_system_samples() > 1:
            return f"{sample.node_name}_d"
        else:
            return f"{sample.node_name}_s"

    @classmethod
    def exec_host_tag(cls, node_name: str, device_name: str) -> str:
        return f"{node_name}_exec"

    @classmethod
    def consensus_host_tag(cls, node_name: str, device_name: str) -> str:
        return f"{node_name}_consensus"

    @classmethod
    def host_tag_full(cls, sample: NodeSamplingResult) -> str:
        assert sample.num_system_samples() == 1

        return sample.node_name if sample.system_sample(0) is not None else ""

    @classmethod
    def host_tag_exec(cls, sample: NodeSamplingResult) -> str:
        assert sample.num_system_samples() == 2
        sys_sample = sample.system_sample(0)

        return cls.exec_host_tag(sample.node_name, sys_sample.host_name) if sys_sample is not None else ""

    @classmethod
    def host_tag_consensus(cls, sample: NodeSamplingResult) -> str:
        assert sample.num_system_samples() == 2
        sys_sample = sample.system_sample(1)

        return cls.consensus_host_tag(sample.node_name, sys_sample.host_name) if sys_sample is not None else ""
