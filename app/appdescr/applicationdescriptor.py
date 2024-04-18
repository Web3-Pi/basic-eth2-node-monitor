from dataclasses import dataclass
from typing import List

from app.appdescr.components.databasedescr import DatabaseDescr
from app.appdescr.components.waitdelaydescr import WaitDelayDescr
from core.sampling.samplingunit.descriptors.nodedescriptor import NodeDescriptor


@dataclass
class ApplicationDescriptor:
    nodes: List[NodeDescriptor]
    database: DatabaseDescr
    wait_delay: WaitDelayDescr

    def num_nodes(self) -> int:
        return len(self.all_nodes())

    def num_dual_device_nodes(self) -> int:
        return len([x for x in self.nodes if x.is_dual_device()])

    def num_single_device_nodes(self) -> int:
        return self.num_nodes() - self.num_dual_device_nodes()

    def all_nodes(self) -> List[NodeDescriptor]:
        return self.nodes

    def dual_device_nodes(self) -> List[NodeDescriptor]:
        return [x for x in self.nodes if x.is_dual_device()]

    def single_device_nodes(self) -> List[NodeDescriptor]:
        return [x for x in self.nodes if not x.is_dual_device()]

    def __str__(self):
        res = f'{self.__class__.__name__}(nodes=['

        for i in range(len(self.nodes) - 1):
            res += f"{self.nodes[i]}, "

        if len(self.nodes) > 0:
            res += f"{self.nodes[-1]}"

        res += "], "
        res += f'database={self.database}, wait_delay={self.wait_delay})'

        return res
