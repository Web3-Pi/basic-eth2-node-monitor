from typing import List

from core.sampling.samplingunit.descriptors.devicedescriptors import SingleClientDeviceDesc, FullDeviceDesc
from core.sampling.samplingunit.descriptors.supportedclients import SupportedClients


class NodeDescriptor:

    def __init__(self, name: str, *device_descriptors) -> None:
        self.name = name

        assert len(device_descriptors) == 1 or len(device_descriptors) == 2

        if len(device_descriptors) == 2:
            assert all([isinstance(desc, SingleClientDeviceDesc) for desc in device_descriptors])
        else:
            assert isinstance(device_descriptors[0], FullDeviceDesc)

        self.device_descriptors: List = list(device_descriptors)

    def is_dual_device(self) -> bool:
        return len(self.device_descriptors) == 2

    def get_execution_device_descriptor(self) -> SingleClientDeviceDesc:
        assert self.is_dual_device()

        res = list(filter(lambda descr: descr.supported_client == SupportedClients.GETH, self.device_descriptors))
        assert len(res) == 1

        return res[0]

    def get_consensus_device_descriptor(self) -> SingleClientDeviceDesc:
        assert self.is_dual_device()

        res = list(filter(lambda descr: descr.supported_client != SupportedClients.GETH, self.device_descriptors))
        assert len(res) == 1 and res[0].supported_client == SupportedClients.LIGHTHOUSE or \
               res[0].supported_client == SupportedClients.GENERIC_CONSENSUS

        return res[0]

    def get_full_device_descriptor(self) -> FullDeviceDesc:
        assert not self.is_dual_device()
        assert isinstance(self.device_descriptors[0], FullDeviceDesc)

        return self.device_descriptors[0]

    def __str__(self):
        res = f"{self.__class__.__name__}(name='{self.name}', device_descriptors="
        if len(self.device_descriptors) == 1:
            res += f"[{self.device_descriptors[0]}])"
        else:
            res += f"[{self.device_descriptors[0]}, {self.device_descriptors[1]}])"

        return res
