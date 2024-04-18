from dataclasses import dataclass

from core.sampling.samplingunit.descriptors.supportedclients import SupportedClients


@dataclass
class SingleClientDeviceDesc:
    host: str

    client_port: int
    system_monitor_port: int

    supported_client: SupportedClients


@dataclass
class FullDeviceDesc:
    host: str

    exec_client_port: int
    consensus_client_port: int
    system_monitor_port: int

    consensus_client: SupportedClients
