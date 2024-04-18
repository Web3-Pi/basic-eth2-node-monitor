from dataclasses import dataclass


@dataclass
class ExecutionSyncResult:
    synced: bool
    last_block: int
    sync_percent: float

    def __str__(self):
        return f"{self.__class__.__name__}: synced {self.synced}, last_block {self.last_block}"
