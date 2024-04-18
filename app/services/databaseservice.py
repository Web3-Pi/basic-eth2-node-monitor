from __future__ import annotations

from app.appdescr.components.databasedescr import DatabaseDescr
from core.sampling.samplers.node.results.nodesamplingresult import NodeSamplingResult
from core.database.influxdb.influxdbwriter import InfluxDBWriter
from core.database.mappers.noderesultmapper import NodeResultMapper
from util.strconverions import as_http_addr


class DatabaseService:

    def __init__(self, db_writer: InfluxDBWriter) -> None:
        self.db_writer = db_writer
        self.converter = NodeResultMapper()

    def start(self):
        pass
        # print(f"DatabaseService: Starting database service, connected to remote endpoint {self.db_writer.db_url}")

    def write_sample(self, node_sample: NodeSamplingResult) -> int:
        entries = self.converter.to_db_entries(node_sample)
        self.db_writer.write_batch(entries)

        return len(entries)

    def shutdown(self):
        print("DatabaseService: shutting down")
        self.db_writer.close()

    @classmethod
    def create(cls, descr: DatabaseDescr) -> DatabaseService | None:
        db = InfluxDBWriter.create(as_http_addr(descr.host, descr.port), descr.user, descr.password, descr.database)

        if db is not None:
            return DatabaseService(db)

        return None
