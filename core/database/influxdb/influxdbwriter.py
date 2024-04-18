from __future__ import annotations

import datetime
import json
from typing import List

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import WriteOptions
from influxdb_client.rest import ApiException

from config.conf import DEFAULT_INFLUXDB_FLUSH_INTERVAL, DEFAULT_INFLUXDB_BATCH_SIZE
from core.database.influxdb.influxdbentry import InfluxDBEntry


class InfluxDBWriter:

    RETENTION_POLICY = "autogen"

    def __init__(self, db_url: str, client: InfluxDBClient, bucket: str) -> None:
        self.db_url = db_url

        self.client = client
        self.bucket = bucket

        wo = WriteOptions(
            batch_size=DEFAULT_INFLUXDB_BATCH_SIZE,
            flush_interval=DEFAULT_INFLUXDB_FLUSH_INTERVAL
        )

        self.api_writer = self.client.write_api(write_options=wo)
        self.num_written_data_points = 0
        self.start_time = datetime.datetime.now()

    def get_db_url(self) -> str:
        return self.db_url

    @staticmethod
    def to_point(entry: InfluxDBEntry) -> Point:
        return Point(entry.measurement_name).tag(entry.tag_name, entry.tag).field(entry.field, entry.value)

    def _write_point(self, point: Point) -> None:
        self.num_written_data_points += 1
        self.api_writer.write(bucket=self.bucket, record=point)

    def write(self, entry: InfluxDBEntry) -> None:
        self._write_point(self.to_point(entry))

    def write_batch(self, entries: List[InfluxDBEntry]) -> None:
        for entry in entries:
            self.write(entry)

    def close(self):
        self.api_writer.close()
        self.client.close()

    @classmethod
    def create(cls, db_endpoint: str, username: str, passwd: str, database: str) -> InfluxDBWriter | None:
        client = InfluxDBClient(url=db_endpoint, token=f'{username}:{passwd}', org='-')
        bucket = f'{database}/{cls.RETENTION_POLICY}'

        if not client.ping():
            print(f"InfluxDB: could not connect to remote host: {db_endpoint} "
                  f"with provided credentials, user: {username}, pass: {passwd}")
            return None

        try:
            client.query_api().query(f'from(bucket:"{bucket}") |> range(start: -1ms)')
        except ApiException as ex:
            print(f"InfluxDB: Database '{database}' not present or accessible.\n"
                  f"InfluxDB: Error message from the database server: '{json.loads(ex.body.decode('utf-8'))['error']}'")

            client.close()

            return None

        return InfluxDBWriter(db_endpoint, client, bucket)
