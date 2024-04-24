from typing import Dict


class EthSyncingResult:

    def __init__(self, result_dict: Dict | None):
        self.sync_status: Dict | None = result_dict

    def is_synced(self) -> bool:
        return self.sync_status is None

    def get_starting_block(self) -> int:
        assert not self.is_synced()
        return int(self.sync_status["startingBlock"], 16)

    def get_current_block(self) -> int:
        assert not self.is_synced()
        return int(self.sync_status["currentBlock"], 16)

    def get_highest_block(self) -> int:
        assert not self.is_synced()
        return int(self.sync_status["highestBlock"], 16)

    def sync_percent(self) -> float:
        assert not self.is_synced()

        hb = self.get_highest_block()
        if hb == 0:
            return 0.0
        else:
            return 100.0 * float(self.get_current_block()) / float(hb)

    def __str__(self):
        if self.is_synced():
            return 'EthSyncingResult: "Synced"'
        else:
            return f'EthSyncingResult: {self.sync_status}'


class EthBlockNumberResult:

    def __init__(self, result_str: str) -> None:
        self.block_number: int = int(result_str, 16)

    def get_block_number(self):
        return self.block_number

    def __str__(self):
        return f"EthBlockNumberResult: {self.block_number}"
