from dataclasses import dataclass


@dataclass
class SystemResult:

    host_name: str

    num_cores: int
    cpu_percent: float

    mem_used: int
    swap_used: int
    disk_used: int

    cpu_temp: float

    def __str__(self):
        return f"{self.__class__.__name__}: host_name {self.host_name}, num_cores {self.num_cores}, " \
               f"cpu_percent {self.cpu_percent}, mem_used {self.mem_used}, swap_used {self.swap_used}, " \
               f"disk_used {self.disk_used}, cpu_temp {self.cpu_temp}"
