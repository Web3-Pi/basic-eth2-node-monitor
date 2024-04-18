from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.database.defaults.defaults import DefaultEntryFields


@dataclass
class InfluxDBEntry:
    measurement_name: str
    tag_name: str
    tag: str
    field: str
    value: Any

    @classmethod
    def default(cls, measurement_name: str, host: str, field: str, value: Any) -> InfluxDBEntry:
        return InfluxDBEntry(measurement_name, DefaultEntryFields.HOST_NAME, host, field, value)


class InfluxDBEntryBuilder:

    def __init__(self, node_name: str) -> None:
        self.node_name = node_name

    def build(self, measurement_name: str, field: str, value: Any) -> InfluxDBEntry:
        return InfluxDBEntry.default(measurement_name, self.node_name, field, value)
