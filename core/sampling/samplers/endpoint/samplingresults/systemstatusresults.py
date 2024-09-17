from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from util.strconverions import h


@dataclass
class SystemStatusResult:

    host_name: str = ""

    num_cores: int = -1
    cpu_percent: float = 0.0

    mem_total: int = -1
    mem_used: int = -1
    mem_free: int = -1
    mem_percent: float = 0.0

    swap_total: int = -1
    swap_used: int = -1
    swap_free: int = -1
    swap_percent: float = 0.0

    disk_used: int = -1

    cpu_temp: float = 0.0

    @classmethod
    def from_dict(cls, d: Dict) -> SystemStatusResult:
        return SystemStatusResult(d["host_name"],
                                  d["num_cores"], d["cpu_percent"],
                                  d["mem_total"], d["mem_used"], d["mem_free"], d["mem_percent"],
                                  d["swap_total"], d["swap_used"], d["swap_free"], d["swap_percent"],
                                  d["disk_used"], d.get("cpu_temp", 0.0))

    def __str__(self):
        hmt = h(self.mem_total)
        hmu = h(self.mem_used)
        hmf = h(self.mem_free)

        hst = h(self.swap_total)
        hsu = h(self.swap_used)
        hsf = h(self.swap_free)

        hdu = h(self.disk_used)

        m = f"SystemStatusResultWrapper: '{self.host_name}' " \
            f"CPU: cores {self.num_cores}, load: {self.cpu_percent}%, temp: {self.cpu_temp} C," \
            f"MEM: total {hmt}, used {hmu}, free {hmf}, percent {self.mem_percent}%, " \
            f"SWAP: total {hst}, used {hsu}, free {hsf} percent {self.swap_percent}%, " \
            f"DISK: used {hdu}"

        return m
