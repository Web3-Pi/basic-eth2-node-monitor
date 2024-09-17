from typing import List

from core.database.mappers.hostmapping import HostTagMapper
from core.sampling.samplers.device.samplingresults.systemresult import SystemResult
from core.sampling.samplers.node.results.nodesamplingresult import NodeSamplingResult
from core.database.mappers.customentriesmapper import CustomEntriesMapper
from core.database.defaults.mappers import client_sync_status_to_float, node_sync_status_to_float
from core.database.influxdb.influxdbentry import InfluxDBEntry


class NodeResultMapper:

    def __init__(self) -> None:
        self.last_block_cache = {}
        self.mapper: CustomEntriesMapper | None = None

    def _status_entries(self, sample: NodeSamplingResult) -> List[InfluxDBEntry]:
        return self.mapper.sync_status_entries(
            client_sync_status_to_float(sample.exec_cli_sync_status()),
            client_sync_status_to_float(sample.consensus_cli_sync_status()),
            node_sync_status_to_float(sample.node_sync_status())
        )

    @classmethod
    def _map_system_entry(cls, host_name_tag: str, s: SystemResult | None) -> List[InfluxDBEntry]:
        res = []
        if s is not None:
            res = CustomEntriesMapper.system_stats_entries(host_name_tag,
                                                           s.num_cores, s.cpu_percent,
                                                           s.mem_used, s.swap_used, s.disk_used,
                                                           s.cpu_temp)

        return res

    @classmethod
    def _system_entries(cls, sample: NodeSamplingResult) -> List[InfluxDBEntry]:
        assert 1 <= sample.num_system_samples() <= 2

        res = []
        if sample.num_system_samples() == 1:
            res += cls._map_system_entry(HostTagMapper.host_tag_full(sample), sample.system_sample(0))
        else:
            res += cls._map_system_entry(HostTagMapper.host_tag_exec(sample), sample.execution_dev_system_sample())
            res += cls._map_system_entry(HostTagMapper.host_tag_consensus(sample), sample.consensus_dev_system_sample())

        return res

    def _bchain_entries(self, sample: NodeSamplingResult) -> List[InfluxDBEntry]:
        if sample.represents_active_node():
            res = self.mapper.sync_percent_entries(sample.sync_percent)
            self.last_block_cache[sample.node_name] = sample.last_block_num
        else:
            res = self.mapper.sync_percent_entries(0.0)

        last_block_num = self.last_block_cache.get(sample.node_name)
        if last_block_num:
            res += self.mapper.last_block_entries(last_block_num)

        return res

    def to_db_entries(self, sample: NodeSamplingResult) -> List[InfluxDBEntry]:
        sample.node_name = HostTagMapper.node_name_wih_type_suffix(sample)
        self.mapper = CustomEntriesMapper(sample.node_name)

        res = []
        res += self._status_entries(sample)
        res += self._system_entries(sample)
        res += self._bchain_entries(sample)

        return res
