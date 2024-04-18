from core.sampling.samplers.device.devicesamplers.consensusdevicesampler import ConsensusDeviceSampler
from core.sampling.samplers.device.devicesamplers.executiondevicesampler import ExecutionDeviceSampler
from core.sampling.samplers.device.devicesamplers.fullnodedevicesampler import FullNodeDeviceSampler
from core.sampling.samplers.device.adapters.gethexecution import SamplerAdapterGethExecution
from core.sampling.samplers.device.adapters.lighthouseconsensus import SamplerAdapterLighthouseConsensus
from core.sampling.samplers.device.adapters.genericconsensus import SamplerAdapterGenericConsensus
from core.sampling.samplers.device.adapters.systemcompletesystemsimple import \
    SamplerAdapterSystemCompleteSystemSimple
from core.sampling.samplers.endpoint.endpointsamplersprovider import EndpointSamplersProvider
from util.strconverions import as_http_addr, as_websocket_addr


class AdaptersProvider:
    @staticmethod
    def sys_sampler_adapter(endpoint: str, port: int) -> SamplerAdapterSystemCompleteSystemSimple:
        sampler = EndpointSamplersProvider.system_endpoint_sampler(as_http_addr(endpoint, port))
        return SamplerAdapterSystemCompleteSystemSimple(sampler)

    @staticmethod
    def geth_sampler_adapter(endpoint: str, port: int) -> SamplerAdapterGethExecution:
        sampler = EndpointSamplersProvider.geth_endpoint_sampler(as_websocket_addr(endpoint, port))
        return SamplerAdapterGethExecution(sampler)

    @staticmethod
    def lighthouse_sampler_adapter(endpoint: str, port: int) -> SamplerAdapterLighthouseConsensus:
        sampler = EndpointSamplersProvider.lighthouse_endpoint_sampler(as_http_addr(endpoint, port))
        return SamplerAdapterLighthouseConsensus(sampler)

    @staticmethod
    def generic_consensus_sampler_adapter(endpoint: str, port: int) -> SamplerAdapterGenericConsensus:
        sampler = EndpointSamplersProvider.generic_consensus_endpoint_sampler(as_http_addr(endpoint, port))
        return SamplerAdapterGenericConsensus(sampler)


class DeviceSamplersProvider:

    @classmethod
    def geth_exec_device_sampler(cls, endpoint: str, gth_port: int, sys_port: int) -> ExecutionDeviceSampler:
        return ExecutionDeviceSampler(endpoint,
                                      AdaptersProvider.geth_sampler_adapter(endpoint, gth_port),
                                      AdaptersProvider.sys_sampler_adapter(endpoint, sys_port))

    @classmethod
    def lighthouse_consensus_device_sampler(cls, endpoint: str, lhs_port: int, sys_port: int) -> ConsensusDeviceSampler:
        return ConsensusDeviceSampler(endpoint,
                                      AdaptersProvider.lighthouse_sampler_adapter(endpoint, lhs_port),
                                      AdaptersProvider.sys_sampler_adapter(endpoint, sys_port))

    @classmethod
    def generic_consensus_device_sampler(cls, endpoint: str, cns_port: int, sys_port: int) -> ConsensusDeviceSampler:
        return ConsensusDeviceSampler(endpoint,
                                      AdaptersProvider.generic_consensus_sampler_adapter(endpoint, cns_port),
                                      AdaptersProvider.sys_sampler_adapter(endpoint, sys_port))

    @classmethod
    def lighthouse_full_node_device_sampler(cls, endpoint: str,
                                            gth_port: int, lhs_port: int, sys_port: int) -> FullNodeDeviceSampler:
        return FullNodeDeviceSampler(endpoint,
                                     AdaptersProvider.geth_sampler_adapter(endpoint, gth_port),
                                     AdaptersProvider.lighthouse_sampler_adapter(endpoint, lhs_port),
                                     AdaptersProvider.sys_sampler_adapter(endpoint, sys_port))

    @classmethod
    def generic_consensus_full_node_device_sampler(cls, endpoint: str,
                                                   gt_port: int, cns_port: int, sys_port: int) -> FullNodeDeviceSampler:
        return FullNodeDeviceSampler(endpoint,
                                     AdaptersProvider.geth_sampler_adapter(endpoint, gt_port),
                                     AdaptersProvider.generic_consensus_sampler_adapter(endpoint, cns_port),
                                     AdaptersProvider.sys_sampler_adapter(endpoint, sys_port))
