from typing import List

from core.database.defaults.defaults import DefaultEntryFields
from core.database.defaults.mappers import sync_percent_to_sync_percent_4
from core.database.influxdb.influxdbentry import InfluxDBEntry, InfluxDBEntryBuilder


class CustomEntriesMapper:
    DEF = DefaultEntryFields

    def __init__(self, node_name: str) -> None:
        self.entry_builder = InfluxDBEntryBuilder(node_name)

    @classmethod
    def system_stats_entries(cls, host_name: str,
                             num_cores: int, cpu_percent: float,
                             mem_used: int, swap_used: int, disk_used: int) -> List[InfluxDBEntry]:
        return [InfluxDBEntry.default(cls.DEF.CPU, host_name, cls.DEF.USED_PERCENT, num_cores * cpu_percent),
                InfluxDBEntry.default(cls.DEF.MEM, host_name, cls.DEF.USED_BYTES, mem_used),
                InfluxDBEntry.default(cls.DEF.SWAP, host_name, cls.DEF.USED_BYTES, swap_used),
                InfluxDBEntry.default(cls.DEF.DISK, host_name, cls.DEF.USED_BYTES, disk_used)]

    def sync_percent_entries_4(self, p0: float, p1: float, p2: float, p3: float) -> List[InfluxDBEntry]:
        return [self.entry_builder.build(self.DEF.CHAIN, self.DEF.SYNC_PART_PERC_0, p0),
                self.entry_builder.build(self.DEF.CHAIN, self.DEF.SYNC_PART_PERC_1, p1),
                self.entry_builder.build(self.DEF.CHAIN, self.DEF.SYNC_PART_PERC_2, p2),
                self.entry_builder.build(self.DEF.CHAIN, self.DEF.SYNC_PART_PERC_3, p3)]

    def sync_percent_entries(self, percent: float) -> List[InfluxDBEntry]:
        return self.sync_percent_entries_4(*sync_percent_to_sync_percent_4(percent))

    def last_block_entries(self, block_num: int) -> List[InfluxDBEntry]:
        return [self.entry_builder.build(self.DEF.CHAIN, self.DEF.LAST_BLOCK, block_num)]

    def sync_status_entries(self, status_exec: float,
                            status_consensus: float,
                            status_node: float) -> List[InfluxDBEntry]:
        return [self.entry_builder.build(self.DEF.STATUS_EXEC, self.DEF.ACTIVE_PERCENT, status_exec),
                self.entry_builder.build(self.DEF.STATUS_CONSENSUS, self.DEF.ACTIVE_PERCENT, status_consensus),
                self.entry_builder.build(self.DEF.STATUS_NODE, self.DEF.ACTIVE_PERCENT, status_node)]
