from typing import Dict


class LighthouseEth1SyncingResult:

    def __init__(self, data_dict: Dict):
        self.sync_status: Dict = data_dict

    def is_synced(self) -> bool:
        return self.sync_status["eth1_node_sync_status_percentage"] == 100

    def get_head_block_number(self) -> int:
        return self.sync_status["head_block_number"]

    def get_head_block_timestamp(self) -> int:
        return self.sync_status["head_block_timestamp"]

    def get_latest_cached_block_number(self) -> int:
        return self.sync_status["latest_cached_block_number"]

    def get_latest_cached_block_timestamp(self) -> int:
        return self.sync_status["latest_cached_block_timestamp"]

    def get_voting_target_timestamp(self) -> int:
        return self.sync_status["voting_target_timestamp"]

    def get_eth1_node_sync_status_percentage(self) -> float:
        return self.sync_status["eth1_node_sync_status_percentage"]

    def get_lighthouse_is_cached_and_ready(self) -> bool:
        return self.sync_status["lighthouse_is_cached_and_ready"]

    def __str__(self):
        return f'LighthouseEth1SyncingResult: {self.sync_status}'


class LighthouseSyncingResult:

    def __init__(self, data: Dict | str) -> None:
        self.sync_status = data
        self.is_synced_ = isinstance(data, str) and data == "Synced"

    def is_synced(self) -> bool:
        return self.is_synced_

    def get_start_lot(self) -> int:
        assert not self.is_synced()
        return int(self.sync_status["start_slot"])

    def get_target_slot(self) -> int:
        assert not self.is_synced()
        return int(self.sync_status["target_slot"])

    def __str__(self):
        if self.is_synced():
            return 'LighthouseSyncingResult: "Synced"'
        else:
            return f'LighthouseSyncingResult: {self.sync_status}'
