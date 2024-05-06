import enum
from typing import Dict


class EthV1NodeHealthStatus(enum.Enum):
    SYNCED = 0
    SYNCING = 1


class EthV1NodeHealthResult:

    def __init__(self, status_code: int) -> None:
        if status_code == 200:
            self.status = EthV1NodeHealthStatus.SYNCED
        elif status_code == 206:
            self.status = EthV1NodeHealthStatus.SYNCING

    def get_status(self) -> EthV1NodeHealthStatus:
        return self.status

    def __str__(self):
        return f"EthV1NodeHealthResult: {self.status}"


class EthV1NodeSyncingResult:

    def __init__(self, result_dict: Dict):
        self.sync_status: Dict = result_dict

    def is_synced(self) -> bool:
        return not self.sync_status["is_syncing"] and int(self.sync_status["sync_distance"]) <= 1 \
            and not self.sync_status["el_offline"] and not self.sync_status["is_optimistic"]

    def get_sync_progress_percent(self) -> float:
        if self.is_synced():
            return 100.0

        head_slot = int(self.sync_status["head_slot"])
        sync_distance = int(self.sync_status["sync_distance"])

        if head_slot == 0:
            return 0.0

        return 100.0 * float(head_slot - sync_distance) / float(head_slot)

    def __str__(self):
        if self.is_synced():
            return f'EthV1NodeSyncingResult: "Synced: {self.get_sync_progress_percent()}%"'
        else:
            return f'EthV1NodeSyncingResult: {self.sync_status}: {self.get_sync_progress_percent()}%'
