from dataclasses import dataclass


@dataclass
class ConsensusSyncResult:
    synced: bool
    sync_percent: float

    def __str__(self):
        return f"{self.__class__.__name__}: synced {self.synced}, sync_percent {self.sync_percent}"
